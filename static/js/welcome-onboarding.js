// Welcome Notification and Onboarding Tour System
// Professional implementation with sound effects and smooth animations

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        NOTIFICATION_DURATION: 6000, // 6 seconds
        NOTIFICATION_SOUND_VOLUME: 0.3,
        TYPING_SPEED: 50, // ms per character
        AUTO_NEXT_DELAY: 5000, // 5 seconds for auto-advance
        LOCAL_STORAGE_KEY: 'ismailStore_userState',
        ANIMATION_DURATION: 300
    };

    // User state management
    const UserState = {
        isNewUser: true,
        hasSeenWelcome: false,
        hasCompletedTour: false,
        tourStep: 0,
        
        load() {
            const saved = localStorage.getItem(CONFIG.LOCAL_STORAGE_KEY);
            if (saved) {
                const state = JSON.parse(saved);
                Object.assign(this, state);
            }
        },
        
        save() {
            localStorage.setItem(CONFIG.LOCAL_STORAGE_KEY, JSON.stringify({
                isNewUser: this.isNewUser,
                hasSeenWelcome: this.hasSeenWelcome,
                hasCompletedTour: this.hasCompletedTour,
                tourStep: this.tourStep
            }));
        },
        
        markWelcomeShown() {
            this.hasSeenWelcome = true;
            this.save();
        },
        
        markTourCompleted() {
            this.hasCompletedTour = true;
            this.isNewUser = false;
            this.save();
        },
        
        skipTour() {
            this.hasCompletedTour = true;
            this.isNewUser = false;
            this.save();
        }
    };

    // Welcome Notification System
    const WelcomeNotification = {
        audioContext: null,
        
        init() {
            if (!UserState.hasSeenWelcome) {
                setTimeout(() => this.show(), 1000);
            }
        },
        
        createSound() {
            try {
                // Create Web Audio API context
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                
                // Create a pleasant notification sound
                const duration = 0.5;
                const oscillator = this.audioContext.createOscillator();
                const gainNode = this.audioContext.createGain();
                
                oscillator.connect(gainNode);
                gainNode.connect(this.audioContext.destination);
                
                // Create a pleasant chime sound
                oscillator.frequency.setValueAtTime(523.25, this.audioContext.currentTime); // C5
                oscillator.frequency.exponentialRampToValueAtTime(659.25, this.audioContext.currentTime + 0.1); // E5
                oscillator.frequency.exponentialRampToValueAtTime(783.99, this.audioContext.currentTime + 0.2); // G5
                
                gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
                gainNode.gain.linearRampToValueAtTime(CONFIG.NOTIFICATION_SOUND_VOLUME, this.audioContext.currentTime + 0.1);
                gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
                
                oscillator.start(this.audioContext.currentTime);
                oscillator.stop(this.audioContext.currentTime + duration);
            } catch (e) {
                console.log('Audio not supported:', e);
            }
        },
        
        show() {
            const notification = this.createElement();
            document.body.appendChild(notification);
            
            // Play sound
            this.createSound();
            
            // Animate in
            requestAnimationFrame(() => {
                notification.classList.add('show');
            });
            
            // Auto-hide after duration
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => {
                    notification.remove();
                    // Show onboarding after notification
                    if (!UserState.hasCompletedTour) {
                        OnboardingTour.init();
                    }
                }, CONFIG.ANIMATION_DURATION);
            }, CONFIG.NOTIFICATION_DURATION);
            
            UserState.markWelcomeShown();
        },
        
        createElement() {
            const notification = document.createElement('div');
            notification.className = 'welcome-notification';
            notification.innerHTML = `
                <div class="notification-content">
                    <div class="notification-icon">
                        <i class="fas fa-gift"></i>
                    </div>
                    <div class="notification-text">
                        <h3>Welcome to Ismail Store!</h3>
                        <p>We're glad to have you here 🎉</p>
                    </div>
                    <button class="notification-close" aria-label="Close notification">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="notification-progress"></div>
            `;
            
            // Close button handler
            notification.querySelector('.notification-close').addEventListener('click', () => {
                notification.classList.remove('show');
                setTimeout(() => notification.remove(), CONFIG.ANIMATION_DURATION);
            });
            
            return notification;
        }
    };

    // Onboarding Tour System
    const OnboardingTour = {
        currentStep: 0,
        overlay: null,
        tooltip: null,
        autoNextTimer: null,
        
        tourSteps: [
            {
                selector: '.logo',
                title: 'Welcome to Ismail Store',
                content: 'Your destination for amazing apps and games. Let\'s take a quick tour!',
                position: 'bottom',
                highlight: 'pulse'
            },
            {
                selector: '.search-box',
                title: 'Search Everything',
                content: 'Find your favorite apps and games instantly with our powerful search.',
                position: 'bottom',
                highlight: 'circle'
            },
            {
                selector: '.sidebar-menu',
                title: 'Browse Categories',
                content: 'Explore different categories to discover new apps tailored to your interests.',
                position: 'right',
                highlight: 'glow'
            },
            {
                selector: '.theme-toggle',
                title: 'Dark Mode',
                content: 'Switch between light and dark themes for comfortable viewing anytime.',
                position: 'bottom',
                highlight: 'circle'
            },
            {
                selector: '.user-menu, .login-btn',
                title: 'Your Account',
                content: 'Sign in to save favorites, track downloads, and get personalized recommendations.',
                position: 'bottom',
                highlight: 'circle'
            },
            {
                selector: '.premium-link',
                title: 'Premium Unlocked',
                content: 'Access exclusive premium apps with all features unlocked!',
                position: 'right',
                highlight: 'glow'
            }
        ],
        
        init() {
            this.currentStep = UserState.tourStep || 0;
            this.showWelcomeScreen();
        },
        
        showWelcomeScreen() {
            const welcomeScreen = document.createElement('div');
            welcomeScreen.className = 'onboarding-welcome';
            welcomeScreen.innerHTML = `
                <div class="onboarding-welcome-content">
                    <div class="welcome-animation">
                        <i class="fas fa-compass"></i>
                    </div>
                    <h2>Ready to explore?</h2>
                    <p>Take a quick tour to discover all the amazing features</p>
                    <div class="welcome-actions">
                        <button class="btn-primary" id="startTour">
                            <i class="fas fa-play"></i>
                            Start the Journey
                        </button>
                        <button class="btn-secondary" id="skipTour">
                            Skip
                        </button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(welcomeScreen);
            
            // Animate in
            requestAnimationFrame(() => {
                welcomeScreen.classList.add('show');
            });
            
            // Button handlers
            document.getElementById('startTour').addEventListener('click', () => {
                welcomeScreen.classList.remove('show');
                setTimeout(() => {
                    welcomeScreen.remove();
                    this.start();
                }, CONFIG.ANIMATION_DURATION);
            });
            
            document.getElementById('skipTour').addEventListener('click', () => {
                welcomeScreen.classList.remove('show');
                setTimeout(() => {
                    welcomeScreen.remove();
                    UserState.skipTour();
                }, CONFIG.ANIMATION_DURATION);
            });
        },
        
        start() {
            this.createOverlay();
            this.createTooltip();
            this.showStep(this.currentStep);
        },
        
        createOverlay() {
            this.overlay = document.createElement('div');
            this.overlay.className = 'tour-overlay';
            document.body.appendChild(this.overlay);
            
            // Skip tour on overlay click
            this.overlay.addEventListener('click', (e) => {
                if (e.target === this.overlay) {
                    this.skip();
                }
            });
        },
        
        createTooltip() {
            this.tooltip = document.createElement('div');
            this.tooltip.className = 'tour-tooltip';
            document.body.appendChild(this.tooltip);
        },
        
        showStep(stepIndex) {
            if (stepIndex >= this.tourSteps.length) {
                this.complete();
                return;
            }
            
            const step = this.tourSteps[stepIndex];
            const element = document.querySelector(step.selector);
            
            if (!element) {
                // Skip to next step if element not found
                this.nextStep();
                return;
            }
            
            // Update user state
            UserState.tourStep = stepIndex;
            UserState.save();
            
            // Highlight element with step info
            this.highlightElement(element, step);
            
            // Show tooltip with typing effect
            this.showTooltip(element, step);
            
            // Set up auto-advance
            this.setupAutoAdvance();
        },
        
        highlightElement(element, step) {
            // Remove previous highlights and markers
            document.querySelectorAll('.tour-highlight, .tour-circle-marker').forEach(el => {
                el.classList.remove('tour-highlight', 'tour-highlight-pulse', 'tour-highlight-glow');
                if (el.classList.contains('tour-circle-marker')) {
                    el.remove();
                }
            });
            
            // Add highlight class based on type
            const highlightType = step.highlight || 'circle';
            element.classList.add('tour-highlight');
            
            if (highlightType === 'pulse') {
                element.classList.add('tour-highlight-pulse');
            } else if (highlightType === 'glow') {
                element.classList.add('tour-highlight-glow');
            }
            
            // Create circle marker for circle type
            if (highlightType === 'circle') {
                const marker = document.createElement('div');
                marker.className = 'tour-circle-marker';
                document.body.appendChild(marker);
                
                // Position the circle marker
                const rect = element.getBoundingClientRect();
                const markerSize = Math.max(rect.width, rect.height) + 40;
                marker.style.width = `${markerSize}px`;
                marker.style.height = `${markerSize}px`;
                marker.style.top = `${rect.top + rect.height / 2 - markerSize / 2}px`;
                marker.style.left = `${rect.left + rect.width / 2 - markerSize / 2}px`;
            }
            
            // Scroll element into view
            element.scrollIntoView({
                behavior: 'smooth',
                block: 'center',
                inline: 'center'
            });
            
            // Update overlay to create spotlight effect
            const rect = element.getBoundingClientRect();
            this.overlay.style.setProperty('--highlight-top', `${rect.top - 20}px`);
            this.overlay.style.setProperty('--highlight-left', `${rect.left - 20}px`);
            this.overlay.style.setProperty('--highlight-width', `${rect.width + 40}px`);
            this.overlay.style.setProperty('--highlight-height', `${rect.height + 40}px`);
        },
        
        showTooltip(element, step) {
            const rect = element.getBoundingClientRect();
            
            // Update tooltip content
            this.tooltip.innerHTML = `
                <div class="tooltip-header">
                    <h3>${step.title}</h3>
                    <button class="tooltip-close" aria-label="Skip tour">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="tooltip-content">
                    <p class="typing-text" data-text="${step.content}"></p>
                </div>
                <div class="tooltip-footer">
                    <div class="tooltip-progress">
                        <span>${this.currentStep + 1} of ${this.tourSteps.length}</span>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${((this.currentStep + 1) / this.tourSteps.length) * 100}%"></div>
                        </div>
                    </div>
                    <div class="tooltip-actions">
                        ${this.currentStep > 0 ? '<button class="btn-back">Back</button>' : ''}
                        <button class="btn-next">
                            ${this.currentStep < this.tourSteps.length - 1 ? 'Next' : 'Finish'}
                        </button>
                    </div>
                </div>
            `;
            
            // Position tooltip
            this.positionTooltip(rect, step.position);
            
            // Start typing animation
            this.startTypingAnimation();
            
            // Button handlers
            const closeBtn = this.tooltip.querySelector('.tooltip-close');
            const nextBtn = this.tooltip.querySelector('.btn-next');
            const backBtn = this.tooltip.querySelector('.btn-back');
            
            closeBtn.addEventListener('click', () => this.skip());
            nextBtn.addEventListener('click', () => this.nextStep());
            if (backBtn) {
                backBtn.addEventListener('click', () => this.previousStep());
            }
            
            // Show tooltip
            requestAnimationFrame(() => {
                this.tooltip.classList.add('show');
            });
        },
        
        positionTooltip(elementRect, position) {
            const tooltipRect = this.tooltip.getBoundingClientRect();
            const spacing = 20;
            let top, left;
            
            // Calculate position based on preference and viewport
            switch (position) {
                case 'bottom':
                    top = elementRect.bottom + spacing;
                    left = elementRect.left + (elementRect.width - tooltipRect.width) / 2;
                    break;
                case 'top':
                    top = elementRect.top - tooltipRect.height - spacing;
                    left = elementRect.left + (elementRect.width - tooltipRect.width) / 2;
                    break;
                case 'right':
                    top = elementRect.top + (elementRect.height - tooltipRect.height) / 2;
                    left = elementRect.right + spacing;
                    break;
                case 'left':
                    top = elementRect.top + (elementRect.height - tooltipRect.height) / 2;
                    left = elementRect.left - tooltipRect.width - spacing;
                    break;
            }
            
            // Ensure tooltip stays within viewport
            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            
            if (left < spacing) left = spacing;
            if (left + tooltipRect.width > viewportWidth - spacing) {
                left = viewportWidth - tooltipRect.width - spacing;
            }
            
            if (top < spacing) top = spacing;
            if (top + tooltipRect.height > viewportHeight - spacing) {
                top = viewportHeight - tooltipRect.height - spacing;
            }
            
            this.tooltip.style.top = `${top}px`;
            this.tooltip.style.left = `${left}px`;
        },
        
        startTypingAnimation() {
            const textElement = this.tooltip.querySelector('.typing-text');
            const fullText = textElement.dataset.text;
            let currentIndex = 0;
            
            textElement.textContent = '';
            
            const typeInterval = setInterval(() => {
                if (currentIndex < fullText.length) {
                    textElement.textContent += fullText[currentIndex];
                    currentIndex++;
                } else {
                    clearInterval(typeInterval);
                }
            }, CONFIG.TYPING_SPEED);
        },
        
        setupAutoAdvance() {
            // Clear existing timer
            if (this.autoNextTimer) {
                clearTimeout(this.autoNextTimer);
            }
            
            // Set new timer
            this.autoNextTimer = setTimeout(() => {
                this.nextStep();
            }, CONFIG.AUTO_NEXT_DELAY);
        },
        
        nextStep() {
            this.clearAutoAdvance();
            this.tooltip.classList.remove('show');
            
            setTimeout(() => {
                this.currentStep++;
                this.showStep(this.currentStep);
            }, CONFIG.ANIMATION_DURATION);
        },
        
        previousStep() {
            this.clearAutoAdvance();
            this.tooltip.classList.remove('show');
            
            setTimeout(() => {
                this.currentStep--;
                this.showStep(this.currentStep);
            }, CONFIG.ANIMATION_DURATION);
        },
        
        skip() {
            this.clearAutoAdvance();
            UserState.skipTour();
            this.cleanup();
        },
        
        complete() {
            this.clearAutoAdvance();
            UserState.markTourCompleted();
            this.showCompletionMessage();
        },
        
        showCompletionMessage() {
            const completion = document.createElement('div');
            completion.className = 'tour-completion';
            completion.innerHTML = `
                <div class="completion-content">
                    <div class="completion-icon">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <h2>Tour Complete!</h2>
                    <p>You're all set to explore Ismail Store</p>
                    <button class="btn-primary" id="finishTour">
                        <i class="fas fa-rocket"></i>
                        Let's Go!
                    </button>
                </div>
            `;
            
            document.body.appendChild(completion);
            
            requestAnimationFrame(() => {
                completion.classList.add('show');
            });
            
            document.getElementById('finishTour').addEventListener('click', () => {
                completion.classList.remove('show');
                setTimeout(() => {
                    completion.remove();
                    this.cleanup();
                }, CONFIG.ANIMATION_DURATION);
            });
        },
        
        clearAutoAdvance() {
            if (this.autoNextTimer) {
                clearTimeout(this.autoNextTimer);
                this.autoNextTimer = null;
            }
        },
        
        cleanup() {
            // Remove highlights and markers
            document.querySelectorAll('.tour-highlight, .tour-circle-marker').forEach(el => {
                el.classList.remove('tour-highlight', 'tour-highlight-pulse', 'tour-highlight-glow');
                if (el.classList.contains('tour-circle-marker')) {
                    el.remove();
                }
            });
            
            // Remove overlay and tooltip
            if (this.overlay) {
                this.overlay.remove();
                this.overlay = null;
            }
            
            if (this.tooltip) {
                this.tooltip.remove();
                this.tooltip = null;
            }
        }
    };

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        // Load user state
        UserState.load();
        
        // Initialize welcome notification
        WelcomeNotification.init();
    }

    // Export for debugging
    window.IsmailStore = window.IsmailStore || {};
    window.IsmailStore.WelcomeOnboarding = {
        UserState,
        WelcomeNotification,
        OnboardingTour,
        resetUser() {
            localStorage.removeItem(CONFIG.LOCAL_STORAGE_KEY);
            location.reload();
        }
    };

})();
