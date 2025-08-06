class AdvancedOracleEBSAssistant {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.apiBaseUrl = 'http://localhost:8000/api';
        this.currentProcedure = null;
        this.currentStep = null;
        this.isLoading = false;
        this.aiFeatures = {
            voiceInput: false,
            smartSuggestions: true,
            predictiveText: true,
            autoComplete: true,
            realTimeValidation: true,
            contextAwareness: true,
            personalizedRecommendations: true,
            smartNotifications: true
        };
        this.userPreferences = this.loadUserPreferences();
        this.conversationContext = [];
        this.aiInsights = [];
        this.performanceMetrics = {
            responseTime: [],
            userSatisfaction: [],
            taskCompletion: []
        };
        
        this.initializeElements();
        this.bindEvents();
        this.initializeAIFeatures();
        this.loadInitialData();
    }
    
    generateSessionId() {
        return 'ai_session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    initializeElements() {
        // Chat elements
        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        this.suggestionsContainer = document.getElementById('suggestions-container');
        this.suggestions = document.getElementById('suggestions');
        
        // AI-enhanced elements
        this.voiceBtn = this.createVoiceButton();
        this.aiInsightsPanel = this.createAIInsightsPanel();
        this.smartSuggestionsPanel = this.createSmartSuggestionsPanel();
        this.contextPanel = this.createContextPanel();
        this.performancePanel = this.createPerformancePanel();
        
        // Sidebar elements
        this.sidebar = document.getElementById('sidebar');
        this.sessionIdDisplay = document.getElementById('session-id-display');
        this.sessionStatus = document.getElementById('session-status');
        this.currentProcedureEl = document.getElementById('current-procedure');
        this.procedureProgress = document.getElementById('procedure-progress');
        this.procedureTitle = document.getElementById('procedure-title');
        this.stepCounter = document.getElementById('step-counter');
        this.progressFill = document.getElementById('progress-fill');
        this.completedSteps = document.getElementById('completed-steps');
        this.proceduresList = document.getElementById('procedures-list');
        
        // Modal elements
        this.screenshotModal = document.getElementById('screenshot-modal');
        this.screenshotImage = document.getElementById('screenshot-image');
        this.screenshotCaption = document.getElementById('screenshot-caption');
        
        // Overlay elements
        this.loadingOverlay = document.getElementById('loading-overlay');
        this.toastContainer = document.getElementById('toast-container');
        
        // Header buttons
        this.progressBtn = document.getElementById('progress-btn');
        this.proceduresBtn = document.getElementById('procedures-btn');
        this.resetBtn = document.getElementById('reset-btn');
        this.closeSidebarBtn = document.getElementById('close-sidebar');
        
        // AI feature buttons
        this.aiToggleBtn = this.createAIToggleButton();
        this.insightsBtn = this.createInsightsButton();
        this.optimizeBtn = this.createOptimizeButton();
        
        // Set session ID display
        this.sessionIdDisplay.textContent = this.sessionId;
    }
    
    createVoiceButton() {
        const voiceBtn = document.createElement('button');
        voiceBtn.className = 'voice-btn';
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceBtn.title = 'Voice Input (AI-Powered)';
        voiceBtn.addEventListener('click', () => this.toggleVoiceInput());
        
        const inputWrapper = document.querySelector('.input-wrapper');
        inputWrapper.appendChild(voiceBtn);
        
        return voiceBtn;
    }
    
    createAIInsightsPanel() {
        const panel = document.createElement('div');
        panel.className = 'ai-insights-panel';
        panel.innerHTML = `
            <div class="panel-header">
                <h4><i class="fas fa-brain"></i> AI Insights</h4>
                <button class="toggle-panel" onclick="app.togglePanel('insights')">
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>
            <div class="panel-content" id="ai-insights-content">
                <div class="no-insights">No insights available yet</div>
            </div>
        `;
        
        this.sidebar.appendChild(panel);
        return panel;
    }
    
    createSmartSuggestionsPanel() {
        const panel = document.createElement('div');
        panel.className = 'smart-suggestions-panel';
        panel.innerHTML = `
            <div class="panel-header">
                <h4><i class="fas fa-lightbulb"></i> Smart Suggestions</h4>
                <button class="toggle-panel" onclick="app.togglePanel('suggestions')">
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>
            <div class="panel-content" id="smart-suggestions-content">
                <div class="suggestion-item" onclick="app.applySuggestion('optimize_workflow')">
                    <i class="fas fa-rocket"></i>
                    <span>Optimize current workflow</span>
                </div>
                <div class="suggestion-item" onclick="app.applySuggestion('predict_completion')">
                    <i class="fas fa-clock"></i>
                    <span>Predict completion time</span>
                </div>
                <div class="suggestion-item" onclick="app.applySuggestion('check_risks')">
                    <i class="fas fa-shield-alt"></i>
                    <span>Check for risks</span>
                </div>
            </div>
        `;
        
        this.sidebar.appendChild(panel);
        return panel;
    }
    
    createContextPanel() {
        const panel = document.createElement('div');
        panel.className = 'context-panel';
        panel.innerHTML = `
            <div class="panel-header">
                <h4><i class="fas fa-layer-group"></i> Context Awareness</h4>
                <button class="toggle-panel" onclick="app.togglePanel('context')">
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>
            <div class="panel-content" id="context-content">
                <div class="context-item">
                    <label>User Experience:</label>
                    <span id="user-experience">Analyzing...</span>
                </div>
                <div class="context-item">
                    <label>Session Focus:</label>
                    <span id="session-focus">Exploration</span>
                </div>
                <div class="context-item">
                    <label>Interaction Pattern:</label>
                    <span id="interaction-pattern">Learning</span>
                </div>
                <div class="context-item">
                    <label>Predicted Next Action:</label>
                    <span id="predicted-action">Start procedure</span>
                </div>
            </div>
        `;
        
        this.sidebar.appendChild(panel);
        return panel;
    }
    
    createPerformancePanel() {
        const panel = document.createElement('div');
        panel.className = 'performance-panel';
        panel.innerHTML = `
            <div class="panel-header">
                <h4><i class="fas fa-chart-line"></i> Performance Metrics</h4>
                <button class="toggle-panel" onclick="app.togglePanel('performance')">
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>
            <div class="panel-content" id="performance-content">
                <div class="metric-item">
                    <label>Avg Response Time:</label>
                    <span id="avg-response-time">-- ms</span>
                </div>
                <div class="metric-item">
                    <label>Task Completion:</label>
                    <span id="task-completion">--%</span>
                </div>
                <div class="metric-item">
                    <label>AI Accuracy:</label>
                    <span id="ai-accuracy">--%</span>
                </div>
                <div class="metric-item">
                    <label>User Satisfaction:</label>
                    <span id="user-satisfaction">
                        <div class="rating-stars" id="satisfaction-stars"></div>
                    </span>
                </div>
            </div>
        `;
        
        this.sidebar.appendChild(panel);
        return panel;
    }
    
    createAIToggleButton() {
        const btn = document.createElement('button');
        btn.className = 'header-btn ai-toggle-btn';
        btn.innerHTML = '<i class="fas fa-robot"></i>';
        btn.title = 'AI Features';
        btn.addEventListener('click', () => this.toggleAIFeatures());
        
        document.querySelector('.header-actions').appendChild(btn);
        return btn;
    }
    
    createInsightsButton() {
        const btn = document.createElement('button');
        btn.className = 'header-btn insights-btn';
        btn.innerHTML = '<i class="fas fa-brain"></i>';
        btn.title = 'AI Insights';
        btn.addEventListener('click', () => this.showAIInsights());
        
        document.querySelector('.header-actions').appendChild(btn);
        return btn;
    }
    
    createOptimizeButton() {
        const btn = document.createElement('button');
        btn.className = 'header-btn optimize-btn';
        btn.innerHTML = '<i class="fas fa-magic"></i>';
        btn.title = 'AI Optimization';
        btn.addEventListener('click', () => this.requestOptimization());
        
        document.querySelector('.header-actions').appendChild(btn);
        return btn;
    }
    
    bindEvents() {
        // Enhanced input events with AI features
        this.messageInput.addEventListener('input', (e) => {
            this.handleInputChange(e);
            if (this.aiFeatures.predictiveText) {
                this.showPredictiveText(e.target.value);
            }
            if (this.aiFeatures.realTimeValidation) {
                this.validateInput(e.target.value);
            }
        });
        
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Header button events
        this.progressBtn.addEventListener('click', () => this.toggleSidebar());
        this.proceduresBtn.addEventListener('click', () => this.toggleSidebar());
        this.resetBtn.addEventListener('click', () => this.resetSession());
        this.closeSidebarBtn.addEventListener('click', () => this.closeSidebar());
        
        // Modal events
        this.screenshotModal.addEventListener('click', (e) => {
            if (e.target === this.screenshotModal) {
                this.closeScreenshotModal();
            }
        });
        
        // AI-enhanced keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeScreenshotModal();
                this.closeSidebar();
            }
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                this.focusSearchInput();
            }
            if (e.ctrlKey && e.key === 'i') {
                e.preventDefault();
                this.showAIInsights();
            }
        });
        
        // Context awareness - track user interactions
        document.addEventListener('click', (e) => {
            this.trackUserInteraction('click', e.target);
        });
        
        // Performance monitoring
        this.startPerformanceMonitoring();
    }
    
    initializeAIFeatures() {
        // Initialize speech recognition if available
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            this.initializeSpeechRecognition();
        }
        
        // Initialize predictive text service
        if (this.aiFeatures.predictiveText) {
            this.initializePredictiveText();
        }
        
        // Initialize context awareness
        if (this.aiFeatures.contextAwareness) {
            this.initializeContextAwareness();
        }
        
        // Initialize smart notifications
        if (this.aiFeatures.smartNotifications) {
            this.initializeSmartNotifications();
        }
        
        // Initialize auto-completion
        if (this.aiFeatures.autoComplete) {
            this.initializeAutoCompletion();
        }
    }
    
    initializeSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            this.speechRecognition = new SpeechRecognition();
            this.speechRecognition.continuous = false;
            this.speechRecognition.interimResults = true;
            this.speechRecognition.lang = 'en-US';
            
            this.speechRecognition.onstart = () => {
                this.voiceBtn.classList.add('recording');
                this.showToast('Listening...', 'info');
            };
            
            this.speechRecognition.onresult = (event) => {
                const result = event.results[event.results.length - 1];
                if (result.isFinal) {
                    this.messageInput.value = result[0].transcript;
                    this.handleInputChange({ target: this.messageInput });
                }
            };
            
            this.speechRecognition.onend = () => {
                this.voiceBtn.classList.remove('recording');
            };
            
            this.speechRecognition.onerror = (event) => {
                this.voiceBtn.classList.remove('recording');
                this.showToast('Voice recognition error', 'error');
            };
        }
    }
    
    initializePredictiveText() {
        this.predictiveTextCache = new Map();
        this.commonPhrases = [
            'start work confirmation',
            'show purchase orders',
            'list invoices',
            'help me with',
            'check payment status',
            'create new supplier',
            'optimize workflow',
            'analyze spending',
            'predict delivery time',
            'assess supplier risk'
        ];
    }
    
    initializeContextAwareness() {
        this.contextData = {
            userExperience: 'novice',
            sessionFocus: 'exploration',
            interactionPattern: 'learning',
            predictedNextAction: 'start_procedure'
        };
        
        this.updateContextDisplay();
    }
    
    initializeSmartNotifications() {
        // Request notification permission
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
        
        this.notificationQueue = [];
        this.setupSmartNotifications();
    }
    
    initializeAutoCompletion() {
        this.autoCompleteData = [
            { text: 'start work confirmation', category: 'procedures' },
            { text: 'show purchase orders', category: 'queries' },
            { text: 'list invoices', category: 'queries' },
            { text: 'register new supplier', category: 'procedures' },
            { text: 'check payment status', category: 'queries' },
            { text: 'optimize current process', category: 'ai_features' },
            { text: 'predict completion time', category: 'ai_features' },
            { text: 'analyze supplier performance', category: 'analytics' }
        ];
        
        this.createAutoCompleteDropdown();
    }
    
    async loadInitialData() {
        try {
            await this.loadProcedures();
            this.showInitialSuggestions();
            this.startAIAnalysis();
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showToast('Error loading application data', 'error');
        }
    }
    
    async loadProcedures() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/procedures`);
            const data = await response.json();
            
            this.renderProceduresEnhanced(data.procedures);
        } catch (error) {
            console.error('Error loading procedures:', error);
            this.proceduresList.innerHTML = '<div class="error">Failed to load procedures</div>';
        }
    }
    
    renderProceduresEnhanced(procedures) {
        if (!procedures || procedures.length === 0) {
            this.proceduresList.innerHTML = '<div class="no-procedures">No procedures available</div>';
            return;
        }
        
        this.proceduresList.innerHTML = procedures.map(proc => {
            const aiFeatures = proc.ai_features || {};
            const featureCount = Object.values(aiFeatures).filter(Boolean).length;
            
            return `
                <div class="procedure-item enhanced" onclick="app.startProcedure('${proc.procedure_id}')">
                    <div class="procedure-header">
                        <h5>${proc.title}</h5>
                        <div class="procedure-badges">
                            <span class="difficulty-badge ${proc.difficulty || 'intermediate'}">${proc.difficulty || 'Intermediate'}</span>
                            ${featureCount > 0 ? `<span class="ai-badge"><i class="fas fa-robot"></i> ${featureCount} AI</span>` : ''}
                        </div>
                    </div>
                    <p>${proc.description}</p>
                    <div class="procedure-meta">
                        <span class="category">${proc.category}</span>
                        <span class="time">${proc.estimated_time || 'Variable'}</span>
                    </div>
                    ${featureCount > 0 ? this.renderAIFeaturesList(aiFeatures) : ''}
                </div>
            `;
        }).join('');
    }
    
    renderAIFeaturesList(aiFeatures) {
        const enabledFeatures = Object.entries(aiFeatures)
            .filter(([key, value]) => value)
            .map(([key, value]) => key.replace(/_/g, ' ').toUpperCase());
        
        if (enabledFeatures.length === 0) return '';
        
        return `
            <div class="ai-features-list">
                <small>AI Features: ${enabledFeatures.slice(0, 3).join(', ')}${enabledFeatures.length > 3 ? '...' : ''}</small>
            </div>
        `;
    }
    
    showInitialSuggestions() {
        const initialSuggestions = [
            'Start work confirmation',
            'Show purchase orders',
            'Optimize my workflow',
            'Predict delivery times',
            'Help'
        ];
        
        this.renderSuggestions(initialSuggestions);
    }
    
    async sendMessage(message = null) {
        const text = message || this.messageInput.value.trim();
        if (!text || this.isLoading) return;
        
        const startTime = performance.now();
        
        // Clear input and disable send button
        this.messageInput.value = '';
        this.sendBtn.disabled = true;
        
        // Add to conversation context
        this.conversationContext.push({
            type: 'user',
            message: text,
            timestamp: new Date().toISOString()
        });
        
        // Add user message to chat
        this.addMessage(text, 'user');
        
        // Show loading with AI indication
        this.setLoading(true, 'AI is processing your request...');
        
        try {
            // Enhanced API call with AI context
            const response = await fetch(`${this.apiBaseUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: text,
                    session_id: this.sessionId,
                    context: {
                        conversation_history: this.conversationContext.slice(-5),
                        user_preferences: this.userPreferences,
                        ai_features_enabled: this.aiFeatures,
                        context_data: this.contextData
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            const endTime = performance.now();
            const responseTime = endTime - startTime;
            
            // Track performance
            this.trackPerformance('response_time', responseTime);
            
            // Add to conversation context
            this.conversationContext.push({
                type: 'assistant',
                message: data.message,
                timestamp: new Date().toISOString(),
                ai_insights: data.ai_insights || []
            });
            
            // Add enhanced assistant response
            this.addMessageEnhanced(data.message, data.message_type || 'assistant', data);
            
            // Update session state
            this.updateSessionState(data.session_state);
            
            // Update current step if provided
            if (data.current_step) {
                this.updateCurrentStep(data.current_step);
            }
            
            // Show AI-enhanced suggestions
            if (data.suggestions) {
                this.renderSuggestionsEnhanced(data.suggestions, data.ai_insights);
            }
            
            // Process AI insights
            if (data.ai_insights) {
                this.processAIInsights(data.ai_insights);
            }
            
            // Update context awareness
            this.updateContextAwareness(data);
            
            // Show validation errors if any
            if (data.validation_errors && data.validation_errors.length > 0) {
                this.showSmartNotification('Please complete all requirements before proceeding', 'warning', data.validation_errors);
            }
            
            // Auto-save important information
            this.autoSaveImportantData(data);
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('Sorry, I encountered an error. AI is analyzing the issue...', 'error');
            this.showSmartNotification('Connection error detected. AI suggests checking your network.', 'error');
            this.trackPerformance('error_rate', 1);
        } finally {
            this.setLoading(false);
        }
    }
    
    addMessageEnhanced(content, type, data = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type} enhanced`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = this.formatMessageEnhanced(content, data);
        
        messageContent.appendChild(messageText);
        
        // Add AI insights panel if available
        if (data && data.ai_insights && data.ai_insights.length > 0) {
            const insightsPanel = this.createMessageInsightsPanel(data.ai_insights);
            messageContent.appendChild(insightsPanel);
        }
        
        // Add enhanced action buttons
        if (data) {
            const actionsDiv = this.createEnhancedActions(data);
            if (actionsDiv) {
                messageContent.appendChild(actionsDiv);
            }
        }
        
        // Add AI confidence indicator
        if (data && data.ai_confidence) {
            const confidenceIndicator = this.createConfidenceIndicator(data.ai_confidence);
            messageContent.appendChild(confidenceIndicator);
        }
        
        // Add timestamp with AI response time
        const timestamp = document.createElement('div');
        timestamp.className = 'timestamp enhanced';
        const responseTime = data && data.response_time ? ` (${data.response_time}ms)` : '';
        timestamp.textContent = new Date().toLocaleTimeString() + responseTime;
        messageContent.appendChild(timestamp);
        
        messageDiv.appendChild(messageContent);
        
        // Remove welcome message if it exists
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Apply AI enhancements
        this.applyMessageEnhancements(messageDiv, data);
    }
    
    formatMessageEnhanced(content, data) {
        let formatted = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/^• (.+)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
        
        // Add AI enhancement indicators
        if (data && data.ai_enhanced) {
            formatted = `<div class="ai-enhanced-content">${formatted}</div>`;
        }
        
        return formatted;
    }
    
    createMessageInsightsPanel(insights) {
        const panel = document.createElement('div');
        panel.className = 'message-insights-panel';
        
        const header = document.createElement('div');
        header.className = 'insights-header';
        header.innerHTML = '<i class="fas fa-brain"></i> AI Insights';
        
        const content = document.createElement('div');
        content.className = 'insights-content';
        
        insights.forEach(insight => {
            const insightDiv = document.createElement('div');
            insightDiv.className = `insight-item ${insight.priority}`;
            insightDiv.innerHTML = `
                <div class="insight-type">${insight.type.replace('_', ' ').toUpperCase()}</div>
                <div class="insight-message">${insight.message}</div>
                <div class="insight-confidence">Confidence: ${(insight.confidence * 100).toFixed(0)}%</div>
            `;
            content.appendChild(insightDiv);
        });
        
        panel.appendChild(header);
        panel.appendChild(content);
        
        return panel;
    }
    
    createEnhancedActions(data) {
        const actionsDiv = document.createElement('div');
        actionsDiv.className = 'message-actions enhanced';
        
        // Screenshot button
        if (data.screenshot) {
            const screenshotBtn = document.createElement('button');
            screenshotBtn.className = 'action-btn screenshot-btn';
            screenshotBtn.innerHTML = '<i class="fas fa-image"></i> View Screenshot';
            screenshotBtn.onclick = () => this.showScreenshot(data.screenshot, data.current_step?.title || 'Step Screenshot');
            actionsDiv.appendChild(screenshotBtn);
        }
        
        // AI optimization button
        if (data.optimization_available) {
            const optimizeBtn = document.createElement('button');
            optimizeBtn.className = 'action-btn optimize-btn';
            optimizeBtn.innerHTML = '<i class="fas fa-magic"></i> AI Optimize';
            optimizeBtn.onclick = () => this.requestOptimization();
            actionsDiv.appendChild(optimizeBtn);
        }
        
        // Prediction button
        if (data.prediction_available) {
            const predictBtn = document.createElement('button');
            predictBtn.className = 'action-btn predict-btn';
            predictBtn.innerHTML = '<i class="fas fa-crystal-ball"></i> Predict Outcome';
            predictBtn.onclick = () => this.requestPrediction();
            actionsDiv.appendChild(predictBtn);
        }
        
        // Export data button
        if (data.oracle_data) {
            const exportBtn = document.createElement('button');
            exportBtn.className = 'action-btn export-btn';
            exportBtn.innerHTML = '<i class="fas fa-download"></i> Export Data';
            exportBtn.onclick = () => this.exportData(data.oracle_data);
            actionsDiv.appendChild(exportBtn);
        }
        
        return actionsDiv.children.length > 0 ? actionsDiv : null;
    }
    
    createConfidenceIndicator(confidence) {
        const indicator = document.createElement('div');
        indicator.className = 'confidence-indicator';
        
        const level = confidence > 0.8 ? 'high' : confidence > 0.6 ? 'medium' : 'low';
        const percentage = Math.round(confidence * 100);
        
        indicator.innerHTML = `
            <div class="confidence-bar ${level}">
                <div class="confidence-fill" style="width: ${percentage}%"></div>
            </div>
            <span class="confidence-text">AI Confidence: ${percentage}%</span>
        `;
        
        return indicator;
    }
    
    applyMessageEnhancements(messageDiv, data) {
        // Add hover effects for AI-enhanced messages
        if (data && data.ai_enhanced) {
            messageDiv.addEventListener('mouseenter', () => {
                this.showQuickInsights(messageDiv, data);
            });
        }
        
        // Add click-to-expand for complex data
        if (data && data.oracle_data && data.oracle_data.length > 3) {
            const expandBtn = document.createElement('button');
            expandBtn.className = 'expand-data-btn';
            expandBtn.textContent = 'Show More';
            expandBtn.onclick = () => this.expandOracleData(data.oracle_data);
            messageDiv.querySelector('.message-content').appendChild(expandBtn);
        }
    }
    
    // AI Feature Methods
    
    toggleVoiceInput() {
        if (this.speechRecognition) {
            if (this.voiceBtn.classList.contains('recording')) {
                this.speechRecognition.stop();
            } else {
                this.speechRecognition.start();
            }
        } else {
            this.showToast('Voice input not supported in this browser', 'warning');
        }
    }
    
    handleInputChange(e) {
        const value = e.target.value;
        this.sendBtn.disabled = !value.trim();
        
        // Update typing indicators
        if (value.length > 0) {
            this.showTypingIndicator();
        } else {
            this.hideTypingIndicator();
        }
        
        // Analyze user input patterns
        this.analyzeInputPattern(value);
    }
    
    showPredictiveText(input) {
        if (input.length < 2) {
            this.hidePredictiveText();
            return;
        }
        
        const predictions = this.generatePredictions(input);
        if (predictions.length > 0) {
            this.displayPredictiveText(predictions);
        }
    }
    
    generatePredictions(input) {
        const inputLower = input.toLowerCase();
        
        // Check cache first
        if (this.predictiveTextCache.has(inputLower)) {
            return this.predictiveTextCache.get(inputLower);
        }
        
        // Generate predictions based on common phrases and context
        const predictions = this.commonPhrases
            .filter(phrase => phrase.toLowerCase().startsWith(inputLower))
            .slice(0, 5)
            .map(phrase => ({
                text: phrase,
                confidence: this.calculatePredictionConfidence(input, phrase),
                type: this.categorizePrediction(phrase)
            }))
            .sort((a, b) => b.confidence - a.confidence);
        
        // Cache the result
        this.predictiveTextCache.set(inputLower, predictions);
        
        return predictions;
    }
    
    calculatePredictionConfidence(input, prediction) {
        const inputWords = input.toLowerCase().split(' ');
        const predictionWords = prediction.toLowerCase().split(' ');
        
        let matches = 0;
        inputWords.forEach(word => {
            if (predictionWords.some(pWord => pWord.startsWith(word))) {
                matches++;
            }
        });
        
        return matches / Math.max(inputWords.length, predictionWords.length);
    }
    
    categorizePrediction(prediction) {
        if (prediction.includes('start') || prediction.includes('create')) return 'action';
        if (prediction.includes('show') || prediction.includes('list')) return 'query';
        if (prediction.includes('help')) return 'assistance';
        return 'general';
    }
    
    displayPredictiveText(predictions) {
        let dropdown = document.getElementById('predictive-dropdown');
        if (!dropdown) {
            dropdown = document.createElement('div');
            dropdown.id = 'predictive-dropdown';
            dropdown.className = 'predictive-dropdown';
            this.messageInput.parentNode.appendChild(dropdown);
        }
        
        dropdown.innerHTML = predictions.map(pred => `
            <div class="prediction-item ${pred.type}" onclick="app.selectPrediction('${pred.text}')">
                <span class="prediction-text">${pred.text}</span>
                <span class="prediction-confidence">${Math.round(pred.confidence * 100)}%</span>
            </div>
        `).join('');
        
        dropdown.style.display = 'block';
    }
    
    selectPrediction(text) {
        this.messageInput.value = text;
        this.hidePredictiveText();
        this.handleInputChange({ target: this.messageInput });
        this.messageInput.focus();
    }
    
    hidePredictiveText() {
        const dropdown = document.getElementById('predictive-dropdown');
        if (dropdown) {
            dropdown.style.display = 'none';
        }
    }
    
    validateInput(input) {
        const validationResult = this.performInputValidation(input);
        this.displayValidationFeedback(validationResult);
    }
    
    performInputValidation(input) {
        const result = {
            isValid: true,
            issues: [],
            suggestions: []
        };
        
        // Check for common issues
        if (input.includes('PO-') && !/PO-\d{4}-\d{3}/.test(input)) {
            result.issues.push('Invalid PO number format');
            result.suggestions.push('Use format: PO-YYYY-NNN');
        }
        
        if (input.includes('INV-') && !/INV-\d{4}-\d{3}/.test(input)) {
            result.issues.push('Invalid invoice number format');
            result.suggestions.push('Use format: INV-YYYY-NNN');
        }
        
        // Check for unclear requests
        if (input.length > 10 && !this.containsActionWord(input)) {
            result.suggestions.push('Try starting with an action word like "show", "create", or "help"');
        }
        
        result.isValid = result.issues.length === 0;
        return result;
    }
    
    containsActionWord(input) {
        const actionWords = ['show', 'create', 'start', 'list', 'help', 'find', 'search', 'analyze', 'predict'];
        return actionWords.some(word => input.toLowerCase().includes(word));
    }
    
    displayValidationFeedback(result) {
        let feedback = document.getElementById('validation-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.id = 'validation-feedback';
            feedback.className = 'validation-feedback';
            this.messageInput.parentNode.appendChild(feedback);
        }
        
        if (result.issues.length > 0 || result.suggestions.length > 0) {
            feedback.innerHTML = `
                ${result.issues.map(issue => `<div class="validation-issue">${issue}</div>`).join('')}
                ${result.suggestions.map(suggestion => `<div class="validation-suggestion">${suggestion}</div>`).join('')}
            `;
            feedback.style.display = 'block';
        } else {
            feedback.style.display = 'none';
        }
    }
    
    // Context and Performance Methods
    
    updateContextAwareness(responseData) {
        // Analyze user behavior patterns
        const behavior = this.analyzeUserBehavior();
        
        // Update context data
        this.contextData = {
            userExperience: this.inferUserExperience(),
            sessionFocus: this.determineSessionFocus(),
            interactionPattern: behavior.pattern,
            predictedNextAction: this.predictNextAction(responseData)
        };
        
        this.updateContextDisplay();
    }
    
    analyzeUserBehavior() {
        const recentInteractions = this.conversationContext.slice(-10);
        
        let queryCount = 0;
        let procedureCount = 0;
        let helpCount = 0;
        
        recentInteractions.forEach(interaction => {
            if (interaction.type === 'user') {
                const message = interaction.message.toLowerCase();
                if (message.includes('show') || message.includes('list')) queryCount++;
                if (message.includes('start') || message.includes('create')) procedureCount++;
                if (message.includes('help')) helpCount++;
            }
        });
        
        let pattern = 'exploratory';
        if (procedureCount > queryCount && procedureCount > helpCount) {
            pattern = 'task_focused';
        } else if (helpCount > 0) {
            pattern = 'learning';
        }
        
        return { pattern, queryCount, procedureCount, helpCount };
    }
    
    inferUserExperience() {
        const totalInteractions = this.conversationContext.length;
        const errorRate = this.calculateErrorRate();
        
        if (totalInteractions < 10 || errorRate > 0.3) {
            return 'novice';
        } else if (totalInteractions < 50 || errorRate > 0.1) {
            return 'intermediate';
        } else {
            return 'expert';
        }
    }
    
    determineSessionFocus() {
        if (this.currentProcedure) {
            return 'procedure_execution';
        } else if (this.conversationContext.some(c => c.message.includes('analyze') || c.message.includes('predict'))) {
            return 'analytics';
        } else {
            return 'exploration';
        }
    }
    
    predictNextAction(responseData) {
        if (this.currentProcedure && this.currentStep) {
            return 'continue_procedure';
        } else if (responseData && responseData.suggestions && responseData.suggestions.length > 0) {
            return responseData.suggestions[0].toLowerCase().replace(' ', '_');
        } else {
            return 'start_procedure';
        }
    }
    
    updateContextDisplay() {
        document.getElementById('user-experience').textContent = this.contextData.userExperience;
        document.getElementById('session-focus').textContent = this.contextData.sessionFocus.replace('_', ' ');
        document.getElementById('interaction-pattern').textContent = this.contextData.interactionPattern.replace('_', ' ');
        document.getElementById('predicted-action').textContent = this.contextData.predictedNextAction.replace('_', ' ');
    }
    
    trackPerformance(metric, value) {
        if (!this.performanceMetrics[metric]) {
            this.performanceMetrics[metric] = [];
        }
        
        this.performanceMetrics[metric].push({
            value: value,
            timestamp: Date.now()
        });
        
        // Keep only last 100 entries
        if (this.performanceMetrics[metric].length > 100) {
            this.performanceMetrics[metric] = this.performanceMetrics[metric].slice(-100);
        }
        
        this.updatePerformanceDisplay();
    }
    
    updatePerformanceDisplay() {
        // Update average response time
        const responseTimes = this.performanceMetrics.response_time || [];
        if (responseTimes.length > 0) {
            const avgTime = responseTimes.reduce((sum, item) => sum + item.value, 0) / responseTimes.length;
            document.getElementById('avg-response-time').textContent = `${Math.round(avgTime)} ms`;
        }
        
        // Update task completion rate
        const completedTasks = this.performanceMetrics.task_completion || [];
        if (completedTasks.length > 0) {
            const completionRate = completedTasks.filter(task => task.value === 1).length / completedTasks.length;
            document.getElementById('task-completion').textContent = `${Math.round(completionRate * 100)}%`;
        }
        
        // Update AI accuracy
        const predictions = this.performanceMetrics.ai_accuracy || [];
        if (predictions.length > 0) {
            const avgAccuracy = predictions.reduce((sum, item) => sum + item.value, 0) / predictions.length;
            document.getElementById('ai-accuracy').textContent = `${Math.round(avgAccuracy * 100)}%`;
        }
        
        // Update user satisfaction
        this.updateSatisfactionStars();
    }
    
    updateSatisfactionStars() {
        const satisfaction = this.performanceMetrics.user_satisfaction || [];
        if (satisfaction.length > 0) {
            const avgSatisfaction = satisfaction.reduce((sum, item) => sum + item.value, 0) / satisfaction.length;
            const stars = Math.round(avgSatisfaction);
            
            const starsContainer = document.getElementById('satisfaction-stars');
            starsContainer.innerHTML = '';
            
            for (let i = 1; i <= 5; i++) {
                const star = document.createElement('i');
                star.className = i <= stars ? 'fas fa-star' : 'far fa-star';
                starsContainer.appendChild(star);
            }
        }
    }
    
    // Smart Notification Methods
    
    showSmartNotification(message, type = 'info', details = null) {
        // Check if notifications are enabled
        if (!this.aiFeatures.smartNotifications) return;
        
        // Analyze notification priority
        const priority = this.analyzeNotificationPriority(message, type, details);
        
        // Show browser notification for high priority
        if (priority === 'high' && 'Notification' in window && Notification.permission === 'granted') {
            new Notification('Oracle EBS Assistant', {
                body: message,
                icon: '/static/images/icon.png'
            });
        }
        
        // Show in-app notification
        this.showToast(message, type);
        
        // Add to notification queue for analysis
        this.notificationQueue.push({
            message,
            type,
            priority,
            timestamp: Date.now(),
            details
        });
    }
    
    analyzeNotificationPriority(message, type, details) {
        if (type === 'error') return 'high';
        if (message.includes('validation') || message.includes('required')) return 'medium';
        if (details && details.length > 0) return 'medium';
        return 'low';
    }
    
    // AI Insights and Optimization Methods
    
    processAIInsights(insights) {
        this.aiInsights = insights;
        this.updateAIInsightsDisplay();
        
        // Process high-priority insights immediately
        insights.forEach(insight => {
            if (insight.priority === 'high') {
                this.showSmartNotification(insight.message, 'warning');
            }
        });
    }
    
    updateAIInsightsDisplay() {
        const content = document.getElementById('ai-insights-content');
        
        if (this.aiInsights.length === 0) {
            content.innerHTML = '<div class="no-insights">No insights available yet</div>';
            return;
        }
        
        content.innerHTML = this.aiInsights.map(insight => `
            <div class="insight-item ${insight.priority}">
                <div class="insight-header">
                    <span class="insight-type">${insight.type.replace('_', ' ').toUpperCase()}</span>
                    <span class="insight-confidence">${Math.round(insight.confidence * 100)}%</span>
                </div>
                <div class="insight-message">${insight.message}</div>
                <div class="insight-actions">
                    ${insight.action_items.map(item => 
                        `<button class="action-item" onclick="app.executeInsightAction('${item}')">${item}</button>`
                    ).join('')}
                </div>
            </div>
        `).join('');
    }
    
    executeInsightAction(action) {
        this.sendMessage(`AI suggestion: ${action}`);
    }
    
    async requestOptimization() {
        this.sendMessage('optimize current workflow');
    }
    
    async requestPrediction() {
        const context = this.currentProcedure ? `predict completion time for ${this.currentProcedure}` : 'predict next best action';
        this.sendMessage(context);
    }
    
    // Additional helper methods...
    
    loadUserPreferences() {
        const saved = localStorage.getItem('oracle_ebs_preferences');
        return saved ? JSON.parse(saved) : {
            theme: 'default',
            language: 'en',
            ai_features_enabled: true,
            notification_preferences: 'all'
        };
    }
    
    saveUserPreferences() {
        localStorage.setItem('oracle_ebs_preferences', JSON.stringify(this.userPreferences));
    }
    
    startPerformanceMonitoring() {
        // Monitor page load time
        window.addEventListener('load', () => {
            const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
            this.trackPerformance('page_load_time', loadTime);
        });
        
        // Monitor user engagement
        let engagementStart = Date.now();
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                const engagement = Date.now() - engagementStart;
                this.trackPerformance('engagement_time', engagement);
            } else {
                engagementStart = Date.now();
            }
        });
    }
    
    calculateErrorRate() {
        const errors = this.conversationContext.filter(c => 
            c.type === 'assistant' && (c.message.includes('error') || c.message.includes('sorry'))
        );
        return errors.length / Math.max(this.conversationContext.length, 1);
    }
    
    // Export and utility methods...
    
    exportData(data) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `oracle_ebs_data_${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }
    
    togglePanel(panelName) {
        const panel = document.querySelector(`.${panelName}-panel .panel-content`);
        if (panel) {
            panel.classList.toggle('collapsed');
        }
    }
    
    applySuggestion(suggestionType) {
        const suggestions = {
            'optimize_workflow': 'optimize my current workflow',
            'predict_completion': 'predict completion time',
            'check_risks': 'assess risks in current process'
        };
        
        this.sendMessage(suggestions[suggestionType] || suggestionType);
    }
    
    showAIInsights() {
        if (this.aiInsights.length > 0) {
            const insightsPanel = document.querySelector('.ai-insights-panel');
            insightsPanel.scrollIntoView({ behavior: 'smooth' });
            insightsPanel.classList.add('highlight');
            setTimeout(() => insightsPanel.classList.remove('highlight'), 2000);
        } else {
            this.showToast('No AI insights available yet. Continue using the assistant to generate insights.', 'info');
        }
    }
    
    toggleAIFeatures() {
        const modal = document.createElement('div');
        modal.className = 'ai-features-modal modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>AI Features Configuration</h3>
                    <button class="close-modal" onclick="this.closest('.modal').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-body">
                    ${Object.entries(this.aiFeatures).map(([feature, enabled]) => `
                        <div class="feature-toggle">
                            <label>
                                <input type="checkbox" ${enabled ? 'checked' : ''} 
                                       onchange="app.toggleAIFeature('${feature}', this.checked)">
                                <span class="feature-name">${feature.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                            </label>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }
    
    toggleAIFeature(feature, enabled) {
        this.aiFeatures[feature] = enabled;
        this.saveUserPreferences();
        this.showToast(`${feature.replace(/_/g, ' ')} ${enabled ? 'enabled' : 'disabled'}`, 'info');
    }
}

// Initialize enhanced application
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AdvancedOracleEBSAssistant();
});