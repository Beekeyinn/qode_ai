import logging

logger = logging.getLogger("runner")


def run_function(function_name, parameters):
    import importlib

    module = importlib.import_module("apps.sandbox.functions")

    logger.info(
        "[Sandbox] Running function %s with parameters %s", function_name, parameters
    )
    func = None
    try:
        func = getattr(module, function_name)
    except (KeyError, AttributeError) as ke:
        logger.error(
            "[Sandbox] Error occurred finding function: %s", function_name, exc_info=ke
        )
        return {"success": False, "data": [], "error": str(ke)}
    try:
        response = func(**parameters)
        logger.info("[Sandbox] Successfully ran function: %s.", function_name)
    except Exception as e:
        logger.error(
            "[Sandbox] Error occurred running function: %s", function_name, exc_info=e
        )
        return {"success": False, "data": []}
    else:
        if response:
            if isinstance(response, dict) or isinstance(response, list):
                return {"success": True, "data": response}
            else:
                return {"success": True, "response": f"{response}"}
        return (
            {"success": True, "message": response}
            if response is not None
            else {"success": True, "message": "Successfully ran function"}
        )
