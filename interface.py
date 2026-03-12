from styles import CSS_STYLE
from scripts import JS_SCRIPT

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <title>BuildingAI Pro</title>
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
        .plan-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px; }}
        .plan-card {{ background: rgba(255,255,255,0.04); border: 2px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 20px; cursor: pointer; transition: 0.3s; text-align: center; }}
        .plan-card:hover, .plan-card.selected {{ border-color: var(--primary); background: rgba(230,126,34,0.1); }}
        .plan-card h3 {{ color: var(--primary); margin: 0 0 8px 0; font-size: 1.1rem; }}
        .plan-card .price {{ font-size: 1.6rem; font-weight: 800; color: white; }}
        .plan-card .price span {{ font-size: 0.8rem; color: #aaa; font-weight: 400; }}
        .plan-card ul {{ list-style: none; padding: 0; margin: 10px 0 0 0; text-align: left; }}
        .plan-card ul li {{ color: #ccc; font-size: 0.8rem; padding: 3px 0; }}
        .plan-card ul li::before {{ content: "✓ "; color: #2ecc71; font-weight: 800; }}

        /* ---- PROFILE ---- */
        .profile-header {{ display: flex; align-items: center; gap: 20px; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #333; }}
        .profile-avatar {{ width: 70px; height: 70px; background: var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800; color: white; flex-shrink: 0; }}
        .profile-badge {{ background: rgba(230,126,34,0.2); border: 1px solid var(--primary); color: var(--primary); padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }}
        .profile-stat {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 15px; text-align: center; }}
        .profile-stat .stat-value {{ font-size: 1.8rem; font-weight: 800; color: var(--primary); }}
        .profile-stat .stat-label {{ font-size: 0.75rem; color: #aaa; margin-top: 4px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 25px; }}

        /* ---- MESSAGES ---- */
        .msg-success {{ background: rgba(46,204,113,0.15); border: 1px solid #2ecc71; color: #2ecc71; padding: 12px; border-radius: 10px; font-size: 0.9rem; margin-top: 10px; text-align: center; }}
        .msg-error {{ background: rgba(231,76,60,0.15); border: 1px solid #e74c3c; color: #e74c3c; padding: 12px; border-radius: 10px; font-size: 0.9rem; margin-top: 10px; text-align: center; }}

        .auth-link {{ color: var(--primary); cursor: pointer; font-size: 0.85rem; text-align: center; margin-top: 15px; display: block; }}
        .auth-link:hover {{ text-decoration: underline; }}
        .active-lang {{ background: rgba(230,126,34,0.3) !important; border-color: var(--primary) !important; color: white !important; }}
        .divider {{ border: none; border-top: 1px solid #333; margin: 20px 0; }}
    </style>
</head>
<body>

    <!-- ===== AUTH OVERLAY ===== -->
    <div id="auth-overlay">
        <div class="auth-card" style="max-width: 420px; width: 90%;">

            <!-- LOGIN PANEL -->
            <div id="panel-login">
                <!-- Dil Seçimi -->
                <div style="display:flex; justify-content:flex-end; gap:8px; margin-bottom:15px;">
                    <button id="langBtn_tr" class="lang-btn active-lang" onclick="dilDegistir('tr')" style="background:rgba(255,255,255,0.08); border:2px solid var(--primary); border-radius:10px; padding:5px 12px; color:white; cursor:pointer; font-size:0.85rem; font-weight:700; transition:0.3s;">🇹🇷 TR</button>
                    <button id="langBtn_en" class="lang-btn" onclick="dilDegistir('en')" style="background:rgba(255,255,255,0.04); border:2px solid rgba(255,255,255,0.15); border-radius:10px; padding:5px 12px; color:#aaa; cursor:pointer; font-size:0.85rem; font-weight:700; transition:0.3s;">🇬🇧 EN</button>
                </div>
                <div class="auth-tabs">
                    <button class="auth-tab tab-login active" onclick="switchPanel('login')">Giriş Yap</button>
                    <button class="auth-tab tab-register" onclick="switchPanel('register')">Kayıt Ol</button>
                </div>
                <h2 id="loginTitleEl" style="text-align:center; margin-bottom:25px;">🏗️ BuildingAI Pro</h2>
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
                <div class="plan-grid">
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
                        <div class="price">₺299 <span>/ay</span></div>
                        <ul>
                            <li>Sınırsız AI sorgu</li>
                            <li>Fotoğraf analizi</li>
                            <li>WhatsApp entegrasyon</li>
                            <li>Kamera bağlantısı</li>
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
                <div class="profile-stat">
                    <div class="stat-value" id="statRapor">0</div>
                    <div class="stat-label">Rapor</div>
                </div>
                <div class="profile-stat">
                    <div class="stat-value" id="statSorgu">0</div>
                    <div class="stat-label">AI Sorgu</div>
                </div>
                <div class="profile-stat">
                    <div class="stat-value" id="statGun">0</div>
                    <div class="stat-label">Aktif Gün</div>
                </div>
            </div>

            <hr class="divider">
            <div style="display:flex; gap:8px; margin-bottom:4px;">
                <button onclick="closeProfile(); odemePaneliAc('pro');" style="flex:1; padding:12px; background:linear-gradient(135deg,#6366f1,#818cf8); border:none; color:white; border-radius:14px; cursor:pointer; font-weight:700; font-size:0.9rem; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
                    ⚡ PRO — 650 TL/ay
                </button>
                <button onclick="closeProfile(); odemePaneliAc('max');" style="flex:1; padding:12px; background:linear-gradient(135deg,#b7791f,#f1c40f); border:none; color:#111; border-radius:14px; cursor:pointer; font-weight:700; font-size:0.9rem; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
                    👑 MAX — 1.990 TL/ay
                </button>
            </div>

            <hr class="divider">
            <button onclick="closeProfile(); rolSifirla();" style="width:100%; padding:12px; background:rgba(99,102,241,0.1); border:1px solid rgba(99,102,241,0.3); color:#818cf8; border-radius:14px; cursor:pointer; font-weight:700; margin-bottom:12px; transition:0.3s;" onmouseover="this.style.background='rgba(99,102,241,0.2)'" onmouseout="this.style.background='rgba(99,102,241,0.1)'">
                🔄 Rolümü Değiştir
            </button>

            <hr class="divider">
            <button onclick="cikisYap()" style="width:100%; padding:14px; background:rgba(231,76,60,0.15); border:1px solid #e74c3c; color:#e74c3c; border-radius:14px; cursor:pointer; font-weight:700; transition:0.3s;" onmouseover="this.style.background='rgba(231,76,60,0.3)'" onmouseout="this.style.background='rgba(231,76,60,0.15)'">
                🚪 Çıkış Yap
            </button>
        </div>
    </div>

    <div id="sidebarOverlay" class="sidebar-overlay" onclick="toggleSidebar()"></div>

    <!-- ===== NAV SIDEBAR ===== -->
    <div id="navSidebar" class="nav-sidebar" style="display:none;">
        <div class="nav-logo">
            <span class="nav-logo-icon">🏗️</span>
            <span class="nav-logo-text">BuildingAI Pro</span>
        </div>
        <div class="nav-links" id="navLinks">
            <div class="nav-item active" id="nav-home" onclick="navGit('home')">
                <span class="nav-icon">🏠</span>
                <span class="nav-label">Ana Sayfa</span>
            </div>
            <div class="nav-item" id="nav-kamera" onclick="navGit('kamera')">
                <span class="nav-icon">📷</span>
                <span class="nav-label">Kamera Analizi</span>
            </div>
            <div class="nav-item" id="nav-hesaplama" onclick="navGit('hesaplama')">
                <span class="nav-icon">🧮</span>
                <span class="nav-label">Hesaplama</span>
            </div>
            <div class="nav-item" id="nav-arsiv" onclick="navGit('arsiv')">
                <span class="nav-icon">📁</span>
                <span class="nav-label">Arşiv</span>
            </div>
            <div class="nav-item" id="nav-gunluk" onclick="navGit('gunluk')">
                <span class="nav-icon">📝</span>
                <span class="nav-label">Günlük Rapor</span>
            </div>
            <div class="nav-item" id="nav-sesli" onclick="navGit('sesli')">
                <span class="nav-icon">🎤</span>
                <span class="nav-label">Sesli Rapor</span>
            </div>
            <div class="nav-item" id="nav-fiyat" onclick="navGit('fiyat')">
                <span class="nav-icon">📊</span>
                <span class="nav-label">Fiyat Takibi</span>
            </div>
            <div class="nav-item" id="nav-stok" onclick="navGit('stok')">
                <span class="nav-icon">📦</span>
                <span class="nav-label">Stok Takibi</span>
            </div>
            <div class="nav-item" id="nav-deprem" onclick="navGit('deprem')">
                <span class="nav-icon">🌍</span>
                <span class="nav-label">Deprem Analizi</span>
            </div>
            <div class="nav-item" id="nav-santiye" onclick="navGit('santiye')" data-rol="muteahhit">
                <span class="nav-icon">🏗️</span>
                <span class="nav-label">Şantiye Dashboard</span>
            </div>
        </div>
        <div class="nav-bottom">
            <div class="nav-item" onclick="openProfile()">
                <span class="nav-icon">👤</span>
                <span class="nav-label">Profil</span>
            </div>
        </div>
    </div>

    <!-- NAV MOBILE OVERLAY -->
    <div id="navOverlay" class="nav-overlay" onclick="closeMobileNav()"></div>

    <!-- ===== TOP HEADER ===== -->
    <div id="topHeader" class="top-header" style="display:none;">
        <button class="header-hamburger" id="hamburgerBtn" onclick="toggleMobileNav()">☰</button>
        <button class="header-collapse-btn" id="collapseBtn" onclick="toggleNavSidebar()">◀</button>
        <div class="header-title" id="headerTitle">🏠 Ana Sayfa</div>
        <div class="header-right">
            <div class="weather-inline">
                <select id="citySelect" class="city-select-inline" onchange="havaGuncelle()">
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
                <div class="weather-data">
                    <span class="weather-temp" id="temp">--°C</span>
                    <span class="weather-cond" id="condition">Yükleniyor...</span>
                </div>
            </div>
            <div class="theme-toggle" onclick="temaToggle()" title="Dark/Light mod"></div>
            <div class="header-profile-btn" onclick="openProfile()" title="Profilim">👤</div>
        </div>
    </div>

    <div id="historySidebar" style="position: fixed; top: 0; left: -350px; width: 320px; height: 100vh; background: #161625; border-right: 1px solid #333; box-shadow: 5px 0 20px rgba(0,0,0,0.8); transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1); z-index: 1000; display: flex; flex-direction: column; padding: 25px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; padding-bottom: 15px; margin-bottom: 15px;">
            <h3 style="color: #f1c40f; margin: 0; font-size: 1.2rem;">🗂️ Şantiye Arşivi</h3>
            <button onclick="toggleHistory()" style="background: none; border: none; color: white; font-size: 1.5rem; cursor: pointer;">✖</button>
        </div>
        <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px;">
            <label style="color:#aaa; font-size:0.8rem;">Tarihe Göre Bul:</label>
            <input type="date" id="historyDateSearch" onchange="filterHistory()" style="background: rgba(255,255,255,0.05); border: 1px solid #444; color: white; padding: 10px; border-radius: 8px; outline: none; cursor: pointer;">
            <label style="color:#aaa; font-size:0.8rem; margin-top:5px;">Sıralama:</label>
            <select id="historySort" onchange="loadHistoryList()" style="background: rgba(255,255,255,0.05); border: 1px solid #444; color: white; padding: 10px; border-radius: 8px; outline: none; cursor: pointer;">
                <option value="yeni">En Yeni Raporlar (Önce)</option>
                <option value="eski">En Eski Raporlar (Önce)</option>
            </select>
        </div>
        <div id="historyList" style="display: flex; flex-direction: column; gap: 10px; overflow-y: auto; padding-right: 5px; height: 100%;"></div>
    </div>

    <!-- ===== MAIN APP ===== -->
    <div id="mainApp" style="display:none;">

    <!-- ROL SEÇİM EKRANI -->
    <div id="rolSecimEkrani" style="display:none; position:fixed; inset:0; background:var(--bg); z-index:6000; align-items:center; justify-content:center; flex-direction:column;">
      <div style="position:absolute; inset:0; background:radial-gradient(ellipse 80% 60% at 50% 0%, rgba(249,115,22,0.12) 0%, transparent 60%); pointer-events:none;"></div>
      <div style="position:relative; z-index:1; text-align:center; width:90%; max-width:700px;">
        <div style="margin-bottom:48px; animation:fadeInDown 0.6s var(--ease) both;">
          <div style="font-size:3rem; margin-bottom:16px;">🏗️</div>
          <h1 style="font-size:2rem; font-weight:900; letter-spacing:-1.5px; background:linear-gradient(135deg,var(--primary),#fb923c); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; margin-bottom:10px;">BuildingAI Pro'ya Hoş Geldiniz</h1>
          <p style="color:var(--text-secondary); font-size:1rem;">Size en iyi deneyimi sunabilmek için kim olduğunuzu öğrenmek istiyoruz.</p>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:32px;">
          <div class="rol-kart" data-rol="muhendis" onclick="rolSecimYap('muhendis')" style="background:rgba(255,255,255,0.04); border:2px solid rgba(255,255,255,0.08); border-radius:24px; padding:36px 24px; cursor:pointer; transition:all 0.3s var(--ease); animation:fadeInUp 0.6s var(--ease) 0.1s both; text-align:center;"
            onmouseover="this.style.borderColor='rgba(249,115,22,0.4)'; this.style.background='rgba(249,115,22,0.06)'; this.style.transform='translateY(-4px)';"
            onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'; this.style.background='rgba(255,255,255,0.04)'; this.style.transform='translateY(0)';">
            <div style="font-size:3.5rem; margin-bottom:16px;">👷</div>
            <h3 style="color:white; font-size:1.2rem; font-weight:800; margin-bottom:8px;">Saha Mühendisiyim</h3>
            <p style="color:var(--text-muted); font-size:0.85rem; line-height:1.6;">Teknik hesaplamalar, kamera analizi ve mühendislik raporları.</p>
            <div style="margin-top:20px; display:flex; flex-wrap:wrap; gap:6px; justify-content:center;">
              <span style="background:rgba(249,115,22,0.1); color:var(--primary); border:1px solid rgba(249,115,22,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Kamera Analizi</span>
              <span style="background:rgba(249,115,22,0.1); color:var(--primary); border:1px solid rgba(249,115,22,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Hesaplamalar</span>
              <span style="background:rgba(249,115,22,0.1); color:var(--primary); border:1px solid rgba(249,115,22,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Teknik Raporlar</span>
            </div>
          </div>
          <div class="rol-kart" data-rol="muteahhit" onclick="rolSecimYap('muteahhit')" style="background:rgba(255,255,255,0.04); border:2px solid rgba(255,255,255,0.08); border-radius:24px; padding:36px 24px; cursor:pointer; transition:all 0.3s var(--ease); animation:fadeInUp 0.6s var(--ease) 0.2s both; text-align:center;"
            onmouseover="this.style.borderColor='rgba(99,102,241,0.4)'; this.style.background='rgba(99,102,241,0.06)'; this.style.transform='translateY(-4px)';"
            onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'; this.style.background='rgba(255,255,255,0.04)'; this.style.transform='translateY(0)';">
            <div style="font-size:3.5rem; margin-bottom:16px;">🏗️</div>
            <h3 style="color:white; font-size:1.2rem; font-weight:800; margin-bottom:8px;">Müteahhit / Proje Yöneticisiyim</h3>
            <p style="color:var(--text-muted); font-size:0.85rem; line-height:1.6;">Şantiye yönetimi, saha raporları ve proje takibi.</p>
            <div style="margin-top:20px; display:flex; flex-wrap:wrap; gap:6px; justify-content:center;">
              <span style="background:rgba(99,102,241,0.1); color:#818cf8; border:1px solid rgba(99,102,241,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Şantiye Takibi</span>
              <span style="background:rgba(99,102,241,0.1); color:#818cf8; border:1px solid rgba(99,102,241,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Günlük Rapor</span>
              <span style="background:rgba(99,102,241,0.1); color:#818cf8; border:1px solid rgba(99,102,241,0.2); border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700;">Saha Analizi</span>
            </div>
          </div>
        </div>
        <p style="color:var(--text-muted); font-size:0.8rem; animation:fadeIn 0.6s 0.4s both;">Bu seçim daha sonra Profil'den değiştirilebilir.</p>
      </div>
    </div>
        <div class="main-content" id="mainContent">
        <div class="container">

        <div class="input-wrapper">
            <input type="file" id="fileInput" accept="image/*" style="display: none;" onchange="resimSecildi(event)">
            <button id="imgBtn" class="btn-action img-btn" onclick="document.getElementById('fileInput').click()" title="Fotoğraf Yükle">📸</button>
            <button id="micBtn" class="btn-action mic-btn" onclick="sesliDinle()" title="Sesli Soru">🎤</button>
            <input type="text" id="soruInput" placeholder="Soru sor, hesap seç veya fotoğraf yükle...">
            <button class="btn-action send-btn" onclick="soruSor()">🚀</button>
        </div>

        <div id="result">
            <div class="res-title">Sistem Hazır</div>
            <div class="res-detail">Veriler yüklendi. Hesaplama bekleniyor...</div>
        </div>

        <div class="read-controls">
            <button class="btn-read-new btn-read-oku" onclick="sesliOku()">🔊 Sesli Oku</button>
            <button class="btn-stop-new btn-read-dur" onclick="sesliDurdur()">⏹ Durdur</button>
            <button class="btn-save-new" onclick="gunlukRaporuKaydet()">💾 Kaydet</button>
        </div>

        <!-- QUICK ACTIONS -->
        <div class="quick-actions">
            <button class="qa-btn" onclick="kameraAc('guvenlik')">
                <span class="qa-icon">🦺</span>
                <span class="qa-label">Güvenlik</span>
            </button>
            <button class="qa-btn" onclick="kameraAc('ilerleme')">
                <span class="qa-icon">📅</span>
                <span class="qa-label">İlerleme</span>
            </button>
            <button class="qa-btn" onclick="kameraAc('genel')">
                <span class="qa-icon">🔍</span>
                <span class="qa-label">Analiz</span>
            </button>
            <button class="qa-btn" onclick="arsivAc()">
                <span class="qa-icon">📁</span>
                <span class="qa-label">Arşiv</span>
            </button>
            <button class="qa-btn" id="sesliRaporBtn" onclick="sesliRaporBaslat()">
                <span class="qa-icon">🎤</span>
                <span class="qa-label">Sesli Rapor</span>
            </button>
            <button class="qa-btn" onclick="document.getElementById('gunlukRaporModal').style.display='flex'">
                <span class="qa-icon">📝</span>
                <span class="qa-label">Günlük Rapor</span>
            </button>
            <button class="qa-btn" onclick="pdfIndir()">
                <span class="qa-icon">📄</span>
                <span class="qa-label">PDF İndir</span>
            </button>
            <button class="qa-btn" onclick="toggleSidebar()">
                <span class="qa-icon">🛠️</span>
                <span class="qa-label">Araçlar</span>
            </button>
            <button class="qa-btn" onclick="haftalikRaporIndir()">
                <span class="qa-icon">📊</span>
                <span class="qa-label">Haftalık Rapor</span>
            </button>
        </div>
        </div><!-- /container -->
        </div><!-- /main-content -->
    </div><!-- /mainApp -->

    <!-- 📸 KAMERA MODALİ -->
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

    <!-- 📁 ARŞİV MODALİ -->
    <div id="arsivModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
        <div style="background:#1a1d21; border-radius:20px; padding:25px; width:90%; max-width:520px; border:1px solid rgba(139,92,246,0.3); max-height:80vh; overflow-y:auto;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; position:sticky; top:0; background:#1a1d21; padding-bottom:10px;">
                <h3 style="color:#8b5cf6; margin:0;">📁 Arşivim</h3>
                <button onclick="arsivKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
            </div>
            <div id="arsivIcerik"></div>
        </div>
    </div>

    <div id="sidebar" class="sidebar">
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

    <!-- 📝 GÜNLÜK RAPOR MODALİ -->
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
                    <textarea id="grYapilanlar" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:10px; min-height:80px; font-family:Arial; font-size:0.9rem; margin-top:5px; resize:vertical; box-sizing:border-box;" placeholder="Örn: 3. kat döşeme betonu döküldü, iskele kurulumu tamamlandı..."></textarea>
                </div>
                <div>
                    <label style="color:#aaa; font-size:0.85rem;">⚠️ Sorunlar / Riskler</label>
                    <textarea id="grSorunlar" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:10px; min-height:60px; font-family:Arial; font-size:0.9rem; margin-top:5px; resize:vertical; box-sizing:border-box;" placeholder="Örn: Malzeme gecikmesi, rüzgar nedeniyle vinç durdu..."></textarea>
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
                <li>Sınırsız AI sorgusu</li>
                <li>Haftalık 20 kamera analizi</li>
                <li>Günde 5 sesli rapor</li>
                <li>Günde 5 günlük rapor</li>
                <li>50 kayıtlık arşiv erişimi</li>
            </ul>
        </div>

        <p style="color:#aaa; font-size:0.88rem; margin:0 0 10px 0;">Aşağıdaki IBAN'a <b style="color:white;">$10</b> gönderin, açıklamaya e-posta adresinizi yazın:</p>
        <div style="background:#111; border:1px solid #333; border-radius:10px; padding:12px; display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
            <span id="ibanText" style="color:#f1c40f; font-family:monospace; font-size:0.9rem; word-break:break-all;">TR80 0001 0090 1095 7865 2050 01</span>
            <button onclick="ibanKopyala()" style="background:#e67e22; border:none; color:white; border-radius:8px; padding:6px 12px; cursor:pointer; font-size:0.8rem; white-space:nowrap; margin-left:10px;">Kopyala</button>
        </div>
        <p style="color:#777; font-size:0.8rem; margin:0 0 18px 0;">Ad:Mehmet Akif Erdemir</p>

        <button onclick="odemeBildirimi()" style="width:100%; padding:14px; background:linear-gradient(135deg,#27ae60,#2ecc71); border:none; color:white; border-radius:14px; cursor:pointer; font-weight:700; font-size:1rem; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
            ✅ Ödemeyi Yaptım
        </button>
        <div id="odemeMsg" style="margin-top:12px; text-align:center; font-size:0.88rem;"></div>
    </div>
</div>

<!-- 📊 FİYAT TAKİBİ MODALİ -->
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
          <option value="demir">Demir</option>
          <option value="cimento">Çimento</option>
          <option value="beton">Beton</option>
          <option value="tugla">Tuğla</option>
          <option value="kum">Kum</option>
        </select>
        <select id="grafGun" onchange="grafikYukle()" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:8px 12px; border-radius:8px; outline:none; font-size:0.85rem;">
          <option value="90" selected>Son 90 Gün</option>
          <option value="365">Son 365 Gün</option>
        </select>
      </div>
      <canvas id="fiyatGrafik" height="160"></canvas>
      <div id="grafBosMesaj" style="text-align:center; color:#555; font-size:0.85rem; padding:40px 0; display:none;">Henüz yeterli veri yok.</div>
    </div>
    <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px;">
      <div style="color:var(--primary); font-weight:700; font-size:0.85rem; margin-bottom:12px;">➕ Fiyat Gir / Güncelle</div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <select id="fiyatMalzeme" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
          <option value="demir">Demir (ton)</option>
          <option value="cimento">Çimento (çuval)</option>
          <option value="beton">Beton (m³)</option>
          <option value="tugla">Tuğla (adet)</option>
          <option value="kum">Kum (ton)</option>
        </select>
        <input type="number" id="fiyatDeger" placeholder="Fiyat (₺)" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
      </div>
      <select id="fiyatSehir" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none; margin-bottom:10px;">
        <option value="genel">Genel (Türkiye Ortalaması)</option>
        <option value="Istanbul">İstanbul</option>
        <option value="Ankara">Ankara</option>
        <option value="Izmir">İzmir</option>
        <option value="Sivas">Sivas</option>
        <option value="Bursa">Bursa</option>
      </select>
      <button onclick="fiyatKaydet()" style="width:100%; padding:12px; background:var(--primary); color:white; border:none; border-radius:10px; cursor:pointer; font-weight:700;">💾 Fiyatı Kaydet</button>
      <div id="fiyatMsg" style="margin-top:8px; font-size:0.85rem; text-align:center;"></div>
    </div>
  </div>
</div>

<!-- 📦 STOK TAKİBİ MODALİ -->
<div id="stokModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
  <div style="background:#1a1d21; border:1px solid rgba(249,115,22,0.3); border-radius:24px; padding:28px; width:92%; max-width:680px; max-height:90vh; overflow-y:auto;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <h3 style="color:var(--primary); margin:0; font-size:1.2rem;">📦 Malzeme Stok Takibi</h3>
      <button onclick="stokModalKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
    </div>

    <!-- Uyarılar -->
    <div id="stokUyarilar" style="margin-bottom:16px;"></div>

    <!-- Stok Kartları -->
    <div id="stokKartlar" style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:20px;"></div>

    <!-- Geçmiş -->
    <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; margin-bottom:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="color:var(--primary); font-weight:700; font-size:0.85rem;">📋 Hareket Geçmişi</div>
        <select id="stokGecmisMalzeme" onchange="stokGecmisYukle()" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:6px 10px; border-radius:8px; outline:none; font-size:0.8rem;">
          <option value="demir">Demir</option>
          <option value="cimento">Çimento</option>
          <option value="beton">Beton</option>
          <option value="tugla">Tuğla</option>
          <option value="kum">Kum</option>
        </select>
      </div>
      <div id="stokGecmisListe" style="max-height:200px; overflow-y:auto;"></div>
    </div>

    <!-- Malzeme Ekle -->
    <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px;">
      <div style="color:var(--primary); font-weight:700; font-size:0.85rem; margin-bottom:12px;">➕ Malzeme Girişi / Çıkışı</div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <select id="stokMalzeme" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
          <option value="demir">Demir</option>
          <option value="cimento">Çimento</option>
          <option value="beton">Beton</option>
          <option value="tugla">Tuğla</option>
          <option value="kum">Kum</option>
        </select>
        <select id="stokTip" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
          <option value="giris">📥 Giriş (Geldi)</option>
          <option value="cikis">📤 Çıkış (Kullanıldı)</option>
        </select>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
        <input type="number" id="stokMiktar" placeholder="Miktar" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
        <select id="stokBirim" style="background:rgba(255,255,255,0.05); border:1px solid #444; color:white; padding:10px; border-radius:8px; outline:none;">
          <option value="ton">Ton</option>
          <option value="m³">m³</option>
          <option value="adet">Adet</option>
          <option value="çuval">Çuval</option>
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

<!-- 🌍 DEPREM ANALİZİ MODALİ -->
<div id="depremModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:9999; align-items:center; justify-content:center;">
  <div style="background:#1a1d21; border:1px solid rgba(249,115,22,0.3); border-radius:24px; padding:28px; width:95%; max-width:900px; max-height:92vh; overflow-y:auto;">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
      <h3 style="color:var(--primary); margin:0; font-size:1.2rem;">🌍 Deprem & Jeolojik Risk Analizi</h3>
      <button onclick="depremModalKapat()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">×</button>
    </div>

    <!-- Konum Girişi -->
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

    <!-- Harita -->
    <div style="border-radius:14px; overflow:hidden; margin-bottom:16px; border:1px solid rgba(255,255,255,0.08);">
      <div id="depremHarita" style="height:320px; width:100%;"></div>
    </div>

    <!-- Analiz Sonucu -->
    <div id="depremAnalizSonuc" style="display:none;">

      <!-- Risk Skoru -->
      <div style="display:grid; grid-template-columns:auto 1fr; gap:16px; background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; margin-bottom:16px; align-items:center;">
        <div style="position:relative; width:90px; height:90px;">
          <svg width="90" height="90" style="transform:rotate(-90deg)">
            <circle cx="45" cy="45" r="36" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="8"/>
            <circle id="riskCircle" cx="45" cy="45" r="36" fill="none" stroke="#ef4444" stroke-width="8"
              stroke-dasharray="226" stroke-dashoffset="226" stroke-linecap="round"
              style="transition:stroke-dashoffset 1.5s ease;"/>
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

      <!-- Fay Hattı + TBDY -->
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

      <!-- Son Depremler Listesi -->
      <div style="background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; margin-bottom:16px;">
        <div style="color:var(--primary); font-weight:700; font-size:0.85rem; margin-bottom:12px;">📋 AFAD Son Depremler (200km çevre)</div>
        <div id="sonDepremlerListe" style="max-height:180px; overflow-y:auto;"></div>
      </div>

      <!-- Öneriler -->
      <div style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); border-radius:14px; padding:16px;">
        <div style="color:#fcd34d; font-weight:700; font-size:0.85rem; margin-bottom:10px;">💡 MÜHENDİSLİK ÖNERİLERİ</div>
        <div id="depremOneriler"></div>
      </div>

    </div>

    <!-- Loading -->
    <div id="depremLoading" style="display:none; text-align:center; padding:40px;">
      <div style="font-size:2rem; margin-bottom:12px;">🔍</div>
      <div style="color:#aaa;">AFAD verileri çekiliyor, AI analiz yapıyor...</div>
    </div>

  </div>
</div>

<!-- ===== ŞANTİYE DASHBOARD MODAL ===== -->
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
      <!-- Özet Kartlar -->
      <div id="santiyeOzet" style="display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:24px;"></div>
      <!-- Harita + Tablo -->
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
      <!-- Şantiye Kartları -->
      <div style="color:#aaa; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;">🗂️ Şantiyeler</div>
      <div id="santiyeKartlar" style="display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px;"></div>
    </div>
  </div>
</div>

<!-- ===== ŞANTİYE FORM MODAL ===== -->
<div id="santiyeFormModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.9); z-index:9100; display:flex; align-items:center; justify-content:center; padding:20px;">
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
            <option value="iyi">✅ İyi</option>
            <option value="dikkat">⚠️ Dikkat</option>
            <option value="sorun">❌ Sorun</option>
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

<!-- 🔒 PLAN KİLİT MODALI (JS tarafından doldurulur) -->
<div id="planKilitModal" style="display:none;"></div>

<!-- 💳 ÖDEME MODALI (JS tarafından doldurulur) -->
<div id="odemeModal" style="display:none;"></div>

{JS_SCRIPT}
</body>
</html>
"""
