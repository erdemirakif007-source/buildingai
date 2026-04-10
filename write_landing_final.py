# -*- coding: utf-8 -*-
# Complete landing.html rewrite - clean, no debt, no accumulated patches

landing_html = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BuildingAI \u2014 \u015eantiyenin Yapay Zekas\u0131</title>
<meta name="description" content="Kamera analizi, AI raporlama, fiyat takibi ve T\u00fcrkiye mevzuat\u0131na uygun hesaplamalar. Saha m\u00fchendisleri i\u00e7in.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<style>
/* ============================================================
   BUILDING AI  —  DESIGN SYSTEM
   Single source of truth. No duplicate rules.
   ============================================================ */

/* --- TOKENS --- */
:root {
  --navy:       #060d1a;
  --navy2:      #0a1628;
  --amber:      #f97316;
  --amber2:     #fb923c;
  --cyan:       #22d3ee;
  --cyan-dim:   rgba(34,211,238,0.12);
  --text1:      #f0f4ff;
  --text2:      #94a3b8;
  --text3:      #3d5070;
  --border:     rgba(255,255,255,0.07);
  --border2:    rgba(255,255,255,0.14);
}

/* --- RESET --- */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: \'Instrument Sans\', sans-serif;
  background: var(--navy);
  color: var(--text1);
  overflow-x: hidden;
}

/* Fine grid texture */
body::before {
  content: \'\';
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image:
    linear-gradient(rgba(34,211,238,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34,211,238,0.025) 1px, transparent 1px);
  background-size: 60px 60px;
}

/* ============================================================
   NAV
   ============================================================ */
nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 200;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 5%; height: 64px;
  background: rgba(6,13,26,0.88);
  backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid var(--border);
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
  font-family: \'Bebas Neue\', sans-serif; font-size: 22px; letter-spacing: .08em;
}
.nav-logo span { color: var(--amber); }
.nav-right { display: flex; align-items: center; gap: 12px; }
.lang-btn {
  background: none; border: 1px solid var(--border2);
  color: var(--text2); font-size: 12px; font-family: \'DM Mono\', monospace;
  padding: 5px 12px; border-radius: 6px; cursor: pointer; transition: all .15s;
}
.lang-btn:hover, .lang-btn.active { border-color: var(--amber); color: var(--amber); }
.nav-cta {
  background: var(--amber); color: #000; font-weight: 600; font-size: 13px;
  padding: 8px 20px; border-radius: 8px; text-decoration: none; transition: all .15s;
}
.nav-cta:hover { background: var(--amber2); transform: translateY(-1px); }
.btn-secondary-nav {
  padding: 8px 18px; font-size: 13px; border-radius: 8px; text-decoration: none;
  border: 1px solid rgba(255,255,255,0.2); color: white; transition: all .15s;
}

/* ============================================================
   HERO  —  TERMINAL CINEMATIC
   ============================================================ */
.hero-scene {
  position: relative;
  width: 100%; height: 100vh; min-height: 700px;
  background: #000; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
}

/* Particle canvas */
#particleCanvas {
  position: absolute; inset: 0; z-index: 1; pointer-events: none;
  width: 100%; height: 100%;
}

/* Ambient orange glow at bottom */
.hero-glow {
  position: absolute; bottom: -250px; left: 50%; transform: translateX(-50%);
  width: 140vw; height: 600px;
  background: radial-gradient(ellipse at center, rgba(249,115,22,0.07) 0%, transparent 65%);
  z-index: 2; pointer-events: none;
}

/* SVG wireframe cranes — far background */
.crane-layer {
  position: absolute; inset: 0; z-index: 3;
  pointer-events: none; overflow: hidden;
}
.crane-svg {
  position: absolute; fill: none;
  stroke: rgba(255,255,255,0.055); stroke-width: 1.2;
}
.crane-1 { bottom: 0; left: 6%;  width: 280px; height: 82vh; }
.crane-2 { bottom: 0; right: 10%; width: 320px; height: 88vh; opacity: 0.7; }
.crane-3 { bottom: 0; left: 44%; width: 160px; height: 55vh; opacity: 0.4; }

/* Animated crane arm — mid-ground */
.crane-arm-layer { position: absolute; inset: 0; z-index: 4; pointer-events: none; }
.crane-arm-pivot {
  position: absolute; top: 9%; left: 12%;
  width: 58vw; height: 5px;
  transform-origin: 0% 50%; transform: rotate(-25deg); opacity: 0;
}
.arm-beam {
  width: 100%; height: 100%;
  background: linear-gradient(90deg, rgba(249,115,22,0.55) 0%, rgba(249,115,22,0.08) 65%, transparent 100%);
  border-radius: 3px; box-shadow: 0 0 18px rgba(249,115,22,0.12);
}
.arm-cable {
  position: absolute; right: 28%; top: 5px;
  width: 1px; height: 28vh;
  background: linear-gradient(to bottom, rgba(255,255,255,0.18), transparent);
}
.arm-hook {
  position: absolute; right: calc(28% - 9px); top: calc(5px + 28vh);
  width: 18px; height: 18px;
  border: 2px solid rgba(249,115,22,0.45);
  border-top: none; border-radius: 0 0 9px 9px;
}

/* Foreground content */
.hero-content {
  position: relative; z-index: 10;
  text-align: center; max-width: 1080px; width: 92%; padding: 0 24px;
}

/* Badge */
.hero-badge {
  display: inline-flex; align-items: center; gap: 10px;
  font-family: \'DM Mono\', monospace; font-size: 11px;
  letter-spacing: 0.18em; text-transform: uppercase; color: var(--amber);
  margin-bottom: 32px;
}
.badge-dot {
  width: 8px; height: 8px; background: var(--amber); border-radius: 50%;
  box-shadow: 0 0 10px var(--amber);
  animation: dotPulse 2s ease-in-out infinite;
}
@keyframes dotPulse { 0%,100%{opacity:1; transform:scale(1)} 50%{opacity:0.35; transform:scale(0.65)} }

/* H1 */
.hero-h1 {
  font-family: \'Bebas Neue\', sans-serif;
  font-size: clamp(58px, 10.5vw, 148px);
  line-height: 0.9; letter-spacing: 0.03em; color: #fff;
  margin-bottom: 30px;
}
.hero-h1 em { font-style: normal; color: var(--cyan); }

/* Subtitle */
.hero-sub {
  font-size: clamp(15px, 1.8vw, 19px); color: #94a3b8;
  max-width: 600px; margin: 0 auto 50px; line-height: 1.65;
}

/* Buttons */
.hero-btns { display: flex; gap: 18px; justify-content: center; flex-wrap: wrap; margin-bottom: 64px; }
.btn-primary {
  background: var(--amber); color: #000 !important;
  font-weight: 700; font-size: 16px; padding: 16px 46px;
  border-radius: 8px; text-decoration: none;
  box-shadow: 0 0 28px rgba(249,115,22,0.4), 0 8px 20px rgba(0,0,0,0.3);
  transition: all 0.3s cubic-bezier(0.16,1,0.3,1); border: none; cursor: pointer;
}
.btn-primary:hover { transform: translateY(-3px) scale(1.04); box-shadow: 0 0 45px rgba(249,115,22,0.6); }
.btn-ghost {
  background: rgba(255,255,255,0.04); color: #fff !important;
  font-weight: 500; font-size: 16px; padding: 16px 46px;
  border-radius: 8px; border: 1px solid rgba(255,255,255,0.14);
  text-decoration: none; transition: all 0.3s; cursor: pointer;
}
.btn-ghost:hover { background: rgba(255,255,255,0.08); border-color: rgba(255,255,255,0.4); transform: translateY(-3px); }

/* Engineering data card (Premium Glassmorphism) */
.eng-card {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
  border-top: 1px solid rgba(255,255,255,0.12);
  border-left: 1px solid rgba(255,255,255,0.12);
  border-right: 1px solid rgba(255,255,255,0.03);
  border-bottom: 1px solid rgba(255,255,255,0.03);
  border-radius: 20px;
  box-shadow:
    0 30px 60px rgba(0,0,0,0.45),
    0 0 0 1px rgba(255,255,255,0.05) inset,
    0 1px 0 rgba(255,255,255,0.12) inset;
  display: flex; flex-wrap: wrap;
  max-width: 820px; margin: 0 auto; overflow: hidden;
}
.eng-cell {
  flex: 1; min-width: 150px; padding: 26px 20px; text-align: center;
  border-right: 1px solid rgba(255,255,255,0.06);
}
.eng-cell:last-child { border-right: none; }
.eng-val {
  font-family: \'DM Mono\', monospace; font-weight: 500;
  font-size: clamp(22px, 3vw, 38px); color: #fff;
  letter-spacing: -0.02em; line-height: 1.1;
}
.eng-lbl {
  font-size: 10px; color: #4b6280; font-family: \'DM Mono\', monospace;
  text-transform: uppercase; letter-spacing: 0.1em; margin-top: 7px; font-weight: 600;
}

/* Seamless gradient to sections below */
.hero-fade {
  position: absolute; bottom: 0; left: 0; width: 100%; height: 220px;
  background: linear-gradient(to top, var(--navy) 0%, transparent 100%);
  z-index: 11; pointer-events: none;
}

/* ============================================================
   TOAST NOTIFICATION
   ============================================================ */
.toast-container { position: fixed; bottom: 24px; right: 24px; z-index: 9999; display: flex; flex-direction: column; gap: 12px; pointer-events: none; }
.toast {
  background: rgba(10,18,35,0.92); backdrop-filter: blur(16px);
  border: 1px solid rgba(244,63,94,0.4); border-radius: 12px;
  padding: 16px 20px; min-width: 300px; max-width: 400px;
  box-shadow: 0 10px 30px rgba(244,63,94,0.2);
  display: flex; align-items: flex-start; gap: 14px;
  transform: translateX(120%); opacity: 0; pointer-events: auto;
  transition: all 0.5s cubic-bezier(0.16,1,0.3,1);
}
.toast-icon { font-size: 22px; line-height: 1; }
.toast-title { font-weight: 600; color: #fff; font-size: 14px; margin-bottom: 3px; }
.toast-desc { font-size: 12px; color: #cbd5e1; line-height: 1.4; }
.toast.show { transform: translateX(0); opacity: 1; }

/* ============================================================
   SECTIONS (Features, Steps, Mevzuat, CTA, Footer)
   ============================================================ */
section { position: relative; z-index: 1; }
.section-inner { max-width: 1100px; margin: 0 auto; padding: 100px 5%; }
.section-label { font-family: \'DM Mono\', monospace; font-size: 11px; letter-spacing: .16em; color: var(--cyan); text-transform: uppercase; margin-bottom: 16px; }
.section-title { font-family: \'Bebas Neue\', sans-serif; font-size: clamp(36px,5vw,60px); letter-spacing: .04em; line-height: 1; margin-bottom: 16px; }
.section-sub { font-size: 16px; color: var(--text2); line-height: 1.7; max-width: 520px; }

.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px,1fr)); gap: 16px; margin-top: 56px; }
.feature-card {
  background: rgba(15,32,64,0.5); border: 1px solid var(--border);
  border-radius: 16px; padding: 28px; transition: all .2s; cursor: default;
  position: relative; overflow: hidden;
}
.feature-card::before { content: \'\'; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: var(--c,transparent); opacity: 0; transition: opacity .2s; }
.feature-card:hover { border-color: var(--border2); transform: translateY(-4px); }
.feature-card:hover::before { opacity: 1; }
.feature-icon { font-size: 32px; margin-bottom: 16px; }
.feature-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
.feature-desc { font-size: 14px; color: var(--text2); line-height: 1.6; }
.feature-tag { display: inline-block; margin-top: 14px; font-family: \'DM Mono\', monospace; font-size: 10px; letter-spacing: .08em; padding: 3px 10px; border-radius: 4px; background: var(--bg,rgba(255,255,255,0.06)); color: var(--tc,var(--text3)); border: 1px solid var(--bc,var(--border)); }

.how-section { background: rgba(10,22,40,0.6); }
.steps { display: flex; flex-direction: column; gap: 0; margin-top: 56px; position: relative; }
.steps::before { content: \'\'; position: absolute; left: 23px; top: 0; bottom: 0; width: 2px; background: linear-gradient(to bottom,var(--amber),var(--cyan),transparent); opacity: .3; }
.step { display: flex; gap: 28px; padding: 32px 0; }
.step-num { width: 48px; height: 48px; border-radius: 50%; flex-shrink: 0; background: var(--navy2); border: 2px solid var(--amber); display: flex; align-items: center; justify-content: center; font-family: \'Bebas Neue\', sans-serif; font-size: 20px; color: var(--amber); position: relative; z-index: 1; }
.step-content { padding-top: 8px; }
.step-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
.step-desc { font-size: 14px; color: var(--text2); line-height: 1.6; max-width: 480px; }

.mevzuat-grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 12px; margin-top: 48px; }
.mevzuat-card { background: var(--cyan-dim); border: 1px solid rgba(34,211,238,0.15); border-radius: 12px; padding: 20px 22px; display: flex; align-items: center; gap: 14px; }
.mevzuat-icon { font-size: 24px; flex-shrink: 0; }
.mevzuat-text { font-size: 14px; font-weight: 500; }
.mevzuat-sub { font-size: 12px; color: var(--text2); margin-top: 3px; }

.cta-section { text-align: center; background: linear-gradient(135deg,rgba(249,115,22,0.08) 0%,rgba(34,211,238,0.05) 100%); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }
.cta-section .section-title { font-size: clamp(40px,6vw,72px); }

footer { padding: 40px 5%; border-top: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; position: relative; z-index: 1; }
.footer-logo { font-family: \'Bebas Neue\', sans-serif; font-size: 18px; letter-spacing: .08em; }
.footer-logo span { color: var(--amber); }
.footer-copy { font-size: 12px; color: var(--text3); font-family: \'DM Mono\', monospace; }

/* Scroll reveal */
.reveal { opacity: 0; transform: translateY(24px); transition: all .6s ease; }
.reveal.visible { opacity: 1; transform: none; }

/* ============================================================
   RESPONSIVE
   ============================================================ */
@media (max-width: 768px) {
  .crane-arm-pivot { display: none; }
  .crane-1, .crane-2 { opacity: 0.12; }
  .eng-card { flex-wrap: wrap; }
  .eng-cell { min-width: 50%; border-bottom: 1px solid rgba(255,255,255,0.06); }
  .eng-cell:nth-child(2) { border-right: none; }
  .hero-btns { gap: 12px; }
  .step { flex-direction: column; gap: 12px; }
  .steps::before { display: none; }
  footer { flex-direction: column; text-align: center; }
  .nav-right .btn-secondary-nav { display: none; }
}
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="nav-logo">
    \U0001f3d7\ufe0f Building<span>AI</span>
  </div>
  <div class="nav-right">
    <button class="lang-btn active" onclick="setLang(\'tr\')" id="btn-tr">TR</button>
    <button class="lang-btn" onclick="setLang(\'en\')" id="btn-en">EN</button>
    <a href="/app" class="btn-secondary-nav" data-tr="Giri\u015f Yap" data-en="Sign In">Giri\u015f Yap</a>
    <a href="/app#register" class="nav-cta" data-tr="\u00dccretsiz Dene" data-en="Try Free">\u00dccretsiz Dene</a>
  </div>
</nav>

<!-- HERO SCENE -->
<div class="hero-scene" id="heroScene">

  <!-- L0: Particle canvas -->
  <canvas id="particleCanvas"></canvas>

  <!-- Ambient glow -->
  <div class="hero-glow"></div>

  <!-- L1: Far-background wireframe cranes -->
  <div class="crane-layer" id="craneLayer">
    <!-- Left Crane -->
    <svg class="crane-svg crane-1" viewBox="0 0 300 600" preserveAspectRatio="xMidYMax meet">
      <line x1="140" y1="600" x2="140" y2="32"/>
      <line x1="160" y1="600" x2="160" y2="32"/>
      <line x1="140" y1="32" x2="160" y2="32"/>
      <line x1="140" y1="100" x2="160" y2="160"/><line x1="160" y1="100" x2="140" y2="160"/>
      <line x1="140" y1="210" x2="160" y2="270"/><line x1="160" y1="210" x2="140" y2="270"/>
      <line x1="140" y1="320" x2="160" y2="380"/><line x1="160" y1="320" x2="140" y2="380"/>
      <line x1="140" y1="430" x2="160" y2="490"/><line x1="160" y1="430" x2="140" y2="490"/>
      <line x1="160" y1="36" x2="295" y2="52"/><line x1="140" y1="32" x2="5" y2="62"/>
      <line x1="148" y1="2" x2="295" y2="52" stroke-dasharray="4,4"/>
      <line x1="148" y1="2" x2="5" y2="62" stroke-dasharray="4,4"/>
      <line x1="108" y1="600" x2="192" y2="600"/>
      <line x1="120" y1="600" x2="140" y2="555"/><line x1="180" y1="600" x2="160" y2="555"/>
    </svg>
    <!-- Right Crane -->
    <svg class="crane-svg crane-2" viewBox="0 0 350 650" preserveAspectRatio="xMidYMax meet">
      <line x1="168" y1="650" x2="168" y2="42"/>
      <line x1="188" y1="650" x2="188" y2="42"/>
      <line x1="168" y1="42" x2="188" y2="42"/>
      <line x1="168" y1="110" x2="188" y2="180"/><line x1="188" y1="110" x2="168" y2="180"/>
      <line x1="168" y1="240" x2="188" y2="310"/><line x1="188" y1="240" x2="168" y2="310"/>
      <line x1="168" y1="370" x2="188" y2="440"/><line x1="188" y1="370" x2="168" y2="440"/>
      <line x1="188" y1="46" x2="345" y2="68"/><line x1="168" y1="42" x2="8" y2="72"/>
      <line x1="176" y1="6" x2="345" y2="68" stroke-dasharray="5,5"/>
      <line x1="176" y1="6" x2="8" y2="72" stroke-dasharray="5,5"/>
      <line x1="138" y1="650" x2="218" y2="650"/>
      <line x1="148" y1="650" x2="168" y2="595"/><line x1="208" y1="650" x2="188" y2="595"/>
    </svg>
    <!-- Center Crane -->
    <svg class="crane-svg crane-3" viewBox="0 0 180 500" preserveAspectRatio="xMidYMax meet">
      <line x1="84" y1="500" x2="84" y2="62"/>
      <line x1="96" y1="500" x2="96" y2="62"/>
      <line x1="84" y1="62" x2="96" y2="62"/>
      <line x1="84" y1="125" x2="96" y2="175"/><line x1="96" y1="125" x2="84" y2="175"/>
      <line x1="84" y1="255" x2="96" y2="305"/><line x1="96" y1="255" x2="84" y2="305"/>
      <line x1="96" y1="65" x2="178" y2="80"/>
      <line x1="84" y1="62" x2="2" y2="82"/>
    </svg>
  </div>

  <!-- L2: Mid-ground animated crane arm -->
  <div class="crane-arm-layer">
    <div class="crane-arm-pivot" id="craneArm">
      <div class="arm-beam"></div>
      <div class="arm-cable"></div>
      <div class="arm-hook"></div>
    </div>
  </div>

  <!-- L3: Typography & engineering data -->
  <div class="hero-content">

    <div class="hero-badge" id="heroBadge"
         data-tr="\U0001f1f9\U0001f1f7 T\u00fcrkiye\'nin \u0130lk Yapay Zeka Destekli \u015eantiye Platformu"
         data-en="\U0001f1f9\U0001f1f7 Turkey\'s First AI-Powered Construction Platform">
      <span class="badge-dot"></span>
      \U0001f1f9\U0001f1f7 T\u00fcrkiye\'nin \u0130lk Yapay Zeka Destekli \u015eantiye Platformu
    </div>

    <h1 class="hero-h1" id="heroH1">
      <span data-tr="\u015eantiyeni" data-en="Manage Your">\u015eantiyeni</span>
      <em data-tr="Yapay Zeka" data-en="with AI">Yapay Zeka</em><br>
      <span data-tr="ile Y\u00f6net" data-en="Construction">ile Y\u00f6net</span>
    </h1>

    <p class="hero-sub" id="heroSub"
       data-tr="Kamera analizi, AI raporlama, fiyat takibi ve T\u00fcrkiye mevzuat\u0131na uygun hesaplamalar. Saha m\u00fchendisleri ve m\u00fcteahhitler i\u00e7in tasarland\u0131."
       data-en="Camera analysis, AI reporting, price tracking and calculations compliant with Turkish regulations. Designed for field engineers and contractors.">
      Kamera analizi, AI raporlama, fiyat takibi ve T\u00fcrkiye mevzuat\u0131na uygun hesaplamalar. Saha m\u00fchendisleri ve m\u00fcteahhitler i\u00e7in tasarland\u0131.
    </p>

    <div class="hero-btns" id="heroBtns">
      <a href="/app#register" class="btn-primary" data-tr="\U0001f680 \u00dccretsiz Ba\u015fla" data-en="\U0001f680 Start Free">\U0001f680 \u00dccretsiz Ba\u015fla</a>
      <a href="#features" class="btn-ghost" data-tr="\u00d6zellikleri G\u00f6r" data-en="See Features">\u00d6zellikleri G\u00f6r</a>
    </div>

    <div class="eng-card" id="engCard">
      <div class="eng-cell">
        <div class="eng-val">50+</div>
        <div class="eng-lbl" data-tr="M\u00fchendislik Hesab\u0131" data-en="Eng. Calculations">M\u00fchendislik Hesab\u0131</div>
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
        <div class="eng-val">\u20ba</div>
        <div class="eng-lbl" data-tr="Yerel Fiyat" data-en="Local Pricing">Yerel Fiyat</div>
      </div>
    </div>

  </div><!-- /hero-content -->

  <!-- Seamless bottom fade -->
  <div class="hero-fade"></div>

</div><!-- /hero-scene -->

<!-- FEATURES -->
<section id="features">
  <div class="section-inner">
    <div class="reveal">
      <div class="section-label" data-tr="\u00d6zellikler" data-en="Features">\u00d6zellikler</div>
      <h2 class="section-title" data-tr="Tek Platformda<br>Her \u015eey" data-en="Everything in<br>One Platform">Tek Platformda<br>Her \u015eey</h2>
      <p class="section-sub" data-tr="Sahadan ofise t\u00fcm ihtiya\u00e7lar\u0131n bir arada. Ba\u015fka uygulamaya gerek yok." data-en="All your needs from field to office in one place. No other apps needed.">
        Sahadan ofise t\u00fcm ihtiya\u00e7lar\u0131n bir arada. Ba\u015fka uygulamaya gerek yok.
      </p>
    </div>
    <div class="features-grid">
      <div class="feature-card reveal" style="--c: var(--amber)">
        <div class="feature-icon">\U0001f916</div>
        <div class="feature-title" data-tr="AI Asistan" data-en="AI Assistant">AI Asistan</div>
        <div class="feature-desc" data-tr="Soru sor, hesap yapt\u0131r, saha foto\u011fraf\u0131 analiz et. T\u00fcrk\u00e7e konu\u015fan, in\u015faat bilen yapay zeka." data-en="Ask questions, calculate, analyze site photos. AI that speaks Turkish and knows construction.">
          Soru sor, hesap yapt\u0131r, saha foto\u011fraf\u0131 analiz et. T\u00fcrk\u00e7e konu\u015fan, in\u015faat bilen yapay zeka.
        </div>
        <span class="feature-tag" style="--bg:rgba(249,115,22,0.1);--tc:#fb923c;--bc:rgba(249,115,22,0.2)" data-tr="T\u00fcrk\u00e7e Destekli" data-en="Turkish Supported">T\u00fcrk\u00e7e Destekli</span>
      </div>
      <div class="feature-card reveal" style="--c: #22d3ee">
        <div class="feature-icon">\U0001f4f7</div>
        <div class="feature-title" data-tr="Kamera Analizi" data-en="Camera Analysis">Kamera Analizi</div>
        <div class="feature-desc" data-tr="Sahadan foto\u011fraf y\u00fckle, AI anl\u0131k analiz yaps\u0131n. \u00c7atlak tespiti, donat\u0131 kontrol\u00fc, kal\u0131p incelemesi." data-en="Upload site photos, let AI analyze instantly. Crack detection, rebar check, formwork inspection.">
          Sahadan foto\u011fraf y\u00fckle, AI anl\u0131k analiz yaps\u0131n. \u00c7atlak tespiti, donat\u0131 kontrol\u00fc, kal\u0131p incelemesi.
        </div>
        <span class="feature-tag" style="--bg:rgba(34,211,238,0.1);--tc:#22d3ee;--bc:rgba(34,211,238,0.2)" data-tr="Anl\u0131k Analiz" data-en="Real-time Analysis">Anl\u0131k Analiz</span>
      </div>
      <div class="feature-card reveal" style="--c: #a78bfa">
        <div class="feature-icon">\U0001f3d7\ufe0f</div>
        <div class="feature-title" data-tr="\u015eantiye Y\u00f6netimi" data-en="Site Management">\u015eantiye Y\u00f6netimi</div>
        <div class="feature-desc" data-tr="G\u00fcnl\u00fck rapor, sesli rapor, ilerleme takibi. M\u00fcteahhitten m\u00fchendise t\u00fcm ekip tek platformda." data-en="Daily reports, voice reports, progress tracking. From contractor to engineer, all on one platform.">
          G\u00fcnl\u00fck rapor, sesli rapor, ilerleme takibi. M\u00fcteahhitten m\u00fchendise t\u00fcm ekip tek platformda.
        </div>
        <span class="feature-tag" style="--bg:rgba(167,139,250,0.1);--tc:#a78bfa;--bc:rgba(167,139,250,0.2)" data-tr="\u00c7oklu \u015eantiye" data-en="Multi-Site">\u00c7oklu \u015eantiye</span>
      </div>
      <div class="feature-card reveal" style="--c: #34d399">
        <div class="feature-icon">\U0001f4b9</div>
        <div class="feature-title" data-tr="Fiyat &amp; Stok Takibi" data-en="Price &amp; Stock Tracking">Fiyat &amp; Stok Takibi</div>
        <div class="feature-desc" data-tr="Demir, \u00e7imento, beton fiyatlar\u0131n\u0131 takip et. Stok d\u00fc\u015f\u00fcnce bildirim al, maliyetleri kontrol et." data-en="Track iron, cement, concrete prices. Get alerts when stock is low, control costs.">
          Demir, \u00e7imento, beton fiyatlar\u0131n\u0131 takip et. Stok d\u00fc\u015f\u00fcnce bildirim al, maliyetleri kontrol et.
        </div>
        <span class="feature-tag" style="--bg:rgba(52,211,153,0.1);--tc:#34d399;--bc:rgba(52,211,153,0.2)" data-tr="Anl\u0131k Fiyatlar" data-en="Live Prices">Anl\u0131k Fiyatlar</span>
      </div>
      <div class="feature-card reveal" style="--c: #f472b6">
        <div class="feature-icon">\U0001f30d</div>
        <div class="feature-title" data-tr="Deprem Analizi" data-en="Earthquake Analysis">Deprem Analizi</div>
        <div class="feature-desc" data-tr="\u015eantiye konumuna g\u00f6re deprem risk analizi. AFAD verileri ve TBDY 2018 parametreleri ile." data-en="Earthquake risk analysis based on site location. With AFAD data and TBDY 2018 parameters.">
          \u015eantiye konumuna g\u00f6re deprem risk analizi. AFAD verileri ve TBDY 2018 parametreleri ile.
        </div>
        <span class="feature-tag" style="--bg:rgba(244,114,182,0.1);--tc:#f472b6;--bc:rgba(244,114,182,0.2)" data-tr="AFAD Entegre" data-en="AFAD Integrated">AFAD Entegre</span>
      </div>
      <div class="feature-card reveal" style="--c: var(--amber)">
        <div class="feature-icon">\U0001f4f1</div>
        <div class="feature-title" data-tr="Mobil Uygulama" data-en="Mobile App">Mobil Uygulama</div>
        <div class="feature-desc" data-tr="Sahada telefona y\u00fckle, internetsiz \u00e7al\u0131\u015f. iOS ve Android destekli PWA uygulama." data-en="Install on phone at site, works offline. PWA app with iOS and Android support.">
          Sahada telefona y\u00fckle, internetsiz \u00e7al\u0131\u015f. iOS ve Android destekli PWA uygulama.
        </div>
        <span class="feature-tag" style="--bg:rgba(249,115,22,0.1);--tc:#fb923c;--bc:rgba(249,115,22,0.2)" data-tr="iOS &amp; Android" data-en="iOS &amp; Android">iOS &amp; Android</span>
      </div>
    </div>
  </div>
</section>

<!-- HOW IT WORKS -->
<section class="how-section">
  <div class="section-inner">
    <div class="reveal">
      <div class="section-label" data-tr="Nas\u0131l \u00c7al\u0131\u015f\u0131r?" data-en="How it Works?">Nas\u0131l \u00c7al\u0131\u015f\u0131r?</div>
      <h2 class="section-title" data-tr="3 Ad\u0131mda<br>Ba\u015fla" data-en="Get Started<br>in 3 Steps">3 Ad\u0131mda<br>Ba\u015fla</h2>
    </div>
    <div class="steps">
      <div class="step reveal">
        <div class="step-num">1</div>
        <div class="step-content">
          <div class="step-title" data-tr="\u00dccretsiz hesap olu\u015ftur" data-en="Create a free account">\u00dccretsiz hesap olu\u015ftur</div>
          <div class="step-desc" data-tr="Email ile 30 saniyede kay\u0131t ol. Kredi kart\u0131 gerekmez. G\u00fcnde 20 AI sorgusu \u00fccretsiz." data-en="Sign up with email in 30 seconds. No credit card required. 20 free AI queries per day.">
            Email ile 30 saniyede kay\u0131t ol. Kredi kart\u0131 gerekmez. G\u00fcnde 20 AI sorgusu \u00fccretsiz.
          </div>
        </div>
      </div>
      <div class="step reveal">
        <div class="step-num">2</div>
        <div class="step-content">
          <div class="step-title" data-tr="\u015eantiyen\u0130 ekle" data-en="Add your construction site">\u015eantiyeni ekle</div>
          <div class="step-desc" data-tr="\u015eantiye ad\u0131, konum ve bilgileri gir. Harita \u00fczerinden deprem riski analiz edilsin." data-en="Enter site name, location and details. Let earthquake risk be analyzed on the map.">
            \u015eantiye ad\u0131, konum ve bilgileri gir. Harita \u00fczerinden deprem riski analiz edilsin.
          </div>
        </div>
      </div>
      <div class="step reveal">
        <div class="step-num">3</div>
        <div class="step-content">
          <div class="step-title" data-tr="AI\'y\u0131 \u00e7al\u0131\u015ft\u0131r" data-en="Run the AI">AI\'y\u0131 \u00e7al\u0131\u015ft\u0131r</div>
          <div class="step-desc" data-tr="Soru sor, foto\u011fraf y\u00fckle, rapor olu\u015ftur. T\u00fcm hesaplamalar T\u00fcrkiye standartlar\u0131na g\u00f6re." data-en="Ask questions, upload photos, generate reports. All calculations according to Turkish standards.">
            Soru sor, foto\u011fraf y\u00fckle, rapor olu\u015ftur. T\u00fcm hesaplamalar T\u00fcrkiye standartlar\u0131na g\u00f6re.
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- MEVZUAT -->
<section>
  <div class="section-inner">
    <div class="reveal">
      <div class="section-label" data-tr="T\u00fcrkiye Mevzuat\u0131" data-en="Turkish Regulations">T\u00fcrkiye Mevzuat\u0131</div>
      <h2 class="section-title" data-tr="Yerel Standartlara<br>Tam Uyum" data-en="Full Compliance with<br>Local Standards">Yerel Standartlara<br>Tam Uyum</h2>
      <p class="section-sub" data-tr="Yabanc\u0131 rakipler T\u00fcrkiye mevzuat\u0131n\u0131 bilmez. Biz burada do\u011fduk, buran\u0131n kurallar\u0131n\u0131 biliyoruz." data-en="Foreign competitors don\'t know Turkish regulations. We were born here, we know the rules.">
        Yabanc\u0131 rakipler T\u00fcrkiye mevzuat\u0131n\u0131 bilmez. Biz burada do\u011fduk, buran\u0131n kurallar\u0131n\u0131 biliyoruz.
      </p>
    </div>
    <div class="mevzuat-grid">
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">\U0001f4d0</div><div><div class="mevzuat-text">TBDY 2018</div><div class="mevzuat-sub" data-tr="T\u00fcrkiye Bina Deprem Y\u00f6netmeli\u011fi" data-en="Turkey Building Earthquake Code">T\u00fcrkiye Bina Deprem Y\u00f6netmeli\u011fi</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">\U0001f3db\ufe0f</div><div><div class="mevzuat-text">TS 500</div><div class="mevzuat-sub" data-tr="Betonarme Yap\u0131 Tasar\u0131m Kurallar\u0131" data-en="Reinforced Concrete Design Rules">Betonarme Yap\u0131 Tasar\u0131m Kurallar\u0131</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">\U0001f30d</div><div><div class="mevzuat-text">AFAD</div><div class="mevzuat-sub" data-tr="Deprem Tehlike Haritas\u0131 Entegrasyonu" data-en="Earthquake Hazard Map Integration">Deprem Tehlike Haritas\u0131 Entegrasyonu</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">\U0001f9ba</div><div><div class="mevzuat-text">\u0130SG</div><div class="mevzuat-sub" data-tr="\u0130\u015f Sa\u011fl\u0131\u011f\u0131 ve G\u00fcvenli\u011fi Standartlar\u0131" data-en="Occupational Health &amp; Safety Standards">\u0130\u015f Sa\u011fl\u0131\u011f\u0131 ve G\u00fcvenli\u011fi Standartlar\u0131</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">\U0001f4b0</div><div><div class="mevzuat-text">TL Fiyat</div><div class="mevzuat-sub" data-tr="G\u00fcncel T\u00fcrk Liras\u0131 Malzeme Fiyatlar\u0131" data-en="Current Turkish Lira Material Prices">G\u00fcncel T\u00fcrk Liras\u0131 Malzeme Fiyatlar\u0131</div></div></div>
      <div class="mevzuat-card reveal"><div class="mevzuat-icon">\U0001f5fa\ufe0f</div><div><div class="mevzuat-text">81 \u0130l</div><div class="mevzuat-sub" data-tr="T\u00fcm T\u00fcrkiye\'de Hava Durumu &amp; Risk" data-en="Weather &amp; Risk Across All Turkey">T\u00fcm T\u00fcrkiye\'de Hava Durumu &amp; Risk</div></div></div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-section">
  <div class="section-inner" style="text-align:center">
    <div class="reveal">
      <div class="section-label" data-tr="Hemen Ba\u015fla" data-en="Get Started">Hemen Ba\u015fla</div>
      <h2 class="section-title" data-tr="\u015eantiyeni<br><span style=\'color:var(--amber)\'> D\u00f6n\u00fc\u015ft\u00fcr</span>" data-en="Transform<br><span style=\'color:var(--amber)\'>Your Site</span>">\u015eantiyeni<br><span style="color:var(--amber)">D\u00f6n\u00fc\u015ft\u00fcr</span></h2>
      <p class="section-sub" style="margin:16px auto 40px; text-align:center"
         data-tr="\u00dccretsiz hesap a\u00e7, 5 dakikada \u015fantiyen\u0130 ekle. Kredi kart\u0131 gerekmez."
         data-en="Create a free account, add your site in 5 minutes. No credit card required.">
        \u00dccretsiz hesap a\u00e7, 5 dakikada \u015fantiyen\u0130 ekle. Kredi kart\u0131 gerekmez.
      </p>
      <a href="/app#register" class="btn-primary" style="font-size:17px;padding:16px 40px"
         data-tr="\U0001f680 \u00dccretsiz Ba\u015fla" data-en="\U0001f680 Start Free">\U0001f680 \u00dccretsiz Ba\u015fla</a>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-logo">Building<span>AI</span></div>
  <div class="footer-copy" data-tr="&copy; 2026 BuildingAI &middot; T\u00fcrkiye\'nin \u015eantiye AI Platformu" data-en="&copy; 2026 BuildingAI &middot; Turkey\'s Construction AI Platform">
    &copy; 2026 BuildingAI &middot; T\u00fcrkiye\'nin \u015eantiye AI Platformu
  </div>
</footer>

<script>
/* ============================================================
   LANGUAGE SWITCHER
   ============================================================ */
function setLang(lang) {
  document.querySelectorAll(\'[data-tr]\').forEach(el => {
    const t = el.getAttribute(\'data-\' + lang);
    if (t) el.innerHTML = t;
  });
  document.getElementById(\'btn-tr\').classList.toggle(\'active\', lang === \'tr\');
  document.getElementById(\'btn-en\').classList.toggle(\'active\', lang === \'en\');
  document.documentElement.lang = lang;
  localStorage.setItem(\'lang\', lang);
}
const savedLang = localStorage.getItem(\'lang\') || \'tr\';
if (savedLang === \'en\') setLang(\'en\');

/* ============================================================
   SCROLL REVEAL (for sections below hero)
   ============================================================ */
const revealObs = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) setTimeout(() => e.target.classList.add(\'visible\'), i * 80);
  });
}, { threshold: 0.1 });
document.querySelectorAll(\'.reveal\').forEach(el => revealObs.observe(el));

/* ============================================================
   429 TOAST NOTIFICATION
   ============================================================ */
const toastContainer = document.createElement(\'div\');
toastContainer.className = \'toast-container\';
document.body.appendChild(toastContainer);

function showRateLimitToast() {
  const t = document.createElement(\'div\');
  t.className = \'toast\';
  const lang = document.documentElement.lang || \'tr\';
  t.innerHTML = `
    <div class="toast-icon">\u23f3</div>
    <div>
      <div class="toast-title">${lang === \'en\' ? \'Too Many Requests (429)\' : \'\u00c7ok Fazla \u0130stek (429)\'}</div>
      <div class="toast-desc">${lang === \'en\' ? \'Please wait. The system is actively protected.\' : \'L\u00fctfen bekleyin. Sistem \u015fu an korunuyor.\'}</div>
    </div>`;
  toastContainer.appendChild(t);
  setTimeout(() => t.classList.add(\'show\'), 10);
  setTimeout(() => { t.classList.remove(\'show\'); setTimeout(() => t.remove(), 500); }, 5000);
}
const _fetch = window.fetch;
window.fetch = async (...a) => { const r = await _fetch(...a); if (r.status === 429) showRateLimitToast(); return r; };
const _XHR = window.XMLHttpRequest;
window.XMLHttpRequest = function() {
  const x = new _XHR();
  x.addEventListener(\'load\', () => { if (x.status === 429) showRateLimitToast(); });
  return x;
};

/* ============================================================
   PARTICLE CANVAS
   ============================================================ */
(function () {
  const canvas = document.getElementById(\'particleCanvas\');
  if (!canvas) return;
  const ctx = canvas.getContext(\'2d\');
  let W, H, pts = [];
  const N = 110;

  function resize() { W = canvas.width = canvas.offsetWidth; H = canvas.height = canvas.offsetHeight; }
  window.addEventListener(\'resize\', resize); resize();

  class P {
    constructor() { this.spawn(); }
    spawn() {
      this.x = Math.random() * W; this.y = Math.random() * H;
      this.r = Math.random() * 1.4 + 0.3;
      this.vx = (Math.random() - .5) * .3; this.vy = -Math.random() * .18 - .04;
      this.a = Math.random() * 0.45 + 0.1;
      this.life = Math.random() * 350 + 200; this.age = 0;
    }
    tick() {
      this.x += this.vx; this.y += this.vy; this.age++;
      if (this.age > this.life || this.x < -10 || this.x > W+10 || this.y < -10) this.spawn();
    }
    draw() {
      const f = 1 - this.age / this.life;
      ctx.beginPath(); ctx.arc(this.x, this.y, this.r, 0, Math.PI*2);
      ctx.fillStyle = `rgba(255,255,255,${this.a * f})`; ctx.fill();
    }
  }
  for (let i = 0; i < N; i++) pts.push(new P());

  function frame() {
    ctx.clearRect(0, 0, W, H);
    pts.forEach(p => { p.tick(); p.draw(); });
    for (let i = 0; i < pts.length; i++) {
      for (let j = i+1; j < pts.length; j++) {
        const dx = pts[i].x - pts[j].x, dy = pts[i].y - pts[j].y;
        const d = Math.sqrt(dx*dx + dy*dy);
        if (d < 95) { ctx.beginPath(); ctx.moveTo(pts[i].x, pts[i].y); ctx.lineTo(pts[j].x, pts[j].y); ctx.strokeStyle = `rgba(255,255,255,${0.025*(1-d/95)})`; ctx.stroke(); }
      }
    }
    requestAnimationFrame(frame);
  }
  frame();
})();

/* ============================================================
   GSAP INTRO + SCROLLTRIGGER PARALLAX
   ============================================================ */
window.addEventListener(\'load\', () => {
  gsap.registerPlugin(ScrollTrigger);

  // Hide initially
  gsap.set([\'#heroBadge\',\'#heroH1\',\'#heroSub\',\'#heroBtns\',\'#engCard\'], { opacity: 0, y: 44 });
  gsap.set(\'#craneArm\', { opacity: 0, rotation: -26 });

  // Staggered intro
  gsap.timeline({ defaults: { ease: \'power3.out\' } })
    .to(\'#heroBadge\', { opacity:1, y:0, duration:0.85, delay:0.25 })
    .to(\'#heroH1\',    { opacity:1, y:0, duration:1.2  }, \'-=0.45\')
    .to(\'#heroSub\',   { opacity:1, y:0, duration:0.9  }, \'-=0.7\')
    .to(\'#heroBtns\',  { opacity:1, y:0, duration:0.9  }, \'-=0.55\')
    .to(\'#engCard\',   { opacity:1, y:0, duration:1.0  }, \'-=0.5\')
    .to(\'#craneArm\',  { opacity:1, rotation:-8, duration:1.8, ease:\'power2.out\' }, \'-=1.4\');

  // Scroll-driven parallax
  const st = {
    trigger: \'#heroScene\', start: \'top top\', end: \'bottom top\', scrub: 1.6
  };
  gsap.to([\'#heroBadge\',\'#heroH1\'], { scrollTrigger: st, y: -130, opacity: 0, scale: 0.96 });
  gsap.to(\'#heroSub\',  { scrollTrigger: st, y: -90,  opacity: 0, delay: 0.05 });
  gsap.to(\'#heroBtns\', { scrollTrigger: st, y: -70,  opacity: 0, delay: 0.1  });
  gsap.to(\'#engCard\',  { scrollTrigger: st, y: -50,  opacity: 0, delay: 0.15 });
  gsap.to(\'#craneLayer\', { scrollTrigger: st, y: -90 });
  gsap.to(\'#craneArm\', { scrollTrigger: st, rotation: 18, y: 220, opacity: 0.25 });
});
</script>
</body>
</html>
'''

with open('landing.html', 'w', encoding='utf-8') as f:
    f.write(landing_html)

print("DONE: Complete clean landing.html written successfully.")
