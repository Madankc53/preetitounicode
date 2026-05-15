/**
 * components.js - Improved for thenepal.io
 */
(async function () {
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

    async function load(id, url) {
        const el = document.getElementById(id);
        if (!el) return;
        
        try {
            const res = await fetch(url);
            if (!res.ok) throw new Error(`Failed to load ${url}`);
            const html = await res.text();
            el.innerHTML = html;
            executeScripts(el);
        } catch (e) {
            console.warn(`Could not load ${url}:`, e);
            el.innerHTML = `<p style="color:red;text-align:center;">Failed to load ${id}</p>`;
        }
    }

    // Load Header & Footer
    await Promise.all([
        load('header', '/header.html'),
        load('footer', '/footer.html')
    ]);

    // Active Link Highlight
    const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
    document.querySelectorAll('.nav-links a').forEach(link => {
        try {
            const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/$/, '') || '/';
            if (linkPath === currentPath || link.classList.contains('active')) {
                link.classList.add('active');
            }
        } catch (e) {}
    });

    // Mobile Menu Toggle (Improved)
    const toggleBtn = document.getElementById('mobileMenuToggle');
    const navLinks = document.querySelector('.nav-links');

    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener('click', function (e) {
            e.stopPropagation();
            navLinks.classList.toggle('active');
            
            // Change hamburger to X
            const spans = this.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                this.style.transform = 'rotate(90deg)';
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
            } else {
                this.style.transform = 'none';
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                toggleBtn.style.transform = 'none';
                const spans = toggleBtn.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !toggleBtn.contains(e.target)) {
                navLinks.classList.remove('active');
                toggleBtn.style.transform = 'none';
            }
        });
    }
})();
