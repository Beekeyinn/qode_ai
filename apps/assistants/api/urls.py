from django.urls import include, path
from rest_framework_nested.routers import NestedDefaultRouter, SimpleRouter

from apps.assistants.api.views import (
    AssistantFileViewSet,
    AssistantModelViewSet,
    AssistantToolViewSet,
)

router = SimpleRouter()
router.register("assistant", AssistantModelViewSet, basename="assistant")
router.register("file", AssistantFileViewSet, basename="file")

assistant_router = NestedDefaultRouter(router, r"assistant", lookup="assistant")
assistant_router.register(r"tool", AssistantToolViewSet, basename="assistant-tool")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(assistant_router.urls)),
]
