from rich import print 
from dotenv import load_dotenv
from langchain.tools import tool 
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Creating Tool
@tool
def get_text_length(text: str) -> int:
    """Returns the number of character in a given text"""
    return len(text)

tools = {
    "get_text_length" : get_text_length
}

# LLM
llm =  ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite"
)

# Tool Binding
llm_with_tool = llm.bind_tools(
    [
        get_text_length
    ]
)

# Message History
message = []
prompt = input("You: ")
query = HumanMessage(prompt)
message.append(query)

# Tool Calling
result = llm_with_tool.invoke(message)
message.append(result)

# Tool Execution
if result.tool_calls:
    tool_name = result.tool_calls[0]["name"]
    tool_message = tools[tool_name].invoke(result.tool_calls[0])
    message.append(tool_message)
   
# Sending the result back to the LLM
result = llm_with_tool.invoke(message)

print(result.content)