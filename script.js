/* =========================================================
   Maqsudjon Polatov — personal site
   Theme toggle, smooth scroll, updates loader
   ========================================================= */

(function () {
  'use strict';

  // ---------- Theme ----------
  const STORAGE_KEY = 'maqsudjon-theme';
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    document.querySelector('meta[name="theme-color"]').setAttribute(
      'content',
      theme === 'light' ? '#fafafa' : '#0a0a0a'
    );
  }

  const saved = localStorage.getItem(STORAGE_KEY);
  const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
  applyTheme(saved || (prefersLight ? 'light' : 'dark'));

  toggle.addEventListener('click', function () {
    const next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    applyTheme(next);
    localStorage.setItem(STORAGE_KEY, next);
  });

  // ---------- Smooth scroll (anchor links) ----------
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      const id = link.getAttribute('href').slice(1);
      const target = document.getElementById(id);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ---------- Updates ----------
  function formatDate(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return iso;
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function renderUpdates(updates) {
    const container = document.getElementById('updates-list');
    if (!updates.length) {
      container.innerHTML = '<p class="loading">No updates yet.</p>';
      return;
    }

    const sorted = updates.slice().sort(function (a, b) {
      return new Date(b.date) - new Date(a.date);
    });

    container.innerHTML = sorted.map(function (u) {
      const tag = u.tag ? '<span class="update-tag">' + escapeHtml(u.tag) + '</span>' : '';
      const paragraphs = escapeHtml(u.body)
        .split(/\n\n+/)
        .map(function (p) { return '<p>' + p.replace(/\n/g, '<br/>') + '</p>'; })
        .join('');
      var shareText = 'Check out: ' + escapeHtml(u.title);
      var shareUrl = encodeURIComponent(window.location.href + '?update=' + escapeHtml(u.date));
      return [
        '<article class="update">',
        '  <div class="update-meta">',
        '    <time datetime="' + escapeHtml(u.date) + '">' + escapeHtml(formatDate(u.date)) + '</time>',
        '    ' + tag,
        '  </div>',
        '  <h3>' + escapeHtml(u.title) + '</h3>',
        '  <div class="update-body">' + paragraphs + '</div>',
        '  <div class="update-actions">',
        '    <button class="btn-share" onclick="shareUpdate(\'' + escapeHtml(u.title) + '\', \'' + escapeHtml(u.date) + '\')" title="Share">↗ Share</button>',
        '    <span class="view-count"><span class="view-icon">○</span> <span id="views-' + u.date.replace(/-/g,'') + '">...</span></span>',
        '  </div>',
        '</article>'
      ].join('');
    }).join('');

    // Fade-in on scroll
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15 });
      container.querySelectorAll('.update').forEach(function (el) { io.observe(el); });
    } else {
      container.querySelectorAll('.update').forEach(function (el) { el.classList.add('visible'); });
    }
  }

  fetch('updates.json', { cache: 'no-cache' })
    .then(function (r) { return r.json(); })
    .then(renderUpdates)
    .catch(function () {
      document.getElementById('updates-list').innerHTML =
        '<p class="loading">Could not load updates.</p>';
    });


  // ---------- Share & View Counter ----------
  window.shareUpdate = function(title, date) {
    var text = "I just read: " + title + " - " + window.location.href;
    if (navigator.share) {
      navigator.share({ title: title, text: text, url: window.location.href });
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(function() {
        alert("Copied to clipboard!");
      });
    }
  };

  // Simple view counter using Cloudflare KV or a persistent counter
  (function() {
    var counts = {};
    // Initialize with mock data — replace with real API later
    var viewEls = document.querySelectorAll('[id^="views-"]');
    viewEls.forEach(function(el) {
      var key = el.id.replace('views-', '');
      var count = Math.floor(Math.random() * 50) + 10; // placeholder
      el.textContent = count + " views";
    });
  })();

})();