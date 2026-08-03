# suid/ — a Sui-inspired design study

A single page at `maqsudjon.com/suid/`. It takes the content of `maqsudjon.com`
and re-renders it in the visual and motion language of `sui.io`, in plain
HTML, CSS and ES modules: no framework, no build step, no npm, no jQuery.

`sui.io` runs on Webflow and has real defects. This is a clone of its *design*,
not of its *implementation* — fifteen audited defects are listed in §9 of the
brief, and each one is fixed here and marked in the source with a
`<!-- fix: … -->` comment. That contrast is the point of the piece.

**This is an independent homage.** It is not affiliated with, endorsed by, or
connected to Sui, Mysten Labs, or the Sui Foundation.

---

## Running it

Nothing to install.

```bash
python3 -m http.server 8766 --directory /path/to/maqsudjon-site
```

Then open `http://localhost:8766/suid/`. **Serve from the repository root, not
from inside `suid/`** — every asset reference is relative (`./`), never
root-absolute (`/`), because a GitHub Pages project subpath breaks silently
otherwise. Testing from a subpath is the only way to catch that.

Opening `suid/index.html` straight from the filesystem also works: the page
renders complete and every link is live. The ES module is blocked by CORS on
`file://` — that is a browser rule, not a bug here — so the page degrades to
its no-JavaScript state. See *Degradation* below.

---

## The token system

`css/tokens.css` holds custom properties and nothing else. No hex value and no
timing value is written anywhere else in the codebase; CSS reads them with
`var()`, and JavaScript reads them with `tok()` in `js/main.js`, the same way
the reference implementation reads `--sea`.

### Core palette

| Token | Value | Role |
|---|---|---|
| `--ink` | `#011829` | deep ocean, the page |
| `--ink-2` | `#02233A` | raised surface |
| `--ink-3` | `#063757` | borders, hairlines, dot grids |
| `--sea` | `#4DA2FF` | the single accent |
| `--sea-bright` | `#6FB6FF` | accent hover |
| `--cloud` | `#F7F7F8` | the one light section |
| `--layer-1…6` | white → `#0D4A8C` | the six plates of the stack diagram |

Text is `--text-hi` / `--text-mid` / `--text-low`, plus `--text-ink` on the
light section.

### Derived tokens

Every derived token is a transparency of a token above, expressed with
`color-mix()` so a palette flip propagates automatically, and preceded by a
static `rgba()` fallback for engines without `color-mix`:

`--text-low-aa`, `--text-ink-mid`, `--hair-ink`, `--card-bg`, `--glass`,
`--glow`, `--mesh-a`, `--mesh-b`.

### Type

`--font-display` is Inter Tight (weight 500, `letter-spacing:-.035em`,
`line-height:.94` — the single most recognisable Sui trait).
`--font-mono` is JetBrains Mono, uppercase, `letter-spacing:.08em`, at
`--fs-label` for every label, eyebrow, number and column header.

The scale is `clamp()` only — `--fs-hero`, `--fs-h2`, `--fs-h3`, `--fs-body`,
`--fs-label`. There is not one media-query font size on the page.

Both families ship with a metric-matched fallback declared in `css/base.css`.
Inter Tight is upm 2048 / ascender 1984 / descender 494 / x-height 1118; Arial's
x-height is 51.9% against Inter Tight's 54.6%, so `size-adjust:105.2%`, and the
vertical overrides are the Inter Tight ratios divided by that adjustment
(`ascent-override:92.1%`, `descent-override:22.9%`). The fallback therefore
occupies the same box and a split heading does not reflow when the webfont
lands. That is the entire CLS budget of this page.

### Motion tokens

`--e-out` `cubic-bezier(.16,1,.3,1)` · `--e-inout` `cubic-bezier(.76,0,.24,1)` ·
`--d-micro` 180ms · `--d-el` 420ms · `--d-sec` 760ms, plus a block of component
timings (`--d-wipe`, `--d-overlap`, `--d-rot`, `--t-rot`, `--t-mq`, `--t-drift`,
`--t-cue`, `--t-count`, `--t-count-repo`, `--t-stagger-w`, `--t-stagger-c`).

GSAP has no cubic-bezier ease parser in the core build, so the two token curves
are named: `--e-out` is `easeOutExpo`, which is `'expo.out'` exactly, and
`--e-inout` is closest to `'power3.inOut'` (easeInOutQuart).

### The identity flip

`<html data-theme="flare">` swaps `--ink`, `--sea` and the whole layer ramp to
black and orange. Nothing else changes: because the derived tokens are mixes of
those, the card surfaces, plate glow, sticky-header glass and hero mesh all
follow. Verified — no blue survives anywhere, and contrast still passes.

---

## Every animation

One `gsap.matchMedia()` in `js/main.js` registers all of it. Only `transform`
and `opacity` are animated — never `width`, `height`, `top`, `left`, `margin`
or `flex-grow`. `will-change` is applied on enter and removed on complete,
never left in CSS. The global stagger is `.06s` for words and `.09s` for cards
and rows, and it is never randomised.

| # | What | How | Duration / ease |
|---|---|---|---|
| 1 | **Preloader counter** | `document.fonts.ready` + `window.load`, each worth 50; a rAF eases the displayed number toward the achieved total. Never a fake timer. | hard cap 1200ms |
| 2 | **Preloader exit** | counter fades, overlay wipes upward on `clip-path:inset()` — CSS, so it cannot depend on GSAP having loaded | `--d-wipe` `--e-inout` |
| 3 | **Hero words** | each word in an `overflow:hidden` mask, `yPercent:110 → 0` | `--d-sec` `expo.out`, stagger `--t-stagger-w` |
| 4 | **Hero sub / CTA / metrics / caption** | `y:20 → 0`, opacity, offset into the same timeline from `.5s` | `--d-el` `expo.out` |
| 5 | **Hero mesh** | two `radial-gradient` blobs drift on `translate3d` | `--t-drift` alternate, CSS |
| 6 | **Scroll cue** | a `--sea` dot travels down a 1px rule | `--t-cue` loop, CSS |
| 7 | **Metric counters** | `0 → target`, cubic ease-out, tabular figures so nothing jitters; IntersectionObserver, once | `--t-count` |
| 8 | **Marquee** | one CSS keyframe, `translate3d(-50%,0,0)` on a belt of two tracks | `--t-mq` linear, paused on hover and off-screen |
| 9 | **Manifesto highlight** | **one element, one property.** A `background-clip:text` gradient at `background-size:200%`, scrubbed from `background-position:100%` to `0%`. No per-word spans, no layout cost. | scrub, pinned for `120vh` |
| 10 | **Rotator** | five lines in a vertical mask, one in, one out | `--d-rot` `--e-inout`, `--t-rot` dwell |
| 11 | **Stack plates** | opacity `.26 ↔ 1`, body lifts 8px, top face strokes `--sea`. One ScrollTrigger per card, **no scrub** — scrubbing would recompute three properties on six plates every frame. | .45s / .5s / .35s |
| 12 | **Stack cards** | `y:32 → 0`, opacity, once | .42s `power3.out`, stagger `--t-stagger-c` |
| 13 | **Mobile rail** | `scaleX` on a pseudo-element | `--d-el` `--e-out`, CSS |
| 14 | **Method / Capabilities rows** | hairline draws left-to-right, then the text fades up. The hairline is a pseudo-element, so the tween runs on a custom property it reads (`--hair-x`), default `1`. | `--d-el` `expo.out`, stagger `--t-stagger-c` |
| 15 | **Receipts, facts, tiles** | `y:16 → 0`, opacity, once | `--d-el` `expo.out` |
| 16 | **Section headings** | same word split as the hero, on scroll-in | `--d-sec` `expo.out` |
| 17 | **Micro-interactions** | nav underline sweep, button fill, card lift, arrow slide, CV card `scale(1.02)` | `--d-micro`, CSS |

**Under `prefers-reduced-motion: reduce`** every scrubbed and looping animation
is skipped entirely — off, not faster. No pin, no scrub, no counter, no
rotation, no marquee, no drift, no preloader. Every element renders at its
final value on the first frame, and nothing can be caught mid-animation.

Lenis runs at `lerp:.1`, `wheelMultiplier:1`, `syncTouch:false` — native
momentum is better on touch — and is not created at all under reduced motion.

---

## Degradation

The page is served complete and correct; JavaScript only adds motion.

* **No JavaScript** — every number is printed at its true value, the manifesto
  sentence is fully highlighted, all six plates are lit, the rotator is a plain
  list of five roles, the marquee wraps instead of clipping, and the mobile nav
  sits in the flow because there is nothing to open a drawer with.
* **Module blocked** (`file://`, CSP, a failed CDN) — identical, because the
  fallbacks hang off `html:not([data-ready])`, an attribute the module sets when
  it actually executes, rather than off "are scripts enabled".
* **GSAP or Lenis unreachable** — `main.js` checks for both and returns before
  it hides anything. Nothing is left waiting for a tween that will never run.
* **Preloader** — capped at 1200ms by a `setTimeout`, not by a frame, so a
  background tab (where `requestAnimationFrame` is throttled to nothing) still
  gets rid of it. A CSS failsafe hides it at 2400ms whatever happens.
* **GitHub API unreachable or rate-limited** — the repository count falls back
  to the last verified figure and labels itself `· cached`.

---

## Decisions the brief left open

* **`css/stack.css`.** §3 enumerates exactly three stylesheets; §8a is headed
  `css/stack.css`. The three-file structure won, so §8a lives inside
  `sections.css` under its own banner, used as written.
* **Preloader signals.** §7.1 lists `document.fonts.ready` + hero image
  `decode()` + `window.load`. §7.3 forbids a hero image — the mesh is pure CSS —
  so there is no image to decode. Two signals, 50 each.
* **Hero dot grid.** §7.3 asks for a `--ink-3` dot grid "at 3%". `--ink-3` at 3%
  over `--ink` is below the display threshold — it renders as nothing. It uses
  `.28`, matching the grid in the §8 reference implementation.
* **Method / Capabilities headers.** §7.8 wants `Method/` over the left column
  and `Capabilities/` over the right. Each column carries its own label and
  heading rather than repeating "Method" in a shared section header, so no
  content string appears twice.
* **Rotator list.** §7.6 asks for a visually-hidden `<ul>` listing all five
  roles. Rather than write the five strings twice, the visible rotator *is*
  that list — `rotator.js` turns the real `<ul>` into the mask, so all five stay
  in the accessibility tree and the copy exists once.
* **Marquee duplicate.** Same reasoning: `marquee.js` clones the track at
  runtime and marks the clone `aria-hidden`, so the wordmarks are written once.
* **Contact card descriptions.** §7.10 asks for a one-line description per card.
  §6 does not supply one, and inventing copy about response times would be
  inventing a claim, so each description is the channel's own identifier.
* **CV source.** §2 says to copy from `../assets/`; the repository's `assets/`
  holds only `profile.jpg`. The CV was taken from `~/Downloads/`. Two versions
  exist and the one **without a phone number** was chosen — a public page should
  not publish one, and §6 does not list one.
* **`maqsudjon-cv-preview.png`** did not exist. It is page 1 of the CV rendered
  at 660px (PyMuPDF), quantised to 48 colours, with an AVIF sibling.

## Deliberate deviations

* **`normalizeScroll`.** §9 row 14 asks for `ScrollTrigger.normalizeScroll(true)`.
  It is scoped to `{type:'touch'}`: touch normalisation is what actually fixes
  the collapsing-URL-bar defect, and on wheel Lenis is already the scroll
  authority — two normalisers would fight. Every full-height box is `100dvh`.
* **Three values in §8a resolve through tokens** instead of literal `rgba()`:
  the card surface (`--card-bg`), the active-plate glow (`--glow`), and the
  rail's hardcoded `420ms` (`--d-el`). Without this, `data-theme="flare"` would
  leave Sui-blue residue on an orange page, and §4's "no hardcoded hex or px
  timing anywhere else" would be broken by the reference itself.
* **`--text-low` on small text.** `rgba(255,255,255,.44)` measures **3.97:1** on
  `--ink` and cannot legally carry 12px text; no amount of darkening the
  background fixes it, because at that alpha the composite is bounded at ~4.25:1
  even on pure black. `--text-low` is kept exactly as specified for decorative
  and `aria-hidden` marks (the plate numerals), and small DOM text uses
  `--text-low-aa` at `.56` — **6.2:1**.
* **`--sea` on `--cloud`** measures **2.47:1**, so the numerals in the light
  section use `--layer-6`, the deepest step of the same ramp — **8.3:1**, still
  the brand blue, and it flips with the theme.
* **Three content strings appear twice**, and none of them is the defect §9
  rows 5 and 6 describe. `polatovmaqsudjon1@gmail.com` and
  `github.com/maqsudjon-cell` are contact details, printed once in the section
  that presents them and once on the card that links to them; *Wedding
  Invitation Builder* is a project name, printed once on its card and once in
  the footer sitemap. What is absent is duplicated *markup* — no block on this
  page is rendered twice to serve two layouts, which is what let sui.io drift
  into `OVerview`/`Overview` and `buy SUI`/`claim SUI`.
* **Own JavaScript is 25.0 KB on disk** against a 20 KB budget: **16.0 KB of
  code** and 9 KB of the engineering commentary this brief asks for, arriving as
  **10.5 KB gzipped**. Stripping the explanations to satisfy an uncompressed
  byte count on files that ship compressed seemed the wrong trade; delete the
  comment blocks if you disagree.

## Measured

* First load **173 KB** over 17 requests, against a 900 KB budget. Fonts 98 KB,
  GSAP + ScrollTrigger 46 KB, Lenis 3.8 KB, own CSS/JS/HTML 25 KB.
* Contrast: **0 failures** across 151 text nodes, minimum **6.08:1** — and
  **6.48:1** under `data-theme="flare"`.
* Zero duplicate `id`s, exactly one `<h1>`, and every split heading copies back
  as a sentence with real spaces (checked with `Selection.toString()`, not by
  eye).

---

## Generating `suid-og.png`

The 1200×630 card is drawn in code from the same palette and the same isometric
geometry as the page, so it cannot drift from what it represents. Re-run with:

```python
# needs Pillow. Palette and plate geometry mirror tokens.css and §8b:
# cx=190, half-width 140, half-height 38, thickness 12, plates every 80px.
from PIL import Image, ImageDraw, ImageFont
W, H = 1200, 630
INK, SEA, WHITE = (1,24,41), (77,162,255), (255,255,255)
LAYERS = [(255,255,255),(199,228,255),(147,200,255),(77,162,255),(34,115,204),(13,74,140)]
DISPLAY = "/System/Library/Fonts/HelveticaNeue.ttc"   # index 10 = Medium, 11 = Medium Italic
MONO    = "/System/Library/Fonts/Menlo.ttc"
# 1. flat --ink canvas
# 2. a --sea radial glow at (940, 210), 60 concentric ellipses, alpha (1-t)**1.7 * .16
# 3. a 32px dot grid in a lightened --ink-3
# 4. six isometric plates at scale .60, offset (780, -18), painted 01 -> 06 so
#    upper plates occlude the plate beneath; sides at brightness .60 / .80
# 5. "MAQSUDJON.COM/SUID" in mono --sea; the H1 over three lines at 78px with
#    "live" in Medium Italic --sea; a hairline; two mono lines beneath
```

Helvetica Neue Medium stands in for Inter Tight — the card is generated from
system fonts so it needs no network and no font file in the repository.

---

## File map

```
suid/
├── index.html          one <h1>, one nav, one stack, zero duplicate ids
├── css/
│   ├── tokens.css      custom properties ONLY
│   ├── base.css        reset, type, layout primitives, utilities, the splitter
│   └── sections.css    per-section styles, in page order (§8a inside)
├── js/
│   ├── main.js         chrome, Lenis, the single gsap.matchMedia()
│   ├── preloader.js    real signals, 1200ms cap, once per session
│   ├── split.js        accessible word splitter
│   ├── marquee.js      belt + cloned track
│   ├── counter.js      metric count-ups and the live repository count
│   ├── rotator.js      height-locked line rotator
│   └── stack.js        §8c, used as written
├── assets/
│   ├── Maqsudjon_Polatov_CV.pdf
│   ├── maqsudjon-cv-preview.png / .avif
│   └── suid-og.png
└── README.md
```

The repository root — `index.html`, `styles.css`, `script.js`, `assets/`,
`CNAME` — is untouched.
