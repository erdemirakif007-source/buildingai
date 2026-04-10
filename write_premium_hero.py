# -*- coding: utf-8 -*-
# Terminal Industries-Grade Hero Rewrite
# Techniques: SVG Spotlight, Text Scramble, ScrollTrigger PIN + scrub

landing = r"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BuildingAI — Şantiyenin Yapay Zekası</title>
<meta name="description" content="50+ mühendislik hesabı, TBDY 2018 uyumlu AI asistan. Türkiye'nin şantiye platformu.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:ital,wght@0,400;0,500;0,600&display=swap" rel="stylesheet">

<!-- GSAP Suite (head = no FOUC) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/TextPlugin.min.js"></script>

<style>
/* ================================================================
   DESIGN SYSTEM — BuildingAI
   ================================================================ */
:root {
  --bg:        #030712;
  --navy:      #060d1a;
  --amber:     #f97316;
  --amber2:    #fb923c;
  --cyan:      #22d3ee;
  --text1:     #f0f4ff;
  --text2:     #94a3b8;
  --text3:     #3d5070;
  --border:    rgba(255,255,255,0.07);
  --border2:   rgba(255,255,255,0.14);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  font-family:'Instrument Sans',sans-serif;
  background:var(--bg); color:var(--text1);
  overflow-x:hidden;
}

/* ── NAV ── */
nav{
  position:fixed;top:0;left:0;right:0;z-index:500;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 5%;height:64px;
  background:rgba(3,7,18,0.82);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);
}
.nav-logo{
  display:flex;align-items:center;gap:10px;
  font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:.08em;
}
.nav-logo span{color:var(--amber)}
.nav-right{display:flex;align-items:center;gap:12px}
.lang-btn{
  background:none;border:1px solid var(--border2);
  color:var(--text2);font-size:12px;font-family:'DM Mono',monospace;
  padding:5px 12px;border-radius:6px;cursor:pointer;transition:all .15s;
}
.lang-btn:hover,.lang-btn.active{border-color:var(--amber);color:var(--amber)}
.nav-cta{
  background:var(--amber);color:#000;font-weight:600;font-size:13px;
  padding:8px 20px;border-radius:8px;text-decoration:none;transition:all .15s;
}
.nav-cta:hover{background:var(--amber2);transform:translateY(-1px)}
.btn-ghost-nav{
  padding:8px 18px;font-size:13px;border-radius:8px;text-decoration:none;
  border:1px solid rgba(255,255,255,0.2);color:white;transition:all .15s;
}

/* ================================================================
   HERO — PINNED CINEMATIC SCENE
   ================================================================ */
.hero-pin-wrap{
  /* ScrollTrigger will pin this */
  position:relative;
  height:100vh; min-height:700px;
}

.hero-scene{
  position:relative;
  width:100%;height:100%;
  background:var(--bg);
  overflow:hidden;
  display:flex;align-items:center;justify-content:center;
}

/* ── SVG Spotlight — mouse-tracking radial glow ── */
#spotlight{
  position:absolute;inset:0;z-index:1;pointer-events:none;
  width:100%;height:100%;
}

/* ── Particle Canvas ── */
#particleCanvas{
  position:absolute;inset:0;z-index:2;
  pointer-events:none;width:100%;height:100%;
}

/* ── Grid overlay ── */
.hero-grid{
  position:absolute;inset:0;z-index:3;pointer-events:none;
  background-image:
    linear-gradient(rgba(34,211,238,0.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(34,211,238,0.025) 1px,transparent 1px);
  background-size:64px 64px;
}

/* ── SVG wireframe cranes (far background) ── */
.crane-layer{
  position:absolute;inset:0;z-index:4;
  pointer-events:none;overflow:hidden;
}
.crane-svg{
  position:absolute;fill:none;
  stroke:rgba(255,255,255,0.05);stroke-width:1.2;
}
.crane-1{bottom:0;left:5%;width:260px;height:80vh}
.crane-2{bottom:0;right:8%;width:310px;height:88vh;opacity:.7}
.crane-3{bottom:0;left:43%;width:150px;height:52vh;opacity:.35}

/* ── Ambient amber glow ── */
.hero-glow{
  position:absolute;bottom:-300px;left:50%;transform:translateX(-50%);
  width:160vw;height:700px;z-index:5;pointer-events:none;
  background:radial-gradient(ellipse at center,
    rgba(249,115,22,0.09) 0%,
    rgba(249,115,22,0.03) 35%,
    transparent 70%);
}

/* ── Animated crane arm (mid-ground) ── */
.crane-arm-layer{position:absolute;inset:0;z-index:6;pointer-events:none}
.crane-arm-pivot{
  position:absolute;top:11%;left:10%;
  width:60vw;height:5px;
  transform-origin:0% 50%;
  /* starts off-screen — GSAP sets initial */
}
.arm-beam{
  width:100%;height:100%;
  background:linear-gradient(90deg,
    rgba(249,115,22,0.6) 0%,
    rgba(249,115,22,0.1) 60%,transparent 100%);
  border-radius:3px;
  box-shadow:0 0 20px rgba(249,115,22,0.14);
}
.arm-cable{
  position:absolute;right:26%;top:5px;
  width:1px;height:30vh;
  background:linear-gradient(to bottom,rgba(255,255,255,0.2),transparent);
}
.arm-hook{
  position:absolute;right:calc(26% - 9px);top:calc(5px + 30vh);
  width:18px;height:18px;
  border:2px solid rgba(249,115,22,0.5);
  border-top:none;border-radius:0 0 9px 9px;
}

/* ── Hero foreground content ── */
.hero-content{
  position:relative;z-index:10;
  text-align:center;
  max-width:1100px;width:92%;padding:0 24px;
}

/* System label */
.hero-sys-label{
  display:inline-flex;align-items:center;gap:10px;
  font-family:'DM Mono',monospace;font-size:11px;
  letter-spacing:0.2em;text-transform:uppercase;color:var(--amber);
  margin-bottom:28px;
}
.sys-dot{
  width:7px;height:7px;background:var(--amber);border-radius:50%;
  box-shadow:0 0 10px var(--amber);
  animation:pulse 2s ease-in-out infinite;
}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(.6)}}

/* Main heading */
.hero-h1{
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(60px,11vw,155px);
  line-height:.88;letter-spacing:.03em;
  color:#fff;margin-bottom:32px;
  /* Scramble effect target wrapper */
}
.hero-h1 .word-ai{color:var(--cyan)}

/* Subtitle */
.hero-sub{
  font-size:clamp(15px,1.8vw,19px);color:var(--text2);
  max-width:580px;margin:0 auto 52px;line-height:1.65;
}

/* Buttons */
.hero-btns{
  display:flex;gap:18px;justify-content:center;flex-wrap:wrap;
  margin-bottom:60px;
}
.btn-fire{
  background:var(--amber);color:#000!important;
  font-weight:700;font-size:16px;padding:16px 48px;
  border-radius:8px;text-decoration:none;border:none;cursor:pointer;
  box-shadow:0 0 30px rgba(249,115,22,.45),0 8px 22px rgba(0,0,0,.35);
  transition:all .35s cubic-bezier(.16,1,.3,1);
  font-family:'Instrument Sans',sans-serif;
}
.btn-fire:hover{transform:translateY(-3px) scale(1.04);box-shadow:0 0 52px rgba(249,115,22,.65)}
.btn-ghost{
  background:rgba(255,255,255,.04);color:#fff!important;
  font-weight:500;font-size:16px;padding:16px 48px;
  border-radius:8px;border:1px solid rgba(255,255,255,.13);
  text-decoration:none;transition:all .3s;cursor:pointer;
}
.btn-ghost:hover{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.38);transform:translateY(-3px)}

/* ── Engineering Data Card — Premium Glassmorphism ── */
.eng-card{
  /* Layered glass: expensive feel */
  background:rgba(255,255,255,0.04);
  backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px);
  border-radius:20px;
  border-top: 1px solid rgba(255,255,255,0.14);
  border-left: 1px solid rgba(255,255,255,0.14);
  border-right:1px solid rgba(255,255,255,0.04);
  border-bottom:1px solid rgba(255,255,255,0.04);
  box-shadow:
    0 32px 64px rgba(0,0,0,.5),
    inset 0 1px 0 rgba(255,255,255,.12),
    inset 0 0 0 1px rgba(255,255,255,.04),
    0 0 0 1px rgba(249,115,22,.05);
  display:flex;flex-wrap:wrap;
  max-width:840px;margin:0 auto;
  overflow:hidden;
}
.eng-cell{
  flex:1;min-width:160px;
  padding:28px 20px;text-align:center;
  border-right:1px solid rgba(255,255,255,.06);
  position:relative;
}
.eng-cell:last-child{border-right:none}
.eng-cell::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(249,115,22,.15),transparent);
}
.eng-val{
  font-family:'DM Mono',monospace;font-weight:500;
  font-size:clamp(22px,3vw,40px);color:#fff;
  letter-spacing:-0.03em;line-height:1.1;
}
.eng-lbl{
  font-size:10px;color:#4a6080;font-family:'DM Mono',monospace;
  text-transform:uppercase;letter-spacing:0.1em;
  margin-top:8px;font-weight:600;
}

/* ── Seamless bottom gradient ── */
.hero-fade{
  position:absolute;bottom:0;left:0;width:100%;height:240px;
  background:linear-gradient(to top,var(--navy) 0%,transparent 100%);
  z-index:20;pointer-events:none;
}

/* ================================================================
   TOAST
   ================================================================ */
.toast-container{position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:12px;pointer-events:none}
.toast{
  background:rgba(8,15,30,.93);backdrop-filter:blur(16px);
  border:1px solid rgba(244,63,94,.4);border-radius:12px;
  padding:16px 20px;min-width:300px;max-width:400px;
  box-shadow:0 10px 30px rgba(244,63,94,.2);
  display:flex;align-items:flex-start;gap:14px;
  transform:translateX(120%);opacity:0;pointer-events:auto;
  transition:all .5s cubic-bezier(.16,1,.3,1);
}
.toast.show{transform:translateX(0);opacity:1}
.toast-icon{font-size:22px;line-height:1}
.toast-title{font-weight:600;color:#fff;font-size:14px;margin-bottom:3px}
.toast-desc{font-size:12px;color:#cbd5e1;line-height:1.4}

/* ================================================================
   SECTIONS
   ================================================================ */
section{position:relative;z-index:1}
.section-inner{max-width:1100px;margin:0 auto;padding:100px 5%}
.section-label{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.16em;color:var(--cyan);text-transform:uppercase;margin-bottom:16px}
.section-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(36px,5vw,60px);letter-spacing:.04em;line-height:1;margin-bottom:16px}
.section-sub{font-size:16px;color:var(--text2);line-height:1.7;max-width:520px}

.features-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:56px}
.feature-card{
  background:rgba(15,32,64,.5);border:1px solid var(--border);
  border-radius:16px;padding:28px;transition:all .2s;cursor:default;
  position:relative;overflow:hidden;
}
.feature-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--c,transparent);opacity:0;transition:opacity .2s}
.feature-card:hover{border-color:var(--border2);transform:translateY(-4px)}
.feature-card:hover::before{opacity:1}
.feature-icon{font-size:32px;margin-bottom:16px}
.feature-title{font-size:18px;font-weight:600;margin-bottom:8px}
.feature-desc{font-size:14px;color:var(--text2);line-height:1.6}
.feature-tag{display:inline-block;margin-top:14px;font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.08em;padding:3px 10px;border-radius:4px;background:var(--bg,rgba(255,255,255,.06));color:var(--tc,var(--text3));border:1px solid var(--bc,var(--border))}

.how-section{background:rgba(10,22,40,.6)}
.steps{display:flex;flex-direction:column;gap:0;margin-top:56px;position:relative}
.steps::before{content:'';position:absolute;left:23px;top:0;bottom:0;width:2px;background:linear-gradient(to bottom,var(--amber),var(--cyan),transparent);opacity:.3}
.step{display:flex;gap:28px;padding:32px 0}
.step-num{width:48px;height:48px;border-radius:50%;flex-shrink:0;background:var(--navy);border:2px solid var(--amber);display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:20px;color:var(--amber);position:relative;z-index:1}
.step-content{padding-top:8px}
.step-title{font-size:18px;font-weight:600;margin-bottom:8px}
.step-desc{font-size:14px;color:var(--text2);line-height:1.6;max-width:480px}

.mevzuat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:48px}
.mevzuat-card{background:rgba(34,211,238,.06);border:1px solid rgba(34,211,238,.14);border-radius:12px;padding:20px 22px;display:flex;align-items:center;gap:14px}
.mevzuat-icon{font-size:24px;flex-shrink:0}
.mevzuat-text{font-size:14px;font-weight:500}
.mevzuat-sub{font-size:12px;color:var(--text2);margin-top:3px}

.cta-section{text-align:center;background:linear-gradient(135deg,rgba(249,115,22,.08) 0%,rgba(34,211,238,.05) 100%);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.cta-section .section-title{font-size:clamp(40px,6vw,72px)}

footer{padding:40px 5%;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;position:relative;z-index:1}
.footer-logo{font-family:'Bebas Neue',sans-serif;font-size:18px;letter-spacing:.08em}
.footer-logo span{color:var(--amber)}
.footer-copy{font-size:12px;color:var(--text3);font-family:'DM Mono',monospace}

/* Scroll reveal */
.reveal{opacity:0;transform:translateY(24px);transition:all .6s ease}
.reveal.visible{opacity:1;transform:none}

/* Responsive */
@media(max-width:768px){
  .crane-arm-pivot{display:none}
  .crane-1,.crane-2{opacity:.08}
  .eng-card{flex-wrap:wrap}
  .eng-cell{min-width:50%;border-bottom:1px solid rgba(255,255,255,.06)}
  .eng-cell:nth-child(2){border-right:none}
  .hero-btns{gap:12px}
  .step{flex-direction:column;gap:12px}
  .steps::before{display:none}
  footer{flex-direction:column;text-align:center}
  .nav-right .btn-ghost-nav{display:none}
}
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="nav-logo">🏗️ Building<span>AI</span></div>
  <div class="nav-right">
    <button class="lang-btn active" onclick="setLang('tr')" id="btn-tr">TR</button>
    <button class="lang-btn" onclick="setLang('en')" id="btn-en">EN</button>
    <a href="/app" class="btn-ghost-nav" data-tr="Giriş Yap" data-en="Sign In">Giriş Yap</a>
    <a href="/app#register" class="nav-cta" data-tr="Ücretsiz Dene" data-en="Try Free">Ücretsiz Dene</a>
  </div>
</nav>

<!-- ============================================================
     HERO — PINNED CINEMATIC PARALLAX SCENE
     ============================================================ -->
<div class="hero-pin-wrap" id="heroPinWrap">
<div class="hero-scene" id="heroScene">

  <!-- SVG Spotlight (mouse-following) -->
  <svg id="spotlight" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="spotGrad" cx="50%" cy="50%" r="50%">
        <stop offset="0%"   stop-color="rgba(249,115,22,0.08)"/>
        <stop offset="100%" stop-color="transparent"/>
      </radialGradient>
    </defs>
    <ellipse id="spotEllipse" cx="50%" cy="50%" rx="600" ry="500" fill="url(#spotGrad)" opacity="0"/>
  </svg>

  <!-- Particle canvas -->
  <canvas id="particleCanvas"></canvas>

  <!-- Fine grid -->
  <div class="hero-grid"></div>

  <!-- Ambient glow -->
  <div class="hero-glow"></div>

  <!-- L1 — Far wireframe cranes -->
  <div class="crane-layer" id="craneLayer">
    <svg class="crane-svg crane-1" viewBox="0 0 300 600" preserveAspectRatio="xMidYMax meet">
      <line x1="140" y1="600" x2="140" y2="30"/>
      <line x1="160" y1="600" x2="160" y2="30"/>
      <line x1="140" y1="30" x2="160" y2="30"/>
      <line x1="140" y1="95"  x2="160" y2="155"/><line x1="160" y1="95"  x2="140" y2="155"/>
      <line x1="140" y1="205" x2="160" y2="265"/><line x1="160" y1="205" x2="140" y2="265"/>
      <line x1="140" y1="315" x2="160" y2="375"/><line x1="160" y1="315" x2="140" y2="375"/>
      <line x1="140" y1="425" x2="160" y2="485"/><line x1="160" y1="425" x2="140" y2="485"/>
      <line x1="160" y1="34"  x2="298" y2="50"/>
      <line x1="140" y1="30"  x2="2"   y2="60"/>
      <line x1="148" y1="1"   x2="298" y2="50" stroke-dasharray="4,5"/>
      <line x1="148" y1="1"   x2="2"   y2="60" stroke-dasharray="4,5"/>
      <line x1="106" y1="600" x2="194" y2="600"/>
      <line x1="120" y1="600" x2="140" y2="555"/>
      <line x1="180" y1="600" x2="160" y2="555"/>
    </svg>
    <svg class="crane-svg crane-2" viewBox="0 0 350 650" preserveAspectRatio="xMidYMax meet">
      <line x1="168" y1="650" x2="168" y2="40"/>
      <line x1="188" y1="650" x2="188" y2="40"/>
      <line x1="168" y1="40"  x2="188" y2="40"/>
      <line x1="168" y1="110" x2="188" y2="178"/><line x1="188" y1="110" x2="168" y2="178"/>
      <line x1="168" y1="238" x2="188" y2="306"/><line x1="188" y1="238" x2="168" y2="306"/>
      <line x1="168" y1="366" x2="188" y2="434"/><line x1="188" y1="366" x2="168" y2="434"/>
      <line x1="188" y1="44"  x2="346" y2="66"/>
      <line x1="168" y1="40"  x2="6"   y2="70"/>
      <line x1="176" y1="4"   x2="346" y2="66" stroke-dasharray="5,5"/>
      <line x1="176" y1="4"   x2="6"   y2="70" stroke-dasharray="5,5"/>
      <line x1="136" y1="650" x2="220" y2="650"/>
      <line x1="148" y1="650" x2="168" y2="596"/>
      <line x1="208" y1="650" x2="188" y2="596"/>
    </svg>
    <svg class="crane-svg crane-3" viewBox="0 0 180 500" preserveAspectRatio="xMidYMax meet">
      <line x1="84" y1="500" x2="84" y2="62"/>
      <line x1="96" y1="500" x2="96" y2="62"/>
      <line x1="84" y1="62"  x2="96" y2="62"/>
      <line x1="84" y1="126" x2="96" y2="178"/><line x1="96" y1="126" x2="84" y2="178"/>
      <line x1="84" y1="256" x2="96" y2="308"/><line x1="96" y1="256" x2="84" y2="308"/>
      <line x1="96" y1="65"  x2="178" y2="80"/>
      <line x1="84" y1="62"  x2="2"   y2="82"/>
    </svg>
  </div>

  <!-- L2 — Animated crane arm -->
  <div class="crane-arm-layer">
    <div class="crane-arm-pivot" id="craneArm">
      <div class="arm-beam"></div>
      <div class="arm-cable"></div>
      <div class="arm-hook"></div>
    </div>
  </div>

  <!-- L3 — Foreground typography + data -->
  <div class="hero-content">

    <div class="hero-sys-label" id="heroLabel"
         data-tr="🇹🇷 Türkiye'nin İlk Yapay Zeka Destekli Şantiye Platformu"
         data-en="🇹🇷 Turkey's First AI-Powered Construction Platform">
      <span class="sys-dot"></span>
      🇹🇷 Türkiye'nin İlk Yapay Zeka Destekli Şantiye Platformu
    </div>

    <h1 class="hero-h1" id="heroH1">
      <span class="line-1">
        <span data-tr="Şantiyeni" data-en="Manage Your">Şantiyeni</span>
        <span class="word-ai" data-tr=" Yapay Zeka" data-en=" with AI"> Yapay Zeka</span>
      </span><br>
      <span class="line-2" data-tr="ile Yönet" data-en="Construction">ile Yönet</span>
    </h1>

    <p class="hero-sub" id="heroSub"
       data-tr="Kamera analizi, AI raporlama, fiyat takibi ve Türkiye mevzuatına uygun hesaplamalar. Saha mühendisleri ve müteahhitler için tasarlandı."
       data-en="Camera analysis, AI reporting, price tracking and calculations compliant with Turkish regulations. Designed for field engineers and contractors.">
      Kamera analizi, AI raporlama, fiyat takibi ve Türkiye mevzuatına uygun hesaplamalar.
      Saha mühendisleri ve müteahhitler için tasarlandı.
    </p>

    <div class="hero-btns" id="heroBtns">
      <a href="/app#register" class="btn-fire"
         data-tr="🚀 Ücretsiz Başla" data-en="🚀 Start Free">🚀 Ücretsiz Başla</a>
      <a href="#features" class="btn-ghost"
         data-tr="Özellikleri Gör" data-en="See Features">Özellikleri Gör</a>
    </div>

    <div class="eng-card" id="engCard">
      <div class="eng-cell">
        <div class="eng-val">50+</div>
        <div class="eng-lbl" data-tr="Mühendislik Hesabı" data-en="Eng. Calculations">Mühendislik Hesabı</div>
      </div>
      <div class="eng-cell">
        <div class="eng-val">7/24</div>
        <div class="eng-lbl" data-tr="AI Asistan" data-en="AI Assistant">AI Asistan</div>
      </div>
      <div class="eng-cell">
        <div class="eng-val">TBDY 2018</div>
        <div class="eng-lbl" data-tr="Tam Uyumlu" data-en="Fully Compliant">Tam Uyumlu</div>
      </div>
      <div class="eng-cell">
        <div class="eng-val">₺</div>
        <div class="eng-lbl" data-tr="Yerel Fiyat" data-en="Local Pricing">Yerel Fiyat</div>
      </div>
    </div>

  </div><!-- /hero-content -->

  <div class="hero-fade"></div>
</div><!-- /hero-scene -->
</div><!-- /hero-pin-wrap -->

<!-- FEATURES -->
<section id="features">
  <div class="section-inner">
    <div class="reveal">
      <div class="section-label" data-tr="Özellikler" data-en="Features">Özellikler</div>
      <h2 class="section-title" data-tr="Tek Platformda<br>Her Şey" data-en="Everything in<br>One Platform">Tek Platformda<br>Her Şey</h2>
      <p class="section-sub" data-tr="Sahadan ofise tüm ihtiyaçların bir arada. Başka uygulamaya gerek yok." data-en="All your needs from field to office in one place. No other apps needed.">
        Sahadan ofise tüm ihtiyaçların bir arada. Başka uygulamaya gerek yok.
      </p>
    </div>
    <div class="features-grid">
      <div class="feature-card reveal" style="--c:var(--amber)">
        <div class="feature-icon">🤖</div>
        <div class="feature-title" data-tr="AI Asistan" data-en="AI Assistant">AI Asistan</div>
        <div class="feature-desc" data-tr="Soru sor, hesap yaptır, saha fotoğrafı analiz et. Türkçe konuşan, inşaat bilen yapay zeka." data-en="Ask questions, calculate, analyze site photos. AI that speaks Turkish and knows construction.">Soru sor, hesap yaptır, saha fotoğrafı analiz et. Türkçe konuşan, inşaat bilen yapay zeka.</div>
        <span class="feature-tag" style="--bg:rgba(249,115,22,.1);--tc:#fb923c;--bc:rgba(249,115,22,.2)" data-tr="Türkçe Destekli" data-en="Turkish Supported">Türkçe Destekli</span>
      </div>
      <div class="feature-card reveal" style="--c:#22d3ee">
        <div class="feature-icon">📷</div>
        <div class="feature-title" data-tr="Kamera Analizi" data-en="Camera Analysis">Kamera Analizi</div>
        <div class="feature-desc" data-tr="Sahadan fotoğraf yükle, AI anlık analiz yapsın. Çatlak tespiti, donatı kontrolü, kalıp incelemesi." data-en="Upload site photos, AI analyzes instantly. Crack detection, rebar check, formwork inspection.">Sahadan fotoğraf yükle, AI anlık analiz yapsın. Çatlak tespiti, donatı kontrolü, kalıp incelemesi.</div>
        <span class="feature-tag" style="--bg:rgba(34,211,238,.1);--tc:#22d3ee;--bc:rgba(34,211,238,.2)" data-tr="Anlık Analiz" data-en="Real-time Analysis">Anlık Analiz</span>
      </div>
      <div class="feature-card reveal" style="--c:#a78bfa">
        <div class="feature-icon">🏗️</div>
        <div class="feature-title" data-tr="Şantiye Yönetimi" data-en="Site Management">Şantiye Yönetimi</div>
        <div class="feature-desc" data-tr="Günlük rapor, sesli rapor, ilerleme takibi. Müteahhitten mühendise tüm ekip tek platformda." data-en="Daily reports, voice reports, progress tracking. All team on one platform.">Günlük rapor, sesli rapor, ilerleme takibi. Müteahhitten mühendise tüm ekip tek platformda.</div>
        <span class="feature-tag" style="--bg:rgba(167,139,250,.1);--tc:#a78bfa;--bc:rgba(167,139,250,.2)" data-tr="Çoklu Şantiye" data-en="Multi-Site">Çoklu Şantiye</span>
      </div>
      <div class="feature-card reveal" style="--c:#34d399">
        <div class="feature-icon">💹</div>
        <div class="feature-title" data-tr="Fiyat &amp; Stok Takibi" data-en="Price &amp; Stock Tracking">Fiyat &amp; Stok Takibi</div>
        <div class="feature-desc" data-tr="Demir, çimento, beton fiyatlarını takip et. Stok düşünce bildirim al, maliyetleri kontrol et." data-en="Track iron, cement, concrete prices. Get alerts when stock is low.">Demir, çimento, beton fiyatlarını takip et. Stok düşünce bildirim al, maliyetleri kontrol et.</div>
        <span class="feature-tag" style="--bg:rgba(52,211,153,.1);--tc:#34d399;--bc:rgba(52,211,153,.2)" data-tr="Anlık Fiyatlar" data-en="Live Prices">Anlık Fiyatlar</span>
      </div>
      <div class="feature-card reveal" style="--c:#f472b6">
        <div class="feature-icon">🌍</div>
        <div class="feature-title" data-tr="Deprem Analizi" data-en="Earthquake Analysis">Deprem Analizi</div>
        <div class="feature-desc" data-tr="Şantiye konumuna göre deprem risk analizi. AFAD verileri ve TBDY 2018 parametreleri ile." data-en="Earthquake risk analysis based on site location. With AFAD data and TBDY 2018 parameters.">Şantiye konumuna göre deprem risk analizi. AFAD verileri ve TBDY 2018 parametreleri ile.</div>
        <span class="feature-tag" style="--bg:rgba(244,114,182,.1);--tc:#f472b6;--bc:rgba(244,114,182,.2)" data-tr="AFAD Entegre" data-en="AFAD Integrated">AFAD Entegre</span>
      </div>
      <div class="feature-card reveal" style="--c:var(--amber)">
        <div class="feature-icon">📱</div>
        <div class="feature-title" data-tr="Mobil Uygulama" data-en="Mobile App">Mobil Uygulama</div>
        <div class="feature-desc" data-tr="Sahada telefona yükle, internetsiz çalış. iOS ve Android destekli PWA uygulama." data-en="Install on phone at site, works offline. PWA app with iOS and Android support.">Sahada telefona yükle, internetsiz çalış. iOS ve Android destekli PWA uygulama.</div>
        <span class="feature-tag" style="--bg:rgba(249,115,22,.1);--tc:#fb923c;--bc:rgba(249,115,22,.2)" data-tr="iOS &amp; Android" data-en="iOS &amp; Android">iOS &amp; Android</span>
      </div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="how-section">
  <div class="section-inner">
    <div class="reveal">
      <div class="section-label" data-tr="Nasıl Çalışır?" data-en="How it Works?">Nasıl Çalışır?</div>
      <h2 class="section-title" data-tr="3 Adımda<br>Başla" data-en="Get Started<br>in 3 Steps">3 Adımda<br>Başla</h2>
    </div>
    <div class="steps">
      <div class="step reveal">
        <div class="step-num">1</div>
        <div class="step-content">
          <div class="step-title" data-tr="Ücretsiz hesap oluştur" data-en="Create a free account">Ücretsiz hesap oluştur</div>
          <div class="step-desc" data-tr="Email ile 30 saniyede kayıt ol. Kredi kartı gerekmez. Günde 20 AI sorgusu ücretsiz." data-en="Sign up in 30 seconds. No credit card. 20 free AI queries per day.">Email ile 30 saniyede kayıt ol. Kredi kartı gerekmez. Günde 20 AI sorgusu ücretsiz.</div>
        </div>
      </div>
      <div class="step reveal">
        <div class="step-num">2</div>
        <div class="step-content">
          <div class="step-title" data-tr="Şantiyeni ekle" data-en="Add your construction site">Şantiyeni ekle</div>
          <div class="step-desc" data-tr="Şantiye adı, konum ve bilgileri gir. Harita üzerinden deprem riski analiz edilsin." data-en="Enter site name, location and details. Let earthquake risk be analyzed on the map.">Şantiye adı, konum ve bilgileri gir. Harita üzerinden deprem riski analiz edilsin.</div>
        </div>
      </div>
      <div class="step reveal">
        <div class="step-num">3</div>
        <div class="step-content">
          <div class="step-title" data-tr="AI'ı çalıştır" data-en="Run the AI">AI'ı çalıştır</div>
          <div class="step-desc" data-tr="Soru sor, fotoğraf yükle, rapor oluştur. Tüm hesaplamalar Türkiye standartlarına göre." data-en="Ask questions, upload photos, generate reports. All calculations per Turkish standards.">Soru sor, fotoğraf yükle, rapor oluştur. Tüm hesaplamalar Türkiye standartlarına göre.</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- MEVZUAT -->
<section>
  <div class="section-inner">
    <div class="reveal">
      <div class="section-label" data-tr="Türkiye Mevzuatı" data-en="Turkish Regulations">Türkiye Mevzuatı</div>
      <h2 class="section-title" data-tr="Yerel Standartlara<br>Tam Uyum" data-en="Full Compliance with<br>Local Standards">Yerel Standartlara<br>Tam Uyum</h2>
      <p class="section-sub" data-tr="Yabancı rakipler Türkiye mevzuatını bilmez. Biz burada doğduk, buranın kurallarını biliyoruz." data-en="Foreign competitors don't know Turkish regulations. We know the rules.">Yabancı rakipler Türkiye mevzuatını bilmez. Biz burada doğduk, buranın kurallarını biliyoruz.</p>
    </div>
    <div class="mevzuat-grid">
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">📐</div><div><div class="mevzuat-text">TBDY 2018</div><div class="mevzuat-sub" data-tr="Türkiye Bina Deprem Yönetmeliği" data-en="Turkey Building Earthquake Code">Türkiye Bina Deprem Yönetmeliği</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">🏛️</div><div><div class="mevzuat-text">TS 500</div><div class="mevzuat-sub" data-tr="Betonarme Yapı Tasarım Kuralları" data-en="Reinforced Concrete Design Rules">Betonarme Yapı Tasarım Kuralları</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">🌍</div><div><div class="mevzuat-text">AFAD</div><div class="mevzuat-sub" data-tr="Deprem Tehlike Haritası Entegrasyonu" data-en="Earthquake Hazard Map Integration">Deprem Tehlike Haritası Entegrasyonu</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">🦺</div><div><div class="mevzuat-text">İSG</div><div class="mevzuat-sub" data-tr="İş Sağlığı ve Güvenliği Standartları" data-en="Occupational Health &amp; Safety Standards">İş Sağlığı ve Güvenliği Standartları</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">💰</div><div><div class="mevzuat-text">TL Fiyat</div><div class="mevzuat-sub" data-tr="Güncel Türk Lirası Malzeme Fiyatları" data-en="Current Turkish Lira Material Prices">Güncel Türk Lirası Malzeme Fiyatları</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">🗺️</div><div><div class="mevzuat-text">81 İl</div><div class="mevzuat-sub" data-tr="Tüm Türkiye'de Hava Durumu &amp; Risk" data-en="Weather &amp; Risk Across All Turkey">Tüm Türkiye'de Hava Durumu &amp; Risk</div></div></div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-section">
  <div class="section-inner" style="text-align:center">
    <div class="reveal">
      <div class="section-label" data-tr="Hemen Başla" data-en="Get Started">Hemen Başla</div>
      <h2 class="section-title" data-tr="Şantiyeni<br><span style='color:var(--amber)'>Dönüştür</span>" data-en="Transform<br><span style='color:var(--amber)'>Your Site</span>">Şantiyeni<br><span style="color:var(--amber)">Dönüştür</span></h2>
      <p class="section-sub" style="margin:16px auto 40px;text-align:center" data-tr="Ücretsiz hesap aç, 5 dakikada şantiyeni ekle. Kredi kartı gerekmez." data-en="Create a free account, add your site in 5 minutes. No credit card.">Ücretsiz hesap aç, 5 dakikada şantiyeni ekle. Kredi kartı gerekmez.</p>
      <a href="/app#register" class="btn-fire" style="font-size:17px;padding:16px 42px" data-tr="🚀 Ücretsiz Başla" data-en="🚀 Start Free">🚀 Ücretsiz Başla</a>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-logo">Building<span>AI</span></div>
  <div class="footer-copy" data-tr="© 2026 BuildingAI · Türkiye'nin Şantiye AI Platformu" data-en="© 2026 BuildingAI · Turkey's Construction AI Platform">© 2026 BuildingAI · Türkiye'nin Şantiye AI Platformu</div>
</footer>

<!-- ============================================================
     SCRIPTS
     ============================================================ -->
<script>
/* ── Language switcher ── */
function setLang(lang) {
  document.querySelectorAll('[data-tr]').forEach(el => {
    const t = el.getAttribute('data-' + lang);
    if (t) el.innerHTML = t;
  });
  document.getElementById('btn-tr').classList.toggle('active', lang === 'tr');
  document.getElementById('btn-en').classList.toggle('active', lang === 'en');
  document.documentElement.lang = lang;
  localStorage.setItem('lang', lang);
}
if (localStorage.getItem('lang') === 'en') setLang('en');

/* ── Scroll reveal (for sections below hero) ── */
const ro = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) setTimeout(() => e.target.classList.add('visible'), i * 80);
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => ro.observe(el));

/* ── Toast 429 ── */
const tc = document.createElement('div');
tc.className = 'toast-container';
document.body.appendChild(tc);
function showRateLimitToast() {
  const t = document.createElement('div');
  t.className = 'toast';
  const lang = document.documentElement.lang || 'tr';
  t.innerHTML = `<div class="toast-icon">⏳</div><div><div class="toast-title">${lang==='en'?'Too Many Requests (429)':'Çok Fazla İstek (429)'}</div><div class="toast-desc">${lang==='en'?'Please wait. System is protected.':'Lütfen bekleyin. Sistem korunuyor.'}</div></div>`;
  tc.appendChild(t);
  setTimeout(() => t.classList.add('show'), 10);
  setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 500); }, 5000);
}
const _f = window.fetch;
window.fetch = async (...a) => { const r = await _f(...a); if (r.status === 429) showRateLimitToast(); return r; };
window.XMLHttpRequest = (function(O) {
  return function() { const x = new O(); x.addEventListener('load', () => { if (x.status===429) showRateLimitToast(); }); return x; };
})(window.XMLHttpRequest);

/* ── Particle canvas ── */
(function() {
  const canvas = document.getElementById('particleCanvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, pts = [];
  const N = 100;
  function resize() { W = canvas.width = canvas.offsetWidth; H = canvas.height = canvas.offsetHeight; }
  window.addEventListener('resize', resize); resize();
  class P {
    constructor(){ this.spawn() }
    spawn(){
      this.x = Math.random()*W; this.y = Math.random()*H;
      this.r = Math.random()*1.3+0.25;
      this.vx = (Math.random()-.5)*.28; this.vy = -Math.random()*.16-.04;
      this.a = Math.random()*.42+.1; this.life = Math.random()*320+180; this.age=0;
    }
    tick(){ this.x+=this.vx; this.y+=this.vy; this.age++; if(this.age>this.life||this.x<-10||this.x>W+10||this.y<-10) this.spawn(); }
    draw(){
      const f=1-this.age/this.life;
      ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(255,255,255,${this.a*f})`; ctx.fill();
    }
  }
  for(let i=0;i<N;i++) pts.push(new P());
  function frame(){
    ctx.clearRect(0,0,W,H);
    pts.forEach(p=>{p.tick();p.draw()});
    for(let i=0;i<pts.length;i++){
      for(let j=i+1;j<pts.length;j++){
        const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);
        if(d<90){ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.strokeStyle=`rgba(255,255,255,${0.022*(1-d/90)})`;ctx.stroke();}
      }
    }
    requestAnimationFrame(frame);
  }
  frame();
})();

/* ── SVG Spotlight (mouse tracking) ── */
(function(){
  const scene = document.getElementById('heroScene');
  const ellipse = document.getElementById('spotEllipse');
  if(!scene||!ellipse) return;
  gsap.to('#spotEllipse', { opacity:1, duration:1.5, delay:1.5, ease:'power2.out' });
  scene.addEventListener('mousemove', e => {
    const r = scene.getBoundingClientRect();
    const x = ((e.clientX - r.left) / r.width) * 100;
    const y = ((e.clientY - r.top) / r.height) * 100;
    gsap.to(ellipse, { attr:{ cx: x+'%', cy: y+'%' }, duration:0.8, ease:'power2.out', overwrite:true });
  });
  scene.addEventListener('mouseleave', () => {
    gsap.to(ellipse, { attr:{ cx:'50%', cy:'50%' }, opacity:0, duration:1, ease:'power2.out' });
  });
  scene.addEventListener('mouseenter', () => {
    gsap.to(ellipse, { opacity:1, duration:0.5, ease:'power2.out' });
  });
})();

/* ── GSAP Hero Animations ── */
window.addEventListener('load', () => {
  gsap.registerPlugin(ScrollTrigger, TextPlugin);

  /* Set initial hidden states */
  gsap.set(['#heroLabel','#heroH1','#heroSub','#heroBtns','#engCard'], { opacity:0, y:50 });
  gsap.set('#craneArm', { opacity:0, rotation:-28, transformOrigin:'0% 50%' });

  /* INTRO: staggered entrance */
  const intro = gsap.timeline({ defaults: { ease:'power4.out' } });
  intro
    .to('#heroLabel', { opacity:1, y:0, duration:0.9, delay:0.2 })
    .to('#heroH1',    { opacity:1, y:0, duration:1.4 }, '-=0.5')
    .to('#heroSub',   { opacity:1, y:0, duration:0.9 }, '-=0.8')
    .to('#heroBtns',  { opacity:1, y:0, duration:0.9 }, '-=0.6')
    .to('#engCard',   { opacity:1, y:0, duration:1.1 }, '-=0.6')
    .to('#craneArm',  { opacity:1, rotation:-7, duration:2.2, ease:'power2.out' }, '-=1.8');

  /* TEXT SCRAMBLE on H1 (TextPlugin shimmer) */
  const chars = 'ABCDEFGHIJKLMNOPRSTWXYZabcdefghijklmnoprstuvwxyz0123456789';
  function scramble(el, finalText, duration) {
    let frame = 0;
    const totalFrames = Math.round(duration * 60);
    const tick = () => {
      const progress = frame / totalFrames;
      const revealed = Math.floor(progress * finalText.length);
      let text = finalText.slice(0, revealed);
      for (let i = revealed; i < finalText.length; i++) {
        text += chars[Math.floor(Math.random() * chars.length)];
      }
      el.textContent = text;
      frame++;
      if (frame <= totalFrames) requestAnimationFrame(tick);
      else el.textContent = finalText;
    };
    tick();
  }

  /* Scramble each line after intro delay */
  setTimeout(() => {
    const line2 = document.querySelector('.line-2');
    if (line2) scramble(line2, line2.textContent.trim(), 1.2);
  }, 1800);

  /* SCROLL-DRIVEN PARALLAX */
  const stConfig = {
    trigger: '#heroPinWrap',
    start: 'top top',
    end: '+=80%',
    scrub: 1.8,
  };

  /* Content fades up */
  gsap.to(['#heroLabel','#heroH1'], { scrollTrigger:stConfig, y:-140, opacity:0, scale:0.96 });
  gsap.to('#heroSub',  { scrollTrigger:{...stConfig,start:'top top',end:'+=60%'}, y:-90,  opacity:0 });
  gsap.to('#heroBtns', { scrollTrigger:{...stConfig,start:'top top',end:'+=55%'}, y:-70,  opacity:0 });
  gsap.to('#engCard',  { scrollTrigger:{...stConfig,start:'top top',end:'+=50%'}, y:-50,  opacity:0 });

  /* Cranes drift upward (slow parallax) */
  gsap.to('#craneLayer', { scrollTrigger:stConfig, y:-100 });

  /* Crane arm rotates and lifts away */
  gsap.to('#craneArm', {
    scrollTrigger: { trigger:'#heroPinWrap', start:'top top', end:'+=70%', scrub:2 },
    rotation: 20, y: 250, opacity: 0.2
  });

  ScrollTrigger.refresh();
});
</script>
</body>
</html>
"""

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(landing)
print("DONE: Terminal Industries-grade hero written.")
