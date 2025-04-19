import os, json
from dotenv import load_dotenv
from openai import AzureOpenAI

from triage_agent import TriageAgent
from customer_support_agent import CustomerSupportAgent
from utils import colored_text
from agent import Agent


def execute_tool_call(tool_call, tools_map, current_agent_name):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(
        colored_text(f"{current_agent_name}:", "yellow"),
        colored_text(f"{name}({args})", "magenta"),
    )

    return tools_map[name](**args)


def run_full_turn(client, agent: Agent, messages):
    current_agent = agent
    # looping so that the LLM can respond to the tools calls
    while True:
        response = client.chat.completions.create(
            model=current_agent.deployment,
            messages=[{"role": "system", "content": current_agent.instructions}] + messages,
            tools=current_agent.tool_schemas,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:
            print(colored_text(f"{current_agent.name}:", "yellow"), message.content)

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, current_agent.tools_map, current_agent.name)

            if isinstance(result, Agent):
                current_agent = result
                result = f"Transferred to {current_agent.name} agent."

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    return current_agent


def chat_loop(client, agent):
    messages = []
    current_agent = agent
    while True:
        user = input(colored_text("User: ", "blue"))
        messages.append({"role": "user", "content": user})

        current_agent = run_full_turn(client, current_agent, messages)


def main():
    load_dotenv()
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2025-01-01-preview",
    )
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    customer_service_agent = CustomerSupportAgent(deployment=deployment)
    triage_agent = TriageAgent(
        deployment=deployment,
        service_agent=customer_service_agent,
        sales_agent=None,
    )
    customer_service_agent.set_triage_agent(triage_agent)
    chat_loop(client, triage_agent)
    

if __name__ == "__main__":
    main()
