from django.urls import include, path

urlpatterns = [
    path("account/", include("apps.accounts.api.urls")),
    path("", include("apps.assistants.api.urls")),
    path("", include("apps.message.api.urls")),
]
