from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, Runnable

load_dotenv()

# Prompt Template
short_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in 1-2 lines."
)

detailed_prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in detail."
)

# Model
model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite"
)

# Output Parser
parser = StrOutputParser()

# Chain
chain = RunnableParallel(
    {
        "Short" : short_prompt | model | parser,
        "Detailed" : detailed_prompt | model | parser
    }
)

result = chain.invoke("Machine Learning")
print(result)


