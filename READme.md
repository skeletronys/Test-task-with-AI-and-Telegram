# AI Telegram Car Consultant

An AI-powered Telegram bot that acts as a smart car dealership assistant.

---

## Features

- Chat via Telegram with a GPT-based agent
- Short-term memory (context-aware)
- Search answers in uploaded knowledge
- Google search via `/search` command using SerpAPI

---

## Used Libraries

| Library                  | Description                            |
|--------------------------|----------------------------------------|
| `langchain`              | Framework for building LLM-powered apps |
| `faiss-cpu`              | Fast vector search engine (FAISS)      |
| `OpenAIEmbeddings`       | Transforms text into numerical vectors |
| `CharacterTextSplitter`  | Splits large text into chunks          |
| `ConversationBufferMemory` | Stores short conversation context     |
| `telebot`                | Telegram bot API                       |
| `dotenv`                 | Loads environment variables from `.env` |
| `serpapi`                | Google Search API for real-time results |

---

## Installation

```bash
git clone https://github.com/yourname/project.git
cd project
pip install -r requirements.txt
