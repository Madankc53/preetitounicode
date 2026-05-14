export async function onRequest(context) {
  const response = await context.next();
  
  // This looks for the closing </body> tag and injects the footer before it
  return new HTMLRewriter()
    .on("body", {
      element(el) {
        el.append(`
          <footer style="text-align:center; padding: 2rem; background: #222; color: white;">
            <p>Built with GitHub & Cloudflare Pages</p>
          </footer>
        `, { html: true });
      },
    })
    .transform(response);
}
