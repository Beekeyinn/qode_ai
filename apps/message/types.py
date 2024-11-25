from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class RoleChoices(TextChoices):
    USER = "user", _("user")
    ASSISTANT = "assistant", _("assistant")
