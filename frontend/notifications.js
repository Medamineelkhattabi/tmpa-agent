// Système de notifications pour l'assistant
class NotificationManager {
    constructor() {
        this.permission = Notification.permission;
    }

    async requestPermission() {
        if (this.permission === 'default') {
            this.permission = await Notification.requestPermission();
        }
        return this.permission === 'granted';
    }

    showNotification(title, options = {}) {
        if (this.permission === 'granted') {
            return new Notification(title, {
                icon: '/logo_tmpa.png',
                badge: '/logo_tmpa.png',
                ...options
            });
        }
    }

    notifyStepComplete(stepName) {
        this.showNotification('Étape Terminée', {
            body: `${stepName} complétée avec succès`,
            tag: 'step-complete'
        });
    }

    notifyProcedureComplete(procedureName) {
        this.showNotification('Procédure Terminée', {
            body: `${procedureName} terminée avec succès`,
            tag: 'procedure-complete'
        });
    }
}

// Export pour utilisation dans app.js
window.NotificationManager = NotificationManager;