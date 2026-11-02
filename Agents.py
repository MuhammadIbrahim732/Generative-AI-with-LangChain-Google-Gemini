import os
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, ToolMessage 

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

# Tools
tools = {
    "get_weather": get_weather,
    "get_news": get_news
}

# Tool Binding
llm_with_tool = llm.bind_tools(
    [
        get_weather,
        get_news
    ]
)


# Agent Loop

messages = []

print("----- City Intelligence System -----")
print("Type Exit To Quit...")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(HumanMessage(content=user_input))

    while True:

        # LLM Response
        result = llm_with_tool.invoke(messages)

        messages.append(result)

        # Check Tool Calls
        if result.tool_calls:

            denied = False

            for tool_call in result.tool_calls:

                tool_name = tool_call["name"]

                # Human In The Loop
                confirm = input(
                    f"Agent wants to call {tool_name}. Approve (y/n): "
                )

                if confirm.lower() != "y":

                    messages.append(
                        ToolMessage(
                            content="Tool execution denied by user.",
                            tool_call_id=tool_call["id"]
                        )
                    )

                    denied = True
                    continue

                # Tool Execution
                tool_result = tools[tool_name].invoke(
                    tool_call["args"]
                )

                # Tool Response
                messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call["id"]
                    )
                )

            continue

        # Final AI Response
        else:

            print("AI:", result.text)
            break
