#!/usr/bin/env python3
"""One HTML page and one 1200x630 card per show, so a shared link has its own image."""
import html
import json
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data.js")
OG = os.path.join(ROOT, "og")
S = os.path.join(ROOT, "s")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W, H = 1200, 630
SITE = "https://maqsudjon.com/show"


def load():
    raw = open(DATA, encoding="utf-8").read()
    raw = raw[raw.index("["): raw.rindex("]") + 1]
    return json.loads(raw)


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(draw, text, size, max_w, bold=True):
    f = font(size, bold)
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines[:2]


def cover(src):
    im = Image.open(src).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (im.width - W) // 2
    top = max(0, (im.height - H) // 2 - 20)
    return im.crop((left, top, left + W, top + H))


def card(show):
    src = os.path.join(ROOT, show["slides"][0]["img"].lstrip("/"))
    im = cover(src)
    out = os.path.join(OG, show["id"] + ".jpg")
    im.save(out, quality=86, optimize=True)
    return out


def home():
    im = Image.new("RGB", (W, H), (243, 241, 236))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 18, H), fill=(242, 186, 22))
    d.text((72, 180), "MAQSUDJON", font=font(22, True), fill=(120, 116, 108))
    d.text((72, 230), "Show", font=font(92, True), fill=(24, 24, 22))
    d.text((72, 370), "Dars slaydlari.", font=font(32, False), fill=(24, 24, 22))
    im.save(os.path.join(OG, "home.jpg"), quality=86, optimize=True)


def page(show):
    title = show["title"]
    desc = " · ".join(p for p in (show.get("when"), show.get("sub")) if p)
    url = f"{SITE}/s/{show['id']}/"
    image = f"{SITE}/og/{show['id']}.jpg"
    esc = html.escape
    doc = f"""<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<base href="/show/">
<title>{esc(title)} · Show</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#f3f1ec">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Show">
<meta property="og:locale" content="uz_UZ">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:secure_url" content="{image}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap">
<link rel="stylesheet" href="app.css">
</head>
<body>
<div class="atmosphere" aria-hidden="true"><img src="wall.jpg" alt=""></div>
<div id="app"></div>
<script src="data.js?v=33"></script>
<script src="app.js?v=33"></script>
</body>
</html>
"""
    folder = os.path.join(S, show["id"])
    os.makedirs(folder, exist_ok=True)
    open(os.path.join(folder, "index.html"), "w", encoding="utf-8").write(doc)


def main():
    os.makedirs(OG, exist_ok=True)
    shows = load()
    home()
    for show in shows:
        card(show)
        page(show)
        print(show["id"])
    print("pages", len(shows))


if __name__ == "__main__":
    main()
