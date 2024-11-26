from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.api.serializers import UserSerializer
from apps.accounts.models import User

from apps.core.mixins import ResponseMixin
from apps.core.decorator import api_exception_handler

from django.utils.decorators import method_decorator


class IdentityView(GenericAPIView, ResponseMixin):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user
        return []

    @method_decorator(api_exception_handler)
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset())
        return self.return_response(serializer.data, status=status.HTTP_200_OK)
