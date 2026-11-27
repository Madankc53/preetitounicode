#!/usr/bin/env python3
"""Compress PDF and PNG to PDF pages. Reuses make_pro_tools.py pieces. Run from repo root."""
_pro = open('scripts/make_pro_tools.py', encoding='utf-8').read()
_a = _pro.index('# ================= IMAGE COMPRESSOR')
_b = _pro.index('# ================= SHARED PIECES')
_c = _pro.index('# ================= PDF TO JPG')
exec(_pro[:_a])
exec(_pro[_b:_c])   # helpers + JPG TO PDF (JP_TOOL, JP_JS); regenerates jpg-to-pdf identically

NE['compress-pdf'] = {'h2': 'नेपालीमा: PDF को साइज कसरी घटाउने?',
  'steps': ['PDF फाइल छान्नुहोस्।',
            'कम्प्रेसन स्तर छान्नुहोस्। फारमले निश्चित साइज (जस्तै 200 KB) माग्छ भने "Target size" मा त्यो संख्या लेख्नुहोस्।',
            '"Compress PDF" थिच्नुहोस् र साइज घटेको फाइल डाउनलोड गर्नुहोस्।'],
  'note': 'यो टुलले PDF का पेजलाई फोटो बनाएर सानो गर्छ, त्यसैले साइज धेरै घट्छ तर PDF भित्रको अक्षर छानेर कपी गर्न मिल्दैन। स्क्यान गरिएका कागजातका लागि यो ठीक हुन्छ। फाइल इन्टरनेटमा अपलोड हुँदैन।',
  'faq': [('PDF को साइज 100 KB मुनि कसरी ल्याउने?', '"Target size" मा 100 लेखेर "Compress PDF" थिच्नुहोस्। टुलले साइज पुग्ने गरी स्तर आफैँ घटाउँछ।'),
          ('कम्प्रेस गरेपछि अक्षर कपी हुँदैन किन?', 'किनभने पेजहरू फोटोका रूपमा सुरक्षित हुन्छन्। कपी गर्न मिल्ने अक्षर चाहिए मूल फाइल राख्नुहोस्।'),
          ('मेरो PDF सुरक्षित छ?', 'छ। सबै काम तपाईंको ब्राउजरमै हुन्छ र फाइल अपलोड हुँदैन।')]}
NE['png-to-pdf'] = {'h2': 'नेपालीमा: PNG लाई PDF कसरी बनाउने?',
  'steps': ['PNG फोटोहरू छान्नुहोस्। धेरै एकैपटक छान्न सकिन्छ।',
            'तीरले क्रम मिलाउनुहोस्, ढल्किएको फोटो "Rotate" ले सोझ्याउनुहोस्।',
            'पेजको साइज (A4) छान्नुहोस् र "Create PDF" थिच्नुहोस्।',
            '"Download PDF" थिचेर PDF डाउनलोड गर्नुहोस्।'],
  'note': 'PNG को पारदर्शी भाग सेतो हुन्छ। फोटो इन्टरनेटमा अपलोड हुँदैनन्। फाइल ठूलो भए "Small" गुणस्तर छान्नुहोस्।',
  'faq': [('स्क्रिनसट PDF कसरी बनाउने?', 'स्क्रिनसट PNG छानेर "Create PDF" थिच्नुहोस्। अक्षर राम्ररी देखिनुपर्ने भए "High" गुणस्तर छान्नुहोस्।'),
          ('PDF को साइज कसरी घटाउने?', '"Small" गुणस्तर छान्नुहोस्, वा बनेको PDF लाई Compress PDF मा लैजानुहोस्।')]}

DOC_LIBS = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>\n'
            '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>')

# ================= COMPRESS PDF =================
CP_TOOL = KIT_CSS + '<style>progress{width:100%;height:10px}.tk-res{margin:10px 0;padding:12px 14px;border:1px solid var(--line);border-radius:var(--r);background:var(--bg);font-size:1rem}.tk-res b{font-size:1.15rem}</style>\n  <div class="conv tk" id="app">\n    ' + head(['1. Add PDF', '2. Compress', '3. Download']) + '\n    ' + dz(False, 'Drop a PDF here, or tap to choose', 'It is compressed on your device.', 'application/pdf,.pdf', False) + '''
    <div id="panel" hidden>
      <p class="tk-sec" id="fnm"></p>
      ''' + chips('lvl', 'lvl1', 'Compression', [('lt', 'Light'), ('bal', 'Balanced'), ('str', 'Strong')], 'bal') + '''
      <div class="tk-row" style="margin-top:12px"><div class="f"><label class="l" for="tgt">Target size in KB (optional)</label><input class="tk-in" id="tgt" placeholder="e.g. 200" inputmode="numeric" autocomplete="off"></div></div>
      <div class="tk-row" id="pw" hidden style="margin-top:12px"><div class="f"><label class="l" for="pwi">This PDF needs a password</label><input class="tk-in" id="pwi" type="password" autocomplete="off"></div></div>
      <progress id="pr" max="1" value="0" hidden></progress>
      <p class="tk-live" id="live" aria-live="polite"></p>
      <div class="tk-res" id="res" hidden></div>
      <div class="tk-bar"><div class="tk-sum" id="sum"></div><button class="tk-b" id="clr" type="button">Start over</button><button class="tk-b pri" id="go" type="button">Compress PDF</button><a class="tk-b pri" id="dl" download="compressed.pdf" href="#" hidden>Download PDF</a></div>
    </div>
  </div>'''
CP_JS = r"""(function(){""" + BASE_JS + r"""
  var file=null,url=null,CAP=100;
  var LV={lt:[[150,.8]],bal:[[110,.65]],str:[[80,.5]]};
  var LADDER=[[150,.8],[120,.7],[100,.6],[80,.5],[65,.4],[50,.35]];
  var st=lsGet('cp-set',{lvl:'bal'});setRadio('lvl',st.lvl);
  function stale(){$('dl').hidden=true;$('go').hidden=false;$('res').hidden=true;if(file)step(1);}
  bind(function(fl){file=fl[0];$('panel').hidden=false;$('fnm').textContent=file.name+' · '+kb(file.size);$('pw').hidden=true;$('live').textContent='';mini(true,'Change PDF');stale();},function(f){return f.type==='application/pdf'||/\.pdf$/i.test(f.name);});
  [].forEach.call(document.querySelectorAll('input[name=lvl]'),function(r){r.addEventListener('change',function(){lsSet('cp-set',{lvl:val('lvl')});stale();});});
  $('tgt').addEventListener('input',stale);
  async function open(){var L=window.pdfjsLib;if(!L)throw new Error('lib');L.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    return L.getDocument({data:await file.arrayBuffer(),password:$('pwi').value||undefined}).promise;}
  async function build(pdf,n,dpi,q,label){
    var J=window.jspdf.jsPDF,doc=null,sc=dpi/72;
    for(var i=1;i<=n;i++){
      $('live').textContent=label+' page '+i+' of '+n+'...';$('pr').value=(i-1)/n;await new Promise(function(r){setTimeout(r,0)});
      var p=await pdf.getPage(i),b=p.getViewport({scale:1}),vp=p.getViewport({scale:sc}),f=Math.min(1,Math.sqrt(16000000/(vp.width*vp.height)));if(f<1)vp=p.getViewport({scale:sc*f});
      var c=document.createElement('canvas');c.width=Math.floor(vp.width);c.height=Math.floor(vp.height);var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
      await p.render({canvasContext:x,viewport:vp}).promise;
      var d=c.toDataURL('image/jpeg',q),o=b.width>b.height?'l':'p';
      if(!doc)doc=new J({unit:'pt',format:[b.width,b.height],orientation:o,compress:true});else doc.addPage([b.width,b.height],o);
      doc.addImage(d,'JPEG',0,0,b.width,b.height,undefined,'FAST');c.width=c.height=0;
    }
    return doc.output('blob');
  }
  $('go').addEventListener('click',async function(){
    if(!window.jspdf){$('live').textContent='The PDF library did not load. Check your connection and reload.';return;}
    $('go').disabled=true;$('pr').hidden=false;$('pr').value=0;$('res').hidden=true;
    try{
      var pdf=await open(),n=Math.min(pdf.numPages,CAP),over=pdf.numPages>CAP,tgt=parseInt($('tgt').value,10)*1024,blob,note='';
      if(tgt>0){
        var tries=0,best=null;
        for(var k=0;k<LADDER.length;k++){tries++;blob=await build(pdf,n,LADDER[k][0],LADDER[k][1],'Compressing (try '+tries+')');best=blob;if(blob.size<=tgt)break;}
        if(blob.size>tgt)note='The smallest result is still above '+kb(tgt)+'. Try Split PDF to keep fewer pages.';
      }else{var l=LV[val('lvl')][0];blob=await build(pdf,n,l[0],l[1],'Compressing');}
      var a=$('dl'),res=$('res');
      if(blob.size>=file.size){res.hidden=false;res.innerHTML='<b>This PDF is already small.</b> Compressing would make it larger ('+kb(blob.size)+' vs '+kb(file.size)+'), so keep your original file.';$('live').textContent='';$('sum').textContent='';
      }else{
        if(url)URL.revokeObjectURL(url);url=URL.createObjectURL(blob);a.href=url;a.download=file.name.replace(/\.pdf$/i,'')+'-compressed.pdf';a.hidden=false;$('go').hidden=true;
        var pc=Math.min(99,Math.round((1-blob.size/file.size)*100));
        res.hidden=false;res.innerHTML='<b>'+kb(file.size)+' → '+kb(blob.size)+'</b> (about '+pc+'% smaller)';
        $('sum').innerHTML='<b>'+n+'</b> page'+(n>1?'s':'');$('live').textContent=(note?note+' ':'')+(over?'Only the first '+CAP+' pages were included. ':'')+'Pages are saved as images, so the text cannot be selected or copied.';step(2);
      }
      $('pw').hidden=true;
    }catch(e){
      if(e&&e.name==='PasswordException'){$('pw').hidden=false;$('live').textContent=e.code===2?'Wrong password. Try again.':'Enter the password, then press Compress PDF.';}
      else if(e&&e.message==='lib')$('live').textContent='The PDF library did not load. Check your connection and reload.';
      else $('live').textContent='Could not compress this PDF. It may be damaged.';
    }
    $('pr').hidden=true;$('go').disabled=false;
  });
  $('clr').addEventListener('click',function(){file=null;$('panel').hidden=true;$('res').hidden=true;$('tgt').value='';mini(false,'Drop a PDF here, or tap to choose');step(0);});
  step(0);
})();"""
CP_SECTIONS = """  <h2>How to compress a PDF</h2>
  <ol>
    <li>Choose your PDF.</li>
    <li>Pick <strong>Light</strong>, <strong>Balanced</strong> or <strong>Strong</strong>. If a form allows only a certain size, type it in <strong>Target size</strong>, for example <code>200</code> for 200 KB.</li>
    <li>Press <strong>Compress PDF</strong>, check the new size, then download the file.</li>
  </ol>
  <p>The file is compressed in your browser. It is not uploaded to any server.</p>
  <h2>How this compressor works</h2>
  <p>Each page is redrawn as a compressed picture and rebuilt into a new PDF. This makes scanned documents, photo PDFs and certificates much smaller. The trade-off is that the text becomes part of the picture, so you cannot select or copy it afterwards. If you need searchable text, keep your original file and compress only the copy you upload.</p>
  <div class="note"><p><strong>Meeting a size limit.</strong> For Loksewa, university and job portals, enter the allowed size in Target size. The tool tries stronger settings until the file fits. If it still does not fit, use <a href="/split-pdf/">Split PDF</a> to keep only the pages the form needs. To make a small PDF from photos in the first place, use <a href="/jpg-to-pdf/">JPG to PDF</a>.</p></div>"""
CP_FAQ = [("Is this PDF compressor free?", "Yes. It is free, needs no account and adds no watermark."),
          ("Is my PDF uploaded to a server?", "No. The PDF is compressed in your browser on your own device."),
          ("How do I reduce a PDF to a certain size, like 200 KB?", "Type the size in the Target size box and press Compress PDF. The tool tries stronger compression until the file fits, or tells you if it cannot."),
          ("Why can I not select the text after compressing?", "Pages are saved as compressed pictures. That is what makes the file small, but the text is no longer separate from the image."),
          ("Why did the tool say my PDF is already small?", "A PDF that is mostly text can be smaller than a picture of the same page. Compressing would make it larger, so keep the original."),
          ("Does it work with password-protected PDFs?", "Yes, if you know the password. The tool asks for it."),
          ("Is there a page limit?", "The tool compresses up to 100 pages at a time to keep your browser responsive.")]
page('compress-pdf', 'Compress PDF: Reduce PDF Size to KB or MB (Free, No Upload)',
     'Compress a PDF free in your browser. Choose a level or type a target size such as 200 KB. No upload, no sign-up, no watermark. Works on phones.',
     'Compress PDF', 'PDF को साइज घटाउनुहोस्', 'File tool',
     'Make a PDF smaller for forms and email. Pick a level or set a target size in KB. Your file stays on your device.',
     CP_TOOL, CP_SECTIONS, CP_FAQ, DOC_LIBS, CP_JS,
     [('/split-pdf/', 'Split PDF'), ('/jpg-to-pdf/', 'JPG to PDF'), ('/image-compressor/', 'Image compressor'), ('/merge-pdf/', 'Merge PDF')],
     'Compress PDF', 'Free browser-based tool that reduces PDF file size, with an optional target size in KB, without uploading the file.')

# ================= PNG TO PDF =================
PN_TOOL = JP_TOOL.replace('JPG, PNG or WebP. Paste with Ctrl+V.', 'PNG works best. JPG and WebP also work. Paste with Ctrl+V.').replace('Drop images here, or tap to choose', 'Drop PNG images here, or tap to choose')
PN_JS = JP_JS.replace('Drop images here, or tap to choose', 'Drop PNG images here, or tap to choose').replace("'jp-set'", "'pn-set'").replace("'images'", "'png-images'")
PN_SECTIONS = """  <h2>How to convert PNG to PDF</h2>
  <ol>
    <li>Choose one or more PNG images. Screenshots, scans and graphics all work.</li>
    <li>Use the arrows to put the pages in order, rotate any that are sideways, and remove those you do not need.</li>
    <li>Choose the page size (A4, Letter or the same size as the image), then press <strong>Create PDF</strong> and download it.</li>
  </ol>
  <p>The conversion runs in your browser, so your images are not uploaded.</p>
  <h2>What happens to transparent PNGs?</h2>
  <p>PDF pages have a background, so the transparent parts of a PNG are filled with white. Logos and signatures on a transparent background will appear on a white page.</p>
  <div class="note"><p><strong>Keep screenshots sharp.</strong> Pages are stored as compressed images. Choose <strong>High</strong> quality for screenshots with small text and <strong>Small</strong> if the PDF must stay under an upload limit. You can also shrink the finished file with <a href="/compress-pdf/">Compress PDF</a>.</p></div>
  <p>Need the reverse? <a href="/pdf-to-jpg/">PDF to JPG</a> turns PDF pages back into PNG or JPG images. For JPG photos, use <a href="/jpg-to-pdf/">JPG to PDF</a>.</p>"""
PN_FAQ = [("How do I convert PNG to PDF?", "Add your PNG files, put them in order, choose the page size and press Create PDF. Then download the PDF."),
          ("Is this PNG to PDF converter free?", "Yes. It is free, needs no account and adds no watermark."),
          ("Are my images uploaded?", "No. The PDF is made in your browser, so the images stay on your device."),
          ("Can I combine several PNG files into one PDF?", "Yes. Add them all, arrange the order, and each image becomes one page."),
          ("What happens to transparent areas?", "They become white, because PDF pages have a solid background."),
          ("How do I make the PDF smaller?", "Choose the Small quality before you create the PDF, or run the result through Compress PDF.")]
page('png-to-pdf', 'PNG to PDF Converter: Combine PNG Images into One PDF (Free, No Upload)',
     'Convert PNG images to PDF free in your browser. Combine screenshots and scans into one PDF, reorder and rotate pages, choose A4 or Letter. No upload, no watermark.',
     'PNG to PDF Converter', 'PNG लाई PDF मा बदल्नुहोस्', 'File tool',
     'Turn PNG screenshots and images into one PDF. Reorder and rotate pages, choose A4 or Letter. Everything happens in your browser.',
     PN_TOOL, PN_SECTIONS, PN_FAQ,
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>', PN_JS,
     [('/jpg-to-pdf/', 'JPG to PDF'), ('/compress-pdf/', 'Compress PDF'), ('/merge-pdf/', 'Merge PDF'), ('/pdf-to-jpg/', 'PDF to JPG')],
     'PNG to PDF Converter', 'Free browser-based tool that converts PNG images into a single PDF without uploading them.')
print('pdf tools 2 ok')
