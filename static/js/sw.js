/**
 * Service Worker for BOM System PWA
 * Provides offline functionality, caching, and performance improvements
 */

const CACHE_NAME = 'bom-system-v1';
const STATIC_CACHE_NAME = 'bom-static-v1';
const DYNAMIC_CACHE_NAME = 'bom-dynamic-v1';

// Files to cache immediately
const STATIC_FILES = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  'https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/materia/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  'https://unpkg.com/htmx.org@1.9.2'
];

// Routes to cache dynamically
const DYNAMIC_ROUTES = [
  '/dashboard/',
  '/masters/fabrics/',
  '/masters/accessories/',
  '/styles/',
  '/orders/',
  '/purchase/',
  '/reports/'
];

// Network-first routes (always try network first)
const NETWORK_FIRST_ROUTES = [
  '/api/',
  '/admin/',
  '/auth/'
];

// Install event - cache static files
self.addEventListener('install', event => {
  console.log('Service Worker: Installing...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Service Worker: Static files cached successfully');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('Service Worker: Error caching static files:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker: Activating...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== STATIC_CACHE_NAME && cacheName !== DYNAMIC_CACHE_NAME) {
              console.log('Service Worker: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker: Activated successfully');
        return self.clients.claim();
      })
  );
});

// Fetch event - handle requests with different strategies
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip chrome-extension and other non-http requests
  if (!request.url.startsWith('http')) {
    return;
  }
  
  // Handle different types of requests
  if (isStaticFile(request.url)) {
    // Cache first strategy for static files
    event.respondWith(cacheFirstStrategy(request));
  } else if (isNetworkFirstRoute(request.url)) {
    // Network first strategy for API and admin routes
    event.respondWith(networkFirstStrategy(request));
  } else if (isDynamicRoute(request.url)) {
    // Stale while revalidate for dynamic content
    event.respondWith(staleWhileRevalidateStrategy(request));
  } else {
    // Default to network first
    event.respondWith(networkFirstStrategy(request));
  }
});

// Cache first strategy - good for static assets
function cacheFirstStrategy(request) {
  return caches.match(request)
    .then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }
      
      return fetch(request)
        .then(networkResponse => {
          // Cache the response for future use
          if (networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(STATIC_CACHE_NAME)
              .then(cache => {
                cache.put(request, responseClone);
              });
          }
          return networkResponse;
        })
        .catch(() => {
          // Return offline fallback if available
          return getOfflineFallback(request);
        });
    });
}

// Network first strategy - good for dynamic content that needs to be fresh
function networkFirstStrategy(request) {
  return fetch(request)
    .then(networkResponse => {
      // Cache successful responses
      if (networkResponse.status === 200) {
        const responseClone = networkResponse.clone();
        caches.open(DYNAMIC_CACHE_NAME)
          .then(cache => {
            cache.put(request, responseClone);
          });
      }
      return networkResponse;
    })
    .catch(() => {
      // Fallback to cache if network fails
      return caches.match(request)
        .then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return getOfflineFallback(request);
        });
    });
}

// Stale while revalidate strategy - serve from cache, update in background
function staleWhileRevalidateStrategy(request) {
  return caches.match(request)
    .then(cachedResponse => {
      const fetchPromise = fetch(request)
        .then(networkResponse => {
          if (networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(DYNAMIC_CACHE_NAME)
              .then(cache => {
                cache.put(request, responseClone);
              });
          }
          return networkResponse;
        })
        .catch(() => {
          // If network fails and we have cache, return cache
          if (cachedResponse) {
            return cachedResponse;
          }
          return getOfflineFallback(request);
        });
      
      // Return cached response immediately if available, otherwise wait for network
      return cachedResponse || fetchPromise;
    });
}

// Helper functions
function isStaticFile(url) {
  return url.includes('/static/') || 
         url.includes('.css') || 
         url.includes('.js') || 
         url.includes('.png') || 
         url.includes('.jpg') || 
         url.includes('.jpeg') || 
         url.includes('.gif') || 
         url.includes('.svg') || 
         url.includes('.ico') || 
         url.includes('bootstrap') || 
         url.includes('htmx');
}

function isNetworkFirstRoute(url) {
  return NETWORK_FIRST_ROUTES.some(route => url.includes(route));
}

function isDynamicRoute(url) {
  return DYNAMIC_ROUTES.some(route => url.includes(route));
}

function getOfflineFallback(request) {
  const url = new URL(request.url);
  
  // Return offline page for navigation requests
  if (request.mode === 'navigate') {
    return caches.match('/offline.html')
      .then(response => {
        if (response) {
          return response;
        }
        // Create a simple offline response
        return new Response(
          `<!DOCTYPE html>
          <html>
          <head>
            <title>Offline - BOM System</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
              body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
              .offline-container { max-width: 400px; margin: 0 auto; }
              .offline-icon { font-size: 64px; margin-bottom: 20px; }
              h1 { color: #333; }
              p { color: #666; line-height: 1.5; }
              .retry-btn { 
                background: #007bff; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 5px; 
                cursor: pointer; 
                margin-top: 20px;
              }
            </style>
          </head>
          <body>
            <div class="offline-container">
              <div class="offline-icon">📱</div>
              <h1>You're Offline</h1>
              <p>It looks like you're not connected to the internet. Please check your connection and try again.</p>
              <button class="retry-btn" onclick="window.location.reload()">Retry</button>
            </div>
          </body>
          </html>`,
          {
            headers: {
              'Content-Type': 'text/html',
              'Cache-Control': 'no-cache'
            }
          }
        );
      });
  }
  
  // Return a simple error response for other requests
  return new Response(
    JSON.stringify({
      error: 'Offline',
      message: 'This content is not available offline'
    }),
    {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
      },
      status: 503
    }
  );
}

// Background sync for form submissions
self.addEventListener('sync', event => {
  console.log('Service Worker: Background sync triggered:', event.tag);
  
  if (event.tag === 'background-sync-form') {
    event.waitUntil(syncFormData());
  }
});

// Sync form data when back online
function syncFormData() {
  return new Promise((resolve, reject) => {
    // Get pending form submissions from IndexedDB
    // This would require implementing IndexedDB storage for offline form submissions
    console.log('Service Worker: Syncing form data...');
    resolve();
  });
}

// Push notification handling
self.addEventListener('push', event => {
  console.log('Service Worker: Push notification received');
  
  const options = {
    body: event.data ? event.data.text() : 'New notification from BOM System',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View',
        icon: '/static/icons/checkmark.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/icons/xmark.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('BOM System', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  console.log('Service Worker: Notification clicked');
  
  event.notification.close();
  
  if (event.action === 'explore') {
    // Open the app
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Message handling from main thread
self.addEventListener('message', event => {
  console.log('Service Worker: Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(DYNAMIC_CACHE_NAME)
        .then(cache => {
          return cache.addAll(event.data.urls);
        })
    );
  }
});

// Periodic background sync (if supported)
self.addEventListener('periodicsync', event => {
  console.log('Service Worker: Periodic sync triggered:', event.tag);
  
  if (event.tag === 'content-sync') {
    event.waitUntil(syncContent());
  }
});

function syncContent() {
  // Sync critical content in the background
  return fetch('/api/sync/')
    .then(response => response.json())
    .then(data => {
      console.log('Service Worker: Content synced:', data);
    })
    .catch(error => {
      console.error('Service Worker: Content sync failed:', error);
    });
}

// Cache management utilities
function cleanupCaches() {
  return caches.open(DYNAMIC_CACHE_NAME)
    .then(cache => {
      return cache.keys()
        .then(requests => {
          // Remove old entries (keep last 50)
          if (requests.length > 50) {
            const requestsToDelete = requests.slice(0, requests.length - 50);
            return Promise.all(
              requestsToDelete.map(request => cache.delete(request))
            );
          }
        });
    });
}

// Run cleanup periodically
setInterval(cleanupCaches, 24 * 60 * 60 * 1000); // Once per day

console.log('Service Worker: Script loaded successfully');