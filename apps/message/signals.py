from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.core.openai.assistant import AiAssistant
from apps.core.openai.type import ThreadMetaData
from apps.message.models import Message, Thread


@receiver(post_save, sender=Thread)
def create_assistant_thread(instance: Thread, created, sender, *args, **kwargs):
    if created:
        assistant = AiAssistant.from_assistant_id(instance.assistant.assistant_id)
        meta_data = ThreadMetaData(user=instance.user.email, modified=False)
        assistant.create_thread(messages=[], metadata=meta_data)
        instance.thread_id = assistant.thread.id
        instance.save()


@receiver(post_delete, sender=Thread)
def delete_assistant_thread(instance: Thread, sender, *args, **kwargs):
    if instance.thread_id:
        instance.aiassistant.delete_thread(instance.thread_id)
