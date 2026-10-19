#!/usr/bin/env python3
"""Zitou (zitou.uz + zitou.app) haqidagi batafsil yozuv (EN + UZ), 2026-10-19.

Yozuvni, OG rasmlarini, bosh sahifadagi feed yozuvini, /log/ arxivini,
sitemap'ni va ikkala RSS lentasini bitta joydan yangilaydi.

    python3 tools/post_zitou.py
"""
import html
import re
import sys
sys.path.insert(0, "tools")
sys.path.insert(0, "tools/og")
from build_log_post import build, fig, pair, ROOT, BASE

EN = """
<p class="lede">On 19 September 2026 I started learning Chinese. There was very little to learn it with in Uzbek, so four days later the first version of Zitou went up. A month on, it is a free app with a 124,039-word dictionary, every HSK list, native audio for 8,563 words, a six-lesson HSK 1 course for classrooms and, since today, two addresses: <a href="https://zitou.uz">zitou.uz</a> in Uzbek and <a href="https://zitou.app">zitou.app</a> for everything else.</p>

<p>This is the long version: what is in it, how a class uses it, why it now lives at two addresses, how it is built, and what I am not claiming.</p>

""" + pair("zitou-uz-home.webp", "zitou-app-en.webp",
           "The same product at its two addresses: zitou.uz in Uzbek, zitou.app/en in English. Eight more languages live on zitou.app.",
           "Zitou home page at zitou.uz, in Uzbek", "Zitou home page at zitou.app/en, in English") + """

<h2>What is in it</h2>

<p>The core is a dictionary and a course. The dictionary comes from CC-CEDICT: 124,039 words, searchable by character, by pinyin with or without tones, or by the meaning in Uzbek, Russian or English. 8,296 of them, every word of HSK 1–6 plus 472 everyday words that are on no list, have an Uzbek and a Russian meaning. The course follows all three HSK lists: the 2025 revision (10,057 words), HSK 3.0 and HSK 2.0, each level its own course.</p>

<ul>
<li><strong>Native audio.</strong> 8,563 words are recordings of native speakers from audio-cmn (CC BY-SA). The rest use the device's Chinese voice.</li>
<li><strong>Stroke order.</strong> Every character: watch it, trace it over grey, then write it from memory with a finger. The stroke data is Make Me a Hanzi.</li>
<li><strong>Spaced repetition.</strong> Words come back just before you would forget them, scheduled with FSRS. You only press Start.</li>
<li><strong>Tones in colour.</strong> First tone red, second orange, third green, fourth blue, so a tone is remembered by the eye as well as the ear.</li>
<li><strong>Grammar.</strong> 103 topics for HSK 1–4, each with a pattern, a short rule, examples with pinyin, the common mistake and a two-minute exercise.</li>
<li><strong>Mock exams.</strong> HSK 1–4 in the real HSK 2.0 format, with the listening played as in the exam, the timer and the pass mark, and a first HSK 3.0 level-1 paper.</li>
<li><strong>Small tools.</strong> A translator for text, voice or the photo of a sign; a phrasebook of 80+ phrases for a trip to China; your name in Chinese, character by character; Daily 5, the same five questions for everyone at a level, to send to a friend; and China news in Uzbek, each item with its source.</li>
</ul>

<p>It works without an account, in ten interface languages, in the browser on a phone, a tablet or a computer.</p>

""" + fig("zitou-word.webp",
          "One of the 7,823 Uzbek word pages: the meaning in Uzbek and English, the characters, stroke order, audio and example sentences. These pages are most of what search engines find.",
          "The word page for 你好 on zitou.uz") + """

<h2>The HSK 1 course, built for a classroom</h2>

<p>Most learners here do not study alone. They sit in a class with a teacher and a textbook, so the newest part of Zitou is for that room. The HSK 1 course has six lessons. A teacher opens a lesson on the big screen at <a href="https://zitou.app/dars/">zitou.app/dars</a> and gets a six-digit code. Students type it on their phones, with no account, and answer each exercise together. The teacher sees who answered, who got it wrong and who pressed "I don't understand", as it happens.</p>

""" + fig("zitou-dars.webp",
          "zitou.app/dars: “The teacher on the screen. The class on their phones.” A student enters the code; a teacher picks a lesson and starts it live.",
          "The live lesson page with the code entry and the lesson list") + """

<p>Between lessons there are two more pages. <a href="https://zitou.app/vocab/">/vocab</a> teaches the course's 162 words five at a time (listen, see, find) and has a mode where the phone says the words and you only listen. <a href="https://zitou.app/daftar/">/daftar</a> is the word notebook: each word's character, pinyin, meaning, stroke order and audio.</p>

""" + pair("zitou-d6.webp", "zitou-vocab.webp",
           "Left: lesson 6, slide 4 of 19, the new words with tone-coloured pinyin. Right: /vocab, 162 words in six lessons, five at a time.",
           "Lesson 6 slide with four new words", "The HSK 1 word trainer with six lessons") + """

<p>Lesson 6 went in yesterday: the telephone, shopping, food and the taxi. The textbook comes with its own recordings, and they are copyrighted, so I did not use them. Every word that audio-cmn has is a native recording. Every sentence, dialogue and word it lacks is generated with <a href="https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh">Kokoro v1.1-zh</a>, an open speech model under Apache-2.0, in three fixed voices. The pages credit both.</p>

<h2>Two addresses</h2>

<p>Today Zitou got <a href="https://zitou.uz">zitou.uz</a>. The Uzbek pages moved there: the home page, the 7,823 word pages, the dictionary guide, HSK lists, grammar, the mock test, articles and China news. <a href="https://zitou.app">zitou.app</a> keeps the other nine languages and the app.</p>

<p>The split follows one rule. Anything that holds a sign-in or saved progress stays on zitou.app (the app, the course pages, the live games) because a browser keeps those per address, and moving them would have split every learner's progress in two. Pages people read moved freely. A 301 sends every old URL to its new home, so nothing that was indexed or shared breaks.</p>

<p>Opening zitou.app on its own now picks a language. An Uzbek browser, or a visitor in Uzbekistan whose browser is not set to Russian, goes to zitou.uz; everyone else goes to their own language, or to English.</p>

<p>Why .uz at all? Google reads a country domain as a signal for that country, and a teacher in Tashkent can say "zitou nuqta uz" in class without spelling anything. It also gave the class code a short home: a student types <code>zitou.uz/482915</code> and lands in whichever live lesson or game has that code.</p>

<p>Each address has its own sitemaps and robots file, its own Search Console and Bing Webmaster property, and one full RSS feed. <a href="https://zitou.uz/feed.xml">zitou.uz/feed.xml</a> carries release notes, articles, guides and the latest China news together. Questions now go to <a href="mailto:salom@zitou.uz">salom@zitou.uz</a>.</p>

""" + fig("zitou-poster.webp",
          "An A4 poster for classrooms. The QR code opens zitou.uz; the class code works for lessons and games alike.",
          "Zitou classroom poster in Uzbek with a QR code") + """

<h2>How it is built</h2>

<p>Zitou is one Cloudflare Worker with static assets. The dictionary is not a database: it is static JSON built from CC-CEDICT and the HSK lists, which is how a 124,000-word dictionary runs on the free plan. D1 holds accounts, classes and the news; a Durable Object holds each live game and each live lesson, one room per code.</p>

<p>The free plan is a real constraint. Crawlers once used up the whole daily allowance of requests, so the Worker now keeps a budget: bulk crawlers are turned away before the limit, and Google, Bing and Yandex are always served.</p>

<p>The two addresses are one deploy. A single file decides which host a path belongs to. The build rewrites every link in every page for the host that serves it and writes each host's sitemaps and robots file; the Worker does the redirects and rewrites the pages it renders itself. The domain went live in two steps, first attached and checked with the old code and only then the redirects, because the .uz registry took about two hours to hand over the nameservers.</p>

<h2>Telegram and open data</h2>

<p>The channel <a href="https://t.me/zitougg">@zitougg</a> posts one HSK word a day with its recording and its stroke animation. The bot <a href="https://t.me/zitouggbot">@zitouggbot</a> looks words up in any chat, sends greetings in Chinese, and runs a daily word and quiz in groups.</p>

<p>The vocabulary underneath is public: <a href="https://huggingface.co/datasets/Maqsudjonpolatov/hsk-chinese-uzbek-russian">8,296 HSK words with Uzbek and Russian meanings</a> on Hugging Face under CC BY 4.0, with a small dictionary Space next to it.</p>

<h2>The numbers as they are</h2>

<p>On 12 October Search Console showed about 5,950 pages indexed, and 927 impressions and 19 clicks over 28 days. That is small, and most of the impressions came from the HSK 7–9 list pages, which answer questions nobody in Uzbekistan is asking yet. zitou.uz is there to move those numbers for the pages that matter here. I will write down what happens.</p>

<p>The iPhone and Android versions are coming. Until then Zitou runs in the browser and installs to the home screen from zitou.app.</p>

<h2>What I'm not claiming</h2>

<ul>
<li>The Uzbek and Russian meanings were written with AI help. They are corrected from learners' reports, and both the app and the dataset say so.</li>
<li>I am a beginner in the language this teaches. That keeps me honest about what a beginner needs on day one, and it means anything Chinese should be checked by a native speaker before it is used for more than practice.</li>
<li>It is not the first or the only way to learn Chinese in Uzbek. It is a free one, and it is still early.</li>
</ul>

<p>Try it at <a href="https://zitou.uz">zitou.uz</a> in Uzbek or <a href="https://zitou.app">zitou.app</a> in any other language. Start with HSK 1, or type your own name.</p>
"""

UZ = """
<p class="lede">2026-yil 19-sentabrda xitoy tilini o'rganishni boshladim. O'zbek tilida o'rganish uchun deyarli hech narsa yo'q edi, shuning uchun to'rt kundan keyin Zitou'ning birinchi versiyasi chiqdi. Bir oy o'tib, u bepul ilova: 124 039 so'zli lug'at, HSK'ning hamma ro'yxatlari, 8 563 so'z ona tilida so'zlashuvchi ovozida, sinf uchun olti darslik HSK 1 kursi va bugundan boshlab ikki manzil: o'zbekcha <a href="https://zitou.uz">zitou.uz</a> va qolgan hamma narsa uchun <a href="https://zitou.app">zitou.app</a>.</p>

<p>Bu uzun nusxasi: ichida nima bor, sinf undan qanday foydalanadi, nega endi ikki manzilda turadi, qanday qurilgan va nimani da'vo qilmayman.</p>

""" + pair("zitou-uz-home.webp", "zitou-app-en.webp",
           "Bitta mahsulot, ikki manzil: o'zbekcha zitou.uz va inglizcha zitou.app/en. Yana sakkiz til zitou.app'da.",
           "zitou.uz'dagi o'zbekcha bosh sahifa", "zitou.app/en'dagi inglizcha bosh sahifa") + """

<h2>Ichida nima bor</h2>

<p>Asosi — lug'at va kurs. Lug'at CC-CEDICT'dan: 124 039 so'z, iyeroglif, pinyin (tonli yoki tonsiz) yoki o'zbekcha, ruscha, inglizcha ma'nosi bo'yicha qidiriladi. Ulardan 8 296 tasi, ya'ni HSK 1–6 ning hamma so'zi va hech qaysi ro'yxatda yo'q 472 ta kundalik so'z, o'zbekcha va ruscha ma'noga ega. Kurs HSK'ning uchala ro'yxati bo'yicha: 2025-yilgi yangi ro'yxat (10 057 so'z), HSK 3.0 va HSK 2.0, har bir daraja alohida kurs.</p>

<ul>
<li><strong>Xitoylik ovozi.</strong> 8 563 so'z — audio-cmn'dan (CC BY-SA) ona tilida so'zlashuvchilarning yozuvlari. Qolganlari qurilmaning xitoycha ovozida.</li>
<li><strong>Chiziq tartibi.</strong> Har bir iyeroglif: avval ko'rasiz, keyin kulrang ustidan chizasiz, keyin barmoq bilan yoddan yozasiz. Chiziqlar ma'lumoti — Make Me a Hanzi.</li>
<li><strong>Aqlli takrorlash.</strong> So'z aynan unutay deganingizda qaytadi, FSRS algoritmi bilan. Siz faqat "Boshlash"ni bosasiz.</li>
<li><strong>Tonlar rangda.</strong> 1-ton qizil, 2-ton to'q sariq, 3-ton yashil, 4-ton ko'k — tonni quloq bilan ham, ko'z bilan ham eslab qolasiz.</li>
<li><strong>Grammatika.</strong> HSK 1–4 uchun 103 mavzu: qolip, qisqa qoida, pinyinli misollar, ko'p uchraydigan xato va 2 daqiqalik mashq.</li>
<li><strong>Sinov imtihonlari.</strong> HSK 1–4 haqiqiy HSK 2.0 formatida: tinglash imtihondagidek eshittiriladi, vaqt va o'tish bali bor. HSK 3.0 formatidagi birinchi 1-daraja varianti ham bor.</li>
<li><strong>Kichik vositalar.</strong> Matn, ovoz yoki yozuv rasmini tarjima qiladigan tarjimon; Xitoyga safar uchun 80 dan ortiq ibora; ismingiz xitoycha, iyeroglifma-iyeroglif; Kunlik 5 — darajangizdagi hamma uchun bir xil besh savol, do'stga yuborish uchun; va o'zbek tilidagi Xitoy yangiliklari, har birida manbasi bilan.</li>
</ul>

<p>Hisobsiz, o'nta interfeys tilida, telefon, planshet yoki kompyuter brauzerida ishlaydi.</p>

""" + fig("zitou-word.webp",
          "zitou.uz'dagi 7 823 ta o'zbekcha so'z sahifasidan biri: o'zbekcha va inglizcha ma'nosi, iyerogliflari, chiziq tartibi, ovozi va misol gaplar. Qidiruv tizimlari asosan shu sahifalarni topadi.",
          "zitou.uz'dagi 你好 so'z sahifasi") + """

<h2>HSK 1 kursi — sinf uchun</h2>

<p>Bizda ko'pchilik yolg'iz o'qimaydi: ustoz va kitob bilan sinfda o'tiradi. Shuning uchun Zitou'ning eng yangi qismi o'sha xona uchun. HSK 1 kursida olti dars bor. Ustoz katta ekranda <a href="https://zitou.app/dars/">zitou.app/dars</a> da darsni ochadi va olti xonali kod oladi. O'quvchilar uni telefonda, hisobsiz yozadi va har bir mashqqa birga javob beradi. Kim javob berdi, kim adashdi, kim "tushunmadim" dedi — ustoz shu zahoti ko'radi.</p>

""" + fig("zitou-dars.webp",
          "zitou.app/dars: “Ustoz ekranda. Sinf telefonda.” O'quvchi kodni kiritadi, ustoz darsni tanlab jonli boshlaydi.",
          "Kod kiritish va darslar ro'yxati bilan jonli dars sahifasi") + """

<p>Darslar orasida yana ikki sahifa bor. <a href="https://zitou.app/vocab/">/vocab</a> kursning 162 ta so'zini beshtadan o'rgatadi (tinglaysiz, ko'rasiz, topasiz), unda telefon so'zlarni o'zi aytib beradigan, siz faqat tinglaydigan rejim ham bor. <a href="https://zitou.app/daftar/">/daftar</a> — lug'at daftari: har bir so'zning iyeroglifi, pinyini, ma'nosi, yozilish tartibi va ovozi.</p>

""" + pair("zitou-d6.webp", "zitou-vocab.webp",
           "Chapda: 6-dars, 19 slayddan 4-chisi, yangi so'zlar tonlari rangli pinyin bilan. O'ngda: /vocab, olti darsdagi 162 so'z, beshtadan.",
           "To'rtta yangi so'zli 6-dars slaydi", "Olti darsli HSK 1 so'z mashqi") + """

<p>6-dars kecha qo'shildi: telefon, xarid, taom va taksi. Darslikning o'z audiolari bor, lekin ular mualliflik huquqi bilan himoyalangan, shuning uchun ularni ishlatmadim. audio-cmn'da bor har bir so'z — ona tilida so'zlashuvchining yozuvi. Unda bo'lmagan har bir gap, dialog va so'z Apache-2.0 litsenziyali ochiq nutq modeli <a href="https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh">Kokoro v1.1-zh</a> bilan, uchta doimiy ovozda yasalgan. Sahifalarda ikkalasi ham ko'rsatilgan.</p>

<h2>Ikki manzil</h2>

<p>Bugun Zitou <a href="https://zitou.uz">zitou.uz</a> manziliga ega bo'ldi. O'zbekcha sahifalar o'sha yerga ko'chdi: bosh sahifa, 7 823 ta so'z sahifasi, lug'at qo'llanmasi, HSK ro'yxatlari, grammatika, sinov testi, maqolalar va Xitoy yangiliklari. <a href="https://zitou.app">zitou.app</a>'da qolgan to'qqizta til va ilovaning o'zi qoldi.</p>

<p>Bo'linish bitta qoidaga bo'ysunadi. Kirish yoki saqlangan natijani ushlab turadigan hamma narsa (ilova, kurs sahifalari, jonli o'yinlar) zitou.app'da qoladi, chunki brauzer bularni har bir manzil uchun alohida saqlaydi va ularni ko'chirish har bir o'quvchining natijasini ikkiga bo'lib yuborardi. O'qiladigan sahifalar bemalol ko'chdi. Har bir eski manzil 301 bilan yangi joyiga yo'naltiriladi, shuning uchun indekslangan yoki ulashilgan hech narsa buzilmaydi.</p>

<p>zitou.app'ning o'zi ochilsa, endi tilni tanlaydi. Brauzeri o'zbekcha bo'lgan yoki O'zbekistonda turgan va brauzeri ruschaga sozlanmagan odam zitou.uz'ga o'tadi; qolganlar o'z tiliga yoki inglizchaga.</p>

<p>Nega aynan .uz? Google mamlakat domenini o'sha mamlakat uchun belgi deb o'qiydi, Toshkentdagi ustoz esa darsda "zitou nuqta uz" deb hech narsani harflamasdan ayta oladi. Sinf kodi ham qisqa uy topdi: o'quvchi <code>zitou.uz/482915</code> ni yozadi va shu kodli jonli dars yoki o'yinga tushadi.</p>

<p>Har bir manzilning o'z sitemap'lari va robots fayli, o'z Search Console va Bing Webmaster property'si va bitta to'liq RSS lentasi bor. <a href="https://zitou.uz/feed.xml">zitou.uz/feed.xml</a> yangilanishlar, maqolalar, qo'llanmalar va so'nggi Xitoy yangiliklarini bir joyda beradi. Savollar endi <a href="mailto:salom@zitou.uz">salom@zitou.uz</a> ga.</p>

""" + fig("zitou-poster.webp",
          "Sinflar uchun A4 plakat. QR kod zitou.uz'ni ochadi; sinf kodi darslar uchun ham, o'yinlar uchun ham ishlaydi.",
          "QR kodli o'zbekcha Zitou plakati") + """

<h2>Qanday qurilgan</h2>

<p>Zitou — statik fayllari bilan bitta Cloudflare Worker. Lug'at ma'lumotlar bazasi emas: u CC-CEDICT va HSK ro'yxatlaridan yasalgan statik JSON, 124 ming so'zli lug'at bepul tarifda aynan shu tufayli ishlaydi. D1'da hisoblar, sinflar va yangiliklar; har bir jonli o'yin va jonli dars o'z Durable Object'ida, har bir kodga bitta xona.</p>

<p>Bepul tarif — haqiqiy cheklov. Bir marta botlar kunlik so'rovlar limitini to'liq yeb qo'ygan edi, shuning uchun Worker endi o'z byudjetini yuritadi: ommaviy botlar limitdan oldin to'xtatiladi, Google, Bing va Yandex esa doim xizmat oladi.</p>

<p>Ikki manzil — bitta deploy. Qaysi yo'l qaysi manzilga tegishli ekanini bitta fayl hal qiladi. Build har bir sahifadagi har bir havolani o'sha sahifani beradigan manzilga moslab qayta yozadi va har bir manzilning sitemap'i va robots faylini yaratadi; Worker yo'naltirishlarni bajaradi va o'zi chizadigan sahifalarni qayta yozadi. Domen ikki bosqichda ishga tushdi: avval eski kod bilan ulanib tekshirildi, faqat keyin yo'naltirishlar yoqildi, chunki .uz reyestri nameserver'larni topshirishiga taxminan ikki soat ketdi.</p>

<h2>Telegram va ochiq ma'lumot</h2>

<p><a href="https://t.me/zitougg">@zitougg</a> kanali har kuni bitta HSK so'zini ovozi va yozilish animatsiyasi bilan chiqaradi. <a href="https://t.me/zitouggbot">@zitouggbot</a> boti istalgan chatda so'z topadi, xitoycha tabrik yuboradi va guruhlarda kunlik so'z va test o'tkazadi.</p>

<p>Ostidagi lug'at ochiq: Hugging Face'da CC BY 4.0 bilan <a href="https://huggingface.co/datasets/Maqsudjonpolatov/hsk-chinese-uzbek-russian">o'zbekcha va ruscha ma'noli 8 296 HSK so'zi</a>, yonida kichik lug'at Space'i ham bor.</p>

<h2>Raqamlar qanday bo'lsa, shunday</h2>

<p>12-oktabrda Search Console taxminan 5 950 ta indekslangan sahifa, 28 kunda 927 ko'rsatish va 19 klik ko'rsatdi. Bu kam, va ko'rsatishlarning ko'pi HSK 7–9 ro'yxati sahifalaridan keldi — O'zbekistonda hali hech kim bermayotgan savollarga javob beradigan sahifalar. zitou.uz aynan shu yerda muhim sahifalar raqamini o'zgartirish uchun. Nima bo'lganini yozib boraman.</p>

<p>iPhone va Android versiyalari yo'lda. Ungacha Zitou brauzerda ishlaydi va zitou.app'dan bosh ekranga o'rnatiladi.</p>

<h2>Nimani da'vo qilmayman</h2>

<ul>
<li>O'zbekcha va ruscha ma'nolar sun'iy intellekt yordamida yozilgan. Ular o'quvchilarning xabarlari asosida tuzatib boriladi, ilova ham, dataset ham buni ochiq aytadi.</li>
<li>Men o'rgatayotgan tilda boshlovchiman. Bu boshlovchiga birinchi kuni nima kerakligi haqida meni halol tutadi, lekin xitoycha har qanday narsani mashqdan boshqa maqsadda ishlatishdan oldin ona tilida so'zlashuvchi tekshirishi kerak.</li>
<li>Bu xitoy tilini o'zbek tilida o'rganishning birinchi yoki yagona yo'li emas. Bu bepul yo'llardan biri, va hali boshlanishi.</li>
</ul>

<p>Sinab ko'ring: o'zbekcha <a href="https://zitou.uz">zitou.uz</a>, boshqa tillarda <a href="https://zitou.app">zitou.app</a>. HSK 1 dan boshlang yoki o'z ismingizni yozing.</p>
"""

EN_SLUG = "log-2026-10-19-zitou-chinese-in-uzbek"
UZ_SLUG = "log-2026-10-19-zitou-chinese-in-uzbek-uz"
EN_TITLE = "Zitou: Chinese in Uzbek, at zitou.uz and zitou.app"
UZ_TITLE = "Zitou: xitoy tili o'zbek tilida, zitou.uz va zitou.app"
EN_DESC = ("A free app for learning Chinese in Uzbek and nine other languages: a 124,039-word dictionary, "
           "every HSK list, a six-lesson HSK 1 course for classrooms, why it now lives at two addresses, "
           "how it is built and the numbers as they are.")
UZ_DESC = ("Xitoy tilini o'zbek va yana to'qqiz tilda o'rganish uchun bepul ilova: 124 039 so'zli lug'at, "
           "HSK'ning hamma ro'yxatlari, sinf uchun olti darslik HSK 1 kursi, nega endi ikki manzilda, "
           "qanday qurilgan va raqamlar qanday bo'lsa, shunday.")

# OG rasmlari avval: build() ularni o'zi topadi
from build_og import make
make(EN_SLUG, "Chinese in Uzbek, at zitou.uz and zitou.app",
     "124,039 words · every HSK list · an HSK 1 course for classrooms · free", "19 OCT 2026", "PRODUCT", 70)
make(UZ_SLUG, "Xitoy tili o'zbek tilida: zitou.uz va zitou.app",
     "124 039 so'z · HSK ro'yxatlari · sinf uchun HSK 1 kursi · bepul", "19 OKT 2026", "MAHSULOT", 70)

build(EN_SLUG, "en", EN_TITLE, EN_DESC, "19 OCT 2026", "2026-10-19", "PRODUCT", EN,
      UZ_SLUG, "O'ZBEKCHA", "← ALL ENTRIES")
build(UZ_SLUG, "uz", UZ_TITLE, UZ_DESC, "19 OKT 2026", "2026-10-19", "MAHSULOT", UZ,
      EN_SLUG, "ENGLISH", "← BARCHA YOZUVLAR")

# bosh sahifadagi jonli feed va /log/ arxivi (add_log_entries'ning o'z funksiyalari)
import add_log_entries as A
entry = {
    "date": "2026-10-19", "tag": "Tech", "slug": EN_SLUG, "title": EN_TITLE,
    "body": ("I started learning Chinese on 19 September, and there was very little to learn it with in Uzbek, "
             "so I built Zitou. A month on it is a free app: a 124,039-word dictionary, every HSK list, native audio "
             "for 8,563 words, stroke-order writing, spaced repetition, grammar and HSK mock exams, in ten languages, "
             "with no account needed.\n\n"
             "The newest part is for classrooms: an HSK 1 course of six lessons that a teacher runs on the big screen "
             "while the class answers on their phones with a six-digit code, plus a word trainer for the course's "
             "162 words and a word notebook. Lesson 6 went in on 18 October, voiced with native recordings and an "
             "open speech model instead of the textbook's copyrighted audio.\n\n"
             "Today Zitou got zitou.uz. The Uzbek pages live there now; zitou.app keeps the other nine languages and "
             "the app, because sign-ins and saved progress belong to one address. A class joins with zitou.uz/ and "
             "the code, and each address has its own sitemaps, Search Console property and full RSS feed.\n\n"
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
    block = (f'  <url><loc>{BASE}/log/{EN_SLUG}.html</loc><lastmod>2026-10-19</lastmod>{alt}\n'
             f'  <url><loc>{BASE}/log/{UZ_SLUG}.html</loc><lastmod>2026-10-19</lastmod>{alt}\n')
    i = s.index(f"  <url><loc>{BASE}/log/log-")
    sm.write_text(s[:i] + block + s[i:])
    print("  sitemap.xml: +2")

import build_feed
build_feed.main()
print("zitou: EN + UZ yozildi")
