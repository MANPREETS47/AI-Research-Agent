# 🧠 Autonomous Research Agent

An intelligent **AI-powered research assistant** that performs structured research across multiple sources, analyzes information, and produces clear, concise answers in real time.

Built with **LangGraph, FastAPI, React, and modern LLM tooling**, this system combines conversational AI with automated research workflows.

---

# 🚀 Features

### 🧠 Intelligent Query Classification
The system first determines whether the user query is:

- Casual conversation
- General knowledge
- Research-oriented

This prevents unnecessary searches and improves response speed.

---

### 🔎 Multi-Source Research

For research questions, the agent automatically gathers information from:

- 🌐 **Web search (Tavily)**
- 💬 **Community insights (Reddit)**

These sources are analyzed and synthesized before producing a final answer.

---

### 🧩 Agentic Research Workflow

Instead of a single prompt, the system runs a **multi-step reasoning pipeline**:

```
User Query
   │
   ▼
Query Classification
   │
   ▼
Research Planning
   │
   ▼
Web / Reddit Retrieval
   │
   ▼
Source Analysis
   │
   ▼
Information Synthesis
   │
   ▼
Final Response
```

This architecture ensures **better reliability and reasoning** compared to a simple chatbot.

---

### ⚡ Real-Time Streaming Responses

Responses are streamed to the frontend as they are generated, creating a **ChatGPT-like interactive experience**.

---

### 💬 Persistent Chat Sessions

Users can:

- Create new chats
- Resume previous conversations
- View chat history in a sidebar

Each chat is securely linked to the authenticated user.

---

### 🔐 Authentication System

Supports:

- Email & Password login
- Google OAuth login

JWT tokens are used to secure all API endpoints.

---

# 🏗️ System Architecture

```
Frontend (React)
        │
        ▼
FastAPI Backend
        │
        ├── Authentication (JWT + Google OAuth)
        │
        ├── Chat API
        │
        ▼
LangGraph Research Agent
        │
        ├── Query Classifier
        ├── Research Planner
        ├── Web Retrieval (Tavily)
        ├── Reddit Retrieval
        ├── Source Analysis
        ├── Response Synthesis
        │
        ▼
Database (SQLite / PostgreSQL)
```

---

# 🛠️ Tech Stack

## Frontend
- React
- TypeScript
- React Markdown
- Streaming Fetch API

## Backend
- FastAPI
- LangGraph
- LangChain
- ChatGroq LLM

## AI Tools
- Tavily (Web Search)
- DDGS (Reddit Search)

## Database
- SQLite (development)
- PostgreSQL (production ready)

## Authentication
- JWT Authentication
- Google OAuth

---

# 📂 Project Structure

```
project-root
│
├── backend
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   ├── oauth.py
│   ├── agent.py
│   └── schemas.py
│
├── frontend
│   ├── src
│   └── components
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/research-agent.git
cd research-agent
```

---

## 2️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
GOOGLE_CLIENT_ID=your_id
GOOGLE_CLIENT_SECRET=your_secret
JWT_SECRET=your_secret
```

Run backend:

```bash
uvicorn main:app --reload
```

---

## 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

# 🧪 Example Queries

The agent can handle queries like:

```
What is a Convolutional Neural Network?

Latest developments in quantum computing

Best programming languages according to developers?

Explain how transformers work in deep learning
```

---

# 📸 Screenshots

*(Add screenshots after UI is finalized)*

- Chat Interface
- Research Response Example
- Chat History Sidebar

---

# 📈 Future Improvements

- Deep research mode with multi-query exploration
- Source citation display
- Vector memory for long-term knowledge
- Research reports generation
- Agent tool expansion

---

# 👨‍💻 Author

Developed by **Manpreet Singh**

Focused on building intelligent AI systems combining:

- LLMs
- Autonomous agents
- Full-stack engineering

---

# ⭐ If You Like This Project

Give the repository a ⭐ on GitHub.

---

# 📜 License

MIT License

---

# 💡 Inspiration

Inspired by systems such as:

- Perplexity AI
- ChatGPT
- Autonomous research agents

---

# 🧠 Final Note

This project demonstrates how **LLM systems can be designed as structured research agents rather than simple chatbots**, enabling more reliable and explainable AI responses.
