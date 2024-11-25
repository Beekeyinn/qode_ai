from rest_framework.viewsets import ModelViewSet

from apps.assistants.api.serializers import (
    AssistantFileModelSerialzer,
    AssistantFileModelUpdateSerializer,
)
from apps.assistants.models import AssistantFile
from apps.core.permissions import IsOwnerOrReadOnly
from apps.core.views import MultiSerializerViewSetMixin


class AssistantFileViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_action_classes = {
        "put": AssistantFileModelUpdateSerializer,
        "patch": AssistantFileModelUpdateSerializer,
    }
    serializer_class = AssistantFileModelSerialzer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AssistantFile.objects.filter(user=self.request.user)
        return []


