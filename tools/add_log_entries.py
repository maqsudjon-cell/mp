#!/usr/bin/env python3
"""Build log yozuvini bir vaqtda ikkala joyga qo'shadi.

Sayt ikkita joyda bir xil ro'yxatni ko'rsatadi:
  · bosh sahifadagi jonli feed  — index.html ichidagi `updates` massivi
  · /log/ arxivi                — har bir yozuv alohida HTML sahifa

Bu ikkisi ajralib ketmasligi kerak. Skript bitta manbadan ikkalasini ham
yasaydi, ustiga /log/index.html, feed.xml va sitemap.xml ni yangilaydi.

    python3 tools/add_log_entries.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://maqsudjon.com"
OYLAR = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
HAFTA = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']


def sana(d):
    y, m, dd = d.split('-')
    return f"{dd} {OYLAR[int(m)-1]} {y}"


def rfc(d):
    import datetime
    dt = datetime.date.fromisoformat(d)
    return f"{HAFTA[dt.weekday()]}, {dt.day:02d} {OYLAR[dt.month-1].capitalize()} {dt.year} 12:00:00 +0500"


def ankor(entry):
    """Bosh sahifadagi JS bilan bir xil id yasaydi (feed render funksiyasi)."""
    t = re.sub(r'[^a-z0-9]+', '-', entry["title"].lower()).strip('-')[:32]
    return f'log-{entry["date"]}-{t}'


SAHIFA = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Maqsudjon Polatov — build log</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#000000">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Maqsudjon Polatov">
<meta property="og:image" content="{BASE}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/og-image.png">
<meta name="author" content="Maqsudjon Polatov">
<meta property="article:published_time" content="{date}">
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
h1{{font-family:'Funnel Display',sans-serif;font-weight:600;font-size:clamp(24px,5vw,34px);line-height:1.2;color:#fff;margin-bottom:26px;letter-spacing:-.01em}}
.body{{white-space:pre-wrap;font-size:16px}}
.foot{{margin-top:44px;border-top:1px solid #4d4d4d;padding-top:20px;font-family:'Geist Mono',monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#888}}
.foot a{{color:#888;font-weight:400;text-decoration:none}}
::selection{{background:#fff;color:#000}}</style>
</head>
<body>
<div class="wrap">
  <nav class="top"><a href="/">✳ MAQSUDJON POLATOV</a><a href="/log/">BUILD LOG</a></nav>
  <div class="meta">{datestr}<b>{tag}</b></div>
  <h1>{title}</h1>
  <div class="body">{body}</div>
  <div class="foot"><a href="/#{anchor}">Open in the live build log →</a> · <a href="/feed.xml">RSS</a> · © 2026 Maqsudjon Polatov</div>
</div>
<script data-goatcounter="https://maqsudjon.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def sahifa_yoz(e):
    """Bitta /log/ sahifasini yozadi. `havolalar` matndagi so'zni <a> ga aylantiradi."""
    desc = e["body"].split("\n\n")[0][:155]
    body = html.escape(e["body"], quote=False).replace("'", "&#x27;")
    for matn, url in e.get("havolalar", {}).items():
        body = body.replace(matn, f'<a href="{url}" rel="noopener">{matn}</a>', 1)
    url = f'{BASE}/log/{e["slug"]}.html'
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": e["title"], "description": desc, "datePublished": e["date"],
        "inLanguage": "en", "mainEntityOfPage": url, "image": f"{BASE}/og-image.png",
        "author": {"@type": "Person", "name": "Maqsudjon Polatov",
                   "url": "https://maqsudjon.com/"}}, ensure_ascii=False)
    (ROOT / "log" / f'{e["slug"]}.html').write_text(SAHIFA.format(
        title=html.escape(e["title"]), desc=html.escape(desc), url=url, BASE=BASE,
        ld=ld, datestr=sana(e["date"]), tag=e["tag"], body=body,
        anchor=ankor(e), date=e["date"]))

# ── Yozuvlar ────────────────────────────────────────────────────────────────
# `sahifa=False` — /log/ sahifasi allaqachon bor, faqat bosh sahifaga qo'shiladi.

YOZUVLAR = [
{
 "date": "2026-07-21", "tag": "Tech", "sahifa": True,
 "slug": "log-2026-07-21-ctn-language-centre",
 "title": "CTN Language Centre — ctnlc.uz, built as one file",
 "havolalar": {"ctnlc.uz": "https://ctnlc.uz"},
 "body": """An English school in Mirzo Ulug'bek district, Tashkent, needed a site. It is live at ctnlc.uz, and it is one self-contained index.html — trilingual UZ/RU/EN with the choice kept in localStorage, a light/dark toggle, scroll-reveal animations, courses, teachers, FAQ, a live Maps embed, and a lead form that copies the enquiry and opens Telegram.

The palette started as cyan and ended as a clean blue, #4D6BFE, on a light hero. The direction came from looking hard at DeepSeek, x.ai and Anthropic and deciding that education sites here reach for gradients far too readily.

The favicon set and the 1200x630 social card are generated by a small Python script rather than drawn by hand, so a colour change is one command away instead of an afternoon.

One near-miss worth writing down: the repo already held a listening test and about 40 MB of MP3s. A force-push would have deleted the audio, so the deploy went through the GitHub contents API instead. I only knew because I looked first.

Search Console verified the same day, sitemap submitted, and structured data for an educational organisation and a local business — with no rating, because there isn't one yet."""
},
{
 "date": "2026-07-23", "tag": "Tech", "sahifa": True,
 "slug": "log-2026-07-23-zed-avlod-school",
 "title": "ZED AVLOD School — zedavlod.uz",
 "havolalar": {"zedavlod.uz": "https://zedavlod.uz"},
 "body": """A school in To'raqo'rg'on, Namangan region, running since 2020. This one is family, which raised the bar rather than lowering it. Live at zedavlod.uz, trilingual UZ/RU/EN.

The part I care about is the results table: thirteen real CEFR certificate scores, the top one C1 and several B2, every one of them checkable against the state certificate database at sertifikat.uzbmb.uz. No percentages, no round numbers, no invented success rate.

What stayed out matters as much. No certificate ID numbers and no photographs of the students. One official-looking portrait turned up in the photo folder and stayed out entirely, because nobody had confirmed who it was — captioning an unidentified person as the founder would have been a lie with a face attached to it.

The rest is the usual full stack for a new domain: FAQ schema, organisation and site structured data with real coordinates, hreflang, its own analytics site, Search Console verified and the sitemap submitted."""
},
{
 "date": "2026-07-25", "tag": "Tech", "sahifa": True,
 "slug": "log-2026-07-25-chiziq-web-studio",
 "title": "Chiziq — a web studio whose portfolio you can actually open",
 "havolalar": {"chzq.uz": "https://chzq.uz"},
 "body": """A web studio aimed at being the cheaper and better-looking alternative to the incumbent in this market. It started as then.uz and became chzq.uz — Chiziq, Uzbek for line — because a brand people can say out loud in their own language beats a clever English pun.

The one real weapon on the site is the portfolio. Every studio in the country publishes client testimonials, and anyone can type a testimonial. So here each project opens in a modal containing a live iframe of the actual site: flarestamina.com, zedavlod.uz, ctnlc.uz, the wedding invite builder, the full mock platform and my own portfolio. They all sit on GitHub Pages, so nothing blocks the embed. The pitch is one line — not reviews, sites you can open right now.

Prices are published, which is rarer here than it should be: landing 1.5 M, business site 3 M, catalogue or shop 6 M, Telegram bot 1.2 M, mini app 6 M so'm. Free prototype in 24 hours, pay after. Hosting 0 so'm, because a static site on GitHub Pages costs nothing to run and pretending otherwise is just markup.

Dark studio palette, near-black and lime, UZ/RU/EN. The brand assets are rendered by code with headless Chrome, not drawn by an image model."""
},
{
 "date": "2026-08-01", "tag": "Tech", "sahifa": True,
 "slug": "log-2026-08-01-payvandchi-workshop",
 "title": "payvandchi.maqsudjon.com — my own workshop, finally online",
 "havolalar": {"payvandchi.maqsudjon.com": "https://payvandchi.maqsudjon.com"},
 "body": """I weld metal grilles in Tashkent. The workshop now has a site at payvandchi.maqsudjon.com: window grilles, balcony grilles, railings and canopies, with real photographs of real jobs and no stock imagery anywhere.

And no gates. We do not make them, so the word does not appear on the site, and every photograph showing a door grille was left out rather than implying a service we cannot deliver. Dropping a photo is cheaper than an awkward phone call.

The engineering here was weight. The hero image came in at 521 KB, which on a Tashkent mobile connection is a wait you can see. Re-encoded and resized it is 173 KB — a third of the bytes, no visible difference.

Adding a photograph is two steps: a line in categories.csv, then run the gallery build script. An English version followed on 5 August, and a fresh batch of workshop photos on 23 August."""
},
{
 "date": "2026-08-04", "tag": "Tech", "sahifa": True,
 "slug": "log-2026-08-04-reshotkachi-second-build",
 "title": "reshotkachi — the same workshop, built a second time",
 "havolalar": {"reshotkachi.maqsudjon.com": "https://reshotkachi.maqsudjon.com"},
 "body": """Same workshop, same photographs, built again as a completely different site. Not laziness — a test. If the product is identical, how much does design alone change how it reads?

A lot, is the answer. This version arranges 123 photographs into a three-dimensional gallery wall in UZ/RU/EN, and it feels like a different business to the one I shipped three days earlier. Same welder, same grilles, same prices.

Live at reshotkachi.maqsudjon.com. Worth keeping both around: when a client says they want something that looks serious, I can now show two serious options instead of describing one."""
},
{
 "date": "2026-08-07", "tag": "Tech", "sahifa": True,
 "slug": "log-2026-08-07-kvadrat-calculator",
 "title": "KVADRAT — a square-metre calculator for grille jobs",
 "havolalar": {"kvdrt.maqsudjon.com": "https://kvdrt.maqsudjon.com"},
 "body": """The least glamorous thing I have built and possibly the one I use most. Live at kvdrt.maqsudjon.com.

You type three numbers — width, height, and how far the grille projects from the wall — and it returns the front face plus all four side faces, which is the area you actually price.

The whole design problem was the input order. 120 130 30 has to mean width 120, height 130, projection 30, every single time, for someone holding a tape measure in one hand and a phone in the other. Making that impossible to misread took longer than the arithmetic did."""
},
{
 "date": "2026-08-24", "tag": "IELTS", "sahifa": True,
 "slug": "log-2026-08-24-flarestamina-walls-hub-news-tools",
 "title": "Flarestamina — the login walls came down, and the hub stopped being a list",
 "havolalar": {"flarestamina.com/ielts-hub": "https://flarestamina.com/ielts-hub/",
               "flarestamina.com/stats": "https://flarestamina.com/stats/"},
 "body": """Traffic had been falling and I assumed it was an SEO problem. It was three login walls.

The hub that all 113 test pages hang off called an auth guard, so every single person arriving from Google was bounced to an account page before seeing anything at all. The Writing Lab had two gates — a login and a hardcoded access code. The speaking section had a third. All three are gone. Signing in is now optional and only buys you saved results.

The hub itself stopped being a wall of links. It asks one question — choose a skill — and offers five cards: Listening with 73 papers, Reading with 25, Writing, Speaking, and the full mock, with a start-here card pointing at Cambridge 21. The audit also caught that the hub builds its list in JavaScript, so a crawler saw an empty page and none of the catalogue behind it. That is why flarestamina.com/tests now exists: a plain static index of every test, so Google can read what a person could already see.

Then the actual SEO, across 113 separate repositories through the GitHub API. Missing meta descriptions 101 to 0, every one generated from the page's own real headings rather than imagined. Missing canonical tags 107 to 1. Missing analytics 108 to 1. Duplicate titles 2 to 0. Structured data 0 to 106 test pages. Titles rewritten to match what people actually type. Three new landing pages for listening, reading and Uzbek-language search, plus an IndexNow key and a sitemap that stopped lying about its dates.

The audit also found a duplicated analytics snippet double-counting every pageview, 65 pages still carrying a headline from a previous redesign, and nineteen reading pages sharing identical body text, which to a search engine reads as one page repeated nineteen times. All fixed.

Last piece: flarestamina.com/stats, every site's visitor count in one table with no login. Having to check seven dashboards was exactly why I checked none of them."""
},
# ── /log/ sahifasi allaqachon bor, faqat bosh sahifaga qo'shiladi ───────────
{
 "date": "2026-08-22", "tag": "IELTS", "sahifa": False,
 "slug": "log-2026-08-22-flarestamina-paper-redesign",
 "title": "I rebuilt the whole of Flarestamina in a weekend — and deleted the framework doing it",
 "body": """Flarestamina looked like three different products. The hub was black and orange with JetBrains Mono, the news section had its own palette, the account page was a fourth thing, and the tools each had their own language toggle that forgot what the last page knew. It worked. It just did not look like one thing built by one person.

This weekend it became one thing. Every page except the practice tests moved to a single design: white paper, Inter and IBM Plex Mono, a four-point spark, and a teal-to-fuchsia gradient rail as the only colour on the entire site.

The interesting part is what I threw away. The design arrived as a compiled React bundle — 262 KB of JavaScript, 52 KB of CSS, and an index.html whose body was one empty div, with no source in my workspace. Shipping that as the home page of a site that lives on search traffic would have meant never being able to edit the copy again, and handing a crawler a blank page. So I rebuilt it as static HTML instead.

Full write-up: maqsudjon.com/log/log-2026-08-22-flarestamina-paper-redesign.html"""
},
{
 "date": "2026-08-27", "tag": "Tech", "sahifa": False,
 "slug": "log-2026-08-27-tadam-wedding-photo-album",
 "title": "Tadam: a wedding album with no app and no database",
 "body": """At an Uzbek wedding there are three hundred guests and three hundred phones, and the couple ends up seeing about twenty of the photographs, forwarded into a group chat and compressed into mush. tadam.uz is my attempt to fix that with a QR code on the table.

The couple creates an album — a title and a date, no account. They get a guest link, a management link and a printable QR sheet. A guest scans it, picks photos, uploads. No app, no sign-up, no password. The couple downloads everything as one ZIP.

It runs as a Cloudflare Worker with R2 as the only datastore. No SQL, no key-value store, nothing else to fall over at eleven at night on a Saturday. Every upload is checked by magic bytes rather than trusting the file extension, photos are served under a locked-down policy that cannot execute anything, random album IDs use rejection sampling after I measured 12.65% bias in the obvious approach over two million samples, and the ZIP carries a real Content-Length so the progress bar is honest.

It was called Chaqnoq for three days, until I said it out loud and watched someone fail to spell it back to me. A wedding product is spoken about, not typed.

Honest status: live, hardened, fast, and not yet used at a single real wedding. Full write-up: maqsudjon.com/log/log-2026-08-27-tadam-wedding-photo-album.html"""
},
{
 "date": "2026-08-27", "tag": "Tech", "sahifa": False,
 "slug": "log-2026-08-27-seven-sites-six-weeks",
 "title": "Seven sites in six weeks",
 "body": """A roundup of everything between 15 July and 27 August: CTN Language Centre, ZED AVLOD School, the Chiziq web studio, my own welding workshop, its second build as Reshotkachi, the KVADRAT calculator, the Flarestamina redesign and SEO sweep, and Tadam.

One constraint ran through all of it: nothing invented. No fabricated review counts, no made-up ratings in the structured data, no student names attached to faces I could not verify, and no "first and only in Uzbekistan" — which I was tempted by and left out, because I cannot prove it and a claim you cannot prove is just a nicer-sounding lie.

The numbers, quoted exactly rather than rounded into something impressive. Search Console on 23 August: 911 impressions, 83 clicks, average position 11.1 — position 11 is page two, and page two is nowhere. Analytics: 238 visits in a week, of which Google was about 8%. Almost all real traffic is people sharing links directly.

The honest reading is that the SEO work is a bet that has not paid out yet, and the sites that work are the ones somebody had a reason to send to a friend.

The post is also published in Uzbek. Full write-up: maqsudjon.com/log/log-2026-08-27-seven-sites-six-weeks.html"""
},
]


def bosh_sahifa(yozuvlar):
    """index.html ichidagi `updates` massiviga qo'shadi (unshift bloklari)."""
    p = ROOT / "index.html"
    s = p.read_text()
    bor = set(re.findall(r'"title":\s*"((?:[^"\\]|\\.)*)"', s))
    bor = {json.loads('"' + t + '"') for t in bor}

    bloklar = []
    for e in yozuvlar:
        if e["title"] in bor:
            continue
        bloklar.append("updates.unshift({\n"
                       f'  "date":{json.dumps(e["date"])},\n'
                       f'  "title":{json.dumps(e["title"], ensure_ascii=False)},\n'
                       f'  "tag":{json.dumps(e["tag"])},\n'
                       f'  "body":{json.dumps(e["body"], ensure_ascii=False)}\n'
                       "});")
    if not bloklar:
        return 0
    # Oxirgi unshift blokidan keyin joylashtiramiz.
    oxirgi = [m.end() for m in re.finditer(r'^\}\);$', s, re.M)][-1]
    s = s[:oxirgi] + "\n\n" + "\n\n".join(bloklar) + s[oxirgi:]
    p.write_text(s)
    return len(bloklar)


def arxiv(yozuvlar):
    """/log/index.html ro'yxatini qayta tartiblab yozadi."""
    p = ROOT / "log" / "index.html"
    s = p.read_text()
    blok = re.search(r'(<ul class="list">\n)(.*?)(</ul>)', s, re.S)
    qatorlar = [q for q in blok.group(2).split("\n") if q.strip()]

    for e in yozuvlar:
        if f'/log/{e["slug"]}.html' in blok.group(2):
            continue
        qatorlar.append(f'<li><span class="d">{sana(e["date"])}</span>'
                        f'<a href="/log/{e["slug"]}.html">{html.escape(e["title"])}</a></li>')

    def kalit(q):
        m = re.search(r'/log/log-(\d{4}-\d{2}-\d{2})', q)
        return m.group(1) if m else "0000-00-00"
    qatorlar.sort(key=kalit, reverse=True)

    s = s[:blok.start(2)] + "\n".join(qatorlar) + "\n" + s[blok.end(2):]
    s = re.sub(r'BUILD LOG · \d+ ENTRIES', f'BUILD LOG · {len(qatorlar)} ENTRIES', s)
    p.write_text(s)
    return len(qatorlar)


def lenta(yozuvlar):
    """feed.xml ga item qo'shadi."""
    p = ROOT / "feed.xml"
    s = p.read_text()
    yangi = []
    for e in yozuvlar:
        url = f'{BASE}/log/{e["slug"]}.html'
        if url in s:
            continue
        desc = e["body"].split("\n\n")[0][:280]
        yangi.append(f"""  <item>
    <title>{html.escape(e["title"])}</title>
    <link>{url}</link>
    <guid>{url}</guid>
    <pubDate>{rfc(e["date"])}</pubDate>
    <description>{html.escape(desc)}</description>
  </item>""")
    if not yangi:
        return 0
    i = s.index("  <item>")
    p.write_text(s[:i] + "\n".join(yangi) + "\n" + s[i:])
    return len(yangi)


def xarita(yozuvlar):
    """sitemap.xml ga manzil qo'shadi."""
    p = ROOT / "sitemap.xml"
    s = p.read_text()
    yangi = [f'  <url><loc>{BASE}/log/{e["slug"]}.html</loc><lastmod>{e["date"]}</lastmod></url>'
             for e in yozuvlar if f'/log/{e["slug"]}.html' not in s]
    if not yangi:
        return 0
    i = s.index("  <url><loc>" + BASE + "/log/log-")
    p.write_text(s[:i] + "\n".join(yangi) + "\n" + s[i:])
    return len(yangi)


if __name__ == "__main__":
    yangi_sahifa = [e for e in YOZUVLAR if e["sahifa"]]
    for e in yangi_sahifa:
        sahifa_yoz(e)
        print(f"  sahifa  {e['slug']}")

    print(f"\n  bosh sahifa: +{bosh_sahifa(YOZUVLAR)} yozuv")
    print(f"  /log/ arxivi: {arxiv(yangi_sahifa)} ta jami")
    print(f"  feed.xml: +{lenta(yangi_sahifa)}")
    print(f"  sitemap.xml: +{xarita(yangi_sahifa)}")
