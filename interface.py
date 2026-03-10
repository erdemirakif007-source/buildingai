from styles import CSS_STYLE
from scripts import JS_SCRIPT

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <title>BuildingAI Pro</title>
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
            <button onclick="closeProfile(); proYukselt();" style="width:100%; padding:14px; background:linear-gradient(135deg,#e67e22,#f39c12); border:none; color:white; border-radius:14px; cursor:pointer; font-weight:700; font-size:1rem; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
                ⚡ Pro'ya Geç - $10/ay
            </button>

            <hr class="divider">
            <button onclick="cikisYap()" style="width:100%; padding:14px; background:rgba(231,76,60,0.15); border:1px solid #e74c3c; color:#e74c3c; border-radius:14px; cursor:pointer; font-weight:700; transition:0.3s;" onmouseover="this.style.background='rgba(231,76,60,0.3)'" onmouseout="this.style.background='rgba(231,76,60,0.15)'">
                🚪 Çıkış Yap
            </button>
        </div>
    </div>

    <div id="sidebarOverlay" class="sidebar-overlay" onclick="toggleSidebar()"></div>

    <div onclick="toggleHistory()" style="position: fixed; top: 30px; right: 100px; width: 55px; height: 55px; background: #161625; border: 2px solid #2ecc71; border-radius: 50%; cursor: pointer; z-index: 1000; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(46,204,113,0.2); transition: 0.3s;" onmouseover="this.style.transform='scale(1.1)';" onmouseout="this.style.transform='scale(1)';" title="Şantiye Arşivi">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#2ecc71" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 26px; height: 26px;">
            <path d="M12 8v4l3 3"></path>
            <path d="M2.05 13a10 10 0 1 0 2.18-7.18L1 9h6"></path>
        </svg>
    </div>

    <!-- Profil butonu -->
    <div onclick="openProfile()" style="position: fixed; top: 30px; right: 30px; width: 55px; height: 55px; background: #161625; border: 2px solid var(--primary); border-radius: 50%; cursor: pointer; z-index: 1000; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(230,126,34,0.2); transition: 0.3s; font-size: 1.4rem;" onmouseover="this.style.transform='scale(1.1)';" onmouseout="this.style.transform='scale(1)';" title="Profilim">
        👤
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

    <div class="container" id="mainApp" style="display:none;">
        <div class="header-grid">
            <h1>🏗️ BuildingAI</h1>
            <div class="weather-widget">
                <select id="citySelect" class="city-dropdown" onchange="havaGuncelle()">
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
                <span class="temp" id="temp">--°C</span>
                <span class="condition" id="condition">Yükleniyor...</span>
            </div>
        </div>

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

        <div style="display: flex; gap: 10px; margin-top: 15px;">
            <button class="btn-read btn-read-oku" onclick="sesliOku()">🔊 OKU</button>
            <button class="btn-read stop-btn btn-read-dur" onclick="sesliDurdur()">🛑 DURDUR</button>
        </div>

        <!-- 📸 KAMERA BUTONLARI -->
        <div style="display:flex; gap:8px; margin-top:12px; flex-wrap:wrap;">
            <button onclick="kameraAc('guvenlik')" style="flex:1; background:linear-gradient(135deg,#e74c3c,#c0392b); color:white; border:none; padding:10px 12px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:0.85rem;">🦺 Güvenlik Analizi</button>
            <button onclick="kameraAc('ilerleme')" style="flex:1; background:linear-gradient(135deg,#2980b9,#1a6fa8); color:white; border:none; padding:10px 12px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:0.85rem;">📅 İlerleme Takibi</button>
            <button onclick="kameraAc('genel')" style="flex:1; background:linear-gradient(135deg,#27ae60,#1e8449); color:white; border:none; padding:10px 12px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:0.85rem;">🔍 Genel Analiz</button>
            <button onclick="arsivAc()" style="flex:1; background:linear-gradient(135deg,#8e44ad,#6c3483); color:white; border:none; padding:10px 12px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:0.85rem;">📁 Arşivim</button>
            <button id="sesliRaporBtn" onclick="sesliRaporBaslat()" style="flex:1; background:linear-gradient(135deg,#8e44ad,#6c3483); color:white; border:none; padding:10px 12px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:0.85rem;">🎤 Sesli Rapor</button>
            <button onclick="document.getElementById('gunlukRaporModal').style.display='flex'" style="flex:1; background:linear-gradient(135deg,#f39c12,#e67e22); color:white; border:none; padding:10px 12px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:0.85rem;">📝 Günlük Rapor</button>
        </div>

        <div class="tool-fab" onclick="toggleSidebar()" title="Mühendislik Araçları">🛠️</div>
    </div>

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

{JS_SCRIPT}
</body>
</html>
"""
