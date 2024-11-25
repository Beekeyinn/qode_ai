from rest_framework.viewsets import ModelViewSet

from apps.core.permissions import IsOwnerOrReadOnly
from apps.message.api.serializers.thread import ThreadSerializer
from apps.message.models import Thread


class ThreadViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ThreadSerializer
    http_method_names = ["get", "put"]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Thread.objects.filter(user=self.request.user)
        return []
