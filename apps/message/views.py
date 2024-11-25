import json
from ast import arguments
from http.client import responses

from django.shortcuts import render
from django.utils.text import slugify
from rest_framework import status
from rest_framework.response import Response

from apps.assistants.models import Assistant
from apps.core.openai.runner import run_function
from apps.message.models import Message, Thread


# Create your views here.
class AssistantMessageView(object):
    def get_thread(self, thread_id):
        self.thread = Thread.objects.get(id=thread_id)
        self.aiassistant = self.thread.aiassistant

    def create_new_thread(self, message, assistant_id):
        assistant = Assistant.objects.get(slug=assistant_id)
        self.thread = Thread.objects.create(
            name=slugify(" ".join(message.split(" ")[:5])),
            user=self.request.user,
            assistant=assistant,
        )
        self.aiassistant = self.thread.aiassistant

    def create_message(self, role, message_id, message):
        return Message.objects.create(
            thread=self.thread, message_id=message_id, role=role, message=message
        )

    def handle_text_response(self, response):
        ret_response = []
        for data in response.data:
            message = self.create_message(
                role=data.role,
                message_id=data.id,
                message="\n".join([cont.text.value for cont in data.content]),
            )
            ret_response.append(
                {
                    "role": data.role,
                    "message": "\n".join([cont.text.value for cont in data.content]),
                }
            )

        return Response(
            {"messages": ret_response},
            status=status.HTTP_200_OK,
        )

    def handle_function_call_response(self, response):
        tools_outputs = []
        print("handle_function_call_response: ", response)
        for data in response:
            print("Assistant function calling data: ", data)
            function_name = data["function"]
            parameters = data["arguments"]
            parameters["user"] = getattr(getattr(self, "request", None), "user", None)
            print("Running function", function_name, parameters)
            res = run_function(function_name, self.thread.assistant, **parameters)
            print("function runned successfully", res)

            tools_outputs.append(
                {"tool_call_id": data["id"], "output": json.dumps(res)}
            )
        is_function, response = self.aiassistant.send_tool_call_response(tools_outputs)
        return self.check_function_or_not(is_function, response)

    def check_function_or_not(self, is_function, response):
        print("Checking function", is_function, response)
        if is_function:
            print("handling function call response")
            return self.handle_function_call_response(response)
        else:
            print("Handling response")
            return self.handle_text_response(response)
