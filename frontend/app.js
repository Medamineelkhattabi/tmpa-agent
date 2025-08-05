class OracleEBSAssistant {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.apiBaseUrl = 'http://localhost:8000/api';
        this.currentProcedure = null;
        this.currentStep = null;
        this.isLoading = false;
        
        this.initializeElements();
        this.bindEvents();
        this.loadInitialData();
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    initializeElements() {
        // Chat elements
        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        this.suggestionsContainer = document.getElementById('suggestions-container');
        this.suggestions = document.getElementById('suggestions');
        
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
        
        // Set session ID display
        this.sessionIdDisplay.textContent = this.sessionId;
    }
    
    bindEvents() {
        // Input events
        this.messageInput.addEventListener('input', () => {
            this.sendBtn.disabled = !this.messageInput.value.trim();
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
        
        // Escape key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeScreenshotModal();
                this.closeSidebar();
            }
        });
    }
    
    async loadInitialData() {
        try {
            await this.loadProcedures();
            this.showInitialSuggestions();
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showToast('Error loading application data', 'error');
        }
    }
    
    async loadProcedures() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/procedures`);
            const data = await response.json();
            
            this.renderProcedures(data.procedures);
        } catch (error) {
            console.error('Error loading procedures:', error);
            this.proceduresList.innerHTML = '<div class="error">Failed to load procedures</div>';
        }
    }
    
    renderProcedures(procedures) {
        if (!procedures || procedures.length === 0) {
            this.proceduresList.innerHTML = '<div class="no-procedures">No procedures available</div>';
            return;
        }
        
        this.proceduresList.innerHTML = procedures.map(proc => `
            <div class="procedure-item" onclick="app.startProcedure('${proc.procedure_id}')">
                <h5>${proc.title}</h5>
                <p>${proc.description}</p>
                <span class="procedure-category">${proc.category}</span>
            </div>
        `).join('');
    }
    
    showInitialSuggestions() {
        const initialSuggestions = [
            'Start work confirmation',
            'Show purchase orders',
            'List invoices',
            'Help'
        ];
        
        this.renderSuggestions(initialSuggestions);
    }
    
    renderSuggestions(suggestions) {
        if (!suggestions || suggestions.length === 0) {
            this.suggestionsContainer.style.display = 'none';
            return;
        }
        
        this.suggestionsContainer.style.display = 'block';
        this.suggestions.innerHTML = suggestions.map(suggestion => 
            `<button class="suggestion-btn" onclick="app.sendSuggestion('${suggestion}')">${suggestion}</button>`
        ).join('');
    }
    
    async sendMessage(message = null) {
        const text = message || this.messageInput.value.trim();
        if (!text || this.isLoading) return;
        
        // Clear input and disable send button
        this.messageInput.value = '';
        this.sendBtn.disabled = true;
        
        // Add user message to chat
        this.addMessage(text, 'user');
        
        // Show loading
        this.setLoading(true);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: text,
                    session_id: this.sessionId,
                    context: {}
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Add assistant response
            this.addMessage(data.message, data.message_type || 'assistant', data);
            
            // Update session state
            this.updateSessionState(data.session_state);
            
            // Update current step if provided
            if (data.current_step) {
                this.updateCurrentStep(data.current_step);
            }
            
            // Show suggestions
            if (data.suggestions) {
                this.renderSuggestions(data.suggestions);
            }
            
            // Show validation errors if any
            if (data.validation_errors && data.validation_errors.length > 0) {
                this.showToast('Please complete all requirements before proceeding', 'warning');
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('Sorry, I encountered an error. Please try again.', 'error');
            this.showToast('Connection error. Please check your network.', 'error');
        } finally {
            this.setLoading(false);
        }
    }
    
    sendSuggestion(suggestion) {
        this.sendMessage(suggestion);
    }
    
    addMessage(content, type, data = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        messageText.innerHTML = this.formatMessage(content);
        
        messageContent.appendChild(messageText);
        
        // Add screenshot button if available
        if (data && data.screenshot) {
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'message-actions';
            
            const screenshotBtn = document.createElement('button');
            screenshotBtn.className = 'action-btn screenshot-btn';
            screenshotBtn.innerHTML = '<i class="fas fa-image"></i> View Screenshot';
            screenshotBtn.onclick = () => this.showScreenshot(data.screenshot, data.current_step?.title || 'Step Screenshot');
            
            actionsDiv.appendChild(screenshotBtn);
            messageContent.appendChild(actionsDiv);
        }
        
        // Add timestamp
        const timestamp = document.createElement('div');
        timestamp.className = 'timestamp';
        timestamp.textContent = new Date().toLocaleTimeString();
        messageContent.appendChild(timestamp);
        
        messageDiv.appendChild(messageContent);
        
        // Remove welcome message if it exists
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    formatMessage(content) {
        // Convert markdown-like formatting to HTML
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>')
            .replace(/^• (.+)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    }
    
    updateSessionState(sessionState) {
        if (!sessionState) return;
        
        // Update status badge
        this.sessionStatus.textContent = this.formatStatus(sessionState.status);
        this.sessionStatus.className = `status-badge ${sessionState.status.replace('_', '-')}`;
        
        // Update current procedure
        if (sessionState.current_procedure) {
            this.currentProcedure = sessionState.current_procedure;
            this.currentProcedureEl.innerHTML = `<span class="active-procedure">${sessionState.current_procedure}</span>`;
            this.showProcedureProgress(sessionState);
        } else {
            this.currentProcedure = null;
            this.currentProcedureEl.innerHTML = '<span class="no-procedure">No active procedure</span>';
            this.hideProcedureProgress();
        }
    }
    
    updateCurrentStep(stepData) {
        this.currentStep = stepData;
        // Additional step-specific UI updates can be added here
    }
    
    showProcedureProgress(sessionState) {
        this.procedureProgress.style.display = 'block';
        
        // Update procedure title (you might want to fetch the actual title)
        this.procedureTitle.textContent = sessionState.current_procedure.replace('_', ' ').toUpperCase();
        
        // Calculate progress
        const completedCount = sessionState.completed_steps ? sessionState.completed_steps.length : 0;
        const totalSteps = this.estimateTotalSteps(sessionState.current_procedure);
        const currentStepCount = sessionState.current_step ? completedCount + 1 : completedCount;
        
        this.stepCounter.textContent = `${currentStepCount}/${totalSteps}`;
        
        // Update progress bar
        const progressPercent = (completedCount / totalSteps) * 100;
        this.progressFill.style.width = `${progressPercent}%`;
        
        // Update completed steps list
        this.renderCompletedSteps(sessionState.completed_steps, sessionState.current_step);
    }
    
    hideProcedureProgress() {
        this.procedureProgress.style.display = 'none';
    }
    
    renderCompletedSteps(completedSteps, currentStep) {
        const steps = completedSteps || [];
        
        let stepsHtml = steps.map(step => 
            `<div class="step-item completed">
                <i class="fas fa-check-circle"></i>
                ${this.formatStepName(step)}
            </div>`
        ).join('');
        
        if (currentStep) {
            stepsHtml += `<div class="step-item current">
                <i class="fas fa-circle"></i>
                ${this.formatStepName(currentStep)}
            </div>`;
        }
        
        this.completedSteps.innerHTML = stepsHtml;
    }
    
    formatStepName(stepId) {
        return stepId.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    formatStatus(status) {
        return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    estimateTotalSteps(procedureId) {
        // This is a rough estimate - in a real app, you'd get this from the procedure data
        const stepCounts = {
            'work_confirmation': 6,
            'invoice_submission': 6,
            'view_purchase_orders': 3
        };
        return stepCounts[procedureId] || 5;
    }
    
    showScreenshot(screenshotPath, caption) {
        this.screenshotImage.src = screenshotPath;
        this.screenshotCaption.textContent = caption;
        this.screenshotModal.style.display = 'block';
    }
    
    closeScreenshotModal() {
        this.screenshotModal.style.display = 'none';
    }
    
    async startProcedure(procedureId) {
        const procedureNames = {
            'work_confirmation': 'Start work confirmation',
            'invoice_submission': 'Submit invoice',
            'view_purchase_orders': 'View purchase orders'
        };
        
        const message = procedureNames[procedureId] || `Start ${procedureId}`;
        await this.sendMessage(message);
        this.closeSidebar();
    }
    
    async resetSession() {
        if (!confirm('Are you sure you want to reset your session? This will clear all progress.')) {
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/session/${this.sessionId}/reset`, {
                method: 'POST'
            });
            
            if (response.ok) {
                // Clear chat messages
                this.chatMessages.innerHTML = `
                    <div class="welcome-message">
                        <div class="welcome-content">
                            <i class="fas fa-robot welcome-icon"></i>
                            <h2>Session Reset</h2>
                            <p>Your session has been reset. You can start a new procedure or ask me anything!</p>
                        </div>
                    </div>
                `;
                
                // Reset UI state
                this.currentProcedure = null;
                this.currentStep = null;
                this.updateSessionState({ status: 'not_started' });
                this.showInitialSuggestions();
                
                this.showToast('Session reset successfully', 'success');
            } else {
                throw new Error('Failed to reset session');
            }
        } catch (error) {
            console.error('Error resetting session:', error);
            this.showToast('Failed to reset session', 'error');
        }
    }
    
    toggleSidebar() {
        if (window.innerWidth <= 768) {
            this.sidebar.classList.toggle('open');
        }
    }
    
    closeSidebar() {
        this.sidebar.classList.remove('open');
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        this.loadingOverlay.style.display = loading ? 'block' : 'none';
        this.sendBtn.disabled = loading || !this.messageInput.value.trim();
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        this.toastContainer.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
        
        // Remove on click
        toast.addEventListener('click', () => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        });
    }
}

// Global functions for inline event handlers
function closeScreenshotModal() {
    if (window.app) {
        window.app.closeScreenshotModal();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new OracleEBSAssistant();
});

// Handle responsive sidebar
window.addEventListener('resize', () => {
    if (window.innerWidth > 768 && window.app) {
        window.app.closeSidebar();
    }
});