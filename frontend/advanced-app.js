// Advanced Oracle EBS Assistant - Enhanced Frontend
class OracleEBSAssistant {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.sessionId = this.generateSessionId();
        this.currentProcedure = null;
        this.isTyping = false;
        this.voiceEnabled = false;
        this.darkMode = localStorage.getItem('darkMode') === 'true';
        this.language = localStorage.getItem('language') || 'en';
        this.notifications = [];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeTheme();
        this.initializeVoice();
        this.loadUserPreferences();
        this.startPeriodicUpdates();
        this.initializeNotifications();
    }

    setupEventListeners() {
        // Enhanced chat input with auto-complete
        const chatInput = document.getElementById('chatInput');
        const sendButton = document.getElementById('sendButton');
        const voiceButton = document.getElementById('voiceButton');
        
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        chatInput.addEventListener('input', () => {
            this.handleAutoComplete();
            this.updateSendButtonState();
        });

        sendButton.addEventListener('click', () => this.sendMessage());
        voiceButton.addEventListener('click', () => this.toggleVoice());

        // Advanced UI controls
        document.getElementById('themeToggle').addEventListener('click', () => this.toggleTheme());
        document.getElementById('languageSelect').addEventListener('change', (e) => this.changeLanguage(e.target.value));
        document.getElementById('exportChat').addEventListener('click', () => this.exportChatHistory());
        document.getElementById('clearChat').addEventListener('click', () => this.clearChatHistory());
        
        // Procedure shortcuts
        this.setupProcedureShortcuts();
        
        // Drag and drop for file uploads
        this.setupDragAndDrop();
    }

    async sendMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;

        this.addMessageToChat('user', message);
        input.value = '';
        this.updateSendButtonState();
        this.showTypingIndicator();

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId,
                    context: {
                        language: this.language,
                        timestamp: new Date().toISOString(),
                        user_preferences: this.getUserPreferences()
                    }
                })
            });

            const data = await response.json();
            this.hideTypingIndicator();
            
            this.addMessageToChat('assistant', data.message, {
                suggestions: data.suggestions,
                screenshot: data.screenshot,
                currentStep: data.current_step,
                oracleData: data.oracle_data
            });

            this.updateProgressBar(data.session_state);
            this.updateSidebar(data.session_state);
            
            if (this.voiceEnabled) {
                this.speakMessage(data.message);
            }

        } catch (error) {
            this.hideTypingIndicator();
            this.addMessageToChat('error', 'Connection error. Please try again.');
            this.showNotification('Connection error', 'error');
        }
    }

    addMessageToChat(type, content, extras = {}) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const timestamp = new Date().toLocaleTimeString();
        
        let messageHTML = `
            <div class="message-header">
                <span class="message-type">${type === 'user' ? '👤 You' : '🤖 Assistant'}</span>
                <span class="message-time">${timestamp}</span>
            </div>
            <div class="message-content">${this.formatMessage(content)}</div>
        `;

        // Add enhanced features based on message type
        if (extras.suggestions && extras.suggestions.length > 0) {
            messageHTML += this.createSuggestionsHTML(extras.suggestions);
        }

        if (extras.screenshot) {
            messageHTML += this.createScreenshotHTML(extras.screenshot);
        }

        if (extras.currentStep) {
            messageHTML += this.createStepProgressHTML(extras.currentStep);
        }

        if (extras.oracleData) {
            messageHTML += this.createDataVisualizationHTML(extras.oracleData);
        }

        messageDiv.innerHTML = messageHTML;
        chatMessages.appendChild(messageDiv);
        
        // Smooth scroll with animation
        this.smoothScrollToBottom();
        
        // Add message to history
        this.addToHistory(type, content, timestamp);
    }

    createSuggestionsHTML(suggestions) {
        return `
            <div class="suggestions-container">
                <div class="suggestions-title">💡 Quick Actions:</div>
                <div class="suggestions-grid">
                    ${suggestions.map(suggestion => `
                        <button class="suggestion-btn" onclick="assistant.selectSuggestion('${suggestion}')">
                            ${suggestion}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    }

    createScreenshotHTML(screenshot) {
        return `
            <div class="screenshot-container">
                <div class="screenshot-header">
                    <span>📸 Visual Guide</span>
                    <button class="screenshot-fullscreen" onclick="assistant.openScreenshotModal('${screenshot}')">
                        🔍 View Full Size
                    </button>
                </div>
                <img src="${screenshot}" alt="Step Screenshot" class="screenshot-preview" 
                     onclick="assistant.openScreenshotModal('${screenshot}')">
            </div>
        `;
    }

    createStepProgressHTML(step) {
        return `
            <div class="step-progress-container">
                <div class="step-header">
                    <h4>📋 ${step.title}</h4>
                    <div class="step-status">Step ${this.getCurrentStepNumber()}</div>
                </div>
                <div class="step-description">${step.description}</div>
                <div class="step-instructions">
                    <strong>Instructions:</strong> ${step.instructions}
                </div>
                ${step.validation_criteria.length > 0 ? `
                    <div class="validation-criteria">
                        <strong>✅ Validation Checklist:</strong>
                        <ul>
                            ${step.validation_criteria.map(criteria => `<li>${criteria}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
            </div>
        `;
    }

    createDataVisualizationHTML(data) {
        if (!data || !data.results) return '';
        
        return `
            <div class="data-visualization">
                <div class="data-header">
                    <span>📊 Data Results</span>
                    <button class="export-data-btn" onclick="assistant.exportData(${JSON.stringify(data).replace(/"/g, '&quot;')})">
                        📥 Export
                    </button>
                </div>
                <div class="data-content">
                    ${this.formatDataResults(data.results)}
                </div>
            </div>
        `;
    }

    formatDataResults(results) {
        if (!Array.isArray(results)) return JSON.stringify(results, null, 2);
        
        return `
            <div class="data-table">
                <table>
                    <thead>
                        <tr>
                            ${Object.keys(results[0] || {}).map(key => `<th>${key}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${results.map(row => `
                            <tr>
                                ${Object.values(row).map(value => `<td>${value}</td>`).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    // Advanced UI Features
    toggleTheme() {
        this.darkMode = !this.darkMode;
        document.body.classList.toggle('dark-mode', this.darkMode);
        localStorage.setItem('darkMode', this.darkMode);
        this.showNotification(`${this.darkMode ? 'Dark' : 'Light'} mode enabled`, 'info');
    }

    async changeLanguage(language) {
        this.language = language;
        localStorage.setItem('language', language);
        await this.updateUILanguage();
        this.showNotification(`Language changed to ${language.toUpperCase()}`, 'info');
    }

    initializeVoice() {
        if ('speechRecognition' in window || 'webkitSpeechRecognition' in window) {
            this.recognition = new (window.speechRecognition || window.webkitSpeechRecognition)();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = this.language;

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('chatInput').value = transcript;
                this.sendMessage();
            };

            this.recognition.onerror = () => {
                this.showNotification('Voice recognition error', 'error');
            };
        }

        // Text-to-speech
        this.synthesis = window.speechSynthesis;
    }

    toggleVoice() {
        if (this.recognition) {
            if (this.voiceEnabled) {
                this.recognition.stop();
                this.voiceEnabled = false;
                document.getElementById('voiceButton').textContent = '🎤';
            } else {
                this.recognition.start();
                this.voiceEnabled = true;
                document.getElementById('voiceButton').textContent = '🔴';
            }
        }
    }

    speakMessage(text) {
        if (this.synthesis) {
            const utterance = new SpeechSynthesisUtterance(text.replace(/[*#]/g, ''));
            utterance.lang = this.language;
            this.synthesis.speak(utterance);
        }
    }

    // Auto-complete functionality
    handleAutoComplete() {
        const input = document.getElementById('chatInput');
        const value = input.value.toLowerCase();
        
        const suggestions = [
            'start work confirmation',
            'submit invoice',
            'view purchase orders',
            'create goods receipt',
            'track payment status',
            'show analytics dashboard',
            'get recommendations'
        ];

        const matches = suggestions.filter(s => s.includes(value) && value.length > 2);
        this.showAutoComplete(matches);
    }

    showAutoComplete(suggestions) {
        let dropdown = document.getElementById('autoCompleteDropdown');
        if (!dropdown) {
            dropdown = document.createElement('div');
            dropdown.id = 'autoCompleteDropdown';
            dropdown.className = 'autocomplete-dropdown';
            document.querySelector('.chat-input-container').appendChild(dropdown);
        }

        if (suggestions.length === 0) {
            dropdown.style.display = 'none';
            return;
        }

        dropdown.innerHTML = '';
        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            item.textContent = suggestion;
            item.addEventListener('click', () => this.selectAutoComplete(suggestion));
            dropdown.appendChild(item);
        });
        dropdown.style.display = 'block';
    }

    selectAutoComplete(suggestion) {
        document.getElementById('chatInput').value = suggestion;
        document.getElementById('autoCompleteDropdown').style.display = 'none';
        this.sendMessage();
    }

    // Notification system
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">×</button>
        `;
        
        document.getElementById('notificationContainer').appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    // Export functionality
    exportChatHistory() {
        const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        const blob = new Blob([JSON.stringify(history, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `oracle-ebs-chat-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    exportData(data) {
        const csv = this.convertToCSV(data.results);
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `oracle-data-${Date.now()}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }

    convertToCSV(data) {
        if (!Array.isArray(data) || data.length === 0) return '';
        
        const headers = Object.keys(data[0]);
        const csvContent = [
            headers.join(','),
            ...data.map(row => headers.map(header => `"${row[header] || ''}"`).join(','))
        ].join('\n');
        
        return csvContent;
    }

    // Utility functions
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    formatMessage(content) {
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    smoothScrollToBottom() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }

    addToHistory(type, content, timestamp) {
        const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        history.push({ type, content, timestamp, sessionId: this.sessionId });
        localStorage.setItem('chatHistory', JSON.stringify(history.slice(-100))); // Keep last 100 messages
    }

    getUserPreferences() {
        return {
            darkMode: this.darkMode,
            language: this.language,
            voiceEnabled: this.voiceEnabled
        };
    }

    updateSendButtonState() {
        const input = document.getElementById('chatInput');
        const button = document.getElementById('sendButton');
        button.disabled = !input.value.trim();
    }

    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'typingIndicator';
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
            <span>Assistant is typing...</span>
        `;
        document.getElementById('chatMessages').appendChild(indicator);
        this.smoothScrollToBottom();
    }

    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) indicator.remove();
    }
}

// Initialize the enhanced assistant
const assistant = new OracleEBSAssistant();