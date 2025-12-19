from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import your combined chain (RAG + memory)
from src.combined_chain import CombinedLegalChatbot

app = FastAPI(title="Legal Aid Chatbot - Quick Test API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allow all origins (dev only)
    allow_credentials=True,
    allow_methods=["*"],     # <-- MUST include OPTIONS
    allow_headers=["*"],
)
# Initialize your chatbot chain
chat_chain = CombinedLegalChatbot()

class ChatRequest(BaseModel):
    user_query: str

@app.post("/chat")
def chat(request: ChatRequest):
    """Return chatbot RAG + memory response."""
    response = chat_chain.generate(request.user_query)
    return {"response": response}

@app.get("/")
def home():
    return {"message": "Chat API is running."}

if __name__ == "__main__":
    uvicorn.run("api_chat_only_check:app", host="0.0.0.0", port=8000, reload=True)
