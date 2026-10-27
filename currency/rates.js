/* Exchange rates for the currency pages: window.NPRRates
 *
 * Gets today's rates from a public, free rates feed (daily data, all values
 * per 1 US dollar). Tries several mirrors of the same feed in turn.
 *
 *   NPRRates.load()  -> Promise<{ rates, date, source }>
 *       source 'live'   : fetched just now
 *       source 'cached' : network failed; the last good rates saved in this
 *                         browser are returned together with their own date
 *       rejects with Error('unavailable') if there is neither
 *   NPRRates.convert(rates, amount, 'AED', 'NPR') -> number
 *
 * There is deliberately NO built-in fallback number: if no real rate is
 * available the page says so instead of showing a made-up one.
 */
(function (global) {
  'use strict';

  var CACHE_KEY = 'thenepal.rates.v1';
  var TIMEOUT_MS = 6000;
  var SOURCES = [
    'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json',
    'https://latest.currency-api.pages.dev/v1/currencies/usd.json',
    'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json'
  ];

  function fetchJSON(url, ms) {
    return new Promise(function (resolve, reject) {
      var finished = false;
      var ctl = 'AbortController' in global ? new AbortController() : null;
      var timer = setTimeout(function () {
        if (finished) return;
        finished = true;
        if (ctl) ctl.abort();
        reject(new Error('timeout'));
      }, ms);
      var opts = ctl ? { signal: ctl.signal, cache: 'no-cache' } : { cache: 'no-cache' };
      fetch(url, opts)
        .then(function (r) {
          if (!r.ok) throw new Error('http ' + r.status);
          return r.json();
        })
        .then(function (json) {
          if (finished) return;
          finished = true;
          clearTimeout(timer);
          resolve(json);
        })
        .catch(function (err) {
          if (finished) return;
          finished = true;
          clearTimeout(timer);
          reject(err);
        });
    });
  }

  // Turn the feed's {date, usd:{npr:..., aed:...}} into {rates:{NPR:..}, date}.
  // Reject anything that does not look right rather than show a wrong number.
  function normalise(json) {
    if (!json || typeof json.usd !== 'object' || json.usd === null) return null;
    var rates = {};
    for (var code in json.usd) {
      var v = json.usd[code];
      if (typeof v === 'number' && isFinite(v) && v > 0) rates[code.toUpperCase()] = v;
    }
    rates.USD = 1;
    // Sanity check: 1 USD is worth somewhere between 50 and 500 rupees.
    if (!rates.NPR || rates.NPR < 50 || rates.NPR > 500) return null;
    return { rates: rates, date: String(json.date || '') };
  }

  function readCache() {
    try {
      var c = JSON.parse(localStorage.getItem(CACHE_KEY));
      if (c && c.rates && c.rates.NPR) return c;
    } catch (e) { /* storage blocked or corrupt: ignore */ }
    return null;
  }

  function writeCache(d) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({ rates: d.rates, date: d.date, saved: Date.now() }));
    } catch (e) { /* storage blocked or full: ignore */ }
  }

  function load() {
    var i = 0;
    function next() {
      if (i >= SOURCES.length) {
        var c = readCache();
        if (c) return Promise.resolve({ rates: c.rates, date: c.date, saved: c.saved, source: 'cached' });
        return Promise.reject(new Error('unavailable'));
      }
      return fetchJSON(SOURCES[i++], TIMEOUT_MS)
        .then(function (json) {
          var d = normalise(json);
          if (!d) throw new Error('bad data');
          d.source = 'live';
          writeCache(d);
          return d;
        })
        .catch(next);
    }
    return next();
  }

  function convert(rates, amount, from, to) {
    if (!rates || !rates[from] || !rates[to]) return NaN;
    return (amount / rates[from]) * rates[to];
  }

  global.NPRRates = { load: load, convert: convert };
})(window);
