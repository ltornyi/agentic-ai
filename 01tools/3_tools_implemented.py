import os, json
from dotenv import load_dotenv
from openai import AzureOpenAI

from utils import colored_text, function_to_schema


def create_system_message():
    return (
        "You are a customer support agent for ACME Corp. "
        "Always answer in a sentence or less. "
        "Follow the following routine with the user: "
        "1. First, ask probing questions to understand the user's problem deeper.\n"
        " - unless the user has already provided a reason.\n"
        "2. Propose a fix (make one up if you have to).\n"
        "3. Only if not satisfied, offer a refund.\n"
        "4. If accepted, search for the order ID and execute the refund."
        ""
    )


def look_up_item(search_query):
    """ Use to find item ID.
    Search query can be a description or keywords.
    Returns the item ID or null if not found.
    """
    item_id = "item_12345"
    print(colored_text("Found item:", "green"), item_id)
    return item_id


def execute_refund(item_id, reason="Not provided"):
    """ Use to execute a refund for a specific item ID.
    Returns 'success' if the refund was executed amd 'failure' otherwise.
    """
    print(colored_text("\n\n===Refund summary===", "green"))
    print(colored_text(f"Item ID: {item_id}", "green"))
    print(colored_text(f"Reason: {reason}", "green"))
    print(colored_text("====================\n", "green"))
    print(colored_text("Refund executed successfully.", "green"))
    return "success"


def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(
        colored_text("Assistant:", "yellow"),
        colored_text(f"{name}({args})", "magenta"),
    )

    return tools_map[name](**args)


def build_tools():
    tools = [execute_refund, look_up_item]
    tool_schemas = [function_to_schema(tool) for tool in tools]
    tools_map = {tool.__name__: tool for tool in tools}
    return tools_map, tool_schemas


def run_full_turn(client, deployment, system_message, tools, messages, tools_map):

    # looping so that the LLM can respond to the tools calls
    while True:
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "system", "content": system_message}] + messages,
            tools=tools,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:
            print(colored_text("Assistant:", "yellow"), message.content)

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools_map)
            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)


def chat_loop(client, deployment):
    system_message = create_system_message()
    tools_map, tool_schemas = build_tools()
    messages = []
    while True:
        user = input(colored_text("User: ", "blue"))
        messages.append({"role": "user", "content": user})

        run_full_turn(client, deployment, system_message, tool_schemas, messages, tools_map)


def main():
    load_dotenv()
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2025-01-01-preview",
    )
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    chat_loop(client, deployment)
    

if __name__ == "__main__":
    main()
