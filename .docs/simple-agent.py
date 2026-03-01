from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()

from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime


@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@dataclass
class Context:
    """Custom runtime context schema."""

    user_id: str


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always rainy in {city}!"


SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_weather],
    system_prompt=SYSTEM_PROMPT,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "who gonna be the next pm of india?"}]}
)

print(result["messages"][-1].content)
