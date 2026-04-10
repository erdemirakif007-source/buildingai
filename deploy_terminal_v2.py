import re

with open("landing.html", "r", encoding="utf-8") as f:
    content = f.read()

# ═══════════════════════════════════════════════════════════════════════
# 1. NEW CSS — Terminal Industries Cinematic Construction Site
# ═══════════════════════════════════════════════════════════════════════
new_hero_css = r"""/* ── TERMINAL CINEMATIC HERO ── */
.hero-scene {
  position: relative;
  width: 100%;
  height: 100vh;
  min-height: 700px;
  background: #000;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Particle Canvas Layer */
#particleCanvas {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

/* SVG Wireframe Crane Layer (Far Background) */
.crane-layer {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  overflow: hidden;
}

.crane-svg {
  position: absolute;
  stroke: rgba(255,255,255,0.06);
  stroke-width: 1;
  fill: none;
}

.crane-1 { bottom: 0; left: 8%; width: 300px; height: 85vh; opacity: 0.5; }
.crane-2 { bottom: 0; right: 12%; width: 350px; height: 90vh; opacity: 0.35; }
.crane-3 { bottom: 0; left: 45%; width: 180px; height: 60vh; opacity: 0.2; }

/* Rotating Crane Arm (Middle Ground) */
.crane-arm-layer {
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
}

.crane-arm-pivot {
  position: absolute;
  top: 8%;
  left: 15%;
  width: 55vw;
  height: 4px;
  transform-origin: 0% 50%;
  transform: rotate(-8deg);
}
.crane-arm-pivot .arm-beam {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(249,115,22,0.5) 0%, rgba(249,115,22,0.1) 60%, transparent 100%);
  border-radius: 2px;
  box-shadow: 0 0 15px rgba(249,115,22,0.15);
}
.crane-arm-pivot .arm-cable {
  position: absolute;
  right: 30%;
  top: 4px;
  width: 1px;
  height: 25vh;
  background: linear-gradient(to bottom, rgba(255,255,255,0.15), rgba(255,255,255,0.03));
}
.crane-arm-pivot .arm-hook {
  position: absolute;
  right: calc(30% - 8px);
  top: calc(4px + 25vh);
  width: 16px;
  height: 16px;
  border: 2px solid rgba(249,115,22,0.4);
  border-radius: 0 0 8px 8px;
  border-top: none;
}

/* Foreground Content */
.hero-content {
  position: relative;
  z-index: 10;
  text-align: center;
  max-width: 1100px;
  width: 90%;
  padding: 0 20px;
}

.hero-badge-term {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: 'DM Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: #f97316;
  margin-bottom: 30px;
  opacity: 0;
}
.hero-badge-term .dot {
  width: 8px;
  height: 8px;
  background: #f97316;
  border-radius: 50%;
  box-shadow: 0 0 12px #f97316;
  animation: dotPulse 2s infinite;
}
@keyframes dotPulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.7)} }

.hero-content h1 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(56px, 10vw, 140px);
  line-height: 0.92;
  letter-spacing: 0.03em;
  color: #fff;
  margin-bottom: 28px;
  opacity: 0;
}
.hero-content h1 em {
  font-style: normal;
  color: #22d3ee;
}

.hero-subtitle {
  font-size: clamp(15px, 1.8vw, 20px);
  color: #94a3b8;
  max-width: 620px;
  margin: 0 auto 48px;
  line-height: 1.65;
  opacity: 0;
}

.hero-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 60px;
  opacity: 0;
}

.btn-fire {
  background: #f97316;
  color: #000 !important;
  font-weight: 700;
  font-size: 16px;
  padding: 16px 44px;
  border-radius: 8px;
  text-decoration: none;
  font-family: 'Instrument Sans', sans-serif;
  box-shadow: 0 0 30px rgba(249,115,22,0.4), 0 8px 20px rgba(0,0,0,0.4);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  border: none;
  cursor: pointer;
}
.btn-fire:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 0 50px rgba(249,115,22,0.6), 0 12px 30px rgba(0,0,0,0.5);
}

.btn-outline {
  background: transparent;
  color: #fff !important;
  font-weight: 500;
  font-size: 16px;
  padding: 16px 44px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.15);
  text-decoration: none;
  transition: all 0.3s;
  cursor: pointer;
}
.btn-outline:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.4);
  transform: translateY(-3px);
}

/* Engineering Data Strip */
.eng-strip {
  display: flex;
  justify-content: center;
  gap: 0;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  overflow: hidden;
  opacity: 0;
  max-width: 800px;
  margin: 0 auto;
}
.eng-cell {
  flex: 1;
  padding: 28px 16px;
  text-align: center;
  border-right: 1px solid rgba(255,255,255,0.06);
}
.eng-cell:last-child { border-right: none; }
.eng-val {
  font-family: 'DM Mono', monospace;
  font-size: clamp(24px, 3vw, 36px);
  font-weight: 500;
  color: #fff;
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.eng-label {
  font-size: 11px;
  color: #64748b;
  font-family: 'DM Mono', monospace;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-top: 8px;
  font-weight: 500;
}

/* Ambient Glow */
.hero-scene::after {
  content: '';
  position: absolute;
  bottom: -200px;
  left: 50%;
  transform: translateX(-50%);
  width: 120vw;
  height: 500px;
  background: radial-gradient(ellipse at center, rgba(249,115,22,0.08) 0%, transparent 70%);
  z-index: 0;
  pointer-events: none;
}

/* Seamless Bottom Gradient */
.hero-scene-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 200px;
  background: linear-gradient(to top, var(--navy) 0%, transparent 100%);
  z-index: 15;
  pointer-events: none;
}

/* ── TOAST NOTIFICATION ── */
.toast-container {
  position: fixed; bottom: 24px; right: 24px; z-index: 9999;
  display: flex; flex-direction: column; gap: 12px; pointer-events: none;
}
.toast {
  background: rgba(15, 23, 42, 0.92); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(244, 63, 94, 0.4); border-radius: 12px;
  padding: 16px 20px; min-width: 300px; max-width: 400px;
  box-shadow: 0 10px 30px rgba(244, 63, 94, 0.25);
  display: flex; align-items: flex-start; gap: 14px;
  transform: translateX(120%); opacity: 0; pointer-events: auto;
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-icon { font-size: 24px; line-height: 1; }
.toast-content { flex: 1; }
.toast-title { font-weight: 600; color: #fff; font-size: 15px; margin-bottom: 4px; font-family: 'Instrument Sans', sans-serif;}
.toast-desc { font-size: 13px; color: #cbd5e1; font-family: 'Instrument Sans', sans-serif; line-height: 1.4; }
.toast.show { transform: translateX(0); opacity: 1; }

/* Responsive */
@media (max-width: 768px) {
  .hero-scene { min-height: 100vh; }
  .crane-arm-pivot { display: none; }
  .crane-1, .crane-2 { opacity: 0.15; }
  .eng-strip { flex-wrap: wrap; }
  .eng-cell { min-width: 50%; border-bottom: 1px solid rgba(255,255,255,0.06); }
  .eng-cell:nth-child(2) { border-right: none; }
}
"""

# ═══════════════════════════════════════════════════════════════════════
# 2. NEW HTML — Layered Parallax Structure
# ═══════════════════════════════════════════════════════════════════════
new_hero_html = r"""<!-- HERO SCENE -->
<div class="hero-scene" id="heroScene">

  <!-- Layer 0: Canvas Particle Field -->
  <canvas id="particleCanvas"></canvas>

  <!-- Layer 1: Far Background SVG Wireframe Cranes -->
  <div class="crane-layer" id="craneLayer">
    <!-- Crane 1 (Left) -->
    <svg class="crane-svg crane-1" viewBox="0 0 300 600" preserveAspectRatio="xMidYMax meet">
      <line x1="140" y1="600" x2="140" y2="30"/>
      <line x1="160" y1="600" x2="160" y2="30"/>
      <line x1="140" y1="30" x2="160" y2="30"/>
      <!-- Cross bracing -->
      <line x1="140" y1="100" x2="160" y2="150"/>
      <line x1="160" y1="100" x2="140" y2="150"/>
      <line x1="140" y1="200" x2="160" y2="250"/>
      <line x1="160" y1="200" x2="140" y2="250"/>
      <line x1="140" y1="300" x2="160" y2="350"/>
      <line x1="160" y1="300" x2="140" y2="350"/>
      <line x1="140" y1="400" x2="160" y2="450"/>
      <line x1="160" y1="400" x2="140" y2="450"/>
      <!-- Jib arm -->
      <line x1="160" y1="35" x2="300" y2="50"/>
      <line x1="140" y1="30" x2="0" y2="60"/>
      <!-- Counter cables -->
      <line x1="148" y1="0" x2="300" y2="50" stroke-dasharray="4,4"/>
      <line x1="148" y1="0" x2="0" y2="60" stroke-dasharray="4,4"/>
      <!-- Base -->
      <line x1="110" y1="600" x2="190" y2="600"/>
      <line x1="120" y1="600" x2="140" y2="550"/>
      <line x1="180" y1="600" x2="160" y2="550"/>
    </svg>

    <!-- Crane 2 (Right) -->
    <svg class="crane-svg crane-2" viewBox="0 0 350 650" preserveAspectRatio="xMidYMax meet">
      <line x1="170" y1="650" x2="170" y2="40"/>
      <line x1="190" y1="650" x2="190" y2="40"/>
      <line x1="170" y1="40" x2="190" y2="40"/>
      <line x1="170" y1="120" x2="190" y2="180"/>
      <line x1="190" y1="120" x2="170" y2="180"/>
      <line x1="170" y1="240" x2="190" y2="300"/>
      <line x1="190" y1="240" x2="170" y2="300"/>
      <line x1="170" y1="360" x2="190" y2="420"/>
      <line x1="190" y1="360" x2="170" y2="420"/>
      <line x1="190" y1="45" x2="350" y2="65"/>
      <line x1="170" y1="40" x2="10" y2="70"/>
      <line x1="178" y1="5" x2="350" y2="65" stroke-dasharray="5,5"/>
      <line x1="178" y1="5" x2="10" y2="70" stroke-dasharray="5,5"/>
      <line x1="140" y1="650" x2="220" y2="650"/>
      <line x1="148" y1="650" x2="170" y2="590"/>
      <line x1="212" y1="650" x2="190" y2="590"/>
    </svg>

    <!-- Crane 3 (Center-far) -->
    <svg class="crane-svg crane-3" viewBox="0 0 180 500" preserveAspectRatio="xMidYMax meet">
      <line x1="85" y1="500" x2="85" y2="60"/>
      <line x1="95" y1="500" x2="95" y2="60"/>
      <line x1="85" y1="60" x2="95" y2="60"/>
      <line x1="85" y1="120" x2="95" y2="170"/>
      <line x1="95" y1="120" x2="85" y2="170"/>
      <line x1="85" y1="250" x2="95" y2="300"/>
      <line x1="95" y1="250" x2="85" y2="300"/>
      <line x1="95" y1="63" x2="180" y2="78"/>
      <line x1="85" y1="60" x2="0" y2="80"/>
    </svg>
  </div>

  <!-- Layer 2: Animated Crane Arm (Mid-ground) -->
  <div class="crane-arm-layer" id="craneArmLayer">
    <div class="crane-arm-pivot" id="craneArm">
      <div class="arm-beam"></div>
      <div class="arm-cable"></div>
      <div class="arm-hook"></div>
    </div>
  </div>

  <!-- Layer 3: Foreground Typography & Data -->
  <div class="hero-content" id="heroContent">
    <div class="hero-badge-term" id="heroBadge" data-tr="🇹🇷 Türkiye'nin İlk Yapay Zeka Destekli Şantiye Platformu" data-en="🇹🇷 Turkey's First AI-Powered Construction Platform">
      <span class="dot"></span>
      🇹🇷 Türkiye'nin İlk Yapay Zeka Destekli Şantiye Platformu
    </div>

    <h1 id="heroH1">
      <span data-tr="Şantiyeni" data-en="Manage Your">Şantiyeni</span> <em data-tr="Yapay Zeka" data-en="with AI">Yapay Zeka</em><br>
      <span data-tr="ile Yönet" data-en="Construction">ile Yönet</span>
    </h1>

    <p class="hero-subtitle" id="heroSub" data-tr="Kamera analizi, AI raporlama, fiyat takibi ve Türkiye mevzuatına uygun hesaplamalar. Saha mühendisleri ve müteahhitler için tasarlandı." data-en="Camera analysis, AI reporting, price tracking and calculations compliant with Turkish regulations. Designed for field engineers and contractors.">
      Kamera analizi, AI raporlama, fiyat takibi ve Türkiye mevzuatına uygun hesaplamalar. Saha mühendisleri ve müteahhitler için tasarlandı.
    </p>

    <div class="hero-actions" id="heroActions">
      <a href="/app#register" class="btn-fire" data-tr="🚀 Ücretsiz Başla" data-en="🚀 Start Free">🚀 Ücretsiz Başla</a>
      <a href="#features" class="btn-outline" data-tr="Özellikleri Gör" data-en="See Features">Özellikleri Gör</a>
    </div>

    <div class="eng-strip" id="engStrip">
      <div class="eng-cell">
        <div class="eng-val">50+</div>
        <div class="eng-label" data-tr="Mühendislik Hesabı" data-en="Eng. Calculations">Mühendislik Hesabı</div>
      </div>
      <div class="eng-cell">
        <div class="eng-val">7/24</div>
        <div class="eng-label" data-tr="AI Asistan" data-en="AI Assistant">AI Asistan</div>
      </div>
      <div class="eng-cell">
        <div class="eng-val">TBDY 2018</div>
        <div class="eng-label" data-tr="Tam Uyumlu" data-en="Fully Compliant">Tam Uyumlu</div>
      </div>
      <div class="eng-cell">
        <div class="eng-val">₺</div>
        <div class="eng-label" data-tr="Yerel Fiyat" data-en="Local Pricing">Yerel Fiyat</div>
      </div>
    </div>
  </div>

  <!-- Seamless bottom gradient -->
  <div class="hero-scene-fade"></div>
</div>"""

# ═══════════════════════════════════════════════════════════════════════
# 3. GSAP + Canvas Particle System + ScrollTrigger
# ═══════════════════════════════════════════════════════════════════════
gsap_and_particles = r"""
<!-- GSAP & ScrollTrigger -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
// ── Particle Field (Terminal Industries style) ──
(function() {
  const canvas = document.getElementById('particleCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let w, h, particles = [];
  const PARTICLE_COUNT = 120;

  function resize() {
    w = canvas.width = canvas.offsetWidth;
    h = canvas.height = canvas.offsetHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * w;
      this.y = Math.random() * h;
      this.r = Math.random() * 1.5 + 0.3;
      this.vx = (Math.random() - 0.5) * 0.3;
      this.vy = (Math.random() - 0.5) * 0.15 - 0.1;
      this.alpha = Math.random() * 0.5 + 0.1;
      this.life = Math.random() * 400 + 200;
      this.age = 0;
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.age++;
      if (this.age > this.life || this.x < -10 || this.x > w+10 || this.y < -10 || this.y > h+10) this.reset();
    }
    draw() {
      const fade = 1 - (this.age / this.life);
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${this.alpha * fade})`;
      ctx.fill();
    }
  }

  for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());

  function animate() {
    ctx.clearRect(0, 0, w, h);
    particles.forEach(p => { p.update(); p.draw(); });

    // Draw faint connecting lines for nearby particles
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        if (dist < 100) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(255, 255, 255, ${0.03 * (1 - dist/100)})`;
          ctx.stroke();
        }
      }
    }
    requestAnimationFrame(animate);
  }
  animate();
})();

// ── GSAP Animations ──
document.addEventListener('DOMContentLoaded', () => {
  gsap.registerPlugin(ScrollTrigger);

  // ── INTRO STAGGERED TIMELINE ──
  const intro = gsap.timeline({ defaults: { ease: "power3.out" }});
  intro
    .to("#heroBadge", { opacity: 1, y: 0, duration: 0.8, delay: 0.3 })
    .fromTo("#heroH1", { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 1.2 }, "-=0.4")
    .fromTo("#heroSub", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9 }, "-=0.7")
    .fromTo("#heroActions", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.9 }, "-=0.5")
    .fromTo("#engStrip", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 1 }, "-=0.5")
    .fromTo("#craneArm", { rotation: -25, opacity: 0 }, { rotation: -8, opacity: 1, duration: 2, ease: "power2.out" }, "-=1.5");

  // ── SCROLL-DRIVEN PARALLAX ──
  const scrollTL = gsap.timeline({
    scrollTrigger: {
      trigger: "#heroScene",
      start: "top top",
      end: "bottom top",
      scrub: 1.5,
      pin: false
    }
  });

  scrollTL
    .to("#heroH1", { y: -120, opacity: 0, scale: 0.97 }, 0)
    .to("#heroSub", { y: -80, opacity: 0 }, 0.05)
    .to("#heroActions", { y: -60, opacity: 0 }, 0.1)
    .to("#engStrip", { y: -40, opacity: 0 }, 0.15)
    .to("#heroBadge", { y: -100, opacity: 0 }, 0)
    .to("#craneLayer", { y: -80 }, 0)
    .to("#craneArm", { rotation: 15, y: 200, opacity: 0.3 }, 0);
});
</script>
</body>"""

# ═══════════════════════════════════════════════════════════════════════
# APPLY REPLACEMENTS
# ═══════════════════════════════════════════════════════════════════════

# 1. Replace CSS block
content = re.sub(
    r"/\* ── CINEMATIC Gece Şantiyesi.*?/\* ── SECTION BASE ── \*/",
    new_hero_css + "\n\n/* ── SECTION BASE ── */",
    content, flags=re.DOTALL
)

# 2. Replace HTML Hero block
content = re.sub(
    r"<!-- HERO WRAPPER FOR SCROLL ANIMATIONS -->.*?</div>\s*\n\s*\n\s*<!-- FEATURES -->",
    new_hero_html + "\n\n<!-- FEATURES -->",
    content, flags=re.DOTALL
)

# 3. Remove old GSAP scripts (from previous iteration)
content = re.sub(
    r"\n<!-- GSAP & ScrollTrigger -->.*?</script>\s*\n</body>",
    gsap_and_particles,
    content, flags=re.DOTALL
)

# 4. Remove old responsive rules for hero (from older iterations)
content = content.replace(
    "  .hero h1 { font-size: 52px; }\n  .hero-stats { gap: 24px; }\n",
    ""
)

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(content)

print("DONE: Terminal Industries Cinematic Hero v2 deployed successfully!")
