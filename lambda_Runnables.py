from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda

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
        "Short" : RunnableLambda(lambda x: x["Short"]) | short_prompt | model | parser,
        "Detailed" : RunnableLambda(lambda x: x["Detailed"]) | detailed_prompt | model | parser
    }
)

result = chain.invoke({
    "Short": {"topic": "Machine Learning"},
    "Detailed": {"topic": "Deep Machine"}
})
print(result)


