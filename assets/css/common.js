/**
 * Common JavaScript for GitHub Pages PWA
 * Handles service worker registration, offline detection, and common utilities
 */

// ============================================
// Service Worker Registration
// ============================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('ServiceWorker registered successfully:', registration.scope);
                
                // Check for updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    console.log('Service Worker update found!');
                    
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            showUpdateNotification();
                        }
                    });
                });
            })
            .catch(error => {
                console.log('ServiceWorker registration failed:', error);
            });
        
        // Handle controller changes
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            console.log('Service Worker controller changed');
            window.location.reload();
        });
    });
}

// Show update notification
function showUpdateNotification() {
    const notification = document.createElement('div');
    notification.className = 'update-notification';
    notification.innerHTML = `
        <div class="update-content">
            <span>🚀 New version available!</span>
            <button onclick="location.reload()">Update Now</button>
        </div>
    `;
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
}

// ============================================
// Offline Detection
// ============================================

let isOffline = false;

function updateOfflineStatus() {
    const indicator = document.getElementById('offline-indicator');
    if (!navigator.onLine) {
        isOffline = true;
        if (indicator) {
            indicator.classList.add('show');
        }
        document.body.classList.add('offline-mode');
        showToast('You are offline. Some features may be limited.', 'warning');
    } else {
        if (isOffline) {
            isOffline = false;
            if (indicator) {
                indicator.classList.remove('show');
            }
            document.body.classList.remove('offline-mode');
            showToast('Back online! 🎉', 'success');
        }
    }
}

// Listen for online/offline events
window.addEventListener('online', updateOfflineStatus);
window.addEventListener('offline', updateOfflineStatus);

// Initial check
updateOfflineStatus();

// ============================================
// Toast Notifications
// ============================================

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <span class="toast-icon">${getToastIcon(type)}</span>
            <span class="toast-message">${message}</span>
        </div>
    `;
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

function getToastIcon(type) {
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    return icons[type] || icons.info;
}

// ============================================
// Loading States
// ============================================

function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        const loadingOverlay = document.createElement('div');
        loadingOverlay.className = 'loading-overlay';
        loadingOverlay.id = `loading-${containerId}`;
        loadingOverlay.innerHTML = '<div class="spinner"></div>';
        container.style.position = 'relative';
        container.appendChild(loadingOverlay);
    }
}

function hideLoading(containerId) {
    const loadingOverlay = document.getElementById(`loading-${containerId}`);
    if (loadingOverlay) {
        loadingOverlay.remove();
    }
}

// ============================================
// Progress Bar
// ============================================

let progressBar = null;

function initProgressBar() {
    progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    document.body.appendChild(progressBar);
}

function updateProgressBar(percent) {
    if (!progressBar) {
        initProgressBar();
    }
    progressBar.style.width = `${percent}%`;
    
    if (percent >= 100) {
        setTimeout(() => {
            progressBar.style.width = '0';
        }, 500);
    }
}

// Monitor page load progress
window.addEventListener('beforeunload', () => {
    updateProgressBar(0);
});

window.addEventListener('load', () => {
    updateProgressBar(100);
});

// ============================================
// Form Validation
// ============================================

const Validators = {
    required: (value) => value && value.trim() !== '' ? null : 'This field is required',
    email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) ? null : 'Invalid email address',
    phone: (value) => /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/.test(value) ? null : 'Invalid phone number',
    minLength: (min) => (value) => value.length >= min ? null : `Minimum ${min} characters required`,
    maxLength: (max) => (value) => value.length <= max ? null : `Maximum ${max} characters allowed`
};

function validateForm(formId, rules) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    const errors = {};
    
    for (const [fieldName, fieldRules] of Object.entries(rules)) {
        const field = form.elements[fieldName];
        if (!field) continue;
        
        const value = field.value;
        const fieldErrors = [];
        
        for (const rule of fieldRules) {
            let error;
            if (typeof rule === 'function') {
                error = rule(value);
            } else if (typeof rule === 'string') {
                error = Validators[rule]?.(value);
            }
            
            if (error) {
                fieldErrors.push(error);
            }
        }
        
        if (fieldErrors.length > 0) {
            errors[fieldName] = fieldErrors;
            isValid = false;
            showFieldError(field, fieldErrors[0]);
        } else {
            clearFieldError(field);
        }
    }
    
    return isValid;
}

function showFieldError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    field.classList.add('error');
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('error');
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// ============================================
// AJAX/Fetch Utilities
// ============================================

async function fetchAPI(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    };
    
    const finalOptions = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, finalOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        return { success: true, data };
    } catch (error) {
        console.error('API Error:', error);
        showToast(error.message, 'error');
        return { success: false, error: error.message };
    }
}

// ============================================
// Local Storage Helpers
// ============================================

const Storage = {
    set(key, value, useSession = false) {
        const storage = useSession ? sessionStorage : localStorage;
        try {
            storage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    },
    
    get(key, defaultValue = null, useSession = false) {
        const storage = useSession ? sessionStorage : localStorage;
        try {
            const item = storage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Storage error:', error);
            return defaultValue;
        }
    },
    
    remove(key, useSession = false) {
        const storage = useSession ? sessionStorage : localStorage;
        storage.removeItem(key);
    },
    
    clear(useSession = false) {
        const storage = useSession ? sessionStorage : localStorage;
        storage.clear();
    }
};

// ============================================
// Dark Mode Toggle
// ============================================

function initDarkMode() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = Storage.get('theme');
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.add('dark-mode');
    }
    
    // Create toggle button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'dark-mode-toggle';
    toggleBtn.innerHTML = '🌙';
    toggleBtn.addEventListener('click', toggleDarkMode);
    document.body.appendChild(toggleBtn);
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    Storage.set('theme', isDark ? 'dark' : 'light');
    
    const toggleBtn = document.querySelector('.dark-mode-toggle');
    toggleBtn.innerHTML = isDark ? '☀️' : '🌙';
}

// ============================================
// Lazy Loading Images
// ============================================

function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.dataset.src;
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                    }
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for older browsers
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// ============================================
// Smooth Scroll
// ============================================

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ============================================
// Copy to Clipboard
// ============================================

async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
        return true;
    } catch (error) {
        console.error('Copy failed:', error);
        showToast('Failed to copy', 'error');
        return false;
    }
}

// ============================================
// Initialize on DOM Load
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing common.js');
    initProgressBar();
    initDarkMode();
    initLazyLoading();
    initSmoothScroll();
    
    // Add offline indicator to DOM if not present
    if (!document.getElementById('offline-indicator')) {
        const indicator = document.createElement('div');
        indicator.id = 'offline-indicator';
        indicator.className = 'offline-indicator';
        indicator.innerHTML = '📡 You are offline';
        document.body.appendChild(indicator);
    }
});

// ============================================
// Export for module usage
// ============================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        showToast,
        showLoading,
        hideLoading,
        validateForm,
        fetchAPI,
        Storage,
        copyToClipboard
    };
}
// Add to your common.js
function loadPreetiFont() {
    const fontLink = document.createElement('link');
    fontLink.rel = 'stylesheet';
    fontLink.href = '/assets/css/fonts.css';
    document.head.appendChild(fontLink);
    
    // Check if font loaded
    document.fonts.ready.then(() => {
        console.log('Preeti font loaded successfully');
        showToast('Nepali font loaded', 'success');
    }).catch(error => {
        console.error('Font loading error:', error);
    });
}

// Load font if page has Nepali content
if (document.documentElement.lang === 'ne' || 
    document.querySelector('[lang="ne"], .nepali-text, .preeti-font')) {
    loadPreetiFont();
}
