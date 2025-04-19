from utils import colored_text
from agent import Agent


def create_system_message():
    return (
        "You are a sales agent for ACME Corp. "
        "Always answer in a sentence or less. "
        "Follow the following routine with the user: "
        "1. Ask them about any problems in their life related to bicycles.\n"
        "2. Casually mention one of ACME's crazy made-up products that can help - don't mention price.\n"
        "3. Once the user is bought in, drop a ridiculous price.\n"
        "4. If the user says yes, tell them a crazy caveat and execute their order.\n"
        ""
    )


def execute_order(product, price: int):
    """ Price should be in USD.
    """
    print("\n\n===Order summary===")
    print(colored_text(f"Product: {product}", "green"))
    print(colored_text(f"Price: {price}", "green"))
    print(colored_text("====================\n", "green"))
    confirm = input(
        colored_text("Do you want to proceed with the order? (yes/no): ", "blue")
    ).strip().lower()
    if confirm == "y":
        print(colored_text("Order executed successfully.", "green"))
        return "success"
    else:
        print(colored_text("Order cancelled.", "red"))
        return "failure"


class SalesAgent(Agent):
    """
    Represents a sales agent with specific tools and instructions.
    """
    triage_agent: Agent = None

    def transfer_to_triage(self):
        """ Use this if the user brings up a topic outside sales or buying.
        Use for anything you cannot deal with.
        """
        return self.triage_agent

    def __init__(self, deployment: str):
        super().__init__(
            name="Sales Agent",
            deployment=deployment,
            instructions=create_system_message(),
            tools=[execute_order],
        )

    def set_triage_agent(self, triage_agent: Agent):
        """ Set the triage agent for this sales agent. """
        self.triage_agent = triage_agent
        self.add_tool(self.transfer_to_triage)