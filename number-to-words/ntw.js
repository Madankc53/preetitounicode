/* Number to words (Nepali and English, lakh/crore system). Exact decimal-string maths, no floats. */
(function (root) {
  var NE = ['शुन्य','एक','दुई','तीन','चार','पाँच','छ','सात','आठ','नौ','दश','एघार','बाह्र','तेह्र','चौध','पन्ध्र','सोह्र','सत्र','अठार','उन्नाइस','बीस','एक्काइस','बाइस','तेइस','चौबीस','पच्चीस','छब्बीस','सत्ताइस','अठ्ठाइस','उनन्तीस','तीस','एकतीस','बत्तीस','तेत्तीस','चौंतीस','पैंतीस','छत्तीस','सैंतीस','अठतीस','उनन्चालीस','चालीस','एकचालीस','बयालीस','त्रिचालीस','चौवालीस','पैंतालीस','छयालीस','सतचालीस','अठचालीस','उनन्चास','पचास','एकाउन्न','बाउन्न','त्रिपन्न','चवन्न','पचपन्न','छपन्न','सन्ताउन्न','अन्ठाउन्न','उनन्साठी','साठी','एकसट्ठी','बयसट्ठी','त्रिसट्ठी','चौसट्ठी','पैंसट्ठी','छयसट्ठी','सतसट्ठी','अठसट्ठी','उनन्सत्तरी','सत्तरी','एकहत्तर','बहत्तर','त्रिहत्तर','चौहत्तर','पचहत्तर','छयहत्तर','सतहत्तर','अठहत्तर','उनासी','असी','एकासी','बयासी','त्रियासी','चौरासी','पचासी','छयासी','सतासी','अठासी','उनान्नब्बे','नब्बे','एकान्नब्बे','बयान्नब्बे','त्रियान्नब्बे','चौरान्नब्बे','पन्चान्नब्बे','छयान्नब्बे','सन्तान्नब्बे','अन्ठान्नब्बे','उनान्सय'];
  var EN_ONES = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve','Thirteen','Fourteen','Fifteen','Sixteen','Seventeen','Eighteen','Nineteen'];
  var EN_TENS = ['','','Twenty','Thirty','Forty','Fifty','Sixty','Seventy','Eighty','Ninety'];
  var NE_SCALE = ['', 'हजार', 'लाख', 'करोड', 'अर्ब', 'खर्ब'];
  var EN_SCALE = ['', 'Thousand', 'Lakh', 'Crore', 'Arab', 'Kharab'];
  var MAX_DIGITS = 13;

  function en99(n) {
    if (n < 20) return EN_ONES[n];
    var t = EN_TENS[Math.floor(n / 10)], o = n % 10;
    return o ? t + '-' + EN_ONES[o] : t;
  }
  function ne99(n) { return NE[n]; }

  // Split integer digit string into [ones(3), then pairs] groups, low to high
  function groups(s) {
    var g = [], i = s.length;
    g.push(parseInt(s.slice(Math.max(0, i - 3)), 10)); i -= 3;
    while (i > 0) { g.push(parseInt(s.slice(Math.max(0, i - 2), i), 10)); i -= 2; }
    return g;
  }
  function words(s, lang) {
    if (/^0+$/.test(s)) return lang === 'ne' ? NE[0] : EN_ONES[0];
    var g = groups(s), out = [];
    for (var k = g.length - 1; k >= 0; k--) {
      var v = g[k]; if (!v) continue;
      var part;
      if (k === 0) {
        var h = Math.floor(v / 100), r = v % 100, p = [];
        if (h) p.push(lang === 'ne' ? NE[h] + ' सय' : EN_ONES[h] + ' Hundred');
        if (r) p.push(lang === 'ne' ? ne99(r) : en99(r));
        part = p.join(' ');
        if (lang === 'en' && h && r) part = EN_ONES[h] + ' Hundred and ' + en99(r);
      } else {
        part = (lang === 'ne' ? ne99(v) + ' ' + NE_SCALE[k] : en99(v) + ' ' + EN_SCALE[k]);
      }
      out.push(part);
    }
    return out.join(' ');
  }

  // Parse user text into {int:'123', frac:'05'} ; returns {error} on bad input
  function parse(text) {
    var t = String(text == null ? '' : text).trim();
    t = t.replace(/[०-९]/g, function (c) { return String(c.charCodeAt(0) - 0x966); });
    t = t.replace(/[,\s]/g, '');
    if (!t) return { error: 'empty' };
    if (!/^\d*\.?\d*$/.test(t) || !/\d/.test(t)) return { error: 'invalid' };
    var parts = t.split('.');
    var ip = (parts[0] || '0').replace(/^0+(?=\d)/, '');
    var fp = parts[1] || '';
    if (ip.length > MAX_DIGITS) return { error: 'toolarge' };
    if (fp.length > 2 && /[1-9]/.test(fp.slice(2))) return { error: 'precision' };
    fp = (fp + '00').slice(0, 2);
    return { int: ip, frac: fp };
  }

  function convert(text) {
    var p = parse(text);
    if (p.error) return p;
    var paisa = parseInt(p.frac, 10), hasInt = !/^0+$/.test(p.int);
    var ne = [], en = [];
    if (hasInt || !paisa) {
      ne.push(words(p.int, 'ne') + ' रुपैयाँ');
      en.push(words(p.int, 'en') + ' Rupees');
    }
    if (paisa) {
      ne.push(words(String(paisa), 'ne') + ' पैसा');
      en.push(words(String(paisa), 'en') + ' Paisa');
    }
    var nes = ne.join(' ') + ' मात्र';
    var ens = en.join(' and ') + ' Only';
    if (hasInt && /^1 /.test('')) {}
    return { ok: true, ne: nes, en: ens, int: p.int, frac: p.frac,
             neNumber: words(p.int, 'ne'), enNumber: words(p.int, 'en') };
  }

  var api = { convert: convert, parse: parse, words: words, NE: NE, MAX_DIGITS: MAX_DIGITS };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.NTW = api;
})(typeof self !== 'undefined' ? self : this);
