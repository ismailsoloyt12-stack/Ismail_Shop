// Helpful Reviews System
// This script handles the voting functionality for marking reviews as helpful

class HelpfulReviews {
    constructor() {
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.updateButtonStates();
    }

    attachEventListeners() {
        // Attach click event to all helpful buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('helpful-btn') || e.target.closest('.helpful-btn')) {
                e.preventDefault();
                const button = e.target.classList.contains('helpful-btn') ? e.target : e.target.closest('.helpful-btn');
                this.handleHelpfulVote(button);
            }
        });
    }

    async handleHelpfulVote(button) {
        const reviewId = button.dataset.reviewId;
        const countElement = button.querySelector('.helpful-count');
        
        // Check if user is logged in
        if (!window.currentUser || !window.currentUser.id) {
            this.showMessage('Please log in to vote on reviews', 'error');
            return;
        }

        // Disable button during request
        button.disabled = true;
        button.classList.add('voting');

        try {
            const response = await fetch(`/api/review/helpful/${reviewId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            });

            const data = await response.json();

            if (data.success) {
                // Update count
                countElement.textContent = data.helpful_votes;
                
                // Mark as voted
                button.classList.add('voted');
                button.disabled = true;
                
                // Update button text
                const buttonText = button.querySelector('.helpful-text');
                if (buttonText) {
                    buttonText.textContent = 'Helpful ✓';
                }

                this.showMessage(data.message || 'Thank you for your feedback!', 'success');
                
                // Add animation
                this.animateVote(button);
            } else {
                this.showMessage(data.message || 'Unable to vote at this time', 'error');
            }
        } catch (error) {
            console.error('Error voting on review:', error);
            this.showMessage('Connection error. Please try again.', 'error');
        } finally {
            button.disabled = data.success;
            button.classList.remove('voting');
        }
    }

    animateVote(button) {
        // Add pulse animation
        button.style.transform = 'scale(1.1)';
        button.style.transition = 'transform 0.2s ease';
        
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 200);

        // Add color flash
        const originalColor = button.style.backgroundColor;
        button.style.backgroundColor = '#4CAF50';
        
        setTimeout(() => {
            button.style.backgroundColor = originalColor;
        }, 500);
    }

    updateButtonStates() {
        // Update button states based on user voting history
        // This would typically check against a user's voting history
        const helpfulButtons = document.querySelectorAll('.helpful-btn');
        
        helpfulButtons.forEach(button => {
            const reviewId = button.dataset.reviewId;
            
            // Check if user has already voted (this could be passed from server)
            if (window.userVotedReviews && window.userVotedReviews.includes(reviewId)) {
                button.classList.add('voted');
                button.disabled = true;
                
                const buttonText = button.querySelector('.helpful-text');
                if (buttonText) {
                    buttonText.textContent = 'Helpful ✓';
                }
            }
        });
    }

    showMessage(message, type = 'info') {
        // Create or update notification
        let notification = document.getElementById('helpful-notification');
        
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'helpful-notification';
            notification.className = 'helpful-notification';
            document.body.appendChild(notification);
        }

        notification.textContent = message;
        notification.className = `helpful-notification ${type} show`;

        // Auto hide after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    // Sort reviews by helpfulness
    sortReviewsByHelpfulness() {
        const reviewsContainer = document.querySelector('.reviews-list');
        if (!reviewsContainer) return;

        const reviews = Array.from(reviewsContainer.querySelectorAll('.review-item'));
        
        reviews.sort((a, b) => {
            const aVotes = parseInt(a.querySelector('.helpful-count')?.textContent || 0);
            const bVotes = parseInt(b.querySelector('.helpful-count')?.textContent || 0);
            return bVotes - aVotes; // Sort descending by helpful votes
        });

        // Reorder in DOM
        reviews.forEach(review => {
            reviewsContainer.appendChild(review);
        });
    }
}

// Initialize helpful reviews system when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.helpfulReviews = new HelpfulReviews();
    
    // Add sort button for reviews if there are multiple reviews
    const reviewsContainer = document.querySelector('.reviews-list');
    if (reviewsContainer && reviewsContainer.children.length > 1) {
        addSortButton();
    }
});

function addSortButton() {
    const reviewsHeader = document.querySelector('.reviews-header');
    if (reviewsHeader && !document.getElementById('sort-reviews-btn')) {
        const sortButton = document.createElement('button');
        sortButton.id = 'sort-reviews-btn';
        sortButton.className = 'sort-reviews-btn';
        sortButton.innerHTML = '<i class="fas fa-sort"></i> Sort by Helpfulness';
        
        sortButton.addEventListener('click', () => {
            window.helpfulReviews.sortReviewsByHelpfulness();
            sortButton.textContent = '✓ Sorted by Helpfulness';
            sortButton.disabled = true;
        });
        
        reviewsHeader.appendChild(sortButton);
    }
}
