// ==========================================
// PREMIUM CAROUSEL & INTERACTIONS SYSTEM
// ==========================================

class PremiumCarousel {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        
        this.wrapper = this.container.querySelector('.carousel-wrapper');
        this.items = this.wrapper ? this.wrapper.children : [];
        this.prevBtn = this.container.querySelector('.carousel-prev');
        this.nextBtn = this.container.querySelector('.carousel-next');
        
        // Configuration
        this.options = {
            itemsPerView: options.itemsPerView || 4,
            gap: options.gap || 20,
            autoplay: options.autoplay || false,
            autoplayDelay: options.autoplayDelay || 5000,
            loop: options.loop || false,
            responsive: options.responsive || {
                1200: { itemsPerView: 4 },
                992: { itemsPerView: 3 },
                768: { itemsPerView: 2 },
                480: { itemsPerView: 2 }
            }
        };
        
        this.currentIndex = 0;
        this.maxIndex = 0;
        this.autoplayTimer = null;
        this.isTransitioning = false;
        
        this.init();
    }
    
    init() {
        if (!this.wrapper || this.items.length === 0) return;
        
        this.updateResponsive();
        this.setupEventListeners();
        this.updateCarousel();
        
        if (this.options.autoplay) {
            this.startAutoplay();
        }
    }
    
    updateResponsive() {
        const width = window.innerWidth;
        const breakpoints = Object.keys(this.options.responsive).sort((a, b) => b - a);
        
        for (const breakpoint of breakpoints) {
            if (width <= parseInt(breakpoint)) {
                this.options.itemsPerView = this.options.responsive[breakpoint].itemsPerView;
            }
        }
        
        this.maxIndex = Math.max(0, this.items.length - this.options.itemsPerView);
    }
    
    setupEventListeners() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
        
        // Touch/Swipe support
        let touchStartX = 0;
        let touchEndX = 0;
        
        this.wrapper.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        this.wrapper.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe(touchStartX, touchEndX);
        }, { passive: true });
        
        // Mouse drag support
        let mouseDown = false;
        let startX = 0;
        let scrollLeft = 0;
        
        this.wrapper.addEventListener('mousedown', (e) => {
            mouseDown = true;
            startX = e.pageX - this.wrapper.offsetLeft;
            scrollLeft = this.wrapper.scrollLeft;
            this.wrapper.style.cursor = 'grabbing';
        });
        
        this.wrapper.addEventListener('mouseleave', () => {
            mouseDown = false;
            this.wrapper.style.cursor = 'grab';
        });
        
        this.wrapper.addEventListener('mouseup', () => {
            mouseDown = false;
            this.wrapper.style.cursor = 'grab';
        });
        
        this.wrapper.addEventListener('mousemove', (e) => {
            if (!mouseDown) return;
            e.preventDefault();
            const x = e.pageX - this.wrapper.offsetLeft;
            const walk = (x - startX) * 2;
            this.wrapper.scrollLeft = scrollLeft - walk;
        });
        
        // Responsive update
        window.addEventListener('resize', () => {
            this.updateResponsive();
            this.updateCarousel();
        });
        
        // Pause autoplay on hover
        if (this.options.autoplay) {
            this.container.addEventListener('mouseenter', () => this.stopAutoplay());
            this.container.addEventListener('mouseleave', () => this.startAutoplay());
        }
    }
    
    handleSwipe(startX, endX) {
        const threshold = 50;
        const diff = startX - endX;
        
        if (Math.abs(diff) > threshold) {
            if (diff > 0) {
                this.next();
            } else {
                this.prev();
            }
        }
    }
    
    updateCarousel() {
        if (this.isTransitioning) return;
        
        const itemWidth = this.wrapper.offsetWidth / this.options.itemsPerView;
        const translateX = -this.currentIndex * itemWidth;
        
        this.wrapper.style.transform = `translateX(${translateX}px)`;
        
        // Update button states
        if (this.prevBtn) {
            this.prevBtn.disabled = !this.options.loop && this.currentIndex === 0;
        }
        
        if (this.nextBtn) {
            this.nextBtn.disabled = !this.options.loop && this.currentIndex >= this.maxIndex;
        }
        
        // Trigger custom event
        this.container.dispatchEvent(new CustomEvent('carouselUpdate', {
            detail: { currentIndex: this.currentIndex }
        }));
    }
    
    next() {
        if (this.isTransitioning) return;
        
        if (this.currentIndex < this.maxIndex) {
            this.currentIndex++;
        } else if (this.options.loop) {
            this.currentIndex = 0;
        }
        
        this.updateCarousel();
    }
    
    prev() {
        if (this.isTransitioning) return;
        
        if (this.currentIndex > 0) {
            this.currentIndex--;
        } else if (this.options.loop) {
            this.currentIndex = this.maxIndex;
        }
        
        this.updateCarousel();
    }
    
    startAutoplay() {
        if (!this.options.autoplay) return;
        
        this.stopAutoplay();
        this.autoplayTimer = setInterval(() => {
            this.next();
        }, this.options.autoplayDelay);
    }
    
    stopAutoplay() {
        if (this.autoplayTimer) {
            clearInterval(this.autoplayTimer);
            this.autoplayTimer = null;
        }
    }
    
    goToIndex(index) {
        if (index >= 0 && index <= this.maxIndex) {
            this.currentIndex = index;
            this.updateCarousel();
        }
    }
}

// ==========================================
// HERO BACKGROUND CAROUSEL
// ==========================================

class HeroCarousel {
    constructor() {
        this.hero = document.getElementById('heroSection');
        if (!this.hero) return;
        
        this.indicators = document.querySelectorAll('#heroIndicators .carousel-dot');
        this.backgrounds = [
            'https://images.unsplash.com/photo-1611162617474-5b21e879e113?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
            'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        ];
        
        this.currentIndex = 0;
        this.init();
    }
    
    init() {
        // Preload images
        this.preloadImages();
        
        // Setup indicators
        this.indicators.forEach((dot, index) => {
            dot.addEventListener('click', () => this.goToSlide(index));
        });
        
        // Auto-rotate backgrounds
        setInterval(() => this.nextSlide(), 8000);
    }
    
    preloadImages() {
        this.backgrounds.forEach(url => {
            const img = new Image();
            img.src = url;
        });
    }
    
    goToSlide(index) {
        this.currentIndex = index;
        this.updateBackground();
        this.updateIndicators();
    }
    
    nextSlide() {
        this.currentIndex = (this.currentIndex + 1) % this.backgrounds.length;
        this.updateBackground();
        this.updateIndicators();
    }
    
    updateBackground() {
        this.hero.style.backgroundImage = `url('${this.backgrounds[this.currentIndex]}')`;
        this.hero.style.transition = 'background-image 1s ease-in-out';
    }
    
    updateIndicators() {
        this.indicators.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentIndex);
        });
    }
}

// ==========================================
// SCREENSHOT GALLERY
// ==========================================

class ScreenshotGallery {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;
        
        this.wrapper = this.container.querySelector('.screenshots-wrapper');
        this.screenshots = this.wrapper ? this.wrapper.querySelectorAll('.screenshot') : [];
        this.prevBtn = this.container.querySelector('.screenshot-nav-btn.prev');
        this.nextBtn = this.container.querySelector('.screenshot-nav-btn.next');
        
        this.currentIndex = 0;
        this.init();
    }
    
    init() {
        if (!this.wrapper || this.screenshots.length === 0) return;
        
        // Navigation buttons
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }
        
        // Click to expand
        this.screenshots.forEach((screenshot, index) => {
            screenshot.addEventListener('click', () => this.expandScreenshot(index));
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (this.isExpanded) {
                if (e.key === 'ArrowLeft') this.prev();
                if (e.key === 'ArrowRight') this.next();
                if (e.key === 'Escape') this.closeExpanded();
            }
        });
    }
    
    prev() {
        const scrollAmount = this.screenshots[0].offsetWidth + 20;
        this.wrapper.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    }
    
    next() {
        const scrollAmount = this.screenshots[0].offsetWidth + 20;
        this.wrapper.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
    
    expandScreenshot(index) {
        // Create lightbox
        const lightbox = document.createElement('div');
        lightbox.className = 'screenshot-lightbox';
        lightbox.innerHTML = `
            <div class="lightbox-content">
                <button class="lightbox-close">&times;</button>
                <button class="lightbox-prev"><i class="fas fa-chevron-left"></i></button>
                <button class="lightbox-next"><i class="fas fa-chevron-right"></i></button>
                <img src="${this.screenshots[index].querySelector('img').src}" alt="Screenshot">
                <div class="lightbox-counter">${index + 1} / ${this.screenshots.length}</div>
            </div>
        `;
        
        document.body.appendChild(lightbox);
        this.currentIndex = index;
        this.isExpanded = true;
        
        // Setup lightbox controls
        lightbox.querySelector('.lightbox-close').addEventListener('click', () => this.closeExpanded());
        lightbox.querySelector('.lightbox-prev').addEventListener('click', () => this.lightboxPrev());
        lightbox.querySelector('.lightbox-next').addEventListener('click', () => this.lightboxNext());
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) this.closeExpanded();
        });
        
        // Add animation
        setTimeout(() => lightbox.classList.add('active'), 10);
    }
    
    lightboxPrev() {
        this.currentIndex = (this.currentIndex - 1 + this.screenshots.length) % this.screenshots.length;
        this.updateLightbox();
    }
    
    lightboxNext() {
        this.currentIndex = (this.currentIndex + 1) % this.screenshots.length;
        this.updateLightbox();
    }
    
    updateLightbox() {
        const lightbox = document.querySelector('.screenshot-lightbox');
        if (!lightbox) return;
        
        const img = lightbox.querySelector('img');
        const counter = lightbox.querySelector('.lightbox-counter');
        
        img.src = this.screenshots[this.currentIndex].querySelector('img').src;
        counter.textContent = `${this.currentIndex + 1} / ${this.screenshots.length}`;
    }
    
    closeExpanded() {
        const lightbox = document.querySelector('.screenshot-lightbox');
        if (!lightbox) return;
        
        lightbox.classList.remove('active');
        setTimeout(() => lightbox.remove(), 300);
        this.isExpanded = false;
    }
}

// ==========================================
// SMOOTH SCROLL & ANIMATIONS
// ==========================================

class SmoothInteractions {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupSmoothScroll();
        this.setupParallax();
        this.setupIntersectionObserver();
        this.setupHoverEffects();
    }
    
    setupSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    const offset = 100;
                    const targetPosition = target.offsetTop - offset;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }
    
    setupParallax() {
        const parallaxElements = document.querySelectorAll('.hero-section');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = 0.5;
                element.style.transform = `translateY(${scrolled * speed}px)`;
            });
        });
    }
    
    setupIntersectionObserver() {
        const options = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    
                    // Stagger animation for grid items
                    if (entry.target.classList.contains('app-card')) {
                        const delay = Array.from(entry.target.parentElement.children).indexOf(entry.target) * 50;
                        entry.target.style.animationDelay = `${delay}ms`;
                    }
                }
            });
        }, options);
        
        // Observe elements
        document.querySelectorAll('.app-card, .category-card, .featured-banner').forEach(el => {
            observer.observe(el);
        });
    }
    
    setupHoverEffects() {
        // Magnetic buttons
        document.querySelectorAll('.hero-btn, .carousel-btn, .view-all').forEach(button => {
            button.addEventListener('mousemove', (e) => {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                
                button.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
            });
            
            button.addEventListener('mouseleave', () => {
                button.style.transform = '';
            });
        });
        
        // 3D card tilt effect
        document.querySelectorAll('.app-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width;
                const y = (e.clientY - rect.top) / rect.height;
                
                const tiltX = (y - 0.5) * 10;
                const tiltY = (x - 0.5) * -10;
                
                card.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateZ(10px)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }
}

// ==========================================
// INITIALIZE ALL COMPONENTS
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize carousels
    const featuredCarousel = new PremiumCarousel('featuredCarousel', {
        itemsPerView: 4,
        gap: 20,
        loop: true,
        responsive: {
            1200: { itemsPerView: 4 },
            992: { itemsPerView: 3 },
            768: { itemsPerView: 2 },
            480: { itemsPerView: 2 }
        }
    });
    
    const trendingCarousel = new PremiumCarousel('trendingCarousel', {
        itemsPerView: 4,
        gap: 20,
        loop: true,
        autoplay: true,
        autoplayDelay: 4000,
        responsive: {
            1200: { itemsPerView: 4 },
            992: { itemsPerView: 3 },
            768: { itemsPerView: 2 },
            480: { itemsPerView: 2 }
        }
    });
    
    const recentCarousel = new PremiumCarousel('recentCarousel', {
        itemsPerView: 4,
        gap: 20,
        loop: false,
        responsive: {
            1200: { itemsPerView: 4 },
            992: { itemsPerView: 3 },
            768: { itemsPerView: 2 },
            480: { itemsPerView: 2 }
        }
    });
    
    // Initialize hero carousel
    const heroCarousel = new HeroCarousel();
    
    // Initialize screenshot gallery (if on app detail page)
    if (document.getElementById('screenshotGallery')) {
        const screenshotGallery = new ScreenshotGallery('screenshotGallery');
    }
    
    // Initialize smooth interactions
    const smoothInteractions = new SmoothInteractions();
    
    // Add loading animation
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
    });
});

// ==========================================
// ADDITIONAL STYLES FOR LIGHTBOX
// ==========================================

const lightboxStyles = `
    .screenshot-lightbox {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.95);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .screenshot-lightbox.active {
        opacity: 1;
    }
    
    .lightbox-content {
        position: relative;
        max-width: 90%;
        max-height: 90%;
    }
    
    .lightbox-content img {
        max-width: 100%;
        max-height: 90vh;
        border-radius: 10px;
    }
    
    .lightbox-close {
        position: absolute;
        top: -40px;
        right: 0;
        background: none;
        border: none;
        color: white;
        font-size: 36px;
        cursor: pointer;
        transition: transform 0.3s;
    }
    
    .lightbox-close:hover {
        transform: rotate(90deg);
    }
    
    .lightbox-prev,
    .lightbox-next {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(255, 255, 255, 0.1);
        border: none;
        color: white;
        font-size: 24px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .lightbox-prev {
        left: -70px;
    }
    
    .lightbox-next {
        right: -70px;
    }
    
    .lightbox-prev:hover,
    .lightbox-next:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-50%) scale(1.1);
    }
    
    .lightbox-counter {
        position: absolute;
        bottom: -40px;
        left: 50%;
        transform: translateX(-50%);
        color: white;
        font-size: 14px;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated {
        animation: fadeInUp 0.6s ease-out forwards;
        opacity: 0;
    }
`;

// Inject lightbox styles
const styleSheet = document.createElement('style');
styleSheet.textContent = lightboxStyles;
document.head.appendChild(styleSheet);

console.log('🚀 Premium Carousel System Initialized!');
