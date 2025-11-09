from langchain.agents import create_agent
from langchain_ollama import ChatOllama


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = ChatOllama(model="llama3-groq-tool-use:8b", base_url="http://groucho:11434")
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a weather agent.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Tokyo?"}]}
)

for message in result["messages"]:
    print(type(message).__name__, message.content)
