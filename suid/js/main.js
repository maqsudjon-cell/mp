/* ---------------------------------------------------------------------------
   main.js — chrome, Lenis, and the single gsap.matchMedia() every animation
   on this page registers through.

   Load order is deliberate:
     1. chrome (banner, nav, sticky header) — no dependencies, runs at once
     2. preloader — starts before anything can block it
     3. document.fonts.ready → split text → build motion
   Splitting before the webfont lands is the entire CLS risk on this page, so
   it waits. Everything else is already in its final state in the HTML, which
   is why the page is complete with the CDN blocked or JS off.
   ------------------------------------------------------------------------ */

import { initPreloader }   from './preloader.js';
import { splitAll }        from './split.js';
import { initMarquee }     from './marquee.js';
import { initCounters, initRepoCounter } from './counter.js';
import { initRotator }     from './rotator.js';
import { initStack }       from './stack.js';

const root = document.documentElement;
const cs   = getComputedStyle(root);

/* Two different questions, two different flags.
   .js         — set in <head>, before paint: scripts are allowed to run, so
                 the preloader is permitted to show.
   [data-ready] — set here: these modules actually executed. Opened straight
                 from the filesystem, a module script is blocked by CORS and
                 never runs even though scripts are enabled; the CSS fallbacks
                 (nav in flow, marquee wrapped, plates lit) hang off this, so
                 that case degrades exactly like JS being switched off. */
root.dataset.ready = '';

/* Every duration in this codebase lives in tokens.css. This is how JS reads
   one — the same way §8 reads --sea. */
const tok = name => {
  const v = cs.getPropertyValue(name).trim();
  return v.endsWith('ms') ? parseFloat(v) : parseFloat(v) * 1000;
};

/* GSAP eases are the token curves by another name:
   --e-out   cubic-bezier(.16,1,.3,1)   = easeOutExpo    = 'expo.out'
   --e-inout cubic-bezier(.76,0,.24,1)  ≈ easeInOutQuart = 'power3.inOut'   */
const E_OUT = 'expo.out';

const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;
const HAS_GSAP = typeof window.gsap !== 'undefined' &&
                 typeof window.ScrollTrigger !== 'undefined';

let lenis = null;

/* ============================================================ chrome ===== */

/* Banner — dismissed for good, and the head script applies the stored state
   before first paint so it never flashes on a return visit. */
const closeBanner = document.querySelector('[data-banner-close]');
closeBanner && closeBanner.addEventListener('click', () => {
  root.dataset.banner = 'off';
  try{ localStorage.setItem('suid_banner', 'off'); }catch(e){}
  const mark = document.querySelector('.wordmark');
  mark && mark.focus();                       // focus never lands on nothing
});

/* One nav, one DOM. The button only flips an attribute; CSS does the rest. */
const header = document.querySelector('[data-header]');
const navBtn = document.querySelector('[data-nav-toggle]');
const setNav = open => {
  header.dataset.open = String(open);
  navBtn.setAttribute('aria-expanded', String(open));
};
if(header && navBtn){
  navBtn.addEventListener('click', () => setNav(header.dataset.open !== 'true'));
  header.querySelectorAll('.nav a').forEach(a =>
    a.addEventListener('click', () => setNav(false)));
  addEventListener('keydown', e => {
    if(e.key === 'Escape' && header.dataset.open === 'true'){ setNav(false); navBtn.focus(); }
  });

  const onScroll = () => header.classList.toggle('is-stuck', scrollY > 80);
  addEventListener('scroll', onScroll, { passive:true });
  onScroll();
}

/* In-page links go through Lenis when it is running, native otherwise. */
document.addEventListener('click', e => {
  const a = e.target.closest && e.target.closest('a[href^="#"]');
  if(!a || !lenis) return;
  const id = a.getAttribute('href');
  if(id.length < 2) return;
  const target = document.querySelector(id);
  if(!target) return;
  e.preventDefault();
  lenis.scrollTo(target, { offset:-72 });
  history.replaceState(null, '', id);
});

/* ========================================================== sequence ===== */

const ready = initPreloader({ wipe: tok('--d-wipe'), overlap: tok('--d-overlap') });
const fonts = document.fonts ? document.fonts.ready : Promise.resolve();

fonts.then(() => {
  splitAll();
  build();
});

function build(){
  initCounters(tok('--t-count'));
  initRepoCounter(tok('--t-count-repo'));
  initRotator({ dwell: tok('--t-rot'), dur: tok('--d-rot') });
  initMarquee();

  /* No GSAP (blocked CDN, offline): the page keeps every final state it was
     served with. Nothing is hidden waiting for a tween that will never run. */
  if(!HAS_GSAP) return;

  gsap.registerPlugin(ScrollTrigger);

  /* fix 14: pinned sections + 100vh break when the mobile URL bar collapses.
     Every full-height box on this page is 100dvh, and touch scrolling is
     normalised so a collapsing URL bar cannot jump a pinned section. Scoped
     to touch on purpose: on wheel, Lenis is already the scroll authority and
     two normalisers would fight each other. */
  ScrollTrigger.normalizeScroll({ type:'touch', allowNestedScroll:true });

  if(!REDUCED && typeof Lenis !== 'undefined'){
    lenis = new Lenis({ lerp:.1, wheelMultiplier:1, syncTouch:false });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
  }

  /* Order matters, and not for style. ScrollTrigger measures in creation
     order, and the manifesto pin adds 120vh of scroll to everything below it.
     Register the pin first — it is the earlier section on the page — so the
     stack is measured in a document that already includes the pin's spacer. */
  const mm = gsap.matchMedia();
  motion(mm);
  initStack(mm);

  /* A deep link lands before the pinned manifesto exists. The browser jumps
     to #work, ScrollTrigger then inserts 120vh of pin spacer above it, and the
     visitor is left staring at the wrong section. Measure once the pins are
     in, and correct. */
  ScrollTrigger.refresh();
  if(location.hash) jumpTo(document.querySelector(location.hash));
}

function jumpTo(target){
  if(!target) return;
  const y = target.getBoundingClientRect().top + scrollY - 72;
  if(lenis) lenis.scrollTo(y, { immediate:true });
  else scrollTo(0, y);
}

/* ============================================================ motion ===== */

function motion(mm){
  const heroWords = gsap.utils.toArray('.hero__h1 .w>i');
  const SW = tok('--t-stagger-w') / 1000;      // .06 words
  const SC = tok('--t-stagger-c') / 1000;      // .09 cards and rows
  const SEC = tok('--d-sec') / 1000;
  const EL  = tok('--d-el') / 1000;

  /* Reduced motion is off, not fast: no scrub, no pin, no loop, and every
     element sits at its final value from the first frame. */
  mm.add('(prefers-reduced-motion: reduce)', () => {
    gsap.set(heroWords, { yPercent:0, opacity:1 });
    gsap.set('.hero__sub, .hero__cta, .metrics, .hero__caption', { opacity:1, y:0 });
    ready.then(() => {});
  });

  mm.add('(prefers-reduced-motion: no-preference)', () => {

    /* --- manifesto: one element, one property --------------------------
       Registered first, before anything below it on the page. A single
       background-position scrub on a background-clip:text gradient: no
       per-word spans, no layout, no paint beyond the text itself. */
    const line = document.querySelector('[data-highlight]');
    if(line){
      gsap.fromTo(line,
        { backgroundPosition:'100% 0' },
        { backgroundPosition:'0% 0', ease:'none',
          scrollTrigger:{
            trigger:'[data-manifesto]', start:'top top', end:'+=120%',
            pin:true, scrub:true, anticipatePin:1,
            /* This pin adds 120vh of scroll to everything below it, and
               ScrollTrigger measures in creation order. Any trigger below the
               manifesto that is registered before this one measures itself in
               a document 120vh shorter than the one being scrolled — which
               ran the stack's plates two cards ahead of the card on screen. */
            refreshPriority:1
          }});
    }

    /* --- hero ---------------------------------------------------------- */
    const tl = gsap.timeline({
      paused:true,
      onStart:()  => heroWords.forEach(w => w.style.willChange = 'transform'),
      onComplete:() => heroWords.forEach(w => w.style.willChange = '')
    });
    tl.from(heroWords, { yPercent:110, duration:SEC, ease:E_OUT, stagger:SW })
      .from('.hero__sub',     { y:20, opacity:0, duration:EL, ease:E_OUT }, .5)
      .from('.hero__cta',     { y:20, opacity:0, duration:EL, ease:E_OUT }, .58)
      .from('.metrics',       { y:20, opacity:0, duration:EL, ease:E_OUT }, .66)
      .from('.hero__caption', { opacity:0, duration:EL, ease:E_OUT }, .74);
    ready.then(() => tl.play());

    /* --- every other split heading ------------------------------------- */
    gsap.utils.toArray('[data-split]').forEach(h => {
      if(h.classList.contains('hero__h1')) return;
      const words = h.querySelectorAll('.w>i');
      gsap.from(words, {
        yPercent:110, duration:SEC, ease:E_OUT, stagger:SW,
        onStart:()    => words.forEach(w => w.style.willChange = 'transform'),
        onComplete:() => words.forEach(w => w.style.willChange = ''),
        scrollTrigger:{ trigger:h, start:'top 86%', once:true }
      });
    });

    /* --- method + capabilities rows ------------------------------------
       The hairline is a pseudo-element, so the tween runs on a custom
       property the pseudo-element reads. Default is 1: with no JS the rules
       are simply drawn. */
    const rows = gsap.utils.toArray('.row');
    const rowKids = rows.flatMap(r => [...r.children]);
    gsap.set(rows, { '--hair-x':0 });
    gsap.set(rowKids, { opacity:0, y:16 });
    ScrollTrigger.batch(rows, {
      start:'top 88%', once:true,
      onEnter: batch => {
        gsap.to(batch, { '--hair-x':1, duration:EL, ease:E_OUT, stagger:SC });
        gsap.to(batch.flatMap(r => [...r.children]),
                { opacity:1, y:0, duration:EL, ease:E_OUT, stagger:SC });
      }
    });

    /* --- receipts and contact furniture --------------------------------- */
    gsap.utils.toArray('.fact, .cv, .tile').forEach(el => {
      gsap.from(el, {
        opacity:0, y:16, duration:EL, ease:E_OUT,
        scrollTrigger:{ trigger:el, start:'top 92%', once:true }
      });
    });
  });
}
