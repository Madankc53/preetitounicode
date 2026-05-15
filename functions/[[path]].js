export async function onRequest(context) {
  const response = await context.next();
  
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("text/html")) {
    return response;
  }

  // 1. ADSENSE MAIN SCRIPT (Goes in <head>)
  const adsenseScript = `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1239173186536702" crossorigin="anonymous"></script>`;

  // 2. HEADER & NAVIGATION
  const headerHTML = `
    <header style="background: #1a202c; color: white; padding: 1rem 0; font-family: sans-serif;">
      <div style="max-width: 1000px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; padding: 0 1rem;">
        <div style="font-size: 1.5rem; font-weight: bold;">
          <a href="/" style="color: #63b3ed; text-decoration: none;">Converter<span style="color:white">.thenepal.io</span></a>
        </div>
        <nav>
          <a href="/" style="color: white; margin-left: 1.5rem; text-decoration: none;">Home</a>
          <a href="/units" style="color: white; margin-left: 1.5rem; text-decoration: none;">Units</a>
        </nav>
      </div>
    </header>
  `;

  // 3. TOP AD UNIT (Injected after header)
  const topAdHTML = `
    <div style="max-width: 1000px; margin: 1rem auto; padding: 0 1rem;">
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-1239173186536702"
           data-ad-slot="1642070334"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </div>
  `;

  // 4. FOOTER
  const footerHTML = `
    <footer style="background: #f7fafc; color: #4a5568; padding: 2rem 0; margin-top: 4rem; border-top: 1px solid #e2e8f0; text-align: center; font-family: sans-serif;">
      <p>&copy; ${new Date().getFullYear()} thenepal.io</p>
    </footer>
  `;

  return new HTMLRewriter()
    .on('head', {
      element(el) {
        // Puts the AdSense script in the head
        el.append(adsenseScript, { html: true });
      },
    })
    .on('body', {
      element(el) {
        // Prepend adds to the very top of <body> in order
        el.prepend(headerHTML, { html: true });
        el.prepend(topAdHTML, { html: true }); // This will appear right after header
        
        // Append adds to the bottom of <body>
        el.append(footerHTML, { html: true });
      },
    })
    .transform(response);
}
