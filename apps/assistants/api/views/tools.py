from rest_framework.viewsets import ModelViewSet

from apps.assistants.api.serializers import AssistantToolSerializer
from apps.assistants.models import AssistantTool
from apps.core.permissions import IsOwnerOrReadOnly


class AssistantToolViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AssistantToolSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AssistantTool.objects.filter(
                assistant__id=self.kwargs.get("assistant_pk"),
            )
        return []
