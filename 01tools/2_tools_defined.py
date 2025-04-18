import os, json
from dotenv import load_dotenv
from openai import AzureOpenAI

from utils import colored_text


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


def create_tool_schemas():
    return [
        {
            "type": "function",
            "function": {
                "name": "execute_refund",
                "description": "",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item_id": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["item_id"],
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "look_up_item",
                "description": "Use to find item ID.\n Search query can be a description or keywords.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_query": {"type": "string"},
                    },
                    "required": ["search_query"],
                }
            }
        }
    ]


def run_full_turn(client, deployment, system_message, tools, messages):
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "system", "content": system_message}] + messages,
        tools=tools,
    )
    message = response.choices[0].message
    messages.append(message)

    if message.content:
        print(colored_text("Assistant:", "yellow"), message.content)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(
                colored_text("Assistant:", "yellow"),
                colored_text(f"Calling tool: {name}({args})", "magenta"),
            )


def chat_loop(client, deployment):
    system_message = create_system_message()
    tools = create_tool_schemas()
    messages = []
    while True:
        user = input(colored_text("User: ", "blue"))
        messages.append({"role": "user", "content": user})

        run_full_turn(client, deployment, system_message, tools, messages)


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
