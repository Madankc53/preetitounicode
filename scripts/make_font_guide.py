#!/usr/bin/env python3
"""Generate /nepali-font-conversion-guide/ (hub for Preeti, Kantipur, Unicode fonts). Run from repo root."""
import json, os, re
SITE = 'https://converter.thenepal.io'
SLUG = 'nepali-font-conversion-guide'
URL = f'{SITE}/{SLUG}/'
TITLE = 'Nepali Font Converter Guide: Preeti, Kantipur, Mangal & Unicode'
DESC = 'Which Nepali font is your text in, and which converter do you need? Learn to tell Preeti, Kantipur and Unicode apart and fix common conversion problems.'
MODIFIED = '2026-11-15'

# reuse the look of the other font pages
base = open('preeti-to-kalimati-converter/index.html', encoding='utf-8').read()
CSS = re.search(r'<style>(.*?)</style>', base, re.S).group(1)
CSS += '''
.lead{font-size:18px;color:var(--ink2);max-width:760px;margin-bottom:6px}
.det textarea{min-height:120px}
.verdict{margin-top:10px;padding:12px 14px;border-radius:10px;border:1px solid var(--border);background:var(--bg);font-size:15px;color:var(--ink2)}
.verdict b{color:var(--ink)}.verdict .pv{display:block;margin-top:6px;font-size:18px;color:var(--ink);font-family:Mukta,"Noto Sans Devanagari",sans-serif}
.verdict a{color:var(--blue);font-weight:600}
.tw{overflow-x:auto;margin:6px 0 12px}.tw table{min-width:560px}
th{background:var(--bg);font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
td code,.c code{background:var(--bg);border:1px solid var(--border);border-radius:5px;padding:1px 6px;font-size:14px}
.ne-box{background:var(--surface);border:1px solid var(--border);border-left:4px solid var(--red);border-radius:10px;padding:12px 14px;font-family:Mukta,"Noto Sans Devanagari",sans-serif;font-size:17px;color:var(--ink2)}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}.toc a{border:1px solid var(--border);border-radius:18px;padding:5px 12px;font-size:13px;text-decoration:none;color:var(--ink);background:var(--surface)}
.demo{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:center;margin:10px 0}
.demo div.b{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:12px;font-size:20px}
.demo .l{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);display:block;margin-bottom:4px}
@media(max-width:600px){.demo{grid-template-columns:1fr}.demo .ar{transform:rotate(90deg);justify-self:center}}
'''

# worked examples are checked against the converter engine in tests/preeti-engine.test.cjs
EXAMPLES = [('g]kfn ;/sf/', 'नेपाल सरकार'), ('lzIff', 'शिक्षा'), ('k|wfgdGqL', 'प्रधानमन्त्री'),
            ('/fli6«o', 'राष्ट्रिय'), ('ljZjljBfno', 'विश्वविद्यालय'), ('sfo{s|d', 'कार्यक्रम'),
            ('If]q', 'क्षेत्र'), ('s]Gb|', 'केन्द्र')]

FAQ = [
 ('What is the difference between legacy Nepali fonts and Unicode?',
  'Legacy fonts such as Preeti and Kantipur store Nepali as ordinary English keystrokes and only look like Nepali when the matching font is applied. Unicode stores real Devanagari characters, so the text stays correct in any Unicode Nepali font, on any phone, website or search engine.'),
 ('How can I tell whether my text is Preeti or Kantipur?',
  'Click the text in Word and read the font name in the font box. Pasted into a plain text box, both look like English letters and symbols such as <code>];{}|</code>. Kantipur also uses a few extra symbols that Preeti does not. The detector at the top of this page gives a first guess, but the font name in the original file is the reliable answer.'),
 ('Can one tool convert every Nepali font?',
  'No. Every legacy font has its own key mapping, so each one needs its own table. This site converts Preeti and Kantipur. Fonts such as Sagarmatha and PCS Nepali are not supported here yet, and text in them is left unchanged in Word files.'),
 ('Are Mangal and Kalimati Unicode fonts?',
  'Yes. Mangal and Kalimati are Unicode Devanagari fonts, as are Noto Sans Devanagari and Nirmala UI. Text typed in them is already Unicode and needs no conversion. Use a converter only when you need the legacy Preeti form, for example for a print shop.'),
 ('Why should I convert legacy text to Unicode?',
  'Unicode text can be searched, copied, read aloud by screen readers, shown on phones without installing fonts, and indexed by Google. Legacy text appears to those systems as meaningless English letters.'),
 ('Is the conversion perfect?',
  'It is mapping-based, so common text converts reliably, but rare joined letters, unusual typing habits and mixed English text can need a manual fix. Always read names, numbers and dates against the original before you publish.'),
]

def faq_plain(a): return re.sub(r'<[^>]+>', '', a)

ld = [
 {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL,
  "mainEntityOfPage": URL, "inLanguage": "en", "dateModified": MODIFIED, "datePublished": MODIFIED,
  "author": {"@type": "Organization", "name": "TheNepal.io", "url": "https://thenepal.io/"},
  "publisher": {"@type": "Organization", "name": "TheNepal.io", "url": "https://thenepal.io/"},
  "image": f"{SITE}/assets/og-default.png"},
 {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
   {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": faq_plain(a)}} for q, a in FAQ]},
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
   {"@type": "ListItem", "position": 2, "name": "Nepali font conversion guide", "item": URL}]},
]

ex_rows = ''.join(f'<tr><td><code>{p}</code></td><td>{u}</td></tr>' for p, u in EXAMPLES)
faqh = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)

BODY = '''
<div class="tool det" id="detector">
<div class="lbl">Paste a few words and I will guess the font</div>
<textarea id="in" aria-label="Paste Nepali text to detect its font" placeholder="Paste text that looks wrong, for example: g]kfn ;/sf/" spellcheck="false"></textarea>
<div class="verdict" id="verdict" aria-live="polite">Paste at least a few words. Nothing is uploaded; the check runs in your browser.</div>
<p class="note">This is a first guess from the text alone. The font name shown in Word for the original file is the reliable answer.</p>
</div>

<nav class="toc" aria-label="On this page"><a href="#why">Legacy vs Unicode</a><a href="#choose">Which converter</a><a href="#identify">Identify the font</a><a href="#fonts">Font by font</a><a href="#examples">Examples</a><a href="#problems">Problems and fixes</a><a href="#checklist">Checklist</a><a href="#faq">FAQ</a></nav>

<section class="c" id="summary-ne"><h2>नेपालीमा छोटो सार</h2>
<div class="ne-box">Preeti, Kantipur जस्ता पुराना फन्टमा लेखिएको नेपाली पाठ वास्तवमा अंग्रेजी अक्षरको रूपमा सुरक्षित हुन्छ। Mangal, Kalimati, Noto Sans Devanagari जस्ता Unicode फन्टमा असली देवनागरी अक्षर हुन्छन्। पहिले कागजात कुन फन्टमा छ पत्ता लगाउनुहोस् (Word मा फन्टको नाम हेर्नुहोस्), त्यसपछि मिल्दो कन्भर्टर प्रयोग गर्नुहोस्, र रूपान्तरणपछि नाम, अङ्क र जोडाक्षर एकपटक पढेर जाँच्नुहोस्।</div></section>

<section class="c" id="why"><h2>Legacy fonts vs Unicode: why Nepali text breaks</h2>
<p>Old Nepali typing fonts such as <b>Preeti</b> and <b>Kantipur</b> reuse the English keyboard. When you press <code>s</code> the file stores the letter s, and the font draws it as क. Without that font installed, the same file shows plain English letters.</p>
<div class="demo"><div class="b"><span class="l">What the file stores (Preeti)</span>g]kfn ;/sf/</div><div class="ar" aria-hidden="true">→</div><div class="b"><span class="l">Unicode text</span>नेपाल सरकार</div></div>
<p><b>Unicode</b> stores the real Devanagari characters, so the text looks the same everywhere and search engines, screen readers and phones can read it. That is why government sites, forms and Google need Unicode, and why print shops that still use Preeti sometimes need the opposite direction.</p></section>

<section class="c" id="choose"><h2>Which converter should I use?</h2>
<div class="tw"><table>
<tr><th>What you have</th><th>What you want</th><th>Use this</th></tr>
<tr><td>English-looking text from a Preeti document (<code>g]kfn</code>)</td><td>Normal Nepali Unicode</td><td><a href="/preeti-to-unicode-converter/">Preeti to Unicode</a></td></tr>
<tr><td>Text with Kantipur symbols such as <code>¥</code> or <code>¨</code></td><td>Unicode</td><td><a href="/preeti-to-unicode-converter/kantipur-to-unicode">Kantipur to Unicode</a></td></tr>
<tr><td>Preeti text you want to set in Kalimati</td><td>Unicode shown in Kalimati</td><td><a href="/preeti-to-kalimati-converter/">Preeti to Kalimati</a></td></tr>
<tr><td>A Word file (.docx) in Preeti or Kantipur</td><td>Unicode .docx with formatting kept</td><td><a href="/preeti-to-unicode-converter/#word-file">Upload in the converter</a></td></tr>
<tr><td>Real Nepali (Unicode, Mangal, Kalimati)</td><td>Preeti for a printer or DTP software</td><td><a href="/unicode-to-preeti-converter/">Unicode to Preeti</a> or <a href="/mangal-to-preeti-converter/">Mangal to Preeti</a></td></tr>
<tr><td>Nepali words written in English letters (<code>namaste</code>)</td><td>Unicode or Preeti</td><td><a href="/nepali-typing/">Roman to Nepali typing</a> or <a href="/roman-to-preeti-converter/">Roman to Preeti</a></td></tr>
</table></div></section>

<section class="c" id="identify"><h2>How to tell which font your text is in</h2>
<ol>
<li><b>Check the font name in Word.</b> Click inside the text and read the font box. <i>Preeti</i> or <i>Kantipur</i> means legacy text; <i>Mangal</i>, <i>Kalimati</i>, <i>Noto Sans Devanagari</i> or <i>Nirmala UI</i> means Unicode.</li>
<li><b>Paste it into a plain text box.</b> Legacy text turns into English letters with symbols like <code>] ; { | /</code>. Unicode keeps real Devanagari letters.</li>
<li><b>Look for Kantipur symbols.</b> Characters such as <code>¥ ¨ ¬ µ Ô ‹ ›</code> appear in Kantipur text, not in Preeti.</li>
<li><b>Boxes or question marks</b> mean the right font is missing on your device, not that the text is wrong.</li>
<li><b>Use the detector above</b> for a quick guess, then confirm with a short sample in the converter.</li>
</ol></section>

<section class="c" id="fonts"><h2>Font by font: what each one is and where it falls short</h2>
<div class="tw"><table>
<tr><th>Font</th><th>Type</th><th>Convert with</th><th>Limits to know</th></tr>
<tr><td><b>Preeti</b></td><td>Legacy</td><td><a href="/preeti-to-unicode-converter/">Preeti to Unicode</a></td><td>Mapping-based. Rare joined letters and unusual typing habits may need proofreading. Plain 0&ndash;9 are letter keys in Preeti, so numbers need the &ldquo;keep digits&rdquo; option.</td></tr>
<tr><td><b>Kantipur</b></td><td>Legacy</td><td><a href="/preeti-to-unicode-converter/kantipur-to-unicode">Kantipur to Unicode</a></td><td>In this site&rsquo;s tables Kantipur matches Preeti for nearly every key, but two keys differ (<code>F</code>, <code>X</code>) and about twenty symbols exist only in Kantipur. Using the Preeti converter on Kantipur text can give a wrong ँ or ह्.</td></tr>
<tr><td><b>Sagarmatha</b></td><td>Legacy</td><td>Not supported here yet</td><td>Text in this font is left unchanged in Word files, with a note.</td></tr>
<tr><td><b>PCS Nepali</b></td><td>Legacy</td><td>Not supported here yet</td><td>Needs its own mapping table.</td></tr>
<tr><td><b>Mangal</b></td><td>Unicode</td><td>No conversion needed</td><td>Comes with Windows. Use <a href="/mangal-to-preeti-converter/">Mangal to Preeti</a> only if you need Preeti text.</td></tr>
<tr><td><b>Kalimati</b></td><td>Unicode</td><td><a href="/preeti-to-kalimati-converter/">Preeti to Kalimati</a></td><td>Convert to Unicode, then set the font to Kalimati. The font itself is not hosted here.</td></tr>
<tr><td><b>Noto Sans Devanagari, Nirmala UI</b></td><td>Unicode</td><td>No conversion needed</td><td>Good choices for web pages and phones.</td></tr>
</table></div>
<p>Two general limits apply to every legacy mapping. First, fonts with the same name from different sources can differ slightly. Second, a converter works from key tables, not meaning, so it cannot spot a typing mistake in the original.</p></section>

<section class="c" id="examples"><h2>Worked examples</h2>
<p>These are real Preeti keystrokes and the Unicode the converter produces for them. Compare them with your own text.</p>
<div class="tw"><table><tr><th>Preeti keystrokes</th><th>Unicode result</th></tr>@@EX@@</table></div>
<p>Notice the vowel sign <code>l</code> in <code>lzIff</code>: Preeti types the ि <i>before</i> the consonant, and the converter moves it to the right place. The same happens with <code>{</code> for the रेफ in <code>sfo{s|d</code>.</p>
<p>Hard letters can also be added with one click using the palette in the <a href="/preeti-to-unicode-converter/">Preeti to Unicode converter</a>.</p></section>

<section class="c" id="problems"><h2>Common problems and fixes</h2>
<details><summary>The output still looks like English letters</summary><p>Either the text is already Unicode, or the converter is set to the wrong direction. If it contains real Devanagari, you do not need Preeti to Unicode; use <a href="/unicode-to-preeti-converter/">Unicode to Preeti</a> if you need the legacy form.</p></details>
<details><summary>The output is Nepali but some letters are wrong</summary><p>Usually the wrong font was chosen. Check the font name in the original file. If the text has Kantipur-only symbols, use the <a href="/preeti-to-unicode-converter/kantipur-to-unicode">Kantipur converter</a>.</p></details>
<details><summary>A vowel sign or रेफ is on the wrong letter</summary><p>The converter reorders ि and र् automatically. If one word still comes out wrong, send it through the <a href="/contact/">contact page</a> with the original keystrokes so the mapping can be fixed.</p></details>
<details><summary>Numbers turned into joined letters</summary><p>In Preeti, plain 0&ndash;9 are letter keys (for example <code>1</code> is ज्ञ). Turn on <b>Keep 0&ndash;9 as English digits</b> in the converter if your text has ordinary numbers. Nepali digits typed with Shift (<code>!@#</code>) convert to १२३.</p></details>
<details><summary>Links and email addresses were damaged</summary><p>The Preeti converter now keeps web addresses and email addresses unchanged. Other English words inside plain text cannot be told apart from Preeti keys. For Word files, upload the .docx: only runs set in Preeti or Kantipur are converted.</p></details>
<details><summary>I see boxes or question marks after converting</summary><p>The text is correct Unicode, but your device has no font for it. In Word choose Mangal, Kalimati or Noto Sans Devanagari.</p></details>
<details><summary>Text copied from a PDF converts badly</summary><p>PDF text can lose spaces or carry its own key order. Try a short line first. Scanned PDFs are pictures and need OCR, which this site does not offer.</p></details>
<details><summary>My printer or DTP software needs Preeti</summary><p>Convert your Unicode text with <a href="/unicode-to-preeti-converter/">Unicode to Preeti</a>, then set the Preeti font in the layout program. You can <a href="/download-preeti-font.html">download the Preeti font</a> to preview it.</p></details>
</section>

<section class="c" id="checklist"><h2>Before and after you convert</h2>
<ol>
<li>Keep a copy of the original file.</li>
<li>Find the font name and pick the matching converter.</li>
<li>Convert a short sample first and compare it with the original.</li>
<li>Convert the full text or upload the .docx.</li>
<li>Set a Unicode font in the result (Mangal, Kalimati or Noto Sans Devanagari).</li>
<li>Read names, numbers, dates and joined letters once against the original.</li>
</ol></section>

<section class="c" id="faq"><h2>Frequently asked questions</h2>@@FAQ@@</section>
<section class="c"><h2>Related tools</h2><div class="rel"><a href="/preeti-to-unicode-converter/">Preeti to Unicode</a><a href="/preeti-to-unicode-converter/kantipur-to-unicode">Kantipur to Unicode</a><a href="/unicode-to-preeti-converter/">Unicode to Preeti</a><a href="/preeti-to-kalimati-converter/">Preeti to Kalimati</a><a href="/mangal-to-preeti-converter/">Mangal to Preeti</a><a href="/nepali-typing/">Roman to Nepali typing</a><a href="/preeti-unicode-guide/">Preeti to Unicode guide</a><a href="/download-preeti-font.html">Download Preeti font</a></div></section>
'''
BODY = BODY.replace('@@EX@@', ex_rows).replace('@@FAQ@@', faqh)

JS = r'''
(function(){
var COMMON=['को','मा','छ','हो','र','का','ले','लाई','पनि','यो','नेपाल','सरकार','गर्न','हुन','भएको','थियो','छन्','बाट','कि','त्यो'];
function dev(t){return (t.match(/[ऀ-ॿ]/g)||[]).length}
function letters(t){return (t.match(/[A-Za-zऀ-ॿ]/g)||[]).length}
function score(t,f){var out=PreetiFwd.convert(t,f);var w=out.split(/[\s.,।|?!]+/);var h=0;for(var i=0;i<w.length;i++)if(COMMON.indexOf(w[i])>-1)h++;return {out:out,h:h}}
function esc(s){return s.replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function run(){
 var t=document.getElementById('in').value.trim(),v=document.getElementById('verdict');
 if(t.length<6){v.innerHTML='Paste at least a few words. Nothing is uploaded; the check runs in your browser.';return}
 var L=letters(t),D=dev(t);
 if(D/Math.max(L,1)>0.5){v.innerHTML='<b>This is already Nepali Unicode.</b> No conversion is needed. If you need Preeti text for a printer, use <a href="/unicode-to-preeti-converter/">Unicode to Preeti</a>.';return}
 if(/[¥¨¬µºÂÈÎÏÔøŒœ‹›™]/.test(t)){var k=score(t,'kantipur');v.innerHTML='<b>Looks like Kantipur.</b> It contains symbols used by Kantipur. Try the <a href="/preeti-to-unicode-converter/kantipur-to-unicode">Kantipur converter</a>.<span class="pv">'+esc(k.out.slice(0,90))+'</span>';return}
 var sw=(t.toLowerCase().match(/\b(the|and|is|of|to|in|for|with|that|this|are|you|have)\b/g)||[]).length;
 if(sw>=3&&!/[\];{}|\\\[]/.test(t)){v.innerHTML='<b>This looks like English text.</b> Preeti text has many symbols such as <code>] ; { |</code>. If this is Nepali typed in English letters (like <i>namaste</i>), use <a href="/nepali-typing/">Roman to Nepali typing</a>.';return}
 var p=score(t,'preeti');
 if(p.h>=1||(/[\];{}|\[]/.test(t)&&dev(p.out)>=4)){v.innerHTML='<b>Probably Preeti'+(p.h?' (common Nepali words found after converting)':'')+'.</b> Open the <a href="/preeti-to-unicode-converter/">Preeti to Unicode converter</a> and check this preview.<span class="pv">'+esc(p.out.slice(0,90))+'</span>';return}
 v.innerHTML='<b>I cannot tell from this text.</b> Check the font name in the original file, or try a longer sample.'
}
document.getElementById('in').addEventListener('input',run);
})();
'''

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="article">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{SITE}/assets/og-default.png">
<meta property="og:site_name" content="TheNepal.io">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Mukta:wght@400;600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Mukta:wght@400;600&display=swap" rel="stylesheet"></noscript>
<link rel="preload" href="/header.html" as="fetch" crossorigin>
<link rel="preload" href="/footer.html" as="fetch" crossorigin>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<div id="header" style="min-height:61px"></div>
<main class="wrap">
<p class="crumb"><a href="/">Home</a> › Nepali font conversion guide</p>
<h1>Nepali Font Converter Guide</h1>
<p class="lead">Not sure which font your Nepali text is in, or which converter to use? Start here. Learn how Preeti, Kantipur and Unicode differ, how to recognise each, and how to fix the most common conversion problems.</p>
{BODY}
</main>
<div id="footer"></div>
<script src="/assets/preeti-fwd.js"></script>
<script>{JS}</script>
<script src="/components.js"></script>
</body>
</html>
'''
os.makedirs(SLUG, exist_ok=True)
open(f'{SLUG}/index.html', 'w', encoding='utf-8').write(html)
print(SLUG, len(html))
