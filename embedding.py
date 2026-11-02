from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(
    model = "gemini-embedding-2",
    dimensions = 64
)

vector = embeddings.embed_query(
    "What is VsCode?"
)

print(vector)