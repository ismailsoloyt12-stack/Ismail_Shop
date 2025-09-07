// Enhanced Review System with Netlify Forms Integration
// This script handles all review functionality including submission, storage, and real-time display

class ReviewSystem {
    constructor(appId) {
        this.appId = appId;
        this.reviews = [];
        this.currentRating = 5;
        this.init();
    }

    init() {
        this.loadReviews();
        this.setupEventListeners();
        this.initializeForm();
        this.fetchNetlifyReviews();
    }

    // Setup all event listeners
    setupEventListeners() {
        // Open review modal button
        const writeReviewBtn = document.querySelector('.write-review-btn');
        if (writeReviewBtn) {
            writeReviewBtn.addEventListener('click', () => this.openReviewModal());
        }

        // Close modal buttons
        const closeBtn = document.querySelector('.close-modal');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeReviewModal());
        }

        // Star rating interaction
        const stars = document.querySelectorAll('.star-icon');
        stars.forEach((star, index) => {
            star.addEventListener('click', () => this.setRating(index + 1));
            star.addEventListener('mouseenter', () => this.previewRating(index + 1));
        });

        const starsContainer = document.querySelector('.stars-container');
        if (starsContainer) {
            starsContainer.addEventListener('mouseleave', () => this.updateStarDisplay(this.currentRating));
        }

        // Character counter
        const textarea = document.getElementById('review_comment');
        if (textarea) {
            textarea.addEventListener('input', (e) => {
                document.getElementById('charCount').textContent = e.target.value.length;
            });
        }

        // Form submission
        const form = document.getElementById('reviewForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Close modals on outside click
        window.addEventListener('click', (e) => {
            const reviewModal = document.getElementById('reviewModal');
            const successModal = document.getElementById('reviewSuccessModal');
            
            if (e.target === reviewModal) {
                this.closeReviewModal();
            }
            if (e.target === successModal) {
                this.closeSuccessModal();
            }
        });
    }

    // Initialize form
    initializeForm() {
        this.updateStarDisplay(5);
        document.getElementById('rating').value = 5;
        
        // Add form validation
        const form = document.getElementById('reviewForm');
        if (form) {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            inputs.forEach(input => {
                input.addEventListener('invalid', (e) => {
                    e.preventDefault();
                    this.showFieldError(input);
                });
                input.addEventListener('input', () => {
                    this.clearFieldError(input);
                });
            });
        }
    }

    // Open review modal
    openReviewModal() {
        const modal = document.getElementById('reviewModal');
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
            
            // Animate modal entrance
            setTimeout(() => {
                modal.querySelector('.review-modal-content').style.transform = 'scale(1)';
                modal.querySelector('.review-modal-content').style.opacity = '1';
            }, 10);
        }
    }

    // Close review modal
    closeReviewModal() {
        const modal = document.getElementById('reviewModal');
        if (modal) {
            modal.querySelector('.review-modal-content').style.transform = 'scale(0.95)';
            modal.querySelector('.review-modal-content').style.opacity = '0';
            
            setTimeout(() => {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
                this.resetForm();
            }, 300);
        }
    }

    // Reset form
    resetForm() {
        const form = document.getElementById('reviewForm');
        if (form) {
            form.reset();
            document.getElementById('charCount').textContent = '0';
            this.setRating(5);
            this.clearAllFieldErrors();
        }
    }

    // Set rating
    setRating(rating) {
        this.currentRating = rating;
        document.getElementById('rating').value = rating;
        this.updateStarDisplay(rating);
        this.updateRatingText(rating);
    }

    // Preview rating on hover
    previewRating(rating) {
        this.updateStarDisplay(rating);
        this.updateRatingText(rating);
    }

    // Update star display
    updateStarDisplay(rating) {
        const stars = document.querySelectorAll('.star-icon');
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('active');
                star.style.transform = 'scale(1.1)';
            } else {
                star.classList.remove('active');
                star.style.transform = 'scale(1)';
            }
        });
    }

    // Update rating text
    updateRatingText(rating) {
        const ratingText = document.querySelector('.rating-text');
        if (ratingText) {
            const texts = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
            ratingText.textContent = texts[rating];
            
            // Update color based on rating
            const colors = ['', '#f44336', '#ff9800', '#ffc107', '#8bc34a', '#4caf50'];
            ratingText.style.color = colors[rating];
        }
    }

    // Handle form submission
    async handleFormSubmit(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        
        // Show loading state
        const submitBtn = form.querySelector('.btn-submit');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
        submitBtn.disabled = true;
        
        try {
            // Create review object
            const review = {
                app_id: this.appId,
                reviewer_name: formData.get('reviewer_name'),
                reviewer_email: formData.get('reviewer_email'),
                rating: parseInt(formData.get('rating')),
                review_title: formData.get('review_title'),
                review_comment: formData.get('review_comment'),
                recommend: formData.get('recommend') === 'yes',
                created_at: new Date().toISOString()
            };
            
            // Save locally first for immediate display
            this.saveReviewLocally(review);
            
            // Submit to Netlify Forms (this happens in the background)
            const netlifyResponse = await fetch('/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(formData).toString()
            });
            
            // Also submit to our serverless function for persistent storage
            const apiResponse = await fetch('/api/reviews', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(review)
            });
            
            // Show success
            this.closeReviewModal();
            this.showSuccessModal();
            this.displayReview(review, true);
            this.updateOverallRating();
            
        } catch (error) {
            console.error('Error submitting review:', error);
            // Still show success if local save worked
            this.closeReviewModal();
            this.showSuccessModal();
            this.loadReviews();
        } finally {
            // Reset button state
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    // Save review locally
    saveReviewLocally(review) {
        const storageKey = `reviews_${this.appId}`;
        let reviews = JSON.parse(localStorage.getItem(storageKey) || '[]');
        reviews.unshift(review);
        localStorage.setItem(storageKey, JSON.stringify(reviews));
        this.reviews = reviews;
    }

    // Load reviews
    loadReviews() {
        const reviewsList = document.getElementById('reviewsList');
        if (!reviewsList) return;
        
        // Get local reviews
        const storageKey = `reviews_${this.appId}`;
        const localReviews = JSON.parse(localStorage.getItem(storageKey) || '[]');
        
        // Combine with any existing reviews
        this.reviews = localReviews;
        
        if (this.reviews.length === 0) {
            reviewsList.innerHTML = `
                <div class="no-reviews">
                    <i class="fas fa-comment-slash"></i>
                    <p>No reviews yet. Be the first to review!</p>
                    <button class="btn-primary" onclick="reviewSystem.openReviewModal()">
                        <i class="fas fa-edit"></i> Write the First Review
                    </button>
                </div>
            `;
        } else {
            reviewsList.innerHTML = '';
            this.reviews.slice(0, 10).forEach(review => {
                this.displayReview(review);
            });
        }
    }

    // Fetch reviews from Netlify function
    async fetchNetlifyReviews() {
        try {
            const response = await fetch(`/api/reviews/${this.appId}`);
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.reviews.length > 0) {
                    // Merge with local reviews (avoiding duplicates)
                    const storageKey = `reviews_${this.appId}`;
                    const localReviews = JSON.parse(localStorage.getItem(storageKey) || '[]');
                    
                    const mergedReviews = this.mergeReviews(localReviews, data.reviews);
                    localStorage.setItem(storageKey, JSON.stringify(mergedReviews));
                    
                    this.loadReviews();
                }
            }
        } catch (error) {
            console.log('Could not fetch server reviews, using local storage');
        }
    }

    // Merge reviews avoiding duplicates
    mergeReviews(local, server) {
        const merged = [...local];
        const localIds = new Set(local.map(r => r.id || `${r.reviewer_name}_${r.created_at}`));
        
        server.forEach(review => {
            const reviewId = review.id || `${review.reviewer_name}_${review.created_at}`;
            if (!localIds.has(reviewId)) {
                merged.push(review);
            }
        });
        
        // Sort by date
        merged.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        
        return merged;
    }

    // Display a single review
    displayReview(review, prepend = false) {
        const reviewsList = document.getElementById('reviewsList');
        if (!reviewsList) return;
        
        // Remove "no reviews" message if it exists
        const noReviews = reviewsList.querySelector('.no-reviews');
        if (noReviews) {
            noReviews.remove();
        }
        
        const date = new Date(review.created_at || Date.now());
        const formattedDate = date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
        
        const userName = review.reviewer_name || 'Anonymous';
        const initial = userName.charAt(0).toUpperCase();
        
        const reviewHTML = document.createElement('div');
        reviewHTML.className = 'review-item';
        reviewHTML.style.animation = prepend ? 'slideInNew 0.5s ease' : 'slideIn 0.5s ease';
        
        reviewHTML.innerHTML = `
            <div class="review-header">
                <div class="reviewer-info">
                    <div class="reviewer-avatar" style="background: ${this.getAvatarColor(userName)}">
                        ${initial}
                    </div>
                    <div class="reviewer-details">
                        <h4>${userName}</h4>
                        <span class="review-date">${formattedDate}</span>
                        ${review.verified ? '<span class="verified-badge"><i class="fas fa-check-circle"></i> Verified</span>' : ''}
                    </div>
                </div>
                <div class="review-rating">
                    ${this.generateStars(review.rating)}
                </div>
            </div>
            ${review.review_title ? `<div class="review-title">${review.review_title}</div>` : ''}
            <p class="review-comment">${review.review_comment}</p>
            <div class="review-footer">
                ${review.recommend ? `
                    <span class="review-recommended">
                        <i class="fas fa-thumbs-up"></i> Recommends this app
                    </span>
                ` : ''}
                <div class="review-actions">
                    <button class="helpful-btn" onclick="reviewSystem.markHelpful('${review.id || Date.now()}')">
                        <i class="far fa-thumbs-up"></i> Helpful (${review.helpful_count || 0})
                    </button>
                </div>
            </div>
        `;
        
        if (prepend) {
            reviewsList.prepend(reviewHTML);
        } else {
            reviewsList.appendChild(reviewHTML);
        }
    }

    // Generate star HTML
    generateStars(rating) {
        let stars = '';
        for (let i = 0; i < 5; i++) {
            stars += `<i class="${i < rating ? 'fas' : 'far'} fa-star"></i>`;
        }
        return stars;
    }

    // Get avatar color based on name
    getAvatarColor(name) {
        const colors = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
        ];
        
        let hash = 0;
        for (let i = 0; i < name.length; i++) {
            hash = name.charCodeAt(i) + ((hash << 5) - hash);
        }
        
        return colors[Math.abs(hash) % colors.length];
    }

    // Mark review as helpful
    markHelpful(reviewId) {
        const storageKey = `helpful_${this.appId}_${reviewId}`;
        if (localStorage.getItem(storageKey)) {
            this.showNotification('You have already marked this review as helpful');
            return;
        }
        
        localStorage.setItem(storageKey, 'true');
        
        // Update helpful count in local storage
        const reviewsKey = `reviews_${this.appId}`;
        let reviews = JSON.parse(localStorage.getItem(reviewsKey) || '[]');
        
        reviews = reviews.map(review => {
            if ((review.id || `${review.reviewer_name}_${review.created_at}`) === reviewId) {
                review.helpful_count = (review.helpful_count || 0) + 1;
            }
            return review;
        });
        
        localStorage.setItem(reviewsKey, JSON.stringify(reviews));
        
        // Update display
        this.loadReviews();
        this.showNotification('Thanks for your feedback!');
    }

    // Update overall rating
    updateOverallRating() {
        if (this.reviews.length === 0) return;
        
        const totalRating = this.reviews.reduce((sum, review) => sum + (review.rating || 5), 0);
        const avgRating = (totalRating / this.reviews.length).toFixed(1);
        
        // Update rating display
        const ratingNumber = document.querySelector('.rating-number');
        const reviewCount = document.querySelector('.review-count');
        
        if (ratingNumber) ratingNumber.textContent = avgRating;
        if (reviewCount) reviewCount.textContent = `${this.reviews.length} reviews`;
        
        // Update stars
        const starsContainer = document.querySelector('.stars-large');
        if (starsContainer) {
            const fullStars = Math.floor(avgRating);
            const hasHalfStar = avgRating % 1 >= 0.5;
            
            starsContainer.innerHTML = '';
            for (let i = 0; i < 5; i++) {
                if (i < fullStars) {
                    starsContainer.innerHTML += '<i class="fas fa-star"></i>';
                } else if (i === fullStars && hasHalfStar) {
                    starsContainer.innerHTML += '<i class="fas fa-star-half-alt"></i>';
                } else {
                    starsContainer.innerHTML += '<i class="far fa-star"></i>';
                }
            }
        }
    }

    // Show success modal
    showSuccessModal() {
        const modal = document.getElementById('reviewSuccessModal');
        if (modal) {
            modal.style.display = 'block';
            
            setTimeout(() => {
                this.closeSuccessModal();
            }, 3000);
        }
    }

    // Close success modal
    closeSuccessModal() {
        const modal = document.getElementById('reviewSuccessModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    // Show notification
    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    // Field validation helpers
    showFieldError(field) {
        field.classList.add('error');
        const errorMsg = document.createElement('span');
        errorMsg.className = 'field-error';
        errorMsg.textContent = field.validationMessage || 'This field is required';
        field.parentElement.appendChild(errorMsg);
    }

    clearFieldError(field) {
        field.classList.remove('error');
        const errorMsg = field.parentElement.querySelector('.field-error');
        if (errorMsg) errorMsg.remove();
    }

    clearAllFieldErrors() {
        document.querySelectorAll('.field-error').forEach(error => error.remove());
        document.querySelectorAll('.error').forEach(field => field.classList.remove('error'));
    }
}

// Add required styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInNew {
        from {
            opacity: 0;
            transform: translateY(-20px);
            background: #fffbf0;
        }
        to {
            opacity: 1;
            transform: translateY(0);
            background: #f9f9f9;
        }
    }

    .review-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 15px;
    }

    .review-actions {
        display: flex;
        gap: 10px;
    }

    .helpful-btn {
        background: none;
        border: 1px solid #ddd;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        color: #666;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .helpful-btn:hover {
        background: #f0f0f0;
        border-color: #667eea;
        color: #667eea;
    }

    .verified-badge {
        color: #4caf50;
        font-size: 12px;
        margin-left: 8px;
    }

    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        gap: 10px;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        z-index: 10003;
    }

    .notification.show {
        transform: translateX(0);
    }

    .notification.success {
        border-left: 4px solid #4caf50;
    }

    .notification.error {
        border-left: 4px solid #f44336;
    }

    .field-error {
        color: #f44336;
        font-size: 12px;
        margin-top: 5px;
        display: block;
    }

    input.error, textarea.error {
        border-color: #f44336 !important;
    }

    .no-reviews .btn-primary {
        margin-top: 20px;
    }
`;
document.head.appendChild(style);

// Initialize review system when DOM is ready
let reviewSystem;
document.addEventListener('DOMContentLoaded', function() {
    // Get app ID from the page (you'll need to set this in your template)
    const appIdElement = document.querySelector('[data-app-id]');
    const appId = appIdElement ? appIdElement.dataset.appId : 'default';
    
    reviewSystem = new ReviewSystem(appId);
});
