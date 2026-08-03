/* ---------------------------------------------------------------------------
   stack.js — §7.7, reference implementation from §8c, used as written.

   No scrub here — deliberate. Scrubbing would recompute three properties on
   six plates every frame. One trigger per card with a tween on state change
   is the same visual result at a fraction of the cost. This is precisely
   where sui.io gets heavy.
   ------------------------------------------------------------------------ */

export function initStack(mm){
  const section = document.querySelector('[data-stack]');
  if(!section) return;

  const plates = [...section.querySelectorAll('.plate')];
  const cards  = [...section.querySelectorAll('.card')];
  const dots   = [...section.querySelectorAll('.rail__dot')];
  const SEA    = getComputedStyle(document.documentElement)
                   .getPropertyValue('--sea').trim();
  let current = -1;

  function setActive(i){
    if(i === current) return;
    current = i;
    plates.forEach((plate,n)=>{
      const on = n === i;
      plate.classList.toggle('is-active',on);
      gsap.to(plate,{opacity:on?1:.26,duration:.45,ease:'power2.out',overwrite:'auto'});
      gsap.to(plate.querySelector('.plate__body'),
              {y:on?-8:0,duration:.5,ease:'power3.out',overwrite:'auto'});
      gsap.to(plate.querySelector('.plate__top'),
              {stroke:on?SEA:'rgba(0,0,0,0)',duration:.35,overwrite:'auto'});
    });
    dots.forEach((d,n)=>d.classList.toggle('is-active',n<=i));
  }

  mm.add('(prefers-reduced-motion: reduce)',()=>{
    section.dataset.motion = 'off';
    gsap.set(plates,{opacity:1,clearProps:'transform'});
    gsap.set(cards,{opacity:1,y:0});
    dots.forEach(d=>d.classList.add('is-active'));
  });

  /* §8c drives both of these with ScrollTrigger.create, and on a page with no
     pinned section that is exactly right. This page pins the manifesto for
     120vh directly above the stack, and every ScrollTrigger below that pin
     resolves its start to a scroll position 120vh short of the real one —
     measured, invariant under refresh(), refreshPriority, creation order and
     normalizeScroll. The plates ran two cards ahead of the card on screen.

     IntersectionObserver is not subject to that bookkeeping at all: it reports
     real geometry against the real viewport, so a pin above it cannot skew it.
     It is also cheaper than six triggers, which is the same argument §8c makes
     for not scrubbing. setActive and the reduced-motion branch are unchanged. */
  mm.add('(prefers-reduced-motion: no-preference)',()=>{
    gsap.set(cards,{opacity:0,y:32});

    const reveal = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{
        if(!e.isIntersecting) return;
        reveal.unobserve(e.target);                     // once
        e.target.style.willChange='transform, opacity';
        gsap.to(e.target,{opacity:1,y:0,duration:.42,ease:'power3.out',
          onComplete:()=>{e.target.style.willChange='';}});
      });
    },{rootMargin:'0px 0px -12% 0px'});                 // ≈ start:'top 88%'
    cards.forEach(card=>reveal.observe(card));

    /* A zero-height band at 45% of the viewport: the card crossing it owns the
       stack. Cards never overlap, so at most one can cross at a time, and the
       gaps between them simply keep the previous plate lit. */
    const line = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{
        if(e.isIntersecting) setActive(cards.indexOf(e.target));
      });
    },{rootMargin:'-45% 0px -55% 0px'});
    cards.forEach(card=>line.observe(card));

    setActive(0);
    return ()=>{ reveal.disconnect(); line.disconnect(); };   // matchMedia cleanup
  });
}
