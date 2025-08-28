// Raccourcis clavier pour l'assistant Oracle EBS
class KeyboardShortcuts {
    constructor(chatInterface) {
        this.chatInterface = chatInterface;
        this.setupShortcuts();
    }

    setupShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl + Enter : Envoyer message
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                this.chatInterface.sendMessage();
            }
            
            // Ctrl + N : Nouvelle procédure
            if (e.ctrlKey && e.key === 'n') {
                e.preventDefault();
                this.showProcedureList();
            }
            
            // Ctrl + H : Aide
            if (e.ctrlKey && e.key === 'h') {
                e.preventDefault();
                this.showHelp();
            }
            
            // Escape : Fermer modales
            if (e.key === 'Escape') {
                this.closeModals();
            }
            
            // F1 : Guide rapide
            if (e.key === 'F1') {
                e.preventDefault();
                this.showQuickGuide();
            }
        });
    }

    showProcedureList() {
        const message = "Afficher les procédures disponibles";
        this.chatInterface.addMessage(message, 'user');
        this.chatInterface.sendToBackend(message);
    }

    showHelp() {
        const helpMessage = `
🔧 Raccourcis Clavier:
• Ctrl + Enter : Envoyer message
• Ctrl + N : Nouvelle procédure  
• Ctrl + H : Aide
• Escape : Fermer modales
• F1 : Guide rapide
        `;
        this.chatInterface.addMessage(helpMessage, 'assistant');
    }

    closeModals() {
        const modals = document.querySelectorAll('.modal.active');
        modals.forEach(modal => modal.classList.remove('active'));
    }

    showQuickGuide() {
        const guide = `
🚀 Guide Rapide:
1. Tapez "start" pour commencer une procédure
2. Utilisez "help" pour obtenir de l'aide
3. Tapez "done" pour passer à l'étape suivante
4. Cliquez sur les captures d'écran pour les agrandir
        `;
        this.chatInterface.addMessage(guide, 'assistant');
    }
}

window.KeyboardShortcuts = KeyboardShortcuts;