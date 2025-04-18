import os
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


def chat_loop(client, deployment):
    system_message = create_system_message()
    messages = []
    while True:
        user = input(colored_text("User:", "blue"))
        messages.append({"role": "user", "content": user})

        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "system", "content": system_message}] + messages,
        )
        message = response.choices[0].message
        print(colored_text("Assistant:", "yellow"), message.content)

        messages.append(message)


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
