import re

with open("landing.html", "r", encoding="utf-8") as f:
    content = f.read()

new_css = """/* ── PREMIUM HERO AESTHETICS ── */
:root {
  --hero-bg: transparent;
  --orb-1: rgba(139, 92, 246, 0.3);
  --orb-2: rgba(34, 211, 238, 0.25);
  --orb-3: rgba(236, 72, 153, 0.2);
  --glass-bg: rgba(255, 255, 255, 0.04);
  --glass-border-top: rgba(255, 255, 255, 0.15);
  --glass-border-bot: rgba(255, 255, 255, 0.02);
  --hero-text: #f0f4ff;
  --hero-text-glow: linear-gradient(135deg, #ffffff, #a5b4fc);
  --hero-sub-text: #94a3b8;
  --stat-bg: linear-gradient(180deg, rgba(255, 255, 255, 0.03) 0%, transparent 100%);
  --stat-border: rgba(255, 255, 255, 0.06);
}

@media (prefers-color-scheme: light) {
  :root {
    --hero-bg: rgba(248, 250, 252, 1);
    --orb-1: rgba(139, 92, 246, 0.4);
    --orb-2: rgba(34, 211, 238, 0.35);
    --orb-3: rgba(236, 72, 153, 0.3);
    --glass-bg: rgba(255, 255, 255, 0.6);
    --glass-border-top: rgba(255, 255, 255, 0.8);
    --glass-border-bot: rgba(0, 0, 0, 0.05);
    --hero-text: #1e293b;
    --hero-text-glow: linear-gradient(135deg, #1e293b, #4f46e5);
    --hero-sub-text: #475569;
    --stat-bg: linear-gradient(180deg, rgba(0, 0, 0, 0.02) 0%, transparent 100%);
    --stat-border: rgba(0, 0, 0, 0.08);
  }
}

.hero {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  flex-direction: column; text-align: center;
  padding: 130px 5% 90px;
  position: relative; z-index: 1;
  overflow: hidden;
  background: var(--hero-bg);
  transition: background 0.5s ease;
}

/* Antigravity Fluid Background Orbs */
.hero::before, .hero::after, .hero-orb-3 {
  content: ''; position: absolute; border-radius: 50%; filter: blur(90px); z-index: -1;
  animation: antigravityFlow 25s infinite alternate cubic-bezier(0.45, 0.05, 0.55, 0.95);
  opacity: 0.7;
}
.hero::before { width: 45vw; height: 45vw; background: var(--orb-1); top: -10%; left: -5%; }
.hero::after { width: 40vw; height: 40vw; background: var(--orb-2); bottom: -15%; right: -10%; animation-delay: -7s; }
.hero-orb-3 { 
  position: absolute; width: 35vw; height: 35vw; background: var(--orb-3); 
  top: 30%; left: 30%; animation: antigravityFlow 20s infinite alternate-reverse ease-in-out; filter: blur(100px); z-index: -1;
}

@keyframes antigravityFlow {
  0% { transform: translate(0, 0) rotate(0deg) scale(1); }
  33% { transform: translate(15%, 10%) rotate(45deg) scale(1.1); }
  66% { transform: translate(-10%, 20%) rotate(90deg) scale(0.9); }
  100% { transform: translate(-5%, -15%) rotate(135deg) scale(1.05); }
}

/* Premium Glassmorphism Card */
.hero-glass {
  background: var(--glass-bg);
  backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px);
  border-top: 1px solid var(--glass-border-top);
  border-left: 1px solid var(--glass-border-top);
  border-right: 1px solid var(--glass-border-bot);
  border-bottom: 1px solid var(--glass-border-bot);
  border-radius: 36px;
  padding: 70px 50px 0; max-width: 1040px; width: 100%;
  box-shadow: 
    0 40px 80px -20px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.15),
    inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  margin: 0 auto;
  opacity: 0; transform: translateY(40px);
  animation: slideUpGlass 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes slideUpGlass { to { transform: translateY(0); opacity: 1; } }

/* Staggered Content Animations */
.hero-glass > *:not(.hero-stats) {
  opacity: 0; transform: translateY(20px);
  animation: stggerFloat 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.hero-glass .hero-badge { animation-delay: 0.2s; }
.hero-glass h1 { animation-delay: 0.4s; }
.hero-glass .hero-sub { animation-delay: 0.6s; }
.hero-glass .hero-btns { animation-delay: 0.8s; }
.hero-glass .hero-stats { 
  opacity: 0; transform: translateY(20px);
  animation: stggerFloat 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  animation-delay: 1.0s; 
}

@keyframes stggerFloat { to { opacity: 1; transform: translateY(0); } }

/* Badge */
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px; padding: 6px 16px;
  font-family: 'DM Mono', monospace; font-size: 11px; letter-spacing: .12em;
  color: var(--hero-text); text-transform: uppercase; margin-bottom: 24px;
}
@media (prefers-color-scheme: light) { .hero-badge { background: rgba(0,0,0,0.03); border-color: rgba(0,0,0,0.08); } }
.hero-badge::before {
  content: ''; width: 6px; height: 6px; border-radius: 50%;
  background: var(--hero-text); box-shadow: 0 0 8px var(--hero-text); animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

/* Typography */
.hero h1 {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(52px, 9vw, 100px);
  letter-spacing: .02em; line-height: 1.05;
  margin-bottom: 24px;
  background: var(--hero-text-glow);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text; color: var(--hero-text);
  text-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
.hero h1 em { color: var(--cyan); font-style: normal; -webkit-text-fill-color: var(--cyan); }

.hero-sub {
  font-size: clamp(16px, 2vw, 19px); color: var(--hero-sub-text); max-width: 640px;
  line-height: 1.7; margin: 0 auto 40px; font-weight: 400;
}

/* Buttons */
.hero-btns { display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; margin-bottom: 60px; }

.btn-gemini {
  background: linear-gradient(135deg, #1e293b, #0f172a); border: 1px solid rgba(255,255,255,0.15);
  color: #fff !important; font-weight: 500; font-size: 15px; font-family: 'Instrument Sans', sans-serif;
  padding: 15px 36px; border-radius: 12px; cursor: pointer;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.1);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  text-decoration: none; display: inline-flex; align-items: center; gap: 10px;
}
@media (prefers-color-scheme: light) {
  .btn-gemini { background: linear-gradient(135deg, #f8fafc, #e2e8f0); color: #0f172a !important; border-color: rgba(0,0,0,0.1); box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
}
.btn-gemini:hover { transform: translateY(-4px); box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25); }

.btn-glass {
  background: rgba(255, 255, 255, 0.03); color: var(--hero-text) !important; font-weight: 500; font-size: 15px;
  padding: 15px 36px; border-radius: 12px; border: 1px solid var(--glass-border-bot); cursor: pointer;
  transition: all 0.4s; text-decoration: none;
}
.btn-glass:hover { background: rgba(255,255,255,0.08); transform: translateY(-4px); }

/* Engineering Data Hierarchy */
.hero-stats {
  display: flex; flex-wrap: wrap; justify-content: center;
  padding: 50px 20px; 
  background: var(--stat-bg);
  border-top: 1px solid var(--stat-border);
  border-radius: 0 0 36px 36px;
  margin-left: -50px; margin-right: -50px; box-shadow: inset 0 20px 40px -20px rgba(0,0,0,0.05);
}
.stat-item { text-align: center; flex: 1; min-width: 140px; position: relative; }
.stat-item:not(:last-child)::after {
  content: ''; position: absolute; right: 0; top: 15%; height: 70%; width: 1px;
  background: var(--stat-border);
}
.stat-num {
  font-family: 'DM Mono', monospace; font-size: clamp(32px, 4vw, 40px); font-weight: 500; letter-spacing: -0.04em;
  background: var(--hero-text-glow); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; line-height: 1.1;
  text-shadow: 0 4px 12px rgba(255,255,255,0.05);
}
.stat-lbl { 
  font-size: 13px; color: var(--hero-sub-text); margin-top: 8px; font-family: 'Instrument Sans', sans-serif; 
  letter-spacing: 0.04em; text-transform: uppercase; font-weight: 600;
}

@media (max-width: 768px) {
  .hero-glass { padding: 50px 20px 0; }
  .hero-stats { margin-left: -20px; margin-right: -20px; padding: 30px 10px; }
  .stat-item:not(:last-child)::after { display: none; }
  .stat-item { min-width: 45%; margin-bottom: 20px; }
}

/* ── TOAST NOTIFICATION ── */
.toast-container {
  position: fixed; bottom: 24px; right: 24px; z-index: 9999;
  display: flex; flex-direction: column; gap: 12px; pointer-events: none;
}
.toast {
  background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
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
.toast.show { transform: translateX(0); opacity: 1; }"""

new_html = """<!-- HERO -->
<section class="hero">
  <div class="hero-orb-3"></div>
  <div class="hero-glass">
    <div class="hero-badge" data-tr="🇹🇷 Türkiye'nin Şantiye AI Platformu" data-en="🇹🇷 Turkey's Construction AI Platform">
      🇹🇷 Türkiye'nin Şantiye AI Platformu
    </div>

    <h1>
      <span data-tr="Şantiyeni" data-en="Manage Your">Şantiyeni</span> <em data-tr="Yapay Zeka" data-en="with AI">Yapay Zeka</em><br>
      <span data-tr="ile Yönet" data-en="Construction">ile Yönet</span>
    </h1>

    <p class="hero-sub" data-tr="Kamera analizi, AI raporlama, fiyat takibi ve Türkiye mevzuatına uygun hesaplamalar. Saha mühendisleri ve müteahhitler için tasarlandı." data-en="Camera analysis, AI reporting, price tracking and calculations compliant with Turkish regulations. Designed for field engineers and contractors.">
      Kamera analizi, AI raporlama, fiyat takibi ve Türkiye mevzuatına uygun hesaplamalar. Saha mühendisleri ve müteahhitler için tasarlandı.
    </p>

    <div class="hero-btns">
      <a href="/app#register" class="btn-gemini" data-tr="✨ Ücretsiz Başla" data-en="✨ Start Free">✨ Ücretsiz Başla</a>
      <a href="#features" class="btn-glass" data-tr="Özellikleri Gör" data-en="See Features">Özellikleri Gör</a>
    </div>

    <div class="hero-stats">
      <div class="stat-item">
        <div class="stat-num">50+</div>
        <div class="stat-lbl" data-tr="Mühendislik Hesabı" data-en="Engineering Calculations">Mühendislik Hesabı</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">7/24</div>
        <div class="stat-lbl" data-tr="AI Asistan" data-en="AI Assistant">AI Asistan</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">TBDY 2018</div>
        <div class="stat-lbl" data-tr="Tam Uyumlu" data-en="Fully Compliant">Tam Uyumlu</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">TR</div>
        <div class="stat-lbl" data-tr="Yerel Fiyatlandırma" data-en="Local Pricing">Yerel Fiyatlandırma</div>
      </div>
    </div>
  </div>
</section>"""

# Replace CSS
content = re.sub(r"/\* ── HERO ── \*/.*?\.toast\.show \{ transform: translateX\(0\); opacity: 1; \}", new_css, content, flags=re.DOTALL)

# Replace HTML
content = re.sub(r"<!-- HERO -->.*?</section>", new_html, content, flags=re.DOTALL)

with open("landing.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated landing.html with Premium Glassmorphism")
