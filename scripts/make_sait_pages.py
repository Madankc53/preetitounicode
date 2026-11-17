"""Month pages for marriage (bibaha) sait 2083: Poush (none), Magh (6), Falgun (12).
Dates are the 2083 list already published on /2083/subha-sait (NPNS panchanga). Run from repo root."""
import sys, datetime, os
sys.path.insert(0, 'scripts')
src = open('scripts/make_event_pages.py', encoding='utf8').read()
exec(compile(src.split('# ---------------- Bibaha Panchami')[0], 'make_event_pages_head', 'exec'))
NUM = '०१२३४५६७८९'
def ne(n): return ''.join(NUM[int(c)] for c in str(n))
REL = [('/2083/subha-sait', 'Shubha Sait 2083 (all dates)'), ('/2083/bibaha-panchami', 'Bibaha Panchami 2083 and Mangsir sait'), ('/2083/nepal-public-holidays', 'Public holidays 2083'), ('/bs-to-ad/', 'BS to AD converter')]
CONFIRM = 'These are auspicious calendar days. The exact time (muhurta) must be confirmed with your family astrologer from the bride and groom\'s horoscopes.'
MONTHS = {9: ('Poush', 'पौष'), 10: ('Magh', 'माघ'), 11: ('Falgun', 'फाल्गुन')}
SAIT = {10: [4, 12, 15, 19, 20, 27], 11: [3, 4, 11, 12, 15, 16, 17, 18, 20, 25, 26, 30]}
def dt(m, d): return bs.bs_to_ad(2083, m, d)

def write(slug, out):
    open(f'2083/{slug}.html', 'w', encoding='utf8').write(out)

def month_page(m):
    en, nep = MONTHS[m]; days = SAIT[m]; n = len(days)
    first = dt(m, days[0]); start = dt(m, 1); end = dt(m, bs.CANONICAL[2083][m-1])
    rows = ''.join(f'<tr><td>{en} {d}</td><td>{dt(m,d).strftime("%A")}</td><td>{dt(m,d).strftime("%b %-d, %Y")}</td></tr>' for d in days)
    plist = ', '.join(str(d) for d in days)
    wk = [d for d in days if dt(m, d).weekday() in (5, 6)]
    slug = f'{en.lower()}-bibaha-sait'
    busiest = ' It is the busiest wedding month of 2083.' if n == 12 else ''
    extra = ''
    if n == 12:
        extra = f'<p>Falgun 15, 16, 17 and 18 ({dt(m,15).strftime("%b %-d")} to {dt(m,18).strftime("%b %-d")}) are four sait days in a row, so venues and photographers are likely to book out first for those dates.</p>'
    secs = f'''  <section aria-labelledby="dates">
    <h2 id="dates">Marriage dates in {en} 2083</h2>
    <p>{en} 2083 runs from {start.strftime("%B %-d")} to {end.strftime("%B %-d, %Y")}. The 2083 marriage sait list has <strong>{n} dates in {en}</strong>: {en} {plist}.{busiest}</p>
    <div class="tablebox"><table><thead><tr><th>Nepali date</th><th>Day</th><th>English date</th></tr></thead><tbody>{rows}</tbody></table></div>
    {extra}
    <p class="note">{CONFIRM}</p>
  </section>

  <section aria-labelledby="plan">
    <h2 id="plan">Planning tips</h2>
    <ul>
      <li>{len(wk)} of the {n} dates fall on a Saturday or Sunday, when most offices are closed and guests can travel more easily.</li>
      <li>Book the hall, priest, band and caterer as early as you can; popular dates fill first.</li>
      <li>Use the <a href="{BASE}/bs-to-ad/">BS to AD converter</a> to share the English date with family abroad.</li>
    </ul>
    <p>See every ceremony date (Bibaha, Bratabandha, Pasni, Griha Pravesh) on the <a href="{BASE}/2083/subha-sait">Shubha Sait 2083 page</a>.</p>
  </section>
'''
    faqs = [(f'How many marriage dates are there in {en} 2083?', f'There are <strong>{n}</strong> marriage sait dates in {en} 2083: {en} {plist}.'),
            (f'When is the first marriage date in {en} 2083?', f'{en} {days[0]}, 2083 BS, which is {first.strftime("%A, %B %-d, %Y")}.'),
            (f'When is the last marriage date in {en} 2083?', f'{en} {days[-1]}, 2083 BS, which is {dt(m,days[-1]).strftime("%A, %B %-d, %Y")}.'),
            ('Is the time of the wedding fixed?', CONFIRM)]
    out = page(slug, title=f'{en} 2083 Marriage Dates: {n} Bibaha Sait ({first.strftime("%b %-d")} onward) | {nep} विवाह साइत',
        desc=f'{en} 2083 marriage (bibaha) sait: {n} dates, {en} {plist}. English dates, weekdays and planning tips. From the 2083 Panchanga list.',
        h1=f'{en} 2083 Marriage Dates (Bibaha Sait)', h1ne=f'{nep} {ne(2083)} विवाह साइत — {ne(n)} दिन',
        answer=f'<strong>{en} 2083 has {n} marriage sait dates:</strong> {en} {plist}. The first is {first.strftime("%A, %b %-d, %Y")}.',
        facts=[('Marriage dates', str(n)), ('First date', first.strftime('%a, %b %-d, %Y')), ('Last date', dt(m, days[-1]).strftime('%a, %b %-d, %Y')), ('Month runs', f'{start.strftime("%b %-d")} to {end.strftime("%b %-d, %Y")}')],
        target_iso=f'{first.isoformat()}T00:00:00+05:45', cd_label=f'Time left until the first {en} 2083 marriage sait ({first.strftime("%b %-d")})', cd_done='The first marriage sait of the month is today',
        sections=secs, faqs=faqs,
        related=[('/2083/falgun-bibaha-sait' if m == 10 else '/2083/magh-bibaha-sait', 'Falgun 2083 marriage dates' if m == 10 else 'Magh 2083 marriage dates'), (f'/nepali-calendar-2083/{en.lower()}-2083', f'{en} 2083 calendar')] + REL,
        event={"@type": "WebPage", "name": f"{en} 2083 marriage dates", "url": f"{BASE}/2083/{slug}"})
    write(slug, out)

def poush_page():
    last = dt(8, 26); nxt = dt(10, 4); s = dt(9, 1); e = dt(9, bs.CANONICAL[2083][8])
    secs = f'''  <section aria-labelledby="ans">
    <h2 id="ans">Why is there no marriage sait in Poush?</h2>
    <p>In Poush 2083 ({s.strftime("%B %-d")} to {e.strftime("%B %-d, %Y")}) the published marriage sait list has no dates. Poush is traditionally avoided for weddings, so families usually choose Mangsir, Magh or Falgun instead.</p>
  </section>

  <section aria-labelledby="near">
    <h2 id="near">Nearest marriage dates</h2>
    <div class="tablebox"><table><thead><tr><th></th><th>Nepali date</th><th>English date</th></tr></thead><tbody>
    <tr><td>Last before Poush</td><td>Mangsir 26, 2083</td><td>{last.strftime("%A, %b %-d, %Y")}</td></tr>
    <tr><td>First after Poush</td><td>Magh 4, 2083</td><td>{nxt.strftime("%A, %b %-d, %Y")}</td></tr></tbody></table></div>
    <p>See all <a href="{BASE}/2083/magh-bibaha-sait">6 marriage dates in Magh</a> and <a href="{BASE}/2083/falgun-bibaha-sait">12 in Falgun</a>. {CONFIRM}</p>
  </section>
'''
    faqs = [('Is there a marriage sait in Poush 2083?', f'No. The 2083 marriage sait list has no dates in Poush ({s.strftime("%b %-d")} to {e.strftime("%b %-d, %Y")}).'),
            ('When is the next marriage date after Mangsir 2083?', f'Magh 4, 2083 BS, which is {nxt.strftime("%A, %B %-d, %Y")}.'),
            ('Which months have marriage sait in 2083?', 'Baisakh, Jestha (1 date), Ashadh, Mangsir, Magh and Falgun. See the Shubha Sait 2083 page for the full list.')]
    out = page('poush-bibaha-sait', title='Poush 2083 Marriage Dates: None, Next Is Magh 4 | पौष विवाह साइत',
        desc=f'Is there a marriage sait in Poush 2083? No. The last date is Mangsir 26 ({last.strftime("%b %-d")}) and the next is Magh 4 ({nxt.strftime("%b %-d, %Y")}).',
        h1='Poush 2083 Marriage Dates (Bibaha Sait)', h1ne='पौष २०८३ विवाह साइत — कुनै साइत छैन',
        answer=f'<strong>There is no marriage sait in Poush 2083.</strong> The last date before it is Mangsir 26 ({last.strftime("%b %-d, %Y")}) and the next is Magh 4 ({nxt.strftime("%A, %b %-d, %Y")}).',
        facts=[('Marriage dates', '0'), ('Month runs', f'{s.strftime("%b %-d")} to {e.strftime("%b %-d, %Y")}'), ('Next date', f'Magh 4, {nxt.strftime("%b %-d, %Y")}')],
        target_iso=f'{nxt.isoformat()}T00:00:00+05:45', cd_label='Time left until the next marriage sait (Magh 4)', cd_done='The next marriage sait is today',
        sections=secs, faqs=faqs, related=[('/2083/magh-bibaha-sait', 'Magh 2083 marriage dates'), ('/2083/falgun-bibaha-sait', 'Falgun 2083 marriage dates'), ('/nepali-calendar-2083/poush-2083', 'Poush 2083 calendar')] + REL,
        event={"@type": "WebPage", "name": "Poush 2083 marriage dates", "url": f"{BASE}/2083/poush-bibaha-sait"})
    write('poush-bibaha-sait', out)

month_page(10); month_page(11); poush_page(); print('built')
