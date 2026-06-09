import os

BASE = "https://converter.thenepal.io/nepali-calendar-2083"
OUT  = "/mnt/user-data/outputs/month-pages"
os.makedirs(OUT, exist_ok=True)

# ── Month master data ──────────────────────────────────────────────────────
MONTHS = [
  dict(
    id="baisakh", num=1, ne="वैशाख", en="Baisakh", days=31,
    startDOW=2,  # Tuesday=2
    adStart="April 14, 2026", adEnd="May 14, 2026",
    adStartISO="2026-04-14", adEndISO="2026-05-14",
    adStartObj=(2026,3,14),
    slug="baisakh-2083",
    prev=None, next_="jestha",
    keywords="baisakh 2083, baisakh 2083 calendar, vaisakh 2083, baisakh patro 2083, baisakh 2083 holidays, nepali new year 2083 date, baisakh 2083 tithi",
    desc="Baisakh 2083 BS calendar with all dates, tithi, holidays and AD dates. Baisakh 1, 2083 = April 14, 2026 (Nepali New Year). 31 days.",
    intro_en="""Baisakh 2083 BS is the <strong>first month of the Nepali year 2083</strong>. It runs from <strong>April 14, 2026 to May 14, 2026 AD</strong> and has <strong>31 days</strong>. 
Baisakh 1 is Nepal's national New Year — a public holiday when the country celebrates with processions, music and family gatherings. 
This month contains the best auspicious marriage (Shubha Sait) windows of 2083 BS: <strong>Baisakh 7–8 (Apr 20–21)</strong> and <strong>Baisakh 22–25 (May 5–8)</strong>. 
Baisakh also marks the start of Nepal's summer planting season. Banks, government offices, and schools are closed on Baisakh 1 and every Saturday.""",
    intro_ne="वैशाख २०८३ नेपाली नयाँ वर्षको पहिलो महिना हो। यसमा ३१ दिन छन् र <strong>अप्रिल १४, २०२६</strong> देखि <strong>मे १४, २०२६</strong> सम्म पर्दछ। वैशाख १ मा नयाँ वर्षको राष्ट्रिय बिदा हुन्छ। यस महिनामा विवाह र ब्रतबन्धका उत्तम शुभ साइतहरू पर्दछन्।",
    holidays={
      1: dict(label="नयाँ वर्ष — Nepali New Year", type="hol", adDate="Apr 14, 2026", dayEn="Tuesday",
              desc="Nepal's national New Year day. Grand celebrations across the country. All government offices, banks, and schools are closed.",
              tithi="प्रतिपदा"),
    },
    aus=[
      dict(type="विवाह (Marriage)", ne="वैशाख ७–८", ad="Apr 20–21, 2026"),
      dict(type="विवाह (Marriage)", ne="वैशाख २२–२५", ad="May 5–8, 2026"),
      dict(type="ब्रतबन्ध (Bratabandha)", ne="वैशाख ४, ९, १८", ad="Apr 17, 22, May 1"),
    ],
    faqs=[
      dict(q="When is Baisakh 1, 2083? Nepali New Year 2083 date?",
           a="Baisakh 1, 2083 BS falls on Tuesday, April 14, 2026. This is the Nepali New Year day — a national public holiday in Nepal."),
      dict(q="How many days in Baisakh 2083?",
           a="Baisakh 2083 has 31 days, from April 14, 2026 to May 14, 2026 AD."),
      dict(q="What are the auspicious marriage dates in Baisakh 2083?",
           a="Auspicious marriage dates (Shubha Sait) in Baisakh 2083: Baisakh 7–8 (Apr 20–21, 2026) and Baisakh 22–25 (May 5–8, 2026). Bratabandha dates: Baisakh 4, 9, 18."),
      dict(q="Is Baisakh 1 a public holiday in Nepal?",
           a="Yes. Baisakh 1 (Nepali New Year) is a national public holiday in Nepal. All government offices, banks, and schools are closed."),
    ],
    events=[
      dict(name="Nepali New Year 2083", date="2026-04-14", desc="Baisakh 1, 2083 — Nepal national holiday."),
    ],
    note=None,
  ),
  dict(
    id="jestha", num=2, ne="जेठ", en="Jestha", days=32,
    startDOW=5,  # Friday
    adStart="May 15, 2026", adEnd="June 15, 2026",
    adStartISO="2026-05-15", adEndISO="2026-06-15",
    adStartObj=(2026,4,15),
    slug="jestha-2083",
    prev="baisakh", next_="ashadh",
    keywords="jestha 2083, jestha 2083 calendar, jeth 2083, jestha 2083 holidays, republic day 2083, ganatantra diwas 2083, mala maas 2083, jestha patro 2083",
    desc="Jestha 2083 BS calendar — 32 days, May 15 to June 15, 2026. Republic Day on Jestha 15. Mala Maas begins Jestha 3. Holidays, tithi and AD dates.",
    intro_en="""Jestha 2083 BS is the <strong>second month</strong> of the Nepali year, running from <strong>May 15 to June 15, 2026</strong> and has <strong>32 days</strong>. 
Two major events mark this month. First, <strong>Republic Day (Ganatantra Diwas)</strong> falls on <strong>Jestha 15 (May 29, 2026)</strong> — a national public holiday commemorating Nepal becoming a republic in 2008. 
Second and critically, the rare <strong>Mala Maas (Adhik Maas)</strong> begins on <strong>Jestha 3 (May 17, 2026)</strong> and runs until Ashadh 1 (June 15, 2026). 
During Mala Maas, <strong>no auspicious marriage or Bratabandha dates</strong> are observed. This intercalary month is why Dashain and Tihar fall so much later in 2083 compared to previous years.""",
    intro_ne="जेठ २०८३ नेपाली वर्षको दोस्रो महिना हो। यसमा ३२ दिन छन् र <strong>मे १५, २०२६</strong> देखि <strong>जुन १५, २०२६</strong> सम्म पर्दछ। <strong>जेठ १५ मा गणतन्त्र दिवस</strong> (सार्वजनिक बिदा) र <strong>जेठ ३ देखि अधिक मास</strong> सुरु हुन्छ।",
    holidays={
      15: dict(label="गणतन्त्र दिवस — Republic Day", type="hol", adDate="May 29, 2026", dayEn="Friday",
               desc="Nepal Republic Day (Ganatantra Diwas). Celebrated every Jestha 15. National public holiday — offices, banks, schools closed.",
               tithi="पञ्चदशी"),
      3:  dict(label="Mala Maas Begins 🌙", type="mala", adDate="May 17, 2026", dayEn="Sunday",
               desc="Adhik Maas (intercalary month) starts today. Runs until Ashadh 1 (Jun 15, 2026). No auspicious dates during this period.",
               tithi="तृतीया"),
    },
    aus=[
      dict(type="विवाह (Marriage)", ne="जेठ १–२", ad="May 15–16, 2026"),
      dict(type="⚠ No Sait — Mala Maas", ne="जेठ ३ – आषाढ १", ad="May 17 – Jun 15 (No auspicious dates)"),
    ],
    faqs=[
      dict(q="Republic Day 2083 date — When is Ganatantra Diwas 2083?",
           a="Republic Day (Ganatantra Diwas) 2083 falls on Friday, May 29, 2026 (Jestha 15, 2083 BS). It is a national public holiday in Nepal."),
      dict(q="When does Mala Maas start in 2083?",
           a="Mala Maas (Adhik Maas) starts on Jestha 3, 2083 BS — Sunday, May 17, 2026 — and ends on Ashadh 1, 2083 (June 15, 2026)."),
      dict(q="How many days in Jestha 2083?",
           a="Jestha 2083 has 32 days, from May 15, 2026 to June 15, 2026 AD."),
      dict(q="Are there auspicious dates in Jestha 2083?",
           a="Only Jestha 1–2 (May 15–16, 2026) are auspicious. From Jestha 3 (May 17) onward, Mala Maas begins and no auspicious dates are observed until Ashadh 1."),
    ],
    events=[
      dict(name="Republic Day 2083 — Ganatantra Diwas", date="2026-05-29", desc="Jestha 15, 2083 — National public holiday."),
    ],
    note="🌙 Mala Maas begins this month on Jestha 3 (May 17, 2026).",
  ),
  dict(
    id="ashadh", num=3, ne="आषाढ", en="Ashadh", days=32,
    startDOW=2,  # Tuesday
    adStart="June 16, 2026", adEnd="July 17, 2026",
    adStartISO="2026-06-16", adEndISO="2026-07-17",
    adStartObj=(2026,5,16),
    slug="ashadh-2083",
    prev="jestha", next_="shrawan",
    keywords="ashadh 2083, ashadh 2083 calendar, asar 2083, ashadh patro 2083, ashadh 2083 tithi, ashadh 2083 after mala maas",
    desc="Ashadh 2083 BS calendar — 32 days, June 16 to July 17, 2026. First month after Mala Maas. All dates, tithi, and AD dates.",
    intro_en="""Ashadh 2083 BS is the <strong>third month</strong> of the Nepali year, running from <strong>June 16 to July 17, 2026</strong> with <strong>32 days</strong>. 
This is the <strong>first regular month after Mala Maas ends</strong> on Ashadh 1 (June 15, 2026). All AD dates in this month and beyond are shifted approximately 30 days later than in a normal year — a direct result of the intercalary month. 
Ashadh is Nepal's <strong>monsoon month</strong>. Heavy rainfall begins across the country. Farmers begin paddy planting (Asar 15 / Ropain Diwas). 
Auspicious dates resume this month — verify the exact Shubha Sait windows with the official NPNS Panchanga.""",
    intro_ne="आषाढ २०८३ नेपाली वर्षको तेस्रो महिना हो। यसमा ३२ दिन छन् र <strong>जुन १६, २०२६</strong> देखि <strong>जुलाई १७, २०२६</strong> सम्म पर्दछ। <strong>अधिक मास आषाढ १ मा समाप्त</strong> हुन्छ र नियमित शुभ साइतहरू फेरि सुरु हुन्छन्। मनसुनको वर्षा सुरु हुने यो महिनामा रोपाइँ महोत्सव मनाइन्छ।",
    holidays={},
    aus=[
      dict(type="Sait Resumes — verify NPNS", ne="आषाढ (Panchanga confirm)", ad="Jun 16+ · Check official calendar"),
    ],
    faqs=[
      dict(q="When does Mala Maas end in 2083?",
           a="Mala Maas ends on Ashadh 1, 2083 BS — June 15, 2026. Regular months and auspicious dates resume from Ashadh onwards."),
      dict(q="How many days in Ashadh 2083?",
           a="Ashadh 2083 has 32 days, from June 16, 2026 to July 17, 2026 AD."),
      dict(q="What is Asar 15 (Ropain Diwas) in 2083?",
           a="Asar 15 (Ashadh 15, 2083) falls on June 30, 2026. It is celebrated as Ropain Diwas — national paddy planting day — with farmers planting rice seedlings in flooded fields."),
      dict(q="Why are Ashadh 2083 AD dates later than normal?",
           a="Because of the Mala Maas intercalary month in Jestha/Ashadh 2083 BS, all AD dates from Ashadh onward are approximately 30 days later than in a normal Nepali year."),
    ],
    events=[],
    note="✅ Mala Maas ends — Ashadh 1 (Jun 15, 2026). Regular calendar resumes.",
  ),
  dict(
    id="shrawan", num=4, ne="श्रावण", en="Shrawan", days=31,
    startDOW=6,  # Saturday
    adStart="July 18, 2026", adEnd="August 17, 2026",
    adStartISO="2026-07-18", adEndISO="2026-08-17",
    adStartObj=(2026,6,18),
    slug="shrawan-2083",
    prev="ashadh", next_="bhadra",
    keywords="shrawan 2083, shrawan 2083 calendar, sawan 2083, shrawan patro 2083, shrawan 2083 holidays, shrawan 2083 tithi, shrawan sombar vrat 2083",
    desc="Shrawan 2083 BS calendar — 31 days, July 18 to August 17, 2026. Shrawan Sombar Vrat, Nag Panchami, Janai Purnima dates. Tithi and AD dates.",
    intro_en="""Shrawan 2083 BS is the <strong>fourth month</strong> of the Nepali year, running from <strong>July 18 to August 17, 2026</strong> with <strong>31 days</strong>. 
Shrawan is <strong>Nepal's most sacred month for Lord Shiva devotees</strong>. Every Monday (Sombar) in Shrawan is celebrated as a special fast day — <strong>Shrawan Sombar Vrat</strong>. Pashupatinath Temple and Shiva temples nationwide see massive crowds. 
Key events: <strong>Nag Panchami</strong> (serpent worship), <strong>Janai Purnima</strong> (sacred thread changing day and Raksha Bandhan), and <strong>Ghanta Karna</strong> (demon effigy burning).
Shrawan 1 (July 18) falls on a <strong>Saturday — Nepal's weekly holiday</strong>.""",
    intro_ne="श्रावण २०८३ नेपाली वर्षको चौथो महिना हो। यसमा ३१ दिन छन् र <strong>जुलाई १८, २०२६</strong> देखि <strong>अगस्त १७, २०२६</strong> सम्म पर्दछ। श्रावण महिनामा शिव भक्तहरू हरेक सोमबार व्रत बस्छन्। नाग पञ्चमी र जनै पूर्णिमा यस महिनामा पर्दछन्।",
    holidays={},
    aus=[
      dict(type="Sombar Vrat Mondays", ne="श्रावण सोमबार", ad="Jul 20, 27, Aug 3, 10, 17"),
    ],
    faqs=[
      dict(q="How many days in Shrawan 2083?",
           a="Shrawan 2083 has 31 days, from July 18, 2026 to August 17, 2026 AD."),
      dict(q="When is Nag Panchami 2083?",
           a="Nag Panchami 2083 falls in Shrawan 2083 BS. The exact date should be verified with the official NPNS Panchanga as it depends on Tithi calculation."),
      dict(q="When is Janai Purnima 2083?",
           a="Janai Purnima (Raksha Bandhan) 2083 falls on the Purnima (full moon) of Shrawan 2083. Verify the exact date with official Panchanga sources."),
      dict(q="What is Shrawan Sombar Vrat?",
           a="Shrawan Sombar Vrat is a sacred Monday fast observed throughout the Shrawan month. Shiva devotees fast and visit Pashupatinath and other Shiva temples. It is one of Nepal's most widely observed religious traditions."),
    ],
    events=[],
    note=None,
  ),
  dict(
    id="bhadra", num=5, ne="भाद्र", en="Bhadra", days=31,
    startDOW=2,  # Tuesday
    adStart="August 18, 2026", adEnd="September 17, 2026",
    adStartISO="2026-08-18", adEndISO="2026-09-17",
    adStartObj=(2026,7,18),
    slug="bhadra-2083",
    prev="shrawan", next_="ashoj",
    keywords="bhadra 2083, bhadra 2083 calendar, bhadau 2083, teej 2083 date, haritalika teej 2083, bhadra patro 2083, bhadra 2083 holidays",
    desc="Bhadra 2083 BS calendar — 31 days, August 18 to September 17, 2026. Haritalika Teej (women's holiday), Indra Jatra, Ganesh Chaturthi dates, tithi and AD dates.",
    intro_en="""Bhadra 2083 BS is the <strong>fifth month</strong>, running from <strong>August 18 to September 17, 2026</strong> with <strong>31 days</strong>. 
The most prominent event is <strong>Haritalika Teej</strong> — a major festival for women where they fast for the long life of their husbands or to pray for a good husband. Teej is a <strong>public holiday specifically for women</strong> in Nepal. 
Also in Bhadra: <strong>Ganesh Chaturthi</strong> (worship of Lord Ganesh), <strong>Indra Jatra</strong> preparations in Kathmandu Valley, and <strong>Rishi Panchami</strong>.
Bhadra is also the tail end of the monsoon season, with heavy rainfall still common across Nepal.""",
    intro_ne="भाद्र २०८३ नेपाली वर्षको पाँचौं महिना हो। यसमा ३१ दिन छन् र <strong>अगस्त १८, २०२६</strong> देखि <strong>सेप्टेम्बर १७, २०२६</strong> सम्म पर्दछ। यस महिनामा <strong>हरितालिका तीज</strong> (महिलाहरूको सार्वजनिक बिदा) र गणेश चतुर्थी पर्दछन्।",
    holidays={},
    aus=[],
    faqs=[
      dict(q="Teej 2083 date — When is Haritalika Teej 2083?",
           a="Haritalika Teej 2083 falls in Bhadra 2083 BS (~September 2026). The exact date depends on Tritiya Tithi of Bhadra Shukla Paksha. Verify with the official NPNS Panchanga."),
      dict(q="Is Teej a public holiday in Nepal?",
           a="Yes. Haritalika Teej is a public holiday specifically for women in Nepal. Male government employees still work on this day."),
      dict(q="How many days in Bhadra 2083?",
           a="Bhadra 2083 has 31 days, from August 18, 2026 to September 17, 2026 AD."),
      dict(q="When is Indra Jatra 2083?",
           a="Indra Jatra 2083 is observed in Bhadra/Ashoj 2083 BS in Kathmandu Valley. The festival celebrates Indra (god of rain) and features the Kumari chariot procession. Verify the exact date with NPNS."),
    ],
    events=[],
    note=None,
  ),
  dict(
    id="ashoj", num=6, ne="असोज", en="Ashoj", days=30,
    startDOW=5,  # Friday
    adStart="September 18, 2026", adEnd="October 17, 2026",
    adStartISO="2026-09-18", adEndISO="2026-10-17",
    adStartObj=(2026,8,18),
    slug="ashoj-2083",
    prev="bhadra", next_="kartik",
    keywords="ashoj 2083, ashoj 2083 calendar, asoj 2083, dashain 2083 date, ghatasthapana 2083, constitution day 2083, sambidhan diwas 2083, ashoj patro 2083 holidays",
    desc="Ashoj 2083 BS calendar — 30 days, Sep 18 to Oct 17, 2026. Constitution Day (Ashoj 3), Dashain Ghatasthapana (Ashoj 25 = Oct 11). Full holidays, tithi, AD dates.",
    intro_en="""Ashoj 2083 BS is the <strong>sixth month</strong>, running from <strong>September 18 to October 17, 2026</strong> with <strong>30 days</strong>. 
This is one of the most eventful months of 2083 BS. <strong>Constitution Day (Sambidhan Diwas)</strong> falls on <strong>Ashoj 3 (September 19, 2026 — Saturday)</strong>, a national holiday that also falls on Nepal's weekly day off. 
The biggest event: <strong>Dashain Ghatasthapana</strong> — the start of Nepal's greatest festival — falls on <strong>Ashoj 25 (October 11, 2026)</strong>. Due to Mala Maas, Dashain begins much later than in previous years. 
A sacred Kalash is established and Jamara (barley seedlings) are planted on Ghatasthapana day.""",
    intro_ne="असोज २०८३ नेपाली वर्षको छैटौं महिना हो। यसमा ३० दिन छन् र <strong>सेप्टेम्बर १८, २०२६</strong> देखि <strong>अक्टोबर १७, २०२६</strong> सम्म पर्दछ। <strong>असोज ३ मा संविधान दिवस</strong> र <strong>असोज २५ मा दशैंको घटस्थापना</strong> पर्दछ।",
    holidays={
      3:  dict(label="संविधान दिवस — Constitution Day", type="hol", adDate="Sep 19, 2026", dayEn="Saturday",
               desc="Nepal Constitution Day. Also falls on Saturday (weekly holiday). National public holiday.",
               tithi="तृतीया"),
      25: dict(label="घटस्थापना — Dashain Day 1", type="hol", adDate="Oct 11, 2026", dayEn="Sunday",
               desc="Ghatasthapana — first day of Dashain. Kalash established, Jamara planted. National public holiday.",
               tithi="पञ्चमी"),
    },
    aus=[],
    faqs=[
      dict(q="Dashain 2083 Ghatasthapana date — When does Dashain start in 2083?",
           a="Dashain 2083 Ghatasthapana falls on Sunday, October 11, 2026 (Ashoj 25, 2083 BS). This is the first day of the 15-day Dashain festival. Due to Mala Maas in 2083, Dashain is much later than usual."),
      dict(q="Constitution Day 2083 date — When is Sambidhan Diwas 2083?",
           a="Constitution Day 2083 falls on Saturday, September 19, 2026 (Ashoj 3, 2083 BS). It is a national public holiday. Notably it also falls on Saturday, Nepal's weekly off day."),
      dict(q="How many days in Ashoj 2083?",
           a="Ashoj 2083 has 30 days, from September 18, 2026 to October 17, 2026 AD."),
      dict(q="Why is Dashain so late in 2083?",
           a="Dashain 2083 falls later because of the Mala Maas (intercalary month) that occurred in Jestha–Ashadh 2083 BS (May–June 2026). This extra month pushed all subsequent festivals approximately one month later on the English calendar."),
    ],
    events=[
      dict(name="Constitution Day 2083", date="2026-09-19", desc="Ashoj 3, 2083 — National public holiday."),
      dict(name="Dashain Ghatasthapana 2083", date="2026-10-11", desc="Ashoj 25, 2083 — Dashain Day 1. National public holiday."),
    ],
    note=None,
  ),
  dict(
    id="kartik", num=7, ne="कार्तिक", en="Kartik", days=29,
    startDOW=0,  # Sunday
    adStart="October 18, 2026", adEnd="November 15, 2026",
    adStartISO="2026-10-18", adEndISO="2026-11-15",
    adStartObj=(2026,9,18),
    slug="kartik-2083",
    prev="ashoj", next_="mangsir",
    keywords="kartik 2083, kartik 2083 calendar, dashain 2083 tika date, tihar 2083 date, bhai tika 2083, vijaya dashami 2083, kartik patro 2083, deepawali 2083",
    desc="Kartik 2083 BS calendar — 29 days, Oct 18 to Nov 15, 2026. Vijaya Dashami Oct 20, Tihar Bhai Tika Nov 11. Full holidays, tithi, AD dates.",
    intro_en="""Kartik 2083 BS is the <strong>seventh month</strong>, running from <strong>October 18 to November 15, 2026</strong> with <strong>29 days</strong>. 
This is <strong>Nepal's most festive month</strong> — hosting the climax of both Dashain and Tihar. 
<strong>Vijaya Dashami (Dashain Tika)</strong> falls on <strong>Kartik 3 (October 20, 2026)</strong>. This is the main day of Dashain when elders apply Tika and Jamara to younger family members. Government offices close for the full Dashain period. 
<strong>Tihar (Deepawali)</strong> spans several days in mid-Kartik, culminating in <strong>Bhai Tika on Kartik 25 (November 11, 2026)</strong> — when sisters apply a special seven-coloured Tika to their brothers. 
<strong>Chhath Parva</strong> also falls in Kartik 2083.""",
    intro_ne="कार्तिक २०८३ नेपाली वर्षको सातौं महिना हो। यसमा २९ दिन छन् र <strong>अक्टोबर १८, २०२६</strong> देखि <strong>नोभेम्बर १५, २०२६</strong> सम्म पर्दछ। <strong>विजया दशमी (कार्तिक ३, अक्टोबर २०)</strong> र <strong>भाइ टीका / तिहार (कार्तिक २५, नोभेम्बर ११)</strong> यस महिनामा पर्दछन्।",
    holidays={
      3:  dict(label="विजया दशमी — Dashain Tika", type="hol", adDate="Oct 20, 2026", dayEn="Tuesday",
               desc="Main day of Dashain. Elders apply Tika and Jamara. The most important national public holiday in Nepal.",
               tithi="दशमी"),
      25: dict(label="भाइ टीका — Tihar (Bhai Tika)", type="hol", adDate="Nov 11, 2026", dayEn="Wednesday",
               desc="Final day of Tihar / Deepawali. Sisters apply seven-coloured Tika to brothers. National public holiday.",
               tithi="पञ्चमी"),
    },
    aus=[],
    faqs=[
      dict(q="Vijaya Dashami 2083 date — When is Dashain Tika 2083?",
           a="Vijaya Dashami (Dashain Tika) 2083 falls on Tuesday, October 20, 2026 (Kartik 3, 2083 BS). This is the main day of Dashain and a national public holiday in Nepal."),
      dict(q="Tihar 2083 date — When is Bhai Tika 2083?",
           a="Tihar Bhai Tika 2083 falls on Wednesday, November 11, 2026 (Kartik 25, 2083 BS). This is the final and most celebrated day of the Tihar festival."),
      dict(q="How many days in Kartik 2083?",
           a="Kartik 2083 has 29 days, from October 18, 2026 to November 15, 2026 AD."),
      dict(q="When is Chhath 2083?",
           a="Chhath Parva 2083 falls in Kartik 2083. The exact date (Saptami to Saptami) depends on Tithi — verify with the official MoHA gazette."),
      dict(q="How many days is the Dashain holiday in Nepal 2083?",
           a="The official Dashain government holiday in Nepal typically runs from around Ghatasthapana (Ashoj 25) through Vijaya Dashami (Kartik 3). Vijaya Dashami on October 20, 2026 is the main public holiday day."),
    ],
    events=[
      dict(name="Vijaya Dashami 2083", date="2026-10-20", desc="Kartik 3, 2083 — Dashain main day. National public holiday."),
      dict(name="Tihar Bhai Tika 2083", date="2026-11-11", desc="Kartik 25, 2083 — Tihar final day. National public holiday."),
    ],
    note=None,
  ),
  dict(
    id="mangsir", num=8, ne="मंसिर", en="Mangsir", days=30,
    startDOW=1,  # Monday
    adStart="November 16, 2026", adEnd="December 15, 2026",
    adStartISO="2026-11-16", adEndISO="2026-12-15",
    adStartObj=(2026,10,16),
    slug="mangsir-2083",
    prev="kartik", next_="poush",
    keywords="mangsir 2083, mangsir 2083 calendar, mansir 2083, mangsir patro 2083, mangsir 2083 holidays, mangsir 2083 tithi, mangsir 2083 sait",
    desc="Mangsir 2083 BS calendar — 30 days, November 16 to December 15, 2026. Auspicious marriage dates, tithi and AD dates.",
    intro_en="""Mangsir 2083 BS is the <strong>eighth month</strong>, running from <strong>November 16 to December 15, 2026</strong> with <strong>30 days</strong>. 
Mangsir is when Nepal's winter truly arrives — clear blue skies, cool mornings, and the post-festival calm after Dashain and Tihar. 
This month is popular for <strong>wedding season</strong>. Auspicious marriage dates (Shubha Sait) in Mangsir should be verified with the official NPNS Panchanga as they depend on exact Tithi calculations for 2083. 
Notable: <strong>Vivah Panchami</strong> (the divine wedding of Ram and Sita) is observed in Mangsir. The month also includes <strong>Gita Jayanti</strong>.""",
    intro_ne="मंसिर २०८३ नेपाली वर्षको आठौं महिना हो। यसमा ३० दिन छन् र <strong>नोभेम्बर १६, २०२६</strong> देखि <strong>डिसेम्बर १५, २०२६</strong> सम्म पर्दछ। दशैं-तिहारपछिको शान्त यो महिनामा विवाहका शुभ साइतहरू पर्न सक्छन्।",
    holidays={},
    aus=[
      dict(type="विवाह — verify NPNS", ne="मंसिर (Panchanga)", ad="Nov–Dec 2026 · Confirm official Sait"),
    ],
    faqs=[
      dict(q="How many days in Mangsir 2083?",
           a="Mangsir 2083 has 30 days, from November 16, 2026 to December 15, 2026 AD."),
      dict(q="Are there auspicious marriage dates in Mangsir 2083?",
           a="Mangsir is a popular wedding month in Nepal. Exact auspicious dates (Shubha Sait) for Mangsir 2083 should be verified with the official NPNS Panchanga or your local Jyotish (astrologer)."),
      dict(q="When is Vivah Panchami 2083?",
           a="Vivah Panchami 2083 falls in Mangsir 2083 BS on the Panchami (5th day) of Shukla Paksha. Verify the exact date with the official Panchanga."),
    ],
    events=[],
    note=None,
  ),
  dict(
    id="poush", num=9, ne="पौष", en="Poush", days=29,
    startDOW=3,  # Wednesday
    adStart="December 16, 2026", adEnd="January 13, 2027",
    adStartISO="2026-12-16", adEndISO="2027-01-13",
    adStartObj=(2026,11,16),
    slug="poush-2083",
    prev="mangsir", next_="magh",
    keywords="poush 2083, poush 2083 calendar, push 2083, poush patro 2083, christmas nepal 2083, poush 2083 tithi, poush 2083 holidays",
    desc="Poush 2083 BS calendar — 29 days, December 16, 2026 to January 13, 2027. Christmas public holiday, tithi and AD dates.",
    intro_en="""Poush 2083 BS is the <strong>ninth month</strong>, running from <strong>December 16, 2026 to January 13, 2027</strong> with <strong>29 days</strong>. 
Poush is the <strong>heart of Nepal's winter</strong>. Temperatures drop sharply in the hills and mountains, while the Terai remains mild. 
<strong>Christmas (December 25)</strong> is a gazetted public holiday in Nepal, falling in Poush 2083. 
<strong>Tula Sankranti</strong> and <strong>Udhauli</strong> (Kirat community harvest festival) are also observed this month. 
The month leads directly into Maghe Sankranti on Magh 1.""",
    intro_ne="पौष २०८३ नेपाली वर्षको नवौं महिना हो। यसमा २९ दिन छन् र <strong>डिसेम्बर १६, २०२६</strong> देखि <strong>जनवरी १३, २०२७</strong> सम्म पर्दछ। <strong>क्रिसमस (डिसेम्बर २५)</strong> सार्वजनिक बिदा यस महिनामा पर्दछ।",
    holidays={},
    aus=[],
    faqs=[
      dict(q="How many days in Poush 2083?",
           a="Poush 2083 has 29 days, from December 16, 2026 to January 13, 2027 AD."),
      dict(q="Is Christmas a public holiday in Nepal?",
           a="Yes. Christmas (December 25) is a gazetted public holiday in Nepal. It falls in Poush 2083 BS."),
      dict(q="What comes after Poush 2083?",
           a="Magh 2083 follows Poush. Magh 1 (January 14, 2027) is Maghe Sankranti — one of the most celebrated national holidays in Nepal."),
    ],
    events=[],
    note=None,
  ),
  dict(
    id="magh", num=10, ne="माघ", en="Magh", days=29,
    startDOW=4,  # Thursday
    adStart="January 14, 2027", adEnd="February 11, 2027",
    adStartISO="2027-01-14", adEndISO="2027-02-11",
    adStartObj=(2027,0,14),
    slug="magh-2083",
    prev="poush", next_="falgun",
    keywords="magh 2083, magh 2083 calendar, magh patro 2083, maghe sankranti 2083, maghi 2083, magh 2083 holidays, magh 2083 tithi",
    desc="Magh 2083 BS calendar — 29 days, January 14 to February 11, 2027. Maghe Sankranti / Maghi on Magh 1. Public holiday, tithi and AD dates.",
    intro_en="""Magh 2083 BS is the <strong>tenth month</strong>, running from <strong>January 14 to February 11, 2027</strong> with <strong>29 days</strong>. 
<strong>Magh 1 (January 14, 2027)</strong> is <strong>Maghe Sankranti</strong> — one of Nepal's most beloved festivals. On this day, people eat traditional foods: <strong>til (sesame)</strong>, <strong>ghiu (clarified butter)</strong>, <strong>chaku (molasses sweet)</strong>, and <strong>tarul (yam)</strong>. 
The Tharu community celebrates this day as <strong>Maghi</strong> — their New Year. It is a national public holiday. 
Devotees also take ritual baths at the confluence of sacred rivers (Triveni, Devghat). The month marks the end of the harshest winter.""",
    intro_ne="माघ २०८३ नेपाली वर्षको दशौं महिना हो। यसमा २९ दिन छन् र <strong>जनवरी १४, २०२७</strong> देखि <strong>फेब्रुअरी ११, २०२७</strong> सम्म पर्दछ। <strong>माघ १ मा माघे संक्रान्ति / माघी</strong> राष्ट्रिय बिदा पर्दछ।",
    holidays={
      1: dict(label="माघे संक्रान्ति / माघी", type="hol", adDate="Jan 14, 2027", dayEn="Thursday",
              desc="Maghe Sankranti — first day of Magh. Celebrated with til, ghiu, chaku. Tharu New Year (Maghi). National public holiday.",
              tithi="प्रतिपदा"),
    },
    aus=[
      dict(type="विवाह (Marriage)", ne="माघ (Panchanga)", ad="Jan–Feb 2027 · Verify with NPNS"),
    ],
    faqs=[
      dict(q="Maghe Sankranti 2083 date — When is Maghe Sankranti?",
           a="Maghe Sankranti 2083 falls on Thursday, January 14, 2027 (Magh 1, 2083 BS). It is a national public holiday celebrated with traditional foods like til, ghiu, chaku and tarul."),
      dict(q="How many days in Magh 2083?",
           a="Magh 2083 has 29 days, from January 14, 2027 to February 11, 2027 AD."),
      dict(q="What is Maghi 2083?",
           a="Maghi is the Tharu community's New Year, celebrated on Magh 1 (January 14, 2027). It coincides with Maghe Sankranti and is a national public holiday in Nepal."),
    ],
    events=[
      dict(name="Maghe Sankranti / Maghi 2083", date="2027-01-14", desc="Magh 1, 2083 — National public holiday."),
    ],
    note=None,
  ),
  dict(
    id="falgun", num=11, ne="फाल्गुन", en="Falgun", days=30,
    startDOW=5,  # Friday
    adStart="February 12, 2027", adEnd="March 13, 2027",
    adStartISO="2027-02-12", adEndISO="2027-03-13",
    adStartObj=(2027,1,12),
    slug="falgun-2083",
    prev="magh", next_="chaitra",
    keywords="falgun 2083, falgun 2083 calendar, phagun 2083, holi 2083 date, fagu purnima 2083, falgun patro 2083, falgun 2083 tithi",
    desc="Falgun 2083 BS calendar — 30 days, February 12 to March 13, 2027. Holi (Fagu Purnima) date, tithi and AD dates.",
    intro_en="""Falgun 2083 BS is the <strong>eleventh month</strong>, running from <strong>February 12 to March 13, 2027</strong> with <strong>30 days</strong>. 
Falgun is the month of <strong>Holi (Fagu Purnima)</strong> — the vibrant festival of colours. In Nepal, Kathmandu Valley celebrates Holi one day before the rest of the country (on Chaturdashi), while hill and Terai regions celebrate on the Purnima (full moon) day. 
Spring begins in Falgun — mustard fields bloom yellow across the Terai and temperatures start rising. This is also an active wedding season with several auspicious dates — verify with official Panchanga.""",
    intro_ne="फाल्गुन २०८३ नेपाली वर्षको एघारौं महिना हो। यसमा ३० दिन छन् र <strong>फेब्रुअरी १२, २०२७</strong> देखि <strong>मार्च १३, २०२७</strong> सम्म पर्दछ। <strong>फागु पूर्णिमा (होली)</strong> यस महिनामा पर्दछ।",
    holidays={},
    aus=[
      dict(type="विवाह — verify NPNS", ne="फाल्गुन (Panchanga)", ad="Feb–Mar 2027 · Confirm official Sait"),
    ],
    faqs=[
      dict(q="Holi 2083 date — When is Fagu Purnima 2083?",
           a="Holi (Fagu Purnima) 2083 falls in Falgun 2083 BS (February–March 2027). Kathmandu Valley celebrates one day earlier (Chaturdashi). Verify the exact date with official Panchanga sources."),
      dict(q="How many days in Falgun 2083?",
           a="Falgun 2083 has 30 days, from February 12, 2027 to March 13, 2027 AD."),
      dict(q="Are there auspicious marriage dates in Falgun 2083?",
           a="Falgun typically has several auspicious marriage dates. Verify exact Shubha Sait windows for Falgun 2083 with the official NPNS Panchanga."),
    ],
    events=[],
    note=None,
  ),
  dict(
    id="chaitra", num=12, ne="चैत्र", en="Chaitra", days=30,
    startDOW=6,  # Saturday
    adStart="March 14, 2027", adEnd="April 13, 2027",
    adStartISO="2027-03-14", adEndISO="2027-04-13",
    adStartObj=(2027,2,14),
    slug="chaitra-2083",
    prev="falgun", next_=None,
    keywords="chaitra 2083, chaitra 2083 calendar, chait 2083, chaitra patro 2083, chaitra dashain 2083, ram navami 2083, chaitra 2083 holidays",
    desc="Chaitra 2083 BS calendar — 30 days, March 14 to April 13, 2027. Last month of 2083. Chaitra Dashain, Ram Navami, Ghode Jatra. Tithi and AD dates.",
    intro_en="""Chaitra 2083 BS is the <strong>twelfth and final month</strong> of the Nepali year, running from <strong>March 14 to April 13, 2027</strong> with <strong>30 days</strong>. 
Chaitra 1 (March 14, 2027) falls on a <strong>Saturday — Nepal's weekly holiday</strong>. 
This month hosts <strong>Chaitra Dashain</strong> (a shorter version of the main Dashain), <strong>Ram Navami</strong> (birth anniversary of Lord Ram), and <strong>Ghode Jatra</strong> (horse racing festival) in Kathmandu. 
<strong>Chaitra 30 (April 13, 2027)</strong> is the last day of 2083 BS. The following day — <strong>Baisakh 1, 2084 (April 14, 2027)</strong> — will be the Nepali New Year 2084.
This is also the peak of Nepal's spring trekking season.""",
    intro_ne="चैत्र २०८३ नेपाली वर्षको बाह्रौं र अन्तिम महिना हो। यसमा ३० दिन छन् र <strong>मार्च १४, २०२७</strong> देखि <strong>अप्रिल १३, २०२७</strong> सम्म पर्दछ। <strong>चैत्र ३० मा वर्ष २०८३ समाप्त हुन्छ।</strong>",
    holidays={},
    aus=[],
    faqs=[
      dict(q="How many days in Chaitra 2083?",
           a="Chaitra 2083 has 30 days, from March 14, 2027 to April 13, 2027 AD."),
      dict(q="When does Nepali year 2083 end?",
           a="Nepali year 2083 BS ends on Chaitra 30, 2083 — April 13, 2027 AD. The New Year 2084 begins on Baisakh 1, 2084 (April 14, 2027)."),
      dict(q="When is Ghode Jatra 2083?",
           a="Ghode Jatra 2083 falls in Chaitra 2083 BS (~March 2027). It is a horse racing festival held at Tundikhel, Kathmandu, celebrating the defeat of the demon Tundi. Verify the exact date with official sources."),
      dict(q="When is Ram Navami 2083?",
           a="Ram Navami 2083 falls on the Navami (9th day) of Shukla Paksha in Chaitra 2083 BS. Verify the exact date with the official NPNS Panchanga."),
    ],
    events=[],
    note=None,
  ),
]

# ── Shared CSS (inlined per page for Cloudflare static) ─────────────────
SHARED_CSS = """
    :root{--red:#C0392B;--red-lt:#FEF0EE;--red-dk:#96281B;--sat:#C0392B;--sun:#1A5FAA;--gold:#A07800;--gold-lt:#FFF8E0;--mala:#5B2D8E;--mala-lt:#F2EDFF;--ink:#1C1C1E;--ink2:#3A3A3C;--ink3:#6C6C70;--paper:#FDFAF5;--card:#FFFFFF;--border:#E5DDD0;--nav-h:52px;--radius:10px;--shadow:0 2px 14px rgba(0,0,0,0.07)}
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    html{scroll-behavior:smooth;scroll-padding-top:calc(var(--nav-h) + 8px)}
    body{font-family:'DM Sans',sans-serif;background:var(--paper);color:var(--ink);line-height:1.55;-webkit-text-size-adjust:100%}
    /* NAV */
    .month-nav{position:sticky;top:0;z-index:200;background:var(--ink);height:var(--nav-h);display:flex;align-items:center;overflow-x:auto;overflow-y:hidden;-webkit-overflow-scrolling:touch;scrollbar-width:none;gap:4px;padding:0 10px;box-shadow:0 2px 12px rgba(0,0,0,.25)}
    .month-nav::-webkit-scrollbar{display:none}
    .mnav-home{display:flex;align-items:center;gap:5px;color:#F4C26B;text-decoration:none;font-family:'Tiro Devanagari Hindi',serif;font-size:.9rem;font-weight:600;white-space:nowrap;padding:6px 10px;border-radius:6px;border-right:1px solid rgba(255,255,255,.15);margin-right:4px;flex-shrink:0}
    .mnav-home:hover{background:rgba(255,255,255,.1)}
    .mnav-divider{color:rgba(255,255,255,.3);flex-shrink:0;font-size:.8rem}
    .mnav-btn{flex-shrink:0;background:transparent;border:none;color:#A89F90;font-family:'Tiro Devanagari Hindi',serif;font-size:.88rem;padding:6px 10px;border-radius:6px;cursor:pointer;white-space:nowrap;transition:background .15s,color .15s;text-decoration:none;display:inline-flex;align-items:center}
    .mnav-btn:hover{background:rgba(255,255,255,.1);color:#fff}
    .mnav-btn.active{background:var(--red);color:#fff;font-weight:600}
    /* HERO */
    .hero{background:var(--ink);color:#fff;text-align:center;padding:40px 20px 34px;position:relative;overflow:hidden}
    .hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 70% 55% at 85% 5%,rgba(192,57,43,.4) 0%,transparent 65%),radial-gradient(ellipse 50% 50% at 10% 95%,rgba(91,45,142,.35) 0%,transparent 60%);pointer-events:none}
    .hero-ne{font-family:'Tiro Devanagari Hindi',serif;font-size:clamp(2.2rem,8vw,4.2rem);line-height:1.1;position:relative}
    .hero-ne em{color:#F4C26B;font-style:normal}
    .hero-en{font-family:'Playfair Display',serif;font-size:clamp(.82rem,2.2vw,1rem);color:#A89F90;margin-top:8px;letter-spacing:.1em;text-transform:uppercase;position:relative}
    .hero-meta{font-size:.78rem;color:#7A7060;margin-top:6px;position:relative}
    .hero-cta{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:18px;position:relative}
    .cta-btn{display:inline-flex;align-items:center;gap:6px;background:var(--red);color:#fff;border-radius:8px;padding:9px 16px;font-weight:600;font-size:.84rem;text-decoration:none;transition:background .18s,transform .14s}
    .cta-btn:hover{background:var(--red-dk);transform:translateY(-1px)}
    .cta-btn.ghost{background:transparent;border:1.5px solid rgba(255,255,255,.28);color:#E0D8C8}
    .cta-btn.ghost:hover{background:rgba(255,255,255,.08)}
    /* LAYOUT */
    .wrap{max-width:900px;margin:0 auto;padding:0 16px}
    .ad-slot{max-width:900px;margin:14px auto;padding:0 16px}
    /* BREADCRUMB */
    .bc{max-width:900px;margin:12px auto 0;padding:0 16px;font-size:.74rem;color:var(--ink3)}
    .bc a{color:var(--red);text-decoration:none}.bc a:hover{text-decoration:underline}
    .bc span{margin:0 5px}
    /* INTRO */
    .intro-box{margin:18px 0 12px;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px;box-shadow:var(--shadow)}
    .intro-box h1{font-family:'Playfair Display',serif;font-size:clamp(1.1rem,3.2vw,1.35rem);margin-bottom:10px}
    .intro-box p{font-size:.87rem;color:var(--ink2);line-height:1.75;margin-bottom:8px}
    .intro-box p:last-child{margin-bottom:0}
    .intro-box a{color:var(--red)}
    .intro-box strong{color:var(--ink)}
    /* NOTICE */
    .notice{border-radius:var(--radius);padding:13px 16px;display:flex;gap:12px;align-items:flex-start;margin:12px 0;font-size:.83rem}
    .notice.mala{background:var(--mala-lt);border:1.5px solid var(--mala)}
    .notice.mala strong{color:var(--mala)}
    .notice.mala a{color:var(--mala);font-weight:600}
    .notice.green{background:#E8F7EE;border:1.5px solid #1A7A4A}
    .notice.green strong{color:#1A7A4A}
    .notice-ico{font-size:1.4rem;flex-shrink:0;margin-top:2px}
    .notice p{color:var(--ink2);line-height:1.6;margin-top:3px}
    /* SEC HEAD */
    .sec-head{font-family:'Playfair Display',serif;font-size:1.15rem;margin:22px 0 12px;display:flex;align-items:center;gap:10px}
    .sec-head::after{content:'';flex:1;height:1px;background:var(--border)}
    /* HOL CARDS */
    .hol-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin-bottom:24px}
    .hol-card{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--red);border-radius:var(--radius);padding:13px 15px;display:flex;gap:12px;align-items:center;box-shadow:var(--shadow);cursor:pointer;transition:transform .14s,box-shadow .14s}
    .hol-card:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.1)}
    .hol-card.gold{border-left-color:var(--gold)}
    .hol-dblk{text-align:center;min-width:44px}
    .hol-bsn{font-family:'Tiro Devanagari Hindi',serif;font-size:1.5rem;color:var(--red);line-height:1}
    .hol-card.gold .hol-bsn{color:var(--gold)}
    .hol-mne{font-size:.58rem;color:var(--ink3);text-transform:uppercase;letter-spacing:.04em;margin-top:2px}
    .hol-nm{font-weight:600;font-size:.85rem}
    .hol-ad{font-size:.72rem;color:var(--ink3);margin-top:2px}
    .hol-desc-txt{font-size:.75rem;color:var(--ink3);margin-top:4px;line-height:1.55}
    .tag{display:inline-block;font-size:.58rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:2px 7px;border-radius:20px;margin-top:4px}
    .tag.nat{background:var(--red-lt);color:var(--red)}.tag.fest{background:var(--gold-lt);color:var(--gold)}.tag.week{background:var(--mala-lt);color:var(--mala)}
    /* CALENDAR */
    .cal-section{margin-bottom:28px}
    .cal-head{display:flex;align-items:baseline;flex-wrap:wrap;gap:10px;margin-bottom:8px}
    .cal-head h2{font-family:'Tiro Devanagari Hindi',serif;font-size:1.5rem;font-weight:400}
    .cal-head-en{font-family:'Playfair Display',serif;font-size:.9rem;color:var(--ink3);font-style:italic}
    .cal-head-days{margin-left:auto;font-size:.72rem;color:var(--ink3);font-weight:500}
    .tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:var(--radius)}
    table.cal{width:100%;border-collapse:collapse;min-width:290px;background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden}
    table.cal thead th{background:var(--ink);color:#fff;font-size:.68rem;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:8px 2px;text-align:center}
    table.cal thead th:last-child{color:#FF9B9B}
    table.cal thead th:first-child{color:#A8C8FF}
    table.cal td{border:1px solid #EDE5D8;vertical-align:top;padding:4px 4px 14px;height:62px;width:14.28%;position:relative;cursor:pointer;transition:background .1s}
    table.cal td:hover:not(.empty){background:#F5F0E8!important}
    table.cal td.empty{background:var(--paper);cursor:default;pointer-events:none}
    table.cal td.is-sat .bs-num{color:var(--sat)}
    table.cal td.is-sat{background:#FFF7F6}
    table.cal td.is-sun .bs-num{color:var(--sun)}
    table.cal td.is-hol{background:var(--red-lt)}
    table.cal td.is-hol .bs-num{color:var(--red)!important}
    table.cal td.is-mala{background:var(--mala-lt)}
    table.cal td.is-mala .bs-num{color:var(--mala)!important}
    table.cal td.is-purnima::after{content:'🌕';position:absolute;top:2px;right:3px;font-size:.5rem;line-height:1}
    table.cal td.is-ekadashi::after{content:'🌓';position:absolute;top:2px;right:3px;font-size:.5rem;line-height:1}
    table.cal td.is-today{box-shadow:inset 0 0 0 2.5px var(--gold)}
    .bs-num{font-family:'Tiro Devanagari Hindi',serif;font-size:clamp(1.05rem,3vw,1.42rem);line-height:1;display:block}
    .ad-num{font-size:.58rem;color:var(--ink3);display:block;margin-top:1px}
    .cell-bot{font-size:.48rem;display:block;position:absolute;bottom:2px;left:3px;right:3px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;line-height:1.2}
    .cell-bot.hol-lbl{color:var(--red);font-weight:700}
    .cell-bot.tithi-lbl{color:var(--ink3)}
    /* TITHI TABLE */
    .tithi-table{width:100%;border-collapse:collapse;font-size:.8rem;background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;margin-bottom:24px}
    .tithi-table thead th{background:var(--ink);color:#fff;padding:8px 10px;text-align:left;font-size:.72rem;font-weight:600;letter-spacing:.05em}
    .tithi-table tbody tr:nth-child(even){background:#FAF6F0}
    .tithi-table td{padding:7px 10px;border-bottom:1px solid var(--border)}
    .tithi-table td:first-child{font-family:'Tiro Devanagari Hindi',serif;font-size:1rem;color:var(--ink)}
    .tithi-table td.hol-cell{color:var(--red);font-weight:600}
    .tithi-table td.sat-cell{color:var(--sat)}
    .tithi-table td.purnima-cell{color:var(--mala);font-weight:600}
    /* MONTH NAV CARDS */
    .month-nav-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin-bottom:24px}
    .mnc{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:10px 13px;text-decoration:none;color:var(--ink);display:block;transition:transform .14s,box-shadow .14s;box-shadow:var(--shadow)}
    .mnc:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.1)}
    .mnc.current{border:2px solid var(--red);background:var(--red-lt)}
    .mnc-ne{font-family:'Tiro Devanagari Hindi',serif;font-size:1.1rem;display:block}
    .mnc-en{font-size:.68rem;color:var(--ink3);display:block}
    .mnc-days{font-size:.62rem;color:var(--ink3)}
    /* AUS */
    .aus-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin-bottom:24px}
    .aus-card{background:var(--gold-lt);border:1px solid #DDBA55;border-radius:var(--radius);padding:12px 14px;box-shadow:var(--shadow)}
    .aus-card.mala{background:var(--mala-lt);border-color:var(--mala)}
    .aus-type{font-size:.6rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--gold)}
    .aus-card.mala .aus-type{color:var(--mala)}
    .aus-ne{font-family:'Tiro Devanagari Hindi',serif;font-size:1rem;color:var(--ink2);display:block;margin-top:3px}
    .aus-ad{font-size:.72rem;color:var(--ink3)}
    /* FAQ */
    .faq-list{margin-bottom:24px}
    .faq-item{border:1px solid var(--border);border-radius:var(--radius);background:var(--card);margin-bottom:8px;box-shadow:var(--shadow);overflow:hidden}
    .faq-q{width:100%;text-align:left;background:none;border:none;padding:13px 15px;font-family:'DM Sans',sans-serif;font-size:.875rem;font-weight:600;color:var(--ink);cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:10px;line-height:1.4}
    .faq-q:hover{background:var(--paper)}
    .faq-arrow{font-size:.8rem;color:var(--ink3);transition:transform .2s;flex-shrink:0}
    .faq-item.open .faq-arrow{transform:rotate(180deg)}
    .faq-a{max-height:0;overflow:hidden;transition:max-height .28s ease,padding .2s;padding:0 15px;font-size:.84rem;color:var(--ink2);line-height:1.7}
    .faq-item.open .faq-a{max-height:300px;padding:0 15px 13px}
    /* LEGEND */
    .legend{display:flex;flex-wrap:wrap;gap:11px;margin-bottom:18px}
    .leg{display:flex;align-items:center;gap:6px;font-size:.72rem;color:var(--ink2)}
    .leg-dot{width:12px;height:12px;border-radius:3px;flex-shrink:0}
    /* PREV/NEXT */
    .pn-nav{display:flex;gap:10px;margin:20px 0}
    .pn-btn{flex:1;background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:13px 16px;text-decoration:none;color:var(--ink);display:flex;align-items:center;gap:10px;box-shadow:var(--shadow);transition:transform .14s,box-shadow .14s;min-width:0}
    .pn-btn:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,.1);border-color:var(--red)}
    .pn-btn.next{flex-direction:row-reverse;text-align:right}
    .pn-arrow{font-size:1.2rem;flex-shrink:0;color:var(--red)}
    .pn-label{font-size:.65rem;color:var(--ink3);display:block;text-transform:uppercase;letter-spacing:.06em}
    .pn-ne{font-family:'Tiro Devanagari Hindi',serif;font-size:1.1rem;display:block}
    .pn-en{font-size:.75rem;color:var(--ink3)}
    /* FOOT */
    .foot-note{background:#F0EAE0;border-radius:var(--radius);padding:13px 17px;font-size:.77rem;color:var(--ink3);margin-bottom:32px;line-height:1.7}
    .foot-note a{color:var(--red)}.foot-note strong{color:var(--ink2)}
    /* MODAL */
    .overlay{display:none;position:fixed;inset:0;background:rgba(28,28,30,.5);backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px);z-index:500;align-items:flex-end;justify-content:center}
    .overlay.open{display:flex}
    .sheet{background:var(--card);border-radius:20px 20px 0 0;width:100%;max-width:480px;max-height:90vh;overflow-y:auto;padding-bottom:env(safe-area-inset-bottom,16px);animation:sheetUp .26s cubic-bezier(.16,1,.3,1);box-shadow:0 -10px 40px rgba(0,0,0,.2)}
    @keyframes sheetUp{from{transform:translateY(100%)}to{transform:translateY(0)}}
    @media(min-width:580px){.overlay{align-items:center;padding:20px}.sheet{border-radius:18px;max-height:85vh}}
    .sheet-handle{width:36px;height:4px;background:var(--border);border-radius:4px;margin:12px auto 0}
    .sheet-hdr{padding:15px 17px 11px;border-bottom:1px solid var(--border);display:flex;align-items:flex-start;justify-content:space-between}
    .sheet-bs{font-family:'Tiro Devanagari Hindi',serif;font-size:3rem;line-height:1;color:var(--ink)}
    .sheet-mne{font-family:'Tiro Devanagari Hindi',serif;font-size:1rem;color:var(--ink3);display:block;margin-top:2px}
    .sheet-close{background:#F2F2F7;border:none;border-radius:50%;width:30px;height:30px;font-size:.9rem;cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--ink2);flex-shrink:0;margin-top:4px}
    .sheet-body{padding:15px 17px}
    .srow{display:flex;align-items:flex-start;gap:12px;padding:9px 0;border-bottom:1px solid var(--border)}
    .srow:last-of-type{border-bottom:none}
    .srow-ico{font-size:1.1rem;width:25px;text-align:center;flex-shrink:0;margin-top:1px}
    .srow-lbl{font-size:.68rem;color:var(--ink3);display:block}
    .srow-val{font-size:.88rem;font-weight:600;color:var(--ink);display:block}
    .sat-note{background:var(--red-lt);border-radius:8px;padding:9px 12px;font-size:.78rem;color:var(--red);font-weight:500;margin-top:8px}
    .hol-badge{display:flex;align-items:center;gap:7px;background:var(--red-lt);color:var(--red);border:1px solid #F1B7B0;border-radius:8px;padding:8px 12px;font-weight:600;font-size:.82rem;margin-top:8px}
    .hol-desc-modal{font-size:.77rem;color:var(--ink3);margin-top:5px;line-height:1.6}
    .wa-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:#25D366;color:#fff;border-radius:10px;padding:11px;text-decoration:none;font-weight:600;font-size:.86rem;margin-top:13px;transition:background .18s}
    .wa-btn:hover{background:#1EAA52}
    .conv-btn{display:flex;align-items:center;justify-content:center;gap:7px;background:var(--red);color:#fff;border-radius:10px;padding:11px;text-decoration:none;font-weight:600;font-size:.86rem;margin-top:7px;transition:background .18s}
    .conv-btn:hover{background:var(--red-dk)}
    .sheet-links{display:flex;gap:8px;margin-top:7px;flex-wrap:wrap}
    .sheet-links a{flex:1;min-width:110px;display:flex;align-items:center;justify-content:center;gap:5px;background:var(--paper);border:1px solid var(--border);border-radius:8px;padding:8px 10px;text-decoration:none;color:var(--ink2);font-size:.77rem;font-weight:500;transition:background .14s}
    .sheet-links a:hover{background:#EDE8DE}
    @media print{.month-nav,.hero-cta,.ad-slot,.overlay,.pn-nav{display:none!important}body{background:#fff}table.cal td{height:48px}.tbl-wrap{overflow:visible}}
    @media(max-width:400px){table.cal td{height:50px;padding:3px 2px 12px}.bs-num{font-size:.98rem}.cell-bot{display:none}}
"""

SHARED_JS = """
const ND=['०','१','२','३','४','५','६','७','८','९'];
const toNe=n=>String(n).split('').map(d=>ND[+d]).join('');
const TODAY=new Date();
const TITHIS=['प्रतिपदा','द्वितीया','तृतीया','चतुर्थी','पञ्चमी','षष्ठी','सप्तमी','अष्टमी','नवमी','दशमी','एकादशी','द्वादशी','त्रयोदशी','चतुर्दशी','पूर्णिमा / औँसी'];
const DAY_NE=['आइतबार','सोमबार','मंगलबार','बुधबार','बिहीबार','शुक्रबार','शनिबार'];
const DAY_EN=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
function toggleFaq(btn){const item=btn.closest('.faq-item');const isOpen=item.classList.contains('open');document.querySelectorAll('.faq-item.open').forEach(i=>i.classList.remove('open'));if(!isOpen)item.classList.add('open');btn.setAttribute('aria-expanded',!isOpen);}
function openModal(d){
  document.getElementById('s-bs').textContent=d.bsDayNe;
  document.getElementById('s-mne').textContent=d.monthNe+' २०८३';
  document.getElementById('s-ad').textContent=d.adStr;
  document.getElementById('s-bs-full').textContent=d.bsDayNe+' '+d.monthNe+' २०८३ BS';
  document.getElementById('s-tithi').textContent=d.tithiStr;
  document.getElementById('s-day').textContent=d.dayNe+' — '+d.dayEn;
  document.getElementById('s-sat-note').style.display=d.isSat?'block':'none';
  const hw=document.getElementById('s-hol-wrap');
  if(d.isHoliday&&d.holName){document.getElementById('s-hol-badge').textContent='🎉 '+d.holName;document.getElementById('s-hol-desc').textContent=d.holDesc||'';hw.style.display='block';}
  else hw.style.display='none';
  const waText=encodeURIComponent('📅 '+d.bsDayNe+' '+d.monthNe+' २०८३ BS\\n'+d.adStr+'\\nTithi: '+d.tithiStr+(d.isHoliday?'\\n🎉 '+d.holName:'')+'\\n\\nNepali Calendar 2083 → converter.thenepal.io');
  document.getElementById('s-wa').href='https://wa.me/?text='+waText;
  document.getElementById('s-conv').href='https://converter.thenepal.io/bs-to-ad/?year=2083&month='+d.monthNum+'&day='+d.bsDay;
  document.getElementById('overlay').classList.add('open');
  document.body.style.overflow='hidden';
}
function closeModal(){document.getElementById('overlay').classList.remove('open');document.body.style.overflow='';}
function closeOutside(e){if(e.target===document.getElementById('overlay'))closeModal();}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});
"""

MODAL_HTML = """
<div class="overlay" id="overlay" role="dialog" aria-modal="true" onclick="closeOutside(event)">
  <div class="sheet">
    <div class="sheet-handle"></div>
    <div class="sheet-hdr">
      <div><div class="sheet-bs" id="s-bs">—</div><span class="sheet-mne" id="s-mne">—</span></div>
      <button class="sheet-close" onclick="closeModal()" aria-label="Close">✕</button>
    </div>
    <div class="sheet-body">
      <div class="srow"><div class="srow-ico">📅</div><div><span class="srow-lbl">Gregorian (AD) Date</span><span class="srow-val" id="s-ad"></span></div></div>
      <div class="srow"><div class="srow-ico">🗓</div><div><span class="srow-lbl">Bikram Sambat (BS)</span><span class="srow-val" id="s-bs-full"></span></div></div>
      <div class="srow"><div class="srow-ico">🌙</div><div><span class="srow-lbl">Tithi (Lunar Phase)</span><span class="srow-val" id="s-tithi"></span></div></div>
      <div class="srow"><div class="srow-ico">📆</div><div><span class="srow-lbl">Day of Week</span><span class="srow-val" id="s-day"></span></div></div>
      <div id="s-hol-wrap" style="display:none"><div class="hol-badge" id="s-hol-badge"></div><p class="hol-desc-modal" id="s-hol-desc"></p></div>
      <div id="s-sat-note" class="sat-note" style="display:none">🔴 <strong>शनिबार — Saturday</strong> is Nepal's official weekly holiday.</div>
      <a class="wa-btn" id="s-wa" href="#" target="_blank" rel="noopener">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        Share on WhatsApp
      </a>
      <a class="conv-btn" id="s-conv" href="https://converter.thenepal.io/bs-to-ad/" target="_blank" rel="noopener">📅 Convert on converter.thenepal.io →</a>
      <div class="sheet-links">
        <a href="https://converter.thenepal.io/date-converter/" target="_blank" rel="noopener">🔄 Full Converter</a>
        <a href="https://converter.thenepal.io/ad-to-bs/" target="_blank" rel="noopener">📅 AD → BS</a>
        <a href="{MAIN_URL}">📅 Full 2083 Calendar</a>
      </div>
    </div>
  </div>
</div>
"""

def build_calendar_js(m):
    """Return JS that builds the calendar grid for month m."""
    hol_js = "{"
    for day, h in m['holidays'].items():
        esc = h['label'].replace("'", "\\'")
        desc_esc = h['desc'].replace("'", "\\'")
        hol_js += f"{day}:{{label:'{esc}',type:'{h['type']}',desc:'{desc_esc}'}},"
    hol_js += "}"

    adStart = m['adStartObj']
    return f"""
(function(){{
  const m={{id:'{m["id"]}',ne:'{m["ne"]}',en:'{m["en"]}',num:{m["num"]},days:{m["days"]},
    startAD:new Date({adStart[0]},{adStart[1]},{adStart[2]}),startDOW:{m["startDOW"]},
    holidays:{hol_js}}};
  const container=document.getElementById('cal-container');
  const sec=document.createElement('section');
  sec.className='cal-section';sec.id=m.id;
  const head=document.createElement('div');head.className='cal-head';
  head.innerHTML='<h2>'+m.ne+' २०८३</h2><span class="cal-head-en">'+m.en+' 2083</span><span class="cal-head-days">'+m.days+' days</span>';
  sec.appendChild(head);
  const tw=document.createElement('div');tw.className='tbl-wrap';
  const tbl=document.createElement('table');tbl.className='cal';tbl.setAttribute('role','grid');
  tbl.innerHTML='<thead><tr><th scope="col">आइत<br><small style="font-weight:400;opacity:.7;font-size:.6em">Sun</small></th><th scope="col">सोम</th><th scope="col">मंगल</th><th scope="col">बुध</th><th scope="col">बिही</th><th scope="col">शुक्र</th><th scope="col">शनि<br><small style="font-weight:400;opacity:.7;font-size:.6em;color:#FF9B9B">Off</small></th></tr></thead>';
  const tbody=document.createElement('tbody');
  const cells=[];
  for(let i=0;i<m.startDOW;i++)cells.push(null);
  for(let d=1;d<=m.days;d++)cells.push(d);
  while(cells.length%7)cells.push(null);
  for(let r=0;r<cells.length/7;r++){{
    const tr=document.createElement('tr');
    for(let c=0;c<7;c++){{
      const td=document.createElement('td');
      const bsD=cells[r*7+c];
      if(bsD===null){{td.className='empty';td.setAttribute('aria-hidden','true');}}
      else{{
        const adDate=new Date(m.startAD);adDate.setDate(m.startAD.getDate()+(bsD-1));
        const adDay=adDate.getDate();
        const adMon=adDate.toLocaleString('en-US',{{month:'short'}});
        const dow=(m.startDOW+bsD-1)%7;
        const hol=m.holidays[bsD];
        const isSat=dow===6,isSun=dow===0;
        const isHol=hol?.type==='hol',isMala=hol?.type==='mala';
        const isToday=adDate.toDateString()===TODAY.toDateString();
        const tithiIdx=(bsD-1)%15;
        const tithiStr=TITHIS[tithiIdx];
        const isPurnima=tithiIdx===14,isEkadashi=tithiIdx===10;
        td.className=[isSat?'is-sat':'',isSun?'is-sun':'',isHol?'is-hol':'',isMala?'is-mala':'',isToday?'is-today':'',isPurnima?'is-purnima':'',isEkadashi?'is-ekadashi':''].filter(Boolean).join(' ');
        td.setAttribute('role','gridcell');
        td.setAttribute('aria-label',m.ne+' '+bsD+', '+adDay+' '+adMon+(isHol?' — '+hol.label:''));
        td.innerHTML='<span class="bs-num">'+toNe(bsD)+'</span><span class="ad-num">'+adDay+' '+adMon+'</span><span class="cell-bot '+(isHol||isMala?'hol-lbl':'tithi-lbl')+'">'+(hol?.label??tithiStr)+'</span>';
        const md={{bsDay:bsD,bsDayNe:toNe(bsD),monthNe:m.ne,monthEn:m.en,monthNum:m.num,
          adStr:adDate.toLocaleDateString('en-US',{{weekday:'long',year:'numeric',month:'long',day:'numeric'}}),
          dayNe:DAY_NE[dow],dayEn:DAY_EN[dow],tithiStr,isHoliday:isHol,isSat,
          holName:hol?.label??null,holDesc:hol?.desc??null}};
        td.addEventListener('click',()=>openModal(md));
      }}
      tr.appendChild(td);
    }}
    tbody.appendChild(tr);
  }}
  tbl.appendChild(tbody);tw.appendChild(tbl);sec.appendChild(tw);
  container.appendChild(sec);
}})();
"""

def build_tithi_table(m):
    """Build a detailed day-by-day reference table for the month."""
    from datetime import date, timedelta
    TITHIS_PY = ['प्रतिपदा','द्वितीया','तृतीया','चतुर्थी','पञ्चमी','षष्ठी','सप्तमी','अष्टमी','नवमी','दशमी','एकादशी','द्वादशी','त्रयोदशी','चतुर्दशी','पूर्णिमा / औँसी']
    DAY_EN_PY  = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    DAY_NE_PY  = ['आइत','सोम','मंगल','बुध','बिही','शुक्र','शनि']
    NE_D       = ['०','१','२','३','४','५','६','७','८','९']
    toNe_py    = lambda n: ''.join(NE_D[int(d)] for d in str(n))

    adStart = m['adStartObj']
    base = date(adStart[0], adStart[1]+1 if adStart[1] < 12 else 1, adStart[2])
    # Python months are 1-indexed; adStartObj uses 0-indexed months like JS
    base = date(adStart[0], adStart[1]+1, adStart[2])

    rows = ""
    for day in range(1, m['days']+1):
        ad = base + timedelta(days=day-1)
        dow = (m['startDOW'] + day - 1) % 7
        tithi_idx = (day-1) % 15
        tithi = TITHIS_PY[tithi_idx]
        hol = m['holidays'].get(day)
        is_sat = dow == 6
        is_purnima = tithi_idx == 14
        is_ekadashi = tithi_idx == 10

        day_cls = "sat-cell" if is_sat else ""
        tithi_cls = "purnima-cell" if is_purnima else ""
        hol_cls = "hol-cell" if hol and hol['type']=='hol' else ""
        hol_icon = "🔴 " if hol and hol['type']=='hol' else ("🌙 " if hol and hol['type']=='mala' else "")
        hol_txt  = hol['label'] if hol else ("🌕 Purnima" if is_purnima else ("🌓 Ekadashi" if is_ekadashi else "—"))

        rows += f"""<tr>
          <td>{toNe_py(day)} ({day})</td>
          <td class="{day_cls}">{DAY_NE_PY[dow]} <small style="color:var(--ink3)">({DAY_EN_PY[dow]})</small>{'<br><small style="color:var(--red)">Off</small>' if is_sat else ''}</td>
          <td>{ad.strftime('%b %d, %Y')}</td>
          <td class="{tithi_cls}">{tithi}</td>
          <td class="{hol_cls}">{hol_icon}{hol_txt}</td>
        </tr>"""
    return f"""
<div class="tbl-wrap" style="margin-bottom:24px">
<table class="tithi-table">
  <thead><tr>
    <th>BS Date</th><th>Weekday</th><th>AD Date</th><th>Tithi</th><th>Event / Holiday</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
</div>"""

def build_month_nav(current_id):
    links = ""
    for m in MONTHS:
        cls = "mnav-btn active" if m['id']==current_id else "mnav-btn"
        links += f'<a href="{BASE}/{m["slug"]}/" class="{cls}">{m["ne"]}</a>\n'
    return links

def build_month_cards(current_id):
    cards = ""
    for m in MONTHS:
        cls = "mnc current" if m['id']==current_id else "mnc"
        cards += f'<a href="{BASE}/{m["slug"]}/" class="{cls}"><span class="mnc-ne">{m["ne"]}</span><span class="mnc-en">{m["en"]} 2083</span><span class="mnc-days">{m["days"]} days</span></a>\n'
    return cards

def build_events_schema(m):
    if not m['events']:
        return ""
    evs = []
    for e in m['events']:
        evs.append(f'{{"@type":"Event","name":"{e["name"]}","startDate":"{e["date"]}","description":"{e["desc"]}","location":{{"@type":"Country","name":"Nepal"}}}}')
    return ",\n".join(evs) + ","

def build_faq_schema(m):
    items = []
    for f in m['faqs']:
        q = f['q'].replace('"','\\"')
        a = f['a'].replace('"','\\"')
        items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    return ",\n".join(items)

def build_hol_cards(m):
    if not m['holidays']:
        return '<p style="color:var(--ink3);font-size:.85rem">No major public holidays this month. Every Saturday is Nepal\'s weekly holiday.</p>'
    cards = ""
    for day, h in m['holidays'].items():
        NE_D = ['०','१','२','३','४','५','६','७','८','९']
        toNe_py = lambda n: ''.join(NE_D[int(d)] for d in str(n))
        cls = "gold" if h['type']=='mala' else ""
        tag_cls = "week" if h['type']=='mala' else "nat"
        tag_txt = "Adhik Maas" if h['type']=='mala' else "National Holiday"
        cards += f"""
<div class="hol-card {cls}">
  <div class="hol-dblk">
    <div class="hol-bsn">{toNe_py(day)}</div>
    <div class="hol-mne">{m['ne']}</div>
  </div>
  <div>
    <div class="hol-nm">{h['label']}</div>
    <div class="hol-ad">{h['adDate']} · {h['dayEn']}</div>
    <div class="hol-desc-txt">{h['desc']}</div>
    <span class="tag {tag_cls}">{tag_txt}</span>
  </div>
</div>"""
    return cards

def build_aus_cards(m):
    if not m['aus']:
        return '<p style="color:var(--ink3);font-size:.85rem">No specific auspicious dates listed for this month. Verify with official NPNS Panchanga.</p>'
    cards = ""
    for a in m['aus']:
        is_mala = "No Sait" in a['type'] or "Mala" in a['type']
        cls = "mala" if is_mala else ""
        cards += f'<div class="aus-card {cls}"><div class="aus-type">{a["type"]}</div><span class="aus-ne">{a["ne"]}</span><div class="aus-ad">{a["ad"]}</div></div>'
    return cards

def build_faqs_html(m):
    html = ""
    for f in m['faqs']:
        html += f"""
<div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
  <button class="faq-q" onclick="toggleFaq(this)" aria-expanded="false">
    <span itemprop="name">{f['q']}</span><span class="faq-arrow">▼</span>
  </button>
  <div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
    <span itemprop="text">{f['a']}</span>
  </div>
</div>"""
    return html

def build_prev_next(m):
    prev_m = next((x for x in MONTHS if x['id']==m['prev']), None) if m['prev'] else None
    next_m = next((x for x in MONTHS if x['id']==m['next_']), None) if m['next_'] else None
    html = '<div class="pn-nav">'
    if prev_m:
        html += f'<a class="pn-btn" href="{BASE}/{prev_m["slug"]}/"><span class="pn-arrow">←</span><div><span class="pn-label">Previous Month</span><span class="pn-ne">{prev_m["ne"]}</span><span class="pn-en">{prev_m["en"]} 2083</span></div></a>'
    else:
        html += '<div></div>'
    if next_m:
        html += f'<a class="pn-btn next" href="{BASE}/{next_m["slug"]}/"><div><span class="pn-label">Next Month</span><span class="pn-ne">{next_m["ne"]}</span><span class="pn-en">{next_m["en"]} 2083</span></div><span class="pn-arrow">→</span></a>'
    html += '</div>'
    return html

# ── Generate each month page ─────────────────────────────────────────────
for m in MONTHS:
    events_schema = build_events_schema(m)
    faq_schema    = build_faq_schema(m)
    note_html = ""
    if m.get('note'):
        note_html = f'<div class="notice mala"><div class="notice-ico">🌙</div><div><strong>{m["note"]}</strong></div></div>'

    mala_notice = ""
    if m['id'] == 'jestha':
        mala_notice = '''<div class="notice mala"><div class="notice-ico">🌙</div><div><strong>Mala Maas Begins — Jestha 3 (May 17, 2026)</strong><p>Adhik Maas starts this month and runs until Ashadh 1 (Jun 15, 2026). <strong>No auspicious marriage or Bratabandha dates</strong> from Jestha 3 onward. Major festivals shift ~30 days later. <a href="https://converter.thenepal.io/date-converter/" target="_blank" rel="noopener">Verify any date →</a></p></div></div>'''
    elif m['id'] == 'ashadh':
        mala_notice = '''<div class="notice green"><div class="notice-ico">✅</div><div><strong>Mala Maas Ended — Ashadh 1 (June 15, 2026)</strong><p>Regular calendar resumes. Auspicious dates can now be observed. AD dates in this and subsequent months are ~30 days later than a normal year.</p></div></div>'''

    html = f"""<!DOCTYPE html>
<html lang="ne" prefix="og: https://ogp.me/ns#">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{m['en']} 2083 Calendar — {m['ne']} २०८३ पात्रो | Holidays, Tithi & AD Dates</title>
  <meta name="description" content="{m['desc']}"/>
  <meta name="keywords" content="{m['keywords']}"/>
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"/>
  <link rel="canonical" href="{BASE}/{m['slug']}/"/>
  <meta property="og:type" content="website"/>
  <meta property="og:title" content="{m['en']} 2083 BS — {m['ne']} २०८३ | Holidays, Tithi &amp; AD Dates"/>
  <meta property="og:description" content="{m['desc']}"/>
  <meta property="og:url" content="{BASE}/{m['slug']}/"/>
  <meta property="og:locale" content="ne_NP"/>
  <meta property="og:site_name" content="TheNepal.io"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{m['en']} 2083 Calendar | {m['ne']} २०८३ पात्रो"/>
  <meta name="twitter:description" content="{m['desc']}"/>

  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@graph":[
      {{"@type":"WebPage",
        "@id":"{BASE}/{m['slug']}/",
        "url":"{BASE}/{m['slug']}/",
        "name":"{m['en']} 2083 BS — {m['ne']} २०८३ Calendar",
        "description":"{m['desc']}",
        "inLanguage":["ne","en"],
        "isPartOf":{{"@id":"{BASE}/"}},
        "breadcrumb":{{"@type":"BreadcrumbList","itemListElement":[
          {{"@type":"ListItem","position":1,"name":"Home","item":"https://thenepal.io/"}},
          {{"@type":"ListItem","position":2,"name":"Nepali Calendar 2083","item":"{BASE}/"}},
          {{"@type":"ListItem","position":3,"name":"{m['en']} 2083","item":"{BASE}/{m['slug']}/"}}
        ]}}
      }},
      {events_schema}
      {{"@type":"FAQPage","mainEntity":[{faq_schema}]}}
    ]
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Tiro+Devanagari+Hindi:ital@0;1&family=Playfair+Display:ital,wght@0,600;0,700;1,600&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1239173186536702" crossorigin="anonymous"></script>
  <style>{SHARED_CSS}</style>
</head>
<body>

<div id="header"></div>

<!-- STICKY NAV -->
<nav class="month-nav" aria-label="Calendar navigation">
  <a class="mnav-home" href="{BASE}/">२०८३ ▸</a>
  {build_month_nav(m['id'])}
</nav>

<!-- HERO -->
<header class="hero">
  <div class="hero-ne">{m['ne']} <em>२०८३</em></div>
  <div class="hero-en">{m['en']} 2083 BS — Nepali Calendar</div>
  <div class="hero-meta">{m['adStart']} — {m['adEnd']} &bull; {m['days']} days</div>
  <div class="hero-cta">
    <a class="cta-btn" href="{BASE}/">📅 Full Year 2083</a>
    <a class="cta-btn ghost" href="https://converter.thenepal.io/bs-to-ad/?year=2083&month={m['num']}&day=1" target="_blank" rel="noopener">🔄 BS → AD Converter</a>
  </div>
</header>

<!-- TOP AD -->
<div class="ad-slot">
  <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1239173186536702" data-ad-slot="1642070334" data-ad-format="auto" data-full-width-responsive="true"></ins>
  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
</div>

<!-- BREADCRUMB -->
<nav class="bc" aria-label="Breadcrumb">
  <a href="https://thenepal.io/">Home</a><span>›</span>
  <a href="https://converter.thenepal.io/">Tools</a><span>›</span>
  <a href="{BASE}/">Nepali Calendar 2083</a><span>›</span>
  <span>{m['en']} 2083</span>
</nav>

<div class="wrap">

  <!-- INTRO / H1 -->
  <div class="intro-box">
    <h1>{m['en']} 2083 BS — {m['ne']} २०८३ पात्रो | Holidays, Tithi &amp; AD Dates</h1>
    <p>{m['intro_en']}</p>
    <p><strong>नेपालीमा:</strong> {m['intro_ne']}</p>
    <p>Click any date in the calendar below for full details, Tithi, and a WhatsApp share link. Use <a href="https://converter.thenepal.io/bs-to-ad/?year=2083&month={m['num']}&day=1" target="_blank" rel="noopener">converter.thenepal.io</a> to convert any {m['en']} 2083 date to AD.</p>
  </div>

  {mala_notice}
  {note_html}

  <!-- HOLIDAYS -->
  <h2 class="sec-head">🎉 Holidays in {m['en']} 2083</h2>
  <div class="hol-grid">{build_hol_cards(m)}</div>

  <!-- CALENDAR -->
  <h2 class="sec-head">📅 {m['en']} 2083 Calendar Grid</h2>
  <div id="cal-container"></div>

  <!-- MID AD -->
  <div class="ad-slot" style="padding:0;margin:12px 0">
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1239173186536702" data-ad-slot="2045458610" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>

  <!-- FULL TITHI TABLE -->
  <h2 class="sec-head">🌙 Full Day-by-Day Tithi Table — {m['en']} 2083</h2>
  {build_tithi_table(m)}

  <!-- AUSPICIOUS DATES -->
  <h2 class="sec-head">💍 Auspicious Dates (शुभ साइत) — {m['en']} 2083</h2>
  <div class="aus-grid">{build_aus_cards(m)}</div>

  <!-- LEGEND -->
  <div class="legend">
    <div class="leg"><div class="leg-dot" style="background:var(--red-lt);border:1px solid var(--red)"></div>Public Holiday</div>
    <div class="leg"><div class="leg-dot" style="background:#FFF7F6;border:1px solid var(--sat)"></div>Saturday (Off)</div>
    <div class="leg"><div class="leg-dot" style="background:#EDF4FF;border:1px solid var(--sun)"></div>Sunday</div>
    <div class="leg"><div class="leg-dot" style="border:2.5px solid var(--gold);background:transparent"></div>Today</div>
    <div class="leg"><span style="font-size:.8rem">🌕</span> Purnima</div>
    <div class="leg"><span style="font-size:.8rem">🌓</span> Ekadashi</div>
    <div class="leg"><span style="font-size:.8rem">👆</span> Tap for details</div>
  </div>

  <!-- FAQ -->
  <h2 class="sec-head">❓ {m['en']} 2083 — Frequently Asked Questions</h2>
  <div class="faq-list" itemscope itemtype="https://schema.org/FAQPage">
    {build_faqs_html(m)}
  </div>

  <!-- ALL MONTHS NAV -->
  <h2 class="sec-head">📅 All Months — Nepali Calendar 2083 BS</h2>
  <div class="month-nav-cards">{build_month_cards(m['id'])}</div>

  <!-- PREV / NEXT -->
  {build_prev_next(m)}

  <!-- BOTTOM AD -->
  <div class="ad-slot" style="padding:0;margin:12px 0">
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1239173186536702" data-ad-slot="1642070334" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>

  <!-- FOOT NOTE -->
  <div class="foot-note">
    <strong>📌 Sources:</strong> Month data per Nepal Panchanga Nirnayak Samiti (NPNS) 2083 BS. Holidays per MoHA gazette.
    Date conversion: <a href="https://converter.thenepal.io/date-converter/" target="_blank" rel="noopener">converter.thenepal.io</a>.
    Official gazette: <a href="https://moha.gov.np" target="_blank" rel="noopener">moha.gov.np</a>.<br>
    ⚠️ <strong>Saturday is Nepal's official weekly holiday.</strong> Tithi labels are approximate — verify exact Tithis with the official NPNS Panchanga.
  </div>

</div><!-- /wrap -->

<div id="footer"></div>
<script src="/components.js"></script>

{MODAL_HTML.replace('{MAIN_URL}', BASE + '/')}

<script>
{SHARED_JS}
{build_calendar_js(m)}
</script>
</body>
</html>"""

    fpath = os.path.join(OUT, f"{m['slug']}.html")
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ {m['slug']}.html  ({len(html):,} bytes)")

print(f"\n✅ All 12 month pages generated in {OUT}")
