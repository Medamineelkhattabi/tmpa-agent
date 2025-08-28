// Gestionnaire de thèmes pour l'assistant
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.applyTheme(this.currentTheme);
        this.createThemeToggle();
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        this.updateToggleButton();
    }

    createThemeToggle() {
        const header = document.querySelector('.header');
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'theme-toggle';
        toggleBtn.innerHTML = this.currentTheme === 'light' ? '🌙' : '☀️';
        toggleBtn.title = 'Changer le thème';
        toggleBtn.onclick = () => this.toggleTheme();
        
        header.appendChild(toggleBtn);
    }

    updateToggleButton() {
        const toggleBtn = document.querySelector('.theme-toggle');
        if (toggleBtn) {
            toggleBtn.innerHTML = this.currentTheme === 'light' ? '🌙' : '☀️';
        }
    }
}

// CSS pour les thèmes
const themeStyles = `
:root[data-theme="dark"] {
    --bg-color: #1a1a1a;
    --surface-color: #2d2d2d;
    --text-color: #ffffff;
    --text-secondary: #b0b0b0;
    --border-color: #404040;
    --primary-color: #3b82f6;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --error-color: #ef4444;
}

.theme-toggle {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 0.5rem;
    transition: background-color 0.2s;
}

.theme-toggle:hover {
    background-color: var(--border-color);
}
`;

// Injecter les styles
const styleSheet = document.createElement('style');
styleSheet.textContent = themeStyles;
document.head.appendChild(styleSheet);

window.ThemeManager = ThemeManager;