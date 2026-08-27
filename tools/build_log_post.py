#!/usr/bin/env python3
"""
Build log yozuvini yasaydi.

Mavjud yozuvlar bitta `.body` bloki ichida `white-space: pre-wrap` bilan
yozilgan — rasm qo'shib bo'lmaydi. Bu skript o'sha ko'rinishni saqlab,
ikkita narsa qo'shadi:

  · <figure> — skrinshot va izoh
  · til juftligi — har bir yozuvning EN va UZ nusxasi bir-biriga ishora
    qiladi (hreflang bilan), qolgan sayt ingliz tilida qolaveradi.

    python3 tools/build_log_post.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://maqsudjon.com"

SHELL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Maqsudjon Polatov — build log</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="{lang}" href="{url}">
<link rel="alternate" hreflang="{other_lang}" href="{other_url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#000000">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<link href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@500;600&family=Geist:wght@400;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">{ld}</script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#000;color:#ffffffbb;font-family:'Geist',system-ui,sans-serif;line-height:1.7}}
.wrap{{max-width:720px;margin:0 auto;padding:48px 24px 80px}}
a{{color:#fff;font-weight:600;text-decoration:underline;text-decoration-color:#4d4d4d;text-underline-offset:4px}}
a:hover{{text-decoration-color:#fff}}
.top{{display:flex;justify-content:space-between;gap:14px;font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#888;margin-bottom:46px}}
.top a{{color:#888;font-weight:400;text-decoration:none}}
.top a:hover{{color:#fff}}
.meta{{font-family:'Geist Mono',monospace;font-size:12px;letter-spacing:.1em;color:#888;margin-bottom:14px}}
.meta b{{color:#f2d8cd;font-weight:500;border:1px solid #4d4d4d;padding:2px 7px;margin-left:8px}}
.meta .alt{{float:right;color:#888;font-weight:400;text-decoration:none;border:1px solid #4d4d4d;padding:2px 7px}}
.meta .alt:hover{{color:#fff;border-color:#fff}}
h1{{font-family:'Funnel Display',sans-serif;font-weight:600;font-size:clamp(24px,5vw,34px);line-height:1.2;color:#fff;margin-bottom:26px;letter-spacing:-.01em}}
h2{{font-family:'Funnel Display',sans-serif;font-weight:600;font-size:19px;color:#fff;margin:40px 0 14px;letter-spacing:-.01em}}
.body{{font-size:16px}}
.body p{{margin-bottom:18px}}
.body ul{{margin:0 0 18px 20px}}
.body li{{margin-bottom:7px}}
.lede{{color:#ffffffdd;font-size:17px}}
code{{font-family:'Geist Mono',monospace;font-size:.86em;color:#f2d8cd;background:#141414;border:1px solid #262626;border-radius:4px;padding:1px 5px;overflow-wrap:anywhere}}
strong{{color:#fff;font-weight:600}}
em{{color:#ffffffdd}}
figure{{margin:26px 0 30px}}
figure img{{width:100%;height:auto;display:block;border:1px solid #2a2a2a;border-radius:6px;background:#111}}
figcaption{{font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.08em;color:#888;margin-top:10px;line-height:1.6}}
.pair{{display:grid;gap:12px;grid-template-columns:1fr}}
@media(min-width:620px){{.pair{{grid-template-columns:1fr 1fr}}}}
.pair img{{border-radius:6px}}
.foot{{margin-top:44px;border-top:1px solid #4d4d4d;padding-top:20px;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#888}}
.foot a{{color:#888;font-weight:400;text-decoration:none}}
::selection{{background:#fff;color:#000}}</style>
</head>
<body>
<div class="wrap">
  <nav class="top"><a href="/">✳ MAQSUDJON POLATOV</a><a href="/log/">BUILD LOG</a></nav>
  <div class="meta">{datestr}<b>{cat}</b><a class="alt" href="{other_url}">{other_label}</a></div>
  <h1>{title}</h1>
  <div class="body">
{body}
  </div>
  <div class="foot"><a href="/log/">{back}</a> · <a href="/feed.xml">RSS</a> · © 2026 Maqsudjon Polatov</div>
</div>
<script data-goatcounter="https://maqsudjon.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def fig(src, caption, alt):
    return (f'<figure><img src="/log/img/{src}" alt="{html.escape(alt)}" loading="lazy">'
            f'<figcaption>{caption}</figcaption></figure>')


def pair(a, b, caption, alt_a, alt_b):
    return (f'<figure><div class="pair">'
            f'<img src="/log/img/{a}" alt="{html.escape(alt_a)}" loading="lazy">'
            f'<img src="/log/img/{b}" alt="{html.escape(alt_b)}" loading="lazy">'
            f'</div><figcaption>{caption}</figcaption></figure>')


def build(slug, lang, title, desc, datestr, iso, cat, body,
          other_slug, other_label, back, og="/og-image.png"):
    url = f"{BASE}/log/{slug}.html"
    other_url = f"{BASE}/log/{other_slug}.html"
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": title, "description": desc, "datePublished": iso,
        "inLanguage": lang, "mainEntityOfPage": url,
        "image": BASE + og,
        "author": {"@type": "Person", "name": "Maqsudjon Polatov",
                   "url": "https://maqsudjon.com/"},
    }, ensure_ascii=False)
    out = SHELL.format(
        lang=lang, other_lang="uz" if lang == "en" else "en",
        title=html.escape(title), desc=html.escape(desc),
        url=url, other_url=other_url, other_label=other_label,
        og=BASE + og, ld=ld, datestr=datestr, cat=cat, body=body, back=back)
    p = ROOT / "log" / f"{slug}.html"
    p.write_text(out)
    return p
