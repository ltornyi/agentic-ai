from pydantic import BaseModel

from utils import function_to_schema

class Agent(BaseModel):
    """
    Represents an agent with a name and an Azure openAI deployment name.
    """

    name: str
    deployment: str
    instructions: str
    tools: list
    tools_map: dict = {}
    tool_schemas: list = []

    def __init__(self, name: str, deployment: str, instructions: str = "You are a helpful assistant.", tools: list = []):
        """
        Initializes the Agent with a name, deployment, instructions, and tools.
        :param name: The name of the agent.
        :param deployment: The Azure OpenAI deployment name.
        :param instructions: Instructions for the agent.
        :param tools: List of tools that the agent can use.
        """
        super().__init__(name=name, deployment=deployment, instructions=instructions, tools=tools)
        self.tools_map = {tool.__name__: tool for tool in tools}
        self.tool_schemas = [function_to_schema(tool) for tool in tools]

    def add_tool(self, tool):
        """
        Adds a tool to the agent.
        :param tool: The tool to add.
        """
        self.tools.append(tool)
        self.tools_map[tool.__name__] = tool
        self.tool_schemas.append(function_to_schema(tool))