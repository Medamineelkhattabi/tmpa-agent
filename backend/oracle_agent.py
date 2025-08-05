import json
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re

from langchain.agents import AgentType, initialize_agent
from langchain.tools import BaseTool
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain_community.llms.fake import FakeListLLM

from .models import (
    ChatResponse, SessionState, WorkflowStep, MessageType, 
    WorkflowStatus, ProcedureInfo, ValidationRule
)

class OracleEBSAgent:
    """
    Rule-based agent for Oracle EBS R12 i-Supplier procedures.
    Strictly follows predefined procedures and validates user inputs.
    """
    
    def __init__(self):
        self.procedures_data = {}
        self.oracle_modules = {}
        self.validation_rules = {}
        self.mock_oracle_data = {}
        
    async def initialize(self):
        """Initialize the agent with procedures and validation rules"""
        await self._load_procedures()
        await self._load_mock_data()
        
    async def _load_procedures(self):
        """Load procedures from JSON file"""
        try:
            with open('/workspace/procedures.json', 'r') as f:
                data = json.load(f)
                self.procedures_data = data.get('procedures', {})
                self.oracle_modules = data.get('oracle_modules', {})
                self.validation_rules = data.get('validation_rules', {})
        except FileNotFoundError:
            print("Warning: procedures.json not found, using empty procedures")
            
    async def _load_mock_data(self):
        """Load mock Oracle data for testing"""
        self.mock_oracle_data = {
            "purchase_orders": [
                {
                    "po_number": "PO-2024-001",
                    "supplier": "Tanger Med Services",
                    "status": "Approved",
                    "amount": 50000.00,
                    "currency": "MAD",
                    "created_date": "2024-01-15",
                    "delivery_date": "2024-02-15",
                    "description": "IT Services Contract"
                },
                {
                    "po_number": "PO-2024-002", 
                    "supplier": "Mediterranean Logistics",
                    "status": "Pending",
                    "amount": 25000.00,
                    "currency": "MAD",
                    "created_date": "2024-01-20",
                    "delivery_date": "2024-02-20",
                    "description": "Transportation Services"
                }
            ],
            "invoices": [
                {
                    "invoice_number": "INV-2024-001",
                    "po_number": "PO-2024-001",
                    "supplier": "Tanger Med Services",
                    "amount": 12500.00,
                    "status": "Submitted",
                    "submission_date": "2024-01-25"
                }
            ],
            "suppliers": [
                {
                    "supplier_id": "SUP-001",
                    "name": "Tanger Med Services",
                    "status": "Active",
                    "contact_email": "contact@tangermed-services.com",
                    "registration_date": "2023-06-01"
                },
                {
                    "supplier_id": "SUP-002",
                    "name": "Mediterranean Logistics",
                    "status": "Active", 
                    "contact_email": "info@med-logistics.com",
                    "registration_date": "2023-08-15"
                }
            ]
        }
        
    async def process_message(self, message: str, session: SessionState, context: Dict[str, Any] = {}) -> ChatResponse:
        """Process user message and return appropriate response"""
        
        # Analyze user intent
        intent = self._analyze_intent(message.lower())
        
        if intent == "start_procedure":
            return await self._handle_procedure_start(message, session)
        elif intent == "continue_procedure":
            return await self._handle_procedure_continuation(message, session)
        elif intent == "oracle_query":
            return await self._handle_oracle_query(message, session)
        elif intent == "help":
            return await self._handle_help_request(message, session)
        else:
            return await self._handle_general_query(message, session)
            
    def _analyze_intent(self, message: str) -> str:
        """Analyze user message to determine intent"""
        
        # Keywords for different intents
        procedure_keywords = ["create", "start", "begin", "how to", "guide", "step", "procedure"]
        oracle_keywords = ["search", "find", "show", "view", "list", "po", "invoice", "supplier"]
        help_keywords = ["help", "what can", "available", "options", "commands"]
        continue_keywords = ["next", "continue", "done", "completed", "yes", "proceed"]
        
        if any(keyword in message for keyword in help_keywords):
            return "help"
        elif any(keyword in message for keyword in continue_keywords):
            return "continue_procedure"
        elif any(keyword in message for keyword in oracle_keywords):
            return "oracle_query"
        elif any(keyword in message for keyword in procedure_keywords):
            return "start_procedure"
        else:
            return "general"
            
    async def _handle_procedure_start(self, message: str, session: SessionState) -> ChatResponse:
        """Handle request to start a new procedure"""
        
        # Extract procedure from message
        procedure_id = self._extract_procedure_id(message)
        
        if not procedure_id:
            # Show available procedures
            procedures = self.get_available_procedures()
            suggestions = [f"Start {proc['title']}" for proc in procedures[:5]]
            
            return ChatResponse(
                message="I can help you with the following Oracle EBS R12 i-Supplier procedures:\n\n" + 
                       "\n".join([f"• {proc['title']}: {proc['description']}" for proc in procedures]),
                session_state=session,
                suggestions=suggestions
            )
            
        if procedure_id not in self.procedures_data:
            return ChatResponse(
                message=f"I don't have information about the procedure '{procedure_id}'. Please choose from the available procedures.",
                session_state=session,
                suggestions=["Show available procedures"]
            )
            
        # Start the procedure
        procedure = self.procedures_data[procedure_id]
        first_step = procedure['steps'][0] if procedure['steps'] else None
        
        if not first_step:
            return ChatResponse(
                message=f"The procedure '{procedure['title']}' has no defined steps.",
                session_state=session
            )
            
        # Update session state
        session.current_procedure = procedure_id
        session.current_step = first_step['step_id']
        session.status = WorkflowStatus.IN_PROGRESS
        session.updated_at = datetime.now()
        
        # Create workflow step
        workflow_step = WorkflowStep(
            step_id=first_step['step_id'],
            title=first_step['title'],
            description=first_step['description'],
            instructions=first_step['instructions'],
            screenshot=first_step.get('screenshot'),
            validation_criteria=first_step.get('validation_criteria', []),
            next_steps=first_step.get('next_steps', [])
        )
        
        response_message = f"Starting procedure: **{procedure['title']}**\n\n"
        response_message += f"**Prerequisites:**\n"
        for prereq in procedure.get('prerequisites', []):
            response_message += f"• {prereq}\n"
        response_message += f"\n**Step 1: {first_step['title']}**\n"
        response_message += f"{first_step['description']}\n\n"
        response_message += f"**Instructions:** {first_step['instructions']}\n\n"
        response_message += "Type 'done' or 'next' when you've completed this step."
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            current_step=workflow_step,
            screenshot=first_step.get('screenshot'),
            suggestions=["Done with this step", "Show screenshot", "Cancel procedure"]
        )
        
    async def _handle_procedure_continuation(self, message: str, session: SessionState) -> ChatResponse:
        """Handle continuation of current procedure"""
        
        if not session.current_procedure or not session.current_step:
            return ChatResponse(
                message="You don't have an active procedure. Please start a new procedure first.",
                session_state=session,
                suggestions=["Show available procedures"]
            )
            
        procedure = self.procedures_data[session.current_procedure]
        current_step_data = None
        
        # Find current step
        for step in procedure['steps']:
            if step['step_id'] == session.current_step:
                current_step_data = step
                break
                
        if not current_step_data:
            return ChatResponse(
                message="Error: Current step not found in procedure.",
                session_state=session
            )
            
        # Validate step completion if validation criteria exist
        validation_errors = self._validate_step_completion(
            session.current_procedure, 
            session.current_step, 
            session.workflow_data
        )
        
        if validation_errors:
            return ChatResponse(
                message="Please complete the following requirements before proceeding:\n\n" + 
                       "\n".join([f"• {error}" for error in validation_errors]),
                session_state=session,
                validation_errors=validation_errors,
                suggestions=["Retry step", "Show help"]
            )
            
        # Mark current step as completed
        if session.current_step not in session.completed_steps:
            session.completed_steps.append(session.current_step)
            
        # Find next step
        next_steps = current_step_data.get('next_steps', [])
        
        if not next_steps:
            # Procedure completed
            session.status = WorkflowStatus.COMPLETED
            session.current_step = None
            session.updated_at = datetime.now()
            
            return ChatResponse(
                message=f"🎉 Congratulations! You have successfully completed the procedure: **{procedure['title']}**\n\n" +
                       "All steps have been completed. Is there anything else I can help you with?",
                session_state=session,
                suggestions=["Start another procedure", "View purchase orders", "Show available procedures"]
            )
            
        # Move to next step
        next_step_id = next_steps[0]  # Take first next step
        next_step_data = None
        
        for step in procedure['steps']:
            if step['step_id'] == next_step_id:
                next_step_data = step
                break
                
        if not next_step_data:
            return ChatResponse(
                message="Error: Next step not found in procedure.",
                session_state=session
            )
            
        # Update session
        session.current_step = next_step_id
        session.updated_at = datetime.now()
        
        # Create workflow step
        workflow_step = WorkflowStep(
            step_id=next_step_data['step_id'],
            title=next_step_data['title'],
            description=next_step_data['description'],
            instructions=next_step_data['instructions'],
            screenshot=next_step_data.get('screenshot'),
            validation_criteria=next_step_data.get('validation_criteria', []),
            next_steps=next_step_data.get('next_steps', [])
        )
        
        step_number = len(session.completed_steps) + 1
        response_message = f"✅ Step completed!\n\n"
        response_message += f"**Step {step_number}: {next_step_data['title']}**\n"
        response_message += f"{next_step_data['description']}\n\n"
        response_message += f"**Instructions:** {next_step_data['instructions']}\n\n"
        response_message += "Type 'done' or 'next' when you've completed this step."
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            current_step=workflow_step,
            screenshot=next_step_data.get('screenshot'),
            suggestions=["Done with this step", "Show screenshot", "Cancel procedure"]
        )
        
    async def _handle_oracle_query(self, message: str, session: SessionState) -> ChatResponse:
        """Handle Oracle EBS module queries"""
        
        query_type, parameters = self._parse_oracle_query(message)
        
        if not query_type:
            return ChatResponse(
                message="I can help you query Oracle EBS data. Available queries:\n\n" +
                       "• **Purchase Orders**: Search by PO number, supplier, or date range\n" +
                       "• **Invoices**: View invoice status and payment tracking\n" +
                       "• **Suppliers**: Search supplier information and performance\n\n" +
                       "Example: 'Show purchase order PO-2024-001' or 'List all invoices'",
                session_state=session,
                suggestions=["Show purchase orders", "List invoices", "Search suppliers"]
            )
            
        try:
            result = await self.query_oracle_module(query_type['module'], query_type['type'], parameters)
            
            if not result:
                return ChatResponse(
                    message=f"No data found for your query.",
                    session_state=session
                )
                
            # Format response based on module
            formatted_response = self._format_oracle_response(query_type['module'], result)
            
            return ChatResponse(
                message=formatted_response,
                session_state=session,
                oracle_data=result,
                suggestions=["Show more details", "Export data", "New search"]
            )
            
        except Exception as e:
            return ChatResponse(
                message=f"Error querying Oracle data: {str(e)}",
                session_state=session,
                message_type=MessageType.ERROR
            )
            
    async def _handle_help_request(self, message: str, session: SessionState) -> ChatResponse:
        """Handle help and general information requests"""
        
        help_message = """
🤖 **Oracle EBS R12 i-Supplier Assistant for Tanger Med**

I can help you with:

**📋 Procedures & Workflows:**
• Create Work Confirmation
• Submit Invoice
• View Purchase Orders
• Step-by-step guidance with screenshots

**🔍 Oracle EBS Queries:**
• Search Purchase Orders
• View Invoice Status
• Check Supplier Information
• Track Payment Status

**💡 Available Commands:**
• "Start [procedure name]" - Begin a guided procedure
• "Show purchase orders" - Query PO data
• "List invoices" - View invoice information
• "Search suppliers" - Find supplier details
• "Help" - Show this message

**🎯 Current Session:**
"""
        
        if session.current_procedure:
            procedure = self.procedures_data.get(session.current_procedure, {})
            help_message += f"• Active Procedure: {procedure.get('title', 'Unknown')}\n"
            help_message += f"• Current Step: {session.current_step}\n"
            help_message += f"• Completed Steps: {len(session.completed_steps)}\n"
        else:
            help_message += "• No active procedure\n"
            
        help_message += "\nWhat would you like to do?"
        
        return ChatResponse(
            message=help_message,
            session_state=session,
            suggestions=[
                "Start work confirmation",
                "Show purchase orders", 
                "List available procedures",
                "View session progress"
            ]
        )
        
    async def _handle_general_query(self, message: str, session: SessionState) -> ChatResponse:
        """Handle general queries that don't fit other categories"""
        
        # Check if message contains any procedure-related keywords
        procedures = self.get_available_procedures()
        matching_procedures = []
        
        for proc in procedures:
            if any(keyword in message.lower() for keyword in proc['title'].lower().split()):
                matching_procedures.append(proc)
                
        if matching_procedures:
            suggestions = [f"Start {proc['title']}" for proc in matching_procedures[:3]]
            response = "I found these related procedures:\n\n"
            for proc in matching_procedures:
                response += f"• **{proc['title']}**: {proc['description']}\n"
            response += "\nWould you like to start one of these procedures?"
            
            return ChatResponse(
                message=response,
                session_state=session,
                suggestions=suggestions
            )
            
        # Default response for unrecognized queries
        return ChatResponse(
            message="I'm specifically designed to help with Oracle EBS R12 i-Supplier procedures for Tanger Med. " +
                   "I can guide you through official workflows, help you query Oracle data, and track your progress.\n\n" +
                   "Type 'help' to see what I can do, or ask me to start a specific procedure.",
            session_state=session,
            suggestions=["Show help", "List procedures", "Show purchase orders"]
        )
        
    def _extract_procedure_id(self, message: str) -> Optional[str]:
        """Extract procedure ID from user message"""
        message_lower = message.lower()
        
        # Map common phrases to procedure IDs
        procedure_mappings = {
            "work confirmation": "work_confirmation",
            "create work confirmation": "work_confirmation",
            "confirmation": "work_confirmation",
            "invoice": "invoice_submission",
            "submit invoice": "invoice_submission",
            "purchase order": "view_purchase_orders",
            "view purchase orders": "view_purchase_orders",
            "po": "view_purchase_orders"
        }
        
        for phrase, procedure_id in procedure_mappings.items():
            if phrase in message_lower:
                return procedure_id
                
        return None
        
    def _parse_oracle_query(self, message: str) -> Tuple[Optional[Dict], Dict[str, Any]]:
        """Parse Oracle query from user message"""
        message_lower = message.lower()
        
        # Purchase Orders
        if any(keyword in message_lower for keyword in ["po", "purchase order", "purchase orders"]):
            if "po-" in message_lower:
                # Extract PO number
                po_match = re.search(r'po-[\d-]+', message_lower)
                if po_match:
                    return {"module": "purchase_orders", "type": "search_by_po_number"}, {"po_number": po_match.group().upper()}
            return {"module": "purchase_orders", "type": "list_all"}, {}
            
        # Invoices
        elif any(keyword in message_lower for keyword in ["invoice", "invoices"]):
            return {"module": "invoices", "type": "list_all"}, {}
            
        # Suppliers
        elif any(keyword in message_lower for keyword in ["supplier", "suppliers"]):
            return {"module": "suppliers", "type": "list_all"}, {}
            
        return None, {}
        
    def _format_oracle_response(self, module: str, data: List[Dict]) -> str:
        """Format Oracle query response for display"""
        
        if module == "purchase_orders":
            if not data:
                return "No purchase orders found."
                
            response = f"**Purchase Orders ({len(data)} found):**\n\n"
            for po in data:
                response += f"📋 **{po['po_number']}**\n"
                response += f"   • Supplier: {po['supplier']}\n"
                response += f"   • Status: {po['status']}\n"
                response += f"   • Amount: {po['amount']} {po['currency']}\n"
                response += f"   • Delivery Date: {po['delivery_date']}\n\n"
                
        elif module == "invoices":
            if not data:
                return "No invoices found."
                
            response = f"**Invoices ({len(data)} found):**\n\n"
            for inv in data:
                response += f"🧾 **{inv['invoice_number']}**\n"
                response += f"   • PO: {inv['po_number']}\n"
                response += f"   • Supplier: {inv['supplier']}\n"
                response += f"   • Amount: {inv['amount']}\n"
                response += f"   • Status: {inv['status']}\n\n"
                
        elif module == "suppliers":
            if not data:
                return "No suppliers found."
                
            response = f"**Suppliers ({len(data)} found):**\n\n"
            for sup in data:
                response += f"🏢 **{sup['name']}**\n"
                response += f"   • ID: {sup['supplier_id']}\n"
                response += f"   • Status: {sup['status']}\n"
                response += f"   • Contact: {sup['contact_email']}\n\n"
        else:
            response = "Data retrieved successfully."
            
        return response
        
    def _validate_step_completion(self, procedure_id: str, step_id: str, workflow_data: Dict) -> List[str]:
        """Validate if step can be completed based on validation rules"""
        errors = []
        
        # Get validation rules for procedure
        rules = self.validation_rules.get(procedure_id, {})
        
        # For demo purposes, we'll implement basic validation
        # In a real system, this would check against actual Oracle data
        
        return errors  # Return empty for now
        
    async def query_oracle_module(self, module: str, query_type: str, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query Oracle EBS module (mocked implementation)"""
        
        if module not in self.mock_oracle_data:
            return []
            
        data = self.mock_oracle_data[module]
        
        if query_type == "list_all":
            return data
        elif query_type == "search_by_po_number":
            po_number = parameters.get("po_number")
            return [item for item in data if item.get("po_number") == po_number]
        else:
            return data
            
    def get_available_procedures(self) -> List[ProcedureInfo]:
        """Get list of available procedures"""
        procedures = []
        
        for proc_id, proc_data in self.procedures_data.items():
            procedures.append(ProcedureInfo(
                procedure_id=proc_id,
                title=proc_data['title'],
                description=proc_data['description'],
                category=proc_data.get('category', 'general'),
                prerequisites=proc_data.get('prerequisites', [])
            ))
            
        return procedures
        
    def get_procedure_details(self, procedure_id: str) -> Optional[Dict]:
        """Get detailed information about a specific procedure"""
        return self.procedures_data.get(procedure_id)
        
    def get_validation_rules(self, procedure_id: str) -> Dict[str, Any]:
        """Get validation rules for a procedure"""
        return self.validation_rules.get(procedure_id, {})