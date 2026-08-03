/* ---------------------------------------------------------------------------
   counter.js — §7.3 metrics and §7.9 live repository count.

   Every number is already printed at its true value in the HTML, so the page
   is correct with no JavaScript and under reduced-motion. These functions
   reset a number to zero and count back up to the value that was printed.
   The animated glyphs are aria-hidden; a visually-hidden sibling carries the
   real figure, so a screen reader never hears a number mid-count.

   fix 7: sui.io prints $380,000,000 of TVL with no source and no date. The
   repository count is fetched at view time, cached for an hour, labelled
   live or cached, and degrades to the last verified figure offline.
   ------------------------------------------------------------------------ */

const KEY = 'suid_repos', TTL = 36e5;

const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

function onView(el, fn){
  if(!('IntersectionObserver' in window)){ fn(); return; }
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if(!e.isIntersecting) return;
      io.unobserve(e.target);
      fn();
    });
  }, { threshold:.4 });
  io.observe(el);
}

export function countTo(el, value, ms){
  const t0 = performance.now();
  const step = now => {
    const p = Math.min(1, (now - t0) / ms);
    el.textContent = String(Math.round(value * (1 - Math.pow(1 - p, 3))));
    if(p < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

/* Hero metrics — trigger on view, once. */
export function initCounters(ms){
  if(reduced()) return;
  document.querySelectorAll('[data-count]:not([data-repo-count])').forEach(el => {
    const value = Number(el.dataset.count);
    el.textContent = '0';
    onView(el, () => countTo(el, value, ms));
  });
}

/* Receipts — the number itself is live. */
export function initRepoCounter(ms){
  const el = document.querySelector('[data-repo-count]');
  if(!el) return;
  const vh  = document.querySelector('[data-repo-vh]');
  const src = document.querySelector('[data-repo-src]');
  const fallback = Number(el.dataset.count);

  const render = (value, state) => {
    if(vh)  vh.textContent  = value + ' public repositories';
    if(src) src.textContent = 'Source: GitHub API · ' + state;
    if(reduced()){ el.textContent = String(value); return; }
    el.textContent = '0';
    onView(el, () => countTo(el, value, ms));
  };

  let cached = null;
  try{ cached = JSON.parse(sessionStorage.getItem(KEY) || 'null'); }catch(e){}

  if(cached && Date.now() - cached.t < TTL){
    render(cached.v, 'cached');
  }else{
    fetch('https://api.github.com/users/maqsudjon-cell')
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(d => {
        try{ sessionStorage.setItem(KEY, JSON.stringify({ v:d.public_repos, t:Date.now() })); }catch(e){}
        render(d.public_repos, 'live');
      })
      .catch(() => render(fallback, 'cached'));
  }
}
