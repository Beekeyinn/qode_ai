from rest_framework.response import Response

from apps.core.pagination import SingleResultPagination


class ResponseMixin:

    def formatted_response(self, response: Response):
        return ResponseMixin.return_response(response)

    def return_response(self, response_data: dict, status: int = 200):
        response = Response(response_data, status=status)
        return self.formatted_response(response)

    @staticmethod
    def formatted_response(response: Response):
        is_success = response.status_code in [200, 201]
        is_validation_error = response.status_code == 400

        data = response.data
        errors = None
        message = None
        exception = None
        if data:
            errors = data.get("errors") or data.get("error") or data
            message = data.get("message", data.get("detail", None))
            exception = data.get("exception") if not is_success else None

        formatted_response = {
            "success": is_success,
            "status": response.status_code,
        }
        if is_success:
            formatted_response["data"] = data.get("data", data)
        else:
            formatted_response["message"] = message
            formatted_response["exception"] = exception
        if is_validation_error:
            formatted_response["errors"] = errors

        return Response(formatted_response, response.status_code)

    @staticmethod
    def return_response(response_data: dict, status: int = 200):
        response = Response(response_data, status=status)
        return ResponseMixin.formatted_response(response)


class SingleResultPaginationMixin:
    pagination_class = SingleResultPagination
