// Enhanced App Store JavaScript - Professional Implementation
// Includes: Fixed Sidebar, Theme System, Command Palette, Mobile UX

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        MOBILE_BREAKPOINT: 768,
        SIDEBAR_ANIMATION_DURATION: 300,
        THEME_KEY: 'app-store-theme',
        COMMAND_PALETTE_KEY: 'app-store-cmd-history',
        SEARCH_DEBOUNCE_MS: 300,
        SCROLL_OFFSET: 80
    };

    // App State Management
    const AppState = {
        theme: 'light',
        sidebarOpen: false,
        commandPaletteOpen: false,
        isMobile: false,
        scrollPosition: 0,
        commandHistory: []
    };

    // DOM Elements Cache
    const Elements = {
        html: null,
        body: null,
        navbar: null,
        sidebar: null,
        sidebarOverlay: null,
        mainContent: null,
        footer: null,
        themeToggle: null,
        themeIcon: null,
        menuToggle: null,
        commandPalette: null,
        commandSearch: null,
        commandResults: null
    };

    // Initialize DOM Elements
    function initializeElements() {
        Elements.html = document.documentElement;
        Elements.body = document.body;
        Elements.navbar = document.querySelector('.navbar');
        Elements.sidebar = document.getElementById('sidebar');
        Elements.mainContent = document.getElementById('mainContent');
        Elements.footer = document.querySelector('.footer');
        Elements.themeToggle = document.getElementById('themeToggle');
        Elements.themeIcon = document.getElementById('themeIcon');
        Elements.menuToggle = document.getElementById('menuToggle');
    }

    // ===========================================
    // Theme System - Persistent & Flash-Free
    // ===========================================
    
    const ThemeManager = {
        init() {
            // Apply theme immediately to prevent flash
            const savedTheme = this.getSavedTheme();
            this.applyTheme(savedTheme, false);
            this.setupEventListeners();
            this.updateMetaThemeColor();
        },

        getSavedTheme() {
            const saved = localStorage.getItem(CONFIG.THEME_KEY);
            if (saved) return saved;
            
            // Check system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                return 'dark';
            }
            return 'light';
        },

        applyTheme(theme, animate = true) {
            AppState.theme = theme;
            
            // Apply theme to HTML element
            Elements.html.setAttribute('data-theme', theme);
            
            // Save preference
            localStorage.setItem(CONFIG.THEME_KEY, theme);
            
            // Update icon
            this.updateIcon(theme);
            
            // Update meta theme color
            this.updateMetaThemeColor();
            
            // Add animation class if needed
            if (animate && Elements.body) {
                Elements.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
                setTimeout(() => {
                    if (Elements.body) {
                        Elements.body.style.transition = '';
                    }
                }, 300);
            }
        },

        updateIcon(theme) {
            if (Elements.themeIcon) {
                Elements.themeIcon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
            }
        },

        updateMetaThemeColor() {
            const metaThemeColor = document.querySelector('meta[name="theme-color"]');
            const color = AppState.theme === 'dark' ? '#0f0f0f' : '#ffffff';
            
            if (metaThemeColor) {
                metaThemeColor.setAttribute('content', color);
            } else {
                const meta = document.createElement('meta');
                meta.name = 'theme-color';
                meta.content = color;
                document.head.appendChild(meta);
            }
        },

        toggle() {
            const newTheme = AppState.theme === 'light' ? 'dark' : 'light';
            this.applyTheme(newTheme, true);
        },

        setupEventListeners() {
            if (Elements.themeToggle) {
                Elements.themeToggle.addEventListener('click', () => this.toggle());
            }

            // Listen for system theme changes
            if (window.matchMedia) {
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
                    if (!localStorage.getItem(CONFIG.THEME_KEY)) {
                        this.applyTheme(e.matches ? 'dark' : 'light', true);
                    }
                });
            }
        }
    };

    // ===========================================
    // Sidebar Manager - Fixed & Mobile-Optimized
    // ===========================================
    
    const SidebarManager = {
        init() {
            this.createOverlay();
            this.setupEventListeners();
            this.initializeState();
            this.setupMobileCloseButton();
            this.setupSwipeGestures();
            this.setupFocusTrap();
        },

        createOverlay() {
            if (!Elements.sidebarOverlay) {
                const overlay = document.createElement('div');
                overlay.className = 'sidebar-overlay';
                Elements.body.appendChild(overlay);
                Elements.sidebarOverlay = overlay;
                
                // Close sidebar when clicking overlay
                overlay.addEventListener('click', () => this.close());
            }
        },

        setupMobileCloseButton() {
            if (AppState.isMobile && Elements.sidebar) {
                const existingBtn = Elements.sidebar.querySelector('.sidebar-close');
                if (!existingBtn) {
                    const closeBtn = document.createElement('button');
                    closeBtn.className = 'sidebar-close';
                    closeBtn.innerHTML = '<i class="fas fa-times"></i>';
                    closeBtn.setAttribute('aria-label', 'Close sidebar');
                    closeBtn.addEventListener('click', () => this.close());
                    Elements.sidebar.prepend(closeBtn);
                }
            }
        },

        initializeState() {
            AppState.isMobile = window.innerWidth <= CONFIG.MOBILE_BREAKPOINT;
            
            if (AppState.isMobile) {
                this.setMobileState();
            } else {
                this.setDesktopState();
            }
        },

        setMobileState() {
            if (Elements.sidebar) {
                Elements.sidebar.classList.add('hidden');
                Elements.sidebar.classList.remove('active');
            }
            if (Elements.mainContent) {
                Elements.mainContent.classList.add('expanded');
            }
            if (Elements.footer) {
                Elements.footer.classList.add('expanded');
            }
        },

        setDesktopState() {
            if (Elements.sidebar) {
                Elements.sidebar.classList.remove('hidden', 'active');
            }
            if (Elements.mainContent) {
                Elements.mainContent.classList.remove('expanded');
            }
            if (Elements.footer) {
                Elements.footer.classList.remove('expanded');
            }
            if (Elements.sidebarOverlay) {
                Elements.sidebarOverlay.classList.remove('active');
            }
            Elements.body.classList.remove('sidebar-open');
        },

        open() {
            if (!Elements.sidebar) return;
            
            AppState.sidebarOpen = true;
            
            if (AppState.isMobile) {
                // Mobile behavior
                Elements.sidebar.classList.remove('hidden');
                setTimeout(() => {
                    Elements.sidebar.classList.add('active');
                    Elements.sidebarOverlay?.classList.add('active');
                    Elements.body.classList.add('sidebar-open');
                }, 10);
                
                // Trap focus
                this.trapFocus();
            } else {
                // Desktop behavior
                Elements.sidebar.classList.remove('hidden');
                Elements.mainContent?.classList.remove('expanded');
                Elements.footer?.classList.remove('expanded');
            }
        },

        close() {
            if (!Elements.sidebar) return;
            
            AppState.sidebarOpen = false;
            
            if (AppState.isMobile) {
                // Mobile behavior
                Elements.sidebar.classList.remove('active');
                Elements.sidebarOverlay?.classList.remove('active');
                Elements.body.classList.remove('sidebar-open');
                
                setTimeout(() => {
                    Elements.sidebar.classList.add('hidden');
                }, CONFIG.SIDEBAR_ANIMATION_DURATION);
                
                // Release focus trap
                this.releaseFocus();
            } else {
                // Desktop behavior
                Elements.sidebar.classList.add('hidden');
                Elements.mainContent?.classList.add('expanded');
                Elements.footer?.classList.add('expanded');
            }
        },

        toggle() {
            if (AppState.sidebarOpen || !Elements.sidebar?.classList.contains('hidden')) {
                this.close();
            } else {
                this.open();
            }
        },

        trapFocus() {
            if (!Elements.sidebar) return;
            
            const focusableElements = Elements.sidebar.querySelectorAll(
                'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
            );
            
            const firstFocusableElement = focusableElements[0];
            const lastFocusableElement = focusableElements[focusableElements.length - 1];
            
            Elements.sidebar.addEventListener('keydown', this.handleTrapFocus = (e) => {
                if (e.key === 'Tab') {
                    if (e.shiftKey) {
                        if (document.activeElement === firstFocusableElement) {
                            lastFocusableElement?.focus();
                            e.preventDefault();
                        }
                    } else {
                        if (document.activeElement === lastFocusableElement) {
                            firstFocusableElement?.focus();
                            e.preventDefault();
                        }
                    }
                }
            });
            
            firstFocusableElement?.focus();
        },

        releaseFocus() {
            if (this.handleTrapFocus && Elements.sidebar) {
                Elements.sidebar.removeEventListener('keydown', this.handleTrapFocus);
                this.handleTrapFocus = null;
            }
        },

        setupSwipeGestures() {
            let touchStartX = 0;
            let touchEndX = 0;
            
            document.addEventListener('touchstart', (e) => {
                touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });
            
            document.addEventListener('touchend', (e) => {
                touchEndX = e.changedTouches[0].screenX;
                this.handleSwipe(touchStartX, touchEndX);
            }, { passive: true });
        },

        handleSwipe(startX, endX) {
            if (!AppState.isMobile) return;
            
            const swipeThreshold = 50;
            const swipeDistance = endX - startX;
            
            // Swipe right to open (from left edge)
            if (swipeDistance > swipeThreshold && startX < 50 && !AppState.sidebarOpen) {
                this.open();
            }
            // Swipe left to close
            else if (swipeDistance < -swipeThreshold && AppState.sidebarOpen) {
                this.close();
            }
        },

        setupEventListeners() {
            // Menu toggle button
            if (Elements.menuToggle) {
                Elements.menuToggle.addEventListener('click', () => this.toggle());
            }
            
            // Close on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && AppState.sidebarOpen && AppState.isMobile) {
                    this.close();
                }
            });
            
            // Handle window resize
            let resizeTimer;
            window.addEventListener('resize', () => {
                clearTimeout(resizeTimer);
                resizeTimer = setTimeout(() => {
                    const wasMobile = AppState.isMobile;
                    AppState.isMobile = window.innerWidth <= CONFIG.MOBILE_BREAKPOINT;
                    
                    if (wasMobile !== AppState.isMobile) {
                        this.initializeState();
                        if (AppState.isMobile) {
                            this.setupMobileCloseButton();
                        }
                    }
                }, 250);
            });
            
            // Close sidebar when clicking links on mobile
            if (AppState.isMobile && Elements.sidebar) {
                Elements.sidebar.querySelectorAll('a').forEach(link => {
                    link.addEventListener('click', () => {
                        setTimeout(() => this.close(), 100);
                    });
                });
            }
        }
    };

    // ===========================================
    // Command Palette - Power Feature
    // ===========================================
    
    const CommandPalette = {
        commands: [],
        selectedIndex: 0,
        
        init() {
            this.createPalette();
            this.loadCommands();
            this.setupEventListeners();
        },

        createPalette() {
            const palette = document.createElement('div');
            palette.className = 'command-palette';
            palette.innerHTML = `
                <div class="command-palette-modal">
                    <div class="command-palette-header">
                        <i class="fas fa-search"></i>
                        <input type="text" class="command-palette-search" placeholder="Type a command or search..." autocomplete="off">
                        <span class="command-shortcut">ESC</span>
                    </div>
                    <div class="command-palette-results"></div>
                </div>
            `;
            
            Elements.body.appendChild(palette);
            Elements.commandPalette = palette;
            Elements.commandSearch = palette.querySelector('.command-palette-search');
            Elements.commandResults = palette.querySelector('.command-palette-results');
        },

        loadCommands() {
            // Define available commands
            this.commands = [
                {
                    title: 'Go to Home',
                    description: 'Navigate to homepage',
                    icon: 'fa-home',
                    action: () => window.location.href = '/',
                    keywords: ['home', 'main', 'index']
                },
                {
                    title: 'Toggle Theme',
                    description: 'Switch between light and dark mode',
                    icon: 'fa-adjust',
                    action: () => ThemeManager.toggle(),
                    keywords: ['theme', 'dark', 'light', 'mode']
                },
                {
                    title: 'Open Sidebar',
                    description: 'Show navigation sidebar',
                    icon: 'fa-bars',
                    action: () => SidebarManager.open(),
                    keywords: ['menu', 'navigation', 'sidebar']
                },
                {
                    title: 'Search Apps',
                    description: 'Search for apps and games',
                    icon: 'fa-search',
                    action: () => {
                        const searchInput = document.querySelector('.search-box input');
                        if (searchInput) {
                            searchInput.focus();
                            this.close();
                        }
                    },
                    keywords: ['find', 'search', 'look']
                },
                {
                    title: 'View Games',
                    description: 'Browse games category',
                    icon: 'fa-gamepad',
                    action: () => window.location.href = '/category/Games',
                    keywords: ['games', 'play', 'gaming']
                },
                {
                    title: 'View Apps',
                    description: 'Browse apps category',
                    icon: 'fa-th',
                    action: () => window.location.href = '/category/Apps',
                    keywords: ['apps', 'applications', 'software']
                },
                {
                    title: 'View Tools',
                    description: 'Browse tools category',
                    icon: 'fa-tools',
                    action: () => window.location.href = '/category/Tools',
                    keywords: ['tools', 'utilities', 'utility']
                },
                {
                    title: 'View Social',
                    description: 'Browse social apps',
                    icon: 'fa-users',
                    action: () => window.location.href = '/category/Social',
                    keywords: ['social', 'chat', 'messaging']
                },
                {
                    title: 'My Favorites',
                    description: 'View your favorite apps',
                    icon: 'fa-heart',
                    action: () => window.location.href = '/favorites',
                    keywords: ['favorites', 'likes', 'saved']
                },
                {
                    title: 'Refresh Page',
                    description: 'Reload the current page',
                    icon: 'fa-sync',
                    action: () => window.location.reload(),
                    keywords: ['refresh', 'reload', 'update']
                },
                {
                    title: 'Scroll to Top',
                    description: 'Go to top of page',
                    icon: 'fa-arrow-up',
                    action: () => {
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                        this.close();
                    },
                    keywords: ['top', 'up', 'scroll']
                },
                {
                    title: 'Scroll to Bottom',
                    description: 'Go to bottom of page',
                    icon: 'fa-arrow-down',
                    action: () => {
                        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
                        this.close();
                    },
                    keywords: ['bottom', 'down', 'scroll']
                },
                {
                    title: 'Print Page',
                    description: 'Print the current page',
                    icon: 'fa-print',
                    action: () => {
                        window.print();
                        this.close();
                    },
                    keywords: ['print', 'pdf', 'save']
                },
                {
                    title: 'Copy Link',
                    description: 'Copy current page URL',
                    icon: 'fa-link',
                    action: () => {
                        navigator.clipboard.writeText(window.location.href);
                        this.showNotification('Link copied to clipboard!');
                        this.close();
                    },
                    keywords: ['copy', 'link', 'url', 'share']
                }
            ];
            
            // Load dynamic app data if available
            this.loadAppCommands();
        },

        loadAppCommands() {
            // Try to fetch app data for quick navigation
            fetch('/apps_data.json')
                .then(response => response.json())
                .then(data => {
                    if (data && data.apps) {
                        data.apps.forEach(app => {
                            this.commands.push({
                                title: `Open ${app.name}`,
                                description: `${app.developer} - ${app.category}`,
                                icon: 'fa-rocket',
                                action: () => window.location.href = `/app/${app.id}`,
                                keywords: [app.name.toLowerCase(), app.category.toLowerCase(), app.developer.toLowerCase()]
                            });
                        });
                    }
                })
                .catch(error => console.log('Could not load app data for command palette'));
        },

        open() {
            if (!Elements.commandPalette) return;
            
            AppState.commandPaletteOpen = true;
            Elements.commandPalette.classList.add('active');
            Elements.commandSearch.value = '';
            Elements.commandSearch.focus();
            
            this.renderResults(this.commands.slice(0, 10));
            this.selectedIndex = 0;
            
            // Prevent body scroll
            Elements.body.style.overflow = 'hidden';
        },

        close() {
            if (!Elements.commandPalette) return;
            
            AppState.commandPaletteOpen = false;
            Elements.commandPalette.classList.remove('active');
            
            // Restore body scroll
            Elements.body.style.overflow = '';
        },

        toggle() {
            if (AppState.commandPaletteOpen) {
                this.close();
            } else {
                this.open();
            }
        },

        search(query) {
            if (!query) {
                this.renderResults(this.commands.slice(0, 10));
                return;
            }
            
            const lowerQuery = query.toLowerCase();
            const results = this.commands.filter(cmd => {
                const titleMatch = cmd.title.toLowerCase().includes(lowerQuery);
                const descMatch = cmd.description.toLowerCase().includes(lowerQuery);
                const keywordMatch = cmd.keywords.some(k => k.includes(lowerQuery));
                
                return titleMatch || descMatch || keywordMatch;
            });
            
            // Fuzzy matching for better results
            results.sort((a, b) => {
                const aTitle = a.title.toLowerCase();
                const bTitle = b.title.toLowerCase();
                
                if (aTitle.startsWith(lowerQuery) && !bTitle.startsWith(lowerQuery)) return -1;
                if (!aTitle.startsWith(lowerQuery) && bTitle.startsWith(lowerQuery)) return 1;
                
                return 0;
            });
            
            this.renderResults(results.slice(0, 10));
        },

        renderResults(results) {
            if (!Elements.commandResults) return;
            
            if (results.length === 0) {
                Elements.commandResults.innerHTML = `
                    <div class="command-result">
                        <div class="command-result-icon">
                            <i class="fas fa-search"></i>
                        </div>
                        <div class="command-result-content">
                            <div class="command-result-title">No results found</div>
                            <div class="command-result-description">Try a different search term</div>
                        </div>
                    </div>
                `;
                return;
            }
            
            Elements.commandResults.innerHTML = results.map((cmd, index) => `
                <div class="command-result ${index === this.selectedIndex ? 'selected' : ''}" data-index="${index}">
                    <div class="command-result-icon">
                        <i class="fas ${cmd.icon}"></i>
                    </div>
                    <div class="command-result-content">
                        <div class="command-result-title">${this.escapeHtml(cmd.title)}</div>
                        <div class="command-result-description">${this.escapeHtml(cmd.description)}</div>
                    </div>
                    <div class="command-result-action">
                        <span>↵</span>
                    </div>
                </div>
            `).join('');
            
            // Add click handlers
            Elements.commandResults.querySelectorAll('.command-result').forEach((el, index) => {
                el.addEventListener('click', () => {
                    this.executeCommand(results[index]);
                });
                
                el.addEventListener('mouseenter', () => {
                    this.selectedIndex = index;
                    this.updateSelection();
                });
            });
        },

        updateSelection() {
            Elements.commandResults.querySelectorAll('.command-result').forEach((el, index) => {
                if (index === this.selectedIndex) {
                    el.classList.add('selected');
                } else {
                    el.classList.remove('selected');
                }
            });
        },

        executeCommand(command) {
            if (command && command.action) {
                command.action();
                
                // Save to history
                this.saveToHistory(command);
            }
        },

        saveToHistory(command) {
            const history = JSON.parse(localStorage.getItem(CONFIG.COMMAND_PALETTE_KEY) || '[]');
            
            // Remove if already exists
            const existingIndex = history.findIndex(h => h.title === command.title);
            if (existingIndex !== -1) {
                history.splice(existingIndex, 1);
            }
            
            // Add to beginning
            history.unshift({
                title: command.title,
                timestamp: Date.now()
            });
            
            // Keep only last 10
            history.splice(10);
            
            localStorage.setItem(CONFIG.COMMAND_PALETTE_KEY, JSON.stringify(history));
        },

        showNotification(message) {
            const notification = document.createElement('div');
            notification.className = 'command-notification';
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: var(--accent-primary);
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                z-index: 10000;
                animation: slideInUp 0.3s ease;
            `;
            
            Elements.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 2000);
        },

        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },

        setupEventListeners() {
            // Global keyboard shortcut
            document.addEventListener('keydown', (e) => {
                // Ctrl/Cmd + K
                if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                    e.preventDefault();
                    this.toggle();
                }
                
                // Handle navigation when palette is open
                if (AppState.commandPaletteOpen) {
                    switch(e.key) {
                        case 'Escape':
                            e.preventDefault();
                            this.close();
                            break;
                        case 'ArrowDown':
                            e.preventDefault();
                            this.navigateDown();
                            break;
                        case 'ArrowUp':
                            e.preventDefault();
                            this.navigateUp();
                            break;
                        case 'Enter':
                            e.preventDefault();
                            this.selectCurrent();
                            break;
                    }
                }
            });
            
            // Search input
            if (Elements.commandSearch) {
                let searchTimeout;
                Elements.commandSearch.addEventListener('input', (e) => {
                    clearTimeout(searchTimeout);
                    searchTimeout = setTimeout(() => {
                        this.search(e.target.value);
                        this.selectedIndex = 0;
                    }, 100);
                });
            }
            
            // Close on outside click
            if (Elements.commandPalette) {
                Elements.commandPalette.addEventListener('click', (e) => {
                    if (e.target === Elements.commandPalette) {
                        this.close();
                    }
                });
            }
        },

        navigateDown() {
            const results = Elements.commandResults.querySelectorAll('.command-result');
            if (this.selectedIndex < results.length - 1) {
                this.selectedIndex++;
                this.updateSelection();
                results[this.selectedIndex].scrollIntoView({ block: 'nearest' });
            }
        },

        navigateUp() {
            if (this.selectedIndex > 0) {
                this.selectedIndex--;
                this.updateSelection();
                const results = Elements.commandResults.querySelectorAll('.command-result');
                results[this.selectedIndex].scrollIntoView({ block: 'nearest' });
            }
        },

        selectCurrent() {
            const results = Elements.commandResults.querySelectorAll('.command-result');
            const selected = results[this.selectedIndex];
            if (selected) {
                selected.click();
            }
        }
    };

    // ===========================================
    // Additional UX Enhancements
    // ===========================================
    
    const UXEnhancements = {
        init() {
            this.setupSmoothScroll();
            this.setupLazyLoading();
            this.setupCardAnimations();
            this.setupAlertHandlers();
            this.setupNavbarHiding();
            this.setupAccessibility();
        },

        setupSmoothScroll() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        const offset = CONFIG.SCROLL_OFFSET;
                        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                        window.scrollTo({
                            top: targetPosition,
                            behavior: 'smooth'
                        });
                    }
                });
            });
        },

        setupLazyLoading() {
            const lazyImages = document.querySelectorAll('img[data-lazy]');
            
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.lazy;
                            img.removeAttribute('data-lazy');
                            img.classList.add('loaded');
                            imageObserver.unobserve(img);
                        }
                    });
                }, {
                    rootMargin: '50px 0px',
                    threshold: 0.01
                });
                
                lazyImages.forEach(img => imageObserver.observe(img));
            } else {
                // Fallback for browsers without IntersectionObserver
                lazyImages.forEach(img => {
                    img.src = img.dataset.lazy;
                    img.removeAttribute('data-lazy');
                });
            }
        },

        setupCardAnimations() {
            const appCards = document.querySelectorAll('.app-card');
            
            if ('IntersectionObserver' in window) {
                const cardObserver = new IntersectionObserver((entries) => {
                    entries.forEach((entry, index) => {
                        if (entry.isIntersecting) {
                            setTimeout(() => {
                                entry.target.style.setProperty('--card-index', index);
                                entry.target.classList.add('animate-in');
                            }, index * 50);
                            cardObserver.unobserve(entry.target);
                        }
                    });
                }, {
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                });
                
                appCards.forEach(card => {
                    card.style.opacity = '0';
                    cardObserver.observe(card);
                });
            }
        },

        setupAlertHandlers() {
            document.querySelectorAll('.alert-close').forEach(button => {
                button.addEventListener('click', function() {
                    const alert = this.parentElement;
                    alert.style.animation = 'slideOutRight 0.3s ease';
                    setTimeout(() => alert.remove(), 300);
                });
            });
            
            // Auto-dismiss after 5 seconds
            document.querySelectorAll('.alert').forEach(alert => {
                setTimeout(() => {
                    if (alert && alert.parentNode) {
                        alert.style.animation = 'slideOutRight 0.3s ease';
                        setTimeout(() => alert.remove(), 300);
                    }
                }, 5000);
            });
        },

        setupNavbarHiding() {
            let lastScrollTop = 0;
            let scrollTimer;
            
            window.addEventListener('scroll', () => {
                if (!AppState.isMobile) return;
                
                clearTimeout(scrollTimer);
                scrollTimer = setTimeout(() => {
                    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                    
                    if (scrollTop > lastScrollTop && scrollTop > 100) {
                        // Scrolling down
                        Elements.navbar.style.transform = 'translateY(-100%)';
                    } else {
                        // Scrolling up
                        Elements.navbar.style.transform = 'translateY(0)';
                    }
                    
                    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
                }, 50);
            });
        },

        setupAccessibility() {
            // Add skip link
            const skipLink = document.createElement('a');
            skipLink.href = '#mainContent';
            skipLink.className = 'skip-link';
            skipLink.textContent = 'Skip to main content';
            Elements.body.insertBefore(skipLink, Elements.body.firstChild);
            
            // Ensure all images have alt text
            document.querySelectorAll('img:not([alt])').forEach(img => {
                img.setAttribute('alt', '');
            });
            
            // Add ARIA labels where needed
            Elements.menuToggle?.setAttribute('aria-label', 'Toggle navigation menu');
            Elements.themeToggle?.setAttribute('aria-label', 'Toggle theme');
            
            // Handle focus styles
            document.addEventListener('mousedown', () => {
                Elements.body.classList.add('using-mouse');
            });
            
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    Elements.body.classList.remove('using-mouse');
                }
            });
        }
    };

    // ===========================================
    // App Features
    // ===========================================
    
    const AppFeatures = {
        init() {
            this.setupReviews();
            this.setupShareButton();
            this.setupReadMore();
            this.setupScreenshotCarousel();
            this.setupNumberFormatting();
        },

        setupReviews() {
            const reviewModal = document.getElementById('reviewModal');
            const reviewForm = document.getElementById('reviewForm');
            const starRating = document.querySelectorAll('.star-rating i');
            let selectedRating = 0;
            
            // Star rating interaction
            starRating.forEach((star, index) => {
                star.addEventListener('click', () => {
                    selectedRating = index + 1;
                    this.updateStars(starRating, selectedRating);
                });
                
                star.addEventListener('mouseenter', () => {
                    this.updateStars(starRating, index + 1);
                });
            });
            
            document.querySelector('.star-rating')?.addEventListener('mouseleave', () => {
                this.updateStars(starRating, selectedRating);
            });
            
            // Review form submission
            reviewForm?.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                if (selectedRating === 0) {
                    alert('Please select a rating');
                    return;
                }
                
                const comment = document.getElementById('reviewComment')?.value;
                const appId = window.location.pathname.split('/').pop();
                
                try {
                    const response = await fetch(`/api/review/${appId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            rating: selectedRating,
                            comment: comment
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        this.showNotification('Review submitted successfully!', 'success');
                        if (reviewModal) reviewModal.style.display = 'none';
                        setTimeout(() => location.reload(), 1500);
                    } else {
                        this.showNotification('Error submitting review', 'error');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    this.showNotification('Error submitting review', 'error');
                }
            });
        },

        updateStars(stars, rating) {
            stars.forEach((star, index) => {
                if (index < rating) {
                    star.classList.remove('far');
                    star.classList.add('fas', 'active');
                } else {
                    star.classList.remove('fas', 'active');
                    star.classList.add('far');
                }
            });
        },

        setupShareButton() {
            document.querySelector('.share-btn')?.addEventListener('click', async () => {
                if (navigator.share) {
                    try {
                        await navigator.share({
                            title: document.title,
                            url: window.location.href
                        });
                    } catch (err) {
                        if (err.name !== 'AbortError') {
                            console.log('Error sharing:', err);
                        }
                    }
                } else {
                    // Fallback: copy to clipboard
                    navigator.clipboard.writeText(window.location.href);
                    this.showNotification('Link copied to clipboard!', 'success');
                }
            });
        },

        setupReadMore() {
            const readMoreBtn = document.querySelector('.read-more-btn');
            const aboutContent = document.querySelector('.about-content p');
            
            readMoreBtn?.addEventListener('click', function() {
                if (aboutContent.style.maxHeight === 'none') {
                    aboutContent.style.maxHeight = '100px';
                    aboutContent.style.overflow = 'hidden';
                    this.textContent = 'Read more';
                } else {
                    aboutContent.style.maxHeight = 'none';
                    aboutContent.style.overflow = 'visible';
                    this.textContent = 'Read less';
                }
            });
        },

        setupScreenshotCarousel() {
            const carousel = document.querySelector('.screenshots-carousel');
            if (!carousel) return;
            
            let isDown = false;
            let startX;
            let scrollLeft;
            
            carousel.addEventListener('mousedown', (e) => {
                isDown = true;
                carousel.style.cursor = 'grabbing';
                startX = e.pageX - carousel.offsetLeft;
                scrollLeft = carousel.scrollLeft;
            });
            
            carousel.addEventListener('mouseleave', () => {
                isDown = false;
                carousel.style.cursor = 'grab';
            });
            
            carousel.addEventListener('mouseup', () => {
                isDown = false;
                carousel.style.cursor = 'grab';
            });
            
            carousel.addEventListener('mousemove', (e) => {
                if (!isDown) return;
                e.preventDefault();
                const x = e.pageX - carousel.offsetLeft;
                const walk = (x - startX) * 2;
                carousel.scrollLeft = scrollLeft - walk;
            });
        },

        setupNumberFormatting() {
            function formatNumber(num) {
                if (num >= 1000000) {
                    return (num / 1000000).toFixed(1) + 'M';
                } else if (num >= 1000) {
                    return (num / 1000).toFixed(1) + 'K';
                }
                return num.toString();
            }
            
            document.querySelectorAll('.stat-value').forEach(elem => {
                const text = elem.textContent;
                const num = parseInt(text.replace(/,/g, ''));
                if (!isNaN(num) && num > 999) {
                    elem.textContent = formatNumber(num);
                }
            });
        },

        showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type}`;
            notification.innerHTML = `
                ${message}
                <button class="alert-close">&times;</button>
            `;
            
            const container = document.querySelector('.flash-messages') || (() => {
                const div = document.createElement('div');
                div.className = 'flash-messages';
                Elements.mainContent?.prepend(div);
                return div;
            })();
            
            container.appendChild(notification);
            
            notification.querySelector('.alert-close')?.addEventListener('click', () => {
                notification.remove();
            });
            
            setTimeout(() => {
                notification.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 5000);
        }
    };

    // ===========================================
    // Initialization
    // ===========================================
    
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initialize);
        } else {
            initialize();
        }
    }

    function initialize() {
        console.log('🚀 Enhanced App Store initializing...');
        
        // Initialize elements
        initializeElements();
        
        // Apply theme immediately (before other initializations)
        ThemeManager.init();
        
        // Initialize core features
        SidebarManager.init();
        CommandPalette.init();
        
        // Initialize UX enhancements
        UXEnhancements.init();
        
        // Initialize app features
        AppFeatures.init();
        
        // Mark as loaded
        Elements.body?.classList.add('loaded');
        
        console.log('✅ Enhanced App Store ready!');
    }

    // Start the app
    init();

    // Expose API for debugging
    window.AppStore = {
        state: AppState,
        theme: ThemeManager,
        sidebar: SidebarManager,
        commandPalette: CommandPalette,
        version: '2.0.0'
    };

})();
