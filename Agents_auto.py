import os
import requests

from rich import print
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

# Weather Tool
@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a given city.
    Input: City name, for example Faisalabad or Lahore.
    """

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        return f"""
        Weather in {city}:

        Temperature: {temperature}°C
        Feels Like: {feels_like}°C
        Condition: {description}
        Humidity: {humidity}%
        Wind Speed: {wind_speed} m/s
        """

    except requests.exceptions.HTTPError:
        return "City not found or weather API request failed."

    except requests.exceptions.RequestException as e:
        return f"Weather service error: {e}"

###
###

# Tavily News Tool
tavily_client = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city: str) -> str:
    """
    Get the latest news and updates about any city.
    Input: City name, e.g. Faisalabad, Lahore, London.
    """

    response = tavily_client.search(
        query = f"Latest news and updates in {city}",
        topic = "news",
        max_results = 3,
        search_depth = "basic"
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}."

    output = []

    for result in results:
        output.append(
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Content: {result['content']}\n"
        )

    return "\n".join(output)

print(get_news.invoke("Lahore"))

# LLM
llm = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite"
)

# Wrap Tool Call
@wrap_tool_call
def human_approval(request, handler):
    """ Ask For Human Approval Beofore Every Tool Call."""

    tool_name = request.tool_call["name"]
    confirm = input(f"Agent wants to call {tool_name}. Approve? (yes/no):  ")

    if confirm.lower() != "yes":
        return ToolMessage(
            content = "Tool Call denied by user.",
            tool_call_id = request.tool_call["id"]
        )

    return handler(request)

# Agent
agent = create_agent(
    model = llm,
    tools = [
        get_news,
        get_weather
    ],
    system_prompt = "You are a helpful City Assistant.",
    middleware = [
        human_approval
    ]
)

print("----- City Agent -----")
print("Type Exit to Quit..")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = agent.invoke(
        {
            "messages" : [{
                "role" : "user",
                "content" : user_input
            }]
        }
    )

    print(result["messages"][-1].content)





