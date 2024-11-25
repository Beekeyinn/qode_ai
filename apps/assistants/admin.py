from django.contrib import admin

from apps.assistants.forms import AssistantToolCreateForm
from apps.assistants.models import Assistant, AssistantFile, AssistantTool

# Register your models here.


class AssistantAdmin(admin.ModelAdmin):
    list_display = [
        "assistant_id",
        "name",
        "slug",
        "user",
        "model",
        "instructions",
        "description",
    ]

    search_fields = (
        "user__email",
        "name",
    )
    list_filter = (
        "model",
        "is_global",
    )


class AssistantFileAdmin(admin.ModelAdmin):
    list_display = [
        "file_id",
        "name",
        "user",
        "assistant",
        "purpose",
        "file",
        "file_size",
    ]

    search_fields = (
        "user__email",
        "name",
    )

    list_filter = ("purpose",)


class AssistantToolAdmin(admin.ModelAdmin):
    form = AssistantToolCreateForm
    list_display = [
        "assistant",
        "tool_type",
        "function_name",
        "function_logic",
        "function_descriptor",
    ]

    search_fields = (
        "assistant_name",
        "assistant__user__email",
    )

    list_filter = ("tool_type",)


admin.site.register(Assistant, AssistantAdmin)
admin.site.register(AssistantFile, AssistantFileAdmin)
admin.site.register(AssistantTool, AssistantToolAdmin)
