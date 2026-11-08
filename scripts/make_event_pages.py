"""Generate the Bibaha Panchami 2083 and Chhath 2083 pages from the Bhai Tika page's look and countdown.
Run from repo root: python3 scripts/make_event_pages.py"""
import re, json, html, datetime, sys
sys.path.insert(0, 'scripts')
import bs_data as bs

tpl = open('2083/tihar/bhai-tika.html', encoding='utf8').read()
STYLE = re.search(r'<style>.*?</style>', tpl, re.S).group(0)
FONTS = re.findall(r'<link rel="preconnect".*?<noscript>.*?</noscript>', tpl, re.S)[0]
BASE = 'https://converter.thenepal.io'
SRC = 'Dates are calculated from the BS calendar tables on this site and checked against published Nepali calendars.'

def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r'<[^>]+>', '', a))}} for q, a in faqs]}

def page(slug, title, desc, h1, h1ne, answer, facts, target_iso, cd_label, cd_done, sections, faqs, related, event):
    url = f'{BASE}/2083/{slug}'
    ld = {"@context": "https://schema.org", "@graph": [event, faq_ld(faqs), {
        "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://thenepal.io/"},
            {"@type": "ListItem", "position": 2, "name": "Tools", "item": BASE + "/"},
            {"@type": "ListItem", "position": 3, "name": "2083", "item": BASE + "/nepali-calendar-2083/"},
            {"@type": "ListItem", "position": 4, "name": h1, "item": url}]}]}
    faq_html = ''.join(f'    <details{" open" if i==0 else ""}>\n      <summary>{q}</summary>\n      <p>{a}</p>\n    </details>\n' for i, (q, a) in enumerate(faqs))
    rel = ''.join(f'      <li><a href="{BASE}{h}">{t}</a></li>\n' for h, t in related)
    fact_html = ''.join(f'        <div><dt>{k}</dt><dd>{v}</dd></div>\n' for k, v in facts)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="geo.region" content="NP">
<meta property="og:type" content="article">
<meta property="og:site_name" content="TheNepal.io">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="theme-color" content="#2a1740">
<link rel="preload" href="/header.html" as="fetch" crossorigin>
<link rel="preload" href="/footer.html" as="fetch" crossorigin>
{FONTS}
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
{STYLE}
</head>
<body>
  <div id="header" style="min-height:61px"></div>
<a class="skip" href="#main-content">Skip to main content</a>

<header class="hero">
  <div class="wrap">
    <div>
      <p class="crumbs"><a href="https://thenepal.io/">Home</a> / <a href="{BASE}/">Tools</a> / <a href="{BASE}/nepali-calendar-2083/">2083</a> / {h1}</p>
      <h1>{h1}</h1>
      <p class="h1ne ne">{h1ne}</p>
      <p class="answer">{answer}</p>
      <dl class="facts">
{fact_html}      </dl>
    </div>
    <div class="tika" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
  </div>
</header>

<div class="count" role="timer" aria-label="Countdown">
  <div class="wrap">
    <p id="cdlabel">{cd_label}</p>
    <div class="clock" id="clock">
      <div><b id="d">–</b><small>days</small></div>
      <div><b id="h">–</b><small>hours</small></div>
      <div><b id="m">–</b><small>minutes</small></div>
      <div><b id="s">–</b><small>seconds</small></div>
    </div>
  </div>
</div>
<main id="main-content" class="wrap">

{sections}
  <section aria-labelledby="faq">
    <h2 id="faq">{h1.split(":")[0]}: frequently asked questions</h2>
{faq_html}  </section>

  <section aria-labelledby="related">
    <h2 id="related">Related pages for 2083 BS</h2>
    <ul>
{rel}    </ul>
  </section>

  <p class="sources"><strong>Sources and updates.</strong> {SRC} Last reviewed Nov 2026. If your family follows a different patro, confirm with it.</p>
</main>
<div id="footer"></div>
<script src="/components.js"></script>
<script>
(function(){{
  var target = new Date("{target_iso}").getTime();
  var ids = ["d","h","m","s"].map(function(i){{return document.getElementById(i)}});
  var clock = document.getElementById("clock");
  function pad(n){{return n<10?"0"+n:""+n}}
  function tick(){{
    var diff = target - Date.now();
    if(diff <= 0){{ clock.innerHTML = '<span id="done">{cd_done}</span>'; return; }}
    var s = Math.floor(diff/1000);
    ids[0].textContent = Math.floor(s/86400);
    ids[1].textContent = pad(Math.floor(s%86400/3600));
    ids[2].textContent = pad(Math.floor(s%3600/60));
    ids[3].textContent = pad(s%60);
    setTimeout(tick, 1000);
  }}
  tick();
}})();
</script>
</body>
</html>
'''

def ad(m, d):
    x = bs.bs_to_ad(2083, m, d)
    return x

# ---------------- Bibaha Panchami ----------------
sait = [(9,'Day and night'),(10,'Day and night'),(16,'Night'),(17,'Daytime'),(19,'Night'),(24,'Night'),(25,'Night'),(26,'Daytime')]
rows = ''.join(f'<tr><td>Mangsir {d}</td><td>{ad(8,d).strftime("%a, %b %-d, %Y")}</td><td>{t}</td></tr>' for d,t in sait)
bp_sections = f'''  <section aria-labelledby="date">
    <h2 id="date">Bibaha Panchami 2083 date</h2>
    <p><strong>Date:</strong> Monday, December 14, 2026, which is Mangsir 28, 2083 BS. Bibaha Panchami (also Vivah Panchami) falls on Mangsir Shukla Panchami, the fifth day of the bright lunar fortnight in the month of Mangsir (Margashirsha).</p>
    <p><strong>What it marks:</strong> the wedding of Lord Ram and Sita in Janakpur. The main celebration is at Janaki Mandir in Janakpurdham, Madhesh Province, where a wedding procession and a ceremonial marriage are held. It is listed as a holiday in Madhesh Province.</p>
    <p class="note">In Mithila tradition many families avoid holding their own weddings on this day. Mangsir 28 is also not among the official marriage sait dates for 2083 (listed below). Ask your pandit if you are planning a ceremony near it.</p>
  </section>

  <section aria-labelledby="sait">
    <h2 id="sait">Wedding sait in Mangsir 2083</h2>
    <p>Mangsir 2083 runs from November 17 to December 15, 2026. The published marriage lagan list for 2083 has <strong>8 dates in Mangsir</strong>:</p>
    <div class="tablebox">
      <table>
        <thead><tr><th>Nepali date</th><th>English date</th><th>Lagan time</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p>After Mangsir there is no marriage sait in Poush. The next ones are 6 dates in Magh (starting Jan 18, 2027) and 12 in Falgun, the busiest month. See the full list on the <a href="{BASE}/2083/subha-sait">Shubha Sait 2083 page</a>, which also covers Bratabandha, Pasni and Griha Pravesh.</p>
  </section>

  <section aria-labelledby="holiday">
    <h2 id="holiday">Is Bibaha Panchami a public holiday?</h2>
    <p>It is a holiday in Madhesh Province, not a nationwide holiday. See the <a href="{BASE}/2083/nepal-public-holidays">2083 public holidays list</a> for national dates.</p>
  </section>
'''
bp_faqs = [
 ("When is Bibaha Panchami 2083?", "Bibaha Panchami 2083 is on <strong>Monday, December 14, 2026</strong>, which is Mangsir 28, 2083 BS (Mangsir Shukla Panchami)."),
 ("How many marriage sait dates are there in Mangsir 2083?", "There are 8 marriage sait dates in Mangsir 2083: Mangsir 9, 10, 16, 17, 19, 24, 25 and 26 (Nov 25, Nov 26, Dec 2, Dec 3, Dec 5, Dec 10, Dec 11 and Dec 12, 2026)."),
 ("Is Mangsir 28 a marriage sait?", "No. Bibaha Panchami (Mangsir 28, Dec 14, 2026) is not among the 2083 marriage lagan dates, and many Mithila families avoid weddings on this day."),
 ("When does Mangsir 2083 start and end?", "Mangsir 2083 starts on November 17, 2026 and ends on December 15, 2026."),
 ("Is Bibaha Panchami a public holiday in Nepal?", "It is a holiday in Madhesh Province, where the main celebration is held at Janaki Mandir in Janakpurdham. It is not a nationwide public holiday."),
]
bp_event = {"@type": "Event", "name": "Bibaha Panchami 2083", "startDate": "2026-12-14", "endDate": "2026-12-14",
  "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {"@type": "Place", "name": "Janakpurdham, Nepal", "address": {"@type": "PostalAddress", "addressCountry": "NP"}},
  "description": "Wedding of Ram and Sita, celebrated on Mangsir Shukla Panchami in Janakpurdham."}
bp = page('bibaha-panchami',
  'Bibaha Panchami 2083: Mon, Dec 14, 2026 (Mangsir 28) + Wedding Sait | विवाह पञ्चमी',
  'Bibaha Panchami 2083 is on Monday, December 14, 2026 (Mangsir 28, 2083 BS). Date, days left, and all 8 marriage sait dates in Mangsir 2083 with English dates.',
  'Bibaha Panchami 2083: Date and Wedding Sait',
  'विवाह पञ्चमी २०८३ — मंसिर २८ गते, सोमबार',
  '<strong>Bibaha Panchami 2083 is on Monday, December 14, 2026</strong> (Mangsir 28, 2083 BS). Mangsir has 8 marriage sait dates, listed below.',
  [('English date','Mon, Dec 14, 2026'),('Nepali date','Mangsir 28, 2083 BS'),('Tithi','Mangsir Shukla Panchami'),('Mangsir sait','8 dates')],
  '2026-12-14T00:00:00+05:45','Time left until Bibaha Panchami 2083 begins in Nepal (midnight, Dec 14)','Bibaha Panchami is today in Nepal',
  bp_sections, bp_faqs,
  [('/2083/subha-sait','Shubha Sait 2083 (all marriage dates)'),('/nepali-calendar-2083/mangsir-2083','Mangsir 2083 calendar'),('/2083/nepal-public-holidays','Public holidays 2083'),('/nepali-calendar-2083/','Nepali calendar 2083'),('/bs-to-ad/','BS to AD converter')],
  bp_event)
open('2083/bibaha-panchami.html','w',encoding='utf8').write(bp)

# ---------------- Chhath ----------------
ch_sections = '''  <section aria-labelledby="date">
    <h2 id="date">Chhath 2083 dates and arghya times</h2>
    <p>Chhath is a four-day festival of sun worship. In 2083 the main day, with the evening offering to the setting sun (Sandhya Arghya), is <strong>Sunday, November 15, 2026</strong> (Kartik 29), on Kartik Shukla Shashthi.</p>
    <div class="tablebox">
      <table>
        <thead><tr><th>Day</th><th>Nepali date</th><th>English date</th><th>What happens</th></tr></thead>
        <tbody>
          <tr><td>Nahay-Khay</td><td>Kartik 27</td><td>Fri, Nov 13</td><td>Bathing and a pure meal; the fast begins</td></tr>
          <tr><td>Kharna</td><td>Kartik 28</td><td>Sat, Nov 14</td><td>Day-long fast, broken after sunset with kheer</td></tr>
          <tr><td>Sandhya Arghya</td><td>Kartik 29</td><td>Sun, Nov 15</td><td>Offering to the setting sun at a river or pond (sunset about 5:11 PM in Kathmandu)</td></tr>
          <tr><td>Usha Arghya</td><td>Kartik 30</td><td>Mon, Nov 16</td><td>Offering to the rising sun (sunrise about 6:25 AM in Kathmandu); the fast ends</td></tr>
        </tbody>
      </table>
    </div>
    <p class="note">Sunset and sunrise are calculated for Kathmandu. They differ by a few minutes in other cities (for example Janakpur, Biratnagar and Birgunj), so follow your local ghat committee or patro for the exact time.</p>
  </section>

  <section aria-labelledby="what">
    <h2 id="what">What is Chhath?</h2>
    <p>Chhath Parva is dedicated to the sun god Surya and Chhathi Maiya. It is celebrated mostly by Madhesi and Tharu communities and by Bihari and Maithili families, with large gatherings on river banks, ponds and ghats across Nepal's Terai and in Kathmandu. Devotees fast without water for about 36 hours and offer fruit, thekua and sugarcane to the sun.</p>
  </section>

  <section aria-labelledby="holiday">
    <h2 id="holiday">Is Chhath a holiday in Nepal?</h2>
    <p>Chhath is included in the 2083 public holiday list on Kartik 29 (Nov 15, 2026). Confirm with your office or school, since local notices can differ. See the full <a href="https://converter.thenepal.io/2083/nepal-public-holidays">2083 holidays list</a>.</p>
  </section>
'''
ch_faqs = [
 ("When is Chhath 2083?", "The main day of Chhath 2083, with the Sandhya Arghya (evening offering), is <strong>Sunday, November 15, 2026</strong> (Kartik 29, 2083 BS). The festival runs from Friday, November 13 to Monday, November 16."),
 ("What time is the Chhath arghya in Kathmandu?", "In Kathmandu the sun sets at about 5:11 PM on November 15 (Sandhya Arghya) and rises at about 6:25 AM on November 16 (Usha Arghya). Times differ slightly by city."),
 ("What are the four days of Chhath?", "Nahay-Khay (Nov 13), Kharna (Nov 14), Sandhya Arghya (Nov 15) and Usha Arghya (Nov 16)."),
 ("Is Chhath a public holiday in Nepal?", "Chhath, Kartik 29 (November 15, 2026), is in the 2083 holiday list. Check your office or school notice to confirm."),
 ("How many days left for Chhath 2083?", "Use the countdown at the top of this page. It counts down to the evening arghya on November 15, 2026 at about 5:11 PM Nepal time."),
]
ch_event = {"@type": "Event", "name": "Chhath Parva 2083", "startDate": "2026-11-13", "endDate": "2026-11-16",
  "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {"@type": "Place", "name": "Nepal", "address": {"@type": "PostalAddress", "addressCountry": "NP"}},
  "description": "Four-day sun worship festival; Sandhya Arghya on Kartik 29 (Nov 15, 2026)."}
ch = page('chhath-parva',
  'Chhath 2083: Sunday, Nov 15, 2026 (Kartik 29) — Arghya Time in Kathmandu | छठ पर्व',
  'Chhath 2083 main day is Sunday, November 15, 2026 (Kartik 29, 2083 BS). Four-day dates, sunset and sunrise arghya times for Kathmandu, and days left.',
  'Chhath 2083: Date and Arghya Time',
  'छठ पर्व २०८३ — कात्तिक २९ गते, आइतबार',
  '<strong>Chhath 2083 main day is Sunday, November 15, 2026</strong> (Kartik 29, 2083 BS). Evening arghya at about 5:11 PM in Kathmandu; morning arghya on Nov 16 at about 6:25 AM.',
  [('Main day','Sun, Nov 15, 2026'),('Nepali date','Kartik 29, 2083 BS'),('Evening arghya','About 5:11 PM'),('Morning arghya','About 6:25 AM, Nov 16')],
  '2026-11-15T17:11:00+05:45','Time left until the Chhath 2083 evening arghya (about 5:11 PM, Nov 15)','Chhath arghya time has arrived in Nepal',
  ch_sections, ch_faqs,
  [('/2083/tihar/bhai-tika','Bhai Tika 2083'),('/2083/tihar/','Tihar 2083'),('/nepali-calendar-2083/kartik-2083','Kartik 2083 calendar'),('/2083/nepal-public-holidays','Public holidays 2083'),('/bs-to-ad/','BS to AD converter')],
  ch_event)
open('2083/chhath-parva.html','w',encoding='utf8').write(ch)
print('done')
