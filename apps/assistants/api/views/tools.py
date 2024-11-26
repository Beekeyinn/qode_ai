from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from apps.assistants.api.serializers import AssistantToolSerializer
from apps.assistants.models import AssistantTool
from apps.core.permissions import IsOwnerOrReadOnly
from apps.core.mixins import ResponseMixin
from apps.core.decorator import api_exception_handler

from django.utils.decorators import method_decorator


class AssistantToolViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
    ResponseMixin,
):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AssistantToolSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AssistantTool.objects.filter(
                assistant__id=self.kwargs.get("assistant_pk"),
            )
        return []

    @method_decorator(api_exception_handler)
    def create(self, request, *args, **kwargs):
        return self.formatted_response(super().create(request, *args, **kwargs))

    @method_decorator(api_exception_handler)
    def update(self, request, *args, **kwargs):
        return self.formatted_response(super().update(request, *args, **kwargs))

    @method_decorator(api_exception_handler)
    def destroy(self, request, *args, **kwargs):
        return self.formatted_response(super().destroy(request, *args, **kwargs))

    @method_decorator(api_exception_handler)
    def list(self, request, *args, **kwargs):
        return self.formatted_response(super().list(request, *args, **kwargs))

    @method_decorator(api_exception_handler)
    def retrieve(self, request, *args, **kwargs):
        return self.formatted_response(super().retrieve(request, *args, **kwargs))

    @method_decorator(api_exception_handler)
    def partial_update(self, request, *args, **kwargs):
        return self.formatted_response(super().partial_update(request, *args, **kwargs))
