from utils import colored_text
from agent import Agent


def create_system_message():
    return (
        "You are a customer service bot for ACME Corp. "
        "Always be very brief. "
        "Father information to direct the user to the right agent. "
        "Make your questions very natural, human-like and subtle. "
    )


def transfer_to_customer_service():
    """ Use to transfer the user to customer service agent.
    Use for issues, repairs and refunds.
    """
    return None


class TriageAgent(Agent):
    """
    Represents a triage agent with specific tools and instructions.
    """
    service_agent: Agent = None
    sales_agent: Agent = None

    def transfer_to_customer_service(self):
        """ Use to transfer the user to customer service agent.
        Use for issues, repairs and refunds.
        """
        return self.service_agent
    
    def transfer_to_sales(self):
        """ Use to transfer the user to sales agent.
        Use for anything sales or buying related.
        """
        return self.sales_agent

    def __init__(self, deployment: str, service_agent: Agent, sales_agent: Agent):
        super().__init__(
            name="Triage Agent",
            deployment=deployment,
            instructions=create_system_message(),
            tools=[self.transfer_to_customer_service, self.transfer_to_sales],
        )
        self.service_agent = service_agent
        self.sales_agent = sales_agent