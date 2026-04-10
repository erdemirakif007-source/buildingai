from styles import CSS_STYLE
from scripts import JS_SCRIPT

NEW_HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="BuildingAI">
    <meta name="theme-color" content="#f97316">
    <link rel="manifest" href="/static/manifest.json">
    <link rel="apple-touch-icon" href="/static/logo_3d_baret.png">
    <link rel="icon" type="image/png" href="/static/logo_3d_baret.png">
    <link rel="shortcut icon" type="image/png" href="/static/logo_3d_baret.png">
    <title>BuildingAI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    {CSS_STYLE}
    <style>
        /* ---- PROFILE ---- */
        .profile-header {{ display: flex; align-items: center; gap: 20px; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.08); }}
        .profile-avatar {{ width: 70px; height: 70px; background: var(--amber); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; color: #000; flex-shrink: 0; }}
        .profile-badge {{ background: rgba(249,115,22,0.15); border: 1px solid rgba(249,115,22,0.3); color: var(--amber); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }}
        .profile-stat {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 15px; text-align: center; }}
        .profile-stat .stat-value {{ font-size: 1.8rem; font-weight: 800; color: var(--amber); }}
        .profile-stat .stat-label {{ font-size: 0.75rem; color: var(--text-secondary); margin-top: 4px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 25px; }}
    </style>
</head>
<body>
<div id="mobile-overlay" onclick="closeMobileMenu()"></div>

<!-- ===== PREMIUM AUTH OVERLAY ===== -->
<div id="auth-overlay">

  <!-- Background glows -->
  <div class="auth-glow-1" aria-hidden="true"></div>
  <div class="auth-glow-2" aria-hidden="true"></div>

  <!-- ── LEFT: Brand Panel ── -->
  <div class="auth-brand-panel">
    <div class="auth-logo">🏗️ Building<span>AI</span></div>

    <h2 class="auth-brand-h">Türkiye'nin<br>İnşaat Platformu</h2>
    <p class="auth-brand-sub">Saha mühendisleri ve müteahhitler için yapay zeka destekli tam kontrol. TBDY 2018 uyumlu, 7/24 aktif.</p>

    <div class="auth-brand-feats">
      <div class="auth-brand-feat">
        <div class="auth-feat-check">✓</div>
        <div class="auth-feat-text"><strong>AI Kamera Analizi</strong> — Çatlak, donatı ve kalıp tespiti</div>
      </div>
      <div class="auth-brand-feat">
        <div class="auth-feat-check">✓</div>
        <div class="auth-feat-text"><strong>TBDY 2018 Uyumlu</strong> — Otomatik hesap & raporlama</div>
      </div>
      <div class="auth-brand-feat">
        <div class="auth-feat-check">✓</div>
        <div class="auth-feat-text"><strong>Deprem Risk Analizi</strong> — AFAD verisiyle anlık sismik değerlendirme</div>
      </div>
      <div class="auth-brand-feat">
        <div class="auth-feat-check">✓</div>
        <div class="auth-feat-text"><strong>Maliyet & Stok Takibi</strong> — Canlı piyasa fiyatları</div>
      </div>
    </div>

    <div class="auth-brand-mini-stats">
      <div>
        <div class="auth-mini-stat-val amber">500+</div>
        <div class="auth-mini-stat-lbl">Aktif Mühendis</div>
      </div>
      <div>
        <div class="auth-mini-stat-val">12K+</div>
        <div class="auth-mini-stat-lbl">AI Analizi</div>
      </div>
      <div>
        <div class="auth-mini-stat-val">%98</div>
        <div class="auth-mini-stat-lbl">TBDY Uyumu</div>
      </div>
    </div>
  </div>

  <!-- ── RIGHT: Form Panel ── -->
  <div class="auth-form-panel">
    <!-- Mobile-only mini logo (hidden on desktop via CSS) -->
    <div class="auth-mobile-logo">🏗️ Building<span>AI</span></div>

    <div class="auth-card">

      <!-- Language toggle -->
      <div class="auth-lang-row">
        <button id="langBtn_tr" class="auth-lang-btn active-lang" onclick="dilDegistir('tr')">🇹🇷 TR</button>
        <button id="langBtn_en" class="auth-lang-btn" onclick="dilDegistir('en')">🇬🇧 EN</button>
      </div>

      <!-- LOGIN PANEL -->
      <div id="panel-login">
        <h2 id="loginTitleEl">Hoş Geldiniz</h2>
        <p class="auth-card-sub">BuildingAI hesabınıza giriş yapın.</p>
        <div class="auth-tabs">
          <button class="auth-tab tab-login active" onclick="switchPanel('login')">Giriş Yap</button>
          <button class="auth-tab tab-register" onclick="switchPanel('register')">Kayıt Ol</button>
        </div>

        <!-- Google Sign-In -->
        <button class="google-btn" onclick="googleGirisYap()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          Google ile Giriş Yap
        </button>
        <div class="auth-divider"><span>veya e-posta ile</span></div>

        <input type="email" id="loginEmail" class="auth-input" placeholder="E-posta adresi">
        <input type="password" id="loginPass" class="auth-input" placeholder="Şifre" style="margin-bottom:20px;">
        <button class="auth-btn" id="loginBtn" onclick="girisYap()">Şantiyeye Giriş Yap →</button>
        <div id="loginMsg" style="margin-top:12px;font-size:13px;text-align:center;min-height:20px;"></div>
        <div style="text-align:center;margin-top:14px;">
          <a class="auth-forgot-link" onclick="switchPanel('forgot')">Şifremi unuttum</a>
        </div>
      </div>

      <!-- REGISTER PANEL -->
      <div id="panel-register" style="display:none;">
        <h2>Hesap Oluştur</h2>
        <p class="auth-card-sub">Ücretsiz başla, istediğin zaman yükselt.</p>
        <div class="auth-tabs">
          <button class="auth-tab tab-login" onclick="switchPanel('login')">Giriş Yap</button>
          <button class="auth-tab tab-register active" onclick="switchPanel('register')">Kayıt Ol</button>
        </div>

        <!-- Google Register -->
        <button class="google-btn" onclick="googleGirisYap()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          Google ile Kayıt Ol
        </button>
        <div class="auth-divider"><span>veya e-posta ile</span></div>

        <input type="text"     id="regName"        class="auth-input" placeholder="Ad Soyad">
        <input type="text"     id="regCompany"     class="auth-input" placeholder="Şirket / Proje (opsiyonel)">
        <input type="email"    id="regEmail"       class="auth-input" placeholder="E-posta adresi">
        <input type="password" id="regPass"        class="auth-input" placeholder="Şifre (min. 8 karakter)">
        <input type="password" id="regPassConfirm" class="auth-input" placeholder="Şifreyi tekrarla">

        <!-- Premium Plan Chips -->
        <div class="plan-section-label">Plan Seçin</div>
        <div class="plan-chips" id="planChips">
          <div class="plan-chip selected" id="plan-free" onclick="selectPlan('free')" role="radio" aria-checked="true">
            <div class="plan-chip-radio"></div>
            <div class="plan-chip-body">
              <div class="plan-chip-name">Ücretsiz</div>
              <div class="plan-chip-desc">10 AI sorgu/gün · 50+ hesaplama · 10 arşiv</div>
            </div>
            <div class="plan-chip-price">₺0<span>/ay</span></div>
          </div>
          <div class="plan-chip" id="plan-pro" onclick="selectPlan('pro')" role="radio" aria-checked="false">
            <div class="plan-chip-radio"></div>
            <div class="plan-chip-body">
              <div class="plan-chip-name">⚡ Pro <span class="plan-chip-badge">Popüler</span></div>
              <div class="plan-chip-desc">Sınırsız AI · 5 şantiye · Kamera & stok takibi</div>
            </div>
            <div class="plan-chip-price">₺650<span>/ay</span></div>
          </div>
          <div class="plan-chip" id="plan-max" onclick="selectPlan('max')" role="radio" aria-checked="false">
            <div class="plan-chip-radio"></div>
            <div class="plan-chip-body">
              <div class="plan-chip-name">👑 Max</div>
              <div class="plan-chip-desc">Her şey sınırsız · Haftalık rapor · Filigransız PDF</div>
            </div>
            <div class="plan-chip-price">₺1.990<span>/ay</span></div>
          </div>
        </div>

        <button class="auth-btn" id="regBtn" onclick="kayitOl()" style="margin-top:4px;">Hesabı Oluştur →</button>
        <div id="regMsg" style="margin-top:12px;font-size:13px;text-align:center;min-height:20px;"></div>
      </div>

      <!-- FORGOT PASSWORD PANEL -->
      <div id="panel-forgot" style="display:none;">
        <h2>🔑 Şifre Sıfırla</h2>
        <p class="auth-card-sub">E-posta adresinize 6 haneli sıfırlama kodu göndereceğiz.</p>
        <div id="forgot-step1">
          <input type="email" id="forgotEmail" class="auth-input" placeholder="E-posta adresi">
          <button class="auth-btn" id="forgotBtn" onclick="sifreSifirla()">Kod Gönder →</button>
          <div id="forgotMsg" style="margin-top:12px;font-size:13px;text-align:center;"></div>
        </div>
        <div id="forgot-step2" style="display:none;">
          <p style="color:#4ade80;font-size:13px;text-align:center;margin-bottom:16px;">✅ Kod gönderildi — e-postanızı kontrol edin.</p>
          <input type="text"     id="resetKod"          class="auth-input" placeholder="6 haneli kod" maxlength="6" style="text-align:center;letter-spacing:10px;font-size:1.5rem;font-weight:700;">
          <input type="password" id="resetYeniSifre"    class="auth-input" placeholder="Yeni şifre (min. 8 karakter)">
          <input type="password" id="resetYeniSifreTekrar" class="auth-input" placeholder="Yeni şifreyi tekrarla">
          <button class="auth-btn" onclick="sifreGuncelle()">Şifreyi Güncelle →</button>
          <div id="resetMsg" style="margin-top:12px;font-size:13px;text-align:center;"></div>
          <div style="text-align:center;margin-top:12px;">
            <a class="auth-link" style="font-size:12px;color:rgba(255,255,255,0.35);cursor:pointer;" onclick="document.getElementById('forgot-step1').style.display='block';document.getElementById('forgot-step2').style.display='none';">← Farklı e-posta dene</a>
          </div>
        </div>
        <div style="text-align:center;margin-top:16px;">
          <a class="auth-link" onclick="switchPanel('login')" style="font-size:13px;color:rgba(255,255,255,0.4);cursor:pointer;">← Giriş sayfasına dön</a>
        </div>
      </div>

    </div>
  </div>
</div>

<!-- ===== PROFILE MODAL ===== -->
<div id="profileModal" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.85); backdrop-filter:blur(10px); z-index:4000; align-items:center; justify-content:center;">
    <div style="background:rgba(8,16,32,0.97);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px); border:2px solid var(--primary); border-radius:28px; padding:35px; width:90%; max-width:480px; max-height:85vh; overflow-y:auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:25px;">
            <h2 style="color:var(--primary); margin:0;">👤 Profilim</h2>
            <button onclick="closeProfile()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">✖</button>
        </div>
        <div class="profile-header">
            <div class="profile-avatar" id="profileAvatar">E</div>
            <div>
                <div style="font-size:1.3rem; font-weight:800; color:white;" id="profileName">Erdem</div>
                <div style="color:#aaa; font-size:0.9rem;" id="profileEmail">erdem@mail.com</div>
                <div class="profile-badge" id="profilePlan" style="margin-top:8px;">ÜCRETSİZ PLAN</div>
            </div>
        </div>
        <div class="stats-grid">
            <div class="profile-stat"><div class="stat-value" id="statRapor">0</div><div class="stat-label">Rapor</div></div>
            <div class="profile-stat"><div class="stat-value" id="statSorgu">0</div><div class="stat-label">AI Sorgu</div></div>
            <div class="profile-stat"><div class="stat-value" id="statGun">0</div><div class="stat-label">Aktif Gün</div></div>
        </div>
        <hr class="divider">
        <div style="display:flex; gap:8px; margin-bottom:4px;">
            <button onclick="closeProfile(); odemePaneliAc('pro');" style="flex:1; padding:12px; background:linear-gradient(135deg,#6366f1,#818cf8); border:none; color:white; border-radius:14px; cursor:pointer; font-weight:700; font-size:0.9rem; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">⚡ PRO — 650 TL/ay</button>
            <button onclick="closeProfile(); odemePaneliAc('max');" style="flex:1; padding:12px; background:linear-gradient(135deg,#b7791f,#f1c40f); border:none; color:#111; border-radius:14px; cursor:pointer; font-weight:700; font-size:0.9rem; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">👑 MAX — 1.990 TL/ay</button>
        </div>
        <hr class="divider">
        <button onclick="closeProfile(); rolSifirla();" style="width:100%; padding:12px; background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.3); color:#818cf8; border-radius:14px; cursor:pointer; font-weight:700; margin-bottom:12px; transition:0.3s;" onmouseover="this.style.background='rgba(99,102,241,0.2)'" onmouseout="this.style.background='rgba(99,102,241,0.1)'">🔄 Rolümü Değiştir</button>
        <hr class="divider">
        <button onclick="cikisYap()" style="width:100%; padding:14px; background:rgba(231,76,60,0.15); border:1px solid #e74c3c; color:#e74c3c; border-radius:14px; cursor:pointer; font-weight:700; transition:0.3s;" onmouseover="this.style.background='rgba(231,76,60,0.3)'" onmouseout="this.style.background='rgba(231,76,60,0.15)'">🚪 Çıkış Yap</button>
    </div>
</div>

<!-- Compat: dummy elements for legacy JS -->
<div id="navSidebar" style="position:absolute; top:-9999px; left:-9999px; width:0; height:0; overflow:hidden;"></div>
<div id="topHeader" style="position:absolute; top:-9999px; left:-9999px; width:0; height:0; overflow:hidden;"></div>
<div id="sidebarOverlay" class="sidebar-overlay" style="display:none; pointer-events:none;" onclick="toggleSidebar()"></div>

<!-- Hidden legacy elements -->
<input type="text" id="soruInput" style="display:none" placeholder="Soru sor...">
<div id="navLinks" style="display:none;"></div>
<div id="historySidebar" style="display:none;"></div>
<div id="historyList" style="display:none;"></div>
<div id="weatherWidget" style="display:none;"></div>
<div id="planBadge" style="display:none;">FREE</div>
<span id="tbPageTitle" style="display:none;"></span>

<!-- ===== ANA UYGULAMA ===== -->
<div id="mainApp" style="display:none;">

    <!-- ROL SEÇİM EKRANI -->
    <div id="rolSecimEkrani" style="display:none; position:fixed; inset:0; background:var(--bg); z-index:6000; align-items:center; justify-content:center; flex-direction:column;">
      <div style="position:absolute; inset:0; background:radial-gradient(ellipse 80% 60% at 50% 0%, rgba(249,115,22,0.12) 0%, transparent 60%); pointer-events:none;"></div>
      <div style="position:relative; z-index:1; text-align:center; width:90%; max-width:700px;">
        <div style="margin-bottom:48px;">
          <div style="font-size:3rem; margin-bottom:16px;">🏗️</div>
          <h1 style="font-size:2rem; font-weight:900; letter-spacing:-1.5px; background:linear-gradient(135deg,var(--primary),#fb923c); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:10px;">BuildingAI Pro'ya Hoş Geldiniz</h1>
          <p style="color:var(--text-secondary); font-size:1rem;">Size en iyi deneyimi sunabilmek için kim olduğunuzu öğrenmek istiyoruz.</p>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:32px;">
          <div class="rol-kart" data-rol="muhendis" onclick="rolSecimYap('muhendis')" style="background:rgba(255,255,255,0.04); border:2px solid rgba(255,255,255,0.08); border-radius:24px; padding:36px 24px; cursor:pointer; transition:all 0.3s; text-align:center;"
            onmouseover="this.style.borderColor='rgba(249,115,22,0.4)'; this.style.background='rgba(249,115,22,0.06)'; this.style.transform='translateY(-4px)';"
            onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'; this.style.background='rgba(255,255,255,0.04)'; this.style.transform='translateY(0)';">
            <div style="font-size:3.5rem; margin-bottom:16px;">👷</div>
            <h3 style="color:white; font-size:1.2rem; font-weight:800; margin-bottom:8px;">Saha Mühendisiyim</h3>
            <p style="color:var(--text-secondary); font-size:0.85rem; line-height:1.6;">Teknik hesaplamalar, kamera analizi ve mühendislik raporları.</p>
            <div style="margin-top:20px; display:flex; flex-wrap:wrap; gap:6px; justify-content:center;">
              <span style="background:rgba(249,115,22,0.1); color:var(--primary); border:1px solid rgba(249,115,22,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Kamera Analizi</span>
              <span style="background:rgba(249,115,22,0.1); color:var(--primary); border:1px solid rgba(249,115,22,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Hesaplamalar</span>
              <span style="background:rgba(249,115,22,0.1); color:var(--primary); border:1px solid rgba(249,115,22,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Teknik Raporlar</span>
            </div>
          </div>
          <div class="rol-kart" data-rol="muteahhit" onclick="rolSecimYap('muteahhit')" style="background:rgba(255,255,255,0.04); border:2px solid rgba(255,255,255,0.08); border-radius:24px; padding:36px 24px; cursor:pointer; transition:all 0.3s; text-align:center;"
            onmouseover="this.style.borderColor='rgba(99,102,241,0.4)'; this.style.background='rgba(99,102,241,0.06)'; this.style.transform='translateY(-4px)';"
            onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'; this.style.background='rgba(255,255,255,0.04)'; this.style.transform='translateY(0)';">
            <div style="font-size:3.5rem; margin-bottom:16px;">🏗️</div>
            <h3 style="color:white; font-size:1.2rem; font-weight:800; margin-bottom:8px;">Müteahhit / Proje Yöneticisiyim</h3>
            <p style="color:var(--text-secondary); font-size:0.85rem; line-height:1.6;">Şantiye yönetimi, saha raporları ve proje takibi.</p>
            <div style="margin-top:20px; display:flex; flex-wrap:wrap; gap:6px; justify-content:center;">
              <span style="background:rgba(99,102,241,0.1); color:#818cf8; border:1px solid rgba(99,102,241,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Şantiye Takibi</span>
              <span style="background:rgba(99,102,241,0.1); color:#818cf8; border:1px solid rgba(99,102,241,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Günlük Rapor</span>
              <span style="background:rgba(99,102,241,0.1); color:#818cf8; border:1px solid rgba(99,102,241,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Saha Analizi</span>
            </div>
          </div>
        </div>
        <p style="color:var(--text-secondary); font-size:0.8rem;">Bu seçim daha sonra Profil'den değiştirilebilir.</p>
      </div>
    </div>

    <!-- ===== YENİ UYGULAMA KABUĞU ===== -->
    <div id="app" style="position:relative; z-index:1;">

      <!-- TOPBAR — TAM GENİŞLİK -->
      <div id="topbar">
        <button id="hamburger-btn" onclick="toggleMobileMenu()">
          <span></span><span></span><span></span>
        </button>
        <div class="tb-logo">
          <img src="/static/logo_3d_baret.png" style="width:38px; height:38px; object-fit:contain; filter: drop-shadow(0 0 6px rgba(249,115,22,0.4));">
          Building<em>AI</em>&nbsp;<span id="planLabel">Pro</span>
        </div>
        <div class="tb-right">
          <select id="citySelect" class="tb-city tb-hide-mobile" onchange="havaGuncelle()">
            <option value="Adana">Adana</option><option value="Adıyaman">Adıyaman</option>
            <option value="Afyonkarahisar">Afyonkarahisar</option><option value="Ağrı">Ağrı</option>
            <option value="Amasya">Amasya</option><option value="Ankara">Ankara</option>
            <option value="Antalya">Antalya</option><option value="Artvin">Artvin</option>
            <option value="Aydın">Aydın</option><option value="Balıkesir">Balıkesir</option>
            <option value="Bilecik">Bilecik</option><option value="Bingöl">Bingöl</option>
            <option value="Bitlis">Bitlis</option><option value="Bolu">Bolu</option>
            <option value="Burdur">Burdur</option><option value="Bursa">Bursa</option>
            <option value="Çanakkale">Çanakkale</option><option value="Çankırı">Çankırı</option>
            <option value="Çorum">Çorum</option><option value="Denizli">Denizli</option>
            <option value="Diyarbakır">Diyarbakır</option><option value="Edirne">Edirne</option>
            <option value="Elazığ">Elazığ</option><option value="Erzincan">Erzincan</option>
            <option value="Erzurum">Erzurum</option><option value="Eskişehir">Eskişehir</option>
            <option value="Gaziantep">Gaziantep</option><option value="Giresun">Giresun</option>
            <option value="Gümüşhane">Gümüşhane</option><option value="Hakkari">Hakkari</option>
            <option value="Hatay">Hatay</option><option value="Isparta">Isparta</option>
            <option value="Mersin">Mersin</option><option value="İstanbul">İstanbul</option>
            <option value="İzmir">İzmir</option><option value="Kars">Kars</option>
            <option value="Kastamonu">Kastamonu</option><option value="Kayseri">Kayseri</option>
            <option value="Kırklareli">Kırklareli</option><option value="Kırşehir">Kırşehir</option>
            <option value="Kocaeli">Kocaeli</option><option value="Konya">Konya</option>
            <option value="Kütahya">Kütahya</option><option value="Malatya">Malatya</option>
            <option value="Manisa">Manisa</option><option value="Kahramanmaraş">Kahramanmaraş</option>
            <option value="Mardin">Mardin</option><option value="Muğla">Muğla</option>
            <option value="Muş">Muş</option><option value="Nevşehir">Nevşehir</option>
            <option value="Niğde">Niğde</option><option value="Ordu">Ordu</option>
            <option value="Rize">Rize</option><option value="Sakarya">Sakarya</option>
            <option value="Samsun">Samsun</option><option value="Siirt">Siirt</option>
            <option value="Sinop">Sinop</option><option value="Sivas" selected>Sivas</option>
            <option value="Tekirdağ">Tekirdağ</option><option value="Tokat">Tokat</option>
            <option value="Trabzon">Trabzon</option><option value="Tunceli">Tunceli</option>
            <option value="Şanlıurfa">Şanlıurfa</option><option value="Uşak">Uşak</option>
            <option value="Van">Van</option><option value="Yozgat">Yozgat</option>
            <option value="Zonguldak">Zonguldak</option><option value="Aksaray">Aksaray</option>
            <option value="Bayburt">Bayburt</option><option value="Karaman">Karaman</option>
            <option value="Kırıkkale">Kırıkkale</option><option value="Batman">Batman</option>
            <option value="Şırnak">Şırnak</option><option value="Bartın">Bartın</option>
            <option value="Ardahan">Ardahan</option><option value="Iğdır">Iğdır</option>
            <option value="Yalova">Yalova</option><option value="Karabük">Karabük</option>
            <option value="Kilis">Kilis</option><option value="Osmaniye">Osmaniye</option>
            <option value="Düzce">Düzce</option>
          </select>
          <div class="tb-weather-block" id="weatherBlock" style="display:none">
            <span style="font-size:14px;">⛅</span>
            <span id="condition" class="tb-cond">Yükleniyor...</span>
            <span id="temp" class="tb-temp">--°C</span>
          </div>
          <div class="theme-toggle" id="themeToggle"></div>
          <div class="tb-avatar" onclick="openProfile()" id="avatarBtn">EA</div>
        </div>
      </div>

      <!-- BODY SATIRI: sidebar + içerik -->
      <div id="bodyRow">

        <!-- SOL SIDEBAR -->
        <div id="sidebar">
          <!-- Logo -->
          <div id="sidebarLogoBar">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
              <div style="width:32px;height:32px;background:linear-gradient(135deg,#F97316,#EA6010);border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 2px 8px rgba(249,115,22,0.35);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
              </div>
              <div>
                <div class="sb-brand">BuildingAI</div>
              </div>
            </div>
            <div class="sb-brand-sub">Şantiye Komuta Merkezi</div>
          </div>

          <!-- Nav -->
          <div style="flex:1;padding:8px 0;">
            <!-- Ana Panel -->
            <div class="nav-item active" id="nav-home" onclick="navGit('home')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
              Ana Panel
            </div>
            <!-- Şantiyelerim -->
            <div class="nav-item" id="nav-santiye" onclick="navGit('santiye')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
              Şantiyelerim
            </div>
            <!-- Stok Takibi -->
            <div class="nav-item" id="nav-stok" onclick="navGit('stok')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
              Stok Takibi
            </div>
            <!-- ISG & Güvenlik -->
            <div class="nav-item" id="nav-guvenlik" onclick="guvenlikAc()" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              ISG &amp; Güvenlik
            </div>
            <!-- Raporlar -->
            <div class="nav-item" id="nav-gunluk" onclick="navGit('gunluk')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
              Raporlar
            </div>
            <!-- Ayarlar -->
            <div class="nav-item" id="nav-ayarlar" onclick="sayfaGoster('ayarlar')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
              Ayarlar
            </div>

            <!-- Divider + ekstra nav -->
            <div style="height:1px;background:#1E293B;margin:10px 16px;"></div>
            <div class="nav-item" id="nav-kamera" onclick="navGit('kamera')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>
              Kamera Analizi
            </div>
            <div class="nav-item" id="nav-hesaplama" onclick="navGit('hesaplama')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              Mühendislik
            </div>
            <div class="nav-item" id="nav-fiyat" onclick="navGit('fiyat')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
              Fiyat Takibi
            </div>
            <div class="nav-item" id="nav-arsiv" onclick="navGit('arsiv')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><polyline points="21 8 21 21 3 21 3 8"/><rect x="1" y="3" width="22" height="5"/><line x1="10" y1="12" x2="14" y2="12"/></svg>
              Arşiv
            </div>
          </div>

          <div class="sb-fill"></div>
          <div class="sb-foot">
            <div class="sb-upgrade" onclick="odemePaneliAc('max')">
              <div class="sb-upgrade-title">👑 Max'e Geç</div>
              <div class="sb-upgrade-sub">Çoklu şantiye &amp; stok</div>
            </div>
          </div>
        </div>

        <!-- SAĞ ANA ALAN -->
        <div id="mainArea">

          <!-- ══════ İÇERİK BAŞLIĞI ══════ -->
          <div id="contentHeader">
            <!-- Sol: başlık + tarih -->
            <div>
              <div style="font-size:20px;font-weight:800;color:#0F172A;letter-spacing:-0.4px;" id="contentTitle">Genel Bakış</div>
              <div style="font-size:12px;color:#94A3B8;margin-top:2px;" id="contentDate"></div>
            </div>
            <!-- Sağ: online durum + çan + kullanıcı -->
            <div style="display:flex;align-items:center;gap:12px;position:relative;">
              <!-- Online durum butonu -->
              <div id="onlineStatusBtn" style="display:flex;align-items:center;gap:7px;border:1.5px solid #F97316;border-radius:8px;padding:6px 12px;cursor:default;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F97316" stroke-width="2"><line x1="1" y1="1" x2="23" y2="23"/><path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55M5 12.55a10.94 10.94 0 0 1 5.17-2.39M10.71 5.05A16 16 0 0 1 22.56 9M1.42 9a15.91 15.91 0 0 1 4.7-2.88M12 20h.01"/></svg>
                <span style="font-size:12px;font-weight:600;color:#F97316;" id="onlineStatusText">İnternet Yok</span>
                <span id="offlineQueueBadge" style="font-size:11px;color:#F97316;display:none;"> · <span id="offlineQueueCount">0</span> Kayıt</span>
              </div>
              <!-- Bildirim çanı -->
              <div style="position:relative;cursor:pointer;" onclick="showToast('Bildirimler yakında', 'info')">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                <span id="notifDot" style="display:none;position:absolute;top:-2px;right:-2px;width:8px;height:8px;border-radius:50%;background:#EF4444;border:1.5px solid #FFFFFF;"></span>
              </div>
              <!-- Kullanıcı -->
              <div style="display:flex;align-items:center;gap:10px;cursor:pointer;padding:6px 10px;border-radius:8px;transition:background 0.15s;" onclick="avatarMenuAc()"
                onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='transparent'">
                <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#818cf8);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:white;flex-shrink:0;" id="headerAvatar">EA</div>
                <div style="line-height:1.3;">
                  <div style="font-size:13px;font-weight:600;color:#0F172A;" id="headerUserName">Kullanıcı</div>
                  <div style="font-size:11px;color:#94A3B8;" id="headerUserRole">Şantiye Şefi</div>
                </div>
              </div>

              <!-- ══════ AVATAR DROPDOWN MENU ══════ -->
              <div id="avatarMenu" style="display:none;position:absolute;top:56px;right:0;width:300px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,0.12);z-index:999;overflow:hidden;">

                <!-- Bölüm 1: Kullanıcı başlığı -->
                <div style="padding:16px;display:flex;gap:12px;align-items:center;border-bottom:1px solid #E2E8F0;">
                  <div id="amAvatar" style="width:40px;height:40px;border-radius:50%;background:#0D1117;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:white;flex-shrink:0;">EA</div>
                  <div style="min-width:0;">
                    <div id="amName" style="font-size:14px;font-weight:600;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Kullanıcı</div>
                    <div id="amEmail" style="font-size:12px;color:#94A3B8;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">kullanici@email.com</div>
                    <div id="amRole" style="display:inline-block;margin-top:4px;background:#F1F5F9;color:#64748B;font-size:11px;font-weight:500;padding:2px 8px;border-radius:20px;">Şantiye Şefi</div>
                  </div>
                </div>

                <!-- Bölüm 2: Aktif Şantiye -->
                <div id="amSantiyeBox" onclick="document.getElementById('avatarMenu').style.display='none';sayfaGoster('santiye');"
                  style="padding:12px 16px;background:#F8FAFC;cursor:pointer;border-bottom:1px solid #E2E8F0;transition:background 0.15s;"
                  onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='#F8FAFC'">
                  <div style="font-size:10px;font-weight:600;color:#94A3B8;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:4px;">Aktif Şantiye</div>
                  <div id="amSantiyeAd" style="font-size:13px;font-weight:600;color:#0F172A;margin-bottom:6px;">—</div>
                  <div style="height:4px;background:#E2E8F0;border-radius:2px;overflow:hidden;">
                    <div id="amSantiyeBar" style="height:100%;background:#3B82F6;border-radius:2px;width:0%;transition:width 0.4s;"></div>
                  </div>
                  <div id="amSantiyeAlt" style="font-size:11px;color:#94A3B8;margin-top:4px;">—</div>
                </div>

                <!-- Bölüm 3: Menü linkleri -->
                <div style="padding:6px 8px;border-top:1px solid #E2E8F0;">
                  <div onclick="document.getElementById('avatarMenu').style.display='none';sayfaGoster('ayarlar');"
                    style="padding:9px 8px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:10px;font-size:13px;color:#1E293B;transition:background 0.15s;"
                    onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='transparent'">⚙️ Ayarlar</div>
                  <div onclick="document.getElementById('avatarMenu').style.display='none';showToast('Bildirimler yakında', 'info');"
                    style="padding:9px 8px;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;font-size:13px;color:#1E293B;transition:background 0.15s;"
                    onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='transparent'">
                    <span>🔔 Bildirimler</span>
                  </div>
                  <div onclick="document.getElementById('avatarMenu').style.display='none';sayfaGoster('ayarlar');setTimeout(function(){{ayarlarKategoriGoster('plan');}},80);"
                    style="padding:9px 8px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:10px;font-size:13px;color:#1E293B;transition:background 0.15s;"
                    onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='transparent'">💳 Plan &amp; Ödeme</div>
                  <div onclick="document.getElementById('avatarMenu').style.display='none';showToast('Yardım merkezi yakında', 'info');"
                    style="padding:9px 8px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:10px;font-size:13px;color:#1E293B;transition:background 0.15s;"
                    onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='transparent'">❓ Yardım</div>
                </div>

                <!-- Bölüm 4: Karanlık Mod -->
                <div style="padding:6px 8px;border-top:1px solid #E2E8F0;">
                  <div style="padding:9px 8px;display:flex;align-items:center;justify-content:space-between;">
                    <span style="font-size:13px;color:#1E293B;display:flex;align-items:center;gap:10px;">🌙 Karanlık Mod</span>
                    <label style="position:relative;display:inline-block;width:36px;height:20px;cursor:pointer;flex-shrink:0;">
                      <input type="checkbox" id="karanlikModToggle" onchange="temaDegistir()" style="opacity:0;width:0;height:0;position:absolute;">
                      <span id="karanlikModTrack" style="position:absolute;inset:0;background:#CBD5E1;border-radius:20px;transition:0.3s;"></span>
                      <span id="karanlikModKnob" style="position:absolute;width:14px;height:14px;left:3px;bottom:3px;background:white;border-radius:50%;transition:0.3s;box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
                    </label>
                  </div>
                </div>

                <!-- Bölüm 5: Çıkış -->
                <div style="padding:6px 8px 10px;border-top:1px solid #E2E8F0;">
                  <div onclick="cikisYap()"
                    style="padding:9px 8px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:10px;font-size:13px;color:#EF4444;font-weight:600;transition:background 0.15s;"
                    onmouseover="this.style.background='#FEF2F2'" onmouseout="this.style.background='transparent'">→ Çıkış Yap</div>
                </div>

              </div><!-- /avatarMenu -->

            </div>
          </div>

          <!-- ══════ AI OMNI-COMMAND BAR (light) ══════ -->
          <div id="aiCommandBar" style="background:#FFFFFF;border-bottom:1px solid #E2E8F0;padding:14px 20px;flex-shrink:0;z-index:49;">
            <div id="aiBarInner" style="display:flex;align-items:center;gap:10px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:10px 14px;transition:border-color 0.15s,box-shadow 0.15s;">
              <svg id="aiSparkle" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="color:#6366f1;flex-shrink:0;transition:color 0.15s;">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3l1.5 4.5L11 9l-4.5 1.5L5 15l-1.5-4.5L-1 9l4.5-1.5zM19 3l1 3 3 1-3 1-1 3-1-3-3-1 3-1z"/>
              </svg>
              <input type="text" id="aiCommandInput"
                placeholder="AI Asistan: Soru sor, stok ekle veya komut ver..."
                onfocus="aiBarFocus(true)" onblur="aiBarFocus(false)"
                onkeydown="if(event.key==='Enter') aiCommandGonder()"
                style="flex:1;background:transparent;border:none;outline:none;color:#0F172A;font-size:14px;min-width:0;"/>
              <div style="width:1px;height:18px;background:#E2E8F0;flex-shrink:0;"></div>
              <button onclick="document.getElementById('aiFileInput').click()" title="Fotoğraf veya belge yükle"
                style="background:none;border:none;cursor:pointer;color:#94A3B8;padding:4px;border-radius:6px;font-size:16px;line-height:1;flex-shrink:0;transition:color 0.15s;"
                onmouseover="this.style.color='#475569'" onmouseout="this.style.color='#94A3B8'">📎</button>
              <input type="file" id="aiFileInput" accept="image/*,.pdf" style="display:none" onchange="aiDosyaSecildi(this)"/>
              <button id="aiMicBtn" onmousedown="aiMicBasildi()" onmouseup="aiMicBirakildi()" title="Sesli komut (basılı tut)"
                style="background:none;border:none;cursor:pointer;color:#94A3B8;padding:4px;border-radius:6px;font-size:16px;line-height:1;flex-shrink:0;transition:background 0.15s,color 0.15s;">🎙️</button>
              <button id="aiSendBtn" onclick="aiCommandGonder()"
                style="background:#3B82F6;border:none;cursor:pointer;color:white;padding:7px 16px;border-radius:8px;font-size:13px;font-weight:600;flex-shrink:0;display:flex;align-items:center;gap:6px;transition:background 0.15s;"
                onmouseover="this.style.background='#2563EB'" onmouseout="this.style.background='#3B82F6'">
                <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                Gönder
              </button>
            </div>
            <!-- Hızlı komut chipleri -->
            <div id="aiQuickChips" style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;">
              <button onclick="aiCommandCalistir('Stok durumu özeti')"
                style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                onmouseover="this.style.background='#E2E8F0';this.style.color='#0F172A'" onmouseout="this.style.background='#F1F5F9';this.style.color='#475569'">Stok Durumu</button>
              <button onclick="aiCommandCalistir('Bugünün özeti nedir?')"
                style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                onmouseover="this.style.background='#E2E8F0';this.style.color='#0F172A'" onmouseout="this.style.background='#F1F5F9';this.style.color='#475569'">Bugünün Özeti</button>
              <button onclick="aiCommandCalistir('ISG tutanağı oluştur')"
                style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                onmouseover="this.style.background='#E2E8F0';this.style.color='#0F172A'" onmouseout="this.style.background='#F1F5F9';this.style.color='#475569'">ISG Raporu</button>
              <button onclick="aiCommandCalistir('Çimento stoğu sorgula')"
                style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                onmouseover="this.style.background='#E2E8F0';this.style.color='#0F172A'" onmouseout="this.style.background='#F1F5F9';this.style.color='#475569'">Çimento Stok</button>
            </div>
            <!-- Quick dropdown (focus'ta açılır) -->
            <div id="aiQuickCommands" style="display:none;max-width:700px;margin:6px 0 0;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.08);">
              <div style="padding:6px 12px;border-bottom:1px solid #F1F5F9;font-size:10px;color:#94A3B8;letter-spacing:0.1em;text-transform:uppercase;">Hızlı Komutlar</div>
              <div id="aiQuickList"></div>
            </div>
            <!-- AI Sonuç banner -->
            <div id="aiResultBanner" style="display:none;max-width:700px;margin:8px 0 0;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:12px 14px;box-shadow:0 1px 3px rgba(0,0,0,0.06);">
              <div id="aiResultContent"></div>
            </div>
          </div>

          <div id="content">

            <!-- 3 STAT KARTI -->
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;" class="fade-in" id="dashKpiGrid">

              <!-- Kart 1: AI Sorgu -->
              <div class="kpi-card" id="kpi-ai" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:20px;display:flex;align-items:flex-start;justify-content:space-between;gap:14px;box-shadow:0 1px 3px rgba(0,0,0,0.06);cursor:default;position:relative;overflow:hidden;">
                <div>
                  <div style="font-size:12px;font-weight:500;color:#64748B;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.05em;">AI Sorgu (Bugün)</div>
                  <div class="kpi-val" id="kpiAiVal" style="font-size:36px;font-weight:700;color:#3B82F6;line-height:1;">--</div>
                  <div style="font-size:12px;color:#94A3B8;margin-top:6px;">Limitsiz kullanım</div>
                  <div class="kpi-bar-wrap" style="background:#EFF6FF;height:4px;border-radius:2px;margin-top:10px;width:100px;"><div class="kpi-bar" id="kpiAiBar" style="width:0%;background:#3B82F6;height:100%;border-radius:2px;transition:width 0.5s;"></div></div>
                </div>
                <div style="width:42px;height:42px;border-radius:10px;background:#EFF6FF;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
                </div>
              </div>

              <!-- Kart 2: Kamera Analizi -->
              <div class="kpi-card" id="kpi-kamera" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:20px;display:flex;align-items:flex-start;justify-content:space-between;gap:14px;box-shadow:0 1px 3px rgba(0,0,0,0.06);cursor:default;position:relative;overflow:hidden;">
                <div>
                  <div style="font-size:12px;font-weight:500;color:#64748B;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.05em;">Kamera Analizi</div>
                  <div class="kpi-val" id="kpiKameraVal" style="font-size:36px;font-weight:700;color:#10B981;line-height:1;">--</div>
                  <div style="font-size:12px;color:#94A3B8;margin-top:6px;">Bu hafta</div>
                  <div class="kpi-bar-wrap" style="background:#F0FDF4;height:4px;border-radius:2px;margin-top:10px;width:100px;"><div class="kpi-bar" id="kpiKameraBar" style="width:0%;background:#10B981;height:100%;border-radius:2px;transition:width 0.5s;"></div></div>
                </div>
                <div style="width:42px;height:42px;border-radius:10px;background:#F0FDF4;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>
                </div>
              </div>

              <!-- Kart 3: Aktif Plan -->
              <div class="kpi-card kpi-plan-card" id="kpi-plan" onclick="openProfile()" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:20px;display:flex;align-items:flex-start;justify-content:space-between;gap:14px;box-shadow:0 1px 3px rgba(0,0,0,0.06);cursor:pointer;position:relative;overflow:hidden;">
                <div>
                  <div style="font-size:12px;font-weight:500;color:#64748B;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.05em;">Aktif Plan</div>
                  <div class="kpi-val" id="kpiPlanVal" style="font-size:22px;font-weight:800;color:#8B5CF6;line-height:1;text-transform:uppercase;letter-spacing:0.04em;">--</div>
                  <div class="kpi-lbl" id="kpiRaporVal" style="font-size:12px;color:#94A3B8;margin-top:6px;">Rapor: <span id="kpiRaporSpan">--</span> bugün</div>
                  <div style="font-size:11px;color:#8B5CF6;margin-top:10px;font-weight:600;">Profili görüntüle →</div>
                </div>
                <div style="width:42px;height:42px;border-radius:10px;background:#F5F3FF;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                </div>
              </div>

            </div><!-- /3 stat kart -->

            <!-- 2 KOLON: Saha Günlüğü (sol %60) + AI Uyarıları (sağ %40) -->
            <div style="display:flex;gap:14px;flex:1;min-height:0;" class="fade-in">

              <!-- SOL: Saha Günlüğü & OCR Akışı -->
              <div style="flex:3;min-width:0;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06);">
                <div style="padding:16px 18px;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;">
                  <div>
                    <div style="font-size:14px;font-weight:700;color:#0F172A;">📋 Saha Günlüğü &amp; OCR Akışı</div>
                    <div style="font-size:11px;color:#94A3B8;margin-top:2px;">Son kayıtlar ve otomatik okumalar</div>
                  </div>
                  <button onclick="stokModalAc()"
                    style="background:#3B82F6;border:none;color:white;font-size:12px;font-weight:600;padding:7px 14px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:background 0.15s;white-space:nowrap;"
                    onmouseover="this.style.background='#2563EB'" onmouseout="this.style.background='#3B82F6'">
                    + Yeni Kayıt
                  </button>
                </div>
                <div id="sahaGunluguListe" style="flex:1;overflow-y:auto;padding:8px 12px;display:flex;flex-direction:column;gap:2px;">
                  <div style="color:#94A3B8;font-size:12px;text-align:center;padding:24px;">Yükleniyor...</div>
                </div>
                <!-- Alt hızlı eylemler -->
                <div style="padding:10px 14px;border-top:1px solid #F1F5F9;display:flex;gap:8px;flex-shrink:0;flex-wrap:wrap;">
                  <button onclick="kameraAc('genel')"
                    style="background:#F8FAFC;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:6px 12px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:all 0.15s;"
                    onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='#F8FAFC'">
                    📷 Fotoğraf Yükle
                  </button>
                  <button onclick="kameraAc('ocr')"
                    style="background:#F8FAFC;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:6px 12px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:all 0.15s;"
                    onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='#F8FAFC'">
                    📄 İrsaliye Oku (OCR)
                  </button>
                  <button onclick="showToast('ISG modülü yakında aktif olacak', 'info')"
                    style="background:#F8FAFC;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:6px 12px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:all 0.15s;"
                    onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='#F8FAFC'">
                    🛡️ ISG Tutanağı
                  </button>
                </div>
              </div>

              <!-- SAĞ: AI Uyarıları -->
              <div id="aiAlertsPanel" style="flex:2;min-width:0;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.06);">
                <div style="padding:16px 18px;border-bottom:1px solid #F1F5F9;flex-shrink:0;">
                  <div style="display:flex;align-items:center;gap:8px;">
                    <div style="font-size:14px;font-weight:700;color:#0F172A;">AI Uyarıları</div>
                    <span id="kritikBadge" style="display:none;background:#FEF2F2;color:#DC2626;font-size:10px;font-weight:700;padding:2px 8px;border-radius:20px;border:1px solid #FECACA;white-space:nowrap;">0 Kritik</span>
                  </div>
                  <div style="font-size:11px;color:#94A3B8;margin-top:2px;">Acil dikkat gerektiren</div>
                </div>
                <div id="aiAlertsContent" style="flex:1;overflow-y:auto;padding:8px 12px;display:flex;flex-direction:column;gap:6px;">
                  <div style="color:#94A3B8;font-size:12px;line-height:1.7;text-align:center;padding:24px 8px;">
                    Şu an aktif uyarı bulunmuyor.<br>Sistem tüm şantiyeleri izliyor.
                  </div>
                </div>
                <div style="padding:12px 14px;border-top:1px solid #F1F5F9;flex-shrink:0;">
                  <button onclick="navGit('gunluk')"
                    style="background:none;border:none;color:#3B82F6;font-size:12px;font-weight:600;cursor:pointer;padding:0;transition:color 0.15s;"
                    onmouseover="this.style.color='#2563EB'" onmouseout="this.style.color='#3B82F6'">
                    Tüm Uyarıları Gör →
                  </button>
                </div>
              </div>

            </div><!-- /2 kolon -->

            <!-- Hidden JS compat: legacy IDs -->
            <span id="statKamera" style="display:none;">12</span>
            <span id="statIlerleme" style="display:none;">87</span>
            <span id="statGuvenlik" style="display:none;">0</span>
            <span id="kpiRaporVal2" style="display:none;"></span>
            <div class="quick-actions" style="display:none;" aria-hidden="true">
              <div class="quick-btn" onclick="guvenlikAc()" id="raporlarBtn"><div class="quick-btn-icon">⚠️</div><div class="quick-btn-label">GÜVENLİK</div></div>
            </div>
            <div class="quick-sub" id="raporlarSub" style="display:none;" aria-hidden="true">
              <div class="quick-sub-btn" onclick="navGit('gunluk')">📋 Günlük Rapor</div>
              <div class="quick-sub-btn" onclick="pdfIndir()">📄 PDF İndir</div>
            </div>
            <div class="quick-sub" id="analizSub" style="display:none;" aria-hidden="true">
              <div class="quick-sub-btn" onclick="navGit('kamera')">📷 Kamera Analizi</div>
            </div>
            <input type="text" id="userInput" style="display:none;" placeholder="Soru sor..."/>
            <div id="result" style="display:none;"></div>
            <!-- YOLO sonucu modal flow için sabit alan — innerHTML değişse silinmez -->
            <div id="yoloModalPanel" style="margin-top:8px;"></div>

          </div><!-- /content -->

          <!-- ══════ ŞANTİYE SAYFASI ══════ -->
          <div id="santiyePage" style="display:none;flex:1;flex-direction:column;overflow:hidden;background:#F1F5F9;">

            <!-- Arama + Yeni Şantiye -->
            <div style="background:#FFFFFF;border-bottom:1px solid #E2E8F0;padding:14px 24px;display:flex;align-items:center;gap:12px;flex-shrink:0;">
              <div style="flex:1;display:flex;align-items:center;gap:10px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:10px;padding:9px 14px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <input id="santiyeArama" type="text" placeholder="Şantiye ara..."
                  oninput="santiyePageFiltrele(this.value)"
                  style="flex:1;background:transparent;border:none;outline:none;color:#0F172A;font-size:14px;"/>
              </div>
              <button onclick="santiyeEkleModalAc(null)"
                style="background:#3B82F6;border:none;color:white;font-size:13px;font-weight:700;padding:10px 18px;border-radius:10px;cursor:pointer;display:flex;align-items:center;gap:7px;transition:background 0.15s;white-space:nowrap;flex-shrink:0;"
                onmouseover="this.style.background='#2563EB'" onmouseout="this.style.background='#3B82F6'">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                Yeni Şantiye
              </button>
            </div>

            <div style="flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:16px;">

              <!-- Gizli KPI refs (JS compat) -->
              <div style="display:none;" aria-hidden="true">
                <span id="spKpiToplam"></span><span id="spKpiIyi"></span><span id="spKpiDikkat"></span><span id="spKpiIsci"></span>
              </div>

              <!-- Öne Çıkan (ilk 3 — yatay kart) -->
              <div>
                <div style="font-size:13px;font-weight:600;color:#64748B;margin-bottom:10px;">Aktif Projeler</div>
                <div id="santiyePageHoriz" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;"></div>
              </div>

              <!-- Tüm şantiyeler — dikey grid -->
              <div>
                <div style="font-size:13px;font-weight:600;color:#64748B;margin-bottom:10px;">Tüm Projeler</div>
                <div id="santiyePageGrid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;"></div>
              </div>

            </div>
          </div><!-- /santiyePage -->

          <!-- ══════ FİYAT TAKİBİ SAYFASI ══════ -->
          <div id="fiyatPage" style="display:none;flex:1;flex-direction:column;overflow:hidden;background:#F1F5F9;">

            <!-- AI Command Bar -->
            <div style="background:#FFFFFF;border-bottom:1px solid #E2E8F0;padding:14px 20px;flex-shrink:0;z-index:49;">
              <div style="display:flex;align-items:center;gap:10px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:10px 14px;transition:border-color 0.15s,box-shadow 0.15s;">
                <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="#6366f1" stroke-width="2" style="flex-shrink:0;"><path stroke-linecap="round" stroke-linejoin="round" d="M5 3l1.5 4.5L11 9l-4.5 1.5L5 15l-1.5-4.5L-1 9l4.5-1.5zM19 3l1 3 3 1-3 1-1 3-1-3-3-1 3-1z"/></svg>
                <input id="fiyatAiInput" type="text" placeholder="AI Asistan: Malzeme fiyat trendlerini sor, tahmin iste..."
                  onkeydown="if(event.key==='Enter') fiyatAiGonder()"
                  style="flex:1;background:transparent;border:none;outline:none;color:#0F172A;font-size:14px;min-width:0;"/>
                <div style="width:1px;height:18px;background:#E2E8F0;flex-shrink:0;"></div>
                <button onclick="fiyatAiGonder()"
                  style="background:#3B82F6;border:none;cursor:pointer;color:white;padding:7px 16px;border-radius:8px;font-size:13px;font-weight:600;flex-shrink:0;display:flex;align-items:center;gap:6px;transition:background 0.15s;"
                  onmouseover="this.style.background='#2563EB'" onmouseout="this.style.background='#3B82F6'">
                  <svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                  Gönder
                </button>
              </div>
              <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;">
                <button onclick="fiyatAiQuick('Çelik fiyat trendi ve tahminleri')"
                  style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                  onmouseover="this.style.background='#E2E8F0'" onmouseout="this.style.background='#F1F5F9'">Çelik Fiyatları</button>
                <button onclick="fiyatAiQuick('Beton fiyat trendi ve tahminleri')"
                  style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                  onmouseover="this.style.background='#E2E8F0'" onmouseout="this.style.background='#F1F5F9'">Beton Fiyatları</button>
                <button onclick="fiyatAiQuick('Hangi malzemeyi şimdi satın almalıyım?')"
                  style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                  onmouseover="this.style.background='#E2E8F0'" onmouseout="this.style.background='#F1F5F9'">Satın Alma Önerisi</button>
              </div>
              <div id="fiyatAiResult" style="display:none;margin-top:10px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:12px 14px;font-size:13px;color:#0F172A;"></div>
            </div>

            <!-- Content -->
            <div style="flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:16px;">

              <!-- 3 Chart Cards -->
              <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;">

                <!-- Çelik -->
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                  <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px;gap:8px;">
                    <div>
                      <div style="font-size:14px;font-weight:700;color:#0F172A;">Çelik Fiyatları</div>
                      <div style="font-size:11px;color:#94A3B8;margin-top:2px;">Çelik Fiyatları: <span id="celikFiyatLabel" style="color:#EF4444;font-weight:600;">—</span></div>
                    </div>
                    <select id="celikPeriod" onchange="fiyatGrafikYukle('demir','celikGrafik','celikFiyatLabel',this.value)"
                      style="font-size:11px;font-weight:600;color:#475569;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:7px;padding:4px 8px;cursor:pointer;outline:none;">
                      <option value="30">Son 1 Ay</option>
                      <option value="90" selected>Son 3 Ay</option>
                      <option value="180">Son 6 Ay</option>
                    </select>
                  </div>
                  <canvas id="celikGrafik" height="160"></canvas>
                </div>

                <!-- Beton -->
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                  <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px;gap:8px;">
                    <div>
                      <div style="font-size:14px;font-weight:700;color:#0F172A;">Beton Fiyatları</div>
                      <div style="font-size:11px;color:#94A3B8;margin-top:2px;">Beton Fiyatları: <span id="betonFiyatLabel" style="color:#EF4444;font-weight:600;">—</span></div>
                    </div>
                    <select id="betonPeriod" onchange="fiyatGrafikYukle('beton','betonGrafik','betonFiyatLabel',this.value)"
                      style="font-size:11px;font-weight:600;color:#475569;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:7px;padding:4px 8px;cursor:pointer;outline:none;">
                      <option value="30">Son 1 Ay</option>
                      <option value="90" selected>Son 3 Ay</option>
                      <option value="180">Son 6 Ay</option>
                    </select>
                  </div>
                  <canvas id="betonGrafik" height="160"></canvas>
                </div>

                <!-- Kereste -->
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                  <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:12px;gap:8px;">
                    <div>
                      <div style="font-size:14px;font-weight:700;color:#0F172A;">Kereste Fiyatları</div>
                      <div style="font-size:11px;color:#94A3B8;margin-top:2px;">Kereste Fiyatları: <span id="keresteFiyatLabel" style="color:#EF4444;font-weight:600;">—</span></div>
                    </div>
                    <select id="kerestePeriod" onchange="fiyatGrafikYukle('cimento','keresteGrafik','keresteFiyatLabel',this.value)"
                      style="font-size:11px;font-weight:600;color:#475569;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:7px;padding:4px 8px;cursor:pointer;outline:none;">
                      <option value="30">Son 1 Ay</option>
                      <option value="90" selected>Son 3 Ay</option>
                      <option value="180">Son 6 Ay</option>
                    </select>
                  </div>
                  <canvas id="keresteGrafik" height="160"></canvas>
                </div>

              </div>

              <!-- AI Insights -->
              <div>
                <div style="font-size:18px;font-weight:700;color:#0F172A;">AI Piyasa Tahminleri &amp; Satın Alma Önerileri</div>
                <div style="font-size:12px;color:#94A3B8;margin-top:2px;margin-bottom:14px;">AI Piyasa Tahminleri &amp; Satın Alma Önerileri</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">

                  <!-- Piyasa Analizi -->
                  <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                      <div style="font-size:15px;font-weight:700;color:#0F172A;">📊 Piyasa Analizi</div>
                      <div style="width:32px;height:32px;background:#EFF6FF;border-radius:8px;display:flex;align-items:center;justify-content:center;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
                      </div>
                    </div>
                    <div id="fiyatAnalizSubtitle" style="font-size:11px;color:#94A3B8;margin-bottom:14px;">Piyasa analizi yükleniyor...</div>
                    <div id="fiyatAnalizList" style="display:flex;flex-direction:column;gap:8px;"></div>
                  </div>

                  <!-- Satın Alma Zamanı -->
                  <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,0.05);display:flex;flex-direction:column;">
                    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
                      <div style="font-size:15px;font-weight:700;color:#0F172A;">📦 Satın Alma Zamanı</div>
                      <div style="width:32px;height:32px;background:#F0FDF4;border-radius:8px;display:flex;align-items:center;justify-content:center;">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
                      </div>
                    </div>
                    <div id="fiyatSatinSubtitle" style="font-size:11px;color:#94A3B8;margin-bottom:14px;">Öneri yükleniyor...</div>
                    <div id="fiyatSatinList" style="display:flex;flex-direction:column;gap:8px;flex:1;"></div>
                    <button onclick="fiyatAiQuick('Şu an hangi malzemeyi satın almalıyım? Detaylı öneri ver.')"
                      style="margin-top:16px;width:100%;background:#3B82F6;border:none;color:white;padding:13px;border-radius:10px;cursor:pointer;font-weight:700;font-size:14px;transition:background 0.15s;font-family:inherit;"
                      onmouseover="this.style.background='#2563EB'" onmouseout="this.style.background='#3B82F6'">Satın Al</button>
                  </div>

                </div>
              </div>

            </div>
          </div><!-- /fiyatPage -->

          <!-- ══════ STOK TAKİBİ SAYFASI ══════ -->
          <div id="stokPage" style="display:none;flex:1;flex-direction:column;overflow:hidden;background:#F1F5F9;">

            <!-- AI Command Bar -->
            <div style="background:#FFFFFF;border-bottom:1px solid #E2E8F0;padding:14px 20px;flex-shrink:0;">
              <div style="display:flex;align-items:center;gap:10px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:12px;padding:10px 14px;">
                <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="#6366f1" stroke-width="2" style="flex-shrink:0;"><path stroke-linecap="round" stroke-linejoin="round" d="M5 3l1.5 4.5L11 9l-4.5 1.5L5 15l-1.5-4.5L-1 9l4.5-1.5zM19 3l1 3 3 1-3 1-1 3-1-3-3-1 3-1z"/></svg>
                <input id="stokAiInput" type="text" placeholder="AI Asistan: Stok durumu sor, malzeme analizi iste..."
                  onkeydown="if(event.key==='Enter') stokAiGonder()"
                  style="flex:1;background:transparent;border:none;outline:none;color:#0F172A;font-size:14px;min-width:0;"/>
                <div style="width:1px;height:18px;background:#E2E8F0;flex-shrink:0;"></div>
                <button onclick="stokAiGonder()"
                  style="background:#3B82F6;border:none;cursor:pointer;color:white;padding:7px 16px;border-radius:8px;font-size:13px;font-weight:600;flex-shrink:0;display:flex;align-items:center;gap:6px;transition:background 0.15s;"
                  onmouseover="this.style.background='#2563EB'" onmouseout="this.style.background='#3B82F6'">
                  <svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
                  Gönder
                </button>
              </div>
              <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;">
                <button onclick="stokAiQuick('Toplam stok durumu ve kritik malzemeler neler?')"
                  style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                  onmouseover="this.style.background='#E2E8F0'" onmouseout="this.style.background='#F1F5F9'">Stok Durumu</button>
                <button onclick="stokAiQuick('Hangi malzemeler kritik seviyede?')"
                  style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                  onmouseover="this.style.background='#E2E8F0'" onmouseout="this.style.background='#F1F5F9'">Kritik Stoklar</button>
                <button onclick="stokAiQuick('Bu ay toplam malzeme maliyeti nedir?')"
                  style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
                  onmouseover="this.style.background='#E2E8F0'" onmouseout="this.style.background='#F1F5F9'">Maliyet Analizi</button>
              </div>
              <div id="stokAiResult" style="display:none;margin-top:10px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:12px 14px;font-size:13px;color:#0F172A;line-height:1.6;"></div>
            </div>

            <!-- İçerik -->
            <div style="flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:14px;">

              <!-- Uyarılar -->
              <div id="stokUyarilar"></div>

              <!-- Şantiye Filtre -->
              <div style="display:flex;align-items:center;gap:10px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                <select id="stokSantiye" onchange="stokSantiyeDegisti()"
                  style="background:#FFFFFF;border:1.5px solid #E2E8F0;color:#0F172A;padding:8px 14px;border-radius:9px;font-size:13px;font-weight:600;outline:none;cursor:pointer;min-width:200px;">
                  <option value="">Tüm Şantiyeler</option>
                </select>
              </div>

              <!-- Stok Kartları -->
              <div>
                <div style="font-size:12px;font-weight:600;color:#94A3B8;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">Malzeme Stok Durumu</div>
                <div id="stokKartlar" style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;"></div>
              </div>

              <!-- Alt 2 Bölüm -->
              <div style="display:grid;grid-template-columns:1.2fr 1fr;gap:14px;min-height:320px;">

                <!-- Hareket Geçmişi -->
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                  <div style="padding:14px 16px;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;">
                    <div style="font-size:13px;font-weight:700;color:#0F172A;">📋 Hareket Geçmişi</div>
                    <select id="stokGecmisMalzeme" onchange="stokGecmisYukle()"
                      style="background:#F8FAFC;border:1px solid #E2E8F0;color:#475569;padding:5px 10px;border-radius:7px;font-size:12px;font-weight:600;outline:none;cursor:pointer;">
                      <option value="demir">Demir</option>
                      <option value="cimento">Çimento</option>
                      <option value="beton">Beton</option>
                      <option value="tugla">Tuğla</option>
                      <option value="kum">Kum</option>
                    </select>
                  </div>
                  <div id="stokGecmisListe" style="flex:1;overflow-y:auto;padding:8px 12px;"></div>
                </div>

                <!-- Malzeme Girişi / Çıkışı -->
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:10px;overflow-y:auto;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                  <div style="font-size:13px;font-weight:700;color:#0F172A;display:flex;align-items:center;gap:6px;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                    Malzeme Girişi / Çıkışı
                  </div>

                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                    <select id="stokMalzeme"
                      style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#0F172A;padding:9px 12px;border-radius:9px;font-size:13px;outline:none;cursor:pointer;">
                      <option value="demir">🔩 Demir</option>
                      <option value="cimento">🏭 Çimento</option>
                      <option value="beton">🧱 Beton</option>
                      <option value="tugla">🏠 Tuğla</option>
                      <option value="kum">⛱️ Kum</option>
                    </select>
                    <select id="stokTip"
                      style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#0F172A;padding:9px 12px;border-radius:9px;font-size:13px;outline:none;cursor:pointer;">
                      <option value="giris">📥 Giriş</option>
                      <option value="cikis">📤 Çıkış</option>
                    </select>
                  </div>

                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                    <input type="number" id="stokMiktar" placeholder="Miktar"
                      style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#0F172A;padding:9px 12px;border-radius:9px;font-size:13px;outline:none;transition:border-color 0.15s;box-sizing:border-box;"
                      onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">
                    <select id="stokBirim"
                      style="background:#F8FAFC;border:1.5px solid #E2E8F0;color:#0F172A;padding:9px 12px;border-radius:9px;font-size:13px;outline:none;cursor:pointer;">
                      <option value="ton">Ton</option>
                      <option value="m³">m³</option>
                      <option value="adet">Adet</option>
                      <option value="çuval">Çuval</option>
                    </select>
                  </div>

                  <input type="text" id="stokTedarikci" placeholder="Tedarikçi (opsiyonel)"
                    style="width:100%;background:#F8FAFC;border:1.5px solid #E2E8F0;color:#0F172A;padding:9px 12px;border-radius:9px;font-size:13px;outline:none;transition:border-color 0.15s;box-sizing:border-box;"
                    onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">

                  <input type="number" id="stokFiyat" placeholder="Birim Fiyat ₺ (opsiyonel)"
                    style="width:100%;background:#F8FAFC;border:1.5px solid #E2E8F0;color:#0F172A;padding:9px 12px;border-radius:9px;font-size:13px;outline:none;transition:border-color 0.15s;box-sizing:border-box;"
                    onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">

                  <input type="text" id="stokNotlar" placeholder="Notlar (opsiyonel)"
                    style="width:100%;background:#F8FAFC;border:1.5px solid #E2E8F0;color:#0F172A;padding:9px 12px;border-radius:9px;font-size:13px;outline:none;transition:border-color 0.15s;box-sizing:border-box;"
                    onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">

                  <button onclick="stokKaydet()"
                    style="width:100%;background:#3B82F6;border:none;color:white;padding:12px;border-radius:10px;cursor:pointer;font-weight:700;font-size:14px;transition:background 0.15s;font-family:inherit;margin-top:2px;"
                    onmouseover="this.style.background='#2563EB'" onmouseout="this.style.background='#3B82F6'">
                    💾 Kaydet
                  </button>
                  <div id="stokMsg" style="font-size:12px;text-align:center;min-height:16px;"></div>
                </div>

              </div>
            </div>
          </div><!-- /stokPage -->

          <!-- ══════ KAMERA ANALİZİ SAYFASI ══════ -->
          <div id="kameraPage" style="display:none;flex:1;flex-direction:column;overflow:hidden;background:#F1F5F9;">

            <!-- ══ SAYFA BAŞLIĞI ══ -->
            <div style="background:#FFFFFF;border-bottom:1px solid #E2E8F0;padding:16px 24px 14px;flex-shrink:0;">
              <!-- Proje Çubuğu -->
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:10px;">
                <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
                  <div id="kpProjeAnchor" onclick="kpProjeDropdownAc()" style="display:flex;align-items:center;gap:6px;cursor:pointer;padding:4px 10px;border-radius:8px;border:1px solid #E2E8F0;background:#F8FAFC;transition:all 0.15s;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='#F8FAFC'">
                    <span style="font-size:11px;font-weight:600;color:#94A3B8;text-transform:uppercase;letter-spacing:0.05em;">Aktif Proje:</span>
                    <span id="kpAktifProjeName" style="font-size:13px;font-weight:700;color:#0F172A;max-width:200px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Şantiye seçin...</span>
                    <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="#94A3B8" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
                  </div>
                  <span id="kpSantiyeDurum" style="background:#DCFCE7;color:#16A34A;font-size:11px;font-weight:700;padding:4px 10px;border-radius:20px;display:none;">Şantiye Durumu: Aktif</span>
                  <span id="kpSantiyeKonum" style="display:none;align-items:center;gap:4px;font-size:12px;color:#64748B;">
                    <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                    <span id="kpSantiyeKonumText"></span>
                  </span>
                </div>
                <div style="display:flex;gap:8px;flex-shrink:0;">
                  <button onclick="yeniKameraEkleAc()" style="display:flex;align-items:center;gap:6px;background:#0F172A;border:none;color:white;font-size:13px;font-weight:700;padding:9px 16px;border-radius:10px;cursor:pointer;transition:background 0.15s;white-space:nowrap;"
                    onmouseover="this.style.background='#1E293B'" onmouseout="this.style.background='#0F172A'">
                    <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>
                    Yeni Kamera Ekle
                  </button>
                  <!-- Dropdown split button -->
                  <div style="position:relative;display:flex;" data-foto-dropdown>
                    <button onclick="kameraFotoInputAc()" style="display:flex;align-items:center;gap:6px;background:#F97316;border:none;color:white;font-size:13px;font-weight:700;padding:9px 14px;border-radius:10px 0 0 10px;cursor:pointer;transition:background 0.15s;white-space:nowrap;"
                      onmouseover="this.style.background='#ea6010'" onmouseout="this.style.background='#F97316'">
                      <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                      + Fotoğraf / Kanıt Ekle
                    </button>
                    <button onclick="kpFotoDropdownToggle()" style="display:flex;align-items:center;justify-content:center;background:#F97316;border:none;border-left:1px solid rgba(255,255,255,0.25);color:white;padding:9px 10px;border-radius:0 10px 10px 0;cursor:pointer;transition:background 0.15s;"
                      onmouseover="this.style.background='#ea6010'" onmouseout="this.style.background='#F97316'">
                      <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
                    </button>
                    <div id="kpFotoDropdown" style="display:none;position:absolute;top:calc(100% + 6px);right:0;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,0.12);z-index:500;min-width:160px;overflow:hidden;">
                      <button onclick="kameraFotoInputAc();kpFotoDropdownToggle()" style="display:flex;align-items:center;gap:8px;width:100%;padding:10px 14px;background:transparent;border:none;font-size:13px;font-weight:600;color:#0F172A;cursor:pointer;text-align:left;"
                        onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='transparent'">
                        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#64748B" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                        Dosya Seç
                      </button>
                    </div>
                  </div>
                  <input type="file" id="kameraPageFileInput" accept="image/*" style="display:none;" onchange="kameraPageDosyaAnalizEt(event)">
                </div>
              </div>
              <!-- Başlık + Açıklama -->
              <div>
                <div style="font-size:22px;font-weight:800;color:#0F172A;line-height:1.2;">Kamera Analizi</div>
                <div id="kpSayfaDesc" style="font-size:13px;color:#64748B;margin-top:4px;">Bu şantiyeye bağlı <span id="kpAktifKameraAdet">0</span> aktif kamera ve <span id="kpAnalizGunAdet">0</span> günlük analiz kaydı inceleniyor.</div>
              </div>
            </div>

            <!-- ══ FİLTRE ÇUBUĞU ══ -->
            <div style="background:#FFFFFF;border-bottom:1px solid #E2E8F0;padding:10px 24px;flex-shrink:0;display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
              <div style="flex:1;min-width:180px;display:flex;align-items:center;gap:8px;background:#F8FAFC;border:1.5px solid #E2E8F0;border-radius:10px;padding:8px 12px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                <input id="kameraArama" type="text" placeholder="Kamera veya olay türüne göre ara..."
                  oninput="kameraPageFiltrele(this.value)"
                  style="flex:1;background:transparent;border:none;outline:none;color:#0F172A;font-size:13px;"/>
              </div>
              <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
                <button class="kamera-chip active" id="kchip-all" onclick="kameraChipSec('all',this)" style="background:#0F172A;border:1.5px solid #0F172A;color:white;font-size:12px;font-weight:600;padding:6px 14px;border-radius:20px;cursor:pointer;transition:all 0.15s;">Tümü</button>
                <button class="kamera-chip" id="kchip-guvenlik" onclick="kameraChipSec('guvenlik',this)" style="background:#FEF3C7;border:1.5px solid #FDE68A;color:#D97706;font-size:12px;font-weight:600;padding:6px 14px;border-radius:20px;cursor:pointer;transition:all 0.15s;">Sadece İhlaller</button>
                <button class="kamera-chip" id="kchip-ilerleme" onclick="kameraChipSec('ilerleme',this)" style="background:#EFF6FF;border:1.5px solid #BFDBFE;color:#2563EB;font-size:12px;font-weight:600;padding:6px 14px;border-radius:20px;cursor:pointer;transition:all 0.15s;">Araç Çiğneleni</button>
                <button class="kamera-chip" id="kchip-genel" onclick="kameraChipSec('genel',this)" style="background:#F0FDF4;border:1.5px solid #BBF7D0;color:#16A34A;font-size:12px;font-weight:600;padding:6px 14px;border-radius:20px;cursor:pointer;transition:all 0.15s;">Personel Tahlim</button>
              </div>
            </div>

            <!-- ══ İKİ SÜTUNLU İÇERİK ══ -->
            <div style="flex:1;overflow:hidden;display:flex;">

              <!-- SOL ANA ALAN -->
              <div id="kameraPageMain" style="flex:1;overflow-y:auto;padding:20px 20px 40px 24px;display:flex;flex-direction:column;gap:20px;">

                <!-- ─── Canlı Kamera İzleme ─── -->
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                  <div style="padding:14px 18px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #E2E8F0;">
                    <div style="display:flex;align-items:center;gap:8px;">
                      <span style="display:inline-block;width:8px;height:8px;background:#EF4444;border-radius:50%;animation:kpPulse 1.5s infinite;"></span>
                      <span style="font-size:14px;font-weight:700;color:#0F172A;">Canlı Kamera İzleme</span>
                    </div>
                    <div style="display:flex;gap:6px;">
                      <button id="kpGridBtn" onclick="kpKameraGoruntuleme('grid')" title="Izgara görünümü" style="background:#0F172A;border:none;padding:6px 8px;border-radius:7px;cursor:pointer;display:flex;align-items:center;">
                        <svg width="14" height="14" fill="white" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
                      </button>
                      <button id="kpListBtn" onclick="kpKameraGoruntuleme('list')" title="Liste görünümü" style="background:#F1F5F9;border:none;padding:6px 8px;border-radius:7px;cursor:pointer;display:flex;align-items:center;">
                        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#475569" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
                      </button>
                      <button onclick="kpKameraFullscreen()" title="Tam ekran" style="background:#F1F5F9;border:none;padding:6px 8px;border-radius:7px;cursor:pointer;display:flex;align-items:center;">
                        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#475569" stroke-width="2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>
                      </button>
                    </div>
                  </div>
                  <!-- Kamera Grid -->
                  <div id="kpCameraGrid" style="padding:12px 16px 16px;display:grid;grid-template-columns:repeat(3,1fr);gap:8px;"></div>
                  <div id="kpCameraEmpty" style="display:none;"></div>
                </div>

                <!-- ─── AI Fotoğraf Kanıtları ─── -->
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                  <div style="padding:14px 18px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #E2E8F0;">
                    <div style="display:flex;align-items:center;gap:8px;">
                      <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="#6366f1" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                      <span style="font-size:14px;font-weight:700;color:#0F172A;">AI Anlık Fotoğraf Kanıtları</span>
                      <span id="kpAiBadge" style="background:#EFF6FF;color:#2563EB;font-size:11px;font-weight:700;padding:2px 8px;border-radius:12px;">0</span>
                    </div>
                    <div style="display:flex;gap:6px;align-items:center;">
                      <button id="kpSortBtn" onclick="kpSortToggle()" style="font-size:12px;font-weight:700;color:#64748B;background:#F8FAFC;border:1px solid #E2E8F0;padding:5px 12px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:4px;">↓ En Yeni</button>
                      <button onclick="kameraPageYukle()" style="font-size:12px;font-weight:700;color:#64748B;background:#F8FAFC;border:1px solid #E2E8F0;padding:5px 12px;border-radius:8px;cursor:pointer;text-transform:uppercase;letter-spacing:0.03em;">Yenile</button>
                    </div>
                  </div>
                  <!-- Analiz Yükleniyor -->
                  <div id="kpAnalysisLoading" style="display:none;padding:24px;text-align:center;">
                    <div style="width:36px;height:36px;border:3px solid #E2E8F0;border-top-color:#6366f1;border-radius:50%;animation:spin 0.8s linear infinite;margin:0 auto 10px;"></div>
                    <div style="font-size:13px;font-weight:600;color:#0F172A;">AI analiz yapıyor...</div>
                    <div style="font-size:12px;color:#64748B;margin-top:3px;">Fotoğraf işleniyor, lütfen bekleyin</div>
                  </div>
                  <div id="kpAiKartlar" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;padding:16px 18px;"></div>
                  <div id="kpAiEmpty" style="padding:40px;text-align:center;cursor:pointer;transition:all 0.15s;"
                    onclick="kameraFotoInputAc()"
                    onmouseover="this.style.background='#FFF7ED'" onmouseout="this.style.background='transparent'">
                    <svg width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="#CBD5E1" stroke-width="1.5" style="margin:0 auto 10px;display:block;"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>
                    <div style="font-size:13px;font-weight:700;color:#475569;">Fotoğraf yükle ve AI ile analiz et</div>
                    <div style="font-size:12px;color:#94A3B8;margin-top:4px;">Sağ üstteki "+ Fotoğraf / Kanıt Ekle" butonunu kullanın</div>
                  </div>
                </div>

                <!-- ─── Manuel Kanıtlar ─── -->
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.05);">
                  <div style="padding:14px 18px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #E2E8F0;">
                    <div style="display:flex;align-items:center;gap:8px;">
                      <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="#0F172A" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                      <span style="font-size:14px;font-weight:700;color:#0F172A;">Manuel Kanıtlar</span>
                      <span id="kpManuelBadge" style="background:#F1F5F9;color:#475569;font-size:11px;font-weight:700;padding:2px 8px;border-radius:12px;">0</span>
                    </div>
                    <div style="display:flex;gap:8px;">
                      <button onclick="kpManuelEkleAc()" style="font-size:12px;font-weight:700;color:#F97316;background:#FFF7ED;border:1px solid #FED7AA;padding:5px 12px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:4px;">
                        <svg width="11" height="11" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
                        Ekle
                      </button>
                      <button style="font-size:12px;font-weight:700;color:#64748B;background:#F8FAFC;border:1px solid #E2E8F0;padding:5px 12px;border-radius:8px;cursor:pointer;text-transform:uppercase;letter-spacing:0.03em;">Tümünü Arşivle</button>
                    </div>
                  </div>
                  <!-- Manuel Kayıt Formu -->
                  <div id="kpManuelForm" style="display:none;padding:14px 18px;border-bottom:1px solid #E2E8F0;">
                    <div style="font-size:13px;font-weight:700;color:#0F172A;margin-bottom:10px;">Manuel Kanıt Kaydet</div>
                    <select id="kpManuelTip" style="width:100%;padding:9px 12px;border:1.5px solid #E2E8F0;border-radius:8px;font-size:13px;color:#0F172A;background:#F8FAFC;margin-bottom:8px;outline:none;">
                      <option value="gozlem">Saha Gözlemi</option>
                      <option value="ihbar">İhbar / Şikayet</option>
                      <option value="denetim">Denetim Notu</option>
                      <option value="kaza">Kaza / Olay</option>
                    </select>
                    <textarea id="kpManuelNot" placeholder="Gözlem notunu girin..." style="width:100%;padding:9px 12px;border:1.5px solid #E2E8F0;border-radius:8px;font-size:13px;color:#0F172A;background:#F8FAFC;resize:vertical;min-height:70px;font-family:inherit;outline:none;margin-bottom:8px;box-sizing:border-box;"></textarea>
                    <div style="display:flex;gap:8px;">
                      <button onclick="kpManuelKaydet()" style="flex:1;background:#0F172A;border:none;color:white;font-size:13px;font-weight:700;padding:9px;border-radius:8px;cursor:pointer;">Kaydet</button>
                      <button onclick="document.getElementById('kpManuelForm').style.display='none'" style="padding:9px 14px;background:#F1F5F9;border:none;color:#475569;font-size:13px;font-weight:600;border-radius:8px;cursor:pointer;">İptal</button>
                    </div>
                  </div>
                  <div id="kpManuelKartlar" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;padding:16px 18px;"></div>
                  <div id="kpManuelEmpty" style="display:none;padding:36px;text-align:center;color:#94A3B8;font-size:13px;">Henüz manuel kanıt kaydedilmemiş.</div>
                </div>

              </div><!-- /kameraPageMain -->

              <!-- ══ SAĞ PANEL WRAPPER ══ -->
              <div style="width:300px;flex-shrink:0;overflow-y:auto;padding:16px 16px 24px 8px;display:flex;flex-direction:column;gap:12px;background:#F1F5F9;">

                <!-- ── Yapay Zeka Tespit Arışı KARTI ── -->
                <div style="background:#0F172A;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.18);flex-shrink:0;">

                  <!-- Başlık -->
                  <div style="padding:14px 16px 12px;border-bottom:1px solid rgba(255,255,255,0.07);">
                    <div style="display:flex;align-items:center;justify-content:space-between;">
                      <div style="display:flex;align-items:center;gap:8px;">
                        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#6366f1" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                        <span style="font-size:11px;font-weight:800;color:#E2E8F0;text-transform:uppercase;letter-spacing:0.08em;">Yapay Zeka Tespit Arışı</span>
                      </div>
                      <span style="background:#10B981;color:white;font-size:9px;font-weight:800;padding:3px 8px;border-radius:20px;letter-spacing:0.06em;">CANLI</span>
                    </div>
                  </div>

                  <!-- Tespit Listesi -->
                  <div id="kpTespitAkis" style="padding:8px 16px;display:flex;flex-direction:column;">
                    <div style="text-align:center;padding:20px 0;color:#475569;font-size:12px;">Analiz geçmişi yükleniyor...</div>
                  </div>

                  <!-- Logları Dışa Aktar -->
                  <div style="padding:10px 16px 14px;">
                    <button onclick="kpLoguIndirv()" style="width:100%;display:flex;align-items:center;justify-content:center;gap:8px;padding:11px;background:#1D4ED8;border:none;color:#FFFFFF;font-size:11px;font-weight:700;border-radius:10px;cursor:pointer;letter-spacing:0.05em;text-transform:uppercase;transition:background 0.15s;"
                      onmouseover="this.style.background='#1e40af'" onmouseout="this.style.background='#1D4ED8'">
                      <svg width="13" height="13" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                      Logları Dışa Aktar
                    </button>
                  </div>
                </div><!-- /tespit kartı -->

                <!-- ── Analiz Özeti KARTI ── -->
                <div style="background:#0F172A;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.18);flex-shrink:0;padding:16px;">

                  <!-- Başlık -->
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
                    <div style="width:28px;height:28px;background:#1E3A5F;border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                      <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#60A5FA" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                    </div>
                    <span style="font-size:12px;font-weight:800;color:#E2E8F0;text-transform:uppercase;letter-spacing:0.07em;">Analiz Özeti</span>
                  </div>

                  <!-- Stat Grid -->
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">

                    <!-- TESPİTLER -->
                    <div style="background:#1E293B;border-radius:12px;padding:12px 12px 10px;">
                      <div style="font-size:9px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">TESPİTLER</div>
                      <div id="kpStatToplam" style="font-size:26px;font-weight:800;color:#FFFFFF;line-height:1;letter-spacing:-0.5px;">0</div>
                      <div id="kpStatToplamDelta" style="font-size:10px;color:#10B981;margin-top:5px;font-weight:600;"></div>
                    </div>

                    <!-- İHLALLER -->
                    <div style="background:#1E293B;border-radius:12px;padding:12px 12px 10px;position:relative;">
                      <div style="font-size:9px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">İHLALLER</div>
                      <div id="kpStatIhlal" style="font-size:26px;font-weight:800;color:#EF4444;line-height:1;letter-spacing:-0.5px;">0</div>
                      <div id="kpStatIhlalDelta" style="font-size:10px;color:#EF4444;margin-top:5px;font-weight:700;"></div>
                      <div style="position:absolute;top:10px;right:10px;width:20px;height:20px;background:#F97316;border-radius:50%;display:flex;align-items:center;justify-content:center;">
                        <svg width="10" height="10" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="3"><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                      </div>
                    </div>

                    <!-- MANUEL KANITLAR (AI) -->
                    <div style="background:#1E293B;border-radius:12px;padding:12px 12px 10px;">
                      <div style="font-size:9px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">MANUEL KANITLAR</div>
                      <div id="kpStatAi" style="font-size:26px;font-weight:800;color:#FFFFFF;line-height:1;letter-spacing:-0.5px;">0</div>
                    </div>

                    <!-- MANUEL KANITLAR -->
                    <div style="background:#1E293B;border-radius:12px;padding:12px 12px 10px;">
                      <div style="font-size:9px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">MANUEL KANITLAR</div>
                      <div id="kpStatManuel" style="font-size:26px;font-weight:800;color:#FFFFFF;line-height:1;letter-spacing:-0.5px;">0</div>
                    </div>

                  </div>

                  <!-- Haftalık Limit -->
                  <div style="background:#1E293B;border-radius:10px;padding:10px 12px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                      <span style="font-size:10px;font-weight:600;color:#64748B;">Haftalık Limit</span>
                      <span id="kpLimitText" style="font-size:10px;font-weight:700;color:#CBD5E1;">0 / 3</span>
                    </div>
                    <div style="height:4px;background:#334155;border-radius:2px;overflow:hidden;">
                      <div id="kpLimitBar" style="height:100%;background:#F97316;border-radius:2px;transition:width 0.4s;width:0%;"></div>
                    </div>
                    <div style="font-size:10px;color:#475569;margin-top:5px;">Pro/Max planla sınırsız analiz yapın</div>
                  </div>
                </div><!-- /analiz özeti kartı -->


              </div><!-- /sağ panel wrapper -->

            </div><!-- /iki sütun -->

            <!-- ══ YENİ KAMERA EKLE MODALİ ══ -->
            <div id="yeniKameraModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:9000;align-items:center;justify-content:center;backdrop-filter:blur(4px);">
              <div style="background:#FFFFFF;border-radius:20px;padding:28px;width:440px;max-width:94vw;box-shadow:0 20px 60px rgba(0,0,0,0.3);animation:kpSlideUp 0.2s ease;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
                  <div>
                    <div style="font-size:17px;font-weight:800;color:#0F172A;">Yeni Kamera Ekle</div>
                    <div style="font-size:12px;color:#64748B;margin-top:2px;">IP kamera veya RTSP akış adresi tanımlayın</div>
                  </div>
                  <button onclick="yeniKameraKapat()" style="background:#F1F5F9;border:none;width:32px;height:32px;border-radius:8px;cursor:pointer;font-size:18px;color:#475569;display:flex;align-items:center;justify-content:center;">×</button>
                </div>
                <div style="display:flex;flex-direction:column;gap:12px;">
                  <div>
                    <label style="font-size:12px;font-weight:600;color:#475569;display:block;margin-bottom:5px;">Kamera Adı *</label>
                    <input id="ykAd" placeholder="örn. CAM-01 Ana Giriş" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;font-size:13px;color:#0F172A;background:#F8FAFC;outline:none;box-sizing:border-box;font-family:inherit;"
                      onfocus="this.style.borderColor='#F97316'" onblur="this.style.borderColor='#E2E8F0'"/>
                  </div>
                  <div>
                    <label style="font-size:12px;font-weight:600;color:#475569;display:block;margin-bottom:5px;">Bağlantı URL'si</label>
                    <input id="ykUrl" placeholder="rtsp://192.168.1.x:554/stream veya http://..." style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;font-size:13px;color:#0F172A;background:#F8FAFC;outline:none;box-sizing:border-box;font-family:inherit;"
                      onfocus="this.style.borderColor='#F97316'" onblur="this.style.borderColor='#E2E8F0'"/>
                  </div>
                  <div>
                    <label style="font-size:12px;font-weight:600;color:#475569;display:block;margin-bottom:5px;">Konum / Bölge</label>
                    <input id="ykKonum" placeholder="örn. Kuzey Cephe, B Blok Giriş" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;font-size:13px;color:#0F172A;background:#F8FAFC;outline:none;box-sizing:border-box;font-family:inherit;"
                      onfocus="this.style.borderColor='#F97316'" onblur="this.style.borderColor='#E2E8F0'"/>
                  </div>
                  <div>
                    <label style="font-size:12px;font-weight:600;color:#475569;display:block;margin-bottom:5px;">Kamera Türü</label>
                    <select id="ykTip" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;font-size:13px;color:#0F172A;background:#F8FAFC;outline:none;">
                      <option value="ip">IP Kamera</option>
                      <option value="rtsp">RTSP Akış</option>
                      <option value="http">HTTP / MJPEG</option>
                      <option value="usb">USB / Webcam</option>
                    </select>
                  </div>
                </div>
                <div style="display:flex;gap:10px;margin-top:20px;">
                  <button onclick="yeniKameraKaydet()" id="ykKaydetBtn" style="flex:1;background:#F97316;border:none;color:white;font-size:14px;font-weight:700;padding:11px;border-radius:10px;cursor:pointer;transition:background 0.15s;"
                    onmouseover="this.style.background='#ea6010'" onmouseout="this.style.background='#F97316'">Kamera Kaydet</button>
                  <button onclick="yeniKameraKapat()" style="padding:11px 18px;background:#F1F5F9;border:none;color:#475569;font-size:14px;font-weight:600;border-radius:10px;cursor:pointer;">İptal</button>
                </div>
              </div>
            </div>

          </div><!-- /kameraPage -->

          <!-- ══════ AYARLAR SAYFASI ══════ -->
          <div id="ayarlarPage" style="display:none;flex:1;overflow:hidden;background:#F8FAFC;">
            <div style="display:flex;height:100%;">

              <!-- Sol Nav -->
              <div id="ayarlarNav" style="width:190px;flex-shrink:0;background:#FFFFFF;border-right:1px solid #E2E8F0;display:flex;flex-direction:column;overflow:hidden;">
                <div style="flex:1;padding:8px 8px 8px;overflow-y:auto;display:flex;flex-direction:column;gap:2px;">

                  <div id="ayarlarBtn-profil" onclick="ayarlarKategoriGoster('profil')"
                    style="display:flex;align-items:center;gap:9px;padding:8px 10px;font-size:13px;font-weight:500;border-radius:8px;cursor:pointer;color:#64748B;transition:all 0.15s;white-space:nowrap;">
                    <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8" style="flex-shrink:0;"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                    Profil &amp; Hesap
                  </div>

                  <div id="ayarlarBtn-santiye" onclick="ayarlarKategoriGoster('santiye')"
                    style="display:flex;align-items:center;gap:9px;padding:8px 10px;font-size:13px;font-weight:500;border-radius:8px;cursor:pointer;color:#64748B;transition:all 0.15s;white-space:nowrap;">
                    <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8" style="flex-shrink:0;"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
                    Şantiye Varsayılanları
                  </div>

                  <div id="ayarlarBtn-ai" onclick="ayarlarKategoriGoster('ai')"
                    style="display:flex;align-items:center;gap:9px;padding:8px 10px;font-size:13px;font-weight:500;border-radius:8px;cursor:pointer;color:#64748B;transition:all 0.15s;white-space:nowrap;">
                    <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8" style="flex-shrink:0;"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>
                    AI Asistan
                  </div>

                  <div id="ayarlarBtn-bildirim" onclick="ayarlarKategoriGoster('bildirim')"
                    style="display:flex;align-items:center;gap:9px;padding:8px 10px;font-size:13px;font-weight:500;border-radius:8px;cursor:pointer;color:#64748B;transition:all 0.15s;white-space:nowrap;">
                    <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8" style="flex-shrink:0;"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
                    Bildirim Kanalları
                  </div>

                  <div id="ayarlarBtn-plan" onclick="ayarlarKategoriGoster('plan')"
                    style="display:flex;align-items:center;gap:9px;padding:8px 10px;font-size:13px;font-weight:500;border-radius:8px;cursor:pointer;color:#64748B;transition:all 0.15s;white-space:nowrap;">
                    <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8" style="flex-shrink:0;"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
                    Plan &amp; Ödeme
                  </div>

                  <div id="ayarlarBtn-guvenlik" onclick="ayarlarKategoriGoster('guvenlik')"
                    style="display:flex;align-items:center;gap:9px;padding:8px 10px;font-size:13px;font-weight:500;border-radius:8px;cursor:pointer;color:#64748B;transition:all 0.15s;white-space:nowrap;">
                    <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8" style="flex-shrink:0;"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                    Güvenlik &amp; Gizlilik
                  </div>

                </div>
              </div>

              <!-- Sağ İçerik -->
              <div id="ayarlarIcerik" style="flex:1;overflow-y:auto;padding:32px 40px;background:#FFFFFF;color:#1E293B;">
              </div>

            </div>
          </div><!-- /ayarlarPage -->

          <!-- ══════ ARŞİV SAYFASI ══════ -->
          <div id="arsivPage" style="display:none;flex:1;flex-direction:column;overflow:hidden;background:#F1F5F9;">

            <!-- Üst Başlık -->
            <div style="background:#FFFFFF;border-bottom:1px solid #E2E8F0;padding:20px 24px;flex-shrink:0;">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
                <div>
                  <div style="font-size:20px;font-weight:800;color:#0F172A;">Arşiv</div>
                  <div style="font-size:12px;color:#64748B;margin-top:2px;" id="arsivSubtitle">Yükleniyor...</div>
                </div>
                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 14px;text-align:center;">
                    <div id="arsivStatRapor" style="font-size:18px;font-weight:800;color:#0F172A;">—</div>
                    <div style="font-size:10px;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">AI Raporu</div>
                  </div>
                  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 14px;text-align:center;">
                    <div id="arsivStatKamera" style="font-size:18px;font-weight:800;color:#0F172A;">—</div>
                    <div style="font-size:10px;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">Kamera Analizi</div>
                  </div>
                  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 14px;text-align:center;">
                    <div id="arsivStatToplam" style="font-size:18px;font-weight:800;color:#F97316;">—</div>
                    <div style="font-size:10px;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">Toplam</div>
                  </div>
                </div>
              </div>
              <!-- Filtre + Arama -->
              <div style="display:flex;gap:10px;margin-top:14px;align-items:center;flex-wrap:wrap;">
                <div style="display:flex;gap:6px;">
                  <button id="arsivTabTumu" onclick="arsivTabSec('tumu')"
                    style="font-size:12px;font-weight:700;padding:6px 14px;border-radius:8px;border:1.5px solid #0F172A;background:#0F172A;color:white;cursor:pointer;transition:all 0.15s;">Tümü</button>
                  <button id="arsivTabRapor" onclick="arsivTabSec('rapor')"
                    style="font-size:12px;font-weight:700;padding:6px 14px;border-radius:8px;border:1.5px solid #E2E8F0;background:white;color:#64748B;cursor:pointer;transition:all 0.15s;">AI Raporları</button>
                  <button id="arsivTabKamera" onclick="arsivTabSec('kamera')"
                    style="font-size:12px;font-weight:700;padding:6px 14px;border-radius:8px;border:1.5px solid #E2E8F0;background:white;color:#64748B;cursor:pointer;transition:all 0.15s;">Kamera Analizleri</button>
                </div>
                <div style="position:relative;flex:1;min-width:180px;max-width:320px;">
                  <svg style="position:absolute;left:10px;top:50%;transform:translateY(-50%);pointer-events:none;" width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#94A3B8" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
                  <input id="arsivAramaInput" type="text" placeholder="Kayıt ara..." oninput="arsivFiltrele()"
                    style="width:100%;padding:7px 12px 7px 30px;border:1.5px solid #E2E8F0;border-radius:8px;font-size:12px;color:#0F172A;background:#F8FAFC;outline:none;box-sizing:border-box;font-family:inherit;">
                </div>
              </div>
            </div>

            <!-- Kayıt Listesi -->
            <div style="flex:1;overflow-y:auto;padding:20px 24px;">
              <div id="arsivIcerik">
                <div style="text-align:center;padding:60px 20px;color:#94A3B8;">
                  <div style="font-size:32px;margin-bottom:8px;">📁</div>
                  <div style="font-size:14px;font-weight:600;">Yükleniyor...</div>
                </div>
              </div>
            </div>
          </div><!-- /arsivPage -->

        </div><!-- /mainArea -->

      </div><!-- /bodyRow -->
    </div><!-- /app -->

</div><!-- /mainApp -->

<!-- Gizli fotoğraf input -->
<input type="file" id="photoInput" accept="image/*" style="display:none" onchange="fotoYukle(this)">
<input type="file" id="fileInput" accept="image/*" style="display:none" onchange="resimSecildi(event)">

<!-- ===== KAMERA MODALİ ===== -->
<div id="kameraModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
    <div style="background:rgba(8,16,32,0.97);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px); border-radius:20px; padding:25px; width:90%; max-width:480px; border:1px solid rgba(230,126,34,0.3);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
            <h3 style="color:#e67e22; margin:0;">📸 Kamera Analizi</h3>
            <button onclick="kameraKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
        </div>
        <input type="hidden" id="kameraAnalizTipi" value="genel">
        <video id="kameraVideo" autoplay playsinline style="width:100%; border-radius:12px; background:#000; max-height:300px;"></video>
        <canvas id="kameraCanvas" style="display:none;"></canvas>
        <div style="display:flex; gap:10px; margin-top:15px;">
            <button onclick="fotografCek()" style="flex:1; background:#e67e22; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">📷 Fotoğraf Çek</button>
            <label style="flex:1; background:#2c3e50; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold; text-align:center;">
                📂 Yükle
                <input type="file" accept="image/*" onchange="kameraFotoYukle(event)" style="display:none;">
            </label>
        </div>
    </div>
</div>

<!-- ARŞİV DETAY MODALİ (satır içi görüntüleme) -->
<div id="arsivDetayModal" style="display:none;position:fixed;inset:0;background:rgba(15,23,42,0.7);z-index:9999;align-items:center;justify-content:center;padding:20px;backdrop-filter:blur(6px);">
  <div style="background:#FFFFFF;border-radius:20px;width:100%;max-width:640px;max-height:88vh;display:flex;flex-direction:column;box-shadow:0 24px 64px rgba(0,0,0,0.3);overflow:hidden;">
    <div style="background:#0D1117;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;">
      <span id="arsivDetayBaslik" style="color:#F1F5F9;font-weight:700;font-size:1rem;">Kayıt Detayı</span>
      <button onclick="arsivDetayKapat()" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:#94A3B8;width:30px;height:30px;border-radius:8px;cursor:pointer;font-size:1rem;display:flex;align-items:center;justify-content:center;">✕</button>
    </div>
    <div id="arsivDetayIcerik" style="flex:1;overflow-y:auto;padding:20px;font-size:13px;color:#1E293B;line-height:1.8;"></div>
  </div>
</div>

<!-- ===== MÜHENDİSLİK PANELİ ===== -->
<div id="sidebarPanel">
  <!-- Header -->
  <div style="background:#0D1117; padding:18px 20px; display:flex; align-items:center; justify-content:space-between; flex-shrink:0;">
    <div>
      <div style="font-size:16px; font-weight:700; color:#F1F5F9;">🏗️ Mühendislik Paneli</div>
      <div style="font-size:11px; color:#64748B; margin-top:2px;">Profesyonel saha hesapları</div>
    </div>
    <button onclick="toggleSidebar()"
      style="background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); color:#94A3B8; width:32px; height:32px; border-radius:8px; cursor:pointer; font-size:16px; display:flex; align-items:center; justify-content:center; transition:all 0.15s;"
      onmouseover="this.style.background='rgba(255,255,255,0.15)'" onmouseout="this.style.background='rgba(255,255,255,0.08)'">✕</button>
  </div>

  <!-- İçerik -->
  <div style="padding:8px 0 32px; overflow-y:auto; flex:1;">
    <div class="category-title">STRÜKTÜR & KABA YAPI</div>
    <div class="tool-card" onclick="runCalc('beton')"><h4>🧱 Beton Metrajı</h4><small>Hacim ve Mikser</small></div>
    <div class="tool-card" onclick="runCalc('demir_ag')"><h4>⚖️ Donatı Ağırlığı</h4><small>kg/Ton</small></div>
    <div class="tool-card" onclick="runCalc('as_alan')"><h4>📏 Donatı Alanı (As)</h4><small>Adet ve Çapa Göre Kesit</small></div>
    <div class="tool-card" onclick="runCalc('etriye')"><h4>🌀 Etriye Boyu</h4><small>Kanca ve Paspayı Dahil</small></div>

    <div class="category-title">MİMARİ & İNCE İŞLER</div>
    <div class="tool-card" onclick="runCalc('tugla')"><h4>🧱 Tuğla Hesabı</h4><small>Duvar m²'den Adet Tahmini</small></div>
    <div class="tool-card" onclick="runCalc('seramik')"><h4>📐 Seramik & Parke</h4><small>Fireli Paket Metrajı</small></div>
    <div class="tool-card" onclick="runCalc('boya')"><h4>🎨 Boya & Sıva</h4><small>Yüzeyden Sarfiyat Hesabı</small></div>

    <div class="category-title">ALTYAPI & HAFRİYAT</div>
    <div class="tool-card" onclick="runCalc('kubaj')"><h4>🚜 Hafriyat Küpajı</h4><small>Kazı ve Dolgu Hacmi</small></div>
    <div class="tool-card" onclick="runCalc('egim')"><h4>📐 Eğim & Açı</h4><small>Rampa ve Şev Analizi</small></div>
  </div>
</div>

<!-- ===== HESAPLAMA MODALİ ===== -->
<div id="inputModal" class="modal-overlay">
  <div class="modal-content">
    <div class="modal-header">
      <span id="modalTitle" class="modal-header-title">Hesaplama</span>
      <button class="modal-header-close" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body">
      <div id="modalBody"></div>
      <div id="modalResult" class="modal-result">
        <div style="font-size:0.7rem;font-weight:700;color:#F97316;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">SONUÇ</div>
        <div id="modalResultValue" class="modal-result-value">—</div>
        <div id="modalResultDetail" class="modal-result-detail"></div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="modal-btn btn-cancel" onclick="closeModal()">İPTAL</button>
      <button id="modalHesaplaBtn" class="modal-btn btn-confirm" onclick="submitModal()">HESAPLA</button>
    </div>
  </div>
</div>

<!-- ===== GÜNLÜK RAPOR MODALİ ===== -->
<div id="gunlukRaporModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.6); z-index:9999; align-items:center; justify-content:center; padding:16px; backdrop-filter:blur(4px);">
  <div style="background:#FFFFFF; border-radius:20px; width:100%; max-width:460px; overflow:hidden; box-shadow:0 24px 64px rgba(0,0,0,0.35); max-height:92vh; display:flex; flex-direction:column;">

    <!-- Dark Header -->
    <div style="background:#0D1117; padding:16px 20px; display:flex; align-items:center; justify-content:space-between; flex-shrink:0;">
      <div style="display:flex; align-items:center; gap:10px;">
        <div style="width:36px; height:36px; background:rgba(255,255,255,0.08); border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <svg width="22" height="22" viewBox="0 0 100 100" fill="none" stroke="#CBD5E1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="35" y1="80" x2="38" y2="15"/><line x1="48" y1="80" x2="45" y2="15"/>
            <line x1="35" y1="80" x2="48" y2="68"/><line x1="48" y1="80" x2="35" y2="68"/>
            <line x1="35" y1="68" x2="48" y2="56"/><line x1="48" y1="68" x2="35" y2="56"/>
            <line x1="30" y1="80" x2="52" y2="80"/>
            <line x1="38" y1="15" x2="16" y2="15"/><rect x="11" y="12" width="8" height="6" rx="1"/>
            <line x1="45" y1="15" x2="84" y2="15"/>
            <line x1="38" y1="15" x2="56" y2="10"/><line x1="56" y1="10" x2="84" y2="15"/>
            <circle cx="41" cy="14" r="2" fill="#CBD5E1" stroke="none"/>
            <line x1="84" y1="15" x2="84" y2="28"/>
            <circle cx="84" cy="31" r="3" fill="none" stroke="#CBD5E1" stroke-width="2"/>
            <line x1="84" y1="34" x2="84" y2="50"/>
          </svg>
        </div>
        <span style="color:white; font-size:1rem; font-weight:700;">Günlük Rapor Oluştur</span>
      </div>
      <button onclick="gunlukRaporKapat()" style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:white; width:30px; height:30px; border-radius:8px; cursor:pointer; font-size:1rem; display:flex; align-items:center; justify-content:center; line-height:1;">✕</button>
    </div>

    <!-- Form Body -->
    <div style="padding:20px; overflow-y:auto; display:flex; flex-direction:column; gap:16px;">

      <!-- Tarih -->
      <div>
        <label style="display:block; font-size:0.82rem; color:#374151; font-weight:600; margin-bottom:6px;">Tarih</label>
        <div class="gr-field-wrap">
          <div class="gr-field-icon">📅</div>
          <input type="date" id="grTarih" style="flex:1; border:none !important; outline:none; padding:10px 12px; font-size:0.88rem; color:#0F172A !important; background:transparent !important; font-family:inherit;">
        </div>
      </div>

      <!-- Çalışan İşçi Sayısı -->
      <div>
        <label style="display:block; font-size:0.82rem; color:#374151; font-weight:600; margin-bottom:6px;">Çalışan İşçi Sayısı</label>
        <div class="gr-field-wrap">
          <div class="gr-field-icon">👷</div>
          <input type="number" id="grIsci" placeholder="0" min="0" style="flex:1; border:none !important; outline:none; padding:10px 12px; font-size:0.88rem; color:#0F172A !important; background:transparent !important; font-family:inherit;">
        </div>
      </div>

      <!-- Yapılan İşler -->
      <div>
        <label style="display:flex; align-items:center; gap:6px; font-size:0.82rem; color:#374151; font-weight:600; margin-bottom:6px;">
          <span>📋</span> Yapılan İşler
        </label>
        <textarea id="grYapilanlar" placeholder="Örn: 3. kat döşeme betonu döküldü..."></textarea>
      </div>

      <!-- Sorunlar / Riskler -->
      <div>
        <label style="display:flex; align-items:center; gap:6px; font-size:0.82rem; color:#374151; font-weight:600; margin-bottom:6px;">
          <span>⚠️</span> Sorunlar / Riskler
        </label>
        <textarea id="grSorunlar" placeholder="Örn: Malzeme gecikmesi, hava koşulları..."></textarea>
      </div>

      <!-- Yarın Yapılacaklar -->
      <div>
        <label style="display:flex; align-items:center; gap:6px; font-size:0.82rem; color:#374151; font-weight:600; margin-bottom:6px;">
          <span>➡️</span> Yarın Yapılacaklar
        </label>
        <textarea id="grYarin" placeholder="Örn: 4. kat kolon kalıpları kurulacak..."></textarea>
      </div>

      <!-- İSG Durumu -->
      <div>
        <label style="display:flex; align-items:center; gap:6px; font-size:0.82rem; color:#374151; font-weight:600; margin-bottom:10px;">
          <span>🦺</span> İSG Durumu
        </label>
        <div style="display:flex; align-items:center; gap:10px;">
          <label class="sfToggle">
            <input type="checkbox" id="grIsgToggle" checked onchange="grIsgDegisti(this)">
            <span class="sfToggleSlider"></span>
          </label>
          <span id="grIsgLabel" style="font-size:0.88rem; color:#374151; font-weight:500;">Uygun</span>
          <select id="grIsg" style="display:none;">
            <option value="iyi">iyi</option>
            <option value="orta">orta</option>
            <option value="kotu">kötü</option>
          </select>
        </div>
      </div>

      <!-- Sonuç alanı -->
      <div id="gunlukRaporSonuc"></div>

    </div>

    <!-- Footer Button -->
    <div style="padding:16px 20px; flex-shrink:0; border-top:1px solid #F1F5F9;">
      <button onclick="gunlukRaporOlustur()" style="width:100%; padding:14px; background:#0D1117; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:700; font-size:0.92rem;">Yapay Zeka ile Raporu Tamamla</button>
    </div>

  </div>
</div>

<!-- PRO MODAL -->
<div id="proModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.8); z-index:9999; align-items:center; justify-content:center;">
    <div style="background:#1a1a2e; border:1px solid #e67e22; border-radius:20px; padding:35px; max-width:460px; width:90%; position:relative;">
        <button onclick="proModalKapat()" style="position:absolute; top:15px; right:18px; background:none; border:none; color:#aaa; font-size:1.5rem; cursor:pointer;">✖</button>
        <h2 style="color:#e67e22; margin:0 0 6px 0; font-size:1.4rem;">⚡ BuildingAI Pro</h2>
        <p style="color:#aaa; margin:0 0 20px 0; font-size:0.9rem;">Tüm özelliklere sınırsız erişim için Pro plana geçin.</p>
        <div style="background:rgba(230,126,34,0.08); border:1px solid rgba(230,126,34,0.3); border-radius:14px; padding:18px; margin-bottom:20px;">
            <div style="font-size:2rem; font-weight:800; color:white; margin-bottom:4px;">$10 <span style="font-size:0.9rem; color:#aaa; font-weight:400;">/ay</span></div>
            <ul style="color:#ccc; font-size:0.88rem; margin:10px 0 0 0; padding-left:18px; line-height:1.8;">
                <li>Sınırsız AI sorgusu</li><li>Haftalık 20 kamera analizi</li>
                <li>Günde 5 sesli rapor</li><li>Günde 5 günlük rapor</li><li>50 kayıtlık arşiv erişimi</li>
            </ul>
        </div>
        <p style="color:#aaa; font-size:0.88rem; margin:0 0 10px 0;">Aşağıdaki IBAN'a <b style="color:white;">$10</b> gönderin, açıklamaya e-posta adresinizi yazın:</p>
        <div style="background:#111; border:1px solid #333; border-radius:10px; padding:12px; display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
            <span id="ibanText" style="color:#f1c40f; font-family:monospace; font-size:0.9rem; word-break:break-all;">TR80 0001 0090 1095 7865 2050 01</span>
            <button onclick="ibanKopyala()" style="background:#e67e22; border:none; color:white; border-radius:8px; padding:6px 12px; cursor:pointer; font-size:0.8rem; white-space:nowrap; margin-left:10px;">Kopyala</button>
        </div>
        <p style="color:#777; font-size:0.8rem; margin:0 0 18px 0;">Ad:Mehmet Akif Erdemir</p>
        <button onclick="odemeBildirimi()" style="width:100%; padding:14px; background:linear-gradient(135deg,#27ae60,#2ecc71); border:none; color:white; border-radius:14px; cursor:pointer; font-weight:700; font-size:1rem;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">✅ Ödemeyi Yaptım</button>
        <div id="odemeMsg" style="margin-top:12px; text-align:center; font-size:0.88rem;"></div>
    </div>
</div>

<!-- FİYAT TAKİBİ MODALİ -->
<div id="fiyatModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
  <div style="background:rgba(8,16,32,0.97);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px); border:1px solid rgba(249,115,22,0.3); border-radius:24px; padding:28px; width:92%; max-width:640px; max-height:88vh; overflow-y:auto;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <h3 style="color:var(--primary); margin:0; font-size:1.2rem;">📊 Malzeme Fiyat Takibi</h3>
      <button onclick="fiyatModalKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
    </div>
    <div id="uyarilar" style="margin-bottom:16px;"></div>
    <div id="fiyatKartlari" style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:20px;"></div>
    <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; margin-bottom:20px;">
      <div style="color:var(--primary); font-weight:700; font-size:0.85rem; margin-bottom:12px;">📈 Fiyat Geçmişi</div>
      <div style="display:flex; gap:8px; margin-bottom:12px; flex-wrap:wrap;">
        <select id="grafMalzeme" onchange="grafikYukle()" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:8px 12px; border-radius:8px; outline:none; font-size:0.85rem;">
          <option value="demir">Demir</option><option value="cimento">Çimento</option>
          <option value="beton">Beton</option><option value="tugla">Tuğla</option><option value="kum">Kum</option>
        </select>
        <select id="grafGun" onchange="grafikYukle()" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:8px 12px; border-radius:8px; outline:none; font-size:0.85rem;">
          <option value="90" selected>Son 90 Gün</option><option value="365">Son 365 Gün</option>
        </select>
      </div>
      <canvas id="fiyatGrafik" height="160"></canvas>
      <div id="grafBosMesaj" style="text-align:center; color:#555; font-size:0.85rem; padding:40px 0; display:none;">Henüz yeterli veri yok.</div>
    </div>
    <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px;">
      <div style="color:var(--primary); font-weight:700; font-size:0.85rem; margin-bottom:12px;">➕ Fiyat Gir / Güncelle</div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <select id="fiyatMalzeme" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
          <option value="demir">Demir (ton)</option><option value="cimento">Çimento (çuval)</option>
          <option value="beton">Beton (m³)</option><option value="tugla">Tuğla (adet)</option><option value="kum">Kum (ton)</option>
        </select>
        <input type="number" id="fiyatDeger" placeholder="Fiyat (₺)" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
      </div>
      <select id="fiyatSehir" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none; margin-bottom:10px;">
        <option value="genel">Genel (Türkiye Ortalaması)</option>
        <option value="Istanbul">İstanbul</option><option value="Ankara">Ankara</option>
        <option value="Izmir">İzmir</option><option value="Sivas">Sivas</option><option value="Bursa">Bursa</option>
      </select>
      <button onclick="fiyatKaydet()" style="width:100%; padding:12px; background:var(--primary); color:white; border:none; border-radius:10px; cursor:pointer; font-weight:700;">💾 Fiyatı Kaydet</button>
      <div id="fiyatMsg" style="margin-top:8px; font-size:0.85rem; text-align:center;"></div>
    </div>
  </div>
</div>

<!-- STOK TAKİBİ MODALİ -->
<div id="stokModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
  <div style="background:rgba(8,16,32,0.97);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px); border:1px solid rgba(249,115,22,0.3); border-radius:24px; padding:28px; width:92%; max-width:680px; max-height:90vh; overflow-y:auto;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <h3 style="color:var(--primary); margin:0; font-size:1.2rem;">📦 Malzeme Stok Takibi</h3>
      <button onclick="stokModalKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
    </div>
    <div id="stokUyarilar" style="margin-bottom:16px;"></div>
    <div id="stokKartlar" style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:20px;"></div>
    <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; margin-bottom:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="color:var(--primary); font-weight:700; font-size:0.85rem;">📋 Hareket Geçmişi</div>
        <select id="stokGecmisMalzeme" onchange="stokGecmisYukle()" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:6px 10px; border-radius:8px; outline:none; font-size:0.8rem;">
          <option value="demir">Demir</option><option value="cimento">Çimento</option>
          <option value="beton">Beton</option><option value="tugla">Tuğla</option><option value="kum">Kum</option>
        </select>
      </div>
      <div id="stokGecmisListe" style="max-height:200px; overflow-y:auto;"></div>
    </div>
    <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px;">
      <div style="color:var(--primary); font-weight:700; font-size:0.85rem; margin-bottom:12px;">➕ Malzeme Girişi / Çıkışı</div>
      <select id="stokSantiye" required onchange="stokSantiyeDegisti()" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(249,115,22,0.4); color:white; padding:10px; border-radius:8px; outline:none; margin-bottom:10px;">
        <option value="">📍 Şantiye Seçin... (zorunlu)</option>
      </select>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <select id="stokMalzeme" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
          <option value="demir">Demir</option><option value="cimento">Çimento</option>
          <option value="beton">Beton</option><option value="tugla">Tuğla</option><option value="kum">Kum</option>
        </select>
        <select id="stokTip" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
          <option value="giris">📥 Giriş (Geldi)</option><option value="cikis">📤 Çıkış (Kullanıldı)</option>
        </select>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <input type="number" id="stokMiktar" placeholder="Miktar" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
        <select id="stokBirim" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
          <option value="ton">Ton</option><option value="m³">m³</option>
          <option value="adet">Adet</option><option value="çuval">Çuval</option>
        </select>
      </div>
      <input type="text" id="stokTedarikci" placeholder="Tedarikçi (opsiyonel)" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none; margin-bottom:10px; box-sizing:border-box;">
      <input type="number" id="stokFiyat" placeholder="Birim Fiyat ₺ (opsiyonel)" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none; margin-bottom:10px; box-sizing:border-box;">
      <input type="text" id="stokNotlar" placeholder="Notlar (opsiyonel)" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none; margin-bottom:10px; box-sizing:border-box;">
      <button onclick="stokKaydet()" style="width:100%; padding:12px; background:var(--primary); color:white; border:none; border-radius:10px; cursor:pointer; font-weight:700;">💾 Kaydet</button>
      <div id="stokMsg" style="margin-top:8px; font-size:0.85rem; text-align:center;"></div>
    </div>
  </div>
</div>

<!-- DEPREM ANALİZİ MODALİ -->
<div id="depremModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
  <div style="background:rgba(8,16,32,0.97);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px); border:1px solid rgba(249,115,22,0.3); border-radius:24px; padding:28px; width:95%; max-width:900px; max-height:92vh; overflow-y:auto;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <h3 style="color:var(--primary); margin:0; font-size:1.2rem;">🌍 Deprem & Jeolojik Risk Analizi</h3>
      <button onclick="depremModalKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
    </div>
    <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; margin-bottom:16px;">
      <div style="color:var(--primary); font-weight:700; font-size:0.85rem; margin-bottom:12px;">📍 Şantiye Konumu</div>
      <div style="display:grid; grid-template-columns:1fr auto; gap:10px; margin-bottom:10px;">
        <input type="text" id="depremAdres" placeholder="Şantiye adresi veya şehir (örn: Sivas, Merkez)" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none; font-size:0.9rem;">
        <button onclick="depremKonumBul()" style="padding:10px 16px; background:var(--primary); color:white; border:none; border-radius:8px; cursor:pointer; font-weight:700; white-space:nowrap;">📍 Konumu Bul</button>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr auto; gap:10px;">
        <input type="number" id="depremLat" placeholder="Enlem (ör: 39.74)" step="0.0001" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
        <input type="number" id="depremLon" placeholder="Boylam (ör: 37.01)" step="0.0001" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
        <button onclick="depremAnalizBaslat()" style="padding:10px 16px; background:#8b5cf6; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:700; white-space:nowrap;">🔍 Analiz Et</button>
      </div>
      <div id="depremKonumMsg" style="margin-top:8px; font-size:0.8rem; color:#aaa;"></div>
    </div>
    <div style="border-radius:14px; overflow:hidden; margin-bottom:16px; border:1px solid rgba(255,255,255,0.08);">
      <div id="depremHarita" style="height:320px; width:100%;"></div>
    </div>
    <div id="depremAnalizSonuc" style="display:none;">
      <div style="display:grid; grid-template-columns:auto 1fr; gap:16px; background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; margin-bottom:16px; align-items:center;">
        <div style="position:relative; width:90px; height:90px;">
          <svg width="90" height="90" style="transform:rotate(-90deg)">
            <circle cx="45" cy="45" r="36" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="8"/>
            <circle id="riskCircle" cx="45" cy="45" r="36" fill="none" stroke="#ef4444" stroke-width="8" stroke-dasharray="226" stroke-dashoffset="226" stroke-linecap="round" style="transition:stroke-dashoffset 1.5s ease;"/>
          </svg>
          <div style="position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center;">
            <span id="riskSkorText" style="color:white; font-size:1.3rem; font-weight:900; line-height:1;">0</span>
            <span style="color:#aaa; font-size:0.6rem;">RİSK</span>
          </div>
        </div>
        <div>
          <div id="riskSeviyeText" style="font-size:1.4rem; font-weight:900; margin-bottom:4px;"></div>
          <div id="riskZeminText" style="color:#aaa; font-size:0.85rem; margin-bottom:6px;"></div>
          <div id="riskOzetText" style="color:#ccc; font-size:0.82rem; line-height:1.5;"></div>
        </div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px;">
        <div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.2); border-radius:12px; padding:14px;">
          <div style="color:#fca5a5; font-weight:700; font-size:0.8rem; margin-bottom:10px;">⚡ EN YAKIN FAY HATTI</div>
          <div id="fayAd" style="color:white; font-weight:700; font-size:0.9rem; margin-bottom:4px;"></div>
          <div id="fayMesafe" style="color:#ef4444; font-size:1.1rem; font-weight:800; margin-bottom:4px;"></div>
          <div id="fayTip" style="color:#aaa; font-size:0.78rem;"></div>
          <div id="faySonDeprem" style="color:#aaa; font-size:0.78rem; margin-top:4px;"></div>
        </div>
        <div style="background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2); border-radius:12px; padding:14px;">
          <div style="color:#a5b4fc; font-weight:700; font-size:0.8rem; margin-bottom:10px;">📐 TBDY 2018 PARAMETRELERİ</div>
          <div id="tbdyParams" style="font-size:0.82rem; line-height:1.8;"></div>
        </div>
      </div>
      <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; margin-bottom:16px;">
        <div style="color:var(--primary); font-weight:700; font-size:0.85rem; margin-bottom:12px;">📋 AFAD Son Depremler (200km çevre)</div>
        <div id="sonDepremlerListe" style="max-height:180px; overflow-y:auto;"></div>
      </div>
      <div style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); border-radius:14px; padding:16px;">
        <div style="color:#fcd34d; font-weight:700; font-size:0.85rem; margin-bottom:10px;">💡 MÜHENDİSLİK ÖNERİLERİ</div>
        <div id="depremOneriler"></div>
      </div>
    </div>
    <div id="depremLoading" style="display:none; text-align:center; padding:40px;">
      <div style="font-size:2rem; margin-bottom:12px;">🔍</div>
      <div style="color:#aaa;">AFAD verileri çekiliyor, AI analiz yapıyor...</div>
    </div>
  </div>
</div>

<!-- ŞANTİYELERİM MODAL — Premium SaaS · CartoDB Harita · Chart.js Grafikler -->
<div id="santiyeModal" style="display:none; position:fixed; inset:0; z-index:9000; overflow-y:auto; padding:24px; background:rgba(3,7,18,0.93); backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px);">
  <div style="max-width:1140px; margin:0 auto; background:rgba(6,11,26,0.98); border-radius:24px; border:1px solid rgba(99,102,241,0.18); overflow:hidden; box-shadow:0 0 100px rgba(99,102,241,0.10), 0 32px 80px rgba(0,0,0,0.80);">

    <!-- ── HEADER ── -->
    <div style="background:rgba(255,255,255,0.03); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); border-bottom:1px solid rgba(255,255,255,0.08); border-radius:16px 16px 0 0; padding:18px 28px; display:flex; align-items:center; justify-content:space-between;">
      <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:44px;height:44px;background:rgba(249,115,22,0.15);border:1px solid rgba(249,115,22,0.35);border-radius:10px;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:24px;">
          🏗️
        </div>
        <div style="display:flex; flex-direction:column; gap:4px;">
          <div style="font-size:22px; font-weight:700; color:#F1F5F9; line-height:1;">Şantiyelerim</div>
          <div id="santiyeAltBaslik" style="font-size:12px; color:rgba(255,255,255,0.4); font-style:italic; line-height:1;">Gerçek zamanlı izleme</div>
        </div>
      </div>
      <div style="display:flex; gap:10px; align-items:center;">
        <button onclick="santiyeEkleModalAc(null)"
          style="background:linear-gradient(135deg,#6366f1,#14b8a6); color:white; border:none; border-radius:10px; padding:10px 20px; font-weight:600; font-size:14px; cursor:pointer; transition:all 0.2s ease; font-family:inherit;"
          onmouseover="this.style.opacity='0.85';this.style.transform='translateY(-1px)'"
          onmouseout="this.style.opacity='1';this.style.transform='translateY(0)'">
          + Yeni Şantiye
        </button>
        <button onclick="santiyeModalKapat()" style="background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.1); color:#94a3b8; width:36px; height:36px; border-radius:8px; cursor:pointer; font-size:1rem; transition:all 0.2s;">✕</button>
      </div>
    </div>

    <!-- ── KPI KARTLARI ── -->
    <div id="santiyeOzet" style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px; padding:16px 28px; border-bottom:1px solid rgba(255,255,255,0.04);"></div>

    <!-- ── İKİ SÜTUN: Harita (Sol) + Grafikler (Sağ) ── -->
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; padding:16px 28px; border-bottom:1px solid rgba(255,255,255,0.04);">

      <!-- SOL: CartoDB Dark Matter Harita -->
      <div>
        <div style="font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:rgba(99,102,241,0.65); margin-bottom:10px;">📍 Harita</div>
        <div style="position:relative;">
          <div id="santiyeHarita" style="height:300px; border-radius:14px; overflow:hidden; border:1px solid rgba(99,102,241,0.16); background:rgba(3,7,18,0.8);"></div>
          <div id="santiyeHaritaBadge" style="display:none; position:absolute; top:10px; right:10px; background:rgba(6,11,26,0.90); backdrop-filter:blur(10px); border:1px solid rgba(99,102,241,0.30); border-radius:8px; padding:5px 12px; font-size:11px; font-weight:700; color:#a5b4fc; z-index:400; pointer-events:none;">
            <span id="santiyeHaritaCount">0</span> Şantiye Aktif
          </div>
        </div>
      </div>

      <!-- SAĞ: Chart.js Grafikler -->
      <div>
        <div style="font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:rgba(99,102,241,0.65); margin-bottom:10px;">📊 Karşılaştırma</div>
        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:20px; display:flex; flex-direction:column; gap:16px;">
          <!-- Grafik 1: İlerleme -->
          <div>
            <div style="font-size:10px; font-weight:600; color:rgba(148,163,184,0.6); text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;">İlerleme Karşılaştırması</div>
            <div style="height:160px;"><canvas id="ilerlemeChart"></canvas></div>
          </div>
          <!-- Grafik 2: İşçi Dağılımı -->
          <div>
            <div style="font-size:10px; font-weight:600; color:rgba(148,163,184,0.6); text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;">İşçi Dağılımı</div>
            <div style="height:160px;"><canvas id="isciChart"></canvas></div>
          </div>
          <!-- Grafik 3: Durum Özeti -->
          <div id="santiyeDurumOzet" style="display:flex; gap:8px; flex-wrap:wrap;"></div>
        </div>
      </div>
    </div>

    <!-- ── PROJE KARTLARI ── -->
    <div style="padding:16px 28px 28px;">
      <div style="font-size:9.5px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:rgba(99,102,241,0.65); margin-bottom:14px;">🗂️ Projeler</div>
      <div id="santiyeKartlar" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:14px;"></div>
    </div>

  </div>
</div>

<!-- GÜVENLİK MODALI -->
<div id="guvenlikModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.65); z-index:9999; align-items:flex-start; justify-content:center; overflow-y:auto; padding:16px; backdrop-filter:blur(4px);">
  <div style="background:#F8FAFC; border-radius:20px; width:100%; max-width:480px; overflow:hidden; margin:auto; box-shadow:0 24px 64px rgba(0,0,0,0.35);">

    <!-- Dark Header -->
    <div style="background:#0D1117; padding:14px 18px; display:flex; align-items:center; justify-content:space-between;">
      <div style="display:flex; align-items:center; gap:10px;">
        <div style="width:36px; height:36px; background:rgba(255,255,255,0.08); border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
            <circle cx="12" cy="8" r="2" fill="#CBD5E1" stroke="none"/>
          </svg>
        </div>
        <span style="color:white; font-size:1rem; font-weight:700;">Güvenlik Modülü</span>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <div style="border:1.5px solid rgba(255,255,255,0.35); border-radius:8px; padding:4px 10px; color:white; font-size:0.75rem; font-weight:700; white-space:nowrap;">GÜVENLİK SKORU: <span id="guvenlikSkor">--</span></div>
        <button onclick="guvenlikKapat()" style="background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:white; width:28px; height:28px; border-radius:7px; cursor:pointer; font-size:0.9rem; display:flex; align-items:center; justify-content:center; line-height:1;">✕</button>
      </div>
    </div>

    <!-- Sub-header -->
    <div style="background:#FFFFFF; padding:10px 14px; border-bottom:1px solid #E2E8F0;">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; flex-wrap:wrap;">
        <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
          <span style="font-size:0.6rem; color:#94A3B8; font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">ŞANTİYE SEÇİN:</span>
          <select id="guvenlikSantiye" onchange="guvenlikSantiyeDegisti()" style="border:1px solid #CBD5E1; border-radius:8px; padding:4px 8px; font-size:0.78rem; color:#0F172A; background:#F8FAFC; outline:none; max-width:155px;">
            <option value="">Seçin...</option>
          </select>
          <span id="guvenlikDurumBadge" style="background:#DCFCE7; color:#16A34A; border:1px solid #BBF7D0; border-radius:20px; padding:2px 9px; font-size:0.68rem; font-weight:700;">Şantiye Durumu: Aktif</span>
        </div>
        <div style="text-align:right; font-size:0.7rem; color:#64748B; line-height:1.7;">
          <div>Tarih: <span id="guvenlikTarih">--</span></div>
          <div>Sorumlu Şef: <span id="guvenlikSorumlu">--</span></div>
        </div>
      </div>
    </div>

    <!-- Tab bar -->
    <div style="background:#FFFFFF; display:flex; border-bottom:2px solid #E2E8F0; overflow-x:auto;">
      <button class="gv-tab active" onclick="gTab('isg',this)"><span style="font-size:1.1rem; display:block;">📋</span>İSG Kontrol</button>
      <button class="gv-tab" onclick="gTab('ekipman',this)"><span style="font-size:1.1rem; display:block;">🔧</span>Ekipman</button>
      <button class="gv-tab" onclick="gTab('hava',this)"><span style="font-size:1.1rem; display:block;">🌤</span>Hava Uyarıları</button>
      <button class="gv-tab" onclick="gTab('olay',this)"><span style="font-size:1.1rem; display:block;">📢</span>Olay Bildir</button>
      <button class="gv-tab" onclick="gTab('acil',this)"><span style="font-size:1.1rem; display:block;">⚡</span>Acil Durum</button>
    </div>

    <!-- Tab: ISG -->
    <div id="gtab-isg" class="gv-tab-content" style="background:#F8FAFC; padding:14px;">
      <div style="background:#FFFFFF; border-radius:14px; padding:14px; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid #F1F5F9;">
          <span style="font-size:0.9rem; font-weight:700; color:#0F172A;">Kişisel Koruyucu Donanım</span>
          <span id="isg-progress-1" style="font-size:0.78rem; color:#64748B; font-weight:600;">0/5</span>
        </div>
        <div id="isg-kkd-list">
          <div class="gv-check-item" data-group="kkd" onclick="gToggle(this)"><div class="gv-item-icon">⛑</div><div class="gv-item-body"><div class="gv-item-name">Baret / Koruyucu Kask</div><div class="gv-item-sub">Tüm personel için zorunlu</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="kkd" onclick="gToggle(this)"><div class="gv-item-icon">🦺</div><div class="gv-item-body"><div class="gv-item-name">Reflektif Yelek</div><div class="gv-item-sub">Görünürlük için</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="kkd" onclick="gToggle(this)"><div class="gv-item-icon">👢</div><div class="gv-item-body"><div class="gv-item-name">Güvenlik Botu — Çelik Burunlu</div><div class="gv-item-sub">Tüm saha personeli</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="kkd" onclick="gToggle(this)"><div class="gv-item-icon">🥽</div><div class="gv-item-body"><div class="gv-item-name">Koruyucu Gözlük</div><div class="gv-item-sub">Kaynak ve kesme işlemleri</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="kkd" onclick="gToggle(this)"><div class="gv-item-icon">🔗</div><div class="gv-item-body"><div class="gv-item-name">Emniyet Kemeri / Güvenlik Halatı</div><div class="gv-item-sub">Yüksekte çalışma zorunlu</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
        </div>
      </div>
      <div style="background:#FFFFFF; border-radius:14px; padding:14px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid #F1F5F9;">
          <span style="font-size:0.9rem; font-weight:700; color:#0F172A;">Saha Güvenliği</span>
          <span id="isg-progress-2" style="font-size:0.78rem; color:#64748B; font-weight:600;">0/6</span>
        </div>
        <div id="isg-saha-list">
          <div class="gv-check-item" data-group="saha" onclick="gToggle(this)"><div class="gv-item-icon">🚧</div><div class="gv-item-body"><div class="gv-item-name">Güvenlik Barikatları Yerinde</div><div class="gv-item-sub">Güvenlik Barikatları Yerinde</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="saha" onclick="gToggle(this)"><div class="gv-item-icon">🧯</div><div class="gv-item-body"><div class="gv-item-name">Yangın Söndürücü Erişilebilir</div><div class="gv-item-sub">Yangın Söndürücü Erişilebilir</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="saha" onclick="gToggle(this)"><div class="gv-item-icon">🩹</div><div class="gv-item-body"><div class="gv-item-name">İlk Yardım Çantası Dolu</div><div class="gv-item-sub">İlk Yardım Çantası Dolu</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="saha" onclick="gToggle(this)"><div class="gv-item-icon">🚪</div><div class="gv-item-body"><div class="gv-item-name">Acil Çıkış Yolları Açık</div><div class="gv-item-sub">Acil Çıkış Yolları Açık</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="saha" onclick="gToggle(this)"><div class="gv-item-icon">⚠️</div><div class="gv-item-body"><div class="gv-item-name">Uyarı Levhaları Yerinde</div><div class="gv-item-sub">Uyarı Levhaları Yerinde</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" data-group="saha" onclick="gToggle(this)"><div class="gv-item-icon">💡</div><div class="gv-item-body"><div class="gv-item-name">Aydınlatma Yeterli</div><div class="gv-item-sub">Aydınlatma Yeterli</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
        </div>
      </div>
      <button onclick="guvenlikRaporuKaydet()" style="width:100%; padding:14px; background:#0D1117; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:700; font-size:0.88rem;">Günlük İSG Kontrol Raporunu Kaydet 💾</button>
    </div>

    <!-- Tab: Ekipman -->
    <div id="gtab-ekipman" class="gv-tab-content" style="display:none; background:#F8FAFC; padding:14px;">
      <div style="font-size:0.9rem; color:#0F172A; font-weight:700; margin-bottom:12px; line-height:1.8;">
        Toplam Ekipman: <span id="gvEkipmanToplam">8</span> &nbsp;|&nbsp; Kritik Bakım: <span id="gvEkipmanKritik" style="color:#EF4444;">2</span>
      </div>
      <div style="background:#FFFFFF; border-radius:14px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.05); margin-bottom:12px;">
        <div id="ekipman-list">
          <div class="gv-check-item" onclick="gToggle(this)" style="padding:10px 14px; border-bottom:1px solid #F1F5F9;"><div class="gv-item-icon">🏗</div><div class="gv-item-body"><div class="gv-item-name">Kule Vinç</div><div class="gv-item-sub">Son Bakım: 01.04.2024 · Operatör Yetkinliği: Uygun</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" onclick="gToggle(this)" style="padding:10px 14px; border-bottom:1px solid #F1F5F9;"><div class="gv-item-icon">🚜</div><div class="gv-item-body"><div class="gv-item-name">Ekskavatör</div><div class="gv-item-sub">Son Bakım: 20.04.2024 · Operatör Yetkinliği: Uygun</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" onclick="gToggle(this)" style="padding:10px 14px; border-bottom:1px solid #F1F5F9;"><div class="gv-item-icon">⚙️</div><div class="gv-item-body"><div class="gv-item-name">Jeneratör</div><div class="gv-item-sub">Son Bakım: 05.05.2024 · Operatör Yetkinliği: Gözden Geçirilmeli</div></div><button class="gv-ctrl-btn" style="background:#F59E0B;">Kontrol Et</button></div>
          <div class="gv-check-item" onclick="gToggle(this)" style="padding:10px 14px; border-bottom:1px solid #F1F5F9;"><div class="gv-item-icon">🛗</div><div class="gv-item-body"><div class="gv-item-name">Yük Asansörü</div><div class="gv-item-sub">Son Bakım: 15.03.2024 · Operatör Yetkinliği: Gözden Geçirilmeli</div></div><button class="gv-ctrl-btn" style="background:#F59E0B;">Kontrol Et</button></div>
          <div class="gv-check-item" onclick="gToggle(this)" style="padding:10px 14px; border-bottom:1px solid #F1F5F9;"><div class="gv-item-icon">🧱</div><div class="gv-item-body"><div class="gv-item-name">Beton Mikseri</div><div class="gv-item-sub">Son Bakım: 01.04.2024 · Operatör Yetkinliği: Uygun</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" onclick="gToggle(this)" style="padding:10px 14px; border-bottom:1px solid #F1F5F9;"><div class="gv-item-icon">⚡</div><div class="gv-item-body"><div class="gv-item-name">Elektrik Panosu</div><div class="gv-item-sub">Son Bakım: 20.04.2024 · Topraklama: Uygun</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" onclick="gToggle(this)" style="padding:10px 14px; border-bottom:1px solid #F1F5F9;"><div class="gv-item-icon">🔩</div><div class="gv-item-body"><div class="gv-item-name">İskele Sistemi</div><div class="gv-item-sub">Son Bakım: 05.05.2024 · Stabilite: Uygun</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
          <div class="gv-check-item" onclick="gToggle(this)" style="padding:10px 14px;"><div class="gv-item-icon">🪚</div><div class="gv-item-body"><div class="gv-item-name">Taşlama ve Kesme Ekipmanları</div><div class="gv-item-sub">Son Bakım: 01.04.2024 · Operatör Yetkinliği: Uygun</div></div><button class="gv-ctrl-btn">Kontrol Et</button></div>
        </div>
      </div>
      <button onclick="ekipmanRaporuKaydet()" style="width:100%; padding:14px; background:#0D1117; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:700; font-size:0.88rem;">Günlük İSG Kontrol Raporunu Kaydet 💾</button>
    </div>

    <!-- Tab: Hava Uyarıları -->
    <div id="gtab-hava" class="gv-tab-content" style="display:none; background:#F8FAFC; padding:14px;">
      <div style="background:#FFFFFF; border-radius:14px; padding:14px; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:0.9rem; font-weight:700; color:#0F172A; margin-bottom:12px;">Yapay Zeka Hava Analizi</div>
        <div id="gv-hava-risk" style="display:flex; align-items:center; gap:12px; padding:12px; background:#F0FDF4; border-radius:10px; margin-bottom:12px;">
          <span style="font-size:2.2rem;">🛡</span>
          <div>
            <div id="gv-risk-label" style="color:#16A34A; font-weight:800; font-size:0.9rem; text-transform:uppercase;">DÜŞÜK RİSK</div>
            <div id="gv-risk-text" style="color:#64748B; font-size:0.78rem; margin-top:2px;">Hava durumu yükleniyor...</div>
          </div>
        </div>
        <div style="overflow-x:auto;">
          <table style="width:100%; border-collapse:collapse; font-size:0.78rem;">
            <thead><tr style="border-bottom:2px solid #E2E8F0;">
              <th style="text-align:left; padding:6px 4px; color:#64748B; font-weight:600;">Gün</th>
              <th style="text-align:center; padding:6px 4px; color:#64748B; font-weight:600;">İkon</th>
              <th style="text-align:center; padding:6px 4px; color:#64748B; font-weight:600;">Temp</th>
              <th style="text-align:center; padding:6px 4px; color:#64748B; font-weight:600;">Rüzgar</th>
              <th style="text-align:left; padding:6px 4px; color:#64748B; font-weight:600;">Karam Uyarığı</th>
            </tr></thead>
            <tbody id="gv-hava-satirlar">
              <tr><td colspan="5" style="text-align:center; color:#94A3B8; padding:16px; font-size:0.8rem;">Yükleniyor...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
      <div id="gv-ai-onerisi" style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:14px; display:flex; gap:10px; align-items:flex-start;">
        <span style="font-size:1.1rem; flex-shrink:0;">💡</span>
        <div>
          <div style="font-weight:700; color:#1D4ED8; font-size:0.82rem; margin-bottom:4px;">AI Önerisi</div>
          <div id="gv-ai-onerisi-text" style="color:#374151; font-size:0.8rem; line-height:1.5;">Hava durumu analizi bekleniyor...</div>
        </div>
      </div>
    </div>

    <!-- Tab: Olay Bildir -->
    <div id="gtab-olay" class="gv-tab-content" style="display:none; background:#F8FAFC; padding:14px;">
      <div style="background:#FFFFFF; border-radius:14px; padding:14px; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:0.9rem; font-weight:700; color:#0F172A; margin-bottom:12px;">Olay Bildir</div>
        <div style="display:flex; flex-direction:column; gap:10px;">
          <div>
            <label style="font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:0.3px;">Olay Türü</label>
            <select id="olayTur" style="width:100%; border:1px solid #CBD5E1; border-radius:8px; padding:9px 10px; font-size:0.85rem; color:#0F172A; background:#F8FAFC; outline:none; margin-top:4px;">
              <option value="kaza">Kaza</option>
              <option value="ramak_kala">Ramak Kala</option>
              <option value="hasar">Hasar</option>
              <option value="ihlal">İSG İhlali</option>
              <option value="yangin">Yangın / Risk</option>
            </select>
          </div>
          <div>
            <label style="font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:0.3px;">Açıklama</label>
            <textarea id="olayAciklama" placeholder="Açıklama" style="width:100%; border:1px solid #CBD5E1; border-radius:8px; padding:9px 10px; font-size:0.85rem; color:#0F172A; background:#F8FAFC; outline:none; min-height:80px; resize:vertical; margin-top:4px; box-sizing:border-box; font-family:inherit;"></textarea>
          </div>
          <div>
            <label style="font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase; letter-spacing:0.3px;">Fotoğraf Ekle</label>
            <div onclick="document.getElementById('olayFotoInput').click()" id="olayFotoArea" style="border:2px dashed #CBD5E1; border-radius:10px; padding:16px; text-align:center; cursor:pointer; background:#F8FAFC; margin-top:4px;">
              <div id="olayFotoOnizleme" style="font-size:1.8rem; color:#94A3B8;">📷</div>
              <div style="color:#94A3B8; font-size:0.75rem; margin-top:4px;">Fotoğraf seçmek için tıklayın</div>
            </div>
            <input type="file" id="olayFotoInput" accept="image/*" style="display:none;" onchange="olayFotoSecildi(this.files[0])">
          </div>
          <div id="olayMsg" style="font-size:0.78rem; text-align:center;"></div>
        </div>
      </div>
      <div style="background:#FFFFFF; border-radius:14px; padding:14px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:0.9rem; font-weight:700; color:#0F172A; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid #E2E8F0;">Son Olaylar</div>
        <div id="sonOlaylar">
          <div style="color:#94A3B8; font-size:0.8rem; text-align:center; padding:12px;">Henüz kayıtlı olay yok.</div>
        </div>
      </div>
      <button onclick="olayBildir()" style="width:100%; padding:14px; background:#0D1117; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:700; font-size:0.88rem;">Bildirimi Gönder</button>
    </div>

    <!-- Tab: Acil Durum -->
    <div id="gtab-acil" class="gv-tab-content" style="display:none; background:#F8FAFC; padding:14px;">
      <div style="background:#FFFFFF; border-radius:14px; padding:14px; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:0.9rem; font-weight:700; color:#0F172A; margin-bottom:12px;">Acil Çağrı</div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-bottom:8px;">
          <a href="tel:112" style="background:#DC2626; border-radius:10px; padding:12px 6px; text-align:center; text-decoration:none; display:block;">
            <div style="font-size:1.2rem;">📞</div>
            <div style="color:white; font-weight:700; font-size:0.75rem; margin-top:4px;">Ambulans</div>
            <div style="color:rgba(255,255,255,0.75); font-size:0.68rem;">112</div>
          </a>
          <a href="tel:110" style="background:#DC2626; border-radius:10px; padding:12px 6px; text-align:center; text-decoration:none; display:block;">
            <div style="font-size:1.2rem;">🚒</div>
            <div style="color:white; font-weight:700; font-size:0.75rem; margin-top:4px;">İtfaiye</div>
            <div style="color:rgba(255,255,255,0.75); font-size:0.68rem;">110</div>
          </a>
          <a href="tel:155" style="background:#0D1117; border-radius:10px; padding:12px 6px; text-align:center; text-decoration:none; display:block;">
            <div style="font-size:1.2rem;">👮</div>
            <div style="color:white; font-weight:700; font-size:0.68rem; margin-top:4px; line-height:1.3;">Şantiye<br>Güvenliği</div>
          </a>
        </div>
        <a href="tel:155" style="display:flex; align-items:center; justify-content:center; gap:8px; background:#0D1117; border-radius:10px; padding:12px; text-decoration:none;">
          <span style="font-size:1.1rem;">👮</span>
          <span style="color:white; font-weight:700; font-size:0.85rem;">Şantiye Güvenliği</span>
        </a>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <div style="background:#FFFFFF; border-radius:14px; padding:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
          <div style="font-size:0.82rem; font-weight:700; color:#0F172A; margin-bottom:8px;">Tahliye Planı</div>
          <div id="acilMap" style="width:100%; height:110px; border-radius:8px; overflow:hidden; background:#E2E8F0; display:flex; align-items:center; justify-content:center; font-size:1.5rem;">🗺</div>
        </div>
        <div style="background:#FFFFFF; border-radius:14px; padding:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
          <div style="font-size:0.82rem; font-weight:700; color:#0F172A; margin-bottom:8px;">Acil Durum Toplanma Alanları</div>
          <div style="font-size:0.78rem; color:#374151; line-height:2.1;">
            <div><strong>Alan A:</strong> Ana Giriş Kapısı</div>
            <div><strong>Alan B:</strong> Arka Bahçe</div>
            <div><strong>Alan C:</strong> Kantin Karşısı</div>
          </div>
        </div>
      </div>
      <div style="background:#FFFFFF; border-radius:14px; padding:14px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:0.85rem; font-weight:700; color:#0F172A; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid #E2E8F0;">İlkyardımcı Personel</div>
        <div id="acilPersonelListe" style="display:flex; flex-direction:column; gap:6px; margin-bottom:10px;">
          <div style="color:#94A3B8; font-size:0.78rem; text-align:center; padding:8px;">Personel eklenmemiş.</div>
        </div>
        <div style="display:flex; gap:6px;">
          <input id="acilPersonelAd" type="text" placeholder="Ad Soyad (Görev)" style="flex:1; border:1px solid #CBD5E1; border-radius:8px; padding:7px 8px; font-size:0.78rem; outline:none; background:#F8FAFC; color:#0F172A; min-width:0;">
          <input id="acilPersonelTel" type="tel" placeholder="Telefon" style="width:100px; border:1px solid #CBD5E1; border-radius:8px; padding:7px 8px; font-size:0.78rem; outline:none; background:#F8FAFC; color:#0F172A; flex-shrink:0;">
          <button onclick="acilPersonelEkle()" style="background:#0D1117; color:white; border:none; border-radius:8px; padding:7px 10px; cursor:pointer; font-size:0.78rem; font-weight:700; white-space:nowrap; flex-shrink:0;">+ Ekle</button>
        </div>
      </div>
      <button onclick="guvenlikRaporuKaydet()" style="width:100%; padding:14px; background:#0D1117; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:700; font-size:0.88rem;">Günlük İSG Kontrol Raporunu Kaydet 💾</button>
    </div>

  </div>
</div>

<!-- ŞANTİYE EKLE MODALI — Light Theme -->
<style>
.sfToggle {{ position:relative; display:inline-block; width:44px; height:24px; }}
.sfToggle input {{ opacity:0; width:0; height:0; }}
.sfToggleSlider {{ position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background:#CBD5E1; border-radius:24px; transition:background 0.2s; }}
.sfToggleSlider:before {{ content:""; position:absolute; height:18px; width:18px; left:3px; bottom:3px; background:#FFFFFF; border-radius:50%; transition:transform 0.2s; box-shadow:0 1px 3px rgba(0,0,0,0.2); }}
.sfToggle input:checked + .sfToggleSlider {{ background:#16A34A; }}
.sfToggle input:checked + .sfToggleSlider:before {{ transform:translateX(20px); }}
</style>
<div id="santiyeFormModal" style="display:none; position:fixed; inset:0; background:rgba(15,23,42,0.6); z-index:9100; align-items:center; justify-content:center; padding:20px;">
  <div style="background:#FFFFFF; border-radius:16px; width:100%; max-width:480px; overflow:hidden; box-shadow:0 24px 64px rgba(0,0,0,0.25); max-height:92vh; display:flex; flex-direction:column;">

    <!-- Dark Header -->
    <div style="background:#0D1117; padding:20px 24px; display:flex; align-items:center; justify-content:space-between; flex-shrink:0;">
      <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:40px; height:40px; background:rgba(255,255,255,0.07); border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <svg width="28" height="28" viewBox="0 0 100 100" fill="none" stroke="#CBD5E1" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
            <!-- Mast left rail (tapers: wide base → narrow top) -->
            <line x1="32" y1="82" x2="35" y2="14"/>
            <!-- Mast right rail -->
            <line x1="46" y1="82" x2="43" y2="14"/>
            <!-- Mast X-bracing (6 panels) -->
            <line x1="32" y1="82" x2="46" y2="70"/><line x1="46" y1="82" x2="32" y2="70"/>
            <line x1="32" y1="70" x2="46" y2="58"/><line x1="46" y1="70" x2="32" y2="58"/>
            <line x1="33" y1="58" x2="45" y2="46"/><line x1="45" y1="58" x2="33" y2="46"/>
            <line x1="33" y1="46" x2="45" y2="34"/><line x1="45" y1="46" x2="33" y2="34"/>
            <line x1="34" y1="34" x2="44" y2="22"/><line x1="44" y1="34" x2="34" y2="22"/>
            <!-- Mast base trapezoid (wider at bottom) -->
            <line x1="28" y1="82" x2="50" y2="82"/>
            <!-- Counter-jib (extends left) -->
            <line x1="35" y1="14" x2="14" y2="14"/>
            <!-- Counter-weight box -->
            <rect x="10" y="11" width="8" height="7" rx="1"/>
            <!-- Main jib (extends right) -->
            <line x1="43" y1="14" x2="82" y2="14"/>
            <!-- Jib top truss (triangular bracing above jib) -->
            <line x1="35" y1="14" x2="55" y2="9"/>
            <line x1="55" y1="9" x2="82" y2="14"/>
            <!-- Jib bottom support line -->
            <line x1="35" y1="14" x2="55" y2="20"/>
            <line x1="55" y1="20" x2="82" y2="14"/>
            <!-- Top circle (mast crown) -->
            <circle cx="39" cy="13" r="2.5" fill="#CBD5E1" stroke="none"/>
            <!-- Hook rope -->
            <line x1="72" y1="14" x2="72" y2="42"/>
            <!-- Hook link circle -->
            <circle cx="72" cy="44" r="2.2"/>
            <!-- Hook curve -->
            <path d="M70 46 Q66 52 69 56 Q72 59 75 56" stroke-width="2.8"/>
            <!-- Ground base line -->
            <line x1="24" y1="82" x2="88" y2="82"/>
            <!-- Building 1 (shorter, left) -->
            <rect x="52" y="56" width="14" height="26" rx="1"/>
            <line x1="52" y1="64" x2="66" y2="64"/>
            <line x1="52" y1="72" x2="66" y2="72"/>
            <line x1="59" y1="56" x2="59" y2="82"/>
            <!-- Building 2 (taller, right) -->
            <rect x="67" y="44" width="20" height="38" rx="1"/>
            <line x1="67" y1="53" x2="87" y2="53"/>
            <line x1="67" y1="62" x2="87" y2="62"/>
            <line x1="67" y1="71" x2="87" y2="71"/>
            <line x1="77" y1="44" x2="77" y2="82"/>
          </svg>
        </div>
        <div>
          <div id="santiyeFormBaslik" style="font-size:15px; font-weight:700; color:#F1F5F9; letter-spacing:-0.01em;">Yeni Şantiye Ekle</div>
          <div style="font-size:11.5px; color:#64748B; margin-top:2px;">Yeni proje kaydı oluşturuyor</div>
        </div>
      </div>
      <button onclick="santiyeFormKapat()" style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10); color:#64748B; width:32px; height:32px; border-radius:8px; cursor:pointer; font-size:16px; line-height:1; transition:all 0.15s; display:flex; align-items:center; justify-content:center;"
        onmouseover="this.style.background='rgba(255,255,255,0.12)';this.style.color='#CBD5E1'"
        onmouseout="this.style.background='rgba(255,255,255,0.06)';this.style.color='#64748B'">✕</button>
    </div>

    <!-- Form Body -->
    <div style="padding:20px 24px; display:flex; flex-direction:column; gap:14px; overflow-y:auto; background:#F8FAFC;">
      <input type="hidden" id="santiyeFormId">
      <textarea id="santiyeFormNotlar" style="display:none;"></textarea>
      <div id="ragDropLabel" style="display:none;"></div>
      <div id="ragDropZone" style="display:none;" ondragover="ragDragOver(event)" ondragleave="ragDragLeave(event)" ondrop="ragDrop(event)"></div>
      <input type="file" id="santiyeFormDosya" accept=".pdf,.xlsx,.xls,.doc,.docx" multiple style="display:none;" onchange="ragDosyaSecildi(this)">

      <!-- ŞANTİYE FOTOĞRAFI -->
      <div>
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:6px;">Şantiye Fotoğrafı</div>
        <div id="santiyeFotoAlani"
          onclick="document.getElementById('santiyeFotoInput').click()"
          ondragover="event.preventDefault(); this.style.borderColor='#3B82F6'; this.style.background='#EFF6FF';"
          ondragleave="this.style.borderColor='#E2E8F0'; this.style.background='#FFFFFF';"
          ondrop="event.preventDefault(); this.style.borderColor='#E2E8F0'; this.style.background='#FFFFFF'; santiyeFotoSecildi(event.dataTransfer.files[0])"
          style="border:1.5px dashed #CBD5E1; border-radius:9px; background:#FFFFFF; height:120px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; cursor:pointer; transition:all 0.15s; position:relative; overflow:hidden;">
          <img id="santiyeFotoOnizleme" src="" alt="" style="display:none; position:absolute; inset:0; width:100%; height:100%; object-fit:cover; border-radius:8px;">
          <div id="santiyeFotoPlaceholder" style="display:flex; flex-direction:column; align-items:center; gap:6px; pointer-events:none;">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="1.6" stroke-linecap="round"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>
            <span style="font-size:12px; font-weight:600; color:#3B82F6;">Fotoğraf ekle</span>
            <span style="font-size:10.5px; color:#94A3B8;">JPG, PNG · Sürükle veya tıkla</span>
          </div>
          <button id="santiyeFotoKaldir" onclick="event.stopPropagation(); santiyeFotoTemizle()" style="display:none; position:absolute; top:6px; right:6px; background:rgba(0,0,0,0.5); border:none; color:white; width:24px; height:24px; border-radius:50%; cursor:pointer; font-size:13px; line-height:1; align-items:center; justify-content:center;">✕</button>
        </div>
        <input type="file" id="santiyeFotoInput" accept="image/*" style="display:none;" onchange="santiyeFotoSecildi(this.files[0])">
      </div>

      <!-- ŞANTİYE ADI -->
      <div>
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:6px;">Şantiye Adı</div>
        <input type="text" id="santiyeFormAd" placeholder="örn: Atatürk Bulvarı Konut Projesi"
          style="width:100%; background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:9px; color:#0F172A; padding:10px 13px; font-size:14px; outline:none; transition:border-color 0.15s; font-family:inherit; box-sizing:border-box;"
          onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">
      </div>

      <!-- KONUM -->
      <div>
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:6px;">Konum</div>
        <input type="text" id="santiyeFormKonum" placeholder="örn: Sivas, Merkez"
          style="width:100%; background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:9px; color:#0F172A; padding:10px 13px; font-size:14px; outline:none; transition:border-color 0.15s; font-family:inherit; box-sizing:border-box;"
          onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">
      </div>

      <!-- HARİTADAN KONUM SEÇ -->
      <div>
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:8px; display:flex; align-items:center; gap:5px;">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="#EF4444" stroke="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5s2.5 1.12 2.5 2.5S13.38 11.5 12 11.5z"/></svg>
          Haritadan Konum Seç
          <span style="font-weight:400; color:#94A3B8; text-transform:none; letter-spacing:0;">(opsiyonel)</span>
        </div>
        <div id="santiyeFormMiniHarita" style="height:180px; border-radius:9px; overflow:hidden; border:1.5px solid #E2E8F0; background:#E2E8F0; cursor:crosshair;"></div>
        <div style="font-size:11px; color:#94A3B8; margin-top:4px;">Haritaya tıklayın → enlem/boylam otomatik dolar</div>
      </div>

      <!-- ENLEM / BOYLAM -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div>
          <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:6px;">Enlem</div>
          <input type="number" id="santiyeFormLat" placeholder="39.7477" step="0.0001"
            style="width:100%; background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:9px; color:#0F172A; padding:10px 12px; font-size:13px; outline:none; font-family:inherit; box-sizing:border-box; transition:border-color 0.15s;"
            onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">
        </div>
        <div>
          <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:6px;">Boylam</div>
          <input type="number" id="santiyeFormLon" placeholder="37.0179" step="0.0001"
            style="width:100%; background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:9px; color:#0F172A; padding:10px 12px; font-size:13px; outline:none; font-family:inherit; box-sizing:border-box; transition:border-color 0.15s;"
            onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">
        </div>
      </div>

      <!-- İLERLEME / İŞÇİ SAYISI -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div>
          <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:6px;">İlerleme (%)</div>
          <input type="number" id="santiyeFormIlerleme" placeholder="0" min="0" max="100" value="0"
            style="width:100%; background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:9px; color:#0F172A; padding:10px 12px; font-size:13px; outline:none; font-family:inherit; box-sizing:border-box; transition:border-color 0.15s;"
            onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">
        </div>
        <div>
          <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:6px;">İşçi Sayısı</div>
          <input type="number" id="santiyeFormIsci" placeholder="0" min="0" value="0"
            style="width:100%; background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:9px; color:#0F172A; padding:10px 12px; font-size:13px; outline:none; font-family:inherit; box-sizing:border-box; transition:border-color 0.15s;"
            onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'">
        </div>
      </div>

      <!-- DURUM toggle -->
      <div style="background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:9px; padding:12px 14px; display:flex; align-items:center; justify-content:space-between;">
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B;">Durum</div>
        <div style="display:flex; align-items:center; gap:10px;">
          <span id="santiyeFormDurumLabel" style="font-size:13px; font-weight:600; color:#16A34A;">Açık</span>
          <label class="sfToggle">
            <input type="checkbox" id="santiyeFormDurumToggle" checked onchange="sfDurumToggle(this)">
            <span class="sfToggleSlider"></span>
          </label>
        </div>
      </div>
      <select id="santiyeFormDurum" style="display:none;">
        <option value="iyi">İyi</option>
        <option value="dikkat">Dikkat</option>
        <option value="sorun">Sorun</option>
      </select>

      <!-- İSG NOTU -->
      <div>
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:6px;">İSG Notu</div>
        <textarea id="santiyeFormIsg" placeholder="Güvenlik durumu, aktif ISG notları..." rows="3"
          style="width:100%; background:#FFFFFF; border:1.5px solid #E2E8F0; border-radius:9px; color:#0F172A; padding:10px 13px; font-size:13px; outline:none; font-family:inherit; resize:vertical; box-sizing:border-box; transition:border-color 0.15s;"
          onfocus="this.style.borderColor='#3B82F6'" onblur="this.style.borderColor='#E2E8F0'"></textarea>
      </div>

      <!-- DOSYA YÜKLEME -->
      <div style="border:1.5px dashed #CBD5E1; border-radius:9px; padding:14px; background:#F8FAFC;">
        <div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#64748B; margin-bottom:10px;">📎 Şantiye Dosyaları</div>
        <div style="font-size:11px; color:#94A3B8; margin-bottom:10px;">PDF, Excel veya Word dosyaları — AI belleğine eklenir</div>
        <label style="display:flex; align-items:center; gap:8px; cursor:pointer;">
          <div style="background:#EFF6FF; border:1.5px solid #BFDBFE; border-radius:7px; padding:7px 14px; font-size:12px; font-weight:600; color:#2563EB; white-space:nowrap; transition:background 0.15s;"
            onmouseover="this.style.background='#DBEAFE'" onmouseout="this.style.background='#EFF6FF'">
            + Dosya Seç
          </div>
          <input type="file" id="santiyeFormDosyaInput" multiple accept=".pdf,.xlsx,.xls,.doc,.docx"
            style="display:none" onchange="santiyeFormDosyaSecildi(this)">
          <span id="santiyeFormDosyaLabel" style="font-size:12px; color:#64748B;">Henüz dosya seçilmedi</span>
        </label>
        <div id="santiyeFormDosyaListesi" style="margin-top:8px; display:flex; flex-wrap:wrap; gap:6px;"></div>
      </div>

      <!-- ŞANTİYE SİL (sadece edit modda) -->
      <div id="santiyeSilBlok" style="display:none; border:1.5px solid #FEE2E2; border-radius:9px; padding:14px; background:#FFF5F5;">
        <div style="display:flex; align-items:center; justify-content:space-between;">
          <div>
            <div style="font-size:13px; font-weight:700; color:#DC2626;">Şantiyeyi Sil</div>
            <div style="font-size:11px; color:#EF4444; margin-top:2px;">Bu işlem geri alınamaz.</div>
          </div>
          <button onclick="santiyeSilOnay()" id="santiyeSilBtn"
            style="background:#DC2626; border:none; color:#FFFFFF; padding:8px 16px; border-radius:7px; cursor:pointer; font-weight:700; font-size:12px; font-family:inherit; transition:background 0.15s; white-space:nowrap;"
            onmouseover="this.style.background='#B91C1C'" onmouseout="this.style.background='#DC2626'">
            🗑 Şantiyeyi Sil
          </button>
        </div>
      </div>

      <div id="santiyeFormMsg" style="font-size:11.5px; min-height:14px;"></div>

      <button onclick="santiyeKaydet()"
        style="width:100%; background:#3B82F6; border:none; color:#FFFFFF; padding:13px; border-radius:10px; cursor:pointer; font-weight:700; font-size:14px; letter-spacing:0.01em; transition:background 0.15s; font-family:inherit;"
        onmouseover="this.style.background='#2563EB'"
        onmouseout="this.style.background='#3B82F6'">
        Şantiye Ekle
      </button>
    </div>

  </div>
</div>

<!-- 🔒 PLAN KİLİT MODALI -->
<div id="planKilitModal" style="display:none;"></div>

<!-- 💳 ÖDEME MODALI -->
<div id="odemeModal" style="display:none;"></div>

{JS_SCRIPT}
<script>
if ('serviceWorker' in navigator) {{
  window.addEventListener('load', () => {{
    navigator.serviceWorker.register('/static/sw.js')
      .then(reg => console.log('SW kayıtlı'))
      .catch(err => console.log('SW hatası:', err));
  }});
}}
</script>
</body>
</html>
"""
