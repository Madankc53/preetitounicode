"""Generate winter festival pages (Dhanya Purnima/Yomari Punhi, Tamu Lhosar, Maghe Sankranti, Saraswati Puja).
Reuses page() from make_event_pages.py. Run from repo root: python3 scripts/make_winter_pages.py"""
import sys
sys.path.insert(0, 'scripts')
src = open('scripts/make_event_pages.py', encoding='utf8').read()
exec(compile(src.split('# ---------------- Bibaha Panchami')[0], 'make_event_pages_head', 'exec'))

NOTE_HOL = 'Check your office or school notice for the exact holiday rules.'
def ev(name, start, desc, place='Nepal'):
    return {"@type": "Event", "name": name, "startDate": start, "endDate": start,
            "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {"@type": "Place", "name": place, "address": {"@type": "PostalAddress", "addressCountry": "NP"}}, "description": desc}
REL_COMMON = [('/2083/nepal-public-holidays', 'Public holidays 2083'), ('/nepali-calendar-2083/', 'Nepali calendar 2083'), ('/bs-to-ad/', 'BS to AD converter')]

def build(slug, **kw):
    out = page(slug, **kw)
    open(f'2083/{slug}.html', 'w', encoding='utf8').write(out)

# ---- Dhanya Purnima / Yomari Punhi
build('yomari-punhi',
 title='Yomari Punhi / Dhanya Purnima 2083: Thu, Dec 24, 2026 (Poush 9) | योमरी पुन्ही',
 desc='Yomari Punhi and Dhanya Purnima 2083 fall on Thursday, December 24, 2026 (Poush 9, 2083 BS). Date, what it is, the yomari recipe basics, and days left.',
 h1='Yomari Punhi 2083: Date and Meaning', h1ne='योमरी पुन्ही / धान्य पूर्णिमा २०८३ — पुस ९ गते, बिहीबार',
 answer='<strong>Yomari Punhi and Dhanya Purnima 2083 fall on Thursday, December 24, 2026</strong> (Poush 9, 2083 BS), on the full moon.',
 facts=[('English date', 'Thu, Dec 24, 2026'), ('Nepali date', 'Poush 9, 2083 BS'), ('Tithi', 'Purnima (full moon)'), ('Celebrated by', 'Newar community, nationwide harvest tradition')],
 target_iso='2026-12-24T00:00:00+05:45', cd_label='Time left until Yomari Punhi / Dhanya Purnima 2083 begins in Nepal (midnight, Dec 24)', cd_done='Yomari Punhi is today in Nepal',
 sections='''  <section aria-labelledby="date">
    <h2 id="date">Yomari Punhi 2083 date</h2>
    <p><strong>Date:</strong> Thursday, December 24, 2026, which is Poush 9, 2083 BS. It falls on the full moon (Purnima) after the rice harvest. The 2083 holiday list names this day as Dhanya Purnima, and the Newar community celebrates the same full moon as Yomari Punhi.</p>
  </section>

  <section aria-labelledby="what">
    <h2 id="what">What is Yomari Punhi?</h2>
    <p>Yomari Punhi is a Newar harvest festival. Families make <strong>yomari</strong>, a steamed dumpling of rice-flour dough shaped like a fig, filled with <em>chaku</em> (hardened molasses) and sesame, or sometimes khuwa. The name comes from Newar words meaning "tasty bread" and "full moon". Yomari is offered to the gods first, then shared with relatives and neighbours. The festival is especially lively in Kathmandu, Lalitpur, Bhaktapur and Panauti.</p>
    <p>Dhanya Purnima, "grain full moon", is the wider Hindu harvest full moon, when families give thanks for the new rice.</p>
  </section>

  <section aria-labelledby="holiday">
    <h2 id="holiday">Is it a public holiday?</h2>
    <p>Dhanya Purnima, Poush 9 (Dec 24, 2026), is in the 2083 holiday list. The next day, Christmas, is Poush 10 (Friday, Dec 25). ''' + NOTE_HOL + ''' See the <a href="https://converter.thenepal.io/2083/nepal-public-holidays">2083 holidays list</a>.</p>
  </section>
''',
 faqs=[("When is Yomari Punhi 2083?", "Yomari Punhi and Dhanya Purnima 2083 are on <strong>Thursday, December 24, 2026</strong> (Poush 9, 2083 BS)."),
       ("What is yomari made of?", "Yomari is a steamed dumpling of rice-flour dough filled with chaku (hardened molasses) and sesame seeds, or with khuwa."),
       ("Who celebrates Yomari Punhi?", "It is a Newar festival, celebrated mainly in the Kathmandu Valley, including Kathmandu, Lalitpur, Bhaktapur and Panauti."),
       ("Is Dhanya Purnima a public holiday in Nepal?", "Dhanya Purnima on Poush 9 (Dec 24, 2026) is in the 2083 holiday list. Check your office or school notice."),
       ("What is the difference between Yomari Punhi and Dhanya Purnima?", "Both are on the same harvest full moon. Yomari Punhi is the Newar festival of eating yomari; Dhanya Purnima is the wider Hindu harvest full moon.")],
 related=[('/2083/bibaha-panchami', 'Bibaha Panchami 2083 (Dec 14)'), ('/2083/tamu-lhosar', 'Tamu Lhosar 2083 (Dec 30)'), ('/nepali-calendar-2083/poush-2083', 'Poush 2083 calendar')] + REL_COMMON,
 event=ev('Yomari Punhi / Dhanya Purnima 2083', '2026-12-24', 'Newar harvest festival and Dhanya Purnima on Poush 9, 2083 BS.', 'Kathmandu Valley, Nepal'))

# ---- Tamu Lhosar
build('tamu-lhosar',
 title='Tamu Lhosar 2083: Wed, Dec 30, 2026 (Poush 15) — Gurung New Year | तमु ल्होसार',
 desc='Tamu Lhosar 2083, the Gurung New Year, is on Wednesday, December 30, 2026 (Poush 15, 2083 BS). Date, meaning, and days left. Sonam Lhosar follows on Magh 24.',
 h1='Tamu Lhosar 2083: Date and Meaning', h1ne='तमु ल्होसार २०८३ — पुस १५ गते, बुधबार',
 answer='<strong>Tamu Lhosar 2083 is on Wednesday, December 30, 2026</strong> (Poush 15, 2083 BS). It is the Gurung (Tamu) New Year.',
 facts=[('English date', 'Wed, Dec 30, 2026'), ('Nepali date', 'Poush 15, 2083 BS'), ('Celebrated by', 'Gurung (Tamu) community'), ('Next Lhosar', 'Sonam Lhosar, Magh 24')],
 target_iso='2026-12-30T00:00:00+05:45', cd_label='Time left until Tamu Lhosar 2083 begins in Nepal (midnight, Dec 30)', cd_done='Tamu Lhosar is today in Nepal',
 sections='''  <section aria-labelledby="date">
    <h2 id="date">Tamu Lhosar 2083 date</h2>
    <p><strong>Date:</strong> Wednesday, December 30, 2026, which is Poush 15, 2083 BS. Tamu Lhosar is observed on Poush 15 every year, so it falls on December 30 or 29 in most years.</p>
  </section>

  <section aria-labelledby="what">
    <h2 id="what">What is Tamu Lhosar?</h2>
    <p>Tamu Lhosar is the New Year of the Gurung community, who call themselves Tamu. "Lho" means year and "sar" means new. People wear traditional dress, hold cultural programmes with music and dance, and gather with family. Celebrations are largest in Pokhara and Kaski, Lamjung, Gorkha, Tanahun, Syangja and Kathmandu, where Gurung communities live.</p>
    <p>Nepal has three main Lhosar festivals: Tamu Lhosar (Gurung, Poush 15), Sonam Lhosar (Tamang and Sherpa communities, Magh 24 in 2083, Sunday Feb 7, 2027) and Gyalpo Lhosar (Falgun).</p>
  </section>

  <section aria-labelledby="holiday">
    <h2 id="holiday">Is Tamu Lhosar a public holiday?</h2>
    <p>Yes, Tamu Lhosar on Poush 15 (Dec 30, 2026) is in the 2083 holiday list. ''' + NOTE_HOL + ''' See the <a href="https://converter.thenepal.io/2083/nepal-public-holidays">2083 holidays list</a>.</p>
  </section>
''',
 faqs=[("When is Tamu Lhosar 2083?", "Tamu Lhosar 2083 is on <strong>Wednesday, December 30, 2026</strong> (Poush 15, 2083 BS)."),
       ("Who celebrates Tamu Lhosar?", "The Gurung (Tamu) community celebrates it as their New Year, with traditional dress, music and dance."),
       ("Is Tamu Lhosar a public holiday in Nepal?", "Tamu Lhosar on Poush 15 (Dec 30, 2026) is in the 2083 holiday list. Check your office or school notice."),
       ("When is Sonam Lhosar 2083?", "Sonam Lhosar 2083 is on Magh 24, which is Sunday, February 7, 2027."),
       ("What does Lhosar mean?", "\"Lho\" means year and \"sar\" means new, so Lhosar means New Year.")],
 related=[('/2083/yomari-punhi', 'Yomari Punhi 2083 (Dec 24)'), ('/2083/maghe-sankranti', 'Maghe Sankranti 2083 (Jan 15)'), ('/nepali-calendar-2083/poush-2083', 'Poush 2083 calendar')] + REL_COMMON,
 event=ev('Tamu Lhosar 2083', '2026-12-30', 'Gurung (Tamu) New Year on Poush 15, 2083 BS.'))

# ---- Maghe Sankranti
build('maghe-sankranti',
 title='Maghe Sankranti 2083: Fri, Jan 15, 2027 (Magh 1) — Date, Food, Meaning | माघे सङ्क्रान्ति',
 desc='Maghe Sankranti 2083 is on Friday, January 15, 2027 (Magh 1, 2083 BS). Date, traditional foods, river bathing, Tharu Maghi, and days left.',
 h1='Maghe Sankranti 2083: Date, Food and Meaning', h1ne='माघे सङ्क्रान्ति २०८३ — माघ १ गते, शुक्रबार',
 answer='<strong>Maghe Sankranti 2083 is on Friday, January 15, 2027</strong> (Magh 1, 2083 BS), the first day of the month of Magh.',
 facts=[('English date', 'Fri, Jan 15, 2027'), ('Nepali date', 'Magh 1, 2083 BS'), ('Also called', 'Maghi, Makar Sankranti'), ('Foods', 'Til laddu, ghee, chaku, yam')],
 target_iso='2027-01-15T00:00:00+05:45', cd_label='Time left until Maghe Sankranti 2083 begins in Nepal (midnight, Jan 15)', cd_done='Maghe Sankranti is today in Nepal',
 sections='''  <section aria-labelledby="date">
    <h2 id="date">Maghe Sankranti 2083 date</h2>
    <p><strong>Date:</strong> Friday, January 15, 2027, which is Magh 1, 2083 BS. Maghe Sankranti always falls on the first day of Magh, when the sun enters Capricorn (Makar), so the English date is usually January 14 or 15.</p>
  </section>

  <section aria-labelledby="what">
    <h2 id="what">What is Maghe Sankranti?</h2>
    <p>Maghe Sankranti (also Makar Sankranti) marks the end of the cold month of Poush and the start of longer, warmer days. People bathe at rivers and holy confluences, such as Devghat, Triveni and Sankhu, and visit temples. The festival food includes <strong>ghee, chaku (molasses), til laddu (sesame sweets), yam (tarul), sweet potato and spinach</strong>. Elders give blessings and families share a meal together.</p>
    <p>For the Tharu community it is Maghi, their New Year, with dance and community feasts, especially in the Terai. The Magar community also celebrates it as a major festival.</p>
  </section>

  <section aria-labelledby="holiday">
    <h2 id="holiday">Is Maghe Sankranti a public holiday?</h2>
    <p>Yes, Magh 1 (Jan 15, 2027) is in the 2083 holiday list. ''' + NOTE_HOL + ''' See the <a href="https://converter.thenepal.io/2083/nepal-public-holidays">2083 holidays list</a>.</p>
  </section>
''',
 faqs=[("When is Maghe Sankranti 2083?", "Maghe Sankranti 2083 is on <strong>Friday, January 15, 2027</strong> (Magh 1, 2083 BS)."),
       ("What do people eat on Maghe Sankranti?", "Ghee, chaku (molasses), til laddu (sesame sweets), yam (tarul), sweet potato and spinach are the traditional foods."),
       ("Is Maghe Sankranti a public holiday in Nepal?", "Yes. Magh 1 (Jan 15, 2027) is in the 2083 holiday list. Check your office or school notice."),
       ("Why is Maghe Sankranti celebrated?", "It marks the start of the month of Magh and the sun's move into Capricorn, after the coldest days of Poush."),
       ("What is Maghi?", "Maghi is the Tharu New Year, celebrated on the same day with dance and a community feast.")],
 related=[('/2083/tamu-lhosar', 'Tamu Lhosar 2083 (Dec 30)'), ('/2083/saraswati-puja', 'Saraswati Puja 2083 (Feb 11)'), ('/nepali-calendar-2083/magh-2083', 'Magh 2083 calendar')] + REL_COMMON,
 event=ev('Maghe Sankranti 2083', '2027-01-15', 'First day of Magh 2083 BS; Maghi (Tharu New Year).'))

# ---- Saraswati Puja
build('saraswati-puja',
 title='Saraswati Puja 2083: Thu, Feb 11, 2027 (Magh 28) — Shree Panchami | सरस्वती पूजा',
 desc='Saraswati Puja (Shree Panchami, Basanta Panchami) 2083 is on Thursday, February 11, 2027 (Magh 28, 2083 BS). Date, how schools celebrate, holiday status, days left.',
 h1='Saraswati Puja 2083: Date and Meaning', h1ne='सरस्वती पूजा / श्रीपञ्चमी २०८३ — माघ २८ गते, बिहीबार',
 answer='<strong>Saraswati Puja 2083 is on Thursday, February 11, 2027</strong> (Magh 28, 2083 BS), on Magh Shukla Panchami.',
 facts=[('English date', 'Thu, Feb 11, 2027'), ('Nepali date', 'Magh 28, 2083 BS'), ('Tithi', 'Magh Shukla Panchami'), ('Holiday', 'Educational institutions')],
 target_iso='2027-02-11T00:00:00+05:45', cd_label='Time left until Saraswati Puja 2083 begins in Nepal (midnight, Feb 11)', cd_done='Saraswati Puja is today in Nepal',
 sections='''  <section aria-labelledby="date">
    <h2 id="date">Saraswati Puja 2083 date</h2>
    <p><strong>Date:</strong> Thursday, February 11, 2027, which is Magh 28, 2083 BS. It is observed on Magh Shukla Panchami, the fifth day of the bright lunar fortnight. The festival is also called Shree Panchami and Basanta Panchami, and it marks the start of spring.</p>
  </section>

  <section aria-labelledby="what">
    <h2 id="what">What happens on Saraswati Puja?</h2>
    <p>Saraswati is the goddess of knowledge, music and learning. Schools, colleges and families set up her image, and students place books, pens and instruments in front of her for blessing. Many children are introduced to writing on this day (their first letters). People wear yellow, and the day is considered auspicious for starting studies.</p>
  </section>

  <section aria-labelledby="holiday">
    <h2 id="holiday">Is Saraswati Puja a holiday?</h2>
    <p>Saraswati Puja on Magh 28 (Feb 11, 2027) is in the 2083 holiday list as a holiday for educational institutions. ''' + NOTE_HOL + ''' See the <a href="https://converter.thenepal.io/2083/nepal-public-holidays">2083 holidays list</a>.</p>
  </section>
''',
 faqs=[("When is Saraswati Puja 2083?", "Saraswati Puja 2083 is on <strong>Thursday, February 11, 2027</strong> (Magh 28, 2083 BS)."),
       ("Is Saraswati Puja the same as Shree Panchami?", "Yes. Saraswati Puja, Shree Panchami and Basanta Panchami are names for the same day, Magh Shukla Panchami."),
       ("Is Saraswati Puja a public holiday in Nepal?", "It is in the 2083 holiday list as a holiday for educational institutions. Check your office or school notice."),
       ("What do students do on Saraswati Puja?", "Students place books, pens and instruments before Saraswati for blessing, and young children are often introduced to their first letters."),
       ("What colour is worn on Saraswati Puja?", "Yellow is the traditional colour, linked to spring.")],
 related=[('/2083/maghe-sankranti', 'Maghe Sankranti 2083 (Jan 15)'), ('/nepali-calendar-2083/magh-2083', 'Magh 2083 calendar'), ('/2083/subha-sait', 'Shubha Sait 2083')] + REL_COMMON,
 event=ev('Saraswati Puja 2083', '2027-02-11', 'Saraswati Puja / Shree Panchami on Magh 28, 2083 BS.'))
print('built')
