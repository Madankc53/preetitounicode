"""Generate festival/national-day pages for Poush 2083 to Baisakh 2084 from the gazette-based holiday list on this site.
Reuses page() from make_event_pages.py. Run from repo root: python3 scripts/make_spring_pages.py"""
import sys, datetime
sys.path.insert(0, 'scripts')
src = open('scripts/make_event_pages.py', encoding='utf8').read()
exec(compile(src.split('# ---------------- Bibaha Panchami')[0], 'make_event_pages_head', 'exec'))

NOTE_HOL = 'Check your office or school notice for the exact holiday rules.'
def ev(name, start, desc):
    return {"@type": "Event", "name": name, "startDate": start, "endDate": start,
            "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {"@type": "Place", "name": "Nepal", "address": {"@type": "PostalAddress", "addressCountry": "NP"}}, "description": desc}
REL_COMMON = [('/2083/nepal-public-holidays', 'Public holidays 2083'), ('/nepali-calendar-2083/', 'Nepali calendar 2083'), ('/bs-to-ad/', 'BS to AD converter')]
NUM = '०१२३४५६७८९'
def ne(n): return ''.join(NUM[int(c)] for c in str(n))
DOW_NE = {'Monday':'सोमबार','Tuesday':'मङ्गलबार','Wednesday':'बुधबार','Thursday':'बिहीबार','Friday':'शुक्रबार','Saturday':'शनिबार','Sunday':'आइतबार'}

def make(slug, name, ne_name, iso, bs_m_en, bs_m_ne, bs_d, about, holiday, extra_faqs, related, tithi=None, also=None, kind='Holiday', path='2083', year=2083, ev_desc=None, hol_label='Holiday status', title=None):
    d = datetime.date.fromisoformat(iso)
    full = d.strftime('%A, %B %-d, %Y'); short = d.strftime('%b %-d, %Y'); dow = d.strftime('%A')
    # the date must agree with the BS table on this site
    m_idx = ['Baisakh','Jestha','Ashadh','Shrawan','Bhadra','Ashoj','Kartik','Mangsir','Poush','Magh','Falgun','Chaitra'].index(bs_m_en)+1
    assert bs.bs_to_ad(year, m_idx, bs_d) == d, (slug, bs.bs_to_ad(year, m_idx, bs_d), d)
    ttl = f'{name} {year}: {d.strftime("%b %-d, %Y")} ({bs_m_en} {bs_d}) | {ne_name}'
    if title: ttl = title
    desc = f'{name} {year} is on {full} ({bs_m_en} {bs_d}, {year} BS). Date, meaning, how it is observed, holiday status and days left.'
    facts = [('English date', d.strftime('%a, %b %-d, %Y')), ('Nepali date', f'{bs_m_en} {bs_d}, {year} BS')]
    if tithi: facts.append(('Tithi', tithi))
    facts.append((hol_label, holiday[0]))
    secs = f'''  <section aria-labelledby="date">
    <h2 id="date">{name} {year} date</h2>
    <p><strong>Date:</strong> {full}, which is {bs_m_en} {bs_d}, {year} BS.{(" "+also) if also else ""}</p>
  </section>

  <section aria-labelledby="what">
    <h2 id="what">About {name}</h2>
{about}
  </section>

  <section aria-labelledby="holiday">
    <h2 id="holiday">Is {name} a public holiday?</h2>
    <p>{holiday[1]} {NOTE_HOL} See the <a href="https://converter.thenepal.io/2083/nepal-public-holidays">2083 holidays list</a>.</p>
  </section>
'''
    faqs = [(f'When is {name} {year}?', f'{name} {year} is on <strong>{full}</strong> ({bs_m_en} {bs_d}, {year} BS).'),
            (f'Is {name} a public holiday in Nepal?', holiday[1] + ' ' + NOTE_HOL)] + extra_faqs
    out = page(slug, title=ttl, desc=desc, h1=f'{name} {year}: Date and Meaning', h1ne=f'{ne_name} {ne(year)} — {bs_m_ne} {ne(bs_d)} गते, {DOW_NE[dow]}',
        answer=f'<strong>{name} {year} is on {full}</strong> ({bs_m_en} {bs_d}, {year} BS).',
        facts=facts, target_iso=f'{iso}T00:00:00+05:45', cd_label=f'Time left until {name} {year} begins in Nepal (midnight, {d.strftime("%b %-d")})',
        cd_done=f'{name} is today in Nepal', sections=secs, faqs=faqs, related=related + REL_COMMON,
        event=ev(f'{name} {year}', iso, ev_desc or f'{name} on {bs_m_en} {bs_d}, {year} BS.'))
    if path != '2083':
        out = out.replace(f'{BASE}/2083/{slug}', f'{BASE}/{path}/{slug}')
    import os; os.makedirs(path, exist_ok=True)
    open(f'{path}/{slug}.html', 'w', encoding='utf8').write(out)

P = lambda *t: '\n'.join(f'    <p>{x}</p>' for x in t)

make('christmas-nepal', 'Christmas', 'क्रिसमस', '2026-12-25', 'Poush', 'पौष', 10,
 P('Christmas Day is the Christian festival marking the birth of Jesus Christ. Nepal\'s Christian community, which is spread across Kathmandu and many hill and Terai districts, celebrates with church services, carols, decorated trees, shared meals and gifts.',
   'Churches in Kathmandu, Pokhara, Dharan and other towns hold special prayers on Christmas Eve and Christmas morning.'),
 ('Community holiday', 'Christmas Day (Poush 10, Dec 25, 2026) is in the 2083 holiday list as a holiday for Christian employees, not a general national holiday for everyone.'),
 [("Is Christmas a holiday for everyone in Nepal?", "No. In the 2083 holiday list it is a community holiday for Christian employees. Other offices and schools usually work as normal."),
  ("What day of the week is Christmas 2026?", "Christmas Day 2026 falls on a Friday, which is a regular working day in Nepal for most people.")],
 [('/2083/maghe-sankranti', 'Maghe Sankranti 2083 (Jan 15)'), ('/2083/tamu-lhosar', 'Tamu Lhosar 2083 (Dec 30)'), ('/nepali-calendar-2083/poush-2083', 'Poush 2083 calendar')],
 kind='Community holiday', ev_desc='Christmas Day, Poush 10, 2083 BS.', hol_label='Holiday', title='Christmas 2026 in Nepal: Dec 25 (Poush 10, 2083) | क्रिसमस')

make('prithvi-jayanti', 'Prithvi Jayanti', 'पृथ्वी जयन्ती', '2027-01-11', 'Poush', 'पौष', 27,
 P('Prithvi Jayanti marks the birth anniversary of King Prithvi Narayan Shah (1723 to 1775), who began the unification of Nepal from Gorkha. It is observed on Poush 27 every year and is also called <strong>National Unity Day (Rastriya Ekta Diwas)</strong>.',
   'Government bodies, schools and organisations hold programmes and rallies, and people pay respects to the Shah-era monuments, including in Gorkha.'),
 ('National holiday', 'Prithvi Jayanti (Poush 27, Jan 11, 2027) is a national holiday in the 2083 holiday list.'),
 [("What is Prithvi Jayanti also called?", "It is also called National Unity Day (Rastriya Ekta Diwas)."),
  ("Who was Prithvi Narayan Shah?", "He was the king of Gorkha who began the unification of Nepal in the 18th century and is regarded as the founder of modern Nepal.")],
 [('/2083/maghe-sankranti', 'Maghe Sankranti 2083 (Jan 15)'), ('/nepali-calendar-2083/poush-2083', 'Poush 2083 calendar'), ('/2083/tamu-lhosar', 'Tamu Lhosar 2083')],
 ev_desc='Birth anniversary of King Prithvi Narayan Shah; National Unity Day.')

make('shahid-diwas', "Martyrs' Day", 'शहीद दिवस', '2027-01-30', 'Magh', 'माघ', 16,
 P('Martyrs\' Day (Shahid Diwas) remembers the people who gave their lives for democracy and the nation. It is observed on Magh 16 each year, honouring the four martyrs <strong>Shukraraj Shastri, Dharma Bhakta Mathema, Gangalal Shrestha and Dashrath Chand</strong>, who were executed during the Rana period.',
   'Wreaths are laid at memorials, and official programmes are held across the country.'),
 ('National holiday', 'Martyrs\' Day (Magh 16, Jan 30, 2027) is a national holiday in the 2083 holiday list. In 2083 it falls on a Saturday, which is already a weekly holiday.'),
 [("Who are the four martyrs remembered on Shahid Diwas?", "Shukraraj Shastri, Dharma Bhakta Mathema, Gangalal Shrestha and Dashrath Chand."),
  ("Does Martyrs' Day 2083 fall on a weekend?", "Yes. In 2083 it is on a Saturday, so it falls on a day that is already a weekly holiday.")],
 [('/2083/saraswati-puja', 'Saraswati Puja 2083 (Feb 11)'), ('/nepali-calendar-2083/magh-2083', 'Magh 2083 calendar'), ('/2083/maghe-sankranti', 'Maghe Sankranti 2083')],
 ev_desc='Shahid Diwas, Magh 16, 2083 BS.')

make('sonam-lhosar', 'Sonam Lhosar', 'सोनाम ल्होसार', '2027-02-07', 'Magh', 'माघ', 24,
 P('Sonam Lhosar is the New Year of the Tamang community, celebrated in the month of Magh. Families dress in traditional clothes, share feasts, sing and dance to the damphu, and visit relatives.',
   'Large celebrations are held in Kathmandu, including around Boudhanath, and in Tamang-majority districts such as Rasuwa, Nuwakot and Sindhupalchok.'),
 ('Community holiday', 'Sonam Lhosar (Magh 24, Feb 7, 2027) is in the 2083 holiday list as a holiday for the Tamang community. In 2083 it falls on a Sunday.'),
 [("Who celebrates Sonam Lhosar?", "Sonam Lhosar is the New Year of the Tamang community."),
  ("Is Sonam Lhosar a holiday for everyone?", "It is a community holiday for the Tamang community in the 2083 list. Other offices and schools usually follow their own notice.")],
 [('/2083/tamu-lhosar', 'Tamu Lhosar 2083 (Dec 30)'), ('/2083/saraswati-puja', 'Saraswati Puja 2083 (Feb 11)'), ('/nepali-calendar-2083/magh-2083', 'Magh 2083 calendar')],
 kind='Community holiday', ev_desc='Tamang New Year, Magh 24, 2083 BS.', hol_label='Holiday')

make('prajatantra-diwas', 'Democracy Day', 'प्रजातन्त्र दिवस', '2027-02-19', 'Falgun', 'फाल्गुन', 7,
 P('National Democracy Day (Prajatantra Diwas) marks the end of the Rana regime on Falgun 7, 2007 BS (February 1951) and the start of democratic politics in Nepal.',
   'Government programmes, rallies and messages from leaders mark the day every year.'),
 ('National holiday', 'Democracy Day (Falgun 7, Feb 19, 2027) is a national holiday in the 2083 holiday list. In 2083 it falls on a Friday.'),
 [("What does Democracy Day commemorate?", "The end of the Rana regime on Falgun 7, 2007 BS (1951 AD)."),
  ("What day is Democracy Day 2083?", "Friday, February 19, 2027.")],
 [('/2083/saraswati-puja', 'Saraswati Puja 2083 (Feb 11)'), ('/2083/maha-shivaratri', 'Maha Shivaratri 2083 (Mar 6)'), ('/nepali-calendar-2083/falgun-2083', 'Falgun 2083 calendar')],
 ev_desc='Prajatantra Diwas, Falgun 7, 2083 BS.')

make('maha-shivaratri', 'Maha Shivaratri', 'महाशिवरात्रि', '2027-03-06', 'Falgun', 'फाल्गुन', 22,
 P('Maha Shivaratri, the Great Night of Shiva, is one of the biggest Hindu festivals in Nepal. Devotees fast, stay awake through the night and offer water, bel leaves and flowers to Lord Shiva.',
   '<strong>Pashupatinath Temple</strong> in Kathmandu draws very large crowds, including sadhus and pilgrims from Nepal and India. Many people light fires and gather at Shiva temples across the country.'),
 ('Festival holiday', 'Maha Shivaratri (Falgun 22, Mar 6, 2027) is in the 2083 holiday list. In 2083 it falls on a Saturday, which is already a weekly holiday.'),
 [("Where is Maha Shivaratri celebrated in Nepal?", "The main celebration is at Pashupatinath Temple in Kathmandu, with gatherings at Shiva temples across the country."),
  ("Does Maha Shivaratri 2083 fall on a weekend?", "Yes. It is on a Saturday, which is already a weekly holiday.")],
 [('/2083/holi', 'Holi 2083 (Mar 21-22)'), ('/nepali-calendar-2083/falgun-2083', 'Falgun 2083 calendar'), ('/2083/gyalpo-lhosar', 'Gyalpo Lhosar 2083 (Mar 9)')],
 tithi='Falgun Krishna Chaturdashi', also='The festival follows the lunar calendar, so the English date changes every year.', hol_label='Holiday', ev_desc='Maha Shivaratri, Falgun 22, 2083 BS.')

make('gyalpo-lhosar', 'Gyalpo Lhosar', 'ग्याल्पो ल्होसार', '2027-03-09', 'Falgun', 'फाल्गुन', 25,
 P('Gyalpo Lhosar is the New Year of the Sherpa, Tibetan and related Himalayan communities. Families clean their homes, put on traditional dress, share festive food and visit monasteries.',
   'Celebrations are especially visible in Boudhanath and Swayambhu in Kathmandu and in Solukhumbu, Humla and other Himalayan districts.'),
 ('Community holiday', 'Gyalpo Lhosar (Falgun 25, Mar 9, 2027) is in the 2083 holiday list as a community holiday for the Sherpa and Tibetan communities.'),
 [("Who celebrates Gyalpo Lhosar?", "It is the New Year of the Sherpa, Tibetan and related Himalayan communities."),
  ("Where can I see Gyalpo Lhosar celebrations?", "Boudhanath and Swayambhu in Kathmandu are popular places, along with Himalayan districts such as Solukhumbu.")],
 [('/2083/maha-shivaratri', 'Maha Shivaratri 2083 (Mar 6)'), ('/2083/holi', 'Holi 2083 (Mar 21-22)'), ('/nepali-calendar-2083/falgun-2083', 'Falgun 2083 calendar')],
 kind='Community holiday', ev_desc='Gyalpo Lhosar, Falgun 25, 2083 BS.', hol_label='Holiday')

make('holi', 'Holi', 'होली / फागु पूर्णिमा', '2027-03-21', 'Chaitra', 'चैत्र', 7,
 P('Holi (Fagu Purnima), the festival of colours, is celebrated on the full moon of Falgun. People throw coloured powder and water at each other, and the festival welcomes spring.',
   'In Kathmandu the celebrations begin about a week earlier, when a bamboo pole (<strong>chir</strong>) is raised at Basantapur Durbar Square. Nepal holds Holi on <strong>two dates</strong>: the hill and mountain districts on Chaitra 7 and the Terai districts on Chaitra 8.'),
 ('Festival holiday', 'In the 2083 holiday list Holi is on Chaitra 7 (Mar 21, 2027) for the hill and mountain districts and on Chaitra 8 (Mar 22, 2027) for the Terai districts.'),
 [("Why does Nepal celebrate Holi on two days?", "The hill and mountain districts celebrate on Chaitra 7 (Mar 21, 2027) and the Terai districts on Chaitra 8 (Mar 22, 2027), as shown in the 2083 holiday list."),
  ("What is the chir at Basantapur?", "A bamboo pole with colourful strips of cloth that is raised at Basantapur Durbar Square in Kathmandu to open the Holi festival.")],
 [('/2083/maha-shivaratri', 'Maha Shivaratri 2083 (Mar 6)'), ('/nepali-calendar-2083/chaitra-2083', 'Chaitra 2083 calendar'), ('/2084/nepali-new-year', 'Nepali New Year 2084 (Apr 14)')],
 also='This is the date for the hill and mountain districts. The Terai districts celebrate the next day, <strong>Monday, March 22, 2027 (Chaitra 8)</strong>.', hol_label='Holiday (hill)', ev_desc='Fagu Purnima / Holi, Chaitra 7, 2083 BS (hill districts); Chaitra 8 in the Terai.')

make('nepali-new-year', 'Nepali New Year', 'नयाँ वर्ष', '2027-04-14', 'Baisakh', 'वैशाख', 1,
 P('Baisakh 1 is the first day of the Bikram Sambat (BS) year and Nepal\'s national New Year. People greet each other with "Naya Barsha ko Shubhakamana", visit temples and relatives, and share special food.',
   'Public events include the <strong>Bisket Jatra</strong> in Bhaktapur, which runs through the New Year days, and programmes across Kathmandu Valley and other towns. Nepal\'s calendar year 2084 begins on this day.'),
 ('National holiday', 'Baisakh 1 is a national public holiday in Nepal. Government offices, banks and schools are closed.'),
 [("What year will it be on Baisakh 1, 2084?", "It will be the BS year 2084, which is 2027 to 2028 in the AD calendar."),
  ("How do you say Happy New Year in Nepali?", "Naya Barsha ko Shubhakamana (नयाँ वर्षको शुभकामना).")],
 [('/2084/calendar', 'Nepali calendar 2084'), ('/nepali-calendar-2084/baisakh-2084', 'Baisakh 2084 calendar'), ('/nepali-calendar-2083/chaitra-2083', 'Chaitra 2083 calendar')],
 path='2084', year=2084, ev_desc='Baisakh 1, 2084 BS, Nepali New Year.')
print('built')

# Christmas is searched by AD year
_p = '2083/christmas-nepal.html'
_s = open(_p, encoding='utf8').read().replace('<h1>Christmas 2083: Date and Meaning</h1>', '<h1>Christmas 2026 in Nepal: Date and Holiday Status</h1>')
open(_p, 'w', encoding='utf8').write(_s)
