from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import TavilySearchResults

load_dotenv()

search_tool = TavilySearchResults(max_results = 5)

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite"
)

prompt = ChatPromptTemplate.from_template(
    """
you are a helpful assistant that summarizes news into clear bullet points with bold headings.
{news}
"""
)

chain = prompt | llm | StrOutputParser()

news_result = search_tool.run("Latest AI news of 2026")

result = chain.invoke(
    {
        "news": news_result
    }
)

print(news_result)