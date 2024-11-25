from apps.assistants.models import Assistant, AssistantTool


def run_function(function_name, assistant: Assistant, **parameters):
    import importlib

    import requests

    module = importlib.import_module("apps.core.functions")

    print("Params", function_name, assistant, parameters)
    function_string = ""
    func = None
    try:
        func = getattr(module, function_name)
    except KeyError as ke:
        print("Function not found in project")
        tool = AssistantTool.objects.filter(
            function_name=function_name, assistant=assistant
        ).first()
        if tool is None:
            return {"success": False, "message": "Function not found"}
        function_string = tool.function_logic
        exec(function_string)
        func = locals()[function_name]
    try:
        print("function in runner", func, parameters)
        response = func(**parameters)
    except Exception as e:
        print("Error occured while executing function: ", e.__class__.__name__, e)
        return {"success": False, "error": f"{e.__class__.__name__}: {e}"}
    else:
        print("Dammm working")
        if response:
            if isinstance(response, dict):
                return response
            else:
                return {"success": True, "response": f"{response}"}
        return (
            {"success": True, "message": response}
            if response is not None
            else {"success": True, "message": "Successfully runned"}
        )
