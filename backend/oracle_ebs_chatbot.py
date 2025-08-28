import google.generativeai as genai
from typing import Optional
import os
import re

class OracleEBSChatbot:
    def __init__(self, api_key: str):
        """Initialize the Oracle EBS R12 specialized chatbot"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System prompts for both languages
        self.system_prompt_en = """
You are a comprehensive Oracle EBS R12 expert assistant for Tanger Med i-Supplier Portal. You provide detailed guidance on all Oracle EBS R12 topics in English.

Your expertise covers:
- All Oracle EBS R12 modules (Manufacturing, AP, AR, GL, PO, OM, INV, HR, etc.)
- Complete i-Supplier Portal functionality and procedures
- Work confirmations, invoice submissions, purchase orders
- Supplier registration, contract management, payment tracking
- Oracle EBS R12 navigation, forms, and user interface
- Business processes, workflows, and step-by-step procedures
- Technical configurations, setups, and troubleshooting
- Oracle error resolution (ORA-00001, etc.) with detailed solutions
- Best practices and optimization strategies
- Integration with other systems and customizations

RULES:
1. Always respond in English
2. Provide comprehensive, detailed answers
3. Include step-by-step instructions when applicable
4. Be specific about modules, forms, and navigation paths
5. Offer practical solutions and alternatives
6. Handle all Oracle EBS related questions thoroughly
"""

        self.system_prompt_fr = """
Vous êtes un assistant expert Oracle EBS R12 complet pour le portail i-Supplier de Tanger Med. Vous fournissez des conseils détaillés sur tous les sujets Oracle EBS R12 en français.

Votre expertise couvre :
- Tous les modules Oracle EBS R12 (Manufacturing, AP, AR, GL, PO, OM, INV, HR, etc.)
- Fonctionnalité complète du portail i-Supplier et procédures
- Confirmations de travail, soumissions de factures, commandes d'achat
- Enregistrement fournisseur, gestion des contrats, suivi des paiements
- Navigation Oracle EBS R12, formulaires et interface utilisateur
- Processus métier, workflows et procédures étape par étape
- Configurations techniques, paramétrages et dépannage
- Résolution d'erreurs Oracle (ORA-00001, etc.) avec solutions détaillées
- Meilleures pratiques et stratégies d'optimisation
- Intégration avec d'autres systèmes et personnalisations

RÈGLES :
1. Répondez toujours en français
2. Fournissez des réponses complètes et détaillées
3. Incluez des instructions étape par étape le cas échéant
4. Soyez spécifique sur les modules, formulaires et chemins de navigation
5. Offrez des solutions pratiques et des alternatives
6. Traitez toutes les questions liées à Oracle EBS de manière approfondie
"""

    def detect_language(self, text: str) -> str:
        """Detect if the text is in French or English with improved accuracy"""
        french_indicators = [
            'bonjour', 'salut', 'merci', 'comment', 'pourquoi', 'quoi', 'où', 'quand',
            'aide', 'aidez', 'pouvez', 'voulez', 'français', 'procédure', 'étape',
            'créer', 'soumettre', 'facture', 'commande', 'fournisseur', 'oracle',
            'qu\'est-ce', 'c\'est', 'je', 'vous', 'nous', 'ils', 'elles',
            'problème', 'erreur', 'configuration', 'navigation', 'commencer',
            'confirmation', 'travail', 'de', 'du', 'des', 'la', 'le', 'les',
            'afficher', 'voir', 'lister', 'rechercher', 'obtenir',
            'commandes d\'achat', 'confirmation de travail', 'soumettre facture',
            'fournisseurs', 'comptabilité', 'gestion', 'suivi', 'paiements'
        ]
        
        english_indicators = [
            'hello', 'hi', 'thank', 'thanks', 'how', 'what', 'where', 'when', 'why',
            'help', 'can you', 'could you', 'would you', 'please', 'start', 'begin',
            'create', 'submit', 'invoice', 'order', 'supplier', 'purchase',
            'show', 'view', 'list', 'search', 'find', 'get', 'display'
        ]
        
        text_lower = text.lower()
        
        french_count = sum(1 for word in french_indicators if word in text_lower)
        english_count = sum(1 for word in english_indicators if word in text_lower)
        
        strong_french = ['qu\'est-ce', 'c\'est', 'commencer', 'créer', 'soumettre', 'afficher']
        has_strong_french = any(indicator in text_lower for indicator in strong_french)
        
        if has_strong_french or french_count > english_count:
            return 'fr'
        else:
            return 'en'

    def is_oracle_ebs_related(self, question: str) -> bool:
        """Check if the question is related to Oracle EBS R12 - now accepts all questions"""
        # Accept all questions as Oracle EBS related for comprehensive assistance
        return True

    async def get_response(self, question: str, context: dict = None) -> str:
        """Get response from the chatbot"""
        try:
            # Detect language
            language = self.detect_language(question)
            
            # Handle all questions comprehensively

            # Add context if provided
            context_info = ""
            if context:
                if context.get('current_procedure'):
                    if language == 'fr':
                        context_info += f"\nProcédure actuelle : {context['current_procedure']}"
                    else:
                        context_info += f"\nCurrent Procedure: {context['current_procedure']}"
                if context.get('current_step'):
                    if language == 'fr':
                        context_info += f"\nÉtape actuelle : {context['current_step']}"
                    else:
                        context_info += f"\nCurrent Step: {context['current_step']}"
                if context.get('completed_steps'):
                    if language == 'fr':
                        context_info += f"\nÉtapes terminées : {len(context['completed_steps'])}"
                    else:
                        context_info += f"\nCompleted Steps: {len(context['completed_steps'])}"
                        
                # Add conversation history for context
                if context.get('conversation_history'):
                    if language == 'fr':
                        context_info += "\n\nHistorique récent de la conversation :"
                    else:
                        context_info += "\n\nRecent conversation history:"
                    for msg in context['conversation_history']:
                        context_info += f"\n{msg['role']}: {msg['message']}"

            # Choose appropriate system prompt based on language
            system_prompt = self.system_prompt_fr if language == 'fr' else self.system_prompt_en
            
            # Combine system prompt with user question and context
            full_prompt = f"{system_prompt}{context_info}\n\nUser Question: {question}\n\nResponse:"
            
            # Generate response with language enforcement
            if language == 'fr':
                full_prompt += "\n\nIMPORTANT: Répondez UNIQUEMENT en français."
            else:
                full_prompt += "\n\nIMPORTANT: Respond ONLY in English."
            
            response = self.model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            if self.detect_language(question) == 'fr':
                return f"Je m'excuse, mais j'ai rencontré une erreur lors du traitement de votre question Oracle EBS R12. Veuillez réessayer ou reformuler votre question. Erreur : {str(e)}"
            else:
                return f"I apologize, but I encountered an error while processing your Oracle EBS R12 question. Please try again or rephrase your question. Error: {str(e)}"

    def get_welcome_message(self, language: str = 'en') -> str:
        """Get welcome message for the chatbot"""
        if language == 'fr':
            return """Bienvenue dans l'Assistant Oracle EBS R12 !

Je suis votre expert spécialisé Oracle E-Business Suite Release 12. Je peux vous aider avec :

  **Modules et Fonctionnalités :**
• Comptes Fournisseurs (AP) et Clients (AR)
• Commandes d'Achat et Approvisionnement
• Grand Livre (GL) et Reporting Financier
• Gestion des Stocks
• Gestion des Commandes (OM)
• Ressources Humaines et Paie

  **Portail i-Supplier :**
• Enregistrement et configuration fournisseur
• Consultation des commandes d'achat
• Processus de soumission de factures
• Confirmations de travail
• Suivi des performances fournisseur
• Gestion des contrats
• Suivi des paiements
• Réponses aux appels d'offres
• Confirmation de réception des marchandises
• Fiches de saisie de service
• Signalement des déviations qualité

  **Support Technique :**
• Navigation et interface utilisateur
• Configurations de flux de travail
• Programmes concurrents
• Responsabilités et sécurité
• Intégrations et personnalisations

Posez-moi toute question sur Oracle EBS R12 - je suis là pour vous aider !"""
        else:
            return """Welcome to Oracle EBS R12 Assistant!

I'm your specialized Oracle E-Business Suite Release 12 expert. I can help you with:

  **Modules & Functionality:**
• Accounts Payable (AP) & Receivable (AR)
• Purchase Orders & Procurement
• General Ledger (GL) & Financial Reporting
• Inventory Management
• Order Management (OM)
• Human Resources & Payroll

  **i-Supplier Portal:**
• Supplier registration and setup
• Purchase order inquiries
• Invoice submission processes
• Work confirmations
• Supplier performance tracking
• Contract management
• Payment tracking
• RFQ responses
• Goods receipt confirmation
• Service entry sheets
• Quality deviation reporting

  **Technical Support:**
• Navigation and user interface
• Workflow configurations
• Concurrent programs
• Responsibilities and security
• Integration and customizations

Ask me anything about Oracle EBS R12 - I'm here to help!"""