from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

ExceptionType = list[dict[str, str]]


class FineTuneJobException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidCredential(APIException):
    status_code = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
    default_detail = _("invalid password or username")
    default_code = "Invalid credentials"


def get_exception_traceback(ex: Exception) -> ExceptionType:
    traceback = ex.__traceback__
    traces = []
    while traceback is not None:
        trace = {
            "filename": traceback.tb_frame.f_code.co_filename,
            "name": traceback.tb_frame.f_code.co_name,
            "line_no": traceback.tb_lineno,
        }
        traces.append(trace)
        traceback = traceback.tb_next
    return traces
