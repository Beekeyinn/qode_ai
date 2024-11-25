import json
import time
from pprint import pprint

from openai import BadRequestError, PermissionDeniedError

from apps.accounts.models import User
from apps.core.openai.assistant import AiAssistant
from apps.core.openai.files import OpenAiFiles

from .models import Assistant, AssistantFile, AssistantTool

user, created = User.objects.get_or_create(email="admin@admin.com", username="admin")


def get_files():
    ai_files = OpenAiFiles(to_dict=True)
    files = ai_files.get_files()
    for data in files["data"]:
        params = {
            "file_id": data["id"],
            "file_size": data["bytes"],
            "name": data["filename"],
            "purpose": data["purpose"],
            "user": user,
        }
        try:
            content = ai_files.get_file_content(data["id"])
        except PermissionDeniedError as e:
            print("Permission Denied while getting content: ", e.message)
        except BadRequestError as e:
            print("Bad Request error while getting content: ", e.message)
        else:
            params["file"] = content
        print("Params: ", params)
        AssistantFile.objects.get_or_create(**params)


def get_assistants():
    assistants = AiAssistant.all_assistants()
    for data in assistants["data"]:
        file_ids = data.get("file_ids")
        files = AssistantFile.objects.filter(file_id__in=file_ids)
        tools = data.get("tools")
        assistant_prams = {
            "assistant_id": data["id"],
            "description": data["description"],
            "instructions": data["instructions"],
            "model": data["model"],
            "name": data["name"],
            "user": user,
            "is_global": True,
        }
        print("Assistant prams:", assistant_prams.get("assistant_id"))
        assistant, created = Assistant.objects.get_or_create(**assistant_prams)
        time.sleep(5)
        for file in files:
            AssistantFile.objects.filter(id=file.id).update(assistant=assistant)

        for tool in tools:
            print("tool: %s" % tool)
            params = {
                "tool_type": tool["type"],
                "assistant": assistant,
            }
            if tool["type"] == "function":
                params["function_descriptor"] = tool["function"]
            AssistantTool.objects.get_or_create(**params)
        print("\n\n\n")


def get_tools():
    for assis in Assistant.objects.all():
        assistant = AiAssistant.from_assistant_id(assis.assistant_id)
        for tool in assistant.assistant.tools:
            tool_d = json.loads(tool.model_dump_json())
            params = {"tool_type": tool_d["type"], "assistant": assis}
            if tool_d["type"] == "function":
                params["function_name"] = tool_d["function"]["name"]
                params["function_descriptor"] = tool_d["function"]
            # AssistantTool.objects.create(**params)
