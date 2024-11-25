from django.shortcuts import render


def page_not_found_error(request, exception):
    context = {}
    response = render(request, "errors/page_404.html", context)
    response.status_code = 404
    return response


def server_error(request):
    context = {}
    response = render(request, "errors/page_500.html", context)
    response.status_code = 500
    return response


def bad_request_error(request, exception):
    context = {}
    response = render(request, "errors/page_400.html", context)
    response.status_code = 400
    return response


def permission_denied(request, exception):
    context = {}
    response = render(request, "errors/page_403.html", context)
    response.status_code = 403
    return response
