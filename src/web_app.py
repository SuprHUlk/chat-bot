#!/usr/bin/env python
"""
Web application for the CDP Support Agent Chatbot.
This script runs a FastAPI server that serves the web interface and provides the chatbot API.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

from src.chatbot import CDPChatbot

# Initialize FastAPI app
app = FastAPI(title="CDP Support Agent Chatbot")

# Get the directory of the current file
current_dir = Path(__file__).parent.absolute()

# Mount static files
static_dir = current_dir / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize chatbot
chatbot = CDPChatbot()

# Define request model
class Question(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve the home page"""
    return FileResponse(static_dir / "index.html")

@app.post("/ask")
async def ask_question(question: Question):
    """Process a question and return the chatbot's response"""
    try:
        response = chatbot.answer_question(question.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

def main():
    """Run the web application"""
    # Create the static directory if it doesn't exist
    os.makedirs(static_dir, exist_ok=True)
    
    # Print access information
    print("\n" + "="*50)
    print("CDP Support Agent Chatbot Web Interface")
    print("="*50)
    print("Server starting up...")
    print("Access the web interface at: http://localhost:8000 or http://127.0.0.1:8000")
    print("Note: Do not use http://0.0.0.0:8000 in your browser")
    print("="*50 + "\n")
    
    # Run the FastAPI server
    uvicorn.run("src.web_app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main() 