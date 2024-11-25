from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.core.models import ExtraFieldsModelsMixin

# Create your models here.


class OpenAiModel(ExtraFieldsModelsMixin):
    name = models.CharField(
        _("Model Name"), max_length=200, default="gpt-4o-mini", unique=True
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Assistant(ExtraFieldsModelsMixin):
    class ModelChoices(models.TextChoices):
        GPT4P = "gpt-4-1106-preview", _("GPT 4 Preview")
        GPT3 = "gpt-3.5-turbo-16k", _("GPT 3")
        GPT4 = "gpt-4-1106", _("GPT 4")

    user = models.ForeignKey(User, related_name="assistants", on_delete=models.CASCADE)
    slug = models.SlugField(
        _("Slug"), null=True, blank=False, max_length=200, unique=True
    )
    assistant_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(_("Assitant Name"), max_length=200)
    description = models.TextField(_("Description"), blank=True, null=True)
    instructions = models.TextField(_("Instructions"), blank=False)
    model = models.ForeignKey(
        OpenAiModel, on_delete=models.CASCADE, related_name="assistants"
    )
    is_global = models.BooleanField(_("Is Global"), default=False)

    def __str__(self) -> str:
        return f"{self.name}"


class AssistantTool(ExtraFieldsModelsMixin):
    class ToolsChoices(models.TextChoices):
        CODE_INTERPRETER = "code_interpreter", _("Code Interpreter")
        FUNCTION = "function", _("Function")
        RETRIEVAL = "retrieval", _("Retrieval")

    tool_type = models.CharField(
        _("Tool Type"),
        max_length=50,
        choices=ToolsChoices.choices,
        default=ToolsChoices.RETRIEVAL,
    )
    function_name = models.CharField(
        _("Function Name"), max_length=100, null=True, blank=True
    )
    function_logic = models.TextField(_("Function Logic"), null=True, blank=True)
    function_descriptor = models.JSONField(
        _("Function OpenAPI descriptor"), null=True, blank=True
    )
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)

    @property
    def tool(self):
        tool = {"type": self.tool_type}
        if self.tool_type == "function":
            tool["function"] = self.function_descriptor or ""
        return tool

    # def clean_function_descriptor(self, value):
    #     if self.tool_type == "function" and value is None:
    #         raise ValueError("tool type function needs function parameter")
    #     else:
    #         self.function_descriptor = None
    #     return value

    # def clean_function_logic(self, value):
    #     if self.tool_type == "function" and (value is None or value == ""):
    #         raise ValueError("tool type function needs function logic parameter")
    #     else:
    #         self.function_logic = None
    #     return value

    # def clean_function_name(self, value):
    #     if self.tool_type == "function" and (value is None or value == ""):
    #         raise ValueError("tool type function needs function name parameter")
    #     else:
    #         self.function_name = None
    #     return value


class AssistantFile(ExtraFieldsModelsMixin):
    user = models.ForeignKey(
        User, related_name="assistant_files", on_delete=models.CASCADE
    )
    file_id = models.CharField(_("File ID"), max_length=200, null=True, unique=True)
    name = models.CharField(_("File Name"), max_length=400)
    file_size = models.PositiveBigIntegerField(_("File Size In Bytes"), null=True)
    purpose = models.CharField(_("Purpose"), max_length=100, default="assitant")
    file = models.FileField(
        _("File"), upload_to="assistant/files", null=True, blank=True
    )
    assistant = models.ForeignKey(
        Assistant, related_name="files", on_delete=models.CASCADE, null=True
    )

    def __str__(self) -> str:
        return f"{self.name}"


class AssistantVectorStore(ExtraFieldsModelsMixin):
    user = models.ForeignKey(
        User, related_name="assistant_vector_stores", on_delete=models.CASCADE
    )
    name = models.CharField(_("Vector Store Name"), max_length=200)
    vector_store_id = models.CharField(
        _("Vector Store ID"), max_length=200, null=True, unique=True
    )
    assistant = models.OneToOneField(
        Assistant, related_name="vector_stores", on_delete=models.CASCADE, null=True
    )
    files = models.ManyToManyField(AssistantFile, related_name="vector_stores")

    def __str__(self) -> str:
        return f"{self.name}"
