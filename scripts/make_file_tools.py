#!/usr/bin/env python3
"""Generates /jpg-to-pdf/ and /pdf-to-jpg/ (client-side tools, nothing uploaded). Head/CSS reused from number-to-words/index.html.
Run from repo root: python3 scripts/make_file_tools.py"""
import re, json, os
SITE = 'https://converter.thenepal.io'
base = open('number-to-words/index.html', encoding='utf-8').read()
CSS = re.search(r'<style>.*?</style>', base, re.S).group(0)
EXTRA_CSS = '''<style>
.drop{position:relative;display:block;overflow:hidden;border:2px dashed var(--line);border-radius:14px;padding:26px 14px;text-align:center;background:var(--bg);cursor:pointer}
.drop:hover,.drop:focus-within,.drop.over{border-color:var(--red)}
.drop b{display:block;font-size:1.05rem;color:var(--ink)}.drop span{font-size:.88rem;color:var(--mute)}
.drop input{position:absolute;left:0;top:0;opacity:0;width:1px;height:1px}
.opts{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0}.opts .field{flex:1 1 150px}.opts select{width:100%}
.list{list-style:none;margin:14px 0;padding:0;display:grid;gap:8px}
.list li{display:flex;align-items:center;gap:10px;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:8px}
.list img{width:56px;height:56px;object-fit:cover;border-radius:8px;flex:none;background:var(--line)}
.list .nm{flex:1;min-width:0;font-size:.9rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--ink)}
.list button{font:inherit;font-weight:700;border:1.5px solid var(--line);background:transparent;color:var(--ink);border-radius:8px;padding:4px 9px;cursor:pointer}
.list button:hover,.list button:focus-visible{border-color:var(--red);outline:none}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin:14px 0}
.grid figure{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:8px;text-align:center}
.grid img{width:100%;height:auto;display:block;border-radius:6px}
.grid figcaption{font-size:.8rem;color:var(--mute);margin:6px 0}
.grid a{font-weight:700;font-size:.85rem}
.dl{display:inline-block;text-decoration:none}
progress{width:100%;height:10px;margin:8px 0}
</style>'''
def sub(s, **k):
    for a, b in k.items(): s = s.replace('{{%s}}' % a, b)
    return s

def page(slug, title, desc, h1, ne, eyebrow, lead, tool_html, sections, faq, scripts, js, related, app_name, app_desc):
    url = f'{SITE}/{slug}/'
    faq_ld = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in faq]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": app_name, "url": url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any (web browser)", "description": app_desc,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "NPR"}, "isAccessibleForFree": True, "inLanguage": "en"},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": app_name, "item": url}]},
        {"@type": "FAQPage", "mainEntity": faq_ld}]}
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="TheNepal.io">
<meta property="og:image" content="{SITE}/assets/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/og-default.png">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
'''
    # reuse fonts/adsense lines from base head (between ld+json and <style>)
    mid = base[base.index('<link rel="preconnect"'):base.index('<style>')]
    faq_html = ''.join(f'  <details><summary>{q}</summary><p>{a}</p></details>\n' for q, a in faq)
    rel = ''.join(f'    <a href="{h}">{t}</a>\n' for h, t in related)
    body = f'''{CSS}
{EXTRA_CSS}
<link rel="preload" href="/header.html" as="fetch" crossorigin>
<link rel="preload" href="/footer.html" as="fetch" crossorigin>
</head>
<body>
<div id="header" style="min-height:61px"></div>
<main class="page" id="main-content">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{h1}</h1>
  <p class="ne">{ne}</p>
  <p class="lead">{lead}</p>
{tool_html}
  <div class="ad">
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-1239173186536702" data-ad-slot="1642070334" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
  </div>
{sections}
  <h2>Frequently asked questions</h2>
{faq_html}  <h2>Related tools</h2>
  <div class="pills">
{rel}  </div>
</main>
<div id="footer"></div>
{scripts}
<script>
{js}
</script>
<script src="/components.js"></script>
</body>
</html>
'''
    os.makedirs(slug, exist_ok=True)
    open(f'{slug}/index.html', 'w', encoding='utf-8').write(head + mid + body)

# ---------------- JPG to PDF ----------------
J_TOOL = '''  <div class="conv">
    <label class="drop" id="drop" for="files"><input id="files" type="file" accept="image/jpeg,image/png,image/webp,image/*" multiple><b>Choose images or drop them here</b><span>JPG, JPEG, PNG or WebP. Nothing is uploaded.</span></label>
    <ul class="list" id="list" aria-live="polite"></ul>
    <div class="opts">
      <div class="field"><label for="size">Page size</label><select id="size"><option value="a4">A4</option><option value="letter">Letter</option><option value="fit">Same as image</option></select></div>
      <div class="field"><label for="mar">Margin</label><select id="mar"><option value="0">None</option><option value="18" selected>Small</option><option value="36">Large</option></select></div>
      <div class="field"><label for="qual">Quality / file size</label><select id="qual"><option value="hi">High (best quality)</option><option value="md" selected>Medium (balanced)</option><option value="lo">Small (for upload limits)</option></select></div>
    </div>
    <p><button class="btn" id="go" type="button" disabled>Create PDF</button> <button class="btn alt" id="clr" type="button" disabled>Clear all</button></p>
    <p class="status" id="msg" aria-live="polite">Add one or more images to begin.</p>
    <p id="out" hidden><a class="btn dl" id="dl" download="images.pdf">Download PDF</a> <span class="status" id="sz"></span></p>
  </div>'''
J_SECTIONS = '''  <h2>How to convert JPG to PDF</h2>
  <ol>
    <li>Choose your JPG, PNG or WebP images. You can pick several at once, or add more later.</li>
    <li>Use the arrows to put the pages in the order you want. Remove any you do not need.</li>
    <li>Pick the page size, margin and quality, then press <strong>Create PDF</strong> and download the file.</li>
  </ol>
  <p>Everything runs inside your browser. Your photos are not uploaded to any server, which matters for citizenship certificates, passports, bank KYC and other private documents.</p>
  <h2>Making a PDF small enough for a form</h2>
  <p>Many Nepali online forms, job applications and university portals set a file-size limit. Choose <strong>Small</strong> quality to shrink the PDF. The final size is shown after conversion; if it is still too large, remove a page or convert fewer images at a time.</p>
  <div class="note"><p><strong>Check the result.</strong> Open the PDF and make sure text on documents is still readable before you submit it. Use High quality for documents with small print.</p></div>'''
J_FAQ = [
 ("Is this JPG to PDF converter free?", "Yes. It is free, with no sign-up and no watermark."),
 ("Are my images uploaded anywhere?", "No. The conversion happens in your browser on your own device. The images never leave it."),
 ("Can I combine many JPG images into one PDF?", "Yes. Add as many images as you like, reorder them with the arrows, and each one becomes a page in a single PDF."),
 ("How do I make the PDF smaller?", "Choose Small quality. This reduces the image resolution and compression quality, which usually cuts the file size a lot."),
 ("Does it work on a phone?", "Yes. On Android and iPhone, tap Choose images and pick photos from your gallery or camera."),
 ("Can I convert PNG or WebP as well?", "Yes. PNG and WebP images are accepted and placed into the PDF as JPEG pages. Transparent areas become white."),
]
J_JS = r'''(function(){
  var items=[],$=function(i){return document.getElementById(i)},list=$('list'),go=$('go'),clr=$('clr'),msg=$('msg'),out=$('out'),dl=$('dl'),sz=$('sz'),drop=$('drop'),url=null;
  var Q={hi:{max:3000,q:.92},md:{max:1800,q:.75},lo:{max:1200,q:.55}};
  function kb(n){return n>1048576?(n/1048576).toFixed(2)+' MB':Math.round(n/1024)+' KB';}
  function load(f){return new Promise(function(res,rej){
    if(window.createImageBitmap){createImageBitmap(f,{imageOrientation:'from-image'}).then(res,function(){fall()});}else fall();
    function fall(){var u=URL.createObjectURL(f),im=new Image();im.onload=function(){res(im)};im.onerror=function(){rej()};im.src=u;}
  });}
  function thumb(b){var c=document.createElement('canvas'),w=b.width||b.naturalWidth,h=b.height||b.naturalHeight,s=112/Math.max(w,h);c.width=Math.max(1,Math.round(w*s));c.height=Math.max(1,Math.round(h*s));c.getContext('2d').drawImage(b,0,0,c.width,c.height);return c.toDataURL('image/jpeg',.7);}
  function render(){
    list.innerHTML='';
    items.forEach(function(it,i){
      var li=document.createElement('li');
      li.innerHTML='<img alt="" src="'+it.t+'"><span class="nm"></span><button type="button" aria-label="Move up" data-a="u" data-i="'+i+'">&uarr;</button><button type="button" aria-label="Move down" data-a="d" data-i="'+i+'">&darr;</button><button type="button" aria-label="Remove" data-a="x" data-i="'+i+'">&times;</button>';
      li.querySelector('.nm').textContent=(i+1)+'. '+it.n;list.appendChild(li);
    });
    go.disabled=clr.disabled=!items.length;
    msg.textContent=items.length?items.length+' image'+(items.length>1?'s':'')+' ready.':'Add one or more images to begin.';
  }
  async function add(files){
    msg.textContent='Reading images...';
    for(var i=0;i<files.length;i++){var f=files[i];if(!/^image\//.test(f.type)&&!/\.(jpe?g|png|webp)$/i.test(f.name))continue;
      try{var b=await load(f);items.push({n:f.name,b:b,t:thumb(b)});}catch(e){msg.textContent='Could not read '+f.name+'.';}}
    out.hidden=true;render();
  }
  $('files').addEventListener('change',function(e){add(Array.from(e.target.files));e.target.value='';});
  ['dragover','dragenter'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.add('over');});});
  ['dragleave','drop'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.remove('over');if(n==='drop'&&e.dataTransfer)add(Array.from(e.dataTransfer.files));});});
  list.addEventListener('click',function(e){var a=e.target.getAttribute&&e.target.getAttribute('data-a');if(!a)return;var i=+e.target.getAttribute('data-i');
    if(a==='x')items.splice(i,1);else if(a==='u'&&i>0){var t=items[i];items[i]=items[i-1];items[i-1]=t;}else if(a==='d'&&i<items.length-1){var t2=items[i];items[i]=items[i+1];items[i+1]=t2;}
    out.hidden=true;render();});
  clr.addEventListener('click',function(){items=[];out.hidden=true;render();});
  go.addEventListener('click',async function(){
    var J=window.jspdf&&window.jspdf.jsPDF;if(!J){msg.textContent='The PDF library did not load. Check your connection and reload.';return;}
    go.disabled=true;var size=$('size').value,m=+$('mar').value,q=Q[$('qual').value],doc=null;
    try{
      for(var i=0;i<items.length;i++){
        msg.textContent='Building page '+(i+1)+' of '+items.length+'...';await new Promise(function(r){setTimeout(r,0)});
        var b=items[i].b,w=b.width||b.naturalWidth,h=b.height||b.naturalHeight,s=Math.min(1,q.max/Math.max(w,h)),cw=Math.round(w*s),ch=Math.round(h*s);
        var c=document.createElement('canvas');c.width=cw;c.height=ch;var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,cw,ch);x.drawImage(b,0,0,cw,ch);
        var d=c.toDataURL('image/jpeg',q.q),pw,ph;
        if(size==='fit'){pw=w*.75+m*2;ph=h*.75+m*2;}else{var P=size==='a4'?[595.28,841.89]:[612,792];pw=w>h?P[1]:P[0];ph=w>h?P[0]:P[1];}
        var o=pw>ph?'l':'p';if(!doc)doc=new J({unit:'pt',format:[pw,ph],orientation:o,compress:true});else doc.addPage([pw,ph],o);
        var aw=pw-m*2,ah=ph-m*2,r=Math.min(aw/w,ah/h),iw=w*r,ih=h*r;
        doc.addImage(d,'JPEG',(pw-iw)/2,(ph-ih)/2,iw,ih,undefined,'FAST');
      }
      var blob=doc.output('blob');if(url)URL.revokeObjectURL(url);url=URL.createObjectURL(blob);dl.href=url;
      dl.download=(items.length===1?items[0].n.replace(/\.[^.]+$/,''):'images')+'.pdf';sz.textContent=items.length+' page'+(items.length>1?'s':'')+', '+kb(blob.size);out.hidden=false;msg.textContent='Done. Your PDF is ready.';
    }catch(e){msg.textContent='Something went wrong while creating the PDF. Try fewer or smaller images.';}
    go.disabled=false;
  });
  render();
})();'''
page('jpg-to-pdf', 'JPG to PDF Converter: Combine Images into One PDF (Free, No Upload)',
     'Convert JPG, PNG and WebP images to PDF free in your browser. Combine many photos into one PDF, set page size and quality, no upload, no watermark.',
     'JPG to PDF Converter', 'तस्बिरलाई PDF मा बदल्नुहोस्', 'File tool',
     'Turn photos and scans into one PDF. Reorder pages, choose A4 or Letter, and shrink the file for upload limits. It all happens in your browser.',
     J_TOOL, J_SECTIONS, J_FAQ, '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>', J_JS,
     [('/pdf-to-jpg/', 'PDF to JPG'), ('/unit-converter/', 'Unit converter'), ('/preeti-to-unicode-converter/', 'Preeti to Unicode'), ('/date-converter/', 'Date converter')],
     'JPG to PDF Converter', 'Free browser-based tool that converts JPG, PNG and WebP images into a single PDF without uploading them.')

# ---------------- PDF to JPG ----------------
P_TOOL = '''  <div class="conv">
    <label class="drop" id="drop" for="file"><input id="file" type="file" accept="application/pdf,.pdf"><b>Choose a PDF or drop it here</b><span>Nothing is uploaded. Pages are converted on your device.</span></label>
    <div class="opts">
      <div class="field"><label for="dpi">Image quality</label><select id="dpi"><option value="96">Small (96 dpi)</option><option value="150" selected>Standard (150 dpi)</option><option value="220">High (220 dpi)</option></select></div>
    </div>
    <p><button class="btn" id="go" type="button" disabled>Convert to JPG</button> <button class="btn alt" id="zip" type="button" hidden>Download all (ZIP)</button></p>
    <progress id="pr" max="1" value="0" hidden></progress>
    <p class="status" id="msg" aria-live="polite">Choose a PDF to begin.</p>
    <div class="grid" id="grid"></div>
  </div>'''
P_SECTIONS = '''  <h2>How to convert a PDF to JPG</h2>
  <ol>
    <li>Choose your PDF file.</li>
    <li>Pick the image quality. Standard (150 dpi) suits most uses; High is sharper but larger.</li>
    <li>Press <strong>Convert to JPG</strong>. Each page becomes a JPG image you can download one by one or all together as a ZIP.</li>
  </ol>
  <p>The PDF is opened and drawn by your browser, so the file is never sent to a server. That keeps documents such as certificates and bank statements private.</p>
  <div class="note"><p><strong>Large PDFs.</strong> Very long or heavy PDFs can be slow on older phones. If the page stops, try the Small quality option or split the PDF first. Password-protected PDFs cannot be opened here.</p></div>'''
P_FAQ = [
 ("Is this PDF to JPG converter free?", "Yes. It is free, needs no account and adds no watermark."),
 ("Is my PDF uploaded to a server?", "No. The PDF is read and converted in your browser, so it stays on your device."),
 ("Does it convert every page?", "Yes. Each page of the PDF becomes its own JPG image, named with the page number. The tool stops at 100 pages to keep your browser responsive."),
 ("Which quality should I choose?", "Standard (150 dpi) is good for screens and most forms. Choose High (220 dpi) if you need to zoom into small print, or Small to keep files light."),
 ("Can it open a password-protected PDF?", "No. Remove the password first, then convert the file."),
 ("Does it work on a phone?", "Yes, on current Android and iPhone browsers. Large PDFs may be slow on older phones."),
]
P_JS = r'''(function(){
  var $=function(i){return document.getElementById(i)},go=$('go'),zip=$('zip'),msg=$('msg'),grid=$('grid'),pr=$('pr'),drop=$('drop'),file=null,out=[],urls=[];
  function pick(f){if(!f)return;if(f.type!=='application/pdf'&&!/\.pdf$/i.test(f.name)){msg.textContent='Please choose a PDF file.';return;}
    file=f;go.disabled=false;zip.hidden=true;grid.innerHTML='';msg.textContent=f.name+' selected.';}
  $('file').addEventListener('change',function(e){pick(e.target.files[0]);});
  ['dragover','dragenter'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.add('over');});});
  ['dragleave','drop'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.remove('over');if(n==='drop'&&e.dataTransfer)pick(e.dataTransfer.files[0]);});});
  go.addEventListener('click',async function(){
    var L=window.pdfjsLib;if(!L){msg.textContent='The PDF library did not load. Check your connection and reload.';return;}
    L.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    go.disabled=true;zip.hidden=true;grid.innerHTML='';out=[];urls.forEach(URL.revokeObjectURL);urls=[];pr.hidden=false;pr.value=0;
    try{
      var buf=await file.arrayBuffer(),pdf=await L.getDocument({data:buf}).promise,n=Math.min(pdf.numPages,100),sc=(+$('dpi').value)/72,base=file.name.replace(/\.pdf$/i,'');
      for(var i=1;i<=n;i++){
        msg.textContent='Converting page '+i+' of '+n+(pdf.numPages>n?' (first 100 pages only)':'')+'...';
        var p=await pdf.getPage(i),vp=p.getViewport({scale:sc}),k=Math.min(1,Math.sqrt(16000000/(vp.width*vp.height)));if(k<1)vp=p.getViewport({scale:sc*k});
        var c=document.createElement('canvas');c.width=Math.floor(vp.width);c.height=Math.floor(vp.height);var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
        await p.render({canvasContext:x,viewport:vp}).promise;
        var blob=await new Promise(function(r){c.toBlob(r,'image/jpeg',.9)}),u=URL.createObjectURL(blob),nm=base+'-page-'+i+'.jpg';urls.push(u);out.push({n:nm,b:blob});
        var f=document.createElement('figure');f.innerHTML='<img alt="Page '+i+'" src="'+u+'"><figcaption>Page '+i+' · '+Math.round(blob.size/1024)+' KB</figcaption><a download="'+nm+'" href="'+u+'">Download</a>';grid.appendChild(f);
        pr.value=i/n;c.width=c.height=0;
      }
      msg.textContent='Done. '+n+' page'+(n>1?'s':'')+' converted.';zip.hidden=n<2;
    }catch(e){msg.textContent=(e&&e.name==='PasswordException')?'This PDF is password protected. Remove the password and try again.':'Could not read this PDF. It may be damaged or protected.';}
    pr.hidden=true;go.disabled=false;
  });
  zip.addEventListener('click',async function(){
    if(!window.JSZip){msg.textContent='The ZIP library did not load. Download pages one by one.';return;}
    var z=new JSZip();out.forEach(function(o){z.file(o.n,o.b);});msg.textContent='Preparing ZIP...';
    var b=await z.generateAsync({type:'blob'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=file.name.replace(/\.pdf$/i,'')+'-jpg.zip';document.body.appendChild(a);a.click();a.remove();msg.textContent='ZIP downloaded.';
  });
})();'''
page('pdf-to-jpg', 'PDF to JPG Converter: Turn PDF Pages into Images (Free, No Upload)',
     'Convert PDF pages to JPG images free in your browser. Choose quality, download each page or all as a ZIP. No upload, no sign-up, no watermark.',
     'PDF to JPG Converter', 'PDF लाई JPG मा बदल्नुहोस्', 'File tool',
     'Turn every page of a PDF into a JPG image. Pick the quality and download pages one by one or all as a ZIP. Your file stays on your device.',
     P_TOOL, P_SECTIONS, P_FAQ,
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>', P_JS,
     [('/jpg-to-pdf/', 'JPG to PDF'), ('/unit-converter/', 'Unit converter'), ('/preeti-to-unicode-converter/', 'Preeti to Unicode'), ('/date-converter/', 'Date converter')],
     'PDF to JPG Converter', 'Free browser-based tool that converts each page of a PDF into a JPG image without uploading the file.')

# ---------------- Image compressor + converter (shared JS core) ----------------
CORE = r"""
  var $=function(i){return document.getElementById(i)},drop=$('drop'),msg=$('msg'),grid=$('grid'),go=$('go'),zip=$('zip'),files=[],res=[],urls=[];
  function kb(n){return n>1048576?(n/1048576).toFixed(2)+' MB':Math.round(n/1024)+' KB';}
  function load(f){return new Promise(function(ok,bad){
    if(window.createImageBitmap){createImageBitmap(f,{imageOrientation:'from-image'}).then(ok,fall);}else fall();
    function fall(){var u=URL.createObjectURL(f),im=new Image();im.onload=function(){ok(im)};im.onerror=bad;im.src=u;}});}
  function draw(b,s,fill){var w=b.width||b.naturalWidth,h=b.height||b.naturalHeight,c=document.createElement('canvas');c.width=Math.max(1,Math.round(w*s));c.height=Math.max(1,Math.round(h*s));var x=c.getContext('2d');if(fill){x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);}x.drawImage(b,0,0,c.width,c.height);return c;}
  function toBlob(c,t,q){return new Promise(function(r){c.toBlob(r,t,q)});}
  function pick(list){files=Array.from(list).filter(function(f){return /^image\//.test(f.type)||/\.(jpe?g|png|webp|gif|bmp)$/i.test(f.name)});go.disabled=!files.length;zip.hidden=true;grid.innerHTML='';
    msg.textContent=files.length?files.length+' image'+(files.length>1?'s':'')+' selected.':'Choose one or more images to begin.';}
  $('file').addEventListener('change',function(e){pick(e.target.files);});
  ['dragover','dragenter'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.add('over');});});
  ['dragleave','drop'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.remove('over');if(n==='drop'&&e.dataTransfer)pick(e.dataTransfer.files);});});
  function card(name,blob,note){var u=URL.createObjectURL(blob);urls.push(u);var f=document.createElement('figure');f.innerHTML='<img alt="" src="'+u+'"><figcaption></figcaption><a download="'+name.replace(/"/g,'')+'" href="'+u+'">Download</a>';f.querySelector('figcaption').textContent=note;grid.appendChild(f);}
  zip.addEventListener('click',async function(){
    if(!window.JSZip){msg.textContent='The ZIP library did not load. Download files one by one.';return;}
    var z=new JSZip();res.forEach(function(o){z.file(o.n,o.b);});msg.textContent='Preparing ZIP...';
    var b=await z.generateAsync({type:'blob'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='images.zip';document.body.appendChild(a);a.click();a.remove();msg.textContent='ZIP downloaded.';});
  async function run(fn){
    go.disabled=true;zip.hidden=true;grid.innerHTML='';res=[];urls.forEach(URL.revokeObjectURL);urls=[];
    for(var i=0;i<files.length;i++){msg.textContent='Working on image '+(i+1)+' of '+files.length+'...';await new Promise(function(r){setTimeout(r,0)});
      try{var b=await load(files[i]);await fn(files[i],b);}catch(e){var p=document.createElement('p');p.className='err';p.textContent='Could not read '+files[i].name+'.';grid.appendChild(p);}}
    msg.textContent='Done. '+res.length+' image'+(res.length===1?'':'s')+' ready.';zip.hidden=res.length<2;go.disabled=false;}
"""
C_TOOL = """  <div class="conv">
    <label class="drop" id="drop" for="file"><input id="file" type="file" accept="image/*" multiple><b>Choose images or drop them here</b><span>JPG, PNG, WebP. Nothing is uploaded.</span></label>
    <div class="opts">
      <div class="field"><label for="tgt">Target size</label><select id="tgt"><option value="20">Under 20 KB</option><option value="50">Under 50 KB</option><option value="100" selected>Under 100 KB</option><option value="200">Under 200 KB</option><option value="500">Under 500 KB</option><option value="1024">Under 1 MB</option><option value="c">Custom (KB)...</option></select></div>
      <div class="field" id="cw" hidden><label for="cust">Custom size in KB</label><input id="cust" type="number" min="5" max="5000" value="150" style="width:100%;font:inherit;padding:10px;border-radius:10px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink)"></div>
    </div>
    <p><button class="btn" id="go" type="button" disabled>Compress images</button> <button class="btn alt" id="zip" type="button" hidden>Download all (ZIP)</button></p>
    <p class="status" id="msg" aria-live="polite">Choose one or more images to begin.</p>
    <div class="grid" id="grid"></div>
  </div>"""
C_JS = r"""(function(){""" + CORE + r"""
  $('tgt').addEventListener('change',function(){$('cw').hidden=this.value!=='c';});
  go.addEventListener('click',function(){
    var T=($('tgt').value==='c'?Math.max(5,+$('cust').value||100):+$('tgt').value)*1024;
    run(async function(f,b){
      var s=1,blob=null,q=.92,best=null;
      for(var round=0;round<8;round++){
        var c=draw(b,s,true),lo=.1,hi=.95;best=null;
        for(var k=0;k<7;k++){var m=(lo+hi)/2,bl=await toBlob(c,'image/jpeg',m);if(bl.size<=T){best=bl;lo=m;}else hi=m;}
        if(best){blob=best;break;}
        s*=.82;
      }
      var nm=f.name.replace(/\.[^.]+$/,'')+'-compressed.jpg';
      if(!blob){blob=await toBlob(draw(b,s,true),'image/jpeg',.1);}
      res.push({n:nm,b:blob});
      card(nm,blob,kb(f.size)+' → '+kb(blob.size)+(blob.size>T?' (could not reach target)':''));
    });
  });
})();"""
page('image-compressor', 'Image Compressor: Reduce Photo Size to 50KB, 100KB, 200KB (Free, No Upload)',
     'Reduce JPG, PNG and WebP photo size to a target like 20KB, 50KB, 100KB or 200KB for Nepali online forms. Free, runs in your browser, no upload.',
     'Image Compressor (Reduce Photo Size to KB)', 'फोटोको साइज KB मा घटाउनुहोस्', 'File tool',
     'Shrink a photo to the size an online form asks for. Pick a target such as 50 KB or 100 KB and download the compressed JPG. Your image never leaves your device.',
     C_TOOL, """  <h2>How to reduce an image to 50 KB or 100 KB</h2>
  <ol>
    <li>Choose one or more photos.</li>
    <li>Pick the size limit the form asks for, or enter your own in KB.</li>
    <li>Press <strong>Compress images</strong> and download the result. The before and after sizes are shown for each image.</li>
  </ol>
  <p>The tool lowers the JPEG quality until the file fits. If quality alone is not enough, it also reduces the pixel dimensions a little, so a very small target such as 20 KB gives a smaller picture.</p>
  <h2>When you need a small image</h2>
  <p>Online forms in Nepal often limit uploads: job applications, exam and university forms, passport-size photos, signatures and scanned documents. Check the exact size and format on the form, then compress to just under that limit.</p>
  <div class="note"><p><strong>Check the result.</strong> Look at the compressed image before you submit it. Very small limits reduce detail, so a signature or ID photo should still be clear and readable. Output is always JPG.</p></div>""",
     [("How do I reduce a photo to 100 KB?", "Choose the image, select Under 100 KB and press Compress. The tool finds the best quality that fits and shows the new size."),
      ("Is my photo uploaded to a server?", "No. Compression happens in your browser. The photo stays on your device."),
      ("Why is my compressed image smaller in pixels?", "To reach a very small target the tool may reduce the dimensions as well as the quality. Choose a larger target if you need more detail."),
      ("Can I compress many images at once?", "Yes. Select several, compress them together and download them one by one or as a ZIP."),
      ("What format is the result?", "JPG. PNG and WebP images are converted to JPG with a white background replacing any transparency."),
      ("Does it work on a phone?", "Yes. Choose photos from your gallery on Android or iPhone.")],
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>', C_JS,
     [('/jpg-to-pdf/', 'JPG to PDF'), ('/image-converter/', 'Image converter'), ('/pdf-to-jpg/', 'PDF to JPG'), ('/unit-converter/', 'Unit converter')],
     'Image Compressor', 'Free browser-based tool that reduces JPG, PNG and WebP photo size to a target number of KB without uploading the image.')

V_TOOL = """  <div class="conv">
    <label class="drop" id="drop" for="file"><input id="file" type="file" accept="image/*" multiple><b>Choose images or drop them here</b><span>JPG, PNG, WebP, GIF, BMP. Nothing is uploaded.</span></label>
    <div class="opts">
      <div class="field"><label for="fmt">Convert to</label><select id="fmt"><option value="image/jpeg">JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select></div>
      <div class="field"><label for="q">Quality (JPG and WebP)</label><select id="q"><option value=".95">High</option><option value=".85" selected>Good</option><option value=".7">Smaller file</option></select></div>
    </div>
    <p><button class="btn" id="go" type="button" disabled>Convert</button> <button class="btn alt" id="zip" type="button" hidden>Download all (ZIP)</button></p>
    <p class="status" id="msg" aria-live="polite">Choose one or more images to begin.</p>
    <div class="grid" id="grid"></div>
  </div>"""
V_JS = r"""(function(){""" + CORE + r"""
  go.addEventListener('click',function(){
    var t=$('fmt').value,q=+$('q').value,ext={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[t];
    run(async function(f,b){
      var blob=await toBlob(draw(b,1,t==='image/jpeg'),t,q);
      if(!blob||blob.type!==t)throw 0;
      var nm=f.name.replace(/\.[^.]+$/,'')+'.'+ext;res.push({n:nm,b:blob});card(nm,blob,kb(f.size)+' → '+kb(blob.size));
    });
  });
})();"""
page('image-converter', 'JPG Converter: Convert PNG or WebP to JPG and JPG to PNG (Free, No Upload)',
     'Free image converter for JPG, PNG and WebP. Convert PNG to JPG, WebP to JPG or JPG to PNG in your browser, many files at once, no upload, no watermark.',
     'JPG Converter (PNG, WebP, JPG)', 'तस्बिर JPG, PNG, WebP मा बदल्नुहोस्', 'File tool',
     'Convert images between JPG, PNG and WebP. Do several at once and download them as a ZIP. Everything runs in your browser.',
     V_TOOL, """  <h2>How to convert an image to JPG</h2>
  <ol>
    <li>Choose your images (PNG, WebP, GIF, BMP or JPG).</li>
    <li>Select the format you want, then the quality.</li>
    <li>Press <strong>Convert</strong> and download each file, or all of them in a ZIP.</li>
  </ol>
  <p>Many forms and websites accept only JPG. WebP photos saved from a phone or the web often need converting first. Converting to JPG replaces any transparent area with white.</p>
  <h2>Which format should I use?</h2>
  <ul>
    <li><strong>JPG</strong>: best for photos and the most widely accepted.</li>
    <li><strong>PNG</strong>: best for logos, screenshots and images with transparency; files are larger.</li>
    <li><strong>WebP</strong>: smaller files on websites; not accepted everywhere.</li>
  </ul>
  <p>Need a particular file size? Use the <a href="/image-compressor/">image compressor</a>. To make a PDF, use <a href="/jpg-to-pdf/">JPG to PDF</a>.</p>""",
     [("How do I convert PNG to JPG?", "Choose the PNG, select JPG as the output format and press Convert. Transparent areas become white."),
      ("How do I convert WebP to JPG?", "Choose the WebP file, select JPG and press Convert. It works the same way as any other image."),
      ("Is this image converter free and private?", "Yes. It is free and the files are converted in your browser, so they are never uploaded."),
      ("Will converting reduce the quality?", "Converting to JPG or WebP is lossy, so choose High quality if detail matters. Converting to PNG keeps every pixel but makes larger files."),
      ("Can I convert many images at once?", "Yes. Select several and download them individually or as a ZIP."),
      ("Does it support JPG to PNG?", "Yes. Choose JPG files and select PNG as the output format.")],
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>', V_JS,
     [('/image-compressor/', 'Image compressor'), ('/jpg-to-pdf/', 'JPG to PDF'), ('/pdf-to-jpg/', 'PDF to JPG'), ('/unit-converter/', 'Unit converter')],
     'Image Converter', 'Free browser-based tool that converts images between JPG, PNG and WebP without uploading them.')
print('ok')
