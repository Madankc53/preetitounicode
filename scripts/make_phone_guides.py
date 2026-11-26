#!/usr/bin/env python3
"""Generates 4 how-to guides under /guide/ for the file tools. Reuses CSS/skeleton of guide/convert-nepali-date-of-birth-bs-to-ad.html.
Run from repo root: python3 scripts/make_phone_guides.py"""
import re, json, html
SITE = 'https://converter.thenepal.io'
TPL = open('guide/convert-nepali-date-of-birth-bs-to-ad.html', encoding='utf-8').read()
CSS = re.search(r'<style>.*?</style>', TPL, re.S).group(0)
THEME = re.search(r'<script>\n\(function\(\)\{try\{var t=localStorage.*?</script>', TPL, re.S).group(0)
FOOT = TPL[TPL.index('<!-- Footer component'):TPL.index('<script>\n/* ================= Page script')]
DATE = '2026-11-24'
esc = html.escape

def steps(items): return '<ol class="bl-steps">' + ''.join(f'<li><strong>{t}</strong>{d}</li>' for t, d in items) + '</ol>'
def table(head, rows): return '<div class="bl-tablewrap"><table class="bl-table"><thead><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'
def note(t, ok=False): return f'<div class="bl-note{" ok" if ok else ""}"><p>{t}</p></div>'
def ul(items): return '<ul class="bl-list">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def guide(g):
    slug = g['slug']; url = f'{SITE}/guide/{slug}'
    faq = g['faq']
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": g['h1'], "description": g['desc'], "datePublished": g.get("date", DATE), "dateModified": g.get("date", DATE), "inLanguage": "en", "mainEntityOfPage": url,
         "publisher": {"@type": "Organization", "name": "TheNepal.io", "url": SITE + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": g['tool_name'], "item": SITE + g['tool']}, {"@type": "ListItem", "position": 3, "name": g['crumb'], "item": url}]},
        {"@type": "HowTo", "name": g['h1'], "step": [{"@type": "HowToStep", "name": t, "text": re.sub('<[^>]+>', '', d)} for t, d in g['steps']]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in faq]}]}
    faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    rel = ''.join(f'<a href="{u}"><b>{t}</b><span>{d}</span></a>' for u, t, d in g['related'])
    jump = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in g['jump'])
    ne_steps = ''.join(f'<li>{x}</li>' for x in g['ne_steps'])
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(g['title'])}</title>
<meta name="description" content="{esc(g['desc'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#1d4ed8">
<link rel="canonical" href="{url}">
<link rel="preload" href="/header.html" as="fetch" crossorigin>
<link rel="preload" href="/footer.html" as="fetch" crossorigin>
<meta property="og:type" content="article">
<meta property="og:site_name" content="TheNepal.io">
<meta property="og:title" content="{esc(g['h1'])}">
<meta property="og:description" content="{esc(g['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/assets/og-default.png">
{THEME}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{CSS}
<style>.bl-nepali{{margin-top:34px;padding:18px;border:1px solid var(--bl-bd);border-radius:16px;background:var(--bl-card);font-family:"Noto Sans Devanagari","Tiro Devanagari Hindi","Mukta",system-ui,sans-serif;line-height:1.85}}.bl-nepali h2{{margin-top:0}}</style>
</head>

<body>
<div class="bl-prog" id="bl-prog" aria-hidden="true"></div>
<div id="site-header" style="min-height:60px">
  <noscript><nav style="padding:14px 16px"><a href="/">Home</a> · <a href="/file-tools/">File tools</a> · <a href="/about">About</a></nav></noscript>
</div>

<main id="main-content" class="bl">
  <div class="bl-wrap">
    <nav class="bl-crumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li><a href="{g['tool']}">{g['tool_name']}</a></li><li aria-current="page">{g['crumb']}</li></ol></nav>
    <article>
      <header class="bl-hero">
        <span class="bl-eyebrow">Guide · {g['eyebrow']}</span>
        <h1>{g['h1']}</h1>
        <p class="bl-meta">Updated <time datetime="{g.get('date', DATE)}">{g.get('date_h', '24 November 2026')}</time> · {g['read']} min read</p>
        <div class="bl-ans"><p><strong>Short answer:</strong> {g['short']}</p></div>
        <p class="bl-ne" lang="ne">{g['ne_line']}</p>
        <div class="bl-cta"><a class="bl-btn pri" href="{g['tool']}">{g['cta']}</a><a class="bl-btn" href="#steps">See the steps</a></div>
        <ul class="bl-jump" aria-label="Jump to">{jump}</ul>
      </header>
{g['body']}
      <section class="bl-nepali" lang="ne" id="nepali"><h2>नेपालीमा छोटो गाइड</h2><ol class="bl-list">{ne_steps}</ol><p>{g['ne_note']}</p></section>
      <section class="bl-faq" id="faq" aria-labelledby="faq-h"><h2 id="faq-h">Frequently asked questions</h2>{faq_html}</section>
      <h2 id="related">Related tools and guides</h2>
      <div class="bl-rel">{rel}</div>
      <p class="bl-disc">{g['disc']}</p>
    </article>
  </div>
</main>

{FOOT}<script>
(function(){{var bar=document.getElementById('bl-prog');function prog(){{var h=document.documentElement,max=h.scrollHeight-h.clientHeight;bar.style.width=(max>0?Math.min(100,h.scrollTop/max*100):0)+'%';}}window.addEventListener('scroll',prog,{{passive:true}});window.addEventListener('resize',prog);prog();}})();
</script>
<script src="/sw-register.js" defer></script>
</body>
</html>
'''
    import os
    open(f'guide/{slug}.html', 'w', encoding='utf-8').write(out)

DISC = 'This guide gives general information. Upload rules differ between websites, so always follow the size, format and file-type limits written on the form or notice you are filling in.'
TOOLS_REL = [('/file-tools/', 'All file tools', 'Free, private, in your browser')]

G = []
# ---------- 1. reduce photo size ----------
G.append(dict(slug='reduce-photo-size-to-50kb-100kb', title='How to Reduce Photo Size to 50 KB or 100 KB on Your Phone (Free)',
 desc='Step-by-step: reduce a photo to 50 KB, 100 KB or 200 KB on your phone for an online form. Free, private, no app, and what to do if it is still too big.',
 h1='How to Reduce Photo Size to 50 KB or 100 KB on Your Phone', crumb='Reduce photo size to KB', eyebrow='Photos', read=5,
 tool='/image-compressor/', tool_name='Image Compressor', cta='Open the Image Compressor',
 short='open the <a href="/image-compressor/">Image Compressor</a>, add your photo, choose <strong>50 KB</strong> or <strong>100 KB</strong>, wait a moment and download the result. It works in your phone browser, needs no app, and your photo is never uploaded.',
 ne_line='फारममा फोटो ५० KB वा १०० KB भन्दा कम चाहिएको छ? Image Compressor खोल्नुहोस्, फोटो थप्नुहोस्, सीमा छान्नुहोस् र डाउनलोड गर्नुहोस्। फोटो इन्टरनेटमा अपलोड हुँदैन।',
 jump=[('why', 'Why photos are big'), ('steps', 'Steps'), ('still', 'Still too big?'), ('mistakes', 'Mistakes'), ('faq', 'FAQ')],
 steps=[('Open the Image Compressor', 'Go to the <a href="/image-compressor/">Image Compressor</a> in your phone browser (Chrome, Safari or any other).'),
        ('Add your photo', 'Tap <em>Choose images</em> to pick from your gallery, or <em>Take photo</em> to use the camera. You can add several photos at once.'),
        ('Choose the size limit', 'Tap the limit your form asks for: 20, 50, 100, 200 or 500 KB, 1 MB, or type your own number.'),
        ('Check the result', 'The new size appears next to the old one. Tap <em>Compare</em> and drag the slider to see before and after.'),
        ('Download and upload', 'Tap <em>Download</em> and attach the new file to your form. For several photos, use <em>Download all (ZIP)</em>.')],
 body='''      <h2 id="why">Why a phone photo is so big</h2>
      <p>A modern phone camera takes pictures with many millions of pixels, so one photo is often 2 to 6 MB. An online form that allows only 100 KB is asking for a file roughly 20 to 60 times smaller. Two things make a file smaller: <strong>lower image quality</strong> (more compression) and <strong>fewer pixels</strong> (a smaller picture). The compressor adjusts both automatically until the file fits.</p>
      <h2 id="steps">How to reduce a photo to 50 KB or 100 KB, step by step</h2>
      ''' + steps([('Open the Image Compressor', 'Go to the <a href="/image-compressor/">Image Compressor</a> in your phone browser.'), ('Add your photo', 'Tap <em>Choose images</em> to pick from your gallery, or <em>Take photo</em> to use the camera.'), ('Choose the size limit', 'Tap 20, 50, 100, 200 or 500 KB, 1 MB, or type your own number.'), ('Check the result', 'The new size appears beside the old one. Tap <em>Compare</em> and drag the slider to see before and after.'), ('Download and upload', 'Tap <em>Download</em> and attach the new file to your form.')]) + '''
      ''' + note('<strong>Private by design.</strong> The photo is compressed inside your browser. It is not sent to any server, so it is safe to use for ID photos, certificates and signatures.', True) + '''
      <h2 id="still">What if the photo is still too big or looks bad?</h2>
      ''' + ul(['<strong>Choose a larger limit</strong> if the form allows it. A 100 KB photo is much sharper than a 20 KB one.', '<strong>Keep &ldquo;Reduce dimensions if needed&rdquo; on.</strong> Very small limits are only possible with a smaller picture. Turn it off only if the form demands the original pixel size.', '<strong>Need an exact pixel size too?</strong> Use the <a href="/photo-resizer/">Photo &amp; Signature Resizer</a>, which sets width, height and maximum KB together.', '<strong>Crop first.</strong> A tight crop around the face or document leaves fewer pixels to compress, so quality stays higher at the same size.', '<strong>Use good light.</strong> Noisy, dark photos compress badly and end up blurrier at the same file size.']) + '''
      <h2 id="sizes">Typical limits and what to expect</h2>
      <p>These are common examples only. Your form sets the real limit.</p>
      ''' + table(['Limit', 'Result', 'Good for'], [['20 KB', 'Small picture, visible softness', 'Signatures, tiny thumbnails'], ['50 KB', 'Clear at passport-photo size', 'Small photo fields'], ['100 KB', 'Sharp for most faces and text', 'Photos and ID scans'], ['200 KB', 'Very good quality', 'Photos with fine detail'], ['500 KB to 1 MB', 'Near original quality', 'Full-page document photos']]) + '''
      <h2 id="mistakes">Common mistakes to avoid</h2>
      ''' + ul(['Compressing the same file again and again. Always start from the original photo, because each pass loses detail.', 'Renaming a PNG to .jpg. Convert it properly with the <a href="/image-converter/">JPG Converter</a>.', 'Submitting without opening the result. Look at it once to make sure a face or text is still clear.', 'Taking a photo of a document at a slant or in shadow. Retake it flat and well lit before compressing.']),
 ne_steps=['<a href="/image-compressor/">Image Compressor</a> खोल्नुहोस्।', '"Choose images" थिचेर ग्यालरीबाट फोटो छान्नुहोस् वा "Take photo" बाट क्यामेरा प्रयोग गर्नुहोस्।', 'फारमले मागेको सीमा (20, 50, 100, 200 KB आदि) छान्नुहोस्।', '"Compare" ले अघि र पछि हेर्नुहोस्, अनि "Download" थिच्नुहोस्।'],
 ne_note='सानो सीमा राख्दा फोटोको स्पष्टता घट्छ, त्यसैले डाउनलोड गरेपछि फोटो हेर्नुहोस्। पिक्सेल साइज पनि चाहिएमा <a href="/photo-resizer/">फोटो र हस्ताक्षर साइज</a> टुल प्रयोग गर्नुहोस्।',
 faq=[('How do I reduce a photo to 100 KB on my phone?', 'Open the Image Compressor in your phone browser, add the photo, tap 100 KB and download the result. It takes a few seconds and needs no app.'),
      ('How do I reduce a photo to 50 KB?', 'Do the same but tap 50 KB. If the picture looks too soft, try 100 KB or crop the photo first.'),
      ('Is it safe to compress my ID or certificate photo here?', 'Yes. The tool works inside your browser and does not upload the file, so the image stays on your device.'),
      ('Why is my compressed photo smaller in pixels?', 'To reach a very small limit the tool may shrink the picture as well as the quality. Turn off the reduce-dimensions option if the form needs the original pixel size.'),
      ('Can I compress many photos at once?', 'Yes. Add several photos, they are all reduced to the same limit, and you can download them together as a ZIP.'),
      ('My iPhone photo will not open in the tool. What do I do?', 'Some iPhones save photos as HEIC. Change Settings, Camera, Formats to Most Compatible so new photos save as JPG, or share the photo as JPG before adding it.')],
 related=[('/image-compressor/', 'Image Compressor', 'The tool this guide uses'), ('/photo-resizer/', 'Photo &amp; Signature Resizer', 'Exact pixels and maximum KB'), ('/guide/make-pdf-from-photos-on-phone', 'Make a PDF from photos', 'Combine photos into one PDF'), ('/image-converter/', 'JPG Converter', 'PNG or WebP to JPG'), ('/file-tools/', 'All file tools', 'Free, private, in your browser')], disc=DISC))
# ---------- 2. PDF from photos ----------
G.append(dict(slug='make-pdf-from-photos-on-phone', title='How to Make a PDF From Photos on Your Phone (Free, No App)',
 desc='Make one PDF from several photos or scans on your phone. Reorder, rotate, choose A4 and shrink the file for upload limits. Free, no app, nothing uploaded.',
 h1='How to Make a PDF From Photos on Your Phone', crumb='Make a PDF from photos', eyebrow='PDF', read=5,
 tool='/jpg-to-pdf/', tool_name='JPG to PDF', cta='Open JPG to PDF',
 short='open <a href="/jpg-to-pdf/">JPG to PDF</a>, add your photos, put them in order, choose <strong>A4</strong> and tap <strong>Create PDF</strong>. Pick <em>Small</em> quality if the form has a size limit. It runs in your browser and nothing is uploaded.',
 ne_line='धेरै फोटो वा स्क्यानबाट एउटै PDF चाहिएको छ? JPG to PDF खोल्नुहोस्, फोटो थप्नुहोस्, क्रम मिलाउनुहोस् र "Create PDF" थिच्नुहोस्।',
 jump=[('before', 'Before you start'), ('steps', 'Steps'), ('size', 'Make it smaller'), ('mistakes', 'Mistakes'), ('faq', 'FAQ')],
 steps=[('Photograph each page flat and well lit', 'Place the document on a plain surface, hold the phone straight above it and avoid shadows.'),
        ('Open JPG to PDF', 'Go to <a href="/jpg-to-pdf/">JPG to PDF</a> and tap <em>Choose files</em>. Select all the photos at once.'),
        ('Put the pages in order', 'Use the arrow buttons to move pages, <em>Rotate</em> for sideways pictures and <em>Remove</em> for extras.'),
        ('Choose page size, margin and quality', 'Pick <em>A4</em> for most forms, a <em>Small</em> margin, and <em>Balanced</em> quality, or <em>Small</em> for tight limits.'),
        ('Create and download', 'Tap <em>Create PDF</em>. The page count and file size appear, then tap <em>Download PDF</em>.')],
 body='''      <h2 id="before">Before you start: take clean photos</h2>
      <p>A PDF is only as clear as the photos inside it. A few seconds of care at this stage makes a neat document:</p>
      ''' + ul(['Put the paper on a dark, plain surface and use daylight or a lamp from the side to avoid your own shadow.', 'Hold the phone straight above the page so the edges are square, and let the whole page fit with a small border.', 'Take one photo per page, in reading order, so they land in the gallery in the right sequence.']) + '''
      <h2 id="steps">How to make a PDF from photos, step by step</h2>
      ''' + steps([('Open JPG to PDF', 'Go to <a href="/jpg-to-pdf/">JPG to PDF</a> and tap <em>Choose files</em>. Select all the photos at once.'), ('Put the pages in order', 'Use the arrow buttons to move pages, <em>Rotate</em> for sideways pictures and <em>Remove</em> for extras.'), ('Choose page size, margin and quality', 'Pick <em>A4</em> for most forms, a <em>Small</em> margin, and <em>Balanced</em> quality, or <em>Small</em> for tight limits.'), ('Create and download', 'Tap <em>Create PDF</em>. The page count and file size appear, then tap <em>Download PDF</em>.')]) + '''
      ''' + note('<strong>Private by design.</strong> The PDF is built inside your browser. Your photos are not uploaded, which matters for citizenship, passport, bank and exam documents.', True) + '''
      <h2 id="size">How to make the PDF smaller</h2>
      <p>Many portals limit PDFs to 1 MB or 2 MB. If yours is too big:</p>
      ''' + ul(['Choose <strong>Small</strong> quality before you create the PDF.', 'Remove pages the form does not need.', 'Make sure the photos are not much larger than necessary. You can first shrink each one with the <a href="/image-compressor/">Image Compressor</a>.', 'Split the document into two PDFs if the form accepts more than one file.']) + '''
      <h2 id="pagesize">A4, Letter or same as image?</h2>
      ''' + table(['Option', 'Use it when'], [['A4', 'Most forms and offices in Nepal and across Asia and Europe'], ['Letter', 'The recipient is in the United States or Canada'], ['Same as image', 'You want no white borders, for example a long receipt']]) + '''
      <h2 id="mistakes">Common mistakes to avoid</h2>
      ''' + ul(['Pages in the wrong order. Check the numbered list before you press Create PDF.', 'Sideways pages. Use Rotate, then look at the thumbnail.', 'Cropped edges on important text. Retake the photo with a small border all round.', 'A very large PDF from full-quality photos. Use Small quality when a limit applies.']),
 ne_steps=['सबै पेजको फोटो सिधा र उज्यालोमा खिच्नुहोस्।', '<a href="/jpg-to-pdf/">JPG to PDF</a> खोलेर सबै फोटो छान्नुहोस्।', 'तीरले क्रम मिलाउनुहोस्, ढल्किएको फोटो "Rotate" ले सोझ्याउनुहोस्।', 'A4 र गुणस्तर छानेर "Create PDF" थिच्नुहोस्, अनि "Download PDF"।'],
 ne_note='अपलोड सीमा भए गुणस्तरमा "Small" छान्नुहोस्। तपाईंका कागजात इन्टरनेटमा अपलोड हुँदैनन्।',
 faq=[('How do I make a PDF from photos on my phone?', 'Open JPG to PDF in your phone browser, add the photos, arrange them, choose A4 and tap Create PDF. Then download the file.'),
      ('Can I put many photos in one PDF?', 'Yes. Each photo becomes one page, in the order shown in the list.'),
      ('How do I make the PDF under 1 MB?', 'Choose Small quality, remove unneeded pages, and shrink very large photos first with the Image Compressor.'),
      ('Will the PDF have a watermark?', 'No. Nothing is added to your file.'),
      ('Are my documents uploaded anywhere?', 'No. The PDF is created inside your browser and the photos stay on your device.'),
      ('Can I rotate a sideways photo?', 'Yes. Tap Rotate on that page and check the thumbnail before you create the PDF.')],
 related=[('/jpg-to-pdf/', 'JPG to PDF', 'The tool this guide uses'), ('/image-compressor/', 'Image Compressor', 'Shrink photos before making the PDF'), ('/guide/convert-pdf-to-jpg-on-phone', 'Convert PDF to JPG', 'The reverse: pages to images'), ('/guide/reduce-photo-size-to-50kb-100kb', 'Reduce photo size to KB', 'For photo upload limits'), ('/file-tools/', 'All file tools', 'Free, private, in your browser')], disc=DISC))
# ---------- 3. WebP to JPG ----------
G.append(dict(slug='convert-webp-to-jpg', title='How to Convert WebP to JPG (Free, No Upload, Works on Phone)',
 desc='Convert WebP images to JPG in your browser, on phone or computer. Free, no upload, many files at once, with a ZIP download. Also PNG to JPG and JPG to PNG.',
 h1='How to Convert WebP to JPG', crumb='Convert WebP to JPG', eyebrow='Images', read=4,
 tool='/image-converter/', tool_name='JPG Converter', cta='Open the JPG Converter',
 short='open the <a href="/image-converter/">JPG Converter</a>, add your WebP image, choose <strong>JPG</strong> and download the result. It works on phone and computer, handles many files at once, and nothing is uploaded.',
 ne_line='WebP फोटो JPG मा बदल्नुपर्‍यो? JPG Converter खोल्नुहोस्, फोटो थप्नुहोस्, JPG छान्नुहोस् र डाउनलोड गर्नुहोस्।',
 jump=[('what', 'What WebP is'), ('steps', 'Steps'), ('which', 'Which format?'), ('mistakes', 'Mistakes'), ('faq', 'FAQ')],
 steps=[('Open the JPG Converter', 'Go to the <a href="/image-converter/">JPG Converter</a>.'), ('Add your WebP files', 'Tap <em>Choose files</em> or drag them in. You can add many at once.'), ('Choose JPG', 'Under <em>Convert to</em>, tap <em>JPG</em>. Pick <em>High</em> quality if detail matters.'), ('Download', 'Tap <em>Download</em> beside each file, or <em>Download all (ZIP)</em>.')],
 body='''      <h2 id="what">What is WebP, and why do I need JPG?</h2>
      <p>WebP is an image format created for websites. It makes smaller files than JPG at similar quality, so many sites and some phones save pictures as <code>.webp</code>. The problem is that some forms, older programs and upload portals accept only JPG or PNG, and a WebP file is rejected or will not open.</p>
      <h2 id="steps">How to convert WebP to JPG, step by step</h2>
      ''' + steps([('Open the JPG Converter', 'Go to the <a href="/image-converter/">JPG Converter</a>.'), ('Add your WebP files', 'Tap <em>Choose files</em> or drag them in. You can add many at once.'), ('Choose JPG', 'Under <em>Convert to</em>, tap <em>JPG</em>. Pick <em>High</em> quality if detail matters.'), ('Download', 'Tap <em>Download</em> beside each file, or <em>Download all (ZIP)</em>.')]) + '''
      ''' + note('<strong>Transparent areas become white.</strong> JPG cannot store transparency, so any see-through part of a WebP or PNG is filled with white.') + '''
      <h2 id="which">JPG, PNG or WebP: which should I use?</h2>
      ''' + table(['Format', 'Best for', 'Watch out for'], [['JPG', 'Photos, and the format most forms accept', 'No transparency; slight quality loss each time it is saved'], ['PNG', 'Logos, screenshots, images with transparency', 'Larger files for photos'], ['WebP', 'Websites that want small files', 'Not accepted by every program or portal']]) + '''
      <h2 id="mistakes">Common mistakes to avoid</h2>
      ''' + ul(['Renaming <code>photo.webp</code> to <code>photo.jpg</code>. The content stays WebP, so some systems still reject it. Convert it properly.', 'Converting again and again. Each JPG save loses a little detail, so convert once from the original.', 'Forgetting the size limit. After converting, use the <a href="/image-compressor/">Image Compressor</a> if the form also limits KB.', 'Expecting transparency to survive in JPG. Choose PNG when you need it.']),
 ne_steps=['<a href="/image-converter/">JPG Converter</a> खोल्नुहोस्।', 'WebP फोटो छान्नुहोस् (धेरै एकैपटक पनि मिल्छ)।', '"Convert to" मा JPG छान्नुहोस्।', '"Download" वा "Download all (ZIP)" थिच्नुहोस्।'],
 ne_note='फाइलको नाम .webp बाट .jpg मा फेर्दैमा फर्म्याट बदलिँदैन; टुलबाट नै बदल्नुहोस्। JPG मा पारदर्शी भाग सेतो हुन्छ।',
 faq=[('How do I convert WebP to JPG on my phone?', 'Open the JPG Converter in your phone browser, add the WebP image, choose JPG and download. No app is needed.'),
      ('Is converting WebP to JPG free and private?', 'Yes. It is free, and the conversion happens in your browser, so the image is not uploaded.'),
      ('Can I convert PNG to JPG too?', 'Yes. Add PNG files and choose JPG. You can also convert JPG to PNG or WebP.'),
      ('Will I lose quality?', 'JPG is a lossy format, so a tiny amount of detail can be lost. Choose High quality to keep it very close to the original.'),
      ('Why does my form reject a renamed .jpg file?', 'The file inside is still WebP. Convert it with the tool so the content really becomes JPG.'),
      ('Can I convert many images at once?', 'Yes. Add them all and download them one by one or as a ZIP.')],
 related=[('/image-converter/', 'JPG Converter', 'The tool this guide uses'), ('/image-compressor/', 'Image Compressor', 'Set a maximum KB after converting'), ('/guide/reduce-photo-size-to-50kb-100kb', 'Reduce photo size to KB', 'For photo upload limits'), ('/guide/make-pdf-from-photos-on-phone', 'Make a PDF from photos', 'Images into one PDF'), ('/file-tools/', 'All file tools', 'Free, private, in your browser')], disc=DISC))
# ---------- 4. PDF to JPG ----------
G.append(dict(slug='convert-pdf-to-jpg-on-phone', title='How to Convert a PDF to JPG on Your Phone or Computer (Free)',
 desc='Convert PDF pages to JPG images on your phone or computer. Choose pages and quality, download one by one or as a ZIP. Free, no upload, password PDFs supported.',
 h1='How to Convert a PDF to JPG on Your Phone or Computer', crumb='Convert PDF to JPG', eyebrow='PDF', read=4,
 tool='/pdf-to-jpg/', tool_name='PDF to JPG', cta='Open PDF to JPG',
 short='open <a href="/pdf-to-jpg/">PDF to JPG</a>, add your PDF, choose the quality and the pages you want, then tap <strong>Convert</strong>. Download each page as a JPG, or all of them as a ZIP. Nothing is uploaded.',
 ne_line='PDF का पेजलाई फोटो (JPG) बनाउनुपर्‍यो? PDF to JPG खोल्नुहोस्, PDF छान्नुहोस्, गुणस्तर छान्नुहोस् र "Convert" थिच्नुहोस्।',
 jump=[('when', 'When you need it'), ('steps', 'Steps'), ('quality', 'Choosing quality'), ('mistakes', 'Mistakes'), ('faq', 'FAQ')],
 steps=[('Open PDF to JPG', 'Go to <a href="/pdf-to-jpg/">PDF to JPG</a> and tap <em>Choose file</em>.'), ('Choose quality and format', 'Pick <em>Standard</em> for most uses, <em>High</em> for small print, and JPG or PNG.'), ('Pick the pages', 'Leave <em>Pages</em> empty for all, or type something like <code>1-3, 5</code> for only those pages.'), ('Convert and download', 'Tap <em>Convert</em>. Download each page, or tap <em>Download all (ZIP)</em>. If the PDF has a password, the tool asks for it.')],
 body='''      <h2 id="when">When do you need a PDF as images?</h2>
      <p>Some portals accept only image files, not PDFs. You may also want to share one page in a chat app, put a page in a presentation, or edit it in a photo app. Converting a PDF to JPG gives you one picture for each page.</p>
      <h2 id="steps">How to convert a PDF to JPG, step by step</h2>
      ''' + steps([('Open PDF to JPG', 'Go to <a href="/pdf-to-jpg/">PDF to JPG</a> and tap <em>Choose file</em>.'), ('Choose quality and format', 'Pick <em>Standard</em> for most uses, <em>High</em> for small print, and JPG or PNG.'), ('Pick the pages', 'Leave <em>Pages</em> empty for all, or type something like <code>1-3, 5</code> for only those pages.'), ('Convert and download', 'Tap <em>Convert</em>. Download each page, or tap <em>Download all (ZIP)</em>. If the PDF has a password, the tool asks for it.')]) + '''
      ''' + note('<strong>Private by design.</strong> Your browser opens and draws the PDF. The file is not sent to any server.', True) + '''
      <h2 id="quality">Which quality should I choose?</h2>
      ''' + table(['Quality', 'Resolution', 'Use it for'], [['Small', '96 dpi', 'Quick previews and chat sharing'], ['Standard', '150 dpi', 'Most forms, screens and email'], ['High', '220 dpi', 'Small print, zooming in, printing small']]) + '''
      <p>Higher quality means a larger file. If the image must be under a size limit, convert it and then shrink it with the <a href="/image-compressor/">Image Compressor</a>.</p>
      <h2 id="mistakes">Common mistakes to avoid</h2>
      ''' + ul(['Converting a huge PDF on an old phone. Pick only the pages you need, or use the Small quality.', 'Forgetting the password. A protected PDF cannot be opened without it.', 'Expecting editable text. The result is a picture of the page, not text you can edit.', 'Choosing PNG for photos. PNG files are larger, so JPG is usually better for scans and photos.']),
 ne_steps=['<a href="/pdf-to-jpg/">PDF to JPG</a> खोलेर PDF छान्नुहोस्।', 'गुणस्तर (Standard) र फर्म्याट (JPG) छान्नुहोस्।', 'सबै पेज चाहिँदैन भने "Pages" मा जस्तै 1-3, 5 लेख्नुहोस्।', '"Convert" थिचेर पेज एक-एक गरी वा ZIP मा डाउनलोड गर्नुहोस्।'],
 ne_note='पासवर्ड भएको PDF भए टुलले पासवर्ड सोध्छ। तपाईंको PDF इन्टरनेटमा अपलोड हुँदैन।',
 faq=[('How do I convert a PDF to JPG on my phone?', 'Open PDF to JPG in your phone browser, add the PDF, choose the quality and tap Convert. Then download each page or all pages as a ZIP.'),
      ('Can I convert only some pages?', 'Yes. Type the page numbers in the Pages box, for example 2-4 or 1, 3. Leave it empty for all pages.'),
      ('Can it open a password-protected PDF?', 'Yes, if you know the password. The tool asks for it and then converts the pages.'),
      ('Is my PDF uploaded to a server?', 'No. The conversion happens inside your browser, so the file stays on your device.'),
      ('Why is the JPG so large?', 'High quality and big pages create bigger images. Choose Standard or Small, or shrink the result with the Image Compressor.'),
      ('Is there a page limit?', 'The tool converts up to 100 pages at a time to keep your browser responsive.')],
 related=[('/pdf-to-jpg/', 'PDF to JPG', 'The tool this guide uses'), ('/jpg-to-pdf/', 'JPG to PDF', 'The reverse: images into one PDF'), ('/image-compressor/', 'Image Compressor', 'Shrink the images afterwards'), ('/guide/make-pdf-from-photos-on-phone', 'Make a PDF from photos', 'Step-by-step guide'), ('/file-tools/', 'All file tools', 'Free, private, in your browser')], disc=DISC))

G.append(dict(slug='merge-pdf-files-on-phone', date='2026-11-26', date_h='26 November 2026', title='How to Merge PDF Files Into One on Your Phone (Free, No App)',
 desc='Combine several PDF files into one on your phone or computer. Put the files in order, pick pages, and download one PDF. Free, no upload, no watermark.',
 h1='How to Merge PDF Files Into One on Your Phone', crumb='Merge PDF files', eyebrow='PDF', read=4,
 tool='/merge-pdf/', tool_name='Merge PDF', cta='Open Merge PDF',
 short='open <a href="/merge-pdf/">Merge PDF</a>, add your PDF files, put them in the right order with the arrows, then tap <strong>Merge PDFs</strong> and <strong>Download PDF</strong>. Nothing is uploaded.',
 ne_line='धेरै PDF लाई एउटै PDF बनाउनुपर्‍यो? Merge PDF खोल्नुहोस्, फाइलहरू छान्नुहोस्, क्रम मिलाउनुहोस् र "Merge PDFs" थिच्नुहोस्।',
 jump=[('when', 'When you need it'), ('steps', 'Steps'), ('size', 'Keeping the size small'), ('mistakes', 'Mistakes'), ('faq', 'FAQ')],
 steps=[('Open Merge PDF', 'Go to <a href="/merge-pdf/">Merge PDF</a> and tap <em>Choose files</em>. You can select several PDFs at once.'), ('Put the files in order', 'Use the up and down arrows. The merged PDF follows the order on screen.'), ('Choose pages if needed', 'To use only some pages of a file, type them in its <em>Pages</em> box, for example <code>1-3, 5</code>.'), ('Merge and download', 'Tap <em>Merge PDFs</em>, then <em>Download PDF</em>.')],
 body='''      <h2 id="when">When do you need to merge PDFs?</h2>
      <p>Many job, admission and bank forms accept only one PDF but ask for several documents, such as a citizenship certificate, a transcript and a photo page. Merging puts them in a single file in the order you choose.</p>
      <h2 id="steps">How to merge PDF files, step by step</h2>
      ''' + steps([('Open Merge PDF', 'Go to <a href="/merge-pdf/">Merge PDF</a> and tap <em>Choose files</em>. You can select several PDFs at once.'), ('Put the files in order', 'Use the up and down arrows. The merged PDF follows the order on screen.'), ('Choose pages if needed', 'To use only some pages of a file, type them in its <em>Pages</em> box, for example <code>1-3, 5</code>.'), ('Merge and download', 'Tap <em>Merge PDFs</em>, then <em>Download PDF</em>.')]) + '''
      ''' + note('<strong>Private by design.</strong> Your browser combines the files. They are not sent to any server.', True) + '''
      <h2 id="size">How do I keep the merged file small?</h2>
      <p>The merged file is about as large as the originals added together. If the form has an upload limit, make the parts smaller first.</p>
      ''' + ul(['Shrink photos with the <a href="/image-compressor/">Image Compressor</a> before you make PDFs.', 'Make each scan a PDF with <a href="/jpg-to-pdf/">JPG to PDF</a> and choose the Small quality.', 'Then merge the small PDFs here.']) + '''
      <h2 id="mistakes">Common mistakes to avoid</h2>
      ''' + ul(['Adding a password-protected PDF. Remove the password first, because locked files cannot be merged.', 'Wrong order. Check the numbers beside each file name before you merge.', 'Including pages you do not need. Type the pages you want in the Pages box.', 'Not opening the result. Scroll through the merged PDF once before you upload it.']),
 ne_steps=['<a href="/merge-pdf/">Merge PDF</a> खोलेर PDF फाइलहरू छान्नुहोस्।', 'तीर (↑ ↓) ले फाइलको क्रम मिलाउनुहोस्।', 'कुनै फाइलको केही पेज मात्र चाहिए "Pages" मा जस्तै 1-3, 5 लेख्नुहोस्।', '"Merge PDFs" थिचेर "Download PDF" बाट डाउनलोड गर्नुहोस्।'],
 ne_note='तपाईंका PDF इन्टरनेटमा अपलोड हुँदैनन्। पासवर्ड भएको PDF जोड्न पहिले पासवर्ड हटाउनुपर्छ।',
 faq=[('How do I merge PDF files on my phone?', 'Open Merge PDF in your phone browser, add the PDFs, put them in order and tap Merge PDFs. Then download the new PDF.'),
      ('Can I merge only some pages of a file?', 'Yes. Type the page numbers in the Pages box under that file, for example 1-3, 5. Leave it empty to use every page.'),
      ('Is my PDF uploaded to a server?', 'No. The files are combined in your browser, so they stay on your device.'),
      ('Why is the merged PDF so large?', 'It is about the sum of the original files. Make the images smaller before creating the PDFs, then merge them.'),
      ('Can I merge password-protected PDFs?', 'Not directly. Remove the password first, then add the file.'),
      ('Does merging reduce quality?', 'No. Pages are copied as they are, so text stays sharp.')],
 related=[('/merge-pdf/', 'Merge PDF', 'The tool this guide uses'), ('/split-pdf/', 'Split PDF', 'Keep or remove pages'), ('/jpg-to-pdf/', 'JPG to PDF', 'Make a PDF from photos'), ('/image-compressor/', 'Image Compressor', 'Shrink photos before you make a PDF')], disc=DISC))

G.append(dict(slug='remove-pages-from-pdf', date='2026-11-26', date_h='26 November 2026', title='How to Remove Pages from a PDF or Extract Pages (Free, No Upload)',
 desc='Delete pages from a PDF, keep only the pages you need, or save each page separately. Free in your browser on phone or computer. No upload, no watermark.',
 h1='How to Remove Pages from a PDF or Extract Pages', crumb='Remove or extract PDF pages', eyebrow='PDF', read=4,
 tool='/split-pdf/', tool_name='Split PDF', cta='Open Split PDF',
 short='open <a href="/split-pdf/">Split PDF</a>, add your PDF, choose <strong>Remove these pages</strong> or <strong>Keep only these pages</strong>, type the page numbers and tap <strong>Split PDF</strong>. Nothing is uploaded.',
 ne_line='PDF बाट पेज हटाउनुपर्‍यो वा केही पेज मात्र राख्नुपर्‍यो? Split PDF खोल्नुहोस्, PDF छान्नुहोस्, पेज नम्बर लेख्नुहोस् र "Split PDF" थिच्नुहोस्।',
 jump=[('when', 'When you need it'), ('steps', 'Steps'), ('modes', 'Which option to choose'), ('mistakes', 'Mistakes'), ('faq', 'FAQ')],
 steps=[('Open Split PDF', 'Go to <a href="/split-pdf/">Split PDF</a> and choose your PDF. The tool shows the number of pages.'), ('Choose what to do', 'Pick <em>Keep only these pages</em>, <em>Remove these pages</em> or <em>Save every page separately</em>.'), ('Type the page numbers', 'Use numbers and ranges, for example <code>1-3, 5</code>. Page 1 is the first page of the file.'), ('Split and download', 'Tap <em>Split PDF</em>, then download the new PDF or the ZIP.')],
 body='''      <h2 id="when">When do you need to remove or extract PDF pages?</h2>
      <p>A scan may contain a blank page, a wrong page or pages the form does not ask for. You may also need to send only one page of a long file. Removing or extracting pages gives you a new, shorter PDF and leaves the original unchanged.</p>
      <h2 id="steps">How to remove pages from a PDF, step by step</h2>
      ''' + steps([('Open Split PDF', 'Go to <a href="/split-pdf/">Split PDF</a> and choose your PDF. The tool shows the number of pages.'), ('Choose what to do', 'Pick <em>Keep only these pages</em>, <em>Remove these pages</em> or <em>Save every page separately</em>.'), ('Type the page numbers', 'Use numbers and ranges, for example <code>1-3, 5</code>. Page 1 is the first page of the file.'), ('Split and download', 'Tap <em>Split PDF</em>, then download the new PDF or the ZIP.')]) + '''
      ''' + note('<strong>Private by design.</strong> Your browser makes the new file. The PDF is not sent to any server.', True) + '''
      <h2 id="modes">Which option should I choose?</h2>
      ''' + table(['Option', 'What you get', 'Use it when'], [['Keep only these pages', 'One PDF with just the pages you list', 'You need page 4, or pages 2-3, from a long file'], ['Remove these pages', 'One PDF without the pages you list', 'A blank or wrong page must go'], ['Save every page separately', 'A ZIP with one PDF per page', 'Each page must be uploaded on its own']]) + '''
      <h2 id="mistakes">Common mistakes to avoid</h2>
      ''' + ul(['Counting pages wrongly. Use the page numbers shown in your PDF viewer, starting at 1.', 'Choosing Keep when you meant Remove. Keep makes a file with only the listed pages.', 'Trying a password-protected PDF. Remove the password first.', 'Not checking the result. Open the new PDF and look at every page before you upload it.']),
 ne_steps=['<a href="/split-pdf/">Split PDF</a> खोलेर PDF छान्नुहोस्।', 'पेज राख्ने, हटाउने वा हरेक पेज अलग बनाउने विकल्प छान्नुहोस्।', '"Pages" मा जस्तै 1-3, 5 लेख्नुहोस्।', '"Split PDF" थिचेर बनेको फाइल डाउनलोड गर्नुहोस्।'],
 ne_note='मूल PDF जस्ताको तस्तै रहन्छ र नयाँ फाइल मात्र बन्छ। PDF इन्टरनेटमा अपलोड हुँदैन।',
 faq=[('How do I remove a page from a PDF on my phone?', 'Open Split PDF, add the PDF, choose Remove these pages, type the page number and tap Split PDF. Then download the new PDF.'),
      ('How do I extract one page from a PDF?', 'Choose Keep only these pages and type the page number, for example 4.'),
      ('Can I save every page as a separate file?', 'Yes. Choose Save every page separately to get a ZIP with one PDF per page, up to 300 pages.'),
      ('Is my PDF uploaded to a server?', 'No. The new file is made in your browser, so the PDF stays on your device.'),
      ('Does it change my original PDF?', 'No. The original file stays as it is, and you get a new file.'),
      ('Can I do this with a password-protected PDF?', 'Not directly. Remove the password first, then add the file.')],
 related=[('/split-pdf/', 'Split PDF', 'The tool this guide uses'), ('/merge-pdf/', 'Merge PDF', 'Combine PDFs into one'), ('/pdf-to-jpg/', 'PDF to JPG', 'Turn pages into pictures'), ('/jpg-to-pdf/', 'JPG to PDF', 'Make a PDF from photos')], disc=DISC))

for g in G: guide(g)
print('guides ok', len(G))
