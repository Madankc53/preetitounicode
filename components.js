/**
 * components.js  — loads header.html & footer.html into every page
 * Place <div id="header"></div> and <div id="footer"></div> in your HTML.
 */
(async function () {
  async function load(id, url) {
    const el = document.getElementById(id);
    if (!el) return;
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(res.status);
      el.innerHTML = await res.text();
    } catch (e) {
      console.warn(`Could not load ${url}:`, e);
    }
  }

  // Load both in parallel
  await Promise.all([
    load('header', '/header.html'),
    load('footer', '/footer.html'),
  ]);

  // Highlight the active nav link
  const links = document.querySelectorAll('nav ul a');
  const current = window.location.pathname.replace(/\/$/, '') || '/';
  links.forEach(link => {
    const href = new URL(link.href).pathname.replace(/\/$/, '') || '/';
    if (href === current) link.classList.add('active');
  });

  // Mobile hamburger toggle
  const toggle = document.querySelector('.nav-toggle');
  const navList = document.querySelector('nav ul');
  if (toggle && navList) {
    toggle.addEventListener('click', () => navList.classList.toggle('open'));
  }
})();
