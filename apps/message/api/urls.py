from cgitb import lookup

from django.urls import include, path
from rest_framework_nested.routers import NestedDefaultRouter, SimpleRouter

from apps.assistants.api.urls import router as assistant_router
from apps.message.api.views.message import MessageCreateApiView, MessageViewSet
from apps.message.api.views.thread import ThreadViewSet

router = SimpleRouter()
router.register("thread", ThreadViewSet, basename="thread")

thread_parent_router = NestedDefaultRouter(
    assistant_router, r"assistant", lookup="assistant"
)
thread_parent_router.register("thread", ThreadViewSet, basename="thread")

message_router = NestedDefaultRouter(thread_parent_router, r"thread", lookup="thread")
message_router.register("message", MessageViewSet, basename="message")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(message_router.urls)),
    path("", include(thread_parent_router.urls)),
    path(
        "assistant/<slug:assistant_slug>/message/",
        MessageCreateApiView.as_view(),
        name="assistant-thread-and-message-create",
    ),
]
