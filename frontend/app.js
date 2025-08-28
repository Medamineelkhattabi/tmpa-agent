// Oracle EBS Assistant - Simple Version
class OracleEBSAssistant {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.sessionId = this.generateSessionId();
        this.currentProcedure = null;
        this.isTyping = false;
        this.currentLanguage = 'en'; // Default to English
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadProcedures();
        this.updateSessionDisplay();
        this.loadWelcomeMessage();
    }

    setupEventListeners() {
        const messageInput = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');
        
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        messageInput.addEventListener('input', () => {
            this.updateSendButtonState();
        });

        sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Header buttons
        document.getElementById('progress-btn').addEventListener('click', () => this.showProgress());
        document.getElementById('procedures-btn').addEventListener('click', () => this.showProcedures());
        document.getElementById('reset-btn').addEventListener('click', () => this.resetSession());
        
        // Language toggle button (if exists)
        const langBtn = document.getElementById('language-btn');
        if (langBtn) {
            langBtn.addEventListener('click', () => this.toggleLanguage());
        }
    }

    async sendMessage() {
        const input = document.getElementById('message-input');
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
                    session_id: this.sessionId
                })
            });

            const data = await response.json();
            this.hideTypingIndicator();
            
            // Update current language based on response
            if (data.language) {
                this.currentLanguage = data.language;
                this.updateLanguageDisplay();
            }
            
            this.addMessageToChat('assistant', data.response || data.message, {
                suggestions: data.suggestions,
                screenshot: data.screenshot,
                currentStep: data.current_step
            });

            if (data.session_state) {
                this.updateProgress(data.session_state);
            }

        } catch (error) {
            this.hideTypingIndicator();
            const errorMsg = this.currentLanguage === 'fr' ? 
                'Désolé, il y a eu une erreur de connexion. Veuillez réessayer.' :
                'Sorry, there was a connection error. Please try again.';
            this.addMessageToChat('assistant', errorMsg);
        }
    }

    addMessageToChat(type, content, extras = {}) {
        const chatMessages = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const timestamp = new Date().toLocaleTimeString();
        
        let messageHTML = `
            <div class="message-header">
                <span class="message-type">${type === 'user' ? 'You' : 'Assistant'}</span>
                <span class="message-time">${timestamp}</span>
            </div>
            <div class="message-content">${this.formatMessage(content)}</div>
        `;

        if (extras.suggestions && extras.suggestions.length > 0) {
            messageHTML += this.createSuggestionsHTML(extras.suggestions);
        }

        if (extras.screenshot) {
            messageHTML += this.createScreenshotHTML(extras.screenshot);
        }

        messageDiv.innerHTML = messageHTML;
        chatMessages.appendChild(messageDiv);
        
        this.scrollToBottom();
    }

    createSuggestionsHTML(suggestions) {
        return `
            <div class="suggestions-container">
                <div class="suggestions-title">Quick Actions:</div>
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
                    <button class="screenshot-btn" onclick="assistant.openScreenshot('${screenshot}')">
                        View Screenshot
                    </button>
                </div>
            </div>
        `;
    }

    selectSuggestion(suggestion) {
        const input = document.getElementById('message-input');
        input.value = suggestion;
        this.sendMessage();
    }

    openScreenshot(screenshot) {
        const modal = document.getElementById('screenshot-modal');
        const img = document.getElementById('screenshot-image');
        img.src = screenshot;
        modal.style.display = 'block';
    }

    async loadProcedures() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/procedures`);
            const data = await response.json();
            this.displayProcedures(data.procedures || []);
        } catch (error) {
            console.error('Failed to load procedures:', error);
        }
    }

    displayProcedures(procedures) {
        const container = document.getElementById('procedures-list');
        if (procedures.length === 0) {
            container.innerHTML = '<div class="no-procedures">No procedures available</div>';
            return;
        }

        container.innerHTML = procedures.map(proc => `
            <div class="procedure-item" onclick="assistant.startProcedure('${proc.procedure_id}')">
                <div class="procedure-title">${proc.title}</div>
                <div class="procedure-description">${proc.description}</div>
            </div>
        `).join('');
    }

    startProcedure(procedureId) {
        const input = document.getElementById('message-input');
        input.value = `Start ${procedureId.replace('_', ' ')}`;
        this.sendMessage();
    }

    updateProgress(sessionState) {
        if (sessionState.current_procedure) {
            this.currentProcedure = sessionState.current_procedure;
            const progressContainer = document.getElementById('procedure-progress');
            const currentProcedure = document.getElementById('current-procedure');
            
            progressContainer.style.display = 'block';
            currentProcedure.innerHTML = `<span class="active-procedure">${sessionState.current_procedure}</span>`;
            
            document.getElementById('procedure-title').textContent = sessionState.current_procedure;
            document.getElementById('step-counter').textContent = `${sessionState.completed_steps.length + 1}/10`;
            
            const progress = ((sessionState.completed_steps.length + 1) / 10) * 100;
            document.getElementById('progress-fill').style.width = `${progress}%`;
        }
    }

    showProgress() {
        if (this.currentProcedure) {
            const progressMsg = this.currentLanguage === 'fr' ? 
                `Procédure actuelle : ${this.currentProcedure}\nProgrès : En cours` :
                `Current procedure: ${this.currentProcedure}\nProgress: In progress`;
            this.addMessageToChat('assistant', progressMsg);
        } else {
            const noProgressMsg = this.currentLanguage === 'fr' ? 
                'Aucune procédure active. Commencez une nouvelle procédure pour suivre le progrès.' :
                'No active procedure. Start a new procedure to track progress.';
            this.addMessageToChat('assistant', noProgressMsg);
        }
    }

    showProcedures() {
        const input = document.getElementById('message-input');
        const proceduresMsg = this.currentLanguage === 'fr' ? 
            'Afficher les procédures disponibles' :
            'Show available procedures';
        input.value = proceduresMsg;
        this.sendMessage();
    }

    resetSession() {
        this.sessionId = this.generateSessionId();
        this.currentProcedure = null;
        document.getElementById('chat-messages').innerHTML = '';
        document.getElementById('procedure-progress').style.display = 'none';
        const noProcText = this.currentLanguage === 'fr' ? 'Aucune procédure active' : 'No active procedure';
        document.getElementById('current-procedure').innerHTML = `<span class="no-procedure">${noProcText}</span>`;
        this.updateSessionDisplay();
        
        const resetMsg = this.currentLanguage === 'fr' ? 
            'Session réinitialisée. Comment puis-je vous aider ?' :
            'Session reset. How can I help you?';
        this.addMessageToChat('assistant', resetMsg);
    }

    updateSessionDisplay() {
        document.getElementById('session-id-display').textContent = this.sessionId.substring(0, 8) + '...';
        document.getElementById('session-status').textContent = 'Active';
    }

    showTypingIndicator() {
        this.isTyping = true;
        const chatMessages = document.getElementById('chat-messages');
        const indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.className = 'typing-indicator';
        indicator.innerHTML = '<span>Assistant is typing...</span>';
        chatMessages.appendChild(indicator);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isTyping = false;
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }

    updateSendButtonState() {
        const input = document.getElementById('message-input');
        const button = document.getElementById('send-btn');
        button.disabled = !input.value.trim();
    }

    formatMessage(content) {
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    scrollToBottom() {
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }
    
    async loadWelcomeMessage() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/welcome?lang=${this.currentLanguage}`);
            const data = await response.json();
            this.addMessageToChat('assistant', data.message);
        } catch (error) {
            const welcomeMsg = this.currentLanguage === 'fr' ? 
                'Bienvenue dans l\'Assistant Oracle EBS R12 pour Tanger Med!' :
                'Welcome to Oracle EBS R12 Assistant for Tanger Med!';
            this.addMessageToChat('assistant', welcomeMsg);
        }
    }
    
    toggleLanguage() {
        this.currentLanguage = this.currentLanguage === 'en' ? 'fr' : 'en';
        this.updateLanguageDisplay();
        
        // Send a language switch message
        const switchMsg = this.currentLanguage === 'fr' ? 
            'Bonjour, je peux vous aider en français.' :
            'Hello, I can help you in English.';
        this.addMessageToChat('assistant', switchMsg);
    }
    
    updateLanguageDisplay() {
        const langBtn = document.getElementById('language-btn');
        if (langBtn) {
            langBtn.textContent = this.currentLanguage === 'en' ? 'FR' : 'EN';
            langBtn.title = this.currentLanguage === 'en' ? 'Switch to French' : 'Passer à l\'anglais';
        }
        
        // Update UI text based on language
        this.updateUILanguage();
    }
    
    updateUILanguage() {
        const translations = {
            en: {
                'message-placeholder': 'Type your message...',
                'progress-btn': 'Progress',
                'procedures-btn': 'Procedures',
                'reset-btn': 'Reset',
                'send-btn': 'Send',
                'no-procedure': 'No active procedure',
                'session-status': 'Active'
            },
            fr: {
                'message-placeholder': 'Tapez votre message...',
                'progress-btn': 'Progrès',
                'procedures-btn': 'Procédures',
                'reset-btn': 'Réinitialiser',
                'send-btn': 'Envoyer',
                'no-procedure': 'Aucune procédure active',
                'session-status': 'Actif'
            }
        };
        
        const currentTranslations = translations[this.currentLanguage];
        
        // Update placeholder
        const messageInput = document.getElementById('message-input');
        if (messageInput) {
            messageInput.placeholder = currentTranslations['message-placeholder'];
        }
        
        // Update button texts
        const elements = ['progress-btn', 'procedures-btn', 'reset-btn', 'send-btn'];
        elements.forEach(id => {
            const element = document.getElementById(id);
            if (element && currentTranslations[id]) {
                element.textContent = currentTranslations[id];
            }
        });
        
        // Update status texts
        const sessionStatus = document.getElementById('session-status');
        if (sessionStatus) {
            sessionStatus.textContent = currentTranslations['session-status'];
        }
    }
    
    detectLanguage(text) {
        const frenchWords = ['bonjour', 'salut', 'merci', 'comment', 'pourquoi', 'aide', 'procédure', 'étape'];
        const textLower = text.toLowerCase();
        const frenchCount = frenchWords.filter(word => textLower.includes(word)).length;
        return frenchCount > 0 ? 'fr' : 'en';
    }
}

// Close screenshot modal
function closeScreenshotModal() {
    document.getElementById('screenshot-modal').style.display = 'none';
}

// Initialize the assistant
const assistant = new OracleEBSAssistant();