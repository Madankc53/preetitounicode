#!/usr/bin/env python3
"""Generate the Mangal→Preeti, Roman→Preeti and Preeti→Kalimati converter pages."""
import json, os
SITE='https://converter.thenepal.io'

CSS='''*{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#0f0e0b;--ink2:#3a3830;--muted:#6b6960;--bg:#f7f5f0;--surface:#fff;--border:#e4e1d8;--blue:#003893;--red:#C0392B;--green:#1a6e40;--r:14px}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#edeae2;--ink2:#b8b4a8;--muted:#9a9688;--bg:#111210;--surface:#1a1c18;--border:#2c2e28;--blue:#7ea6ec}}
:root[data-theme="dark"]{--ink:#edeae2;--ink2:#b8b4a8;--muted:#9a9688;--bg:#111210;--surface:#1a1c18;--border:#2c2e28;--blue:#7ea6ec}
body{font-family:Outfit,Mukta,system-ui,sans-serif;background:var(--bg);color:var(--ink);line-height:1.65}
.wrap{max-width:980px;margin:0 auto;padding:0 16px}
h1{font-size:clamp(26px,5vw,40px);line-height:1.2;margin:22px 0 6px}
.sub{color:var(--ink2);margin-bottom:16px;max-width:720px}
.crumb{font-size:12px;color:var(--muted);margin-top:14px}.crumb a{color:inherit}
.tool{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:14px;margin-bottom:22px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:720px){.grid{grid-template-columns:1fr}}
.lbl{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin-bottom:6px}
.lbl .q{margin-left:auto;display:flex;gap:6px;text-transform:none;letter-spacing:0}
textarea,.out{width:100%;min-height:190px;border:1px solid var(--border);border-radius:10px;padding:12px;font-size:17px;line-height:1.7;background:var(--bg);color:var(--ink);font-family:Mukta,"Noto Sans Devanagari",sans-serif;resize:vertical;white-space:pre-wrap;word-break:break-word;overflow:auto}
.out.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:16px}
.out.kal{font-family:Kalimati,Mukta,"Noto Sans Devanagari",sans-serif}
.btn{font:600 13px Outfit,sans-serif;border:1px solid var(--border);background:transparent;color:var(--ink);border-radius:18px;padding:7px 14px;min-height:36px;cursor:pointer}
.btn.pri{background:var(--red);border-color:var(--red);color:#fff}
.row{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;align-items:center}
.cnt{margin-left:auto;font-size:12px;color:var(--muted)}
.note{font-size:13px;color:var(--ink2);background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:9px 12px;margin-top:10px}
.note a{color:var(--blue)}
section.c{margin:26px 0}
section.c h2{font-size:22px;margin-bottom:8px}
section.c p,section.c li{color:var(--ink2);margin-bottom:8px}
section.c ol,section.c ul{padding-left:22px}
details{border:1px solid var(--border);border-radius:10px;padding:10px 14px;margin-bottom:8px;background:var(--surface)}
summary{font-weight:600;cursor:pointer}
details p{margin-top:8px}
table{border-collapse:collapse;width:100%;font-size:15px}td,th{border:1px solid var(--border);padding:6px 10px;text-align:left}
.rel{display:flex;gap:8px;flex-wrap:wrap}.rel a{border:1px solid var(--border);border-radius:18px;padding:6px 14px;text-decoration:none;color:var(--ink);font-size:14px;background:var(--surface)}
'''

COMMON_JS='''
function $(i){return document.getElementById(i)}
function toast(m){var t=$('toast');t.textContent=m;t.style.opacity=1;setTimeout(function(){t.style.opacity=0},1600)}
function copyOut(){var v=$('out').textContent;if(!v){toast('Nothing to copy');return}
 (navigator.clipboard?navigator.clipboard.writeText(v):Promise.reject()).then(function(){toast('Copied')},function(){var r=document.createRange();r.selectNodeContents($('out'));var s=getSelection();s.removeAllRanges();s.addRange(r);document.execCommand('copy');toast('Copied')})}
function pasteIn(){if(!navigator.clipboard||!navigator.clipboard.readText){$('in').focus();toast('Press Ctrl+V to paste');return}
 navigator.clipboard.readText().then(function(t){$('in').value=t;run()},function(){$('in').focus();toast('Press Ctrl+V to paste')})}
function clearAll(){$('in').value='';run();$('in').focus()}
function sample(){$('in').value=SAMPLE;run()}
function dl(){var v=$('out').textContent;if(!v)return;var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([v],{type:'text/plain;charset=utf-8'}));a.download=FILE;a.click()}
$('in').addEventListener('input',run);
(function(){var h=decodeURIComponent((location.hash||'').slice(1));if(h){try{$('in').value=h}catch(e){}}run()})();
'''

PAGES=[
dict(
 slug='mangal-to-preeti-converter',
 title='Mangal to Preeti Converter – Unicode to Preeti Font Online | TheNepal.io',
 desc='Convert Mangal (Nepali Unicode) text to Preeti font text online. Paste Unicode Nepali, copy the Preeti keystroke text and apply the Preeti font. Free, private, no sign-up.',
 h1='Mangal to Preeti Converter',
 sub='Mangal is a Unicode font. Paste your Mangal (Unicode) Nepali text and get Preeti text you can use with the Preeti font in Word, PageMaker or InDesign.',
 inlbl='Mangal / Unicode input', outlbl='Preeti output', outcls='mono',
 sample='नेपाल एक सुन्दर देश हो। संविधान, शिक्षा र स्वास्थ्य सबैका लागि।',
 scripts=['/u2p-engine.js'],
 core="var SAMPLE=%s,FILE='preeti-text.txt';\nfunction run(){var v=$('in').value;$('out').textContent=PreetiU2P.convert(v);$('cnt').textContent=v.length+' characters'}",
 note='The output looks like English letters (for example <b>नेपाल</b> becomes <code>g]kfn</code>). That is correct: it only turns into Nepali after you set the font of the pasted text to <b>Preeti</b>. <a href="/download-preeti-font">Download the Preeti font</a> if it is not installed.',
 body='''<section class="c"><h2>How to convert Mangal to Preeti</h2><ol>
<li>Paste your Mangal or any Unicode Nepali text into the left box (or press <b>Paste</b>).</li>
<li>The Preeti text appears on the right instantly. Press <b>Copy</b>.</li>
<li>In Word, PageMaker or InDesign, paste the text and change its font to <b>Preeti</b>. The Nepali letters appear.</li></ol></section>
<section class="c"><h2>Mangal, Unicode and Preeti: what is the difference?</h2>
<p><b>Mangal</b> is the default Nepali font in Windows. It is a <b>Unicode</b> font, so text typed in Mangal can be searched, copied between apps and shown on websites.</p>
<p><b>Preeti</b> is a legacy font. It stores Nepali as ordinary English keystrokes and only looks Nepali because the font draws different shapes for those keys. Many printing presses, government offices and older designs still require Preeti. This tool bridges the two.</p>
<table><tr><th>Mangal (Unicode)</th><th>Preeti text</th></tr><tr><td>नेपाल</td><td>g]kfn</td></tr><tr><td>शिक्षा</td><td>lzIff</td></tr><tr><td>संविधान</td><td>;+ljwfg</td></tr><tr><td>प्रधानमन्त्री</td><td>k|wfgdGqL</td></tr></table></section>''',
 faq=[('Is Mangal the same as Unicode?','Mangal is a font; the text you type with it is Unicode. Any Unicode Nepali text (Mangal, Kalimati, Noto Sans Devanagari and others) converts the same way.'),
      ('Why does the Preeti output look like English?','Preeti text is English keystrokes. It shows Nepali only when the Preeti font is applied to it.'),
      ('Is my text uploaded anywhere?','No. The conversion runs in your browser; nothing is sent to a server.'),
      ('Can I convert Preeti back to Unicode?','Yes, use the <a href="/preeti-to-unicode-converter/">Preeti to Unicode converter</a>.')],
 rel=[('/preeti-to-unicode-converter/','Preeti to Unicode'),('/unicode-to-preeti-converter/','Unicode to Preeti'),('/roman-to-preeti-converter/','Roman to Preeti'),('/preeti-to-kalimati-converter/','Preeti to Kalimati'),('/download-preeti-font','Download Preeti font')],
),
dict(
 slug='roman-to-preeti-converter',
 title='Roman to Preeti Converter – Type Nepali in English, Get Preeti | TheNepal.io',
 desc='Type Nepali in English letters (Roman) and get Nepali Unicode and Preeti font text instantly. Free Roman to Preeti converter, runs in your browser.',
 h1='Roman to Preeti Converter',
 sub='Type Nepali in English letters (for example <i>nepaal</i>, <i>shikshaa</i>). You get Nepali Unicode and ready-to-use Preeti text.',
 inlbl='Roman Nepali input', outlbl='Preeti output', outcls='mono',
 sample='nepaal ek sundar desh ho. sarkaar le shikshaa ra swaasthya ma dhyaan dinuparchha.',
 scripts=['/nepali-typing/engine.js','/u2p-engine.js'],
 extra_out='<div class="lbl" style="margin-top:10px">Nepali Unicode</div><div class="out" id="uni" style="min-height:70px"></div>',
 core="var SAMPLE=%s,FILE='preeti-text.txt';\nfunction run(){var v=$('in').value,u=NepaliTyping.convert(v);$('uni').textContent=u;$('out').textContent=PreetiU2P.convert(u);$('cnt').textContent=v.length+' characters'}",
 note='Roman spelling is phonetic: <code>aa</code> = आ, <code>ee</code> = ई, <code>sh</code> = श, <code>chh</code> = छ, <code>ksh</code> = क्ष, <code>gy</code> = ज्ञ, <code>M</code> = ं, and <code>{text}</code> stays as typed. The Preeti output only looks Nepali after you apply the <b>Preeti</b> font. <a href="/nepali-typing/">See the full typing scheme</a>.',
 body='''<section class="c"><h2>How to type Nepali in Preeti from English</h2><ol>
<li>Type the Nepali word in English letters. Use <code>aa</code> for the long आ sound, for example <code>nepaal</code> (नेपाल) or <code>namaste</code>.</li>
<li>Check the Nepali Unicode shown under the output. If a word is wrong, adjust the spelling (for example <code>shikshaa</code> gives शिक्षा).</li>
<li>Copy the Preeti output, paste it into Word or your publishing software and set the font to <b>Preeti</b>.</li></ol></section>
<section class="c"><h2>Why go through Unicode?</h2><p>Roman input is first converted to standard Nepali Unicode, then to Preeti. That keeps conjuncts, the short-i vowel (ि) and reph (र्) in the right place, so the Preeti text looks correct in the final document.</p>
<table><tr><th>Roman</th><th>Unicode</th><th>Preeti</th></tr><tr><td>nepaal</td><td>नेपाल</td><td>g]kfn</td></tr><tr><td>shikshaa</td><td>शिक्षा</td><td>lzIff</td></tr><tr><td>swaasthya</td><td>स्वास्थ्य</td><td>:jf:Yo</td></tr><tr><td>namaste</td><td>नमस्ते</td><td>gd:t]</td></tr></table></section>''',
 faq=[('Is Roman to Preeti accurate?','Roman Nepali spelling is ambiguous, so always check the Unicode line. Once the Unicode is right, the Preeti conversion follows fixed rules.'),
      ('Can I type in Preeti directly?','You need the Preeti font and a Preeti keyboard layout for that. This page lets you type normal English letters instead.'),
      ('Does it work offline or privately?','The conversion runs in your browser; nothing is uploaded.'),
      ('How do I get Unicode only?','Use the <a href="/nepali-typing/">Roman to Nepali typing tool</a>.')],
 rel=[('/nepali-typing/','Roman to Nepali typing'),('/unicode-to-preeti-converter/','Unicode to Preeti'),('/mangal-to-preeti-converter/','Mangal to Preeti'),('/preeti-to-unicode-converter/','Preeti to Unicode'),('/download-preeti-font','Download Preeti font')],
),
dict(
 slug='preeti-to-kalimati-converter',
 title='Preeti to Kalimati Converter – Convert Preeti to Unicode (Kalimati) | TheNepal.io',
 desc='Convert Preeti text to Kalimati. Kalimati is a Unicode font, so we convert Preeti to Nepali Unicode that you can set in Kalimati in Word. Free, private, instant.',
 h1='Preeti to Kalimati Converter',
 sub='Kalimati is a Unicode font. Paste Preeti text, get Nepali Unicode, then set the font to Kalimati (or any Unicode font) in your document.',
 inlbl='Preeti input', outlbl='Kalimati / Unicode output', outcls='kal', inclass='',
 sample='g]kfn Pp6f ;'"'"'Gb/ b]z xf] .',
 scripts=['/assets/preeti-fwd.js'],
 core="var SAMPLE=%s,FILE='kalimati-unicode.txt';\nfunction run(){var v=$('in').value;$('out').textContent=PreetiFwd.convert(v,'preeti');$('cnt').textContent=v.length+' characters'}",
 note='The box above previews your text in Kalimati if the font is installed on your device, otherwise in a similar Nepali font. The copied text is standard Unicode: in Word choose <b>Kalimati</b> from the font list. Kalimati is not distributed by this site.',
 body='''<section class="c"><h2>How to convert Preeti to Kalimati</h2><ol>
<li>Paste your Preeti text (the English-looking letters such as <code>g]kfn</code>) into the left box.</li>
<li>Press <b>Copy</b> to copy the Nepali Unicode result.</li>
<li>Paste it into Word, Google Docs or a website and choose the <b>Kalimati</b> font. Because the text is Unicode, it works with Kalimati, Mangal, Noto Sans Devanagari and other fonts.</li></ol></section>
<section class="c"><h2>Preeti vs Kalimati</h2>
<p><b>Preeti</b> is a legacy font that stores Nepali as English keystrokes. <b>Kalimati</b> is a Unicode font used by Nepali government offices and publications. There is no direct key-to-key mapping from Preeti to Kalimati; the correct way is Preeti → Unicode → Kalimati, which is exactly what this converter does.</p>
<table><tr><th>Preeti</th><th>Unicode (shown in Kalimati)</th></tr><tr><td>g]kfn</td><td>नेपाल</td></tr><tr><td>;+ljwfg</td><td>संविधान</td></tr><tr><td>jf8{</td><td>वार्ड</td></tr><tr><td>kmf]g</td><td>फोन</td></tr></table></section>''',
 faq=[('Is Kalimati a Unicode font?','Yes. Kalimati is a Unicode Nepali font, so the converted text can also be shown in any other Unicode Nepali font.'),
      ('Why is there no Kalimati-specific output?','Unicode text is independent of the font. Choose Kalimati in your editor and the same text is displayed in it.'),
      ('Where can I get the Kalimati font?','From the original font publisher or your office. This site does not host it.'),
      ('Can I convert a Word file?','Use the <a href="/preeti-to-unicode-converter/">Preeti to Unicode converter</a>, which supports .docx and .txt uploads.')],
 rel=[('/preeti-to-unicode-converter/','Preeti to Unicode'),('/preeti-to-unicode-converter/kantipur-to-unicode','Kantipur to Unicode'),('/mangal-to-preeti-converter/','Mangal to Preeti'),('/unicode-to-preeti-converter/','Unicode to Preeti'),('/preeti-unicode-guide/','Preeti & Unicode guide')],
),
]

def build(p):
    url=f"{SITE}/{p['slug']}/"
    faq=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":__import__('re').sub('<[^>]+>','',a)}} for q,a in p['faq']]
    ld=[{"@context":"https://schema.org","@type":"WebApplication","name":p['h1'],"url":url,"applicationCategory":"UtilitiesApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"description":p['desc'],"inLanguage":["en","ne"]},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},{"@type":"ListItem","position":2,"name":p['h1'],"item":url}]}]
    faqh=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in p['faq'])
    rel=''.join(f'<a href="{u}">{t}</a>' for u,t in p['rel'])
    core=p['core']%json.dumps(p['sample'],ensure_ascii=False)
    scripts=''.join(f'<script src="{s}"></script>' for s in p['scripts'])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-default.png">
<meta property="og:site_name" content="TheNepal.io">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Mukta:wght@400;600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Mukta:wght@400;600&display=swap" rel="stylesheet"></noscript>
<link rel="preload" href="/header.html" as="fetch" crossorigin>
<link rel="preload" href="/footer.html" as="fetch" crossorigin>
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<div id="header" style="min-height:61px"></div>
<main class="wrap">
<p class="crumb"><a href="/">Home</a> › {p['h1']}</p>
<h1>{p['h1']}</h1>
<p class="sub">{p['sub']}</p>
<div class="tool">
<div class="grid">
<div><div class="lbl">{p['inlbl']}<span class="q"><button class="btn pri" type="button" onclick="pasteIn()">📋 Paste</button><button class="btn" type="button" onclick="sample()">Sample</button><button class="btn" type="button" onclick="clearAll()">Clear</button></span></div>
<textarea id="in" aria-label="{p['inlbl']}" placeholder="Paste or type here" spellcheck="false"></textarea></div>
<div><div class="lbl">{p['outlbl']}<span class="q"><button class="btn pri" type="button" onclick="copyOut()">Copy</button><button class="btn" type="button" onclick="dl()">.txt</button></span></div>
<div class="out {p['outcls']}" id="out" aria-live="polite"></div>{p.get('extra_out','')}</div>
</div>
<div class="row"><span class="cnt" id="cnt"></span></div>
<p class="note">{p['note']}</p>
</div>
{p['body']}
<section class="c"><h2>Frequently asked questions</h2>{faqh}</section>
<section class="c"><h2>Related tools</h2><div class="rel">{rel}</div></section>
</main>
<div id="toast" style="position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#222;color:#fff;padding:8px 16px;border-radius:18px;font-size:13px;opacity:0;transition:opacity .2s;pointer-events:none;z-index:50"></div>
<div id="footer"></div>
{scripts}
<script>{core}{COMMON_JS}</script>
<script src="/components.js"></script>
</body>
</html>
'''
for p in PAGES:
    os.makedirs(p['slug'],exist_ok=True)
    open(f"{p['slug']}/index.html",'w',encoding='utf-8').write(build(p))
    print(p['slug'])
