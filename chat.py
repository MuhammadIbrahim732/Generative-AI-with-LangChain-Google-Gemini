from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 

model = init_chat_model("gemini-3.5-flash-lite",model_provider="google_genai")

messages = [
    SystemMessage(content="You are a Experienced Python Teacher"),

]

print("----------Welcome Type 0 to exit the application")
while True:
    prompt = input("You: ")
    if prompt == "0":
        break
    messages.append(HumanMessage(content = prompt))
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.text))
    print("bot: ", response.text)

