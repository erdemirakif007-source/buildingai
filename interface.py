from styles import CSS_STYLE
from scripts import JS_SCRIPT

HTML_TEMPLATE = f"""
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
    <link rel="apple-touch-icon" href="/static/icon-192.png">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="icon" type="image/png" sizes="96x96" href="/static/favicon-96x96.png">
    <title>BuildingAI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    {CSS_STYLE}
    <style>
        /* ---- AUTH TABS ---- */
        .auth-tabs {{ display: flex; margin-bottom: 25px; border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }}
        .auth-tab {{ flex: 1; padding: 12px; background: transparent; border: none; color: #aaa; cursor: pointer; font-weight: 700; font-size: 0.9rem; transition: 0.3s; }}
        .auth-tab.active {{ background: var(--primary); color: white; }}

        /* ---- PLAN CARDS ---- */
        .plan-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 20px; }}
        .plan-card {{ background: rgba(255,255,255,0.04); border: 2px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 14px; cursor: pointer; transition: 0.3s; text-align: center; font-size: 13px; min-width: 0; }}
        .plan-card:hover, .plan-card.selected {{ border-color: var(--primary); background: rgba(230,126,34,0.1); }}
        .plan-card h3 {{ color: var(--primary); margin: 0 0 8px 0; font-size: 1.1rem; }}
        .plan-card .price {{ font-size: 1.3rem; font-weight: 800; color: white; }}
        .plan-card .price span {{ font-size: 0.8rem; color: #aaa; font-weight: 400; }}
        .plan-card ul {{ list-style: none; padding: 0; margin: 10px 0 0 0; text-align: left; }}
        .plan-card ul li {{ color: #ccc; font-size: 0.75rem; padding: 3px 0; }}
        .plan-card ul li::before {{ content: "✓ "; color: #2ecc71; font-weight: 800; }}

        /* ---- PROFILE ---- */
        .profile-header {{ display: flex; align-items: center; gap: 20px; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #333; }}
        .profile-avatar {{ width: 70px; height: 70px; background: var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; color: white; flex-shrink: 0; }}
        .profile-badge {{ background: rgba(230,126,34,0.2); border: 1px solid var(--primary); color: var(--primary); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }}
        .profile-stat {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 15px; text-align: center; }}
        .profile-stat .stat-value {{ font-size: 1.8rem; font-weight: 800; color: var(--primary); }}
        .profile-stat .stat-label {{ font-size: 0.75rem; color: #aaa; margin-top: 4px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 25px; }}
    </style>
</head>
<body>
<div id="mobile-overlay" onclick="closeMobileMenu()"></div>

<!-- ===== AUTH OVERLAY ===== -->
<div id="auth-overlay">
    <div class="auth-card" style="max-width: 420px; width: 90%;">

        <!-- LOGIN PANEL -->
        <div id="panel-login">
            <div style="display:flex; justify-content:flex-end; gap:8px; margin-bottom:15px;">
                <button id="langBtn_tr" class="lang-btn active-lang" onclick="dilDegistir('tr')" style="background:rgba(255,255,255,0.08); border:2px solid var(--primary); border-radius:10px; padding:5px 12px; color:white; cursor:pointer; font-size:0.85rem; font-weight:700; transition:0.3s;">🇹🇷 TR</button>
                <button id="langBtn_en" class="lang-btn" onclick="dilDegistir('en')" style="background:rgba(255,255,255,0.04); border:2px solid rgba(255,255,255,0.15); border-radius:10px; padding:5px 12px; color:#aaa; cursor:pointer; font-size:0.85rem; font-weight:700; transition:0.3s;">🇬🇧 EN</button>
            </div>
            <div class="auth-tabs">
                <button class="auth-tab tab-login active" onclick="switchPanel('login')">Giriş Yap</button>
                <button class="auth-tab tab-register" onclick="switchPanel('register')">Kayıt Ol</button>
            </div>
            <h2 id="loginTitleEl" style="text-align:center; margin-bottom:25px;">🏗️ BuildingAI</h2>
            <input type="email" id="loginEmail" class="auth-input" placeholder="E-posta adresi">
            <input type="password" id="loginPass" class="auth-input" placeholder="Şifre">
            <button class="auth-btn" id="loginBtn" onclick="girisYap()">Şantiyeye Giriş Yap</button>
            <div id="loginMsg"></div>
            <a class="auth-link" onclick="switchPanel('forgot')">Şifremi unuttum</a>
        </div>

        <!-- REGISTER PANEL -->
        <div id="panel-register" style="display:none;">
            <div class="auth-tabs">
                <button class="auth-tab tab-login" onclick="switchPanel('login')">Giriş Yap</button>
                <button class="auth-tab tab-register active" onclick="switchPanel('register')">Kayıt Ol</button>
            </div>
            <h2 style="text-align:center; margin-bottom:20px;">🏗️ Hesap Oluştur</h2>
            <input type="text" id="regName" class="auth-input" placeholder="Ad Soyad">
            <input type="text" id="regCompany" class="auth-input" placeholder="Şirket / Proje Adı (opsiyonel)">
            <input type="email" id="regEmail" class="auth-input" placeholder="E-posta adresi">
            <input type="password" id="regPass" class="auth-input" placeholder="Şifre (min. 6 karakter)">
            <input type="password" id="regPassConfirm" class="auth-input" placeholder="Şifreyi tekrarla">
            <hr class="divider">
            <p style="color:#aaa; font-size:0.85rem; margin: 0 0 10px 0;">Plan seçin:</p>
            <div class="plan-grid" style="grid-template-columns: 1fr 1fr 1fr;">
                <div class="plan-card selected" id="plan-free" onclick="selectPlan('free')">
                    <h3>Ücretsiz</h3>
                    <div class="price">₺0 <span>/ay</span></div>
                    <ul>
                        <li>20 AI sorgu/gün</li>
                        <li>Temel hesaplamalar</li>
                        <li>Rapor arşivi</li>
                    </ul>
                </div>
                <div class="plan-card" id="plan-pro" onclick="selectPlan('pro')">
                    <h3>⚡ Pro</h3>
                    <div class="price">₺650 <span>/ay</span></div>
                    <ul>
                        <li>Sınırsız AI sorgu</li>
                        <li>Fotoğraf analizi</li>
                        <li>WhatsApp entegrasyon</li>
                        <li>1 şantiye</li>
                    </ul>
                </div>
                <div class="plan-card" id="plan-max" onclick="selectPlan('max')">
                    <h3>👑 Max</h3>
                    <div class="price">₺1.990 <span>/ay</span></div>
                    <ul>
                        <li>Her şey dahil</li>
                        <li>Sınırsız şantiye</li>
                        <li>Stok takibi</li>
                        <li>Öncelikli destek</li>
                    </ul>
                </div>
            </div>
            <button class="auth-btn" id="regBtn" onclick="kayitOl()" style="margin-top:20px;">Hesabı Oluştur</button>
            <div id="regMsg"></div>
        </div>

        <!-- FORGOT PASSWORD PANEL -->
        <div id="panel-forgot" style="display:none;">
            <h2 style="text-align:center; margin-bottom:10px;">🔑 Şifre Sıfırlama</h2>
            <p style="color:#aaa; font-size:0.9rem; text-align:center; margin-bottom:20px;">E-posta adresinize 6 haneli kod göndereceğiz.</p>
            <div id="forgot-step1">
                <input type="email" id="forgotEmail" class="auth-input" placeholder="E-posta adresi">
                <button class="auth-btn" id="forgotBtn" onclick="sifreSifirla()">Kod Gönder</button>
                <div id="forgotMsg"></div>
            </div>
            <div id="forgot-step2" style="display:none;">
                <p style="color:#2ecc71; font-size:0.85rem; text-align:center; margin-bottom:15px;">✅ Kod gönderildi! E-postanızı kontrol edin.</p>
                <input type="text" id="resetKod" class="auth-input" placeholder="6 haneli kod" maxlength="6" style="text-align:center; letter-spacing:8px; font-size:1.4rem; font-weight:bold;">
                <input type="password" id="resetYeniSifre" class="auth-input" placeholder="Yeni şifre (min. 8 karakter)">
                <input type="password" id="resetYeniSifreTekrar" class="auth-input" placeholder="Yeni şifreyi tekrarla">
                <button class="auth-btn" onclick="sifreGuncelle()">Şifreyi Güncelle</button>
                <div id="resetMsg"></div>
                <a class="auth-link" onclick="document.getElementById('forgot-step1').style.display='block';document.getElementById('forgot-step2').style.display='none';">← Farklı e-posta dene</a>
            </div>
            <a class="auth-link" onclick="switchPanel('login')" style="margin-top:10px;">← Giriş sayfasına dön</a>
        </div>

    </div>
</div>

<!-- ===== PROFILE MODAL ===== -->
<div id="profileModal" style="display:none; position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.85); backdrop-filter:blur(10px); z-index:4000; align-items:center; justify-content:center;">
    <div style="background:#1a1d21; border:2px solid var(--primary); border-radius:28px; padding:35px; width:90%; max-width:480px; max-height:85vh; overflow-y:auto;">
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
          <span style="font-size:22px;">🏗️</span>
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
          <div style="padding:10px 13px 4px;">
            <div class="sb-section-title">⚡ ANA PANEL</div>
          </div>
          <div class="nav-item active" id="nav-home" onclick="navGit('home')">
            <span class="nav-icon">🏠</span> Ana Sayfa
          </div>
          <div class="nav-item" id="nav-santiye" onclick="santiyeModalAc()">
            <span class="nav-icon">🏗️</span> Şantiyelerim
          </div>

          <div style="padding:10px 13px 4px;">
            <div class="sb-section-title">📊 ANALİZ</div>
          </div>
          <div class="nav-item" id="nav-kamera" onclick="navGit('kamera')">
            <span class="nav-icon">📷</span> Kamera Analizi
          </div>
          <div class="nav-item" id="nav-hesaplama" onclick="navGit('hesaplama')">
            <span class="nav-icon">⚙️</span> Mühendislik Paneli
          </div>
          <div class="nav-item" id="nav-deprem" onclick="navGit('deprem')">
            <span class="nav-icon">🌍</span> Deprem Analizi
          </div>

          <div style="padding:10px 13px 4px;">
            <div class="sb-section-title">📋 RAPORLAR</div>
          </div>
          <div class="nav-item" id="nav-gunluk" onclick="navGit('gunluk')">
            <span class="nav-icon">📋</span> Günlük Rapor
          </div>
          <div class="nav-item" id="nav-sesli" onclick="navGit('sesli')">
            <span class="nav-icon">🎤</span> Sesli Rapor
          </div>
          <div class="nav-item" id="nav-pdf" onclick="pdfIndir()">
            <span class="nav-icon">📄</span> PDF İndir
          </div>
          <div class="nav-item" id="nav-haftalik" onclick="haftalikRaporIndir()">
            <span class="nav-icon">📊</span> Haftalık Rapor
          </div>

          <div style="padding:10px 13px 4px;">
            <div class="sb-section-title">📦 TAKİP</div>
          </div>
          <div class="nav-item" id="nav-fiyat" onclick="navGit('fiyat')">
            <span class="nav-icon">💹</span> Fiyat Takibi
          </div>
          <div class="nav-item" id="nav-stok" onclick="navGit('stok')">
            <span class="nav-icon">📦</span> Stok Takibi
            <span style="width:8px;height:8px;border-radius:50%;background:#f97316;box-shadow:0 0 6px #f97316;margin-left:auto;flex-shrink:0;"></span>
          </div>
          <div class="nav-item" id="nav-arsiv" onclick="arsivAc()">
            <span class="nav-icon">📁</span> Arşiv
          </div>
          <div class="sb-fill"></div>
          <div class="sb-foot">
            <div class="sb-upgrade" onclick="odemePaneliAc('max')">
              <div class="sb-upgrade-title">👑 Max'e Geç</div>
              <div class="sb-upgrade-sub">Çoklu şantiye & stok</div>
            </div>
          </div>
        </div>

        <!-- SAĞ ANA ALAN -->
        <div id="mainArea">
          <div id="content">

            <!-- HIZLI ERİŞİM BUTONLARI -->
            <div class="quick-actions fade-in">
              <div class="quick-btn" onclick="guvenlikAc()">
                <div class="quick-btn-icon">⚠️</div>
                <div class="quick-btn-label">GÜVENLİK</div>
              </div>
              <div class="quick-btn" id="raporlarBtn" onclick="toggleRaporlarSub()">
                <div class="quick-btn-icon">📋</div>
                <div class="quick-btn-label">RAPORLAR ▾</div>
              </div>
              <div class="quick-btn" onclick="analizAc()">
                <div class="quick-btn-icon">🔍</div>
                <div class="quick-btn-label">ANALİZ ▾</div>
              </div>
              <div class="quick-btn" onclick="arsivAc()">
                <div class="quick-btn-icon">📁</div>
                <div class="quick-btn-label">ARŞİV</div>
              </div>
            </div>

            <!-- RAPORLAR ALT MENÜ -->
            <div class="quick-sub fade-in" id="raporlarSub" style="display:flex; animation-delay:0.04s;">
              <div class="quick-sub-btn" onclick="navGit('gunluk')">📋 Günlük Rapor</div>
              <div class="quick-sub-btn" onclick="navGit('sesli')">🎤 Sesli Rapor</div>
              <div class="quick-sub-btn" onclick="pdfIndir()">📄 PDF İndir</div>
              <div class="quick-sub-btn" onclick="haftalikRaporIndir()">📊 Haftalık Rapor</div>
            </div>

            <!-- ANALİZ ALT MENÜ -->
            <div class="quick-sub fade-in" id="analizSub" style="display:none; animation-delay:0.04s;">
              <div class="quick-sub-btn" onclick="navGit('kamera')">📷 Kamera Analizi</div>
              <div class="quick-sub-btn" onclick="navGit('deprem')">🌍 Deprem Analizi</div>
            </div>

            <!-- ARAMA KUTUSU -->
            <div class="search-wrap fade-in" style="animation-delay:0.08s;">
              <div class="search-border"></div>
              <div class="search-box">
                <div class="search-icons">
                  <div class="search-icon cam" onclick="document.getElementById('photoInput').click()" title="Fotoğraf yükle">📷</div>
                  <div class="search-icon tool" onclick="navGit('hesaplama')" title="Hesaplama">🔧</div>
                </div>
                <div class="search-mid">
                  <div class="search-label">AI Asistan</div>
                  <input
                    class="search-input-real"
                    id="userInput"
                    placeholder="Soru sor, hesap seç veya saha fotoğrafı yükle..."
                    onkeydown="if(event.key==='Enter') sorularGonder()"
                  />
                </div>
                <button class="search-send" onclick="sorularGonder()">→</button>
              </div>
            </div>

            <!-- SONUÇ KUTUSU -->
            <div class="result-wrap fade-in" style="animation-delay:0.12s;">
              <div class="result-border"></div>
              <div class="result-box" id="result">
                <div class="result-header">
                  <div class="result-live-dot"></div>
                  <div class="result-title">🏗️ Mühendislik Paneli Hazır<span style="display:inline-flex;align-items:center;gap:4px;background:#16a34a;color:white;font-size:11px;font-weight:700;padding:2px 10px;border-radius:12px;margin-left:10px;vertical-align:middle;"><span style="width:6px;height:6px;border-radius:50%;background:white;display:inline-block;animation:livepulse 1.5s infinite;"></span>LIVE</span></div>
                  <div class="result-live-tag">LIVE</div>
                </div>
                <div class="result-body">
                  Kamera analizi, mühendislik hesapları ve raporlama araçlarına hazırsınız.
                  Soru sorabilir, fotoğraf yükleyebilir veya bir hesaplama başlatabilirsiniz.
                </div>
                <div style="display:flex;gap:10px;margin-top:16px;flex-wrap:wrap;padding-bottom:8px;">
                  <span style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);padding:7px 16px;border-radius:20px;font-size:13px;color:#e2e8f0;">🏗️ Aktif Kamera: <span id="statKamera">12</span></span>
                  <span style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);padding:7px 16px;border-radius:20px;font-size:13px;color:#e2e8f0;">📊 Günlük İlerleme: %<span id="statIlerleme">87</span></span>
                  <span style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);padding:7px 16px;border-radius:20px;font-size:13px;color:#e2e8f0;">🔔 Güvenlik Uyarısı: <span id="statGuvenlik">0</span></span>
                </div>
              </div>
            </div>

          </div><!-- /content -->
        </div><!-- /mainArea -->

      </div><!-- /bodyRow -->
    </div><!-- /app -->

</div><!-- /mainApp -->

<!-- Gizli fotoğraf input -->
<input type="file" id="photoInput" accept="image/*" style="display:none" onchange="fotoYukle(this)">
<input type="file" id="fileInput" accept="image/*" style="display:none" onchange="resimSecildi(event)">

<!-- ===== KAMERA MODALİ ===== -->
<div id="kameraModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
    <div style="background:#1a1d21; border-radius:20px; padding:25px; width:90%; max-width:480px; border:1px solid rgba(230,126,34,0.3);">
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

<!-- ===== ARŞİV MODALİ ===== -->
<div id="arsivModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
    <div style="background:#1a1d21; border-radius:20px; padding:25px; width:90%; max-width:520px; border:1px solid rgba(139,92,246,0.3); max-height:80vh; overflow-y:auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; position:sticky; top:0; background:#1a1d21; padding-bottom:10px;">
            <h3 style="color:#8b5cf6; margin:0;">📁 Arşivim</h3>
            <button onclick="arsivKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
        </div>
        <div id="arsivIcerik"></div>
    </div>
</div>

<!-- ===== MÜHENDİSLİK PANELİ ===== -->
<div id="sidebarPanel" class="sidebar" style="padding:28px 28px 40px;">
    <h2 style="color:var(--primary);">📊 Mühendislik Paneli</h2>
    <p style="color:gray; font-size:0.75rem; margin-bottom:20px;">Onlarca Profesyonel Saha Hesabı</p>
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
    <button class="btn-read" onclick="toggleSidebar()" style="width:100%; margin-top:30px; border-color:#888; color:#888;">KAPAT</button>
</div>

<!-- ===== HESAPLAMA MODALİ ===== -->
<div id="inputModal" class="modal-overlay">
    <div class="modal-content">
        <div id="modalTitle" class="modal-header">Hesaplama Parametreleri</div>
        <div id="modalBody" class="modal-body"></div>
        <div class="modal-footer">
            <button class="modal-btn btn-cancel" onclick="closeModal()">İPTAL</button>
            <button class="modal-btn btn-confirm" onclick="submitModal()">HESAPLA</button>
        </div>
    </div>
</div>

<!-- ===== GÜNLÜK RAPOR MODALİ ===== -->
<div id="gunlukRaporModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
    <div style="background:#1a1d21; border-radius:20px; padding:25px; width:90%; max-width:520px; border:1px solid rgba(230,126,34,0.3); max-height:85vh; overflow-y:auto;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
            <h3 style="color:#e67e22; margin:0;">📝 Günlük Rapor</h3>
            <button onclick="gunlukRaporKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
        </div>
        <div style="display:flex; flex-direction:column; gap:12px;">
            <div>
                <label style="color:#aaa; font-size:0.85rem;">📅 Tarih</label>
                <input type="date" id="grTarih" class="auth-input" style="margin-top:5px;">
            </div>
            <div>
                <label style="color:#aaa; font-size:0.85rem;">👷 Bugün kaç işçi çalıştı?</label>
                <input type="number" id="grIsci" class="auth-input" placeholder="Örn: 12" style="margin-top:5px;">
            </div>
            <div>
                <label style="color:#aaa; font-size:0.85rem;">✅ Bugün yapılan işler</label>
                <textarea id="grYapilanlar" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:10px; min-height:80px; font-family:Arial; font-size:0.9rem; margin-top:5px; resize:vertical; box-sizing:border-box;" placeholder="Örn: 3. kat döşeme betonu döküldü..."></textarea>
            </div>
            <div>
                <label style="color:#aaa; font-size:0.85rem;">⚠️ Sorunlar / Riskler</label>
                <textarea id="grSorunlar" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:10px; min-height:60px; font-family:Arial; font-size:0.9rem; margin-top:5px; resize:vertical; box-sizing:border-box;" placeholder="Örn: Malzeme gecikmesi..."></textarea>
            </div>
            <div>
                <label style="color:#aaa; font-size:0.85rem;">📅 Yarın yapılacaklar</label>
                <textarea id="grYarin" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:10px; min-height:60px; font-family:Arial; font-size:0.9rem; margin-top:5px; resize:vertical; box-sizing:border-box;" placeholder="Örn: 4. kat kolon kalıpları kurulacak..."></textarea>
            </div>
            <div>
                <label style="color:#aaa; font-size:0.85rem;">🦺 İSG Durumu</label>
                <select id="grIsg" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:10px; font-size:0.9rem; margin-top:5px;">
                    <option value="iyi">✅ İyi — İhlal yok</option>
                    <option value="orta">⚠️ Orta — Küçük ihlaller var</option>
                    <option value="kotu">🚨 Kötü — Ciddi ihlaller var</option>
                </select>
            </div>
        </div>
        <button onclick="gunlukRaporOlustur()" style="width:100%; margin-top:20px; padding:14px; background:#e67e22; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold; font-size:1rem;">🤖 AI ile Rapor Oluştur</button>
        <div id="gunlukRaporSonuc" style="margin-top:15px;"></div>
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
  <div style="background:#1a1d21; border:1px solid rgba(249,115,22,0.3); border-radius:24px; padding:28px; width:92%; max-width:640px; max-height:88vh; overflow-y:auto;">
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
  <div style="background:#1a1d21; border:1px solid rgba(249,115,22,0.3); border-radius:24px; padding:28px; width:92%; max-width:680px; max-height:90vh; overflow-y:auto;">
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
  <div style="background:#1a1d21; border:1px solid rgba(249,115,22,0.3); border-radius:24px; padding:28px; width:95%; max-width:900px; max-height:92vh; overflow-y:auto;">
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

<!-- ŞANTİYE DASHBOARD MODAL -->
<div id="santiyeModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:9000; overflow-y:auto; padding:20px;">
  <div style="max-width:1100px; margin:0 auto; background:#1a1a2e; border-radius:24px; border:1px solid rgba(255,255,255,0.1); overflow:hidden;">
    <div style="background:linear-gradient(135deg,#e67e22,#d35400); padding:24px 28px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <h2 style="margin:0; color:white; font-size:1.4rem;">🏗️ Şantiye Dashboard</h2>
        <div style="color:rgba(255,255,255,0.7); font-size:0.85rem; margin-top:4px;">Tüm şantiyelerinizi yönetin</div>
      </div>
      <div style="display:flex; gap:10px; align-items:center;">
        <button onclick="santiyeEkleModalAc(null)" style="background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.3); color:white; padding:8px 18px; border-radius:10px; cursor:pointer; font-weight:700;">+ Yeni Şantiye</button>
        <button onclick="santiyeModalKapat()" style="background:rgba(255,255,255,0.1); border:none; color:white; width:36px; height:36px; border-radius:50%; cursor:pointer; font-size:1.2rem;">✕</button>
      </div>
    </div>
    <div style="padding:24px;">
      <div id="santiyeOzet" style="display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:24px;"></div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:24px;">
        <div>
          <div style="color:#aaa; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">📍 Harita</div>
          <div id="santiyeHarita" style="height:300px; border-radius:14px; overflow:hidden; border:1px solid rgba(255,255,255,0.1);"></div>
        </div>
        <div>
          <div style="color:#aaa; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">📊 Karşılaştırma</div>
          <div id="santiyeTablo" style="max-height:300px; overflow-y:auto;"></div>
        </div>
      </div>
      <div style="color:#aaa; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">🗂️ Şantiyeler</div>
      <div id="santiyeKartlar" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px;"></div>
    </div>
  </div>
</div>

<!-- GÜVENLİK MODALI -->
<div id="guvenlikModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:9999; align-items:flex-start; justify-content:center; overflow-y:auto; padding:20px; backdrop-filter:blur(8px);">
  <div style="background:#0f1a2e; border:1px solid rgba(255,255,255,0.10); border-radius:24px; width:100%; max-width:900px; overflow:hidden; margin:auto;">

    <!-- Header -->
    <div style="background:linear-gradient(135deg,#dc2626,#991b1b); padding:22px 28px; display:flex; justify-content:space-between; align-items:center;">
      <div>
        <h2 style="margin:0; color:white; font-size:1.3rem;">🦺 Güvenlik Modülü</h2>
        <div style="color:rgba(255,255,255,0.7); font-size:0.85rem; margin-top:4px;" id="guvenlikTarih"></div>
      </div>
      <div style="display:flex; align-items:center; gap:16px;">
        <div style="text-align:center;">
          <div id="guvenlikSkor" style="font-size:2rem; font-weight:800; color:white;">--</div>
          <div style="font-size:0.7rem; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:1px;">Güvenlik Skoru</div>
        </div>
        <button onclick="guvenlikKapat()" style="background:rgba(255,255,255,0.15); border:none; color:white; width:36px; height:36px; border-radius:50%; cursor:pointer; font-size:1.2rem;">✕</button>
      </div>
    </div>

    <!-- Stat row -->
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px; padding:16px 24px; border-bottom:1px solid rgba(255,255,255,0.08);">
      <div style="background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.2); border-radius:12px; padding:12px; text-align:center;">
        <div id="stat-guvenli-gun" style="font-size:1.6rem; font-weight:800; color:#22c55e;">0</div>
        <div style="font-size:0.7rem; color:#aaa; margin-top:2px;">Güvenli Gün</div>
      </div>
      <div style="background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.2); border-radius:12px; padding:12px; text-align:center;">
        <div id="stat-acik-uyari" style="font-size:1.6rem; font-weight:800; color:#f59e0b;">0</div>
        <div style="font-size:0.7rem; color:#aaa; margin-top:2px;">Açık Uyarı</div>
      </div>
      <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.2); border-radius:12px; padding:12px; text-align:center;">
        <div id="stat-olay" style="font-size:1.6rem; font-weight:800; color:#ef4444;">0</div>
        <div style="font-size:0.7rem; color:#aaa; margin-top:2px;">Olay Bu Ay</div>
      </div>
      <div style="background:rgba(59,130,246,0.1); border:1px solid rgba(59,130,246,0.2); border-radius:12px; padding:12px; text-align:center;">
        <div id="stat-ekipman" style="font-size:1.6rem; font-weight:800; color:#3b82f6;">0</div>
        <div style="font-size:0.7rem; color:#aaa; margin-top:2px;">Ekipman OK</div>
      </div>
    </div>

    <!-- Tabs -->
    <div style="display:flex; gap:6px; padding:14px 24px; border-bottom:1px solid rgba(255,255,255,0.08); flex-wrap:wrap;">
      <button class="g-tab active" onclick="gTab('isg',this)">🦺 İSG Kontrol</button>
      <button class="g-tab" onclick="gTab('ekipman',this)">🏗️ Ekipman</button>
      <button class="g-tab" onclick="gTab('hava',this)">🌡️ Hava Uyarıları</button>
      <button class="g-tab" onclick="gTab('olay',this)">⚠️ Olay Bildir</button>
      <button class="g-tab" onclick="gTab('acil',this)">🚨 Acil Durum</button>
    </div>

    <!-- Tab: ISG -->
    <div id="gtab-isg" class="g-tab-content" style="padding:20px 24px;">
      <div style="margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="color:white; font-weight:700;">Kişisel Koruyucu Donanım</div>
          <div id="isg-progress-1" style="font-size:0.8rem; color:#aaa;">0/5</div>
        </div>
        <div id="isg-kkd-list">
          <div class="g-check-item" data-group="kkd" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Baret / Koruyucu Kask</div><div class="g-check-sub">Tüm personel için zorunlu</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="kkd" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Reflektif Yelek</div><div class="g-check-sub">Görünürlük için</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="kkd" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Güvenlik Botu — Çelik Burunlu</div><div class="g-check-sub">Tüm saha personeli</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="kkd" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Koruyucu Gözlük</div><div class="g-check-sub">Kaynak ve kesme işlemleri</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="kkd" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Emniyet Kemeri / Güvenlik Halatı</div><div class="g-check-sub">Yüksekte çalışma zorunlu</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        </div>
      </div>
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
          <div style="color:white; font-weight:700;">Saha Güvenliği</div>
          <div id="isg-progress-2" style="font-size:0.8rem; color:#aaa;">0/6</div>
        </div>
        <div id="isg-saha-list">
          <div class="g-check-item" data-group="saha" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Güvenlik Barikatları Yerinde</div><div class="g-check-sub">Çevre ve kazı güvenliği</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="saha" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Yangın Söndürücü Erişilebilir</div><div class="g-check-sub">Son kontrol tarihi geçerli mi?</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="saha" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">İlk Yardım Çantası Dolu</div><div class="g-check-sub">Malzeme eksiği var mı?</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="saha" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Acil Çıkış Yolları Açık</div><div class="g-check-sub">Tahliye rotası engelsiz</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="saha" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Uyarı Levhaları Yerinde</div><div class="g-check-sub">Risk bölgeleri işaretli</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
          <div class="g-check-item" data-group="saha" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Aydınlatma Yeterli</div><div class="g-check-sub">Gece çalışma varsa zorunlu</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        </div>
      </div>
      <button onclick="guvenlikRaporuKaydet()" style="width:100%; margin-top:20px; padding:14px; background:#dc2626; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:700; font-size:0.95rem;">💾 Günlük İSG Kontrol Raporunu Kaydet</button>
    </div>

    <!-- Tab: Ekipman -->
    <div id="gtab-ekipman" class="g-tab-content" style="display:none; padding:20px 24px;">
      <div id="ekipman-list">
        <div class="g-check-item" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Kule Vinci — Günlük Kontrol</div><div class="g-check-sub">Kablo, fren, yük kapasitesi, operatör sertifikası</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        <div class="g-check-item" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">İskele Stabilitesi</div><div class="g-check-sub">Bağlantı noktaları, yük taşıma kapasitesi</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        <div class="g-check-item" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Elektrik Panosu Güvenliği</div><div class="g-check-sub">Topraklama, kaçak akım rölesi (RCD)</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        <div class="g-check-item" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">İş Makinesi — Yağ & Su & Fren</div><div class="g-check-sub">Günlük bakım kontrol listesi</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        <div class="g-check-item" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Beton Mikseri</div><div class="g-check-sub">Döner tambur, karıştırma bıçakları</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        <div class="g-check-item" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Jeneratör</div><div class="g-check-sub">Yakıt seviyesi, egzoz güvenliği</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        <div class="g-check-item" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Kazıcı / Ekskavatör</div><div class="g-check-sub">Hidrolik sistem, kova durumu</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
        <div class="g-check-item" onclick="gToggle(this)"><div class="g-checkbox">○</div><div><div class="g-check-label">Taşlama & Kesme Ekipmanları</div><div class="g-check-sub">Disk durumu, koruyucu kapak</div></div><span class="g-badge g-badge-warn">Kontrol Et</span></div>
      </div>
      <button onclick="ekipmanRaporuKaydet()" style="width:100%; margin-top:20px; padding:14px; background:#dc2626; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:700;">💾 Ekipman Kontrol Raporunu Kaydet</button>
    </div>

    <!-- Tab: Hava -->
    <div id="gtab-hava" class="g-tab-content" style="display:none; padding:20px 24px;">
      <div id="hava-uyarilari" style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:16px; text-align:center; color:#aaa;">
          Hava durumu yükleniyor...
        </div>
      </div>
    </div>

    <!-- Tab: Olay -->
    <div id="gtab-olay" class="g-tab-content" style="display:none; padding:20px 24px;">
      <div style="display:flex; flex-direction:column; gap:12px;">
        <select id="olayTur" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:12px; border-radius:10px; outline:none; font-size:0.9rem;">
          <option value="">Olay Türü Seçin</option>
          <option>Kaza / Yaralanma</option>
          <option>Tehlikeli Durum</option>
          <option>Ekipman Arızası</option>
          <option>Malzeme Hasarı</option>
          <option>Yangın / Yangın Riski</option>
          <option>İSG İhlali</option>
          <option>Diğer</option>
        </select>
        <select id="olaySiddet" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:12px; border-radius:10px; outline:none; font-size:0.9rem;">
          <option value="">Şiddet Derecesi</option>
          <option value="dusuk">🟢 Düşük — Küçük olay, tıbbi müdahale gerekmedi</option>
          <option value="orta">🟡 Orta — Tıbbi müdahale gerekti</option>
          <option value="yuksek">🔴 Yüksek — Ciddi yaralanma / acil durum</option>
        </select>
        <input type="text" id="olayKonum" placeholder="Konum (Ör: 3. kat, kuzey cephe, bodrum)" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:12px; border-radius:10px; outline:none; font-size:0.9rem;">
        <input type="text" id="olayKisi" placeholder="Etkilenen kişi sayısı ve isimleri" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:12px; border-radius:10px; outline:none; font-size:0.9rem;">
        <textarea id="olayAciklama" placeholder="Olay detaylı açıklaması..." style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:12px; border-radius:10px; outline:none; font-size:0.9rem; min-height:100px; resize:vertical;"></textarea>
        <textarea id="olayOnlem" placeholder="Alınan önlemler ve yapılan müdahale..." style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:12px; border-radius:10px; outline:none; font-size:0.9rem; min-height:80px; resize:vertical;"></textarea>
        <button onclick="olayBildir()" style="width:100%; padding:14px; background:#dc2626; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:700; font-size:0.95rem;">🚨 Olay Bildir & Kaydet</button>
        <div id="olayMsg" style="text-align:center; font-size:0.85rem;"></div>
      </div>
    </div>

    <!-- Tab: Acil -->
    <div id="gtab-acil" class="g-tab-content" style="display:none; padding:20px 24px;">
      <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:20px;">
        <a href="tel:112" style="background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.3); border-radius:14px; padding:18px 12px; text-align:center; text-decoration:none; transition:all .2s;" onmouseover="this.style.background='rgba(239,68,68,0.25)'" onmouseout="this.style.background='rgba(239,68,68,0.15)'">
          <div style="font-size:1.8rem; margin-bottom:6px;">🚑</div>
          <div style="color:white; font-weight:700; font-size:0.9rem;">Ambulans</div>
          <div style="color:#ef4444; font-size:1.1rem; font-weight:800; margin-top:4px;">112</div>
        </a>
        <a href="tel:110" style="background:rgba(249,115,22,0.15); border:1px solid rgba(249,115,22,0.3); border-radius:14px; padding:18px 12px; text-align:center; text-decoration:none; transition:all .2s;" onmouseover="this.style.background='rgba(249,115,22,0.25)'" onmouseout="this.style.background='rgba(249,115,22,0.15)'">
          <div style="font-size:1.8rem; margin-bottom:6px;">🚒</div>
          <div style="color:white; font-weight:700; font-size:0.9rem;">İtfaiye</div>
          <div style="color:#f97316; font-size:1.1rem; font-weight:800; margin-top:4px;">110</div>
        </a>
        <a href="tel:155" style="background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3); border-radius:14px; padding:18px 12px; text-align:center; text-decoration:none; transition:all .2s;" onmouseover="this.style.background='rgba(59,130,246,0.25)'" onmouseout="this.style.background='rgba(59,130,246,0.15)'">
          <div style="font-size:1.8rem; margin-bottom:6px;">👮</div>
          <div style="color:white; font-weight:700; font-size:0.9rem;">Polis</div>
          <div style="color:#3b82f6; font-size:1.1rem; font-weight:800; margin-top:4px;">155</div>
        </a>
        <a href="tel:186" style="background:rgba(234,179,8,0.15); border:1px solid rgba(234,179,8,0.3); border-radius:14px; padding:18px 12px; text-align:center; text-decoration:none; transition:all .2s;" onmouseover="this.style.background='rgba(234,179,8,0.25)'" onmouseout="this.style.background='rgba(234,179,8,0.15)'">
          <div style="font-size:1.8rem; margin-bottom:6px;">⚡</div>
          <div style="color:white; font-weight:700; font-size:0.9rem;">Elektrik Arıza</div>
          <div style="color:#eab308; font-size:1.1rem; font-weight:800; margin-top:4px;">186</div>
        </a>
        <a href="tel:187" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); border-radius:14px; padding:18px 12px; text-align:center; text-decoration:none; transition:all .2s;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
          <div style="font-size:1.8rem; margin-bottom:6px;">💧</div>
          <div style="color:white; font-weight:700; font-size:0.9rem;">Doğalgaz Arıza</div>
          <div style="color:#aaa; font-size:1.1rem; font-weight:800; margin-top:4px;">187</div>
        </a>
        <a href="tel:182" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); border-radius:14px; padding:18px 12px; text-align:center; text-decoration:none; transition:all .2s;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='rgba(255,255,255,0.05)'">
          <div style="font-size:1.8rem; margin-bottom:6px;">🏥</div>
          <div style="color:white; font-weight:700; font-size:0.9rem;">ALO Doktor</div>
          <div style="color:#aaa; font-size:1.1rem; font-weight:800; margin-top:4px;">182</div>
        </a>
      </div>
      <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:16px; margin-bottom:16px;">
        <div style="color:#f97316; font-weight:700; margin-bottom:12px;">📍 Toplanma Noktası</div>
        <input type="text" id="toplanmaNoktasi" placeholder="Toplanma noktası adresini girin..." style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:10px; border-radius:8px; outline:none; font-size:0.9rem; margin-bottom:10px; box-sizing:border-box;">
        <button onclick="toplanmaKaydet()" style="padding:10px 20px; background:#f97316; color:black; border:none; border-radius:8px; cursor:pointer; font-weight:700;">Kaydet</button>
      </div>
      <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:14px; padding:16px;">
        <div style="color:#f97316; font-weight:700; margin-bottom:12px;">👷 Şantiye Sorumlusu</div>
        <input type="text" id="sorumlAd" placeholder="Ad Soyad" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:10px; border-radius:8px; outline:none; font-size:0.9rem; margin-bottom:8px; box-sizing:border-box;">
        <input type="tel" id="sorumlTel" placeholder="Telefon numarası" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.12); color:white; padding:10px; border-radius:8px; outline:none; font-size:0.9rem; margin-bottom:10px; box-sizing:border-box;">
        <button onclick="sorumlKaydet()" style="padding:10px 20px; background:#f97316; color:black; border:none; border-radius:8px; cursor:pointer; font-weight:700;">Kaydet</button>
      </div>
    </div>

  </div>
</div>

<!-- ŞANTİYE FORM MODAL -->
<div id="santiyeFormModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.9); z-index:9100; align-items:center; justify-content:center; padding:20px;">
  <div style="background:#1a1a2e; border-radius:20px; border:1px solid rgba(255,255,255,0.1); width:100%; max-width:500px; overflow:hidden;">
    <div style="background:linear-gradient(135deg,#e67e22,#d35400); padding:20px 24px; display:flex; justify-content:space-between; align-items:center;">
      <h3 id="santiyeFormBaslik" style="margin:0; color:white;">Şantiye Ekle</h3>
      <button onclick="santiyeFormKapat()" style="background:rgba(255,255,255,0.1); border:none; color:white; width:32px; height:32px; border-radius:50%; cursor:pointer; font-size:1.1rem;">✕</button>
    </div>
    <div style="padding:24px;">
      <input type="hidden" id="santiyeFormId">
      <input type="text" id="santiyeFormAd" class="auth-input" placeholder="Şantiye Adı *">
      <input type="text" id="santiyeFormKonum" class="auth-input" placeholder="Konum (Şehir, İlçe) *">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <input type="number" id="santiyeFormLat" class="auth-input" placeholder="Enlem (opsiyonel)" step="0.0001" style="margin-bottom:0;">
        <input type="number" id="santiyeFormLon" class="auth-input" placeholder="Boylam (opsiyonel)" step="0.0001" style="margin-bottom:0;">
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <div>
          <label style="color:#aaa; font-size:0.78rem; display:block; margin-bottom:4px;">İlerleme (%)</label>
          <input type="number" id="santiyeFormIlerleme" class="auth-input" placeholder="0-100" min="0" max="100" value="0" style="margin-bottom:0;">
        </div>
        <div>
          <label style="color:#aaa; font-size:0.78rem; display:block; margin-bottom:4px;">İşçi Sayısı</label>
          <input type="number" id="santiyeFormIsci" class="auth-input" placeholder="Kişi sayısı" min="0" value="0" style="margin-bottom:0;">
        </div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <div>
          <label style="color:#aaa; font-size:0.78rem; display:block; margin-bottom:4px;">Durum</label>
          <select id="santiyeFormDurum" class="auth-input" style="margin-bottom:0;">
            <option value="iyi">✅ İyi</option><option value="dikkat">⚠️ Dikkat</option><option value="sorun">❌ Sorun</option>
          </select>
        </div>
        <div>
          <label style="color:#aaa; font-size:0.78rem; display:block; margin-bottom:4px;">İSG Durumu</label>
          <input type="text" id="santiyeFormIsg" class="auth-input" placeholder="İSG notu" style="margin-bottom:0;">
        </div>
      </div>
      <textarea id="santiyeFormNotlar" class="auth-input" placeholder="Notlar (opsiyonel)" rows="3" style="resize:vertical;"></textarea>
      <div id="santiyeFormMsg" style="margin-top:8px;"></div>
      <button onclick="santiyeKaydet()" class="auth-btn" style="margin-top:12px;">💾 Kaydet</button>
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
