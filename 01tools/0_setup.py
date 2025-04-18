import os
from dotenv import load_dotenv
from openai import AzureOpenAI

from utils import colored_text


def chat_loop(client, deployment):
    system_message = "You are a helpful assistant."
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
