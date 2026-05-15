/**
 * Upgraded components.js
 * - Loads header.html & footer.html into every page.
 * - Supports script execution (essential for AdSense).
 * - Robust active link highlighting.
 * - Improved mobile menu logic.
 */
(async function () {
    /**
     * Helper to execute scripts in injected HTML
     * innerHTML doesn't execute <script> tags, so we must manually re-insert them.
     */
    function executeScripts(container) {
        const scripts = container.querySelectorAll('script');
        scripts.forEach(oldScript => {
            const newScript = document.createElement('script');
            Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
            newScript.appendChild(document.createTextNode(oldScript.innerHTML));
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    }

    async function load(id, url) {
        const el = document.getElementById(id);
        if (!el) return;
        try {
            const res = await fetch(url);
            if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`);
            const html = await res.text();
            el.innerHTML = html;
            
            // Crucial: Execute scripts (like AdSense) inside the injected HTML
            executeScripts(el);
        } catch (e) {
            console.warn(`Could not load ${url}:`, e);
        }
    }

    // 1. Load both in parallel
    await Promise.all([
        load('header', '/header.html'),
        load('footer', '/footer.html'),
    ]);

    // 2. Highlight the active nav link
    const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
    const navLinks = document.querySelectorAll('nav ul a, .nav-links a');
    
    navLinks.forEach(link => {
        try {
            const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/$/, '') || '/';
            if (linkPath === currentPath) {
                link.classList.add('active');
                // Also add to parent li if needed for styling
                if (link.parentElement.tagName === 'LI') {
                    link.parentElement.classList.add('active');
                }
            }
        } catch (e) {
            // Ignore external or invalid links
        }
    });

    // 3. Mobile hamburger toggle logic
    // We look for common classes: .nav-toggle (user's) or .mobile-menu-toggle (mine)
    const toggle = document.querySelector('.nav-toggle, .mobile-menu-toggle');
    const navList = document.querySelector('nav ul, .nav-links');
    
    if (toggle && navList) {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();
            navList.classList.toggle('open');
            navList.classList.toggle('active'); // Support both class names
            toggle.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navList.contains(e.target) && !toggle.contains(e.target)) {
                navList.classList.remove('open', 'active');
                toggle.classList.remove('active');
            }
        });
    }
})();
