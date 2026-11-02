from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

class Movie(BaseModel): #Schema
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

parser = PydanticOutputParser(
    pydantic_object=Movie
)

model = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash-lite",   
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract Movie Information from the paragraph.\n{format_instructions}"),
    ("human", "{paragraph}")
])

para = input("Paste Your Paragraph: ")

final_prompt = prompt.invoke(
    {"paragraph": para,
     "format_instructions": parser.get_format_instructions()
    }
)

response = model.invoke(final_prompt)

print(response.content)