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







