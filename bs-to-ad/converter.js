/**
 * converter.js — Shared BS↔AD Conversion Engine
 * Used by: /bs-to-ad/, /ad-to-bs/, /date-converter/
 * Base: 2000-01-01 BS = 1943-04-14 AD (UTC)
 * Data: 2081 Chaitra=30, 2082 Chaitra=31 (verified)
 */
"use strict";

/* ── BS Calendar Data 2000–2090 ── */
const BS_DATA={
  2000:[30,32,31,32,31,30,30,30,29,30,29,31],
  2001:[31,31,32,31,31,31,30,29,30,29,30,30],
  2002:[31,31,32,32,31,30,30,29,30,29,30,30],
  2003:[31,32,31,32,31,30,30,30,29,29,30,31],
  2004:[30,32,31,32,31,30,30,30,29,30,29,31],
  2005:[31,31,32,31,31,31,30,29,30,29,30,30],
  2006:[31,31,32,32,31,30,30,29,30,29,30,30],
  2007:[31,32,31,32,31,30,30,30,29,29,30,31],
  2008:[31,31,31,32,31,31,29,30,30,29,29,31],
  2009:[31,31,32,31,31,31,30,29,30,29,30,30],
  2010:[31,31,32,32,31,30,30,29,30,29,30,30],
  2011:[31,32,31,32,31,30,30,30,29,29,30,31],
  2012:[31,31,31,32,31,31,29,30,30,29,30,30],
  2013:[31,31,32,31,31,31,30,29,30,29,30,30],
  2014:[31,31,32,32,31,30,30,29,30,29,30,30],
  2015:[31,32,31,32,31,30,30,30,29,29,30,31],
  2016:[31,31,31,32,31,31,29,30,30,29,30,30],
  2017:[31,31,32,31,31,31,30,29,30,29,30,30],
  2018:[31,31,32,32,31,30,30,29,30,29,30,30],
  2019:[31,32,31,32,31,30,30,30,29,29,30,31],
  2020:[31,31,31,32,31,31,29,30,30,29,30,30],
  2021:[31,31,32,31,31,31,30,29,30,29,30,30],
  2022:[31,31,32,32,31,30,30,29,30,29,30,30],
  2023:[31,32,31,32,31,30,30,30,29,29,30,31],
  2024:[31,31,31,32,31,31,29,30,30,29,30,30],
  2025:[31,31,32,31,31,31,30,29,30,29,30,30],
  2026:[31,31,32,32,31,30,30,29,30,29,30,30],
  2027:[31,32,31,32,31,30,30,30,29,29,30,31],
  2028:[31,31,31,32,31,31,29,30,30,29,30,30],
  2029:[31,31,32,31,31,31,30,29,30,29,30,30],
  2030:[31,31,32,32,31,30,30,29,30,29,30,30],
  2031:[31,32,31,32,31,30,30,30,29,29,30,31],
  2032:[31,31,31,32,31,31,29,30,30,29,30,30],
  2033:[31,31,32,31,31,31,30,29,30,29,30,30],
  2034:[31,31,32,32,31,30,30,29,30,29,30,30],
  2035:[31,32,31,32,31,30,30,30,29,29,30,31],
  2036:[31,31,31,32,31,31,29,30,29,30,30,30],
  2037:[31,31,32,31,31,31,30,29,30,29,30,30],
  2038:[31,31,32,32,31,30,30,29,30,29,30,30],
  2039:[31,32,31,32,31,30,30,30,29,29,30,31],
  2040:[31,31,31,32,31,31,29,30,30,29,30,30],
  2041:[31,31,32,31,31,31,30,29,30,29,30,30],
  2042:[31,31,32,32,31,30,30,29,30,29,30,30],
  2043:[31,32,31,32,31,30,30,30,29,29,30,31],
  2044:[31,31,31,32,31,31,29,30,30,29,30,30],
  2045:[31,31,32,31,31,31,30,29,30,29,30,30],
  2046:[31,31,32,32,31,30,30,29,30,29,30,30],
  2047:[31,32,31,32,31,30,30,30,29,29,30,31],
  2048:[31,31,31,32,31,31,29,30,30,29,30,30],
  2049:[31,31,32,31,31,31,30,29,30,29,30,30],
  2050:[31,31,32,32,31,30,30,29,30,29,30,30],
  2051:[31,32,31,32,31,30,30,30,29,29,30,31],
  2052:[31,31,31,32,31,31,29,30,30,29,30,30],
  2053:[31,31,32,31,31,31,30,29,30,29,30,30],
  2054:[31,31,32,32,31,30,30,29,30,29,30,30],
  2055:[31,32,31,32,31,30,30,30,29,29,30,31],
  2056:[31,31,31,32,31,31,29,30,30,29,30,30],
  2057:[31,31,32,31,31,31,30,29,30,29,30,30],
  2058:[31,31,32,32,31,30,30,29,30,29,30,30],
  2059:[31,32,31,32,31,30,30,30,29,29,30,31],
  2060:[31,31,31,32,31,31,29,30,30,29,30,30],
  2061:[31,31,32,31,31,31,30,29,30,29,30,30],
  2062:[31,31,32,32,31,30,30,29,30,29,30,30],
  2063:[31,32,31,32,31,30,30,30,29,29,30,31],
  2064:[31,31,31,32,31,31,29,30,30,29,30,30],
  2065:[31,31,32,31,31,31,30,29,30,29,30,30],
  2066:[31,31,32,32,31,30,30,29,30,29,30,30],
  2067:[31,32,31,32,31,30,30,30,29,29,30,31],
  2068:[31,31,31,32,31,31,29,30,30,29,30,30],
  2069:[31,31,32,31,31,31,30,29,30,29,30,30],
  2070:[31,31,32,32,31,30,30,29,30,29,30,30],
  2071:[31,32,31,32,31,30,30,30,29,29,30,31],
  2072:[31,31,31,32,31,31,29,30,30,29,30,30],
  2073:[31,31,32,31,31,31,30,29,30,29,30,30],
  2074:[31,31,32,32,31,30,30,29,30,29,30,30],
  2075:[31,32,31,32,31,30,30,30,29,29,30,31],
  2076:[31,31,31,32,31,31,29,30,30,29,30,30],
  2077:[31,31,32,31,31,31,30,29,30,29,30,30],
  2078:[31,31,32,32,31,30,30,29,30,29,30,30],
  2079:[31,32,31,32,31,30,30,30,29,29,30,31],
  2080:[31,31,31,32,31,31,30,29,30,29,30,30],
  2081:[31,31,32,31,31,31,30,29,30,29,30,30],
  2082:[31,31,32,32,31,30,30,29,30,29,30,31],
  2083:[31,32,31,32,31,30,30,30,29,29,30,31],
  2084:[31,31,31,32,31,31,29,30,30,29,30,30],
  2085:[31,31,32,31,31,31,30,29,30,29,30,30],
  2086:[31,31,32,32,31,30,30,29,30,29,30,30],
  2087:[31,32,31,32,31,30,30,30,29,29,30,31],
  2088:[31,31,31,32,31,31,29,30,30,29,30,30],
  2089:[31,31,32,31,31,31,30,29,30,29,30,30],
  2090:[31,31,32,32,31,30,30,29,30,29,30,30]
};

const MEN=["Baisakh","Jestha","Ashadh","Shrawan","Bhadra","Ashwin","Kartik","Mangsir","Poush","Magh","Falgun","Chaitra"];
const MNP=["बैशाख","जेठ","असार","श्रावण","भाद्र","आश्विन","कार्तिक","मंसिर","पुष","माघ","फागुन","चैत"];
const DEN=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
const DNP=["आइतबार","सोमबार","मंगलबार","बुधबार","बिहिबार","शुक्रबार","शनिबार"];
const ND=["०","१","२","३","४","५","६","७","८","९"];

/* ── Utilities ── */
const BASE=Date.UTC(1943,3,14);
function addDays(base,n){return new Date(base+n*86400000);}
function npNum(n){return String(n).split("").map(c=>ND[+c]??c).join("");}
function fmtAD(y,m,d){
  const mn=["January","February","March","April","May","June","July","August","September","October","November","December"];
  return mn[m-1]+" "+String(d).padStart(2,"0")+", "+y;
}
function nepaliNow(){
  // Returns current date in Nepal time (UTC+5:45) as {y,m,d}
  const np=new Date(Date.now()+((5*60+45)*60000));
  return{y:np.getUTCFullYear(),m:np.getUTCMonth()+1,d:np.getUTCDate()};
}
function bsOffset(y,m,d){
  let o=0;
  for(let i=2000;i<y;i++)BS_DATA[i].forEach(x=>o+=x);
  for(let i=0;i<m-1;i++)o+=BS_DATA[y][i];
  return o+d-1;
}

/* ── Validation ── */
function valBS(y,m,d){
  y=+y;m=+m;d=+d;
  if(!y||!m||!d||isNaN(y)||isNaN(m)||isNaN(d))return"Please fill year, month and day.";
  if(y<2000||y>2090)return"Year must be between 2000 and 2090 BS.";
  if(m<1||m>12)return"Month must be between 1 and 12.";
  const mx=BS_DATA[y][m-1];
  if(d<1||d>mx)return MEN[m-1]+" "+y+" has "+mx+" days. Day "+d+" is invalid.";
  return null;
}
function valAD(y,m,d){
  y=+y;m=+m;d=+d;
  if(!y||!m||!d||isNaN(y)||isNaN(m)||isNaN(d))return"Please fill year, month and day.";
  const dt=new Date(Date.UTC(y,m-1,d));
  if(dt.getUTCFullYear()!==y||dt.getUTCMonth()!==m-1||dt.getUTCDate()!==d)return"Invalid date (e.g. Feb 30 doesn't exist).";
  if(y<1943||y>2034)return"Supported range: 1943–2034 AD.";
  return null;
}

/* ── Core converters ── */
function convertBStoAD(y,m,d){
  const e=valBS(y,m,d);if(e)return{error:e};
  const ad=addDays(BASE,bsOffset(+y,+m,+d));
  const dw=ad.getUTCDay();
  return{ad,adY:ad.getUTCFullYear(),adM:ad.getUTCMonth()+1,adD:ad.getUTCDate(),dn:DEN[dw],dnp:DNP[dw]};
}
function convertADtoBS(y,m,d){
  const e=valAD(y,m,d);if(e)return{error:e};
  const ad=Date.UTC(+y,+m-1,+d);
  let rem=Math.floor((ad-BASE)/86400000);
  if(rem<0)return{error:"Date is before the supported range."};
  let by=2000;
  while(by<=2090){const yd=BS_DATA[by].reduce((a,b)=>a+b,0);if(rem<yd)break;rem-=yd;by++;}
  if(by>2090)return{error:"Date exceeds 2090 BS."};
  let bm=1;
  for(let i=0;i<12;i++){if(rem<BS_DATA[by][i]){bm=i+1;break;}rem-=BS_DATA[by][i];}
  const bd=rem+1,dw=new Date(ad).getUTCDay();
  return{by,bm,bd,mn:MEN[bm-1],mnp:MNP[bm-1],dn:DEN[dw],dnp:DNP[dw]};
}
function todayBS(){
  const n=nepaliNow();
  return convertADtoBS(n.y,n.m,n.d);
}

/* ── UI Helpers ── */
function showToast(msg){
  let t=document.getElementById("toast");
  if(!t){t=document.createElement("div");t.id="toast";document.body.appendChild(t);}
  t.textContent=msg;t.classList.add("show");
  clearTimeout(t._t);t._t=setTimeout(()=>t.classList.remove("show"),2400);
}
function copyText(s){
  if(!s)return;
  navigator.clipboard.writeText(s).then(()=>showToast("✓ Copied!"))
    .catch(()=>{const el=document.createElement("textarea");el.value=s;
      el.style.cssText="position:fixed;opacity:0";document.body.appendChild(el);
      el.select();document.execCommand("copy");document.body.removeChild(el);
      showToast("✓ Copied!");});
}
function shareResult(s){
  if(navigator.share)navigator.share({title:document.title,text:s,url:location.href}).catch(()=>{});
  else{copyText(s);showToast("✓ Copied — share it!");}
}
