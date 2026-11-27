#!/usr/bin/env python3
"""Sign PDF tool (client-side: pdf.js view + pdf-lib embed). Run from repo root."""
_pro = open('scripts/make_pro_tools.py', encoding='utf-8').read()
exec(_pro[:_pro.index('# ================= IMAGE COMPRESSOR')])
exec(_pro[_pro.index('# ================= SHARED PIECES'):_pro.index('# ================= JPG TO PDF (pro)')])

NE['sign-pdf'] = {'h2': 'नेपालीमा: PDF मा सही (हस्ताक्षर) कसरी गर्ने?',
  'steps': ['PDF फाइल छान्नुहोस्।',
            'औँला वा माउसले आफ्नो सही कोर्नुहोस्, वा सहीको फोटो अपलोड गर्नुहोस्। अनि "Use signature" थिच्नुहोस्।',
            'पेज छानेर "Place signature on this page" थिच्नुहोस्। सहीलाई तानेर ठाउँमा राख्नुहोस्, कुनामा तानेर ठूलो-सानो बनाउनुहोस्।',
            '"Sign PDF" थिचेर हस्ताक्षर गरिएको PDF डाउनलोड गर्नुहोस्।'],
  'note': 'यसले PDF मा तपाईंको सहीको तस्बिर राख्छ। यो डिजिटल सर्टिफिकेट भएको हस्ताक्षर होइन। कार्यालयले खास किसिमको हस्ताक्षर मागेको छ भने उसको निर्देशन पालना गर्नुहोस्। PDF र सही इन्टरनेटमा अपलोड हुँदैनन्।',
  'faq': [('मोबाइलबाट PDF मा सही कसरी गर्ने?', 'ब्राउजरमा Sign PDF खोल्नुहोस्, PDF छान्नुहोस्, औँलाले सही कोर्नुहोस्, पेजमा राख्नुहोस् र डाउनलोड गर्नुहोस्।'),
          ('मेरो सही सुरक्षित छ?', 'छ। सबै काम तपाईंको ब्राउजरमै हुन्छ, सही वा PDF कतै पठाइँदैन।'),
          ('धेरै पेजमा सही गर्न मिल्छ?', 'मिल्छ। हरेक पेजमा गएर "Place signature on this page" थिच्नुहोस्।')]}

SG_TOOL = KIT_CSS + '''<style>
.tk-sigpad{position:relative;border:2px dashed var(--line);border-radius:var(--r);background:#fff;margin:8px 0}
.tk-sigpad canvas{display:block;width:100%;height:170px;touch-action:none;cursor:crosshair}
.tk-sigpad small{position:absolute;left:12px;bottom:8px;color:#8a8478;pointer-events:none;font-size:.85rem}
.tk-prev{display:flex;align-items:center;gap:12px;margin:8px 0;padding:10px;border:1px solid var(--line);border-radius:var(--r);background:#fff}
.tk-prev img{height:54px;max-width:60%;object-fit:contain}
.tk-nav{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:10px 0}
.tk-nav .tk-b{min-width:56px}.tk-nav span{font-weight:700}
.tk-pv{position:relative;border:1px solid var(--line);background:#fff;border-radius:8px;overflow:hidden;touch-action:pan-y;line-height:0}
.tk-pv canvas{display:block;width:100%;height:auto}
.tk-sg{position:absolute;border:2px solid #c0392b;border-radius:4px;touch-action:none;cursor:move;box-sizing:border-box;background:rgba(255,255,255,.15)}
.tk-sg img{display:block;width:100%;height:auto;pointer-events:none;user-select:none}
.tk-sg .rs{position:absolute;right:-12px;bottom:-12px;width:26px;height:26px;border-radius:50%;background:#c0392b;border:3px solid #fff;cursor:nwse-resize;touch-action:none}
#sigarea .tk-bar,#placearea .tk-bar{position:static;margin:12px 0 0;padding:0;border:0;background:none}
.tk-note2{margin:8px 0;color:var(--ink2);font-size:.95rem;line-height:1.5}
</style>
  <div class="conv tk" id="app">
    ''' + head(['1. Add PDF', '2. Place signature', '3. Download']) + '\n    ' + dz(False, 'Drop a PDF here, or tap to choose', 'The PDF and your signature stay on your device.', 'application/pdf,.pdf', False) + '''
    <div id="panel" hidden>
      <p class="tk-sec" id="fnm"></p>
      <div id="sigarea">
        ''' + chips('smode', 'sml', 'Step 1: create your signature', [('draw', 'Draw'), ('img', 'Upload image')], 'draw') + '''
        <div id="drawbox">
          <div class="tk-sigpad"><canvas id="pad" aria-label="Signature drawing area"></canvas><small id="padh">Sign here with your finger or mouse</small></div>
          ''' + chips('ink', 'inkl', 'Ink colour', [('#111111', 'Black'), ('#1a3fa0', 'Blue')], '#111111') + '''
        </div>
        <div id="upbox" hidden>
          <p class="tk-note2">Use a clear photo of your signature on white paper. The white background is removed.</p>
          <label class="tk-b" for="sigfile" style="display:inline-flex">Choose signature image</label><input id="sigfile" type="file" accept="image/*" hidden>
        </div>
        <div class="tk-bar"><div class="tk-sum" id="sgmsg"></div><button class="tk-b" id="padclr" type="button">Clear</button><button class="tk-b pri" id="use" type="button">Use signature</button></div>
      </div>
      <div id="placearea" hidden>
        <p class="tk-sec">Step 2: place it on the page</p>
        <div class="tk-prev"><img id="sigprev" alt="Your signature"><button class="tk-b" id="chg" type="button">Change signature</button></div>
        <div class="tk-nav"><button class="tk-b" id="prev" type="button" aria-label="Previous page">←</button><span id="pgl"></span><button class="tk-b" id="next" type="button" aria-label="Next page">→</button></div>
        <div class="tk-pv" id="pv"><canvas id="pc"></canvas><div class="tk-sg" id="sg" hidden><img id="sgi" alt=""><span class="rs" id="rs" aria-label="Resize"></span></div></div>
        <p class="tk-note2" id="pnote">Tap the button to add your signature to this page, then drag it into position. Drag the red dot to resize.</p>
        <div class="tk-bar"><button class="tk-b pri" id="place" type="button">Place signature on this page</button><button class="tk-b" id="rm" type="button" hidden>Remove from this page</button></div>
      </div>
      <div class="tk-row" id="pw" hidden style="margin-top:12px"><div class="f"><label class="l" for="pwi">This PDF needs a password</label><input class="tk-in" id="pwi" type="password" autocomplete="off"></div></div>
      <p class="tk-live" id="live" aria-live="polite"></p>
      <div class="tk-bar"><div class="tk-sum" id="sum"></div><button class="tk-b" id="clr" type="button">Start over</button><button class="tk-b pri" id="go" type="button" hidden>Sign PDF</button><a class="tk-b pri" id="dl" download="signed.pdf" href="#" hidden>Download signed PDF</a></div>
    </div>
  </div>'''

SG_JS = r"""(function(){""" + BASE_JS + r"""
  var file=null,buf=null,pdf=null,cur=1,sig=null,pl={},url=null,rot={},pad=$('pad'),px=pad.getContext('2d'),drawn=false,down=false,last=null,renderId=0;
  function isPdf(f){return f.type==='application/pdf'||/\.pdf$/i.test(f.name);}
  function sizePad(){var r=pad.getBoundingClientRect(),d=Math.min(window.devicePixelRatio||1,2);if(!r.width)return;var keep=drawn?px.getImageData(0,0,pad.width,pad.height):null;pad.width=Math.round(r.width*d);pad.height=Math.round(r.height*d);px.setTransform(d,0,0,d,0,0);px.lineCap='round';px.lineJoin='round';if(keep)px.putImageData(keep,0,0);}
  function pt(e){var r=pad.getBoundingClientRect();return {x:e.clientX-r.left,y:e.clientY-r.top};}
  pad.addEventListener('pointerdown',function(e){e.preventDefault();pad.setPointerCapture(e.pointerId);down=true;last=pt(e);px.strokeStyle=val('ink');px.fillStyle=val('ink');px.beginPath();px.arc(last.x,last.y,1.4,0,6.3);px.fill();drawn=true;$('padh').hidden=true;});
  pad.addEventListener('pointermove',function(e){if(!down)return;e.preventDefault();var p=pt(e);px.strokeStyle=val('ink');px.lineWidth=2.8;px.beginPath();px.moveTo(last.x,last.y);px.lineTo(p.x,p.y);px.stroke();last=p;});
  ['pointerup','pointercancel'].forEach(function(n){pad.addEventListener(n,function(){down=false;});});
  function clearPad(){px.save();px.setTransform(1,0,0,1,0,0);px.clearRect(0,0,pad.width,pad.height);px.restore();drawn=false;$('padh').hidden=false;$('sgmsg').textContent='';}
  $('padclr').addEventListener('click',clearPad);
  function setMode(){var m=val('smode');$('drawbox').hidden=m!=='draw';$('upbox').hidden=m!=='img';$('padclr').hidden=m!=='draw';$('sgmsg').textContent='';if(m==='draw')setTimeout(sizePad,0);}
  [].forEach.call(document.querySelectorAll('input[name=smode]'),function(r){r.addEventListener('change',setMode);});
  function trim(c){var x=c.getContext('2d'),w=c.width,h=c.height,d=x.getImageData(0,0,w,h).data,x0=w,y0=h,x1=-1,y1=-1;
    for(var y=0;y<h;y++)for(var xx=0;xx<w;xx++){if(d[(y*w+xx)*4+3]>20){if(xx<x0)x0=xx;if(xx>x1)x1=xx;if(y<y0)y0=y;if(y>y1)y1=y;}}
    if(x1<0)return null;var m=6;x0=Math.max(0,x0-m);y0=Math.max(0,y0-m);x1=Math.min(w-1,x1+m);y1=Math.min(h-1,y1+m);
    var o=document.createElement('canvas');o.width=x1-x0+1;o.height=y1-y0+1;o.getContext('2d').drawImage(c,x0,y0,o.width,o.height,0,0,o.width,o.height);return o;}
  function accept(c){var t=trim(c);if(!t){$('sgmsg').textContent='Draw or upload your signature first.';return;}
    sig={url:t.toDataURL('image/png'),w:t.width,h:t.height};$('sigprev').src=sig.url;$('sgi').src=sig.url;$('sigarea').hidden=true;$('placearea').hidden=false;step(1);
    Object.keys(pl).forEach(function(k){pl[k].fh=null;});showPage();}
  $('use').addEventListener('click',function(){if(val('smode')==='draw'){if(!drawn){$('sgmsg').textContent='Draw your signature first.';return;}accept(pad);}else{$('sgmsg').textContent=upCanvas?'':'Choose a signature image first.';if(upCanvas)accept(upCanvas);}});
  var upCanvas=null;
  $('sigfile').addEventListener('change',async function(){var f=this.files[0];if(!f)return;
    try{var b=await createImageBitmap(f,{imageOrientation:'from-image'}),s=Math.min(1,900/Math.max(b.width,b.height)),c=document.createElement('canvas');c.width=Math.round(b.width*s);c.height=Math.round(b.height*s);var x=c.getContext('2d');x.drawImage(b,0,0,c.width,c.height);
      var im=x.getImageData(0,0,c.width,c.height),d=im.data;for(var i=0;i<d.length;i+=4){var l=.299*d[i]+.587*d[i+1]+.114*d[i+2],a=l>225?0:(l>150?(225-l)/75*255:255);d[i+3]=Math.min(d[i+3],a);if(d[i+3]>0){d[i]=Math.min(d[i],40);d[i+1]=Math.min(d[i+1],40);d[i+2]=Math.min(d[i+2],60);}}
      x.putImageData(im,0,0);upCanvas=c;$('sgmsg').textContent='Image ready. Press Use signature.';}catch(e){upCanvas=null;$('sgmsg').textContent='Could not read that image.';}});
  $('chg').addEventListener('click',function(){$('placearea').hidden=true;$('sigarea').hidden=false;setMode();sizePad();});
  /* ---- PDF viewing ---- */
  bind(async function(fl){file=fl[0];$('live').textContent='Opening PDF...';pl={};rot={};cur=1;$('dl').hidden=true;$('go').hidden=true;
    try{buf=await file.arrayBuffer();var L=window.pdfjsLib;L.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';pdf=await L.getDocument({data:buf.slice(0)}).promise;
      $('panel').hidden=false;$('fnm').textContent=file.name+' · '+pdf.numPages+' page'+(pdf.numPages>1?'s':'')+' · '+kb(file.size);$('live').textContent='';mini(true,'Change PDF');$('sigarea').hidden=false;$('placearea').hidden=true;setMode();setTimeout(sizePad,0);step(1);updateGo();
    }catch(e){$('panel').hidden=true;$('live').textContent=(e&&e.name==='PasswordException')?'This PDF is password-protected. Remove the password first, then try again.':'This PDF could not be opened. It may be damaged.';}
  },isPdf);
  async function showPage(){
    var id=++renderId;$('pgl').textContent='Page '+cur+' of '+pdf.numPages;$('prev').disabled=cur<=1;$('next').disabled=cur>=pdf.numPages;
    var p=await pdf.getPage(cur);if(id!==renderId)return;rot[cur]=(p.rotate%360)!==0;
    var cw=$('pv').clientWidth||320,d=Math.min(window.devicePixelRatio||1,2),b=p.getViewport({scale:1}),sc=cw*d/b.width,vp=p.getViewport({scale:sc}),c=$('pc');c.width=Math.floor(vp.width);c.height=Math.floor(vp.height);
    var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);await p.render({canvasContext:x,viewport:vp}).promise;if(id!==renderId)return;
    $('place').hidden=!!rot[cur];$('pnote').textContent=rot[cur]?'This page is rotated, so signing it is not supported. Choose another page.':'Tap the button to add your signature to this page, then drag it into position. Drag the red dot to resize.';
    drawSig();}
  $('prev').addEventListener('click',function(){if(cur>1){cur--;showPage();}});$('next').addEventListener('click',function(){if(cur<pdf.numPages){cur++;showPage();}});
  function drawSig(){var o=pl[cur],g=$('sg');if(!o||!sig){g.hidden=true;$('rm').hidden=true;$('place').textContent='Place signature on this page';return;}
    g.hidden=false;$('rm').hidden=false;$('place').hidden=true;g.style.left=o.fx*100+'%';g.style.top=o.fy*100+'%';g.style.width=o.fw*100+'%';}
  function fh(o){var pv=$('pv');return ($('sg').offsetHeight||o.fw*pv.clientWidth*sig.h/sig.w)/pv.clientHeight;}
  function updateGo(){var n=Object.keys(pl).length;$('go').hidden=!n;$('dl').hidden=true;$('sum').innerHTML=n?'<b>'+n+'</b> page'+(n>1?'s':'')+' to sign':'';}
  $('place').addEventListener('click',function(){var fw=.3,r=sig.h/sig.w,pvw=$('pv').clientWidth,pvh=$('pv').clientHeight,h=fw*pvw*r/pvh;pl[cur]={fx:.55,fy:Math.max(0,Math.min(.8,1-h-.04)),fw:fw};drawSig();updateGo();step(1);});
  $('rm').addEventListener('click',function(){delete pl[cur];$('place').hidden=!!rot[cur];drawSig();updateGo();});
  var mode=null,st=null;
  $('sg').addEventListener('pointerdown',function(e){var o=pl[cur];if(!o)return;e.preventDefault();$('sg').setPointerCapture(e.pointerId);mode=e.target.id==='rs'?'rs':'mv';st={x:e.clientX,y:e.clientY,fx:o.fx,fy:o.fy,fw:o.fw};});
  $('sg').addEventListener('pointermove',function(e){if(!mode)return;var o=pl[cur],pv=$('pv'),W=pv.clientWidth,H=pv.clientHeight,dx=(e.clientX-st.x)/W,dy=(e.clientY-st.y)/H,r=sig.h/sig.w;
    if(mode==='mv'){o.fx=Math.max(0,Math.min(1-o.fw,st.fx+dx));var h=o.fw*W*r/H;o.fy=Math.max(0,Math.min(1-h,st.fy+dy));}
    else{var fw=Math.max(.08,Math.min(1-st.fx,st.fw+dx)),h2=fw*W*r/H;if(st.fy+h2>1)fw=(1-st.fy)*H/(W*r);o.fw=Math.max(.08,fw);}
    drawSig();});
  ['pointerup','pointercancel'].forEach(function(n){$('sg').addEventListener(n,function(){mode=null;});});
  window.addEventListener('resize',function(){if(pdf&&!$('placearea').hidden)showPage();});
  $('go').addEventListener('click',async function(){
    var PL=window.PDFLib;if(!PL){$('live').textContent='The PDF library did not load. Check your connection and reload.';return;}
    $('go').disabled=true;$('live').textContent='Signing...';
    try{var doc=await PL.PDFDocument.load(buf),img=await doc.embedPng(await (await fetch(sig.url)).arrayBuffer()),pages=doc.getPages();
      Object.keys(pl).forEach(function(k){var o=pl[k],pg=pages[+k-1],s=pg.getSize(),w=o.fw*s.width,h=w*sig.h/sig.w;pg.drawImage(img,{x:o.fx*s.width,y:s.height-o.fy*s.height-h,width:w,height:h});});
      var blob=new Blob([await doc.save()],{type:'application/pdf'});if(url)URL.revokeObjectURL(url);url=URL.createObjectURL(blob);
      var a=$('dl');a.href=url;a.download=file.name.replace(/\.pdf$/i,'')+'-signed.pdf';a.hidden=false;$('go').hidden=true;$('sum').innerHTML='<b>'+Object.keys(pl).length+'</b> page'+(Object.keys(pl).length>1?'s':'')+' signed · <b>'+kb(blob.size)+'</b>';$('live').textContent='Done. Your signed PDF is ready.';step(2);
    }catch(e){$('live').textContent=(e&&/encrypt/i.test(String(e.message)))?'This PDF is password-protected. Remove the password first.':'Something went wrong while signing this PDF.';}
    $('go').disabled=false;});
  $('clr').addEventListener('click',function(){file=null;buf=null;pdf=null;pl={};sig=null;clearPad();$('panel').hidden=true;$('live').textContent='';mini(false,'Drop a PDF here, or tap to choose');step(0);});
  step(0);
})();"""

SG_SECTIONS = """  <h2>How to sign a PDF online</h2>
  <ol>
    <li>Choose your PDF.</li>
    <li>Draw your signature with your finger or mouse, or upload a photo of your signature on white paper, then press <strong>Use signature</strong>.</li>
    <li>Open the page you want to sign and press <strong>Place signature on this page</strong>. Drag the signature into position and drag the red dot to resize it. Repeat on other pages if needed.</li>
    <li>Press <strong>Sign PDF</strong> and download the signed file.</li>
  </ol>
  <p>The PDF and your signature are handled in your browser. Nothing is uploaded, and no account is needed.</p>
  <h2>What kind of signature is this?</h2>
  <p>The tool places an image of your handwritten signature on the page, like signing a printout and scanning it. It is not a digital certificate signature. If an office, bank or court asks for a specific type of electronic signature, follow its instructions.</p>
  <div class="note"><p><strong>Tips.</strong> Sign on a phone for the most natural result. For a photo of a paper signature, use a dark pen on white paper in good light. If the file is too large to upload afterwards, use <a href="/compress-pdf/">Compress PDF</a>. To keep only the pages you need, use <a href="/split-pdf/">Split PDF</a>.</p></div>"""
SG_FAQ = [("Is this Sign PDF tool free?", "Yes. It is free, needs no account and adds no watermark."),
          ("Is my PDF or signature uploaded to a server?", "No. The PDF is opened and signed in your browser, and your signature is not stored or sent anywhere."),
          ("Can I sign a PDF on my phone?", "Yes. Draw your signature with your finger, place it on the page and download the file."),
          ("Can I sign more than one page?", "Yes. Go to each page and press Place signature on this page. Pages without a signature stay unchanged."),
          ("Is this a legally binding digital signature?", "It adds an image of your signature. Whether that is accepted depends on the office or form, so follow the instructions you were given."),
          ("Why can I not sign some pages?", "Pages that are rotated in the PDF are not supported yet. Choose another page, or rotate the file before signing."),
          ("Does it work with password-protected PDFs?", "No. Remove the password first, then add the file.")]
page('sign-pdf', 'Sign PDF Online: Add Your Signature to a PDF (Free, No Upload)',
     'Sign a PDF free in your browser. Draw or upload your signature, place it on any page, and download. No upload, no sign-up, no watermark. Works on phones.',
     'Sign PDF', 'PDF मा सही गर्नुहोस्', 'File tool',
     'Add your signature to a PDF. Draw it or upload a photo, drag it into place and download. Your file and signature stay on your device.',
     SG_TOOL, SG_SECTIONS, SG_FAQ,
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>', SG_JS,
     [('/compress-pdf/', 'Compress PDF'), ('/merge-pdf/', 'Merge PDF'), ('/split-pdf/', 'Split PDF'), ('/jpg-to-pdf/', 'JPG to PDF')],
     'Sign PDF', 'Free browser-based tool that adds an image of your signature to a PDF without uploading the file.')
print('sign pdf ok')
