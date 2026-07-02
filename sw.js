/* maqsudjon.com service worker — offline shell, cache-first assets */
const CACHE = 'mp-v2';
const SHELL = ['./', './index.html', './profile.jpg', './favicon.svg', './og-image.png'];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;
  // never intercept video — range requests break through SW
  if (url.pathname.endsWith('.mp4')) return;
  // pages: network-first with cached shell fallback (offline)
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).then(r => {
        const cp = r.clone();
        caches.open(CACHE).then(c => c.put('./index.html', cp));
        return r;
      }).catch(() => caches.match('./index.html'))
    );
    return;
  }
  // static assets: cache-first
  e.respondWith(
    caches.match(e.request).then(m => m || fetch(e.request).then(r => {
      if (r.ok && /\.(png|jpg|svg|ico|webmanifest|pdf)$/.test(url.pathname)) {
        const cp = r.clone();
        caches.open(CACHE).then(c => c.put(e.request, cp));
      }
      return r;
    }))
  );
});
