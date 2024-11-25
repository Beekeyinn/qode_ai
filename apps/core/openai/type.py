from typing import Any, Literal, TypedDict

MODELS = Literal["gpt-4-1106-preview", "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]


TOOLS = Literal["code_interpreter", "retrieval"]


class Function(TypedDict):
    """type:function, function:dict"""

    type: str
    func: dict[str, Any]


class ThreadMetaData(TypedDict):
    user: str
    modified: bool


class ToolOutput(TypeError):
    """
    output: should be json dumped to string.
    """

    id: str
    output: str
