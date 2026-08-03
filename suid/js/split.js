/* ---------------------------------------------------------------------------
   split.js — accessible word splitter.

   fix 1 + 2: sui.io's splitter drops the whitespace between words, so its
   headings render as one token (Industrytransformationpoweredby Sui,
   Stay in theloop) and paste back with no spaces at all.

   The visual gutter is .25em of margin-right on the mask, exactly as specified
   — the layout never depends on white space. But a browser serialises a
   selection from rendered text, not from the DOM, and two adjacent
   inline-blocks with nothing between them serialise as one word. So each pair
   of masks is separated by a space inside a font-size:0 span: zero advance,
   zero contribution to the line box, nothing for the layout to rely on, and
   real spaces when the heading is copied out. Measured in the browser against
   four other candidates before it was chosen.

   The parent carries the whole string as aria-label and every generated span
   is hidden from assistive tech, so the heading is announced once, correctly.
   ------------------------------------------------------------------------ */

export function splitAll(root = document){
  root.querySelectorAll('[data-split]').forEach(splitWords);
}

export function splitWords(el){
  if(el.dataset.splitDone) return [];

  const text   = el.textContent.replace(/\s+/g, ' ').trim();
  const accent = (el.dataset.accent || '').toLowerCase();
  if(!el.getAttribute('aria-label')) el.setAttribute('aria-label', text);

  const words = text.split(' ');
  const frag  = document.createDocumentFragment();
  const inner = [];

  words.forEach((word, i) => {
    const mask = document.createElement('span');
    mask.className = 'w';
    mask.setAttribute('aria-hidden', 'true');

    const line = document.createElement('i');
    if(accent && word.replace(/[^\p{L}]/gu, '').toLowerCase() === accent) line.className = 'accent';
    line.textContent = word;

    mask.appendChild(line);
    frag.appendChild(mask);
    inner.push(line);

    if(i < words.length - 1){
      const gap = document.createElement('span');
      gap.className = 'sp';
      gap.setAttribute('aria-hidden', 'true');
      gap.textContent = ' ';
      frag.appendChild(gap);
    }
  });

  el.textContent = '';
  el.appendChild(frag);
  el.dataset.splitDone = '1';
  return inner;
}
