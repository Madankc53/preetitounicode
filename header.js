/**
 * thenepal.io — Shared Header
 * Usage: <script src="/header.js"></script>  (place just before </body>)
 * The script detects the current page and highlights the active nav link.
 */
(function () {
  // ── Nav links — add/edit here to update ALL pages ──────────────────
  const NAV_LINKS = [
    { href: 'https://thenepal.io',                             label: '🏠 Home' },
    { href: 'https://converter.thenepal.io/',                  label: '🔤 Preeti ↔ Unicode' },
    { href: 'https://converter.thenepal.io/date-converter/',   label: '📅 Date Converter',  badge: 'NEW' },
  ];

  // ── Detect active link ──────────────────────────────────────────────
  const currentURL = window.location.href;
  const isActive = (href) => currentURL.startsWith(href) && href !== 'https://thenepal.io'
    ? true
    : currentURL === href || currentURL === href + '/';

  // ── Build nav items HTML ────────────────────────────────────────────
  const navHTML = NAV_LINKS.map(link => {
    const active = isActive(link.href) ? ' class="active"' : '';
    const badge  = link.badge ? ` <span class="nav-badge">${link.badge}</span>` : '';
    return `<a href="${link.href}"${active}>${link.label}${badge}</a>`;
  }).join('');

  // ── Full header HTML ────────────────────────────────────────────────
  const headerHTML = `
<header id="site-header">
  <a href="https://thenepal.io" class="logo" title="thenepal.io">
    🇳🇵 Preeti<span class="logo-accent">Unicode</span>.io
  </a>
  <div class="header-right">
    <span class="privacy-badge">🔒 100% Private</span>
    <span class="header-badge">FREE Forever</span>
    <button class="dark-toggle" id="dark-toggle" onclick="siteHeaderToggleDark()" aria-label="Toggle dark mode">🌙</button>
  </div>
</header>
<nav class="tools-nav" aria-label="Nepali Tools">
  <span class="tools-nav-label">🛠 Tools</span>
  ${navHTML}
</nav>`;

  // ── Styles (injected once) ──────────────────────────────────────────
  const css = `
#site-header {
  background: var(--blue, #003893);
  color: white;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  position: sticky;
  top: 0;
  z-index: 200;
  box-shadow: 0 2px 16px rgba(0,0,0,0.2);
  gap: 10px;
}
#site-header .logo {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.3px;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  text-decoration: none;
  color: white;
}
#site-header .logo-accent { color: var(--gold, #D4AF37); }
#site-header .header-right { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
#site-header .header-badge,
#site-header .privacy-badge {
  font-size: 10px; padding: 4px 10px; border-radius: 20px; white-space: nowrap;
}
#site-header .header-badge {
  background: rgba(255,255,255,0.12); border: 1px solid rgba(255,255,255,0.2);
}
#site-header .privacy-badge {
  background: rgba(26,122,74,0.35); border: 1px solid rgba(26,122,74,0.5); color: #7ef5b4;
}
#site-header .dark-toggle {
  width: 34px; height: 34px; border-radius: 50%;
  border: 1.5px solid rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.08);
  cursor: pointer; font-size: 17px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s; color: white; flex-shrink: 0;
}
#site-header .dark-toggle:hover {
  background: rgba(255,255,255,0.18); border-color: rgba(255,255,255,0.5);
}
nav.tools-nav {
  background: rgba(0,0,0,0.25);
  border-top: 1px solid rgba(255,255,255,0.1);
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 4px;
  overflow-x: auto;
  scrollbar-width: none;
  background-color: var(--blue, #003893);
}
nav.tools-nav::-webkit-scrollbar { display: none; }
nav.tools-nav .tools-nav-label {
  font-size: 9px; font-weight: 600; letter-spacing: 1.2px;
  text-transform: uppercase; color: rgba(255,255,255,0.4);
  white-space: nowrap; padding-right: 8px;
  border-right: 1px solid rgba(255,255,255,0.15); margin-right: 4px;
}
nav.tools-nav a {
  color: rgba(255,255,255,0.7); text-decoration: none;
  font-size: 11px; font-weight: 500;
  padding: 7px 12px; white-space: nowrap;
  transition: all 0.2s;
  border-bottom: 2px solid transparent;
  display: flex; align-items: center; gap: 5px;
}
nav.tools-nav a:hover { color: white; background: rgba(255,255,255,0.08); }
nav.tools-nav a.active { color: white; border-bottom-color: var(--gold, #D4AF37); font-weight: 600; }
nav.tools-nav .nav-badge {
  font-size: 8px; background: #C0392B; color: white;
  padding: 1px 5px; border-radius: 8px; font-weight: 700;
}`;

  // ── Inject styles ───────────────────────────────────────────────────
  const styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ── Inject header before <body> content ────────────────────────────
  const wrapper = document.createElement('div');
  wrapper.innerHTML = headerHTML;
  document.body.insertBefore(wrapper, document.body.firstChild);

  // ── Dark mode: sync with whatever theme system the page uses ────────
  function syncToggleIcon() {
    const btn = document.getElementById('dark-toggle');
    if (!btn) return;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    btn.textContent = isDark ? '☀️' : '🌙';
  }

  window.siteHeaderToggleDark = function () {
    const html  = document.documentElement;
    const next  = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('preeti-theme', next);
    syncToggleIcon();
    // Also call the page's own toggleDarkMode if it exists
    if (typeof toggleDarkMode === 'function' && toggleDarkMode !== window.siteHeaderToggleDark) {
      // already handled above — avoid double-toggle
    }
  };

  // Apply saved theme on load
  const saved   = localStorage.getItem('preeti-theme');
  const prefers = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme   = saved || (prefers ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
  syncToggleIcon();
})();
