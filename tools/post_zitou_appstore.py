#!/usr/bin/env python3
"""Zitou App Store'ga chiqdi (EN + UZ), 2026-11-05.

Yozuvni, OG rasmlarini, bosh sahifadagi feed yozuvini, /log/ arxivini,
sitemap'ni va ikkala RSS lentasini bitta joydan yangilaydi (post_zitou.py kabi).

    python3 tools/post_zitou_appstore.py
"""
import html
import sys
sys.path.insert(0, "tools")
sys.path.insert(0, "tools/og")
from build_log_post import build, ROOT, BASE

STORE = "https://apps.apple.com/app/id6818937091"

EN = f"""
<p class="lede">On 5 November 2026 Zitou went live on the App Store as <a href="{STORE}">Zitou: Learn Chinese &amp; HSK</a>. It is free to download, for iPhone on iOS 15 or later.</p>

<h2>The same app, one more door</h2>

<p>The iPhone app is the same Zitou as <a href="https://zitou.app">zitou.app</a>: a native shell around the web app. That was a choice, not a shortcut. A fix or a new HSK mock paper reaches the website, the Telegram Mini App and the iPhone app in one deploy, without waiting for a review.</p>

<p>What the shell adds is what only a phone can do:</p>

<ul>
<li><strong>Sign in with Apple</strong>, next to Google and Telegram, all leading to the same account and the same progress.</li>
<li><strong>Daily reminders</strong>, planned on the phone itself, because a web view has no web push.</li>
<li><strong>Pro through the App Store</strong>, monthly or yearly. The server checks every transaction with Apple before it switches Pro on.</li>
<li><strong>The share sheet</strong>, and zitou.app links that open in the app instead of the browser.</li>
</ul>

<h2>Android</h2>

<p>There is no Google Play version yet. Until there is, Android users open <a href="https://t.me/zitouggbot">@zitouggbot</a> in Telegram, where the whole app runs as a Mini App, or use it in the browser. The site now says exactly that under its download buttons, instead of a button that leads nowhere.</p>

<h2>What changed on the sites</h2>

<ul>
<li>The App Store button on every landing page is live; it said "coming soon" until this week.</li>
<li>Safari shows its own "Open / Get" banner for the app on every page, except over a live lesson on a classroom screen.</li>
<li>An iPhone browser is sent to the App Store, instead of being taught to add an icon to the home screen.</li>
<li>The Telegram bot's greeting ends with the App Store link.</li>
</ul>

<h2>What I am not claiming</h2>

<p>No download numbers in this post. I will publish them when I can show where they come from.</p>
"""

UZ = f"""
<p class="lede">2026-yil 5-noyabrda Zitou App Store'da <a href="{STORE}">Zitou: Learn Chinese &amp; HSK</a> nomi bilan chiqdi. Yuklab olish bepul, iOS 15 va undan yangi iPhone uchun.</p>

<h2>O'sha ilova, yana bir eshik</h2>

<p>iPhone ilovasi <a href="https://zitou.app">zitou.app</a> dagi o'sha Zitou: veb-ilova atrofidagi native qobiq. Bu yo'lni ataylab tanladim. Tuzatish yoki yangi HSK sinov varianti sayt, Telegram Mini App va iPhone ilovasiga bitta deploy bilan yetib boradi, tekshiruvni kutmasdan.</p>

<p>Qobiq faqat telefon qila oladigan narsalarni qo'shadi:</p>

<ul>
<li><strong>Apple bilan kirish</strong>, Google va Telegram yonida. Hammasi bitta hisobga va bitta natijaga olib boradi.</li>
<li><strong>Kunlik eslatmalar</strong> telefonning o'zida rejalashtiriladi, chunki web view'da web push yo'q.</li>
<li><strong>App Store orqali Pro</strong>, oylik yoki yillik. Server Pro'ni yoqishdan oldin har bir tranzaksiyani Apple bilan tekshiradi.</li>
<li><strong>Ulashish oynasi</strong>, va zitou.app havolalari brauzerda emas, ilovaning o'zida ochiladi.</li>
</ul>

<h2>Android</h2>

<p>Google Play versiyasi hali yo'q. U chiqquncha Android foydalanuvchilari Telegram'da <a href="https://t.me/zitouggbot">@zitouggbot</a> ni ochadi, u yerda butun ilova Mini App bo'lib ishlaydi, yoki brauzerda foydalanadi. Endi saytdagi yuklab olish tugmalari ostida aynan shu yozilgan, hech qayerga olib bormaydigan tugma o'rniga.</p>

<h2>Saytlarda nima o'zgardi</h2>

<ul>
<li>Har bir landing sahifadagi App Store tugmasi ishlaydi; shu haftagacha unda "tez kunda" yozuvi turardi.</li>
<li>Safari har bir sahifada ilova uchun o'zining "Ochish / Yuklab olish" bannerini ko'rsatadi, sinf ekranidagi jonli dars bundan mustasno.</li>
<li>iPhone brauzeri bosh ekranga belgi qo'shishni o'rgatish o'rniga App Store'ga yuboriladi.</li>
<li>Telegram botining salomlashuv xabari App Store havolasi bilan tugaydi.</li>
</ul>

<h2>Nima demayman</h2>

<p>Bu yozuvda yuklab olishlar soni yo'q. Ularni qayerdan olinganini ko'rsata olganimda e'lon qilaman.</p>
"""

EN_SLUG = "log-2026-11-05-zitou-on-the-app-store"
UZ_SLUG = "log-2026-11-05-zitou-on-the-app-store-uz"
EN_TITLE = "Zitou is on the App Store"
UZ_TITLE = "Zitou App Store'da"
EN_DESC = ("Zitou: Learn Chinese & HSK went live on the App Store on 5 November 2026. What the iPhone app adds "
           "to the website, why it is the same app underneath, and where Android users find it for now.")
UZ_DESC = ("Zitou: Learn Chinese & HSK 2026-yil 5-noyabrda App Store'da chiqdi. iPhone ilovasi saytga nima "
           "qo'shadi, nega u aslida o'sha ilova va Android foydalanuvchilari uni hozircha qayerdan topadi.")

# OG rasmlari avval: build() ularni o'zi topadi
from build_og import make
make(EN_SLUG, "Zitou is on the App Store",
     "Zitou: Learn Chinese & HSK · for iPhone · free", "05 NOV 2026", "PRODUCT", 76)
make(UZ_SLUG, "Zitou App Store'da",
     "Zitou: Learn Chinese & HSK · iPhone uchun · bepul", "05 NOY 2026", "MAHSULOT", 76)

build(EN_SLUG, "en", EN_TITLE, EN_DESC, "05 NOV 2026", "2026-11-05", "PRODUCT", EN,
      UZ_SLUG, "O'ZBEKCHA", "← ALL ENTRIES")
build(UZ_SLUG, "uz", UZ_TITLE, UZ_DESC, "05 NOY 2026", "2026-11-05", "MAHSULOT", UZ,
      EN_SLUG, "ENGLISH", "← BARCHA YOZUVLAR")

# bosh sahifadagi jonli feed va /log/ arxivi (add_log_entries'ning o'z funksiyalari)
import add_log_entries as A
entry = {
    "date": "2026-11-05", "tag": "Tech", "slug": EN_SLUG, "title": EN_TITLE,
    "body": ("Zitou went live on the App Store on 5 November as Zitou: Learn Chinese & HSK, free for iPhone.\n\n"
             "It is the same app as zitou.app, in a native shell, so one deploy still reaches the website, the Telegram "
             "Mini App and the iPhone app. The shell adds Sign in with Apple, daily reminders planned on the phone, Pro "
             "through the App Store and the share sheet.\n\n"
             "There is no Google Play version yet: Android users open @zitouggbot in Telegram, where the whole app runs "
             "as a Mini App. The landing pages say so under the download buttons, and the App Store button no longer "
             "says \"coming soon\".\n\n"
             "The post is also published in Uzbek. Full write-up: maqsudjon.com/log/" + EN_SLUG + ".html"),
}
print(f"  bosh sahifa: +{A.bosh_sahifa([entry])} yozuv")
print(f"  /log/ arxivi: {A.arxiv([entry])} ta jami")
li = ROOT / "log" / "index.html"
s = li.read_text()
own = f'<a href="/log/{EN_SLUG}.html">{html.escape(EN_TITLE)}</a></li>'
if own in s:
    li.write_text(s.replace(own, f'<a href="/log/{EN_SLUG}.html">{html.escape(EN_TITLE)}</a>'
                                 f'<a class="uz" href="/log/{UZ_SLUG}.html">O&#x27;ZBEKCHA</a></li>'))

# sitemap: ikkala til, bir-biriga hreflang bilan
sm = ROOT / "sitemap.xml"
s = sm.read_text()
if EN_SLUG not in s:
    alt = (f'\n    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/log/{EN_SLUG}.html"/>'
           f'\n    <xhtml:link rel="alternate" hreflang="uz" href="{BASE}/log/{UZ_SLUG}.html"/></url>')
    block = (f'  <url><loc>{BASE}/log/{EN_SLUG}.html</loc><lastmod>2026-11-08</lastmod>{alt}\n'
             f'  <url><loc>{BASE}/log/{UZ_SLUG}.html</loc><lastmod>2026-11-08</lastmod>{alt}\n')
    i = s.index(f"  <url><loc>{BASE}/log/log-")
    sm.write_text(s[:i] + block + s[i:])
    print("  sitemap.xml: +2")

import build_feed
build_feed.main()
print("zitou app store: EN + UZ yozildi")
