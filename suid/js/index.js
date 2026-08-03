/* ---------------------------------------------------------------------------
   index.js — the "Everything else/" section.

   Renders from ./projects.json, never from markup, so the list can be edited
   by hand without touching a line of HTML. The count above the list is the
   manifest length, not a number typed into the page — the same reason §7.9
   fetches the repository total instead of hardcoding it.

   Every row reveals through revealOnce with the shared MOTION config: same
   620ms, same easing, same 0.08 stagger as the rest of the page. No new
   motion vocabulary here.
   ------------------------------------------------------------------------ */

import { MOTION, revealOnce } from './main.js';

const pad = n => String(n).padStart(2, '0');

export async function initIndex(){
  const root = document.querySelector('[data-index-list]');
  if(!root) return;

  let data;
  try{
    const r = await fetch('./projects.json');
    if(!r.ok) throw new Error(r.status);
    data = await r.json();
  }catch(e){
    root.innerHTML = '<p class="idx__empty mono">The project manifest could not be loaded. ' +
                     'It is readable at <a href="./projects.json">projects.json</a>.</p>';
    return;
  }

  const groups = data.groups || [];
  const total  = groups.reduce((n, g) => n + g.projects.length, 0);

  const count = document.querySelector('[data-index-count]');
  if(count) count.textContent = String(total);
  const stamp = document.querySelector('[data-index-stamp]');
  if(stamp && data.generated) stamp.textContent = 'verified ' + data.generated;

  let n = 0;
  const frag = document.createDocumentFragment();

  groups.forEach(group => {
    if(!group.projects.length) return;

    const block = document.createElement('div');
    block.className = 'idx__group';

    const head = document.createElement('h3');
    head.className = 'label idx__domain';
    head.textContent = group.domain;
    block.appendChild(head);

    const list = document.createElement('ul');
    list.className = 'idx__list';
    list.setAttribute('role', 'list');

    group.projects.forEach(p => {
      n += 1;
      const li = document.createElement('li');
      li.className = 'idx__row';

      const a = document.createElement('a');
      a.className = 'idx__link';
      a.href = p.url;
      a.target = '_blank';
      a.rel = 'noreferrer';

      const num = document.createElement('span');
      num.className = 'idx__n mono';
      num.setAttribute('aria-hidden', 'true');
      num.textContent = pad(n);

      const title = document.createElement('span');
      title.className = 'idx__t';
      title.textContent = p.title;

      const cat = document.createElement('span');
      cat.className = 'idx__c mono';
      cat.textContent = p.category || '';

      /* The visible URL is the hostname plus path, trimmed of its scheme —
         the anchor already carries the real address. */
      const url = document.createElement('span');
      url.className = 'idx__u mono';
      url.textContent = p.url.replace(/^https?:\/\//, '').replace(/\/$/, '');

      a.append(num, title, cat, url);
      li.appendChild(a);
      list.appendChild(li);
    });

    block.appendChild(list);
    frag.appendChild(block);
  });

  root.innerHTML = '';
  root.appendChild(frag);

  if(matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if(typeof gsap === 'undefined') return;

  const rows = [...root.querySelectorAll('.idx__row')];
  gsap.set(rows, { opacity:0, y:MOTION.y });
  revealOnce(rows, row => {
    gsap.to(row, { opacity:1, y:0, duration:MOTION.el, ease:MOTION.ease });
  }, '0px 0px -6% 0px');
}
