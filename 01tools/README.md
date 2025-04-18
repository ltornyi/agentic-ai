# Idea: customer service agent

## example chat

    user: hi, where is my order?
    openai: what is your order number?
    user: 12345
    developer code: calls get_order(12345)
        function response: {status: "shipped", tracking_number: "ABC123"}
    developer code: passes response to openai
    openai: your order has been shipped. the tracking number is ABC123.


## Python environment setup

    python3 -m venv venv
    . ./venv/bin/activate
    pip install openai python-dotenv

## Deploy OpenAI model and set environment variables

create .env file and add variables to it:

    AZURE_OPENAI_API_KEY="REPLACE_WITH_YOUR_KEY_VALUE_HERE"
    AZURE_OPENAI_ENDPOINT="REPLACE_WITH_YOUR_ENDPOINT_HERE"
    AZURE_OPENAI_DEPLOYMENT="REPLACE_WITH_YOUR_DEPLOYMENT_HERE"

## Building and evolving the agent

### 0_setup.py

Simple chat loop to demonstrate the setup.

### 1_routines.py
System prompt to make the LLM follow a routine. Actions are hallucinations because at this point it doesn't have access to the tools. A typical chat example:

* User:Hi! Who are you?
* Assistant: I am a customer support agent for ACME Corp, here to assist you with any questions or issues you may have. How can I help you today?
* User:My roadrunner catcher has broken into two pieces
* Assistant: I'm sorry to hear that! Could you please explain how the road runner catcher got damaged?
* User:I was trying to catch a roadrunner
* Assistant: I see! Have you had any prior issues with the road runner catcher, or is this the first time something has gone wrong?
* User:it was the first time
* Assistant: Thank you for that information! It sounds like it may have been an unexpected mishap. I recommend using a sturdy adhesive to reattach the pieces, or if that's not effective, I can help arrange a refund for you. Would you like a refund?
* User:yes, I want a refund
* Assistant: Could you please provide your order ID so I can process the refund for you?
* User:1456778
* Assistant: Thank you! I will now process the refund for order ID 1456778. Please hold on a moment. 
Your refund has been successfully processed! If you have any other questions or need further assistance, feel free to ask.

### 2_tools_defined.py

Tools are defined but the actual functions are not implemented. This crashes as soon as the LLM decides to call a tool because the call is not implemented. For each tool_call_id a message is expected to sent back to the LLM. Example chat:

* User: Hi! who are you?
* Assistant: I'm a customer support agent for ACME Corp, here to assist you with any questions or issues you may have. How can I help you today?
* User: My e-scooter fails to start
* Assistant: Can you please provide more details about the issue, such as any error messages or lights on the display?
* User: the display is all red and reads contact support
* Assistant: It sounds like there may be a battery or connectivity issue. Have you tried charging the e-scooter fully and then attempting to start it again?
* User: yes, but it doesn't help
* Assistant: I recommend performing a hard reset by turning the scooter off, waiting for a minute, and then turning it back on. If that doesn't work, we can look into a refund option if you prefer.
* User: yes, I want a refund
* Assistant: Calling tool: look_up_item({'search_query': 'e-scooter'})
* User: Can I have my refund?

The code crashes at this point with the error message "An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'."