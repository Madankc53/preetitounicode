/* Roman to Nepali Unicode (phonetic). See the scheme table on the page. */
(function (root) {
  var CONS = [
    ['ksh','क्ष'],['chh','छ'],['shh','ष'],['gy','ज्ञ'],['tr','त्र'],
    ['kh','ख'],['gh','घ'],['Ng','ङ'],['ch','च'],['jh','झ'],['Th','ठ'],['Dh','ढ'],['th','थ'],['dh','ध'],['ph','फ'],['bh','भ'],['sh','श'],['Sh','ष'],
    ['k','क'],['g','ग'],['c','च'],['j','ज'],['T','ट'],['D','ड'],['N','ण'],['t','त'],['d','द'],['n','न'],['p','प'],['f','फ'],['b','ब'],['m','म'],
    ['y','य'],['r','र'],['l','ल'],['w','व'],['v','व'],['s','स'],['h','ह'],['z','ज'],['Y','ञ']
  ];
  var VOW = [ // roman, independent, matra
    ['aa','आ','ा'],['ai','ऐ','ै'],['au','औ','ौ'],['ee','ई','ी'],['oo','ऊ','ू'],
    ['a','अ',''],['i','इ','ि'],['u','उ','ु'],['e','ए','े'],['o','ओ','ो'],['A','आ','ा'],['I','ई','ी'],['U','ऊ','ू'],['R','ऋ','ृ']
  ];
  var MARK = { 'M': 'ं', '~': 'ँ', 'H': 'ः' };
  var HAL = '्';

  function starts(s, i, tok) { return s.substr(i, tok.length) === tok; }
  function findCons(s, i) { for (var k = 0; k < CONS.length; k++) if (starts(s, i, CONS[k][0])) return CONS[k]; return null; }
  function findVow(s, i) { for (var k = 0; k < VOW.length; k++) if (starts(s, i, VOW[k][0])) return VOW[k]; return null; }

  function digits(str) { return str.replace(/[0-9]/g, function (d) { return String.fromCharCode(0x966 + (+d)); }); }

  function word(w) {
    // A capitalised name such as "Nepal" or "Ram" is read as lowercase.
    if (/^[A-Z][a-z]+$/.test(w)) w = w.charAt(0).toLowerCase() + w.slice(1);
    var out = '', i = 0, prevVowelOrStart = true;
    while (i < w.length) {
      var c = findCons(w, i);
      if (c) {
        out += c[1]; i += c[0].length;
        var v = findVow(w, i);
        if (v) { out += v[2]; i += v[0].length; prevVowelOrStart = true; continue; }
        if (w.charAt(i) === '_') { out += HAL; i++; prevVowelOrStart = false; continue; }
        if (i < w.length && findCons(w, i)) { out += HAL; }
        prevVowelOrStart = false;
        continue;
      }
      var v2 = findVow(w, i);
      if (v2) { out += v2[1]; i += v2[0].length; prevVowelOrStart = true; continue; }
      var ch = w.charAt(i);
      if (MARK[ch]) { out += MARK[ch]; i++; continue; }
      out += ch; i++;
    }
    return out;
  }

  function convert(text, opts) {
    opts = opts || {};
    var useDigits = opts.digits !== false;
    var res = '', i = 0, s = String(text == null ? '' : text);
    while (i < s.length) {
      var ch = s.charAt(i);
      if (ch === '{') { // literal block
        var j = s.indexOf('}', i + 1);
        if (j > -1) { res += s.slice(i + 1, j); i = j + 1; continue; }
      }
      if (/[A-Za-z_~]/.test(ch)) {
        var j2 = i; while (j2 < s.length && /[A-Za-z_~]/.test(s.charAt(j2))) j2++;
        res += word(s.slice(i, j2)); i = j2; continue;
      }
      if (/[0-9]/.test(ch)) {
        var j3 = i; while (j3 < s.length && /[0-9.]/.test(s.charAt(j3)) && !(s.charAt(j3) === '.' && !/[0-9]/.test(s.charAt(j3 + 1) || ''))) j3++;
        var num = s.slice(i, j3); res += useDigits ? digits(num) : num; i = j3; continue;
      }
      if (ch === '.') { res += '।'; i++; continue; }
      res += ch; i++;
    }
    return res;
  }
  var api = { convert: convert, word: word, CONS: CONS, VOW: VOW };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.NepaliTyping = api;
})(typeof self !== 'undefined' ? self : this);
