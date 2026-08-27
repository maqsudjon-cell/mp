#!/usr/bin/env python3
"""IndexNow — Bing, Yandex va Seznam'ga yangilangan manzillarni bildiradi.

Google IndexNow'ni qo'llamaydi; u uchun Search Console kerak.
Kalit fayli sayt ildizida turishi shart: https://maqsudjon.com/<KALIT>.txt

    python3 tools/indexnow.py <manzil> [manzil ...]
"""
import json
import subprocess
import sys

KALIT = "e81beec87a8949632b976392272ae1d2"
HOST = "maqsudjon.com"


def yubor(manzillar):
    payload = json.dumps({
        "host": HOST,
        "key": KALIT,
        "keyLocation": f"https://{HOST}/{KALIT}.txt",
        "urlList": manzillar,
    })
    # curl ishlatiladi: tizim CA to'plami bilan keladi, python'niki bu
    # mashinada to'liq emas.
    r = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "30",
         "-X", "POST", "https://api.indexnow.org/indexnow",
         "-H", "Content-Type: application/json; charset=utf-8",
         "--data-binary", payload],
        capture_output=True, text=True)
    return r.stdout.strip()


if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        sys.exit("Manzil bering.")
    print(f"  {yubor(urls)} — {len(urls)} ta manzil yuborildi")
