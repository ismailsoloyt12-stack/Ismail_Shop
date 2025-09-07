// Main JavaScript for App Store

// Dark Mode Toggle
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const html = document.documentElement;

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme') || 'light';
html.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

themeToggle?.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    if (themeIcon) {
        themeIcon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
    }
}

// Sidebar Toggle with Mobile Support
const menuToggle = document.getElementById('menuToggle');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');
const footer = document.querySelector('.footer');
let sidebarOverlay = null;

// Create sidebar overlay for mobile
function createSidebarOverlay() {
    if (!sidebarOverlay) {
        sidebarOverlay = document.createElement('div');
        sidebarOverlay.className = 'sidebar-overlay';
        document.body.appendChild(sidebarOverlay);
        
        // Close sidebar when clicking overlay
        sidebarOverlay.addEventListener('click', closeMobileSidebar);
    }
    return sidebarOverlay;
}

// Create close button for mobile sidebar
function createSidebarCloseButton() {
    const closeBtn = document.createElement('button');
    closeBtn.className = 'sidebar-close';
    closeBtn.innerHTML = '<i class="fas fa-times"></i>';
    closeBtn.addEventListener('click', closeMobileSidebar);
    sidebar?.prepend(closeBtn);
}

// Open mobile sidebar
function openMobileSidebar() {
    if (window.innerWidth <= 768) {
        sidebar?.classList.add('active');
        sidebar?.classList.remove('hidden');
        document.body.classList.add('sidebar-open');
        const overlay = createSidebarOverlay();
        setTimeout(() => overlay?.classList.add('active'), 10);
    }
}

// Close mobile sidebar
function closeMobileSidebar() {
    sidebar?.classList.remove('active');
    document.body.classList.remove('sidebar-open');
    sidebarOverlay?.classList.remove('active');
    setTimeout(() => {
        if (window.innerWidth <= 768) {
            sidebar?.classList.add('hidden');
        }
    }, 300);
}

// Toggle sidebar based on screen size
function toggleSidebar() {
    if (window.innerWidth <= 768) {
        // Mobile behavior
        if (sidebar?.classList.contains('active')) {
            closeMobileSidebar();
        } else {
            openMobileSidebar();
        }
    } else {
        // Desktop behavior
        sidebar?.classList.toggle('hidden');
        mainContent?.classList.toggle('expanded');
        if (footer) footer.classList.toggle('expanded');
    }
}

menuToggle?.addEventListener('click', toggleSidebar);

// Initialize sidebar for mobile
function initializeSidebar() {
    if (window.innerWidth <= 768) {
        sidebar?.classList.add('hidden');
        sidebar?.classList.remove('active');
        mainContent?.classList.add('expanded');
        if (footer) footer.classList.add('expanded');
        createSidebarCloseButton();
    } else {
        // Desktop view
        sidebar?.classList.remove('active', 'hidden');
        mainContent?.classList.remove('expanded');
        if (footer) footer.classList.remove('expanded');
        document.body.classList.remove('sidebar-open');
        sidebarOverlay?.classList.remove('active');
    }
}

// Handle window resize
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        initializeSidebar();
    }, 250);
});

// Initialize on load
initializeSidebar();

// Close sidebar when clicking on a link (mobile)
if (window.innerWidth <= 768) {
    document.querySelectorAll('.sidebar-menu a').forEach(link => {
        link.addEventListener('click', () => {
            setTimeout(closeMobileSidebar, 100);
        });
    });
}

// Swipe gestures for mobile sidebar
let touchStartX = 0;
let touchEndX = 0;

function handleSwipe() {
    if (window.innerWidth <= 768) {
        const swipeThreshold = 50;
        const swipeDistance = touchEndX - touchStartX;
        
        // Swipe right to open sidebar
        if (swipeDistance > swipeThreshold && touchStartX < 50) {
            openMobileSidebar();
        }
        // Swipe left to close sidebar
        else if (swipeDistance < -swipeThreshold && sidebar?.classList.contains('active')) {
            closeMobileSidebar();
        }
    }
}

document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
}, { passive: true });

// Close alerts
document.querySelectorAll('.alert-close').forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.style.display = 'none';
    });
});

// Review Modal
const reviewModal = document.getElementById('reviewModal');
const closeModal = document.querySelector('.modal .close');

function showReviewForm() {
    if (reviewModal) {
        reviewModal.style.display = 'block';
    }
}

closeModal?.addEventListener('click', () => {
    if (reviewModal) {
        reviewModal.style.display = 'none';
    }
});

window.addEventListener('click', (event) => {
    if (event.target === reviewModal) {
        reviewModal.style.display = 'none';
    }
});

// Star Rating
const starRating = document.querySelectorAll('.star-rating i');
let selectedRating = 0;

starRating.forEach((star, index) => {
    star.addEventListener('click', () => {
        selectedRating = index + 1;
        updateStars(selectedRating);
    });
    
    star.addEventListener('mouseenter', () => {
        updateStars(index + 1);
    });
});

document.querySelector('.star-rating')?.addEventListener('mouseleave', () => {
    updateStars(selectedRating);
});

function updateStars(rating) {
    starRating.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('far');
            star.classList.add('fas', 'active');
        } else {
            star.classList.remove('fas', 'active');
            star.classList.add('far');
        }
    });
}

// Review Form Submit
const reviewForm = document.getElementById('reviewForm');
reviewForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const comment = document.getElementById('reviewComment').value;
    const appId = window.location.pathname.split('/').pop();
    
    if (selectedRating === 0) {
        alert('Please select a rating');
        return;
    }
    
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
            alert('Review submitted successfully!');
            reviewModal.style.display = 'none';
            location.reload();
        } else {
            alert('Error submitting review. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error submitting review. Please try again.');
    }
});

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Lazy Loading Images
const lazyImages = document.querySelectorAll('img[data-lazy]');
const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.lazy;
            img.removeAttribute('data-lazy');
            imageObserver.unobserve(img);
        }
    });
});

lazyImages.forEach(img => imageObserver.observe(img));

// Search Box Focus
const searchInput = document.querySelector('.search-box input');
searchInput?.addEventListener('focus', () => {
    searchInput.parentElement.classList.add('focused');
});

searchInput?.addEventListener('blur', () => {
    searchInput.parentElement.classList.remove('focused');
});

// App Card Animations
const appCards = document.querySelectorAll('.app-card');
const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.5s ease forwards';
            cardObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

appCards.forEach(card => {
    card.style.opacity = '0';
    cardObserver.observe(card);
});

// Add fadeInUp animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Read More Toggle
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

// Screenshot Carousel
const screenshotsCarousel = document.querySelector('.screenshots-carousel');
if (screenshotsCarousel) {
    let isDown = false;
    let startX;
    let scrollLeft;
    
    screenshotsCarousel.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - screenshotsCarousel.offsetLeft;
        scrollLeft = screenshotsCarousel.scrollLeft;
        screenshotsCarousel.style.cursor = 'grabbing';
    });
    
    screenshotsCarousel.addEventListener('mouseleave', () => {
        isDown = false;
        screenshotsCarousel.style.cursor = 'grab';
    });
    
    screenshotsCarousel.addEventListener('mouseup', () => {
        isDown = false;
        screenshotsCarousel.style.cursor = 'grab';
    });
    
    screenshotsCarousel.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - screenshotsCarousel.offsetLeft;
        const walk = (x - startX) * 2;
        screenshotsCarousel.scrollLeft = scrollLeft - walk;
    });
}

// Format numbers (downloads, reviews, etc.)
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// Update download counts
document.querySelectorAll('.stat-value').forEach(elem => {
    const text = elem.textContent;
    const num = parseInt(text);
    if (!isNaN(num) && num > 999) {
        elem.textContent = formatNumber(num);
    }
});

// Share functionality
document.querySelector('.share-btn')?.addEventListener('click', async () => {
    if (navigator.share) {
        try {
            await navigator.share({
                title: document.title,
                url: window.location.href
            });
        } catch (err) {
            console.log('Error sharing:', err);
        }
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href);
        alert('Link copied to clipboard!');
    }
});

// Auto-hide navbar on scroll (mobile)
let lastScrollTop = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (window.innerWidth <= 768) {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    }
});

// Initialize tooltips
const initTooltips = () => {
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(elem => {
        const title = elem.getAttribute('title');
        elem.removeAttribute('title');
        elem.setAttribute('data-tooltip', title);
    });
};

initTooltips();

// Page load animations
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

console.log('App Store JS loaded successfully!');
