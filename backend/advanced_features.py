"""
Advanced Features Module for Oracle EBS Assistant
Provides enhanced AI capabilities, analytics, and integrations
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid
import hashlib
from collections import defaultdict, deque

# Enhanced data structures
@dataclass
class UserSession:
    session_id: str
    user_id: Optional[str]
    start_time: datetime
    last_activity: datetime
    preferences: Dict[str, Any]
    interaction_history: List[Dict]
    performance_metrics: Dict[str, float]
    context_memory: Dict[str, Any]

@dataclass
class ProcedureAnalytics:
    procedure_id: str
    completion_rate: float
    average_duration: float
    common_issues: List[str]
    user_satisfaction: float
    optimization_suggestions: List[str]

@dataclass
class SmartRecommendation:
    type: str
    title: str
    description: str
    confidence: float
    priority: int
    context: Dict[str, Any]
    actions: List[str]

class RecommendationType(Enum):
    NEXT_STEP = "next_step"
    PROCESS_OPTIMIZATION = "process_optimization"
    ERROR_PREVENTION = "error_prevention"
    EFFICIENCY_IMPROVEMENT = "efficiency_improvement"
    COMPLIANCE_REMINDER = "compliance_reminder"

class AdvancedFeaturesManager:
    """Manages advanced AI features and analytics"""
    
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
        self.analytics_cache = {}
        self.recommendation_engine = RecommendationEngine()
        self.performance_monitor = PerformanceMonitor()
        self.context_analyzer = ContextAnalyzer()
        self.predictive_engine = PredictiveEngine()
        
    async def initialize(self):
        """Initialize advanced features"""
        await self.load_historical_data()
        await self.setup_analytics_pipeline()
        
    async def load_historical_data(self):
        """Load historical data for analytics"""
        pass
        
    async def setup_analytics_pipeline(self):
        """Setup analytics processing pipeline"""
        pass
        
    async def enhance_user_session(self, session_id: str, user_data: Dict) -> UserSession:
        """Create or enhance user session with advanced tracking"""
        if session_id not in self.sessions:
            self.sessions[session_id] = UserSession(
                session_id=session_id,
                user_id=user_data.get('user_id'),
                start_time=datetime.now(),
                last_activity=datetime.now(),
                preferences=user_data.get('preferences', {}),
                interaction_history=[],
                performance_metrics={},
                context_memory={}
            )
        
        session = self.sessions[session_id]
        session.last_activity = datetime.now()
        return session
        
    async def generate_smart_recommendations(self, session: UserSession, context: Dict) -> List[SmartRecommendation]:
        """Generate AI-powered recommendations"""
        recommendations = []
        
        # Analyze user behavior patterns
        behavior_analysis = await self.analyze_user_behavior(session)
        
        # Generate contextual recommendations
        if context.get('current_procedure'):
            recommendations.extend(
                await self.recommendation_engine.get_procedure_recommendations(
                    context['current_procedure'], behavior_analysis
                )
            )
        
        # Add efficiency recommendations
        recommendations.extend(
            await self.recommendation_engine.get_efficiency_recommendations(session)
        )
        
        # Add predictive recommendations
        try:
            predictions = await self.predictive_engine.predict_next_action(session)
            if predictions.get('action'):
                recommendations.append(SmartRecommendation(
                    type=RecommendationType.NEXT_STEP.value,
                    title=f"Suggested Next Action: {predictions['action']}",
                    description="Based on your activity pattern",
                    confidence=predictions.get('confidence', 0.5),
                    priority=1,
                    context=context,
                    actions=[predictions['action']]
                ))
        except Exception as e:
            print(f"Advanced features error: {e}")
        
        return sorted(recommendations, key=lambda x: (x.priority, -x.confidence))
    
    async def analyze_user_behavior(self, session: UserSession) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        history = session.interaction_history
        
        analysis = {
            'interaction_frequency': len(history),
            'preferred_procedures': self._get_preferred_procedures(history),
            'common_errors': self._identify_common_errors(history),
            'efficiency_score': self._calculate_efficiency_score(history),
            'learning_curve': self._analyze_learning_curve(history),
            'time_patterns': self._analyze_time_patterns(history)
        }
        
        return analysis
    
    async def get_predictive_insights(self, session: UserSession, context: Dict) -> Dict[str, Any]:
        """Generate predictive insights"""
        insights = {
            'next_likely_action': await self.predictive_engine.predict_next_action(session),
            'completion_probability': await self.predictive_engine.predict_completion_probability(session, context),
            'potential_issues': await self.predictive_engine.predict_potential_issues(session, context),
            'optimization_opportunities': await self.predictive_engine.identify_optimizations(session),
            'resource_requirements': await self.predictive_engine.predict_resource_needs(session, context)
        }
        
        return insights
    
    async def generate_analytics_dashboard(self, timeframe: str = '7d') -> Dict[str, Any]:
        """Generate comprehensive analytics dashboard"""
        end_date = datetime.now()
        start_date = end_date - self._parse_timeframe(timeframe)
        
        dashboard = {
            'overview': await self._get_overview_metrics(start_date, end_date),
            'procedure_analytics': await self._get_procedure_analytics(start_date, end_date),
            'user_engagement': await self._get_engagement_metrics(start_date, end_date),
            'performance_trends': await self._get_performance_trends(start_date, end_date),
            'system_health': await self._get_system_health_metrics(),
            'recommendations': await self._get_system_recommendations()
        }
        
        return dashboard
    
    def _get_preferred_procedures(self, history: List[Dict]) -> List[str]:
        """Identify user's preferred procedures"""
        procedure_counts = defaultdict(int)
        for interaction in history:
            if 'procedure' in interaction:
                procedure_counts[interaction['procedure']] += 1
        
        return sorted(procedure_counts.keys(), key=procedure_counts.get, reverse=True)[:5]
    
    def _identify_common_errors(self, history: List[Dict]) -> List[str]:
        """Identify common user errors"""
        errors = []
        for interaction in history:
            if interaction.get('type') == 'error':
                errors.append(interaction.get('error_type', 'unknown'))
        
        return list(set(errors))
    
    def _calculate_efficiency_score(self, history: List[Dict]) -> float:
        """Calculate user efficiency score"""
        if not history:
            return 0.0
        
        completed_procedures = sum(1 for h in history if h.get('status') == 'completed')
        total_procedures = sum(1 for h in history if 'procedure' in h)
        
        if total_procedures == 0:
            return 0.0
        
        return (completed_procedures / total_procedures) * 100
    
    def _analyze_learning_curve(self, history: List[Dict]) -> Dict[str, float]:
        """Analyze user learning progression"""
        if len(history) < 2:
            return {'trend': 0.0, 'improvement_rate': 0.0}
        
        # Calculate improvement over time
        recent_performance = self._calculate_recent_performance(history[-10:])
        early_performance = self._calculate_recent_performance(history[:10])
        
        improvement_rate = (recent_performance - early_performance) / max(early_performance, 1)
        
        return {
            'trend': improvement_rate,
            'improvement_rate': improvement_rate * 100,
            'current_level': recent_performance
        }
    
    def _analyze_time_patterns(self, history: List[Dict]) -> Dict[str, Any]:
        """Analyze user activity time patterns"""
        if not history:
            return {}
        
        hour_activity = defaultdict(int)
        day_activity = defaultdict(int)
        
        for interaction in history:
            if 'timestamp' in interaction:
                dt = datetime.fromisoformat(interaction['timestamp'])
                hour_activity[dt.hour] += 1
                day_activity[dt.strftime('%A')] += 1
        
        peak_hour = max(hour_activity.keys(), key=hour_activity.get) if hour_activity else 9
        peak_day = max(day_activity.keys(), key=day_activity.get) if day_activity else 'Monday'
        
        return {
            'peak_hour': peak_hour,
            'peak_day': peak_day,
            'activity_distribution': dict(hour_activity),
            'weekly_pattern': dict(day_activity)
        }
    
    def _parse_timeframe(self, timeframe: str) -> timedelta:
        """Parse timeframe string to timedelta"""
        if timeframe.endswith('d'):
            return timedelta(days=int(timeframe[:-1]))
        elif timeframe.endswith('w'):
            return timedelta(weeks=int(timeframe[:-1]))
        elif timeframe.endswith('m'):
            return timedelta(days=int(timeframe[:-1]) * 30)
        else:
            return timedelta(days=7)

class RecommendationEngine:
    """AI-powered recommendation engine"""
    
    def __init__(self):
        self.recommendation_rules = self._load_recommendation_rules()
        self.ml_models = {}  # Placeholder for ML models
    
    async def get_procedure_recommendations(self, procedure_id: str, behavior_analysis: Dict) -> List[SmartRecommendation]:
        """Get procedure-specific recommendations"""
        recommendations = []
        
        # Rule-based recommendations
        if behavior_analysis.get('efficiency_score', 0) < 70:
            recommendations.append(SmartRecommendation(
                type=RecommendationType.EFFICIENCY_IMPROVEMENT.value,
                title="Improve Procedure Efficiency",
                description="Consider using keyboard shortcuts and batch operations to speed up your workflow",
                confidence=0.8,
                priority=2,
                context={'procedure': procedure_id},
                actions=["Show keyboard shortcuts", "Enable batch mode"]
            ))
        
        # Context-aware recommendations
        if 'invoice' in procedure_id and behavior_analysis.get('common_errors'):
            recommendations.append(SmartRecommendation(
                type=RecommendationType.ERROR_PREVENTION.value,
                title="Prevent Common Invoice Errors",
                description="Use validation templates to avoid common invoice submission errors",
                confidence=0.9,
                priority=1,
                context={'procedure': procedure_id, 'errors': behavior_analysis['common_errors']},
                actions=["Load validation template", "Enable auto-check"]
            ))
        
        return recommendations
    
    async def get_efficiency_recommendations(self, session: UserSession) -> List[SmartRecommendation]:
        """Get efficiency improvement recommendations"""
        recommendations = []
        
        # Analyze session patterns
        if len(session.interaction_history) > 10:
            # Recommend workflow optimization
            recommendations.append(SmartRecommendation(
                type=RecommendationType.PROCESS_OPTIMIZATION.value,
                title="Optimize Your Workflow",
                description="Based on your usage patterns, consider grouping similar tasks together",
                confidence=0.7,
                priority=3,
                context={'session_id': session.session_id},
                actions=["Show workflow tips", "Create task groups"]
            ))
        
        return recommendations
    
    def _load_recommendation_rules(self) -> Dict:
        """Load recommendation rules"""
        return {
            'efficiency_thresholds': {
                'low': 50,
                'medium': 75,
                'high': 90
            },
            'error_patterns': {
                'validation_errors': ['missing_fields', 'invalid_format'],
                'process_errors': ['wrong_sequence', 'missing_prerequisites']
            }
        }

class PredictiveEngine:
    """Predictive analytics engine"""
    
    async def predict_next_action(self, session: UserSession) -> Dict[str, Any]:
        """Predict user's next likely action"""
        history = session.interaction_history
        
        if not history:
            return {'action': 'start_procedure', 'confidence': 0.5}
        
        # Simple pattern matching (in production, use ML models)
        last_actions = [h.get('action') for h in history[-5:]]
        
        # Pattern-based prediction
        if 'start_procedure' in last_actions and 'complete_step' not in last_actions:
            return {'action': 'continue_procedure', 'confidence': 0.8}
        elif 'view_data' in last_actions:
            return {'action': 'export_data', 'confidence': 0.6}
        else:
            return {'action': 'start_new_task', 'confidence': 0.4}
    
    async def predict_completion_probability(self, session: UserSession, context: Dict) -> float:
        """Predict probability of successful completion"""
        if not context.get('current_procedure'):
            return 0.5
        
        # Factors affecting completion probability
        factors = {
            'user_experience': self._calculate_experience_factor(session),
            'procedure_complexity': self._get_procedure_complexity(context['current_procedure']),
            'time_of_day': self._get_time_factor(),
            'session_duration': self._get_session_duration_factor(session)
        }
        
        # Weighted average (simplified model)
        weights = {'user_experience': 0.4, 'procedure_complexity': 0.3, 'time_of_day': 0.1, 'session_duration': 0.2}
        probability = sum(factors[k] * weights[k] for k in factors.keys())
        
        return min(max(probability, 0.0), 1.0)
    
    async def predict_potential_issues(self, session: UserSession, context: Dict) -> List[Dict[str, Any]]:
        """Predict potential issues user might encounter"""
        issues = []
        
        # Based on historical patterns
        common_errors = session.context_memory.get('common_errors', [])
        if common_errors:
            issues.append({
                'type': 'recurring_error',
                'description': f"You've encountered {common_errors[0]} before",
                'probability': 0.7,
                'prevention': "Double-check validation criteria"
            })
        
        # Time-based predictions
        current_hour = datetime.now().hour
        if current_hour > 17:  # After business hours
            issues.append({
                'type': 'system_performance',
                'description': "System may be slower during maintenance hours",
                'probability': 0.4,
                'prevention': "Consider completing critical tasks during business hours"
            })
        
        return issues
    
    async def identify_optimizations(self, session: UserSession) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        optimizations = []
        
        # Analyze interaction patterns
        history = session.interaction_history
        if len(history) > 5:
            # Check for repetitive actions
            action_counts = defaultdict(int)
            for interaction in history[-10:]:
                action_counts[interaction.get('action', 'unknown')] += 1
            
            repetitive_actions = [action for action, count in action_counts.items() if count > 3]
            
            if repetitive_actions:
                optimizations.append({
                    'type': 'automation',
                    'description': f"Consider automating repetitive {repetitive_actions[0]} actions",
                    'potential_savings': "30% time reduction",
                    'implementation': "Enable batch processing"
                })
        
        return optimizations
    
    async def predict_resource_needs(self, session: UserSession, context: Dict) -> Dict[str, Any]:
        """Predict resource requirements"""
        return {
            'estimated_time': self._estimate_completion_time(context),
            'required_documents': self._predict_required_documents(context),
            'system_resources': self._estimate_system_load(context),
            'support_likelihood': self._predict_support_need(session, context)
        }
    
    def _calculate_experience_factor(self, session: UserSession) -> float:
        """Calculate user experience factor"""
        total_interactions = len(session.interaction_history)
        if total_interactions < 5:
            return 0.3
        elif total_interactions < 20:
            return 0.6
        else:
            return 0.9
    
    def _get_procedure_complexity(self, procedure_id: str) -> float:
        """Get procedure complexity factor"""
        complexity_map = {
            'work_confirmation': 0.7,
            'invoice_submission': 0.8,
            'supplier_registration': 0.9,
            'goods_receipt_confirmation': 0.6,
            'vendor_performance_evaluation': 0.9
        }
        return complexity_map.get(procedure_id, 0.7)
    
    def _get_time_factor(self) -> float:
        """Get time-based performance factor"""
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:  # Business hours
            return 0.8
        else:
            return 0.6
    
    def _get_session_duration_factor(self, session: UserSession) -> float:
        """Get session duration factor"""
        duration = (datetime.now() - session.start_time).total_seconds() / 3600  # hours
        if duration < 0.5:
            return 0.9  # Fresh session
        elif duration < 2:
            return 0.8  # Normal session
        else:
            return 0.6  # Long session, potential fatigue

class PerformanceMonitor:
    """System performance monitoring"""
    
    def __init__(self):
        self.metrics = defaultdict(deque)
        self.alerts = []
    
    async def track_performance(self, metric_name: str, value: float):
        """Track performance metric"""
        self.metrics[metric_name].append({
            'timestamp': datetime.now(),
            'value': value
        })
        
        # Keep only recent metrics (last 1000 entries)
        if len(self.metrics[metric_name]) > 1000:
            self.metrics[metric_name].popleft()
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        summary = {}
        
        for metric_name, values in self.metrics.items():
            if values:
                recent_values = [v['value'] for v in list(values)[-100:]]  # Last 100 values
                summary[metric_name] = {
                    'current': recent_values[-1] if recent_values else 0,
                    'average': sum(recent_values) / len(recent_values),
                    'min': min(recent_values),
                    'max': max(recent_values),
                    'trend': self._calculate_trend(recent_values)
                }
        
        return summary
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction"""
        if len(values) < 2:
            return 'stable'
        
        recent_avg = sum(values[-10:]) / min(len(values), 10)
        older_avg = sum(values[-20:-10]) / min(len(values[:-10]), 10) if len(values) > 10 else recent_avg
        
        if recent_avg > older_avg * 1.05:
            return 'increasing'
        elif recent_avg < older_avg * 0.95:
            return 'decreasing'
        else:
            return 'stable'

class ContextAnalyzer:
    """Advanced context analysis"""
    
    async def analyze_conversation_context(self, messages: List[Dict]) -> Dict[str, Any]:
        """Analyze conversation context"""
        context = {
            'topics': self._extract_topics(messages),
            'sentiment': self._analyze_sentiment(messages),
            'complexity': self._assess_complexity(messages),
            'user_intent': self._determine_intent(messages),
            'knowledge_gaps': self._identify_knowledge_gaps(messages)
        }
        
        return context
    
    def _extract_topics(self, messages: List[Dict]) -> List[str]:
        """Extract main topics from conversation"""
        # Simplified topic extraction
        topics = set()
        keywords = ['invoice', 'purchase order', 'supplier', 'contract', 'payment', 'quality', 'confirmation']
        
        for message in messages:
            content = message.get('content', '').lower()
            for keyword in keywords:
                if keyword in content:
                    topics.add(keyword)
        
        return list(topics)
    
    def _analyze_sentiment(self, messages: List[Dict]) -> Dict[str, float]:
        """Analyze conversation sentiment"""
        # Simplified sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'perfect', 'thanks', 'helpful']
        negative_words = ['problem', 'issue', 'error', 'difficult', 'confused', 'stuck']
        
        positive_count = 0
        negative_count = 0
        total_words = 0
        
        for message in messages:
            if message.get('type') == 'user':
                content = message.get('content', '').lower()
                words = content.split()
                total_words += len(words)
                
                positive_count += sum(1 for word in words if word in positive_words)
                negative_count += sum(1 for word in words if word in negative_words)
        
        if total_words == 0:
            return {'positive': 0.5, 'negative': 0.5, 'neutral': 0.0}
        
        positive_ratio = positive_count / total_words
        negative_ratio = negative_count / total_words
        neutral_ratio = 1 - positive_ratio - negative_ratio
        
        return {
            'positive': positive_ratio,
            'negative': negative_ratio,
            'neutral': neutral_ratio
        }
    
    def _assess_complexity(self, messages: List[Dict]) -> float:
        """Assess conversation complexity"""
        if not messages:
            return 0.0
        
        # Factors: message length, technical terms, question complexity
        total_complexity = 0
        message_count = 0
        
        technical_terms = ['oracle', 'ebs', 'supplier', 'procurement', 'invoice', 'po', 'rfq']
        
        for message in messages:
            if message.get('type') == 'user':
                content = message.get('content', '')
                
                # Length factor
                length_factor = min(len(content) / 100, 1.0)
                
                # Technical terms factor
                tech_count = sum(1 for term in technical_terms if term in content.lower())
                tech_factor = min(tech_count / 3, 1.0)
                
                # Question complexity (number of questions)
                question_factor = min(content.count('?') / 2, 1.0)
                
                complexity = (length_factor + tech_factor + question_factor) / 3
                total_complexity += complexity
                message_count += 1
        
        return total_complexity / message_count if message_count > 0 else 0.0
    
    def _determine_intent(self, messages: List[Dict]) -> str:
        """Determine primary user intent"""
        if not messages:
            return 'unknown'
        
        recent_messages = messages[-3:]  # Look at last 3 messages
        
        intent_keywords = {
            'help': ['help', 'how', 'what', 'explain'],
            'action': ['start', 'create', 'submit', 'complete'],
            'information': ['show', 'view', 'list', 'search', 'find'],
            'problem': ['error', 'issue', 'problem', 'stuck', 'not working']
        }
        
        intent_scores = defaultdict(int)
        
        for message in recent_messages:
            if message.get('type') == 'user':
                content = message.get('content', '').lower()
                for intent, keywords in intent_keywords.items():
                    for keyword in keywords:
                        if keyword in content:
                            intent_scores[intent] += 1
        
        return max(intent_scores.keys(), key=intent_scores.get) if intent_scores else 'unknown'
    
    def _identify_knowledge_gaps(self, messages: List[Dict]) -> List[str]:
        """Identify user knowledge gaps"""
        gaps = []
        
        confusion_indicators = ['confused', 'don\'t understand', 'what does', 'how do i', 'not sure']
        
        for message in messages:
            if message.get('type') == 'user':
                content = message.get('content', '').lower()
                for indicator in confusion_indicators:
                    if indicator in content:
                        # Extract the topic they're confused about
                        if 'oracle' in content:
                            gaps.append('oracle_ebs_basics')
                        elif 'invoice' in content:
                            gaps.append('invoice_process')
                        elif 'supplier' in content:
                            gaps.append('supplier_management')
                        else:
                            gaps.append('general_process')
                        break
        
        return list(set(gaps))  # Remove duplicates
        
    async def _get_overview_metrics(self, start_date, end_date):
        return {'total_sessions': 0, 'active_users': 0, 'procedures_completed': 0}
        
    async def _get_procedure_analytics(self, start_date, end_date):
        return {'most_used': [], 'completion_rates': {}}
        
    async def _get_engagement_metrics(self, start_date, end_date):
        return {'avg_session_duration': 0, 'user_satisfaction': 0}
        
    async def _get_performance_trends(self, start_date, end_date):
        return {'response_time': [], 'error_rate': []}
        
    async def _get_system_health_metrics(self):
        return {'status': 'healthy', 'uptime': '99.9%'}
        
    async def _get_system_recommendations(self):
        return []
        
    def _calculate_recent_performance(self, history):
        if not history:
            return 0.0
        completed = sum(1 for h in history if h.get('status') == 'completed')
        return (completed / len(history)) * 100 if history else 0.0
        
    def _estimate_completion_time(self, context):
        procedure = context.get('current_procedure', '')
        time_estimates = {
            'work_confirmation': '15-20 minutes',
            'invoice_submission': '10-15 minutes'
        }
        return time_estimates.get(procedure, '10-30 minutes')
    
    def _predict_required_documents(self, context):
        procedure = context.get('current_procedure', '')
        if 'invoice' in procedure:
            return ['Invoice copy', 'Delivery receipt']
        return []
    
    def _estimate_system_load(self, context):
        return 'Normal'
    
    def _predict_support_need(self, session, context):
        return 0.2