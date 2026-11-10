/* Font-aware .docx converter for legacy Nepali fonts.
   Only runs set in a supported legacy font (Preeti / Kantipur) are converted; English and Unicode runs are left alone.
   Returns the converted text and a new .docx with formatting kept. Runs fully in the browser. */
(function (root) {
  var W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main';
  var JSZIP_URL = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js';
  var PARTS = /^word\/(document|header\d*|footer\d*|footnotes|endnotes)\.xml$/;

  function loadJSZip() {
    if (root.JSZip) return Promise.resolve(root.JSZip);
    return new Promise(function (res, rej) {
      var s = document.createElement('script'); s.src = JSZIP_URL;
      s.onload = function () { root.JSZip ? res(root.JSZip) : rej(new Error('JSZip missing')); };
      s.onerror = function () { rej(new Error('Could not load the .docx library')); };
      document.head.appendChild(s);
    });
  }
  function kids(el, name) { var o = []; for (var c = el && el.firstChild; c; c = c.nextSibling) if (c.nodeType === 1 && c.localName === name) o.push(c); return o; }
  function first(el, name) { return kids(el, name)[0] || null; }
  function attr(el, n) { return el ? (el.getAttributeNS(W, n) || el.getAttribute('w:' + n)) : null; }
  function fontOf(rPr) {
    var f = first(rPr, 'rFonts'); if (!f) return null;
    return attr(f, 'ascii') || attr(f, 'hAnsi') || attr(f, 'cs') || attr(f, 'eastAsia');
  }
  function legacyKind(name) {
    if (!name) return null;
    if (/preeti/i.test(name)) return 'preeti';
    if (/kantipur/i.test(name)) return 'kantipur';
    if (/sagarmatha|himalb|himali|pcs\s*nepali|shangrila|ganess|nepali\s*bold|aakriti/i.test(name)) return 'unsupported';
    return null;
  }
  function parseStyles(xml) {
    var map = {}, def = null; if (!xml) return { map: map, def: def };
    var d = new DOMParser().parseFromString(xml, 'application/xml');
    var dd = d.getElementsByTagNameNS(W, 'rPrDefault')[0]; if (dd) def = fontOf(first(dd, 'rPr'));
    Array.prototype.forEach.call(d.getElementsByTagNameNS(W, 'style'), function (st) {
      var id = attr(st, 'styleId'); var b = first(st, 'basedOn');
      map[id] = { font: fontOf(first(st, 'rPr')), based: b ? attr(b, 'val') : null };
    });
    return { map: map, def: def };
  }
  function styleFont(styles, id) {
    var guard = 0; while (id && styles.map[id] && guard++ < 12) { if (styles.map[id].font) return styles.map[id].font; id = styles.map[id].based; }
    return null;
  }
  function runText(r) {
    var s = '';
    for (var c = r.firstChild; c; c = c.nextSibling) {
      if (c.nodeType !== 1) continue;
      if (c.localName === 't') s += c.textContent; else if (c.localName === 'tab') s += '\t'; else if (c.localName === 'br' || c.localName === 'cr') s += '\n';
    }
    return s;
  }
  function setRunText(r, text) {
    var ts = kids(r, 't'); var t = ts[0];
    if (!t) { t = r.ownerDocument.createElementNS(W, 'w:t'); r.appendChild(t); }
    t.textContent = text; t.setAttribute('xml:space', 'preserve');
    for (var i = 1; i < ts.length; i++) r.removeChild(ts[i]);
    kids(r, 'tab').forEach(function (n) { r.removeChild(n); });
  }
  function setFont(r, name) {
    var doc = r.ownerDocument, rPr = first(r, 'rPr');
    if (!rPr) { rPr = doc.createElementNS(W, 'w:rPr'); r.insertBefore(rPr, r.firstChild); }
    var f = first(rPr, 'rFonts');
    if (!f) { f = doc.createElementNS(W, 'w:rFonts'); rPr.insertBefore(f, rPr.firstChild); }
    ['ascii', 'hAnsi', 'cs', 'eastAsia'].forEach(function (a) { f.setAttributeNS(W, 'w:' + a, name); });
    ['asciiTheme', 'hAnsiTheme', 'cstheme', 'eastAsiaTheme'].forEach(function (a) { f.removeAttributeNS(W, a); });
  }

  // convertFn(text, kind) -> unicode text
  function processPart(xml, styles, convertFn, stats, forceAll) {
    var doc = new DOMParser().parseFromString(xml, 'application/xml');
    var out = [];
    Array.prototype.forEach.call(doc.getElementsByTagNameNS(W, 'p'), function (p) {
      var pPr = first(p, 'pPr'), pStyle = pPr && first(pPr, 'pStyle');
      var pFont = fontOf(first(pPr, 'rPr')) || styleFont(styles, pStyle && attr(pStyle, 'val')) || styles.def;
      var groups = [], cur = null, para = '';
      Array.prototype.forEach.call(p.getElementsByTagNameNS(W, 'r'), function (r) {
        if (r.parentNode !== p && !(r.parentNode.localName === 'hyperlink' || r.parentNode.localName === 'smartTag' || r.parentNode.localName === 'ins')) return;
        var rPr = first(r, 'rPr'), rs = rPr && first(rPr, 'rStyle');
        var font = fontOf(rPr) || styleFont(styles, rs && attr(rs, 'val')) || pFont;
        var kind = legacyKind(font);
        if (font) stats.fonts[font] = (stats.fonts[font] || 0) + 1;
        var text = runText(r);
        var conv = kind === 'preeti' || kind === 'kantipur' || (forceAll && !kind && text.trim() && !/[\u0900-\u097F]/.test(text));
        if (kind === 'unsupported' && text.trim()) stats.unsupported = true;
        if (conv) { if (!cur) { cur = { runs: [], text: '', kind: kind || forceAll }; groups.push(cur); } cur.runs.push(r); cur.text += text; }
        else { cur = null; para += text; if (text.trim()) stats.kept++; }
        r.__g = conv ? cur : null; r.__t = text;
      });
      // rebuild paragraph text in order and convert grouped runs
      para = '';
      Array.prototype.forEach.call(p.getElementsByTagNameNS(W, 'r'), function (r) {
        if (r.__g === undefined) return;
        if (r.__g) {
          var g = r.__g;
          if (!g.done) {
            g.done = true; g.out = convertFn(g.text, g.kind === 'kantipur' ? 'kantipur' : 'preeti');
            stats.converted += g.text.trim() ? 1 : 0; stats.chars += g.text.length;
            setRunText(g.runs[0], g.out); setFont(g.runs[0], 'Mangal');
            for (var i = 1; i < g.runs.length; i++) p.removeChild && g.runs[i].parentNode.removeChild(g.runs[i]);
            para += g.out;
          }
        } else para += r.__t;
      });
      out.push(para);
    });
    return { text: out.join('\n'), xml: new XMLSerializer().serializeToString(doc) };
  }

  async function convertDocx(buf, convertFn, opts) {
    var JSZip = await loadJSZip();
    var zip = await JSZip.loadAsync(buf);
    var stylesXml = zip.file('word/styles.xml') ? await zip.file('word/styles.xml').async('string') : '';
    var styles = parseStyles(stylesXml);
    var names = Object.keys(zip.files).filter(function (n) { return PARTS.test(n); });
    // pass 1: detect whether any supported legacy font is used
    var probe = { fonts: {}, kept: 0, converted: 0, chars: 0 }, any = false;
    for (var i = 0; i < names.length; i++) {
      var xml = await zip.file(names[i]).async('string');
      var d = new DOMParser().parseFromString(xml, 'application/xml');
      Array.prototype.forEach.call(d.getElementsByTagNameNS(W, 'r'), function (r) {
        var rPr = first(r, 'rPr'), rs = rPr && first(rPr, 'rStyle');
        var p = r.parentNode; while (p && p.localName !== 'p') p = p.parentNode;
        var pp = p && first(p, 'pPr'), ps = pp && first(pp, 'pStyle');
        var f = fontOf(rPr) || styleFont(styles, rs && attr(rs, 'val')) || fontOf(first(pp, 'rPr')) || styleFont(styles, ps && attr(ps, 'val')) || styles.def;
        var k = legacyKind(f); if (k === 'preeti' || k === 'kantipur') any = true;
      });
    }
    var stats = { fonts: {}, kept: 0, converted: 0, chars: 0, unsupported: false, forced: !any };
    var text = '';
    for (var j = 0; j < names.length; j++) {
      var x = await zip.file(names[j]).async('string');
      var res = processPart(x, styles, convertFn, stats, !any);
      zip.file(names[j], res.xml);
      if (names[j] === 'word/document.xml') text = res.text;
    }
    var blob = await zip.generateAsync({ type: 'blob', mimeType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
    return { text: text, blob: blob, stats: stats };
  }
  root.DocxLegacyConvert = { convert: convertDocx };
})(typeof self !== 'undefined' ? self : this);
