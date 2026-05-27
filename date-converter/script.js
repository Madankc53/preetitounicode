/**
 * Nepali Date Converter - script.js
 * BS↔AD using exact day-offset method
 * Base: 2000-01-01 BS = 1943-04-14 AD
 * Verified against Hamro Patro
 */
"use strict";

const BS_START = 2000, BS_END = 2090;
const AD_BASE  = new Date(1943, 3, 14); // April 14 1943

/* ── Helpers ── */
function addDays(date, n) {
  const d = new Date(date.getTime());
  d.setDate(d.getDate() + n);
  return d;
}
function bsDayOffset(bsY, bsM, bsD) {
  let off = 0;
  for (let y = BS_START; y < bsY; y++) BS_DATA[y].forEach(x => off += x);
  for (let m = 0; m < bsM - 1; m++) off += BS_DATA[bsY][m];
  return off + bsD - 1;
}
function formatAD(y, m, d) {
  const mn = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"];
  return mn[m-1] + " " + String(d).padStart(2,"0") + ", " + y;
}
function getNepaliMonth(i, lang) {
  return lang === "np" ? BS_MONTHS_NP[i-1] : BS_MONTHS_EN[i-1];
}
function getDayName(dt, lang) {
  return lang === "np" ? DAYS_NP[dt.getDay()] : DAYS_EN[dt.getDay()];
}

/* ── Validate ── */
function validateBSDate(y, m, d) {
  y = +y; m = +m; d = +d;
  if (!y || !m || !d) return "Please fill year, month and day.";
  if (y < BS_START || y > BS_END) return "Year must be 2000–2090 BS.";
  if (m < 1 || m > 12) return "Month must be 1–12.";
  if (!BS_DATA[y]) return "Year data not available.";
  const max = BS_DATA[y][m-1];
  if (d < 1 || d > max) return BS_MONTHS_EN[m-1]+" "+y+" has "+max+" days. Day "+d+" is invalid.";
  return null;
}
function validateADDate(y, m, d) {
  y = +y; m = +m; d = +d;
  if (!y || !m || !d) return "Please fill year, month and day.";
  const dt = new Date(y, m-1, d);
  if (dt.getFullYear()!==y || dt.getMonth()!==m-1 || dt.getDate()!==d)
    return "Invalid date (e.g. Feb 30 doesn't exist).";
  if (y < 1943 || y > 2034) return "Supported range: approx 1943–2034 AD.";
  return null;
}

/* ── Converters ── */
function convertBSToAD(bsY, bsM, bsD) {
  const err = validateBSDate(bsY, bsM, bsD);
  if (err) return { error: err };
  const adDate = addDays(AD_BASE, bsDayOffset(+bsY, +bsM, +bsD));
  const dow = adDate.getDay();
  return { adDate, adYear: adDate.getFullYear(), adMonth: adDate.getMonth()+1,
           adDay: adDate.getDate(), dayName: DAYS_EN[dow], dayNameNP: DAYS_NP[dow] };
}
function convertADToBS(adY, adM, adD) {
  const err = validateADDate(adY, adM, adD);
  if (err) return { error: err };
  const adDate = new Date(+adY, +adM-1, +adD);
  let rem = Math.round((adDate - AD_BASE) / 86400000);
  if (rem < 0) return { error: "Date is before supported range." };
  let bsY = BS_START;
  while (bsY <= BS_END) {
    const yd = BS_DATA[bsY].reduce((a,b)=>a+b,0);
    if (rem < yd) break;
    rem -= yd; bsY++;
  }
  if (bsY > BS_END) return { error: "Date exceeds 2090 BS." };
  let bsM = 1;
  for (let m = 0; m < 12; m++) {
    if (rem < BS_DATA[bsY][m]) { bsM = m+1; break; }
    rem -= BS_DATA[bsY][m];
  }
  const bsD = rem + 1, dow = adDate.getDay();
  return { bsYear: bsY, bsMonth: bsM, bsDay: bsD,
           monthName: BS_MONTHS_EN[bsM-1], monthNameNP: BS_MONTHS_NP[bsM-1],
           dayName: DAYS_EN[dow], dayNameNP: DAYS_NP[dow] };
}
function getTodayBS() {
  const n = new Date();
  return convertADToBS(n.getFullYear(), n.getMonth()+1, n.getDate());
}

/* ── Toast ── */
function showToast(msg) {
  let t = document.getElementById("toast");
  if (!t) { t = document.createElement("div"); t.id="toast"; document.body.appendChild(t); }
  t.textContent = msg; t.classList.add("show");
  clearTimeout(t._t); t._t = setTimeout(()=>t.classList.remove("show"), 2500);
}
function copyResult(txt) {
  if (!txt) return;
  navigator.clipboard.writeText(txt).then(()=>showToast("✓ Copied!"))
    .catch(()=>{ const el=document.createElement("textarea"); el.value=txt;
      el.style.cssText="position:fixed;opacity:0"; document.body.appendChild(el);
      el.select(); document.execCommand("copy"); document.body.removeChild(el);
      showToast("✓ Copied!"); });
}
function shareResult(txt) {
  if (navigator.share) navigator.share({title:"Nepali Date Converter",text:txt,url:location.href}).catch(()=>{});
  else { copyResult(txt); showToast("✓ Link copied — share it!"); }
}

/* ── State ── */
let currentResult = "";

/* ── Update BS day max hint ── */
function updateBSDayHint() {
  const y = +document.getElementById("bs-year").value;
  const m = +document.getElementById("bs-month").value;
  const hint = document.getElementById("bs-day-hint");
  if (y >= BS_START && y <= BS_END && m >= 1 && m <= 12 && BS_DATA[y]) {
    hint.textContent = "1–" + BS_DATA[y][m-1];
  } else { hint.textContent = ""; }
}

/* ── Render results ── */
function doConvertBSToAD() {
  const y = document.getElementById("bs-year").value.trim();
  const m = document.getElementById("bs-month").value;
  const d = document.getElementById("bs-day").value.trim();
  const resEl = document.getElementById("bs-result");
  const actEl = document.getElementById("bs-actions");
  if (!y || !m || !d) { resEl.innerHTML=""; actEl.style.display="none"; return; }
  const r = convertBSToAD(y, m, d);
  if (r.error) {
    resEl.innerHTML = `<p class="err">⚠ ${r.error}</p>`;
    actEl.style.display="none"; currentResult=""; return;
  }
  const adFmt = formatAD(r.adYear, r.adMonth, r.adDay);
  currentResult = `${y} ${BS_MONTHS_EN[+m-1]} ${d} BS = ${adFmt} AD (${r.dayName})`;
  resEl.innerHTML = `<div class="result-card">
    <span class="r-label">AD Date</span>
    <span class="r-value">${adFmt}</span>
    <div class="tags"><span class="tag">${r.dayName}</span><span class="tag np">${r.dayNameNP}</span></div>
  </div>`;
  actEl.style.display="flex";
}
function doConvertADToBS() {
  const y = document.getElementById("ad-year").value.trim();
  const m = document.getElementById("ad-month").value.trim();
  const d = document.getElementById("ad-day").value.trim();
  const resEl = document.getElementById("ad-result");
  const actEl = document.getElementById("ad-actions");
  if (!y || !m || !d) { resEl.innerHTML=""; actEl.style.display="none"; return; }
  const r = convertADToBS(y, m, d);
  if (r.error) {
    resEl.innerHTML = `<p class="err">⚠ ${r.error}</p>`;
    actEl.style.display="none"; currentResult=""; return;
  }
  const bsFmt = `${r.bsYear} ${r.monthName} ${r.bsDay}`;
  const bsNP  = `${toNepaliDigits(r.bsYear)} ${r.monthNameNP} ${toNepaliDigits(r.bsDay)}`;
  currentResult = `${formatAD(+y,+m,+d)} AD = ${bsFmt} BS (${r.dayName})`;
  resEl.innerHTML = `<div class="result-card">
    <span class="r-label">BS Date</span>
    <span class="r-value">${bsFmt}</span>
    <div class="r-np">${bsNP}</div>
    <div class="tags"><span class="tag">${r.dayName}</span><span class="tag np">${r.dayNameNP}</span><span class="tag">${r.monthName}</span></div>
  </div>`;
  actEl.style.display="flex";
}

/* ── Today widget ── */
function renderToday() {
  const t = getTodayBS(); if (t.error) return;
  const now = new Date();
  document.getElementById("tw-ad").textContent = formatAD(now.getFullYear(),now.getMonth()+1,now.getDate());
  document.getElementById("tw-bs").textContent = `${t.bsYear} ${t.monthName} ${t.bsDay}`;
  document.getElementById("tw-np").textContent = `${toNepaliDigits(t.bsYear)} ${t.monthNameNP} ${toNepaliDigits(t.bsDay)}`;
  document.getElementById("tw-day").textContent = `${t.dayName} / ${t.dayNameNP}`;
}

/* ── Populate month dropdown ── */
function populateMonths() {
  const sel = document.getElementById("bs-month");
  BS_MONTHS_EN.forEach((n,i)=>{
    const o = document.createElement("option");
    o.value = i+1;
    o.textContent = String(i+1).padStart(2,"0")+" — "+n+" ("+BS_MONTHS_NP[i]+")";
    sel.appendChild(o);
  });
}

/* ── Tabs ── */
function initTabs() {
  document.querySelectorAll(".tab-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
      document.querySelectorAll(".tab-btn").forEach(b=>{b.classList.remove("active");b.setAttribute("aria-selected","false");});
      document.querySelectorAll(".tab-pane").forEach(p=>p.classList.remove("active"));
      btn.classList.add("active"); btn.setAttribute("aria-selected","true");
      document.getElementById(btn.dataset.tab).classList.add("active");
    });
  });
}

/* ── Prefill today ── */
function prefillToday() {
  const now = new Date();
  document.getElementById("ad-year").value  = now.getFullYear();
  document.getElementById("ad-month").value = now.getMonth()+1;
  document.getElementById("ad-day").value   = now.getDate();
  const t = getTodayBS();
  if (!t.error) {
    document.getElementById("bs-year").value  = t.bsYear;
    document.getElementById("bs-month").value = t.bsMonth;
    document.getElementById("bs-day").value   = t.bsDay;
    updateBSDayHint();
  }
}

/* ── Init ── */
document.addEventListener("DOMContentLoaded", ()=>{
  populateMonths();
  initTabs();
  renderToday();
  prefillToday();

  // BS inputs
  document.getElementById("bs-year").addEventListener("input", ()=>{ updateBSDayHint(); doConvertBSToAD(); });
  document.getElementById("bs-month").addEventListener("change", ()=>{ updateBSDayHint(); doConvertBSToAD(); });
  document.getElementById("bs-day").addEventListener("input", doConvertBSToAD);

  // AD inputs
  ["ad-year","ad-month","ad-day"].forEach(id=>{
    document.getElementById(id).addEventListener("input", doConvertADToBS);
  });

  // Buttons
  document.getElementById("btn-bs-copy").addEventListener("click",  ()=>copyResult(currentResult));
  document.getElementById("btn-bs-share").addEventListener("click", ()=>shareResult(currentResult));
  document.getElementById("btn-ad-copy").addEventListener("click",  ()=>copyResult(currentResult));
  document.getElementById("btn-ad-share").addEventListener("click", ()=>shareResult(currentResult));
  document.getElementById("btn-bs-clear").addEventListener("click", ()=>{
    ["bs-year","bs-day"].forEach(id=>document.getElementById(id).value="");
    document.getElementById("bs-month").value="";
    document.getElementById("bs-day-hint").textContent="";
    document.getElementById("bs-result").innerHTML="";
    document.getElementById("bs-actions").style.display="none";
    currentResult="";
  });
  document.getElementById("btn-ad-clear").addEventListener("click", ()=>{
    ["ad-year","ad-month","ad-day"].forEach(id=>document.getElementById(id).value="");
    document.getElementById("ad-result").innerHTML="";
    document.getElementById("ad-actions").style.display="none";
    currentResult="";
  });
  document.getElementById("btn-swap").addEventListener("click", ()=>{
    const active = document.querySelector(".tab-btn.active");
    document.querySelectorAll(".tab-btn").forEach(b=>{ if(b!==active) b.click(); });
  });

  // Run initial convert
  doConvertBSToAD();
  doConvertADToBS();
});
