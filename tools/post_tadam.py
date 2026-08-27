#!/usr/bin/env python3
"""tadam.uz haqidagi batafsil yozuv (EN + UZ)."""
import sys
sys.path.insert(0, "tools")
from build_log_post import build, fig

EN = """
<p class="lede">At an Uzbek wedding there are three hundred guests and three hundred phones. By the end of the night those phones hold the only photographs of the evening that show anything real — the tables, the dancing, the grandmother laughing at something off-camera. The couple will see about twenty of them, forwarded into a group chat and compressed into mush. Tadam is my attempt to fix that with a QR code on the table.</p>

<p>It went live at <a href="https://tadam.uz">tadam.uz</a> on 27 August 2026. This is how it works and everything that was harder than it looked.</p>

<h2>The flow</h2>

<p>The couple creates an album — a title and a date, nothing else, no account. They get back three links: a guest link, a management link, and a printable QR sheet. The QR sheet goes on the tables.</p>

<p>A guest scans it, the camera roll opens, they pick photos, they upload. No app, no sign-up, no password. Then the couple opens the management page and downloads everything as a single ZIP.</p>

""" + fig("tadam-home.webp", "The homepage. The entire flow is explained before you scroll — because most visitors arrive from a Telegram link and will not read.", "Tadam homepage showing the four-step flow") + """

<p>The design constraint that drove everything above the fold: someone sees this link dropped in a wedding Telegram group. They have about four seconds of curiosity. If they have to <em>think</em> about what the site is, they leave. So the four steps are visible immediately, illustrated, with no marketing preamble in front of them.</p>

<h2>No app, and no database either</h2>

<p>The no-app decision is obvious once you picture it: nobody at a wedding, holding a plate, is going to install an app. It has to be a web page that works on the first tap.</p>

<p>The no-database decision was less obvious and I'm still pleased with it. The whole thing runs as a Cloudflare Worker with R2 as the <em>only</em> datastore. There is no SQL, no KV namespace, no Durable Object. Album metadata lives in R2 object metadata; the photo list is an R2 prefix listing. A wedding album is written once, read a few times, and then never touched again — that's a workload that does not need a database, and every database I didn't add is a thing that can't go down at 11pm on a Saturday.</p>

<h2>The name</h2>

<p>It was called Chaqnoq for the first three days. Then I said it out loud to someone and watched them fail to spell it back to me. A wedding product is spoken about, not typed — one person tells another at a table. "Chaqnoq" has a consonant cluster that survives neither speech nor a bad phone speaker.</p>

<p>Tadam is the sound a magician makes when the trick lands. It's two syllables, it's spelled how it sounds in Uzbek, Russian and English alike, and it means the same thing in all three.</p>

<p>Renaming a live codebase is where you find out how many places a brand name hides. I wrote a rename script that was <em>context-aware</em> — it knew the difference between the brand in visible text, the brand in a CSS class name, and the string in an API path that must not change — with a mandatory dry run that printed every match before touching anything. A blind find-and-replace would have quietly broken the URLs of every album already created.</p>

<h2>The QR code, measured rather than assumed</h2>

<p>The QR sheet is the physical product. If it doesn't scan from a seated guest's arm's length, in dim wedding lighting, on a sheet that has had somebody's plov on it, nothing else matters.</p>

""" + fig("tadam-qr.webp", "The printable QR sheet: 64 mm code on A5, error-correction level Q, with the typed URL underneath as a fallback.", "Printable QR sheet for a Tadam album") + """

<p>So I measured it instead of hoping. I rendered the QR at the pixel sizes a phone camera actually sees it at from various distances and ran a decoder against each one. It reads reliably from about 15 cm out to 85 cm, which covers everyone who can reach the sheet. It's generated at error-correction level Q, which by specification reconstructs the payload with roughly a quarter of the code damaged — that's the stain tolerance.</p>

<p>Then the link underneath it. Some guests won't scan; they'll squint and type. The URL was <code>tadam.uz/e/?i=4se48ya9r</code> — 23 characters including a question mark and an equals sign, both of which are a nuisance on a phone keyboard. It's now <code>tadam.uz/4se48ya9r</code>, 18 characters, all lowercase letters and digits. A single-segment path 301-redirects to the real album URL, with a reserved-name guard so that a future <code>/about</code> or <code>/qr</code> can never be mistaken for an album ID.</p>

<p>I was asked whether the ID itself could go from nine characters to seven, and I said no. The privacy model of this product is that the link <em>is</em> the password — anyone holding it sees the photographs. Dropping two characters shrinks the keyspace by a factor of about a thousand. Five saved keystrokes is not worth a thousand-fold weaker guess resistance on other people's wedding photos.</p>

<h2>The parts that were actually hard</h2>

<p><strong>Trusting nothing about an upload.</strong> A file's extension and its <code>Content-Type</code> header are both just claims made by the client. Every upload is sniffed by magic bytes — JPEG, PNG, WebP, GIF and HEIC, the last one requiring a walk into the ISO-BMFF <code>ftyp</code> box because iPhones are the primary camera here. Anything that isn't a real image is refused, and the size is rejected from the <code>Content-Length</code> before the body is read rather than after.</p>

<p><strong>Serving user content safely.</strong> Photos are served under <code>default-src 'none'; sandbox</code>. Even if someone found a way to store something executable, the browser has no permission to run it, reach the network, or touch the parent page. The site itself carries HSTS, <code>nosniff</code>, a referrer policy and a permissions policy.</p>

<p><strong>Random IDs that are actually uniform.</strong> The obvious way to pick a random character is <code>random_byte % alphabet_length</code>. That is biased whenever the alphabet doesn't divide 256 evenly, and early characters come up more often than late ones. I measured it over two million samples: <strong>12.65% bias</strong>. Replaced with rejection sampling, which throws away the out-of-range draws and re-rolls.</p>

<p><strong>Delete, without an account.</strong> Every photo gets a delete key derived by SHA-256 from the album and the photo, so a guest can remove a photo they just uploaded and regretted, and the couple can remove anything. The key comparison is constant-time — a timing-leaky comparison would let someone guess a key one byte at a time.</p>

<p><strong>A ZIP with a progress bar.</strong> Streaming a ZIP out of a Worker gives you no <code>Content-Length</code>, so the browser shows an indeterminate spinner and the couple has no idea whether a 400-photo download is at 10% or 90%. <code>FixedLengthStream</code> is the only mechanism that gets a real length onto a streamed Worker response. Computing that length in advance meant working out the exact byte size of the ZIP before generating it.</p>

""" + fig("tadam-albom.webp", "A demo album. These are Wikimedia Commons wedding photographs uploaded to a test album — I did not screenshot anyone's real album, because they are private.", "Tadam guest album view showing uploaded photos") + """

<h2>Knowing when someone uses it</h2>

<p>I wanted to know the moment a real person creates an album, without giving myself a way to snoop on their photos. So there's an owner page listing albums — titles, dates, photo counts, and links — gated behind an encrypted secret, which returns 404 rather than 403 when the secret isn't configured, so its existence isn't advertised. A Telegram bot messages me when an album is created.</p>

""" + fig("tadam-boshqarish.webp", "The management view the couple gets: share links, the QR sheet, the ZIP download, and per-photo delete.", "Tadam album management page") + """

<p>That page hung the first time it met a realistic amount of data. With around two hundred albums it was making R2 calls one after another and taking long enough that I assumed it had crashed. A concurrency pool of twelve brought it to <strong>0.7 seconds</strong>, and photo counts are only computed for the newest forty albums.</p>

<h2>Details I'm glad I spent time on</h2>

<ul>
<li><strong>Photos delete themselves after 60 days.</strong> An R2 lifecycle rule, and it's stated plainly on the site rather than buried. Storing other people's wedding photographs forever is a liability, not a feature.</li>
<li><strong>Fonts are self-hosted and subsetted.</strong> No Google Fonts request, which removes a whole third-party domain from the critical path and from the content-security policy.</li>
<li><strong>The wordmark performs its own name.</strong> On load, "Tadam" briefly becomes "Ta-dam!" in the gradient of the page's accent rail, then settles back. It's the only decorative animation on the site and it earns its place by explaining the name.</li>
<li><strong>113 tests, no test framework.</strong> Plain Node, no dependencies. They run against a real deployment, including the rate limiter, which meant teaching the album-creation helper to back off on a 429.</li>
</ul>

<h2>What I'm not claiming</h2>

<p>I was tempted to put "the first and only service of its kind in Uzbekistan" on the homepage. I didn't, because I haven't checked every competitor in the country and I can't prove it. It would probably have converted better. It would also have been a claim I'd have to defend the first time somebody found a competitor, and the whole point of building things under my own name is that everything on them holds up.</p>

<p>Here's the honest status: tadam.uz is live, hardened, fast, and has not yet been used at a single real wedding. That's the next thing to fix, and it isn't a code problem.</p>
"""

UZ = """
<p class="lede">O'zbek to'yida uch yuz mehmon va uch yuzta telefon bo'ladi. Kechaning oxiriga borib, o'sha kechaning haqiqiy suratlari — stollar, raqs, kadr tashqarisidagi nimagadir kulib turgan buvi — faqat o'sha telefonlarda qoladi. Kelin-kuyov ulardan yigirmatachasini ko'radi: guruhga tashlangan, siqilib tanib bo'lmas holga kelgan. Tadam — shuni stoldagi QR kod bilan tuzatishga urinishim.</p>

<p><a href="https://tadam.uz">tadam.uz</a> 2026-yil 27-avgustda ishga tushdi. Quyida u qanday ishlashi va ko'ringanidan qiyinroq chiqqan hamma narsa.</p>

<h2>Jarayon</h2>

<p>Kelin-kuyov albom yaratadi — nomi va sanasi, boshqa hech narsa, akkaunt ham yo'q. Javobiga uchta havola oladi: mehmon havolasi, boshqaruv havolasi va chop etiladigan QR varaqasi. QR varaqasi stollarga qo'yiladi.</p>

<p>Mehmon uni skanerlaydi, galereyasi ochiladi, suratlarni tanlaydi, yuklaydi. Ilova yo'q, ro'yxatdan o'tish yo'q, parol yo'q. Keyin kelin-kuyov boshqaruv sahifasini ochib, hammasini bitta ZIP qilib yuklab oladi.</p>

""" + fig("tadam-home.webp", "Bosh sahifa. Butun jarayon skroll qilmasdan tushuntirilgan — chunki kelganlarning ko'pi Telegram havolasidan tushadi va o'qib o'tirmaydi.", "Tadam bosh sahifasi, to'rt qadamli jarayon") + """

<p>Birinchi ekranni belgilagan shart shu edi: odam to'y guruhida havolani ko'rib qoladi. Uning qiziqishi taxminan to'rt soniya. Agar sayt nima ekanini <em>o'ylab</em> topishi kerak bo'lsa, chiqib ketadi. Shuning uchun to'rt qadam darrov ko'rinadi, rasm bilan, oldida marketing muqaddimasisiz.</p>

<h2>Ilova ham yo'q, ma'lumotlar bazasi ham yo'q</h2>

<p>Ilovasizlik qarori ko'z oldingizga keltirsangiz o'z-o'zidan tushunarli: to'yda, qo'lida likopcha ushlab turgan odam hech qachon ilova o'rnatmaydi. Birinchi bosishdayoq ochiladigan veb-sahifa bo'lishi shart.</p>

<p>Ma'lumotlar bazasisizlik qarori kamroq ko'rinib turardi va men undan hali ham mamnunman. Hammasi Cloudflare Worker sifatida ishlaydi, R2 esa <em>yagona</em> ma'lumot ombori. SQL yo'q, KV yo'q, Durable Object yo'q. Albom ma'lumotlari R2 obyekt metadatasida turadi; surat ro'yxati — R2 prefiks ro'yxati. To'y albomi bir marta yoziladi, bir necha marta o'qiladi va keyin umuman tegilmaydi — bunga baza kerak emas, qo'shmagan har bir baza esa shanba kuni kechqurun 11 da ishdan chiqolmaydigan bitta narsa demakdir.</p>

<h2>Nom</h2>

<p>Birinchi uch kun u Chaqnoq deb atalgan. Keyin uni ovoz chiqarib aytdim va odam menga qaytarib yoza olmaganini ko'rdim. To'y mahsuloti haqida yozishmaydi — gapirishadi, bir odam stolda ikkinchisiga aytadi. "Chaqnoq" dagi undoshlar to'plami na og'zaki nutqda, na yomon telefon dinamigida omon qoladi.</p>

<p>Tadam — sehrgar fokusi chiqqanda chiqaradigan tovush. Ikki bo'g'in, o'zbekcha ham, ruscha ham, inglizcha ham qanday eshitilsa shunday yoziladi va uchalasida bir xil ma'no beradi.</p>

<p>Ishlab turgan kod bazasining nomini o'zgartirish — brend nomi necha joyga yashiringanini bilib olish joyi. Men <em>kontekstni tushunadigan</em> qayta nomlash skripti yozdim: u ko'rinadigan matndagi brendni, CSS klassidagi brendni va o'zgarmasligi shart bo'lgan API yo'lidagi qatorni bir-biridan ajratardi, ustiga hech narsaga tegmasdan oldin har bir moslikni chop etadigan majburiy dry-run bor edi. Ko'r-ko'rona qidir-almashtir allaqachon yaratilgan har bir albomning havolasini jimgina buzib qo'yardi.</p>

<h2>QR kod — taxmin qilinmadi, o'lchandi</h2>

<p>QR varaqasi — jismoniy mahsulot. Agar u o'tirgan mehmonning qo'li yetadigan masofadan, to'yning xira yorug'ida, ustiga kimningdir palovi tomgan varaqadan skanerlanmasa, qolgan hamma narsaning ahamiyati yo'q.</p>

""" + fig("tadam-qr.webp", "Chop etiladigan QR varaqasi: A5 da 64 mm kod, Q darajali xato tuzatish, pastida qo'lda yozish uchun havola.", "Tadam albomi uchun QR varaqasi") + """

<p>Shuning uchun umid qilish o'rniga o'lchadim. QR'ni telefon kamerasi turli masofadan qanday piksel o'lchamda ko'rsa, o'shanday chiqarib, har biriga dekoder yurgizdim. U taxminan 15 sm dan 85 sm gacha ishonchli o'qiladi — varaqaga qo'li yetadigan hammani qamraydi. Kod Q darajasida yasaladi, bu esa standart bo'yicha kodning chorak qismi shikastlanganda ham ma'lumotni tiklaydi. Dog'ga chidamlilik shundan keladi.</p>

<p>Keyin ostidagi havola. Ba'zi mehmonlar skanerlamaydi — ko'zini qisib, qo'lda yozadi. Havola <code>tadam.uz/e/?i=4se48ya9r</code> edi — 23 belgi, ichida savol belgisi va teng belgisi bor, ikkalasi ham telefon klaviaturasida azob. Endi u <code>tadam.uz/4se48ya9r</code>, 18 belgi, faqat kichik harf va raqam. Bitta bo'lakdan iborat manzil haqiqiy albom havolasiga 301 bilan yo'naltiriladi, ustiga band nomlar ro'yxati bor — kelajakdagi <code>/about</code> yoki <code>/qr</code> hech qachon albom ID'si deb o'qilmaydi.</p>

<p>Mendan ID'ning o'zini to'qqiz belgidan yettitaga tushirish mumkinmi deb so'rashdi, men yo'q dedim. Bu mahsulotning maxfiylik modeli shundan iborat: havolaning o'zi — parol. Uni ushlagan odam suratlarni ko'radi. Ikkita belgini olib tashlash kalit maydonini taxminan ming barobar kichraytiradi. Beshta tejalgan bosish begona odamlarning to'y suratlari uchun ming barobar zaif himoyaga arzimaydi.</p>

<h2>Rostdan qiyin bo'lgan joylar</h2>

<p><strong>Yuklamaga umuman ishonmaslik.</strong> Faylning kengaytmasi ham, <code>Content-Type</code> sarlavhasi ham — mijoz aytgan da'vo, xolos. Har bir yuklama sehrli baytlar bo'yicha tekshiriladi: JPEG, PNG, WebP, GIF va HEIC. Oxirgisi ISO-BMFF <code>ftyp</code> blokining ichiga kirishni talab qiladi, chunki bu yerda asosiy kamera — iPhone. Haqiqiy rasm bo'lmagan hamma narsa rad etiladi, hajm esa tana o'qilgandan keyin emas, <code>Content-Length</code> dan oldin rad qilinadi.</p>

<p><strong>Foydalanuvchi kontentini xavfsiz uzatish.</strong> Suratlar <code>default-src 'none'; sandbox</code> ostida beriladi. Kimdir bajariladigan narsa saqlash yo'lini topsa ham, brauzerda uni ishga tushirishga, tarmoqqa chiqishga yoki ota-sahifaga tegishga ruxsat yo'q. Saytning o'zida HSTS, <code>nosniff</code>, referrer va permissions siyosatlari bor.</p>

<p><strong>Rostdan bir tekis tasodifiy ID.</strong> Tasodifiy belgi tanlashning ko'zga ko'rinadigan yo'li — <code>tasodifiy_bayt % alifbo_uzunligi</code>. Alifbo 256 ga butun bo'linmasa, bu qiyshiq chiqadi: boshidagi belgilar oxiridagilardan ko'proq tushadi. Ikki million namunada o'lchadim: <strong>12,65% qiyshiqlik</strong>. O'rniga rad etish namunasi (rejection sampling) qo'yildi — diapazondan tashqaridagi tortishlar tashlanadi va qayta tortiladi.</p>

<p><strong>Akkauntsiz o'chirish.</strong> Har bir suratga albom va suratdan SHA-256 orqali chiqariladigan o'chirish kaliti beriladi. Shu tufayli mehmon endigina yuklab pushaymon bo'lgan suratini o'chira oladi, kelin-kuyov esa istaganini. Kalitlar solishtiruvi doimiy vaqtda bajariladi — vaqt sizdiradigan solishtiruv kalitni bir baytdan topib olish imkonini berardi.</p>

<p><strong>Progress-barli ZIP.</strong> Worker'dan ZIP oqim bilan uzatilsa, <code>Content-Length</code> bo'lmaydi. Natijada brauzer noaniq spinner ko'rsatadi va kelin-kuyov 400 ta suratlik yuklama 10% dami yoki 90% dami — bilmaydi. Oqim bilan uzatiladigan Worker javobiga haqiqiy uzunlik qo'yishning yagona yo'li — <code>FixedLengthStream</code>. Uzunlikni oldindan hisoblash esa ZIP'ni yasashdan oldin uning aniq bayt hajmini chiqarishni talab qildi.</p>

""" + fig("tadam-albom.webp", "Namuna albom. Bular sinov albomiga yuklangan Wikimedia Commons to'y suratlari — hech kimning haqiqiy albomini skrinshot qilmadim, chunki ular shaxsiy.", "Tadam mehmon albomi ko'rinishi") + """

<h2>Kimdir ishlatganini bilish</h2>

<p>Haqiqiy odam albom yaratgan lahzada bilishni istadim — lekin o'zimga uning suratlariga mo'ralash yo'lini bermasdan. Shuning uchun albomlar ro'yxatini ko'rsatadigan egalik sahifasi bor: nomlar, sanalar, surat soni va havolalar. U shifrlangan maxfiy kalit ortida, kalit sozlanmagan bo'lsa 403 emas, 404 qaytaradi — ya'ni mavjudligini oshkor qilmaydi. Albom yaratilganda Telegram bot menga xabar yozadi.</p>

""" + fig("tadam-boshqarish.webp", "Kelin-kuyovga tegadigan boshqaruv ko'rinishi: ulashish havolalari, QR varaqasi, ZIP yuklash va har bir suratni o'chirish.", "Tadam albomni boshqarish sahifasi") + """

<p>O'sha sahifa haqiqiy hajmdagi ma'lumot bilan birinchi uchrashuvda osilib qoldi. Ikki yuzga yaqin albomda u R2 chaqiruvlarini ketma-ket qilardi va shunchalik cho'zildiki, men uni ishdan chiqqan deb o'yladim. O'n ikkita parallel oqimli hovuz uni <strong>0,7 soniya</strong> ga tushirdi, surat soni esa faqat eng yangi qirqta albom uchun hisoblanadi.</p>

<h2>Vaqt sarflaganimdan xursand bo'lgan tafsilotlar</h2>

<ul>
<li><strong>Suratlar 60 kundan keyin o'zini o'zi o'chiradi.</strong> Bu R2 lifecycle qoidasi va u saytda ko'mib emas, ochiq yozilgan. Begona odamlarning to'y suratlarini abadiy saqlash — imkoniyat emas, javobgarlik.</li>
<li><strong>Shriftlar o'z serverimizda va qirqilgan.</strong> Google Fonts so'rovi yo'q, ya'ni kritik yo'ldan ham, kontent xavfsizlik siyosatidan ham butun boshli uchinchi tomon domeni chiqib ketdi.</li>
<li><strong>Yozuv o'z nomini o'ynab ko'rsatadi.</strong> Sahifa ochilganda "Tadam" bir lahza sahifaning gradient chizig'i rangida "Ta-dam!" ga aylanadi, keyin o'z holiga qaytadi. Saytdagi yagona bezak animatsiyasi va u nomni tushuntirgani uchun o'z o'rnini oqlaydi.</li>
<li><strong>113 ta test, test freymvorkisiz.</strong> Sof Node, tashqi paketsiz. Ular haqiqiy deploy'ga qarshi ishlaydi, so'rov cheklagichi bilan birga — shuning uchun albom yaratish yordamchisiga 429 kelganda kutishni o'rgatishga to'g'ri keldi.</li>
</ul>

<h2>Nima demayman</h2>

<p>Bosh sahifaga "O'zbekistonda birinchi va yagona shunday xizmat" deb yozish ko'nglimga kelgan edi. Yozmadim, chunki mamlakatdagi har bir raqobatchini tekshirmaganman va buni isbotlay olmayman. Ehtimol, u yaxshiroq konversiya berardi. Shu bilan birga, kimdir raqobatchini topgan birinchi kuniyoq himoya qilishim kerak bo'lgan da'vo bo'lardi — o'z nomim ostida narsa qurishning butun ma'nosi esa ulardagi hamma gap tekshiruvga bardosh berishida.</p>

<p>Halol holat shunday: tadam.uz jonli, himoyalangan, tez — va hali birorta ham haqiqiy to'yda ishlatilmagan. Keyingi tuzatiladigan narsa shu, va u kod muammosi emas.</p>
"""

EN_SLUG = "log-2026-08-27-tadam-wedding-photo-album"
UZ_SLUG = "log-2026-08-27-tadam-wedding-photo-album-uz"

build(EN_SLUG, "en",
      "Tadam: a wedding album with no app and no database",
      "How tadam.uz works: guests scan a QR code on the table, upload the photos "
      "already on their phones, and the couple downloads everything as a ZIP. "
      "Cloudflare Workers, R2 only, and a QR code I measured instead of assuming.",
      "27 AUG 2026", "2026-08-27", "PRODUCT", EN,
      UZ_SLUG, "O'ZBEKCHA", "← ALL ENTRIES")

build(UZ_SLUG, "uz",
      "Tadam: ilovasiz va bazasiz to'y albomi",
      "tadam.uz qanday ishlaydi: mehmonlar stoldagi QR kodni skanerlaydi, "
      "telefonidagi suratlarni yuklaydi, kelin-kuyov esa hammasini ZIP qilib oladi. "
      "Cloudflare Workers, faqat R2 va taxmin qilinmay o'lchangan QR kod.",
      "27 AVG 2026", "2026-08-27", "MAHSULOT", UZ,
      EN_SLUG, "ENGLISH", "← BARCHA YOZUVLAR")

print("tadam: EN + UZ yozildi")
