from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from apps.assistants.api.serializers import (
    AssistantModelCreateSerializer,
    AssistantModelSerializer,
    AssistantModelUpdateSerializer,
    AssistantFileListSerializer,
)
from apps.assistants.models import Assistant, AssistantFile, AssistantVectorStore
from apps.core.permissions import IsOwnerOrReadOnly
from apps.core.views import MultiSerializerViewSetMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.core.decorator import api_exception_handler
from apps.core.mixins import ResponseMixin
from django.utils.decorators import method_decorator


class AssistantModelViewSet(MultiSerializerViewSetMixin, ResponseMixin, ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AssistantModelSerializer
    parser_classes = [MultiPartParser, FormParser]
    serializer_action_classes = {
        "list": AssistantModelSerializer,
        "create": AssistantModelCreateSerializer,
        "put": AssistantModelUpdateSerializer,
        "patch": AssistantModelUpdateSerializer,
        "add_files": AssistantFileListSerializer,
    }
    lookup_field = "slug"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            lookups = Q(user=self.request.user) | Q(is_global=True)
            return Assistant.objects.filter(lookups).distinct()
        return []

    @action(detail=True, methods=["post"])
    def add_files(self, request, slug=None):
        assistant = self.get_object()
        serializer: AssistantFileListSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        files = serializer.save()
        vector_store: AssistantVectorStore = assistant.vector_stores
        vector_store.files.add([file.id for file in files])
        return self.return_response({"created": True}, status=status.HTTP_201_CREATED)

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
    def retrieve(self, request, *args, **kwargs):
        return self.formatted_response(super().retrieve(request, *args, **kwargs))

    @method_decorator(api_exception_handler)
    def list(self, request, *args, **kwargs):
        return self.formatted_response(super().list(request, *args, **kwargs))
