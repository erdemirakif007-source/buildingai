import re

with open("landing.html", "r", encoding="utf-8") as f:
    content = f.read()

new_css = """/* ── CINEMATIC Gece Şantiyesi (Terminal Industries Vibe) ── */
:root {
  --term-bg: #030712;
  --term-grid: rgba(255, 255, 255, 0.02);
  --term-accent: #f97316;
  --term-cyan: #22d3ee;
  --term-text-main: #f8fafc;
  --term-text-muted: #94a3b8;
}

body {
  background-color: var(--term-bg);
  color: var(--term-text-main);
  overflow-x: hidden;
}

.hero-wrapper {
  position: relative;
  width: 100%;
  height: 150vh;
  background: var(--term-bg);
  overflow: hidden;
}

.hero-wrapper::before {
  content: ''; position: absolute; inset: 0;
  background-image: linear-gradient(var(--term-grid) 1px, transparent 1px), linear-gradient(90deg, var(--term-grid) 1px, transparent 1px);
  background-size: 50px 50px; opacity: 0.5;
  pointer-events: none;
}

.parallax-layer-1 {
  position: absolute; top: 0; left: 0; width: 100%; height: 120%;
  background: radial-gradient(circle at 50% 30%, rgba(34, 211, 238, 0.05) 0%, transparent 60%),
              linear-gradient(to bottom, #030712, #020617);
  z-index: 1;
}
.crane-bg-1, .crane-bg-2 { position: absolute; bottom: 10%; background: #0f172a; }
.crane-bg-1 { width: 4px; height: 40vh; left: 20%; opacity: 0.4; }
.crane-bg-1::after { content:''; position:absolute; top: 10px; width: 150px; height: 4px; background: #0f172a; transform-origin: left; transform: rotate(-15deg); }
.crane-bg-2 { width: 6px; height: 50vh; right: 25%; opacity: 0.3; }
.crane-bg-2::after { content:''; position:absolute; top: 20px; right: 0; width: 200px; height: 6px; background: #0f172a; transform-origin: right; transform: rotate(10deg); }

.parallax-layer-2 {
  position: absolute; top: -10%; right: -5%; width: 40vw; height: 80vh;
  z-index: 2; opacity: 0.8;
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(0,0,0,0.8) 100%);
  border-left: 2px solid var(--term-accent);
  border-bottom: 2px solid rgba(249,115,22,0.3);
  transform-origin: top right;
  clip-path: polygon(100% 0, 100% 100%, 20% 90%, 0 50%, 60% 0);
  box-shadow: -20px 20px 50px rgba(0,0,0,0.8);
}

@media (max-width: 768px) {
  .parallax-layer-2 { width: 80vw; height: 50vh; right: -20%; }
}

.parallax-layer-3 {
  position: relative; z-index: 10;
  display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
  padding-top: 20vh;
  width: 100%; height: 100%;
}

.hero-main-title { text-align: center; margin-bottom: 50px; }
.hero-main-title h1 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(60px, 10vw, 130px);
  line-height: 0.9; letter-spacing: 0.02em;
  background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  text-shadow: 0 20px 40px rgba(0,0,0,0.8);
  margin-bottom: 20px; color: #fff;
}
.hero-main-title h1 em { color: var(--term-cyan); font-style: normal; -webkit-text-fill-color: var(--term-cyan); }
.hero-main-title p {
  color: var(--term-text-muted); font-size: clamp(16px, 2vw, 20px);
  max-width: 600px; margin: 0 auto; line-height: 1.6;
}

.terminal-glass-card {
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 20px; padding: 40px;
  width: 90%; max-width: 900px;
  box-shadow: 0 30px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
}

.hero-btns { display: flex; gap: 20px; justify-content: center; margin-bottom: 40px; flex-wrap: wrap;}
.btn-terminal {
  background: var(--term-accent); color: #000 !important;
  font-weight: 700; padding: 16px 40px; border-radius: 8px; text-decoration: none;
  font-family: 'Instrument Sans', sans-serif; transition: all 0.3s;
  box-shadow: 0 0 20px rgba(249,115,22,0.4); font-size: 16px;
}
.btn-terminal:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(249,115,22,0.6); }
.btn-ghost {
  background: transparent; color: #fff !important; border: 1px solid rgba(255,255,255,0.2);
  font-weight: 500; padding: 16px 40px; border-radius: 8px; text-decoration: none;
  transition: all 0.3s; font-size: 16px;
}
.btn-ghost:hover { background: rgba(255,255,255,0.05); border-color: #fff; }

.engineering-data {
  display: flex; flex-wrap: wrap; justify-content: space-between;
  border-top: 1px solid rgba(255,255,255,0.05); padding-top: 30px;
}
.eng-item { text-align: center; flex: 1; min-width: 120px; margin-bottom: 15px; }
.eng-num { font-family: 'Bebas Neue', sans-serif; font-size: 40px; color: var(--term-cyan); line-height: 1; }
.eng-lbl { font-size: 13px; color: var(--term-text-muted); font-family: 'DM Mono', monospace; text-transform: uppercase; margin-top: 5px; letter-spacing: 0.05em; font-weight: 600; }

.hero-gradient-bottom {
  position: absolute; bottom: 0; left: 0; width: 100%; height: 250px;
  background: linear-gradient(to top, var(--navy) 0%, transparent 100%);
  z-index: 5;
}
"""

new_html = """<!-- HERO WRAPPER FOR SCROLL ANIMATIONS -->
<div class="hero-wrapper" id="heroWrapper">
  
  <!-- Layer 1: Far Background -->
  <div class="parallax-layer-1" id="layer1">
    <div class="crane-bg-1"></div>
    <div class="crane-bg-2"></div>
  </div>

  <!-- Layer 2: Middle Ground (Giant Arm) -->
  <div class="parallax-layer-2" id="layer2"></div>

  <!-- Layer 3: Foreground Typography -->
  <div class="parallax-layer-3" id="layer3">
    
    <div class="hero-main-title" id="heroTitle">
      <div style="font-family: 'DM Mono', monospace; color: var(--term-accent); font-size: 12px; letter-spacing: 0.15em; margin-bottom: 15px; text-transform: uppercase;" data-tr="🇹🇷 Türkiye'nin İlk Yapay Zeka Destekli Şantiye Platformu" data-en="🇹🇷 Turkey's First AI-Powered Construction Platform">🇹🇷 Türkiye'nin İlk Yapay Zeka Destekli Şantiye Platformu</div>
      <h1>
        <span data-tr="Şantiyeni" data-en="Manage Your">Şantiyeni</span> <em data-tr="Yapay Zeka" data-en="with AI">Yapay Zeka</em><br>
        <span data-tr="ile Yönet" data-en="Construction">ile Yönet</span>
      </h1>
      <p data-tr="Kamera analizi, AI raporlama, fiyat takibi ve Türkiye mevzuatına uygun hesaplamalar. Saha mühendisleri ve müteahhitler için tasarlandı." data-en="Camera analysis, AI reporting, price tracking and calculations compliant with Turkish regulations. Designed for field engineers and contractors.">
        Kamera analizi, AI raporlama, fiyat takibi ve Türkiye mevzuatına uygun hesaplamalar. Saha mühendisleri ve müteahhitler için tasarlandı.
      </p>
    </div>

    <div class="terminal-glass-card" id="heroCard">
      <div class="hero-btns">
        <a href="/app#register" class="btn-terminal" data-tr="🚀 Ücretsiz Başla" data-en="🚀 Start Free">🚀 Ücretsiz Başla</a>
        <a href="#features" class="btn-ghost" data-tr="Özellikleri Gör" data-en="See Features">Özellikleri Gör</a>
      </div>

      <div class="engineering-data">
        <div class="eng-item">
          <div class="eng-num">50+</div>
          <div class="eng-lbl" data-tr="Mühendislik Hesabı" data-en="Engineering Calculations">Mühendislik Hesabı</div>
        </div>
        <div class="eng-item">
          <div class="eng-num">7/24</div>
          <div class="eng-lbl" data-tr="AI Asistan" data-en="AI Assistant">AI Asistan</div>
        </div>
        <div class="eng-item">
          <div class="eng-num">TBDY 2018</div>
          <div class="eng-lbl" data-tr="Tam Uyumlu" data-en="Fully Compliant">Tam Uyumlu</div>
        </div>
        <div class="eng-item">
          <div class="eng-num">TR</div>
          <div class="eng-lbl" data-tr="Yerel Fiyatlandırma" data-en="Local Pricing">Yerel Fiyatlandırma</div>
        </div>
      </div>
    </div>
  </div>

  <div class="hero-gradient-bottom"></div>
</div>"""

gsap_scripts = """
<!-- GSAP & ScrollTrigger -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', () => {
    gsap.registerPlugin(ScrollTrigger);

    // Initial Load Cinematic Animations
    const tl = gsap.timeline();
    tl.fromTo("#heroTitle", {y: 60, opacity: 0}, {y: 0, opacity: 1, duration: 1.2, ease: "power3.out"})
      .fromTo("#heroCard", {y: 50, opacity: 0}, {y: 0, opacity: 1, duration: 1.2, ease: "power3.out"}, "-=0.8")
      .fromTo("#layer2", {rotation: 20, opacity: 0, x: 100}, {rotation: 0, opacity: 0.8, x: 0, duration: 1.8, ease: "power2.out"}, "-=1.2");

    // Scroll-Driven Parallax Timelines
    gsap.to("#heroTitle", {
      scrollTrigger: { trigger: "#heroWrapper", start: "top top", end: "bottom 40%", scrub: true },
      y: -150, opacity: 0.05, scale: 0.95
    });

    gsap.to("#heroCard", {
      scrollTrigger: { trigger: "#heroWrapper", start: "top top", end: "bottom 30%", scrub: true },
      y: -200, opacity: 0.3
    });

    gsap.to("#layer1", {
      scrollTrigger: { trigger: "#heroWrapper", start: "top top", end: "bottom top", scrub: 0.5 },
      y: -100
    });

    gsap.to("#layer2", {
      scrollTrigger: { trigger: "#heroWrapper", start: "top top", end: "bottom top", scrub: 1 },
      y: 300, rotation: -15, scale: 1.1
    });
  });
</script>
</body>"""

# Perform Replacements
# 1. Replace CSS
content = re.sub(r"/\* ── PREMIUM HERO AESTHETICS ── \*/.*?/\* ── SECTION BASE ── \*/", new_css + "\n\n/* ── SECTION BASE ── */", content, flags=re.DOTALL)

# 2. Replace HTML
content = re.sub(r"<!-- HERO -->.*?</section>", new_html, content, flags=re.DOTALL)

# 3. Inject GSAP
content = content.replace("</body>", gsap_scripts)

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Cinematic GSAP Parallax has been deployed successfully!")
