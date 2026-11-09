/* Nepali Unicode -> Preeti (legacy font) converter.
   Original implementation. Output is the keystroke text to which the Preeti font is applied. */
(function (root) {
  var HALF = { 'क':'S','ख':'V','ग':'U','घ':'£','च':'R','ज':'H','झ':'‰','ञ':'~','ण':'0','त':'T','थ':'Y','ध':'W','न':'G','प':'K','ब':'A','भ':'E','म':'D','ल':'N','व':'J','श':'Z','ष':'i','स':':','ह':'X','फ':'ˆ' };
  var FULL = { 'क':'s','ख':'v','ग':'u','घ':'3','ङ':'ª','च':'r','छ':'5','ज':'h','झ':'em','ञ':'`','ट':'6','ठ':'7','ड':'8','ढ':'9','ण':'0f','त':'t','थ':'y','द':'b','ध':'w','न':'g','प':'k','फ':'km','ब':'a','भ':'e','म':'d','य':'o','र':'/','ल':'n','व':'j','श':'z','ष':'if','स':';','ह':'x' };
  // conjunct glyphs that Preeti draws as one key (full form when they end a cluster)
  var SPECIAL = [
    ['क्ष','If'],['ज्ञ','1'],['त्र','q'],['श्र','>'],['द्ध','4'],['द्द','2'],['द्य','B'],['त्त','Q']
  ];
  var SPECIAL_HALF = { 'क्ष':'I' };
  var MATRA = { 'ा':'f','ी':'L','ु':"'",'ू':'"','ृ':'[','े':']','ै':'}','ो':'f]','ौ':'f}' };
  var MARK = { 'ं':'+','ँ':'F','ः':'M' };
  var VOWEL = { 'अ':'c','आ':'cf','इ':'O','ई':'O{','उ':'p','ऊ':'pm','ऋ':'C','ए':'P','ऐ':'P{','ओ':'cf]','औ':'cf}' };
  var DIGIT = { '०':')','१':'!','२':'@','३':'#','४':'$','५':'%','६':'^','७':'&','८':'*','९':'(' };
  var PUNCT = { '।':'.','(':'-',')':'_','.':'=','॥':'..' };
  var VIRAMA = '्';
  var isCons = function (c) { return c && c >= 'क' && c <= 'ह' || c === 'क़' || c === 'ख़' || c === 'ग़' || c === 'ज़' || c === 'ड़' || c === 'ढ़' || c === 'फ़' || c === 'य़'; };

  function encodeCluster(cons, hasReph) {
    // cons: array of consonant letters forming one conjunct cluster (reph already removed)
    var out = '', i = 0;
    while (i < cons.length) {
      var last = i === cons.length - 1, done = false;
      for (var k = 0; k < SPECIAL.length && !done; k++) {
        var parts = SPECIAL[k][0].split(VIRAMA);
        if (parts.length > cons.length - i) continue;
        var ok = true; for (var p = 0; p < parts.length; p++) if (cons[i + p] !== parts[p]) { ok = false; break; }
        if (!ok) continue;
        var endsHere = i + parts.length === cons.length;
        out += SPECIAL[k][1] + (endsHere ? '' : '\\'); i += parts.length; done = true;
      }
      if (done) continue;
      var c = cons[i];
      if (cons[i + 1] === 'र' && FULL[c] !== undefined && c !== 'र') { // conjunct with ra: प्र -> k|
        var tail = i + 2 === cons.length;
        out += FULL[c] + (/[टठडढ]/.test(c) ? '«' : '|') + (tail ? '' : '\\');
        i += 2; continue;
      }
      if (!last) out += HALF[c] !== undefined ? HALF[c] : (FULL[c] || c) + '\\';
      else out += FULL[c] !== undefined ? FULL[c] : c;
      i++;
    }
    return out;
  }

  function convert(text) {
    var s = String(text == null ? '' : text).replace(/[‌‍]/g, '');
    var chars = Array.from(s), out = '', i = 0;
    while (i < chars.length) {
      var ch = chars[i];
      if (isCons(ch)) {
        var cons = [ch], reph = false;
        i++;
        while (chars[i] === VIRAMA && isCons(chars[i + 1])) { cons.push(chars[i + 1]); i += 2; }
        var halant = false;
        if (chars[i] === VIRAMA) { halant = true; i++; }
        if (cons[0] === 'र' && cons.length > 1) { reph = true; cons.shift(); }
        var ikar = '', after = '', matras = '';
        while (i < chars.length && (MATRA[chars[i]] || chars[i] === 'ि' || MARK[chars[i]])) {
          var m = chars[i];
          if (m === 'ि') ikar = 'l'; else if (MATRA[m]) matras += MATRA[m]; else after += MARK[m];
          i++;
        }
        var body;
        if (cons.length === 1 && cons[0] === 'र' && !halant && !ikar && (matras === "'" || matras === '"')) {
          body = matras === "'" ? '?' : '¿'; matras = '';
        } else {
          body = encodeCluster(cons, reph);
          if (halant) body += '\\';
        }
        out += ikar + body + matras + (reph ? '{' : '') + after;
        continue;
      }
      if (VOWEL[ch]) {
        out += VOWEL[ch]; i++;
        while (i < chars.length && (MARK[chars[i]] || MATRA[chars[i]])) { out += MARK[chars[i]] || MATRA[chars[i]]; i++; }
        continue;
      }
      out += DIGIT[ch] !== undefined ? DIGIT[ch] : PUNCT[ch] !== undefined ? PUNCT[ch] : ch;
      i++;
    }
    return out;
  }
  var api = { convert: convert };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.PreetiU2P = api;
})(typeof self !== 'undefined' ? self : this);
