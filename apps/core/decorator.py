import logging
import re as regex
from functools import wraps

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.transaction import atomic
from django.db.utils import IntegrityError
from django.http.response import Http404
from openai import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    BadRequestError,
    OpenAIError,
)
from rest_framework import status
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as response_generator

from .mixins import ResponseMixin

logger = logging.getLogger("django")
from apps.core.exceptions import InvalidCredential, get_exception_traceback


def api_exception_handler(function, use_automic=True, *args, **kwargs):
    @wraps(function)  # type: ignore
    def wrapper(*args, **kwargs):
        try:
            if use_automic:
                with atomic():
                    return function(*args, **kwargs)
            else:
                return function(*args, **kwargs)
        except Exception as exc:
            return custom_exception_handler(exc, function.__class__)

    return wrapper


def custom_exception_handler(exc, function_name):

    if isinstance(exc, IntegrityError):
        return ResponseMixin.formatted_response(
            Response(
                {
                    "detail": "Object already exists",
                    "exception": str(exc).split('"')[0],
                },
                status=status.HTTP_409_CONFLICT,
            )
        )

    if isinstance(exc, ObjectDoesNotExist):
        return ResponseMixin.formatted_response(
            Response(
                {"detail": "Detail Not Found", "exception": str(exc).split('"')[0]},
                status=status.HTTP_404_NOT_FOUND,
            )
        )

    elif isinstance(exc, PermissionDenied):
        logger.error("Multiple Object Returned ERROR", exc_info=exc)

        return ResponseMixin.formatted_response(
            Response(
                {"detail": exc.detail, "exception": str(exc).split('"')[0]},
                status=exc.status_code,
            )
        )

    elif isinstance(exc, MultipleObjectsReturned):

        return ResponseMixin.formatted_response(
            Response(
                {
                    "detail": "Multiple Value Returned",
                    "exception": str(exc).split('"')[0],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        )

    elif isinstance(exc, ValidationError):
        response = response_generator(exc, "")
        return ResponseMixin.formatted_response(response=response)

    elif isinstance(exc, BadRequestError):
        r_detail = regex.findall(r".*'message': '(.*)',.*", exc.message)
        if len(r_detail) > 0:
            detail = r_detail[0]
        else:
            detail = "We encountered an error while trying to generate your content, please try again."
        return ResponseMixin.formatted_response(
            Response(
                {
                    "detail": detail,
                    "exception": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        )

    elif isinstance(
        exc, (APIError, APIConnectionError, AuthenticationError, OpenAIError)
    ):
        logger.error("OPEN AI Error", exc_info=exc)
        return ResponseMixin.formatted_response(
            Response(
                {
                    "detail": "We encountered an error while trying to generate your content, please try again.",
                    "exception": str(exc).split('"')[0],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )

    elif isinstance(exc, InvalidCredential):
        return ResponseMixin.formatted_response(
            Response(
                {
                    "success": False,
                    "detail": exc.detail,
                    "data": [],
                    "exception": str(exc).split('"')[0],
                },
                status=exc.status_code,
            )
        )

    elif isinstance(exc, APIException):
        logger.error("API Error", exc_info=exc)

        return ResponseMixin.formatted_response(
            Response(
                {"detail": exc.detail, "exception": str(exc).split('"')[0]},
                status=exc.status_code,
            )
        )

    elif isinstance(exc, Http404):
        return ResponseMixin.formatted_response(
            Response(
                {"detail": "Detail Not Found", "exception": str(exc).split('"')[0]},
                status=status.HTTP_404_NOT_FOUND,
            )
        )

    else:
        logger.error("Exception Error", exc_info=exc)
        return ResponseMixin.formatted_response(
            Response(
                {
                    "detail": "Something Went Wrong. Please try again",
                    "exception": str(exc).split('"')[0] or "Unknown Error",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        )


def class_exception_handler_with_function(error_handler):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                error_message = f"An error occurred: {e}"
                error_handler(self, func.__name__, error_message)

        return wrapper

    return decorator
