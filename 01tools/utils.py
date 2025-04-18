import inspect

"""
Function to colorize text for terminal output.
"""
def colored_text(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[90m"
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"


"""
Function to convert a function's signature into a JSON schema.
"""
def function_to_schema(func) -> dict:
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(f"Could not inspect function: {func}: {str(e)}")
    
    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError:
            raise ValueError(f"Unsupported parameter type: {param.annotation}")
        parameters[param.name] = {"type": param_type}

    required = [param.name for param in parameters.values() if param.default == inspect._empty]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            }
        }
    }