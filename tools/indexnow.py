#!/usr/bin/env python3
"""IndexNow — Bing, Yandex va Seznam'ga yangilangan manzillarni bildiradi.

Google IndexNow'ni qo'llamaydi; u uchun Search Console kerak.
Kalit fayli sayt ildizida turishi shart: https://maqsudjon.com/<KALIT>.txt

    python3 tools/indexnow.py <manzil> [manzil ...]
"""
import json
import sys
import urllib.request

KALIT = "e81beec87a8949632b976392272ae1d2"
HOST = "maqsudjon.com"


def yubor(manzillar):
    payload = json.dumps({
        "host": HOST,
        "key": KALIT,
        "keyLocation": f"https://{HOST}/{KALIT}.txt",
        "urlList": manzillar,
    }).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow", data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        sys.exit("Manzil bering.")
    print(f"  {yubor(urls)} — {len(urls)} ta manzil yuborildi")
