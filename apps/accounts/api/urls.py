from django.urls import path

from apps.accounts.api.views import IdentityView

urlpatterns = [
    path("identity/", IdentityView.as_view(), name="identity"),
]
