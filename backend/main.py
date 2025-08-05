from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import uuid
from datetime import datetime
import os

from .models import ChatRequest, ChatResponse, SessionState, WorkflowStep
from .oracle_agent import OracleEBSAgent
from .session_manager import SessionManager

app = FastAPI(
    title="Oracle EBS R12 i-Supplier Assistant",
    description="AI-powered assistant for Tanger Med Oracle EBS R12 i-Supplier portal",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="/workspace/static"), name="static")

# Initialize components
session_manager = SessionManager()
oracle_agent = OracleEBSAgent()

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    await oracle_agent.initialize()
    print("Oracle EBS Assistant started successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Oracle EBS R12 i-Supplier Assistant"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for user interactions"""
    try:
        # Get or create session
        session = session_manager.get_session(request.session_id)
        
        # Process the user message with the Oracle agent
        response = await oracle_agent.process_message(
            message=request.message,
            session=session,
            context=request.context or {}
        )
        
        # Update session state
        session_manager.update_session(request.session_id, response.session_state)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/procedures")
async def get_procedures():
    """Get all available procedures"""
    try:
        procedures = oracle_agent.get_available_procedures()
        return {"procedures": procedures}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/procedures/{procedure_id}")
async def get_procedure(procedure_id: str):
    """Get details of a specific procedure"""
    try:
        procedure = oracle_agent.get_procedure_details(procedure_id)
        if not procedure:
            raise HTTPException(status_code=404, detail="Procedure not found")
        return procedure
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/oracle/query")
async def oracle_query(request: dict):
    """Query Oracle EBS modules (mocked for now)"""
    try:
        module = request.get("module")
        query_type = request.get("query_type")
        parameters = request.get("parameters", {})
        
        result = await oracle_agent.query_oracle_module(module, query_type, parameters)
        return {"result": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}/progress")
async def get_session_progress(session_id: str):
    """Get current workflow progress for a session"""
    try:
        session = session_manager.get_session(session_id)
        return {
            "session_id": session_id,
            "current_procedure": session.current_procedure,
            "current_step": session.current_step,
            "completed_steps": session.completed_steps,
            "workflow_data": session.workflow_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/session/{session_id}/reset")
async def reset_session(session_id: str):
    """Reset a session's workflow progress"""
    try:
        session_manager.reset_session(session_id)
        return {"message": "Session reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/validation/{procedure_id}")
async def get_validation_rules(procedure_id: str):
    """Get validation rules for a specific procedure"""
    try:
        rules = oracle_agent.get_validation_rules(procedure_id)
        return {"procedure_id": procedure_id, "validation_rules": rules}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)