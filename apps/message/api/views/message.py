from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.assistants.models import Assistant
from apps.core.decorator import api_exception_handler
from apps.core.permissions import IsOwnerOrReadOnly
from apps.message.api.serializers import MessageCreateSerializer, MessageSerializer
from apps.message.models import Message
from apps.message.views import AssistantMessageView


class MessageViewSet(AssistantMessageView, ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOrReadOnly]
    http_method_names = ["get", "post", "head"]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Message.objects.filter(
                thread__id=self.kwargs.get("thread_pk"), thread__user=self.request.user
            )
        return []

    @method_decorator(lambda x: api_exception_handler(x, use_automic=False))
    def create(self, request, assistant_slug=None, thread_pk=None, *args, **kwargs):
        """Create a new message in previous thread"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        a = Assistant.objects.all().first()
        self.get_thread(thread_pk)
        aiassistant = self.aiassistant
        aiassistant.add_message(serializer.validated_data.get("message"))
        self.create_message(
            aiassistant.message.role,
            aiassistant.message.id,
            serializer.validated_data.get("message"),
        )
        aiassistant.run()
        is_function, response = aiassistant.check_if_function()
        response = self.check_function_or_not(is_function, response)
        if response:
            return response
        return Response("test", status=200)

    @method_decorator(api_exception_handler)
    def list(self, request, *args, **kwargs):
        """List all messages on the given thread of given assistant."""
        return super().list(request, *args, **kwargs)


class MessageCreateApiView(AssistantMessageView, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageCreateSerializer
    http_method_names = ["post"]

    @method_decorator(api_exception_handler)
    def post(self, request, assistant_slug=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.create_new_thread(serializer.validated_data.get("message"), assistant_slug)
        aiassistant = self.aiassistant
        aiassistant.add_message(serializer.validated_data.get("message"))
        self.create_message(
            aiassistant.message.role,
            aiassistant.message.id,
            serializer.validated_data.get("message"),
        )
        aiassistant.run()
        is_function, response = aiassistant.check_if_function()
        response = self.check_function_or_not(is_function, response)
        response.data["thread"] = self.thread.id
        return response
