from email.policy import default

from django.db import models

from apps.accounts.models import User
from apps.assistants.models import Assistant
from apps.core.models import ExtraFieldsModelsMixin
from apps.core.openai.assistant import AiAssistant
from apps.message.types import RoleChoices


# Create your models here.
class Thread(ExtraFieldsModelsMixin):
    thread_id = models.CharField(max_length=200, unique=True)
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)

    @property
    def aiassistant(self):
        assistant = AiAssistant.from_assistant_id_and_thread_id(
            self.assistant.assistant_id, self.thread_id
        )
        return assistant


class Message(ExtraFieldsModelsMixin):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    message_id = models.CharField(max_length=100, unique=True)
    message = models.TextField(null=True, blank=True)
    role = models.CharField(
        max_length=20, choices=RoleChoices.choices, default=RoleChoices.USER
    )
