import logging
import re as regex
from functools import wraps
from typing import cast

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.transaction import atomic
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

logger = logging.getLogger("decorator")


def api_exception_handler(function, use_automic=True, *args, **kwargs):
    @wraps(function)  # type: ignore
    def wrapper(*args, **kwargs):
        try:
            if use_automic:
                with atomic():
                    return function(*args, **kwargs)
            else:
                return function(*args, **kwargs)
        except ObjectDoesNotExist as odn_err:
            logger.error("Object Not Found Error", exc_info=odn_err)
            return Response(
                {"detail": "Detail Not Found", "exception": odn_err},
                status=status.HTTP_404_NOT_FOUND,
            )
        except PermissionDenied as pd:
            logger.error("Multiple Object Returned ERROR", exc_info=pd)

            return Response(
                {"detail": pd.detail, "exception": str(pd)},
                status=pd.status_code,
            )
        except MultipleObjectsReturned as mor_err:
            logger.error("Multiple Object Returned ERROR", exc_info=mor_err)

            return Response(
                {"detail": "Multiple Value Returned", "exception": mor_err},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError as validation_err:
            logger.error("Validation Error", exc_info=validation_err)

            response = response_generator(validation_err, "")
            return response

        except BadRequestError as bre:
            logger.error("OPEN AI Error", exc_info=bre)
            print("error", type(bre.message))
            rdetail = regex.findall(r".*'message': '(.*)',.*", bre.message)
            if len(rdetail) > 0:
                detail = rdetail[0]
            else:
                detail = "We encountered an error while trying to generate your content, please try again."
            return Response(
                {
                    "detail": detail,
                    "exception": str(bre),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (
            APIError,
            APIConnectionError,
            AuthenticationError,
            OpenAIError,
        ) as open_ai_err:
            logger.error("OPEN AI Error", exc_info=open_ai_err)
            return Response(
                {
                    "detail": "We encountered an error while trying to generate your content, please try again.",
                    "exception": str(open_ai_err),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except APIException as ae:
            logger.error("API Error", exc_info=ae)

            return Response(
                {"detail": ae.detail, "exception": str(ae)},
                status=ae.status_code,
            )

        except Exception as exc:
            logger.error("Exception Error", exc_info=exc)
            return Response(
                {"detail": "Internal Server Error", "exception": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
