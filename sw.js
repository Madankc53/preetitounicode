// sw.js for GitHub Pages
const CACHE_NAME = 'my-site-cache-v1';
const OFFLINE_URL = '/offline.html';

// Files to cache for offline access
const urlsToCache = [
  '/',
  '/index.html',
  '/offline.html',
  '/styles.css',    // Add your CSS files
  '/script.js',     // Add your JS files
  '/manifest.json'  // If you have a web app manifest
];

// Install event - cache essential files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache first, fall back to network
self.addEventListener('fetch', event => {
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }

        // Clone the request because it's a one-time use stream
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(response => {
          // Check if we received a valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response because it's a one-time use stream
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then(cache => {
              // Don't cache if it's a Chrome extension request
              if (!event.request.url.includes('chrome-extension')) {
                cache.put(event.request, responseToCache);
              }
            });

          return response;
        }).catch(error => {
          // If both cache and network fail, show offline page
          if (event.request.mode === 'navigate') {
            return caches.match(OFFLINE_URL);
          }
          return new Response('Offline content not available', {
            status: 503,
            statusText: 'Service Unavailable'
          });
        });
      })
  );
});
// In your sw.js urlsToCache array
const urlsToCache = [
  '/',
  '/index.html',
  '/offline.html',
  '/manifest.json',
  '/assets/css/main.css',
  '/assets/css/components.css',
  '/assets/css/animations.css'
];
// In your sw.js urlsToCache array
const urlsToCache = [
  '/',
  '/index.html',
  '/offline.html',
  '/manifest.json',
  '/assets/css/main.css',
  '/assets/css/fonts.css',
  '/assets/js/common.js',
  '/assets/fonts/Preeti.woff2',  // Add your font
  '/assets/fonts/Preeti.woff',    // Fallback format
  '/assets/fonts/Preeti.ttf'      // Fallback format
];
