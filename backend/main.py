from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import uuid
from datetime import datetime
import os

from backend.models import ChatRequest, ChatResponse, SessionState, WorkflowStep
from .oracle_agent import OracleEBSAgent
from .session_manager import SessionManager
from .advanced_features import AdvancedFeaturesManager

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
# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount advanced frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/advanced", StaticFiles(directory=frontend_dir, html=True), name="advanced")


# Initialize components
session_manager = SessionManager()
oracle_agent = OracleEBSAgent()
advanced_features = AdvancedFeaturesManager()

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    await oracle_agent.initialize()
    # await advanced_features.initialize()  # Temporarily disabled
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

@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard(timeframe: str = '7d'):
    """Get comprehensive analytics dashboard"""
    try:
        dashboard = await advanced_features.generate_analytics_dashboard(timeframe)
        return dashboard
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations/{session_id}")
async def get_recommendations(session_id: str):
    """Get AI-powered recommendations for a session"""
    try:
        enhanced_session = await advanced_features.enhance_user_session(session_id, {})
        recommendations = await advanced_features.generate_smart_recommendations(
            enhanced_session, {}
        )
        return {"recommendations": [{
            "type": rec.type,
            "title": rec.title,
            "description": rec.description,
            "confidence": rec.confidence,
            "priority": rec.priority,
            "actions": rec.actions
        } for rec in recommendations]}
    except Exception as e:
        return {"recommendations": []}

@app.get("/api/insights/{session_id}")
async def get_predictive_insights(session_id: str):
    """Get predictive insights for a session"""
    try:
        enhanced_session = await advanced_features.enhance_user_session(session_id, {})
        insights = await advanced_features.get_predictive_insights(enhanced_session, {})
        return {"insights": insights}
    except Exception as e:
        return {"insights": {}}

@app.get("/api/performance/metrics")
async def get_performance_metrics():
    """Get system performance metrics"""
    try:
        metrics = await advanced_features.performance_monitor.get_performance_summary()
        return {"metrics": metrics}
    except Exception as e:
        return {"metrics": {}}

@app.post("/api/feedback")
async def submit_feedback(feedback: dict):
    """Submit user feedback for continuous improvement"""
    try:
        # Process feedback for ML model improvement
        session_id = feedback.get('session_id')
        rating = feedback.get('rating')
        comments = feedback.get('comments')
        
        # Store feedback for analysis
        # In production, this would update ML models
        
        return {"message": "Feedback received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)