// Enhanced Search Functionality with Real-time Suggestions
(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        DEBOUNCE_DELAY: 300,
        MIN_QUERY_LENGTH: 2,
        MAX_SUGGESTIONS: 8,
        TYPING_SPEED: 100,
        TYPING_PAUSE: 2000,
        ENDPOINT: '/api/search/suggestions'
    };

    // State management
    const SearchState = {
        isOpen: false,
        currentQuery: '',
        selectedIndex: -1,
        results: [],
        isLoading: false,
        typingInterval: null,
        currentPlaceholderIndex: 0
    };

    // DOM Elements
    const Elements = {
        searchInput: null,
        searchBox: null,
        searchDropdown: null,
        searchResults: null,
        searchForm: null
    };

    // Placeholder texts for typing animation
    const placeholderTexts = [
        'Search apps & games',
        'Try "Photo Editor"',
        'Search for "WhatsApp"',
        'Find "Minecraft"',
        'Discover new apps'
    ];

    // Initialize the search enhancement
    function init() {
        // Get DOM elements
        Elements.searchInput = document.getElementById('searchInput');
        Elements.searchBox = document.getElementById('searchBox');
        Elements.searchDropdown = document.getElementById('searchDropdown');
        Elements.searchResults = document.getElementById('searchResults');
        Elements.searchForm = document.querySelector('.search-form');

        if (!Elements.searchInput || !Elements.searchDropdown) {
            console.warn('Search elements not found');
            return;
        }

        // Setup event listeners
        setupEventListeners();
        
        // Initialize typing animation
        initTypingAnimation();
        
        // Close dropdown on outside click
        document.addEventListener('click', handleOutsideClick);
    }

    // Setup all event listeners
    function setupEventListeners() {
        // Input event with debouncing
        let debounceTimer;
        Elements.searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            const query = e.target.value.trim();
            
            if (query.length >= CONFIG.MIN_QUERY_LENGTH) {
                SearchState.isLoading = true;
                showLoadingState();
                
                debounceTimer = setTimeout(() => {
                    performSearch(query);
                }, CONFIG.DEBOUNCE_DELAY);
            } else {
                closeDropdown();
            }
        });

        // Focus event
        Elements.searchInput.addEventListener('focus', () => {
            if (SearchState.currentQuery && SearchState.results.length > 0) {
                openDropdown();
            }
            // Stop typing animation when focused
            stopTypingAnimation();
            Elements.searchInput.placeholder = placeholderTexts[0];
        });

        // Blur event (with delay to allow clicking results)
        Elements.searchInput.addEventListener('blur', () => {
            setTimeout(() => {
                if (!Elements.searchBox.contains(document.activeElement)) {
                    // Resume typing animation when not focused
                    startTypingAnimation();
                }
            }, 200);
        });

        // Keyboard navigation
        Elements.searchInput.addEventListener('keydown', handleKeyboardNavigation);

        // Prevent form submission if dropdown is open
        if (Elements.searchForm) {
            Elements.searchForm.addEventListener('submit', (e) => {
                if (SearchState.isOpen && SearchState.selectedIndex >= 0) {
                    e.preventDefault();
                    selectResult(SearchState.selectedIndex);
                }
            });
        }
    }

    // Typing animation for placeholder
    function initTypingAnimation() {
        startTypingAnimation();
    }

    function startTypingAnimation() {
        if (SearchState.typingInterval) return;
        
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        let currentText = placeholderTexts[textIndex];
        
        SearchState.typingInterval = setInterval(() => {
            if (!Elements.searchInput || document.activeElement === Elements.searchInput) {
                return;
            }

            if (!isDeleting) {
                // Typing
                if (charIndex <= currentText.length) {
                    Elements.searchInput.placeholder = currentText.substring(0, charIndex);
                    charIndex++;
                } else {
                    // Pause before deleting
                    setTimeout(() => {
                        isDeleting = true;
                    }, CONFIG.TYPING_PAUSE);
                }
            } else {
                // Deleting
                if (charIndex > 0) {
                    Elements.searchInput.placeholder = currentText.substring(0, charIndex - 1);
                    charIndex--;
                } else {
                    // Move to next text
                    isDeleting = false;
                    textIndex = (textIndex + 1) % placeholderTexts.length;
                    currentText = placeholderTexts[textIndex];
                }
            }
        }, CONFIG.TYPING_SPEED);
    }

    function stopTypingAnimation() {
        if (SearchState.typingInterval) {
            clearInterval(SearchState.typingInterval);
            SearchState.typingInterval = null;
        }
    }

    // Perform search request
    async function performSearch(query) {
        try {
            SearchState.currentQuery = query;
            
            const response = await fetch(`${CONFIG.ENDPOINT}?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success && data.results) {
                SearchState.results = data.results;
                displayResults(data.results);
                openDropdown();
            } else {
                displayNoResults();
            }
        } catch (error) {
            console.error('Search error:', error);
            displayError();
        } finally {
            SearchState.isLoading = false;
        }
    }

    // Display search results
    function displayResults(results) {
        if (!results || results.length === 0) {
            displayNoResults();
            return;
        }

        let html = '<div class="search-section">';
        
        results.forEach((app, index) => {
            // Fix icon path - prepend /static/images/app_icons/ if not absolute
            let iconUrl = app.icon || '/static/images/default-app-icon.png';
            if (iconUrl && !iconUrl.startsWith('/') && !iconUrl.startsWith('http')) {
                iconUrl = `/static/images/app_icons/${iconUrl}`;
            }
            const rating = app.rating ? app.rating.toFixed(1) : '0.0';
            const price = app.price === 0 ? 'Free' : `$${app.price}`;
            
            html += `
                <div class="search-item" data-index="${index}" data-app-id="${app.id}">
                    <img src="${iconUrl}" alt="${escapeHtml(app.name)}" class="search-item-icon">
                    <div class="search-item-content">
                        <div class="search-item-title">${escapeHtml(app.name)}</div>
                        <div class="search-item-subtitle">
                            <span>${escapeHtml(app.developer || 'Unknown Developer')}</span>
                            <span>•</span>
                            <span>${escapeHtml(app.category || 'Uncategorized')}</span>
                        </div>
                    </div>
                    <div class="search-item-meta">
                        <span>⭐ ${rating}</span>
                        <span>${price}</span>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        
        Elements.searchResults.innerHTML = html;
        
        // Add click handlers to results
        Elements.searchResults.querySelectorAll('.search-item').forEach((item, index) => {
            item.addEventListener('click', () => selectResult(index));
            item.addEventListener('mouseenter', () => {
                SearchState.selectedIndex = index;
                updateSelection();
            });
        });
    }

    // Display loading state
    function showLoadingState() {
        Elements.searchResults.innerHTML = `
            <div class="search-empty">
                <i class="fas fa-spinner fa-spin"></i> Searching...
            </div>
        `;
        openDropdown();
    }

    // Display no results message
    function displayNoResults() {
        Elements.searchResults.innerHTML = `
            <div class="search-empty">
                <i class="fas fa-search"></i> No results found
            </div>
        `;
        openDropdown();
    }

    // Display error message
    function displayError() {
        Elements.searchResults.innerHTML = `
            <div class="search-empty">
                <i class="fas fa-exclamation-circle"></i> Error loading results
            </div>
        `;
        openDropdown();
    }

    // Keyboard navigation
    function handleKeyboardNavigation(e) {
        if (!SearchState.isOpen || SearchState.results.length === 0) return;

        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                SearchState.selectedIndex = Math.min(SearchState.selectedIndex + 1, SearchState.results.length - 1);
                updateSelection();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                SearchState.selectedIndex = Math.max(SearchState.selectedIndex - 1, -1);
                updateSelection();
                break;
                
            case 'Enter':
                if (SearchState.selectedIndex >= 0) {
                    e.preventDefault();
                    selectResult(SearchState.selectedIndex);
                }
                break;
                
            case 'Escape':
                e.preventDefault();
                closeDropdown();
                Elements.searchInput.blur();
                break;
        }
    }

    // Update visual selection
    function updateSelection() {
        const items = Elements.searchResults.querySelectorAll('.search-item');
        items.forEach((item, index) => {
            if (index === SearchState.selectedIndex) {
                item.classList.add('kb-selected');
                item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            } else {
                item.classList.remove('kb-selected');
            }
        });
    }

    // Select a result
    function selectResult(index) {
        const result = SearchState.results[index];
        if (result && result.id) {
            window.location.href = `/app/${result.id}`;
        }
    }

    // Open dropdown
    function openDropdown() {
        Elements.searchDropdown.classList.add('active');
        SearchState.isOpen = true;
    }

    // Close dropdown
    function closeDropdown() {
        Elements.searchDropdown.classList.remove('active');
        SearchState.isOpen = false;
        SearchState.selectedIndex = -1;
    }

    // Handle outside clicks
    function handleOutsideClick(e) {
        if (!Elements.searchBox.contains(e.target)) {
            closeDropdown();
        }
    }

    // Utility function to escape HTML
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text || '';
        return div.innerHTML;
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for debugging
    window.SearchEnhanced = {
        state: SearchState,
        config: CONFIG
    };
})();
