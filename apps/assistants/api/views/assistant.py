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


class AssistantModelViewSet(MultiSerializerViewSetMixin, ModelViewSet):
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
        return Response({"created": True}, status=status.HTTP_201_CREATED)
