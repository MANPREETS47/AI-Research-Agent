# AI Research Agent 🔍

## An intelligent AI-powered research assistant that performs structured research across multiple sources, analyzes information, and produces clear, concise answers in real time. Built with LangGraph, FastAPI, React, and modern LLM tooling, this system combines conversational AI with automated research workflows.

🚀 Features
🧠 Intelligent Query Classification

The system first determines whether the user query is:

Casual conversation

General knowledge

Research-oriented

This prevents unnecessary searches and improves response speed.

🔎 Multi-Source Research

For research questions, the agent automatically gathers information from:

🌐 Web search (Tavily)

💬 Community insights (Reddit)

These sources are analyzed and synthesized before producing a final answer.

💬 Persistent Chat Sessions

Users can:

Create new chats

Resume previous conversations

View chat history in a sidebar

Each chat is securely linked to the authenticated user.

🔐 Authentication System

Supports:

Email & Password login

Google OAuth login

JWT tokens are used to secure all API endpoints.

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

## Usage
Run the backend
```
python main.py
```
Run the frontend
```
streamlit run chatbot_frontend.py
```

## Project Structure
```
├── main.py          # Backend: AI Research Agent logic
├── app.py           # Streamlit frontend
├── requirements.txt # Python dependencies
├── .venv/           # Virtual environment
└── README.md
```

## How it works
1. User Input: The user asks a question through the chat interface.

2. Search Phase: The agent performs searches on Google, Bing, and Reddit.

3. Analysis Phase: Each search result is analyzed and summarized individually.

4. Synthesis Phase: All individual analyses are combined into a cohesive final answer.

5. Framing Phase: The final answer is refined for readability and presented to the user.








