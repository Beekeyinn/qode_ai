import json
from typing import Any

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from apps.assistants.signal import bulk_file_signal
from apps.assistants.models import (
    Assistant,
    AssistantFile,
    AssistantTool,
    AssistantVectorStore,
)
from apps.core.openai.assistant import AiAssistant
from apps.core.openai.files import OpenAiFiles
from apps.core.openai.vector import OpenAiVectorStore
from apps.core.slugger import unique_slug_generator
from concurrent.futures import Future, ThreadPoolExecutor, as_completed


@receiver(pre_save, sender=Assistant)
def check_change_in_instruction(instance, sender, *args, **kwargs):
    if instance.slug is None:
        instance.slug = unique_slug_generator(instance, field_name="name")
    old_data = Assistant.objects.filter(id=instance.id).first()
    if old_data and old_data.instructions != instance.instructions:
        setattr(instance, "changed", True)


@receiver(post_save, sender=Assistant)
def assistant_post_save_signal(instance: Assistant, created, sender, *args, **kwargs):
    if hasattr(instance, "changed") or created:
        if getattr(instance, "changed", False):
            assistant = AiAssistant.from_assistant_id(instance.assistant_id)
            assistant.modify_assistant(instance.instructions)
            if not hasattr(instance, "vector_stores"):
                AssistantVectorStore.objects.create(
                    user=instance.user,
                    name=f"{instance.name} Vector Store",
                    assistant=instance,
                )
        elif created:
            if not instance.assistant_id:
                assistant = AiAssistant()
                assistant.create_assistant(
                    instance.name,
                    instance.description,
                    instance.instructions,
                    instance.model,
                    metadata={"user": instance.user.encoded_email},
                )
                instance.assistant_id = assistant.assistant.id
                instance.save()
                AssistantVectorStore.objects.create(
                    user=instance.user,
                    name=f"{instance.name} Vector Store",
                    assistant=instance,
                )


@receiver(post_delete, sender=AssistantFile)
def remove_from_openai(instance: AssistantFile, sender, *args, **kwargs):
    openai_file = OpenAiFiles()
    openai_file.delete_file(instance.file_id)


@receiver(post_save, sender=AssistantFile)
def add_file_to_open_ai(instance: AssistantFile, created, sender, *args, **kwargs):
    if created:
        if instance.file:
            files = OpenAiFiles()
            file = instance.file.open(mode="rb")
            res = files.upload_file(file=file, purpose=instance.purpose)
            instance.id = res.id
        instance.save()


@receiver(post_save, sender=AssistantTool)
def add_tool_to_open_ai(instance: AssistantTool, created, sender, *args, **kwargs):
    if created:
        if instance.assistant:
            ai_assistant = AiAssistant.from_assistant_id(
                instance.assistant.assistant_id
            )
            tools = [
                json.loads(tool.model_dump_json())
                for tool in ai_assistant.assistant.tools
            ]
            tools.append(instance.tool)
            ai_assistant.modify_assistant(
                instruction=instance.assistant.instructions, tool=tools
            )


@receiver(bulk_file_signal)
def handle_bulk_file_upload(sender, files: dict[Any, AssistantFile], **kwargs):
    openai_files = OpenAiFiles()

    def upload_file(file, openai_files):
        file = file.file.open(mode="rb")
        res = openai_files.upload_file(file=file, purpose=file.purpose)
        file.file_id = res.id
        file.save()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(upload_file, file, openai_files) for file in files.values()
        ]
        for future in as_completed(futures):
            exc = future.exception()
            if exc:
                print(f"Exception: {exc}")
                raise exc
            future.result()


@receiver(post_save, sender=AssistantVectorStore)
def add_vector_store_to_open_ai(
    instance: AssistantVectorStore, created, sender, *args, **kwargs
):
    if created:
        vs = OpenAiVectorStore()
        res = vs.create_vector_store(
            instance.name,
            metadata={
                "user": instance.user.encoded_email,
                "assistant": instance.assistant.name,
                "assistant_id": instance.assistant.assistant_id,
            },
        )
        instance.vector_store_id = res.id
        instance.save()



@receiver(post_delete, sender=AssistantVectorStore)
def delete_vector_store_from_open_ai(
    instance: AssistantVectorStore, sender, *args, **kwargs
):
    vs = OpenAiVectorStore()
    vs.delete_vector_store(instance.vector_store_id)
    instance.delete()

