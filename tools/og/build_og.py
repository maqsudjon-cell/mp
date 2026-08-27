#!/usr/bin/env python3
"""Har bir log yozuvi uchun 1200x630 OG rasm yasaydi.

Blog dizayniga mos: qora fon, Funnel Display sarlavha, tepada yorliq,
pastda domen. Headless Chrome bilan render qilinadi (shrift Google
Fonts'dan olinadi), keyin PNG saqlanadi.

    python3 tools/og/build_og.py
"""
import html
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SHELL = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@600&family=Geist+Mono:wght@400&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#000;color:#fff;overflow:hidden;
  display:flex;flex-direction:column;justify-content:space-between;padding:64px 72px;
  font-family:'Geist Mono',monospace}}
.top{{display:flex;justify-content:space-between;align-items:baseline;
  font-size:19px;letter-spacing:.16em;text-transform:uppercase;color:#888}}
h1{{font-family:'Funnel Display',sans-serif;font-weight:600;font-size:{size}px;
  line-height:1.08;letter-spacing:-.025em;color:#fff;max-width:1000px}}
.sub{{color:#ffffffbb;font-size:23px;line-height:1.5;max-width:860px;
  margin-top:26px;font-family:'Geist Mono',monospace;letter-spacing:-.01em}}
.bot{{display:flex;justify-content:space-between;align-items:center;
  font-size:19px;letter-spacing:.16em;text-transform:uppercase;color:#888}}
.tag{{color:#f2d8cd;border:1px solid #4d4d4d;padding:5px 14px}}
.rail{{height:4px;width:190px;margin-bottom:34px;
  background:linear-gradient(90deg,#f2d8cd,#8fb8c9 55%,#4d4d4d)}}
</style></head><body>
<div class="top"><span>✳ MAQSUDJON POLATOV</span><span>{date}</span></div>
<div><div class="rail"></div><h1>{title}</h1><div class="sub">{sub}</div></div>
<div class="bot"><span>maqsudjon.com/log</span><span class="tag">{tag}</span></div>
</body></html>"""


def make(slug, title, sub, date, tag, size=76):
    src = ROOT / "tools" / "og" / f"_{slug}.html"
    out = ROOT / "log" / "og" / f"{slug}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    src.write_text(SHELL.format(title=html.escape(title), sub=html.escape(sub),
                                date=date, tag=tag, size=size))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", "--window-size=1200,630",
                    "--virtual-time-budget=6000", f"--screenshot={out}",
                    src.as_uri()], capture_output=True)
    src.unlink(missing_ok=True)
    kb = out.stat().st_size // 1024 if out.exists() else 0
    print(f"  {out.name:52} {kb} KB")
    return out


YOZUVLAR = [
    ("log-2026-08-27-seven-sites-six-weeks", "Seven sites in six weeks",
     "CTN · ZED AVLOD · Chiziq · Payvandchi · Reshotkachi · KVADRAT · Flarestamina · Tadam",
     "27 AUG 2026", "ROUNDUP", 82),
    ("log-2026-08-27-seven-sites-six-weeks-uz", "Olti haftada yettita sayt",
     "CTN · ZED AVLOD · Chiziq · Payvandchi · Reshotkachi · KVADRAT · Flarestamina · Tadam",
     "27 AVG 2026", "TO'PLAM", 82),
    ("log-2026-08-27-tadam-wedding-photo-album",
     "A wedding album with no app and no database",
     "Guests scan the QR on the table. The couple downloads every photo as a ZIP. tadam.uz",
     "27 AUG 2026", "PRODUCT", 70),
    ("log-2026-08-27-tadam-wedding-photo-album-uz",
     "Ilovasiz va bazasiz to'y albomi",
     "Mehmon stoldagi QR'ni skanerlaydi. Kelin-kuyov hamma suratni ZIP qilib oladi. tadam.uz",
     "27 AVG 2026", "MAHSULOT", 70),
]

if __name__ == "__main__":
    if not Path(CHROME).exists():
        sys.exit("Chrome topilmadi: " + CHROME)
    for slug, t, s, d, tag, size in YOZUVLAR:
        make(slug, t, s, d, tag, size)
