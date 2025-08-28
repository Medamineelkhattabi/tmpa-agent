// Clean Oracle EBS Assistant JavaScript
class OracleEBSAssistant {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.apiBaseUrl = 'http://localhost:8000';
        this.isLoading = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.autoResizeTextarea();
    }

    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }

    setupEventListeners() {
        const input = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');

        // Auto-resize textarea
        input.addEventListener('input', () => {
            this.autoResizeTextarea();
        });

        // Send on Enter (but allow Shift+Enter for new lines)
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    autoResizeTextarea() {
        const textarea = document.getElementById('messageInput');
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    async sendMessage(message = null) {
        const input = document.getElementById('messageInput');
        const messageText = message || input.value.trim();

        if (!messageText || this.isLoading) return;

        // Clear input if not using predefined message
        if (!message) {
            input.value = '';
            this.autoResizeTextarea();
        }

        // Add user message to chat
        this.addMessage(messageText, 'user');

        // Show loading
        this.showLoading();
        this.isLoading = true;

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: messageText,
                    session_id: this.sessionId,
                    context: {}
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Remove loading
            this.hideLoading();
            
            // Add assistant response
            this.addMessage(data.message, 'assistant', data.suggestions, data.current_step);

        } catch (error) {
            console.error('Error:', error);
            this.hideLoading();
            this.addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
        } finally {
            this.isLoading = false;
        }
    }

    addMessage(content, sender, suggestions = [], currentStep = null) {
        const messagesContainer = document.getElementById('chatMessages');
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'user' ? 'You' : 'AI';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';

        // Format message content
        const formattedContent = this.formatMessage(content);
        messageContent.innerHTML = formattedContent;

        // Add workflow step if present
        if (currentStep) {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'workflow-step';
            stepDiv.innerHTML = `
                <h3>${currentStep.title}</h3>
                <p><strong>Description:</strong> ${currentStep.description}</p>
                <p><strong>Instructions:</strong> ${currentStep.instructions}</p>
            `;
            messageContent.appendChild(stepDiv);
        }

        // Add suggestions
        if (suggestions && suggestions.length > 0) {
            const suggestionsDiv = document.createElement('div');
            suggestionsDiv.className = 'suggestions';
            
            suggestions.forEach(suggestion => {
                const btn = document.createElement('button');
                btn.className = 'suggestion-btn';
                btn.textContent = suggestion;
                btn.onclick = () => this.sendMessage(suggestion);
                suggestionsDiv.appendChild(btn);
            });
            
            messageContent.appendChild(suggestionsDiv);
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        messagesContainer.appendChild(messageDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    formatMessage(content) {
        // Convert markdown-like formatting to HTML
        let formatted = content
            // Bold text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Bullet points
            .replace(/^• (.+)$/gm, '<li>$1</li>')
            // Line breaks
            .replace(/\n/g, '<br>');

        // Wrap consecutive list items in ul tags
        formatted = formatted.replace(/(<li>.*<\/li>)(<br>)*(<li>.*<\/li>)/g, '<ul>$1$3</ul>');
        formatted = formatted.replace(/(<\/li>)(<br>)*(<li>)/g, '$1$3');

        return formatted;
    }

    showLoading() {
        const messagesContainer = document.getElementById('chatMessages');
        
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant';
        loadingDiv.id = 'loadingMessage';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = 'AI';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const loading = document.createElement('div');
        loading.className = 'loading';
        loading.innerHTML = '<div class="loading-dot"></div><div class="loading-dot"></div><div class="loading-dot"></div>';
        
        messageContent.appendChild(loading);
        loadingDiv.appendChild(avatar);
        loadingDiv.appendChild(messageContent);
        messagesContainer.appendChild(loadingDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideLoading() {
        const loadingMessage = document.getElementById('loadingMessage');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }

    async resetSession() {
        try {
            await fetch(`${this.apiBaseUrl}/api/session/${this.sessionId}/reset`, {
                method: 'POST'
            });
            
            // Clear chat messages except welcome message
            const messagesContainer = document.getElementById('chatMessages');
            const messages = messagesContainer.querySelectorAll('.message');
            
            // Keep only the first message (welcome message)
            for (let i = 1; i < messages.length; i++) {
                messages[i].remove();
            }
            
            // Generate new session ID
            this.sessionId = this.generateSessionId();
            
        } catch (error) {
            console.error('Error resetting session:', error);
        }
    }

    showHelp() {
        this.sendMessage('Help');
    }
}

// Global functions for HTML onclick events
let assistant;

function sendMessage(message) {
    assistant.sendMessage(message);
}

function resetSession() {
    assistant.resetSession();
}

function showHelp() {
    assistant.showHelp();
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        assistant.sendMessage();
    }
}

// Initialize the assistant when the page loads
document.addEventListener('DOMContentLoaded', () => {
    assistant = new OracleEBSAssistant();
});