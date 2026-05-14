export async function onRequest(context) {
  const response = await context.next();
  const url = new URL(context.request.url);

  // Check if it's an HTML page or the root
  const isHtml = response.headers.get("content-type")?.includes("text/html") || url.pathname.endsWith("/") || url.pathname.endsWith(".html");

  if (!isHtml) {
    return response;
  }

  try {
    // Attempt to fetch the partials
    const [headerRes, footerRes] = await Promise.all([
      context.env.ASSETS.fetch(new URL("/header.html", url)),
      context.env.ASSETS.fetch(new URL("/footer.html", url))
    ]);

    const headerHtml = headerRes.ok ? await headerRes.text() : "<!-- Header Load Failed -->";
    const footerHtml = footerRes.ok ? await footerRes.text() : "<!-- Footer Load Failed -->";

    return new HTMLRewriter()
      .on("body", {
        element(el) {
          el.prepend(headerHtml, { html: true });
          el.append(footerHtml, { html: true });
        },
      })
      .transform(response);
  } catch (e) {
    // If there is an error, return a header showing the error message
    return new Response("Middleware Error: " + e.message, { status: 500 });
  }
}
