from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from oracle_ebs_chatbot import OracleEBSChatbot
import asyncio

app = FastAPI(title="Oracle EBS R12 Assistant", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chatbot with your API key
API_KEY = "AIzaSyC8pw11h7ppDilnA-ITc8-SmF8daANOhIw"
chatbot = None

@app.on_event("startup")
async def startup_event():
    global chatbot
    chatbot = OracleEBSChatbot(API_KEY)
    print("Oracle EBS Chatbot initialized successfully")

class ChatMessage(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

@app.get("/")
async def root():
    return {"message": "Oracle EBS R12 Assistant API", "status": "running"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    """Chat endpoint for Oracle EBS R12 questions"""
    if not chatbot:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    
    try:
        response = await chatbot.get_response(chat_message.message)
        return ChatResponse(
            response=response,
            session_id=chat_message.session_id
        )
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/api/welcome")
async def get_welcome():
    """Get welcome message"""
    if not chatbot:
        return {"message": "Oracle EBS R12 Assistant initializing..."}
    return {"message": chatbot.get_welcome_message()}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Oracle EBS R12 Assistant"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)