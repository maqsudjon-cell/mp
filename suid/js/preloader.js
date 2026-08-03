/* ---------------------------------------------------------------------------
   preloader.js — §7.1

   fix 11: sui.io's preloader runs on every visit with no session guard and
   pushes LCP out each time.

   The counter is driven by two real signals — document.fonts.ready and
   window load — never by a timer. The 1200ms cap is a ceiling, not a
   schedule: if both signals land at 300ms the overlay leaves at 300ms. The
   wipe itself is CSS (clip-path, --d-wipe, --e-inout) so the exit cannot
   depend on GSAP having loaded.

   Returns a promise that resolves --d-overlap before the wipe finishes; that
   is the -0.3 overlap the hero timeline starts on.
   ------------------------------------------------------------------------ */

const SEEN = 'suid_seen';
const CAP  = 1200;

export function initPreloader({ wipe, overlap }){
  const el   = document.querySelector('[data-preloader]');
  const root = document.documentElement;
  const done = () => { root.dataset.preload = 'done'; };

  if(!el) return Promise.resolve();

  // Repeat visit in this session, or reduced-motion: never show it at all.
  const skip = root.dataset.preload === 'done' ||
               matchMedia('(prefers-reduced-motion: reduce)').matches;
  try{ sessionStorage.setItem(SEEN, '1'); }catch(e){}
  if(skip){ done(); return Promise.resolve(); }

  const out = el.querySelector('[data-pl-count]');
  let target = 0, shown = 0, raf = 0, closed = false;
  const t0 = performance.now();

  const signal = () => { target = Math.min(100, target + 50); };
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(signal);
  if(document.readyState === 'complete') signal();
  else addEventListener('load', signal, { once:true });

  return new Promise(resolve => {
    const finish = () => {
      if(closed) return;
      closed = true;
      cancelAnimationFrame(raf);
      out.textContent = '100';
      el.classList.add('is-out');
      setTimeout(resolve, Math.max(0, wipe - overlap));
      setTimeout(done, wipe);
    };

    const tick = now => {
      if(now - t0 >= CAP) target = 100;          // hard ceiling
      shown += (target - shown) * .18;
      if(target === 100 && 100 - shown < .8) shown = 100;
      out.textContent = String(Math.round(shown)).padStart(3, '0');
      if(shown >= 100){ finish(); return; }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);

    /* The cap has to hold even when no frame is delivered. Opened in a
       background tab, requestAnimationFrame is throttled to nothing, and an
       overlay that waits for a frame that never comes is an overlay that
       never leaves. */
    setTimeout(finish, CAP);
  });
}
