from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import graph
from fastapi.responses import StreamingResponse
import asyncio
import json
from proxi import get_current_user
from schema import RegisterRequest
from auth import hash_password
from models import Chat, User
from database import SessionLocal, engine, Base
from schema import LoginRequest
from auth import verify_password, create_access_token
from fastapi import HTTPException, Depends
from sqlalchemy.exc import IntegrityError

Base.metadata.create_all(bind=engine)

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

@app.post("/register")
def register(user: RegisterRequest):
    db = SessionLocal()
    try:
        hashed_password = hash_password(user.password)

        new_user = User(
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()

        return {"message": "User created"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        db.close()

@app.post("/login")
def login(request: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.id})

        return {"access_token": token}
    finally:
        db.close()

@app.get("/chats")
def get_chats(user_id: str = Depends(get_current_user)):

    db = SessionLocal()

    chats = db.query(Chat).filter(Chat.user_id == user_id).all()

    return {"chats": [{"id": chat.id, "title": chat.title} for chat in chats]}