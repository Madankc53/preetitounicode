/* Reducing-balance EMI maths. */
(function (root) {
  // P principal, annualPct nominal yearly rate in %, n months
  function emi(P, annualPct, n) {
    if (!(P > 0) || !(n > 0) || annualPct < 0) return NaN;
    var r = annualPct / 12 / 100;
    if (r === 0) return P / n;
    var f = Math.pow(1 + r, n);
    return P * r * f / (f - 1);
  }
  function schedule(P, annualPct, n) {
    var e = emi(P, annualPct, n), r = annualPct / 12 / 100, bal = P, rows = [];
    if (!isFinite(e)) return rows;
    for (var m = 1; m <= n; m++) {
      var interest = bal * r;
      var principal = m === n ? bal : e - interest;
      var pay = principal + interest;
      bal = bal - principal;
      if (bal < 1e-6) bal = 0;
      rows.push({ month: m, payment: pay, principal: principal, interest: interest, balance: bal });
    }
    return rows;
  }
  function summary(P, annualPct, n) {
    var e = emi(P, annualPct, n);
    if (!isFinite(e)) return null;
    var rows = schedule(P, annualPct, n), total = 0;
    for (var i = 0; i < rows.length; i++) total += rows[i].payment;
    return { emi: e, total: total, interest: total - P, rows: rows };
  }
  var api = { emi: emi, schedule: schedule, summary: summary };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.EMI = api;
})(typeof self !== 'undefined' ? self : this);
