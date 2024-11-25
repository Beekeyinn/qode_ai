import json
import sys
import time
from typing import Any

from openai.pagination import SyncCursorPage
from openai.types.beta.thread_create_params import Message as ThreadMessage
from apps.assistants.models import Assistant, AssistantTool, AssistantFile, AssistantVectorStore, OpenAiModel

from . import client
from .type import MODELS, TOOLS, Function, ThreadMetaData, ToolOutput

# Generating client


DEFAULT_THREAD_META_DATA = ThreadMetaData(user="bikin", modified=False)


class AiAssistant:
    __client = client

    def __init__(
        self,
    ):
        self.flag = False

    @property
    def client(self):
        return self.__client

    @classmethod
    def from_assistant_id(cls, assistant_id, messages=[]):
        instance = cls()
        instance.assistant = cls.__client.beta.assistants.retrieve(
            assistant_id=assistant_id
        )
        instance.create_thread(messages=messages)
        return instance

    @classmethod
    def from_assistant_id_and_thread_id(cls, assistant_id, thread_id):
        instance = cls()
        instance.assistant = cls.__client.beta.assistants.retrieve(
            assistant_id=assistant_id
        )
        instance.get_thread(thread_id)
        return instance

    @classmethod
    def all_assistants(cls):
        response = cls.__client.beta.assistants.list()
        return json.loads(response.model_dump_json())

    def create_assistant(
        self,
        name,
        description,
        instruction,
        tool: TOOLS | list[Function] = "code_interpreter",
        model: MODELS = "gpt-4-1106-preview",
        file_id: list[str | None] = [],
        metadata={},
    ):
        params = {
            "name": name,
            "description": description,
            "instructions": instruction,
            "file_ids": file_id,
            "tools": self.get_tool(tool),
            "model": model,
            "metadata": metadata,
        }
        self.assistant = self.__client.beta.assistants.create(**params)

    def modify_assistant(
        self,
        instruction: str,
        model: str = None,
        tool: TOOLS | Function | None = None,
        name: str = None,
        file_id: list[str] | None = [],
    ):
        if hasattr(self, "assistant"):
            _tool = self.get_tool(tool)
            raw_tool = None if len(_tool) == 0 else _tool
            tools = raw_tool or self.assistant.tools
            self.assistant = self.__client.beta.assistants.update(
                self.assistant.id,
                instructions=instruction or self.assistant.instructions,
                model=model or self.assistant.model,
                tools=tools,
                name=name or self.assistant.name,
                file_ids=file_id or self.assistant.file_ids,
            )
        else:
            raise ValueError("Please create Assistant before updating assistant.")

    def remove_file_from_assistant(self, file_id: str, to_dict=False):
        response = self.__client.beta.assistants.files.delete(
            file_id=file_id, assistant_id=self.assistant.id
        )
        if to_dict:
            return json.loads(response.model_dump_json())
        return response

    def add_files_to_assistant(self, file_id: str, to_dict=False):
        response = self.__client.beta.assistants.files.create(
            assistant_id=self.assistant.id, file_id=file_id
        )
        if to_dict:
            return json.loads(response.model_dump_json())
        return response

    def get_tool(self, tool: TOOLS | Function | None):
        if tool and type(tool) == TOOLS:
            tool = [{"type": tool}]
        elif tool and type(tool) == Function:
            tool = [{"type": "function", "function": tool.func}]
        else:
            tool = []
        return tool

    def get_thread(self, thread_id):
        self.thread = self.__client.beta.threads.retrieve(thread_id=thread_id)

    def create_thread(
        self,
        messages: list[ThreadMessage] = [],
        metadata: ThreadMetaData = DEFAULT_THREAD_META_DATA,
    ):
        self.thread = self.__client.beta.threads.create(
            messages=messages, metadata=metadata
        )

    def delete_thread(self, thread_id):
        thread = self.__client.beta.threads.delete(thread_id)
        if thread.deleted:
            self.thread = None

    def add_message(self, message):
        self.check_active_runs()
        self.message = self.__client.beta.threads.messages.create(
            thread_id=self.thread.id, role="user", content=message
        )

    def run_with_message(self, message, instruction=None, model=None):
        self.add_message(message)
        self.run(instruction=instruction, model=model)

    def run(self, instruction=None, model=None):
        self.runner = self.__client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=instruction or self.assistant.instructions,
            model=model or self.assistant.model,
        )
        self.wait_result()
        return self.runner

    def check_active_runs(self):
        run_list = self.__client.beta.threads.runs.list(thread_id=self.thread.id)
        flag = {"active": False, "id": None}
        for data in run_list.data:
            print("Run: ", data.id, data.status)
            if data.status == "active" or data.status == "requires_action":
                flag["active"] = True
                flag["id"] = data.id
        if flag["active"]:
            self.__client.beta.threads.runs.cancel(
                thread_id=self.thread.id, run_id=flag["id"]
            )

    def wait_result(self):
        while self.runner.status == "in_progress" or self.runner.status == "queued":
            self.runner = self.__client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, run_id=self.runner.id
            )
            time.sleep(0.5)

    def get_result(self) -> SyncCursorPage[ThreadMessage]:
        self.messages = self.__client.beta.threads.messages.list(
            self.thread.id, order="asc", after=self.message.id
        )
        data = self.messages
        return data

    def check_if_function(
        self,
    ) -> tuple[bool, SyncCursorPage[ThreadMessage] | dict[str, Any]]:
        if self.runner.status == "requires_action":
            tool_calls = self.runner.required_action.submit_tool_outputs.tool_calls
            callables = [
                {
                    "id": call.id,
                    "function": call.function.name,
                    "arguments": json.loads(call.function.arguments),
                }
                for call in tool_calls
            ]
            print("Callables: ", callables)
            return True, callables
        else:
            return False, self.get_result()

    def send_tool_call_response(self, output: list[ToolOutput]):
        self.runner = self.__client.beta.threads.runs.submit_tool_outputs(
            run_id=self.runner.id, thread_id=self.thread.id, tool_outputs=output
        )
        self.wait_result()
        return self.check_if_function()

    def get_response_text(self, response):
        return response.data[0].content[0].text.value

    @classmethod
    def seed_assistant(cls):
        """
         {
            "data": [
                {
                    "id": "asst_lKq5nuE4hESYgGCIbLSCrAoY",
                    "created_at": 1732512161,
                    "description": None,
                    "instructions": 'You are a database and data analysis expert. Your task is to understand the provided database schema at an expert level by analyzing the schema and the sample data for each table, then generating an appropriate SQL query based on a specific request.\n\nYou will receive:\n- A **database schema** consisting of multiple tables and relationships.\n- **Example data** for each table to help you understand the structure and constraints.\n\nYour goal is to formulate correct and optimized SQL queries that fulfill a given request based on your deep understanding of the schema.\n\n# Steps\n\n1. **Understand the Schema**: \n   - Analyze the structure of each table.\n   - Recognize the relationships between tables such as primary/foreign keys, one-to-many or many-to-many relationships.\n   - Take note of the fields, data types, and constraints.\n\n2. **Review Example Data**:\n   - Look at the sample data provided to comprehend the typical entries for each table.\n   - Consider edge cases such as null values, incorrect data formats, or unexpected references.\n\n3. **Generate SQL Query**:\n   - Generate an SQL query that matches the given request, using best practices.\n   - Consider potential optimizations (e.g., adding necessary joins, filtering efficiently, limiting results).\n   - Make sure any possible ambiguities are clarified using appropriate joins and conditions.\n\n# Output Format\n\n- Provide the final SQL query.\n- If relevant, add a comment explaining the query\'s purpose and structure.\n\n# Example\n\n**Schema**:\n- **Table `Customers`**:\n  - `id` (integer, primary key)\n  - `name` (varchar)\n  - `email` (varchar)\n  \n- **Table `Orders`**:\n  - `order_id` (integer, primary key)\n  - `customer_id` (integer, foreign key references `Customers.id`)\n  - `amount` (decimal)\n\n**Example Data**:\n- **Customers**:\n  - `{{ "id": 1, "name": "Alice", "email": "alice@example.com" }}`\n  - `{{ "id": 2, "name": "Bob", "email": "bob@example.com" }}`\n\n- **Orders**:\n  - `{{ "order_id": 101, "customer_id": 1, "amount": 200.50 }}`\n  - `{{ "order_id": 102, "customer_id": 2, "amount": 150.00 }}`\n\n**Query Request**:\n- Generate a query that lists each customer name alongside their total amount spent.\n\n**SQL Query**:\n```sql\nSELECT Customers.name, SUM(Orders.amount) AS total_spent\nFROM Customers\nLEFT JOIN Orders ON Customers.id = Orders.customer_id\nGROUP BY Customers.name;\n```\n\n**Comments**:\n- The **LEFT JOIN** ensures that customers without orders are also listed.\n- The **SUM()** function adds up the **amount** of each order per customer.\n- **GROUP BY** makes sure we get a distinct row for each customer.\n\n# Notes\n\n- Always make sure your query is fully accurate and tested against the schema.\n- Take into account unusual cases, like customers without orders.\n- Include aggregated or grouped data if requested, being mindful of NULL values and data integrity.\n\nRespond in JSON Format. Example:\n{\n"query":<SQL Query suitable for sql alchemy>,\n"table":<Query running on table>,\n"mode":<Mode of query: Select, Update, Delete, or more >\n} ',
                    "metadata": {},
                    "model": "gpt-4o-mini",
                    "name": "Database Analytic and Expert",
                    "object": "assistant",
                    "tools": [
                        {"type": "code_interpreter"},
                        {
                            "function": {
                                "name": "get_database_schema",
                                "description": "Retrieves the schema of a specified database",
                                "parameters": {
                                    "properties": {},
                                    "additionalProperties": False,
                                    "type": "object",
                                    "required": [],
                                },
                                "strict": True,
                            },
                            "type": "function",
                        },
                        {
                            "function": {
                                "name": "run_sql_query",
                                "description": "Executes a specified SQL query against a database",
                                "parameters": {
                                    "type": "object",
                                    "required": ["query"],
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": "The SQL query to be executed",
                                        }
                                    },
                                    "additionalProperties": False,
                                },
                                "strict": True,
                            },
                            "type": "function",
                        },
                    ],
                    "response_format": {"type": "text"},
                    "temperature": 1.0,
                    "tool_resources": {
                        "code_interpreter": {"file_ids": []},
                        "file_search": None,
                    },
                    "top_p": 1.0,
                }
            ],
            "object": "list",
            "first_id": "asst_lKq5nuE4hESYgGCIbLSCrAoY",
            "last_id": "asst_lKq5nuE4hESYgGCIbLSCrAoY",
            "has_more": False,
        }
        """
        assistants = cls.all_assistants()
        for assistant in assistants["data"]:
            model = assistant["model"]
            tools = assistant["tools"]
            name = assistant["name"]
            description = assistant["description"]
            instruction = assistant["instructions"]
            tool_resources = assistant["tool_resources"]

