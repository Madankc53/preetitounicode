/**
 * Nepali Date Converter — script.js
 * BS ↔ AD conversion using exact day-offset method.
 * Base reference: 2000-01-01 BS = 1943-04-14 AD
 * Accuracy matches Hamro Patro.
 *
 * Functions:
 *   validateBSDate(y,m,d)
 *   convertBSToAD(bsY,bsM,bsD)
 *   convertADToBS(adY,adM,adD)
 *   getNepaliMonth(monthIndex, lang)
 *   getDayName(jsDate, lang)
 *   copyResult(elementId)
 *   shareResult(text)
 *   getTodayBS()
 */

"use strict";

/* ─── Constants ─────────────────────────────────────────── */
const BS_START_YEAR = 2000;
const BS_END_YEAR   = 2090;

// Base anchor: 2000-01-01 BS = 1943-04-14 AD
const AD_BASE = new Date(1943, 3, 14); // JS month 3 = April

/* ─── Helpers ───────────────────────────────────────────── */

/**
 * Count total days from BS 2000-01-01 to a given BS date (exclusive).
 * @param {number} bsY  BS year
 * @param {number} bsM  BS month (1-based)
 * @param {number} bsD  BS day
 * @returns {number} total day offset
 */
function bsDayOffset(bsY, bsM, bsD) {
  let offset = 0;
  // Sum all days in years before bsY
  for (let y = BS_START_YEAR; y < bsY; y++) {
    const months = BS_DATA[y];
    for (let m = 0; m < 12; m++) offset += months[m];
  }
  // Sum completed months in bsY
  const yearData = BS_DATA[bsY];
  for (let m = 0; m < bsM - 1; m++) offset += yearData[m];
  // Add days (0-based offset: day 1 = +0)
  offset += bsD - 1;
  return offset;
}

/**
 * Add days to a JS Date without mutating the original.
 */
function addDays(date, days) {
  const d = new Date(date.getTime());
  d.setDate(d.getDate() + days);
  return d;
}

/* ─── Validation ────────────────────────────────────────── */

/**
 * Validate a BS date.
 * @returns {string|null} error message or null if valid
 */
function validateBSDate(bsY, bsM, bsD) {
  bsY = parseInt(bsY, 10);
  bsM = parseInt(bsM, 10);
  bsD = parseInt(bsD, 10);

  if (isNaN(bsY) || isNaN(bsM) || isNaN(bsD))
    return "Please enter a complete BS date.";
  if (bsY < BS_START_YEAR || bsY > BS_END_YEAR)
    return `BS year must be between ${BS_START_YEAR} and ${BS_END_YEAR}.`;
  if (bsM < 1 || bsM > 12)
    return "BS month must be between 1 and 12.";

  const maxDay = BS_DATA[bsY][bsM - 1];
  if (bsD < 1 || bsD > maxDay)
    return `BS ${BS_MONTHS_EN[bsM-1]} ${bsY} has only ${maxDay} days. Day ${bsD} is invalid.`;

  return null;
}

/**
 * Validate an AD date.
 * @returns {string|null} error message or null if valid
 */
function validateADDate(adY, adM, adD) {
  adY = parseInt(adY, 10);
  adM = parseInt(adM, 10);
  adD = parseInt(adD, 10);

  if (isNaN(adY) || isNaN(adM) || isNaN(adD))
    return "Please enter a complete AD date.";

  const d = new Date(adY, adM - 1, adD);
  if (d.getFullYear() !== adY || d.getMonth() !== adM - 1 || d.getDate() !== adD)
    return "Invalid AD date (e.g. February 30 does not exist).";

  // Rough range check: 2000 BS ≈ 1943 AD, 2090 BS ≈ 2034 AD
  if (adY < 1943 || adY > 2034)
    return "AD year is outside the supported conversion range (approx. 1943–2034).";

  return null;
}

/* ─── Core Converters ───────────────────────────────────── */

/**
 * Convert BS date → AD date.
 * @param {number} bsY  BS year
 * @param {number} bsM  BS month (1-based)
 * @param {number} bsD  BS day
 * @returns {{ adDate: Date, dayName: string, dayNameNP: string } | { error: string }}
 */
function convertBSToAD(bsY, bsM, bsD) {
  bsY = parseInt(bsY, 10);
  bsM = parseInt(bsM, 10);
  bsD = parseInt(bsD, 10);

  const err = validateBSDate(bsY, bsM, bsD);
  if (err) return { error: err };

  const offset  = bsDayOffset(bsY, bsM, bsD);
  const adDate  = addDays(AD_BASE, offset);
  const dow     = adDate.getDay();

  return {
    adDate,
    dayName:   DAYS_EN[dow],
    dayNameNP: DAYS_NP[dow],
    adYear:    adDate.getFullYear(),
    adMonth:   adDate.getMonth() + 1,
    adDay:     adDate.getDate()
  };
}

/**
 * Convert AD date → BS date.
 * @param {number} adY  AD year
 * @param {number} adM  AD month (1-based)
 * @param {number} adD  AD day
 * @returns {{ bsYear, bsMonth, bsDay, monthName, monthNameNP, dayName, dayNameNP } | { error: string }}
 */
function convertADToBS(adY, adM, adD) {
  adY = parseInt(adY, 10);
  adM = parseInt(adM, 10);
  adD = parseInt(adD, 10);

  const err = validateADDate(adY, adM, adD);
  if (err) return { error: err };

  const adDate  = new Date(adY, adM - 1, adD);
  // Day difference from anchor
  const diffMs  = adDate.getTime() - AD_BASE.getTime();
  let   remaining = Math.round(diffMs / 86400000); // exact integer

  if (remaining < 0)
    return { error: "AD date is before the supported range (1943-04-14)." };

  // Walk through BS years/months to find the BS date
  let bsY = BS_START_YEAR;
  let bsM = 1;
  let bsD = 1;

  // Consume full years
  while (bsY <= BS_END_YEAR) {
    const yearDays = BS_DATA[bsY].reduce((a, b) => a + b, 0);
    if (remaining < yearDays) break;
    remaining -= yearDays;
    bsY++;
  }

  if (bsY > BS_END_YEAR)
    return { error: "AD date exceeds the supported BS range (up to 2090 BS)." };

  // Consume full months
  const yearData = BS_DATA[bsY];
  for (let m = 0; m < 12; m++) {
    if (remaining < yearData[m]) {
      bsM = m + 1;
      break;
    }
    remaining -= yearData[m];
  }

  bsD = remaining + 1;
  const dow = adDate.getDay();

  return {
    bsYear:      bsY,
    bsMonth:     bsM,
    bsDay:       bsD,
    monthName:   getNepaliMonth(bsM, "en"),
    monthNameNP: getNepaliMonth(bsM, "np"),
    dayName:     DAYS_EN[dow],
    dayNameNP:   DAYS_NP[dow]
  };
}

/* ─── Utility Functions ─────────────────────────────────── */

/**
 * Get Nepali month name.
 * @param {number} monthIndex 1-based
 * @param {string} lang "en" | "np"
 */
function getNepaliMonth(monthIndex, lang = "en") {
  if (monthIndex < 1 || monthIndex > 12) return "";
  return lang === "np"
    ? BS_MONTHS_NP[monthIndex - 1]
    : BS_MONTHS_EN[monthIndex - 1];
}

/**
 * Get day name from a JS Date.
 * @param {Date} jsDate
 * @param {string} lang "en" | "np"
 */
function getDayName(jsDate, lang = "en") {
  return lang === "np" ? DAYS_NP[jsDate.getDay()] : DAYS_EN[jsDate.getDay()];
}

/**
 * Get today's BS date.
 */
function getTodayBS() {
  const now = new Date();
  return convertADToBS(now.getFullYear(), now.getMonth() + 1, now.getDate());
}

/**
 * Format AD date as "Month DD, YYYY"
 */
function formatAD(y, m, d) {
  const months = ["January","February","March","April","May","June",
                  "July","August","September","October","November","December"];
  return `${months[m-1]} ${String(d).padStart(2,"0")}, ${y}`;
}

/**
 * Copy text to clipboard, show toast feedback.
 */
function copyResult(text) {
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    showToast("✓ Copied to clipboard!");
  }).catch(() => {
    // Fallback for older browsers
    const el = document.createElement("textarea");
    el.value = text;
    el.style.position = "fixed";
    el.style.opacity  = "0";
    document.body.appendChild(el);
    el.select();
    document.execCommand("copy");
    document.body.removeChild(el);
    showToast("✓ Copied to clipboard!");
  });
}

/**
 * Share result via Web Share API or fallback copy.
 */
function shareResult(text) {
  if (navigator.share) {
    navigator.share({ title: "Nepali Date Converter", text, url: window.location.href })
      .catch(() => {});
  } else {
    copyResult(text);
    showToast("✓ Link copied — share it anywhere!");
  }
}

/**
 * Show a toast notification.
 */
function showToast(message) {
  let toast = document.getElementById("toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove("show"), 2500);
}

/* ─── UI Logic ──────────────────────────────────────────── */

// Track current result text for copy/share
let currentResultText = "";

/**
 * Convert BS → AD and render result.
 */
function doConvertBSToAD() {
  const y = document.getElementById("bs-year").value;
  const m = document.getElementById("bs-month").value;
  const d = document.getElementById("bs-day").value;

  if (!y || !m || !d) { clearResult("bs"); return; }

  const result = convertBSToAD(y, m, d);
  const resEl  = document.getElementById("bs-result");
  const actEl  = document.getElementById("bs-actions");

  if (result.error) {
    resEl.innerHTML = `<p class="error-msg">⚠ ${result.error}</p>`;
    actEl.style.display = "none";
    currentResultText = "";
    return;
  }

  const adFormatted = formatAD(result.adYear, result.adMonth, result.adDay);
  const bsStr = `${y} ${getNepaliMonth(+m, "en")} ${d}`;
  currentResultText = `${bsStr} BS = ${adFormatted} AD (${result.dayName})`;

  resEl.innerHTML = `
    <div class="result-card">
      <div class="result-main">
        <span class="result-label">AD Date</span>
        <span class="result-value">${adFormatted}</span>
      </div>
      <div class="result-meta">
        <span class="tag">${result.dayName}</span>
        <span class="tag">${result.dayNameNP}</span>
      </div>
    </div>`;
  actEl.style.display = "flex";
}

/**
 * Convert AD → BS and render result.
 */
function doConvertADToBS() {
  const y = document.getElementById("ad-year").value;
  const m = document.getElementById("ad-month").value;
  const d = document.getElementById("ad-day").value;

  if (!y || !m || !d) { clearResult("ad"); return; }

  const result = convertADToBS(y, m, d);
  const resEl  = document.getElementById("ad-result");
  const actEl  = document.getElementById("ad-actions");

  if (result.error) {
    resEl.innerHTML = `<p class="error-msg">⚠ ${result.error}</p>`;
    actEl.style.display = "none";
    currentResultText = "";
    return;
  }

  const bsFormatted  = `${result.bsYear} ${result.monthName} ${result.bsDay}`;
  const bsNP         = `${toNepaliDigits(result.bsYear)} ${result.monthNameNP} ${toNepaliDigits(result.bsDay)}`;
  const adStr = formatAD(+y, +m, +d);
  currentResultText = `${adStr} AD = ${bsFormatted} BS (${result.dayName})`;

  resEl.innerHTML = `
    <div class="result-card">
      <div class="result-main">
        <span class="result-label">BS Date</span>
        <span class="result-value">${bsFormatted}</span>
      </div>
      <div class="result-np">${bsNP}</div>
      <div class="result-meta">
        <span class="tag">${result.dayName}</span>
        <span class="tag">${result.dayNameNP}</span>
        <span class="tag">${result.monthName} / ${result.monthNameNP}</span>
      </div>
    </div>`;
  actEl.style.display = "flex";
}

function clearResult(mode) {
  const resEl = document.getElementById(`${mode}-result`);
  const actEl = document.getElementById(`${mode}-actions`);
  if (resEl) resEl.innerHTML = "";
  if (actEl) actEl.style.display = "none";
  currentResultText = "";
}

/**
 * Swap: fill AD converter inputs from a BS→AD result (if available) or vice versa.
 */
function swapMode() {
  // Toggle tab
  const bsTab = document.getElementById("tab-bs");
  const adTab = document.getElementById("tab-ad");
  if (bsTab.classList.contains("active")) {
    adTab.click();
  } else {
    bsTab.click();
  }
}

/**
 * Populate month <select> with BS month options.
 */
function populateBSMonths() {
  const sel = document.getElementById("bs-month");
  BS_MONTHS_EN.forEach((name, i) => {
    const opt = document.createElement("option");
    opt.value = i + 1;
    opt.textContent = `${String(i+1).padStart(2,"0")} — ${name} (${BS_MONTHS_NP[i]})`;
    sel.appendChild(opt);
  });
}

/**
 * Populate BS year <select>.
 */
function populateBSYears() {
  const sel = document.getElementById("bs-year");
  for (let y = BS_END_YEAR; y >= BS_START_YEAR; y--) {
    const opt = document.createElement("option");
    opt.value = y;
    opt.textContent = y;
    sel.appendChild(opt);
  }
}

/**
 * Populate BS day <select> based on chosen year+month.
 */
function updateBSDays() {
  const y   = parseInt(document.getElementById("bs-year").value, 10);
  const m   = parseInt(document.getElementById("bs-month").value, 10);
  const sel = document.getElementById("bs-day");
  const cur = parseInt(sel.value, 10);
  sel.innerHTML = '<option value="">Day</option>';
  if (!y || !m || !BS_DATA[y]) return;
  const max = BS_DATA[y][m - 1];
  for (let d = 1; d <= max; d++) {
    const opt = document.createElement("option");
    opt.value = d;
    opt.textContent = String(d).padStart(2, "0");
    sel.appendChild(opt);
  }
  if (cur >= 1 && cur <= max) sel.value = cur;
}

/**
 * Render Today's BS date in the hero widget.
 */
function renderTodayBS() {
  const today = getTodayBS();
  if (today.error) return;

  const adNow = new Date();
  const adStr = formatAD(adNow.getFullYear(), adNow.getMonth()+1, adNow.getDate());

  document.getElementById("today-ad").textContent   = adStr;
  document.getElementById("today-bs").textContent   =
    `${today.bsYear} ${today.monthName} ${today.bsDay}`;
  document.getElementById("today-bs-np").textContent =
    `${toNepaliDigits(today.bsYear)} ${today.monthNameNP} ${toNepaliDigits(today.bsDay)}`;
  document.getElementById("today-day").textContent  =
    `${today.dayName} / ${today.dayNameNP}`;
}

/* ─── Tab Switching ─────────────────────────────────────── */
function initTabs() {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.tab).classList.add("active");
    });
  });
}

/* ─── Auto-detect today and prefill ────────────────────── */
function prefillToday() {
  const now  = new Date();
  const adY  = now.getFullYear();
  const adM  = now.getMonth() + 1;
  const adD  = now.getDate();

  // Prefill AD→BS form
  document.getElementById("ad-year").value  = adY;
  document.getElementById("ad-month").value = String(adM).padStart(2, "0");
  document.getElementById("ad-day").value   = String(adD).padStart(2, "0");

  // Prefill BS→AD form with today's BS
  const todayBS = getTodayBS();
  if (!todayBS.error) {
    document.getElementById("bs-year").value  = todayBS.bsYear;
    document.getElementById("bs-month").value = todayBS.bsMonth;
    updateBSDays();
    document.getElementById("bs-day").value   = todayBS.bsDay;
  }
}

/* ─── Init ──────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  populateBSYears();
  populateBSMonths();
  initTabs();
  renderTodayBS();
  prefillToday();

  // Auto-convert on change
  ["bs-year","bs-month","bs-day"].forEach(id => {
    document.getElementById(id).addEventListener("change", () => {
      if (id !== "bs-day") updateBSDays();
      doConvertBSToAD();
    });
  });

  ["ad-year","ad-month","ad-day"].forEach(id => {
    document.getElementById(id).addEventListener("input", doConvertADToBS);
    document.getElementById(id).addEventListener("change", doConvertADToBS);
  });

  // Buttons
  document.getElementById("btn-bs-copy")?.addEventListener("click",
    () => copyResult(currentResultText));
  document.getElementById("btn-bs-share")?.addEventListener("click",
    () => shareResult(currentResultText));
  document.getElementById("btn-ad-copy")?.addEventListener("click",
    () => copyResult(currentResultText));
  document.getElementById("btn-ad-share")?.addEventListener("click",
    () => shareResult(currentResultText));
  document.getElementById("btn-bs-clear")?.addEventListener("click",
    () => { ["bs-year","bs-month","bs-day"].forEach(id => document.getElementById(id).value=""); clearResult("bs"); });
  document.getElementById("btn-ad-clear")?.addEventListener("click",
    () => { ["ad-year","ad-month","ad-day"].forEach(id => document.getElementById(id).value=""); clearResult("ad"); });
  document.getElementById("btn-swap")?.addEventListener("click", swapMode);

  // Run initial conversions with prefilled values
  doConvertBSToAD();
  doConvertADToBS();
});
