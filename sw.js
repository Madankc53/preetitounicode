/* Service worker for converter.thenepal.io
 *
 * Goal: pages you have already opened keep working with no connection
 * (converters and date tools run in the browser), and you get a friendly
 * offline page for pages you have not opened yet.
 *
 * Strategy
 *  - Pages (navigations) and .html partials: network first, so you always see
 *    the newest version when online; fall back to the cached copy, then to
 *    /offline.html.
 *  - Other same-origin files (css, js, json, images, fonts): serve the cached
 *    copy immediately and refresh it in the background.
 *  - Anything from another site (ads, Google Fonts, CDNs, exchange rates) is
 *    never touched by this worker.
 *
 * To force every visitor to drop old caches after a big change, bump VERSION.
 */
const VERSION = 'v2';
const CORE_CACHE = 'thenepal-core-' + VERSION;
const RUNTIME_CACHE = 'thenepal-pages-' + VERSION;
const OFFLINE_URL = '/offline.html';
const MAX_RUNTIME_ENTRIES = 80;

// Small shell only. Each file is cached on its own, so one missing file can
// never stop the worker from installing.
const PRECACHE = [
  OFFLINE_URL,
  '/header.html',
  '/footer.html',
  '/components.js',
  '/search-database.js',
  '/search-engine.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CORE_CACHE).then((cache) =>
      Promise.allSettled(PRECACHE.map((url) => cache.add(new Request(url, { cache: 'reload' }))))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys
          .filter((k) => k.startsWith('thenepal-') && k !== CORE_CACHE && k !== RUNTIME_CACHE)
          .map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

function isCacheable(response) {
  // Only cache complete, direct, successful answers. A redirected response must
  // not be reused for a page navigation, and error pages must never be cached.
  return response && response.ok && response.status === 200 && response.type === 'basic' && !response.redirected;
}

async function trimCache(cacheName, max) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - max; i++) await cache.delete(keys[i]);
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (isCacheable(response)) {
      const copy = response.clone();
      caches.open(RUNTIME_CACHE).then((c) => c.put(request, copy)).then(() => trimCache(RUNTIME_CACHE, MAX_RUNTIME_ENTRIES));
    }
    return response;
  } catch (err) {
    const cached = await caches.match(request, { ignoreSearch: true });
    if (cached) return cached;
    if (request.mode === 'navigate') {
      const offline = await caches.match(OFFLINE_URL);
      if (offline) return offline;
    }
    return new Response('You are offline.', {
      status: 503,
      statusText: 'Offline',
      headers: { 'Content-Type': 'text/plain; charset=utf-8' },
    });
  }
}

async function staleWhileRevalidate(request) {
  const cached = await caches.match(request);
  const refresh = fetch(request)
    .then((response) => {
      if (isCacheable(response)) {
        const copy = response.clone();
        caches.open(RUNTIME_CACHE).then((c) => c.put(request, copy));
      }
      return response;
    })
    .catch(() => null);
  if (cached) return cached;
  const fresh = await refresh;
  return fresh || new Response('', { status: 504, statusText: 'Offline' });
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;       // never touch other sites
  if (url.pathname === '/sw.js') return;                  // always fetch the worker fresh

  const isPage = request.mode === 'navigate' || /\.html$/i.test(url.pathname) || url.pathname === '/sitemap.xml';
  event.respondWith(isPage ? networkFirst(request) : staleWhileRevalidate(request));
});
