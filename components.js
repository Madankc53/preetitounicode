/**
 * components.js - Fixed & Improved for thenepal.io
 * Loads header and footer + Mobile Menu + Active Link
 */

(async function () {
    /**
     * Execute scripts inside loaded HTML (important for future ads)
     */
    function executeScripts(container) {
        const scripts = container.querySelectorAll('script');
        scripts.forEach(oldScript => {
            const newScript = document.createElement('script');
            Array.from(oldScript.attributes).forEach(attr => {
                newScript.setAttribute(attr.name, attr.value);
            });
            newScript.textContent = oldScript.innerHTML;
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    }

    /**
     * Load HTML component
     */
    async function loadComponent(id, url) {
        const element = document.getElementById(id);
        if (!element) {
            console.warn(`Element with id "${id}" not found`);
            return;
        }

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            
            const html = await response.text();
            element.innerHTML = html;
            
            // Execute any scripts inside the loaded content
            executeScripts(element);
            
            console.log(`✅ Loaded ${url} successfully`);
        } catch (error) {
            console.error(`❌ Failed to load ${url}:`, error);
            element.innerHTML = `<div style="color:red; text-align:center; padding:20px;">
                Could not load ${id}. Please check file path.
            </div>`;
        }
    }

    // Load Header and Footer in parallel
    await Promise.all([
        loadComponent('header', '/header.html'),
        loadComponent('footer', '/footer.html')
    ]);

    // ====================== ACTIVE LINK HIGHLIGHT ======================
    const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
    
    document.querySelectorAll('.nav-links a, .mobile-nav-links a').forEach(link => {
        try {
            const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/$/, '') || '/';
            if (linkPath === currentPath || link.classList.contains('active')) {
                link.classList.add('active');
            }
        } catch (e) {
            // Ignore external links
        }
    });

    // ====================== MOBILE MENU ======================
    const toggleBtn = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (toggleBtn && mobileMenu) {
        toggleBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            mobileMenu.classList.toggle('active');
            
            // Toggle between hamburger and close icon
            if (mobileMenu.classList.contains('active')) {
                this.innerHTML = '✕';
                this.style.fontSize = '32px';
                this.style.fontWeight = 'bold';
            } else {
                this.innerHTML = '<span class="hamburger"></span>';
                this.style.fontSize = '28px';
            }
        });

        // Close menu when a link is clicked
        document.querySelectorAll('.mobile-nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                toggleBtn.innerHTML = '<span class="hamburger"></span>';
                toggleBtn.style.fontSize = '28px';
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function (e) {
            if (!mobileMenu.contains(e.target) && !toggleBtn.contains(e.target)) {
                mobileMenu.classList.remove('active');
                toggleBtn.innerHTML = '<span class="hamburger"></span>';
                toggleBtn.style.fontSize = '28px';
            }
        });
    }

    console.log('🚀 thenepal.io components loaded successfully');
})();
