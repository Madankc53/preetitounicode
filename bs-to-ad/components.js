/**
 * components.js — Shared Header & Footer
 * Usage: place <div id="header"></div> and <div id="footer"></div>
 * then <script src="/components.js"></script>
 *
 * Each page passes config via window.PAGE_CONFIG before loading this script:
 * window.PAGE_CONFIG = {
 *   title:      "BS to AD Converter",
 *   subtitle:   "Bikram Sambat to Gregorian",
 *   icon:       "🗓",
 *   breadcrumb: "BS to AD Converter",
 *   canonical:  "https://converter.thenepal.io/bs-to-ad/",
 *   footerText: "BS to AD Converter"
 * };
 */
(function(){
  "use strict";

  const cfg = window.PAGE_CONFIG || {};
  const title      = cfg.title      || "Nepali Date Converter";
  const subtitle   = cfg.subtitle   || "BS ↔ AD · Bikram Sambat · Instant & Accurate";
  const icon       = cfg.icon       || "🗓";
  const breadcrumb = cfg.breadcrumb || "Nepali Date Converter";
  const footerText = cfg.footerText || "Nepali Date Converter · BS ↔ AD";
  const year       = new Date().getFullYear();

  /* ── Header ── */
  const hdrEl = document.getElementById("header");
  if(hdrEl){
    hdrEl.innerHTML = `
<header class="hdr" role="banner">
  <div class="wrap">
    <nav class="bc" aria-label="Breadcrumb">
      <a href="https://thenepal.io">Home</a> ›
      <a href="https://converter.thenepal.io">Tools</a> ›
      <span>${breadcrumb}</span>
    </nav>
    <div class="hdr-inner">
      <div class="hdr-ico" aria-hidden="true">${icon}</div>
      <div>
        <h1>${title}</h1>
        <p class="sub">${subtitle}</p>
      </div>
      <span class="hdr-badge">✓ Verified Accuracy</span>
    </div>
  </div>
</header>`;
  }

  /* ── Footer ── */
  const ftrEl = document.getElementById("footer");
  if(ftrEl){
    ftrEl.innerHTML = `
<section class="sec wrap" style="margin-bottom:12px" aria-label="About">
  <p style="font-size:.84rem;color:#444;">
    <strong>About this tool:</strong> Built and maintained by
    <a href="https://madankc.com.np" rel="author">Madan KC</a>,
    a Nepal-based web developer. Conversion data is cross-verified against
    trusted official Nepali calendar sources. Last updated: 2083 BS / 2026 AD.
  </p>
</section>
<footer role="contentinfo">
  <div class="wrap">
    <div class="ftl">
      <a href="https://thenepal.io">TheNepal.io</a>
      <a href="https://madankc.com.np">MadanKC.com.np</a>
      <a href="https://thenepal.io/privacy">Privacy</a>
      <a href="https://thenepal.io/contact">Contact</a>
    </div>
    <p>${footerText} · 2000–2090 BS · Accurate &amp; Verified<br>
    © ${year} TheNepal.io · Built for Nepal 🇳🇵</p>
  </div>
</footer>`;
  }

  /* ── FAQ accordion (shared) ── */
  document.addEventListener("DOMContentLoaded", function(){
    document.querySelectorAll(".faq-q").forEach(function(q){
      function tog(){
        var it=q.parentElement;
        var o=it.classList.toggle("open");
        q.setAttribute("aria-expanded",o);
      }
      q.addEventListener("click",tog);
      q.addEventListener("keydown",function(e){
        if(e.key==="Enter"||e.key===" "){e.preventDefault();tog();}
      });
    });
    // Set footer year (in case fy span exists from old pages)
    var fy=document.getElementById("fy");
    if(fy) fy.textContent=year;
  });

})();
