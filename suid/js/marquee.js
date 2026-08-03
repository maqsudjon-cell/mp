/* ---------------------------------------------------------------------------
   marquee.js — §7.4

   fix 9: sui.io's logo wall mixes SVG, PNG and WEBP at inconsistent optical
   weight and ships no alt text.

   The wordmarks are written once in the HTML as a real list. The second track
   exists only to make the loop seamless, so it is cloned here rather than
   duplicated in the source, and it is hidden from assistive tech. The motion
   is one CSS keyframe on one transform; JS only decides when it may run.
   ------------------------------------------------------------------------ */

export function initMarquee(){
  const mq = document.querySelector('[data-marquee]');
  const track = mq && mq.querySelector('.mq__track');
  if(!track) return;

  const belt = document.createElement('div');
  belt.className = 'mq__belt';
  mq.appendChild(belt);
  belt.appendChild(track);

  const ghost = track.cloneNode(true);
  ghost.setAttribute('aria-hidden', 'true');
  ghost.removeAttribute('role');
  belt.appendChild(ghost);

  if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  mq.classList.add('is-live');

  let hovered = false, offscreen = false;
  const sync = () => mq.classList.toggle('is-paused', hovered || offscreen);

  mq.addEventListener('pointerenter', () => { hovered = true;  sync(); });
  mq.addEventListener('pointerleave', () => { hovered = false; sync(); });

  if('IntersectionObserver' in window){
    new IntersectionObserver(([e]) => { offscreen = !e.isIntersecting; sync(); })
      .observe(mq);
  }
}
