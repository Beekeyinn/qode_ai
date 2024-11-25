from django.shortcuts import redirect, render
from django.views.generic import View

from apps.accounts.mixins import RedirectAuthenticationMixin


class LoginView(RedirectAuthenticationMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")
