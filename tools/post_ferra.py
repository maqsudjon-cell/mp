#!/usr/bin/env python3
"""Ferra App Store'da (EN + UZ), 2026-11-07.

Yozuvni, OG rasmlarini, bosh sahifadagi feed yozuvini, /log/ arxivini,
sitemap'ni va ikkala RSS lentasini bitta joydan yangilaydi (post_zitou_appstore.py kabi).

    python3 tools/post_ferra.py
"""
import html
import sys
sys.path.insert(0, "tools")
sys.path.insert(0, "tools/og")
from build_log_post import build, ROOT, BASE

STORE = "https://apps.apple.com/app/id6831706335"

EN = f"""
<p class="lede">Ferra AI Agents is on the App Store. It is a free iPhone app (iOS 17 or later) where every agent has one job, its own model and its own chats. Android and other Telegram clients get the same app as a Telegram Mini App through <a href="https://t.me/Ferraaibot">@Ferraaibot</a>.</p>

<h2>One name, one job, any model</h2>

<p>You create an agent by giving it a name, one task and a model. The model comes from the live OpenRouter catalog, hundreds of models from many providers, and each agent keeps separate chat threads. Text works everywhere and selected images work when the chosen model accepts them. Three starter agents ship with the app: <strong>Researcher</strong>, <strong>Inbox Manager</strong> and <strong>Study Coach</strong>.</p>

<h2>Free to start, your own key if you want it</h2>

<ul>
<li>The free start mode runs on my OpenRouter account with a limit enforced on the server: 20 free messages a day at the moment. There are no in-app purchases and no subscription.</li>
<li>If you connect your own OpenRouter account (bring your own key), the key is validated and stored encrypted on the server. The plain key is not kept on the phone and is never sent back.</li>
<li>Usage is visible by agent and by model: requests, tokens, the cost the model reports and what is left of the day's free allowance.</li>
</ul>

<h2>Nothing goes out without you</h2>

<p>When an agent proposes an email or a message, you approve it in the app first. Then Apple Mail or Messages opens and you make the final decision there. An approval is not proof of delivery, and the app does not claim it is.</p>

<h2>Android</h2>

<p>There is no native Android app. The Telegram Mini App has been live since 9 November: starter and custom agents, model choice, text and image chat, your own key, usage, approvals and account deletion, all on the same backend as the iPhone app.</p>

<h2>Decks from a single topic</h2>

<p>The sibling site <a href="https://ferra.tou.gg">ferra.tou.gg</a> turns a topic into a finished slide deck with real sources and images, as PPTX or PDF.</p>

<h2>What I am not claiming</h2>

<p>No download numbers in this post. I will publish them when I can show where they come from. Product facts, pricing and the changelog live at <a href="https://tou.gg/ferra/">tou.gg/ferra</a>, and the app is here: <a href="{STORE}">Ferra AI Agents on the App Store</a>.</p>
"""

UZ = f"""
<p class="lede">Ferra AI Agents App Store'da. Bu bepul iPhone ilovasi (iOS 17 va undan yangi): har bir agentning bitta vazifasi, o'z modeli va o'z suhbatlari bor. Android va boshqa Telegram klientlari xuddi shu ilovadan <a href="https://t.me/Ferraaibot">@Ferraaibot</a> orqali Telegram Mini App sifatida foydalanadi.</p>

<h2>Bitta nom, bitta vazifa, istalgan model</h2>

<p>Agent yaratish uchun unga nom, bitta vazifa va model berasiz. Model jonli OpenRouter katalogidan olinadi, ya'ni turli provayderlarning yuzlab modellari, har bir agentning suhbatlari esa alohida. Matn hamma joyda ishlaydi, tanlangan rasmlar esa model ularni qabul qilsagina. Ilova bilan uchta tayyor agent keladi: <strong>Researcher</strong>, <strong>Inbox Manager</strong> va <strong>Study Coach</strong>.</p>

<h2>Bepul boshlash, xohlasangiz o'z kalitingiz</h2>

<ul>
<li>Bepul rejim mening OpenRouter hisobimda ishlaydi, chegarasi serverda tekshiriladi: hozircha kuniga 20 ta bepul xabar. Ilova ichida xaridlar ham, obuna ham yo'q.</li>
<li>O'z OpenRouter hisobingizni ulasangiz (o'z kalitingiz bilan), kalit tekshiriladi va serverda shifrlangan holda saqlanadi. Ochiq kalit telefonda saqlanmaydi va qaytarib yuborilmaydi.</li>
<li>Sarf agent va model bo'yicha ko'rinadi: so'rovlar, tokenlar, model aytgan narx va kunlik bepul limitdan qolgani.</li>
</ul>

<h2>Sizsiz hech narsa chiqib ketmaydi</h2>

<p>Agent email yoki xabar taklif qilsa, avval uni ilovada tasdiqlaysiz. Keyin Apple Mail yoki Xabarlar ochiladi va yakuniy qarorni o'sha yerda qabul qilasiz. Tasdiqlash yetkazilganini bildirmaydi, ilova ham bunday da'vo qilmaydi.</p>

<h2>Android</h2>

<p>Native Android ilovasi yo'q. Telegram Mini App 9-noyabrdan ishlaydi: tayyor va o'zingiz yaratgan agentlar, model tanlash, matn va rasmli suhbat, o'z kalitingiz, sarf, tasdiqlash va hisobni o'chirish, hammasi iPhone ilovasi bilan bir xil serverda.</p>

<h2>Bitta mavzudan tayyor slaydlar</h2>

<p><a href="https://ferra.tou.gg">ferra.tou.gg</a> mavzuni haqiqiy manbalar va rasmlar bilan tayyor slayd taqdimotiga aylantiradi, PPTX yoki PDF ko'rinishida.</p>

<h2>Nima demayman</h2>

<p>Bu yozuvda yuklab olishlar soni yo'q. Ularni qayerdan olinganini ko'rsata olganimda e'lon qilaman. Mahsulot haqidagi faktlar, narx va o'zgarishlar tarixi <a href="https://tou.gg/ferra/">tou.gg/ferra</a> da, ilovaning o'zi esa bu yerda: <a href="{STORE}">Ferra AI Agents, App Store</a>.</p>
"""

EN_SLUG = "log-2026-11-07-ferra-on-the-app-store"
UZ_SLUG = "log-2026-11-07-ferra-on-the-app-store-uz"
EN_TITLE = "Ferra is on the App Store"
UZ_TITLE = "Ferra App Store'da"
EN_DESC = ("Ferra AI Agents, a personal AI-agent app for iPhone, is on the App Store: one name, one job and one model "
           "per agent, nothing sent without your approval, and a Telegram Mini App for Android.")
UZ_DESC = ("Ferra AI Agents, iPhone uchun shaxsiy AI agentlar ilovasi, App Store'da: har bir agentga bitta nom, bitta "
           "vazifa va bitta model, tasdig'ingizsiz hech narsa yuborilmaydi, Android uchun esa Telegram Mini App.")

# OG rasmlari avval: build() ularni o'zi topadi (bor bo'lsa qayta yasamaydi)
from build_og import make
for slug, title, sub, date, tag in [
        (EN_SLUG, "Ferra is on the App Store", "Ferra AI Agents · for iPhone · free", "07 NOV 2026", "PRODUCT"),
        (UZ_SLUG, "Ferra App Store'da", "Ferra AI Agents · iPhone uchun · bepul", "07 NOY 2026", "MAHSULOT")]:
    if not (ROOT / "log" / "og" / f"{slug}.png").exists():
        make(slug, title, sub, date, tag, 76)

build(EN_SLUG, "en", EN_TITLE, EN_DESC, "07 NOV 2026", "2026-11-07", "PRODUCT", EN,
      UZ_SLUG, "O'ZBEKCHA", "← ALL ENTRIES")
build(UZ_SLUG, "uz", UZ_TITLE, UZ_DESC, "07 NOY 2026", "2026-11-07", "MAHSULOT", UZ,
      EN_SLUG, "ENGLISH", "← BARCHA YOZUVLAR")

# bosh sahifadagi jonli feed va /log/ arxivi (add_log_entries'ning o'z funksiyalari)
import add_log_entries as A
entry = {
    "date": "2026-11-07", "tag": "Tech", "slug": EN_SLUG, "title": EN_TITLE,
    "body": ("Ferra AI Agents is on the App Store: a free iPhone app where every agent has one job, its own model and "
             "its own chats.\n\n"
             "The model comes from the live OpenRouter catalog, the free start allows 20 messages a day, and you can "
             "bring your own key. Email and message proposals need your approval in the app before Apple Mail or "
             "Messages even opens.\n\n"
             "There is no native Android app: the same Ferra runs as a Telegram Mini App through @Ferraaibot, live "
             "since 9 November. ferra.tou.gg, its sibling, turns a topic into a finished slide deck.\n\n"
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
    block = (f'  <url><loc>{BASE}/log/{EN_SLUG}.html</loc><lastmod>2026-11-22</lastmod>{alt}\n'
             f'  <url><loc>{BASE}/log/{UZ_SLUG}.html</loc><lastmod>2026-11-22</lastmod>{alt}\n')
    i = s.index(f"  <url><loc>{BASE}/log/log-")
    sm.write_text(s[:i] + block + s[i:])
    print("  sitemap.xml: +2")

import build_feed
build_feed.main()
print("ferra app store: EN + UZ yozildi")
