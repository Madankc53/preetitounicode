export async function onRequest(context) {
  const response = await context.next();
  const url = new URL(context.request.url);

  // Only process HTML pages
  if (!response.headers.get("content-type")?.includes("text/html")) {
    return response;
  }

  try {
    const [headerRes, footerRes] = await Promise.all([
      context.env.ASSETS.fetch(new URL("/header.html", url)),
      context.env.ASSETS.fetch(new URL("/footer.html", url))
    ]);

    const headerHtml = await headerRes.text();
    const footerHtml = await footerRes.text();

    // This is the logic you provided, wrapped for safety
    const headerLogic = `
    <script>
      (function() {
        const currentURL = window.location.href;
        document.querySelectorAll('#header-nav a').forEach(link => {
          if ((currentURL.startsWith(link.href) && link.href !== 'https://thenepal.io/') || currentURL === link.href) {
            link.classList.add('active');
          }
        });
        window.siteHeaderToggleDark = function () {
          const html = document.documentElement;
          const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
          html.setAttribute('data-theme', next);
          localStorage.setItem('preeti-theme', next);
          document.getElementById('dark-toggle').textContent = next === 'dark' ? '☀️' : '🌙';
        };
        const saved = localStorage.getItem('preeti-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', saved);
        document.getElementById('dark-toggle').textContent = saved === 'dark' ? '☀️' : '🌙';
      })();
    </script>`;

    return new HTMLRewriter()
      .on("body", {
        element(el) {
          el.prepend(headerHtml, { html: true }); // Put Header at top
          el.append(footerHtml, { html: true });  // Put Footer at bottom
          el.append(headerLogic, { html: true }); // Activate Scripts
        },
      })
      .transform(response);
  } catch (e) {
    return response;
  }
}
