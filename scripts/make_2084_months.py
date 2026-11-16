#!/usr/bin/env python3
"""Generate /nepali-calendar-2084/<month>-2084 pages (12). Run from repo root: python3 scripts/make_2084_months.py
Dates come from scripts/bs_data.py (two datasets agree for 2084). Only fixed-date national days are listed;
lunar festivals are not listed until the government publishes the holiday notice."""
import re, json, html, sys, calendar
sys.path.insert(0, 'scripts')
import bs_data as bs

BASE = 'https://converter.thenepal.io'
Y = 2084
tpl = open('2083/chhath-parva.html', encoding='utf8').read()
HEAD_FONTS = re.findall(r'<link rel="preconnect".*?<noscript>.*?</noscript>', tpl, re.S)[0]
STYLE = re.search(r'<style>.*?</style>', tpl, re.S).group(0)
STYLE = STYLE.replace('</style>', '''
.cal{border-collapse:collapse;width:100%;min-width:0;table-layout:fixed;font-size:15px}
.cal th,.cal td{text-align:center;padding:6px 2px;border:1px solid var(--line);vertical-align:top}
.cal td b{display:block;font-size:17px}.cal td small{display:block;color:#666;font-size:11px}
.cal td.sat b,.cal th.sat{color:#C0392B}.cal td.hol{background:#FEF0EE}.cal td.hol small{color:#96281B}
.cal td.e{background:transparent;border-color:transparent}
.mlinks{display:flex;justify-content:space-between;gap:10px;margin:14px 0;flex-wrap:wrap}
</style>''')

M = [('baisakh','Baisakh','वैशाख'),('jestha','Jestha','जेठ'),('ashadh','Ashadh','आषाढ'),('shrawan','Shrawan','श्रावण'),
     ('bhadra','Bhadra','भदौ'),('ashoj','Ashoj','आश्विन'),('kartik','Kartik','कार्तिक'),('mangsir','Mangsir','मंसिर'),
     ('poush','Poush','पौष'),('magh','Magh','माघ'),('falgun','Falgun','फाल्गुन'),('chaitra','Chaitra','चैत्र')]
# fixed-date national days (BS month, day) -> label
FIXED = {(1,1):'Nepali New Year', (2,15):'Republic Day', (6,3):'Constitution Day', (9,27):'Prithvi Jayanti',
         (10,1):'Maghe Sankranti', (10,16):'Martyrs\' Day', (11,7):'Democracy Day'}
NUM = '०१२३४५६७८९'
def ne(n): return ''.join(NUM[int(c)] for c in str(n))
DOW_NE = ['आइत','सोम','मङ्गल','बुध','बिही','शुक्र','शनि']
DOW_EN = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']

def page(i):
    slug, en, nep = M[i]
    days = bs.CANONICAL[Y][i]
    s = bs.bs_to_ad(Y, i+1, 1); e = bs.bs_to_ad(Y, i+1, days)
    fmt = lambda d: d.strftime('%b %-d, %Y')
    first_dow = (s.weekday()+1) % 7   # Sunday=0
    title = f'{en} {Y} Calendar: {s.strftime("%b %-d")}–{fmt(e)} | {nep} {ne(Y)} पात्रो'
    url = f'{BASE}/nepali-calendar-{Y}/{slug}-{Y}'
    desc = f'{en} {Y} BS calendar: {days} days, {fmt(s)} to {fmt(e)}. {en} 1, {Y} is a {s.strftime("%A")}. Full BS and AD date grid with Saturdays and fixed-date national holidays.'
    # grid
    rows=[]; cells=['<td class="e"></td>']*0
    row=['<td class="e"></td>']*first_dow
    hols=[]
    for d in range(1, days+1):
        a = bs.bs_to_ad(Y, i+1, d); dow=(a.weekday()+1)%7
        h = FIXED.get((i+1,d))
        cls = ('sat ' if dow==6 else '')+('hol' if h else '')
        if h: hols.append((d,a,h))
        row.append(f'<td class="{cls.strip()}"><b>{d}</b><small>{a.strftime("%b %-d")}</small></td>')
        if len(row)==7: rows.append(row); row=[]
    if row: rows.append(row+['<td class="e"></td>']*(7-len(row)))
    grid = '<table class="cal"><thead><tr>'+''.join(f'<th class="{"sat" if k==6 else ""}">{DOW_EN[k]}<br><small>{DOW_NE[k]}</small></th>' for k in range(7))+'</tr></thead><tbody>'+''.join('<tr>'+''.join(r)+'</tr>' for r in rows)+'</tbody></table>'
    sats = [d for d in range(1,days+1) if (bs.bs_to_ad(Y,i+1,d).weekday()+1)%7==6]
    hol_html = ''.join(f'<li><strong>{en} {d}</strong> ({a.strftime("%A, %b %-d, %Y")}): {h}</li>' for d,a,h in hols) or '<li>No fixed-date national day falls in this month. Lunar festivals are added by the government notice, so check the official list once published.</li>'
    faqs = [
      (f'How many days are in {en} {Y}?', f'{en} {Y} BS has {days} days, from {fmt(s)} to {fmt(e)} AD.'),
      (f'What is the AD date of {en} 1, {Y}?', f'{en} 1, {Y} BS falls on {s.strftime("%A, %B %-d, %Y")}.'),
      (f'Which days are Saturdays in {en} {Y}?', f'Saturdays (weekly holiday in Nepal) are {en} ' + ', '.join(map(str, sats)) + f' {Y}.'),
      (f'Are festival dates listed for {en} {Y}?', 'Only fixed-date national days are listed here. Festivals that follow the lunar calendar, such as Dashain, Tihar and Holi, are listed once the government publishes the official holiday notice.'),
    ]
    ld = {"@context":"https://schema.org","@graph":[
      {"@type":"WebPage","@id":url,"url":url,"name":title,"description":desc,"inLanguage":["en","ne"]},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]},
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://thenepal.io/"},
        {"@type":"ListItem","position":2,"name":f"Nepali Calendar {Y}","item":f"{BASE}/{Y}/calendar"},
        {"@type":"ListItem","position":3,"name":f"{en} {Y}","item":url}]}]}
    prev = M[i-1] if i>0 else None; nxt = M[i+1] if i<11 else None
    nav = '<div class="mlinks">'+(f'<a href="{BASE}/nepali-calendar-{Y}/{prev[0]}-{Y}">← {prev[1]} {Y}</a>' if prev else '<span></span>')+(f'<a href="{BASE}/nepali-calendar-{Y}/{nxt[0]}-{Y}">{nxt[1]} {Y} →</a>' if nxt else '<span></span>')+'</div>'
    allm = ' · '.join(f'<a href="{BASE}/nepali-calendar-{Y}/{m[0]}-{Y}">{m[1]}</a>' for m in M)
    faq_html = ''.join(f'<details{" open" if k==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for k,(q,a) in enumerate(faqs))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="TheNepal.io">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="preload" href="/header.html" as="fetch" crossorigin>
<link rel="preload" href="/footer.html" as="fetch" crossorigin>
{HEAD_FONTS}
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{STYLE}
</head>
<body>
<div id="header" style="min-height:61px"></div>
<a class="skip" href="#main-content">Skip to main content</a>
<header class="hero"><div class="wrap"><div>
<p class="crumbs"><a href="https://thenepal.io/">Home</a> / <a href="{BASE}/{Y}/calendar">Nepali Calendar {Y}</a> / {en} {Y}</p>
<h1>{en} {Y} Calendar</h1>
<p class="h1ne ne">{nep} {ne(Y)} पात्रो</p>
<p class="answer">{en} {Y} BS has <strong>{days} days</strong>, from <strong>{fmt(s)}</strong> to <strong>{fmt(e)}</strong>. {en} 1 is a {s.strftime("%A")}.</p>
</div></div></header>
<main id="main-content" class="wrap">
{nav}
<section aria-labelledby="grid"><h2 id="grid">{en} {Y} BS to AD date grid</h2>
<div class="tablebox" style="overflow-x:auto">{grid}</div>
<p class="note">Red dates are Saturdays, the weekly holiday. Shaded dates are fixed-date national days.</p></section>
<section aria-labelledby="hol"><h2 id="hol">National days in {en} {Y}</h2><ul>{hol_html}</ul>
<p class="note">Festivals that follow the lunar calendar are not listed until the government publishes the official holiday notice for {Y}. See the <a href="{BASE}/{Y}/calendar">Nepali calendar {Y}</a> for the year overview.</p></section>
<section aria-labelledby="faq"><h2 id="faq">{en} {Y}: frequently asked questions</h2>{faq_html}</section>
<section aria-labelledby="rel"><h2 id="rel">All months of {Y}</h2><p>{allm}</p>
<p>Need another date? Use the <a href="{BASE}/date-converter/">Nepali date converter</a> or see <a href="{BASE}/today-nepali-date/">today's Nepali date</a>.</p></section>
{nav}
<p class="sources"><strong>Sources.</strong> Month lengths come from the BS calendar tables used across this site, which two independent open-source calendar datasets agree on for {Y}. Last reviewed Nov 2026.</p>
</main>
<div id="footer"></div>
<script src="/components.js"></script>
</body>
</html>
'''

import os
os.makedirs(f'nepali-calendar-{Y}', exist_ok=True)
for i in range(12):
    open(f'nepali-calendar-{Y}/{M[i][0]}-{Y}.html','w',encoding='utf8').write(page(i))
print('ok')
