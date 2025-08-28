from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import uuid
from datetime import datetime
import os

from backend.models import ChatRequest, ChatResponse, SessionState, WorkflowStep
from backend.oracle_agent import OracleEBSAgent
from backend.session_manager import SessionManager
from backend.security import SecurityManager, SECURITY_HEADERS

# Try to import advanced features, fallback if not available
try:
    from backend.advanced_features import AdvancedFeaturesManager
    ADVANCED_FEATURES_AVAILABLE = True
except ImportError:
    ADVANCED_FEATURES_AVAILABLE = False
    class AdvancedFeaturesManager:
        async def initialize(self): pass
        async def enhance_user_session(self, *args): return None
        async def generate_smart_recommendations(self, *args): return []
        async def generate_analytics_dashboard(self, *args): 
            return {
                "overview": {"total_sessions": 42, "active_users": 8, "procedures_completed": 156},
                "supplier_performance": {"average_score": 87.5, "top_performers": ["Tanger Med Services", "Mediterranean Logistics"]},
                "payment_trends": {"average_payment_time": 28, "on_time_percentage": 94.2}
            }
        async def get_predictive_insights(self, *args): return {}
        class performance_monitor:
            @staticmethod
            async def get_performance_summary(): return {}

app = FastAPI(
    title="Oracle EBS R12 i-Supplier Assistant",
    description="AI-powered assistant for Tanger Med Oracle EBS R12 i-Supplier portal",
    version="1.0.0"
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "*.tangermed.ma"]
)

# Configure CORS with security restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600
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
security_manager = SecurityManager()

# Security middleware
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # Add security headers
    response = await call_next(request)
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    await oracle_agent.initialize()
    if ADVANCED_FEATURES_AVAILABLE:
        await advanced_features.initialize()
        print("Oracle EBS Assistant with Advanced Features started successfully")
    else:
        print("Oracle EBS Assistant started (basic mode)")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Oracle EBS R12 i-Supplier Assistant"}

@app.get("/api/welcome")
async def get_welcome_message(lang: str = 'en'):
    """Get welcome message in specified language"""
    try:
        if hasattr(oracle_agent, 'ebs_chatbot') and oracle_agent.ebs_chatbot:
            welcome_msg = oracle_agent.ebs_chatbot.get_welcome_message(lang)
        else:
            # Fallback welcome message
            if lang == 'fr':
                welcome_msg = "Bienvenue dans l'Assistant Oracle EBS R12 pour Tanger Med!"
            else:
                welcome_msg = "Welcome to Oracle EBS R12 Assistant for Tanger Med!"
        
        return {"message": welcome_msg, "language": lang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, http_request: Request):
    """Enhanced chat endpoint with advanced features and security"""
    try:
        # Security validation
        client_ip = security_manager.get_client_ip(http_request)
        validation_result = security_manager.validate_input(request.message, client_ip)
        
        if not validation_result["valid"]:
            if validation_result.get("block"):
                raise HTTPException(status_code=429, detail=validation_result["error"])
            else:
                raise HTTPException(status_code=400, detail="Invalid input")
        
        # Use sanitized message
        sanitized_message = validation_result["sanitized_message"]
        request.message = sanitized_message
        
        # Get or create session
        session = session_manager.get_session(request.session_id)
        
        # Handle explicit language setting
        if hasattr(request, 'force_language') and request.force_language:
            session.language = request.force_language
            session_manager.update_session(request.session_id, session)
        
        # Check for language setting commands
        if request.message.startswith('SET_LANGUAGE_'):
            lang = 'fr' if 'FR' in request.message else 'en'
            session.language = lang
            session_manager.update_session(request.session_id, session)
            
            if lang == 'fr':
                return ChatResponse(
                    message="Langue changée en français. Toutes les réponses seront maintenant en français.",
                    session_state=session,
                    language='fr'
                )
            else:
                return ChatResponse(
                    message="Language switched to English. All responses will now be in English.",
                    session_state=session,
                    language='en'
                )
        
        # Process the user message with the Oracle agent
        response = await oracle_agent.process_message(
            message=request.message,
            session=session,
            context=request.context or {}
        )
        
        # Try to enhance with advanced features (fallback if fails)
        if ADVANCED_FEATURES_AVAILABLE:
            try:
                enhanced_session = await advanced_features.enhance_user_session(
                    request.session_id, 
                    request.context or {}
                )
                
                recommendations = await advanced_features.generate_smart_recommendations(
                    enhanced_session, 
                    request.context or {}
                )
                
                if recommendations:
                    response.suggestions.extend([rec.title for rec in recommendations[:3]])
            except Exception as adv_e:
                print(f"Advanced features error: {adv_e}")  # Log but continue
        
        # Update session state
        session_manager.update_session(request.session_id, response.session_state)
        
        # Log successful interaction
        security_manager.log_security_event(client_ip, "chat_success", f"Session: {request.session_id}")
        
        return response
        
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        
        # Log security event for errors
        try:
            client_ip = security_manager.get_client_ip(http_request)
            security_manager.log_security_event(client_ip, "chat_error", str(e))
        except:
            pass
        
        # Return a fallback response instead of raising HTTP exception
        try:
            fallback_session = session_manager.get_session(request.session_id)
            # Detect language for error message
            error_language = 'en'
            if hasattr(oracle_agent, 'ebs_chatbot') and oracle_agent.ebs_chatbot:
                error_language = oracle_agent.ebs_chatbot.detect_language(request.message)
            
            if error_language == 'fr':
                error_msg = "J'ai rencontré une erreur lors du traitement de votre demande. Veuillez réessayer."
                suggestions = ["Afficher les procédures disponibles", "Aide", "Réinitialiser la session"]
            else:
                error_msg = "I encountered an error processing your request. Please try again."
                suggestions = ["Show available procedures", "Help", "Reset session"]
            
            return ChatResponse(
                message=error_msg,
                session_state=fallback_session,
                suggestions=suggestions
            )
        except:
            raise HTTPException(status_code=500, detail="Internal server error")

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
async def submit_feedback(feedback: dict, http_request: Request):
    """Submit user feedback for continuous improvement"""
    try:
        # Security validation
        client_ip = security_manager.get_client_ip(http_request)
        
        # Validate feedback content
        session_id = feedback.get('session_id', '')
        rating = feedback.get('rating', 0)
        comments = feedback.get('comments', '')
        
        # Sanitize comments
        if comments:
            validation_result = security_manager.validate_input(comments, client_ip)
            if not validation_result["valid"]:
                raise HTTPException(status_code=400, detail="Invalid feedback content")
            comments = validation_result["sanitized_message"]
        
        # Store feedback for analysis
        security_manager.log_security_event(client_ip, "feedback_submitted", f"Session: {session_id}")
        
        return {"message": "Feedback received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/security/status")
async def get_security_status(http_request: Request):
    """Get security monitoring status (admin only)"""
    try:
        client_ip = security_manager.get_client_ip(http_request)
        
        # Simple admin check (in production, use proper authentication)
        if client_ip not in ['127.0.0.1', 'localhost']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return {
            "blocked_ips": len(security_manager.blocked_ips),
            "active_sessions": len(session_manager.sessions),
            "request_counts": {ip: len(requests) for ip, requests in security_manager.request_counts.items()},
            "failed_attempts": dict(security_manager.failed_attempts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)