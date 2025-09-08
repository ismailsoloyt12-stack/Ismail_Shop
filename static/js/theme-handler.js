// Theme Handler - Dark Mode Support
class ThemeHandler {
    constructor() {
        this.theme = this.getStoredTheme() || this.getSystemTheme();
        this.init();
    }

    init() {
        // Apply theme immediately to prevent flash
        this.applyTheme(this.theme);
        
        // Add theme toggle button to navbar
        this.addThemeToggle();
        
        // Listen for system theme changes
        this.watchSystemTheme();
        
        // Listen for storage events (syncs theme across tabs)
        window.addEventListener('storage', (e) => {
            if (e.key === 'theme') {
                this.theme = e.newValue;
                this.applyTheme(this.theme);
            }
        });
    }

    getStoredTheme() {
        // Check localStorage first
        const localTheme = localStorage.getItem('theme');
        if (localTheme) return localTheme;
        
        // Check cookie as fallback
        const cookieTheme = this.getCookie('theme');
        if (cookieTheme) return cookieTheme;
        
        return null;
    }

    getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }

    watchSystemTheme() {
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                if (!this.getStoredTheme()) {
                    this.theme = e.matches ? 'dark' : 'light';
                    this.applyTheme(this.theme);
                }
            });
        }
    }

    applyTheme(theme) {
        const root = document.documentElement;
        
        if (theme === 'dark') {
            root.setAttribute('data-theme', 'dark');
            document.body.classList.add('dark-mode');
            
            // Update meta theme color
            const metaTheme = document.querySelector('meta[name="theme-color"]');
            if (metaTheme) {
                metaTheme.content = '#1a1a2e';
            }
        } else {
            root.setAttribute('data-theme', 'light');
            document.body.classList.remove('dark-mode');
            
            // Update meta theme color
            const metaTheme = document.querySelector('meta[name="theme-color"]');
            if (metaTheme) {
                metaTheme.content = '#4361ee';
            }
        }
        
        // Update toggle button icon
        this.updateToggleIcon(theme);
        
        // Save preference
        this.saveTheme(theme);
        
        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme } }));
    }

    toggleTheme() {
        this.theme = this.theme === 'dark' ? 'light' : 'dark';
        this.applyTheme(this.theme);
        
        // Send to backend
        fetch('/api/theme/toggle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ theme: this.theme })
        });
    }

    saveTheme(theme) {
        localStorage.setItem('theme', theme);
        this.setCookie('theme', theme, 365);
    }

    addThemeToggle() {
        // Check if toggle already exists
        if (document.getElementById('theme-toggle')) return;
        
        const toggle = document.createElement('button');
        toggle.id = 'theme-toggle';
        toggle.className = 'theme-toggle-btn';
        toggle.setAttribute('aria-label', 'Toggle theme');
        toggle.innerHTML = this.theme === 'dark' ? 
            '<i class="fas fa-sun"></i>' : 
            '<i class="fas fa-moon"></i>';
        
        toggle.addEventListener('click', () => this.toggleTheme());
        
        // Try to add to navbar
        const navbar = document.querySelector('.navbar-nav') || document.querySelector('.nav-menu');
        if (navbar) {
            const li = document.createElement('li');
            li.className = 'nav-item';
            li.appendChild(toggle);
            navbar.appendChild(li);
        } else {
            // Fallback: add to body
            document.body.appendChild(toggle);
        }
    }

    updateToggleIcon(theme) {
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            toggle.innerHTML = theme === 'dark' ? 
                '<i class="fas fa-sun"></i>' : 
                '<i class="fas fa-moon"></i>';
        }
    }

    getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = `expires=${date.toUTCString()}`;
        document.cookie = `${name}=${value};${expires};path=/`;
    }
}

// Initialize theme handler when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeHandler = new ThemeHandler();
    });
} else {
    window.themeHandler = new ThemeHandler();
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeHandler;
}
