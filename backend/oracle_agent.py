import json
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re

# Removed langchain dependencies for simplified version

from backend.models import (
    ChatResponse, SessionState, WorkflowStep, MessageType, 
    WorkflowStatus, ProcedureInfo, ValidationRule
)
from backend.oracle_ebs_chatbot import OracleEBSChatbot
from backend.enhanced_visual_guide_generator import enhanced_visual_guide_generator

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
        # Initialize Oracle EBS chatbot if API key is available
        self.ebs_chatbot = None
        try:
            api_key = os.getenv('GOOGLE_API_KEY') or "AIzaSyC8pw11h7ppDilnA-ITc8-SmF8daANOhIw"
            if api_key:
                self.ebs_chatbot = OracleEBSChatbot(api_key)
        except Exception as e:
            print(f"Oracle EBS Chatbot initialization failed: {e}")
        
    async def initialize(self):
        """Initialize the agent with procedures and validation rules"""
        await self._load_procedures()
        await self._load_mock_data()
        
    async def _load_procedures(self):
        """Load procedures from JSON file"""
        try:
            procedures_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "procedures.json")
            with open(procedures_path, 'r') as f:
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
                    "description": "IT Services Contract",
                    "completion_percentage": 75
                },
                {
                    "po_number": "PO-2024-002", 
                    "supplier": "Mediterranean Logistics",
                    "status": "Pending",
                    "amount": 25000.00,
                    "currency": "MAD",
                    "created_date": "2024-01-20",
                    "delivery_date": "2024-02-20",
                    "description": "Transportation Services",
                    "completion_percentage": 30
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
            ],
            "contracts": [
                {
                    "contract_id": "CNT-2024-001",
                    "supplier": "Tanger Med Services",
                    "status": "Active",
                    "start_date": "2024-01-01",
                    "end_date": "2024-12-31",
                    "value": 500000.00,
                    "performance_score": 92
                }
            ],
            "rfqs": [
                {
                    "rfq_number": "RFQ-2024-001",
                    "title": "Port Equipment Maintenance",
                    "status": "Open",
                    "deadline": "2024-02-28",
                    "estimated_value": 100000.00,
                    "responses_count": 3
                }
            ],
            "analytics": {
                "supplier_performance": {
                    "average_score": 87.5,
                    "top_performers": ["Tanger Med Services", "Mediterranean Logistics"],
                    "improvement_areas": ["Delivery Time", "Documentation"]
                },
                "payment_trends": {
                    "average_payment_time": 28,
                    "on_time_percentage": 94.2,
                    "disputed_payments": 2
                }
            }
        }
        
    async def process_message(self, message: str, session: SessionState, context: Dict[str, Any] = {}) -> ChatResponse:
        """Process user message and return appropriate response"""
        
        # Add current message to conversation history
        session.conversation_history.append({
            "role": "user",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 messages for context
        if len(session.conversation_history) > 20:
            session.conversation_history = session.conversation_history[-20:]
        
        # Handle special commands first
        message_lower = message.lower().strip()
        
        # Handle language switching commands
        french_switch_commands = ["passer au français", "français", "en français", "switch to french"]
        english_switch_commands = ["switch to english", "english", "en anglais", "passer à l'anglais"]
        
        if any(cmd in message_lower for cmd in french_switch_commands):
            return await self._handle_language_switch(session, 'fr')
        elif any(cmd in message_lower for cmd in english_switch_commands):
            return await self._handle_language_switch(session, 'en')
        
        # Handle French cancel commands
        cancel_commands = ["cancel procedure", "cancel", "stop procedure", "quit procedure", 
                          "annuler procédure", "annuler", "arrêter procédure", "quitter procédure"]
        if message_lower in cancel_commands:
            return await self._handle_cancel_procedure(session)
        
        # Handle French reset commands    
        reset_commands = ["reset session", "reset", "start over", "clear session",
                         "réinitialiser session", "réinitialiser", "recommencer", "effacer session"]
        if message_lower in reset_commands:
            return await self._handle_reset_session(session)
        
        # Analyze user intent
        intent = self._analyze_intent(message_lower)
        print(f"DEBUG: Message: '{message}', Intent: '{intent}'")  # Debug logging
        
        if intent == "workflow_request":
            return await self._handle_workflow_request(message, session)
        elif intent == "start_procedure":
            return await self._handle_procedure_start(message, session)
        elif intent == "continue_procedure":
            return await self._handle_procedure_continuation(message, session)
        elif intent == "oracle_query":
            return await self._handle_oracle_query(message, session)
        elif intent == "smart_assistance":
            return await self._handle_smart_assistance(message, session)
        elif intent == "help":
            return await self._handle_help_request(message, session)
        else:
            return await self._handle_general_query(message, session)
            
    def _analyze_intent(self, message: str) -> str:
        """Analyze user message to determine intent with AI enhancement"""
        
        message_lower = message.lower()
        
        # Check for specific procedure requests first (highest priority)
        procedure_phrases = [
            "guide me through", "walk me through", "how to create", "how to submit", "how to view",
            "guidez-moi", "accompagnez-moi", "comment créer", "comment soumettre", "comment voir",
            "work confirmation", "confirmation de travail", "manufacturing", "fabrication"
        ]
        
        if any(phrase in message_lower for phrase in procedure_phrases):
            return "start_procedure"
        
        # Enhanced keywords for different intents (English and French)
        procedure_keywords = [
            "create", "start", "begin", "guide", "step", "procedure", "process", "workflow",
            "créer", "commencer", "démarrer", "guide", "étape", "procédure", "processus"
        ]
        oracle_keywords = [
            "search", "find", "show me", "display", "list", "query",
            "rechercher", "trouver", "afficher", "montrer", "lister"
        ]
        help_keywords = [
            "help", "what can", "available", "options", "assist", "support",
            "aide", "que pouvez", "disponible", "options", "assister", "support"
        ]
        continue_keywords = [
            "next", "continue", "done", "completed", "yes", "proceed",
            "suivant", "continuer", "terminé", "oui", "procéder"
        ]
        
        # Check intent based on keywords
        if any(keyword in message_lower for keyword in help_keywords):
            return "help"
        elif any(keyword in message_lower for keyword in continue_keywords):
            return "continue_procedure"
        elif any(keyword in message_lower for keyword in oracle_keywords):
            return "oracle_query"
        elif any(keyword in message_lower for keyword in procedure_keywords):
            return "start_procedure"
        else:
            return "general"
            
    async def _handle_procedure_start(self, message: str, session: SessionState) -> ChatResponse:
        """Handle request to start a new procedure"""
        
        # Use session language if set, otherwise detect
        if hasattr(session, 'language') and session.language:
            language = session.language
        elif hasattr(session, 'preferred_language') and session.preferred_language:
            language = session.preferred_language
        else:
            # Detect language and store in session
            language = 'en'
            if self.ebs_chatbot:
                language = self.ebs_chatbot.detect_language(message)
            session.language = language
            session.preferred_language = language
        
        # Extract procedure from message
        procedure_id = self._extract_procedure_id(message)
        
        if not procedure_id:
            # Show available procedures
            procedures = self.get_available_procedures()
            
            if language == 'fr':
                suggestions = [f"Commencer {proc.title}" for proc in procedures[:5]]
                response_msg = "Je peux vous aider avec les procédures Oracle EBS R12 i-Supplier suivantes :\n\n" + \
                              "\n".join([f"• {proc.title}: {proc.description}" for proc in procedures])
            else:
                suggestions = [f"Start {proc.title}" for proc in procedures[:5]]
                response_msg = "I can help you with the following Oracle EBS R12 i-Supplier procedures:\n\n" + \
                              "\n".join([f"• {proc.title}: {proc.description}" for proc in procedures])
            
            return ChatResponse(
                message=response_msg,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
        if procedure_id not in self.procedures_data:
            if language == 'fr':
                error_msg = f"Je n'ai pas d'informations sur la procédure '{procedure_id}'. Veuillez choisir parmi les procédures disponibles."
                suggestions = ["Afficher les procédures disponibles"]
            else:
                error_msg = f"I don't have information about the procedure '{procedure_id}'. Please choose from the available procedures."
                suggestions = ["Show available procedures"]
            
            return ChatResponse(
                message=error_msg,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
        # Start the procedure
        procedure = self.procedures_data[procedure_id]
        first_step = procedure['steps'][0] if procedure['steps'] else None
        
        if not first_step:
            if language == 'fr':
                error_msg = f"La procédure '{procedure['title']}' n'a pas d'étapes définies."
            else:
                error_msg = f"The procedure '{procedure['title']}' has no defined steps."
            
            return ChatResponse(
                message=error_msg,
                session_state=session,
                language=language
            )
            
        # Update session state
        session.current_procedure = procedure_id
        session.current_step = first_step['step_id']
        session.status = WorkflowStatus.IN_PROGRESS
        session.updated_at = datetime.now()
        
        # Get visual guide for this step
        visual_guide = enhanced_visual_guide_generator.get_visual_guide(procedure_id, first_step['step_id'], language)
        
        # Create workflow step
        workflow_step = WorkflowStep(
            step_id=first_step['step_id'],
            title=first_step['title'],
            description=first_step['description'],
            instructions=first_step['instructions'],
            screenshot=visual_guide.get('image_url') or first_step.get('screenshot'),
            validation_criteria=first_step.get('validation_criteria', []),
            next_steps=first_step.get('next_steps', [])
        )
        
        if language == 'fr':
            translated_title = self._translate_procedure_content(procedure['title'], language)
            response_message = f"Démarrage de la procédure : **{translated_title}**\n\n"
            response_message += f"**Prérequis :**\n"
            for prereq in procedure.get('prerequisites', []):
                translated_prereq = self._translate_procedure_content(prereq, language)
                response_message += f"• {translated_prereq}\n"
            
            translated_step_title = self._translate_procedure_content(first_step['title'], language)
            translated_description = self._translate_procedure_content(first_step['description'], language)
            translated_instructions = self._translate_procedure_content(first_step['instructions'], language)
            
            response_message += f"\n**Étape 1 : {translated_step_title}**\n"
            response_message += f"{translated_description}\n\n"
            response_message += f"**Instructions :** {translated_instructions}\n\n"
            response_message += "Tapez 'terminé' ou 'suivant' quand vous avez complété cette étape."
            suggestions = ["Terminé avec cette étape", "Afficher capture d'écran", "Annuler procédure"]
        else:
            response_message = f"Starting procedure: **{procedure['title']}**\n\n"
            response_message += f"**Prerequisites:**\n"
            for prereq in procedure.get('prerequisites', []):
                response_message += f"• {prereq}\n"
            response_message += f"\n**Step 1: {first_step['title']}**\n"
            response_message += f"{first_step['description']}\n\n"
            response_message += f"**Instructions:** {first_step['instructions']}\n\n"
            response_message += "Type 'done' or 'next' when you've completed this step."
            suggestions = ["Done with this step", "Show screenshot", "Cancel procedure"]
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            current_step=workflow_step,
            screenshot=first_step.get('screenshot'),
            suggestions=suggestions,
            language=language
        )
        
    async def _handle_procedure_continuation(self, message: str, session: SessionState) -> ChatResponse:
        """Handle continuation of current procedure"""
        
        # Use session language for consistency
        language = getattr(session, 'preferred_language', 'en')
        
        if not session.current_procedure or not session.current_step:
            if language == 'fr':
                error_msg = "Vous n'avez pas de procédure active. Veuillez d'abord commencer une nouvelle procédure."
                suggestions = ["Afficher les procédures disponibles"]
            else:
                error_msg = "You don't have an active procedure. Please start a new procedure first."
                suggestions = ["Show available procedures"]
            
            return ChatResponse(
                message=error_msg,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
        
        # Handle dynamic workflows
        if session.current_procedure.startswith('dynamic_'):
            return await self._handle_dynamic_workflow_continuation(session)
            
        procedure = self.procedures_data[session.current_procedure]
        current_step_data = None
        
        # Find current step
        for step in procedure['steps']:
            if step['step_id'] == session.current_step:
                current_step_data = step
                break
                
        if not current_step_data:
            if language == 'fr':
                error_msg = "Erreur : Étape actuelle non trouvée dans la procédure."
            else:
                error_msg = "Error: Current step not found in procedure."
            
            return ChatResponse(
                message=error_msg,
                session_state=session,
                language=language
            )
            
        # Validate step completion if validation criteria exist
        validation_errors = self._validate_step_completion(
            session.current_procedure, 
            session.current_step, 
            session.workflow_data
        )
        
        if validation_errors:
            if language == 'fr':
                error_msg = "Veuillez compléter les exigences suivantes avant de continuer :\n\n" + \
                           "\n".join([f"• {error}" for error in validation_errors])
                suggestions = ["Réessayer l'étape", "Afficher l'aide"]
            else:
                error_msg = "Please complete the following requirements before proceeding:\n\n" + \
                           "\n".join([f"• {error}" for error in validation_errors])
                suggestions = ["Retry step", "Show help"]
            
            return ChatResponse(
                message=error_msg,
                session_state=session,
                validation_errors=validation_errors,
                suggestions=suggestions,
                language=language
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
            
            if language == 'fr':
                completion_msg = f"Félicitations ! Vous avez terminé avec succès la procédure : **{procedure['title']}**\n\n" + \
                               "Toutes les étapes ont été complétées. Y a-t-il autre chose avec quoi je peux vous aider ?"
                suggestions = ["Commencer une autre procédure", "Voir les commandes d'achat", "Afficher les procédures disponibles"]
            else:
                completion_msg = f"Congratulations! You have successfully completed the procedure: **{procedure['title']}**\n\n" + \
                               "All steps have been completed. Is there anything else I can help you with?"
                suggestions = ["Start another procedure", "View purchase orders", "Show available procedures"]
            
            return ChatResponse(
                message=completion_msg,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
        # Move to next step
        next_step_id = next_steps[0]  # Take first next step
        next_step_data = None
        
        for step in procedure['steps']:
            if step['step_id'] == next_step_id:
                next_step_data = step
                break
                
        if not next_step_data:
            if language == 'fr':
                error_msg = "Erreur : Étape suivante non trouvée dans la procédure."
            else:
                error_msg = "Error: Next step not found in procedure."
            
            return ChatResponse(
                message=error_msg,
                session_state=session,
                language=language
            )
            
        # Update session
        session.current_step = next_step_id
        session.updated_at = datetime.now()
        
        # Get visual guide for next step
        visual_guide = enhanced_visual_guide_generator.get_visual_guide(session.current_procedure, next_step_data['step_id'], language)
        
        # Create workflow step
        workflow_step = WorkflowStep(
            step_id=next_step_data['step_id'],
            title=next_step_data['title'],
            description=next_step_data['description'],
            instructions=next_step_data['instructions'],
            screenshot=visual_guide.get('image_url') or next_step_data.get('screenshot'),
            validation_criteria=next_step_data.get('validation_criteria', []),
            next_steps=next_step_data.get('next_steps', [])
        )
        
        step_number = len(session.completed_steps) + 1
        
        if language == 'fr':
            translated_step_title = self._translate_procedure_content(next_step_data['title'], language)
            translated_description = self._translate_procedure_content(next_step_data['description'], language)
            translated_instructions = self._translate_procedure_content(next_step_data['instructions'], language)
            
            response_message = f"Étape terminée !\n\n"
            response_message += f"**Étape {step_number} : {translated_step_title}**\n"
            response_message += f"{translated_description}\n\n"
            response_message += f"**Instructions :** {translated_instructions}\n\n"
            response_message += "Tapez 'terminé' ou 'suivant' quand vous avez complété cette étape."
            suggestions = ["Terminé avec cette étape", "Afficher capture d'écran", "Annuler procédure"]
        else:
            response_message = f"Step completed!\n\n"
            response_message += f"**Step {step_number}: {next_step_data['title']}**\n"
            response_message += f"{next_step_data['description']}\n\n"
            response_message += f"**Instructions:** {next_step_data['instructions']}\n\n"
            response_message += "Type 'done' or 'next' when you've completed this step."
            suggestions = ["Done with this step", "Show screenshot", "Cancel procedure"]
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            current_step=workflow_step,
            screenshot=next_step_data.get('screenshot'),
            suggestions=suggestions,
            language=language
        )
        
    async def _handle_oracle_query(self, message: str, session: SessionState) -> ChatResponse:
        """Handle Oracle EBS module queries"""
        
        query_type, parameters = self._parse_oracle_query(message)
        
        if not query_type:
            # Use session language for consistency
            language = getattr(session, 'preferred_language', 'en')
            
            if language == 'fr':
                help_msg = "Je peux vous aider à interroger les données Oracle EBS. Requêtes disponibles :\n\n" + \
                          "• **Commandes d'Achat** : Recherche par numéro de commande, fournisseur ou plage de dates\n" + \
                          "• **Factures** : Voir le statut des factures et le suivi des paiements\n" + \
                          "• **Fournisseurs** : Rechercher les informations et performances des fournisseurs\n\n" + \
                          "Exemple : 'Afficher la commande d'achat PO-2024-001' ou 'Lister toutes les factures'"
                suggestions = ["Afficher les commandes d'achat", "Lister les factures", "Rechercher les fournisseurs"]
            else:
                help_msg = "I can help you query Oracle EBS data. Available queries:\n\n" + \
                          "• **Purchase Orders**: Search by PO number, supplier, or date range\n" + \
                          "• **Invoices**: View invoice status and payment tracking\n" + \
                          "• **Suppliers**: Search supplier information and performance\n\n" + \
                          "Example: 'Show purchase order PO-2024-001' or 'List all invoices'"
                suggestions = ["Show purchase orders", "List invoices", "Search suppliers"]
            
            return ChatResponse(
                message=help_msg,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
        try:
            result = await self.query_oracle_module(query_type['module'], query_type['type'], parameters)
            
            if not result:
                return ChatResponse(
                    message=f"No data found for your query.",
                    session_state=session
                )
                
            # Detect language for response formatting
            language = 'en'
            if self.ebs_chatbot:
                language = self.ebs_chatbot.detect_language(message)
            
            # Format response based on module
            formatted_response = self._format_oracle_response(query_type['module'], result, language)
            
            # Language-specific suggestions
            if language == 'fr':
                suggestions = ["Afficher plus de détails", "Exporter les données", "Nouvelle recherche"]
            else:
                suggestions = ["Show more details", "Export data", "New search"]
            
            return ChatResponse(
                message=formatted_response,
                session_state=session,
                oracle_data={"results": result},
                suggestions=suggestions,
                language=language
            )
            
        except Exception as e:
            return ChatResponse(
                message=f"Error querying Oracle data: {str(e)}",
                session_state=session,
                message_type=MessageType.ERROR
            )
            
    async def _handle_help_request(self, message: str, session: SessionState) -> ChatResponse:
        """Handle help and general information requests"""
        
        # Use session language for consistency
        language = getattr(session, 'preferred_language', 'en')
        
        if language == 'fr':
            help_message = """
🤖 **Assistant Oracle EBS R12 i-Supplier pour Tanger Med**

Je peux vous aider avec :

**📋 Procédures et Flux de Travail :**
• Créer une Confirmation de Travail
• Soumettre une Facture
• Voir les Commandes d'Achat
• Enregistrement Fournisseur
• Gestion des Contrats
• Suivi des Paiements
• Réponse aux Appels d'Offres
• Confirmation de Réception des Marchandises
• Création de Fiche de Service
• Demande de Paiement Anticipé
• Rapport de Déviation Qualité
• Évaluation des Performances Fournisseur
• Guidance étape par étape avec captures d'écran

**🔍 Requêtes Oracle EBS :**
• Rechercher les Commandes d'Achat
• Voir le Statut des Factures
• Vérifier les Informations Fournisseur
• Suivre le Statut des Paiements
• Analytiques des Contrats
• Gestion des Appels d'Offres
• Rapports de Performance

**💡 Commandes Disponibles :**
• "Commencer [nom de procédure]" - Débuter une procédure guidée
• "Afficher les commandes d'achat" - Interroger les données de commandes
• "Lister les factures" - Voir les informations de factures
• "Rechercher les fournisseurs" - Trouver les détails des fournisseurs
• "Recommander les prochaines étapes" - Obtenir des recommandations IA
• "Prédire les tendances" - Voir les insights prédictifs
• "Optimiser le processus" - Obtenir des suggestions d'efficacité
• "Aide" - Afficher ce message

**🎯 Session Actuelle :**
"""
            
            if session.current_procedure:
                procedure = self.procedures_data.get(session.current_procedure, {})
                help_message += f"• Procédure Active : {procedure.get('title', 'Inconnue')}\n"
                help_message += f"• Étape Actuelle : {session.current_step}\n"
                help_message += f"• Étapes Terminées : {len(session.completed_steps)}\n"
            else:
                help_message += "• Aucune procédure active\n"
                
            help_message += "\nQue souhaitez-vous faire ?"
            
            suggestions = [
                "Commencer confirmation de travail",
                "Afficher les commandes d'achat", 
                "Lister les procédures disponibles",
                "Obtenir des recommandations",
                "Voir le tableau de bord analytique",
                "Voir le progrès de la session"
            ]
        else:
            help_message = """
🤖 **Oracle EBS R12 i-Supplier Assistant for Tanger Med**

I can help you with:

**📋 Procedures & Workflows:**
• Create Work Confirmation
• Submit Invoice
• View Purchase Orders
• Supplier Registration
• Contract Management
• Payment Tracking
• RFQ Response
• Goods Receipt Confirmation
• Service Entry Sheet Creation
• Advance Payment Request
• Quality Deviation Report
• Vendor Performance Evaluation
• Step-by-step guidance with screenshots

**🔍 Oracle EBS Queries:**
• Search Purchase Orders
• View Invoice Status
• Check Supplier Information
• Track Payment Status
• Contract Analytics
• RFQ Management
• Performance Reports

**💡 Available Commands:**
• "Start [procedure name]" - Begin a guided procedure
• "Show purchase orders" - Query PO data
• "List invoices" - View invoice information
• "Search suppliers" - Find supplier details
• "Recommend next steps" - Get AI recommendations
• "Predict trends" - View predictive insights
• "Optimize process" - Get efficiency suggestions
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
            
            suggestions = [
                "Start work confirmation",
                "Show purchase orders", 
                "List available procedures",
                "Get recommendations",
                "View analytics dashboard",
                "View session progress"
            ]
        
        return ChatResponse(
            message=help_message,
            session_state=session,
            suggestions=suggestions,
            language=language
        )
        
    async def _handle_general_query(self, message: str, session: SessionState) -> ChatResponse:
        """Handle general queries that don't fit other categories"""
        
        # Use session language for consistency
        language = getattr(session, 'preferred_language', 'en')
        
        # Try to get response from Oracle EBS chatbot first
        if self.ebs_chatbot:
            try:
                # Build context with conversation history
                context = {
                    'current_procedure': session.current_procedure,
                    'current_step': session.current_step,
                    'completed_steps': session.completed_steps,
                    'conversation_history': session.conversation_history[-6:] if len(session.conversation_history) > 1 else [],
                    'language': language
                }
                ebs_response = await self.ebs_chatbot.get_response(message, context)
                if ebs_response:
                    suggestions = ["Show procedures", "Start work confirmation", "View purchase orders", "Help"] if language == 'en' else ["Afficher les procédures", "Commencer confirmation de travail", "Voir les commandes d'achat", "Aide"]
                    return ChatResponse(
                        message=ebs_response,
                        session_state=session,
                        suggestions=suggestions,
                        language=language
                    )
            except Exception as e:
                print(f"EBS Chatbot error: {e}")
        
        # Check if message contains any procedure-related keywords
        procedures = self.get_available_procedures()
        matching_procedures = []
        
        for proc in procedures:
            if any(keyword in message.lower() for keyword in proc.title.lower().split()):
                matching_procedures.append(proc)
                
        if matching_procedures:
            if language == 'fr':
                suggestions = [f"Commencer {proc.title}" for proc in matching_procedures[:3]]
                response = "J'ai trouvé ces procédures liées :\n\n"
                for proc in matching_procedures:
                    response += f"• **{proc.title}**: {proc.description}\n"
                response += "\nSouhaitez-vous commencer une de ces procédures ?"
            else:
                suggestions = [f"Start {proc.title}" for proc in matching_procedures[:3]]
                response = "I found these related procedures:\n\n"
                for proc in matching_procedures:
                    response += f"• **{proc.title}**: {proc.description}\n"
                response += "\nWould you like to start one of these procedures?"
            
            return ChatResponse(
                message=response,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
        # Handle Oracle EBS definition questions directly
        if any(phrase in message.lower() for phrase in ['what is oracle', 'what is ebs', 'oracle ebs', 'qu\'est-ce qu\'oracle', 'qu\'est-ce qu\'ebs']):
            if language == 'fr':
                definition_msg = "Oracle E-Business Suite (EBS) R12 est une suite logicielle complète de planification des ressources d'entreprise (ERP) développée par Oracle Corporation. Elle intègre divers processus métier notamment :\n\n" + \
                               "- **Gestion Financière** - Grand Livre, Comptes Fournisseurs, Comptes Clients\n" + \
                               "- **Gestion de la Chaîne d'Approvisionnement** - Approvisionnement, Inventaire, Gestion des Commandes\n" + \
                               "- **Ressources Humaines** - RH, Paie, Administration des Avantages\n" + \
                               "- **Gestion de la Relation Client** - Ventes, Marketing, Service\n" + \
                               "- **Fabrication** - Planification de la Production, Gestion de la Qualité\n\n" + \
                               "Le **Portail i-Supplier** est une interface web qui permet aux fournisseurs d'interagir avec Oracle EBS, leur permettant de consulter les commandes d'achat, soumettre des factures, suivre les paiements et gérer leurs informations fournisseur.\n\n" + \
                               "À Tanger Med, Oracle EBS R12 est utilisé pour rationaliser les processus d'approvisionnement et les interactions avec les fournisseurs."
                suggestions = ["Afficher les procédures", "Commencer confirmation de travail", "Voir les commandes d'achat", "Aide"]
            else:
                definition_msg = "Oracle E-Business Suite (EBS) R12 is a comprehensive enterprise resource planning (ERP) software suite developed by Oracle Corporation. It integrates various business processes including:\n\n" + \
                               "- **Financial Management** - General Ledger, Accounts Payable, Accounts Receivable\n" + \
                               "- **Supply Chain Management** - Procurement, Inventory, Order Management\n" + \
                               "- **Human Resources** - HR, Payroll, Benefits Administration\n" + \
                               "- **Customer Relationship Management** - Sales, Marketing, Service\n" + \
                               "- **Manufacturing** - Production Planning, Quality Management\n\n" + \
                               "The **i-Supplier Portal** is a web-based interface that allows suppliers to interact with Oracle EBS, enabling them to view purchase orders, submit invoices, track payments, and manage their supplier information.\n\n" + \
                               "At Tanger Med, Oracle EBS R12 is used to streamline procurement processes and supplier interactions."
                suggestions = ["Show procedures", "Start work confirmation", "View purchase orders", "Help"]
            
            return ChatResponse(
                message=definition_msg,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
        
        # Default comprehensive response
        if language == 'fr':
            default_msg = "Je suis votre assistant Oracle EBS R12 i-Supplier pour Tanger Med. Je peux vous aider avec :\n\n" + \
                         "**📋 Procédures Disponibles :**\n" + \
                         "• Confirmation de Travail - Créer et soumettre des confirmations\n" + \
                         "• Soumission de Factures - Traiter les soumissions de factures\n" + \
                         "• Commandes d'Achat - Voir et gérer les commandes\n" + \
                         "• Enregistrement Fournisseur - Processus d'inscription\n" + \
                         "• Gestion des Contrats - Gérer les contrats et amendements\n" + \
                         "• Suivi des Paiements - Suivre les paiements de factures\n\n" + \
                         "**🔍 Requêtes Oracle :**\n" + \
                         "• Rechercher des données de commandes d'achat\n" + \
                         "• Voir le statut des factures\n" + \
                         "• Vérifier les informations fournisseur\n\n" + \
                         "Que souhaitez-vous faire ?"
            suggestions = ["Commencer confirmation de travail", "Soumettre facture", "Voir les commandes d'achat", "Aide complète"]
        else:
            default_msg = "I'm your Oracle EBS R12 i-Supplier Assistant for Tanger Med. I can help you with:\n\n" + \
                         "**📋 Available Procedures:**\n" + \
                         "• Work Confirmation - Create and submit work confirmations\n" + \
                         "• Invoice Submission - Process invoice submissions\n" + \
                         "• Purchase Orders - View and manage purchase orders\n" + \
                         "• Supplier Registration - Registration process\n" + \
                         "• Contract Management - Manage contracts and amendments\n" + \
                         "• Payment Tracking - Track invoice payments\n\n" + \
                         "**🔍 Oracle Queries:**\n" + \
                         "• Search purchase order data\n" + \
                         "• View invoice status\n" + \
                         "• Check supplier information\n\n" + \
                         "What would you like to do?"
            suggestions = ["Start work confirmation", "Submit invoice", "View purchase orders", "Full help"]
        
        return ChatResponse(
            message=default_msg,
            session_state=session,
            suggestions=suggestions,
            language=language
        )
        
    def _extract_procedure_id(self, message: str) -> Optional[str]:
        """Extract procedure ID from user message"""
        message_lower = message.lower()
        
        # Enhanced procedure mappings with French and English
        procedure_mappings = {
            # English mappings
            "work confirmation": "work_confirmation",
            "create work confirmation": "work_confirmation",
            "start work confirmation": "work_confirmation",
            "confirmation": "work_confirmation",
            "invoice": "invoice_submission",
            "submit invoice": "invoice_submission",
            "purchase order": "view_purchase_orders",
            "view purchase orders": "view_purchase_orders",
            "show purchase orders": "view_purchase_orders",
            "po": "view_purchase_orders",
            "supplier registration": "supplier_registration",
            "contract management": "contract_management",
            "payment tracking": "payment_tracking",
            "rfq response": "rfq_response",
            "goods receipt": "goods_receipt_confirmation",
            "service entry": "service_entry_sheet",
            "advance payment": "advance_payment_request",
            "quality deviation": "quality_deviation_report",
            "vendor performance": "vendor_performance_evaluation",
            "switch to english": "language_switch_en",
            "english": "language_switch_en",
            # French mappings
            "confirmation de travail": "work_confirmation",
            "créer confirmation de travail": "work_confirmation",
            "commencer confirmation de travail": "work_confirmation",
            "confirmation travail": "work_confirmation",
            "facture": "invoice_submission",
            "soumettre facture": "invoice_submission",
            "soumission facture": "invoice_submission",
            "commande d'achat": "view_purchase_orders",
            "commandes d'achat": "view_purchase_orders",
            "voir commandes d'achat": "view_purchase_orders",
            "afficher les commandes d'achat": "view_purchase_orders",
            "voir commandes": "view_purchase_orders",
            "enregistrement fournisseur": "supplier_registration",
            "gestion des contrats": "contract_management",
            "gérer les contrats": "contract_management",
            "suivi des paiements": "payment_tracking",
            "suivre les paiements": "payment_tracking",
            "réponse aux appels d'offres": "rfq_response",
            "répondre aux appels d'offres": "rfq_response",
            "appels d'offres": "rfq_response",
            "appel d'offres": "rfq_response",
            "confirmation de réception": "goods_receipt_confirmation",
            "réception des marchandises": "goods_receipt_confirmation",
            "fiche de service": "service_entry_sheet",
            "créer fiche de service": "service_entry_sheet",
            "paiement anticipé": "advance_payment_request",
            "demande de paiement anticipé": "advance_payment_request",
            "déviation qualité": "quality_deviation_report",
            "signaler une déviation qualité": "quality_deviation_report",
            "rapport de qualité": "quality_deviation_report",
            "évaluation des performances": "vendor_performance_evaluation",
            "performance fournisseur": "vendor_performance_evaluation",
            "passer au français": "language_switch_fr",
            "français": "language_switch_fr",
            "en français": "language_switch_fr"
        }
        
        # Check longer phrases first to avoid partial matches
        sorted_mappings = sorted(procedure_mappings.items(), key=lambda x: len(x[0]), reverse=True)
        for phrase, procedure_id in sorted_mappings:
            if phrase in message_lower:
                return procedure_id
                
        return None
        
    def _parse_oracle_query(self, message: str) -> Tuple[Optional[Dict], Dict[str, Any]]:
        """Parse Oracle query from user message"""
        message_lower = message.lower()
        
        # Purchase Orders (English and French)
        if any(keyword in message_lower for keyword in ["po", "purchase order", "purchase orders", "commande d'achat", "commandes d'achat", "commande", "commandes", "afficher les commandes", "voir les commandes"]):
            if "po-" in message_lower:
                # Extract PO number
                po_match = re.search(r'po-[\d-]+', message_lower)
                if po_match:
                    return {"module": "purchase_orders", "type": "search_by_po_number"}, {"po_number": po_match.group().upper()}
            return {"module": "purchase_orders", "type": "list_all"}, {}
            
        # Invoices (English and French)
        elif any(keyword in message_lower for keyword in ["invoice", "invoices", "facture", "factures"]):
            return {"module": "invoices", "type": "list_all"}, {}
            
        # Suppliers (English and French)
        elif any(keyword in message_lower for keyword in ["supplier", "suppliers", "fournisseur", "fournisseurs"]):
            return {"module": "suppliers", "type": "list_all"}, {}
            
        # Contracts (English and French)
        elif any(keyword in message_lower for keyword in ["contract", "contracts", "contrat", "contrats"]):
            return {"module": "contracts", "type": "list_all"}, {}
            
        # RFQs (English and French)
        elif any(keyword in message_lower for keyword in ["rfq", "rfqs", "quotation", "appel d'offres", "appels d'offres", "devis"]):
            return {"module": "rfqs", "type": "list_all"}, {}
            
        # Analytics (English and French)
        elif any(keyword in message_lower for keyword in ["analytics", "report", "performance", "trend", "analytique", "rapport", "tendance"]):
            return {"module": "analytics", "type": "dashboard"}, {}
            
        return None, {}
        
    def _format_oracle_response(self, module: str, data: List[Dict], language: str = 'en') -> str:
        """Format Oracle query response for display"""
        
        if module == "purchase_orders":
            if not data:
                return "Aucune commande d'achat trouvée." if language == 'fr' else "No purchase orders found."
                
            if language == 'fr':
                response = f"**Commandes d'Achat ({len(data)} trouvées) :**\n\n"
                for po in data:
                    response += f"**{po['po_number']}**\n"
                    response += f"   - Fournisseur : {po['supplier']}\n"
                    response += f"   - Statut : {po['status']}\n"
                    response += f"   - Montant : {po['amount']} {po['currency']}\n"
                    response += f"   - Date de livraison : {po['delivery_date']}\n\n"
            else:
                response = f"**Purchase Orders ({len(data)} found):**\n\n"
                for po in data:
                    response += f"**{po['po_number']}**\n"
                    response += f"   - Supplier: {po['supplier']}\n"
                    response += f"   - Status: {po['status']}\n"
                    response += f"   - Amount: {po['amount']} {po['currency']}\n"
                    response += f"   - Delivery Date: {po['delivery_date']}\n\n"
                
        elif module == "invoices":
            if not data:
                return "Aucune facture trouvée." if language == 'fr' else "No invoices found."
                
            if language == 'fr':
                response = f"**Factures ({len(data)} trouvées) :**\n\n"
                for inv in data:
                    response += f"**{inv['invoice_number']}**\n"
                    response += f"   - Commande : {inv['po_number']}\n"
                    response += f"   - Fournisseur : {inv['supplier']}\n"
                    response += f"   - Montant : {inv['amount']}\n"
                    response += f"   - Statut : {inv['status']}\n\n"
            else:
                response = f"**Invoices ({len(data)} found):**\n\n"
                for inv in data:
                    response += f"**{inv['invoice_number']}**\n"
                    response += f"   - PO: {inv['po_number']}\n"
                    response += f"   - Supplier: {inv['supplier']}\n"
                    response += f"   - Amount: {inv['amount']}\n"
                    response += f"   - Status: {inv['status']}\n\n"
                
        elif module == "suppliers":
            if not data:
                return "Aucun fournisseur trouvé." if language == 'fr' else "No suppliers found."
                
            if language == 'fr':
                response = f"**Fournisseurs ({len(data)} trouvés) :**\n\n"
                for sup in data:
                    response += f"**{sup['name']}**\n"
                    response += f"   - ID : {sup['supplier_id']}\n"
                    response += f"   - Statut : {sup['status']}\n"
                    response += f"   - Contact : {sup['contact_email']}\n\n"
            else:
                response = f"**Suppliers ({len(data)} found):**\n\n"
                for sup in data:
                    response += f"**{sup['name']}**\n"
                    response += f"   - ID: {sup['supplier_id']}\n"
                    response += f"   - Status: {sup['status']}\n"
                    response += f"   - Contact: {sup['contact_email']}\n\n"
                
        elif module == "contracts":
            if not data:
                return "No contracts found."
                
            response = f"**Contracts ({len(data)} found):**\n\n"
            for contract in data:
                response += f"**{contract['contract_id']}**\n"
                response += f"   - Supplier: {contract['supplier']}\n"
                response += f"   - Status: {contract['status']}\n"
                response += f"   - Value: {contract['value']} MAD\n"
                response += f"   - Performance: {contract['performance_score']}%\n\n"
                
        elif module == "rfqs":
            if not data:
                return "No RFQs found."
                
            response = f"**RFQs ({len(data)} found):**\n\n"
            for rfq in data:
                response += f"**{rfq['rfq_number']}**\n"
                response += f"   - Title: {rfq['title']}\n"
                response += f"   - Status: {rfq['status']}\n"
                response += f"   - Deadline: {rfq['deadline']}\n"
                response += f"   - Responses: {rfq['responses_count']}\n\n"
                
        elif module == "analytics":
            response = "**Analytics Dashboard:**\n\n"
            if isinstance(data, dict):
                if 'supplier_performance' in data:
                    perf = data['supplier_performance']
                    response += f"**Supplier Performance:**\n"
                    response += f"   - Average Score: {perf['average_score']}%\n"
                    response += f"   - Top Performers: {', '.join(perf['top_performers'])}\n\n"
                if 'payment_trends' in data:
                    trends = data['payment_trends']
                    response += f"**Payment Trends:**\n"
                    response += f"   - Average Payment Time: {trends['average_payment_time']} days\n"
                    response += f"   - On-time Percentage: {trends['on_time_percentage']}%\n\n"
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
        
    async def _handle_smart_assistance(self, message: str, session: SessionState) -> ChatResponse:
        """Handle AI-powered smart assistance requests"""
        
        # Use session language for consistency
        language = getattr(session, 'preferred_language', 'en')
        
        message_lower = message.lower()
        
        # Smart recommendations based on context
        if any(word in message_lower for word in ["recommend", "suggest", "recommander", "suggérer"]):
            recommendations = self._generate_smart_recommendations(session, language)
            if language == 'fr':
                title = "🤖 **Recommandations Intelligentes :**"
                suggestions = ["Commencer la procédure recommandée", "Voir les analytiques", "Obtenir plus de suggestions"]
            else:
                title = "🤖 **Smart Recommendations:**"
                suggestions = ["Start recommended procedure", "View analytics", "Get more suggestions"]
            
            return ChatResponse(
                message=f"{title}\n\n{recommendations}",
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
        # Predictive assistance
        elif any(word in message_lower for word in ["predict", "forecast", "prédire", "prévoir", "tendances"]):
            predictions = self._generate_predictions(session, language)
            if language == 'fr':
                title = "🔮 **Insights Prédictifs :**"
                suggestions = ["Voir les prévisions détaillées", "Exporter les prédictions", "Définir des alertes"]
            else:
                title = "🔮 **Predictive Insights:**"
                suggestions = ["View detailed forecast", "Export predictions", "Set alerts"]
            
            return ChatResponse(
                message=f"{title}\n\n{predictions}",
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
        # Process optimization
        elif any(word in message_lower for word in ["optimize", "improve", "optimiser", "améliorer"]):
            optimizations = self._generate_optimizations(session, language)
            if language == 'fr':
                title = "⚡ **Optimisations de Processus :**"
                suggestions = ["Appliquer l'optimisation", "Voir l'analyse d'impact", "Planifier la révision"]
            else:
                title = "⚡ **Process Optimizations:**"
                suggestions = ["Apply optimization", "View impact analysis", "Schedule review"]
            
            return ChatResponse(
                message=f"{title}\n\n{optimizations}",
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
        else:
            if language == 'fr':
                help_msg = "Je peux fournir une assistance intelligente avec :\n\n" + \
                          "• **Recommandations** - Suggérer les meilleures actions suivantes\n" + \
                          "• **Prédictions** - Prévoir les tendances et résultats\n" + \
                          "• **Optimisations** - Améliorer l'efficacité des processus\n\n" + \
                          "Avec quoi souhaitez-vous de l'aide ?"
                suggestions = ["Obtenir des recommandations", "Afficher les prédictions", "Optimiser les processus"]
            else:
                help_msg = "I can provide smart assistance with:\n\n" + \
                          "• **Recommendations** - Suggest next best actions\n" + \
                          "• **Predictions** - Forecast trends and outcomes\n" + \
                          "• **Optimizations** - Improve process efficiency\n\n" + \
                          "What would you like help with?"
                suggestions = ["Get recommendations", "Show predictions", "Optimize processes"]
            
            return ChatResponse(
                message=help_msg,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
    def _generate_smart_recommendations(self, session: SessionState, language: str = 'en') -> str:
        """Generate context-aware recommendations"""
        recommendations = []
        
        # Based on session history
        if not session.current_procedure:
            if language == 'fr':
                recommendations.append("• Commencez par **Enregistrement Fournisseur** si vous êtes nouveau")
                recommendations.append("• Vérifiez **Suivi des Paiements** pour les factures en attente")
                recommendations.append("• Consultez les **Appels d'Offres Ouverts** pour de nouvelles opportunités")
            else:
                recommendations.append("• Start with **Supplier Registration** if you're new")
                recommendations.append("• Check **Payment Tracking** for pending invoices")
                recommendations.append("• Review **Open RFQs** for new opportunities")
        else:
            if language == 'fr':
                recommendations.append(f"• Continuez votre procédure actuelle : {session.current_procedure}")
                recommendations.append("• Sauvegardez le progrès avant de changer de tâche")
            else:
                recommendations.append(f"• Continue your current procedure: {session.current_procedure}")
                recommendations.append("• Save progress before switching tasks")
            
        # Time-based recommendations
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 11:
            if language == 'fr':
                recommendations.append("• Le matin est idéal pour les procédures complexes comme la Gestion des Contrats")
            else:
                recommendations.append("• Morning is ideal for complex procedures like Contract Management")
        elif 14 <= current_hour <= 16:
            if language == 'fr':
                recommendations.append("• L'après-midi est parfait pour la Soumission de Factures et le Suivi des Paiements")
            else:
                recommendations.append("• Afternoon is perfect for Invoice Submission and Payment Tracking")
            
        return "\n".join(recommendations)
        
    def _generate_predictions(self, session: SessionState, language: str = 'en') -> str:
        """Generate predictive insights"""
        predictions = []
        
        if language == 'fr':
            predictions.append("• **Traitement des Paiements** : Prochain paiement probable dans 3-5 jours ouvrables")
            predictions.append("• **Renouvellement de Contrat** : 2 contrats à renouveler dans les 30 prochains jours")
            predictions.append("• **Activité Appels d'Offres** : 3 nouveaux appels d'offres attendus cette semaine selon les tendances historiques")
            predictions.append("• **Performance Fournisseur** : La trajectoire actuelle suggère un score de performance de 95%")
        else:
            predictions.append("• **Payment Processing**: Next payment likely in 3-5 business days")
            predictions.append("• **Contract Renewal**: 2 contracts due for renewal in next 30 days")
            predictions.append("• **RFQ Activity**: 3 new RFQs expected this week based on historical patterns")
            predictions.append("• **Supplier Performance**: Current trajectory suggests 95% performance score")
        
        return "\n".join(predictions)
        
    def _generate_optimizations(self, session: SessionState, language: str = 'en') -> str:
        """Generate process optimization suggestions"""
        optimizations = []
        
        if language == 'fr':
            optimizations.append("• **Traitement par Lots** : Grouper les factures similaires pour réduire le temps de traitement de 40%")
            optimizations.append("• **Préparation de Documents** : Pré-télécharger les documents pour accélérer les soumissions")
            optimizations.append("• **Rappels Automatisés** : Configurer des alertes pour les dates d'échéance de paiement")
            optimizations.append("• **Utilisation de Modèles** : Utiliser des modèles sauvegardés pour des réponses plus rapides aux appels d'offres")
        else:
            optimizations.append("• **Batch Processing**: Group similar invoices to reduce processing time by 40%")
            optimizations.append("• **Document Preparation**: Pre-upload documents to speed up submissions")
            optimizations.append("• **Automated Reminders**: Set up alerts for payment due dates")
            optimizations.append("• **Template Usage**: Use saved templates for faster RFQ responses")
        
        return "\n".join(optimizations)
        
    def _translate_procedure_content(self, content: str, language: str) -> str:
        """Translate procedure content to the specified language"""
        if language != 'fr':
            return content
        
        # Simple translation mapping for common procedure terms
        translations = {
            # Work Confirmation translations
            'Create Work Confirmation': 'Créer une Confirmation de Travail',
            'Login to i-Supplier Portal': 'Connexion au Portail i-Supplier',
            'Navigate to Work Confirmations': 'Naviguer vers les Confirmations de Travail',
            'Create New Work Confirmation': 'Créer une Nouvelle Confirmation de Travail',
            'Select Purchase Order': 'Sélectionner la Commande d\'Achat',
            'Enter Confirmation Details': 'Saisir les Détails de Confirmation',
            'Review and Submit': 'Réviser et Soumettre',
            
            # RFQ Response translations
            'RFQ Response': 'Réponse aux Appels d\'Offres',
            'Review RFQ Requirements': 'Réviser les Exigences de l\'Appel d\'Offres',
            'Prepare Quotation': 'Préparer la Cotation',
            'Submit Quotation': 'Soumettre la Cotation',
            'Analyze RFQ specifications and requirements': 'Analyser les spécifications et exigences de l\'appel d\'offres',
            'Create detailed quotation with pricing and technical details': 'Créer une cotation détaillée avec prix et détails techniques',
            'Submit the completed quotation before deadline': 'Soumettre la cotation complétée avant la date limite',
            'Carefully review technical specs, delivery requirements, and evaluation criteria': 'Examinez attentivement les spécifications techniques, les exigences de livraison et les critères d\'évaluation',
            'Fill in pricing, delivery schedule, and technical compliance details': 'Remplissez les prix, le calendrier de livraison et les détails de conformité technique',
            'Review all details and submit quotation through the portal': 'Révisez tous les détails et soumettez la cotation via le portail',
            'RFQ notification received': 'Notification d\'appel d\'offres reçue',
            'Technical specifications understood': 'Spécifications techniques comprises',
            'Pricing information ready': 'Informations de prix prêtes',
            
            # General translations
            'Access the Oracle EBS R12 i-Supplier portal using your credentials': 'Accédez au portail Oracle EBS R12 i-Supplier en utilisant vos identifiants',
            'Navigate to the i-Supplier portal URL and enter your username and password': 'Naviguez vers l\'URL du portail i-Supplier et saisissez votre nom d\'utilisateur et mot de passe',
            'Access the Work Confirmations section from the main menu': 'Accédez à la section Confirmations de Travail depuis le menu principal',
            'Click on \'Procurement\' in the main menu, then select \'Work Confirmations\'': 'Cliquez sur \'Approvisionnement\' dans le menu principal, puis sélectionnez \'Confirmations de Travail\'',
            'Initiate the creation of a new work confirmation': 'Initiez la création d\'une nouvelle confirmation de travail',
            'Click the \'Create\' button to start a new work confirmation': 'Cliquez sur le bouton \'Créer\' pour commencer une nouvelle confirmation de travail',
            'Choose the purchase order for which you want to create the work confirmation': 'Choisissez la commande d\'achat pour laquelle vous voulez créer la confirmation de travail',
            'Use the search functionality to find and select the appropriate purchase order': 'Utilisez la fonctionnalité de recherche pour trouver et sélectionner la commande d\'achat appropriée',
            'Fill in the work confirmation details including quantities and dates': 'Remplissez les détails de la confirmation de travail incluant les quantités et dates',
            'Enter the confirmed quantity, completion date, and any additional notes': 'Saisissez la quantité confirmée, la date d\'achèvement et toute note supplémentaire',
            'Review all entered information and submit the work confirmation': 'Révisez toutes les informations saisies et soumettez la confirmation de travail',
            'Verify all details are correct and click \'Submit\' to finalize the confirmation': 'Vérifiez que tous les détails sont corrects et cliquez sur \'Soumettre\' pour finaliser la confirmation',
            'Valid i-Supplier login credentials': 'Identifiants de connexion i-Supplier valides',
            'Active purchase order with services': 'Commande d\'achat active avec services',
            'Proper authorization level': 'Niveau d\'autorisation approprié'
        }
        
        translated_content = content
        for english, french in translations.items():
            translated_content = translated_content.replace(english, french)
        
        return translated_content
        
    async def _handle_dynamic_workflow_continuation(self, session: SessionState) -> ChatResponse:
        """Handle continuation of dynamic workflow"""
        
        steps = session.workflow_data.get('steps', [])
        current_step_num = int(session.current_step.split('_')[1])
        
        if current_step_num >= len(steps):
            # Workflow completed
            session.status = WorkflowStatus.COMPLETED
            session.current_step = None
            session.updated_at = datetime.now()
            
            return ChatResponse(
                message=f"Congratulations! You have completed the workflow for: **{session.workflow_data.get('original_question', 'Dynamic Workflow')}**\n\n" +
                       "All steps have been completed. Is there anything else I can help you with?",
                session_state=session,
                suggestions=["Start another procedure", "Ask another question", "Help"]
            )
        
        # Move to next step
        next_step = steps[current_step_num]
        next_step_id = f"step_{current_step_num + 1}"
        
        session.current_step = next_step_id
        session.completed_steps.append(f"step_{current_step_num}")
        session.updated_at = datetime.now()
        
        # Create workflow step
        workflow_step = WorkflowStep(
            step_id=next_step_id,
            title=f"Step {current_step_num + 1}: {next_step['title']}",
            description=next_step['description'],
            instructions=next_step['instructions'],
            next_steps=[f"step_{current_step_num + 2}"] if current_step_num + 1 < len(steps) else []
        )
        
        response_message = f"Step completed!\n\n"
        response_message += f"**Step {current_step_num + 1}: {next_step['title']}**\n"
        response_message += f"{next_step['description']}\n\n"
        response_message += f"**Instructions:** {next_step['instructions']}\n\n"
        response_message += "Type 'done' or 'next' when you've completed this step."
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            current_step=workflow_step,
            suggestions=["Done with this step", "Cancel procedure", "Help"]
        )
        
    async def _handle_cancel_procedure(self, session: SessionState) -> ChatResponse:
        """Handle procedure cancellation"""
        language = getattr(session, 'preferred_language', 'en')
        
        if session.current_procedure:
            procedure_title = self.procedures_data.get(session.current_procedure, {}).get('title', 'Unknown Procedure')
            
            # Reset procedure state but keep session
            session.current_procedure = None
            session.current_step = None
            session.status = WorkflowStatus.NOT_STARTED
            session.updated_at = datetime.now()
            
            if language == 'fr':
                message = f"Procédure '{procedure_title}' annulée.\n\nVotre session est toujours active. Que souhaitez-vous faire ensuite ?"
                suggestions = ["Afficher les procédures disponibles", "Commencer confirmation de travail", "Voir les commandes d'achat", "Aide"]
            else:
                message = f"Procedure '{procedure_title}' has been cancelled.\n\nYour session is still active. What would you like to do next?"
                suggestions = ["Show available procedures", "Start work confirmation", "View purchase orders", "Help"]
            
            return ChatResponse(
                message=message,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
        else:
            if language == 'fr':
                message = "Aucune procédure active à annuler. Que souhaitez-vous faire ?"
                suggestions = ["Afficher les procédures disponibles", "Commencer confirmation de travail", "Voir les commandes d'achat", "Aide"]
            else:
                message = "No active procedure to cancel. What would you like to do?"
                suggestions = ["Show available procedures", "Start work confirmation", "View purchase orders", "Help"]
            
            return ChatResponse(
                message=message,
                session_state=session,
                suggestions=suggestions,
                language=language
            )
            
    async def _handle_reset_session(self, session: SessionState) -> ChatResponse:
        """Handle session reset"""
        # Reset all session data
        session.current_procedure = None
        session.current_step = None
        session.completed_steps = []
        session.workflow_data = {}
        session.status = WorkflowStatus.NOT_STARTED
        session.updated_at = datetime.now()
        
        return ChatResponse(
            message="Session has been reset successfully!\n\n" +
                   "Welcome back to the Oracle EBS R12 i-Supplier Assistant for Tanger Med.\n\n" +
                   "I can help you with procedures, Oracle queries, and smart assistance. What would you like to do?",
            session_state=session,
            suggestions=[
                "Show available procedures",
                "Start work confirmation", 
                "View purchase orders",
                "Get recommendations",
                "Help"
            ]
        )
        
    async def _handle_language_switch(self, session: SessionState, language: str) -> ChatResponse:
        """Handle language switching"""
        # Update session language preference
        session.language = language
        session.preferred_language = language
        session.updated_at = datetime.now()
        
        if language == 'fr':
            message = "Langue changée en français ! 🇫🇷\n\n" + \
                     "Je suis votre assistant Oracle EBS R12 i-Supplier pour Tanger Med. " + \
                     "Je peux vous aider avec les procédures, les requêtes Oracle et l'assistance intelligente.\n\n" + \
                     "Que souhaitez-vous faire ?"
            suggestions = [
                "Afficher les procédures disponibles",
                "Commencer confirmation de travail",
                "Voir les commandes d'achat",
                "Obtenir des recommandations",
                "Aide"
            ]
        else:
            message = "Language switched to English! 🇺🇸\n\n" + \
                     "I'm your Oracle EBS R12 i-Supplier Assistant for Tanger Med. " + \
                     "I can help you with procedures, Oracle queries, and smart assistance.\n\n" + \
                     "What would you like to do?"
            suggestions = [
                "Show available procedures",
                "Start work confirmation",
                "View purchase orders",
                "Get recommendations",
                "Help"
            ]
        
        return ChatResponse(
            message=message,
            session_state=session,
            suggestions=suggestions,
            language=language
        )
        
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
        elif query_type == "dashboard" and module == "analytics":
            return data  # Return analytics data directly
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
        
    async def _handle_workflow_request(self, message: str, session: SessionState) -> ChatResponse:
        """Handle workflow/step-by-step requests by converting AI response to structured steps"""
        
        # Get AI response first
        if self.ebs_chatbot:
            try:
                context = {
                    'current_procedure': session.current_procedure,
                    'current_step': session.current_step,
                    'completed_steps': session.completed_steps
                }
                ai_response = await self.ebs_chatbot.get_response(message, context)
                
                # Convert AI response to workflow if it contains steps
                if self._contains_workflow_steps(ai_response):
                    return await self._create_dynamic_workflow(message, ai_response, session)
                else:
                    # Return AI response with workflow suggestions
                    return ChatResponse(
                        message=ai_response + "\n\nWould you like me to create a step-by-step workflow for this process?",
                        session_state=session,
                        suggestions=["Create workflow", "Show procedures", "Help"]
                    )
            except Exception as e:
                print(f"Workflow AI error: {e}")
        
        # Fallback to general handling
        return await self._handle_general_query(message, session)
        
    def _contains_workflow_steps(self, text: str) -> bool:
        """Check if AI response contains workflow steps"""
        step_indicators = ['step 1', '1.', 'first', 'then', 'next', 'finally', 'step by step']
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in step_indicators)
        
    async def _create_dynamic_workflow(self, original_question: str, ai_response: str, session: SessionState) -> ChatResponse:
        """Create a dynamic workflow from AI response"""
        
        # Extract steps from AI response
        steps = self._extract_steps_from_response(ai_response)
        
        if not steps:
            return ChatResponse(
                message=ai_response,
                session_state=session,
                suggestions=["Show procedures", "Help"]
            )
        
        # Create dynamic procedure ID
        procedure_id = f"dynamic_{hash(original_question) % 10000}"
        
        # Start dynamic workflow
        session.current_procedure = procedure_id
        session.current_step = "step_1"
        session.status = WorkflowStatus.IN_PROGRESS
        session.updated_at = datetime.now()
        session.workflow_data = {"steps": steps, "original_question": original_question}
        
        first_step = steps[0] if steps else None
        if not first_step:
            return ChatResponse(
                message="Could not create workflow from the response.",
                session_state=session
            )
        
        # Get language for visual guide
        language = getattr(session, 'preferred_language', 'en')
        
        # Generate visual guide for dynamic step
        visual_guide = self._generate_dynamic_visual_guide(first_step, language)
        
        # Create workflow step
        workflow_step = WorkflowStep(
            step_id="step_1",
            title=f"Step 1: {first_step['title']}",
            description=first_step['description'],
            instructions=first_step['instructions'],
            screenshot=visual_guide.get('image_url'),
            next_steps=["step_2"] if len(steps) > 1 else []
        )
        
        response_message = f"**Dynamic Workflow: {original_question}**\n\n"
        response_message += f"**Step 1: {first_step['title']}**\n"
        response_message += f"{first_step['description']}\n\n"
        response_message += f"**Instructions:** {first_step['instructions']}\n\n"
        response_message += "Type 'done' or 'next' when you've completed this step."
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            current_step=workflow_step,
            suggestions=["Done with this step", "Cancel procedure", "Help"]
        )
        
    def _extract_steps_from_response(self, response: str) -> List[Dict[str, str]]:
        """Extract steps from AI response text"""
        steps = []
        lines = response.split('\n')
        current_step = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for step indicators
            if any(indicator in line.lower() for indicator in ['step 1', '1.', 'first']):
                if current_step:
                    steps.append(current_step)
                current_step = {
                    'title': line.replace('Step 1:', '').replace('1.', '').replace('First', '').strip(),
                    'description': '',
                    'instructions': ''
                }
            elif any(indicator in line.lower() for indicator in ['step 2', '2.', 'second', 'then', 'next']):
                if current_step:
                    steps.append(current_step)
                current_step = {
                    'title': line.replace('Step 2:', '').replace('2.', '').replace('Second', '').replace('Then', '').replace('Next', '').strip(),
                    'description': '',
                    'instructions': ''
                }
            elif any(indicator in line.lower() for indicator in ['step 3', '3.', 'third', 'finally']):
                if current_step:
                    steps.append(current_step)
                current_step = {
                    'title': line.replace('Step 3:', '').replace('3.', '').replace('Third', '').replace('Finally', '').strip(),
                    'description': '',
                    'instructions': ''
                }
            elif current_step:
                # Add to current step description/instructions
                if not current_step['description']:
                    current_step['description'] = line
                else:
                    current_step['instructions'] += ' ' + line
        
        if current_step:
            steps.append(current_step)
            
        return steps
        
    def _generate_dynamic_visual_guide(self, step_data: Dict[str, str], language: str = 'en') -> Dict:
        """Generate visual guide for dynamic workflow steps"""
        
        # Map step content to appropriate base image
        step_title = step_data.get('title', '').lower()
        step_instructions = step_data.get('instructions', '').lower()
        
        # Determine appropriate base image based on step content
        if 'login' in step_title or 'connexion' in step_title:
            base_image = 'login_screen.png'
        elif 'navigate' in step_title or 'menu' in step_instructions or 'naviguer' in step_title:
            base_image = 'navigate_confirmations.png'
        elif 'create' in step_title or 'créer' in step_title:
            base_image = 'create_confirmation.png'
        elif 'search' in step_instructions or 'select' in step_instructions or 'rechercher' in step_instructions:
            base_image = 'select_po.png'
        elif 'enter' in step_instructions or 'fill' in step_instructions or 'saisir' in step_instructions:
            base_image = 'confirmation_details.png'
        elif 'submit' in step_title or 'soumettre' in step_title:
            base_image = 'review_submit.png'
        else:
            base_image = 'placeholder.png'
        
        # Generate annotated image
        annotated_image_url = enhanced_visual_guide_generator.create_placeholder_image(base_image, language)
        
        return {
            "has_visual": True,
            "image_url": annotated_image_url,
            "base_image": base_image
        }
