#!/usr/bin/env python3
"""Merge PDF and Split PDF tools (client-side, pdf-lib). Reuses page(), KIT_CSS, helpers from make_pro_tools.py.
Run from repo root: python3 scripts/make_pdf_tools.py"""
_pro = open('scripts/make_pro_tools.py', encoding='utf-8').read()
_a = _pro.index('# ================= IMAGE COMPRESSOR')
_b = _pro.index('# ================= SHARED PIECES')
_c = _pro.index('# ================= JPG TO PDF (pro)')
exec(_pro[:_a])          # page() library, KIT_CSS, NE dict
exec(_pro[_b:_c])        # dz(), head(), chips(), BASE_JS

NE['merge-pdf'] = {'h2': 'नेपालीमा: धेरै PDF लाई एउटै PDF कसरी बनाउने?',
  'steps': ['जोड्नुपर्ने PDF फाइलहरू छान्नुहोस्। एकैपटक धेरै छान्न सकिन्छ।',
            'तीर (↑ ↓) ले फाइलको क्रम मिलाउनुहोस्। कुनै फाइलको केही पेज मात्र चाहिए "Pages" मा जस्तै 1-3, 5 लेख्नुहोस्।',
            '"Merge PDFs" थिच्नुहोस्।',
            '"Download PDF" थिचेर जोडिएको PDF डाउनलोड गर्नुहोस्।'],
  'note': 'तपाईंका PDF कुनै सर्भरमा पठाइँदैनन्, सबै काम ब्राउजरमै हुन्छ। त्यसैले नागरिकता, शैक्षिक प्रमाणपत्र वा बैंकका कागजात सुरक्षित रहन्छन्। पासवर्ड भएको PDF जोड्न पहिले पासवर्ड हटाउनुपर्छ।',
  'faq': [('फारममा एउटै PDF मात्र मागेको छ, के गर्ने?', 'सबै कागजातका PDF थपेर क्रम मिलाउनुहोस् र "Merge PDFs" थिच्नुहोस्। फोटो मात्र भए पहिले JPG to PDF प्रयोग गर्नुहोस्।'),
          ('जोडेपछि फाइल ठूलो भयो भने?', 'जोडिएको PDF को साइज प्रायः सबै फाइलको जोडफल जति हुन्छ। सानो चाहिए मूल फोटो पहिले Image Compressor ले घटाएर JPG to PDF बाट PDF बनाउनुहोस्।'),
          ('मोबाइलबाट चल्छ?', 'चल्छ। फोनको फाइलबाट PDF छानेर जोड्न सकिन्छ।')]}
NE['split-pdf'] = {'h2': 'नेपालीमा: PDF का पेज कसरी छुट्याउने वा हटाउने?',
  'steps': ['PDF फाइल छान्नुहोस्।',
            'के गर्ने छान्नुहोस्: चाहिएका पेज मात्र राख्ने, केही पेज हटाउने, वा हरेक पेज अलग PDF बनाउने।',
            '"Pages" मा पेज नम्बर लेख्नुहोस्, जस्तै 1-3, 5।',
            '"Split PDF" थिचेर बनेको फाइल डाउनलोड गर्नुहोस्।'],
  'note': 'PDF तपाईंको डिभाइसबाट बाहिर जाँदैन, सबै काम ब्राउजरमै हुन्छ। पासवर्ड भएको PDF खोल्न सकिँदैन, पहिले पासवर्ड हटाउनुहोस्। मूल फाइल जस्ताको तस्तै रहन्छ, नयाँ फाइल मात्र बन्छ।',
  'faq': [('PDF बाट एउटा मात्र पेज कसरी निकाल्ने?', '"Keep only these pages" छानेर "Pages" मा त्यो पेजको नम्बर लेख्नुहोस्, जस्तै 4। त्यसपछि "Split PDF" थिच्नुहोस्।'),
          ('PDF बाट पेज कसरी हटाउने?', '"Remove these pages" छानेर हटाउनुपर्ने पेज नम्बर लेख्नुहोस्, जस्तै 2, 5-6। बाँकी पेजको नयाँ PDF बन्छ।'),
          ('मूल PDF बिग्रन्छ?', 'बिग्रँदैन। मूल फाइल जस्ताको तस्तै रहन्छ र नयाँ फाइल मात्र बनिन्छ।')]}

PDFLIB = '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>'
PDF_CSS = '<style>.tk-file{grid-template-columns:56px 1fr}.tk-file .ico{width:56px;height:64px;border-radius:10px;background:var(--red);color:#fff;font-weight:800;font-size:.82rem;display:flex;align-items:center;justify-content:center;letter-spacing:.04em}.tk-file .rg{margin-top:6px;min-height:40px;font-size:.92rem;padding:7px 10px}.tk-file .ac .tk-b{min-width:44px;padding:0 12px}.tk-info{margin:8px 0 2px;color:var(--ink2);font-size:.95rem}</style>'

PDF_JS_COMMON = r"""
  var PL=window.PDFLib;
  function isPdf(f){return f.type==='application/pdf'||/\.pdf$/i.test(f.name);}
  function parse(t,n){
    var out=[],bad=false;(t||'').split(',').forEach(function(p){p=p.trim();if(!p)return;var m=p.match(/^(\d+)\s*-\s*(\d+)$/);
      if(m){var a=+m[1],b=+m[2];if(a<1||b>n||a>b){bad=true;return;}for(var i=a;i<=b;i++)out.push(i);}
      else if(/^\d+$/.test(p)){if(+p<1||+p>n){bad=true;return;}out.push(+p);}else bad=true;});
    return {list:out,bad:bad,empty:!(t||'').trim()};
  }
  async function readPdf(f){
    var buf=await f.arrayBuffer();
    try{var d=await PL.PDFDocument.load(buf);return {buf:buf,pages:d.getPageCount()};}
    catch(e){var enc=e&&/encrypt/i.test(String(e.message||e)+String(e.name||''));var er=new Error(enc?'enc':'bad');throw er;}
  }
"""

# ================= MERGE PDF =================
MG_TOOL = KIT_CSS + PDF_CSS + '\n  <div class="conv tk" id="app">\n    ' + head(['1. Add', '2. Arrange', '3. Download']) + '\n    ' + dz(True, 'Drop PDF files here, or tap to choose', 'Add two or more PDFs. They are combined in the order you set.', accept='application/pdf,.pdf', cam=False) + '''
    <div id="panel" hidden>
      <ul class="tk-files" id="files" aria-live="polite"></ul>
      <p class="tk-live" id="live" aria-live="polite"></p>
      <div class="tk-bar"><div class="tk-sum" id="sum"></div><button class="tk-b" id="clr" type="button">Start over</button><button class="tk-b pri" id="go" type="button">Merge PDFs</button><a class="tk-b pri" id="dl" download="merged.pdf" href="#" hidden>Download PDF</a></div>
    </div>
  </div>'''
MG_JS = r"""(function(){""" + BASE_JS + PDF_JS_COMMON + r"""
  var items=[],seq=0,url=null;
  function stale(){$('dl').hidden=true;$('go').hidden=false;if(items.length)step(1);}
  function render(){
    var ul=$('files');ul.innerHTML='';
    items.forEach(function(it,i){var li=document.createElement('li');li.className='tk-file';
      li.innerHTML='<div class="ico" aria-hidden="true">PDF</div><div><div class="nm"></div><span class="st"></span><input class="tk-in rg" type="text" inputmode="text" autocomplete="off" placeholder="Pages (optional), e.g. 1-3, 5" aria-label="Pages to include from this file" data-i="'+it.id+'"></div><div class="ac"><button type="button" class="tk-b" data-a="u" data-i="'+it.id+'" aria-label="Move up">↑</button><button type="button" class="tk-b" data-a="d" data-i="'+it.id+'" aria-label="Move down">↓</button><button type="button" class="tk-b" data-a="x" data-i="'+it.id+'">Remove</button></div>';
      li.querySelector('.nm').textContent=(i+1)+'. '+it.n;li.querySelector('.st').textContent=it.pages+' page'+(it.pages>1?'s':'')+' · '+kb(it.size);li.querySelector('.rg').value=it.r;ul.appendChild(li);});
    var tp=items.reduce(function(s,x){return s+x.pages;},0);
    $('sum').innerHTML=items.length?'<b>'+items.length+'</b> file'+(items.length>1?'s':'')+' · <b>'+tp+'</b> pages':'';$('go').disabled=items.length<2;
    if(items.length===1)$('live').textContent='Add at least one more PDF to merge.';
  }
  bind(async function(fl){
    $('live').textContent='Reading PDFs...';var bad=[];
    for(var i=0;i<fl.length;i++){try{var r=await readPdf(fl[i]);items.push({id:++seq,n:fl[i].name,size:fl[i].size,buf:r.buf,pages:r.pages,r:''});}
      catch(e){bad.push(fl[i].name+(e.message==='enc'?' (password-protected)':' (cannot be read)'));}}
    $('panel').hidden=false;mini(true,'Add more PDFs');$('live').textContent=bad.length?'Skipped: '+bad.join(', ')+'. Password-protected or damaged PDFs cannot be added.':'';stale();render();
    if(items.length===1&&!bad.length)$('live').textContent='Add at least one more PDF to merge.';
  },isPdf);
  $('files').addEventListener('input',function(e){var id=e.target.getAttribute&&e.target.getAttribute('data-i');if(!id||!e.target.classList.contains('rg'))return;var it=items.find(function(x){return x.id===+id});if(it){it.r=e.target.value;stale();}});
  $('files').addEventListener('click',function(e){var a=e.target.getAttribute&&e.target.getAttribute('data-a');if(!a)return;var id=+e.target.getAttribute('data-i'),i=items.findIndex(function(x){return x.id===id});
    if(a==='x')items.splice(i,1);else if(a==='u'&&i>0){var t=items[i];items[i]=items[i-1];items[i-1]=t;}else if(a==='d'&&i<items.length-1){var t2=items[i];items[i]=items[i+1];items[i+1]=t2;}
    if(!items.length){$('panel').hidden=true;mini(false,'Drop PDF files here, or tap to choose');step(0);}$('live').textContent='';stale();render();});
  $('clr').addEventListener('click',function(){items=[];$('panel').hidden=true;$('live').textContent='';mini(false,'Drop PDF files here, or tap to choose');step(0);render();});
  $('go').addEventListener('click',async function(){
    if(!PL){$('live').textContent='The PDF library did not load. Check your connection and reload.';return;}
    $('go').disabled=true;
    try{
      var out=await PL.PDFDocument.create(),total=0;
      for(var i=0;i<items.length;i++){
        var it=items[i],p=parse(it.r,it.pages);
        if(p.bad){$('live').textContent='File '+(i+1)+': pages must be numbers from 1 to '+it.pages+', like 1-3, 5.';$('go').disabled=false;return;}
        var idx=p.empty?Array.from({length:it.pages},function(_,k){return k;}):p.list.map(function(n){return n-1;});
        $('live').textContent='Adding file '+(i+1)+' of '+items.length+'...';await new Promise(function(r){setTimeout(r,0)});
        var src=await PL.PDFDocument.load(it.buf),cp=await out.copyPages(src,idx);cp.forEach(function(pg){out.addPage(pg);});total+=cp.length;
      }
      var bytes=await out.save(),blob=new Blob([bytes],{type:'application/pdf'});
      if(url)URL.revokeObjectURL(url);url=URL.createObjectURL(blob);var a=$('dl');a.href=url;a.hidden=false;$('go').hidden=true;
      $('sum').innerHTML='<b>'+total+'</b> pages · <b>'+kb(blob.size)+'</b>';$('live').textContent='Done. Your merged PDF is ready.';step(2);
    }catch(e){$('live').textContent='Something went wrong. One of the files may be damaged. Try removing files one by one.';}
    $('go').disabled=items.length<2;
  });
  step(0);
})();"""

MG_SECTIONS = """  <h2>How to merge PDF files</h2>
  <ol>
    <li>Choose the PDF files you want to combine. You can pick several at once.</li>
    <li>Use the arrows to put the files in the right order. If you only need some pages of a file, type them in the <strong>Pages</strong> box, for example <code>1-3, 5</code>.</li>
    <li>Press <strong>Merge PDFs</strong>, then <strong>Download PDF</strong>.</li>
  </ol>
  <p>The files are combined by your browser, so they are never sent to a server. That keeps documents such as citizenship certificates, transcripts and bank statements on your own device.</p>
  <h2>When you need one PDF</h2>
  <ul>
    <li>A job or admission form that accepts a single PDF but asks for several documents.</li>
    <li>Scans of both sides of a certificate that are saved as separate files.</li>
    <li>A report that was exported in parts.</li>
  </ul>
  <div class="note"><p><strong>Keep the size small.</strong> The merged file is about as large as the originals added together. If a form has an upload limit, shrink your photos first with the <a href="/image-compressor/">image compressor</a>, then make each scan a PDF with <a href="/jpg-to-pdf/">JPG to PDF</a>, and merge the results here. Password-protected PDFs must be unlocked before they can be merged.</p></div>
  <p>To take pages out of a PDF, use <a href="/split-pdf/">Split PDF</a>.</p>"""
MG_FAQ = [("Is this PDF merger free?", "Yes. It is free, needs no account and adds no watermark."),
          ("Are my PDFs uploaded to a server?", "No. The files are combined in your browser on your own device, so they are not uploaded anywhere."),
          ("Can I merge only some pages of a file?", "Yes. Type the pages in the box under the file, for example 1-3, 5. Leave the box empty to use every page."),
          ("Can I change the order of the files?", "Yes. Use the up and down arrows next to each file. The merged PDF follows the order shown on screen."),
          ("Can I merge password-protected PDFs?", "Not directly. Remove the password first, then add the file. Files that cannot be read are skipped and listed."),
          ("Does merging reduce the quality?", "No. Pages are copied as they are, so text stays sharp and images are not recompressed.")]
page('merge-pdf', 'Merge PDF Files: Combine PDFs into One (Free, No Upload)',
     'Merge PDF files into one free in your browser. Reorder files, pick pages from each, download one PDF. No upload, no sign-up, no watermark. Works on phones.',
     'Merge PDF Files', 'PDF फाइलहरू जोड्नुहोस्', 'File tool',
     'Combine several PDFs into one. Put the files in order, choose pages if you need to, and download. Your files stay on your device.',
     MG_TOOL, MG_SECTIONS, MG_FAQ, PDFLIB, MG_JS,
     [('/guide/merge-pdf-files-on-phone', 'Guide: merge PDF files'), ('/split-pdf/', 'Split PDF'), ('/jpg-to-pdf/', 'JPG to PDF'), ('/image-compressor/', 'Image compressor')],
     'Merge PDF', 'Free browser-based tool that combines several PDF files into one without uploading them.')

# ================= SPLIT PDF =================
SP_TOOL = KIT_CSS + PDF_CSS + '\n  <div class="conv tk" id="app">\n    ' + head(['1. Add', '2. Choose pages', '3. Download']) + '\n    ' + dz(False, 'Drop a PDF here, or tap to choose', 'The file stays on your device.', accept='application/pdf,.pdf', cam=False) + '''
    <div id="panel" hidden>
      <p class="tk-info" id="info"></p>
      ''' + chips('mode', 'mdl', 'What do you want to do?', [('keep', 'Keep only these pages'), ('drop', 'Remove these pages'), ('each', 'Save every page separately')], 'keep') + '''
      <div class="tk-row" id="rwrap" style="margin-top:12px"><div class="f"><label class="l" for="rng" id="rl">Pages to keep</label><input class="tk-in" id="rng" placeholder="e.g. 1-3, 5" inputmode="text" autocomplete="off"></div></div>
      <p class="tk-live" id="live" aria-live="polite"></p>
      <div class="tk-bar"><div class="tk-sum" id="sum"></div><button class="tk-b" id="clr" type="button">Start over</button><button class="tk-b pri" id="go" type="button">Split PDF</button><a class="tk-b pri" id="dl" download="split.pdf" href="#" hidden>Download</a></div>
    </div>
  </div>'''
SP_JS = r"""(function(){""" + BASE_JS + PDF_JS_COMMON + r"""
  var cur=null,url=null,cap=300;
  function stale(){$('dl').hidden=true;$('go').hidden=false;if(cur)step(1);}
  function modeUi(){var m=val('mode');$('rl').textContent=m==='keep'?'Pages to keep':m==='drop'?'Pages to remove':'Pages to save (leave empty for all)';$('rng').placeholder=m==='each'?'e.g. 1-3, 5 (optional)':'e.g. 1-3, 5';}
  bind(async function(fl){
    var f=fl[0];$('live').textContent='Reading PDF...';
    try{var r=await readPdf(f);cur={n:f.name,size:f.size,buf:r.buf,pages:r.pages};$('panel').hidden=false;$('info').textContent=f.name+' · '+r.pages+' page'+(r.pages>1?'s':'')+' · '+kb(f.size);$('live').textContent='';mini(true,'Change PDF');stale();}
    catch(e){$('live').textContent=e.message==='enc'?'This PDF is password-protected. Remove the password first, then try again.':'This PDF could not be read. It may be damaged.';}
  },isPdf);
  [].forEach.call(document.querySelectorAll('input[name=mode]'),function(r){r.addEventListener('change',function(){modeUi();stale();});});
  $('rng').addEventListener('input',stale);
  $('clr').addEventListener('click',function(){cur=null;$('panel').hidden=true;$('live').textContent='';$('rng').value='';mini(false,'Drop a PDF here, or tap to choose');step(0);});
  function base(){return cur.n.replace(/\.pdf$/i,'');}
  function finish(blob,name,label){if(url)URL.revokeObjectURL(url);url=URL.createObjectURL(blob);var a=$('dl');a.href=url;a.download=name;a.textContent=label;a.hidden=false;$('go').hidden=true;$('sum').innerHTML='<b>'+kb(blob.size)+'</b>';step(2);}
  $('go').addEventListener('click',async function(){
    if(!PL){$('live').textContent='The PDF library did not load. Check your connection and reload.';return;}
    var m=val('mode'),p=parse($('rng').value,cur.pages);
    if(p.bad){$('live').textContent='Pages must be numbers from 1 to '+cur.pages+', like 1-3, 5.';return;}
    if(p.empty&&m!=='each'){$('live').textContent=m==='keep'?'Type the pages you want to keep.':'Type the pages you want to remove.';return;}
    $('go').disabled=true;
    try{
      var src=await PL.PDFDocument.load(cur.buf),all=Array.from({length:cur.pages},function(_,k){return k+1;}),pick;
      if(m==='keep')pick=p.list;else if(m==='drop'){var s={};p.list.forEach(function(n){s[n]=1;});pick=all.filter(function(n){return !s[n];});}else pick=p.empty?all:p.list;
      if(!pick.length){$('live').textContent='No pages would be left. Choose fewer pages to remove.';$('go').disabled=false;return;}
      if(m==='each'){
        if(!window.JSZip){$('live').textContent='The ZIP library did not load. Reload and try again.';$('go').disabled=false;return;}
        if(pick.length>cap)pick=pick.slice(0,cap);var z=new JSZip();
        for(var i=0;i<pick.length;i++){$('live').textContent='Saving page '+pick[i]+' ('+(i+1)+' of '+pick.length+')...';await new Promise(function(r){setTimeout(r,0)});
          var d=await PL.PDFDocument.create(),cp=await d.copyPages(src,[pick[i]-1]);d.addPage(cp[0]);z.file(base()+'-page-'+pick[i]+'.pdf',await d.save());}
        var zb=await z.generateAsync({type:'blob'});finish(zb,base()+'-pages.zip','Download ZIP');$('live').textContent='Done. '+pick.length+' PDF files in the ZIP.'+(p.empty&&cur.pages>cap?' (First '+cap+' pages only.)':'');
      }else{
        var out=await PL.PDFDocument.create(),cp2=await out.copyPages(src,pick.map(function(n){return n-1;}));cp2.forEach(function(pg){out.addPage(pg);});
        var blob=new Blob([await out.save()],{type:'application/pdf'});finish(blob,base()+(m==='keep'?'-extract':'-edited')+'.pdf','Download PDF');$('live').textContent='Done. The new PDF has '+pick.length+' page'+(pick.length>1?'s':'')+'.';
      }
    }catch(e){$('live').textContent='Something went wrong. The PDF may be damaged.';}
    $('go').disabled=false;
  });
  modeUi();step(0);
})();"""
SP_SECTIONS = """  <h2>How to split a PDF or take pages out</h2>
  <ol>
    <li>Choose your PDF. The tool shows how many pages it has.</li>
    <li>Pick what you want: <strong>keep only</strong> some pages, <strong>remove</strong> some pages, or <strong>save every page</strong> as its own PDF.</li>
    <li>Type the page numbers, for example <code>1-3, 5</code>, then press <strong>Split PDF</strong> and download the result.</li>
  </ol>
  <p>Your original file is not changed. A new file is made on your device, and nothing is uploaded.</p>
  <h2>Common uses</h2>
  <ul>
    <li>Keep only the pages a form asks for, such as the first two pages of a long scan.</li>
    <li>Remove a blank or wrong page before you upload a document.</li>
    <li>Make a file smaller by sending only the pages that are needed.</li>
  </ul>
  <div class="note"><p><strong>Page numbers.</strong> Page numbers count from the first page of the file, as shown in your PDF viewer. You can type a range such as 2-4 and single pages such as 7, separated by commas. Password-protected PDFs must be unlocked first.</p></div>
  <p>To join files instead, use <a href="/merge-pdf/">Merge PDF</a>. To turn pages into pictures, use <a href="/pdf-to-jpg/">PDF to JPG</a>.</p>"""
SP_FAQ = [("Is this Split PDF tool free?", "Yes. It is free, needs no account and adds no watermark."),
          ("Is my PDF uploaded to a server?", "No. The file is processed in your browser on your own device."),
          ("How do I extract one page from a PDF?", "Choose Keep only these pages, type the page number, such as 4, and press Split PDF."),
          ("How do I delete a page from a PDF?", "Choose Remove these pages, type the page numbers you do not want, such as 2, 5-6, and press Split PDF. You get a new PDF without those pages."),
          ("Can I save each page as a separate PDF?", "Yes. Choose Save every page separately. You get a ZIP file with one PDF per page, up to 300 pages."),
          ("Does it work with password-protected PDFs?", "No. Remove the password first, then add the file.")]
page('split-pdf', 'Split PDF: Extract or Remove Pages from a PDF (Free, No Upload)',
     'Split a PDF free in your browser. Keep chosen pages, delete pages or save every page as its own PDF. No upload, no sign-up, no watermark. Works on phones.',
     'Split PDF and Remove Pages', 'PDF का पेज छुट्याउनुहोस् वा हटाउनुहोस्', 'File tool',
     'Take pages out of a PDF, keep only the ones you need, or save each page as its own file. Your PDF stays on your device.',
     SP_TOOL, SP_SECTIONS, SP_FAQ, PDFLIB + '\n<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>', SP_JS,
     [('/guide/remove-pages-from-pdf', 'Guide: remove pages from a PDF'), ('/merge-pdf/', 'Merge PDF'), ('/pdf-to-jpg/', 'PDF to JPG'), ('/jpg-to-pdf/', 'JPG to PDF')],
     'Split PDF', 'Free browser-based tool that extracts, removes or separates pages of a PDF without uploading it.')
print('pdf tools ok')
