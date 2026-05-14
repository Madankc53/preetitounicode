export async function onRequest(context) {
  const url = new URL(context.request.url);
  const response = await context.next();

  try {
    // 1. Try to fetch the header/footer
    const headerRes = await context.env.ASSETS.fetch(new URL("/header.html", url));
    const footerRes = await context.env.ASSETS.fetch(new URL("/footer.html", url));

    // 2. If the files themselves are missing or 404, this will show a warning in your HTML source
    const headerHtml = headerRes.ok ? await headerRes.text() : "<!-- DEBUG: header.html not found -->";
    const footerHtml = footerRes.ok ? await footerRes.text() : "<!-- DEBUG: footer.html not found -->";

    return new HTMLRewriter()
      .on("body", {
        element(el) {
          el.prepend(headerHtml, { html: true });
          el.append(footerHtml, { html: true });
        },
      })
      .transform(response);
  } catch (err) {
    // 3. This will catch any code crashes
    return new Response(response.body, {
      ...response,
      headers: { ...response.headers, "X-Middleware-Error": err.message }
    });
  }
}
