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

load_dotenv()

checkpointer = MemorySaver()
llm = ChatGroq(model="openai/gpt-oss-20b")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_question: str | None
    google_results: list | None
    bing_results: list | None
    reddit_results: list | None
    # selected_reddit_urls: list[str] | None
    # reddit_posts_data: list | None
    google_analysis: str | None
    bing_analysis: str | None
    reddit_analysis: str | None
    final_answer: str | None
    final_ans_framer: str | None


def google_search(state: State):
    user_question = state.get("user_question", "")
    print(f"Searching Google for: {user_question}")
    google_results = []

    with DDGS() as ddgs:
        for r in ddgs.text(user_question, max_results=5):
            google_results.append(r)

    return {"google_results": google_results}

def bing_search(state: State):
    user_question = state.get("user_question", "")
    print(f"Searching bing for: {user_question}")
    bing_results = []

    with DDGS() as ddgs:
        for r in ddgs.text(user_question, max_results=5):
            bing_results.append(r)


    return {"bing_results": bing_results}


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

# def analyze_reddit_posts(state: State):
#     return

# def retrieve_reddit_posts(state: State):
#     return

def analyze_google_results(state: State):
    google_results = state.get("google_results", [])
    # Perform analysis on Google results
    user_question = state.get("user_question", "")
    print(f"Analyzing Google results for question: {user_question}\n")
    messages = [
        SystemMessage(content="You are an expert research analyst."),
        HumanMessage(content=f"Analyze the following Google search results and provide a concise summary relevant to the question: {user_question}\n\nResults:\n{google_results}"),
    ]

    response = llm.invoke(messages)

    return {"google_analysis": response.content}

def analyze_bing_results(state: State):
    bing_results = state.get("bing_results", [])
    # Perform analysis on Bing results
    user_question = state.get("user_question", "")
    print(f"Analyzing Bing results for question: {user_question}\n")
    messages = [
        SystemMessage(content="You are an expert research analyst."),
        HumanMessage(content=f"Analyze the following Bing search results and provide a concise summary relevant to the question: {user_question}\n\nResults:\n{bing_results}"),
    ]

    response = llm.invoke(messages)

    return {"bing_analysis": response.content}

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
    google_analysis = state.get("google_analysis", "")
    bing_analysis = state.get("bing_analysis", "")
    reddit_analysis = state.get("reddit_analysis", "")

    messages = [
        SystemMessage(content="You are an expert research analyst."),
        HumanMessage(content=f"Please synthesize the following analyses into a cohesive summary:\n\nGoogle Analysis:\n{google_analysis}\n\nBing Analysis:\n{bing_analysis}\n\nReddit Analysis:\n{reddit_analysis}"),
    ]

    response = llm.invoke(messages)

    return {"final_answer": response.content}

def final_ans_framer(state: State):
    final_answer = state.get("final_answer", "")
    user_question = state.get("user_question", "")
    print(f"Framing final answer for question: {user_question}")

    messages = [
        SystemMessage(content="You are an expert research analyst."),
        HumanMessage(content=f"Please provide a final answer to the question which should be easily human readable: {user_question}\n\nBased on the following synthesized analysis:\n{final_answer}"),
    ]

    response = llm.invoke(messages)

    return {"final_ans_framer": response.content}

graph_builder = StateGraph(State)

graph_builder.add_node("google_search", google_search)
graph_builder.add_node("bing_search", bing_search)
graph_builder.add_node("reddit_search", reddit_search)
# graph_builder.add_node("analyze_reddit_posts", analyze_reddit_posts)
# graph_builder.add_node("retrieve_reddit_posts", retrieve_reddit_posts)
graph_builder.add_node("analyze_google_results", analyze_google_results)
graph_builder.add_node("analyze_bing_results", analyze_bing_results)
graph_builder.add_node("analyze_reddit_results", analyze_reddit_results)
graph_builder.add_node("synthesize_analyses", synthesize_analyses)
graph_builder.add_node("final_ans_framer", final_ans_framer)

graph_builder.add_edge(START, "google_search")
graph_builder.add_edge(START, "bing_search")
graph_builder.add_edge(START, "reddit_search")
graph_builder.add_edge("google_search", "analyze_google_results")
graph_builder.add_edge("bing_search", "analyze_bing_results")
graph_builder.add_edge("reddit_search", "analyze_reddit_results")
# graph_builder.add_edge("analyze_reddit_posts", "retrieve_reddit_posts")
# graph_builder.add_edge("retrieve_reddit_posts", "analyze_google_results")
# graph_builder.add_edge("retrieve_reddit_posts", "analyze_bing_results")
# graph_builder.add_edge("retrieve_reddit_posts", "analyze_reddit_results")
graph_builder.add_edge("analyze_google_results", "synthesize_analyses")
graph_builder.add_edge("analyze_bing_results", "synthesize_analyses")
graph_builder.add_edge("analyze_reddit_results", "synthesize_analyses")
graph_builder.add_edge("synthesize_analyses", "final_ans_framer")
graph_builder.add_edge("final_ans_framer", END)

graph = graph_builder.compile(checkpointer=checkpointer)

# def run_chatbot():
#     print("Multi_Source Research Agent")
#     print("Type 'exit' to quit\n'")

#     while True:
#         user_input = input("Ask me anything: ")
#         if user_input.lower() == "exit":
#             print("Bye")
#             break

#         state = {
#             "messages": [{"role": "user", "content": user_input}],
#             "user_question": user_input,
#             "google_results": None,
#             "bing_results": None,
#             "reddit_results": None,
#             # "selected_reddit_urls": None,
#             # "reddit_posts_data": None,
#             "google_analysis": None,
#             "bing_analysis": None,
#             "reddit_analysis": None,
#             "final_answer": None,
#             "final_ans_framer": None,
#         }

#         print("\n Starting parallel research process...")
#         print("Launching Google, Bing, and Reddit searches...\n")
#         final_state = graph.invoke(state)

#         if final_state.get("final_answer"):
#             print(f"\n Final Answer:\n{final_state.get('final_answer')}")

#         print("-" * 80)

# if __name__ == "__main__":
#     run_chatbot()

