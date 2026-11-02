from langchain.tools import tool

@tool
def greet(name: str) -> str:
    """Generate a Greeting Message for a user"""
    return f"Hello {name}, Welcome To Home"


result = greet.invoke(
    {
       "name": "Ibrahim"
    }
)

print(result)