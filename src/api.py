from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.chatbot import CDPChatbot

app = FastAPI()
chatbot = CDPChatbot()

class Question(BaseModel):
    text: str

@app.post("/ask")
async def ask_question(question: Question):
    try:
        response = chatbot.answer_question(question.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 