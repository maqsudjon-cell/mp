#!/usr/bin/env python3
"""
Build log RSS lentalarini /log/ sahifalarining o'zidan, TO'LIQ matn bilan yasaydi.

  · feed.xml     — inglizcha yozuvlar (<html lang="en">)
  · feed-uz.xml  — o'zbekcha yozuvlar (<html lang="uz">)

Har bir item: sarlavha, havola, sana, yorliq (category), qisqa tavsif
(description), yozuvning butun matni (content:encoded, rasmlari va havolalari
mutlaq manzil bilan) va OG rasmi (media:content). Eski yozuvlar matni
`white-space: pre-wrap` bilan yozilgan — ular bo'sh qatordan <p> ga bo'linadi.

Lentani qo'lda tahrirlamang: yangi yozuvdan keyin shu skriptni ishga tushiring
(post_*.py va add_log_entries.py uni o'zi chaqiradi).

    python3 tools/build_feed.py
"""
import datetime
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://maqsudjon.com"
HUB = "https://pubsubhubbub.appspot.com/"
FEEDS = {
    "en": ("feed.xml", "Maqsudjon Polatov — build log",
           "A one-person lab for acting in code and steel — everything I ship, as I ship it. Full posts."),
    "uz": ("feed-uz.xml", "Maqsudjon Polatov — build log (o'zbekcha)",
           "Kod va temir bilan ishlaydigan bir kishilik laboratoriya: chiqargan hamma narsam, chiqargan kunim. To'liq yozuvlar."),
}


def first(pattern, s, default=""):
    m = re.search(pattern, s, re.S)
    return m.group(1) if m else default


def absolute(fragment):
    return re.sub(r'(src|href)="/(?!/)', rf'\1="{BASE}/', fragment)


def rfc822(iso):
    d = datetime.date.fromisoformat(iso[:10])
    dt = datetime.datetime(d.year, d.month, d.day, 12, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=5)))
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0500")


def read_post(p):
    s = p.read_text()
    body = first(r'<div class="body">(.*?)</div>\s*<div class="foot">', s).strip()
    if not body:
        return None
    if ".body{white-space:pre-wrap" in s:
        # eski yozuv: oddiy matn, bo'sh qator — yangi paragraf
        body = "\n".join(f"<p>{para.strip().replace(chr(10), '<br>')}</p>"
                         for para in re.split(r"\n\s*\n", body) if para.strip())
    return {
        "lang": first(r'<html lang="(\w+)"', s, "en"),
        "url": first(r'<link rel="canonical" href="([^"]+)"', s, f"{BASE}/log/{p.name}"),
        "title": html.unescape(first(r"<h1>(.*?)</h1>", s)),
        "desc": html.unescape(first(r'<meta name="description" content="([^"]*)"', s)),
        "date": first(r'article:published_time" content="([^"]+)"', s) or first(r'"datePublished":\s*"([^"]+)"', s),
        "tag": html.unescape(first(r'<div class="meta">[^<]*<b>([^<]+)</b>', s)).strip(),
        "image": first(r'<meta property="og:image" content="([^"]+)"', s),
        "body": absolute(body),
    }


def item(e):
    img = (f'\n    <media:content url="{html.escape(e["image"])}" medium="image" type="image/png" width="1200" height="630"/>'
           if e["image"] else "")
    cat = f"\n    <category>{html.escape(e['tag'])}</category>" if e["tag"] else ""
    content = e["body"].replace("]]>", "]]&gt;")
    return f"""  <item>
    <title>{html.escape(e["title"])}</title>
    <link>{e["url"]}</link>
    <guid isPermaLink="true">{e["url"]}</guid>
    <pubDate>{rfc822(e["date"])}</pubDate>
    <dc:creator>Maqsudjon Polatov</dc:creator>{cat}
    <description>{html.escape(e["desc"])}</description>
    <content:encoded><![CDATA[{content}]]></content:encoded>{img}
  </item>"""


def main():
    posts = [e for e in (read_post(p) for p in sorted((ROOT / "log").glob("log-*.html"))) if e and e["date"]]
    for lang, (name, title, desc) in FEEDS.items():
        items = sorted((e for e in posts if e["lang"] == lang), key=lambda e: (e["date"], e["url"]), reverse=True)
        if not items:
            continue
        last = rfc822(items[0]["date"])
        out = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:media="http://search.yahoo.com/mrss/">
<channel>
  <title>{html.escape(title)}</title>
  <link>{BASE}/log/</link>
  <atom:link href="{BASE}/{name}" rel="self" type="application/rss+xml"/>
  <atom:link href="{HUB}" rel="hub"/>
  <description>{html.escape(desc)}</description>
  <language>{lang}</language>
  <copyright>© 2026 Maqsudjon Polatov</copyright>
  <lastBuildDate>{last}</lastBuildDate>
  <ttl>720</ttl>
  <image><url>{BASE}/favicon-512x512.png</url><title>{html.escape(title)}</title><link>{BASE}/log/</link></image>
{chr(10).join(item(e) for e in items)}
</channel>
</rss>
"""
        (ROOT / name).write_text(out)
        print(f"  {name}: {len(items)} ta yozuv, to'liq matn bilan")


if __name__ == "__main__":
    main()
