// Wishlist System
// This script handles adding/removing apps to/from user's wishlist

class WishlistManager {
    constructor() {
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.updateWishlistButtons();
    }

    attachEventListeners() {
        // Attach click event to all wishlist buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('wishlist-btn') || e.target.closest('.wishlist-btn')) {
                e.preventDefault();
                const button = e.target.classList.contains('wishlist-btn') ? e.target : e.target.closest('.wishlist-btn');
                this.handleWishlistToggle(button);
            }
        });
    }

    async handleWishlistToggle(button) {
        const appId = button.dataset.appId;
        const isInWishlist = button.classList.contains('in-wishlist');
        
        // Check if user is logged in
        if (!window.currentUser || !window.currentUser.id) {
            this.showLoginPrompt();
            return;
        }

        // Disable button during request
        button.disabled = true;
        button.classList.add('loading');

        try {
            const endpoint = isInWishlist ? 
                `/api/wishlist/remove/${appId}` : 
                `/api/wishlist/add/${appId}`;

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            });

            const data = await response.json();

            if (data.success) {
                // Update button state
                if (isInWishlist) {
                    this.removeFromWishlistUI(button, appId);
                    this.showMessage('Removed from wishlist', 'info');
                } else {
                    this.addToWishlistUI(button, appId);
                    this.showMessage('Added to wishlist!', 'success');
                }
                
                // Update wishlist counter
                this.updateWishlistCounter(isInWishlist ? -1 : 1);
                
                // Animate button
                this.animateButton(button);
            } else {
                this.showMessage(data.message || 'Unable to update wishlist', 'error');
            }
        } catch (error) {
            console.error('Error updating wishlist:', error);
            this.showMessage('Connection error. Please try again.', 'error');
        } finally {
            button.disabled = false;
            button.classList.remove('loading');
        }
    }

    addToWishlistUI(button, appId) {
        button.classList.add('in-wishlist');
        
        // Update button text and icon
        const icon = button.querySelector('.wishlist-icon');
        const text = button.querySelector('.wishlist-text');
        
        if (icon) {
            icon.className = 'fas fa-heart wishlist-icon';
        }
        if (text) {
            text.textContent = 'In Wishlist';
        }

        // Update tooltip
        button.title = 'Remove from Wishlist';

        // Add to local storage for persistence
        this.updateLocalWishlist(appId, true);
    }

    removeFromWishlistUI(button, appId) {
        button.classList.remove('in-wishlist');
        
        // Update button text and icon
        const icon = button.querySelector('.wishlist-icon');
        const text = button.querySelector('.wishlist-text');
        
        if (icon) {
            icon.className = 'far fa-heart wishlist-icon';
        }
        if (text) {
            text.textContent = 'Add to Wishlist';
        }

        // Update tooltip
        button.title = 'Add to Wishlist';

        // Remove from local storage
        this.updateLocalWishlist(appId, false);

        // If we're on the wishlist page, remove the entire app card
        if (window.location.pathname.includes('/wishlist')) {
            const appCard = button.closest('.app-card');
            if (appCard) {
                this.removeAppCard(appCard);
            }
        }
    }

    removeAppCard(appCard) {
        appCard.style.transform = 'scale(0.9)';
        appCard.style.opacity = '0';
        
        setTimeout(() => {
            appCard.remove();
            this.checkEmptyWishlist();
        }, 300);
    }

    checkEmptyWishlist() {
        const wishlistContainer = document.querySelector('.wishlist-apps');
        if (wishlistContainer && wishlistContainer.children.length === 0) {
            this.showEmptyWishlistMessage();
        }
    }

    showEmptyWishlistMessage() {
        const container = document.querySelector('.wishlist-apps');
        if (container) {
            container.innerHTML = `
                <div class="empty-wishlist">
                    <i class="fas fa-heart-broken fa-3x mb-3 text-muted"></i>
                    <h4>Your wishlist is empty</h4>
                    <p class="text-muted">Browse apps and add your favorites to your wishlist!</p>
                    <a href="/" class="btn btn-primary">Browse Apps</a>
                </div>
            `;
        }
    }

    animateButton(button) {
        // Pulse animation
        button.style.transform = 'scale(1.1)';
        button.style.transition = 'transform 0.2s ease';
        
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 200);

        // Heart animation for adding to wishlist
        if (button.classList.contains('in-wishlist')) {
            this.createHeartAnimation(button);
        }
    }

    createHeartAnimation(button) {
        const heart = document.createElement('div');
        heart.innerHTML = '❤️';
        heart.className = 'floating-heart';
        heart.style.position = 'absolute';
        heart.style.left = '50%';
        heart.style.top = '50%';
        heart.style.transform = 'translate(-50%, -50%)';
        heart.style.pointerEvents = 'none';
        heart.style.fontSize = '1.5rem';
        heart.style.zIndex = '1000';

        button.style.position = 'relative';
        button.appendChild(heart);

        // Animate the heart
        heart.animate([
            { transform: 'translate(-50%, -50%) scale(1)', opacity: 1 },
            { transform: 'translate(-50%, -200%) scale(0.5)', opacity: 0 }
        ], {
            duration: 1000,
            easing: 'ease-out'
        });

        // Remove the heart after animation
        setTimeout(() => {
            if (heart.parentNode) {
                heart.remove();
            }
        }, 1000);
    }

    updateWishlistButtons() {
        // Initialize button states based on user's wishlist
        const wishlistButtons = document.querySelectorAll('.wishlist-btn');
        const userWishlist = this.getUserWishlist();
        
        wishlistButtons.forEach(button => {
            const appId = button.dataset.appId;
            if (userWishlist.includes(appId)) {
                button.classList.add('in-wishlist');
                
                const icon = button.querySelector('.wishlist-icon');
                const text = button.querySelector('.wishlist-text');
                
                if (icon) {
                    icon.className = 'fas fa-heart wishlist-icon';
                }
                if (text) {
                    text.textContent = 'In Wishlist';
                }
                
                button.title = 'Remove from Wishlist';
            }
        });
    }

    getUserWishlist() {
        // This should ideally come from the server, but we can use localStorage as fallback
        const stored = localStorage.getItem('userWishlist');
        return stored ? JSON.parse(stored) : [];
    }

    updateLocalWishlist(appId, add) {
        let wishlist = this.getUserWishlist();
        
        if (add && !wishlist.includes(appId)) {
            wishlist.push(appId);
        } else if (!add) {
            wishlist = wishlist.filter(id => id !== appId);
        }
        
        localStorage.setItem('userWishlist', JSON.stringify(wishlist));
    }

    updateWishlistCounter(change) {
        const counter = document.querySelector('.wishlist-counter');
        if (counter) {
            let currentCount = parseInt(counter.textContent) || 0;
            currentCount += change;
            counter.textContent = Math.max(0, currentCount);
            
            // Animate counter
            counter.style.transform = 'scale(1.2)';
            setTimeout(() => {
                counter.style.transform = 'scale(1)';
            }, 200);
        }
    }

    showLoginPrompt() {
        const modal = document.createElement('div');
        modal.className = 'login-prompt-modal';
        modal.innerHTML = `
            <div class="login-prompt-content">
                <i class="fas fa-heart fa-2x text-primary mb-3"></i>
                <h4>Sign in to save favorites</h4>
                <p>Create an account or sign in to add apps to your wishlist and access them anywhere!</p>
                <div class="login-prompt-actions">
                    <a href="/login" class="btn btn-primary">Sign In</a>
                    <a href="/register" class="btn btn-outline-primary">Create Account</a>
                    <button class="btn btn-secondary" onclick="this.closest('.login-prompt-modal').remove()">Cancel</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
            }
        }, 10000);
    }

    showMessage(message, type = 'info') {
        // Create or update notification
        let notification = document.getElementById('wishlist-notification');
        
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'wishlist-notification';
            notification.className = 'wishlist-notification';
            document.body.appendChild(notification);
        }

        notification.textContent = message;
        notification.className = `wishlist-notification ${type} show`;

        // Auto hide after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    // Bulk operations for wishlist management
    async clearWishlist() {
        if (!confirm('Are you sure you want to remove all apps from your wishlist?')) {
            return;
        }

        const wishlistItems = document.querySelectorAll('.wishlist-btn.in-wishlist');
        const promises = [];

        for (const button of wishlistItems) {
            const appId = button.dataset.appId;
            promises.push(
                fetch(`/api/wishlist/remove/${appId}`, {
                    method: 'POST',
                    credentials: 'same-origin'
                })
            );
        }

        try {
            await Promise.all(promises);
            
            // Update UI
            wishlistItems.forEach(button => {
                const appId = button.dataset.appId;
                this.removeFromWishlistUI(button, appId);
            });
            
            this.showMessage('Wishlist cleared', 'success');
            
            if (window.location.pathname.includes('/wishlist')) {
                location.reload();
            }
        } catch (error) {
            this.showMessage('Error clearing wishlist', 'error');
        }
    }

    // Share wishlist functionality
    shareWishlist() {
        if (navigator.share) {
            navigator.share({
                title: 'My App Wishlist',
                text: 'Check out my app wishlist!',
                url: window.location.href
            });
        } else {
            // Fallback to copying URL
            navigator.clipboard.writeText(window.location.href).then(() => {
                this.showMessage('Wishlist URL copied to clipboard!', 'success');
            });
        }
    }
}

// Initialize wishlist manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.wishlistManager = new WishlistManager();
});

// Export for use in other scripts
window.WishlistManager = WishlistManager;
