from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ERROR = "error"

class WorkflowStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"
    ERROR = "error"

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
    session_id: str = Field(..., description="Session identifier")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    force_language: Optional[str] = Field(None, description="Force specific language (en/fr)")
    
class ChatMessage(BaseModel):
    type: MessageType
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None

class WorkflowStep(BaseModel):
    step_id: str
    title: str
    description: str
    instructions: str
    screenshot: Optional[str] = None
    validation_criteria: List[str] = []
    next_steps: List[str] = []
    completed: bool = False
    completion_time: Optional[datetime] = None

class SessionState(BaseModel):
    session_id: str
    current_procedure: Optional[str] = None
    current_step: Optional[str] = None
    completed_steps: List[str] = []
    workflow_data: Dict[str, Any] = {}
    status: WorkflowStatus = WorkflowStatus.NOT_STARTED
    preferred_language: str = 'en'
    language: str = 'en'  # Current session language
    conversation_history: List[Dict[str, str]] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
class ChatResponse(BaseModel):
    message: str = Field(..., description="Assistant's response")
    message_type: MessageType = MessageType.ASSISTANT
    session_state: SessionState
    current_step: Optional[WorkflowStep] = None
    screenshot: Optional[str] = None
    suggestions: List[str] = []
    validation_errors: List[str] = []
    oracle_data: Optional[Dict[str, Any]] = None
    language: Optional[str] = Field('en', description="Response language (en/fr)")
    
class ProcedureInfo(BaseModel):
    procedure_id: str
    title: str
    description: str
    category: str
    prerequisites: List[str]
    estimated_time: Optional[str] = None
    difficulty: Optional[str] = None

class OracleQueryRequest(BaseModel):
    module: str = Field(..., description="Oracle module (purchase_orders, invoices, suppliers)")
    query_type: str = Field(..., description="Type of query to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Query parameters")
    
class OracleQueryResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ValidationRule(BaseModel):
    rule_id: str
    description: str
    rule_type: str
    parameters: Dict[str, Any] = {}
    error_message: str

class ProcedureValidation(BaseModel):
    procedure_id: str
    rules: List[ValidationRule]
    
class ProgressUpdate(BaseModel):
    session_id: str
    procedure_id: str
    step_id: str
    status: WorkflowStatus
    data: Optional[Dict[str, Any]] = None