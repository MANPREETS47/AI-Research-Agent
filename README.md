# AI Research Agent 🔍

## Multi-source research chatbot that gathers information from Google, Bing, and Reddit, analyzes the results, and provides concise, human-friendly answers.

Features

- Multi-source Research: Simultaneously searches Google, Bing, and Reddit for relevant content.

- Analysis & Synthesis: Summarizes and synthesizes search results using a powerful LLM (ChatGroq).

- Human-friendly Responses: Generates easy-to-read final answers for user queries.

- Streamlit Frontend: Interactive chat interface for real-time questions and answers.

- State Management: Uses LangGraph for structured flow and state handling of queries and results.

## Tech Stack

- Backend: Python, LangGraph, LangChain-Groq, DDGS (DuckDuckGo Search)

- Frontend: Streamlit

- LLM: ChatGroq (OpenAI GPT OSS 20B)

- Other Libraries: pydantic, typing_extensions, dotenv

# Installation

1. Clone the repository
   ```
   git clone <your-repo-url>
   cd ai-research-agent
   ```
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```
   .venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```






