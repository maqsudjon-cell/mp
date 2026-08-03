/* ---------------------------------------------------------------------------
   rotator.js — §7.6

   fix 8: sui.io rotates headings of unequal length and the container height
   jumps on every change. Here the tallest line is measured in the final
   layout width before anything moves, and min-height is locked to it —
   re-measured on resize, because the tallest line at 1440px is not the
   tallest line at 320px.

   The five roles live in the HTML as one real list. With no JavaScript, or
   under reduced-motion, that list simply renders in full. With JavaScript the
   same elements become the rotator, so the strings exist exactly once and all
   five stay in the accessibility tree.
   ------------------------------------------------------------------------ */

export function initRotator({ dwell, dur }){
  const list = document.querySelector('[data-rotator]');
  if(!list) return;

  const items = [...list.children];
  if(items.length < 2) return;

  list.setAttribute('aria-live', 'off');
  if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  list.classList.add('is-mask');

  const measure = () => {
    list.style.minHeight = '0px';
    let tallest = 0;
    items.forEach(li => {
      const t = li.style.transform, o = li.style.opacity, p = li.style.position;
      li.style.position = 'relative';
      li.style.transform = 'none';
      li.style.opacity = '0';
      tallest = Math.max(tallest, li.offsetHeight);
      li.style.position = p; li.style.transform = t; li.style.opacity = o;
    });
    list.style.minHeight = tallest + 'px';
  };
  measure();

  let resizeTimer;
  addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(measure, 150);
  }, { passive:true });

  let i = 0, timer = null, hovered = false, offscreen = false;
  items[0].classList.add('is-in');

  /* Send a line back below the mask with transitions suppressed, so it never
     animates downward through the visible area on its way to being reused. */
  const park = el => {
    el.style.transition = 'none';
    el.classList.remove('is-out');
    void el.offsetWidth;
    el.style.transition = '';
  };

  const step = () => {
    const current = items[i];
    const next = items[i = (i + 1) % items.length];
    current.classList.replace('is-in', 'is-out');
    next.classList.add('is-in');
    setTimeout(() => park(current), dur);
  };

  const run   = () => { if(!timer) timer = setInterval(step, dwell); };
  const halt  = () => { clearInterval(timer); timer = null; };
  const sync  = () => (hovered || offscreen) ? halt() : run();

  list.addEventListener('pointerenter', () => { hovered = true;  sync(); });
  list.addEventListener('pointerleave', () => { hovered = false; sync(); });
  list.addEventListener('focusin',      () => { hovered = true;  sync(); });
  list.addEventListener('focusout',     () => { hovered = false; sync(); });

  if('IntersectionObserver' in window){
    new IntersectionObserver(([e]) => { offscreen = !e.isIntersecting; sync(); })
      .observe(list);
  }else{
    run();
  }
}
