// Mobile Menu Toggle
    const toggleBtn = document.getElementById('mobileMenuToggle');
    const mobileMenu = document.getElementById('mobileMenu');

    if (toggleBtn && mobileMenu) {
        toggleBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            
            // Optional: Change icon to X
            if (mobileMenu.classList.contains('active')) {
                this.innerHTML = '✕';
                this.style.fontSize = '32px';
            } else {
                this.innerHTML = '<span class="hamburger"></span>';
                this.style.fontSize = '28px';
            }
        });

        // Close menu when link clicked
        document.querySelectorAll('.mobile-nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('active');
                toggleBtn.innerHTML = '<span class="hamburger"></span>';
                toggleBtn.style.fontSize = '28px';
            });
        });
    }
