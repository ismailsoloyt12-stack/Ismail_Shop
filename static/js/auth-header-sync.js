/**
 * Authentication Header Synchronization Module
 * Synchronizes the header UI with Firebase authentication state
 */

// Import Firebase modules
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { 
    getAuth, 
    onAuthStateChanged,
    signOut 
} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

// Firebase configuration (same as in login.html)
const firebaseConfig = {
    apiKey: "AIzaSyBles8dPATnlVUJ8-IKaHyCXqfh6e_HXiI",
    authDomain: "ismailstore-638a3.firebaseapp.com",
    projectId: "ismailstore-638a3",
    storageBucket: "ismailstore-638a3.appspot.com",
    messagingSenderId: "163789107661",
    appId: "1:163789107661:web:8c67ebf5a32369a3051484",
    measurementId: "G-13QF3PJVS4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

/**
 * Creates a user profile element for the header
 * @param {Object} user - Firebase user object
 * @returns {HTMLElement} User profile element
 */
function createUserProfileElement(user) {
    const profileContainer = document.createElement('div');
    profileContainer.className = 'header-user-profile';
    profileContainer.id = 'header-user-profile';
    profileContainer.style.cssText = `
        display: inline-flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        position: relative;
    `;

    // Create profile image or initial
    const profileElement = document.createElement('div');
    
    if (user.photoURL) {
        // Use user's profile picture
        const img = document.createElement('img');
        img.src = user.photoURL;
        img.alt = user.displayName || 'User';
        img.style.cssText = `
            width: 35px;
            height: 35px;
            border-radius: 50%;
            border: 2px solid #4285f4;
            object-fit: cover;
        `;
        profileElement.appendChild(img);
    } else {
        // Use initial in a circle
        const initial = (user.displayName || user.email || 'U')[0].toUpperCase();
        profileElement.style.cssText = `
            width: 35px;
            height: 35px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 16px;
            border: 2px solid #4285f4;
        `;
        profileElement.textContent = initial;
    }

    profileContainer.appendChild(profileElement);

    // Create dropdown menu
    const dropdown = document.createElement('div');
    dropdown.className = 'header-dropdown-menu';
    dropdown.style.cssText = `
        position: absolute;
        top: 100%;
        right: 0;
        margin-top: 10px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        min-width: 200px;
        display: none;
        z-index: 1000;
        padding: 8px 0;
    `;

    // Add dropdown items
    const menuItems = [
        { icon: '👤', text: user.email, action: null },
        { divider: true },
        { icon: '❤️', text: 'My Favorites', action: () => window.location.href = '/favorites' },
        { icon: '📥', text: 'My Downloads', action: null },
        { icon: '⚙️', text: 'Settings', action: null },
        { divider: true },
        { icon: '🚪', text: 'Sign Out', action: () => handleSignOut() }
    ];

    menuItems.forEach(item => {
        if (item.divider) {
            const divider = document.createElement('hr');
            divider.style.cssText = `
                margin: 8px 0;
                border: none;
                border-top: 1px solid #e0e0e0;
            `;
            dropdown.appendChild(divider);
        } else {
            const menuItem = document.createElement('div');
            menuItem.style.cssText = `
                padding: 10px 20px;
                cursor: ${item.action ? 'pointer' : 'default'};
                display: flex;
                align-items: center;
                gap: 10px;
                transition: background 0.2s;
                color: ${item.text === 'Sign Out' ? '#dc3545' : '#333'};
                font-size: 14px;
            `;
            
            if (item.action) {
                menuItem.onmouseover = () => menuItem.style.background = '#f5f5f5';
                menuItem.onmouseout = () => menuItem.style.background = 'transparent';
                menuItem.onclick = (e) => {
                    e.stopPropagation();
                    item.action();
                };
            }
            
            menuItem.innerHTML = `<span>${item.icon}</span> ${item.text}`;
            dropdown.appendChild(menuItem);
        }
    });

    profileContainer.appendChild(dropdown);

    // Toggle dropdown on click
    profileContainer.onclick = (e) => {
        e.stopPropagation();
        dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
    };

    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        dropdown.style.display = 'none';
    });

    return profileContainer;
}

/**
 * Updates the header based on authentication state
 * @param {Object|null} user - Firebase user object or null
 */
function updateHeader(user) {
    // Try multiple possible selectors for the sign-in button
    const signInSelectors = [
        '#header-signin-button',
        '.login-btn',
        '.nav-right .login-btn',
        'a[href*="login"]'
    ];
    
    let signInButton = null;
    for (const selector of signInSelectors) {
        signInButton = document.querySelector(selector);
        if (signInButton) break;
    }

    // Get or create user profile element container
    let userProfileElement = document.getElementById('header-user-profile');
    
    if (user) {
        // User is signed in
        console.log('Header sync: User signed in -', user.email);
        
        // Hide sign-in button
        if (signInButton) {
            signInButton.style.display = 'none';
        }
        
        // Show user profile
        if (!userProfileElement) {
            // Create and insert user profile element
            userProfileElement = createUserProfileElement(user);
            
            // Find the best place to insert the profile element
            const navRight = document.querySelector('.nav-right');
            const userMenu = document.querySelector('.user-menu');
            
            if (navRight) {
                // Remove any existing Flask-based user menu if present
                if (userMenu) {
                    userMenu.style.display = 'none';
                }
                navRight.appendChild(userProfileElement);
            } else if (signInButton && signInButton.parentNode) {
                // Insert next to sign-in button
                signInButton.parentNode.insertBefore(userProfileElement, signInButton.nextSibling);
            }
        } else {
            // Update existing profile element
            userProfileElement.style.display = 'inline-flex';
            // Update profile picture/initial if needed
            updateProfileElement(userProfileElement, user);
        }
        
    } else {
        // User is signed out
        console.log('Header sync: User signed out');
        
        // Show sign-in button
        if (signInButton) {
            signInButton.style.display = 'inline-flex';
        }
        
        // Hide/remove user profile
        if (userProfileElement) {
            userProfileElement.remove();
        }
        
        // Show Flask-based user menu if it was hidden
        const userMenu = document.querySelector('.user-menu');
        if (userMenu) {
            userMenu.style.display = '';
        }
    }
}

/**
 * Updates an existing profile element with new user data
 * @param {HTMLElement} element - The profile element to update
 * @param {Object} user - Firebase user object
 */
function updateProfileElement(element, user) {
    const imgElement = element.querySelector('img');
    const initialElement = element.querySelector('div:first-child');
    const nameElement = element.querySelector('span');
    
    if (user.photoURL && imgElement) {
        imgElement.src = user.photoURL;
    } else if (!user.photoURL && initialElement && !imgElement) {
        const initial = (user.displayName || user.email || 'U')[0].toUpperCase();
        initialElement.textContent = initial;
    }
    
    if (nameElement) {
        nameElement.textContent = user.displayName || user.email.split('@')[0];
    }
}

/**
 * Syncs Firebase authentication with Flask backend
 * @param {Object} user - Firebase user object
 */
async function syncWithFlaskBackend(user) {
    if (!user) return;
    
    try {
        const response = await fetch('/api/firebase-auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                uid: user.uid,
                email: user.email,
                displayName: user.displayName,
                photoURL: user.photoURL
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('Flask backend synced:', data.message);
            // Reload the page to reflect Flask authentication state
            if (window.location.pathname === '/login') {
                window.location.href = '/';
            } else {
                window.location.reload();
            }
        } else {
            console.error('Failed to sync with Flask backend:', data.error);
        }
    } catch (error) {
        console.error('Error syncing with Flask backend:', error);
    }
}

/**
 * Handles sign out
 */
async function handleSignOut() {
    try {
        // First sign out from Firebase
        await signOut(auth);
        console.log('User signed out from Firebase');
        
        // Then clear Flask session
        await fetch('/api/firebase-logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('Flask session cleared');
        
        // Redirect to home page
        window.location.href = '/';
    } catch (error) {
        console.error('Error signing out:', error);
        alert('Sign-out failed. Please try again.');
    }
}

/**
 * Initialize header synchronization
 */
function initHeaderSync() {
    let hasInitialSync = false;
    
    // Set up authentication state observer
    onAuthStateChanged(auth, async (user) => {
        // Check if we need to sync with Flask backend on initial load
        if (user && !hasInitialSync) {
            // Check if Flask session exists by looking for Flask-specific elements
            const flaskUserMenu = document.querySelector('.user-menu');
            const isFlaskAuthenticated = flaskUserMenu && flaskUserMenu.style.display !== 'none';
            
            // If Firebase user exists but Flask session doesn't, sync them
            if (!isFlaskAuthenticated) {
                console.log('Firebase user detected, syncing with Flask backend...');
                await syncWithFlaskBackend(user);
                hasInitialSync = true;
                return; // Page will reload after sync
            }
        }
        
        updateHeader(user);
        
        // Also update body class for CSS styling
        if (user) {
            document.body.classList.add('user-authenticated');
            document.body.classList.remove('user-anonymous');
        } else {
            document.body.classList.add('user-anonymous');
            document.body.classList.remove('user-authenticated');
        }
    });
    
    console.log('Header authentication sync initialized');
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeaderSync);
} else {
    initHeaderSync();
}

// Export functions for external use
window.authHeaderSync = {
    updateHeader,
    handleSignOut,
    auth
};
