/**
 * preeti-engine.js — thenepal.io
 * Robust Preeti → Unicode (and reverse) conversion engine.
 * Loads preeti-map.json from the same origin.
 * Version: 2.0.0
 */

(function (global) {
  "use strict";

  // ─── State ───────────────────────────────────────────────────────────────
  let MAP       = null;   // parsed preeti-map.json
  let FWD       = {};     // flat char→unicode lookup  (all normal+shift+alt)
  let REV_MAP   = {};     // unicode→preeti (best-effort)
  let RULES     = [];     // pre-rules (longest first)
  let POST      = [];     // post-rules (regex)
  let READY     = false;
  const CALLBACKS = [];

  // ─── Load ────────────────────────────────────────────────────────────────
  async function load(mapPath) {
    mapPath = mapPath || "/preeti-map.json";
    try {
      const res = await fetch(mapPath);
      if (!res.ok) throw new Error("HTTP " + res.status);
      MAP = await res.json();
    } catch (e) {
      console.warn("[preeti-engine] Could not load map, using built-in fallback.", e);
      MAP = _builtinFallback();
    }
    _buildLookups();
    READY = true;
    CALLBACKS.forEach(fn => fn());
  }

  function onReady(fn) {
    if (READY) fn(); else CALLBACKS.push(fn);
  }

  // ─── Build flat lookups ──────────────────────────────────────────────────
  function _buildLookups() {
    FWD = {};
    const m = MAP.mappings;

    // Merge normal + shift + alt_codes into FWD
    [m.normal, m.shift, m.alt_codes].forEach(group => {
      if (!group) return;
      Object.assign(FWD, group);
    });

    // Build RULES array sorted longest-match first
    RULES = (MAP.rules || []).slice().sort(
      (a, b) => b.find.length - a.find.length
    );

    // Build POST array (regex)
    POST = (MAP.post_rules || []).map(r => ({
      re: new RegExp(r.find, "g"),
      rep: r.replace
    }));

    // Build reverse map (unicode → preeti key)
    REV_MAP = {};
    Object.entries(FWD).forEach(([k, v]) => {
      if (!REV_MAP[v]) REV_MAP[v] = k;
    });
  }

  // ─── Forward conversion: Preeti ASCII → Unicode ──────────────────────────
  /**
   * Main entry point.
   * @param {string} input  Raw Preeti-encoded text
   * @param {string} [font] "preeti" | "kantipur" | "pcsnepali"  (default "preeti")
   * @returns {string} Unicode Devanagari
   */
  function toUnicode(input, font) {
    if (!input) return "";
    font = font || "preeti";

    let text = input;

    // 1. Apply pre-rules (multi-char substitutions, longest match first)
    text = _applyPreRules(text);

    // 2. Character-by-character substitution
    text = _charConvert(text, font);

    // 3. Post-process: fix vowel ordering, punctuation, spaces
    text = _applyPostRules(text);

    // 4. Fix इ/ि positioning (must come before the consonant it modifies)
    text = _fixVowelOrder(text);

    return text;
  }

  function _applyPreRules(text) {
    // Sort rules by length descending so longer patterns match first
    let i = 0;
    let result = "";
    while (i < text.length) {
      let matched = false;
      for (const rule of RULES) {
        if (text.startsWith(rule.find, i)) {
          result += rule.replace;
          i += rule.find.length;
          matched = true;
          break;
        }
      }
      if (!matched) {
        result += text[i];
        i++;
      }
    }
    return result;
  }

  function _charConvert(text, font) {
    // For kantipur/pcsnepali we'd swap FWD; currently uses same map.
    // Extend here when kantipur-map.json is added.
    let out = "";
    for (let i = 0; i < text.length; i++) {
      const ch = text[i];
      out += FWD[ch] !== undefined ? FWD[ch] : ch;
    }
    return out;
  }

  function _applyPostRules(text) {
    for (const rule of POST) {
      text = text.replace(rule.re, rule.rep);
    }
    return text;
  }

  /**
   * Devanagari vowel sign ि (U+093F) must appear BEFORE the consonant visually
   * but Unicode stores it AFTER. Preeti sometimes emits it before — fix here.
   */
  function _fixVowelOrder(text) {
    // Pattern: ि followed by a consonant cluster → move ि after cluster
    // This handles cases like "ि + क्" → "क् + ि"
    return text.replace(
      /\u093F([\u0915-\u0939](?:\u094D[\u0915-\u0939])*)/g,
      "$1\u093F"
    );
  }

  // ─── Reverse conversion: Unicode → Preeti ASCII ──────────────────────────
  /**
   * @param {string} input  Unicode Devanagari text
   * @returns {string} Preeti ASCII
   */
  function toPreeti(input) {
    if (!input) return "";
    const keys = Object.keys(REV_MAP).sort((a, b) => b.length - a.length);
    let result = "";
    let i = 0;
    while (i < input.length) {
      let matched = false;
      for (const k of keys) {
        if (input.startsWith(k, i)) {
          result += REV_MAP[k];
          i += k.length;
          matched = true;
          break;
        }
      }
      if (!matched) {
        result += input[i];
        i++;
      }
    }
    return result;
  }

  // ─── Clean output ────────────────────────────────────────────────────────
  /**
   * Fix common issues in converted Unicode output.
   * @param {string} text
   * @returns {string}
   */
  function clean(text) {
    if (!text) return "";
    return text
      .replace(/\|/g, "।")          // pipe → danda
      .replace(/।([^\s\n])/g, "। $1") // space after danda
      .replace(/\s+।/g, "।")         // no space before danda
      .replace(/ {2,}/g, " ")         // collapse spaces
      .replace(/\n{3,}/g, "\n\n")     // max 2 blank lines
      .trim();
  }

  // ─── Detect if text is Preeti-encoded ────────────────────────────────────
  /**
   * Heuristic: Preeti text contains many ASCII chars that map to Devanagari.
   * Returns confidence 0–1.
   */
  function detectPreeti(text) {
    if (!text || !READY) return 0;
    const sample = text.slice(0, 200);
    let hits = 0;
    for (const ch of sample) {
      if (FWD[ch] && /[\u0900-\u097F]/.test(FWD[ch])) hits++;
    }
    return hits / Math.max(sample.length, 1);
  }

  // ─── Built-in fallback map ───────────────────────────────────────────────
  function _builtinFallback() {
    return {
      metadata: { version: "fallback" },
      mappings: {
        normal: {
          a:"ब",b:"द",c:"अ",d:"म",e:"भ",f:"ा",g:"न",h:"ज",
          i:"ष्",j:"व",k:"प",l:"ि",m:"ु",n:"ल",o:"य",p:"उ",
          q:"त्र",r:"च",s:"क",t:"त",u:"ग",v:"ख",w:"ध",x:"ह",
          y:"थ",z:"श",
          "0":"ण्","1":"ज्ञ","2":"द्द","3":"घ","4":"द्ध","5":"छ",
          "6":"ट","7":"ठ","8":"ड","9":"ढ",
          ".":"।",",":","," /":"र",";":"स","'":"ु","[":"ृ",
          "]":"े","\\":"्","-":"-","=":"="," ":" ","\n":"\n","\t":"\t"
        },
        shift: {
          A:"ब्",B:"द्य",C:"ऋ",D:"म्",E:"भ्",F:"ँ",G:"न्",H:"ज्",
          I:"क्ष्",J:"व्",K:"प्",L:"ी",M:"ः",N:"ल्",O:"इ",P:"ए",
          Q:"त्त",R:"च्",S:"क्",T:"त्",U:"ग्",V:"ख्",W:"ध्",X:"ह्",
          Y:"थ्",Z:"श्",
          "!":"१","@":"२","#":"३","$":"४","%":"५","^":"६",
          "&":"७","*":"८","(":"९",")":"०",
          ":":"स्","\"":"ू","{":"ै","}":"ौ","|":"्र",
          "_":"–","+":"ं","?":"रु","<":"?",">":"श्र","~":"ँ"
        },
        alt_codes: {}
      },
      rules: [
        {find:"cf]",replace:"ओ"},{find:"cfW",replace:"औ"},{find:"cf",replace:"आ"},
        {find:"O{",replace:"ई"},{find:"pm",replace:"ऊ"},{find:"P{",replace:"ऐ"},
        {find:"Em",replace:"झ"},{find:"f]",replace:"ो"},{find:"fW",replace:"ौ"},
        {find:"]{",replace:"ै"}
      ],
      post_rules: [
        {find:"ाे",replace:"ो"},{find:"ाै",replace:"ौ"},
        {find:"\\|",replace:"।"}
      ]
    };
  }

  // ─── Public API ──────────────────────────────────────────────────────────
  global.PreetiEngine = {
    load,
    onReady,
    toUnicode,
    toPreeti,
    clean,
    detectPreeti,
    get isReady() { return READY; }
  };

})(typeof window !== "undefined" ? window : global);
