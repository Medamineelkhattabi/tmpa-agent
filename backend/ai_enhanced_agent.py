import json
import os
import re
import uuid
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass

# AI/ML imports (simulated for demo - would use real libraries)
import random
import hashlib

from .models import (
    ChatResponse, SessionState, WorkflowStep, MessageType, 
    WorkflowStatus, ProcedureInfo, ValidationRule
)

@dataclass
class AIInsight:
    """Represents an AI-generated insight"""
    type: str
    confidence: float
    message: str
    action_items: List[str]
    priority: str

@dataclass
class PredictionResult:
    """Results from AI predictions"""
    prediction: Any
    confidence: float
    factors: List[str]
    recommendation: str

class AdvancedAIOracle:
    """
    Advanced AI-enhanced Oracle EBS agent with sophisticated capabilities:
    - Natural Language Processing
    - Predictive Analytics
    - Intelligent Automation
    - Context-Aware Recommendations
    - Risk Assessment
    - Performance Optimization
    """
    
    def __init__(self):
        self.procedures_data = {}
        self.oracle_modules = {}
        self.validation_rules = {}
        self.ai_features = {}
        self.mock_oracle_data = {}
        self.user_patterns = {}
        self.ai_models = {}
        
    async def initialize(self):
        """Initialize the advanced AI agent"""
        await self._load_advanced_procedures()
        await self._load_mock_data()
        await self._initialize_ai_models()
        
    async def _load_advanced_procedures(self):
        """Load advanced procedures with AI features"""
        try:
            with open('/workspace/procedures_advanced.json', 'r') as f:
                data = json.load(f)
                self.procedures_data = data.get('procedures', {})
                self.oracle_modules = data.get('oracle_modules', {})
                self.validation_rules = data.get('validation_rules', {})
                self.ai_features = data.get('ai_features', {})
        except FileNotFoundError:
            # Fallback to basic procedures
            with open('/workspace/procedures.json', 'r') as f:
                data = json.load(f)
                self.procedures_data = data.get('procedures', {})
                self.oracle_modules = data.get('oracle_modules', {})
                self.validation_rules = data.get('validation_rules', {})
                
    async def _load_mock_data(self):
        """Load enhanced mock Oracle data with AI-generated insights"""
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
                    "ai_risk_score": 0.2,
                    "predicted_delivery": "2024-02-13",
                    "savings_opportunity": 2500.00
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
                    "ai_risk_score": 0.6,
                    "predicted_delivery": "2024-02-25",
                    "savings_opportunity": 1200.00
                }
            ],
            "invoices": [
                {
                    "invoice_number": "INV-2024-001",
                    "po_number": "PO-2024-001",
                    "supplier": "Tanger Med Services",
                    "amount": 12500.00,
                    "status": "Submitted",
                    "submission_date": "2024-01-25",
                    "ai_fraud_score": 0.1,
                    "payment_prediction": "2024-02-25",
                    "approval_probability": 0.95
                }
            ],
            "suppliers": [
                {
                    "supplier_id": "SUP-001",
                    "name": "Tanger Med Services",
                    "status": "Active",
                    "contact_email": "contact@tangermed-services.com",
                    "registration_date": "2023-06-01",
                    "performance_score": 8.7,
                    "risk_level": "Low",
                    "predicted_growth": 0.15,
                    "reliability_score": 0.92
                },
                {
                    "supplier_id": "SUP-002",
                    "name": "Mediterranean Logistics",
                    "status": "Active", 
                    "contact_email": "info@med-logistics.com",
                    "registration_date": "2023-08-15",
                    "performance_score": 7.2,
                    "risk_level": "Medium",
                    "predicted_growth": 0.08,
                    "reliability_score": 0.78
                }
            ],
            "contracts": [
                {
                    "contract_id": "CNT-2024-001",
                    "supplier": "Tanger Med Services",
                    "value": 500000.00,
                    "start_date": "2024-01-01",
                    "end_date": "2024-12-31",
                    "renewal_probability": 0.85,
                    "risk_factors": ["Currency fluctuation", "Service quality"],
                    "optimization_suggestions": ["Renegotiate payment terms", "Add performance bonuses"]
                }
            ],
            "budgets": [
                {
                    "department": "IT",
                    "allocated": 1000000.00,
                    "spent": 750000.00,
                    "remaining": 250000.00,
                    "forecast_variance": -0.05,
                    "savings_opportunities": 50000.00,
                    "risk_areas": ["Software licenses", "Hardware procurement"]
                }
            ]
        }
        
    async def _initialize_ai_models(self):
        """Initialize AI models and algorithms"""
        self.ai_models = {
            "nlp_processor": self._create_nlp_processor(),
            "risk_assessor": self._create_risk_assessor(),
            "performance_predictor": self._create_performance_predictor(),
            "anomaly_detector": self._create_anomaly_detector(),
            "recommendation_engine": self._create_recommendation_engine()
        }
        
    def _create_nlp_processor(self):
        """Create NLP processor for understanding user intent"""
        return {
            "intent_patterns": {
                "create_procedure": ["create", "start", "begin", "new", "initiate"],
                "query_data": ["show", "display", "list", "find", "search", "get"],
                "help_request": ["help", "how", "what", "explain", "guide"],
                "status_check": ["status", "progress", "state", "current"],
                "optimization": ["optimize", "improve", "enhance", "better"],
                "prediction": ["predict", "forecast", "estimate", "expect"],
                "analysis": ["analyze", "review", "examine", "assess"]
            },
            "entity_extractors": {
                "po_number": r"po[-\s]?(\d{4}-\d{3})",
                "invoice_number": r"inv[-\s]?(\d{4}-\d{3})",
                "supplier_name": r"supplier\s+([a-zA-Z\s]+)",
                "date_range": r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})",
                "amount": r"(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(mad|usd|eur)?"
            }
        }
    
    def _create_risk_assessor(self):
        """Create AI risk assessment model"""
        return {
            "risk_factors": {
                "supplier": ["performance_history", "financial_stability", "compliance_record"],
                "contract": ["value", "duration", "complexity", "jurisdiction"],
                "payment": ["amount", "currency", "terms", "supplier_reliability"],
                "delivery": ["timeline", "complexity", "supplier_capacity", "external_factors"]
            },
            "risk_weights": {
                "low": 0.3,
                "medium": 0.6,
                "high": 0.9
            }
        }
    
    def _create_performance_predictor(self):
        """Create performance prediction model"""
        return {
            "prediction_models": {
                "delivery_time": "linear_regression",
                "supplier_performance": "ensemble",
                "budget_variance": "time_series",
                "contract_renewal": "classification"
            },
            "features": {
                "historical_performance": 0.4,
                "market_conditions": 0.3,
                "supplier_metrics": 0.2,
                "seasonal_factors": 0.1
            }
        }
    
    def _create_anomaly_detector(self):
        """Create anomaly detection system"""
        return {
            "detection_algorithms": ["isolation_forest", "statistical_outliers", "pattern_matching"],
            "anomaly_types": {
                "spending": "unusual_amount_patterns",
                "timing": "irregular_submission_times",
                "supplier": "performance_deviations",
                "compliance": "policy_violations"
            }
        }
    
    def _create_recommendation_engine(self):
        """Create AI recommendation system"""
        return {
            "recommendation_types": {
                "process_optimization": "workflow_improvements",
                "cost_savings": "financial_optimizations",
                "risk_mitigation": "risk_reduction_strategies",
                "performance_enhancement": "efficiency_improvements"
            },
            "personalization_factors": ["user_role", "usage_patterns", "preferences", "context"]
        }

    async def process_message_advanced(self, message: str, session: SessionState, context: Dict[str, Any] = {}) -> ChatResponse:
        """Advanced message processing with AI capabilities"""
        
        # Enhanced NLP processing
        intent_analysis = await self._analyze_intent_advanced(message)
        entities = await self._extract_entities(message)
        context_analysis = await self._analyze_context(session, context)
        
        # Generate AI insights
        ai_insights = await self._generate_ai_insights(message, session, intent_analysis)
        
        # Process based on advanced intent
        if intent_analysis["primary_intent"] == "start_procedure":
            return await self._handle_procedure_start_advanced(message, session, entities, ai_insights)
        elif intent_analysis["primary_intent"] == "continue_procedure":
            return await self._handle_procedure_continuation_advanced(message, session, ai_insights)
        elif intent_analysis["primary_intent"] == "oracle_query":
            return await self._handle_oracle_query_advanced(message, session, entities, ai_insights)
        elif intent_analysis["primary_intent"] == "optimization_request":
            return await self._handle_optimization_request(message, session, ai_insights)
        elif intent_analysis["primary_intent"] == "prediction_request":
            return await self._handle_prediction_request(message, session, entities)
        elif intent_analysis["primary_intent"] == "analysis_request":
            return await self._handle_analysis_request(message, session, entities)
        else:
            return await self._handle_general_query_advanced(message, session, ai_insights)
    
    async def _analyze_intent_advanced(self, message: str) -> Dict[str, Any]:
        """Advanced intent analysis with confidence scores"""
        message_lower = message.lower()
        intent_scores = {}
        
        nlp = self.ai_models["nlp_processor"]
        
        for intent, patterns in nlp["intent_patterns"].items():
            score = sum(1 for pattern in patterns if pattern in message_lower) / len(patterns)
            intent_scores[intent] = score
        
        # Add context-aware intent detection
        if any(word in message_lower for word in ["optimize", "improve", "better", "enhance"]):
            intent_scores["optimization_request"] = 0.8
        
        if any(word in message_lower for word in ["predict", "forecast", "will", "expect"]):
            intent_scores["prediction_request"] = 0.7
            
        if any(word in message_lower for word in ["analyze", "analysis", "review", "assess"]):
            intent_scores["analysis_request"] = 0.6
        
        primary_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        return {
            "primary_intent": primary_intent[0],
            "confidence": primary_intent[1],
            "all_scores": intent_scores,
            "complexity": self._assess_query_complexity(message)
        }
    
    async def _extract_entities(self, message: str) -> Dict[str, List[str]]:
        """Extract entities using advanced NLP"""
        entities = {}
        nlp = self.ai_models["nlp_processor"]
        
        for entity_type, pattern in nlp["entity_extractors"].items():
            matches = re.findall(pattern, message.lower())
            if matches:
                entities[entity_type] = matches
                
        return entities
    
    async def _analyze_context(self, session: SessionState, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze conversation and session context"""
        return {
            "session_duration": (datetime.now() - session.created_at).total_seconds() / 60,
            "procedure_progress": len(session.completed_steps) if session.completed_steps else 0,
            "user_experience_level": self._infer_user_experience(session),
            "current_focus": session.current_procedure or "exploration",
            "interaction_pattern": self._analyze_interaction_pattern(session)
        }
    
    async def _generate_ai_insights(self, message: str, session: SessionState, intent_analysis: Dict) -> List[AIInsight]:
        """Generate AI-powered insights and recommendations"""
        insights = []
        
        # Proactive suggestions based on context
        if session.current_procedure and len(session.completed_steps) > 2:
            insights.append(AIInsight(
                type="efficiency",
                confidence=0.8,
                message="You're making good progress! AI suggests taking a screenshot for your records.",
                action_items=["Capture current screen", "Save progress notes"],
                priority="medium"
            ))
        
        # Risk-based insights
        if "invoice" in message.lower():
            insights.append(AIInsight(
                type="risk_mitigation",
                confidence=0.9,
                message="AI detected invoice-related activity. Recommending duplicate check.",
                action_items=["Verify invoice uniqueness", "Check amount against PO"],
                priority="high"
            ))
        
        # Performance optimization insights
        if intent_analysis["complexity"] > 0.7:
            insights.append(AIInsight(
                type="optimization",
                confidence=0.7,
                message="Complex query detected. AI can break this down into simpler steps.",
                action_items=["Simplify query", "Use guided workflow"],
                priority="low"
            ))
        
        return insights
    
    async def _handle_procedure_start_advanced(self, message: str, session: SessionState, entities: Dict, ai_insights: List[AIInsight]) -> ChatResponse:
        """Advanced procedure start with AI enhancements"""
        
        # Extract procedure from message with AI assistance
        procedure_id = self._extract_procedure_id_advanced(message, entities)
        
        if not procedure_id:
            # AI-powered procedure recommendation
            recommended_procedures = await self._recommend_procedures(session, message)
            suggestions = [f"Start {proc['title']}" for proc in recommended_procedures[:5]]
            
            response_message = "🤖 **AI-Enhanced Procedure Assistant**\n\n"
            response_message += "Based on your query, I recommend these Oracle EBS procedures:\n\n"
            
            for proc in recommended_procedures[:3]:
                response_message += f"• **{proc['title']}** ({proc['difficulty']}) - {proc['estimated_time']}\n"
                response_message += f"  {proc['description']}\n\n"
            
            # Add AI insights
            if ai_insights:
                response_message += "💡 **AI Insights:**\n"
                for insight in ai_insights[:2]:
                    response_message += f"• {insight.message}\n"
            
            return ChatResponse(
                message=response_message,
                session_state=session,
                suggestions=suggestions
            )
            
        if procedure_id not in self.procedures_data:
            return ChatResponse(
                message=f"I don't have information about '{procedure_id}'. Let me suggest alternatives...",
                session_state=session,
                suggestions=["Show available procedures"]
            )
            
        # Enhanced procedure start with AI features
        procedure = self.procedures_data[procedure_id]
        first_step = procedure['steps'][0] if procedure['steps'] else None
        
        if not first_step:
            return ChatResponse(
                message=f"The procedure '{procedure['title']}' has no defined steps.",
                session_state=session
            )
        
        # AI risk assessment for procedure
        risk_assessment = await self._assess_procedure_risk(procedure_id, session)
        
        # Update session state
        session.current_procedure = procedure_id
        session.current_step = first_step['step_id']
        session.status = WorkflowStatus.IN_PROGRESS
        session.updated_at = datetime.now()
        
        # Create enhanced workflow step
        workflow_step = WorkflowStep(
            step_id=first_step['step_id'],
            title=first_step['title'],
            description=first_step['description'],
            instructions=first_step['instructions'],
            screenshot=first_step.get('screenshot'),
            validation_criteria=first_step.get('validation_criteria', []),
            next_steps=first_step.get('next_steps', [])
        )
        
        # Enhanced response with AI features
        response_message = f"🚀 **Starting Enhanced Procedure: {procedure['title']}**\n\n"
        
        # AI-generated procedure overview
        response_message += f"**📊 AI Analysis:**\n"
        response_message += f"• Difficulty: {procedure.get('difficulty', 'Not rated')}\n"
        response_message += f"• Estimated Time: {procedure.get('estimated_time', 'Variable')}\n"
        response_message += f"• Risk Level: {risk_assessment['level']}\n\n"
        
        # AI features available
        ai_features = procedure.get('ai_features', {})
        if ai_features:
            response_message += f"**🤖 AI Features Available:**\n"
            for feature, enabled in ai_features.items():
                if enabled:
                    feature_name = feature.replace('_', ' ').title()
                    response_message += f"• {feature_name}\n"
            response_message += "\n"
        
        response_message += f"**Prerequisites:**\n"
        for prereq in procedure.get('prerequisites', []):
            response_message += f"• {prereq}\n"
        response_message += f"\n**Step 1: {first_step['title']}**\n"
        response_message += f"{first_step['description']}\n\n"
        response_message += f"**Instructions:** {first_step['instructions']}\n\n"
        
        # AI hints
        ai_hints = first_step.get('ai_hints', [])
        if ai_hints:
            response_message += f"**💡 AI Tips:**\n"
            for hint in ai_hints:
                response_message += f"• {hint}\n"
            response_message += "\n"
        
        response_message += "Type 'done' or 'next' when you've completed this step."
        
        suggestions = ["Done with this step", "Show screenshot", "AI assistance", "Cancel procedure"]
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            current_step=workflow_step,
            screenshot=first_step.get('screenshot'),
            suggestions=suggestions
        )
    
    async def _handle_optimization_request(self, message: str, session: SessionState, ai_insights: List[AIInsight]) -> ChatResponse:
        """Handle requests for optimization suggestions"""
        
        optimization_areas = await self._identify_optimization_opportunities(session)
        
        response_message = "🔧 **AI-Powered Optimization Recommendations**\n\n"
        
        for area in optimization_areas:
            response_message += f"**{area['category']}**\n"
            response_message += f"• Current Status: {area['current_state']}\n"
            response_message += f"• Optimization Potential: {area['potential']}\n"
            response_message += f"• Recommended Actions:\n"
            for action in area['actions']:
                response_message += f"  - {action}\n"
            response_message += f"• Expected Benefits: {area['benefits']}\n\n"
        
        suggestions = [
            "Implement suggestions",
            "Get detailed analysis",
            "Schedule optimization",
            "Export recommendations"
        ]
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            suggestions=suggestions
        )
    
    async def _handle_prediction_request(self, message: str, session: SessionState, entities: Dict) -> ChatResponse:
        """Handle predictive analytics requests"""
        
        prediction_results = await self._generate_predictions(message, entities, session)
        
        response_message = "🔮 **AI Predictive Analytics**\n\n"
        
        for prediction in prediction_results:
            response_message += f"**{prediction.prediction}**\n"
            response_message += f"• Confidence: {prediction.confidence:.1%}\n"
            response_message += f"• Key Factors:\n"
            for factor in prediction.factors:
                response_message += f"  - {factor}\n"
            response_message += f"• Recommendation: {prediction.recommendation}\n\n"
        
        suggestions = [
            "Get more details",
            "Update parameters",
            "Export forecast",
            "Set up alerts"
        ]
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            suggestions=suggestions
        )
    
    async def _handle_analysis_request(self, message: str, session: SessionState, entities: Dict) -> ChatResponse:
        """Handle data analysis requests"""
        
        analysis_results = await self._perform_advanced_analysis(message, entities)
        
        response_message = "📊 **AI-Powered Analysis Results**\n\n"
        
        for analysis in analysis_results:
            response_message += f"**{analysis['title']}**\n"
            response_message += f"• Summary: {analysis['summary']}\n"
            response_message += f"• Key Findings:\n"
            for finding in analysis['findings']:
                response_message += f"  - {finding}\n"
            response_message += f"• Recommendations:\n"
            for rec in analysis['recommendations']:
                response_message += f"  - {rec}\n"
            response_message += "\n"
        
        suggestions = [
            "Drill down analysis",
            "Export report",
            "Compare periods",
            "Set benchmarks"
        ]
        
        return ChatResponse(
            message=response_message,
            session_state=session,
            suggestions=suggestions
        )
    
    async def _recommend_procedures(self, session: SessionState, message: str) -> List[Dict]:
        """AI-powered procedure recommendations"""
        
        # Simulate AI recommendation logic
        all_procedures = []
        for proc_id, proc_data in self.procedures_data.items():
            score = self._calculate_recommendation_score(proc_data, session, message)
            all_procedures.append({
                **proc_data,
                "procedure_id": proc_id,
                "recommendation_score": score
            })
        
        # Sort by recommendation score
        return sorted(all_procedures, key=lambda x: x.get("recommendation_score", 0), reverse=True)
    
    def _calculate_recommendation_score(self, procedure: Dict, session: SessionState, message: str) -> float:
        """Calculate AI recommendation score for a procedure"""
        score = 0.5  # Base score
        
        # Keyword matching
        message_lower = message.lower()
        title_lower = procedure.get('title', '').lower()
        description_lower = procedure.get('description', '').lower()
        
        if any(word in title_lower for word in message_lower.split()):
            score += 0.3
            
        if any(word in description_lower for word in message_lower.split()):
            score += 0.2
        
        # User experience level consideration
        difficulty = procedure.get('difficulty', 'intermediate')
        user_experience = self._infer_user_experience(session)
        
        if difficulty == 'beginner' and user_experience == 'novice':
            score += 0.2
        elif difficulty == 'advanced' and user_experience == 'expert':
            score += 0.2
        
        return min(score, 1.0)
    
    def _infer_user_experience(self, session: SessionState) -> str:
        """Infer user experience level from session data"""
        completed_procedures = len(session.completed_steps) if session.completed_steps else 0
        
        if completed_procedures == 0:
            return "novice"
        elif completed_procedures < 5:
            return "intermediate"
        else:
            return "expert"
    
    def _assess_query_complexity(self, message: str) -> float:
        """Assess the complexity of a user query"""
        factors = [
            len(message.split()) > 10,  # Long message
            len(re.findall(r'\?', message)) > 1,  # Multiple questions
            any(word in message.lower() for word in ['and', 'or', 'but', 'also']),  # Complex logic
            len(re.findall(r'\d+', message)) > 2,  # Multiple numbers
        ]
        
        return sum(factors) / len(factors)
    
    def _analyze_interaction_pattern(self, session: SessionState) -> str:
        """Analyze user interaction patterns"""
        if not session.completed_steps:
            return "exploratory"
        elif len(session.completed_steps) > 3:
            return "task_focused"
        else:
            return "learning"
    
    async def _assess_procedure_risk(self, procedure_id: str, session: SessionState) -> Dict[str, Any]:
        """AI-powered procedure risk assessment"""
        
        # Simulate risk assessment
        risk_factors = {
            "work_confirmation": {"level": "Low", "factors": ["Standard procedure", "Low complexity"]},
            "supplier_registration": {"level": "Medium", "factors": ["Document requirements", "Compliance checks"]},
            "contract_management": {"level": "High", "factors": ["Legal implications", "Financial impact"]},
            "catalog_management": {"level": "Medium", "factors": ["Data complexity", "System integration"]}
        }
        
        return risk_factors.get(procedure_id, {"level": "Medium", "factors": ["Standard risk profile"]})
    
    async def _identify_optimization_opportunities(self, session: SessionState) -> List[Dict[str, Any]]:
        """Identify optimization opportunities using AI"""
        
        opportunities = [
            {
                "category": "Workflow Efficiency",
                "current_state": "Manual data entry in multiple steps",
                "potential": "High - 30% time reduction possible",
                "actions": [
                    "Enable auto-fill for common fields",
                    "Use barcode scanning for PO lookup",
                    "Implement bulk operations"
                ],
                "benefits": "Reduced processing time, fewer errors"
            },
            {
                "category": "Data Quality",
                "current_state": "Standard validation rules",
                "potential": "Medium - 15% error reduction",
                "actions": [
                    "Enable AI-powered validation",
                    "Add duplicate detection",
                    "Implement smart suggestions"
                ],
                "benefits": "Higher data accuracy, less rework"
            }
        ]
        
        return opportunities
    
    async def _generate_predictions(self, message: str, entities: Dict, session: SessionState) -> List[PredictionResult]:
        """Generate AI predictions based on request"""
        
        predictions = []
        
        # Delivery time prediction
        if "delivery" in message.lower() or "po" in message.lower():
            predictions.append(PredictionResult(
                prediction="Delivery Time Forecast",
                confidence=0.85,
                factors=["Historical supplier performance", "Current workload", "Seasonal patterns"],
                recommendation="Add 2-day buffer for critical deliveries"
            ))
        
        # Budget prediction
        if "budget" in message.lower() or "spending" in message.lower():
            predictions.append(PredictionResult(
                prediction="Budget Variance Forecast",
                confidence=0.78,
                factors=["Current spending rate", "Planned initiatives", "Market conditions"],
                recommendation="Implement cost controls for Q2"
            ))
        
        return predictions
    
    async def _perform_advanced_analysis(self, message: str, entities: Dict) -> List[Dict[str, Any]]:
        """Perform advanced data analysis"""
        
        analyses = []
        
        if "supplier" in message.lower():
            analyses.append({
                "title": "Supplier Performance Analysis",
                "summary": "Analysis of top 10 suppliers over last 12 months",
                "findings": [
                    "Tanger Med Services: 92% on-time delivery",
                    "Mediterranean Logistics: 78% on-time delivery",
                    "Average performance improvement: 5% YoY"
                ],
                "recommendations": [
                    "Negotiate performance bonuses with top suppliers",
                    "Implement improvement plans for underperforming suppliers",
                    "Consider supplier diversification"
                ]
            })
        
        if "spend" in message.lower() or "cost" in message.lower():
            analyses.append({
                "title": "Spend Analysis",
                "summary": "Comprehensive spending pattern analysis",
                "findings": [
                    "IT services: 35% of total spend",
                    "Transportation: 25% of total spend", 
                    "Seasonal variation: ±15% in Q4"
                ],
                "recommendations": [
                    "Negotiate volume discounts for IT services",
                    "Explore transportation consolidation",
                    "Plan for Q4 budget increases"
                ]
            })
        
        return analyses
    
    def _extract_procedure_id_advanced(self, message: str, entities: Dict) -> Optional[str]:
        """Advanced procedure ID extraction with AI assistance"""
        message_lower = message.lower()
        
        # Enhanced procedure mappings with AI-powered matching
        procedure_mappings = {
            "work confirmation": "work_confirmation",
            "supplier registration": "supplier_registration", 
            "receipt acknowledgment": "receipt_acknowledgment",
            "payment inquiry": "payment_inquiry",
            "contract management": "contract_management",
            "supplier performance": "supplier_performance",
            "budget tracking": "budget_tracking",
            "catalog management": "catalog_management",
            "create work confirmation": "work_confirmation",
            "register supplier": "supplier_registration",
            "acknowledge receipt": "receipt_acknowledgment",
            "check payment": "payment_inquiry",
            "manage contract": "contract_management",
            "evaluate supplier": "supplier_performance",
            "track budget": "budget_tracking",
            "manage catalog": "catalog_management"
        }
        
        # Fuzzy matching with confidence scores
        best_match = None
        best_score = 0
        
        for phrase, procedure_id in procedure_mappings.items():
            # Simple similarity score
            phrase_words = set(phrase.split())
            message_words = set(message_lower.split())
            
            intersection = phrase_words.intersection(message_words)
            union = phrase_words.union(message_words)
            
            if union:
                similarity = len(intersection) / len(union)
                if similarity > best_score and similarity > 0.3:  # Threshold
                    best_score = similarity
                    best_match = procedure_id
        
        return best_match

    # Enhanced oracle query methods would go here...
    async def _handle_oracle_query_advanced(self, message: str, session: SessionState, entities: Dict, ai_insights: List[AIInsight]) -> ChatResponse:
        """Handle advanced Oracle queries with AI enhancement"""
        
        query_type, parameters = self._parse_oracle_query_advanced(message, entities)
        
        if not query_type:
            return ChatResponse(
                message="🤖 **AI-Enhanced Oracle Assistant**\n\nI can help you query Oracle EBS data with advanced AI features:\n\n" +
                       "• **Smart Search**: Natural language queries\n" +
                       "• **Predictive Analytics**: Forecast trends and patterns\n" +
                       "• **Risk Assessment**: Identify potential issues\n" +
                       "• **Performance Insights**: Optimization recommendations\n\n" +
                       "Try: 'Show me high-risk purchase orders' or 'Predict payment delays'",
                session_state=session,
                suggestions=["Show AI insights", "Analyze spending patterns", "Predict delivery dates", "Assess supplier risks"]
            )
        
        try:
            # Enhanced query with AI features
            result = await self.query_oracle_module_advanced(query_type['module'], query_type['type'], parameters)
            
            if not result:
                return ChatResponse(
                    message="No data found for your query. AI suggests refining your search criteria.",
                    session_state=session,
                    suggestions=["Broaden search", "Try different keywords", "Check date ranges"]
                )
            
            # AI-enhanced response formatting
            formatted_response = self._format_oracle_response_advanced(query_type['module'], result, ai_insights)
            
            return ChatResponse(
                message=formatted_response,
                session_state=session,
                oracle_data=result,
                suggestions=["Get AI insights", "Export data", "Set up alerts", "Drill down analysis"]
            )
            
        except Exception as e:
            return ChatResponse(
                message=f"AI detected an error in data retrieval: {str(e)}. Suggesting alternative approaches...",
                session_state=session,
                message_type=MessageType.ERROR,
                suggestions=["Try simplified query", "Check system status", "Contact support"]
            )

    def _parse_oracle_query_advanced(self, message: str, entities: Dict) -> Tuple[Optional[Dict], Dict[str, Any]]:
        """Advanced Oracle query parsing with entity recognition"""
        message_lower = message.lower()
        
        # Enhanced query patterns with AI assistance
        if any(keyword in message_lower for keyword in ["high-risk", "risky", "risk assessment"]):
            return {"module": "suppliers", "type": "risk_analysis"}, {}
        
        if any(keyword in message_lower for keyword in ["predict", "forecast", "estimate"]):
            if "delivery" in message_lower:
                return {"module": "purchase_orders", "type": "delivery_prediction"}, {}
            elif "payment" in message_lower:
                return {"module": "invoices", "type": "payment_prediction"}, {}
        
        if any(keyword in message_lower for keyword in ["optimize", "improve", "savings"]):
            return {"module": "spending", "type": "optimization_analysis"}, {}
        
        # Standard query patterns with entity extraction
        if any(keyword in message_lower for keyword in ["po", "purchase order", "purchase orders"]):
            po_numbers = entities.get("po_number", [])
            if po_numbers:
                return {"module": "purchase_orders", "type": "search_by_po_number"}, {"po_number": po_numbers[0].upper()}
            return {"module": "purchase_orders", "type": "list_all"}, {}
        
        # Continue with other patterns...
        return None, {}

    async def query_oracle_module_advanced(self, module: str, query_type: str, parameters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Advanced Oracle module querying with AI enhancements"""
        
        if module not in self.mock_oracle_data:
            return []
        
        data = self.mock_oracle_data[module]
        
        # AI-enhanced query processing
        if query_type == "risk_analysis":
            # Return high-risk items with AI scoring
            return [item for item in data if item.get("ai_risk_score", 0) > 0.5]
        
        elif query_type == "delivery_prediction":
            # Add AI predictions to results
            enhanced_data = []
            for item in data:
                if "delivery_date" in item:
                    item["ai_prediction"] = {
                        "predicted_date": item.get("predicted_delivery", item["delivery_date"]),
                        "confidence": 0.85,
                        "risk_factors": ["Weather conditions", "Supplier capacity"]
                    }
                enhanced_data.append(item)
            return enhanced_data
        
        elif query_type == "optimization_analysis":
            # Add optimization suggestions
            for item in data:
                item["optimization_suggestions"] = [
                    f"Potential savings: {item.get('savings_opportunity', 0)} MAD",
                    "Consider bulk ordering for better rates",
                    "Negotiate payment terms for cash flow optimization"
                ]
            return data
        
        # Standard query processing
        return data

    def _format_oracle_response_advanced(self, module: str, data: List[Dict], ai_insights: List[AIInsight]) -> str:
        """Advanced response formatting with AI insights"""
        
        if module == "purchase_orders":
            response = f"🤖 **AI-Enhanced Purchase Orders ({len(data)} found):**\n\n"
            for po in data:
                risk_emoji = "🔴" if po.get("ai_risk_score", 0) > 0.5 else "🟢"
                response += f"{risk_emoji} **{po['po_number']}** (Risk: {po.get('ai_risk_score', 0):.1%})\n"
                response += f"   • Supplier: {po['supplier']}\n"
                response += f"   • Amount: {po['amount']} {po['currency']}\n"
                response += f"   • Status: {po['status']}\n"
                
                if po.get("predicted_delivery"):
                    response += f"   • 🔮 Predicted Delivery: {po['predicted_delivery']}\n"
                
                if po.get("savings_opportunity"):
                    response += f"   • 💰 Savings Opportunity: {po['savings_opportunity']} MAD\n"
                
                response += "\n"
        
        # Add AI insights section
        if ai_insights:
            response += "\n💡 **AI Insights:**\n"
            for insight in ai_insights:
                response += f"• {insight.message}\n"
        
        return response

    # Additional helper methods for the advanced AI features...
    
    def get_available_procedures_enhanced(self) -> List[ProcedureInfo]:
        """Get enhanced list of available procedures with AI features"""
        procedures = []
        
        for proc_id, proc_data in self.procedures_data.items():
            ai_features = proc_data.get('ai_features', {})
            ai_feature_count = sum(1 for enabled in ai_features.values() if enabled)
            
            procedures.append(ProcedureInfo(
                procedure_id=proc_id,
                title=proc_data['title'],
                description=proc_data['description'],
                category=proc_data.get('category', 'general'),
                prerequisites=proc_data.get('prerequisites', []),
                estimated_time=proc_data.get('estimated_time'),
                difficulty=proc_data.get('difficulty')
            ))
        
        return procedures