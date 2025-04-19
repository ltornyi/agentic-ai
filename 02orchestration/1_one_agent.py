import os, json
from dotenv import load_dotenv
from openai import AzureOpenAI

from customer_support_agent import CustomerSupportAgent
from utils import colored_text
from agent import Agent


def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(
        colored_text("Assistant:", "yellow"),
        colored_text(f"{name}({args})", "magenta"),
    )

    return tools_map[name](**args)


def run_full_turn(client, agent: Agent, messages):

    # looping so that the LLM can respond to the tools calls
    while True:
        response = client.chat.completions.create(
            model=agent.deployment,
            messages=[{"role": "system", "content": agent.instructions}] + messages,
            tools=agent.tool_schemas,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:
            print(colored_text("Assistant:", "yellow"), message.content)

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, agent.tools_map)
            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)


def chat_loop(client, agent):
    messages = []
    while True:
        user = input(colored_text("User: ", "blue"))
        messages.append({"role": "user", "content": user})

        run_full_turn(client, agent, messages)


def main():
    load_dotenv()
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2025-01-01-preview",
    )
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    agent = CustomerSupportAgent(
        deployment=deployment,
    )
    chat_loop(client, agent)
    

if __name__ == "__main__":
    main()
