# 🤖 Generative AI with LangChain & Google Gemini

A collection of hands-on Generative AI examples built with **LangChain** and **Google Gemini**. The scripts progress from basic chat and embeddings to runnable chains, structured output, tool calling, and human-in-the-loop AI agents.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📚 What's Inside

### 💬 Chat & Embeddings

| File           | Description                                                              |
| -------------- | ------------------------------------------------------------------------ |
| `chat.py`      | Terminal chatbot with conversation history and a system prompt (Python teacher persona) |
| `embedding.py` | Generate text embeddings with `gemini-embedding-2` (64 dimensions)       |

### 🧾 Structured Output

| File      | Description                                                                                             |
| --------- | ------------------------------------------------------------------------------------------------------- |
| `core.py` | Extract structured movie data (title, year, genre, director, cast, rating, summary) from free text using a Pydantic model and `PydanticOutputParser` |

### 🔗 Runnables & Chains (LCEL)

| File                      | Description                                                              |
| ------------------------- | ------------------------------------------------------------------------ |
| `sequence_Runnables.py`   | Sequential chain: `prompt \| model \| parser`                            |
| `parallel_Runnables.py`   | `RunnableParallel` runs a short and a detailed explanation at the same time |
| `lambda_Runnables.py`     | `RunnableLambda` routes different inputs to each parallel branch         |
| `newsummarizer.py`        | Fetches the latest news with Tavily Search and summarizes it into bullet points |

### 🛠️ Tools & Agents

| File              | Description                                                                              |
| ----------------- | ---------------------------------------------------------------------------------------- |
| `custom_tool.py`  | Create a custom tool with the `@tool` decorator                                          |
| `tool_calling.py` | Bind a tool to the LLM, let it decide when to call it, and send the result back          |
| `Agents.py`       | **Manual agent loop**: City Intelligence System with weather and news tools and human approval (`y/n`) before each tool call |
| `Agents_auto.py`  | **Automated agent** built with `create_agent` and middleware (`@wrap_tool_call`) for human approval |

---

## 🌆 Featured Project: City Agent

The agent scripts (`Agents.py`, `Agents_auto.py`) answer questions about any city using two tools:

| Tool          | Source           | Purpose                                            |
| ------------- | ---------------- | -------------------------------------------------- |
| `get_weather` | OpenWeatherMap   | Temperature, feels-like, humidity, wind, condition |
| `get_news`    | Tavily           | Latest news and updates (top 3 results)            |

Before any tool runs, the agent **asks for your approval**. This human-in-the-loop step is written by hand in `Agents.py` and with LangChain middleware in `Agents_auto.py`.

```
You: What's the weather in Lahore and any news?
Agent wants to call get_weather. Approve (y/n): y
Agent wants to call get_news. Approve (y/n): y
AI: Lahore is currently ...
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The scripts also import `tavily-python`, `requests`, `rich`, and `pydantic`, so make sure these are in your `requirements.txt` too:

```
langchain
langchain-core
langchain-community
langchain-google-genai
python-dotenv
pydantic
tavily-python
requests
rich
```

### 4. Add your API keys

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

| Key                   | Needed for                          | Get it from                                              |
| --------------------- | ----------------------------------- | -------------------------------------------------------- |
| `GOOGLE_API_KEY`      | All scripts                         | [Google AI Studio](https://aistudio.google.com/apikey)   |
| `TAVILY_API_KEY`      | `newsummarizer.py`, agents          | [Tavily](https://tavily.com)                             |
| `OPENWEATHER_API_KEY` | `Agents.py`, `Agents_auto.py`       | [OpenWeatherMap](https://openweathermap.org/api)         |

### 5. Run any script

```bash
python chat.py
python core.py
python parallel_Runnables.py
python Agents_auto.py
```

---

## 🧰 Concepts Covered

- Chat models and message history (`SystemMessage`, `HumanMessage`, `AIMessage`)
- Prompt templates (`ChatPromptTemplate`)
- Output parsers (`StrOutputParser`, `PydanticOutputParser`)
- LangChain Expression Language (LCEL): sequence, parallel, and lambda runnables
- Text embeddings
- Custom tools and tool binding (`bind_tools`)
- Tool-calling loops
- AI agents with `create_agent`
- Human-in-the-loop approval and middleware
- Web search with Tavily

---

## 🛠️ Tech Stack

- **Python**
- **LangChain**: framework
- **Google Gemini** (`gemini-3.5-flash-lite`, `gemini-embedding-2`): LLM and embeddings
- **Tavily**: web and news search
- **OpenWeatherMap**: weather data
- **Pydantic**: schema validation
- **Rich**: terminal output

---

## 🔗 Related Project

Looking for a full app built on these concepts? See the **Ask Your PDF** RAG chatbot (FastAPI + ChromaDB + Gemini).

---

## 👤 Author

**Ibrahim**
BS Software Engineering, National Textile University (NTU), Faisalabad

🔗 [LinkedIn](https://linkedin.com/in/muhammad-ibrahim-python)

---

## 📄 License

This project is licensed under the MIT License.
