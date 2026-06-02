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
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute('content', theme === 'light' ? '#fafafa' : '#0a0a0a');
    }
  }

  const saved = localStorage.getItem(STORAGE_KEY);
  const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
  applyTheme(saved || (prefersLight ? 'light' : 'dark'));

  if (toggle) {
    toggle.addEventListener('click', function () {
      const next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      applyTheme(next);
      localStorage.setItem(STORAGE_KEY, next);
    });
  }

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
    var d = new Date(iso);
    if (isNaN(d)) return iso;
    return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function renderUpdates(updates) {
    var container = document.getElementById('updates-list');
    if (!container) return;

    if (!updates || !updates.length) {
      container.innerHTML = '<p class="loading">No updates yet. Check back soon!</p>';
      return;
    }

    var sorted = updates.slice().sort(function (a, b) {
      return new Date(b.date) - new Date(a.date);
    });

    container.innerHTML = sorted.map(function (u) {
      var tag = u.tag ? '<span class="update-tag">' + escapeHtml(u.tag) + '</span>' : '';
      var paragraphs = escapeHtml(u.body)
        .split(/\n\n+/)
        .map(function (p) { return '<p>' + p.replace(/\n/g, '<br/>') + '</p>'; })
        .join('');
      return [
        '<article class="update">',
        '  <div class="update-meta">',
        '    <time datetime="' + escapeHtml(u.date) + '">' + escapeHtml(formatDate(u.date)) + '</time>',
        '    ' + tag,
        '  </div>',
        '  <h3>' + escapeHtml(u.title) + '</h3>',
        '  <div class="update-body">' + paragraphs + '</div>',
        '</article>'
      ].join('');
    }).join('');

    // Fade-in on scroll
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
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

  // Fetch with 5-second timeout
  var container = document.getElementById('updates-list');

  function fetchWithTimeout(url, timeoutMs) {
    return Promise.race([
      fetch(url, { cache: 'no-cache' }),
      new Promise(function (_, reject) {
        setTimeout(function () { reject(new Error('Request timed out')); }, timeoutMs);
      })
    ]);
  }

  fetchWithTimeout('updates.json', 5000)
    .then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    })
    .then(renderUpdates)
    .catch(function () {
      if (container) {
        // Fallback: show latest static update so page never feels empty
        container.innerHTML = [
          '<article class="update visible">',
          '  <div class="update-meta">',
          '    <time datetime="2026-05-29">29 May 2026</time>',
          '    <span class="update-tag">IELTS</span>',
          '  </div>',
          '  <h3>IELTS Hub — 73 listening tests 🚀</h3>',
          '  <div class="update-body">',
          '    <p>Big update today! Added 35 new Diyorbek listening tests — Tests 41 through 76.</p>',
          '    <p>That brings the total to 73 listening tests on the platform. Check them out at <a href="https://pangea8.com" target="_blank" rel="noopener">pangea8.com</a>.</p>',
          '  </div>',
          '</article>',
          '<p class="loading">Could not load live updates. Showing latest saved entry.</p>'
        ].join('');
      }
    });

})();

/* =========================================================
   Share functions (global — used by inline onclick)
   ========================================================= */
function sharePage(platform) {
  var url = encodeURIComponent(window.location.href);
  var fullText = encodeURIComponent("Maqsudjon Polatov — IELTS Hub with 73 listening tests, music as Matsumi, and more. Check out maqsudjon.com and pangea8.com");

  if (platform === 'telegram') {
    window.open("https://t.me/share/url?url=" + url + "&text=" + fullText, "_blank", "width=600,height=400");
  } else if (platform === 'twitter') {
    window.open("https://twitter.com/intent/tweet?text=" + fullText + "&url=" + url, "_blank", "width=600,height=400");
  } else if (platform === 'copy') {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(window.location.href).then(function () {
        var btn = document.querySelector('.share-btn.copy');
        if (!btn) return;
        var orig = btn.innerHTML;
        btn.textContent = "Copied!";
        setTimeout(function () { btn.innerHTML = orig; }, 2000);
      });
    }
  }
}
