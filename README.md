# maqsudjon.com

Personal site of Maqsudjon Polatov — welder, student, producer.
Vanilla HTML + CSS + JS. No build step.

## ⚠️ Add your profile photo first

The site looks for the photo at this exact path:

```
assets/profile.jpg
```

**Steps:**

1. Take or pick a square photo (at least **360 × 360 px**, JPG format).
2. Rename it to exactly **`profile.jpg`** (lowercase, no extra extension like `.JPG.jpg`).
3. Drop it into the **`assets/`** folder, replacing the placeholder file that's already there.
4. Reload the page.

If the file is missing or the path is wrong, the site will gracefully fall back
to showing your initials ("MP") inside the circular frame — no broken-image
icon ever shows. But a real photo is much better.

> **Tip:** the CSS crops the image to a circle and adds a subtle amber ring,
> so a centered, well-lit headshot works best.

## Files

```
.
├── index.html       # all markup
├── styles.css       # theme + layout
├── script.js        # theme toggle, smooth scroll, updates loader
├── updates.json     # the only file you edit to post a new update
├── CNAME            # custom domain for GitHub Pages
├── README.md        # this file
└── assets/
    └── profile.jpg  # <-- replace with a real photo (square, ≥360×360, JPG)
```

Also drop a `favicon.ico` at the repo root when you have one.

## Local preview

No build step. Just serve the folder:

```bash
cd maqsudjon-site
python3 -m http.server 8000
# open http://localhost:8000
```

Opening `index.html` directly with `file://` will not work because the browser
blocks `fetch()` for `updates.json` over `file://`. Always go through a local
server.

## How to add a new update

1. Open `updates.json`.
2. Add a new entry at the **top** of the array:

```json
{
  "date": "2026-06-15",
  "title": "Started learning Japanese",
  "tag": "Personal",
  "body": "Today I bought my first Genki textbook. Korean opened doors I didn't know existed — Japanese might do the same. The plan is 30 minutes a day. No rush."
}
```

3. Commit and push. The site re-renders automatically.

### Field reference

| field   | required | format                                          |
|---------|----------|-------------------------------------------------|
| `date`  | yes      | ISO date `YYYY-MM-DD` (used for sorting)        |
| `title` | yes      | 5–10 words                                      |
| `tag`   | no       | one of: `Music`, `Teaching`, `Trucking`, `Personal`, `Tech` |
| `body`  | yes      | 1–3 short paragraphs. Use `\n\n` for paragraph breaks. |

Updates are sorted **newest first** automatically, so insertion order in the
file doesn't matter — but it's still cleaner to keep the newest on top.

## Deployment (GitHub Pages + Cloudflare DNS)

1. **Create the repo.** On GitHub, create a new public repository named exactly
   `maqsudjon-cell.github.io` (this is your user-site repo — must match your
   username).

2. **Push these files to `main`:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/maqsudjon-cell/maqsudjon-cell.github.io.git
   git push -u origin main
   ```

3. **Enable Pages.** In the repo, go to **Settings → Pages**:
   - Source: **Deploy from a branch**
   - Branch: `main` / root (`/`)
   - Save

4. **Set the custom domain.** Same Pages page:
   - Custom domain: `maqsudjon.com`
   - Save (this writes/reads the `CNAME` file in the repo)

5. **Configure Cloudflare DNS for `maqsudjon.com`:**

   Add **4 A records** for the apex (`@`), all set to **DNS only** (gray cloud):
   | Type | Name | Content            |
   |------|------|--------------------|
   | A    | @    | 185.199.108.153    |
   | A    | @    | 185.199.109.153    |
   | A    | @    | 185.199.110.153    |
   | A    | @    | 185.199.111.153    |

   Add **1 CNAME** for `www`, also **DNS only** (gray cloud):
   | Type  | Name | Content                       |
   |-------|------|-------------------------------|
   | CNAME | www  | maqsudjon-cell.github.io      |

   > The gray cloud (DNS-only) is important. The orange-cloud proxy interferes
   > with GitHub's HTTPS provisioning. You can flip it on later once HTTPS is
   > confirmed working.

6. **Wait 5–30 minutes** for DNS to propagate.

7. **Enable HTTPS.** Back in **Settings → Pages**, tick **Enforce HTTPS** once
   GitHub finishes provisioning the certificate. If the checkbox is grayed out,
   wait a bit longer and reload.

Done. The site is live at `https://maqsudjon.com`.

## Stack

- Vanilla HTML, CSS, JS (no framework, no build, no npm)
- Google Fonts: Space Grotesk, Inter, JetBrains Mono
- Hosted on GitHub Pages, DNS on Cloudflare
