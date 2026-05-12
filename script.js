// ═══════════════════════════════════════════════════
// PREETI ↔ UNICODE CONVERTER - script.js
// Copyright © thenepal.io (https://thenepal.io)
// ═══════════════════════════════════════════════════

let PREETI_MAP = {};
let REVERSE_MAP = {};
let FONT_MAPS = { preeti: {}, kantipur: {}, pcsnepali: {} };
let currentMode = 'pu';
let currentFont = 'preeti';
let uploadedFiles = [];
let hashUpdateTimeout;

// ─── Additional font maps (fallback) ─────────────────
const K2U_SINGLE = {
  'k':'क','l':'ख','m':'ग','n':'घ','o':'ङ','p':'च','q':'छ','r':'ज','s':'झ','t':'ञ',
  'u':'ट','v':'ठ','w':'ड','x':'ढ','y':'ण','z':'त','A':'थ','B':'द','C':'ध','D':'न',
  'E':'प','F':'फ','G':'ब','H':'भ','I':'म','J':'य','K':'र','L':'ल','M':'व','N':'श',
  'O':'ष','P':'स','Q':'ह','a':'अ','b':'आ','c':'इ','d':'ई','e':'उ','f':'ऊ','g':'ए',
  'h':'ऐ','i':'ओ','j':'औ','R':'क्ष','S':'त्र','T':'ज्ञ','[':'ि',']':'ी','{':'ु',
  '}':'ू',';':'े',"'":'ै','/':'ो','?':'ौ','.':'।',',':'ं','<':'ँ','>':'ः',
  '1':'१','2':'२','3':'३','4':'४','5':'५','6':'६','7':'७','8':'८','9':'९','0':'०',
  ' ':' ','\n':'\n','\t':'\t'
};
const PCS2U_SINGLE = { ...PREETI_MAP }; // PCS Nepali is very similar to Preeti

// ─── Load Preeti map from JSON ─────────────────────
async function loadMap() {
  try {
    const resp = await fetch('./preeti-map.json');
    PREETI_MAP = await resp.json();
    buildReverseMap(PREETI_MAP, 'preeti');
    // Build reverse maps for other fonts
    buildReverseMap(K2U_SINGLE, 'kantipur');
    buildReverseMap(PCS2U_SINGLE, 'pcsnepali');
  } catch (e) {
    console.warn('Could not load preeti-map.json, using hardcoded fallback', e);
    // Hardcoded fallback (same as JSON)
    PREETI_MAP = {
      "cf]":"ओ","cf}":"औ","cf":"आ","f]":"ो","f}":"ौ","km":"फ","Qm":"फ्र","k|":"प्त",
      "c":"अ","O":"इ","Ö":"ई","p":"उ","P":"ऊ","C":"ए","s":"क","v":"ख","u":"ग",
      "3":"घ","ª":"ङ","r":"च","5":"छ","h":"ज","´":"झ","~":"ञ","6":"ट","7":"ठ",
      "8":"ड","9":"ढ","0":"ण","t":"त","y":"थ","b":"द","w":"ध","g":"न","k":"प",
      "a":"ब","e":"भ","d":"म","o":"य","/":"य","n":"ल","j":"व","z":"श","if":"ष",
      ";":"स","x":"ह","f":"ा","l":"ि","L":"ी","'":"ु","\"":"ू","]":"े","}":"ै",
      "M":"ं","F":"ँ","\\":"्","H":"ः",":":"ँ",".":"।","<":",",">":".","|":"।",
      "?":"रु","1":"१","2":"२","3":"३","4":"४","5":"५","6":"६","7":"७","8":"८",
      "9":"९","0":"०"," ":" ","\n":"\n","\t":"\t"
    };
    buildReverseMap(PREETI_MAP, 'preeti');
    buildReverseMap(K2U_SINGLE, 'kantipur');
    buildReverseMap(PCS2U_SINGLE, 'pcsnepali');
  }
}

function buildReverseMap(map, font) {
  const rev = {};
  for (const [k, v] of Object.entries(map)) {
    if (!rev[v] && k.length === 1 && ![' ', '\n', '\t'].includes(k)) {
      rev[v] = k;
    }
  }
  FONT_MAPS[font] = { forward: map, reverse: rev };
}

// ─── Conversion engine (longest match first) ──────
function convertText(text, mode, font) {
  if (!text) return '';
  const fontData = FONT_MAPS[font] || FONT_MAPS.preeti;
  if (mode === 'pu') {
    return forwardConvert(text, fontData.forward);
  } else {
    return reverseConvert(text, fontData.reverse, fontData.forward);
  }
}

function forwardConvert(text, map) {
  const keys = Object.keys(map).sort((a, b) => b.length - a.length);
  let result = text;
  for (const key of keys) {
    const escaped = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(escaped, 'g');
    result = result.replace(regex, map[key]);
  }
  // Fix ि matra ordering (ि before consonant → after)
  result = result.replace(/ि([कखगघङचछजझञटठडढणतथदधनपफबभमयरलळवशषसहक्षज्ञत्रश्र])/g, '$1ि');
  return result;
}

function reverseConvert(text, revMap, forwardMap) {
  // First, handle multi-char Unicode sequences that map to Preeti
  // (like ऐ → cf])
  let result = text;
  const multiUni = Object.entries(forwardMap)
    .filter(([k, v]) => k.length > 1 && v.length > 1)
    .sort((a, b) => b[1].length - a[1].length);
  for (const [preeti, uni] of multiUni) {
    result = result.split(uni).join(preeti);
  }
  // Then single chars
  for (const [uni, preeti] of Object.entries(revMap)) {
    result = result.split(uni).join(preeti);
  }
  // Fix ि matra swap: consonant + l → l + consonant
  result = result.replace(/([कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षज्ञत्रश्र])l/g, 'l$1');
  return result;
}

// ─── UI State & Event Handlers ───────────────────
function setMode(m) {
  currentMode = m;
  document.getElementById('btn-pu').classList.toggle('active', m === 'pu');
  document.getElementById('btn-up').classList.toggle('active', m === 'up');
  document.getElementById('in-label').textContent = m === 'pu' ? getFontLabel() + ' Input' : 'Unicode Input';
  document.getElementById('out-label').textContent = m === 'pu' ? 'Unicode Output' : getFontLabel() + ' Output';
  const placeholders = {
    preeti: 'Type Preeti…\nExample: g]kfn = नेपाल\ns = क, v = ख',
    kantipur: 'Type Kantipur…\nk=क, l=ख',
    pcsnepali: 'Type PCS Nepali…\nSimilar to Preeti'
  };
  document.getElementById('inp').placeholder = m === 'pu' ? (placeholders[currentFont] || '') :
    'Type Unicode Devanagari…';
  const ob = document.getElementById('out');
  ob.className = 'out-box' + (m === 'up' ? ' preeti-out' : '') + (ob.textContent === 'Converted text appears here…' ? ' empty' : '');
  updateURLHash();
  convert();
}

function getFontLabel() {
  if (currentFont === 'kantipur') return 'Kantipur';
  if (currentFont === 'pcsnepali') return 'PCS Nepali';
  return 'Preeti';
}

function onFontChange() {
  currentFont = document.getElementById('font-select').value;
  setMode(currentMode);
}

function convert() {
  const inp = document.getElementById('inp').value;
  updateCounters('in', inp);
  const ob = document.getElementById('out');
  if (!inp) {
    ob.textContent = 'Converted text appears here…';
    ob.classList.add('empty');
    updateCounters('out', '');
    return;
  }
  const result = convertText(inp, currentMode, currentFont);
  ob.textContent = result;
  ob.classList.remove('empty');
  updateCounters('out', result);
  updateURLHash();
}

function onInputChange() {
  convert();
  updateURLHashDebounced();
}

function updateCounters(prefix, text) {
  document.getElementById(prefix + '-chars').textContent = text.length;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  document.getElementById(prefix + '-words').textContent = words;
}

function swapAll() {
  const cur = document.getElementById('inp').value;
  const converted = document.getElementById('out').textContent;
  const newMode = currentMode === 'pu' ? 'up' : 'pu';
  setMode(newMode);
  if (converted && converted !== 'Converted text appears here…') {
    document.getElementById('inp').value = converted;
    convert();
  }
}

function getOutputText() {
  const t = document.getElementById('out').textContent;
  return (t && t !== 'Converted text appears here…') ? t : '';
}

async function copyOut() {
  const t = getOutputText();
  if (!t) { showToast('⚠️ Nothing to copy yet'); return; }
  try {
    await navigator.clipboard.writeText(t);
    showToast('✓ Copied to clipboard!');
    document.getElementById('copy-tooltip').classList.add('show');
    setTimeout(() => document.getElementById('copy-tooltip').classList.remove('show'), 1800);
  } catch { showToast('Use Ctrl+C to copy'); }
}

async function pasteInput() {
  try {
    const t = await navigator.clipboard.readText();
    document.getElementById('inp').value = t;
    convert();
  } catch { showToast('Use Ctrl+V to paste'); }
}

function cleanText() {
  const ob = document.getElementById('out');
  let t = ob.textContent;
  if (!t || t === 'Converted text appears here…') {
    const inp = document.getElementById('inp');
    if (inp.value) {
      t = inp.value.replace(/\|/g, '।').replace(/  +/g, ' ').replace(/\n{3,}/g, '\n\n').trim();
      inp.value = t;
      convert();
      showToast('✓ Input cleaned!');
      return;
    }
    showToast('⚠️ Nothing to clean');
    return;
  }
  t = t.replace(/\|/g, '।').replace(/  +/g, ' ').replace(/\n{3,}/g, '\n\n')
       .replace(/।\s*।/g, '।').replace(/\s+।/g, '।').replace(/।([^\s])/g, '। $1').trim();
  ob.textContent = t;
  updateCounters('out', t);
  updateURLHash();
  showToast('✓ Text cleaned (|→।, spaces)');
}

function downloadTxt() {
  const t = getOutputText();
  if (!t) { showToast('⚠️ Nothing to download'); return; }
  const filename = currentMode === 'pu' ? 'unicode-output.txt' : currentFont + '-output.txt';
  dlText(t, filename);
  showToast('✓ Downloaded ' + filename);
}

function clearAll() {
  document.getElementById('inp').value = '';
  document.getElementById('out').textContent = 'Converted text appears here…';
  document.getElementById('out').classList.add('empty');
  updateCounters('in', '');
  updateCounters('out', '');
  updateURLHash();
  showToast('✓ All cleared');
}

function changeFontSize(val) {
  document.documentElement.style.setProperty('--output-font-size', val + 'px');
  document.getElementById('font-size-val').textContent = val + 'px';
  localStorage.setItem('preeti-font-size', val);
}

// ─── Dark Mode ────────────────────────────────────
function toggleDarkMode() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  document.getElementById('dark-toggle').textContent = next === 'dark' ? '☀️' : '🌙';
  localStorage.setItem('preeti-theme', next);
}

function initDarkMode() {
  const saved = localStorage.getItem('preeti-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = saved || (prefersDark ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);
  document.getElementById('dark-toggle').textContent = theme === 'dark' ? '☀️' : '🌙';
}

// ─── URL Hash Parameters (Shareable States) ───────
function updateURLHash() {
  const inp = document.getElementById('inp').value;
  const params = new URLSearchParams();
  params.set('m', currentMode);
  params.set('f', currentFont);
  if (inp && inp.length <= 2000) params.set('t', inp);
  else if (inp) params.set('t', inp.substring(0, 2000));
  window.location.hash = params.toString();
}

function updateURLHashDebounced() {
  clearTimeout(hashUpdateTimeout);
  hashUpdateTimeout = setTimeout(updateURLHash, 400);
}

function loadFromURLHash() {
  const hash = window.location.hash.replace('#', '');
  if (!hash) return;
  const params = new URLSearchParams(hash);
  const m = params.get('m');
  const f = params.get('f');
  const t = params.get('t');
  if (m && (m === 'pu' || m === 'up')) currentMode = m;
  if (f && ['preeti','kantipur','pcsnepali'].includes(f)) {
    currentFont = f;
    document.getElementById('font-select').value = f;
  }
  if (t) document.getElementById('inp').value = t;
  setMode(currentMode);
}

// ─── File Handling ────────────────────────────────
function handleDrag(e, over) {
  e.preventDefault();
  document.getElementById('drop-zone').classList.toggle('dragover', over);
}
function handleDrop(e) {
  e.preventDefault();
  document.getElementById('drop-zone').classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
}
function handleFiles(files) {
  for (const f of files) {
    const ext = f.name.split('.').pop().toLowerCase();
    if (!['txt','docx'].includes(ext)) { showToast('Only .txt and .docx supported'); continue; }
    uploadedFiles.push({ file:f, name:f.name, size:f.size, status:'pending', result:null });
  }
  renderFileList();
  document.getElementById('file-actions').style.display = uploadedFiles.length ? 'flex' : 'none';
}
function renderFileList() {
  const el = document.getElementById('file-list');
  el.innerHTML = uploadedFiles.map((f,i) => `
    <div class="file-item">
      <span class="file-icon">${f.name.endsWith('.docx')?'📝':'📄'}</span>
      <div class="file-info"><div class="file-name">${f.name}</div><div class="file-size">${fmtSize(f.size)}</div></div>
      <span class="file-status ${f.status}">${f.status==='pending'?'⏳ Pending':f.status==='done'?'✅ Done':'❌ Error'}</span>
      ${f.status==='done'?`<button class="btn" style="padding:5px 10px;font-size:10px" onclick="downloadSingleFile(${i})">⬇</button>`:''}
      <button class="file-remove" onclick="removeFile(${i})">✕</button>
    </div>`).join('');
}
function removeFile(i) { uploadedFiles.splice(i,1); renderFileList(); document.getElementById('file-actions').style.display = uploadedFiles.length?'flex':'none'; }
function clearFiles() { uploadedFiles=[]; renderFileList(); document.getElementById('file-actions').style.display='none'; document.getElementById('file-input').value=''; }

async function convertAllFiles() {
  if (!uploadedFiles.length) return;
  const prog = document.getElementById('prog-wrap'), bar = document.getElementById('prog-bar'), lbl = document.getElementById('prog-label');
  prog.classList.add('show');
  for (let i=0; i<uploadedFiles.length; i++) {
    const f = uploadedFiles[i];
    lbl.textContent = `Processing ${f.name}…`;
    bar.style.width = Math.round((i/uploadedFiles.length)*100)+'%';
    try {
      const ext = f.name.split('.').pop().toLowerCase();
      if (ext === 'txt') {
        const text = await readFileAsText(f.file);
        f.result = { type:'txt', data: convertText(text, currentMode, currentFont), name: convertedName(f.name) };
      } else if (ext === 'docx') {
        const buf = await readFileAsArrayBuffer(f.file);
        const res = await mammoth.extractRawText({ arrayBuffer: buf });
        f.result = { type:'docx', data: convertText(res.value, currentMode, currentFont), name: convertedName(f.name) };
      }
      f.status = 'done';
    } catch(e) { f.status='error'; console.error(e); }
    renderFileList();
    await sleep(30);
  }
  bar.style.width='100%'; lbl.textContent='✅ All files converted!';
  setTimeout(()=>prog.classList.remove('show'),2000);
}
function downloadSingleFile(i) {
  const f = uploadedFiles[i]; if (!f?.result) return;
  if (f.result.type==='txt') dlText(f.result.data, f.result.name);
  else dlDocxFallback(f.result.data, f.result.name);
  showToast('✓ Downloaded: '+f.result.name);
}
async function downloadAllFiles() {
  const done = uploadedFiles.filter(f=>f.status==='done');
  if (!done.length) { showToast('Convert files first'); return; }
  for (const f of done) {
    if (f.result.type==='txt') dlText(f.result.data, f.result.name);
    else await dlDocxFallback(f.result.data, f.result.name);
    await sleep(200);
  }
  showToast('✓ Downloaded '+done.length+' file(s)');
}
function convertedName(name) { const p=name.split('.'); p.pop(); return p.join('.')+'-converted.'+name.split('.').pop(); }

async function dlDocxFallback(text, filename) {
  try {
    const { Document, Packer, Paragraph, TextRun } = docx;
    const pars = text.split('\n').map(l => new Paragraph({ children: [new TextRun({ text: l, font: 'Kalimati' }) ] }));
    const doc = new Document({ sections: [{ children: pars }] });
    const buf = await Packer.toBlob(doc);
    const a = document.createElement('a'); a.href=URL.createObjectURL(buf); a.download=filename; a.click();
    URL.revokeObjectURL(a.href);
  } catch(e) { console.warn('docx fallback to txt'); dlText(text, filename.replace('.docx','.txt')); }
}

// ─── Utilities ──────────────────────────────────────
function dlText(text, filename) {
  const blob = new Blob([text], {type:'text/plain;charset=utf-8'});
  const a = document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=filename; a.click();
  URL.revokeObjectURL(a.href);
}
function readFileAsText(file) { return new Promise((res,rej)=>{ const r=new FileReader(); r.onload=()=>res(r.result); r.onerror=rej; r.readAsText(file,'UTF-8'); }); }
function readFileAsArrayBuffer(file) { return new Promise((res,rej)=>{ const r=new FileReader(); r.onload=()=>res(r.result); r.onerror=rej; r.readAsArrayBuffer(file); }); }
function fmtSize(b) { return b<1024?b+' B':b<1048576?(b/1024).toFixed(1)+' KB':(b/1048576).toFixed(1)+' MB'; }
function sleep(ms) { return new Promise(r=>setTimeout(r,ms)); }
function showToast(msg) {
  const t=document.getElementById('toast'); t.textContent=msg; t.classList.add('show');
  clearTimeout(t._timeout); t._timeout=setTimeout(()=>t.classList.remove('show'),2200);
}

// ─── PWA Registration ──────────────────────────────
function registerSW() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(e => console.log('SW registration optional:', e));
  }
}

// ─── Init ───────────────────────────────────────────
async function init() {
  await loadMap();
  initDarkMode();
  registerSW();
  const savedFS = localStorage.getItem('preeti-font-size');
  if (savedFS) { document.getElementById('font-size-slider').value = savedFS; changeFontSize(savedFS); }
  loadFromURLHash();
  if (document.getElementById('inp').value) convert();
  window.addEventListener('hashchange', loadFromURLHash);
}

// Expose global functions
window.setMode = setMode;
window.onFontChange = onFontChange;
window.swapAll = swapAll;
window.copyOut = copyOut;
window.pasteInput = pasteInput;
window.cleanText = cleanText;
window.downloadTxt = downloadTxt;
window.clearAll = clearAll;
window.toggleDarkMode = toggleDarkMode;
window.changeFontSize = changeFontSize;
window.onInputChange = onInputChange;
window.handleDrag = handleDrag;
window.handleDrop = handleDrop;
window.handleFiles = handleFiles;
window.removeFile = removeFile;
window.clearFiles = clearFiles;
window.convertAllFiles = convertAllFiles;
window.downloadAllFiles = downloadAllFiles;
window.downloadSingleFile = downloadSingleFile;

document.addEventListener('DOMContentLoaded', init);
