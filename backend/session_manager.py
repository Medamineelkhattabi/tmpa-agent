import uuid
from typing import Dict, Optional
from datetime import datetime, timedelta
import json

from backend.models import SessionState, WorkflowStatus

class SessionManager:
    """
    Manages user sessions and workflow state persistence.
    In production, this would use a database or Redis for persistence.
    """
    
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}
        self.session_timeout = timedelta(hours=24)  # Sessions expire after 24 hours
        
    def get_session(self, session_id: str) -> SessionState:
        """Get existing session or create new one"""
        
        # Clean up expired sessions
        self._cleanup_expired_sessions()
        
        if session_id in self.sessions:
            session = self.sessions[session_id]
            # Check if session is expired
            if datetime.now() - session.updated_at > self.session_timeout:
                # Session expired, create new one
                del self.sessions[session_id]
                return self._create_new_session(session_id)
            return session
        else:
            return self._create_new_session(session_id)
            
    def _create_new_session(self, session_id: str) -> SessionState:
        """Create a new session with default state"""
        session = SessionState(
            session_id=session_id,
            status=WorkflowStatus.NOT_STARTED,
            preferred_language='en',
            language='en',
            conversation_history=[],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.sessions[session_id] = session
        return session
        
    def update_session(self, session_id: str, session_state: SessionState):
        """Update existing session state"""
        session_state.updated_at = datetime.now()
        self.sessions[session_id] = session_state
        
    def reset_session(self, session_id: str):
        """Reset session to initial state"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            # Preserve language preference when resetting
            preferred_lang = getattr(session, 'preferred_language', 'en')
            current_lang = getattr(session, 'language', preferred_lang)
            session.current_procedure = None
            session.current_step = None
            session.completed_steps = []
            session.workflow_data = {}
            session.status = WorkflowStatus.NOT_STARTED
            session.preferred_language = preferred_lang
            session.language = current_lang
            session.updated_at = datetime.now()
            
    def delete_session(self, session_id: str):
        """Delete a session completely"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            
    def get_all_sessions(self) -> Dict[str, SessionState]:
        """Get all active sessions (for admin purposes)"""
        self._cleanup_expired_sessions()
        return self.sessions.copy()
        
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if current_time - session.updated_at > self.session_timeout:
                expired_sessions.append(session_id)
                
        for session_id in expired_sessions:
            del self.sessions[session_id]
            
    def get_session_stats(self) -> Dict[str, int]:
        """Get statistics about active sessions"""
        self._cleanup_expired_sessions()
        
        stats = {
            "total_sessions": len(self.sessions),
            "active_procedures": 0,
            "completed_procedures": 0,
            "not_started": 0
        }
        
        for session in self.sessions.values():
            if session.status == WorkflowStatus.IN_PROGRESS:
                stats["active_procedures"] += 1
            elif session.status == WorkflowStatus.COMPLETED:
                stats["completed_procedures"] += 1
            elif session.status == WorkflowStatus.NOT_STARTED:
                stats["not_started"] += 1
                
        return stats
        
    def export_session_data(self, session_id: str) -> Optional[Dict]:
        """Export session data for backup/analysis"""
        if session_id not in self.sessions:
            return None
            
        session = self.sessions[session_id]
        return {
            "session_id": session.session_id,
            "current_procedure": session.current_procedure,
            "current_step": session.current_step,
            "completed_steps": session.completed_steps,
            "workflow_data": session.workflow_data,
            "status": session.status.value,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat()
        }
        
    def import_session_data(self, session_data: Dict) -> bool:
        """Import session data from backup"""
        try:
            session = SessionState(
                session_id=session_data["session_id"],
                current_procedure=session_data.get("current_procedure"),
                current_step=session_data.get("current_step"),
                completed_steps=session_data.get("completed_steps", []),
                workflow_data=session_data.get("workflow_data", {}),
                status=WorkflowStatus(session_data.get("status", "not_started")),
                preferred_language=session_data.get("preferred_language", "en"),
                created_at=datetime.fromisoformat(session_data["created_at"]),
                updated_at=datetime.fromisoformat(session_data["updated_at"])
            )
            self.sessions[session.session_id] = session
            return True
        except Exception as e:
            print(f"Error importing session data: {e}")
            return False