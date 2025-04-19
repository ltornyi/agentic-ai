from utils import colored_text
from agent import Agent


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

class CustomerSupportAgent(Agent):
    """
    Represents a customer support agent with specific tools and instructions.
    """
    triage_agent: Agent = None

    def transfer_to_triage(self):
        """ Use to transfer the user to triage agent.
        Use for anything the customer support agent cannot deal with.
        """
        return self.triage_agent

    def __init__(self, deployment: str, triage_agent: Agent = None):
        super().__init__(
            name="Customer Support Agent",
            deployment=deployment,
            instructions=create_system_message(),
            tools=[look_up_item, execute_refund],
        )
        if not triage_agent is None:
            self.triage_agent = triage_agent
            self.tools.append(self.transfer_to_triage)