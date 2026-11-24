#!/usr/bin/env python3
"""Pro versions of /image-compressor/ and /photo-resizer/ (client-side). Reuses page() from make_file_tools.py.
Run from repo root: python3 scripts/make_pro_tools.py"""
_src = open('scripts/make_file_tools.py', encoding='utf-8').read()
exec(_src[:_src.index('# ---------------- JPG to PDF')])
exec(_src[_src.index('J_SECTIONS = '):_src.index('J_JS = ')])
exec(_src[_src.index('P_SECTIONS = '):_src.index('P_JS = ')])

KIT_CSS = '''<style>
.tk{--r:14px}
#nepali{font-family:'Noto Sans Devanagari','Tiro Devanagari Hindi','Mukta',system-ui,sans-serif;line-height:1.85}#nepali h2{font-family:inherit;font-weight:700}
.tk [hidden]{display:none!important}
.tk-drop.mini{padding:14px 12px}.tk-drop.mini svg,.tk-drop.mini small{display:none}.tk-drop.mini b{margin:0;font-size:.98rem}.tk-drop.mini .tk-btns{margin-top:8px}
.tk-chips{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 4px}
.tk-chips label{position:relative}
.tk-chips input{position:absolute;opacity:0;inset:0;width:100%;height:100%;margin:0;cursor:pointer}
.tk-chips span{display:inline-block;min-height:44px;line-height:44px;padding:0 15px;border:1.5px solid var(--line);border-radius:999px;font-weight:700;font-size:.92rem;color:var(--ink);background:var(--bg)}
.tk-chips input:checked+span{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.tk-chips input:focus-visible+span{outline:3px solid var(--red);outline-offset:2px}
.tk-trust{display:flex;flex-wrap:wrap;gap:8px 16px;margin:0 0 14px;padding:0;list-style:none;font-size:.84rem;font-weight:600;color:var(--ink2)}
.tk-trust li::before{content:"✓ ";color:var(--ok);font-weight:800}
.tk-steps{display:flex;gap:6px;list-style:none;margin:0 0 14px;padding:0;font-size:.78rem;font-weight:700;color:var(--mute)}
.tk-steps li{flex:1;text-align:center;padding:7px 4px;border-bottom:3px solid var(--line)}
.tk-steps li.on{color:var(--ink);border-color:var(--red)}
.tk-steps li.done{color:var(--ok);border-color:var(--ok)}
.tk-drop{display:block;position:relative;border:2px dashed var(--line);border-radius:var(--r);padding:30px 16px;text-align:center;background:var(--bg);cursor:pointer;transition:border-color .15s,background .15s}
.tk-drop:hover,.tk-drop.over,.tk-drop:focus-within{border-color:var(--red)}
.tk-drop.over{background:var(--note)}
.tk-drop svg{width:44px;height:44px;color:var(--red)}
.tk-drop b{display:block;font-size:1.08rem;color:var(--ink);margin-top:6px}
.tk-drop small{display:block;color:var(--mute);font-size:.86rem;margin-top:2px}
.tk-drop input{position:absolute;opacity:0;width:1px;height:1px;left:0;top:0}
.tk-btns{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;justify-content:center}
.tk-b{font:inherit;font-weight:700;min-height:46px;padding:0 20px;border-radius:12px;border:1.5px solid var(--line);background:transparent;color:var(--ink);cursor:pointer;display:inline-flex;align-items:center;justify-content:center;text-decoration:none}
.tk-b.pri{background:var(--red);border-color:var(--red);color:#fff}
.tk-b:hover,.tk-b:focus-visible{border-color:var(--red);outline:none}
.tk-b:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.tk-b[disabled],.tk-b[aria-disabled=true]{opacity:.5;pointer-events:none}
.tk-sec{font-size:.74rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);margin:18px 0 4px}
.tk-row{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end}
.tk-row .f{flex:1 1 130px}.tk-row label.l{display:block;font-size:.8rem;font-weight:700;color:var(--mute);margin-bottom:4px}
.tk-in{width:100%;font:inherit;font-size:1.05rem;font-weight:700;padding:11px 12px;border-radius:10px;border:1.5px solid var(--line);background:var(--bg);color:var(--ink);min-height:46px}
.tk-in:focus{outline:2px solid var(--red);outline-offset:1px}
.tk-chk{display:flex;align-items:center;gap:10px;min-height:44px;font-weight:600;color:var(--ink2);cursor:pointer}
.tk-chk input{width:20px;height:20px;accent-color:var(--red)}
.tk-files{list-style:none;margin:12px 0;padding:0;display:grid;gap:10px}
.tk-file{display:grid;grid-template-columns:60px 1fr;gap:12px;align-items:center;background:var(--bg);border:1px solid var(--line);border-radius:var(--r);padding:10px}
.tk-file img{width:60px;height:60px;object-fit:cover;border-radius:10px;background:var(--line)}
.tk-file .nm{font-weight:700;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:.95rem}
.tk-file .st{font-size:.88rem;color:var(--ink2)}
.tk-file .st b{color:var(--ok)}
.tk-file .st.bad b{color:var(--gold)}
.tk-file .ac{grid-column:1/-1;display:flex;gap:8px;flex-wrap:wrap}
.tk-file .tk-b{min-height:40px;padding:0 14px;font-size:.88rem}
.tk-cmp{position:relative;margin:12px 0;border-radius:var(--r);overflow:hidden;border:1px solid var(--line);background:repeating-conic-gradient(var(--line) 0 25%,var(--card) 0 50%) 0 0/16px 16px;line-height:0;touch-action:none}
.tk-cmp img{width:100%;height:auto;display:block;max-height:420px;object-fit:contain;background:var(--card)}
.tk-cmp .top{position:absolute;inset:0;clip-path:inset(0 50% 0 0)}
.tk-cmp .top img{height:100%}
.tk-cmp .bar{position:absolute;top:0;bottom:0;width:3px;background:#fff;box-shadow:0 0 0 1px rgba(0,0,0,.3);left:50%;pointer-events:none}
.tk-cmp .tag{position:absolute;top:8px;font-size:.74rem;font-weight:800;line-height:1.3;background:rgba(0,0,0,.65);color:#fff;padding:3px 9px;border-radius:99px}
.tk-cmp .tag.a{left:8px}.tk-cmp .tag.b{right:8px}
.tk-cmp input{position:absolute;inset:0;width:100%;height:100%;opacity:0;cursor:ew-resize;margin:0}
.tk-bar{position:sticky;bottom:0;z-index:5;display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:var(--card);border-top:1px solid var(--line);margin:14px -18px -18px;padding:12px 18px;border-radius:0 0 16px 16px}
.tk-sum{flex:1 1 160px;font-size:.88rem;color:var(--ink2)}
.tk-sum b{color:var(--ok)}
.tk-live{min-height:1.4em;font-size:.85rem;color:var(--mute);margin:8px 0 0}
.tk-sw{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.tk-sw label{position:relative;width:44px;height:44px}
.tk-sw input[type=radio]{position:absolute;inset:0;opacity:0;width:100%;height:100%;margin:0;cursor:pointer}
.tk-sw i{display:block;width:100%;height:100%;border-radius:50%;border:2px solid var(--line)}
.tk-sw input:checked+i{border-color:var(--red);box-shadow:0 0 0 3px var(--card),0 0 0 5px var(--red)}
.tk-sw input:focus-visible+i{outline:3px solid var(--ink);outline-offset:3px}
.tk-sw input[type=color]{position:static;width:44px;height:44px;border:0;padding:0;background:none;cursor:pointer;opacity:1}
.tk-stage{position:relative;display:inline-block;max-width:100%;line-height:0}
.tk-stage canvas{max-width:100%;height:auto;border:1px solid var(--line);border-radius:12px;touch-action:none;cursor:grab;background:#fff}
.tk-guide{position:absolute;inset:0;pointer-events:none;display:none;overflow:hidden;border-radius:12px}
.tk-guide.on{display:block}
.tk-guide::before{content:"";position:absolute;left:50%;top:48%;width:52%;height:62%;transform:translate(-50%,-50%);border:2px dashed rgba(255,255,255,.95);border-radius:50%;box-shadow:0 0 0 1px rgba(0,0,0,.5),0 0 0 999px rgba(0,0,0,.18)}
@media (max-width:520px){.tk-drop{padding:26px 12px}.tk-bar{margin:14px -14px -14px;padding:10px 14px}.conv{padding:14px}}
</style>'''

UP_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5"/><path d="M4 15v3a2 2 0 002 2h12a2 2 0 002-2v-3"/></svg>'


# ================= NEPALI SECTIONS (defined before pages are built via NE global) =================
NE = {
 'photo-resizer': {'h2': 'नेपालीमा: फोटो र हस्ताक्षरको साइज कसरी मिलाउने?',
  'steps': ['माथि "Choose image" थिचेर फोटो वा हस्ताक्षरको तस्बिर छान्नुहोस् (मोबाइलमा "Take photo" बाट क्यामेराले पनि खिच्न सकिन्छ)।',
            'फारमले मागेको साइज (चौडाइ र उचाइ पिक्सेल वा मिलिमिटरमा) र अधिकतम KB राख्नुहोस्।',
            'फोटोलाई औँलाले तानेर ठाउँमा मिलाउनुहोस्, चाहिए ज्युम गर्नुहोस्।',
            '"Download" थिच्नुहोस्। डाउनलोड गर्नुअघि नै फाइलको साइज KB मा देखिन्छ।'],
  'note': 'सूचना: यहाँ दिइएका साइज उदाहरण मात्र हुन्, आधिकारिक आवश्यकता होइनन्। हरेक फारम वा निकायले आफ्नै साइज र KB सीमा तोक्छ, त्यसैले सूचनामा लेखिएको मान प्रयोग गर्नुहोस् र अपलोड गर्नुअघि फोटो जाँच्नुहोस्। तपाईंको फोटो कुनै सर्भरमा पठाइँदैन, सबै काम तपाईंकै मोबाइल वा कम्प्युटरमा हुन्छ।',
  'faq': [('फोटो १०० KB भन्दा कम कसरी बनाउने?', 'अधिकतम फाइल साइजमा "100 KB" छान्नुहोस्। टुल आफैँ गुणस्तर घटाएर फाइल मिलाउँछ र अन्तिम साइज देखाउँछ।'),
          ('के मेरो फोटो इन्टरनेटमा अपलोड हुन्छ?', 'हुँदैन। सबै काम तपाईंको ब्राउजरमै हुन्छ, फोटो तपाईंको डिभाइसबाट बाहिर जाँदैन।'),
          ('हस्ताक्षरको साइज कसरी मिलाउने?', 'सेतो कागजमा हस्ताक्षर गरेर फोटो खिच्नुहोस्, "Show whole image" छानेर फारमले मागेको साइज र KB राख्नुहोस्।')]},
 'image-compressor': {'h2': 'नेपालीमा: फोटोको साइज KB मा कसरी घटाउने?',
  'steps': ['एक वा धेरै फोटो छान्नुहोस्, तान्नुहोस् वा पेस्ट गर्नुहोस्।',
            'फारमले मागेको सीमा (जस्तै 20, 50, 100 वा 200 KB) छान्नुहोस् वा आफ्नै संख्या लेख्नुहोस्।',
            'केही सेकेन्डमा नतिजा आउँछ। "Compare" थिचेर अघि र पछिको फोटो तुलना गर्नुहोस्।',
            '"Download" थिच्नुहोस्, धेरै फोटो भए "Download all (ZIP)" प्रयोग गर्नुहोस्।'],
  'note': 'सानो सीमा राख्दा फोटोको स्पष्टता घट्न सक्छ, त्यसैले डाउनलोड गरेपछि फोटो हेरेर जाँच्नुहोस्। फारमलाई निश्चित पिक्सेल साइज पनि चाहिन्छ भने "फोटो र हस्ताक्षर साइज" टुल प्रयोग गर्नुहोस्। तपाईंको फोटो अपलोड हुँदैन।',
  'faq': [('फोटो ५० KB मा कसरी ल्याउने?', 'फोटो थपेर "50 KB" छान्नुहोस्। टुलले सबैभन्दा राम्रो गुणस्तरमा त्यो सीमाभित्र पर्ने फाइल बनाउँछ।'),
          ('एकैपटक धेरै फोटो घटाउन सकिन्छ?', 'सकिन्छ। धेरै फोटो थप्नुहोस्, सबै एउटै सीमामा घटाइन्छन् र ZIP मा डाउनलोड गर्न मिल्छ।'),
          ('कुन फर्म्याट छान्ने?', 'JPG सबै ठाउँमा चल्छ र प्रायः फारमका लागि उपयुक्त हुन्छ। WebP सानो हुन्छ तर सबै वेबसाइटले स्वीकार गर्दैन।')]},
 'jpg-to-pdf': {'h2': 'नेपालीमा: फोटोबाट PDF कसरी बनाउने?',
  'steps': ['PDF बनाउनुपर्ने फोटो वा स्क्यान छान्नुहोस्। धेरै फोटो एकैपटक छान्न सकिन्छ।',
            'तीर (↑ ↓) ले पेजको क्रम मिलाउनुहोस्, ढल्किएको फोटो "Rotate" ले सोझ्याउनुहोस्।',
            'पेज साइज (A4 वा Letter), मार्जिन र गुणस्तर छान्नुहोस्।',
            '"Create PDF" थिचेर PDF बनाउनुहोस् र "Download PDF" बाट डाउनलोड गर्नुहोस्।'],
  'note': 'अपलोड सीमा भएका फारमका लागि गुणस्तरमा "Small" छान्नुहोस्। नागरिकता, पासपोर्ट वा बैंकका कागजात पनि सुरक्षित रहन्छन्, किनभने फाइल कुनै सर्भरमा जाँदैन।',
  'faq': [('धेरै फोटोलाई एउटै PDF मा कसरी राख्ने?', 'सबै फोटो थप्नुहोस्, क्रम मिलाउनुहोस् र "Create PDF" थिच्नुहोस्। हरेक फोटो एउटा पेज हुन्छ।'),
          ('PDF को साइज कसरी घटाउने?', 'गुणस्तरमा "Small" छान्नुहोस्। यसले फोटोको रिजोलुसन र गुणस्तर घटाएर फाइल सानो बनाउँछ।'),
          ('मोबाइलबाट चल्छ?', 'चल्छ। ग्यालरीबाट फोटो छान्न वा क्यामेराले खिच्न सकिन्छ।')]},
 'pdf-to-jpg': {'h2': 'नेपालीमा: PDF लाई फोटो (JPG) मा कसरी बदल्ने?',
  'steps': ['PDF फाइल छान्नुहोस् वा तानेर राख्नुहोस्।',
            'फोटोको गुणस्तर (Small, Standard वा High) र फर्म्याट (JPG वा PNG) छान्नुहोस्।',
            'सबै पेज चाहिँदैन भने "Pages" मा जस्तै 1-3, 5 लेख्नुहोस्; खाली छोड्दा सबै पेज बन्छन्।',
            '"Convert" थिच्नुहोस्, त्यसपछि पेज एक-एक गरी वा "Download all (ZIP)" बाट सबै डाउनलोड गर्नुहोस्।'],
  'note': 'पासवर्ड भएको PDF भए टुलले पासवर्ड सोध्छ। तपाईंको PDF कुनै सर्भरमा पठाइँदैन, सबै काम ब्राउजरमै हुन्छ। धेरै ठूला PDF पुराना मोबाइलमा ढिलो हुन सक्छन्।',
  'faq': [('PDF का केही पेज मात्र कसरी बदल्ने?', '"Pages" मा चाहिएको पेज नम्बर लेख्नुहोस्, जस्तै 2-4 वा 1, 3।'),
          ('पासवर्ड भएको PDF खुल्छ?', 'खुल्छ, तर पासवर्ड थाहा हुनुपर्छ। टुलले सोध्छ र त्यसपछि पेज बदल्छ।'),
          ('कुन गुणस्तर छान्ने?', 'धेरैजसो कामका लागि Standard पुग्छ। सानो अक्षर ठूलो गरेर हेर्नुपर्‍यो भने High छान्नुहोस्।')]},
 'image-converter': {'h2': 'नेपालीमा: PNG वा WebP लाई JPG मा कसरी बदल्ने?',
  'steps': ['PNG, WebP, GIF वा JPG फोटो छान्नुहोस्। एकैपटक धेरै छान्न सकिन्छ।',
            'कुन फर्म्याटमा बदल्ने (JPG, PNG वा WebP) र गुणस्तर छान्नुहोस्।',
            'चाहिए फोटोको सबैभन्दा लामो तर्फ 1920, 1280 वा 800 px मा सीमित गर्नुहोस्।',
            'नतिजा आफैँ आउँछ। एक-एक गरी वा "Download all (ZIP)" बाट डाउनलोड गर्नुहोस्।'],
  'note': 'JPG मा बदल्दा पारदर्शी भाग सेतो हुन्छ। तपाईंको फोटो कुनै सर्भरमा जाँदैन। निश्चित KB साइज चाहिएमा "Image Compressor" प्रयोग गर्नुहोस्।',
  'faq': [('PNG लाई JPG कसरी बनाउने?', 'PNG फोटो छान्नुहोस् र "Convert to" मा JPG छान्नुहोस्; नतिजा आफैँ आउँछ।'),
          ('WebP फोटो JPG मा बदल्न मिल्छ?', 'मिल्छ। WebP फाइल छानेर JPG छान्नुहोस्।'),
          ('बदल्दा गुणस्तर घट्छ?', 'JPG र WebP मा थोरै घट्न सक्छ। विवरण महत्त्वपूर्ण छ भने High छान्नुहोस्।')]},
 'file-tools': {'h2': 'नेपालीमा: कुन टुल कहिले प्रयोग गर्ने?',
  'steps': ['फारमले फोटो वा हस्ताक्षरको निश्चित साइज मागेमा: फोटो र हस्ताक्षर साइज टुल।',
            'फाइल धेरै ठूलो भएर अपलोड नभएमा: Image Compressor।',
            'धेरै फोटो वा स्क्यानबाट एउटै PDF चाहिएमा: JPG to PDF।',
            'PDF का पेजहरू फोटोका रूपमा चाहिएमा: PDF to JPG। साइटले JPG मात्र मान्ने भए: JPG Converter।'],
  'note': 'यी सबै टुल तपाईंको ब्राउजरमै चल्छन्, फाइल कुनै सर्भरमा पठाइँदैन, निःशुल्क छन् र वाटरमार्क लाग्दैन। अपलोड गर्नुअघि फारमको सूचनामा लेखिएको साइज र फर्म्याट जाँच्नुहोस्।',
  'faq': [('के यी टुल निःशुल्क छन्?', 'हो, निःशुल्क छन्, साइन-अप चाहिँदैन र वाटरमार्क लाग्दैन।'),
          ('मेरो फाइल सुरक्षित हुन्छ?', 'हुन्छ। फाइल तपाईंको डिभाइसबाट बाहिर जाँदैन, सबै काम ब्राउजरमै हुन्छ।')]},
}
# ================= IMAGE COMPRESSOR =================
IC_TOOL = KIT_CSS + '''
  <div class="conv tk" id="app">
    <ul class="tk-trust"><li>Stays on your device</li><li>Free, no sign-up</li><li>No watermark</li></ul>
    <ol class="tk-steps" id="steps"><li class="on">1. Add</li><li>2. Adjust</li><li>3. Download</li></ol>
    <label class="tk-drop" id="drop" for="file">''' + UP_SVG + '''<b>Drop images here, or tap to choose</b><small>JPG, PNG, WebP. You can also paste with Ctrl+V.</small>
      <input id="file" type="file" accept="image/*" multiple>
      <span class="tk-btns"><span class="tk-b pri">Choose images</span><span class="tk-b" id="cam">Take photo</span></span>
      <input id="camin" type="file" accept="image/*" capture="environment">
    </label>
    <div id="panel" hidden>
      <p class="tk-sec" id="tl">Target size (maximum)</p>
      <div class="tk-chips" id="chips" role="radiogroup" aria-labelledby="tl"></div>
      <div class="tk-row" id="cust" hidden><div class="f"><label class="l" for="ckb">Custom size in KB</label><input class="tk-in" id="ckb" type="number" min="5" max="5000" value="150" inputmode="numeric"></div></div>
      <div class="tk-row" style="margin-top:12px">
        <div class="f"><label class="l" for="fmt">Output format</label><select class="tk-in" id="fmt"><option value="image/jpeg">JPG (works everywhere)</option><option value="image/webp">WebP (smaller)</option></select></div>
        <div class="f"><label class="tk-chk" for="rs"><input type="checkbox" id="rs" checked>Reduce dimensions if needed</label></div>
      </div>
      <p class="tk-live" id="live" aria-live="polite"></p>
      <ul class="tk-files" id="files"></ul>
      <div id="cmpw" hidden>
        <p class="tk-sec">Compare (drag the slider)</p>
        <div class="tk-cmp" id="cmp"><img id="ci1" alt="Compressed"><div class="top" id="ctop"><img id="ci0" alt="Original"></div><span class="bar" id="cbar"></span><span class="tag a" id="ta"></span><span class="tag b" id="tb"></span><input type="range" min="0" max="100" value="50" id="crng" aria-label="Compare original and compressed"></div>
      </div>
      <div class="tk-bar"><div class="tk-sum" id="sum"></div><button class="tk-b" id="clr" type="button">Start over</button><button class="tk-b" id="zip" type="button" hidden>Download all (ZIP)</button></div>
    </div>
  </div>'''
IC_JS = r'''(function(){
  var $=function(i){return document.getElementById(i)},items=[],seq=0,token=0,urls=[],sel=null,drop=$('drop');
  var PRE=[[20,'20 KB'],[50,'50 KB'],[100,'100 KB'],[200,'200 KB'],[500,'500 KB'],[1024,'1 MB'],['c','Custom']];
  var S={t:100,fmt:'image/jpeg',rs:true};
  try{var sv=JSON.parse(localStorage.getItem('ic-set')||'null');if(sv&&sv.t)S=sv;}catch(e){}
  function save(){try{localStorage.setItem('ic-set',JSON.stringify(S));}catch(e){}}
  function kb(n){return n>=1048576?(n/1048576).toFixed(2)+' MB':Math.max(1,Math.round(n/1024))+' KB';}
  function step(n){[].forEach.call($('steps').children,function(li,i){li.className=i<n?'done':(i===n?'on':'');});}
  var ch=$('chips');PRE.forEach(function(p){var l=document.createElement('label'),v=String(p[0]),on=(S.t==='c'?v==='c':String(S.t)===v);
    l.innerHTML='<input type="radio" name="tgt" value="'+v+'"'+(on?' checked':'')+'><span>'+p[1]+'</span>';ch.appendChild(l);});
  $('cust').hidden=S.t!=='c';if(S.ckb)$('ckb').value=S.ckb;$('fmt').value=S.fmt;$('rs').checked=S.rs;
  function target(){return (S.t==='c'?Math.min(5000,Math.max(5,+$('ckb').value||100)):+S.t)*1024;}
  ch.addEventListener('change',function(e){S.t=e.target.value==='c'?'c':+e.target.value;$('cust').hidden=S.t!=='c';save();run();});
  $('ckb').addEventListener('input',function(){S.ckb=$('ckb').value;save();clearTimeout(window._ct);window._ct=setTimeout(run,450);});
  $('fmt').addEventListener('change',function(){S.fmt=this.value;save();run();});
  $('rs').addEventListener('change',function(){S.rs=this.checked;save();run();});
  function load(f){return window.createImageBitmap?createImageBitmap(f,{imageOrientation:'from-image'}):new Promise(function(ok,bad){var u=URL.createObjectURL(f),i=new Image();i.onload=function(){ok(i)};i.onerror=bad;i.src=u;});}
  function draw(b,s,fill){var w=b.width||b.naturalWidth,h=b.height||b.naturalHeight,c=document.createElement('canvas');c.width=Math.max(1,Math.round(w*s));c.height=Math.max(1,Math.round(h*s));var x=c.getContext('2d');if(fill){x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);}x.drawImage(b,0,0,c.width,c.height);return c;}
  function tb(c,t,q){return new Promise(function(r){c.toBlob(r,t,q)});}
  async function squeeze(b,T){
    var jpg=S.fmt==='image/jpeg',s=1,best=null,last=null;
    for(var round=0;round<9;round++){
      var c=draw(b,s,jpg),lo=.08,hi=.95;best=null;
      var top=await tb(c,S.fmt,hi);last={blob:top,w:c.width,h:c.height};if(top.size<=T){return last;}
      for(var k=0;k<7;k++){var m=(lo+hi)/2,bl=await tb(c,S.fmt,m);last={blob:bl,w:c.width,h:c.height};if(bl.size<=T){best={blob:bl,w:c.width,h:c.height};lo=m;}else hi=m;}
      if(best)return best;
      if(!S.rs)break;s*=.8;
    }
    return last;
  }
  function add(list){
    var fl=Array.from(list).filter(function(f){return /^image\//.test(f.type)||/\.(jpe?g|png|webp|gif|bmp)$/i.test(f.name)});if(!fl.length)return;
    Promise.all(fl.map(function(f){return load(f).then(function(b){var u=URL.createObjectURL(f);urls.push(u);items.push({id:++seq,f:f,b:b,u:u,r:null});},function(){});})).then(function(){
      $('panel').hidden=false;drop.querySelector('b').textContent='Add more images';drop.classList.add('mini');step(1);run();});
  }
  $('file').addEventListener('change',function(e){add(e.target.files);e.target.value='';});
  $('cam').addEventListener('click',function(e){e.preventDefault();e.stopPropagation();$('camin').click();});
  $('camin').addEventListener('change',function(e){add(e.target.files);e.target.value='';});
  ['dragover','dragenter'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.add('over');});});
  ['dragleave','drop'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.remove('over');if(n==='drop'&&e.dataTransfer)add(e.dataTransfer.files);});});
  document.addEventListener('paste',function(e){var fs=[].filter.call((e.clipboardData&&e.clipboardData.files)||[],function(f){return /^image\//.test(f.type)});if(fs.length){e.preventDefault();add(fs);}});
  async function run(){
    if(!items.length)return;var my=++token,T=target();$('live').textContent='Compressing...';
    items.forEach(function(it){it.r=null;});render();
    for(var i=0;i<items.length;i++){
      if(my!==token)return;await new Promise(function(r){setTimeout(r,0)});
      var it=items[i];try{var r=await squeeze(it.b,T);}catch(e){continue;}
      if(my!==token)return;it.r={blob:r.blob,w:r.w,h:r.h,u:URL.createObjectURL(r.blob),ok:r.blob.size<=T};urls.push(it.r.u);render();
    }
    if(my===token){$('live').textContent='';step(2);}
  }
  function render(){
    var ul=$('files');ul.innerHTML='';var tot0=0,tot1=0,done=0,miss=0;
    items.forEach(function(it){
      var li=document.createElement('li');li.className='tk-file';var r=it.r,ext=S.fmt==='image/webp'?'webp':'jpg',nm=it.f.name.replace(/\.[^.]+$/,'')+'-compressed.'+ext;
      var st;if(!r)st='<span class="st">Compressing...</span>';else{done++;tot0+=it.f.size;tot1+=r.blob.size;var pc=Math.min(99,Math.round((1-r.blob.size/it.f.size)*100));if(!r.ok)miss++;
        st='<span class="st'+(r.ok?'':' bad')+'">'+kb(it.f.size)+' → <b>'+kb(r.blob.size)+'</b> · '+(pc>0?'−'+pc+'%':'no saving')+' · '+r.w+'×'+r.h+' px'+(r.ok?'':' (above target)')+'</span>';}
      li.innerHTML='<img alt="" src="'+it.u+'"><div><div class="nm"></div>'+st+'</div><div class="ac">'+(r?'<a class="tk-b pri" download="'+nm.replace(/"/g,'')+'" href="'+r.u+'">Download</a><button type="button" class="tk-b" data-a="cmp" data-i="'+it.id+'">Compare</button>':'')+'<button type="button" class="tk-b" data-a="rm" data-i="'+it.id+'">Remove</button></div>';
      li.querySelector('.nm').textContent=it.f.name;ul.appendChild(li);});
    $('zip').hidden=done<2;
    $('sum').innerHTML=done?('<b>'+kb(tot0)+' → '+kb(tot1)+'</b> across '+done+' image'+(done>1?'s':'')+(miss?'. '+miss+' could not reach the target.':'.')):'';
    if(done&&!miss)$('live').textContent='';
    if(miss&&!$('rs').checked)$('live').textContent='Some images stay above the target. Turn on "Reduce dimensions if needed" to go smaller.';
  }
  $('files').addEventListener('click',function(e){var a=e.target.getAttribute&&e.target.getAttribute('data-a');if(!a)return;var id=+e.target.getAttribute('data-i');
    if(a==='rm'){items=items.filter(function(x){return x.id!==id});if(!items.length)reset();else render();$('cmpw').hidden=true;}
    if(a==='cmp'){var it=items.filter(function(x){return x.id===id})[0];if(!it||!it.r)return;$('ci0').src=it.u;$('ci1').src=it.r.u;$('ta').textContent='Original '+kb(it.f.size);$('tb').textContent='Compressed '+kb(it.r.blob.size);$('cmpw').hidden=false;$('cmpw').scrollIntoView({behavior:'smooth',block:'nearest'});}});
  function pos(v){$('ctop').style.clipPath='inset(0 '+(100-v)+'% 0 0)';$('cbar').style.left=v+'%';}
  $('crng').addEventListener('input',function(){pos(this.value);});
  function reset(){token++;items=[];urls.forEach(function(u){URL.revokeObjectURL(u)});urls=[];$('panel').hidden=true;$('files').innerHTML='';$('cmpw').hidden=true;drop.querySelector('b').textContent='Drop images here, or tap to choose';drop.classList.remove('mini');step(0);}
  $('clr').addEventListener('click',reset);
  $('zip').addEventListener('click',async function(){
    if(!window.JSZip){$('live').textContent='The ZIP library did not load. Download files one by one.';return;}
    var z=new JSZip(),ext=S.fmt==='image/webp'?'webp':'jpg',seen={};items.forEach(function(it){if(it.r){var n=it.f.name.replace(/\.[^.]+$/,'')+'-compressed',k=n;seen[n]=(seen[n]||0)+1;if(seen[n]>1)k=n+'-'+seen[n];z.file(k+'.'+ext,it.r.blob);}});
    $('live').textContent='Preparing ZIP...';var b=await z.generateAsync({type:'blob'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='compressed-images.zip';document.body.appendChild(a);a.click();a.remove();$('live').textContent='ZIP downloaded.';step(3);});
  step(0);
})();'''
page('image-compressor', 'Image Compressor: Reduce Photo Size to 50KB, 100KB, 200KB (Free, No Upload)',
     'Reduce JPG, PNG and WebP photo size to a target like 20KB, 50KB, 100KB or 200KB for Nepali online forms. Live before and after preview, free, no upload.',
     'Image Compressor: Reduce Photo Size to KB', 'फोटोको साइज KB मा घटाउनुहोस्', 'File tool',
     'Shrink a photo to the size an online form asks for. Pick a limit such as 50 KB or 100 KB, compare before and after, then download. Your image never leaves your device.',
     IC_TOOL, """  <h2>How to reduce an image to 50 KB or 100 KB</h2>
  <ol>
    <li>Add your photos by choosing them, dragging them in, taking a photo, or pasting.</li>
    <li>Pick the size limit the form asks for, or enter your own in KB. The result updates by itself.</li>
    <li>Check the before and after comparison, then download each file or all of them as a ZIP.</li>
  </ol>
  <p>The tool lowers the quality until the file fits. If quality alone is not enough and <em>Reduce dimensions if needed</em> is on, it also makes the picture a little smaller, so a very small limit such as 20 KB gives a smaller image.</p>
  <h2>When you need a small image</h2>
  <p>Online forms often limit uploads: job applications, exam and university forms, passport-size photos, signatures and scanned documents. Check the exact size and format on the form, then compress to just under that limit. Need exact pixel dimensions as well? Use the <a href="/photo-resizer/">photo and signature resizer</a>.</p>
  <div class="note"><p><strong>Check the result.</strong> Look at the compressed image before you submit it. Very small limits reduce detail, so a signature or ID photo should still be clear and readable. Turn off <em>Reduce dimensions</em> if the form needs the original pixel size.</p></div>""",
     [("How do I reduce a photo to 100 KB?", "Add the photo, choose 100 KB and wait a moment. The tool finds the best quality that fits and shows the new size, with a before and after comparison."),
      ("Is my photo uploaded to a server?", "No. Compression happens in your browser. The photo stays on your device."),
      ("Why is my compressed image smaller in pixels?", "To reach a very small limit the tool may reduce the dimensions as well as the quality. Turn off Reduce dimensions if you must keep the original size, or choose a larger limit."),
      ("Can I compress many images at once?", "Yes. Add several. Each is compressed to the same limit and you can download them one by one or as a ZIP."),
      ("Which format should I choose?", "JPG works everywhere and suits most forms. WebP gives smaller files but is not accepted by every website."),
      ("Does it work on a phone?", "Yes. You can choose from the gallery or take a photo with the camera.")],
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>', IC_JS,
     [('/photo-resizer/', 'Photo & signature resizer'), ('/image-converter/', 'JPG converter'), ('/jpg-to-pdf/', 'JPG to PDF'), ('/pdf-to-jpg/', 'PDF to JPG')],
     'Image Compressor', 'Free browser-based tool that reduces JPG, PNG and WebP photo size to a target number of KB, with before and after comparison, without uploading the image.')


# ================= PHOTO & SIGNATURE RESIZER =================
PR_TOOL = KIT_CSS + """
  <div class="conv tk" id="app">
    <ul class="tk-trust"><li>Stays on your device</li><li>Free, no sign-up</li><li>No watermark</li></ul>
    <ol class="tk-steps" id="steps"><li class="on">1. Add</li><li>2. Set size</li><li>3. Download</li></ol>
    <label class="tk-drop" id="drop" for="file">""" + UP_SVG + """<b>Drop a photo or signature here, or tap to choose</b><small>JPG, PNG, WebP. You can also paste with Ctrl+V.</small>
      <input id="file" type="file" accept="image/*">
      <span class="tk-btns"><span class="tk-b pri">Choose image</span><span class="tk-b" id="cam">Take photo</span></span>
      <input id="camin" type="file" accept="image/*" capture="user">
    </label>
    <div id="panel" hidden>
      <p class="tk-sec" id="pl">Common sizes (examples, check your form)</p>
      <div class="tk-chips" id="pre" role="radiogroup" aria-labelledby="pl"></div>
      <div class="tk-row" style="margin-top:12px">
        <div class="f"><label class="l" for="unit">Unit</label><select class="tk-in" id="unit"><option value="px">Pixels</option><option value="mm">Millimetres</option></select></div>
        <div class="f"><label class="l" for="w">Width</label><input class="tk-in" id="w" type="number" min="1" max="4000" value="413" inputmode="decimal"></div>
        <div class="f"><label class="l" for="h">Height</label><input class="tk-in" id="h" type="number" min="1" max="4000" value="531" inputmode="decimal"></div>
        <div class="f" id="dpiw" hidden><label class="l" for="dpi">Resolution (dpi)</label><input class="tk-in" id="dpi" type="number" min="72" max="600" value="300" inputmode="numeric"></div>
      </div>
      <p class="tk-live" id="eq"></p>
      <p class="tk-sec">Position</p>
      <div class="tk-stage" id="stage"><canvas id="cv" aria-label="Preview. Drag to move the picture."></canvas><div class="tk-guide" id="gd"></div></div>
      <p class="tk-live">Drag the picture to move it. Scroll or use the slider to zoom.</p>
      <div class="tk-row"><div class="f" style="flex:2 1 220px"><label class="l" for="zm">Zoom</label><input id="zm" type="range" min="1" max="4" step="0.01" value="1" style="width:100%;min-height:44px"></div></div>
      <div class="tk-btns" style="justify-content:flex-start">
        <button class="tk-b" id="rl" type="button">Rotate left</button><button class="tk-b" id="rr" type="button">Rotate right</button>
        <button class="tk-b" id="gdb" type="button" aria-pressed="false">Face guide</button><button class="tk-b" id="rst" type="button">Reset</button>
      </div>
      <div class="tk-row" style="margin-top:6px">
        <div class="f"><label class="l" for="kb">Maximum file size</label><select class="tk-in" id="kb"><option value="0">No limit</option><option value="20">20 KB</option><option value="50">50 KB</option><option value="100" selected>100 KB</option><option value="200">200 KB</option><option value="500">500 KB</option></select></div>
        <div class="f"><label class="l" for="fmt">Format</label><select class="tk-in" id="fmt"><option value="image/jpeg">JPG</option><option value="image/png">PNG (no KB limit)</option></select></div>
        <div class="f"><label class="l" for="mode">Fit</label><select class="tk-in" id="mode"><option value="fill">Fill the frame (crop)</option><option value="fit">Show whole image</option></select></div>
      </div>
      <p class="tk-sec" id="bgl">Background colour (for borders and transparent areas)</p>
      <div class="tk-sw" id="sw" role="radiogroup" aria-labelledby="bgl">
        <label><input type="radio" name="bg" value="#ffffff" checked aria-label="White"><i style="background:#fff"></i></label>
        <label><input type="radio" name="bg" value="#d6e6f7" aria-label="Light blue"><i style="background:#d6e6f7"></i></label>
        <label><input type="radio" name="bg" value="#f2f2f2" aria-label="Light grey"><i style="background:#f2f2f2"></i></label>
        <label><input type="radio" name="bg" value="#000000" aria-label="Black"><i style="background:#000"></i></label>
        <label title="Custom colour"><input type="color" id="bgc" value="#ffffff" aria-label="Custom background colour"></label>
      </div>
      <p class="tk-live" id="live" aria-live="polite"></p>
      <div class="tk-bar"><div class="tk-sum" id="sum">Preparing...</div><a class="tk-b pri" id="dl" download="photo.jpg" aria-disabled="true" href="#">Download</a></div>
    </div>
  </div>"""
PR_JS = r"""(function(){
  var $=function(i){return document.getElementById(i)},cv=$('cv'),x=cv.getContext('2d'),bmp=null,rot=0,rc=null,ox=0,oy=0,url=null,tok=0,bt=null,drop=$('drop');
  var PRE=[['413x531','Passport 35×45 mm'],['591x591','Square 2×2 in'],['300x400','300×400 px'],['200x230','200×230 px'],['300x100','Signature 300×100'],['140x60','Signature 140×60']];
  var S={w:413,h:531,unit:'px',dpi:300,kb:100,fmt:'image/jpeg',mode:'fill',bg:'#ffffff'};
  try{var sv=JSON.parse(localStorage.getItem('pr-set')||'null');if(sv&&sv.w)S=sv;}catch(e){}
  function save(){try{localStorage.setItem('pr-set',JSON.stringify(S));}catch(e){}}
  function kb(n){return n>=1048576?(n/1048576).toFixed(2)+' MB':Math.max(1,Math.round(n/1024))+' KB';}
  function step(n){[].forEach.call($('steps').children,function(li,i){li.className=i<n?'done':(i===n?'on':'');});}
  var pc=$('pre');PRE.forEach(function(p){var l=document.createElement('label');l.innerHTML='<input type="radio" name="pre" value="'+p[0]+'"><span>'+p[1]+'</span>';pc.appendChild(l);});
  $('w').value=S.w;$('h').value=S.h;$('unit').value=S.unit;$('dpi').value=S.dpi;$('kb').value=S.kb;$('fmt').value=S.fmt;$('mode').value=S.mode;$('dpiw').hidden=S.unit!=='mm';
  [].forEach.call(document.querySelectorAll('input[name=bg]'),function(r){if(r.value===S.bg)r.checked=true;});
  function dims(){var w=+$('w').value||1,h=+$('h').value||1;if($('unit').value==='mm'){var d=+$('dpi').value||300;w=w/25.4*d;h=h/25.4*d;}return [Math.min(4000,Math.max(10,Math.round(w))),Math.min(4000,Math.max(10,Math.round(h)))];}
  function eq(){var d=dims(),dp=+$('dpi').value||300;$('eq').textContent='Output: '+d[0]+' × '+d[1]+' px ('+(d[0]/dp*25.4).toFixed(0)+' × '+(d[1]/dp*25.4).toFixed(0)+' mm at '+dp+' dpi)';}
  function src(){if(!rot)return bmp;if(rc)return rc;var w=bmp.width||bmp.naturalWidth,h=bmp.height||bmp.naturalHeight,sw=rot%2?h:w,sh=rot%2?w:h,c=document.createElement('canvas');c.width=sw;c.height=sh;var g=c.getContext('2d');g.translate(sw/2,sh/2);g.rotate(rot*Math.PI/2);g.drawImage(bmp,-w/2,-h/2);rc=c;return c;}
  function paint(){if(!bmp)return;var d=dims(),W=d[0],H=d[1],im=src(),iw=im.width||im.naturalWidth,ih=im.height||im.naturalHeight,z=+$('zm').value,
    sc=($('mode').value==='fill'?Math.max(W/iw,H/ih):Math.min(W/iw,H/ih))*z,dw=iw*sc,dh=ih*sc,mx=Math.max(0,(dw-W)/2),my=Math.max(0,(dh-H)/2);
    ox=Math.max(-mx,Math.min(mx,ox));oy=Math.max(-my,Math.min(my,oy));
    if(cv.width!==W||cv.height!==H){cv.width=W;cv.height=H;}x.fillStyle=S.bg;x.fillRect(0,0,W,H);x.drawImage(im,(W-dw)/2+ox,(H-dh)/2+oy,dw,dh);
    eq();clearTimeout(bt);$('dl').setAttribute('aria-disabled','true');$('sum').textContent='Preparing...';bt=setTimeout(build,350);}
  function tb(q,t){return new Promise(function(r){cv.toBlob(r,t||'image/jpeg',q)})}
  async function build(){
    var my=++tok,T=(+$('kb').value)*1024,png=S.fmt==='image/png',b;
    if(png){b=await tb(1,'image/png');}
    else if(!T){b=await tb(.95);}
    else{var top=await tb(.95);if(top.size<=T)b=top;else{var lo=.03,hi=.95,best=null;for(var k=0;k<8;k++){var m=(lo+hi)/2,bl=await tb(m);if(bl.size<=T){best=bl;lo=m;}else hi=m;}b=best||await tb(.03);}}
    if(my!==tok)return;
    if(url)URL.revokeObjectURL(url);url=URL.createObjectURL(b);var a=$('dl');a.href=url;a.removeAttribute('aria-disabled');a.download='photo-'+cv.width+'x'+cv.height+(png?'.png':'.jpg');
    var ok=!T||png||b.size<=T;$('sum').innerHTML=cv.width+' × '+cv.height+' px · <b>'+kb(b.size)+'</b>'+(ok?'':' (above '+kb(T)+')');
    $('live').textContent=ok?'':'Cannot reach '+kb(T)+' at this size. Use smaller dimensions or a higher limit.';step(2);
  }
  function load(f){if(!f)return;var p=window.createImageBitmap?createImageBitmap(f,{imageOrientation:'from-image'}):new Promise(function(ok,bad){var u=URL.createObjectURL(f),i=new Image();i.onload=function(){ok(i)};i.onerror=bad;i.src=u;});
    p.then(function(b){bmp=b;rot=0;rc=null;ox=oy=0;$('zm').value=1;$('panel').hidden=false;drop.classList.add('mini');drop.querySelector('b').textContent='Change image';step(1);paint();},function(){drop.querySelector('b').textContent='Could not read that image. Try another.';});}
  $('file').addEventListener('change',function(e){load(e.target.files[0]);e.target.value='';});
  $('cam').addEventListener('click',function(e){e.preventDefault();e.stopPropagation();$('camin').click();});
  $('camin').addEventListener('change',function(e){load(e.target.files[0]);e.target.value='';});
  ['dragover','dragenter'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.add('over');});});
  ['dragleave','drop'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.remove('over');if(n==='drop'&&e.dataTransfer)load(e.dataTransfer.files[0]);});});
  document.addEventListener('paste',function(e){var f=[].filter.call((e.clipboardData&&e.clipboardData.files)||[],function(f){return /^image\//.test(f.type)})[0];if(f){e.preventDefault();load(f);}});
  function sync(){S.w=+$('w').value;S.h=+$('h').value;S.unit=$('unit').value;S.dpi=+$('dpi').value;S.kb=+$('kb').value;S.fmt=$('fmt').value;S.mode=$('mode').value;save();}
  pc.addEventListener('change',function(e){var p=e.target.value.split('x');$('unit').value='px';$('dpiw').hidden=true;$('w').value=p[0];$('h').value=p[1];ox=oy=0;sync();paint();});
  ['w','h','dpi'].forEach(function(i){$(i).addEventListener('input',function(){[].forEach.call(pc.querySelectorAll('input'),function(r){r.checked=false;});sync();paint();});});
  $('unit').addEventListener('change',function(){var d=dims();$('dpiw').hidden=this.value!=='mm';if(this.value==='mm'){var dp=+$('dpi').value||300;$('w').value=(d[0]/dp*25.4).toFixed(0);$('h').value=(d[1]/dp*25.4).toFixed(0);}else{$('w').value=d[0];$('h').value=d[1];}sync();paint();});
  ['kb','fmt'].forEach(function(i){$(i).addEventListener('change',function(){sync();paint();});});
  $('mode').addEventListener('change',function(){ox=oy=0;sync();paint();});
  $('zm').addEventListener('input',paint);
  [].forEach.call(document.querySelectorAll('input[name=bg]'),function(r){r.addEventListener('change',function(){S.bg=r.value;save();paint();});});
  $('bgc').addEventListener('input',function(){[].forEach.call(document.querySelectorAll('input[name=bg]'),function(r){r.checked=false;});S.bg=this.value;save();paint();});
  $('rl').addEventListener('click',function(){rot=(rot+3)%4;rc=null;ox=oy=0;paint();});$('rr').addEventListener('click',function(){rot=(rot+1)%4;rc=null;ox=oy=0;paint();});
  $('rst').addEventListener('click',function(){rot=0;rc=null;ox=oy=0;$('zm').value=1;paint();});
  $('gdb').addEventListener('click',function(){var on=!$('gd').classList.contains('on');$('gd').classList.toggle('on',on);this.setAttribute('aria-pressed',on);});
  var drag=null;cv.addEventListener('pointerdown',function(e){drag={x:e.clientX,y:e.clientY,ox:ox,oy:oy};cv.setPointerCapture(e.pointerId);cv.style.cursor='grabbing';});
  cv.addEventListener('pointermove',function(e){if(!drag)return;var k=cv.width/cv.clientWidth;ox=drag.ox+(e.clientX-drag.x)*k;oy=drag.oy+(e.clientY-drag.y)*k;paint();});
  ['pointerup','pointercancel'].forEach(function(n){cv.addEventListener(n,function(){drag=null;cv.style.cursor='grab';});});
  cv.addEventListener('wheel',function(e){e.preventDefault();var z=$('zm');z.value=Math.max(1,Math.min(4,+z.value+(e.deltaY<0?.1:-.1)));paint();},{passive:false});
  $('dl').addEventListener('click',function(e){if(this.getAttribute('aria-disabled')==='true')e.preventDefault();});
  eq();step(0);
})();"""
page('photo-resizer', 'Passport Photo and Signature Resizer: Set Size in Pixels, mm and KB (Free)',
     'Resize a photo or signature to exact pixels or mm and a maximum KB for Nepali online forms. Drag to crop, pick a background colour, live file size. Free, no upload.',
     'Photo and Signature Resizer', 'फोटो र हस्ताक्षरको साइज मिलाउनुहोस्', 'File tool',
     'Set the exact size and maximum file size a form asks for. Position the picture, see the final KB live, and download. Your image never leaves your device.',
     PR_TOOL, """  <h2>How to resize a passport photo or signature</h2>
  <ol>
    <li>Add your photo or signature image, or take one with your camera.</li>
    <li>Pick a common size, or type the exact width and height in pixels or millimetres, and the maximum KB.</li>
    <li>Drag the picture into place, zoom if needed, then download. The file size shows live before you download.</li>
  </ol>
  <p>For a signature, sign on plain white paper, photograph it in good light, then choose <em>Show whole image</em> so nothing is cropped. For a face photo, choose <em>Fill the frame</em>, switch on the face guide and centre the face.</p>
  <div class="note"><p><strong>Follow your form's instructions.</strong> The sizes listed here are common examples, not official requirements. Each form, exam body or office sets its own pixel size, KB limit and background colour, so check its notice and enter those values. Check the result before you upload it.</p></div>
  <h2>Pixels, millimetres and KB</h2>
  <p>Pixels set how large the image is on screen, and KB is the file size. A 35 × 45 mm photo at 300 dpi is about 413 × 531 pixels. Switch the unit to millimetres and set the dpi if your form gives a size in mm. A smaller KB limit lowers the JPEG quality, so choose the largest limit your form allows for the sharpest result.</p>
  <p>Need to shrink many ordinary photos instead? Use the <a href="/image-compressor/">image compressor</a>.</p>""",
     [("How do I resize a photo to a specific size in pixels?", "Add the photo, type the width and height in pixels, adjust the position and download. The file has exactly that size."),
      ("How do I make a photo under 50 KB or 100 KB?", "Set the maximum file size to 50 KB or 100 KB. The tool lowers the quality until the file fits and shows the final size before you download."),
      ("Can I enter the size in millimetres?", "Yes. Change the unit to millimetres, enter the width and height, and set the resolution (300 dpi is common). The tool shows the pixel size it will produce."),
      ("Can I use it for a signature?", "Yes. Choose a signature size, use Show whole image so nothing is cropped, and set the KB limit your form asks for."),
      ("Are these the official sizes for Nepali forms?", "No. They are common examples. Always use the exact size, KB limit and background colour written on your form or notice."),
      ("Is my photo uploaded to a server?", "No. Everything happens in your browser, so the image stays on your device."),
      ("Does it work on a phone?", "Yes. Take a photo or choose one from your gallery, then drag with your finger to position it.")],
     '', PR_JS,
     [('/image-compressor/', 'Image compressor'), ('/image-converter/', 'JPG converter'), ('/jpg-to-pdf/', 'JPG to PDF'), ('/pdf-to-jpg/', 'PDF to JPG')],
     'Photo and Signature Resizer', 'Free browser-based tool that resizes a photo or signature to an exact pixel or millimetre size and maximum KB without uploading it.')


# ================= SHARED PIECES FOR THE REMAINING TOOLS =================
def dz(multi, title, small, accept='image/*', cam=True):
    return ('<label class="tk-drop" id="drop" for="file">' + UP_SVG + f'<b>{title}</b><small>{small}</small>'
            f'<input id="file" type="file" accept="{accept}"{" multiple" if multi else ""}>'
            '<span class="tk-btns"><span class="tk-b pri">Choose ' + ('files' if multi else 'file') + '</span>' + ('<span class="tk-b" id="cam">Take photo</span>' if cam else '') + '</span>'
            + ('<input id="camin" type="file" accept="image/*" capture="environment">' if cam else '') + '</label>')
def head(labels):
    return ('<ul class="tk-trust"><li>Stays on your device</li><li>Free, no sign-up</li><li>No watermark</li></ul><ol class="tk-steps" id="steps">'
            + ''.join(f'<li class="{"on" if i == 0 else ""}">{l}</li>' for i, l in enumerate(labels)) + '</ol>')
def chips(name, label_id, label, opts, sel):
    return (f'<p class="tk-sec" id="{label_id}">{label}</p><div class="tk-chips" role="radiogroup" aria-labelledby="{label_id}">'
            + ''.join(f'<label><input type="radio" name="{name}" value="{v}"{" checked" if v == sel else ""}><span>{t}</span></label>' for v, t in opts) + '</div>')
BASE_JS = r"""
  var $=function(i){return document.getElementById(i)},drop=$('drop');
  function kb(n){return n>=1048576?(n/1048576).toFixed(2)+' MB':Math.max(1,Math.round(n/1024))+' KB';}
  function step(n){[].forEach.call($('steps').children,function(li,i){li.className=i<n?'done':(i===n?'on':'');});}
  function val(n){var r=document.querySelector('input[name='+n+']:checked');return r?r.value:null;}
  function setRadio(n,v){[].forEach.call(document.querySelectorAll('input[name='+n+']'),function(r){r.checked=r.value===String(v);});}
  function lsGet(k,d){try{var v=JSON.parse(localStorage.getItem(k)||'null');return v||d;}catch(e){return d;}}
  function lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
  function load(f){return window.createImageBitmap?createImageBitmap(f,{imageOrientation:'from-image'}):new Promise(function(ok,bad){var u=URL.createObjectURL(f),i=new Image();i.onload=function(){ok(i)};i.onerror=bad;i.src=u;});}
  function tb(c,t,q){return new Promise(function(r){c.toBlob(r,t,q)});}
  function isImg(f){return /^image\//.test(f.type)||/\.(jpe?g|png|webp|gif|bmp)$/i.test(f.name);}
  function bind(onFiles,test){
    var t=test||isImg;
    function go(list){var a=Array.from(list).filter(t);if(a.length)onFiles(a);}
    $('file').addEventListener('change',function(e){go(e.target.files);e.target.value='';});
    if($('cam')){$('cam').addEventListener('click',function(e){e.preventDefault();e.stopPropagation();$('camin').click();});$('camin').addEventListener('change',function(e){go(e.target.files);e.target.value='';});}
    ['dragover','dragenter'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.add('over');});});
    ['dragleave','drop'].forEach(function(n){drop.addEventListener(n,function(e){e.preventDefault();drop.classList.remove('over');if(n==='drop'&&e.dataTransfer)go(e.dataTransfer.files);});});
    document.addEventListener('paste',function(e){var a=Array.from((e.clipboardData&&e.clipboardData.files)||[]).filter(t);if(a.length){e.preventDefault();onFiles(a);}});
  }
  function mini(on,t){drop.classList.toggle('mini',on);drop.querySelector('b').textContent=t;}
"""

# ================= JPG TO PDF (pro) =================
JP_TOOL = KIT_CSS + '<style>.tk-file{grid-template-columns:60px 1fr}.tk-file .ac .tk-b{min-width:44px;padding:0 12px}</style>\n  <div class="conv tk" id="app">\n    ' + head(['1. Add', '2. Arrange', '3. Download']) + '\n    ' + dz(True, 'Drop images here, or tap to choose', 'JPG, PNG or WebP. Paste with Ctrl+V.') + '''
    <div id="panel" hidden>
      <ul class="tk-files" id="files" aria-live="polite"></ul>
      ''' + chips('size', 'szl', 'Page size', [('a4', 'A4'), ('letter', 'Letter'), ('fit', 'Same as image')], 'a4') + chips('mar', 'mgl', 'Margin', [('0', 'None'), ('18', 'Small'), ('36', 'Large')], '18') + chips('qual', 'qul', 'Quality (file size)', [('hi', 'High'), ('md', 'Balanced'), ('lo', 'Small')], 'md') + '''
      <p class="tk-live" id="live" aria-live="polite"></p>
      <div class="tk-bar"><div class="tk-sum" id="sum"></div><button class="tk-b" id="clr" type="button">Start over</button><button class="tk-b pri" id="go" type="button">Create PDF</button><a class="tk-b pri" id="dl" download="images.pdf" href="#" hidden>Download PDF</a></div>
    </div>
  </div>'''
JP_JS = r"""(function(){""" + BASE_JS + r"""
  var items=[],seq=0,url=null,Q={hi:{max:3000,q:.92},md:{max:1800,q:.75},lo:{max:1200,q:.55}};
  var st=lsGet('jp-set',{size:'a4',mar:'18',qual:'md'});setRadio('size',st.size);setRadio('mar',st.mar);setRadio('qual',st.qual);
  function thumb(b){var c=document.createElement('canvas'),w=b.width||b.naturalWidth,h=b.height||b.naturalHeight,s=120/Math.max(w,h);c.width=Math.max(1,Math.round(w*s));c.height=Math.max(1,Math.round(h*s));c.getContext('2d').drawImage(b,0,0,c.width,c.height);return c.toDataURL('image/jpeg',.7);}
  function stale(){$('dl').hidden=true;$('go').hidden=false;if(items.length)step(1);}
  function render(){
    var ul=$('files');ul.innerHTML='';
    items.forEach(function(it,i){var li=document.createElement('li');li.className='tk-file';
      li.innerHTML='<img alt="" src="'+it.t+'" style="transform:rotate('+it.r*90+'deg)"><div><div class="nm"></div><span class="st">Page '+(i+1)+' of '+items.length+'</span></div><div class="ac"><button type="button" class="tk-b" data-a="u" data-i="'+it.id+'" aria-label="Move up">↑</button><button type="button" class="tk-b" data-a="d" data-i="'+it.id+'" aria-label="Move down">↓</button><button type="button" class="tk-b" data-a="r" data-i="'+it.id+'">Rotate</button><button type="button" class="tk-b" data-a="x" data-i="'+it.id+'">Remove</button></div>';
      li.querySelector('.nm').textContent=it.n;ul.appendChild(li);});
    $('sum').innerHTML=items.length?'<b>'+items.length+'</b> page'+(items.length>1?'s':'')+' ready':'';$('go').disabled=!items.length;
  }
  bind(async function(fl){
    $('live').textContent='Reading images...';
    for(var i=0;i<fl.length;i++){try{var b=await load(fl[i]);items.push({id:++seq,n:fl[i].name,b:b,t:thumb(b),r:0});}catch(e){$('live').textContent='Could not read '+fl[i].name+'.';}}
    $('panel').hidden=false;mini(true,'Add more images');$('live').textContent='';stale();render();});
  $('files').addEventListener('click',function(e){var a=e.target.getAttribute&&e.target.getAttribute('data-a');if(!a)return;var id=+e.target.getAttribute('data-i'),i=items.findIndex(function(x){return x.id===id});
    if(a==='x')items.splice(i,1);else if(a==='r')items[i].r=(items[i].r+1)%4;else if(a==='u'&&i>0){var t=items[i];items[i]=items[i-1];items[i-1]=t;}else if(a==='d'&&i<items.length-1){var t2=items[i];items[i]=items[i+1];items[i+1]=t2;}
    if(!items.length){$('panel').hidden=true;mini(false,'Drop images here, or tap to choose');step(0);}stale();render();});
  ['size','mar','qual'].forEach(function(n){[].forEach.call(document.querySelectorAll('input[name='+n+']'),function(r){r.addEventListener('change',function(){lsSet('jp-set',{size:val('size'),mar:val('mar'),qual:val('qual')});stale();});});});
  $('clr').addEventListener('click',function(){items=[];$('panel').hidden=true;mini(false,'Drop images here, or tap to choose');step(0);render();});
  $('go').addEventListener('click',async function(){
    var J=window.jspdf&&window.jspdf.jsPDF;if(!J){$('live').textContent='The PDF library did not load. Check your connection and reload.';return;}
    $('go').disabled=true;var size=val('size'),m=+val('mar'),q=Q[val('qual')],doc=null;
    try{
      for(var i=0;i<items.length;i++){
        $('live').textContent='Building page '+(i+1)+' of '+items.length+'...';await new Promise(function(r){setTimeout(r,0)});
        var it=items[i],b=it.b,w0=b.width||b.naturalWidth,h0=b.height||b.naturalHeight,sw=it.r%2?h0:w0,sh=it.r%2?w0:h0,s=Math.min(1,q.max/Math.max(sw,sh)),cw=Math.round(sw*s),ch=Math.round(sh*s);
        var c=document.createElement('canvas');c.width=cw;c.height=ch;var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,cw,ch);x.translate(cw/2,ch/2);x.rotate(it.r*Math.PI/2);x.drawImage(b,-w0*s/2,-h0*s/2,w0*s,h0*s);
        var d=c.toDataURL('image/jpeg',q.q),pw,ph;
        if(size==='fit'){pw=sw*.75+m*2;ph=sh*.75+m*2;}else{var P=size==='a4'?[595.28,841.89]:[612,792];pw=sw>sh?P[1]:P[0];ph=sw>sh?P[0]:P[1];}
        var o=pw>ph?'l':'p';if(!doc)doc=new J({unit:'pt',format:[pw,ph],orientation:o,compress:true});else doc.addPage([pw,ph],o);
        var aw=pw-m*2,ah=ph-m*2,r=Math.min(aw/sw,ah/sh),iw=sw*r,ih=sh*r;doc.addImage(d,'JPEG',(pw-iw)/2,(ph-ih)/2,iw,ih,undefined,'FAST');
      }
      var blob=doc.output('blob');if(url)URL.revokeObjectURL(url);url=URL.createObjectURL(blob);var a=$('dl');a.href=url;a.download=(items.length===1?items[0].n.replace(/\.[^.]+$/,''):'images')+'.pdf';
      $('sum').innerHTML='<b>'+items.length+'</b> page'+(items.length>1?'s':'')+' · <b>'+kb(blob.size)+'</b>';a.hidden=false;$('go').hidden=true;$('live').textContent='Done. Your PDF is ready.';step(2);
    }catch(e){$('live').textContent='Something went wrong. Try fewer or smaller images, or the Small quality.';}
    $('go').disabled=false;
  });
  step(0);
})();"""
page('jpg-to-pdf', 'JPG to PDF Converter: Combine Images into One PDF (Free, No Upload)',
     'Convert JPG, PNG and WebP images to PDF free in your browser. Combine many photos into one PDF, rotate and reorder pages, choose A4 or Letter. No upload, no watermark.',
     'JPG to PDF Converter', 'तस्बिरलाई PDF मा बदल्नुहोस्', 'File tool',
     'Turn photos and scans into one PDF. Reorder and rotate pages, choose A4 or Letter, and shrink the file for upload limits. It all happens in your browser.',
     JP_TOOL, J_SECTIONS.replace('Use the arrows to put the pages in the order you want. Remove any you do not need.', 'Use the arrows to put pages in order, rotate any that are sideways, and remove those you do not need.'), J_FAQ,
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>', JP_JS,
     [('/pdf-to-jpg/', 'PDF to JPG'), ('/image-compressor/', 'Image compressor'), ('/photo-resizer/', 'Photo resizer'), ('/file-tools/', 'All file tools')],
     'JPG to PDF Converter', 'Free browser-based tool that converts JPG, PNG and WebP images into a single PDF without uploading them.')

# ================= PDF TO JPG (pro) =================
PD_TOOL = KIT_CSS + '<style>.tk-pg{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin:14px 0}.tk-pg figure{margin:0;background:var(--bg);border:1px solid var(--line);border-radius:var(--r);padding:8px;text-align:center}.tk-pg img{width:100%;height:auto;display:block;border-radius:8px;background:#fff}.tk-pg figcaption{font-size:.82rem;color:var(--ink2);margin:6px 0}.tk-pg .tk-b{width:100%;min-height:40px;font-size:.88rem}progress{width:100%;height:10px}</style>\n  <div class="conv tk" id="app">\n    ' + head(['1. Add PDF', '2. Convert', '3. Download']) + '\n    ' + dz(False, 'Drop a PDF here, or tap to choose', 'Pages become images on your device.', 'application/pdf,.pdf', False) + '''
    <div id="panel" hidden>
      <p class="tk-sec" id="fnm"></p>
      ''' + chips('dpi', 'dl1', 'Image quality', [('96', 'Small'), ('150', 'Standard'), ('220', 'High')], '150') + chips('ft', 'ftl', 'Format', [('jpg', 'JPG'), ('png', 'PNG')], 'jpg') + '''
      <div class="tk-row" style="margin-top:12px"><div class="f"><label class="l" for="rng">Pages (leave empty for all)</label><input class="tk-in" id="rng" placeholder="e.g. 1-3, 5" inputmode="text" autocomplete="off"></div></div>
      <div class="tk-row" id="pw" hidden style="margin-top:12px"><div class="f"><label class="l" for="pwi">This PDF needs a password</label><input class="tk-in" id="pwi" type="password" autocomplete="off"></div></div>
      <progress id="pr" max="1" value="0" hidden></progress>
      <p class="tk-live" id="live" aria-live="polite"></p>
      <div class="tk-pg" id="grid"></div>
      <div class="tk-bar"><div class="tk-sum" id="sum"></div><button class="tk-b" id="clr" type="button">Start over</button><button class="tk-b" id="zip" type="button" hidden>Download all (ZIP)</button><button class="tk-b pri" id="go" type="button">Convert</button></div>
    </div>
  </div>'''
PD_JS = r"""(function(){""" + BASE_JS + r"""
  var file=null,out=[],urls=[],pdfDoc=null;
  function parse(t,n){var s={};(t||'').split(',').forEach(function(p){p=p.trim();if(!p)return;var m=p.match(/^(\d+)\s*-\s*(\d+)$/);if(m){for(var i=+m[1];i<=+m[2];i++)if(i>=1&&i<=n)s[i]=1;}else if(/^\d+$/.test(p)&&+p>=1&&+p<=n)s[+p]=1;});var a=Object.keys(s).map(Number).sort(function(a,b){return a-b});return a.length?a:null;}
  bind(function(fl){file=fl[0];pdfDoc=null;$('panel').hidden=false;$('fnm').textContent=file.name+' · '+kb(file.size);$('grid').innerHTML='';$('zip').hidden=true;$('pw').hidden=true;$('live').textContent='';mini(true,'Change PDF');step(1);},function(f){return f.type==='application/pdf'||/\.pdf$/i.test(f.name);});
  async function open(){
    var L=window.pdfjsLib;if(!L)throw new Error('lib');L.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    var buf=await file.arrayBuffer();return L.getDocument({data:buf,password:$('pwi').value||undefined}).promise;
  }
  $('go').addEventListener('click',async function(){
    $('go').disabled=true;$('zip').hidden=true;$('grid').innerHTML='';out=[];urls.forEach(URL.revokeObjectURL);urls=[];$('pr').hidden=false;$('pr').value=0;
    try{
      pdfDoc=await open();var pages=parse($('rng').value,pdfDoc.numPages)||Array.from({length:pdfDoc.numPages},function(_,i){return i+1;}),cap=100,over=pages.length>cap;if(over)pages=pages.slice(0,cap);
      var sc=(+val('dpi'))/72,png=val('ft')==='png',base=file.name.replace(/\.pdf$/i,'');
      for(var k=0;k<pages.length;k++){
        var i=pages[k];$('live').textContent='Converting page '+i+' ('+(k+1)+' of '+pages.length+')...';
        var p=await pdfDoc.getPage(i),vp=p.getViewport({scale:sc}),f=Math.min(1,Math.sqrt(16000000/(vp.width*vp.height)));if(f<1)vp=p.getViewport({scale:sc*f});
        var c=document.createElement('canvas');c.width=Math.floor(vp.width);c.height=Math.floor(vp.height);var x=c.getContext('2d');x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);
        await p.render({canvasContext:x,viewport:vp}).promise;
        var blob=await tb(c,png?'image/png':'image/jpeg',.9),u=URL.createObjectURL(blob),nm=base+'-page-'+i+(png?'.png':'.jpg');urls.push(u);out.push({n:nm,b:blob});
        var fg=document.createElement('figure');fg.innerHTML='<img alt="Page '+i+'" src="'+u+'"><figcaption>Page '+i+' · '+kb(blob.size)+'</figcaption><a class="tk-b" download="'+nm+'" href="'+u+'">Download</a>';$('grid').appendChild(fg);
        $('pr').value=(k+1)/pages.length;c.width=c.height=0;
      }
      $('live').textContent='Done. '+pages.length+' page'+(pages.length>1?'s':'')+' converted'+(over?' (first 100 only)':'')+'.';$('sum').innerHTML='<b>'+pages.length+'</b> image'+(pages.length>1?'s':'');$('zip').hidden=pages.length<2;$('pw').hidden=true;step(2);
    }catch(e){
      if(e&&e.name==='PasswordException'){$('pw').hidden=false;$('live').textContent=e.code===2?'Wrong password. Try again.':'Enter the password, then press Convert.';}
      else if(e&&e.message==='lib')$('live').textContent='The PDF library did not load. Check your connection and reload.';
      else $('live').textContent='Could not read this PDF. It may be damaged.';
    }
    $('pr').hidden=true;$('go').disabled=false;
  });
  $('clr').addEventListener('click',function(){file=null;out=[];$('panel').hidden=true;$('grid').innerHTML='';mini(false,'Drop a PDF here, or tap to choose');step(0);});
  $('zip').addEventListener('click',async function(){
    if(!window.JSZip){$('live').textContent='The ZIP library did not load. Download pages one by one.';return;}
    var z=new JSZip();out.forEach(function(o){z.file(o.n,o.b);});$('live').textContent='Preparing ZIP...';
    var b=await z.generateAsync({type:'blob'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=file.name.replace(/\.pdf$/i,'')+'-images.zip';document.body.appendChild(a);a.click();a.remove();$('live').textContent='ZIP downloaded.';});
  step(0);
})();"""
page('pdf-to-jpg', 'PDF to JPG Converter: Turn PDF Pages into Images (Free, No Upload)',
     'Convert PDF pages to JPG or PNG images free in your browser. Pick pages, choose quality, download each page or all as a ZIP. No upload, no sign-up, no watermark.',
     'PDF to JPG Converter', 'PDF लाई JPG मा बदल्नुहोस्', 'File tool',
     'Turn pages of a PDF into JPG or PNG images. Choose the pages and quality, then download them one by one or all as a ZIP. Your file stays on your device.',
     PD_TOOL, P_SECTIONS.replace('Pick the image quality.', 'Choose the pages you want (or leave it empty for all) and the image quality.').replace('Password-protected PDFs cannot be opened here.', 'If a PDF has a password, the tool asks for it.'),
     [(q, a.replace('Remove the password first, then convert the file.', 'Enter the password when asked.') if False else a) for q, a in P_FAQ if not q.startswith('Can it open')] + [("Can it open a password-protected PDF?", "Yes, if you know the password. The tool asks for it and then converts the pages.")],
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>\n<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>', PD_JS,
     [('/jpg-to-pdf/', 'JPG to PDF'), ('/image-compressor/', 'Image compressor'), ('/image-converter/', 'JPG converter'), ('/file-tools/', 'All file tools')],
     'PDF to JPG Converter', 'Free browser-based tool that converts selected pages of a PDF into JPG or PNG images without uploading the file.')

# ================= IMAGE CONVERTER (pro) =================
IV_TOOL = KIT_CSS + '\n  <div class="conv tk" id="app">\n    ' + head(['1. Add', '2. Choose format', '3. Download']) + '\n    ' + dz(True, 'Drop images here, or tap to choose', 'JPG, PNG, WebP, GIF, BMP. Paste with Ctrl+V.') + '''
    <div id="panel" hidden>
      ''' + chips('fmt', 'fml', 'Convert to', [('image/jpeg', 'JPG'), ('image/png', 'PNG'), ('image/webp', 'WebP')], 'image/jpeg') + chips('q', 'ql', 'Quality (JPG and WebP)', [('.95', 'High'), ('.85', 'Good'), ('.7', 'Smaller file')], '.85') + chips('mx', 'mxl', 'Largest side', [('0', 'Original'), ('1920', '1920 px'), ('1280', '1280 px'), ('800', '800 px')], '0') + '''
      <p class="tk-live" id="live" aria-live="polite"></p>
      <ul class="tk-files" id="files"></ul>
      <div class="tk-bar"><div class="tk-sum" id="sum"></div><button class="tk-b" id="clr" type="button">Start over</button><button class="tk-b" id="zip" type="button" hidden>Download all (ZIP)</button></div>
    </div>
  </div>'''
IV_JS = r"""(function(){""" + BASE_JS + r"""
  var items=[],seq=0,token=0,urls=[],EXT={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'};
  var st=lsGet('iv-set',{fmt:'image/jpeg',q:'.85',mx:'0'});setRadio('fmt',st.fmt);setRadio('q',st.q);setRadio('mx',st.mx);
  bind(async function(fl){
    for(var i=0;i<fl.length;i++){try{var b=await load(fl[i]),u=URL.createObjectURL(fl[i]);urls.push(u);items.push({id:++seq,f:fl[i],b:b,u:u,r:null});}catch(e){}}
    $('panel').hidden=false;mini(true,'Add more images');step(1);run();});
  async function run(){
    if(!items.length)return;var my=++token,t=val('fmt'),q=+val('q'),mx=+val('mx');$('live').textContent='Converting...';items.forEach(function(it){it.r=null;});render();
    for(var i=0;i<items.length;i++){if(my!==token)return;await new Promise(function(r){setTimeout(r,0)});var it=items[i],w=it.b.width||it.b.naturalWidth,h=it.b.height||it.b.naturalHeight,s=mx?Math.min(1,mx/Math.max(w,h)):1;
      var c=document.createElement('canvas');c.width=Math.max(1,Math.round(w*s));c.height=Math.max(1,Math.round(h*s));var x=c.getContext('2d');if(t==='image/jpeg'){x.fillStyle='#fff';x.fillRect(0,0,c.width,c.height);}x.drawImage(it.b,0,0,c.width,c.height);
      var bl=await tb(c,t,q);if(my!==token)return;if(!bl||bl.type!==t){it.r={err:1};render();continue;}it.r={blob:bl,u:URL.createObjectURL(bl),w:c.width,h:c.height,t:t};urls.push(it.r.u);render();}
    if(my===token){$('live').textContent='';step(2);}
  }
  function render(){
    var ul=$('files');ul.innerHTML='';var done=0,tot=0;
    items.forEach(function(it){var li=document.createElement('li');li.className='tk-file',r=it.r;var st,nm='';
      if(!r)st='<span class="st">Converting...</span>';else if(r.err)st='<span class="st bad">This browser cannot save that format. Try JPG or PNG.</span>';else{done++;tot+=r.blob.size;nm=it.f.name.replace(/\.[^.]+$/,'')+'.'+EXT[r.t];st='<span class="st">'+kb(it.f.size)+' → <b>'+kb(r.blob.size)+'</b> · '+r.w+'×'+r.h+' px</span>';}
      li.innerHTML='<img alt="" src="'+it.u+'"><div><div class="nm"></div>'+st+'</div><div class="ac">'+(r&&r.blob?'<a class="tk-b pri" download="'+nm.replace(/"/g,'')+'" href="'+r.u+'">Download</a>':'')+'<button type="button" class="tk-b" data-i="'+it.id+'">Remove</button></div>';
      li.querySelector('.nm').textContent=it.f.name;ul.appendChild(li);});
    $('zip').hidden=done<2;$('sum').innerHTML=done?'<b>'+done+'</b> image'+(done>1?'s':'')+' · '+kb(tot):'';
  }
  $('files').addEventListener('click',function(e){var id=+e.target.getAttribute('data-i');if(!id)return;items=items.filter(function(x){return x.id!==id});if(!items.length){reset();}else render();});
  ['fmt','q','mx'].forEach(function(n){[].forEach.call(document.querySelectorAll('input[name='+n+']'),function(r){r.addEventListener('change',function(){lsSet('iv-set',{fmt:val('fmt'),q:val('q'),mx:val('mx')});run();});});});
  function reset(){token++;items=[];urls.forEach(function(u){URL.revokeObjectURL(u)});urls=[];$('panel').hidden=true;$('files').innerHTML='';mini(false,'Drop images here, or tap to choose');step(0);}
  $('clr').addEventListener('click',reset);
  $('zip').addEventListener('click',async function(){
    if(!window.JSZip){$('live').textContent='The ZIP library did not load. Download files one by one.';return;}
    var z=new JSZip(),seen={};items.forEach(function(it){if(it.r&&it.r.blob){var n=it.f.name.replace(/\.[^.]+$/,''),k=n;seen[n]=(seen[n]||0)+1;if(seen[n]>1)k=n+'-'+seen[n];z.file(k+'.'+EXT[it.r.t],it.r.blob);}});
    $('live').textContent='Preparing ZIP...';var b=await z.generateAsync({type:'blob'}),a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='converted-images.zip';document.body.appendChild(a);a.click();a.remove();$('live').textContent='ZIP downloaded.';});
  step(0);
})();"""
page('image-converter', 'JPG Converter: Convert PNG or WebP to JPG and JPG to PNG (Free, No Upload)',
     'Free image converter for JPG, PNG and WebP. Convert PNG to JPG, WebP to JPG or JPG to PNG in your browser, many files at once, no upload, no watermark.',
     'JPG Converter (PNG, WebP, JPG)', 'तस्बिर JPG, PNG, WebP मा बदल्नुहोस्', 'File tool',
     'Convert images between JPG, PNG and WebP. Results update as you change the format, and you can download them all as a ZIP. Everything runs in your browser.',
     IV_TOOL, """  <h2>How to convert an image to JPG</h2>
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
  <p>Need a particular file size? Use the <a href="/image-compressor/">image compressor</a>. To make a PDF, use <a href="/jpg-to-pdf/">JPG to PDF</a>.</p>""", [("How do I convert PNG to JPG?", "Choose the PNG, select JPG as the output format and press Convert. Transparent areas become white."),
      ("How do I convert WebP to JPG?", "Choose the WebP file, select JPG and press Convert. It works the same way as any other image."),
      ("Is this image converter free and private?", "Yes. It is free and the files are converted in your browser, so they are never uploaded."),
      ("Will converting reduce the quality?", "Converting to JPG or WebP is lossy, so choose High quality if detail matters. Converting to PNG keeps every pixel but makes larger files."),
      ("Can I convert many images at once?", "Yes. Select several and download them individually or as a ZIP."),
      ("Does it support JPG to PNG?", "Yes. Choose JPG files and select PNG as the output format.")],
     '<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>', IV_JS,
     [('/image-compressor/', 'Image compressor'), ('/jpg-to-pdf/', 'JPG to PDF'), ('/photo-resizer/', 'Photo resizer'), ('/file-tools/', 'All file tools')],
     'Image Converter', 'Free browser-based tool that converts images between JPG, PNG and WebP without uploading them.')


# ================= HUB: /file-tools/ =================
TOOLS = [('/photo-resizer/', '📸', 'Photo & Signature Resizer', 'Exact pixels or mm and a maximum KB for forms.'),
         ('/image-compressor/', '🗜️', 'Image Compressor', 'Shrink photos to 20, 50, 100 or 200 KB with a before/after check.'),
         ('/jpg-to-pdf/', '🖼️', 'JPG to PDF', 'Combine photos and scans into one PDF. Reorder and rotate.'),
         ('/pdf-to-jpg/', '📄', 'PDF to JPG', 'Turn PDF pages into JPG or PNG images. Pick pages.'),
         ('/image-converter/', '🔄', 'JPG Converter', 'PNG, WebP and JPG in any direction. Many files at once.')]
HUB_TOOL = KIT_CSS + '<style>.hub{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:6px 0 4px}.hub a{display:block;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;min-height:120px}.hub a:hover,.hub a:focus-visible{border-color:var(--red);outline:none}.hub .i{font-size:1.7rem}.hub b{display:block;font-size:1.05rem;color:var(--ink);margin:6px 0 2px}.hub span{font-size:.9rem;color:var(--ink2)}</style>\n  <div class="tk"><ul class="tk-trust"><li>Stays on your device</li><li>Free, no sign-up</li><li>No watermark</li></ul>\n  <div class="hub">' + ''.join(f'<a href="{u}"><span class="i">{i}</span><b>{t}</b><span>{d}</span></a>' for u, i, t, d in TOOLS) + '</div></div>'
HUB_SECTIONS = """  <h2>Which tool do I need?</h2>
  <div class="table-wrap"><table>
    <thead><tr><th>My problem</th><th>Use</th></tr></thead>
    <tbody>
      <tr><td>A form wants a photo or signature of an exact size</td><td><a href="/photo-resizer/">Photo &amp; Signature Resizer</a></td></tr>
      <tr><td>The file is too big to upload (for example over 100 KB)</td><td><a href="/image-compressor/">Image Compressor</a></td></tr>
      <tr><td>I need one PDF made from several photos or scans</td><td><a href="/jpg-to-pdf/">JPG to PDF</a></td></tr>
      <tr><td>I need pictures of the pages in a PDF</td><td><a href="/pdf-to-jpg/">PDF to JPG</a></td></tr>
      <tr><td>The site only accepts JPG and my image is PNG or WebP</td><td><a href="/image-converter/">JPG Converter</a></td></tr>
    </tbody>
  </table></div>
  <h2>Private by design</h2>
  <p>These tools run inside your browser. Your photos, scans and PDFs are not uploaded to any server, so documents such as citizenship certificates, passport photos and bank papers stay on your device. Nothing is added to your files, and there is no watermark or sign-up.</p>
  <h2>Tips for online forms</h2>
  <ul>
    <li>Read the notice for the exact size, KB limit, format and background colour. Forms differ, and the sizes in these tools are examples.</li>
    <li>Resize first, then compress. The resizer can set pixels and a maximum KB together.</li>
    <li>Open the final file and check that text and faces are clear before you upload.</li>
  </ul>"""
HUB_FAQ = [("Are these file tools free?", "Yes. They are free, with no account and no watermark."),
           ("Are my files uploaded?", "No. Everything is processed in your browser on your own device."),
           ("Which tool makes a photo under 100 KB?", "Use the Image Compressor for ordinary photos, or the Photo and Signature Resizer if the form also needs an exact pixel size."),
           ("Do they work on a phone?", "Yes. You can choose photos from your gallery or take one with the camera.")]
page('file-tools', 'Free Online File Tools: Photo Resizer, Image Compressor, JPG to PDF',
     'Free tools for Nepali online forms: resize photos and signatures, compress images to KB, convert JPG to PDF, PDF to JPG and PNG or WebP to JPG. No upload.',
     'Free File Tools for Forms and Documents', 'फारम र कागजातका लागि निःशुल्क उपकरण', 'File tools',
     'Resize photos, shrink files, and convert between JPG, PDF, PNG and WebP. Five tools that run in your browser, so your files stay private.',
     HUB_TOOL, HUB_SECTIONS, HUB_FAQ, '', '// no script',
     [(u, t) for u, _, t, _ in TOOLS[:4]], 'Free File Tools', 'Collection of free browser-based tools to resize, compress and convert photos, signatures and PDFs.')
print('pro tools ok')
