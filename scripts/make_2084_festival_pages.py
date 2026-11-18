"""Dashain 2084 and Tihar 2084 pages (estimates). Dates were computed from sunrise tithi at Kathmandu with PyEphem and
checked against the official 2082/2083 dates on this site (Ghatasthapana, Dashami, Laxmi Puja, Bhai Tika all matched).
They stay labelled 'estimated' until the government announces the 2084 holiday list. Run from repo root."""
import sys, datetime
sys.path.insert(0, 'scripts')
src = open('scripts/make_event_pages.py', encoding='utf8').read()
exec(compile(src.split('# ---------------- Bibaha Panchami')[0], 'make_event_pages_head', 'exec'))
NUM = '०१२३४५६७८९'
def ne(n): return ''.join(NUM[int(c)] for c in str(n))
D = datetime.date
MONTHS = ['Baisakh','Jestha','Ashadh','Shrawan','Bhadra','Ashoj','Kartik','Mangsir','Poush','Magh','Falgun','Chaitra']
def bsd(d):
    for m in range(12):
        for dd in range(1, bs.CANONICAL[2084][m]+1):
            if bs.bs_to_ad(2084, m+1, dd) == d: return f'{MONTHS[m]} {dd}'
    raise ValueError(d)
EST = ('This is an estimate. The date was worked out from the moon\'s position at sunrise in Kathmandu. The same method gives the official 2082 and 2083 dates on this site, '
       'but the government\'s Panchanga decides the final date and a one-day difference is possible.')
CHECK = 'Official dates are normally published late in the previous year (the 2083 holiday list was published in Falgun 2082), so check back around Falgun-Chaitra 2083 (Feb-Apr 2027).'
REL = [('/2084/calendar', 'Nepali calendar 2084'), ('/nepali-calendar-2083/dashain-2083', 'Dashain 2083 (last year)'), ('/2083/nepal-public-holidays', 'Public holidays 2083'), ('/bs-to-ad/', 'BS to AD converter')]

def table(rows):
    body = ''.join(f'<tr><td>{n}</td><td>{bsd(d)}</td><td>{d.strftime("%A, %b %-d, %Y")}</td></tr>' for n, d in rows)
    return f'<div class="tablebox"><table><thead><tr><th>Day</th><th>Nepali date (BS 2084)</th><th>English date (est.)</th></tr></thead><tbody>{body}</tbody></table></div>'

def out(slug, **kw):
    import re
    s = re.sub(re.escape(f'{BASE}/2083/{slug}') + r'(?![\w/-])', f'{BASE}/2084/{slug}', page(slug, **kw))
    s = s.replace('"name": "2083", "item": "https://converter.thenepal.io/nepali-calendar-2083/"', '"name": "2084", "item": "https://converter.thenepal.io/2084/calendar"')
    s = s.replace('https://converter.thenepal.io/nepali-calendar-2083/">2083</a>', 'https://converter.thenepal.io/2084/calendar">2084</a>')
    open(f'2084/{slug}.html', 'w', encoding='utf8').write(s)

# ---------------- Dashain
g, ph, nv, dm, kp = D(2027,9,30), D(2027,10,6), D(2027,10,9), D(2027,10,10), D(2027,10,15)
rows = [('Ghatasthapana (day 1)', g), ('Phulpati (day 7)', ph), ('Maha Navami', nv), ('Vijaya Dashami: Dashain tika', dm), ('Kojagrat Purnima', kp)]
secs = f'''  <section aria-labelledby="dates">
    <h2 id="dates">Dashain 2084 dates (estimated)</h2>
    <p>Ghatasthapana 2084 is expected on <strong>{g.strftime("%A, %B %-d, %Y")}</strong> ({bsd(g)}, 2084 BS) and Vijaya Dashami, the main tika day, on <strong>{dm.strftime("%A, %B %-d, %Y")}</strong> ({bsd(dm)}).</p>
    {table(rows)}
    <p class="note">{EST} Maha Ashtami falls on one of Oct 7 or Oct 8 because the eighth tithi covers both mornings.</p>
  </section>

  <section aria-labelledby="why">
    <h2 id="why">Why is Dashain earlier in 2084?</h2>
    <p>In 2083 Dashain ran from Oct 11 to Oct 21, 2026. In 2084 it starts about 11 days earlier, because the lunar year and the solar BS year drift apart until an extra month (Mala Maas) is added. 2083 had one; 2084 is a regular 12-month year.</p>
  </section>

  <section aria-labelledby="official">
    <h2 id="official">When will the official date be announced?</h2>
    <p>{CHECK} Until then, plan with the dates above but avoid booking non-refundable travel on a single day. For comparison, see the <a href="{BASE}/nepali-calendar-2083/dashain-2083">official Dashain 2083 dates</a>.</p>
  </section>
'''
faqs = [("When is Dashain 2084?", f"Dashain 2084 is estimated to start with Ghatasthapana on <strong>{g.strftime('%A, %B %-d, %Y')}</strong> ({bsd(g)}) and the main Vijaya Dashami tika on <strong>{dm.strftime('%A, %B %-d, %Y')}</strong> ({bsd(dm)}). The government has not published the official date yet."),
        ("When is Ghatasthapana 2084?", f"Estimated {g.strftime('%A, %B %-d, %Y')} ({bsd(g)}, 2084 BS)."),
        ("When is Vijaya Dashami (Dashain tika) 2084?", f"Estimated {dm.strftime('%A, %B %-d, %Y')} ({bsd(dm)}, 2084 BS)."),
        ("Why is Dashain 2084 earlier than 2083?", "Because 2083 had an extra lunar month (Mala Maas) and 2084 does not, Dashain moves about 11 days earlier."),
        ("How accurate is this date?", EST)]
out('dashain', title='Dashain 2084: Estimated Sep 30–Oct 10, 2027 | दशैं २०८४',
    desc=f'Dashain 2084 (estimated): Ghatasthapana {g.strftime("%b %-d, %Y")}, Vijaya Dashami tika {dm.strftime("%b %-d, %Y")}. All main days in BS and AD, why it is earlier than 2083, and when the official date comes.',
    h1='Dashain 2084: Estimated Dates', h1ne='दशैं २०८४ — घटस्थापना असोज १४ गते (अनुमानित)',
    answer=f'<strong>Dashain 2084 is estimated to start on {g.strftime("%A, %B %-d, %Y")}</strong> ({bsd(g)}), with Vijaya Dashami tika on <strong>{dm.strftime("%A, %B %-d, %Y")}</strong> ({bsd(dm)}).',
    facts=[('Ghatasthapana (est.)', g.strftime('%a, %b %-d, %Y')), ('Vijaya Dashami (est.)', dm.strftime('%a, %b %-d, %Y')), ('Status', 'Estimated, not official'), ('Last year (2083)', 'Oct 11 to 21, 2026')],
    target_iso=f'{g.isoformat()}T00:00:00+05:45', cd_label='Time until estimated Ghatasthapana 2084 (midnight, Sep 30)', cd_done='Estimated Ghatasthapana is today',
    sections=secs, faqs=faqs, related=[('/2084/tihar', 'Tihar and Bhai Tika 2084')] + REL,
    event={"@type": "WebPage", "name": "Dashain 2084 estimated dates", "url": f"{BASE}/2084/dashain"})

# ---------------- Tihar
kg, kk, lp, mh, bt = D(2027,10,27), D(2027,10,28), D(2027,10,29), D(2027,10,30), D(2027,10,31)
rows = [('Kaag Tihar (day 1)', kg), ('Kukur Tihar (day 2)', kk), ('Laxmi Puja (day 3)', lp), ('Govardhan Puja, Mha Puja, Nepal Sambat New Year (day 4)', mh), ('Bhai Tika (day 5)', bt)]
secs = f'''  <section aria-labelledby="dates">
    <h2 id="dates">Tihar 2084 dates (estimated)</h2>
    <p>Tihar 2084 is expected from <strong>{kg.strftime("%B %-d")} to {bt.strftime("%B %-d, %Y")}</strong>, with Laxmi Puja on <strong>{lp.strftime("%A, %B %-d")}</strong> and <strong>Bhai Tika on {bt.strftime("%A, %B %-d, %Y")}</strong> ({bsd(bt)}, 2084 BS).</p>
    {table(rows)}
    <p class="note">{EST} The Bhai Tika sahit (auspicious time) is announced only with the official Panchanga, so it is not given here.</p>
  </section>

  <section aria-labelledby="what">
    <h2 id="what">The five days of Tihar</h2>
    <p>Tihar honours crows (Kaag), dogs (Kukur), cows and the goddess Laxmi, then ox and Govardhan, and ends with Bhai Tika, when sisters put a seven-coloured tika on their brothers. The fourth day is also the New Year of the Newar community (Nepal Sambat) and Mha Puja.</p>
  </section>

  <section aria-labelledby="official">
    <h2 id="official">When will the official date be announced?</h2>
    <p>{CHECK} For comparison, see <a href="{BASE}/2083/tihar/">Tihar 2083</a> and <a href="{BASE}/2083/tihar/bhai-tika">Bhai Tika 2083</a>.</p>
  </section>
'''
faqs = [("When is Tihar 2084?", f"Tihar 2084 is estimated for <strong>{kg.strftime('%B %-d')} to {bt.strftime('%B %-d, %Y')}</strong>. The government has not published the official dates yet."),
        ("When is Bhai Tika 2084?", f"Bhai Tika 2084 is estimated for <strong>{bt.strftime('%A, %B %-d, %Y')}</strong> ({bsd(bt)}, 2084 BS)."),
        ("When is Laxmi Puja 2084?", f"Estimated {lp.strftime('%A, %B %-d, %Y')} ({bsd(lp)}, 2084 BS)."),
        ("Is the Bhai Tika time (sahit) known for 2084?", "No. The auspicious time is published only with the official Panchanga, which comes later."),
        ("How accurate is this date?", EST)]
out('tihar', title='Tihar & Bhai Tika 2084: Estimated Oct 27–31, 2027 | तिहार २०८४',
    desc=f'Tihar 2084 (estimated) runs {kg.strftime("%b %-d")} to {bt.strftime("%b %-d, %Y")}: Laxmi Puja {lp.strftime("%b %-d")}, Bhai Tika {bt.strftime("%b %-d")}. Nepali (BS) and English dates for all five days.',
    h1='Tihar and Bhai Tika 2084: Estimated Dates', h1ne='तिहार २०८४ — भाइटीका कार्तिक १५ गते (अनुमानित)',
    answer=f'<strong>Tihar 2084 is estimated for {kg.strftime("%B %-d")} to {bt.strftime("%B %-d, %Y")}</strong>. Laxmi Puja is expected on {lp.strftime("%A, %b %-d")} and <strong>Bhai Tika on {bt.strftime("%A, %b %-d, %Y")}</strong>.',
    facts=[('Laxmi Puja (est.)', lp.strftime('%a, %b %-d, %Y')), ('Bhai Tika (est.)', bt.strftime('%a, %b %-d, %Y')), ('Status', 'Estimated, not official'), ('Last year (2083)', 'Nov 8 to 12, 2026')],
    target_iso=f'{kg.isoformat()}T00:00:00+05:45', cd_label='Time until estimated Kaag Tihar 2084 (midnight, Oct 27)', cd_done='Estimated Kaag Tihar is today',
    sections=secs, faqs=faqs, related=[('/2084/dashain', 'Dashain 2084')] + REL,
    event={"@type": "WebPage", "name": "Tihar and Bhai Tika 2084 estimated dates", "url": f"{BASE}/2084/tihar"})
print('built')
