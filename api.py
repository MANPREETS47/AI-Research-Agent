from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import graph
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    thread_id: str = "1"

class QueryResponse(BaseModel):
    answer: str
    
@app.post("/query")
async def handle_query(request: QueryRequest):
    state = {
        "messages": [{"role": "user", "content": request.question}],
        "user_question": request.question,
        "web_results": None,
        "reddit_results": None,
        "web_analysis": None,
        "reddit_analysis": None,
        "final_answer": None,
        "final_ans_framer": None,
    }
    
    config = {"configurable": {"thread_id": request.thread_id}}

    async def event_stream():
        # Run the sync graph in a thread to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(None, lambda: graph.invoke(state, config))
        
        answer = final_state.get("final_ans_framer") or final_state.get("final_answer") or "Sorry, I couldn't find an answer."
        
        # Stream the answer word by word
        words = answer.split(" ")
        for word in words:
            yield word + " "
            await asyncio.sleep(0.03)

    return StreamingResponse(event_stream(), media_type="text/plain")