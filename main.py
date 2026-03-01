from dotenv import load_dotenv
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from ddgs import DDGS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient()
checkpointer = MemorySaver()
llm = ChatGroq(model="openai/gpt-oss-20b",
               streaming=True)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_question: str
    plan: dict | None
    web_results: list | None
    reddit_results: list | None
    web_analysis: str | None
    reddit_analysis: str | None
    final_answer: str | None
    final_ans_framer: str | None
    query_type: str | None
    
class Plan(BaseModel):
    needs_web: bool
    needs_reddit: bool
    needs_deep_research: bool
    answer_type: str
    
class Query_Type(BaseModel):
    category: str
    
def classify_query(state: State):
    question = state["user_question"]
    print(f"Classifying query: {question}✅")

    structured_llm = llm.with_structured_output(Query_Type)

    result = structured_llm.invoke([
        SystemMessage(content="Classify the query as either 'chat' or 'research' for example if user says hello hi or he says that he wants some help for his research then it should be classified as chat."),
        HumanMessage(content=question)
    ])

    return {"query_type": result.category}

def route_query(state: State):
    if state["query_type"] == "chat":
        return ["chat_node"]
    return ["planner"]

def chat_node(state: State):
    conversation = [
        SystemMessage(content="You are a helpful conversational assistant."),
        *state["messages"],
    ]

    response = llm.invoke(conversation)

    return {"final_ans_framer": response.content}
    
def planner(state: State):
    user_question = state["user_question"]

    structured_llm = llm.with_structured_output(Plan)

    plan = structured_llm.invoke([
        SystemMessage(content="You are a research planning expert."),
        HumanMessage(content=f"Plan research steps for: {user_question}")
    ])

    return {"plan": plan}

def route_plan(state: State):
    plan = state["plan"]

    routes = []

    if plan.needs_web:
        routes.append("web_search")

    if plan.needs_reddit:
        routes.append("reddit_search")

    return routes

def web_search(state: State):
    query = state["user_question"]

    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return {"web_results": response["results"]}


def reddit_search(state: State):
    user_question = state.get("user_question", "")
    print(f"Searching reddit for: {user_question}")
    reddit_results = []

    with DDGS() as ddgs:
        # ddgs.text does not accept a 'site' kwarg; use a site: filter in the query
        query = f"site:reddit.com {user_question}".strip()
        for r in ddgs.text(query, max_results=5):
            reddit_results.append(r)

    return {"reddit_results": reddit_results}

def analyze_web_results(state: State):
    web_results = state.get("web_results", [])
    user_question = state.get("user_question", "")

    response = llm.invoke([
        SystemMessage(content="You are an expert research analyst."),
        HumanMessage(content=f"Analyze these web results for: {user_question}\n\n{web_results} and keep the only top 3 results which are most relevant to the question")
    ])

    return {"web_analysis": response.content}

def analyze_reddit_results(state: State):
    reddit_results = state.get("reddit_results", [])
    # Perform analysis on Reddit results
    user_question = state.get("user_question", "")
    print(f"Analyzing Reddit results for question: {user_question}")
    messages = [
        SystemMessage(content="You are an expert research analyst."),
        HumanMessage(content=f"Analyze the following Reddit search results and provide a concise summary relevant to the question: {user_question}\n\nResults:\n{reddit_results}"),
    ]

    response = llm.invoke(messages)

    return {"reddit_analysis": response.content}

def synthesize_analyses(state: State):
    web_analysis = state.get("web_analysis", "")
    reddit_analysis = state.get("reddit_analysis", "")

    messages = [
        SystemMessage(content="You are an expert research analyst."),
        HumanMessage(content=f"Please synthesize the following analyses into a cohesive summary:\n\nWeb Analysis:\n{web_analysis}\n\nReddit Analysis:\n{reddit_analysis}"),
    ]

    response = llm.invoke(messages)

    return {"final_answer": response.content}

def final_ans_framer(state: State):
    final_answer = state.get("final_answer", "")
    user_question = state.get("user_question", "")
    print(f"Framing final answer for question: {user_question}")

    messages = [
        SystemMessage(content="""You are a helpful research assistant that provides clear, concise answers."""),
        HumanMessage(content=f"""Question: {user_question}\n\nResearch findings:\n{final_answer}\n\nProvide a clear, concise answer based on these findings.
                     Formatting rules:- Be concise and to the point. Avoid unnecessary filler.
                                    - Use short paragraphs and bullet points for readability.
                                    - Do NOT use Markdown tables unless the user explicitly asks for one.
                                    - Do NOT use HTML tags like <br>.
                                    - Use bold (**text**) sparingly for emphasis on key terms only.
                                    - Keep the answer focused and conversational, not like a Wikipedia article.
                                    - Aim for a response length appropriate to the question — short questions get short answers."""),
    ]

    response = llm.invoke(messages)

    return {"final_ans_framer": response.content}

graph_builder = StateGraph(State)

graph_builder = StateGraph(State)

graph_builder.add_node("classify_query", classify_query)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_node("planner", planner)
graph_builder.add_node("web_search", web_search)
graph_builder.add_node("reddit_search", reddit_search)
graph_builder.add_node("analyze_web_results", analyze_web_results)
graph_builder.add_node("analyze_reddit_results", analyze_reddit_results)
graph_builder.add_node("synthesize_analyses", synthesize_analyses)
graph_builder.add_node("final_ans_framer", final_ans_framer)

graph_builder.add_edge(START, "classify_query")

graph_builder.add_conditional_edges(
    "classify_query",
    route_query,
    ["chat_node", "planner"]
)
graph_builder.add_edge("chat_node", END)
graph_builder.add_conditional_edges(
    "planner",
    route_plan,
    ["web_search", "reddit_search"]
)

graph_builder.add_edge("web_search", "analyze_web_results")
graph_builder.add_edge("reddit_search", "analyze_reddit_results")

graph_builder.add_edge("analyze_web_results", "synthesize_analyses")
graph_builder.add_edge("analyze_reddit_results", "synthesize_analyses")

graph_builder.add_edge("synthesize_analyses", "final_ans_framer")
graph_builder.add_edge("final_ans_framer", END)

graph = graph_builder.compile(checkpointer=checkpointer)

