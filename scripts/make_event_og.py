#!/usr/bin/env python3
"""Date-card OG images (1200x630) for festival/sait pages that had no og:image. Run from repo root.
Renders with Chromium (Devanagari shaping) and adds og:image/twitter:image + Event.image to the pages."""
import os, re, json, asyncio
from playwright.async_api import async_playwright
BASE = 'https://converter.thenepal.io'
# slug path -> (English name, date line, BS line, Nepali name)
P = {
 '2083/bibaha-panchami': ('Bibaha Panchami 2083', 'Mon, Dec 14, 2026', 'Mangsir 28, 2083 BS', 'विवाह पञ्चमी'),
 '2083/chhath-parva': ('Chhath Parva 2083', 'Sun, Nov 15, 2026', 'Arghya day · Kartik 29, 2083 BS', 'छठ पर्व'),
 '2083/christmas-nepal': ('Christmas 2083', 'Fri, Dec 25, 2026', 'Poush 10, 2083 BS', 'क्रिसमस'),
 '2083/falgun-bibaha-sait': ('Falgun 2083 Marriage Dates', '12 Bibaha Sait', 'From Feb 15, 2027', 'फाल्गुन विवाह साइत'),
 '2083/gyalpo-lhosar': ('Gyalpo Lhosar 2083', 'Tue, Mar 9, 2027', 'Falgun 25, 2083 BS', 'ग्याल्पो ल्होसार'),
 '2083/holi': ('Holi 2083', 'Sun, Mar 21, 2027', 'Chaitra 7, 2083 BS', 'होली'),
 '2083/magh-bibaha-sait': ('Magh 2083 Marriage Dates', '6 Bibaha Sait', 'From Jan 18, 2027', 'माघ विवाह साइत'),
 '2083/maghe-sankranti': ('Maghe Sankranti 2083', 'Fri, Jan 15, 2027', 'Magh 1, 2083 BS', 'माघे सङ्क्रान्ति'),
 '2083/maha-shivaratri': ('Maha Shivaratri 2083', 'Sat, Mar 6, 2027', 'Falgun 22, 2083 BS', 'महाशिवरात्रि'),
 '2083/poush-bibaha-sait': ('Poush 2083 Marriage Dates', 'No sait this month', 'Next: Magh 4, 2083 BS', 'पौष विवाह साइत'),
 '2083/prajatantra-diwas': ('Democracy Day 2083', 'Fri, Feb 19, 2027', 'Falgun 7, 2083 BS', 'प्रजातन्त्र दिवस'),
 '2083/prithvi-jayanti': ('Prithvi Jayanti 2083', 'Mon, Jan 11, 2027', 'Poush 27, 2083 BS', 'पृथ्वी जयन्ती'),
 '2083/saraswati-puja': ('Saraswati Puja 2083', 'Thu, Feb 11, 2027', 'Magh 28, 2083 BS', 'सरस्वती पूजा'),
 '2083/shahid-diwas': ("Martyrs' Day 2083", 'Sat, Jan 30, 2027', 'Magh 16, 2083 BS', 'शहीद दिवस'),
 '2083/sonam-lhosar': ('Sonam Lhosar 2083', 'Sun, Feb 7, 2027', 'Magh 24, 2083 BS', 'सोनाम ल्होसार'),
 '2083/tamu-lhosar': ('Tamu Lhosar 2083', 'Wed, Dec 30, 2026', 'Poush 15, 2083 BS', 'तमु ल्होसार'),
 '2083/yomari-punhi': ('Yomari Punhi 2083', 'Thu, Dec 24, 2026', 'Poush 9, 2083 BS', 'योमरी पुन्ही'),
 '2084/dashain': ('Dashain 2084', 'Estimated Sep 30 – Oct 10, 2027', 'Official date to be confirmed', 'दशैं २०८४'),
 '2084/nepali-new-year': ('Nepali New Year 2084', 'Wed, Apr 14, 2027', 'Baisakh 1, 2084 BS', 'नयाँ वर्ष'),
 '2084/tihar': ('Tihar & Bhai Tika 2084', 'Estimated Oct 27–31, 2027', 'Official date to be confirmed', 'तिहार २०८४'),
}
FONT = os.path.abspath('scripts/fonts')
def card(n, d, b, ne):
    return f'''<style>
@font-face{{font-family:ND;src:url(file://{FONT}/noto-sans-devanagari-devanagari-700-normal.woff2);font-weight:700}}
*{{margin:0;box-sizing:border-box}}body{{width:1200px;height:630px;background:#1c1c1e;color:#fffaf4;font-family:'DejaVu Sans',Arial,sans-serif;position:relative;overflow:hidden}}
.t{{position:absolute;left:0;right:0;top:0;height:12px;background:#c0392b}}.bt{{position:absolute;left:0;right:0;bottom:0;height:12px;background:#f5c26b}}
.w{{position:absolute;left:70px;right:70px;top:70px;font:700 34px/1 'DejaVu Serif',serif;color:#fffaf4}}.w i{{font-style:normal;color:#f5c26b}}
.ne{{position:absolute;left:70px;right:70px;top:160px;font:700 64px/1.3 ND,sans-serif;color:#f5c26b}}
.n{{position:absolute;left:70px;right:70px;top:250px;font:700 {58 if len(n)<27 else 46}px/1.15 'DejaVu Serif',serif}}
.d{{position:absolute;left:70px;right:70px;top:400px;font:700 {50 if len(d)<24 else 42}px/1.2 'DejaVu Sans',sans-serif}}
.b{{position:absolute;left:70px;right:70px;top:480px;font:400 32px/1.2 'DejaVu Sans',sans-serif;color:#d9d2c5}}
.f{{position:absolute;left:70px;bottom:36px;font:400 24px 'DejaVu Sans',sans-serif;color:#a69f93}}
</style><div class="t"></div><div class="w">TheNepal<i>.io</i></div><div class="ne">{ne}</div><div class="n">{n}</div><div class="d">{d}</div><div class="b">{b}</div><div class="f">converter.thenepal.io</div><div class="bt"></div>'''
async def main():
    async with async_playwright() as pw:
        br = await pw.chromium.launch(); pg = await br.new_page(viewport={'width':1200,'height':630})
        for path, (n, d, b, ne) in P.items():
            html = '<meta charset="utf-8">' + card(n, d, b, ne)
            open('/tmp/_card.html','w',encoding='utf-8').write(html)
            await pg.goto('file:///tmp/_card.html'); await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=f'assets/og/{path.split("/")[-1]}.png')
        await br.close()
asyncio.run(main())
for path, (n, d, b, ne) in P.items():
    slug = path.split('/')[-1]; f = path + '.html'; s = open(f, encoding='utf-8').read(); url = f'{BASE}/assets/og/{slug}.png'
    if 'og:image' not in s:
        tags = (f'<meta property="og:image" content="{url}">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                f'<meta name="twitter:image" content="{url}">\n')
        s = s.replace('<meta name="twitter:card"', tags + '<meta name="twitter:card"', 1)
    if '"@type": "Event",' in s and f'"image": "{url}"' not in s:
        s = s.replace('"@type": "Event",', f'"@type": "Event",\n   "image": ["{url}"],', 1)
    open(f, 'w', encoding='utf-8').write(s)
print('og cards ok', len(P))
