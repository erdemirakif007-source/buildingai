JS_SCRIPT = r"""
<script>
// --- 🌍 DİL SİSTEMİ ---
const TRANSLATIONS = {
    tr: {
        loginTitle: "🏗️ BuildingAI Pro",
        loginBtn: "Şantiyeye Giriş Yap",
        registerBtn: "Hesabı Oluştur",
        forgotBtn: "Sıfırlama Maili Gönder",
        loginTab: "Giriş Yap",
        registerTab: "Kayıt Ol",
        forgotTitle: "🔑 Şifre Sıfırlama",
        forgotDesc: "E-posta adresinize sıfırlama bağlantısı göndereceğiz.",
        emailPlaceholder: "E-posta adresi",
        passPlaceholder: "Şifre",
        namePlaceholder: "Ad Soyad",
        companyPlaceholder: "Şirket / Proje Adı (opsiyonel)",
        passConfirmPlaceholder: "Şifreyi tekrarla",
        forgotLink: "Şifremi unuttum",
        backLink: "← Giriş sayfasına dön",
        planLabel: "Plan seçin:",
        inputPlaceholder: "Soru sor, hesap seç veya fotoğraf yükle...",
        systemReady: "Sistem Hazır",
        systemReadyDesc: "Veriler yüklendi. Hesaplama bekleniyor...",
        aiAnaliz: "🧠 AI ANALİZİ",
        translateBtn: "🇬🇧 Translate to English Technical Report",
        saveBtn: "💾 Günlük Rapor Olarak Kaydet",
        readBtn: "🔊 OKU",
        stopBtn: "🛑 DURDUR",
        thinking: "Şefim, yapay zeka analiz ediyor...",
        aiLang: "tr",
    },
    en: {
        loginTitle: "🏗️ BuildingAI Pro",
        loginBtn: "Enter Site",
        registerBtn: "Create Account",
        forgotBtn: "Send Reset Email",
        loginTab: "Login",
        registerTab: "Register",
        forgotTitle: "🔑 Password Reset",
        forgotDesc: "We will send a reset link to your email address.",
        emailPlaceholder: "Email address",
        passPlaceholder: "Password",
        namePlaceholder: "Full Name",
        companyPlaceholder: "Company / Project Name (optional)",
        passConfirmPlaceholder: "Confirm password",
        forgotLink: "Forgot my password",
        backLink: "← Back to login",
        planLabel: "Choose a plan:",
        inputPlaceholder: "Ask a question, select a calculation or upload a photo...",
        systemReady: "System Ready",
        systemReadyDesc: "Data loaded. Awaiting calculation...",
        aiAnaliz: "🧠 AI ANALYSIS",
        translateBtn: "🇹🇷 Türkçe Rapora Çevir",
        saveBtn: "💾 Save as Daily Report",
        readBtn: "🔊 READ",
        stopBtn: "🛑 STOP",
        thinking: "Analyzing with AI...",
        aiLang: "en",
    }
};

let aktifDil = 'tr';

let aktifRol = localStorage.getItem('bai_rol') || null;
function rolKaydet(rol) { aktifRol = rol; localStorage.setItem('bai_rol', rol); }
function rolSifirla() { aktifRol = null; localStorage.removeItem('bai_rol'); rolEkraniniGoster(); }
function rolEkraniniGoster() {
    const el = document.getElementById('rolSecimEkrani');
    el.style.display = 'flex'; el.style.opacity = '0';
    setTimeout(() => { el.style.transition = 'opacity 0.5s ease'; el.style.opacity = '1'; }, 50);
}
function rolSecimYap(rol) {
    document.querySelectorAll('.rol-kart').forEach(k => {
        if (k.dataset.rol !== rol) { k.style.opacity = '0'; k.style.transform = 'scale(0.8)'; }
    });
    const s = document.querySelector('.rol-kart[data-rol="'+rol+'"]');
    s.style.transform = 'scale(1.05)'; s.style.borderColor = 'var(--primary)';
    setTimeout(() => {
        rolKaydet(rol);
        const el = document.getElementById('rolSecimEkrani');
        el.style.opacity = '0';
        setTimeout(() => { el.style.display = 'none'; navSidebarGuncelle(rol); }, 400);
    }, 600);
}
function raporlarMenuToggle() {
    const menu = document.getElementById('raporlarSubMenu');
    const arrow = document.getElementById('raporlarArrow');
    if (!menu) return;
    const isOpen = menu.style.maxHeight && menu.style.maxHeight !== '0px';
    if (isOpen) {
        menu.style.maxHeight = '0px';
        if (arrow) arrow.style.transform = 'rotate(0deg)';
    } else {
        menu.style.maxHeight = '300px';
        if (arrow) arrow.style.transform = 'rotate(180deg)';
    }
}

function toggleAnalizMenu() {
    const menu = document.getElementById('analizSubMenu');
    const btn  = document.getElementById('analizToggleBtn');
    if (!menu) return;
    const raporlarMenu = document.getElementById('raporlarSubMenu2');
    if (raporlarMenu) raporlarMenu.classList.remove('open');
    const open = menu.classList.toggle('open');
    if (btn) btn.style.background = open ? 'var(--primary-light)' : '';
}
function toggleRaporlarMenu() {
    const menu = document.getElementById('raporlarSubMenu2');
    const btn = document.getElementById('raporlarToggleBtn');
    const analizMenu = document.getElementById('analizSubMenu');
    if (analizMenu) analizMenu.classList.remove('open');
    if (menu) menu.classList.toggle('open');
}

function navSidebarGuncelle(rol) {
    const nav = document.getElementById('navLinks');
    if (!nav) return;
    const plan = window._kullaniciPlan || 'free';
    const oz   = window._planOzellikler || {};
    const stokKilit   = !oz.stok;
    const depremKilit = !oz.deprem_analiz;
    const fiyatKilit  = !oz.fiyat_takip;
    const santiyeKilit = (oz.santiye_max === 0);

    const stokOnclick   = stokKilit   ? `planKilit('stok')`          : `navGit('stok')`;
    const depremOnclick = depremKilit ? `planKilit('deprem_analiz')` : `navGit('deprem')`;
    const fiyatOnclick  = fiyatKilit  ? `planKilit('fiyat_takip')`  : `navGit('fiyat')`;
    const stokLock      = stokKilit   ? ' style="opacity:0.5"' : '';
    const depremLock    = depremKilit ? ' style="opacity:0.5"' : '';
    const fiyatLock     = fiyatKilit  ? ' style="opacity:0.5"' : '';

    if (rol === 'muhendis') {
        nav.innerHTML = `
            <div class="nav-item active" id="nav-home" onclick="navGit('home')"><span class="nav-icon">🏠</span><span class="nav-label">Ana Sayfa</span></div>
            <div class="nav-item" id="nav-kamera" onclick="navGit('kamera')"><span class="nav-icon">📷</span><span class="nav-label">Kamera Analizi</span></div>
            <div class="nav-item" id="nav-hesaplama" onclick="navGit('hesaplama')"><span class="nav-icon">🧮</span><span class="nav-label">Mühendislik Paneli</span></div>
            <div class="nav-item" id="nav-gunluk" onclick="navGit('gunluk')"><span class="nav-icon">📝</span><span class="nav-label">Günlük Rapor</span></div>
            <div class="nav-item" id="nav-sesli" onclick="navGit('sesli')"><span class="nav-icon">🎤</span><span class="nav-label">Sesli Rapor</span></div>
            <div class="nav-item" id="nav-arsiv" onclick="navGit('arsiv')"><span class="nav-icon">📁</span><span class="nav-label">Arşiv</span></div>
            <div class="nav-item" id="nav-fiyat" onclick="${fiyatOnclick}"${fiyatLock}><span class="nav-icon">📊</span><span class="nav-label">Fiyat Takibi${fiyatKilit?' 🔒':''}</span></div>
            <div class="nav-item" id="nav-stok" onclick="${stokOnclick}"${stokLock}><span class="nav-icon">📦</span><span class="nav-label">Stok Takibi${stokKilit?' 🔒':''}</span></div>
            <div class="nav-item" id="nav-deprem" onclick="${depremOnclick}"${depremLock}><span class="nav-icon">🌍</span><span class="nav-label">Deprem Analizi${depremKilit?' 🔒':''}</span></div>
            <div class="nav-item" id="nav-pdf" onclick="pdfIndir()"><span class="nav-icon">📄</span><span class="nav-label">PDF İndir</span></div>
            <div class="nav-item" id="nav-haftalik" onclick="haftalikRaporIndir()"><span class="nav-icon">📊</span><span class="nav-label">Haftalık Rapor</span></div>`;
    } else {
        const santiyeOnclick = santiyeKilit ? `planKilit('santiye')` : `navGit('santiye')`;
        const santiyeLock    = santiyeKilit ? ' style="opacity:0.5"' : '';
        nav.innerHTML = `
            <div class="nav-item active" id="nav-home" onclick="navGit('home')"><span class="nav-icon">🏗️</span><span class="nav-label">Şantiye Dashboard</span></div>
            <div class="nav-item" id="nav-kamera" onclick="navGit('kamera')"><span class="nav-icon">📷</span><span class="nav-label">Saha Analizi</span></div>
            <div class="nav-item" id="nav-gunluk" onclick="navGit('gunluk')"><span class="nav-icon">📝</span><span class="nav-label">Günlük Rapor</span></div>
            <div class="nav-item" id="nav-sesli" onclick="navGit('sesli')"><span class="nav-icon">🎤</span><span class="nav-label">Sesli Rapor</span></div>
            <div class="nav-item" id="nav-arsiv" onclick="navGit('arsiv')"><span class="nav-icon">📁</span><span class="nav-label">Arşiv</span></div>
            <div class="nav-item" id="nav-hesaplama" onclick="navGit('hesaplama')"><span class="nav-icon">🧮</span><span class="nav-label">Hesaplamalar</span></div>
            <div class="nav-item" id="nav-fiyat" onclick="${fiyatOnclick}"${fiyatLock}><span class="nav-icon">📊</span><span class="nav-label">Fiyat Takibi${fiyatKilit?' 🔒':''}</span></div>
            <div class="nav-item" id="nav-stok" onclick="${stokOnclick}"${stokLock}><span class="nav-icon">📦</span><span class="nav-label">Stok Takibi${stokKilit?' 🔒':''}</span></div>
            <div class="nav-item" id="nav-deprem" onclick="${depremOnclick}"${depremLock}><span class="nav-icon">🌍</span><span class="nav-label">Deprem Analizi${depremKilit?' 🔒':''}</span></div>
            <div class="nav-item" id="nav-santiye" onclick="${santiyeOnclick}"${santiyeLock}><span class="nav-icon">🏗️</span><span class="nav-label">Şantiye Yönetimi${santiyeKilit?' 🔒':''}</span></div>
            <div class="nav-item" id="nav-pdf" onclick="pdfIndir()"><span class="nav-icon">📄</span><span class="nav-label">PDF İndir</span></div>
            <div class="nav-item" id="nav-haftalik" onclick="haftalikRaporIndir()"><span class="nav-icon">📊</span><span class="nav-label">Haftalık Rapor</span></div>`;
    }
    document.getElementById('result').innerHTML = rol === 'muhendis'
        ? '<div class="res-title">👷 Mühendis Paneli Hazır</div><div class="res-detail">Kamera analizi, hesaplamalar ve raporlama araçlarına hazırsınız.</div>'
        : '<div class="res-title">🏗️ Müteahhit Paneli Hazır</div><div class="res-detail">Saha yönetimi, rapor sistemi ve analizlere hazırsınız.</div>';
}

function dilDegistir(dil) {
    aktifDil = dil;
    const t = TRANSLATIONS[dil];

    // Bayrak butonları
    document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active-lang'));
    const aktifBtn = document.getElementById('langBtn_' + dil);
    if (aktifBtn) aktifBtn.classList.add('active-lang');

    // Auth ekranı
    const setVal = (id, val) => { const el = document.getElementById(id); if(el) el.placeholder = val; };
    const setTxt = (id, val) => { const el = document.getElementById(id); if(el) el.innerText = val; };
    const setInnerHTML = (id, val) => { const el = document.getElementById(id); if(el) el.innerHTML = val; };

    setTxt('loginTitleEl', t.loginTitle);
    setVal('loginEmail', t.emailPlaceholder);
    setVal('loginPass', t.passPlaceholder);
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) loginBtn.innerText = t.loginBtn;

    setVal('regName', t.namePlaceholder);
    setVal('regCompany', t.companyPlaceholder);
    setVal('regEmail', t.emailPlaceholder);
    setVal('regPass', t.passPlaceholder);
    setVal('regPassConfirm', t.passConfirmPlaceholder);
    const regBtn = document.getElementById('regBtn');
    if (regBtn) regBtn.innerText = t.registerBtn;

    setVal('forgotEmail', t.emailPlaceholder);
    const forgotBtn = document.getElementById('forgotBtn');
    if (forgotBtn) forgotBtn.innerText = t.forgotBtn;

    // Tab butonları
    document.querySelectorAll('.tab-login').forEach(el => el.innerText = t.loginTab);
    document.querySelectorAll('.tab-register').forEach(el => el.innerText = t.registerTab);

    // Ana uygulama
    setVal('soruInput', t.inputPlaceholder);

    // Sistem hazır metni (henüz soru sorulmamışsa)
    const resBox = document.getElementById('result');
    if (resBox && resBox.querySelector('.res-title') && resBox.querySelector('.res-title').innerText.includes('Sistem') || resBox && resBox.querySelector('.res-title') && resBox.querySelector('.res-title').innerText.includes('System')) {
        resBox.innerHTML = `<div class="res-title">${t.systemReady}</div><div class="res-detail">${t.systemReadyDesc}</div>`;
    }

    // OKU / DURDUR butonları
    document.querySelectorAll('.btn-read-oku').forEach(el => el.innerText = t.readBtn);
    document.querySelectorAll('.btn-read-dur').forEach(el => el.innerText = t.stopBtn);
}

// --- 🔐 GİRİŞ SİSTEMİ ---
async function girisYap() {
    const email = document.getElementById('loginEmail').value;
    const pass = document.getElementById('loginPass').value;
    const btn = document.querySelector('.auth-btn');

    if (!email || !pass) {
        alert("Şefim, bilgileri eksik girmeyelim.");
        return;
    }

    btn.innerText = "⏳ Kontrol Ediliyor...";

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: pass })
        });

        const data = await response.json();

        if (response.ok) {
            aktifKullanici = { ...data, email: email };
            // 🔐 Token'ı 7 gün sakla
            localStorage.setItem('bai_token', data.token);
            localStorage.setItem('bai_token_expiry', Date.now() + 7 * 24 * 60 * 60 * 1000);
            localStorage.setItem('bai_user', JSON.stringify({
                full_name: data.full_name,
                email: email,
                plan: data.plan
            }));
            document.getElementById('auth-overlay').style.display = 'none';
            document.getElementById('mainApp').style.display = 'block';
            document.getElementById('navSidebar').style.display = 'flex';
            document.getElementById('topHeader').style.display = 'flex';
            dilDegistir(aktifDil);
            havaGuncelle();
            kullanımDurumuGoster();
            const kayitliRolGiris = localStorage.getItem('bai_rol');
            if (kayitliRolGiris) navSidebarGuncelle(kayitliRolGiris);
            else setTimeout(() => rolEkraniniGoster(), 300);
        } else {
            alert("Hata: " + (data.detail || "Bilgiler yanlış."));
            btn.innerText = "Şantiyeye Giriş Yap";
        }
    } catch (e) {
        alert("Sunucuya bağlanılamadı. app.py çalışıyor mu?");
        btn.innerText = "Şantiyeye Giriş Yap";
    }
}

// --- 🌤️ HAVA DURUMU ---
async function havaGuncelle() {
    if (window.innerWidth <= 768) return;
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : "Sivas";
    const tempEl = document.getElementById('temp');
    const condEl = document.getElementById('condition');
    const widget = document.getElementById('weatherWidget');
    try {
        const res = await fetch(`/hava?sehir=${sehir}`);
        const data = await res.json();
        if (tempEl) tempEl.innerText = data.temp;
        if (condEl) condEl.innerText = data.cond;
        if (widget) widget.textContent = `⛅ ${data.cond} ${data.temp}°`;
    } catch (e) {
        if (condEl) condEl.innerText = "Bağlantı Yok";
        if (widget) widget.textContent = "⛅ --";
    }
}

// --- 🌑 SIDEBAR KONTROLLERİ ---
function toggleSidebar() {
    const side = document.getElementById('sidebarPanel');
    const overlay = document.getElementById('sidebarOverlay');
    const isActive = side.classList.toggle('active');
    if (isActive) overlay.classList.add('active');
    else overlay.classList.remove('active');
}

// --- 🗂️ ARŞİV KONTROLLERİ ---
let butunRaporlar = [];

function toggleHistory() {
    const sidebar = document.getElementById('historySidebar');
    if (sidebar.style.left === '0px') {
        sidebar.style.left = '-350px';
    } else {
        sidebar.style.left = '0px';
        loadHistoryList();
    }
}

async function loadHistoryList() {
    const listDiv = document.getElementById('historyList');
    const sortType = document.getElementById('historySort').value;
    listDiv.innerHTML = "<i style='color:#888;'>Kayıtlar aranıyor...</i>";

    try {
        const response = await fetch('/rapor_listesi');
        const data = await response.json();
        butunRaporlar = data.raporlar;
        renderHistoryList(butunRaporlar, sortType);
    } catch (e) {
        listDiv.innerHTML = "<span style='color:red;'>Bağlantı hatası!</span>";
    }
}

function renderHistoryList(liste, sortType) {
    const listDiv = document.getElementById('historyList');
    listDiv.innerHTML = "";

    if (sortType === 'yeni') {
        liste.sort((a, b) => new Date(b) - new Date(a));
    } else {
        liste.sort((a, b) => new Date(a) - new Date(b));
    }

    if (liste.length === 0) {
        listDiv.innerHTML = "<i style='color:#888;'>Henüz kaydedilmiş rapor yok.</i>";
        return;
    }

    liste.forEach(tarih => {
        listDiv.innerHTML += `
            <button onclick="eskiRaporuGetir('${tarih}')"
            onmouseover="this.style.background='rgba(46,204,113,0.1)'; this.style.borderColor='#2ecc71';"
            onmouseout="this.style.background='rgba(255,255,255,0.03)'; this.style.borderColor='#333';"
            style="background:rgba(255,255,255,0.03); border:1px solid #333; color:#ccc; padding:15px; border-radius:10px; cursor:pointer; text-align:left; transition:0.2s; font-size:1rem; width:100%; margin-bottom:10px;">
                📅 ${tarih} Şantiye Raporu
            </button>
        `;
    });
}

function filterHistory() {
    const secilenTarih = document.getElementById('historyDateSearch').value;
    const sortType = document.getElementById('historySort').value;
    if (!secilenTarih) {
        renderHistoryList(butunRaporlar, sortType);
        return;
    }
    const filtrelenmis = butunRaporlar.filter(t => t.includes(secilenTarih));
    renderHistoryList(filtrelenmis, sortType);
}

async function eskiRaporuGetir(secilenTarih) {
    const resBox = document.getElementById('result');
    toggleHistory();
    resBox.innerHTML = `<i>⏳ ${secilenTarih} tarihli rapor getiriliyor...</i>`;
    try {
        const response = await fetch('/rapor_getir?tarih=' + secilenTarih);
        const data = await response.json();
        resBox.innerHTML = `
            <div class="res-title" style="color:#f1c40f;">🗂️ ŞANTİYE GÜNLÜĞÜ: ${secilenTarih}</div>
            <div class="res-detail" style="color:#fff; font-size:1.1rem; border-top:none; white-space:pre-wrap; line-height:1.6;">${data.icerik}</div>
        `;
    } catch (e) {
        resBox.innerHTML = `<div class="res-title" style="color:#e74c3c;">⚠️ ARŞİV BAĞLANTI HATASI</div>`;
    }
}

// --- 💾 RAPOR KAYDETME ---
async function gunlukRaporuKaydet() {
    const turkceMetni = document.getElementById('analizMetni') ? document.getElementById('analizMetni').innerText : "";
    const ingilizceMetni = document.getElementById('englishMetni') ? document.getElementById('englishMetni').innerText : "";
    const resBox = document.getElementById('result');

    if (!turkceMetni) {
        alert("Şefim, kaydedecek bir analiz yok! Önce bir soru sorun.");
        return;
    }

    const tamRapor = `TURKISH ANALYSIS:\n${turkceMetni}\n\nENGLISH REPORT:\n${ingilizceMetni}`;
    const token = localStorage.getItem('bai_token') || '';

    try {
        const response = await fetch('/rapor_kaydet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rapor_metni: tamRapor, token: token })
        });
        const data = await response.json();
        resBox.innerHTML += `<div style="margin-top:15px; padding:10px; background:rgba(46,204,113,0.2); color:#2ecc71; border-radius:10px; text-align:center; font-weight:bold;">✅ ${data.mesaj}</div>`;
    } catch (e) {
        alert("Rapor kaydedilemedi!");
    }
}

// --- 📂 DRAG & DROP — Şantiyeye Özel RAG Dosya Yükleme ---
let ragSecilenDosyalar = [];

function ragDragOver(e) {
    e.preventDefault();
    const zone = document.getElementById('ragDropZone');
    if (!zone) return;
    zone.style.borderColor = 'rgba(249,115,22,0.80)';
    zone.style.background  = 'rgba(249,115,22,0.10)';
    zone.style.transform   = 'scale(1.01)';
}

function ragDragLeave(e) {
    const zone = document.getElementById('ragDropZone');
    if (!zone) return;
    zone.style.borderColor = 'rgba(249,115,22,0.40)';
    zone.style.background  = 'rgba(249,115,22,0.04)';
    zone.style.transform   = 'scale(1)';
}

function ragDrop(e) {
    e.preventDefault();
    ragDragLeave(e);
    const files = Array.from(e.dataTransfer.files);
    ragDosyalariIsle(files);
}

function ragDosyaSecildi(input) {
    const files = Array.from(input.files);
    ragDosyalariIsle(files);
}

function ragDosyalariIsle(files) {
    const izinli = ['.pdf', '.xlsx', '.xls', '.doc', '.docx'];
    const gecerli = files.filter(f => izinli.some(ext => f.name.toLowerCase().endsWith(ext)));
    if (!gecerli.length) {
        showToast('Sadece PDF, Excel veya Word dosyası yükleyebilirsiniz.', 'error');
        return;
    }
    ragSecilenDosyalar = gecerli;
    const label = document.getElementById('ragDropLabel');
    if (label) {
        label.style.display = 'block';
        label.textContent = gecerli.map(f => `📄 ${f.name}`).join('  ·  ');
    }
    const zone = document.getElementById('ragDropZone');
    if (zone) {
        zone.style.borderColor = 'rgba(249,115,22,0.70)';
        zone.style.background  = 'rgba(249,115,22,0.08)';
    }
}

// --- 📸 RESİM İŞLEME ---
let secilenResimBase64 = null;

function resimSecildi(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        secilenResimBase64 = e.target.result;
        const imgBtn = document.getElementById('imgBtn');
        if (imgBtn) imgBtn.classList.add('active-img');
        document.getElementById('soruInput').placeholder = "📸 Görsel hafızada! Sorunuzu yazın...";
    };
    reader.readAsDataURL(file);
}

// --- 🧠 CHAT HUB — /api/chat bağlantısı ---
const chatSessionId = 'bai_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6);
let chatBaslatildi = false;

function sorularGonder() {
    const input = document.getElementById('userInput');
    const soru = input ? input.value.trim() : '';
    if (!soru) return;
    input.value = '';
    chatMesajEkle('user', soru);
    chatAIYanit(soru);
}

function chatPanelHazirla() {
    if (chatBaslatildi) return;
    const resBox = document.getElementById('result');
    if (!resBox) return;
    resBox.innerHTML = `
        <div class="chat-header">
            <div class="result-live-dot"></div>
            <span class="chat-header-title">🏗️ Şantiye AI</span>
            <span class="result-live-tag">LIVE</span>
            <span class="chat-kaynak" id="chatKaynak">Live+Genel</span>
        </div>
        <div class="chat-history" id="chatHistory"></div>`;
    chatBaslatildi = true;
}

function chatMesajEkle(rol, icerik, meta) {
    chatPanelHazirla();
    const history = document.getElementById('chatHistory');
    if (!history) return;
    const zaman = new Date().toLocaleTimeString('tr-TR', {hour:'2-digit', minute:'2-digit'});
    const div = document.createElement('div');

    if (rol === 'user') {
        div.className = 'chat-msg chat-msg--user';
        div.innerHTML = `<div class="chat-bubble chat-bubble--user"><span class="chat-text">${icerik}</span><span class="chat-time">${zaman}</span></div>`;
    } else if (rol === 'thinking') {
        div.className = 'chat-msg chat-msg--ai';
        div.id = 'chatThinking';
        div.innerHTML = `<div class="chat-avatar">🏗️</div><div class="chat-bubble chat-bubble--ai chat-bubble--thinking"><span class="chat-dots"><span></span><span></span><span></span></span><span style="font-size:11px;color:var(--text-3);margin-left:8px;">Analiz ediyor...</span></div>`;
    } else {
        div.className = 'chat-msg chat-msg--ai';
        let metaHtml = '';
        if (meta && meta.kritik_uyari && meta.kritik_uyari.length > 0) {
            metaHtml = `<div class="chat-uyari">${meta.kritik_uyari.map(u => `<span>${u}</span>`).join('')}</div>`;
        }
        div.innerHTML = `<div class="chat-avatar">🏗️</div><div class="chat-bubble chat-bubble--ai"><div class="chat-text">${markdownToHtml(icerik)}</div>${metaHtml}<span class="chat-time">${zaman}</span></div>`;
    }

    history.appendChild(div);
    history.scrollTop = history.scrollHeight;
}

async function chatAIYanit(soru) {
    chatMesajEkle('thinking', '');
    const token = localStorage.getItem('bai_token') || '';
    try {
        const resp = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({soru, session_id: chatSessionId, token})
        });
        const data = await resp.json();
        const thinking = document.getElementById('chatThinking');
        if (thinking) thinking.remove();

        if (resp.status === 429) {
            chatMesajEkle('ai', '⚡ **Limit doldu!** Pro plana geçerek sınırsız kullanın.');
            return;
        }
        chatMesajEkle('ai', data.cevap, data.canli_durum);

        // Kaynak badge güncelle
        const kaynak = document.getElementById('chatKaynak');
        if (kaynak && data.kaynak) kaynak.textContent = data.kaynak;

        // Güvenlik uyarısı sayacını güncelle
        if (data.canli_durum && data.canli_durum.kritik_uyari) {
            const el = document.getElementById('statGuvenlik');
            if (el) el.textContent = data.canli_durum.kritik_uyari.length;
        }
    } catch (e) {
        const thinking = document.getElementById('chatThinking');
        if (thinking) thinking.remove();
        chatMesajEkle('ai', '⚠️ Bağlantı hatası. Lütfen tekrar deneyin.');
    }
}

function sonucGoster(html) {
    const resBox = document.getElementById('result');
    if (!resBox) return;
    resBox.innerHTML = `
        <div class="result-header">
            <div class="result-live-dot"></div>
            <div class="result-title">🏗️ AI Yanıtı</div>
            <div class="result-live-tag">LIVE</div>
        </div>
        <div class="result-body">${html}</div>`;
}

// --- 🧠 ANA SORU SİSTEMİ ---
async function soruSor() {
    const input = document.getElementById('soruInput');
    const resBox = document.getElementById('result');
    const soru = input.value;
    if (!soru && !secilenResimBase64) return;

    const hava = (document.getElementById('temp').innerText || "") + " " + (document.getElementById('condition').innerText || "");
    input.value = "";
    resBox.innerHTML = `<i>${TRANSLATIONS[aktifDil].thinking}</i>`;

    const token = localStorage.getItem('bai_token') || '';
    const payload = { soru: soru, hava: hava, resim_base64: secilenResimBase64, dil: aktifDil, token, konusma_tonu: localStorage.getItem('ai_konusma_tonu') || 'saha_arkadasi' };

    try {
        const response = await fetch('/sor', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (response.status === 429) {
            const data = await response.json();
            resBox.innerHTML = `<div style="text-align:center; padding:20px;"><div style="font-size:2rem; margin-bottom:10px;">⚡</div><div style="color:#e67e22; font-size:1.1rem; font-weight:bold; margin-bottom:10px;">Limit Doldu!</div><div style="color:#aaa; margin-bottom:20px;">${data.detail}</div><button onclick="proYukselt()" style="background:#e67e22; color:white; border:none; padding:12px 30px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:1rem;">⚡ Pro'ya Geç — 10$/ay</button></div>`;
            return;
        }
        const data = await response.json();

        // Stok komutu kontrolü
        try {
            const cevapTemiz = data.cevap.trim().replace(/```json|```/g, '');
            const parsed = JSON.parse(cevapTemiz);
            if (parsed.stok_komutu === true) {
                await stokKomutuIsle(parsed);
                return;
            }
        } catch(e) {}

        const t = TRANSLATIONS[aktifDil];
        const formatliCevap = markdownToHtml(data.cevap);
        resBox.innerHTML = `
            <div class="res-title">${t.aiAnaliz}</div>
            <div id="analizMetni" style="color:#1E293B; font-size:0.95rem; line-height:1.7; margin-top:10px;">${formatliCevap}</div>
            <button onclick="ingilizceyeCevir()" style="margin-top:15px; background:#2563eb; color:white; border:none; padding:12px 20px; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">${t.translateBtn}</button>
            <button onclick="pdfIndir()" style="margin-top:10px; background:#8b5cf6; color:white; border:none; padding:12px 20px; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">📄 ${aktifDil === 'tr' ? 'PDF Rapor İndir' : 'Download PDF Report'}</button>
            <button onclick="gunlukRaporuKaydet()" style="margin-top:10px; background:#27ae60; color:white; border:none; padding:12px 20px; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">${t.saveBtn}</button>
        `;

        secilenResimBase64 = null;
        const imgBtn = document.getElementById('imgBtn');
        if (imgBtn) imgBtn.classList.remove('active-img');
        document.getElementById('soruInput').placeholder = "Soru sor, hesap seç veya fotoğraf yükle...";
    } catch (e) {
        resBox.innerHTML = "⚠️ BAĞLANTI HATASI";
    }
}

// --- 🇬🇧 İNGİLİZCE ÇEVİRİ ---
async function ingilizceyeCevir() {
    const analizMetni = document.getElementById('analizMetni').innerText;
    const resBox = document.getElementById('result');
    resBox.innerHTML += "<div id='ceviriLoading'><i>⏳ Generating Technical Report in English...</i></div>";

    try {
        const response = await fetch('/cevir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ metin: analizMetni })
        });
        const data = await response.json();
        document.getElementById('ceviriLoading').remove();
        resBox.innerHTML = `
            <div class="res-title" style="color:#3498db;">🇬🇧 TECHNICAL REPORT</div>
            <div class="res-detail" id="englishMetni" style="color:#fff; font-size:1.1rem; border-top:none;">${data.cevap}</div>
            <button onclick="sesliOkuEn()" style="margin-top:15px; background:#e67e22; color:white; border:none; padding:12px 20px; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">🔊 Read Aloud (Listening Practice)</button>
        `;
    } catch (e) {
        alert("Çeviri hatası!");
    }
}

// --- 🔊 SESLİ OKUMA ---
const synth = window.speechSynthesis;
let aktifAudio = null;
let yukluSesler = [];

function sesYukle() {
    yukluSesler = synth.getVoices();
}
synth.onvoiceschanged = sesYukle;
sesYukle();

function enIyiSesiSec(langCode) {
    if (yukluSesler.length === 0) yukluSesler = synth.getVoices();
    // Exact locale match first (e.g. tr-TR)
    let ses = yukluSesler.find(v => v.lang === langCode);
    if (!ses) {
        // Partial match (e.g. lang starts with "tr")
        const prefix = langCode.split('-')[0];
        ses = yukluSesler.find(v => v.lang.startsWith(prefix));
    }
    // Fallback: first available voice
    return ses || yukluSesler[0] || null;
}

async function sesliOku() {
    const metin = document.getElementById('analizMetni') ? document.getElementById('analizMetni').innerText : "";
    if (!metin) return;

    // Stop any existing playback
    sesliDurdur();

    const okuBtn = document.querySelector('.btn-read-oku');
    if (okuBtn) { okuBtn.disabled = true; okuBtn.innerText = '⏳...'; }

    metin = metin.replace(/°C/g, " santigrat derece").replace(/°F/g, " fahrenheit derece").replace(/°/g, " derece");

    try {
        const res = await fetch('/sesli-oku', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ metin: metin, dil: aktifDil })
        });
        if (!res.ok) throw new Error('TTS failed');
        const data = await res.json();

        // Decode base64 audio and play
        const audioBytes = Uint8Array.from(atob(data.audio_base64), c => c.charCodeAt(0));
        const audioBlob = new Blob([audioBytes], { type: data.format === 'mp3' ? 'audio/mpeg' : 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        aktifAudio = new Audio(audioUrl);
        aktifAudio.onended = () => { URL.revokeObjectURL(audioUrl); aktifAudio = null; };
        aktifAudio.play();
    } catch (e) {
        // Fallback to browser TTS with best available Turkish voice
        const utter = new SpeechSynthesisUtterance(metin);
        utter.lang = 'tr-TR';
        utter.rate = 0.9;
        utter.pitch = 1.0;
        utter.volume = 1.0;
        const ses = enIyiSesiSec('tr-TR');
        if (ses) utter.voice = ses;
        synth.speak(utter);
    } finally {
        if (okuBtn) { okuBtn.disabled = false; okuBtn.innerText = TRANSLATIONS[aktifDil].readBtn; }
    }
}

function sesliDurdur() {
    if (aktifAudio) { aktifAudio.pause(); aktifAudio = null; }
    synth.cancel();
}

function sesliOkuEn() {
    const metin = document.getElementById('englishMetni') ? document.getElementById('englishMetni').innerText : "";
    if (!metin) return;
    sesliDurdur();
    const utter = new SpeechSynthesisUtterance(metin);
    utter.lang = 'en-US';
    utter.rate = 0.9;
    utter.pitch = 1.0;
    utter.volume = 1.0;
    const ses = enIyiSesiSec('en-US');
    if (ses) utter.voice = ses;
    synth.speak(utter);
}

// --- 🎤 SESLİ DİNLEME ---
let recognition = null;

function sesliDinle() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert("Tarayıcınız sesli girişi desteklemiyor!");
        return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'tr-TR';
    recognition.continuous = false;
    recognition.interimResults = false;

    const btn = document.getElementById('micBtn');
    recognition.onstart = () => { btn.classList.add('recording'); btn.innerHTML = '🎙️'; };
    recognition.onend = () => { btn.classList.remove('recording'); btn.innerHTML = '🎤'; };
    recognition.onresult = (event) => {
        document.getElementById('soruInput').value = event.results[0][0].transcript;
    };
    recognition.start();
}

// --- 📊 MODAL SİSTEMİ ---
let _modalCurrentType = null;

function openModal(title, fields, type) {
    _modalCurrentType = type;
    document.getElementById('modalTitle').textContent = title;
    const body = document.getElementById('modalBody');
    body.innerHTML = '';
    fields.forEach((f, i) => {
        body.innerHTML += '<label class="modal-field-label">' + f.label + '</label>'
            + '<input type="number" step="any" class="modal-input" id="field_' + f.key + '" placeholder="' + f.placeholder + '">';
    });
    // Result alanını sıfırla
    const res = document.getElementById('modalResult');
    if (res) res.classList.remove('visible');
    const btn = document.getElementById('modalHesaplaBtn');
    if (btn) { btn.textContent = 'HESAPLA'; btn.disabled = false; }
    document.getElementById('inputModal').style.display = 'flex';
    setTimeout(() => document.getElementById('inputModal').classList.add('active'), 10);
    // İlk input'a odaklan + Enter tuşu desteği
    setTimeout(() => {
        const first = body.querySelector('.modal-input');
        if (first) first.focus();
        body.querySelectorAll('.modal-input').forEach(inp => {
            inp.onkeydown = (e) => { if (e.key === 'Enter') submitModal(); };
        });
    }, 150);
}

async function submitModal() {
    const type = _modalCurrentType;
    if (!type) return;
    const btn = document.getElementById('modalHesaplaBtn');
    const inputs = {};
    document.querySelectorAll('.modal-input').forEach(i => {
        inputs[i.id.replace('field_', '')] = parseFloat(i.value) || 0;
    });
    if (btn) { btn.textContent = 'Hesaplanıyor...'; btn.disabled = true; }
    try {
        const url = '/hesapla?tip=' + type + '&v1=' + (inputs.v1||0) + '&v2=' + (inputs.v2||0) + '&v3=' + (inputs.v3||0);
        const res = await fetch(url);
        const data = await res.json();
        document.getElementById('modalResultValue').textContent = data.sonuc || '—';
        document.getElementById('modalResultDetail').textContent = data.detay || '';
        document.getElementById('modalResult').classList.add('visible');
        if (btn) { btn.textContent = 'YENİDEN HESAPLA'; btn.disabled = false; }
    } catch(e) {
        document.getElementById('modalResultValue').textContent = 'Hata oluştu';
        document.getElementById('modalResultDetail').textContent = 'Sunucu bağlantısı başarısız.';
        document.getElementById('modalResult').classList.add('visible');
        if (btn) { btn.textContent = 'HESAPLA'; btn.disabled = false; }
    }
}

function closeModal() {
    document.getElementById('inputModal').classList.remove('active');
    setTimeout(() => document.getElementById('inputModal').style.display = 'none', 250);
    _modalCurrentType = null;
}

// --- 🧮 MÜHENDİSLİK HESAPLAMALARI ---
function runCalc(type) {
    let title, fields;

    if (type === 'beton') {
        title = "🧱 Beton Metrajı";
        fields = [{key:'v1',label:'Boy (m)',placeholder:'5'}, {key:'v2',label:'En (m)',placeholder:'0.5'}, {key:'v3',label:'Yükseklik (m)',placeholder:'2.8'}];
    } else if (type === 'demir_ag') {
        title = "⚖️ Donatı Ağırlığı";
        fields = [{key:'v1',label:'Çap (mm)',placeholder:'14'}, {key:'v2',label:'Uzunluk (m)',placeholder:'120'}];
    } else if (type === 'as_alan') {
        title = "📏 Donatı Alanı (As)";
        fields = [{key:'v1',label:'Çap (mm)',placeholder:'14'}, {key:'v2',label:'Adet',placeholder:'4'}];
    } else if (type === 'etriye') {
        title = "🌀 Etriye Boyu";
        fields = [{key:'v1',label:'Boy (cm)',placeholder:'30'}, {key:'v2',label:'En (cm)',placeholder:'25'}, {key:'v3',label:'Çap (mm)',placeholder:'8'}];
    } else if (type === 'tugla') {
        title = "🧱 Tuğla Hesabı";
        fields = [{key:'v1',label:'Duvar Boy (m)',placeholder:'5'}, {key:'v2',label:'Duvar Yükseklik (m)',placeholder:'2.8'}];
    } else if (type === 'seramik') {
        title = "📐 Seramik & Parke";
        fields = [{key:'v1',label:'Alan (m²)',placeholder:'50'}];
    } else if (type === 'boya') {
        title = "🎨 Boya & Sıva";
        fields = [{key:'v1',label:'Alan (m²)',placeholder:'100'}];
    } else if (type === 'kubaj') {
        title = "🚜 Hafriyat Küpajı";
        fields = [{key:'v1',label:'Uzunluk (m)',placeholder:'10'}, {key:'v2',label:'Genişlik (m)',placeholder:'5'}, {key:'v3',label:'Derinlik (m)',placeholder:'2'}];
    } else if (type === 'egim') {
        title = "📐 Eğim & Açı";
        fields = [{key:'v1',label:'Yükseklik Farkı (m)',placeholder:'1'}, {key:'v2',label:'Yatay Mesafe (m)',placeholder:'10'}];
    } else {
        return;
    }

    openModal(title, fields, type);
}

// --- 📝 MARKDOWN → HTML ---
function markdownToHtml(text) {
    return text
        .replace(/## 📋(.+)/g, '<h3 style="color:#e67e22; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(230,126,34,0.3); padding-bottom:6px;">📋$1</h3>')
        .replace(/## ⚠️(.+)/g, '<h3 style="color:#f39c12; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(243,156,18,0.3); padding-bottom:6px;">⚠️$1</h3>')
        .replace(/## 🛡️(.+)/g, '<h3 style="color:#2ecc71; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(46,204,113,0.3); padding-bottom:6px;">🛡️$1</h3>')
        .replace(/## 📐(.+)/g, '<h3 style="color:#3498db; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(52,152,219,0.3); padding-bottom:6px;">📐$1</h3>')
        .replace(/## (.+)/g, '<h3 style="color:#e67e22; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(230,126,34,0.3); padding-bottom:6px;">$1</h3>')
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/^\* (.+)/gm, '<li style="margin:4px 0; color:inherit;">$1</li>')
        .replace(/(<li.*<\/li>\n?)+/g, '<ul style="padding-left:20px; margin:8px 0;">$&</ul>')
        .replace(/\n\n/g, '<br/><br/>')
        .replace(/\n/g, '<br/>');
}

// --- 📸 KAMERA ANALİZİ ---
let kameraStream = null;

async function kameraAc(analiz_tipi) {
    const token = localStorage.getItem('bai_token');
    if (!token) { alert('Lütfen giriş yapın.'); return; }
    document.getElementById('kameraModal').style.display = 'flex';
    document.getElementById('kameraAnalizTipi').value = analiz_tipi;
    try {
        kameraStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
        document.getElementById('kameraVideo').srcObject = kameraStream;
    } catch(e) {
        // Kamera açılamazsa sadece yükleme seçeneği kalır
    }
}

function kameraKapat() {
    if (kameraStream) { kameraStream.getTracks().forEach(t => t.stop()); kameraStream = null; }
    document.getElementById('kameraModal').style.display = 'none';
}

async function fotografCek() {
    const video = document.getElementById('kameraVideo');
    const canvas = document.getElementById('kameraCanvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    canvas.getContext('2d').drawImage(video, 0, 0);
    const base64 = canvas.toDataURL('image/jpeg', 0.8).split(',')[1];
    await kameraAnalizGonder(base64);
}

async function kameraFotoYukle(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async (e) => { await kameraAnalizGonder(e.target.result.split(',')[1]); };
    reader.readAsDataURL(file);
}

let sonAiCevabi = null;

// ── YOLO Sonuç Paneli ────────────────────────────────────────────────────────
function _yoloPaneliOlustur(y) {
  const riskRenk = y.risk_level === 'YÜKSEK' ? '#ef4444'
                 : y.risk_level === 'ORTA'   ? '#f59e0b'
                 :                             '#22c55e';
  const riskIcon = y.risk_level === 'YÜKSEK' ? '🔴'
                 : y.risk_level === 'ORTA'   ? '🟡'
                 :                             '🟢';

  const ihlalHTML = (y.violations || []).length
    ? (y.violations).map(v =>
        `<span style="background:rgba(239,68,68,0.12);color:#fca5a5;border:1px solid rgba(239,68,68,0.3);
                      border-radius:6px;padding:3px 9px;font-size:11px;font-weight:600;">${v}</span>`
      ).join(' ')
    : `<span style="color:#86efac;font-size:12px;">İhlal tespit edilmedi</span>`;

  const ppe = y.ppe_uyum_orani >= 0
    ? `%${Math.round(y.ppe_uyum_orani * 100)}`
    : 'Bilinmiyor';

  return `
    <div id="yoloPaneli" style="margin-top:14px;background:rgba(15,23,42,0.6);border:1px solid rgba(99,102,241,0.25);
                                border-radius:14px;padding:16px;backdrop-filter:blur(4px);">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,0.07);">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
        </svg>
        <span style="color:#818cf8;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1px;">YOLO Yerel Analiz</span>
        <span style="margin-left:auto;font-size:10px;color:#475569;">Conf: ${((y.confidence||0)*100).toFixed(0)}%</span>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:12px;">
        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:10px;text-align:center;">
          <div style="font-size:18px;font-weight:800;color:${riskRenk};">${riskIcon} ${y.risk_level||'—'}</div>
          <div style="font-size:10px;color:#64748b;margin-top:2px;font-weight:600;">RİSK SEVİYESİ</div>
        </div>
        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:10px;text-align:center;">
          <div style="font-size:22px;font-weight:800;color:#f1f5f9;">${y.kisi_sayisi||0}</div>
          <div style="font-size:10px;color:#64748b;margin-top:2px;font-weight:600;">KİŞİ</div>
        </div>
        <div style="background:rgba(255,255,255,0.04);border-radius:10px;padding:10px;text-align:center;">
          <div style="font-size:18px;font-weight:800;color:#34d399;">${ppe}</div>
          <div style="font-size:10px;color:#64748b;margin-top:2px;font-weight:600;">PPE UYUM</div>
        </div>
      </div>

      <div>
        <div style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px;">TESPİT EDİLEN İHLALLER</div>
        <div style="display:flex;flex-wrap:wrap;gap:6px;">${ihlalHTML}</div>
      </div>
    </div>`;
}

async function kameraAnalizGonder(base64) {
    const token = localStorage.getItem('bai_token');
    const analiz_tipi = document.getElementById('kameraAnalizTipi').value;
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'Sivas';
    const hava = (document.getElementById('temp') ? document.getElementById('temp').innerText : '') + ' ' +
                 (document.getElementById('condition') ? document.getElementById('condition').innerText : '');
    const resBox = document.getElementById('result');
    kameraKapat();
    resBox.innerHTML = '<i>📸 Fotoğraf analiz ediliyor...</i>';
    // Önceki YOLO sonucunu temizle
    const _yoloMP = document.getElementById('yoloModalPanel');
    if (_yoloMP) _yoloMP.innerHTML = '';

    // Store image for bounding box overlay
    const imgData = 'data:image/jpeg;base64,' + base64;

    // Her iki isteği aynı anda başlat
    const aiPromise   = fetch('/kamera-analiz', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({token, resim_base64: base64, analiz_tipi, hava, sehir, dil: aktifDil})
    });
    const yoloPromise = fetch('/yolo/frame', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({token, resim_base64: base64, santiye_id: null})
    });

    try {
        const res = await aiPromise;

        const data = await res.json();
        if (!res.ok) {
            const mesaj = res.status === 429
                ? `<div style="font-size:2rem">🔒</div><strong style="color:#e74c3c">Limit doldu!</strong><div style="color:#aaa;margin-top:8px">${data.detail}</div>`
                : res.status === 503
                ? `<div style="font-size:2rem">⏳</div><strong style="color:#f59e0b">AI servisi yoğun</strong><div style="color:#aaa;margin-top:8px">${data.detail || 'Lütfen birkaç saniye sonra tekrar deneyin.'}</div>`
                : `<div style="font-size:2rem">❌</div><strong style="color:#e74c3c">Hata</strong><div style="color:#aaa;margin-top:8px">${data.detail || 'Bilinmeyen hata'}</div>`;
            resBox.innerHTML = `<div style="text-align:center;padding:20px">${mesaj}</div>`;
            return;
        }
        const p = data.parsed;
        const t = TRANSLATIONS[aktifDil];

        // ── Ortak foto bloğu — tüm tipler için ──
        const fotoBlok = `
            <div id="analizImgWrap" style="position:relative;display:inline-block;width:100%;margin:12px 0 16px;border-radius:12px;overflow:hidden;line-height:0;">
                <img id="analizImg" src="${imgData}" style="width:100%;display:block;border-radius:12px;">
                <canvas id="bbCanvas" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:50;"></canvas>
            </div>`;

        if (analiz_tipi === 'guvenlik' && p) {
            const skor = p.guvenlik_skoru || 0;
            const skorRenk = skor >= 70 ? '#2ecc71' : skor >= 40 ? '#f39c12' : '#e74c3c';
            const ihlaller = (p.ihlaller || []).map(ih =>
                `<div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:10px;padding:10px 14px;margin-bottom:8px;color:#fca5a5;font-size:0.88rem;">🚨 ${ih.aciklama}</div>`
            ).join('');
            const uygunlar = (p.uygun_unsurlar || []).map(u =>
                `<div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.25);border-radius:10px;padding:10px 14px;margin-bottom:8px;color:#86efac;font-size:0.88rem;">✅ ${u}</div>`
            ).join('');
            const onlemler = (p.acil_onlemler || []).map(o =>
                `<div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.25);border-radius:10px;padding:10px 14px;margin-bottom:8px;color:#fcd34d;font-size:0.88rem;">⚠️ ${o}</div>`
            ).join('');

            resBox.innerHTML = `
                <div class="res-title">🦺 GÜVENLİK ANALİZİ</div>
                ${fotoBlok}
                <div style="display:flex;align-items:center;gap:16px;background:rgba(255,255,255,0.04);border-radius:14px;padding:16px;margin-bottom:16px;">
                    <div style="width:64px;height:64px;border-radius:50%;border:4px solid ${skorRenk};display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                        <span style="color:${skorRenk};font-size:1.1rem;font-weight:900;">${skor}</span>
                    </div>
                    <div>
                        <div style="color:white;font-weight:700;font-size:1rem;">Güvenlik Skoru</div>
                        <div style="color:#aaa;font-size:0.85rem;margin-top:2px;">${p.ozet || ''}</div>
                    </div>
                </div>
                ${ihlaller ? `<div style="margin-bottom:12px"><div style="color:#e74c3c;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">İHLALLER</div>${ihlaller}</div>` : ''}
                ${uygunlar ? `<div style="margin-bottom:12px"><div style="color:#2ecc71;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">UYGUN UNSURLAR</div>${uygunlar}</div>` : ''}
                ${onlemler ? `<div style="margin-bottom:16px"><div style="color:#f39c12;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">ACİL ÖNLEMLER</div>${onlemler}</div>` : ''}
                <div id="analizMetni" style="display:none;">${p.ozet || ''}</div>
                <button onclick="pdfIndir()" style="width:100%;margin-top:8px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">📄 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
            // Hibrit analiz kutularını çiz (YOLO + Gemini — visual_data varsa kullan)
            _drawAnalizFromResponse(data);

        } else if (analiz_tipi === 'ilerleme' && p) {
            const yuzde = Math.min(100, Math.max(0, p.ilerleme_yuzdesi || 0));
            const renk = yuzde >= 71 ? '#2ecc71' : yuzde >= 31 ? '#f59e0b' : '#ef4444';
            const tamamlanan = (p.tamamlanan_isler || []).map(i => `<li style="color:#86efac;margin:4px 0;font-size:0.88rem;">✅ ${i}</li>`).join('');
            const devam = (p.devam_eden_isler || []).map(i => `<li style="color:#93c5fd;margin:4px 0;font-size:0.88rem;">🔄 ${i}</li>`).join('');
            const gecikmeler = (p.olasi_gecikmeler || []).map(i => `<li style="color:#fcd34d;margin:4px 0;font-size:0.88rem;">⚠️ ${i}</li>`).join('');

            resBox.innerHTML = `
                <div class="res-title">📅 İLERLEME TAKİBİ</div>
                ${fotoBlok}
                <div style="display:flex;justify-content:center;margin:16px 0;">
                    <div style="position:relative;width:140px;height:140px;">
                        <svg width="140" height="140" style="transform:rotate(-90deg)">
                            <circle cx="70" cy="70" r="58" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="12"/>
                            <circle id="progressCircle" cx="70" cy="70" r="58" fill="none" stroke="${renk}" stroke-width="12"
                                stroke-dasharray="${2 * Math.PI * 58}" stroke-dashoffset="${2 * Math.PI * 58}"
                                stroke-linecap="round" style="transition:stroke-dashoffset 1.5s cubic-bezier(0.19,1,0.22,1)"/>
                        </svg>
                        <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;">
                            <span id="progressNum" style="color:white;font-size:2rem;font-weight:900;line-height:1;">0</span>
                            <span style="color:#aaa;font-size:0.75rem;font-weight:700;">TAMAMLANDI</span>
                        </div>
                    </div>
                </div>
                <div style="background:rgba(255,255,255,0.04);border-radius:12px;padding:14px;margin-bottom:12px;text-align:center;">
                    <div style="color:#aaa;font-size:0.8rem;">Tahmini Süre</div>
                    <div style="color:white;font-weight:700;margin-top:4px;">${p.tahmini_sure || '-'}</div>
                </div>
                ${tamamlanan ? `<div style="margin-bottom:12px"><div style="color:#2ecc71;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">TAMAMLANAN İŞLER</div><ul style="list-style:none;padding:0;">${tamamlanan}</ul></div>` : ''}
                ${devam ? `<div style="margin-bottom:12px"><div style="color:#3b82f6;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">DEVAM EDEN</div><ul style="list-style:none;padding:0;">${devam}</ul></div>` : ''}
                ${gecikmeler ? `<div style="margin-bottom:16px"><div style="color:#f59e0b;font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">OLASI GECİKMELER</div><ul style="list-style:none;padding:0;">${gecikmeler}</ul></div>` : ''}
                <div id="analizMetni" style="display:none;">${p.ozet || ''}</div>
                <button onclick="pdfIndir()" style="width:100%;margin-top:8px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">📄 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
            setTimeout(() => {
                const circle = document.getElementById('progressCircle');
                const numEl = document.getElementById('progressNum');
                if (circle) { const c = 2 * Math.PI * 58; circle.style.strokeDashoffset = c * (1 - yuzde / 100); }
                if (numEl) {
                    let cur = 0; const step = yuzde / 60;
                    const t = setInterval(() => { cur = Math.min(yuzde, cur + step); numEl.textContent = Math.round(cur) + '%'; if (cur >= yuzde) clearInterval(t); }, 25);
                }
            }, 100);
            _drawAnalizFromResponse(data);

        } else if (analiz_tipi === 'genel' && p && p.kategoriler) {
            const k = p.kategoriler;
            const durumRenk = (d) => d === 'iyi' ? '#2ecc71' : d === 'orta' ? '#f59e0b' : d === 'kotu' ? '#ef4444' : '#94a3b8';
            const seviyeRenk = (s) => s === 'dusuk' ? '#2ecc71' : s === 'orta' ? '#f59e0b' : '#ef4444';

            resBox.innerHTML = `
                <div class="res-title">🔍 GENEL ANALİZ</div>
                ${fotoBlok}
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                    <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><span style="font-size:1.2rem;">🦺</span><span style="color:${durumRenk(k.guvenlik?.durum)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.guvenlik?.durum || '-'}</span></div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Güvenlik</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.guvenlik?.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><span style="font-size:1.2rem;">📅</span><span style="color:${durumRenk(k.ilerleme?.durum)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.ilerleme?.durum || '-'}</span></div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">İlerleme</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.ilerleme?.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(249,115,22,0.08);border:1px solid rgba(249,115,22,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><span style="font-size:1.2rem;">📦</span><span style="color:var(--primary);font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.malzeme?.durum || '-'}</span></div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Malzeme</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.malzeme?.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><span style="font-size:1.2rem;">⚠️</span><span style="color:${seviyeRenk(k.risk?.seviye)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.risk?.seviye || '-'}</span></div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Risk</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.risk?.ozet || ''}</div>
                    </div>
                </div>
                <div id="analizMetni" style="display:none;">${data.cevap || ''}</div>
                <button onclick="pdfIndir()" style="width:100%;margin-top:16px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">📄 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
            _drawAnalizFromResponse(data);
        } else {
            resBox.innerHTML = `
                <div class="res-title">📸 KAMERA ANALİZİ</div>
                ${fotoBlok}
                <div id="analizMetni" style="color:#1E293B;font-size:0.95rem;line-height:1.7;margin-top:10px;">${markdownToHtml(data.cevap)}</div>
                <button onclick="pdfIndir()" style="width:100%;margin-top:15px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">📄 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
            _drawAnalizFromResponse(data);
        }

        sonAiCevabi = data.cevap;

        // YOLO stats paneli: allSettled — biri çökerse diğeri çalışmaya devam eder.
        // Not: YOLO tespitleri artık backend'de /kamera-analiz içine gömülü gelir
        // (data.visual_data.yolo_boxes). Ayrı YOLO çağrısı sadece stats paneli için.
        try {
            const [yoloSettled] = await Promise.allSettled([yoloPromise]);
            const yoloPanel = document.getElementById('yoloModalPanel');
            if (yoloSettled.status === 'fulfilled' && yoloSettled.value.ok) {
                const yoloStats = await yoloSettled.value.json();
                if (yoloPanel) yoloPanel.innerHTML = _yoloPaneliOlustur(yoloStats);
                // Ayrı YOLO çağrısı canvas'taki tespitleri geliştirirse yeniden çiz
                if (yoloStats.tespitler && yoloStats.tespitler.length > 0) {
                    _drawAnalizFromResponse(data, yoloStats);
                }
                // Annotated thumbnail kaydet
                if (data.analiz_id) {
                    try {
                        const annotated = await kpBboxThumb(base64, yoloStats.tespitler || []);
                        localStorage.setItem('bai_thumb_' + data.analiz_id, annotated);
                        localStorage.setItem('bai_yolo_' + data.analiz_id, JSON.stringify(yoloStats));
                    } catch(_) {}
                }
            } else {
                if (yoloPanel) yoloPanel.innerHTML = '<div style="color:#f59e0b;font-size:12px;padding:8px;">YOLO servisi yanıt vermedi.</div>';
                if (data.analiz_id) {
                    try { localStorage.setItem('bai_thumb_' + data.analiz_id, imgData); } catch(_) {}
                }
            }
        } catch(_) {
            const yoloPanel = document.getElementById('yoloModalPanel');
            if (yoloPanel) yoloPanel.innerHTML = '<div style="color:#f59e0b;font-size:12px;padding:8px;">YOLO servisi yanıt vermedi.</div>';
            if (data.analiz_id) {
                try { localStorage.setItem('bai_thumb_' + data.analiz_id, imgData); } catch(_) {}
            }
        }

        // Kamera sayfası AI Anlık Fotoğraf Kanıtları listesini güncelle
        if (typeof kameraPageYukle === 'function') kameraPageYukle();

    } catch(e) {
        resBox.innerHTML = `<div style="color:#e74c3c;">Analiz hatası: ${e.message}</div>`;
    }
}

// ihlaller-only çizici (eski yollar için uyumluluk katmanı — drawAnaliz'e yönlendirir)
function drawBoundingBoxes(ihlaller) {
    drawAnaliz(null, { parsed: { ihlaller } });
}

// YOLO-only çizici (eski yollar için uyumluluk katmanı — drawAnaliz'e yönlendirir)
function drawYoloBoundingBoxes(tespitler) {
    drawAnaliz({ tespitler }, null);
}

// ═══════════════════════════════════════════════════════════════════════════
//  Visual Fusion — Hibrit Analiz Canvas Çizicisi (GÜNCEL & KESİN ÇÖZÜM)
// ═══════════════════════════════════════════════════════════════════════════

function _drawAnalizFromResponse(data, yoloStats) {
    const vd = (data && data.visual_data) || {};
    const yoloSrc = yoloStats || (vd.yolo_boxes && vd.yolo_boxes.length > 0 ? { tespitler: vd.yolo_boxes } : null);
    drawAnaliz(yoloSrc, data);
}

function _drawBox(ctx, x, y, w, h, color, label, dashed) {
    if (w <= 0 || h <= 0) return;
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth   = 3;
    ctx.setLineDash(dashed ? [6, 6] : []);
    ctx.strokeRect(x, y, w, h);
    ctx.setLineDash([]);

    if (label) {
        ctx.font = 'bold 12px "Courier New", monospace';
        const tw = ctx.measureText(label).width + 10;
        const lh = 20;
        const ly = (y >= lh) ? y - lh : y + 4;
        const lx = Math.min(x, ctx.canvas.width - tw - 2);

        ctx.fillStyle = color;
        ctx.fillRect(lx, ly, tw, lh);

        ctx.fillStyle = '#ffffff';
        ctx.fillText(label, lx + 5, ly + lh - 5);
    }
    ctx.restore();
}

function drawAnaliz(yoloData, geminiData) {
    const canvas = document.getElementById('bbCanvas');
    const img    = document.getElementById('analizImg');
    if (!canvas || !img) return;

    // KRİTİK DÜZELTME 1: CSS İle Katmanlama
    const wrap = img.closest('#analizImgWrap');
    if (wrap) {
        wrap.style.position = 'relative';
        wrap.style.display  = 'block';
    }

    canvas.style.position      = 'absolute';
    canvas.style.top           = '0';
    canvas.style.left          = '0';
    canvas.style.width         = '100%';
    canvas.style.height        = '100%';
    canvas.style.zIndex        = '10';
    canvas.style.pointerEvents = 'none';

    const vd = (geminiData && geminiData.visual_data) || {};
    const yoloBboxs = (yoloData && yoloData.tespitler) ? yoloData.tespitler : (vd.yolo_boxes || []);
    const gBoxes    = vd.gemini_risk_boxes ? vd.gemini_risk_boxes : (geminiData && geminiData.gemini_boxes || []);
    const ihlaller  = (geminiData && geminiData.parsed && Array.isArray(geminiData.parsed.ihlaller)) ? geminiData.parsed.ihlaller : [];

    function _paint() {
        // KRİTİK DÜZELTME 2: Çözünürlük ve Ölçekleme
        const dispW = img.clientWidth;
        const dispH = img.clientHeight;

        if (!dispW || !dispH) {
            requestAnimationFrame(_paint);
            return;
        }

        canvas.width  = dispW;
        canvas.height = dispH;

        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, dispW, dispH);

        // KRİTİK DÜZELTME 3: Çizim Matematiği
        const natW = img.naturalWidth;
        const natH = img.naturalHeight;

        if (natW && natH) {
            const sx = dispW / natW;
            const sy = dispH / natH;

            // 1. YOLO Çizimleri (Gerçek Pikseller -> Ekran Pikselleri)
            yoloBboxs.forEach(t => {
                if (!t.bbox || t.bbox.length < 4) return;
                const [x1, y1, x2, y2] = t.bbox;
                const cls    = (t.class || '').toLowerCase();
                const conf   = Math.round((t.confidence || 0) * 100);
                const isViol = cls.startsWith('no_') || cls.includes('without');
                const isPers = cls === 'person';
                const color  = isViol ? '#EF4444' : isPers ? '#3B82F6' : '#10B981';
                const label  = cls.replace(/_/g, ' ').toUpperCase() + (conf ? ' %' + conf : '');
                _drawBox(ctx, x1 * sx, y1 * sy, (x2 - x1) * sx, (y2 - y1) * sy, color, label, false);
            });
        }

        // 2. Gemini Çizimleri (Normalize Koordinatlar -> Ekran Pikselleri)
        gBoxes.forEach((g, i) => {
            if (!Array.isArray(g.box) || g.box.length < 4) return;
            let [ymin, xmin, ymax, xmax] = g.box;

            // Gemini halüsinasyon düzeltmesi: piksel değeri uydurunca normalize et
            if (xmax > 1 || ymax > 1) {
                xmin /= 1000; ymin /= 1000; xmax /= 1000; ymax /= 1000;
            }

            if (xmax <= xmin || ymax <= ymin) return;

            const isHigh = (g.risk === 'yüksek' || g.risk === 'high');
            const color  = isHigh ? '#EF4444' : '#F97316';
            const label  = (g.label || 'RİSK BÖLGESİ').toUpperCase();
            _drawBox(ctx, xmin * dispW, ymin * dispH, (xmax - xmin) * dispW, (ymax - ymin) * dispH, color, label, true);
        });

        // 3. Eski İhlal Formatı Uyumluluğu
        ihlaller.forEach((ih, i) => {
            if (ih.x === undefined || ih.w === undefined) return;
            const label = '⚠ ' + (ih.aciklama || 'İHLAL').toUpperCase();
            _drawBox(ctx, ih.x * dispW, ih.y * dispH, ih.w * dispW, ih.h * dispH, '#F97316', label, true);
        });
    }

    if (img.complete && img.naturalWidth > 0) {
        _paint();
    } else {
        img.onload = _paint;
    }
}

// --- 📁 ARŞİV SAYFASI ---
let _arsivData = { raporlar: [], kamera_analizler: [] };
let _arsivAktifTab = 'tumu';

function arsivPageAc() {
  ['content','aiCommandBar','santiyePage','fiyatPage','stokPage','kameraPage'].forEach(pid => {
    const el = document.getElementById(pid);
    if (el) el.style.display = 'none';
  });
  const page = document.getElementById('arsivPage');
  if (!page) return;
  page.style.display = 'flex';
  arsivVeriYukle();
}

async function arsivVeriYukle() {
  const token = localStorage.getItem('bai_token');
  if (!token) return;
  document.getElementById('arsivIcerik').innerHTML = '<div style="text-align:center;padding:60px 20px;color:#94A3B8;"><div style="font-size:32px;margin-bottom:8px;">📁</div><div style="font-size:14px;font-weight:600;">Yükleniyor...</div></div>';
  try {
    const res = await fetch('/arsiv?token=' + token);
    _arsivData = await res.json();
    arsivIstatistikGuncelle();
    arsivRenderListe();
  } catch(e) {
    document.getElementById('arsivIcerik').innerHTML = '<div style="text-align:center;padding:40px;color:#EF4444;font-size:13px;">Arşiv yüklenemedi.</div>';
  }
}

function arsivIstatistikGuncelle() {
  const r = (_arsivData.raporlar || []).length;
  const k = (_arsivData.kamera_analizler || []).length;
  const el = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
  el('arsivStatRapor', r);
  el('arsivStatKamera', k);
  el('arsivStatToplam', r + k);
  const sub = document.getElementById('arsivSubtitle');
  if (sub) sub.textContent = 'Toplam ' + (r + k) + ' kayıt arşivlendi';
}

function arsivTabSec(tab) {
  _arsivAktifTab = tab;
  ['tumu','rapor','kamera'].forEach(t => {
    const btn = document.getElementById('arsivTab' + t.charAt(0).toUpperCase() + t.slice(1));
    if (!btn) return;
    const active = t === tab;
    btn.style.background = active ? '#0F172A' : 'white';
    btn.style.color = active ? 'white' : '#64748B';
    btn.style.borderColor = active ? '#0F172A' : '#E2E8F0';
  });
  arsivRenderListe();
}

function arsivFiltrele() { arsivRenderListe(); }

function arsivRenderListe() {
  const q = (document.getElementById('arsivAramaInput') || {}).value || '';
  const raporlar = (_arsivData.raporlar || []).filter(r =>
    !q || (r.ozet||'').toLowerCase().includes(q.toLowerCase()) || (r.tarih||'').includes(q)
  );
  const kameralar = (_arsivData.kamera_analizler || []).filter(k =>
    !q || (k.ozet||'').toLowerCase().includes(q.toLowerCase()) || (k.sehir||'').toLowerCase().includes(q.toLowerCase())
  );

  let html = '';

  const showRapor = _arsivAktifTab === 'tumu' || _arsivAktifTab === 'rapor';
  const showKamera = _arsivAktifTab === 'tumu' || _arsivAktifTab === 'kamera';

  if (showRapor && raporlar.length > 0) {
    html += '<div style="font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;margin-top:' + (html ? '24px' : '0') + '">📊 AI Raporları (' + raporlar.length + ')</div>';
    html += '<div style="display:flex;flex-direction:column;gap:8px;">';
    raporlar.forEach(r => {
      const tarih = r.tarih || (r.created_at ? r.created_at.slice(0,10) : '—');
      const ozet = (r.ozet || '').replace(/#{1,6}\s*/g,'').replace(/\*\*/g,'').replace(/\*/g,'').replace(/`/g,'').substring(0,110);
      html += '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-left:3px solid #F97316;border-radius:12px;padding:14px 16px;display:flex;align-items:flex-start;gap:12px;transition:box-shadow 0.15s;" onmouseover="this.style.boxShadow=\'0 4px 12px rgba(0,0,0,0.08)\'" onmouseout="this.style.boxShadow=\'none\'">'
        + '<div style="flex:1;cursor:pointer;" onclick="arsivDetayGoster(\'rapor\',' + r.id + ')">'
        + '<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">'
        + '<span style="font-size:10px;font-weight:700;background:#FFF7ED;color:#F97316;padding:2px 8px;border-radius:6px;letter-spacing:0.04em;">AI RAPOR</span>'
        + '<span style="font-size:11px;color:#94A3B8;">📅 ' + tarih + '</span>'
        + '</div>'
        + '<div style="font-size:13px;color:#334155;line-height:1.5;">' + ozet + (ozet.length >= 110 ? '...' : '') + '</div>'
        + '</div>'
        + '<button onclick="arsivSil(\'rapor\',' + r.id + ')" title="Sil" style="width:30px;height:30px;background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#EF4444;font-size:13px;transition:background 0.15s;" onmouseover="this.style.background=\'#EF4444\';this.style.color=\'white\'" onmouseout="this.style.background=\'#FEF2F2\';this.style.color=\'#EF4444\'">🗑</button>'
        + '</div>';
    });
    html += '</div>';
  }

  if (showKamera && kameralar.length > 0) {
    html += '<div style="font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;margin-top:' + (html ? '24px' : '0') + '">📸 Kamera Analizleri (' + kameralar.length + ')</div>';
    html += '<div style="display:flex;flex-direction:column;gap:8px;">';
    kameralar.forEach(k => {
      const tipRenk = k.tip === 'guvenlik' ? '#D97706' : k.tip === 'ilerleme' ? '#2563EB' : '#7C3AED';
      const tipBg   = k.tip === 'guvenlik' ? '#FFFBEB' : k.tip === 'ilerleme' ? '#EFF6FF' : '#F5F3FF';
      const tipAd   = k.tip === 'guvenlik' ? 'GÜVENLİK' : k.tip === 'ilerleme' ? 'İLERLEME' : 'GENEL';
      const tarih   = k.created_at ? k.created_at.slice(0,10) : '—';
      const ozet    = (k.ozet || '').replace(/#{1,6}\s*/g,'').replace(/\*\*/g,'').replace(/\*/g,'').replace(/`/g,'').replace(/[🚨⚠️✅❌🔴]/gu,'').trim().substring(0,110);
      const thumb   = localStorage.getItem('bai_thumb_' + k.id);
      html += '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-left:3px solid ' + tipRenk + ';border-radius:12px;padding:14px 16px;display:flex;align-items:flex-start;gap:12px;transition:box-shadow 0.15s;" onmouseover="this.style.boxShadow=\'0 4px 12px rgba(0,0,0,0.08)\'" onmouseout="this.style.boxShadow=\'none\'">'
        + (thumb ? '<img src="' + thumb + '" style="width:52px;height:40px;object-fit:cover;border-radius:6px;flex-shrink:0;cursor:pointer;" onclick="arsivDetayGoster(\'kamera\',' + k.id + ')">' : '')
        + '<div style="flex:1;cursor:pointer;" onclick="arsivDetayGoster(\'kamera\',' + k.id + ')">'
        + '<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;flex-wrap:wrap;">'
        + '<span style="font-size:10px;font-weight:700;background:' + tipBg + ';color:' + tipRenk + ';padding:2px 8px;border-radius:6px;letter-spacing:0.04em;">' + tipAd + '</span>'
        + (k.sehir ? '<span style="font-size:11px;color:#64748B;">📍 ' + k.sehir + '</span>' : '')
        + '<span style="font-size:11px;color:#94A3B8;">📅 ' + tarih + '</span>'
        + '</div>'
        + '<div style="font-size:13px;color:#334155;line-height:1.5;">' + ozet + (ozet.length >= 110 ? '...' : '') + '</div>'
        + '</div>'
        + '<button onclick="arsivSil(\'kamera\',' + k.id + ')" title="Sil" style="width:30px;height:30px;background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#EF4444;font-size:13px;transition:background 0.15s;" onmouseover="this.style.background=\'#EF4444\';this.style.color=\'white\'" onmouseout="this.style.background=\'#FEF2F2\';this.style.color=\'#EF4444\'">🗑</button>'
        + '</div>';
    });
    html += '</div>';
  }

  if (!html) {
    html = '<div style="text-align:center;padding:60px 20px;color:#94A3B8;">'
      + '<div style="font-size:40px;margin-bottom:10px;">📭</div>'
      + '<div style="font-size:14px;font-weight:600;color:#64748B;">Kayıt bulunamadı</div>'
      + '<div style="font-size:12px;margin-top:4px;">' + (q ? '"' + q + '" için sonuç yok' : 'Henüz arşiv kaydı oluşturulmamış') + '</div>'
      + '</div>';
  }

  document.getElementById('arsivIcerik').innerHTML = html;
}

async function arsivDetayGoster(tip, id) {
  const token = localStorage.getItem('bai_token');
  const modal = document.getElementById('arsivDetayModal');
  const icerikEl = document.getElementById('arsivDetayIcerik');
  const baslikEl = document.getElementById('arsivDetayBaslik');
  if (!modal) return;
  modal.style.display = 'flex';
  icerikEl.innerHTML = '<div style="text-align:center;padding:40px;color:#64748B;">Yükleniyor...</div>';
  try {
    const res = await fetch('/arsiv/' + tip + '/' + id + '?token=' + token);
    const data = await res.json();
    const icerik = data.content || data.sonuc || '';
    if (baslikEl) baslikEl.textContent = tip === 'rapor' ? '📊 AI Raporu' : '📸 Kamera Analizi';
    icerikEl.innerHTML = markdownToHtml(icerik);
  } catch(e) {
    icerikEl.innerHTML = '<div style="color:#EF4444;">Yüklenemedi.</div>';
  }
}

function arsivDetayKapat() {
  const modal = document.getElementById('arsivDetayModal');
  if (modal) modal.style.display = 'none';
}

function arsivKapat() {
  const page = document.getElementById('arsivPage');
  if (page) page.style.display = 'none';
  const content = document.getElementById('content');
  if (content) content.style.display = '';
}

// Legacy alias (backward compat)
function arsivAc() { arsivPageAc(); }

async function arsivSil(tip, id) {
  if (!confirm('Bu kaydı kalıcı olarak silmek istediğinize emin misiniz?')) return;
  const token = localStorage.getItem('bai_token');
  const endpoint = tip === 'rapor' ? '/rapor-sil/' + id : '/kanit-sil/' + id;
  try {
    const res = await fetch(endpoint + '?token=' + token, { method: 'DELETE' });
    if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Hata'); }
    showToast('Kayıt silindi', 'success');
    if (tip === 'kamera') {
      _kpTumAnaliz = (_kpTumAnaliz || []).filter(k => k.id !== id);
      localStorage.removeItem('bai_thumb_' + id);
      localStorage.removeItem('bai_yolo_'  + id);
      kpRenderAiKartlar(_kpTumAnaliz);
      kpRenderTespitAkisi(kpGetVisibleAnaliz());
      kpRenderStats(kpGetVisibleAnaliz());
    }
    // Lokal veriyi güncelle ve sayfayı yeniden render et
    if (tip === 'rapor') _arsivData.raporlar = (_arsivData.raporlar||[]).filter(r => r.id !== id);
    else _arsivData.kamera_analizler = (_arsivData.kamera_analizler||[]).filter(k => k.id !== id);
    arsivIstatistikGuncelle();
    arsivRenderListe();
    arsivDetayKapat();
  } catch(e) {
    showToast('Hata: ' + e.message, 'error');
  }
}

let secilenPlan = 'free';
let selectedPlan = 'free';

// Active panel tracker
let _activePanel = 'login';

function switchPanel(panel) {
    if (panel === _activePanel) return;
    const outEl = document.getElementById('panel-' + _activePanel);
    const inEl  = document.getElementById('panel-' + panel);
    if (!outEl || !inEl) return;

    // Direction: register is "right", login is "left", forgot is "right"
    const dir = (panel === 'register' || panel === 'forgot') ? 1 : -1;

    if (window.gsap) {
        gsap.to(outEl, {
            opacity: 0, x: -28 * dir, duration: 0.22, ease: 'power2.in',
            onComplete: () => {
                outEl.style.display = 'none';
                outEl.style.opacity = '';
                outEl.style.transform = '';
                inEl.style.display = 'block';
                gsap.fromTo(inEl,
                    { opacity: 0, x: 28 * dir },
                    { opacity: 1, x: 0, duration: 0.35, ease: 'power3.out' }
                );
            }
        });
    } else {
        outEl.style.display = 'none';
        inEl.style.display = 'block';
    }
    _activePanel = panel;

    // Sync tab active states
    document.querySelectorAll('.tab-login').forEach(b => b.classList.toggle('active', panel === 'login'));
    document.querySelectorAll('.tab-register').forEach(b => b.classList.toggle('active', panel === 'register'));
}

function googleGirisYap() {
    // OAuth callback'ten dönen token'ı yakala (varsa)
    const params = new URLSearchParams(window.location.search);
    const oauthError = params.get('oauth_error');
    if (oauthError) {
        const msgs = {
            cancelled:      'Google girişi iptal edildi.',
            token_failed:   'Google doğrulama başarısız. Tekrar deneyin.',
            userinfo_failed:'Google bilgileri alınamadı. Tekrar deneyin.',
            no_email:       'Google hesabından e-posta alınamadı.',
        };
        showToast(msgs[oauthError] || 'Google girişi başarısız.', 'error');
        return;
    }
    // Google OAuth sayfasına yönlendir
    window.location.href = '/auth/google/login';
}

function selectPlan(plan) {
  selectedPlan = plan;
  // Support both old .plan-card and new .plan-chip
  document.querySelectorAll('.plan-card, .plan-chip').forEach(c => {
    c.classList.remove('selected');
    c.setAttribute('aria-checked', 'false');
  });
  const card = document.getElementById('plan-' + plan);
  if (card) {
    card.classList.add('selected');
    card.setAttribute('aria-checked', 'true');
    if (window.gsap) {
      gsap.fromTo(card, { scale: 0.97 }, { scale: 1, duration: 0.3, ease: 'back.out(2)' });
    }
  }
}

// --- KAYIT SİSTEMİ ---
async function kayitOl() {
    console.log('Kayıt başladı, seçili plan:', selectedPlan); // debug
    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const pass = document.getElementById('regPass').value;
    const passConfirm = document.getElementById('regPassConfirm').value;
    const btn = document.getElementById('regBtn');
    const msg = document.getElementById('regMsg');

    if (!name || !email || !pass) {
        msg.innerHTML = '<div class="msg-error">Tüm alanları doldurun.</div>';
        return;
    }
    if (pass.length < 8) {
        showToast('Şifre en az 8 karakter olmalı.', 'warning');
        return;
    }
    if (pass !== passConfirm) {
        msg.innerHTML = '<div class="msg-error">Şifreler eşleşmiyor.</div>';
        return;
    }

    btn.innerText = '⏳ Kaydediliyor...';
    btn.disabled = true;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password: pass, full_name: name, plan: selectedPlan })
        });
        const data = await response.json();

        if (response.ok) {
            msg.innerHTML = '<div class="msg-success">✅ Hesabınız oluşturuldu! Giriş yapabilirsiniz.</div>';
            console.log('Kayıt OK, plan:', selectedPlan);
            if (selectedPlan === 'pro' || selectedPlan === 'max') {
                setTimeout(() => {
                    odemePaneliAc(selectedPlan);
                }, 1000);
            }
            setTimeout(() => {
                switchPanel('login');
                document.getElementById('loginEmail').value = email;
            }, 1500);
        } else {
            msg.innerHTML = `<div class="msg-error">${data.detail || 'Kayıt başarısız.'}</div>`;
        }
    } catch (e) {
        msg.innerHTML = '<div class="msg-error">Sunucu bağlantı hatası.</div>';
    }

    btn.innerText = 'Hesabı Oluştur';
    btn.disabled = false;
}

// --- ŞİFRE SIFIRLAMA ---
async function sifreSifirla() {
    const email = document.getElementById('forgotEmail').value.trim();
    if (!email) { document.getElementById('forgotMsg').innerHTML = '<div class="msg-error">E-posta giriniz.</div>'; return; }
    const btn = document.getElementById('forgotBtn');
    btn.disabled = true; btn.textContent = 'Gönderiliyor...';
    try {
        const res = await fetch('/sifre-sifirla', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email }) });
        const data = await res.json();
        if (res.ok) {
            document.getElementById('forgot-step1').style.display = 'none';
            document.getElementById('forgot-step2').style.display = 'block';
        } else {
            document.getElementById('forgotMsg').innerHTML = `<div class="msg-error">${data.detail}</div>`;
        }
    } catch(e) {
        document.getElementById('forgotMsg').innerHTML = '<div class="msg-error">Bağlantı hatası.</div>';
    } finally {
        btn.disabled = false; btn.textContent = 'Kod Gönder';
    }
}

async function sifreGuncelle() {
    const kod = document.getElementById('resetKod').value.trim();
    const yeniSifre = document.getElementById('resetYeniSifre').value;
    const tekrar = document.getElementById('resetYeniSifreTekrar').value;
    if (kod.length !== 6) { document.getElementById('resetMsg').innerHTML = '<div class="msg-error">6 haneli kodu girin.</div>'; return; }
    if (yeniSifre.length < 8) { document.getElementById('resetMsg').innerHTML = '<div class="msg-error">Şifre en az 8 karakter.</div>'; return; }
    if (yeniSifre !== tekrar) { document.getElementById('resetMsg').innerHTML = '<div class="msg-error">Şifreler eşleşmiyor.</div>'; return; }
    try {
        const res = await fetch('/sifre-guncelle', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: kod, yeni_sifre: yeniSifre }) });
        const data = await res.json();
        if (res.ok) {
            document.getElementById('resetMsg').innerHTML = '<div class="msg-success">✅ Şifreniz güncellendi!</div>';
            setTimeout(() => switchPanel('login'), 2000);
        } else {
            document.getElementById('resetMsg').innerHTML = `<div class="msg-error">${data.detail}</div>`;
        }
    } catch(e) {
        document.getElementById('resetMsg').innerHTML = '<div class="msg-error">Bağlantı hatası.</div>';
    }
}

// --- PROFİL ---
let aktifKullanici = null;

function updatePlanLabel() {
  const plan = (document.getElementById('planBadge')?.innerText || '').toLowerCase();
  const label = document.getElementById('planLabel');
  if (!label) return;

  if (plan.includes('admin') || window.isAdmin) {
    label.innerText = 'Admin';
    label.style.color = '#ef4444';
  } else if (plan.includes('max')) {
    label.innerText = 'Max';
    label.style.color = '#f59e0b';
  } else if (plan.includes('pro')) {
    label.innerText = 'Pro';
    label.style.color = '#f97316';
  } else {
    label.innerText = 'Free';
    label.style.color = '#8b8fa8';
  }
}

function openProfile() {
    if (!aktifKullanici) return;
    const modal = document.getElementById('profileModal');
    modal.style.display = 'flex';

    const initials = aktifKullanici.full_name ? aktifKullanici.full_name.charAt(0).toUpperCase() : 'U';
    document.getElementById('profileAvatar').innerText = initials;
    document.getElementById('profileName').innerText = aktifKullanici.full_name || 'Kullanıcı';
    document.getElementById('profileEmail').innerText = aktifKullanici.email || '';
    document.getElementById('profilePlan').innerText = aktifKullanici.plan === 'pro' ? '⚡ PRO PLAN' : 'ÜCRETSİZ PLAN';

    fetch('/rapor_listesi').then(r => r.json()).then(data => {
        document.getElementById('statRapor').innerText = data.raporlar ? data.raporlar.length : 0;
    }).catch(() => {});
    kullanımDurumuGoster();
}

function closeProfile() {
    document.getElementById('profileModal').style.display = 'none';
}

// --- 📄 PDF İNDİR ---
async function pdfIndir() {
    const analiz = document.getElementById('analizMetni') ? document.getElementById('analizMetni').innerText : "";
    const ingilizce = document.getElementById('englishMetni') ? document.getElementById('englishMetni').innerText : "";
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : "Sivas";
    const hava = (document.getElementById('temp') ? document.getElementById('temp').innerText : "") + " " +
                 (document.getElementById('condition') ? document.getElementById('condition').innerText : "");

    if (!analiz) {
        alert(aktifDil === 'tr' ? "Önce bir analiz yapın!" : "Please run an analysis first!");
        return;
    }

    const btn = event.target;
    btn.innerText = aktifDil === 'tr' ? "⏳ Hazırlanıyor..." : "⏳ Preparing...";
    btn.disabled = true;

    try {
        const response = await fetch('/pdf-indir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                kullanici_adi: aktifKullanici ? aktifKullanici.full_name : "Mühendis",
                sehir: sehir,
                hava: hava,
                analiz: analiz,
                ingilizce: ingilizce,
                dil: aktifDil
            })
        });

        if (!response.ok) throw new Error('PDF oluşturulamadı');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `BuildingAI_Rapor_${new Date().toISOString().slice(0,10)}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        btn.innerText = aktifDil === 'tr' ? "✅ PDF İndirildi!" : "✅ PDF Downloaded!";
        setTimeout(() => {
            btn.innerText = aktifDil === 'tr' ? "📄 PDF Rapor İndir" : "📄 Download PDF Report";
            btn.disabled = false;
        }, 2000);
    } catch (e) {
        alert(aktifDil === 'tr' ? "PDF oluşturulurken hata oluştu." : "Error creating PDF.");
        btn.innerText = aktifDil === 'tr' ? "📄 PDF Rapor İndir" : "📄 Download PDF Report";
        btn.disabled = false;
    }
}

function cikisYap() {
    aktifKullanici = null;
    localStorage.removeItem('bai_token');
    localStorage.removeItem('bai_user');
    closeProfile();
    document.getElementById('mainApp').style.display = 'none';
    document.getElementById('navSidebar').style.display = 'none';
    document.getElementById('topHeader').style.display = 'none';
    document.getElementById('auth-overlay').style.display = 'flex';
    document.getElementById('loginEmail').value = '';
    document.getElementById('loginPass').value = '';
    switchPanel('login');
}

// --- 🎤 SESLİ RAPOR ---
let sesliRaporMediaRecorder = null;
let sesliRaporChunks = [];

async function sesliRaporBaslat() {
    const btn = document.getElementById('sesliRaporBtn');

    if (sesliRaporMediaRecorder && sesliRaporMediaRecorder.state === 'recording') {
        sesliRaporMediaRecorder.stop();
        btn.classList.remove('active');
        const icon = btn.querySelector('.qa-icon'); if (icon) icon.textContent = '🎤';
        const label = btn.querySelector('.qa-label'); if (label) label.textContent = 'Sesli Rapor';
        return;
    }

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        sesliRaporChunks = [];
        sesliRaporMediaRecorder = new MediaRecorder(stream);

        sesliRaporMediaRecorder.ondataavailable = e => { if (e.data.size > 0) sesliRaporChunks.push(e.data); };

        sesliRaporMediaRecorder.onstop = async () => {
            stream.getTracks().forEach(t => t.stop());
            const blob = new Blob(sesliRaporChunks, { type: 'audio/webm' });
            const reader = new FileReader();
            reader.onload = async () => {
                const base64 = reader.result.split(',')[1];
                const resBox = document.getElementById('result');
                resBox.innerHTML = '<div class="res-title">🎤 Ses işleniyor...</div><div class="res-detail">Yapay zeka sesinizi analiz ediyor...</div>';
                try {
                    const hava = (document.getElementById('condition')?.innerText || '');
                    const sesliToken = localStorage.getItem('bai_token') || '';
                    const res = await fetch('/sesli-rapor', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ audio_base64: base64, hava, dil: aktifDil, token: sesliToken })
                    });
                    if (res.status === 429) {
                        const err = await res.json();
                        resBox.innerHTML = `<div style="text-align:center; padding:20px;"><div style="font-size:2rem; margin-bottom:10px;">⚡</div><div style="color:#e67e22; font-size:1.1rem; font-weight:bold; margin-bottom:10px;">Limit Doldu!</div><div style="color:#aaa; margin-bottom:20px;">${err.detail}</div><button onclick="proYukselt()" style="background:#e67e22; color:white; border:none; padding:12px 30px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:1rem;">⚡ Pro'ya Geç — 10$/ay</button></div>`;
                        return;
                    }
                    const data = await res.json();
                    if (res.ok) {
                        resBox.innerHTML = `
                            <div class="res-title">📋 Sesli Rapor Oluşturuldu</div>
                            <div id="analizMetni" style="color:#1E293B; font-size:0.95rem; line-height:1.7; margin-top:10px;">${markdownToHtml(data.rapor)}</div>
                            <button onclick="gunlukRaporuKaydet()" style="margin-top:10px; padding:12px 20px; background:#2ecc71; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">💾 Raporu Kaydet</button>
                        `;
                    } else {
                        resBox.innerHTML = `<div class="res-title" style="color:#e74c3c;">Hata</div><div class="res-detail">${data.detail}</div>`;
                    }
                } catch(e) {
                    resBox.innerHTML = '<div class="res-title" style="color:#e74c3c;">Hata</div><div class="res-detail">Ses işlenemedi.</div>';
                }
            };
            reader.readAsDataURL(blob);
        };

        sesliRaporMediaRecorder.start();
        btn.classList.add('active');
        const icon = btn.querySelector('.qa-icon'); if (icon) icon.textContent = '⏹️';
        const label = btn.querySelector('.qa-label'); if (label) label.textContent = 'Durdur';
    } catch(e) {
        alert('Mikrofon erişimi reddedildi.');
    }
}

// --- 📝 GÜNLÜK RAPOR ---
function gunlukRaporAc() {
    const modal = document.getElementById('gunlukRaporModal');
    if (!modal) return;
    modal.style.display = 'flex';
    // Set today's date
    const tarihEl = document.getElementById('grTarih');
    if (tarihEl && !tarihEl.value) {
        tarihEl.value = new Date().toISOString().split('T')[0];
    }
}

function gunlukRaporKapat() {
    document.getElementById('gunlukRaporModal').style.display = 'none';
}

function grIsgDegisti(el) {
    const label = document.getElementById('grIsgLabel');
    const select = document.getElementById('grIsg');
    if (el.checked) {
        if (label) label.textContent = 'Uygun';
        if (select) select.value = 'iyi';
    } else {
        if (label) label.textContent = 'Uygun Değil';
        if (select) select.value = 'orta';
    }
}

async function gunlukRaporOlustur() {
    const tarih = document.getElementById('grTarih').value;
    const isci = document.getElementById('grIsci').value;
    const yapilanlar = document.getElementById('grYapilanlar').value.trim();
    const sorunlar = document.getElementById('grSorunlar').value.trim();
    const yarin = document.getElementById('grYarin').value.trim();
    const isg = document.getElementById('grIsg').value;
    const sonucDiv = document.getElementById('gunlukRaporSonuc');

    if (!yapilanlar) {
        sonucDiv.innerHTML = '<div style="color:#DC2626; font-size:0.82rem; padding:8px 0;">Yapılan işler alanını doldurun.</div>';
        return;
    }

    const veriler = `Tarih: ${tarih || 'Bugün'}, İşçi sayısı: ${isci || 'Belirtilmedi'}, Yapılanlar: ${yapilanlar}, Sorunlar: ${sorunlar || 'Yok'}, Yarın: ${yarin || 'Belirtilmedi'}, İSG durumu: ${isg}`;
    const hava = (document.getElementById('condition')?.innerText || '');

    sonucDiv.innerHTML = '<div style="color:#64748B; font-size:0.82rem; padding:8px 0; text-align:center;">Yapay zeka rapor oluşturuyor...</div>';

    // Disable button
    const btn = document.querySelector('#gunlukRaporModal button[onclick="gunlukRaporOlustur()"]');
    if (btn) { btn.disabled = true; btn.style.opacity = '0.6'; }

    try {
        const token = localStorage.getItem('bai_token');
        const res = await fetch('/gunluk-rapor-olustur', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ veriler, hava, dil: aktifDil, token })
        });
        if (res.status === 429) {
            const data = await res.json();
            sonucDiv.innerHTML = `<div style="text-align:center; padding:16px; background:#FEF3C7; border-radius:10px; font-size:0.85rem; color:#92400E;">${data.detail}<br><button onclick="proYukselt()" style="margin-top:10px; background:#0D1117; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; font-weight:700; font-size:0.82rem;">Pro'ya Geç</button></div>`;
            return;
        }
        const data = await res.json();
        if (res.ok) {
            document.getElementById('result').innerHTML = `
                <div class="res-title">📋 Günlük Rapor</div>
                <div id="analizMetni" style="color:#1E293B; font-size:0.95rem; line-height:1.7; margin-top:10px;">${markdownToHtml(data.rapor)}</div>
            `;
            sonucDiv.innerHTML = `
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:14px; font-size:0.82rem; color:#374151; line-height:1.65; max-height:200px; overflow-y:auto;">${markdownToHtml(data.rapor)}</div>
                <div style="display:flex; gap:8px; margin-top:10px;">
                    <button onclick="gunlukRaporuKaydet(); gunlukRaporKapat();" style="flex:1; padding:10px; background:#16A34A; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:700; font-size:0.82rem;">Arşive Kaydet</button>
                    <button onclick="gunlukRaporKapat()" style="flex:1; padding:10px; background:#F1F5F9; color:#374151; border:none; border-radius:10px; cursor:pointer; font-size:0.82rem;">Kapat</button>
                </div>
            `;
        } else {
            sonucDiv.innerHTML = `<div style="color:#DC2626; font-size:0.82rem;">${data.detail}</div>`;
        }
    } catch(e) {
        sonucDiv.innerHTML = '<div style="color:#DC2626; font-size:0.82rem;">Bağlantı hatası.</div>';
    } finally {
        if (btn) { btn.disabled = false; btn.style.opacity = '1'; }
    }
}

// --- 📋 PLAN SİSTEMİ ---
const PLAN_BILGI = {
    pro: {
        ad: 'PRO', renk: '#6366f1', icon: '⚡', fiyat: '650 TL/ay',
        ozellikler: ['Sınırsız AI Sorgu', '20 Kamera/Hafta', '5 Sesli Rapor/Gün', 'Stok Takibi', 'Fiyat Takibi', 'Deprem Analizi'],
    },
    max: {
        ad: 'MAX', renk: '#f1c40f', icon: '👑', fiyat: '1.990 TL/ay',
        ozellikler: ["Her şey PRO'da +", 'Sınırsız Kamera', 'Haftalık Rapor', 'Şantiye Yönetimi', 'Filigrансыз PDF', 'Öncelikli Destek'],
    },
};
const OZELLIK_ACIKLAMA = {
    stok:            { ad: 'Stok Takibi',             icon: '📦', gereken: 'pro' },
    deprem_analiz:   { ad: 'Deprem Analizi',           icon: '🌍', gereken: 'pro' },
    fiyat_takip:     { ad: 'Fiyat Takibi',             icon: '📊', gereken: 'pro' },
    santiye:         { ad: 'Şantiye Dashboard',        icon: '🏗️', gereken: 'pro' },
    haftalik_rapor:  { ad: 'Haftalık Rapor',           icon: '📈', gereken: 'max' },
    kamera_gelismis: { ad: 'Gelişmiş Kamera Limiti',   icon: '📷', gereken: 'max' },
};

function planKilit(ozellik) {
    const el = document.getElementById('planKilitModal');
    if (!el) return;
    const oz = OZELLIK_ACIKLAMA[ozellik] || { ad: ozellik, icon: '🔒', gereken: 'pro' };
    const hedefPlan = oz.gereken;
    const pb = PLAN_BILGI[hedefPlan] || PLAN_BILGI.pro;
    const ozellikListesi = pb.ozellikler.map(o => `<li style="padding:4px 0; color:#ccc; font-size:0.9rem;">✅ ${o}</li>`).join('');
    el.innerHTML = `
        <div style="background:#1a1a2e; border:1px solid ${pb.renk}; border-radius:20px; padding:36px 32px; max-width:420px; width:90%; position:relative; text-align:center;">
            <button onclick="planKilitKapat()" style="position:absolute; top:14px; right:16px; background:none; border:none; color:#aaa; font-size:1.4rem; cursor:pointer;">✖</button>
            <div style="font-size:3rem; margin-bottom:12px;">🔒</div>
            <h2 style="color:white; margin:0 0 6px 0; font-size:1.3rem;">${oz.icon} ${oz.ad}</h2>
            <p style="color:#aaa; margin:0 0 16px 0; font-size:0.9rem;">Bu özelliği kullanmak için yükseltme gerekiyor.</p>
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:18px; margin-bottom:20px; text-align:left;">
                <div style="font-size:0.85rem; color:#aaa; margin-bottom:8px; text-align:center;">
                    <span style="color:${pb.renk}; font-weight:700; font-size:1.1rem;">${pb.icon} ${pb.ad} PLAN</span>
                    &nbsp;— <b style="color:white;">${pb.fiyat}</b> ile açılır
                </div>
                <ul style="list-style:none; padding:0; margin:0;">${ozellikListesi}</ul>
            </div>
            <button onclick="odemePaneliAc('${hedefPlan}')" style="width:100%; padding:14px; background:linear-gradient(135deg,${pb.renk},${pb.renk}cc); border:none; color:${hedefPlan === 'max' ? '#111' : 'white'}; border-radius:14px; cursor:pointer; font-weight:700; font-size:1rem; margin-bottom:10px; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
                🚀 ${pb.icon} ${pb.ad} Planına Geç
            </button>
            <button onclick="planKilitKapat()" style="width:100%; padding:10px; background:none; border:1px solid #333; color:#777; border-radius:14px; cursor:pointer; font-size:0.9rem; transition:0.3s;">
                Belki Sonra
            </button>
        </div>`;
    el.style.cssText = 'display:flex; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:10000; align-items:center; justify-content:center;';
}
function planKilitKapat() {
    const el = document.getElementById('planKilitModal');
    if (el) { el.style.display = 'none'; el.innerHTML = ''; }
}

function odemePaneliAc(plan) {
    plan = plan || 'pro';
    planKilitKapat();
    const pb = PLAN_BILGI[plan] || PLAN_BILGI.pro;
    const el = document.getElementById('odemeModal');
    if (!el) return;
    el.innerHTML = `
        <div style="background:#1a1a2e; border:1px solid ${pb.renk}; border-radius:20px; padding:32px; max-width:460px; width:90%; position:relative;">
            <button onclick="odemeModalKapat()" style="position:absolute; top:14px; right:16px; background:none; border:none; color:#aaa; font-size:1.4rem; cursor:pointer;">✖</button>
            <h2 style="color:${pb.renk}; margin:0 0 4px 0; font-size:1.35rem;">${pb.icon} ${pb.ad} Plana Geç</h2>
            <p style="color:#aaa; font-size:0.88rem; margin:0 0 18px 0;">IBAN'a ödeme yapın, formu doldurun — 24 saat içinde aktifleştireceğiz.</p>
            <div style="background:#111; border:1px solid #333; border-radius:10px; padding:12px; display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                <span style="color:#f1c40f; font-family:monospace; font-size:0.88rem; word-break:break-all;">TR80 0001 0090 1095 7865 2050 01</span>
                <button onclick="navigator.clipboard.writeText('TR80 0001 0090 1095 7865 2050 01').then(()=>{document.getElementById('odemeModalMsg').textContent='✅ Kopyalandı!';document.getElementById('odemeModalMsg').style.color='#2ecc71';})" style="background:${pb.renk}; border:none; color:${plan === 'max' ? '#111' : 'white'}; border-radius:8px; padding:5px 10px; cursor:pointer; font-size:0.78rem; white-space:nowrap; margin-left:8px;">Kopyala</button>
            </div>
            <p style="color:#555; font-size:0.8rem; margin:0 0 4px 0;">Ad: Mehmet Akif Erdemir</p>
            <p style="color:#aaa; font-size:0.85rem; margin:0 0 16px 0;">Fiyat: <b style="color:white;">${pb.fiyat}</b></p>
            <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:16px;">
                <input type="text" id="odemeAdSoyad" placeholder="Ad Soyad *" style="background:#111; border:1px solid #333; border-radius:10px; padding:11px 14px; color:white; font-size:0.9rem; outline:none;">
                <input type="text" id="odemeTelefon" placeholder="Telefon (opsiyonel)" style="background:#111; border:1px solid #333; border-radius:10px; padding:11px 14px; color:white; font-size:0.9rem; outline:none;">
                <textarea id="odemeAciklama2" placeholder="Açıklama — havale açıklamanıza yazdığınız bilgiyi yazın" rows="2" style="background:#111; border:1px solid #333; border-radius:10px; padding:11px 14px; color:white; font-size:0.9rem; resize:none; outline:none;"></textarea>
            </div>
            <button onclick="odemeBildir('${plan}')" style="width:100%; padding:14px; background:linear-gradient(135deg,#27ae60,#2ecc71); border:none; color:white; border-radius:14px; cursor:pointer; font-weight:700; font-size:1rem; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
                ✅ Ödemeyi Yaptım, Bildiri Gönder
            </button>
            <div id="odemeModalMsg" style="margin-top:10px; text-align:center; font-size:0.88rem;"></div>
        </div>`;
    el.style.cssText = 'display:flex; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:10001; align-items:center; justify-content:center;';
}
function odemeModalKapat() {
    const el = document.getElementById('odemeModal');
    if (el) { el.style.display = 'none'; el.innerHTML = ''; }
}
async function odemeBildir(plan) {
    const token = localStorage.getItem('bai_token');
    if (!token) return;
    plan = plan || 'pro';
    const ad_soyad = document.getElementById('odemeAdSoyad').value.trim();
    const telefon  = document.getElementById('odemeTelefon').value.trim();
    const aciklama = document.getElementById('odemeAciklama2').value.trim();
    const msgEl    = document.getElementById('odemeModalMsg');
    if (!ad_soyad) { msgEl.textContent = '❗ Ad soyad zorunlu.'; msgEl.style.color='#e74c3c'; return; }
    msgEl.textContent = '⏳ Gönderiliyor...'; msgEl.style.color='#aaa';
    try {
        const res = await fetch('/odeme-bildir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token, plan, ad_soyad, telefon, aciklama })
        });
        const data = await res.json();
        if (res.ok) {
            msgEl.textContent = '✅ ' + data.mesaj;
            msgEl.style.color = '#2ecc71';
        } else {
            msgEl.textContent = '❌ ' + (data.detail || 'Bir hata oluştu.');
            msgEl.style.color = '#e74c3c';
        }
    } catch(e) {
        msgEl.textContent = '❌ Bağlantı hatası.';
        msgEl.style.color = '#e74c3c';
    }
}
function planBadgeHTML(plan) {
    if (plan === 'admin') return '<span style="background:rgba(231,76,60,0.15); border:1px solid #e74c3c; color:#e74c3c; border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:700;">🛡️ ADMİN</span>';
    if (plan === 'max')   return '<span style="background:rgba(241,196,15,0.15); border:1px solid #f1c40f; color:#f1c40f; border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:700;">👑 MAX</span>';
    if (plan === 'pro')   return '<span style="background:rgba(99,102,241,0.15); border:1px solid #6366f1; color:#6366f1; border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:700;">⚡ PRO</span>';
    return '<span style="background:rgba(230,126,34,0.15); border:1px solid #e67e22; color:#e67e22; border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:700;">🆓 ÜCRETSİZ</span>';
}

// --- 📊 KULLANIM DURUMU & PRO ---
async function kullanımDurumuGoster() {
    const token = localStorage.getItem('bai_token');
    if (!token) return;
    try {
        const res = await fetch(`/kullanim-durumu?token=${token}`);
        const data = await res.json();
        if (res.ok) {
            window._kullaniciPlan = data.plan;
            window._planOzellikler = data.plan_ozellikleri || {};
            const k = data.kullanim;
            const sorEl = document.getElementById('statSorgu');
            if (sorEl) {
                const sorLimit = k.sor.limit;
                sorEl.textContent = sorLimit === null ? '∞' : `${k.sor.kullanilan}/${sorLimit}`;
            }

            // ── KPI Dashboard Cards ──
            function setKpi(valId, barId, used, limit, labelFn) {
                const vEl = document.getElementById(valId);
                const bEl = document.getElementById(barId);
                if (!vEl) return;
                const pct = limit === null ? 0 : Math.min(100, Math.round((used / limit) * 100));
                vEl.textContent = limit === null ? `${used} / ∞` : (labelFn ? labelFn(used, limit) : `${used} / ${limit}`);
                if (bEl) setTimeout(() => bEl.style.width = (limit === null ? 10 : pct) + '%', 100);
            }
            setKpi('kpiAiVal', 'kpiAiBar', k.sor.kullanilan, k.sor.limit);
            setKpi('kpiKameraVal', 'kpiKameraBar', k.kamera.kullanilan, k.kamera.limit);
            setKpi('kpiRaporVal', 'kpiRaporBar', k.gunluk_rapor.kullanilan, k.gunluk_rapor.limit);
            const planEl = document.getElementById('kpiPlanVal');
            if (planEl) {
                const planLabels = {free:'Ücretsiz', pro:'⚡ Pro', max:'👑 Max', admin:'🛡️ Admin'};
                planEl.textContent = planLabels[data.plan] || data.plan;
                planEl.style.color = data.plan === 'max' ? '#f1c40f' : data.plan === 'pro' ? '#818cf8' : data.plan === 'admin' ? '#22c55e' : '#94a3b8';
            }
            const badge = document.getElementById('profilePlan');
            if (badge) badge.innerHTML = planBadgeHTML(data.plan);
            const topBadge = document.getElementById('planBadge');
            if (topBadge) {
                if (data.plan === 'admin') topBadge.innerHTML = '🛡️ ADMIN';
                else if (data.plan === 'max') topBadge.innerHTML = '👑 MAX';
                else if (data.plan === 'pro') topBadge.innerHTML = '⚡ PRO';
                else topBadge.innerHTML = 'FREE';
            }
            updatePlanLabel();
            const kayitliRol = localStorage.getItem('bai_rol');
            if (kayitliRol) navSidebarGuncelle(kayitliRol);
        }
    } catch(e) {}
}

function proYukselt(aciklama) {
    const msg = aciklama || localStorage.getItem('bai_user') && JSON.parse(localStorage.getItem('bai_user') || '{}').email || '';
    const el = document.getElementById('odemeAciklama');
    if (el) el.value = msg;
    document.getElementById('odemeMsg').textContent = '';
    document.getElementById('proModal').style.display = 'flex';
}

function proModalKapat() {
    document.getElementById('proModal').style.display = 'none';
}

function ibanKopyala() {
    const iban = document.getElementById('ibanText').textContent.trim();
    navigator.clipboard.writeText(iban).then(() => {
        document.getElementById('odemeMsg').textContent = '✅ IBAN kopyalandı!';
        document.getElementById('odemeMsg').style.color = '#2ecc71';
    }).catch(() => {
        document.getElementById('odemeMsg').textContent = 'Kopyalama başarısız. Lütfen manuel kopyalayın.';
        document.getElementById('odemeMsg').style.color = '#e74c3c';
    });
}

async function odemeBildirimi() {
    const token = localStorage.getItem('bai_token');
    if (!token) return;
    const msgEl = document.getElementById('odemeMsg');
    msgEl.textContent = '⏳ Gönderiliyor...';
    msgEl.style.color = '#aaa';
    try {
        const res = await fetch('/odeme-bildirimi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token, plan: selectedPlan || 'pro' })
        });
        const data = await res.json();
        if (res.ok) {
            msgEl.textContent = '✅ ' + data.mesaj;
            msgEl.style.color = '#2ecc71';
        } else {
            msgEl.textContent = '❌ ' + (data.detail || 'Bir hata oluştu.');
            msgEl.style.color = '#e74c3c';
        }
    } catch(e) {
        msgEl.textContent = '❌ Bağlantı hatası.';
        msgEl.style.color = '#e74c3c';
    }
}

// --- 🗺️ NAV SIDEBAR ---
let navCollapsed = false;

function toggleNavSidebar() {
    navCollapsed = !navCollapsed;
    const nav = document.getElementById('navSidebar');
    const header = document.getElementById('topHeader');
    const mainContent = document.getElementById('mainContent');
    const btn = document.getElementById('collapseBtn');
    nav.classList.toggle('collapsed', navCollapsed);
    header.classList.toggle('nav-collapsed', navCollapsed);
    mainContent.classList.toggle('nav-collapsed', navCollapsed);
    btn.textContent = navCollapsed ? '▶' : '◀';
}

function toggleMobileNav() {
    document.getElementById('navSidebar').classList.add('mobile-open');
    document.getElementById('navOverlay').classList.add('active');
}

function closeMobileNav() {
    const overlay = document.getElementById('sidebarOverlay');
    const sidebar = document.getElementById('sidebar');
    if (overlay) overlay.style.display = 'none';
    if (sidebar) sidebar.classList.remove('open');
}

function toggleMobileMenu() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('mobile-overlay');
  const btn = document.getElementById('hamburger-btn');
  const isOpen = sidebar.classList.contains('mobile-open');

  if (isOpen) {
    closeMobileMenu();
  } else {
    // Sidebar'ı aç
    sidebar.style.cssText = `
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      width: 80% !important;
      max-width: 280px !important;
      height: 100vh !important;
      z-index: 9999 !important;
      background: rgba(8, 18, 40, 0.98) !important;
      backdrop-filter: blur(20px) !important;
      -webkit-backdrop-filter: blur(20px) !important;
      overflow-y: auto !important;
      flex-direction: column !important;
      display: flex !important;
      padding-top: 20px !important;
      border-right: 1px solid rgba(255,255,255,0.1) !important;
      pointer-events: auto !important;
    `;
    sidebar.classList.add('mobile-open');

    if (overlay) {
      overlay.style.cssText = `
        display: block !important;
        position: fixed !important;
        top: 0 !important;
        left: 280px !important;
        width: calc(100% - 280px) !important;
        height: 100% !important;
        background: rgba(0,0,0,0.7) !important;
        z-index: 150 !important;
        pointer-events: auto !important;
      `;
    }
    if (btn) btn.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileMenu() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('mobile-overlay');
  const btn = document.getElementById('hamburger-btn');

  if (sidebar) {
    sidebar.style.cssText = '';
    sidebar.classList.remove('mobile-open');
  }
  if (overlay) {
    overlay.style.cssText = 'display: none !important;';
    overlay.classList.remove('active');
  }
  if (btn) btn.classList.remove('open');
  document.body.style.overflow = '';
}

function toggleRaporlarSub() {
  const sub = document.getElementById('raporlarSub');
  const btn = document.getElementById('raporlarBtn');
  const analizSub = document.getElementById('analizSub');

  // Analiz'i kapat
  if (analizSub) analizSub.style.display = 'none';
  document.querySelectorAll('.quick-btn').forEach(b => {
    if (b !== btn) b.classList.remove('active');
  });

  if (sub.style.display === 'flex') {
    sub.style.display = 'none';
    btn.classList.remove('active');
  } else {
    sub.style.display = 'flex';
    btn.classList.add('active');
  }
}

function guvenlikAc() {
  document.querySelectorAll('.quick-btn').forEach(b => b.classList.remove('active'));
  document.querySelector('.quick-btn[onclick="guvenlikAc()"]')?.classList.add('active');

  const modal = document.getElementById('guvenlikModal');
  if (modal) {
    modal.style.display = 'flex';
    // Set date
    const tarih = document.getElementById('guvenlikTarih');
    if (tarih) tarih.textContent = new Date().toLocaleDateString('tr-TR');
    // Load santiyeler into dropdown
    guvenlikSantiyelerYukle();
    // Render acil personel from localStorage
    acilPersonelRender();
    return;
  }
}

async function guvenlikSantiyelerYukle() {
  const token = localStorage.getItem('bai_token');
  const sel = document.getElementById('guvenlikSantiye');
  if (!sel) return;
  try {
    const res = await fetch(`/santiyeler?token=${token}`);
    const data = await res.json();
    const santiyeler = data.santiyeler || [];
    sel.innerHTML = '<option value="">Seçin...</option>' +
      santiyeler.map(s => `<option value="${s.id}">${s.ad}</option>`).join('');
  } catch(e) {}
}

function guvenlikSantiyeDegisti() {
  const sel = document.getElementById('guvenlikSantiye');
  const badge = document.getElementById('guvenlikDurumBadge');
  const sorumlu = document.getElementById('guvenlikSorumlu');
  if (!sel || !sel.value) return;
  const opt = sel.options[sel.selectedIndex];
  // Try to get sorumlu from santiye data (available from page render)
  if (sorumlu) sorumlu.textContent = '--';
  if (badge) { badge.textContent = 'Şantiye Durumu: Aktif'; badge.style.background = '#DCFCE7'; badge.style.color = '#16A34A'; }
}

function analizAc() {
  const sub = document.getElementById('analizSub');
  const btn = document.querySelector('.quick-btn[onclick="analizAc()"]');
  const raporSub = document.getElementById('raporlarSub');
  const raporBtn = document.getElementById('raporlarBtn');

  // Raporlar'ı kapat
  if (raporSub) raporSub.style.display = 'none';
  if (raporBtn) raporBtn.classList.remove('active');

  if (sub.style.display === 'flex') {
    sub.style.display = 'none';
    if (btn) btn.classList.remove('active');
  } else {
    sub.style.display = 'flex';
    if (btn) btn.classList.add('active');
  }
}

function setActiveNav(page) {
    document.querySelectorAll('.nav-item[id^="nav-"]').forEach(el => el.classList.remove('active'));
    const el = document.getElementById('nav-' + page);
    if (el) el.classList.add('active');
}

const PAGE_TITLES = {
    home: '🏠 Ana Sayfa',
    kamera: '📷 Kamera Analizi',
    hesaplama: '🧮 Hesaplama',
    arsiv: '📁 Arşiv',
    gunluk: '📝 Günlük Rapor',
    sesli: '🎤 Sesli Rapor',
};

function navGit(page) {
    closeMobileMenu();
    // Ayarlar sayfası açıksa kapat
    const _ap = document.getElementById('ayarlarPage');
    if (_ap) _ap.style.display = 'none';
    setActiveNav(page);
    const titleEl = document.getElementById('headerTitle');
    if (titleEl) titleEl.textContent = PAGE_TITLES[page] || '';
    const tbTitle = document.getElementById('tbPageTitle');
    if (tbTitle) tbTitle.textContent = PAGE_TITLES[page] || '';
    // Close mobile nav if open
    closeMobileNav();
    // Perform action
    if (page === 'kamera') kameraPageAc();
    else if (page === 'hesaplama') toggleSidebar();
    else if (page === 'arsiv') arsivPageAc();
    else if (page === 'gunluk') gunlukRaporAc();
    else if (page === 'sesli') sesliRaporBaslat();
    else if (page === 'fiyat') fiyatPageAc();
    else if (page === 'stok') stokPageAc();
    else if (page === 'deprem') depremModalAc();
    else if (page === 'santiye') santiyePageAc();
    // home: kapat diğer sayfaları
    else { santiyePageKapat(); fiyatPageKapat(); stokPageKapat(); kameraPageKapat(); arsivKapat(); window.scrollTo({ top: 0, behavior: 'smooth' }); }
}

// --- 📊 FİYAT TAKİBİ ---
let fiyatGrafigi = null;

function fiyatModalAc() {
    document.getElementById('fiyatModal').style.display = 'flex';
    fiyatlarYukle();
}

function fiyatModalKapat() {
    document.getElementById('fiyatModal').style.display = 'none';
}

// --- 📦 STOK TAKİBİ ---
async function stokModalAc() {
    document.getElementById('stokModal').style.display = 'flex';
    await stokSantiyeleriYukle();
    stokYukle();
}

async function stokSantiyeleriYukle() {
    const token = localStorage.getItem('bai_token');
    const sel = document.getElementById('stokSantiye');
    if (!sel) return;
    try {
        const res = await fetch(`/santiyeler?token=${token}`);
        const data = await res.json();
        const santiyeler = data.santiyeler || [];
        sel.innerHTML = '<option value="">📍 Şantiye Seçin... (zorunlu)</option>' +
            santiyeler.map(s => `<option value="${s.id}">${s.ad}</option>`).join('');
    } catch(e) {}
}

function stokSantiyeDegisti() {
    const santiyeId = document.getElementById('stokSantiye').value;
    stokYukle(santiyeId ? parseInt(santiyeId) : null);
}
function stokModalKapat() {
    document.getElementById('stokModal').style.display = 'none';
}

async function stokYukle(santiyeId) {
    const token = localStorage.getItem('bai_token');
    try {
        const url = santiyeId ? `/stok?token=${token}&santiye_id=${santiyeId}` : `/stok?token=${token}`;
        const res = await fetch(url);
        const data = await res.json();

        // Uyarılar
        const uyariDiv = document.getElementById('stokUyarilar');
        if (data.uyarilar && data.uyarilar.length > 0) {
            uyariDiv.innerHTML = data.uyarilar.map(u =>
                `<div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:10px; padding:10px 14px; margin-bottom:8px; color:#fca5a5; font-size:0.85rem;">
                    ⚠️ <b>${u.malzeme}</b> stoğu ${u.bitis_gun} günde bitiyor! (Kalan: ${u.mevcut})
                </div>`
            ).join('');
        } else {
            uyariDiv.innerHTML = '';
        }

        // Kartlar
        const malzemeIkon = {demir:'🔩', cimento:'🏭', beton:'🧱', tugla:'🏠', kum:'⛱️'};
        const malzemeAd = {demir:'Demir', cimento:'Çimento', beton:'Beton', tugla:'Tuğla', kum:'Kum'};
        const kartDiv = document.getElementById('stokKartlar');

        function stokKartHtml(m, s) {
            const uyariRenk = s.bitis_gun && s.bitis_gun <= 7 ? '#EF4444' : s.bitis_gun && s.bitis_gun <= 14 ? '#F59E0B' : '#16A34A';
            const bgRenk    = s.bitis_gun && s.bitis_gun <= 7 ? '#FEF2F2' : s.bitis_gun && s.bitis_gun <= 14 ? '#FFFBEB' : '#F0FDF4';
            return `<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:14px;cursor:pointer;transition:box-shadow 0.15s;box-shadow:0 1px 3px rgba(0,0,0,0.05);" onclick="document.getElementById('stokGecmisMalzeme').value='${m}'; stokGecmisYukle();"
              onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.10)'" onmouseout="this.style.boxShadow='0 1px 3px rgba(0,0,0,0.05)'">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <span style="font-size:1.4rem;">${malzemeIkon[m]}</span>
                    ${s.bitis_gun ? `<span style="background:${bgRenk};color:${uyariRenk};font-size:10px;font-weight:700;padding:2px 6px;border-radius:20px;">${s.bitis_gun}g</span>` : '<span style="color:#CBD5E1;font-size:11px;">—</span>'}
                </div>
                <div style="color:#64748B;font-size:11px;font-weight:600;margin-bottom:4px;">${malzemeAd[m]}</div>
                <div style="color:#0F172A;font-size:1.3rem;font-weight:800;line-height:1;">${s.mevcut}</div>
                <div style="display:flex;justify-content:space-between;margin-top:8px;">
                    <span style="color:#16A34A;font-size:11px;font-weight:600;">+${s.toplam_giris}</span>
                    <span style="color:#EF4444;font-size:11px;font-weight:600;">-${s.toplam_cikis}</span>
                </div>
            </div>`;
        }

        function grupBaslikHtml(ad) {
            return `<div style="grid-column:1/-1;color:#3B82F6;font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:8px 0 4px;border-bottom:2px solid #EFF6FF;margin-bottom:6px;display:flex;align-items:center;gap:5px;"><svg width='11' height='11' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><path d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'/><circle cx='12' cy='10' r='3'/></svg>${ad}</div>`;
        }

        if (data.gruplar && data.gruplar.length > 0) {
            // Gruplu görünüm — tüm şantiyeler
            kartDiv.innerHTML = data.gruplar.map(g =>
                grupBaslikHtml(g.santiye_adi) +
                Object.entries(g.stok).map(([m, s]) => stokKartHtml(m, s)).join('')
            ).join('');
        } else {
            // Tekil şantiye görünümü
            let headerHtml = data.santiye_adi ? grupBaslikHtml(data.santiye_adi) : '';
            kartDiv.innerHTML = headerHtml + Object.entries(data.stok).map(([m, s]) => stokKartHtml(m, s)).join('');
        }

        stokGecmisYukle();
    } catch(e) {
        document.getElementById('stokKartlar').innerHTML = '<div style="color:#aaa; text-align:center; padding:20px; grid-column:1/-1;">Stok verisi yüklenemedi.</div>';
    }
}

async function stokGecmisYukle() {
    const token = localStorage.getItem('bai_token');
    const malzeme = document.getElementById('stokGecmisMalzeme').value;
    try {
        const res = await fetch(`/stok-gecmis/${malzeme}?token=${token}`);
        const data = await res.json();
        const liste = document.getElementById('stokGecmisListe');
        if (!data.gecmis || data.gecmis.length === 0) {
            liste.innerHTML = '<div style="color:#94A3B8; text-align:center; padding:24px; font-size:0.85rem;">Henüz hareket kaydı yok.</div>';
            return;
        }
        liste.innerHTML = data.gecmis.map(k => `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid #F1F5F9;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:32px;height:32px;border-radius:8px;background:${k.tip === 'giris' ? '#DCFCE7' : '#FEE2E2'};display:flex;align-items:center;justify-content:center;font-size:0.9rem;">${k.tip === 'giris' ? '📥' : '📤'}</div>
                    <div>
                        <div style="color:${k.tip === 'giris' ? '#16A34A' : '#DC2626'}; font-weight:700; font-size:0.85rem;">${k.tip === 'giris' ? '+' : '-'}${k.miktar} ${k.birim}</div>
                        <div style="color:#64748B; font-size:0.72rem;">${k.tedarikci || ''} ${k.notlar ? '· ' + k.notlar : ''}</div>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="color:#94A3B8; font-size:0.72rem;">${k.tarih}</span>
                    <button onclick="stokSil(${k.id})" style="background:#FEF2F2; border:1px solid #FECACA; color:#DC2626; border-radius:6px; padding:3px 8px; cursor:pointer; font-size:0.72rem;">Sil</button>
                </div>
            </div>
        `).join('');
    } catch(e) {}
}

async function stokKaydet() {
    const token = localStorage.getItem('bai_token');
    const santiye_id = document.getElementById('stokSantiye').value || null;
    const malzeme = document.getElementById('stokMalzeme').value;
    const tip = document.getElementById('stokTip').value;
    const miktar = document.getElementById('stokMiktar').value;
    const birim = document.getElementById('stokBirim').value;
    const tedarikci = document.getElementById('stokTedarikci').value;
    const fiyat = document.getElementById('stokFiyat').value;
    const notlar = document.getElementById('stokNotlar').value;
    const msg = document.getElementById('stokMsg');
    if (!santiye_id) { msg.innerHTML = '<span style="color:#e74c3c;">Şantiye seçin.</span>'; return; }
    if (!miktar) { msg.innerHTML = '<span style="color:#e74c3c;">Miktar girin.</span>'; return; }
    try {
        const res = await fetch('/stok-ekle', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, santiye_id: santiye_id ? parseInt(santiye_id) : null, malzeme, tip, miktar, birim, tedarikci, fiyat, notlar})
        });
        const data = await res.json();
        if (res.ok) {
            msg.innerHTML = '<span style="color:#2ecc71;">✅ ' + data.mesaj + '</span>';
            document.getElementById('stokMiktar').value = '';
            document.getElementById('stokTedarikci').value = '';
            document.getElementById('stokFiyat').value = '';
            document.getElementById('stokNotlar').value = '';
            stokYukle();
        } else {
            const detail = data.detail || 'Hata.';
            if (detail.startsWith('PLAN_YETERSIZ:')) {
                const parts = detail.split(':');
                planKilit(parts[1] || 'stok');
            } else {
                msg.innerHTML = '<span style="color:#e74c3c;">' + detail + '</span>';
            }
        }
    } catch(e) {
        msg.innerHTML = '<span style="color:#e74c3c;">Bağlantı hatası.</span>';
    }
}

async function stokSil(id) {
    const token = localStorage.getItem('bai_token');
    if (!confirm('Bu kaydı silmek istediğinizden emin misiniz?')) return;
    try {
        await fetch(`/stok-sil/${id}?token=${token}`, {method: 'DELETE'});
        stokGecmisYukle();
        stokYukle();
    } catch(e) {}
}

async function stokKomutuIsle(komut) {
    const token = localStorage.getItem('bai_token');
    const resBox = document.getElementById('result');
    try {
        const sRes = await fetch(`/santiyeler?token=${token}`);
        const sData = await sRes.json();
        const santiyeler = sData.santiyeler || [];
        const hedefAd = (komut.santiye_adi || '').toLowerCase();
        let enIyi = null, enIyiSkor = 0;
        for (const s of santiyeler) {
            const ad = s.ad.toLowerCase();
            if (ad === hedefAd) { enIyi = s; break; }
            const skor = hedefAd.split(' ').filter(w => ad.includes(w)).length;
            if (skor > enIyiSkor) { enIyiSkor = skor; enIyi = s; }
        }
        if (!enIyi) {
            resBox.innerHTML = `<div style="color:#f59e0b; padding:16px;">⚠️ "${komut.santiye_adi}" adında şantiye bulunamadı.</div>`;
            return;
        }
        const tip = komut.islem === 'cikar' ? 'cikis' : 'giris';
        const ekRes = await fetch('/stok-ekle', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, santiye_id: enIyi.id, malzeme: komut.malzeme, tip, miktar: komut.miktar, birim: komut.birim || '', notlar: 'AI komutu'})
        });
        if (ekRes.ok) {
            const islemAdi = tip === 'giris' ? 'eklendi' : 'düşüldü';
            resBox.innerHTML = `<div style="background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.3); border-radius:12px; padding:16px; color:#4ade80; font-weight:600;">✅ ${enIyi.ad} şantiyesine ${komut.miktar}${komut.birim ? ' '+komut.birim : ''} ${komut.malzeme} ${islemAdi}.</div>`;
            showToast(`${enIyi.ad}: ${komut.miktar} ${komut.malzeme} ${islemAdi}`, 'success');
        } else {
            resBox.innerHTML = `<div style="color:#ef4444; padding:16px;">❌ Stok kaydedilemedi.</div>`;
        }
    } catch(e) {
        resBox.innerHTML = `<div style="color:#ef4444; padding:16px;">❌ Hata: ${e.message}</div>`;
    }
}

// --- 🌍 DEPREM ANALİZİ ---
let depremHaritaObj = null;
let depremMarker = null;
let depremDepremKatman = null;

function depremModalAc() {
    document.getElementById('depremModal').style.display = 'flex';
    setTimeout(() => depremHaritaBaslat(), 100);
}

function depremModalKapat() {
    document.getElementById('depremModal').style.display = 'none';
}

function depremHaritaBaslat() {
    if (depremHaritaObj) return;
    depremHaritaObj = L.map('depremHarita').setView([39.0, 35.0], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap',
        maxZoom: 18
    }).addTo(depremHaritaObj);
    depremHaritaObj.on('click', function(e) {
        const lat = e.latlng.lat.toFixed(4);
        const lon = e.latlng.lng.toFixed(4);
        document.getElementById('depremLat').value = lat;
        document.getElementById('depremLon').value = lon;
        document.getElementById('depremKonumMsg').innerHTML = `📍 Seçilen konum: ${lat}, ${lon}`;
        if (depremMarker) depremHaritaObj.removeLayer(depremMarker);
        depremMarker = L.marker([lat, lon]).addTo(depremHaritaObj)
            .bindPopup('🏗️ Şantiye Konumu').openPopup();
    });
    depremSonYukle();
}

async function depremSonYukle() {
    try {
        const res = await fetch('/deprem-son?lat=39.0&lon=35.0&radius=800');
        const data = await res.json();
        if (depremDepremKatman) depremHaritaObj.removeLayer(depremDepremKatman);
        depremDepremKatman = L.layerGroup();
        (data.depremler || []).forEach(d => {
            if (!d.lat || !d.lon) return;
            const r = Math.max(4, Math.min(20, d.buyukluk * 3));
            const renk = d.buyukluk >= 5 ? '#ef4444' : d.buyukluk >= 3 ? '#f59e0b' : '#3b82f6';
            L.circleMarker([d.lat, d.lon], {
                radius: r, color: renk, fillColor: renk,
                fillOpacity: 0.6, weight: 1
            }).bindPopup(`<b>M${d.buyukluk}</b><br>${d.konum}<br>${d.tarih ? d.tarih.substring(0,10) : ''}`).addTo(depremDepremKatman);
        });
        depremDepremKatman.addTo(depremHaritaObj);
    } catch(e) {}
}

async function depremKonumBul() {
    const adres = document.getElementById('depremAdres').value;
    if (!adres) return;
    const msg = document.getElementById('depremKonumMsg');
    msg.innerHTML = '⏳ Konum aranıyor...';
    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(adres+' Türkiye')}&format=json&limit=1`);
        const data = await res.json();
        if (data && data[0]) {
            const lat = parseFloat(data[0].lat).toFixed(4);
            const lon = parseFloat(data[0].lon).toFixed(4);
            document.getElementById('depremLat').value = lat;
            document.getElementById('depremLon').value = lon;
            msg.innerHTML = `✅ Konum bulundu: ${data[0].display_name.substring(0,60)}...`;
            depremHaritaObj.setView([lat, lon], 10);
            if (depremMarker) depremHaritaObj.removeLayer(depremMarker);
            depremMarker = L.marker([lat, lon]).addTo(depremHaritaObj)
                .bindPopup('🏗️ Şantiye Konumu').openPopup();
        } else {
            msg.innerHTML = '❌ Konum bulunamadı, koordinat girin.';
        }
    } catch(e) {
        msg.innerHTML = '❌ Konum arama hatası.';
    }
}

async function depremAnalizBaslat() {
    const token = localStorage.getItem('bai_token');
    const lat = parseFloat(document.getElementById('depremLat').value);
    const lon = parseFloat(document.getElementById('depremLon').value);
    const adres = document.getElementById('depremAdres').value;
    if (!lat || !lon) {
        document.getElementById('depremKonumMsg').innerHTML = '❌ Önce konum seçin veya koordinat girin.';
        return;
    }
    document.getElementById('depremAnalizSonuc').style.display = 'none';
    document.getElementById('depremLoading').style.display = 'block';
    try {
        const res = await fetch('/deprem-risk-analiz', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, lat, lon, adres})
        });
        const d = await res.json();
        document.getElementById('depremLoading').style.display = 'none';
        document.getElementById('depremAnalizSonuc').style.display = 'block';

        const skor = d.risk_skoru || 0;
        const skorRenk = skor >= 75 ? '#ef4444' : skor >= 50 ? '#f59e0b' : skor >= 25 ? '#f97316' : '#2ecc71';
        document.getElementById('riskSkorText').textContent = skor;
        document.getElementById('riskCircle').style.stroke = skorRenk;
        setTimeout(() => {
            document.getElementById('riskCircle').style.strokeDashoffset = 226 * (1 - skor/100);
        }, 100);

        const seviyeRenk = {'Çok Yüksek':'#ef4444','Yüksek':'#f97316','Orta':'#f59e0b','Düşük':'#2ecc71'};
        document.getElementById('riskSeviyeText').textContent = d.risk_seviyesi || '';
        document.getElementById('riskSeviyeText').style.color = seviyeRenk[d.risk_seviyesi] || 'white';
        document.getElementById('riskZeminText').textContent = `Zemin Sınıfı: ${d.zemin_sinifi || '-'}`;
        document.getElementById('riskOzetText').textContent = d.ozet || '';

        const fay = d.en_yakin_fay || {};
        document.getElementById('fayAd').textContent = fay.ad || '-';
        document.getElementById('fayMesafe').textContent = fay.mesafe_km ? `${fay.mesafe_km} km uzaklıkta` : '-';
        document.getElementById('fayTip').textContent = `Tip: ${fay.tip || '-'}`;
        document.getElementById('faySonDeprem').textContent = `Son büyük deprem: ${fay.son_buyuk_deprem || '-'}`;

        const tbdy = d.tbdy_parametreler || {};
        document.getElementById('tbdyParams').innerHTML = `
            <div style="color:#c7d2fe;">Ss: <b style="color:white">${tbdy.Ss || '-'}</b> &nbsp; S1: <b style="color:white">${tbdy.S1 || '-'}</b></div>
            <div style="color:#c7d2fe;">PGA: <b style="color:white">${tbdy.PGA || '-'} g</b></div>
            <div style="color:#c7d2fe;">Bölge: <b style="color:white">${tbdy.deprem_bolgesi || '-'}</b></div>
        `;

        const liste = document.getElementById('sonDepremlerListe');
        if (d.son_depremler && d.son_depremler.length > 0) {
            liste.innerHTML = d.son_depremler.map(dep => {
                const renk = dep.buyukluk >= 5 ? '#ef4444' : dep.buyukluk >= 3 ? '#f59e0b' : '#aaa';
                return `<div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                    <span style="color:${renk}; font-weight:700;">M${dep.buyukluk}</span>
                    <span style="color:#ccc; font-size:0.82rem;">${dep.konum}</span>
                    <span style="color:#555; font-size:0.78rem;">${dep.tarih}</span>
                </div>`;
            }).join('');
        } else {
            liste.innerHTML = `<div style="color:#555; text-align:center; padding:16px; font-size:0.85rem;">AFAD verisi bulunamadı (${d.afad_deprem_sayisi || 0} deprem).</div>`;
        }

        document.getElementById('depremOneriler').innerHTML = (d.oneriler || []).map(o =>
            `<div style="color:#fcd34d; font-size:0.85rem; padding:4px 0; border-bottom:1px solid rgba(245,158,11,0.1);">• ${o}</div>`
        ).join('');

        if (depremMarker) depremHaritaObj.removeLayer(depremMarker);
        depremMarker = L.marker([lat, lon], {
            icon: L.divIcon({
                html: `<div style="background:${skorRenk}; color:white; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:0.75rem; border:3px solid white; box-shadow:0 0 10px ${skorRenk};">${skor}</div>`,
                iconSize: [36,36], iconAnchor: [18,18]
            })
        }).addTo(depremHaritaObj).bindPopup(`🏗️ Şantiye — Risk: ${d.risk_seviyesi}`).openPopup();
        depremHaritaObj.setView([lat, lon], 9);

    } catch(e) {
        document.getElementById('depremLoading').style.display = 'none';
        document.getElementById('depremKonumMsg').innerHTML = `❌ Hata: ${e.message}`;
    }
}

// ═══════════════════════════════════════════════════════════════
// 🏗️  ŞANTİYELERİM — Premium Glassmorphism Dashboard
//     CartoDB Dark Matter · Chart.js · Mini-Harita Koordinat Seçici
// ═══════════════════════════════════════════════════════════════
let santiyeHaritaObj    = null;   // Ana Leaflet haritası
let santiyeMiniHaritaObj = null;  // Form içindeki mini-harita
let santiyeMiniMarker   = null;   // Mini-harita seçim marker'ı
let santiyeVerisi       = [];     // Sunucudan gelen şantiye listesi
let _ilerlemeChart      = null;   // Chart.js ilerleme bar instance
let _isciChart          = null;   // Chart.js işçi doughnut instance

// CartoDB Dark Matter tile URL'i
const _CARTO_DARK = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
const _CARTO_ATTR = '&copy; <a href="https://carto.com/">CARTO</a>';

// ── MODAL AÇMA / KAPAMA ───────────────────────────────────────
function santiyeModalAc() {
    const el = document.getElementById('santiyeModal');
    if (!el) return;
    el.style.display = 'flex';
    setTimeout(() => {
        santiyeHaritaBaslat();
        santiyeYukle();
    }, 80);
}
function santiyeModalKapat() {
    const el = document.getElementById('santiyeModal');
    if (el) el.style.display = 'none';
}

// ── FORM MODAL ────────────────────────────────────────────────
function santiyeEkleModalAc(santiye) {
    const fm = document.getElementById('santiyeFormModal');
    if (!fm) return;
    fm.style.display = 'flex';
    document.getElementById('santiyeFormId').value        = santiye ? santiye.id : '';
    document.getElementById('santiyeFormBaslik').textContent = santiye ? 'Şantiye Düzenle' : 'Yeni Şantiye Ekle';
    document.getElementById('santiyeFormAd').value        = santiye ? santiye.ad : '';
    document.getElementById('santiyeFormKonum').value     = santiye ? santiye.konum : '';
    document.getElementById('santiyeFormLat').value       = santiye ? (santiye.lat || '') : '';
    document.getElementById('santiyeFormLon').value       = santiye ? (santiye.lon || '') : '';
    document.getElementById('santiyeFormIlerleme').value  = santiye ? santiye.ilerleme : 0;
    document.getElementById('santiyeFormIsci').value      = santiye ? santiye.isci_sayisi : 0;
    document.getElementById('santiyeFormDurum').value     = santiye ? santiye.durum : 'iyi';
    document.getElementById('santiyeFormIsg').value       = santiye ? (santiye.isg_durumu || '') : '';
    document.getElementById('santiyeFormNotlar').value    = santiye ? (santiye.notlar || '') : '';
    // Sync durum toggle
    const _dt = document.getElementById('santiyeFormDurumToggle');
    const _dl = document.getElementById('santiyeFormDurumLabel');
    if (_dt) {
        const isAcik = !santiye || santiye.durum !== 'sorun';
        _dt.checked = isAcik;
        if (_dl) { _dl.textContent = isAcik ? 'Açık' : 'Kapalı'; _dl.style.color = isAcik ? '#16A34A' : '#DC2626'; }
    }
    document.getElementById('santiyeFormMsg').innerHTML   = '';
    ragSecilenDosyalar = [];
    const lbl = document.getElementById('ragDropLabel');
    if (lbl) lbl.style.display = 'none';
    // Dosya alanını sıfırla
    const dosyaInput = document.getElementById('santiyeFormDosyaInput');
    if (dosyaInput) dosyaInput.value = '';
    const dosyaLabel = document.getElementById('santiyeFormDosyaLabel');
    if (dosyaLabel) dosyaLabel.textContent = 'Henüz dosya seçilmedi';
    const dosyaListesi = document.getElementById('santiyeFormDosyaListesi');
    if (dosyaListesi) dosyaListesi.innerHTML = '';
    // Sil bloğunu sadece edit modda göster
    const silBlok = document.getElementById('santiyeSilBlok');
    if (silBlok) silBlok.style.display = santiye ? 'block' : 'none';
    // Kaydet butonunu düzenle/ekle olarak güncelle
    const kaydetBtn = document.querySelector('#santiyeFormModal button[onclick="santiyeKaydet()"]');
    if (kaydetBtn) kaydetBtn.textContent = santiye ? 'Değişiklikleri Kaydet' : 'Şantiye Ekle';
    // Fotoğraf alanını sıfırla / mevcut fotoğrafı yükle
    santiyeFotoTemizle();
    if (santiye && santiye.foto) {
        _santiyeFotoBase64 = santiye.foto;
        const oniz = document.getElementById('santiyeFotoOnizleme');
        const ph   = document.getElementById('santiyeFotoPlaceholder');
        const kald = document.getElementById('santiyeFotoKaldir');
        const alan = document.getElementById('santiyeFotoAlani');
        if (oniz) { oniz.src = santiye.foto; oniz.style.display = 'block'; }
        if (ph)   ph.style.display = 'none';
        if (kald) kald.style.display = 'flex';
        if (alan) alan.style.borderStyle = 'solid';
    }
    // Mini-haritayı başlat (100ms gecikme — DOM hazır olsun)
    setTimeout(() => santiyeFormMiniHaritaBaslat(santiye), 120);
}
function santiyeFormKapat() {
    const fm = document.getElementById('santiyeFormModal');
    if (fm) fm.style.display = 'none';
    if (santiyeMiniHaritaObj) {
        santiyeMiniHaritaObj.remove();
        santiyeMiniHaritaObj = null;
        santiyeMiniMarker = null;
    }
}

function santiyeFormDosyaSecildi(input) {
    const dosyalar = Array.from(input.files);
    const label = document.getElementById('santiyeFormDosyaLabel');
    const liste = document.getElementById('santiyeFormDosyaListesi');
    if (!dosyalar.length) return;
    // ragSecilenDosyalar'a ekle (mevcut sistemi kullan)
    ragSecilenDosyalar = dosyalar;
    if (label) label.textContent = `${dosyalar.length} dosya seçildi`;
    if (liste) {
        liste.innerHTML = dosyalar.map(f => `
            <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:5px; padding:3px 8px; font-size:11px; color:#1D4ED8; display:flex; align-items:center; gap:4px;">
                <span>📄</span><span style="max-width:120px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${f.name}</span>
            </div>`).join('');
    }
}

function santiyeSilOnay() {
    const id = document.getElementById('santiyeFormId').value;
    const ad = document.getElementById('santiyeFormAd').value || 'Bu şantiye';
    if (!id) return;
    // Custom onay UI — modal içinde confirm() çalışmayabilir
    const silBlok = document.getElementById('santiyeSilBlok');
    if (!silBlok) return;
    silBlok.innerHTML = `
        <div style="font-size:13px; font-weight:700; color:#DC2626; margin-bottom:8px;">⚠️ Emin misiniz?</div>
        <div style="font-size:12px; color:#64748B; margin-bottom:12px;">"${ad}" kalıcı olarak silinecek.</div>
        <div style="display:flex; gap:8px;">
            <button onclick="santiyeSilYap(${id},'${ad.replace(/'/g,"\\'")}')"
                style="flex:1; background:#DC2626; border:none; color:white; padding:9px; border-radius:7px; cursor:pointer; font-weight:700; font-size:13px; font-family:inherit;">
                Evet, Sil
            </button>
            <button onclick="santiyeSilIptal()"
                style="flex:1; background:#F1F5F9; border:1px solid #E2E8F0; color:#475569; padding:9px; border-radius:7px; cursor:pointer; font-weight:600; font-size:13px; font-family:inherit;">
                İptal
            </button>
        </div>`;
}

function santiyeSilIptal() {
    const silBlok = document.getElementById('santiyeSilBlok');
    if (silBlok) silBlok.innerHTML = `
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <div>
                <div style="font-size:13px; font-weight:700; color:#DC2626;">Şantiyeyi Sil</div>
                <div style="font-size:11px; color:#EF4444; margin-top:2px;">Bu işlem geri alınamaz.</div>
            </div>
            <button onclick="santiyeSilOnay()" id="santiyeSilBtn"
                style="background:#DC2626; border:none; color:#FFFFFF; padding:8px 16px; border-radius:7px; cursor:pointer; font-weight:700; font-size:12px; font-family:inherit; white-space:nowrap;"
                onmouseover="this.style.background='#B91C1C'" onmouseout="this.style.background='#DC2626'">
                🗑 Şantiyeyi Sil
            </button>
        </div>`;
}

async function santiyeSilYap(id, ad) {
    const token = localStorage.getItem('bai_token');
    const silBlok = document.getElementById('santiyeSilBlok');
    if (silBlok) silBlok.innerHTML = '<div style="font-size:13px;color:#64748B;text-align:center;padding:8px;">⏳ Siliniyor...</div>';
    try {
        const res = await fetch(`/santiye-sil/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const data = await res.json();
        if (res.ok) {
            showToast(`"${ad}" silindi.`, 'success');
            santiyeFormKapat();
            if (typeof santiyePageYukle === 'function') santiyePageYukle();
            if (typeof santiyeYukle === 'function') santiyeYukle();
        } else {
            showToast(data.detail || 'Silinemedi.', 'error');
            santiyeSilIptal();
        }
    } catch(e) {
        showToast('Bağlantı hatası.', 'error');
        santiyeSilIptal();
    }
}
function sfDurumToggle(el) {
    const sel = document.getElementById('santiyeFormDurum');
    if (sel) sel.value = el.checked ? 'iyi' : 'sorun';
    const lbl = document.getElementById('santiyeFormDurumLabel');
    if (lbl) { lbl.textContent = el.checked ? 'Açık' : 'Kapalı'; lbl.style.color = el.checked ? '#16A34A' : '#DC2626'; }
}

let _santiyeFotoBase64 = null;
function santiyeFotoSecildi(file) {
    if (!file || !file.type.startsWith('image/')) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        _santiyeFotoBase64 = e.target.result;
        const oniz = document.getElementById('santiyeFotoOnizleme');
        const ph   = document.getElementById('santiyeFotoPlaceholder');
        const kald = document.getElementById('santiyeFotoKaldir');
        if (oniz) { oniz.src = e.target.result; oniz.style.display = 'block'; }
        if (ph)   ph.style.display = 'none';
        if (kald) kald.style.display = 'flex';
        const alan = document.getElementById('santiyeFotoAlani');
        if (alan) alan.style.borderStyle = 'solid';
    };
    reader.readAsDataURL(file);
}
function santiyeFotoTemizle() {
    _santiyeFotoBase64 = null;
    const oniz = document.getElementById('santiyeFotoOnizleme');
    const ph   = document.getElementById('santiyeFotoPlaceholder');
    const kald = document.getElementById('santiyeFotoKaldir');
    const inp  = document.getElementById('santiyeFotoInput');
    if (oniz) { oniz.src = ''; oniz.style.display = 'none'; }
    if (ph)   ph.style.display = 'flex';
    if (kald) kald.style.display = 'none';
    if (inp)  inp.value = '';
    const alan = document.getElementById('santiyeFotoAlani');
    if (alan) alan.style.borderStyle = 'dashed';
}

// ── ANA LİSTE HARİTASI — CartoDB Dark Matter ─────────────────
function santiyeHaritaBaslat() {
    if (santiyeHaritaObj) { santiyeHaritaObj.invalidateSize(); return; }
    santiyeHaritaObj = L.map('santiyeHarita', { zoomControl: true, attributionControl: false })
        .setView([39.0, 35.0], 6);
    L.tileLayer(_CARTO_DARK, { attribution: _CARTO_ATTR, maxZoom: 19, subdomains: 'abcd' })
        .addTo(santiyeHaritaObj);
}

// ── FORM MİNİ-HARİTASI — Koordinat Seçici ───────────────────
function santiyeFormMiniHaritaBaslat(santiye) {
    const el = document.getElementById('santiyeFormMiniHarita');
    if (!el) return;
    // Önceki instance'ı temizle
    if (santiyeMiniHaritaObj) { santiyeMiniHaritaObj.remove(); santiyeMiniHaritaObj = null; }

    const basLat = (santiye && santiye.lat) ? santiye.lat : 39.0;
    const basLon = (santiye && santiye.lon) ? santiye.lon : 35.0;
    const zoom   = (santiye && santiye.lat) ? 10 : 6;

    santiyeMiniHaritaObj = L.map('santiyeFormMiniHarita', { zoomControl: true, attributionControl: false })
        .setView([basLat, basLon], zoom);
    L.tileLayer(_CARTO_DARK, { attribution: _CARTO_ATTR, maxZoom: 19, subdomains: 'abcd' })
        .addTo(santiyeMiniHaritaObj);

    // Düzenlemede mevcut marker göster
    if (santiye && santiye.lat && santiye.lon) {
        santiyeMiniMarker = L.marker([santiye.lat, santiye.lon], {
            icon: L.divIcon({
                html: '<div style="background:#f97316;width:14px;height:14px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 8px rgba(249,115,22,0.8);"></div>',
                iconSize: [14, 14], iconAnchor: [7, 7]
            })
        }).addTo(santiyeMiniHaritaObj);
    }

    // Tıklama: koordinat doldur + marker
    santiyeMiniHaritaObj.on('click', function(e) {
        const lat = e.latlng.lat.toFixed(4);
        const lon = e.latlng.lng.toFixed(4);
        document.getElementById('santiyeFormLat').value = lat;
        document.getElementById('santiyeFormLon').value = lon;
        if (santiyeMiniMarker) santiyeMiniHaritaObj.removeLayer(santiyeMiniMarker);
        santiyeMiniMarker = L.marker([lat, lon], {
            icon: L.divIcon({
                html: '<div style="background:#f97316;width:14px;height:14px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 8px rgba(249,115,22,0.8);"></div>',
                iconSize: [14, 14], iconAnchor: [7, 7]
            })
        }).addTo(santiyeMiniHaritaObj);
    });
}

// ── VERİ YÜKLE ───────────────────────────────────────────────
async function santiyeYukle() {
    const token = localStorage.getItem('bai_token');
    try {
        const res  = await fetch('/santiyeler', { headers: { 'Authorization': 'Bearer ' + token } });
        const data = await res.json();
        santiyeVerisi = data.santiyeler || [];
        santiyeOzetGoster();
        santiyeKartlarGoster();
        santiyeGrafikleriCiz();
        santiyeHaritaGuncelle();
    } catch(e) {
        console.error('Santiye yükleme hatası:', e);
    }
}

// ── KPI KARTLARI ─────────────────────────────────────────────
function santiyeOzetGoster() {
    const toplam     = santiyeVerisi.length;
    const iyi        = santiyeVerisi.filter(s => s.durum === 'iyi').length;
    const dikkat     = santiyeVerisi.filter(s => s.durum === 'dikkat').length;
    const sorun      = santiyeVerisi.filter(s => s.durum === 'sorun').length;
    const toplamIsci = santiyeVerisi.reduce((a, s) => a + (s.isci_sayisi || 0), 0);

    const altBaslik = document.getElementById('santiyeAltBaslik');
    if (altBaslik) altBaslik.textContent = `${toplam} aktif proje · Gerçek zamanlı izleme`;

    const kpiData = [
        { val: toplam,    label: 'TOPLAM PROJE', accent: '#6366f1' },
        { val: iyi,       label: 'İYİ',          accent: '#14b8a6' },
        { val: dikkat,    label: 'DİKKAT',       accent: '#f59e0b' },
        { val: toplamIsci,label: 'TOPLAM İŞÇİ',  accent: '#a855f7' },
    ];
    document.getElementById('santiyeOzet').innerHTML = kpiData.map(k => `
        <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px 20px; border-top:2px solid ${k.accent}; transition:transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
            <div style="font-size:28px; font-weight:700; color:${k.accent}; line-height:1;">${k.val}</div>
            <div style="font-size:11px; color:rgba(255,255,255,0.4); margin-top:6px; text-transform:uppercase; letter-spacing:0.1em;">${k.label}</div>
        </div>`).join('');
}

// ── PROJE KARTLARI ────────────────────────────────────────────
function santiyeKartlarGoster() {
    const el = document.getElementById('santiyeKartlar');
    if (!el) return;

    if (santiyeVerisi.length === 0) {
        el.innerHTML = `
            <div style="grid-column:1/-1; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:60px 20px; gap:16px; color:#475569;">
                <div style="font-size:56px;margin-bottom:12px;">🏗️</div>
                <div style="font-size:15px; font-weight:600; color:#64748b;">Henüz şantiye eklenmedi</div>
                <div style="font-size:12.5px; color:#475569;">Projenizi sisteme ekleyerek takibe başlayın</div>
                <button onclick="santiyeEkleModalAc(null)" style="margin-top:4px; background:linear-gradient(135deg,rgba(249,115,22,0.20),rgba(249,115,22,0.10)); border:1px solid rgba(249,115,22,0.35); color:#fb923c; padding:10px 22px; border-radius:10px; cursor:pointer; font-weight:700; font-size:13px; font-family:inherit; transition:all 0.2s;">İlk Şantiyeni Ekle →</button>
            </div>`;
        return;
    }

    const durumCfg = {
        iyi:    { renk: '#22c55e', badge: '🟢 İyi',     borderTop: '#22c55e' },
        dikkat: { renk: '#f59e0b', badge: '🟡 Dikkat',  borderTop: '#f59e0b' },
        sorun:  { renk: '#ef4444', badge: '🔴 Kritik',  borderTop: '#ef4444' },
    };

    el.innerHTML = santiyeVerisi.map(s => {
        const cfg = durumCfg[s.durum] || durumCfg.iyi;
        const pct = Math.min(100, Math.max(0, s.ilerleme || 0));
        // Progress bar rengi
        const barRenk = pct < 31 ? 'linear-gradient(90deg,#ef4444,#f87171)'
                      : pct < 71 ? 'linear-gradient(90deg,#f59e0b,#fbbf24)'
                      :             'linear-gradient(90deg,#22c55e,#4ade80)';
        // Güvenli JSON serialize (onclick için)
        const safeJson = JSON.stringify(s).replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/"/g,'&quot;');
        return `
        <div class="s-kart" style="backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); border-top:2px solid ${cfg.borderTop};">
            <!-- Başlık + Durum Badge -->
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:10px;">
                <div style="min-width:0;">
                    <div style="font-weight:700; font-size:14.5px; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${s.ad}</div>
                    <div style="font-size:11.5px; color:#64748b; margin-top:3px; display:flex; align-items:center; gap:4px;"><span>📍</span><span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${s.konum || '—'}</span></div>
                </div>
                <span style="flex-shrink:0; font-size:11px; font-weight:700; padding:3px 9px; border-radius:20px; background:${cfg.renk}1a; border:1px solid ${cfg.renk}44; color:${cfg.renk}; white-space:nowrap;">${cfg.badge}</span>
            </div>
            <!-- İlerleme Bar -->
            <div style="margin-bottom:4px; display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:10.5px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">İlerleme</span>
                <span style="font-size:12px; font-weight:700; color:#fff;">${pct}%</span>
            </div>
            <div style="background:rgba(255,255,255,0.06); border-radius:6px; height:5px; margin-bottom:12px; overflow:hidden;">
                <div class="s-progress-bar" style="background:${barRenk}; height:100%; width:0%; border-radius:6px; transition:width 1.1s cubic-bezier(0.4,0,0.2,1);" data-target="${pct}"></div>
            </div>
            <!-- Meta bilgi -->
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px; font-size:11.5px; color:#64748b;">
                <span style="display:flex; align-items:center; gap:4px;">👷 <b style="color:#94a3b8;">${s.isci_sayisi || 0}</b> kişi</span>
                ${s.isg_durumu ? `<span style="display:flex; align-items:center; gap:4px;">🦺 <span style="color:#94a3b8; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:100px;">${s.isg_durumu}</span></span>` : ''}
            </div>
            <!-- Footer -->
            <div style="border-top:1px solid rgba(255,255,255,0.05); padding-top:10px; display:flex; gap:8px;">
                <button onclick="santiyeEkleModalAc(${safeJson})"
                    style="flex:1; background:rgba(99,102,241,0.10); border:1px solid rgba(99,102,241,0.22); color:#818cf8; padding:7px; border-radius:8px; cursor:pointer; font-size:12px; font-weight:600; transition:all 0.18s; font-family:inherit;"
                    onmouseover="this.style.background='rgba(99,102,241,0.22)'" onmouseout="this.style.background='rgba(99,102,241,0.10)'">✏️ Düzenle</button>
                <button onclick="santiyeSilOnay(${s.id},'${(s.ad||'').replace(/'/g,"\\'")}')"
                    style="flex:0 0 auto; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.18); color:#f87171; padding:7px 12px; border-radius:8px; cursor:pointer; font-size:12px; transition:all 0.18s;"
                    onmouseover="this.style.background='rgba(239,68,68,0.20)'" onmouseout="this.style.background='rgba(239,68,68,0.08)'">🗑️</button>
            </div>
        </div>`;
    }).join('');

    // Animasyonlu progress bar'ları tetikle
    requestAnimationFrame(() => {
        document.querySelectorAll('.s-progress-bar').forEach(bar => {
            bar.style.width = bar.dataset.target + '%';
        });
    });
}

// ── CHART.JS — İlerleme Bar + İşçi Doughnut + Durum Özeti ───
function santiyeGrafikleriCiz() {
    if (_ilerlemeChart) { _ilerlemeChart.destroy(); _ilerlemeChart = null; }
    if (_isciChart)     { _isciChart.destroy();     _isciChart = null; }

    const barEl   = document.getElementById('ilerlemeChart');
    const doughEl = document.getElementById('isciChart');
    if (!barEl || !doughEl) return;

    const PALETTE = ['#6366f1','#14b8a6','#f59e0b','#a855f7','#ef4444'];

    // Gerçek veri varsa kullan, yoksa placeholder
    const gercek = santiyeVerisi.length > 0;
    const adlar        = gercek
        ? santiyeVerisi.map(s => s.ad.length > 16 ? s.ad.slice(0,16)+'…' : s.ad)
        : ['Şantiye A', 'Şantiye B', 'Şantiye C'];
    const ilerlemeler  = gercek
        ? santiyeVerisi.map(s => s.ilerleme || 0)
        : [75, 45, 90];
    const isciSayilari = gercek
        ? santiyeVerisi.map(s => s.isci_sayisi || 0)
        : [12, 8, 20];

    const barRenkler = ilerlemeler.map(p =>
        p <= 30 ? 'rgba(239,68,68,0.8)' : p <= 70 ? 'rgba(245,158,11,0.8)' : 'rgba(20,184,166,0.8)'
    );

    // ── Grafik 1: Yatay Bar ──
    _ilerlemeChart = new Chart(barEl.getContext('2d'), {
        type: 'bar',
        data: {
            labels: adlar,
            datasets: [{
                data: ilerlemeler,
                backgroundColor: barRenkler,
                borderRadius: 4,
                borderSkipped: false,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 700 },
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: ctx => ` %${ctx.parsed.x}` } }
            },
            scales: {
                x: {
                    min: 0, max: 100,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: 'rgba(255,255,255,0.4)', font: { size: 9 } }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: 'rgba(255,255,255,0.6)', font: { size: 10 } }
                }
            }
        }
    });

    // ── Grafik 2: Doughnut ──
    _isciChart = new Chart(doughEl.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: adlar,
            datasets: [{
                data: isciSayilari,
                backgroundColor: PALETTE.slice(0, adlar.length),
                borderWidth: 0,
                hoverOffset: 4,
            }]
        },
        options: {
            cutout: '65%',
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 700 },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: 'rgba(255,255,255,0.5)', font: { size: 10 }, boxWidth: 10 }
                },
                tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed} kişi` } }
            }
        }
    });

    // ── Grafik 3: Durum Özeti ──
    const durumEl = document.getElementById('santiyeDurumOzet');
    if (durumEl) {
        if (gercek) {
            const iyi    = santiyeVerisi.filter(s => s.durum === 'iyi').length;
            const dikkat = santiyeVerisi.filter(s => s.durum === 'dikkat').length;
            const kritik = santiyeVerisi.filter(s => s.durum === 'sorun').length;
            durumEl.innerHTML = [
                { emoji:'🟢', label:'İyi',    val: iyi,    renk:'34,197,94'  },
                { emoji:'🟡', label:'Dikkat', val: dikkat, renk:'245,158,11' },
                { emoji:'🔴', label:'Kritik', val: kritik, renk:'239,68,68'  },
            ].map(d => `
                <div style="background:rgba(${d.renk},0.1); border:1px solid rgba(${d.renk},0.3); border-radius:8px; padding:8px 14px; font-size:13px; color:rgba(255,255,255,0.75); white-space:nowrap;">
                    ${d.emoji} ${d.label}: <b style="color:#fff;">${d.val}</b>
                </div>`).join('');
        } else {
            durumEl.innerHTML = '';
        }
    }
}

// ── HARİTA MARKERLARI ─────────────────────────────────────────
function santiyeHaritaGuncelle() {
    if (!santiyeHaritaObj) return;
    // Eski markerları temizle
    santiyeHaritaObj.eachLayer(l => { if (l instanceof L.Marker) santiyeHaritaObj.removeLayer(l); });

    const durumRenk = { iyi: '#22c55e', dikkat: '#f59e0b', sorun: '#ef4444' };
    const koordinatlilar = santiyeVerisi.filter(s => s.lat && s.lon);

    koordinatlilar.forEach(s => {
        const renk = durumRenk[s.durum] || '#f97316';
        L.marker([s.lat, s.lon], {
            icon: L.divIcon({
                html: `<div style="background:${renk}; color:white; border-radius:50%; width:30px; height:30px; display:flex; align-items:center; justify-content:center; font-size:13px; border:2.5px solid rgba(255,255,255,0.85); box-shadow:0 0 12px ${renk}88;">🏗️</div>`,
                iconSize: [30, 30], iconAnchor: [15, 15], className: ''
            })
        }).addTo(santiyeHaritaObj)
        .bindPopup(`<div style="font-family:system-ui;min-width:160px;"><b>${s.ad}</b><br><small>📍 ${s.konum}</small><br>İlerleme: <b>${s.ilerleme||0}%</b><br>👷 ${s.isci_sayisi||0} kişi</div>`);
    });

    // Badge güncelle
    const badge   = document.getElementById('santiyeHaritaBadge');
    const sayiEl  = document.getElementById('santiyeHaritaCount');
    if (badge) badge.style.display = koordinatlilar.length ? 'block' : 'none';
    if (sayiEl) sayiEl.textContent = koordinatlilar.length;

    // Tüm markerları görünüme al
    if (koordinatlilar.length > 1) {
        const bounds = L.latLngBounds(koordinatlilar.map(s => [s.lat, s.lon]));
        santiyeHaritaObj.fitBounds(bounds, { padding: [30, 30] });
    } else if (koordinatlilar.length === 1) {
        santiyeHaritaObj.setView([koordinatlilar[0].lat, koordinatlilar[0].lon], 10);
    }
}

// ── KAYDET ────────────────────────────────────────────────────
async function santiyeKaydet() {
    const token = localStorage.getItem('bai_token');
    const id    = document.getElementById('santiyeFormId').value;
    const msg   = document.getElementById('santiyeFormMsg');
    const btn   = document.querySelector('#santiyeFormModal button[onclick="santiyeKaydet()"]');

    const body = {
        ad:          document.getElementById('santiyeFormAd').value.trim(),
        konum:       document.getElementById('santiyeFormKonum').value.trim(),
        lat:         parseFloat(document.getElementById('santiyeFormLat').value) || null,
        lon:         parseFloat(document.getElementById('santiyeFormLon').value) || null,
        ilerleme:    parseInt(document.getElementById('santiyeFormIlerleme').value) || 0,
        isci_sayisi: parseInt(document.getElementById('santiyeFormIsci').value) || 0,
        durum:       document.getElementById('santiyeFormDurum').value,
        isg_durumu:  document.getElementById('santiyeFormIsg').value.trim(),
        notlar:      document.getElementById('santiyeFormNotlar').value.trim(),
        foto:        _santiyeFotoBase64 || null
    };

    if (!body.ad || !body.konum) {
        msg.innerHTML = '<div style="color:#f87171; font-size:12px;">⚠️ Şantiye adı ve konum zorunludur.</div>';
        return;
    }
    if (btn) { btn.textContent = '⏳ Kaydediliyor...'; btn.disabled = true; }

    try {
        const url = id ? `/santiye-guncelle/${id}` : '/santiye-ekle';
        const res  = await fetch(url, {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const data = await res.json();

        if (res.ok) {
            msg.innerHTML = '<div style="color:#4ade80; font-size:12px;">✅ Kaydedildi!</div>';

            // RAG dosyaları varsa yükle
            if (ragSecilenDosyalar.length > 0) {
                const yeniId = data.id || id;
                if (yeniId) {
                    try {
                        const fd = new FormData();
                        ragSecilenDosyalar.forEach(f => fd.append('dosyalar', f));
                        await fetch(`/santiye-dosya-yukle/${yeniId}?token=${token}`, {
                            method: 'POST',
                            body: fd
                        });
                        showToast('Dosyalar AI belleğine yüklendi ✓', 'success');
                    } catch(_) {
                        showToast('Dosya yüklemesi başarısız.', 'error');
                    }
                }
            }

            setTimeout(() => { santiyeFormKapat(); santiyeYukle(); }, 700);
        } else {
            const detail = data.detail || 'Hata oluştu.';
            if (detail.startsWith('PLAN_YETERSIZ:')) {
                santiyeFormKapat();
                planKilit(detail.split(':')[1] || 'santiye');
            } else {
                msg.innerHTML = `<div style="color:#f87171; font-size:12px;">❌ ${detail}</div>`;
            }
        }
    } catch(e) {
        msg.innerHTML = '<div style="color:#f87171; font-size:12px;">❌ Bağlantı hatası.</div>';
    } finally {
        if (btn) { btn.textContent = '💾 Şantiyeyi Kaydet'; btn.disabled = false; }
    }
}

// ── SİL ───────────────────────────────────────────────────────

async function fiyatlarYukle() {
    const sehir = document.getElementById('citySelect')?.value || 'genel';
    try {
        const res = await fetch(`/fiyatlar?sehir=${sehir}`);
        const data = await res.json();

        const uyariDiv = document.getElementById('uyarilar');
        if (data.uyarilar && data.uyarilar.length > 0) {
            uyariDiv.innerHTML = data.uyarilar.map(u => {
                const artti = parseFloat(u.degisim) > 0;
                return `<div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:10px; padding:10px 14px; margin-bottom:8px; color:#fca5a5; font-size:0.85rem; display:flex; align-items:center; gap:8px;">
                    <span>${artti ? '📈' : '📉'}</span>
                    <span><b>${u.malzeme}</b> bu hafta <b>${u.degisim}%</b> ${artti ? 'arttı' : 'düştü'} — ${u.tarih}</span>
                </div>`;
            }).join('');
        } else {
            uyariDiv.innerHTML = '';
        }

        const malzemeIkon = {demir:'🔩', cimento:'🏭', beton:'🧱', tugla:'🏠', kum:'⛱️'};
        const malzemeAd = {demir:'Demir', cimento:'Çimento', beton:'Beton', tugla:'Tuğla', kum:'Kum'};
        const kartDiv = document.getElementById('fiyatKartlari');
        kartDiv.innerHTML = Object.entries(data.fiyatlar).map(([m, f]) => `
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span style="font-size:1.3rem;">${malzemeIkon[m] || '📦'}</span>
                    <span style="color:#555; font-size:0.72rem;">${f.tarih || '-'}</span>
                </div>
                <div style="color:white; font-weight:700; font-size:0.9rem; margin-bottom:2px;">${malzemeAd[m]}</div>
                <div style="color:var(--primary); font-size:1.2rem; font-weight:800;">${f.fiyat ? '₺'+f.fiyat : '—'}</div>
                <div style="color:#555; font-size:0.72rem;">${f.birim || ''}</div>
            </div>
        `).join('');

        grafikYukle();
    } catch(e) {
        document.getElementById('fiyatKartlari').innerHTML = '<div style="color:#aaa; text-align:center; padding:20px; grid-column:1/-1;">Fiyat verisi yüklenemedi.</div>';
    }
}

async function grafikYukle() {
    const malzeme = document.getElementById('grafMalzeme').value;
    const gun = document.getElementById('grafGun').value;
    try {
        const res = await fetch(`/fiyat-gecmis/${malzeme}?gun=${gun}`);
        const data = await res.json();
        const canvas = document.getElementById('fiyatGrafik');
        const bosMsg = document.getElementById('grafBosMesaj');

        if (!data.gecmis || data.gecmis.length < 2) {
            canvas.style.display = 'none';
            bosMsg.style.display = 'block';
            return;
        }
        canvas.style.display = 'block';
        bosMsg.style.display = 'none';

        if (fiyatGrafigi) fiyatGrafigi.destroy();
        fiyatGrafigi = new Chart(canvas, {
            type: 'line',
            data: {
                labels: data.gecmis.map(d => d.tarih),
                datasets: [{
                    label: malzeme + ' ₺',
                    data: data.gecmis.map(d => parseFloat(d.fiyat)),
                    borderColor: '#f97316',
                    backgroundColor: 'rgba(249,115,22,0.1)',
                    borderWidth: 2,
                    pointRadius: 3,
                    pointHoverRadius: 6,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#666', maxTicksLimit: 6 }, grid: { color: 'rgba(255,255,255,0.05)' } },
                    y: { ticks: { color: '#666', callback: v => '₺'+v }, grid: { color: 'rgba(255,255,255,0.05)' } }
                }
            }
        });
    } catch(e) {}
}

async function fiyatKaydet() {
    const token = localStorage.getItem('bai_token');
    const malzeme = document.getElementById('fiyatMalzeme').value;
    const fiyat = document.getElementById('fiyatDeger').value;
    const sehir = document.getElementById('fiyatSehir').value;
    const msg = document.getElementById('fiyatMsg');

    if (!fiyat) { msg.innerHTML = '<span style="color:#e74c3c;">Fiyat girin.</span>'; return; }

    const birimler = {demir:'ton', cimento:'çuval', beton:'m³', tugla:'adet', kum:'ton'};
    try {
        const res = await fetch('/fiyat-gir', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({token, malzeme, fiyat, birim: birimler[malzeme], sehir})
        });
        const data = await res.json();
        if (res.ok) {
            msg.innerHTML = '<span style="color:#2ecc71;">✅ ' + data.mesaj + '</span>';
            document.getElementById('fiyatDeger').value = '';
            fiyatlarYukle();
        } else {
            msg.innerHTML = '<span style="color:#e74c3c;">' + (data.detail || 'Hata.') + '</span>';
        }
    } catch(e) {
        msg.innerHTML = '<span style="color:#e74c3c;">Bağlantı hatası.</span>';
    }
}

// --- 🌙 TEMA ---
function temaToggle() {
    document.body.classList.toggle('light-mode');
    localStorage.setItem('tema', document.body.classList.contains('light-mode') ? 'light' : 'dark');
}

const kayitliTema = localStorage.getItem('tema');
if (kayitliTema === 'light') document.body.classList.add('light-mode');

// --- 📊 HAFTALIK RAPOR ---
async function haftalikRaporIndir() {
    const token = localStorage.getItem('bai_token');
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'Türkiye';
    const resBox = document.getElementById('result');
    resBox.innerHTML = '<div style="text-align:center; padding:20px;"><div style="font-size:2rem;">📊</div><div style="color:#aaa; margin-top:8px;">Haftalık rapor hazırlanıyor...<br><small>AI analiz yapıyor, PDF oluşturuluyor...</small></div></div>';
    try {
        const res = await fetch('/haftalik-rapor-olustur', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, sehir})
        });
        if (!res.ok) {
            const err = await res.json();
            resBox.innerHTML = `<div style="color:#e74c3c;">❌ ${err.detail || 'Rapor oluşturulamadı.'}</div>`;
            return;
        }
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `BuildingAI_Haftalik_${new Date().toISOString().slice(0,10)}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        resBox.innerHTML = '<div style="text-align:center; padding:20px;"><div style="font-size:2rem;">✅</div><div style="color:#2ecc71; margin-top:8px; font-weight:700;">Haftalık rapor indirildi!</div></div>';
    } catch(e) {
        resBox.innerHTML = `<div style="color:#e74c3c;">❌ Hata: ${e.message}</div>`;
    }
}

// --- SAYFA YÜKLENME ---
document.addEventListener('DOMContentLoaded', async () => {
    sesYukle();
    // Günlük rapor tarih alanını bugünle doldur
    const grTarih = document.getElementById('grTarih');
    if (grTarih) grTarih.value = new Date().toISOString().split('T')[0];

    // ── Google OAuth callback handler ──────────────────────────
    const urlParams = new URLSearchParams(window.location.search);
    const oauthToken = urlParams.get('oauth_token');
    const oauthError = urlParams.get('oauth_error');

    if (oauthToken) {
        // OAuth başarılı: token'ı kaydet, URL'den temizle
        localStorage.setItem('bai_token', oauthToken);
        localStorage.setItem('bai_token_expiry', Date.now() + 7 * 24 * 60 * 60 * 1000);
        window.history.replaceState({}, document.title, '/app');
        showToast('Google ile giriş başarılı! Hoş geldiniz.', 'success');
    } else if (oauthError) {
        const msgs = {
            cancelled:      'Google girişi iptal edildi.',
            token_failed:   'Google doğrulama başarısız. Tekrar deneyin.',
            userinfo_failed:'Google bilgileri alınamadı.',
            no_email:       'Google hesabından e-posta alınamadı.',
        };
        showToast(msgs[oauthError] || 'Google girişi başarısız.', 'error');
        window.history.replaceState({}, document.title, '/app');
    }
    // ──────────────────────────────────────────────────────────

    // 🔐 Otomatik giriş — token varsa kontrol et
    const token = localStorage.getItem('bai_token');
    if (token) {
        try {
            const res = await fetch(`/beni-tanı?token=${token}`);
            if (res.ok) {
                const data = await res.json();
                aktifKullanici = data;
                document.getElementById('auth-overlay').style.display = 'none';
                document.getElementById('mainApp').style.display = 'block';
                document.getElementById('navSidebar').style.display = 'flex';
                document.getElementById('topHeader').style.display = 'flex';
                dilDegistir(aktifDil);
                havaGuncelle();
                kullanımDurumuGoster();
                const kayitliRol = localStorage.getItem('bai_rol');
                if (kayitliRol) navSidebarGuncelle(kayitliRol);
                else rolEkraniniGoster();
                return;
            } else {
                localStorage.removeItem('bai_token');
                localStorage.removeItem('bai_user');
            }
        } catch(e) {
            // Network hatası (offline/PWA) — token geçerliyse uygulamayı göster
            const expiry = localStorage.getItem('bai_token_expiry');
            if (expiry && Date.now() < parseInt(expiry)) {
                const cachedUser = localStorage.getItem('bai_user');
                if (cachedUser) aktifKullanici = JSON.parse(cachedUser);
                document.getElementById('auth-overlay').style.display = 'none';
                document.getElementById('mainApp').style.display = 'block';
                document.getElementById('navSidebar').style.display = 'flex';
                document.getElementById('topHeader').style.display = 'flex';
                dilDegistir(aktifDil);
                const kayitliRol = localStorage.getItem('bai_rol');
                if (kayitliRol) navSidebarGuncelle(kayitliRol);
                else rolEkraniniGoster();
                return;
            }
            localStorage.removeItem('bai_token');
            localStorage.removeItem('bai_token_expiry');
        }
    }
    havaGuncelle();
});

function showToast(msg, type = 'info') {
  const existing = document.getElementById('toastNotif');
  if (existing) existing.remove();

  const colors = {
    info:    { bg: 'rgba(56,189,248,0.15)',  border: 'rgba(56,189,248,0.4)',  icon: 'ℹ️' },
    warning: { bg: 'rgba(249,115,22,0.15)',  border: 'rgba(249,115,22,0.5)',  icon: '⚠️' },
    success: { bg: 'rgba(34,197,94,0.15)',   border: 'rgba(34,197,94,0.4)',   icon: '✅' },
    error:   { bg: 'rgba(239,68,68,0.15)',   border: 'rgba(239,68,68,0.4)',   icon: '❌' },
  };
  const c = colors[type] || colors.info;

  const toast = document.createElement('div');
  toast.id = 'toastNotif';
  toast.style.cssText = `
    position:fixed; top:70px; right:20px; z-index:99999;
    background:${c.bg}; border:1px solid ${c.border};
    backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
    border-radius:14px; padding:14px 20px;
    color:#fff; font-size:14px; font-weight:500;
    display:flex; align-items:center; gap:10px;
    box-shadow:0 8px 32px rgba(0,0,0,0.4);
    animation:toastIn 0.3s ease; max-width:340px;
    font-family:'Poppins',sans-serif;
  `;
  toast.innerHTML = `<span>${msg}</span>
    <button onclick="this.parentElement.remove()" style="background:none;border:none;color:#aaa;cursor:pointer;font-size:16px;margin-left:auto;padding:0 0 0 10px;">✕</button>`;

  const style = document.createElement('style');
  style.textContent = '@keyframes toastIn{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}';
  document.head.appendChild(style);
  document.body.appendChild(toast);
  setTimeout(() => toast?.remove(), 4000);
}

// Legacy shim — yeni dashboard'a yönlendirir
function santiyeListeYukle() { santiyeYukle(); }

function gTab(name, el) {
  document.querySelectorAll('.gv-tab-content').forEach(t => t.style.display = 'none');
  const panel = document.getElementById('gtab-' + name);
  if (panel) panel.style.display = 'block';
  document.querySelectorAll('.gv-tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  if (name === 'hava') guvenlikHavaDurumunuYukle();
  if (name === 'acil') acilMapYukle();
}

function gToggle(el) {
  const btn = el.querySelector('.gv-ctrl-btn');
  if (!btn) return;
  const checked = el.dataset.checked === '1';
  if (checked) {
    el.dataset.checked = '0';
    btn.classList.remove('gv-ctrl-btn-ok');
    btn.textContent = 'Kontrol Et';
    btn.style.background = btn.dataset.origBg || '#0D1117';
  } else {
    if (!btn.dataset.origBg) btn.dataset.origBg = btn.style.background || '#0D1117';
    el.dataset.checked = '1';
    btn.classList.add('gv-ctrl-btn-ok');
    btn.style.background = '';
    btn.textContent = '✓ Tamam';
  }
  guvenlikSkoruGuncelle();
}

function guvenlikSkoruGuncelle() {
  const tumItems = document.querySelectorAll('#guvenlikModal .gv-check-item');
  const tamam = document.querySelectorAll('#guvenlikModal .gv-check-item[data-checked="1"]').length;
  const toplam = tumItems.length;
  const skor = toplam > 0 ? Math.round((tamam / toplam) * 100) : 0;

  const skorEl = document.getElementById('guvenlikSkor');
  if (skorEl) skorEl.textContent = skor;

  // Update ISG progress counters
  const kkdItems = document.querySelectorAll('#isg-kkd-list .gv-check-item');
  const kkdTamam = document.querySelectorAll('#isg-kkd-list .gv-check-item[data-checked="1"]').length;
  const prog1 = document.getElementById('isg-progress-1');
  if (prog1) prog1.textContent = kkdTamam + '/' + kkdItems.length;

  const sahaItems = document.querySelectorAll('#isg-saha-list .gv-check-item');
  const sahaTamam = document.querySelectorAll('#isg-saha-list .gv-check-item[data-checked="1"]').length;
  const prog2 = document.getElementById('isg-progress-2');
  if (prog2) prog2.textContent = sahaTamam + '/' + sahaItems.length;
}

function guvenlikHavaDurumunuYukle() {
  const sehir = document.getElementById('citySelect')?.value || 'Sivas';
  const satirlar = document.getElementById('gv-hava-satirlar');
  const riskEl = document.getElementById('gv-hava-risk');
  const riskLabel = document.getElementById('gv-risk-label');
  const riskText = document.getElementById('gv-risk-text');
  const onerisiText = document.getElementById('gv-ai-onerisi-text');
  if (!satirlar) return;

  fetch('/hava?sehir=' + sehir)
    .then(r => r.json())
    .then(data => {
      const temp = parseFloat(data.sicaklik || data.temp || 20);
      const ruzgar = parseFloat(data.ruzgar || data.wind || 8);
      const durum = (data.durum || data.condition || '').toLowerCase();
      const nem = parseFloat(data.nem || 60);

      // Risk hesapla
      let riskSeviye = 'DÜŞÜK';
      let riskRenk = '#16A34A'; let riskBg = '#F0FDF4'; let riskIkon = '🛡';
      let riskAciklama = 'Şu an için kritik bir hava olayı beklenmiyor. Çalışmalar güvenle devam edebilir.';
      if (ruzgar >= 30 || temp <= 0) {
        riskSeviye = 'YÜKSEK'; riskRenk = '#DC2626'; riskBg = '#FEF2F2'; riskIkon = '⛔';
        riskAciklama = ruzgar >= 30 ? 'Kuvvetli rüzgar — Vinç operasyonları durdurulmalı!' : 'Don riski — Beton dökümü tehlikeli!';
      } else if (ruzgar >= 15 || nem >= 90 || durum.includes('yağmur') || durum.includes('rain') || temp <= 5) {
        riskSeviye = 'ORTA'; riskRenk = '#D97706'; riskBg = '#FFFBEB'; riskIkon = '⚠️';
        riskAciklama = 'Dikkat edilmesi gereken hava koşulları var. Yüksekte çalışmada önlem alın.';
      }
      if (riskEl) riskEl.style.background = riskBg;
      if (riskLabel) { riskLabel.textContent = riskSeviye + ' RİSK'; riskLabel.style.color = riskRenk; }
      if (riskText) riskText.textContent = riskAciklama;

      // Tahmin tablosu (bugün + 4 gün simüle)
      const gunler = ['Bugün', 'Yarın', '2 Gün', '3 Gün', '5 Gün'];
      const ikonlar = durum.includes('yağmur') || durum.includes('rain') ? ['🌧','🌧','⛅','☀️','☀️'] :
                      ruzgar >= 15 ? ['🌬','⛅','☀️','☀️','⛅'] : ['☀️','☀️','⛅','🌧','☀️'];
      const uyarilar = [
        ruzgar >= 15 ? 'Yüksek Rüzgar - Vinç Çalışması Riskli' : 'Normal',
        ruzgar >= 12 ? 'Yüksek Rüzgar - Vinç Çalışması Riskli' : 'Normal',
        durum.includes('yağmur') ? 'Yağmur - Kazı İşleri Durdurulmalı' : 'Normal',
        'Normal', 'Normal'
      ];

      satirlar.innerHTML = gunler.map((g, i) => `
        <tr style="border-bottom:1px solid #F1F5F9;">
          <td style="padding:7px 4px; color:#0F172A; font-weight:500;">${g}</td>
          <td style="padding:7px 4px; text-align:center; font-size:1.1rem;">${ikonlar[i]}</td>
          <td style="padding:7px 4px; text-align:center; color:#0F172A;">${Math.round(temp - i * 2 + i)}°C</td>
          <td style="padding:7px 4px; text-align:center; color:#64748B;">${Math.round(ruzgar + (i % 3) - 1)} km/h</td>
          <td style="padding:7px 4px; color:${uyarilar[i] === 'Normal' ? '#16A34A' : '#D97706'}; font-size:0.75rem;">${uyarilar[i]}</td>
        </tr>
      `).join('');

      // AI Önerisi
      let oneri = 'Hava koşulları çalışma için uygun. Beton dökümü ve yüksek irtifa çalışmalarına devam edilebilir.';
      if (riskSeviye === 'YÜKSEK') oneri = 'Bugün yüksek rüzgar — vinç ve iskele çalışmaları durdurulmalı. İç mekan işlerine odaklanın.';
      else if (riskSeviye === 'ORTA') oneri = 'Öğleden sonra koşullar iyileşecek. Sabah saatlerinde yüksekte çalışmadan kaçının.';
      if (onerisiText) onerisiText.textContent = oneri;
    })
    .catch(() => {
      if (satirlar) satirlar.innerHTML = '<tr><td colspan="5" style="text-align:center; color:#94A3B8; padding:16px;">Hava durumu yüklenemedi.</td></tr>';
    });
}

function guvenlikKapat() {
  document.getElementById('guvenlikModal').style.display = 'none';
  document.querySelectorAll('.quick-btn').forEach(b => b.classList.remove('active'));
}

function guvenlikRaporuKaydet() {
  const tamam = document.querySelectorAll('#guvenlikModal .gv-check-item[data-checked="1"]').length;
  const toplam = document.querySelectorAll('#guvenlikModal .gv-check-item').length;
  showToast(`İSG raporu kaydedildi. ${tamam}/${toplam} madde tamamlandı.`, 'success');
}

function ekipmanRaporuKaydet() {
  const tamam = document.querySelectorAll('#ekipman-list .gv-check-item[data-checked="1"]').length;
  const toplam = document.querySelectorAll('#ekipman-list .gv-check-item').length;
  showToast(`Ekipman kontrol raporu kaydedildi. ${tamam}/${toplam} ekipman kontrol edildi.`, 'success');
}

function olayBildir() {
  const tur = document.getElementById('olayTur').value;
  const aciklama = document.getElementById('olayAciklama').value;
  const msg = document.getElementById('olayMsg');

  if (!aciklama.trim()) {
    if (msg) msg.innerHTML = '<span style="color:#DC2626;">Açıklama alanını doldurun.</span>';
    return;
  }

  const turEtiket = { kaza:'Kaza', ramak_kala:'Ramak Kala', hasar:'Hasar', ihlal:'İSG İhlali', yangin:'Yangın/Risk' };
  const tarih = new Date().toLocaleDateString('tr-TR');
  const yeniOlay = { tur: turEtiket[tur] || tur, aciklama, tarih, durum: 'İnceleniyor' };

  // Add to son olaylar list
  const liste = document.getElementById('sonOlaylar');
  if (liste) {
    const empty = liste.querySelector('[style*="Henüz"]');
    if (empty) empty.remove();
    const div = document.createElement('div');
    div.style.cssText = 'background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:10px 12px; font-size:0.8rem;';
    div.innerHTML = `<div style="color:#94A3B8; font-size:0.72rem;">${tarih}</div><div style="color:#0F172A; font-weight:600; margin-top:2px;">${yeniOlay.tur} — <span style="color:#64748B; font-weight:400;">${aciklama.substring(0,60)}${aciklama.length > 60 ? '...' : ''}</span></div><div style="color:#D97706; font-size:0.7rem; margin-top:3px;">${yeniOlay.durum}</div>`;
    liste.insertBefore(div, liste.firstChild);
  }

  document.getElementById('olayAciklama').value = '';
  document.getElementById('olayFotoOnizleme').innerHTML = '📷';
  if (msg) msg.innerHTML = '<span style="color:#16A34A;">✓ Olay kaydedildi.</span>';
  setTimeout(() => { if (msg) msg.innerHTML = ''; }, 3000);
  showToast('Olay bildirildi ve kaydedildi.', 'success');
}

function olayFotoSecildi(file) {
  if (!file) return;
  const prev = document.getElementById('olayFotoOnizleme');
  if (!prev) return;
  const reader = new FileReader();
  reader.onload = e => {
    prev.innerHTML = `<img src="${e.target.result}" style="max-height:80px; border-radius:6px; object-fit:cover;">`;
  };
  reader.readAsDataURL(file);
}

let _acilMapInited = false;
function acilMapYukle() {
  if (_acilMapInited) return;
  const el = document.getElementById('acilMap');
  if (!el || typeof L === 'undefined') return;
  try {
    el.innerHTML = '';
    el.style.fontSize = '';
    const map = L.map(el, { zoomControl:false, attributionControl:false }).setView([39.9, 32.8], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    L.marker([39.9, 32.8]).addTo(map);
    _acilMapInited = true;
  } catch(e) {}
}

const _acilPersonelListesi = JSON.parse(localStorage.getItem('acil_personel') || '[]');
function acilPersonelRender() {
  const liste = document.getElementById('acilPersonelListe');
  if (!liste) return;
  if (_acilPersonelListesi.length === 0) {
    liste.innerHTML = '<div style="color:#94A3B8; font-size:0.78rem; text-align:center; padding:8px;">Personel eklenmemiş.</div>';
    return;
  }
  liste.innerHTML = _acilPersonelListesi.map((p, i) => `
    <div style="display:flex; align-items:center; gap:8px; padding:8px 10px; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px;">
      <span style="font-size:1rem;">👷</span>
      <div style="flex:1; font-size:0.8rem;">
        <div style="color:#0F172A; font-weight:600;">${p.ad}</div>
        <div style="color:#64748B;">${p.tel}</div>
      </div>
      <button onclick="_acilPersonelSil(${i})" style="background:#FEF2F2; border:1px solid #FECACA; color:#DC2626; border-radius:6px; padding:2px 8px; font-size:0.72rem; cursor:pointer;">Sil</button>
    </div>
  `).join('');
}

function acilPersonelEkle() {
  const ad = document.getElementById('acilPersonelAd').value.trim();
  const tel = document.getElementById('acilPersonelTel').value.trim();
  if (!ad) { showToast('Ad Soyad girin.', 'warning'); return; }
  _acilPersonelListesi.push({ ad, tel });
  localStorage.setItem('acil_personel', JSON.stringify(_acilPersonelListesi));
  document.getElementById('acilPersonelAd').value = '';
  document.getElementById('acilPersonelTel').value = '';
  acilPersonelRender();
}

function _acilPersonelSil(i) {
  _acilPersonelListesi.splice(i, 1);
  localStorage.setItem('acil_personel', JSON.stringify(_acilPersonelListesi));
  acilPersonelRender();
}

function toplanmaKaydet() {
  const nokta = document.getElementById('toplanmaNoktasi')?.value;
  if (!nokta) { showToast('Toplanma noktası boş olamaz.', 'warning'); return; }
  localStorage.setItem('toplanma_noktasi', nokta);
  showToast('📍 Toplanma noktası kaydedildi.', 'success');
}

function sorumlKaydet() {
  const ad = document.getElementById('sorumlAd').value;
  const tel = document.getElementById('sorumlTel').value;
  if (!ad || !tel) { showToast('Ad ve telefon boş olamaz.', 'warning'); return; }
  localStorage.setItem('sorumlu_ad', ad);
  localStorage.setItem('sorumlu_tel', tel);
  showToast('👷 Sorumlu bilgileri kaydedildi.', 'success');
}

window.addEventListener('load', () => {
  if (window.location.hash === '#register') {
    switchPanel('register');
    const overlay = document.getElementById('auth-overlay');
    if (overlay) overlay.style.display = 'flex';
  }
});

// ══════════════════════════════════════════
// AI OMNI-COMMAND BAR — Yeni Fonksiyonlar
// ══════════════════════════════════════════

const AI_QUICK_COMMANDS = [
  'Çimento stoğu sorgula',
  'ISG tutanağı oluştur',
  'C Blok son durumu göster',
  'Taşeron hakedişi hesapla',
  'Bugünkü malzeme fiyatları'
];

function aiBarFocus(focused) {
  const bar = document.getElementById('aiBarInner');
  const sparkle = document.getElementById('aiSparkle');
  const quick = document.getElementById('aiQuickCommands');
  const input = document.getElementById('aiCommandInput');
  if (!bar || !sparkle || !quick || !input) return;
  if (focused) {
    bar.style.borderColor = '#6366f1';
    bar.style.boxShadow = '0 0 0 3px rgba(99,102,241,0.2)';
    sparkle.style.color = '#818cf8';
    if (!input.value.trim()) {
      aiQuickListDoldur();
      quick.style.display = 'block';
    }
  } else {
    setTimeout(() => {
      bar.style.borderColor = 'rgba(99,102,241,0.3)';
      bar.style.boxShadow = 'none';
      sparkle.style.color = 'rgba(99,102,241,0.6)';
      quick.style.display = 'none';
    }, 200);
  }
}

function aiQuickListDoldur() {
  const list = document.getElementById('aiQuickList');
  if (!list) return;
  const _cmds = JSON.parse(localStorage.getItem('ai_hizli_komutlar') || JSON.stringify(AI_QUICK_COMMANDS));
  list.innerHTML = _cmds.map(cmd => `
    <button onclick="aiCommandCalistir('${cmd}')"
      style="width:100%;display:flex;align-items:center;gap:10px;padding:10px 14px;background:none;border:none;cursor:pointer;color:#475569;font-size:13px;text-align:left;transition:background 0.15s;"
      onmouseover="this.style.background='#F8FAFC';this.style.color='#1E293B';"
      onmouseout="this.style.background='none';this.style.color='#475569';">
      <span style="color:#6366f1;font-size:12px;">⚡</span> ${cmd}
    </button>
  `).join('');
}

function aiCommandCalistir(cmd) {
  const input = document.getElementById('aiCommandInput');
  const quick = document.getElementById('aiQuickCommands');
  if (input) input.value = cmd;
  if (quick) quick.style.display = 'none';
  aiCommandGonder();
}

async function aiCommandGonder() {
  const input = document.getElementById('aiCommandInput');
  if (!input) return;
  const query = input.value.trim();
  if (!query) return;

  const token = localStorage.getItem('bai_token') || '';
  const banner = document.getElementById('aiResultBanner');
  const content = document.getElementById('aiResultContent');
  if (!banner || !content) return;

  banner.style.display = 'block';
  content.innerHTML = `<div style="display:flex;align-items:center;gap:10px;">
    <div style="display:flex;gap:4px;">
      <span style="width:7px;height:7px;background:#6366f1;border-radius:50%;display:inline-block;animation:aiBounce 0.8s infinite 0s;"></span>
      <span style="width:7px;height:7px;background:#6366f1;border-radius:50%;display:inline-block;animation:aiBounce 0.8s infinite 0.15s;"></span>
      <span style="width:7px;height:7px;background:#6366f1;border-radius:50%;display:inline-block;animation:aiBounce 0.8s infinite 0.3s;"></span>
    </div>
    <span style="color:#64748B;font-size:13px;">AI işliyor...</span>
  </div>`;
  const savedQuery = query;
  input.value = '';

  try {
    const res = await fetch('/sor', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ soru: savedQuery, token, konusma_tonu: localStorage.getItem('ai_konusma_tonu') || 'saha_arkadasi' })
    });
    const data = await res.json();
    const cevap = data.cevap || data.yanit || data.message || 'Yanıt alınamadı.';
    content.innerHTML = `<div style="display:flex;align-items:flex-start;gap:10px;">
      <span style="color:#6366f1;flex-shrink:0;margin-top:2px;">✦</span>
      <div style="flex:1;">
        <span style="font-size:11px;color:#94A3B8;margin-right:6px;">"${savedQuery}" →</span>
        <span style="font-size:13px;color:#1E293B;line-height:1.6;">${cevap}</span>
      </div>
      <button onclick="aiResultKapat()" style="background:none;border:none;cursor:pointer;color:#94A3B8;font-size:14px;flex-shrink:0;">✕</button>
    </div>`;
  } catch (err) {
    content.innerHTML = `<span style="color:rgba(239,68,68,0.8);font-size:13px;">⚠ Bağlantı hatası. Lütfen tekrar deneyin.</span>`;
  }
}

function aiResultKapat() {
  const banner = document.getElementById('aiResultBanner');
  if (banner) banner.style.display = 'none';
}

function aiMicBasildi() {
  const btn = document.getElementById('aiMicBtn');
  if (!btn) return;
  btn.style.background = 'rgba(239,68,68,0.3)';
  btn.style.color = '#ef4444';
  if (typeof baslatSesliDinleme === 'function') {
    baslatSesliDinleme((metin) => {
      const inp = document.getElementById('aiCommandInput');
      if (inp) inp.value = metin;
    });
  }
}

function aiMicBirakildi() {
  const btn = document.getElementById('aiMicBtn');
  if (!btn) return;
  btn.style.background = 'none';
  btn.style.color = '#94A3B8';
  if (typeof durdurSesliDinleme === 'function') durdurSesliDinleme();
  setTimeout(() => {
    const inp = document.getElementById('aiCommandInput');
    if (inp && inp.value.trim()) aiCommandGonder();
  }, 500);
}

function aiDosyaSecildi(input) {
  if (!input.files || !input.files[0]) return;
  const file = input.files[0];
  if (typeof kameraAnalizDosyaIle === 'function') {
    kameraAnalizDosyaIle(file);
  } else {
    showToast('Dosya alındı: ' + file.name, 'success');
  }
}

// Saha Günlüğü — /rapor_listesi son 5 kayıt
async function sahaGunluguYukle() {
  const el = document.getElementById('sahaGunluguListe');
  if (!el) return;
  const token = localStorage.getItem('bai_token') || '';
  try {
    const res = await fetch(`/rapor_listesi?token=${token}`);
    const data = await res.json();
    const raporlar = data.raporlar || data.items || data.list || [];
    if (!raporlar.length) {
      el.innerHTML = '<div style="color:#94A3B8;font-size:12px;text-align:center;padding:24px;">Henüz kayıt bulunmuyor.</div>';
      return;
    }
    const son5 = raporlar.slice(-5).reverse();
    const durumCfg = {
      'dogrulandi': { bg: '#F0FDF4', border: '#86EFAC', txt: '#16A34A', lbl: 'İşlendi',    ikon: '✓',  ikonBg: '#DCFCE7', ikonTxt: '#16A34A' },
      'uyari':      { bg: '#FFF7ED', border: '#FED7AA', txt: '#EA580C', lbl: 'Uyarı',     ikon: '⚠',  ikonBg: '#FFEDD5', ikonTxt: '#EA580C' },
      'bekleniyor': { bg: '#FEF9F0', border: '#FDE68A', txt: '#B45309', lbl: 'İşleniyor', ikon: '⏳', ikonBg: '#FEF3C7', ikonTxt: '#B45309' },
    };
    el.innerHTML = son5.map(r => {
      const baslik = typeof r === 'string' ? r : (r.baslik || r.ad || r.tip || 'Rapor');
      const zaman  = typeof r === 'string' ? '' : (r.tarih || r.zaman || '');
      const durum  = typeof r === 'object' ? ((r.durum || '').toLowerCase() || 'dogrulandi') : 'dogrulandi';
      const cfg    = durumCfg[durum] || durumCfg['dogrulandi'];
      const isKamera = baslik.toLowerCase().includes('kamera') || baslik.toLowerCase().includes('fotoğraf') || baslik.toLowerCase().includes('ocr');
      return `<div class="saha-row" style="display:flex;align-items:center;gap:12px;padding:10px 8px;border-radius:10px;transition:background 0.15s;">
        <div style="width:36px;height:36px;border-radius:8px;background:${isKamera ? '#EFF6FF' : '#F0FDF4'};display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:16px;">
          ${isKamera ? '📷' : '📄'}
        </div>
        <div style="flex:1;min-width:0;">
          <div style="font-size:13px;font-weight:500;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${baslik}</div>
          <div style="display:flex;align-items:center;gap:6px;margin-top:3px;">
            <span style="background:${cfg.ikonBg};color:${cfg.ikonTxt};font-size:10px;font-weight:600;padding:2px 7px;border-radius:20px;display:inline-flex;align-items:center;gap:3px;">
              <span>${cfg.ikon}</span> ${cfg.lbl}
            </span>
            ${zaman ? `<span style="font-size:10px;color:#94A3B8;">${zaman}</span>` : ''}
          </div>
        </div>
        ${zaman ? `<span style="font-size:11px;color:#94A3B8;flex-shrink:0;">${zaman}</span>` : ''}
      </div>`;
    }).join('');
  } catch (err) {
    el.innerHTML = '<div style="color:#EF4444;font-size:12px;text-align:center;padding:24px;">Veri alınamadı.</div>';
  }
}

// AI Uyarılar — /kullanim-durumu uyari alanı
async function aiAlertsYukle() {
  const el    = document.getElementById('aiAlertsContent');
  const badge = document.getElementById('kritikBadge');
  if (!el) return;
  const token = localStorage.getItem('bai_token') || '';
  try {
    const res  = await fetch(`/kullanim-durumu?token=${token}`);
    const data = await res.json();
    const uyarilar = data.uyarilar || data.alerts || data.warnings || [];
    if (!uyarilar.length) {
      el.innerHTML = '<div style="color:rgba(255,255,255,0.3);font-size:12px;line-height:1.7;text-align:center;padding:12px 8px;">Şu an aktif uyarı bulunmuyor.<br>Sistem tüm şantiyeleri izliyor.</div>';
      if (badge) badge.style.display = 'none';
      return;
    }
    const kritikSayi = uyarilar.filter(u => typeof u === 'object' && (u.seviye || '').toLowerCase() === 'kritik').length;
    if (badge) {
      badge.textContent = kritikSayi + ' Kritik';
      badge.style.display = kritikSayi > 0 ? 'inline-block' : 'none';
    }
    const seviyeCfg = {
      'kritik': { border: '#EF4444', bg: '#FFF5F5', ikonBg: '#FEE2E2', ikon: '⚠', txt: '#DC2626' },
      'uyari':  { border: '#F97316', bg: '#FFF7ED', ikonBg: '#FFEDD5', ikon: '⚠', txt: '#EA580C' },
      'bilgi':  { border: '#3B82F6', bg: '#EFF6FF', ikonBg: '#DBEAFE', ikon: 'ℹ', txt: '#2563EB' },
    };
    el.innerHTML = uyarilar.map(u => {
      const mesaj  = typeof u === 'string' ? u : (u.mesaj || u.message || u.text || String(u));
      const zaman  = typeof u === 'object' ? (u.zaman || u.tarih || '') : '';
      const seviye = typeof u === 'object' ? ((u.seviye || 'bilgi').toLowerCase()) : 'bilgi';
      const cfg    = seviyeCfg[seviye] || seviyeCfg['bilgi'];
      return `<div style="border-left:3px solid ${cfg.border};padding:10px 12px;background:${cfg.bg};border-radius:0 8px 8px 0;margin-bottom:2px;">
        <div style="font-size:12px;font-weight:500;color:#0F172A;line-height:1.4;">${mesaj}</div>
        ${zaman ? `<div style="font-size:10px;color:#94A3B8;margin-top:3px;">${zaman}</div>` : ''}
      </div>`;
    }).join('');
  } catch (err) {
    el.innerHTML = '<div style="color:#EF4444;font-size:12px;text-align:center;padding:24px;">Veri alınamadı.</div>';
  }
}

// ══════════════════════════════════════════
// ══════════════════════════════════════════════════
// KAMERA ANALİZİ SAYFASI — Tam Dashboard
// ══════════════════════════════════════════════════
let _kpAktifTip = 'genel';           // seçili analiz tipi
let _kpAktifChip = 'all';            // aktif filtre chip
let _kpTumAnaliz = [];               // cache
let _kpManuelKayitlar = [];          // localStorage'dan yüklenir
let _kpCameraList    = [];           // registered cameras
let _kpSortDesc      = true;         // true = en yeni önce

function kpGetVisibleAnaliz() {
  const gizli = JSON.parse(localStorage.getItem('bai_gizli_analizler') || '[]');
  return (_kpTumAnaliz || []).filter(k => !gizli.includes(k.id));
}

function kameraPageAc() {
  ['content','aiCommandBar','santiyePage','fiyatPage','stokPage','arsivPage'].forEach(pid => {
    const el = document.getElementById(pid);
    if (el) el.style.display = 'none';
  });
  const kp = document.getElementById('kameraPage');
  if (!kp) return;
  kp.style.display = 'flex';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Kamera Analizi';
  kpSantiyeBilgisiGuncelle();
  kpCameraListYukle();
  kameraPageYukle();
  kpManuelYukle();
}

// ── Santiye bilgisini üst barda güncelle (API'den çek)
let _kpSantiyeler = [];
let _kpAktifSantiye = null;

async function kpSantiyeBilgisiGuncelle() {
  const token = localStorage.getItem('bai_token');
  if (!token) return;
  try {
    const res = await fetch('/santiyeler?token=' + token);
    const data = await res.json();
    _kpSantiyeler = data.santiyeler || [];
    _kpAktifSantiye = _kpSantiyeler.find(s => s.aktif) || _kpSantiyeler[0] || null;
    kpProjeBarGuncelle();
  } catch(e) {}
}

function kpProjeBarGuncelle() {
  const nameEl   = document.getElementById('kpAktifProjeName');
  const durEl    = document.getElementById('kpSantiyeDurum');
  const konumEl  = document.getElementById('kpSantiyeKonum');
  const konumTxt = document.getElementById('kpSantiyeKonumText');
  const adetEl   = document.getElementById('kpAktifKameraAdet');
  if (!_kpAktifSantiye) {
    if (nameEl) nameEl.textContent = 'Şantiye seçin...';
    return;
  }
  if (nameEl) nameEl.textContent = _kpAktifSantiye.ad || '—';
  if (durEl)  durEl.style.display = 'inline-flex';
  if (_kpAktifSantiye.konum && konumEl && konumTxt) {
    konumTxt.textContent = _kpAktifSantiye.konum;
    konumEl.style.display = 'inline-flex';
  }
}

function kpProjeDropdownAc() {
  let dd = document.getElementById('kpProjeDropdownMenu');
  if (dd) { dd.style.display = dd.style.display === 'none' ? 'block' : 'none'; return; }
  // İlk kez oluştur
  dd = document.createElement('div');
  dd.id = 'kpProjeDropdownMenu';
  dd.style.cssText = 'position:absolute;top:calc(100% + 6px);left:0;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,0.12);z-index:600;min-width:240px;overflow:hidden;';
  const anchor = document.getElementById('kpProjeAnchor');
  if (!anchor) return;
  anchor.style.position = 'relative';
  anchor.appendChild(dd);
  kpProjeDropdownRender(dd);
  setTimeout(() => {
    document.addEventListener('click', function handler(e) {
      if (!anchor.contains(e.target)) {
        dd.style.display = 'none';
        document.removeEventListener('click', handler);
      }
    });
  }, 0);
}

function kpProjeDropdownRender(dd) {
  if (_kpSantiyeler.length === 0) {
    dd.innerHTML = '<div style="padding:14px 16px;font-size:13px;color:#94A3B8;text-align:center;">Henüz şantiye eklenmemiş</div>';
    return;
  }
  dd.innerHTML = _kpSantiyeler.map(s =>
    '<button onclick="kpProjeSec(' + s.id + ')" style="display:flex;align-items:center;gap:10px;width:100%;padding:10px 14px;background:' + ((_kpAktifSantiye && s.id === _kpAktifSantiye.id) ? '#F8FAFC' : 'transparent') + ';border:none;cursor:pointer;text-align:left;" onmouseover="this.style.background=\'#F8FAFC\'" onmouseout="this.style.background=\'' + ((_kpAktifSantiye && s.id === _kpAktifSantiye.id) ? '#F8FAFC' : 'transparent') + '\'">'
    + '<div style="width:8px;height:8px;border-radius:50%;background:#10B981;flex-shrink:0;"></div>'
    + '<div style="flex:1;min-width:0;"><div style="font-size:13px;font-weight:600;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + s.ad + '</div>'
    + (s.konum ? '<div style="font-size:11px;color:#94A3B8;">' + s.konum + '</div>' : '')
    + '</div>'
    + ((_kpAktifSantiye && s.id === _kpAktifSantiye.id) ? '<svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#10B981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>' : '')
    + '</button>'
  ).join('');
}

function kpProjeSec(id) {
  _kpAktifSantiye = _kpSantiyeler.find(s => s.id === id) || _kpAktifSantiye;
  kpProjeBarGuncelle();
  const dd = document.getElementById('kpProjeDropdownMenu');
  if (dd) dd.style.display = 'none';
  kpCameraListYukle();
  kameraPageYukle();
}

// ── Kamera grid görüntüleme modu
function kpKameraGoruntuleme(mod) {
  const grid = document.getElementById('kpCameraGrid');
  if (!grid) return;
  const gridBtn = document.getElementById('kpGridBtn');
  const listBtn = document.getElementById('kpListBtn');
  if (mod === 'grid') {
    grid.style.gridTemplateColumns = 'repeat(3,1fr)';
    if (gridBtn) { gridBtn.style.background='#0F172A'; }
    if (listBtn) { listBtn.style.background='#F1F5F9'; }
  } else {
    grid.style.gridTemplateColumns = '1fr';
    if (gridBtn) { gridBtn.style.background='#F1F5F9'; }
    if (listBtn) { listBtn.style.background='#0F172A'; }
  }
}

function kpKameraFullscreen() {
  const el = document.getElementById('kpCameraGrid');
  if (el && el.requestFullscreen) el.requestFullscreen();
}

// ── Yeni kamera ekle modal
function yeniKameraEkleAc() {
  const modal = document.getElementById('yeniKameraModal');
  if (modal) { modal.style.display = 'flex'; }
  ['ykAd','ykUrl','ykKonum'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
}

function yeniKameraKapat() {
  const modal = document.getElementById('yeniKameraModal');
  if (modal) modal.style.display = 'none';
}

async function yeniKameraKaydet() {
  const ad = (document.getElementById('ykAd') || {}).value?.trim();
  if (!ad) { showToast('Kamera adı zorunludur.', 'error'); return; }
  const url    = (document.getElementById('ykUrl')   || {}).value?.trim() || '';
  const konum  = (document.getElementById('ykKonum') || {}).value?.trim() || '';
  const tip    = (document.getElementById('ykTip')   || {}).value || 'ip';
  const token  = localStorage.getItem('bai_token');
  const btn    = document.getElementById('ykKaydetBtn');
  if (btn) { btn.disabled = true; btn.textContent = 'Kaydediliyor...'; }
  try {
    const res  = await fetch('/cameras', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, name: ad, url, location: konum, tip })
    });
    if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Hata'); }
    showToast('Kamera eklendi!', 'success');
    yeniKameraKapat();
    kpCameraListYukle();
  } catch(e) {
    showToast('Hata: ' + e.message, 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = 'Kamera Kaydet'; }
  }
}

// ── Kamera listesi yükle ve render et
async function kpCameraListYukle() {
  const token = localStorage.getItem('bai_token');
  if (!token) return;
  try {
    const res  = await fetch('/cameras?token=' + token);
    _kpCameraList = res.ok ? await res.json() : [];
    kpRenderCameraGrid(_kpCameraList);
    const aktif = _kpCameraList.filter(c => c.aktif).length;
    const adetEl = document.getElementById('kpAktifKameraAdet');
    if (adetEl) adetEl.textContent = aktif;
  } catch(e) { _kpCameraList = []; kpRenderCameraGrid([]); }
}

function kpRenderCameraGrid(liste) {
  const grid  = document.getElementById('kpCameraGrid');
  const empty = document.getElementById('kpCameraEmpty');
  if (!grid) return;
  if (empty) empty.style.display = 'none';
  grid.style.display = 'block';

  const headerHtml = '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
    + '<div style="padding:14px 18px;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between;">'
    + '<div style="display:flex;align-items:center;gap:8px;">'
    + '<span style="display:inline-block;width:8px;height:8px;background:#EF4444;border-radius:50%;animation:kpPulse 2s infinite;flex-shrink:0;"></span>'
    + '<span style="font-size:13px;font-weight:700;color:#0F172A;">Canlı Kamera İzleme</span>'
    + '</div>'
    + '<div style="display:flex;align-items:center;gap:6px;">'
    + '<button title="Izgara görünümü" style="width:30px;height:30px;display:flex;align-items:center;justify-content:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:7px;cursor:pointer;color:#64748B;"><svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg></button>'
    + '<button title="Liste görünümü" style="width:30px;height:30px;display:flex;align-items:center;justify-content:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:7px;cursor:pointer;color:#64748B;"><svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg></button>'
    + '<button title="Tam ekran" style="width:30px;height:30px;display:flex;align-items:center;justify-content:center;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:7px;cursor:pointer;color:#64748B;"><svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg></button>'
    + '</div></div>'
    + '<div style="padding:14px;display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">';

  if (!liste || liste.length === 0) {
    const placeholders = ['CAM-01 ANA GİRİŞ','CAM-02 AÇIK DEPO','CAM-03 KUZEY CEPHE','CAM-04 BATI CEPHE','CAM-05 İÇ ALAN','CAM-06 GÜNEY GİRİŞ'];
    grid.innerHTML = headerHtml + placeholders.map(label => `
      <div onclick="yeniKameraEkleAc()" title="Kamera eklemek için tıklayın"
        style="position:relative;background:linear-gradient(135deg,#0F172A 0%,#1E293B 100%);border-radius:12px;overflow:hidden;height:120px;display:flex;flex-direction:column;justify-content:space-between;border:1px solid #334155;cursor:pointer;transition:border-color 0.2s;"
        onmouseover="this.style.borderColor='#F97316'" onmouseout="this.style.borderColor='#334155'">
        <div style="flex:1;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:6px;padding:12px;">
          <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="#334155" stroke-width="1.5"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>
          <div style="font-size:10px;color:#475569;font-weight:600;">Kamera Ekle</div>
        </div>
        <div style="padding:7px 10px;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:space-between;">
          <div style="font-size:10px;font-weight:700;color:#64748B;text-transform:uppercase;letter-spacing:0.06em;">${label}</div>
          <span style="display:inline-block;width:6px;height:6px;background:#334155;border-radius:50%;"></span>
        </div>
      </div>
    `).join('') + '</div></div>';
    return;
  }

  const tipIkon = { ip: '📡', rtsp: '🔴', http: '🌐', usb: '🎥' };
  grid.innerHTML = headerHtml + liste.map(c => `
    <div style="position:relative;background:#0F172A;border-radius:12px;overflow:hidden;height:120px;display:flex;flex-direction:column;justify-content:space-between;border:1px solid #1E293B;cursor:pointer;transition:border-color 0.2s;"
      onmouseover="this.style.borderColor='#F97316'" onmouseout="this.style.borderColor='#1E293B'">
      <div style="flex:1;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:6px;">
        <div style="font-size:24px;">${tipIkon[c.tip] || '📷'}</div>
        <div style="font-size:10px;color:#475569;font-weight:600;text-align:center;padding:0 8px;">${c.url ? c.url.substring(0,30) + (c.url.length>30?'...':'') : 'URL tanımlı değil'}</div>
      </div>
      <div style="padding:8px 10px;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:space-between;">
        <div>
          <div style="font-size:11px;font-weight:700;color:#FFFFFF;text-transform:uppercase;letter-spacing:0.04em;">${c.name}</div>
          ${c.location ? `<div style="font-size:10px;color:#64748B;margin-top:1px;">${c.location}</div>` : ''}
        </div>
        <div style="display:flex;align-items:center;gap:6px;">
          <span style="display:inline-block;width:6px;height:6px;background:${c.aktif?'#10B981':'#EF4444'};border-radius:50%;animation:${c.aktif?'kpPulse 2s infinite':'none'}"></span>
          <button onclick="event.stopPropagation();kpCameraSil(${c.id},'${c.name.replace(/'/g,'')}')" title="Sil"
            style="background:none;border:none;color:#EF4444;cursor:pointer;padding:2px;opacity:0.7;transition:opacity 0.15s;"
            onmouseover="this.style.opacity='1'" onmouseout="this.style.opacity='0.7'">
            <svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>
          </button>
        </div>
      </div>
    </div>
  `).join('') + '</div></div>';
}

async function kpCameraSil(id, ad) {
  if (!confirm(`"${ad}" kamerasını silmek istediğinize emin misiniz?`)) return;
  const token = localStorage.getItem('bai_token');
  try {
    const res = await fetch('/cameras/' + id + '?token=' + token, { method: 'DELETE' });
    if (!res.ok) throw new Error((await res.json()).detail || 'Hata');
    showToast('Kamera silindi.', 'success');
    kpCameraListYukle();
  } catch(e) { showToast('Hata: ' + e.message, 'error'); }
}

function kameraPageKapat() {
  const kp = document.getElementById('kameraPage');
  if (kp) kp.style.display = 'none';
  const content = document.getElementById('content');
  const cmdBar  = document.getElementById('aiCommandBar');
  if (content) content.style.display = 'flex';
  if (cmdBar)  cmdBar.style.display  = 'block';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Genel Bakış';
}

function kameraKatSec(tip) {
  _kpAktifTip = tip;
  ['guvenlik','ilerleme','genel'].forEach(t => {
    const btn = document.getElementById('katBtn-' + t);
    if (!btn) return;
    if (t === tip) {
      btn.classList.add('active-kat');
      if (t === 'guvenlik') { btn.style.borderColor='#F59E0B'; btn.style.background='#FEF3C7'; btn.style.color='#D97706'; }
      else if (t === 'ilerleme') { btn.style.borderColor='#3B82F6'; btn.style.background='#EFF6FF'; btn.style.color='#2563EB'; }
      else { btn.style.borderColor='#3B82F6'; btn.style.background='#EFF6FF'; btn.style.color='#2563EB'; }
    } else {
      btn.classList.remove('active-kat');
      btn.style.borderColor='#E2E8F0'; btn.style.background='#FFFFFF'; btn.style.color='#475569';
    }
  });
}

function kameraChipSec(chip, el) {
  _kpAktifChip = chip;
  document.querySelectorAll('.kamera-chip').forEach(b => {
    b.style.background=''; b.style.borderColor=''; b.style.color=''; b.style.fontWeight='600';
  });
  if (el) { el.style.borderColor='#0F172A'; el.style.background='#0F172A'; el.style.color='white'; }
  kpRenderAiKartlar(_kpTumAnaliz);
}

// ── Kart Detay Modal — 3 bölüm: YOLO işaretli foto | YOLO özeti | AI metin
async function kpKartDetayGoster(id) {
  const token = localStorage.getItem('bai_token');
  let modal = document.getElementById('kpKartDetayModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'kpKartDetayModal';
    modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:9500;display:flex;align-items:center;justify-content:center;padding:16px;backdrop-filter:blur(6px);';
    modal.onclick = e => { if (e.target === modal) kpKartDetayKapat(); };
    document.body.appendChild(modal);
  }
  modal.style.display = 'flex';
  modal.innerHTML = '<div style="background:#0F172A;border-radius:20px;width:100%;max-width:720px;max-height:92vh;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 28px 80px rgba(0,0,0,0.55);">'
    + '<div style="display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid rgba(255,255,255,0.07);flex-shrink:0;">'
    + '<div style="display:flex;align-items:center;gap:8px;">'
    + '<div style="width:8px;height:8px;border-radius:50%;background:#818cf8;"></div>'
    + '<span style="font-size:14px;font-weight:700;color:#E2E8F0;">AI + YOLO Analiz Detayı</span>'
    + '</div>'
    + '<button onclick="kpKartDetayKapat()" style="width:32px;height:32px;background:rgba(255,255,255,0.08);border:none;border-radius:8px;cursor:pointer;font-size:18px;color:#94A3B8;display:flex;align-items:center;justify-content:center;line-height:1;">×</button>'
    + '</div>'
    + '<div id="kpKartDetayIcerik" style="overflow-y:auto;flex:1;padding:20px;">'
    + '<div style="text-align:center;padding:48px;color:#475569;font-size:13px;">Yükleniyor...</div>'
    + '</div></div>';

  // Yerel önbellekten oku
  const thumb   = localStorage.getItem('bai_thumb_' + id);
  const yoloRaw = localStorage.getItem('bai_yolo_'  + id);
  const yolo    = yoloRaw ? (() => { try { return JSON.parse(yoloRaw); } catch(e) { return null; } })() : null;

  // Sunucudan AI içerik çek
  let aiContent = '', aiTip = 'genel', tarih = '';
  try {
    const res  = await fetch('/arsiv/kamera/' + id + '?token=' + token);
    const data = await res.json();
    aiContent = data.content || data.sonuc || '';
    aiTip  = data.analiz_tipi || 'genel';
    tarih  = data.created_at ? new Date(data.created_at).toLocaleString('tr-TR') : '';
  } catch(e) { /* sunucu hatası — içerik boş kalır */ }

  const riskLevel = yolo ? yolo.risk_level : null;
  const riskRenk  = riskLevel === 'YÜKSEK' ? '#ef4444' : riskLevel === 'ORTA' ? '#f59e0b' : '#22c55e';
  const tipRenk   = aiTip === 'guvenlik' ? '#D97706' : aiTip === 'ilerleme' ? '#2563EB' : '#7C3AED';
  const tipEtiket = aiTip === 'guvenlik' ? 'İş Güvenliği' : aiTip === 'ilerleme' ? 'İlerleme Takibi' : 'Genel Analiz';

  // ── Bölüm 1: YOLO işaretli fotoğraf
  const imgHtml = thumb
    ? '<img src="' + thumb + '" style="width:100%;border-radius:12px;display:block;max-height:360px;object-fit:contain;background:#0a0f1a;">'
    : '<div style="height:180px;background:linear-gradient(135deg,#1E293B,#0F172A);border-radius:12px;display:flex;align-items:center;justify-content:center;">'
      + '<svg width="48" height="48" fill="none" viewBox="0 0 24 24" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg></div>';

  // ── Bölüm 2: YOLO özeti
  const yoloHtml = yolo ? (
    '<div style="background:rgba(129,140,248,0.08);border:1px solid rgba(129,140,248,0.2);border-radius:14px;padding:16px;margin-bottom:14px;">'
    + '<div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">'
    + '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>'
    + '<span style="font-size:11px;font-weight:800;color:#818cf8;text-transform:uppercase;letter-spacing:1px;">YOLO Yerel Analiz</span>'
    + '<span style="margin-left:auto;font-size:10px;color:#475569;">Conf: ' + ((yolo.confidence||0)*100).toFixed(0) + '%</span>'
    + '</div>'
    + '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:' + ((yolo.violations||[]).length || yolo.kisi_sayisi > 0 ? '14px' : '0') + ';">'
    + '<div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">'
    + '<div style="font-size:16px;font-weight:800;color:' + riskRenk + ';">' + (riskLevel || '—') + '</div>'
    + '<div style="font-size:9px;color:#64748B;margin-top:3px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;">RİSK</div></div>'
    + '<div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">'
    + '<div style="font-size:16px;font-weight:800;color:#f1f5f9;">' + (yolo.kisi_sayisi||0) + '</div>'
    + '<div style="font-size:9px;color:#64748B;margin-top:3px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;">KİŞİ</div></div>'
    + '<div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">'
    + '<div style="font-size:16px;font-weight:800;color:#34d399;">' + (yolo.ppe_uyum_orani >= 0 ? '%' + Math.round(yolo.ppe_uyum_orani*100) : '?') + '</div>'
    + '<div style="font-size:9px;color:#64748B;margin-top:3px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;">PPE UYUM</div></div>'
    + '</div>'
    + ((yolo.violations||[]).length
        ? '<div><div style="font-size:10px;color:#64748B;font-weight:700;text-transform:uppercase;letter-spacing:.7px;margin-bottom:7px;">İHLALLER</div>'
          + '<div style="display:flex;flex-wrap:wrap;gap:5px;">'
          + (yolo.violations||[]).map(v => '<span style="background:rgba(239,68,68,0.15);color:#fca5a5;border:1px solid rgba(239,68,68,0.3);border-radius:6px;padding:3px 9px;font-size:11px;font-weight:600;">' + v + '</span>').join('')
          + '</div></div>'
        : '<div style="font-size:12px;color:#86efac;">✓ İhlal tespit edilmedi</div>')
    + '</div>'
  ) : '';

  // ── Bölüm 3: AI analiz metni
  const icerikHtml = typeof markdownToHtml === 'function'
    ? markdownToHtml(aiContent)
    : '<pre style="white-space:pre-wrap;font-family:inherit;">' + aiContent + '</pre>';

  document.getElementById('kpKartDetayIcerik').innerHTML =
    // Fotoğraf
    '<div style="margin-bottom:14px;">' + imgHtml + '</div>'
    // Meta satır
    + '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px;margin-bottom:14px;">'
    + '<span style="background:' + tipRenk + ';color:white;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;">' + tipEtiket + '</span>'
    + '<span style="font-size:11px;color:#475569;">' + tarih + '</span>'
    + '</div>'
    // YOLO özeti
    + yoloHtml
    // AI metin
    + '<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:16px;">'
    + '<div style="font-size:10px;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:.8px;margin-bottom:10px;">AI Analiz Raporu</div>'
    + '<div style="font-size:13px;color:#CBD5E1;line-height:1.75;">' + icerikHtml + '</div>'
    + '</div>'
    // Butonlar
    + '<div style="margin-top:16px;display:flex;gap:8px;justify-content:flex-end;">'
    + '<button onclick="kpAnalizGizle(' + id + ');kpKartDetayKapat()" style="font-size:12px;font-weight:600;color:#EF4444;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);padding:7px 14px;border-radius:8px;cursor:pointer;">Sil</button>'
    + '<button onclick="kpKartDetayKapat()" style="font-size:12px;font-weight:700;color:white;background:#818cf8;border:none;padding:7px 20px;border-radius:8px;cursor:pointer;">Kapat</button>'
    + '</div>';
}

function kpKartDetayKapat() {
  const modal = document.getElementById('kpKartDetayModal');
  if (modal) modal.style.display = 'none';
}

function kpSortToggle() {
  _kpSortDesc = !_kpSortDesc;
  const btn = document.getElementById('kpSortBtn');
  if (btn) btn.textContent = _kpSortDesc ? '↓ En Yeni' : '↑ En Eski';
  kpRenderAiKartlar(_kpTumAnaliz);
}

// ── Analiz sil (server-side + client-side)
async function kpAnalizGizle(id) {
  const token = localStorage.getItem('bai_token');
  try {
    const res = await fetch('/kanit-sil/' + id + '?token=' + token, { method: 'DELETE' });
    if (!res.ok) throw new Error('Silinemedi');
  } catch(e) {
    showToast('Silme başarısız: ' + e.message, 'error');
    return;
  }
  // Sunucudan silindi, artık local cache'den de çıkar
  _kpTumAnaliz = (_kpTumAnaliz || []).filter(k => k.id !== id);
  localStorage.removeItem('bai_thumb_' + id);
  localStorage.removeItem('bai_yolo_'  + id);
  // Gizli listesinden de temizle (artık tamamen silindi)
  try {
    const gizli = JSON.parse(localStorage.getItem('bai_gizli_analizler') || '[]');
    localStorage.setItem('bai_gizli_analizler', JSON.stringify(gizli.filter(x => x !== id)));
  } catch(e) {}
  kpRenderAiKartlar(_kpTumAnaliz);
  const visible = kpGetVisibleAnaliz();
  kpRenderTespitAkisi(visible);
  kpRenderStats(visible);
  showToast('Kayıt silindi', 'success');
}

function kpFotoDropdownToggle() {
  const dd = document.getElementById('kpFotoDropdown');
  if (!dd) return;
  const isOpen = dd.style.display !== 'none';
  dd.style.display = isOpen ? 'none' : 'block';
  if (!isOpen) {
    setTimeout(() => {
      document.addEventListener('click', function handler(e) {
        if (!e.target.closest('[data-foto-dropdown]')) {
          dd.style.display = 'none';
          document.removeEventListener('click', handler);
        }
      });
    }, 0);
  }
}

function kameraFotoInputAc() {
  const inp = document.getElementById('kameraPageFileInput');
  if (inp) inp.click();
}

function kameraPageCamAc() {
  kameraKatSec(_kpAktifTip);
  kameraAc(_kpAktifTip);
}

// Bbox çizili thumbnail üret — bbox coords absolute pixels in original image
function kpBboxThumb(base64, tespitler) {
  return new Promise(resolve => {
    const img = new Image();
    img.onload = () => {
      const MAX = 640;
      const scale = Math.min(1, MAX / Math.max(img.width, img.height, 1));
      const w = Math.round(img.width  * scale);
      const h = Math.round(img.height * scale);
      const canvas = document.createElement('canvas');
      canvas.width = w; canvas.height = h;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, w, h);
      (tespitler || []).forEach(t => {
        if (!t.bbox || t.bbox.length < 4) return;
        const [x1, y1, x2, y2] = t.bbox;
        const cls = (t.class || '').toLowerCase();
        const isViol = cls.startsWith('no_') || cls.includes('without');
        const isOk   = !isViol && (cls === 'hardhat' || cls === 'helmet' || cls.includes('vest') || cls.includes('safety'));
        const color  = isViol ? '#ef4444' : isOk ? '#22c55e' : '#f59e0b';
        const sx1 = x1*scale, sy1 = y1*scale, sw = (x2-x1)*scale, sh = (y2-y1)*scale;
        ctx.strokeStyle = color; ctx.lineWidth = 2;
        ctx.strokeRect(sx1, sy1, sw, sh);
        const label = cls.replace(/_/g,' ') + ' ' + Math.round((t.confidence||0)*100) + '%';
        ctx.font = 'bold 11px sans-serif';
        const tw = ctx.measureText(label).width;
        ctx.fillStyle = color;
        ctx.fillRect(sx1, Math.max(0, sy1-16), tw+6, 16);
        ctx.fillStyle = '#fff';
        ctx.fillText(label, sx1+3, Math.max(13, sy1-3));
      });
      resolve(canvas.toDataURL('image/jpeg', 0.82));
    };
    img.onerror = () => resolve('data:image/jpeg;base64,' + base64);
    img.src = 'data:image/jpeg;base64,' + base64;
  });
}

async function kameraPageDosyaAnalizEt(event) {
  const file = event.target.files[0];
  if (!file) return;
  const loading = document.getElementById('kpAnalysisLoading');
  if (loading) loading.style.display = 'block';

  const base64 = await new Promise((res, rej) => {
    const r = new FileReader();
    r.onload = e => res(e.target.result.split(',')[1]);
    r.onerror = rej;
    r.readAsDataURL(file);
  });
  const token = localStorage.getItem('bai_token');
  const imgData = 'data:image/jpeg;base64,' + base64;

  const container = document.getElementById('kpAiKartlar');
  const empty = document.getElementById('kpAiEmpty');
  if (container) {
    container.style.display = 'grid';
    if (empty) empty.style.display = 'none';
    const tempCard = document.createElement('div');
    tempCard.id = 'kpTempCard';
    tempCard.style.cssText = 'background:#FFFFFF;border:1px solid #E2E8F0;border-left:4px solid #6366f1;border-radius:14px;overflow:hidden;';
    tempCard.innerHTML = `
      <div style="height:130px;overflow:hidden;position:relative;background:#0F172A;display:flex;align-items:center;justify-content:center;">
        <img src="${imgData}" style="width:100%;height:100%;object-fit:cover;opacity:0.5;">
        <div style="position:absolute;display:flex;flex-direction:column;align-items:center;gap:8px;">
          <div style="width:24px;height:24px;border:3px solid #6366f1;border-top-color:transparent;border-radius:50%;animation:spin 0.8s linear infinite;"></div>
          <span style="color:white;font-size:11px;font-weight:600;">AI Analiz Ediyor...</span>
        </div>
      </div>
      <div style="padding:12px 14px;">
        <div style="height:10px;background:#F1F5F9;border-radius:5px;margin-bottom:8px;"></div>
        <div style="height:8px;background:#F1F5F9;border-radius:5px;width:70%;"></div>
      </div>`;
    container.insertBefore(tempCard, container.firstChild);
  }

  const [aiSettled, yoloSettled] = await Promise.allSettled([
    kpAnalizGonder(base64, _kpAktifTip),
    fetch('/yolo/frame', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, resim_base64: base64, santiye_id: null })
    }).then(r => r.ok ? r.json() : null).catch(() => null)
  ]);

  const aiData = aiSettled.status === 'fulfilled' ? aiSettled.value : null;
  const yoloData = yoloSettled.status === 'fulfilled' ? yoloSettled.value : null;

  const tc = document.getElementById('kpTempCard');
  if (tc) tc.remove();
  if (loading) loading.style.display = 'none';
  event.target.value = '';

  if (aiData && aiData.analiz_id) {
    const tespitler = (yoloData && yoloData.tespitler) ? yoloData.tespitler : [];
    const annotated = await kpBboxThumb(base64, tespitler).catch(() => imgData);
    localStorage.setItem('bai_thumb_' + aiData.analiz_id, annotated);
    if (yoloData) {
      try { localStorage.setItem('bai_yolo_' + aiData.analiz_id, JSON.stringify(yoloData)); } catch(e) {}
    }
  }

  await kameraPageYukle();
}

function _yoloStatKutu(deger, renk, etiket) {
  return `<div style="background:rgba(255,255,255,0.04);border-radius:9px;padding:9px;text-align:center;">
    <div style="font-size:15px;font-weight:800;color:${renk};line-height:1;">${deger}</div>
    <div style="font-size:9px;color:#64748b;margin-top:3px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;">${etiket}</div>
  </div>`;
}

async function kpAnalizGonder(base64, analiz_tipi) {
  const token = localStorage.getItem('bai_token');
  const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'İstanbul';
  const hava  = '';
  try {
    const res = await fetch('/kamera-analiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, resim_base64: base64, analiz_tipi, hava, sehir, dil: aktifDil })
    });
    const data = await res.json();
    if (!res.ok) {
      if (res.status === 429) {
        showToast('Limit doldu: ' + (data.detail || ''), 'error');
      } else if (res.status === 503) {
        showToast('AI servisi şu an yoğun, lütfen tekrar deneyin.', 'error');
      } else {
        showToast('Analiz hatası: ' + (data.detail || res.status), 'error');
      }
      return null;
    }
    showToast('AI analiz tamamlandı!', 'success');
    return data;
  } catch(e) {
    showToast('Analiz hatası: ' + e.message, 'error');
    return null;
  }
}

async function kameraPageYukle() {
  const token = localStorage.getItem('bai_token');
  if (!token) return;
  try {
    const res  = await fetch('/arsiv?token=' + token);
    const data = await res.json();
    _kpTumAnaliz = data.kamera_analizler || [];
    kpRenderAiKartlar(_kpTumAnaliz);
    kpRenderTespitAkisi(_kpTumAnaliz);
    kpRenderStats(_kpTumAnaliz);
    kpLimitGuncelle();
    // Analiz günlerini hesapla
    const gunEl = document.getElementById('kpAnalizGunAdet');
    if (gunEl && _kpTumAnaliz.length > 0) {
      const dates = _kpTumAnaliz.map(k => new Date(k.created_at).toDateString());
      const uniqueDays = new Set(dates).size;
      gunEl.textContent = uniqueDays;
    }
  } catch(e) {}
}

function kpRenderAiKartlar(liste) {
  const container = document.getElementById('kpAiKartlar');
  const empty     = document.getElementById('kpAiEmpty');
  const badge     = document.getElementById('kpAiBadge');
  if (!container) return;

  let filtreli = [...liste];
  if (_kpAktifChip !== 'all') filtreli = filtreli.filter(k => k.tip === _kpAktifChip);
  const arama = (document.getElementById('kameraArama') || {}).value || '';
  if (arama.trim()) {
    filtreli = filtreli.filter(k =>
      (k.ozet||'').toLowerCase().includes(arama.toLowerCase()) ||
      (k.tip||'').toLowerCase().includes(arama.toLowerCase()) ||
      (k.sehir||'').toLowerCase().includes(arama.toLowerCase())
    );
  }
  const gizli = JSON.parse(localStorage.getItem('bai_gizli_analizler') || '[]');
  const gorunen = filtreli.filter(k => !gizli.includes(k.id));

  // Tarihe göre sırala
  gorunen.sort((a, b) => {
    const da = new Date(a.created_at||0), db = new Date(b.created_at||0);
    return _kpSortDesc ? db - da : da - db;
  });

  if (badge) badge.textContent = gorunen.length;
  if (gorunen.length === 0) {
    container.style.display = 'none';
    if (empty) empty.style.display = 'block';
    kpRenderTespitAkisi([]);
    kpRenderStats([]);
    return;
  }
  container.style.display = 'block';
  if (empty) empty.style.display = 'none';
  kpRenderTespitAkisi(gorunen);
  kpRenderStats(gorunen);

  const sectionHeader = '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">'
    + '<div style="display:flex;align-items:center;gap:8px;">'
    + '<svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="#2563EB" stroke-width="2"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg>'
    + '<span style="font-size:13px;font-weight:700;color:#0F172A;">AI Anlık Fotoğraf Kanıtları</span>'
    + '</div>'
    + '<button onclick="kpTumunuArsivle()" style="font-size:11px;font-weight:700;color:#2563EB;background:none;border:none;cursor:pointer;padding:4px 8px;border-radius:6px;white-space:nowrap;" onmouseover="this.style.background=\'#EFF6FF\'" onmouseout="this.style.background=\'none\'">TÜMÜNÜ ARŞİVLE</button>'
    + '</div>'
    + '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;">';

  const cardsHtml = gorunen.map(k => {
    let yolo = null;
    try { const raw = localStorage.getItem('bai_yolo_' + k.id); if (raw) yolo = JSON.parse(raw); } catch(e) {}
    const riskLevel = yolo ? yolo.risk_level : null;
    const riskRenk  = riskLevel === 'YÜKSEK' ? '#ef4444' : riskLevel === 'ORTA' ? '#f59e0b' : '#22c55e';

    const tip    = k.tip || 'genel';
    const renk   = tip === 'guvenlik' ? '#D97706' : tip === 'ilerleme' ? '#2563EB' : '#7C3AED';
    const gradA  = tip === 'guvenlik' ? '#78350F' : tip === 'ilerleme' ? '#1E3A5F' : '#2E1065';
    const gradB  = tip === 'guvenlik' ? '#D97706' : tip === 'ilerleme' ? '#1D4ED8' : '#6D28D9';
    const etiket = tip === 'guvenlik' ? 'GÜVENLİK' : tip === 'ilerleme' ? 'İLERLEME' : 'GENEL';

    const dt       = k.created_at ? new Date(k.created_at) : null;
    const tarihGun = dt ? dt.toLocaleDateString('tr-TR', {day:'2-digit',month:'short'}) : '';
    const tarihSat = dt ? dt.toLocaleTimeString('tr-TR', {hour:'2-digit',minute:'2-digit'}) : '';
    const baslik   = (k.ozet||'').replace(/#{1,6}\s*/g,'').replace(/\*\*/g,'').replace(/\*/g,'').split('.')[0].substring(0,52);
    const konum    = k.sehir || '';

    const thumb    = localStorage.getItem('bai_thumb_' + k.id);
    const thumbHtml = thumb
      ? '<img src="' + thumb + '" style="width:100%;height:100%;object-fit:cover;">'
      : '<div style="width:100%;height:100%;background:linear-gradient(135deg,' + gradA + ',' + gradB + ');display:flex;align-items:center;justify-content:center;">'
        + '<svg width="28" height="28" fill="none" viewBox="0 0 24 24" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg></div>';

    const yoloSatir = yolo
      ? '<div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:8px;">'
        + '<span style="background:#F1F5F9;color:#475569;font-size:10px;font-weight:600;padding:2px 6px;border-radius:6px;">👤 ' + (yolo.kisi_sayisi||0) + '</span>'
        + (yolo.ppe_uyum_orani >= 0 ? '<span style="background:#F0FDF4;color:#16A34A;font-size:10px;font-weight:600;padding:2px 6px;border-radius:6px;">PPE %' + Math.round(yolo.ppe_uyum_orani*100) + '</span>' : '')
        + ((yolo.violations||[]).length ? '<span style="background:#FEF2F2;color:#DC2626;font-size:10px;font-weight:600;padding:2px 6px;border-radius:6px;">⚠ ' + yolo.violations.length + ' ihlal</span>' : '<span style="background:#F0FDF4;color:#16A34A;font-size:10px;font-weight:600;padding:2px 6px;border-radius:6px;">✓ Temiz</span>')
        + '</div>'
      : '';

    return '<div onclick="kpKartDetayGoster(' + k.id + ')" style="background:#FFFFFF;border:1px solid #E2E8F0;border-left:4px solid ' + renk + ';border-radius:14px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.06);cursor:pointer;transition:all 0.15s;" onmouseover="this.style.boxShadow=\'0 6px 20px rgba(0,0,0,0.10)\';this.style.transform=\'translateY(-2px)\'" onmouseout="this.style.boxShadow=\'0 1px 4px rgba(0,0,0,0.06)\';this.style.transform=\'none\'">'
      + '<div style="height:130px;overflow:hidden;position:relative;">' + thumbHtml
      + '<div style="position:absolute;bottom:0;left:0;right:0;padding:6px 10px;background:linear-gradient(transparent,rgba(0,0,0,0.78));display:flex;align-items:center;justify-content:space-between;">'
      + '<span style="font-size:10px;font-weight:800;color:white;background:' + renk + ';padding:2px 8px;border-radius:20px;letter-spacing:0.04em;">' + etiket + '</span>'
      + '<span style="font-size:10px;color:rgba(255,255,255,0.88);font-weight:600;">' + tarihGun + ' ' + tarihSat + '</span>'
      + '</div>'
      + (riskLevel ? '<div style="position:absolute;top:8px;right:8px;background:' + riskRenk + ';color:white;font-size:9px;font-weight:800;padding:3px 8px;border-radius:12px;letter-spacing:0.04em;">' + riskLevel + '</div>' : '')
      + '</div>'
      + '<div style="padding:10px 12px;">'
      + '<div style="font-size:12px;font-weight:700;color:#0F172A;margin-bottom:4px;line-height:1.4;">' + baslik + '</div>'
      + (konum ? '<div style="display:flex;align-items:center;gap:4px;margin-bottom:6px;"><svg width="10" height="10" fill="none" viewBox="0 0 24 24" stroke="#94A3B8" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg><span style="font-size:10px;color:#94A3B8;">' + konum + '</span></div>' : '')
      + yoloSatir
      + '<div style="display:flex;align-items:center;justify-content:space-between;gap:6px;">'
      + '<div style="display:flex;align-items:center;gap:5px;"><div style="width:20px;height:20px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:800;color:white;flex-shrink:0;">AI</div><span style="font-size:11px;color:#64748B;">Sistem</span></div>'
      + '<div style="display:flex;gap:5px;">'
      + '<button onclick="event.stopPropagation();kpKartDetayGoster(' + k.id + ')" style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:white;background:#0F172A;border:none;padding:5px 10px;border-radius:6px;cursor:pointer;white-space:nowrap;"><svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>İNCELE</button>'
      + '<button onclick="event.stopPropagation();kpAnalizGizle(' + k.id + ')" style="width:28px;height:28px;display:flex;align-items:center;justify-content:center;background:#FEF2F2;border:none;border-radius:6px;cursor:pointer;" title="Sil"><svg width="11" height="11" fill="none" viewBox="0 0 24 24" stroke="#EF4444" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg></button>'
      + '</div></div></div></div>';
  }).join('');

  container.innerHTML = sectionHeader + cardsHtml + '</div>';
}

function kpRenderTespitAkisi(liste) {
  const container = document.getElementById('kpTespitAkis');
  if (!container) return;
  if (liste.length === 0) {
    container.innerHTML = '<div style="text-align:center;padding:20px;color:#475569;font-size:12px;">Henüz tespit kaydı yok.</div>';
    return;
  }
  const son10 = liste.slice(0, 10);
  container.innerHTML = son10.map(k => {
    const tip   = k.tip || 'genel';
    // Severity belirleme
    const ozLower = (k.ozet || '').toLowerCase();
    let sevLabel, sevRenk, dotRenk;
    if (tip === 'guvenlik' && (ozLower.includes('kask') || ozLower.includes('ihlal') || ozLower.includes('tehlike'))) {
      sevLabel = 'KRİTİK'; sevRenk = '#EF4444'; dotRenk = '#EF4444';
    } else if (tip === 'guvenlik') {
      sevLabel = 'YÜKSEK'; sevRenk = '#F97316'; dotRenk = '#F97316';
    } else if (tip === 'ilerleme') {
      sevLabel = 'ORTA'; sevRenk = '#3B82F6'; dotRenk = '#3B82F6';
    } else {
      sevLabel = 'DÜŞÜK'; sevRenk = '#64748B'; dotRenk = '#475569';
    }
    const tarih = k.created_at ? new Date(k.created_at).toLocaleTimeString('tr-TR', {hour:'2-digit',minute:'2-digit'}) : '';
    const rawBaslik = (k.ozet || '').replace(/#{1,6}\s*/g,'').replace(/\*\*/g,'').replace(/\*/g,'').replace(/`/g,'').replace(/[🚨⚠️✅❌🔴🟡🟢]/gu,'').trim();
    const baslik = rawBaslik.split('.')[0].substring(0,50);
    const detay  = tip === 'guvenlik' ? 'Güvenlik ihlali tespit edildi' : tip === 'ilerleme' ? 'Saha ilerleme kaydı' : 'Genel tespit kaydı';
    return '<div style="display:flex;gap:8px;align-items:flex-start;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05);">'
      + '<div style="width:8px;height:8px;border-radius:50%;background:' + dotRenk + ';flex-shrink:0;margin-top:4px;"></div>'
      + '<div style="flex:1;min-width:0;">'
      + '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px;">'
      + '<span style="font-size:10px;font-weight:800;color:' + sevRenk + ';letter-spacing:0.04em;">' + sevLabel + '</span>'
      + '<span style="font-size:10px;color:#64748B;">' + tarih + '</span>'
      + '</div>'
      + '<div style="font-size:12px;font-weight:600;color:#CBD5E1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + baslik + '</div>'
      + '<div style="font-size:10px;color:#475569;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + detay + '</div>'
      + '</div></div>';
  }).join('');
}

function kpRenderStats(liste) {
  const toplam = liste.length;
  const ihlal  = liste.filter(k => k.tip === 'guvenlik').length;
  const el = (id, val) => { const e = document.getElementById(id); if (e) e.textContent = val; };
  el('kpStatToplam', toplam.toLocaleString('tr-TR'));
  el('kpStatIhlal',  ihlal);
  el('kpStatAi',     toplam);
  const badge = document.getElementById('kpAiBadge');
  if (badge) badge.textContent = toplam;
  // Delta göstergesi
  const deltaEl = document.getElementById('kpStatToplamDelta');
  if (deltaEl) deltaEl.textContent = toplam > 0 ? '▲ aktif kayıt' : '—';
  const ihlalDelta = document.getElementById('kpStatIhlalDelta');
  if (ihlalDelta) {
    if (ihlal > 0) { ihlalDelta.textContent = '! Dikkat'; ihlalDelta.style.color = '#EF4444'; }
    else { ihlalDelta.textContent = '—'; ihlalDelta.style.color = '#64748B'; }
  }
}

async function kpLimitGuncelle() {
  const token = localStorage.getItem('bai_token');
  if (!token) return;
  try {
    const res  = await fetch('/kullanim-durumu?token=' + token);
    const data = await res.json();
    const k = data.kamera || { kullanilan: 0, limit: 3 };
    const txt = document.getElementById('kpLimitText');
    const bar = document.getElementById('kpLimitBar');
    if (txt) txt.textContent = k.kullanilan + ' / ' + (k.limit === -1 ? '∞' : k.limit);
    if (bar) {
      const pct = k.limit === -1 ? 10 : Math.min(100, (k.kullanilan / k.limit) * 100);
      bar.style.width = pct + '%';
      bar.style.background = pct > 80 ? '#EF4444' : '#F97316';
    }
  } catch(e) {}
}

function kameraPageFiltrele(q) {
  kpRenderAiKartlar(_kpTumAnaliz);
}

// Manuel kanıt sistemi
function kpManuelEkleAc() {
  const f = document.getElementById('kpManuelForm');
  if (f) { f.style.display = f.style.display === 'none' ? 'block' : 'none'; }
}

function kpManuelYukle() {
  try {
    const raw = localStorage.getItem('bai_manuel_kanitlar');
    _kpManuelKayitlar = raw ? JSON.parse(raw) : [];
  } catch(e) { _kpManuelKayitlar = []; }
  kpRenderManuelKartlar();
}

function kpManuelKaydet() {
  const tip  = (document.getElementById('kpManuelTip')  || {}).value || 'gozlem';
  const not  = (document.getElementById('kpManuelNot')  || {}).value || '';
  if (!not.trim()) { showToast('Not alanı boş bırakılamaz', 'error'); return; }
  const kayit = { id: Date.now(), tip, not, tarih: new Date().toISOString() };
  _kpManuelKayitlar.unshift(kayit);
  localStorage.setItem('bai_manuel_kanitlar', JSON.stringify(_kpManuelKayitlar));
  document.getElementById('kpManuelNot').value = '';
  document.getElementById('kpManuelForm').style.display = 'none';
  kpRenderManuelKartlar();
  showToast('Manuel kanıt kaydedildi', 'success');
}

function kpManuelSil(id) {
  _kpManuelKayitlar = _kpManuelKayitlar.filter(k => k.id !== id);
  localStorage.setItem('bai_manuel_kanitlar', JSON.stringify(_kpManuelKayitlar));
  kpRenderManuelKartlar();
}

function kpRenderManuelKartlar() {
  const container = document.getElementById('kpManuelKartlar');
  const empty     = document.getElementById('kpManuelEmpty');
  const badge     = document.getElementById('kpManuelBadge');
  if (!container) return;
  if (badge) badge.textContent = _kpManuelKayitlar.length;
  const statManuel = document.getElementById('kpStatManuel');
  if (statManuel) statManuel.textContent = _kpManuelKayitlar.length;
  if (_kpManuelKayitlar.length === 0) {
    container.innerHTML = '';
    if (empty) empty.style.display = 'block';
    return;
  }
  if (empty) empty.style.display = 'none';
  const tipBilgi = {
    gozlem:  { renk: '#2563EB', bg: '#EFF6FF', etiket: '🔍 Saha Gözlemi' },
    ihbar:   { renk: '#D97706', bg: '#FEF3C7', etiket: '📢 İhbar' },
    denetim: { renk: '#7C3AED', bg: '#F5F3FF', etiket: '📋 Denetim Notu' },
    kaza:    { renk: '#DC2626', bg: '#FEF2F2', etiket: '⚠️ Kaza / Olay' },
  };
  const gradMap = {
    gozlem:  ['#1E3A5F','#1D4ED8'],
    ihbar:   ['#78350F','#D97706'],
    denetim: ['#2E1065','#6D28D9'],
    kaza:    ['#7F1D1D','#DC2626'],
  };
  const sectionHeaderManuel = '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">'
    + '<div style="display:flex;align-items:center;gap:8px;">'
    + '<svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="#2563EB" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>'
    + '<span style="font-size:13px;font-weight:700;color:#0F172A;">Manuel Kanıtlar</span>'
    + '</div>'
    + '<button onclick="kpManuelTumunuArsivle && kpManuelTumunuArsivle()" style="font-size:11px;font-weight:700;color:#2563EB;background:none;border:none;cursor:pointer;padding:4px 8px;border-radius:6px;white-space:nowrap;" onmouseover="this.style.background=\'#EFF6FF\'" onmouseout="this.style.background=\'none\'">TÜMÜNÜ ARŞİVLE</button>'
    + '</div>'
    + '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;">';

  const manuelCardsHtml = _kpManuelKayitlar.map(k => {
    const info   = tipBilgi[k.tip] || tipBilgi.gozlem;
    const grads  = gradMap[k.tip] || gradMap.gozlem;
    const tarih  = new Date(k.tarih).toLocaleTimeString('tr-TR', {hour:'2-digit',minute:'2-digit',second:'2-digit'});
    const baslik = k.not.substring(0, 52) + (k.not.length > 52 ? '...' : '');
    const ad     = k.not.split(' ')[0] || 'K';
    const initials = ad.substring(0,2).toUpperCase();
    const emoji  = info.etiket.split(' ')[0];
    const tipAdi = info.etiket.replace(/^[^\s]+ /,'');
    const isKaza = k.tip === 'kaza';
    const badgeText = isKaza ? 'MANUEL KRİTİK' : 'MANUEL KAYIT';
    const badgeBg   = isKaza ? '#DC2626' : info.renk;
    const thumb  = localStorage.getItem('bai_manuel_thumb_' + k.id);
    const thumbHtml = thumb
      ? '<img src="' + thumb + '" style="width:100%;height:100%;object-fit:cover;">'
      : '<div style="width:100%;height:100%;background:linear-gradient(135deg,' + grads[0] + ',' + grads[1] + ');display:flex;align-items:center;justify-content:center;font-size:22px;">' + emoji + '</div>';
    return '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-left:4px solid ' + info.renk + ';border-radius:14px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,0.06);cursor:pointer;transition:all 0.15s;" onmouseover="this.style.boxShadow=\'0 6px 20px rgba(0,0,0,0.10)\';this.style.transform=\'translateY(-2px)\'" onmouseout="this.style.boxShadow=\'0 1px 4px rgba(0,0,0,0.06)\';this.style.transform=\'none\'">'
      + '<div style="height:110px;overflow:hidden;position:relative;">' + thumbHtml
      + '<div style="position:absolute;bottom:0;left:0;right:0;padding:6px 10px;background:linear-gradient(transparent,rgba(0,0,0,0.72));display:flex;align-items:center;justify-content:space-between;">'
      + '<span style="font-size:10px;font-weight:800;color:white;background:' + badgeBg + ';padding:2px 8px;border-radius:20px;">' + badgeText + '</span>'
      + '<span style="font-size:10px;color:rgba(255,255,255,0.85);font-weight:600;">' + tarih + '</span>'
      + '</div></div>'
      + '<div style="padding:10px 12px;">'
      + '<div style="font-size:12px;font-weight:700;color:#0F172A;margin-bottom:4px;line-height:1.4;">' + baslik + '</div>'
      + '<div style="display:flex;align-items:center;gap:4px;margin-bottom:6px;"><svg width="10" height="10" fill="none" viewBox="0 0 24 24" stroke="#94A3B8" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg><span style="font-size:10px;color:#94A3B8;">' + tipAdi + '</span></div>'
      + '<div style="display:flex;align-items:center;justify-content:space-between;gap:6px;">'
      + '<div style="display:flex;align-items:center;gap:6px;"><div style="width:22px;height:22px;border-radius:50%;background:' + info.bg + ';border:1.5px solid ' + info.renk + ';display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:800;color:' + info.renk + ';flex-shrink:0;">' + initials + '</div><span style="font-size:11px;color:#64748B;font-weight:500;">Saha</span></div>'
      + '<div style="display:flex;gap:5px;">'
      + '<button style="display:flex;align-items:center;gap:5px;font-size:11px;font-weight:700;color:white;background:#0F172A;border:none;padding:5px 10px;border-radius:7px;cursor:pointer;white-space:nowrap;"><svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>Görüntüle</button>'
      + '<button onclick="event.stopPropagation();kpManuelSil(' + k.id + ')" style="width:28px;height:28px;display:flex;align-items:center;justify-content:center;background:#FEF2F2;border:none;border-radius:7px;cursor:pointer;" title="Sil"><svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="#EF4444" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg></button>'
      + '</div></div></div></div>';
  }).join('');

  container.style.display = 'block';
  container.innerHTML = sectionHeaderManuel + manuelCardsHtml + '</div>';
}

function kpLoguIndirv() {
  const token = localStorage.getItem('bai_token');
  if (!token) return;
  const satirlar = ['ID,Tip,Özet,Şehir,Tarih'];
  _kpTumAnaliz.forEach(k => {
    satirlar.push([k.id, k.tip, '"'+(k.ozet||'').replace(/"/g,'""')+'"', k.sehir, k.created_at].join(','));
  });
  _kpManuelKayitlar.forEach(k => {
    satirlar.push(['M-'+k.id, k.tip, '"'+(k.not||'').replace(/"/g,'""')+'"', '-', k.tarih].join(','));
  });
  const blob = new Blob([satirlar.join('\\n')], { type: 'text/csv;charset=utf-8;' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = 'kamera-analiz-logu.csv';
  a.click();
  URL.revokeObjectURL(url);
  showToast('Log dosyası indiriliyor...', 'success');
}

// ŞANTİYE SAYFASI — Tam sayfa liste görünümü
// ══════════════════════════════════════════
let _spVerisi = [];   // cache

function santiyePageAc() {
  // Ana içerik + command bar + diğer sayfaları gizle
  const content   = document.getElementById('content');
  const cmdBar    = document.getElementById('aiCommandBar');
  const spPage    = document.getElementById('santiyePage');
  if (!spPage) return;
  ['content','aiCommandBar','fiyatPage','stokPage','kameraPage','arsivPage'].forEach(pid => {
    const el = document.getElementById(pid);
    if (el) el.style.display = 'none';
  });
  spPage.style.display = 'flex';

  // Header başlık güncelle
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Şantiye Yönetimi Genel Bakış';

  // "+ Yeni Şantiye" butonunu header'da göster
  let hBtn = document.getElementById('spHeaderBtn');
  if (!hBtn) {
    hBtn = document.createElement('button');
    hBtn.id = 'spHeaderBtn';
    hBtn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> Yeni Şantiye';
    hBtn.style.cssText = 'background:#3B82F6;border:none;color:white;font-size:13px;font-weight:700;padding:8px 16px;border-radius:10px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:background 0.15s;';
    hBtn.onmouseover = () => hBtn.style.background = '#2563EB';
    hBtn.onmouseout  = () => hBtn.style.background = '#3B82F6';
    hBtn.onclick     = () => santiyeEkleModalAc(null);
    const headerRight = document.querySelector('#contentHeader > div:last-child');
    if (headerRight) headerRight.prepend(hBtn);
  } else { hBtn.style.display = 'flex'; }

  santiyePageYukle();
}

function santiyePageKapat() {
  const content  = document.getElementById('content');
  const cmdBar   = document.getElementById('aiCommandBar');
  const spPage   = document.getElementById('santiyePage');
  if (spPage)  spPage.style.display  = 'none';
  if (content) content.style.display = 'flex';
  if (cmdBar)  cmdBar.style.display  = 'block';

  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Genel Bakış';

  const hBtn = document.getElementById('spHeaderBtn');
  if (hBtn) hBtn.style.display = 'none';
}

// ══════ FİYAT TAKİBİ SAYFASI ══════
const _fpCharts = {};

function _fpHideAll() {
  ['content','aiCommandBar','santiyePage','fiyatPage','stokPage','kameraPage','arsivPage'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });
  const hBtn = document.getElementById('spHeaderBtn');
  if (hBtn) hBtn.style.display = 'none';
}

function fiyatPageAc() {
  _fpHideAll();
  const fp = document.getElementById('fiyatPage');
  if (fp) fp.style.display = 'flex';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Piyasa Fiyat Takibi & Tahminleri';
  setTimeout(() => fiyatPageYukle(), 80);
}

function fiyatPageKapat() {
  const fp = document.getElementById('fiyatPage');
  if (fp) fp.style.display = 'none';
  const content = document.getElementById('content');
  const cmdBar  = document.getElementById('aiCommandBar');
  if (content) content.style.display = 'flex';
  if (cmdBar)  cmdBar.style.display  = 'block';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Genel Bakış';
}

async function fiyatPageYukle() {
  const malzemeler = [
    { malzeme:'demir',   canvas:'celikGrafik',   label:'celikFiyatLabel',   period:'celikPeriod',   ad:'Çelik' },
    { malzeme:'beton',   canvas:'betonGrafik',    label:'betonFiyatLabel',   period:'betonPeriod',   ad:'Beton' },
    { malzeme:'cimento', canvas:'keresteGrafik',  label:'keresteFiyatLabel', period:'kerestePeriod', ad:'Kereste' },
  ];
  const tahminler = [];
  for (const m of malzemeler) {
    const gun = document.getElementById(m.period)?.value || 90;
    const pct = await fiyatGrafikYukle(m.malzeme, m.canvas, m.label, gun);
    tahminler.push({ ad: m.ad, pct });
  }
  _fiyatInsightsGuncelle(tahminler);
}

async function fiyatGrafikYukle(malzeme, canvasId, labelId, gun) {
  try {
    const res  = await fetch(`/fiyat-gecmis/${malzeme}?gun=${gun}`);
    const data = await res.json();
    const gecmis = data.gecmis || [];

    const canvas = document.getElementById(canvasId);
    if (!canvas) return 0;

    // Son fiyatı label'e yaz
    const sonFiyat = gecmis.length > 0 ? parseFloat(gecmis[gecmis.length-1].fiyat) : null;
    const labelEl  = document.getElementById(labelId);
    if (labelEl) labelEl.textContent = sonFiyat ? sonFiyat.toLocaleString('tr-TR') : '—';

    // Geçmiş yoksa örnek veri üret
    let gecmisLabels, gecmisData;
    if (gecmis.length >= 2) {
      gecmisLabels = gecmis.map(d => d.tarih.slice(5));
      gecmisData   = gecmis.map(d => parseFloat(d.fiyat));
    } else {
      const baz = malzeme==='demir' ? 220 : malzeme==='beton' ? 250 : 1800;
      gecmisLabels = Array.from({length:8}, (_,i) => {
        const d = new Date(); d.setDate(d.getDate() - (7-i)*10);
        return (d.getMonth()+1)+'/'+d.getDate();
      });
      gecmisData = gecmisLabels.map((_,i) => Math.round(baz + (Math.random()-0.5)*baz*0.12 + i*baz*0.01));
      if (labelEl) labelEl.textContent = gecmisData[gecmisData.length-1].toLocaleString('tr-TR');
    }

    // Tahmin (basit lineer trend — son 3 noktadan)
    const n = gecmisData.length;
    const slope = n >= 3 ? (gecmisData[n-1] - gecmisData[n-3]) / 2 : gecmisData[n-1] * 0.03;
    const tahminLabels = Array.from({length:4}, (_,i) => {
      const d = new Date(); d.setDate(d.getDate() + (i+1)*15);
      return (d.getMonth()+1)+'/'+d.getDate();
    });
    const tahminData = tahminLabels.map((_,i) => Math.round(gecmisData[n-1] + slope*(i+1)));
    const pct = n > 0 ? Math.round((slope / gecmisData[n-1]) * 100) : 5;

    // Chart
    if (_fpCharts[canvasId]) { _fpCharts[canvasId].destroy(); delete _fpCharts[canvasId]; }
    _fpCharts[canvasId] = new Chart(canvas, {
      type: 'line',
      data: {
        labels: [...gecmisLabels, ...tahminLabels],
        datasets: [
          {
            label: 'Geçmiş',
            data: [...gecmisData, ...Array(tahminLabels.length).fill(null)],
            borderColor: '#EF4444',
            backgroundColor: 'rgba(239,68,68,0.08)',
            borderWidth: 2.2,
            pointRadius: 2,
            pointHoverRadius: 5,
            fill: true,
            tension: 0.4,
            spanGaps: false
          },
          {
            label: 'Tahmin',
            data: [...Array(gecmisLabels.length-1).fill(null), gecmisData[n-1], ...tahminData],
            borderColor: '#22C55E',
            backgroundColor: 'rgba(34,197,94,0.07)',
            borderWidth: 2.2,
            borderDash: [5,4],
            pointRadius: 2,
            pointHoverRadius: 5,
            fill: true,
            tension: 0.4,
            spanGaps: false
          }
        ]
      },
      options: {
        responsive: true,
        animation: { duration: 400 },
        plugins: { legend: { display: false }, tooltip: { mode:'index', intersect:false } },
        scales: {
          x: { ticks: { color:'#94A3B8', font:{size:10}, maxTicksLimit:6 }, grid: { color:'rgba(0,0,0,0.04)' } },
          y: { ticks: { color:'#94A3B8', font:{size:10}, callback: v => '₺'+v.toLocaleString('tr-TR') }, grid: { color:'rgba(0,0,0,0.04)' } }
        }
      }
    });
    return pct;
  } catch(e) { return 0; }
}

function _fiyatInsightsGuncelle(tahminler) {
  const analizEl  = document.getElementById('fiyatAnalizList');
  const satinEl   = document.getElementById('fiyatSatinList');
  const analizSub = document.getElementById('fiyatAnalizSubtitle');
  const satinSub  = document.getElementById('fiyatSatinSubtitle');

  if (analizEl) {
    analizEl.innerHTML = tahminler.map(t => {
      const pct = t.pct || Math.floor(Math.random()*8+3);
      const yön  = pct >= 0 ? 'artış' : 'düşüş';
      const renk = pct >= 0 ? '#EF4444' : '#16A34A';
      return `<div style="display:flex;align-items:flex-start;gap:8px;font-size:13px;color:#334155;">
        <span style="color:${renk};font-size:15px;line-height:1;flex-shrink:0;">•</span>
        ${t.ad} fiyatlarında önümüzdeki ay <strong style="color:${renk};">%${Math.abs(pct)} ${yön}</strong> bekleniyor
      </div>`;
    }).join('');
    if (analizSub) analizSub.textContent = 'Piyasa analizi tamamlandı — artış beklentisi mevcut.';
  }

  if (satinEl) {
    const uygun = tahminler.filter(t => (t.pct || 5) > 3).map(t => t.ad);
    satinEl.innerHTML = (uygun.length > 0 ? uygun : tahminler.map(t=>t.ad)).map(ad =>
      `<div style="display:flex;align-items:flex-start;gap:8px;font-size:13px;color:#334155;">
        <span style="color:#16A34A;font-size:15px;line-height:1;flex-shrink:0;">•</span>
        <strong>${ad}</strong> için en uygun satın alma zamanı <strong style="color:#16A34A;">bu hafta!</strong>
      </div>`
    ).join('');
    if (satinSub) satinSub.textContent = `Satın al: ${(uygun.length>0?uygun:tahminler.map(t=>t.ad)).join(' ve ')} için en uygun zaman bu hafta!`;
  }
}

async function fiyatAiGonder() {
  const inp = document.getElementById('fiyatAiInput');
  const res = document.getElementById('fiyatAiResult');
  const soru = inp?.value?.trim();
  if (!soru || !res) return;
  res.style.display = 'block';
  res.innerHTML = '<span style="color:#94A3B8;">⏳ AI yanıtlıyor...</span>';
  inp.value = '';
  try {
    const token = localStorage.getItem('bai_token');
    const r = await fetch('/sor', {
      method:'POST',
      headers:{'Content-Type':'application/json','Authorization':'Bearer '+token},
      body: JSON.stringify({ soru: '[Fiyat Takibi] ' + soru, token, konusma_tonu: localStorage.getItem('ai_konusma_tonu') || 'saha_arkadasi' })
    });
    const d = await r.json();
    res.innerHTML = d.cevap || d.mesaj || 'Yanıt alınamadı.';
  } catch(e) { res.innerHTML = '<span style="color:#EF4444;">Bağlantı hatası.</span>'; }
}

function fiyatAiQuick(text) {
  const inp = document.getElementById('fiyatAiInput');
  if (inp) { inp.value = text; fiyatAiGonder(); }
}

// ══════ STOK TAKİBİ SAYFASI ══════
function stokPageAc() {
  _fpHideAll();
  const sp = document.getElementById('stokPage');
  if (sp) sp.style.display = 'flex';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Malzeme Stok Takibi';
  stokSantiyeleriYukle().then(() => stokYukle());
}

function stokPageKapat() {
  const sp = document.getElementById('stokPage');
  if (sp) sp.style.display = 'none';
  const content = document.getElementById('content');
  const cmdBar  = document.getElementById('aiCommandBar');
  if (content) content.style.display = 'flex';
  if (cmdBar)  cmdBar.style.display  = 'block';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Genel Bakış';
}

async function stokAiGonder() {
  const inp = document.getElementById('stokAiInput');
  const res = document.getElementById('stokAiResult');
  const soru = inp?.value?.trim();
  if (!soru || !res) return;
  res.style.display = 'block';
  res.innerHTML = '<span style="color:#94A3B8;">⏳ AI yanıtlıyor...</span>';
  inp.value = '';
  try {
    const token = localStorage.getItem('bai_token');
    const r = await fetch('/sor', {
      method:'POST',
      headers:{'Content-Type':'application/json','Authorization':'Bearer '+token},
      body: JSON.stringify({ soru: '[Stok Takibi] ' + soru, token, konusma_tonu: localStorage.getItem('ai_konusma_tonu') || 'saha_arkadasi' })
    });
    const d = await r.json();
    res.innerHTML = d.cevap || d.mesaj || 'Yanıt alınamadı.';
  } catch(e) { res.innerHTML = '<span style="color:#EF4444;">Bağlantı hatası.</span>'; }
}

function stokAiQuick(text) {
  const inp = document.getElementById('stokAiInput');
  if (inp) { inp.value = text; stokAiGonder(); }
}

async function santiyePageYukle() {
  const token = localStorage.getItem('bai_token') || '';
  try {
    const res  = await fetch('/santiyeler', { headers: { Authorization: 'Bearer ' + token } });
    const data = await res.json();
    _spVerisi  = data.santiyeler || [];
  } catch(e) { _spVerisi = []; }
  santiyePageRender(_spVerisi);
}

function santiyePageFiltrele(q) {
  const term = (q || '').toLowerCase().trim();
  const filtered = term ? _spVerisi.filter(s =>
    (s.ad || '').toLowerCase().includes(term) ||
    (s.konum || '').toLowerCase().includes(term)
  ) : _spVerisi;
  santiyePageRender(filtered);
}

function santiyePageRender(liste) {
  // KPI güncelle
  const toplam  = liste.length;
  const iyi     = liste.filter(s => s.durum === 'iyi').length;
  const dikkat  = liste.filter(s => s.durum === 'dikkat').length;
  const isci    = liste.reduce((a, s) => a + (s.isci_sayisi || 0), 0);
  const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
  set('spKpiToplam', toplam); set('spKpiIyi', iyi);
  set('spKpiDikkat', dikkat); set('spKpiIsci', isci);

  const durumCfg = {
    iyi:    { bg:'#F0FDF4', border:'#86EFAC', txt:'#16A34A', icon:'✓',  lbl:'Zamanında'    },
    dikkat: { bg:'#FFF7ED', border:'#FED7AA', txt:'#EA580C', icon:'⚠',  lbl:'Gecikme Riski'},
    sorun:  { bg:'#FEF2F2', border:'#FECACA', txt:'#DC2626', icon:'✕',  lbl:'Kritik Sorun' },
  };

  // İmaj gradients — durum rengine göre
  const gradients = [
    'linear-gradient(135deg,#1E3A5F,#2D5986)',
    'linear-gradient(135deg,#1A3A2A,#2D6045)',
    'linear-gradient(135deg,#3A1A1A,#6B3030)',
    'linear-gradient(135deg,#2A1A3A,#5B3070)',
    'linear-gradient(135deg,#1A2A3A,#304060)',
    'linear-gradient(135deg,#3A2A1A,#705030)',
  ];

  function imgDiv(s, i, w, h, radius) {
    if (s.foto) {
      return `<div style="width:${w};height:${h};border-radius:${radius};flex-shrink:0;overflow:hidden;">
        <img src="${s.foto}" alt="${s.ad}" style="width:100%;height:100%;object-fit:cover;display:block;">
      </div>`;
    }
    const g = gradients[i % gradients.length];
    const initial = (s.ad || 'P').charAt(0).toUpperCase();
    return `<div style="width:${w};height:${h};border-radius:${radius};background:${g};display:flex;align-items:center;justify-content:center;flex-shrink:0;overflow:hidden;">
      <span style="font-size:${parseInt(h)/2.5}px;color:rgba(255,255,255,0.35);font-weight:800;">${initial}</span>
    </div>`;
  }

  function progressBar(pct) {
    const color = pct >= 80 ? '#10B981' : pct >= 50 ? '#3B82F6' : pct >= 30 ? '#F97316' : '#EF4444';
    return `<div class="sp-progress-bar">
      <div class="sp-progress-fill" style="width:${pct}%;background:${color};"></div>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-size:11px;font-weight:700;color:${color};">${pct}%</span>
    </div>`;
  }

  function badge(s) {
    const cfg = durumCfg[s.durum] || durumCfg.iyi;
    return `<span class="sp-badge" style="background:${cfg.bg};color:${cfg.txt};border:1px solid ${cfg.border};">
      <span>${cfg.icon}</span>${cfg.lbl}
    </span>`;
  }

  // Boş durum
  if (liste.length === 0) {
    const empty = `<div style="grid-column:1/-1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 20px;gap:14px;">
      <div style="font-size:52px;">🏗️</div>
      <div style="font-size:15px;font-weight:600;color:#475569;">Henüz şantiye eklenmedi</div>
      <div style="font-size:12px;color:#94A3B8;">Projenizi ekleyerek takibe başlayın</div>
      <button onclick="santiyeEkleModalAc(null)" style="background:#3B82F6;border:none;color:white;padding:10px 20px;border-radius:10px;cursor:pointer;font-weight:700;font-size:13px;margin-top:8px;">+ İlk Şantiyeni Ekle</button>
    </div>`;
    const h = document.getElementById('santiyePageHoriz');
    const g = document.getElementById('santiyePageGrid');
    if (h) h.innerHTML = empty;
    if (g) g.innerHTML = '';
    return;
  }

  // Yatay kartlar (ilk 3)
  const ilk3 = liste.slice(0, 3);
  const horizEl = document.getElementById('santiyePageHoriz');
  if (horizEl) {
    horizEl.innerHTML = ilk3.map((s, i) => {
      const pct = Math.min(100, Math.max(0, s.ilerleme || 0));
      return `<div class="sp-kart-horiz" onclick="santiyeEkleModalAc(${JSON.stringify(s).replace(/"/g,'&quot;')})">
        ${imgDiv(s, i, '110px', '90px', '10px')}
        <div style="flex:1;min-width:0;">
          <div style="font-size:14px;font-weight:700;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${s.ad || 'Şantiye'}</div>
          <div style="font-size:11px;color:#94A3B8;margin-top:3px;display:flex;align-items:center;gap:3px;">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            ${s.konum || '—'}
          </div>
          ${progressBar(pct)}
          ${badge(s)}
        </div>
      </div>`;
    }).join('');
  }

  // Dikey grid (tümü)
  const gridEl = document.getElementById('santiyePageGrid');
  if (gridEl) {
    gridEl.innerHTML = liste.map((s, i) => {
      const pct = Math.min(100, Math.max(0, s.ilerleme || 0));
      return `<div class="sp-kart-vert" onclick="santiyeEkleModalAc(${JSON.stringify(s).replace(/"/g,'&quot;')})">
        ${imgDiv(s, i, '100%', '160px', '0')}
        <div style="padding:12px 14px;">
          <div style="font-size:13px;font-weight:700;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${s.ad || 'Şantiye'}</div>
          <div style="font-size:11px;color:#94A3B8;margin-top:2px;display:flex;align-items:center;gap:3px;">
            <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            ${s.konum || '—'}
          </div>
          ${progressBar(pct)}
          ${badge(s)}
        </div>
      </div>`;
    }).join('');
  }
}

// Dashboard modülleri — auth tamamlanınca otomatik yükle
window.addEventListener('load', function() {
  setTimeout(function() {
    const token = localStorage.getItem('bai_token');
    if (token && document.getElementById('sahaGunluguListe')) {
      sahaGunluguYukle();
      aiAlertsYukle();
    }
  }, 2000);
});

// ── Content Header: tarih, kullanıcı adı, online durum ──
function contentHeaderGuncelle() {
  // Tarih
  const dateEl = document.getElementById('contentDate');
  if (dateEl) {
    const now = new Date();
    const gunler = ['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'];
    const aylar = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran',
                   'Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
    dateEl.textContent = `${gunler[now.getDay()]}, ${now.getDate()} ${aylar[now.getMonth()]} ${now.getFullYear()}`;
  }
  // Kullanıcı adı
  const nameEl   = document.getElementById('headerUserName');
  const avatarEl = document.getElementById('headerAvatar');
  const storedName = localStorage.getItem('bai_user_name') || localStorage.getItem('bai_email') || '';
  if (storedName && nameEl) {
    const display = storedName.includes('@') ? storedName.split('@')[0] : storedName;
    nameEl.textContent = display.charAt(0).toUpperCase() + display.slice(1);
    if (avatarEl) avatarEl.textContent = display.slice(0,2).toUpperCase();
  }
  // Online durum
  const statusText  = document.getElementById('onlineStatusText');
  const statusBtn   = document.getElementById('onlineStatusBtn');
  const queueBadge  = document.getElementById('offlineQueueBadge');
  const queueCount  = document.getElementById('offlineQueueCount');
  if (navigator.onLine) {
    if (statusText) statusText.textContent = 'Çevrimiçi';
    if (statusBtn)  { statusBtn.style.borderColor='#10B981'; }
    const svg = statusBtn && statusBtn.querySelector('svg');
    if (svg) svg.style.stroke = '#10B981';
    if (statusText) statusText.style.color = '#10B981';
    if (queueBadge) queueBadge.style.display = 'none';
  } else {
    if (statusText) statusText.textContent = 'İnternet Yok';
    if (statusBtn)  { statusBtn.style.borderColor='#F97316'; }
    const svg = statusBtn && statusBtn.querySelector('svg');
    if (svg) svg.style.stroke = '#F97316';
    if (statusText) statusText.style.color = '#F97316';
    // Offline queue count from localStorage
    try {
      const q = JSON.parse(localStorage.getItem('bai_offline_queue') || '[]');
      if (q.length > 0 && queueBadge && queueCount) {
        queueBadge.style.display = 'inline';
        queueCount.textContent = q.length;
      }
    } catch(e) {}
  }
}

// Header'ı her zaman güncel tut
document.addEventListener('DOMContentLoaded', contentHeaderGuncelle);
window.addEventListener('online',  contentHeaderGuncelle);
window.addEventListener('offline', contentHeaderGuncelle);
// Auth tamamlandıktan sonra da çalıştır
const _origShowMainApp = window.showMainApp;
if (typeof _origShowMainApp === 'function') {
  window.showMainApp = function() { _origShowMainApp.apply(this, arguments); contentHeaderGuncelle(); };
}
setTimeout(contentHeaderGuncelle, 500);
setTimeout(contentHeaderGuncelle, 2500);

// ═══════════════════════════════════════════════════
// 🔧 AYARLAR SAYFASI — ANA ROUTER
// ═══════════════════════════════════════════════════

function sayfaGoster(sayfa) {
  // Avatar menüyü kapat
  const menu = document.getElementById('avatarMenu');
  if (menu) menu.style.display = 'none';

  if (sayfa === 'ayarlar') {
    // Diğer sayfaları kapat (içerik+cmdBar gösterme)
    ['santiyePage','fiyatPage','stokPage','kameraPage','arsivPage'].forEach(pid => {
      const el = document.getElementById(pid);
      if (el) el.style.display = 'none';
    });
    const content    = document.getElementById('content');
    const cmdBar     = document.getElementById('aiCommandBar');
    const ayarlarPage = document.getElementById('ayarlarPage');
    if (content)      content.style.display    = 'none';
    if (cmdBar)       cmdBar.style.display     = 'none';
    if (ayarlarPage)  ayarlarPage.style.display = 'flex';
    const titleEl = document.getElementById('contentTitle');
    if (titleEl) titleEl.textContent = 'Ayarlar';
    const hBtn = document.getElementById('spHeaderBtn');
    if (hBtn) hBtn.style.display = 'none';
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const navEl = document.getElementById('nav-ayarlar');
    if (navEl) navEl.classList.add('active');
    ayarlarKategoriGoster(localStorage.getItem('ayarlar_kategori') || 'profil');
  } else {
    // Ayarlar sayfasını kapat, diğer sayfaya geç
    const ayarlarPage = document.getElementById('ayarlarPage');
    if (ayarlarPage) ayarlarPage.style.display = 'none';
    navGit(sayfa);
  }
  if (typeof closeMobileMenu === 'function') closeMobileMenu();
}

// ─────────────────────────────────────────────────
// KATEGORİ GÖSTERİCİ
// ─────────────────────────────────────────────────

function ayarlarKategoriGoster(id) {
  localStorage.setItem('ayarlar_kategori', id);
  const kategoriler = ['profil','santiye','ai','bildirim','plan','guvenlik'];
  kategoriler.forEach(k => {
    const btn = document.getElementById('ayarlarBtn-' + k);
    if (!btn) return;
    const active = (k === id);
    btn.style.background = active ? '#3B82F6' : 'transparent';
    btn.style.color      = active ? '#FFFFFF' : '#64748B';
    btn.style.fontWeight = active ? '600' : '500';
    btn.style.boxShadow  = active ? '0 2px 8px rgba(59,130,246,0.35)' : 'none';
  });
  const icerik = document.getElementById('ayarlarIcerik');
  if (!icerik) return;

  const user   = JSON.parse(localStorage.getItem('bai_user') || '{}');
  const kUser  = aktifKullanici || user;
  const isim   = kUser.full_name || '';
  const email  = kUser.email    || '';
  const plan   = window._kullaniciPlan || user.plan || 'free';
  const initials = isim ? isim.split(' ').filter(Boolean).map(w => w[0]).join('').toUpperCase().slice(0,2) : 'U';

  // ──────────────────────────────────────
  // 1. PROFİL & HESAP
  // ──────────────────────────────────────
  if (id === 'profil') {
    const planLabel = {free:'Ücretsiz', pro:'⚡ Pro', max:'👑 Max', admin:'🛡️ Admin'};
    const rolKayitli = localStorage.getItem('bai_rol') || 'santi_sefi';
    icerik.innerHTML = `
      <div style="margin-bottom:24px;">
        <div style="font-size:22px;font-weight:700;color:#0F172A;margin-bottom:4px;">Profil &amp; Hesap</div>
        <div style="font-size:13px;color:#64748B;">Kişisel bilgilerini yönet</div>
      </div>

      <!-- Kart 1: Profil Bilgileri -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid #F1F5F9;">
          <div style="width:64px;height:64px;border-radius:50%;background:#0D1117;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;color:white;flex-shrink:0;">${initials}</div>
          <div>
            <div style="font-size:16px;font-weight:700;color:#0F172A;">${isim || 'Kullanıcı'}</div>
            <div style="font-size:13px;color:#64748B;margin-top:2px;">${email}</div>
            <div style="display:inline-block;margin-top:6px;background:#EEF2FF;color:#6366F1;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;">${planLabel[plan] || 'Ücretsiz'}</div>
          </div>
        </div>
        <div style="font-size:11px;color:#94A3B8;margin-bottom:20px;">📷 Fotoğraf değiştirme yakında eklenecek</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <div>
            <label style="font-size:12px;font-weight:600;color:#64748B;display:block;margin-bottom:6px;">Ad Soyad</label>
            <input id="ayarlarAdSoyad" type="text" value="${isim.replace(/"/g,'&quot;')}"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;transition:border-color 0.15s;"
              onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#E2E8F0'">
          </div>
          <div>
            <label style="font-size:12px;font-weight:600;color:#64748B;display:block;margin-bottom:6px;">E-posta</label>
            <div style="position:relative;">
              <input type="email" value="${email.replace(/"/g,'&quot;')}" readonly
                style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 36px 10px 14px;font-size:14px;width:100%;color:#94A3B8;box-sizing:border-box;outline:none;cursor:not-allowed;">
              <span style="position:absolute;right:12px;top:50%;transform:translateY(-50%);color:#94A3B8;font-size:14px;">🔒</span>
            </div>
          </div>
          <div>
            <label style="font-size:12px;font-weight:600;color:#64748B;display:block;margin-bottom:6px;">Telefon</label>
            <input id="ayarlarTelefon" type="tel" value="${(user.telefon||'').replace(/"/g,'&quot;')}" placeholder="+90 5XX XXX XX XX"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;transition:border-color 0.15s;"
              onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#E2E8F0'">
          </div>
          <div>
            <label style="font-size:12px;font-weight:600;color:#64748B;display:block;margin-bottom:6px;">Rol</label>
            <select id="ayarlarRol"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;cursor:pointer;transition:border-color 0.15s;"
              onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#E2E8F0'">
              <option value="muhendis"     ${rolKayitli==='muhendis'?'selected':''}>Mühendis</option>
              <option value="santi_sefi"   ${rolKayitli==='santi_sefi'||(!rolKayitli||rolKayitli==='mutahhit'||rolKayitli==='proje_muduru')?'':'selected'}>Şantiye Şefi</option>
              <option value="mutahhit"     ${rolKayitli==='mutahhit'?'selected':''}>Müteahhit</option>
              <option value="proje_muduru" ${rolKayitli==='proje_muduru'?'selected':''}>Proje Müdürü</option>
            </select>
          </div>
        </div>
        <button onclick="profilKaydet()"
          style="background:#6366f1;color:white;border:none;border-radius:8px;padding:10px 24px;font-size:14px;cursor:pointer;margin-top:16px;font-weight:600;transition:background 0.15s;"
          onmouseover="this.style.background='#4F46E5'" onmouseout="this.style.background='#6366f1'">Değişiklikleri Kaydet</button>
      </div>

      <!-- Kart 2: Dil & Format -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;">
        <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:16px;">Dil &amp; Format</div>
        <div style="margin-bottom:16px;">
          <div style="font-size:12px;font-weight:600;color:#64748B;margin-bottom:8px;">Dil</div>
          <div style="display:flex;gap:8px;">
            <button id="dilTR" onclick="ayarlarDilSec('tr')"
              style="padding:8px 18px;border-radius:20px;border:1.5px solid #6366f1;background:#EEF2FF;color:#6366F1;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.15s;">🇹🇷 Türkçe</button>
            <button id="dilEN" onclick="ayarlarDilSec('en')"
              style="padding:8px 18px;border-radius:20px;border:1.5px solid #E2E8F0;background:#F8FAFC;color:#64748B;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.15s;">🇬🇧 English</button>
          </div>
        </div>
        <div>
          <div style="font-size:12px;font-weight:600;color:#64748B;margin-bottom:8px;">Tarih Formatı</div>
          <select id="tarihFormat" onchange="localStorage.setItem('tarih_format',this.value)"
            style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;color:#1E293B;outline:none;cursor:pointer;min-width:220px;">
            <option value="DD.MM.YYYY" ${(localStorage.getItem('tarih_format')||'DD.MM.YYYY')==='DD.MM.YYYY'?'selected':''}>GG.AA.YYYY (Türkiye)</option>
            <option value="YYYY-MM-DD" ${localStorage.getItem('tarih_format')==='YYYY-MM-DD'?'selected':''}>YYYY-MM-DD (ISO)</option>
          </select>
        </div>
      </div>`;

  // ──────────────────────────────────────
  // 2. ŞANTİYE VARSAYILANLARI
  // ──────────────────────────────────────
  } else if (id === 'santiye') {
    const birimler = JSON.parse(localStorage.getItem('birim_sistemi') || '{}');
    const uz  = birimler.uzunluk || 'Metre';
    const al  = birimler.alan    || 'm²';
    const ag  = birimler.agirlik || 'kg';
    const saatler = JSON.parse(localStorage.getItem('calisma_saatleri') || '{"baslangic":"08:00","bitis":"18:00","gunler":["Pzt","Sal","Çar","Per","Cum"]}');
    const aktifGunler = saatler.gunler || ['Pzt','Sal','Çar','Per','Cum'];
    const gunler = ['Paz','Pzt','Sal','Çar','Per','Cum','Cmt'];
    const birimRows = [
      {tip:'uzunluk', label:'Uzunluk', u1:'Metre', u2:'Feet', cur:uz},
      {tip:'alan',    label:'Alan',    u1:'m²',    u2:'ft²',  cur:al},
      {tip:'agirlik', label:'Ağırlık', u1:'kg',    u2:'lb',   cur:ag},
    ];
    const birimHTML = '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:24px;padding-top:8px;">'
      + birimRows.map(function(b) {
      const on = (b.cur === b.u1);
      return '<div style="display:flex;flex-direction:column;gap:14px;">'
        + '<div style="font-size:13px;font-weight:500;color:#1E293B;">' + b.label
        + ' <span style="color:#94A3B8;font-size:12px;">(' + b.u1 + ' / ' + b.u2 + ')</span></div>'
        + '<div style="display:flex;align-items:center;gap:10px;">'
        + '<div id="tog-' + b.tip + '" onclick="birimToggle(\'' + b.tip + '\')"'
        + ' style="width:44px;height:24px;border-radius:12px;cursor:pointer;background:' + (on?'#3B82F6':'#CBD5E1') + ';position:relative;transition:background 0.25s;flex-shrink:0;">'
        + '<div style="position:absolute;top:3px;width:18px;height:18px;border-radius:50%;background:white;box-shadow:0 1px 3px rgba(0,0,0,0.2);transition:left 0.25s;left:' + (on?'23px':'3px') + ';"></div>'
        + '</div>'
        + '<span id="tog-label-' + b.tip + '" style="font-size:13px;font-weight:600;color:#0F172A;">' + b.cur + '</span>'
        + '</div></div>';
    }).join('') + '</div>';
    const gunlerHTML = gunler.map(function(g) {
      const ak = aktifGunler.includes(g);
      return '<button onclick="calismaGunToggle(\'' + g + '\',this)"'
        + ' style="padding:6px 14px;border-radius:20px;border:none;cursor:pointer;font-size:13px;font-weight:600;'
        + 'background:' + (ak?'#3B82F6':'#1E293B') + ';color:white;transition:all 0.15s;">' + g + '</button>';
    }).join('');
    icerik.innerHTML =
        '<div style="padding-bottom:20px;margin-bottom:24px;border-bottom:1px solid #F1F5F9;">'
      + '<div style="font-size:20px;font-weight:700;color:#0F172A;">Ayarlar - Şantiye Varsayılanları</div>'
      + '<div style="font-size:12px;color:#94A3B8;margin-top:3px;">Şantiye tercihlerinizi buradan yapılandırın</div>'
      + '</div>'
      + '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:20px 24px;margin-bottom:16px;">'
      + '<div style="font-size:14px;font-weight:700;color:#0F172A;margin-bottom:10px;">Varsayılan Şantiye</div>'
      + '<div style="font-size:12px;color:#64748B;margin-bottom:12px;">Varsayılan şantiye varsayılanları, seçilen şantiyeye uyarlanmış olacaktır.</div>'
      + '<select id="varsayilanSantiyeSel" onchange="varsayilanSantiyeSec(this.value)"'
      + ' style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;cursor:pointer;">'
      + '<option value="">Şantiye seçin...</option></select>'
      + '<div id="varsayilanSantiyeKart" style="display:none;margin-top:12px;background:#F8FAFC;border-radius:10px;padding:16px;border:1px solid #E2E8F0;"></div>'
      + '</div>'
      + '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:20px 24px;margin-bottom:16px;">'
      + '<div style="font-size:14px;font-weight:700;color:#0F172A;margin-bottom:2px;">Birim Sistemi</div>'
      + '<div style="font-size:12px;color:#64748B;margin-bottom:12px;">Hesaplamalarda kullanılacak ölçüm birimlerini seçin</div>'
      + birimHTML
      + '</div>'
      + '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:20px 24px;">'
      + '<div style="font-size:14px;font-weight:700;color:#0F172A;margin-bottom:14px;">Çalışma Saatleri</div>'
      + '<div style="display:flex;gap:16px;margin-bottom:16px;">'
      + '<div style="flex:1;"><label style="font-size:12px;font-weight:600;color:#64748B;display:block;margin-bottom:6px;">Başlangıç</label>'
      + '<input type="time" id="saatBaslangic" value="' + (saatler.baslangic||'08:00') + '" onchange="calismaGunuKaydet()"'
      + ' style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;"></div>'
      + '<div style="flex:1;"><label style="font-size:12px;font-weight:600;color:#64748B;display:block;margin-bottom:6px;">Bitiş</label>'
      + '<input type="time" id="saatBitis" value="' + (saatler.bitis||'18:00') + '" onchange="calismaGunuKaydet()"'
      + ' style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;"></div>'
      + '</div>'
      + '<div style="font-size:12px;font-weight:600;color:#64748B;margin-bottom:10px;">Çalışma Günleri</div>'
      + '<div style="display:flex;gap:8px;flex-wrap:wrap;">' + gunlerHTML + '</div>'
      + '</div>';
    ayarlarSantiyeleriYukle();

  // ──────────────────────────────────────
  // 3. AI ASİSTAN
  // ──────────────────────────────────────
  } else if (id === 'ai') {
    const yanit    = localStorage.getItem('ai_yanit_stili') || 'normal';
    const ton      = localStorage.getItem('ai_konusma_tonu') || 'saha_arkadasi';
    const sesAcik  = localStorage.getItem('ai_ses_asistan') === 'true';
    const bellekAcik = localStorage.getItem('ai_bellek') !== 'false';
    const komutlar = JSON.parse(localStorage.getItem('ai_hizli_komutlar') || JSON.stringify(AI_QUICK_COMMANDS));
    const stilSecenekler = [
      {k:'kisa',      baslik:'Kısa',      aciklama:'Tek cümle, hızlı yanıt'},
      {k:'normal',    baslik:'Normal',    aciklama:'2-3 cümle, dengeli'},
      {k:'ayrintili', baslik:'Ayrıntılı', aciklama:'Tam analiz, liste ve tablo'}
    ];
    const tonSecenekler = [
      {k:'saha_arkadasi', baslik:'Saha Arkadaşı', aciklama:'Samimi, doğrudan, pratik'},
      {k:'hizli_bakis',   baslik:'Hızlı Bakış',   aciklama:'Maddeler + emoji + aksiyon'},
      {k:'hikaye_modu',   baslik:'Hikaye Modu',   aciklama:'Akıcı anlatı, bağlantılı'}
    ];
    icerik.innerHTML = `
      <div style="margin-bottom:24px;">
        <div style="font-size:22px;font-weight:700;color:#1E293B;margin-bottom:4px;">AI Asistan</div>
        <div style="font-size:13px;color:#64748B;">Yapay zeka davranışını özelleştir</div>
      </div>

      <!-- Kart 1: Yanıt Stili -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="font-size:15px;font-weight:700;color:#1E293B;margin-bottom:16px;">Yanıt Stili</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
          ${stilSecenekler.map(s => `
            <div onclick="aiYanitStilSec('${s.k}')" id="aiStil-${s.k}"
              style="padding:16px;border-radius:10px;cursor:pointer;text-align:center;transition:all 0.15s;
                     border:${yanit===s.k?'2px solid #6366F1':'1px solid #E2E8F0'};
                     background:${yanit===s.k?'#EEF2FF':'#FFFFFF'};
                     color:${yanit===s.k?'#4338CA':'#1E293B'};">
              <div style="font-size:14px;font-weight:700;margin-bottom:6px;">${s.baslik}</div>
              <div style="font-size:12px;color:#64748B;">${s.aciklama}</div>
            </div>`).join('')}
        </div>
      </div>

      <!-- Kart 1b: Konuşma Tonu -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="font-size:15px;font-weight:700;color:#1E293B;margin-bottom:4px;">Konuşma Tonu</div>
        <div style="font-size:12px;color:#64748B;margin-bottom:16px;">AI'ın sana nasıl hitap etmesini istiyorsun?</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
          ${tonSecenekler.map(t => `
            <div onclick="aiKonusmaTonuSec('${t.k}')" id="aiTon-${t.k}"
              style="padding:16px;border-radius:10px;cursor:pointer;text-align:center;transition:all 0.15s;
                     border:${ton===t.k?'2px solid #6366F1':'1px solid #E2E8F0'};
                     background:${ton===t.k?'#EEF2FF':'#FFFFFF'};
                     color:${ton===t.k?'#4338CA':'#1E293B'};">
              <div style="font-size:14px;font-weight:700;margin-bottom:6px;">${t.baslik}</div>
              <div style="font-size:12px;color:#64748B;">${t.aciklama}</div>
            </div>`).join('')}
        </div>
      </div>

      <!-- Kart 2: Hızlı Komutlar -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="font-size:15px;font-weight:700;color:#1E293B;margin-bottom:16px;">
          Hızlı Komutlar <span style="font-size:13px;color:#94A3B8;font-weight:400;">(max 6)</span>
        </div>
        <div id="hizliKomutListesi" style="margin-bottom:10px;"></div>
        <button onclick="hizliKomutEkleGoster()" id="hizliKomutEkleBtn"
          style="border:1px dashed #CBD5E1;background:transparent;color:#6366f1;border-radius:8px;padding:10px;width:100%;cursor:pointer;font-size:13px;font-weight:600;transition:all 0.15s;"
          onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='transparent'">+ Yeni Komut Ekle</button>
        <div id="hizliKomutInput" style="display:none;margin-top:8px;">
          <input type="text" id="hizliKomutYeni" placeholder="Komut metnini yazın, Enter ile ekle..." maxlength="80"
            onkeydown="if(event.key==='Enter')hizliKomutEkle()"
            style="background:#F8FAFC;border:1.5px solid #6366f1;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;">
        </div>
      </div>

      <!-- Kart 3: Ses Asistanı -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <div>
            <div style="font-size:15px;font-weight:700;color:#1E293B;">🎙️ Ses Asistanı</div>
            <div style="font-size:12px;color:#64748B;margin-top:2px;">Yanıtları sesli dinle</div>
          </div>
          <label style="position:relative;display:inline-block;width:44px;height:24px;cursor:pointer;flex-shrink:0;">
            <input type="checkbox" ${sesAcik?'checked':''} onchange="aiSesToggle(this)" style="opacity:0;width:0;height:0;position:absolute;">
            <span id="sesTrack" style="position:absolute;inset:0;background:${sesAcik?'#6366f1':'#CBD5E1'};border-radius:24px;transition:0.3s;"></span>
            <span id="sesKnob"  style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:${sesAcik?'23px':'3px'};transition:0.3s;box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
          </label>
        </div>
        <div id="sesAyarlari" style="display:${sesAcik?'block':'none'};margin-top:16px;border-top:1px solid #F1F5F9;padding-top:16px;">
          <div style="margin-bottom:12px;">
            <label style="font-size:12px;font-weight:600;color:#475569;display:block;margin-bottom:8px;">Ses Hızı</label>
            <div style="display:flex;align-items:center;gap:10px;">
              <span style="font-size:12px;color:#64748B;">Yavaş</span>
              <input type="range" min="1" max="3" value="2" style="flex:1;accent-color:#6366f1;cursor:pointer;">
              <span style="font-size:12px;color:#64748B;">Hızlı</span>
            </div>
          </div>
          <div>
            <label style="font-size:12px;font-weight:600;color:#475569;display:block;margin-bottom:8px;">Ses</label>
            <input type="text" value="Ahmet (Erkek)" readonly
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#94A3B8;box-sizing:border-box;cursor:not-allowed;">
            <div style="font-size:11px;color:#94A3B8;margin-top:6px;">Yakında daha fazla ses seçeneği eklenecek</div>
          </div>
        </div>
      </div>

      <!-- Kart 4: AI Belleği -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
          <div>
            <div style="font-size:15px;font-weight:700;color:#1E293B;">AI Belleği</div>
            <div style="font-size:12px;color:#64748B;margin-top:2px;">Geçmiş konuşmaları hatırla</div>
          </div>
          <label style="position:relative;display:inline-block;width:44px;height:24px;cursor:pointer;flex-shrink:0;">
            <input type="checkbox" ${bellekAcik?'checked':''} onchange="localStorage.setItem('ai_bellek',this.checked);this.closest('label').querySelector('span:first-of-type').style.background=this.checked?'#6366f1':'#CBD5E1';this.closest('label').querySelector('span:last-of-type').style.left=this.checked?'23px':'3px';" style="opacity:0;width:0;height:0;position:absolute;">
            <span style="position:absolute;inset:0;background:${bellekAcik?'#6366f1':'#CBD5E1'};border-radius:24px;transition:0.3s;"></span>
            <span style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:${bellekAcik?'23px':'3px'};transition:0.3s;box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
          </label>
        </div>
        <button onclick="if(confirm('Tüm AI belleği silinecek. Emin misiniz?')){localStorage.removeItem('ai_bellek_data');localStorage.removeItem('konusma_gecmisi');showToast('AI belleği temizlendi','success');}"
          style="border:1px solid #EF4444;color:#EF4444;background:transparent;border-radius:8px;padding:8px 16px;font-size:14px;cursor:pointer;font-weight:600;transition:all 0.15s;"
          onmouseover="this.style.background='#FEF2F2'" onmouseout="this.style.background='transparent'">🗑️ Belleği Temizle</button>
      </div>`;
    hizliKomutListesiGuncelle();

  // ──────────────────────────────────────
  // 4. BİLDİRİM KANALLARI
  // ──────────────────────────────────────
  } else if (id === 'bildirim') {
    const bil = JSON.parse(localStorage.getItem('bildirim_kanallar') || '{}');
    const epAcik = !!bil.eposta;
    icerik.innerHTML = `
      <div style="margin-bottom:24px;">
        <div style="font-size:22px;font-weight:700;color:#0F172A;margin-bottom:4px;">Bildirim Kanalları</div>
        <div style="font-size:13px;color:#64748B;">Bildirimlerin nasıl ve nerede iletileceğini ayarla</div>
      </div>
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;overflow:hidden;">

        <!-- Uygulama İçi -->
        <div style="padding:16px 20px;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between;">
          <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:20px;">📱</span>
            <div>
              <div style="font-size:14px;font-weight:600;color:#0F172A;">Uygulama İçi</div>
              <div style="font-size:12px;color:#94A3B8;margin-top:1px;">BuildingAI içinde bildirim</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:12px;color:#94A3B8;">Her zaman aktif</span>
            <label style="position:relative;display:inline-block;width:44px;height:24px;opacity:0.6;cursor:not-allowed;">
              <input type="checkbox" checked disabled style="opacity:0;width:0;height:0;position:absolute;">
              <span style="position:absolute;inset:0;background:#6366f1;border-radius:24px;"></span>
              <span style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:23px;box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
            </label>
          </div>
        </div>

        <!-- E-posta -->
        <div style="border-bottom:1px solid #F1F5F9;">
          <div style="padding:16px 20px;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:12px;">
              <span style="font-size:20px;">📧</span>
              <div>
                <div style="font-size:14px;font-weight:600;color:#0F172A;">E-posta</div>
                <div style="font-size:12px;color:#94A3B8;margin-top:1px;">Önemli olaylar için e-posta al</div>
              </div>
            </div>
            <label style="position:relative;display:inline-block;width:44px;height:24px;cursor:pointer;flex-shrink:0;">
              <input type="checkbox" id="epostaToggle" ${epAcik?'checked':''} onchange="epostaToggleAyar(this)" style="opacity:0;width:0;height:0;position:absolute;">
              <span id="epostaToggleSpan" style="position:absolute;inset:0;background:${epAcik?'#6366f1':'#CBD5E1'};border-radius:24px;transition:0.3s;"></span>
              <span id="epostaToggleKnob" style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:${epAcik?'23px':'3px'};transition:0.3s;box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
            </label>
          </div>
          <div id="epostaAyarlar" style="display:${epAcik?'block':'none'};padding:0 20px 16px 52px;background:#FAFAFA;">
            <div style="display:flex;flex-direction:column;gap:10px;">
              ${[
                {k:'eposta_stok',   label:'Stok uyarıları',       def: bil.eposta_stok  !== false},
                {k:'eposta_isg',    label:'ISG ihlalleri',         def: bil.eposta_isg   !== false},
                {k:'eposta_rapor',  label:'Günlük rapor özeti',    def: !!bil.eposta_rapor},
                {k:'eposta_sistem', label:'Sistem bildirimleri',   def: !!bil.eposta_sistem}
              ].map(item => `
                <label style="display:flex;align-items:center;gap:10px;cursor:pointer;font-size:13px;color:#1E293B;">
                  <input type="checkbox" ${item.def?'checked':''} onchange="bildirimKaydet('${item.k}',this.checked)"
                    style="width:16px;height:16px;accent-color:#6366f1;cursor:pointer;">
                  ${item.label}
                </label>`).join('')}
            </div>
          </div>
        </div>

        <!-- WhatsApp -->
        <div style="padding:16px 20px;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between;">
          <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:20px;">💬</span>
            <div>
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:14px;font-weight:600;color:#0F172A;">WhatsApp</span>
                <span style="background:#FEF3C7;color:#D97706;font-size:11px;font-weight:600;padding:2px 8px;border-radius:20px;">Yakında</span>
              </div>
              <div style="font-size:12px;color:#94A3B8;margin-top:1px;">WhatsApp entegrasyonu için Pro plan gerekli</div>
            </div>
          </div>
          <label style="position:relative;display:inline-block;width:44px;height:24px;opacity:0.4;cursor:not-allowed;">
            <input type="checkbox" disabled style="opacity:0;width:0;height:0;position:absolute;">
            <span style="position:absolute;inset:0;background:#CBD5E1;border-radius:24px;"></span>
            <span style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:3px;"></span>
          </label>
        </div>

        <!-- SMS -->
        <div style="padding:16px 20px;display:flex;align-items:center;justify-content:space-between;">
          <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:20px;">📟</span>
            <div>
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:14px;font-weight:600;color:#0F172A;">SMS</span>
                <span style="background:#F1F5F9;color:#64748B;font-size:11px;font-weight:600;padding:2px 8px;border-radius:20px;">Yakında</span>
              </div>
              <div style="font-size:12px;color:#94A3B8;margin-top:1px;">Acil bildirimler için SMS</div>
            </div>
          </div>
          <label style="position:relative;display:inline-block;width:44px;height:24px;opacity:0.4;cursor:not-allowed;">
            <input type="checkbox" disabled style="opacity:0;width:0;height:0;position:absolute;">
            <span style="position:absolute;inset:0;background:#CBD5E1;border-radius:24px;"></span>
            <span style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:3px;"></span>
          </label>
        </div>

      </div>`;

  // ──────────────────────────────────────
  // 5. PLAN & ÖDEME
  // ──────────────────────────────────────
  } else if (id === 'plan') {
    const planRenk = {
      free:  {bg:'#F1F5F9', color:'#64748B',  label:'Ücretsiz'},
      pro:   {bg:'#EEF2FF', color:'#6366F1',  label:'⚡ Pro'},
      max:   {bg:'#F0FDF4', color:'#16A34A',  label:'👑 Max'},
      admin: {bg:'#F0FDF4', color:'#16A34A',  label:'🛡️ Admin'}
    };
    const pr = planRenk[plan] || planRenk.free;
    const upgradePlan = plan === 'free' ? 'pro' : 'max';
    icerik.innerHTML = `
      <div style="margin-bottom:24px;">
        <div style="font-size:22px;font-weight:700;color:#0F172A;margin-bottom:4px;">Plan &amp; Ödeme</div>
        <div style="font-size:13px;color:#64748B;">Abonelik ve kullanım bilgileri</div>
      </div>

      <!-- Kart 1: Aktif Plan -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
        <div>
          <div style="font-size:12px;color:#64748B;font-weight:500;margin-bottom:6px;">Aktif Plan</div>
          <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:22px;font-weight:800;color:#0F172A;">${pr.label}</span>
            <span style="background:${pr.bg};color:${pr.color};font-size:12px;font-weight:600;padding:4px 12px;border-radius:20px;">Aktif</span>
          </div>
        </div>
        ${(plan !== 'max' && plan !== 'admin') ? `
          <button onclick="odemePaneliAc('${upgradePlan}')"
            style="background:#6366f1;color:white;border:none;border-radius:8px;padding:10px 20px;font-size:13px;font-weight:700;cursor:pointer;transition:background 0.15s;"
            onmouseover="this.style.background='#4F46E5'" onmouseout="this.style.background='#6366f1'">
            ${plan === 'free' ? '⚡ Pro\'ya Geç' : '👑 Max\'e Geç'}
          </button>` : ''}
      </div>

      <!-- Kart 2: Kullanım İstatistikleri -->
      <div id="kullanımKarti" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:16px;">Kullanım İstatistikleri</div>
        <div style="display:flex;align-items:center;justify-content:center;padding:20px;">
          <div style="width:20px;height:20px;border:2px solid #6366f1;border-top-color:transparent;border-radius:50%;animation:spin 0.8s linear infinite;"></div>
        </div>
      </div>

      <!-- Kart 3: Ödeme Yöntemi -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:12px;">Ödeme Yöntemi</div>
        <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:12px 16px;color:#1D4ED8;font-size:13px;font-weight:500;margin-bottom:16px;">
          ℹ️ Manuel IBAN ile ödeme aktif
        </div>
        <button onclick="odemePaneliAc('pro')"
          style="border:1.5px solid #6366f1;background:transparent;color:#6366f1;border-radius:8px;padding:10px 20px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.15s;"
          onmouseover="this.style.background='#EEF2FF'" onmouseout="this.style.background='transparent'">💳 Ödeme Bildir</button>
      </div>

      <!-- Kart 4: Fatura Geçmişi -->
      <div id="faturaKarti" style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;">
        <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:12px;">Fatura Geçmişi</div>
        <div style="display:flex;align-items:center;justify-content:center;padding:20px;">
          <div style="width:20px;height:20px;border:2px solid #6366f1;border-top-color:transparent;border-radius:50%;animation:spin 0.8s linear infinite;"></div>
        </div>
      </div>`;
    ayarlarKullanımYukle();
    ayarlarFaturaYukle();

  // ──────────────────────────────────────
  // 6. GÜVENLİK & GİZLİLİK
  // ──────────────────────────────────────
  } else if (id === 'guvenlik') {
    icerik.innerHTML = `
      <div style="margin-bottom:24px;">
        <div style="font-size:22px;font-weight:700;color:#0F172A;margin-bottom:4px;">Güvenlik &amp; Gizlilik</div>
        <div style="font-size:13px;color:#64748B;">Hesap güvenliğini ve gizlilik tercihlerini yönet</div>
      </div>

      <!-- Kart 1: Şifre Değiştir -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:16px;">Şifre Değiştir</div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <div style="position:relative;">
            <input type="password" id="mevcutSifre" placeholder="Mevcut Şifre"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 44px 10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;transition:border-color 0.15s;"
              onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#E2E8F0'">
            <button onclick="sifreGoster('mevcutSifre',this)" type="button"
              style="position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;font-size:16px;color:#94A3B8;padding:0;line-height:1;">👁</button>
          </div>
          <div style="position:relative;">
            <input type="password" id="yeniSifre" placeholder="Yeni Şifre"
              oninput="sifreGucuHesapla(this)"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 44px 10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;transition:border-color 0.15s;"
              onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#E2E8F0'">
            <button onclick="sifreGoster('yeniSifre',this)" type="button"
              style="position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;font-size:16px;color:#94A3B8;padding:0;line-height:1;">👁</button>
          </div>
          <div id="sifreGucBar" style="display:none;">
            <div style="height:4px;background:#E2E8F0;border-radius:2px;overflow:hidden;margin-bottom:4px;">
              <div id="sifreGucDolgu" style="height:100%;width:0%;border-radius:2px;transition:all 0.3s;"></div>
            </div>
            <div id="sifreGucYazi" style="font-size:12px;font-weight:600;"></div>
          </div>
          <div style="position:relative;">
            <input type="password" id="yeniSifreTekrar" placeholder="Yeni Şifre (Tekrar)"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 44px 10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;transition:border-color 0.15s;"
              onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#E2E8F0'">
            <button onclick="sifreGoster('yeniSifreTekrar',this)" type="button"
              style="position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;font-size:16px;color:#94A3B8;padding:0;line-height:1;">👁</button>
          </div>
        </div>
        <button onclick="sifreGuncelle()"
          style="background:#6366f1;color:white;border:none;border-radius:8px;padding:10px 24px;font-size:14px;cursor:pointer;margin-top:16px;font-weight:600;transition:background 0.15s;"
          onmouseover="this.style.background='#4F46E5'" onmouseout="this.style.background='#6366f1'">Şifreyi Güncelle</button>
      </div>

      <!-- Kart 2: 2FA -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
              <span style="font-size:15px;font-weight:700;color:#0F172A;">İki Faktörlü Doğrulama</span>
              <span style="background:#F1F5F9;color:#64748B;font-size:11px;font-weight:600;padding:2px 8px;border-radius:20px;">Yakında</span>
            </div>
            <div style="font-size:12px;color:#94A3B8;">2FA yakında BuildingAI'a geliyor</div>
          </div>
          <label style="position:relative;display:inline-block;width:44px;height:24px;opacity:0.4;cursor:not-allowed;">
            <input type="checkbox" disabled style="opacity:0;width:0;height:0;position:absolute;">
            <span style="position:absolute;inset:0;background:#CBD5E1;border-radius:24px;"></span>
            <span style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:3px;"></span>
          </label>
        </div>
      </div>

      <!-- Kart 3: Veri & Gizlilik -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;">
        <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:16px;">Veri &amp; Gizlilik</div>
        <button onclick="showToast('Verileriniz hazırlanıyor...', 'info')"
          style="border:1px solid #E2E8F0;background:white;color:#1E293B;border-radius:8px;padding:10px 20px;font-size:14px;cursor:pointer;font-weight:600;transition:all 0.15s;"
          onmouseover="this.style.background='#F8FAFC'" onmouseout="this.style.background='white'">📥 Verilerimi İndir</button>
        <div style="height:1px;background:#E2E8F0;margin:20px 0;"></div>
        <button onclick="hesapSilOnay()"
          style="border:1px solid #EF4444;color:#EF4444;background:transparent;border-radius:8px;padding:10px 20px;font-size:14px;cursor:pointer;font-weight:600;transition:all 0.15s;"
          onmouseover="this.style.background='#FEF2F2'" onmouseout="this.style.background='transparent'">🗑️ Hesabımı Sil</button>
        <div style="font-size:12px;color:#94A3B8;margin-top:8px;">Bu işlem geri alınamaz. Tüm verileriniz kalıcı olarak silinir.</div>
      </div>`;
  }
}

// ─────────────────────────────────────────────────
// YARDIMCI FONKSİYONLAR — Şantiye Varsayılanları
// ─────────────────────────────────────────────────

function ayarlarSantiyeleriYukle() {
  const token = localStorage.getItem('bai_token');
  const sel = document.getElementById('varsayilanSantiyeSel');
  if (!sel || !token) return;
  fetch(`/santiyeler?token=${token}`)
    .then(r => r.json())
    .then(data => {
      const list = data.santiyeler || [];
      const varSantiye = JSON.parse(localStorage.getItem('varsayilan_santiye') || 'null');
      sel.innerHTML = '<option value="">Şantiye seçin...</option>' +
        list.map((s, i) => {
          const val = JSON.stringify(s).replace(/"/g,'&quot;');
          const selected = (varSantiye && varSantiye.id === s.id) ? 'selected' : '';
          return `<option value="${val}" ${selected}>${s.ad}</option>`;
        }).join('');
      if (varSantiye) {
        const kart = document.getElementById('varsayilanSantiyeKart');
        if (kart) { kart.style.display = 'block'; _santiyeKartGoster(kart, varSantiye); }
      }
    }).catch(() => {});
}

function varsayilanSantiyeSec(val) {
  const kart = document.getElementById('varsayilanSantiyeKart');
  if (!kart) return;
  if (!val) { kart.style.display = 'none'; localStorage.removeItem('varsayilan_santiye'); return; }
  try {
    const s = JSON.parse(val.replace(/&quot;/g,'"'));
    kart.style.display = 'block';
    _santiyeKartGoster(kart, s);
    localStorage.setItem('varsayilan_santiye', JSON.stringify(s));
  } catch(e) { kart.style.display = 'none'; }
}

function _santiyeKartGoster(kart, s) {
  const pct   = s.ilerleme || s.tamamlanma || 0;
  const konum = s.konum || s.adres || 'Konum belirtilmemiş';
  const isci  = s.isci_sayisi || s.toplam_isci || 0;
  kart.innerHTML =
    '<div style="font-size:13px;font-weight:700;color:#0F172A;margin-bottom:12px;">Seçili Şantiye Bilgileri</div>'
    + '<div style="display:flex;flex-direction:column;gap:10px;">'
    + '<div style="display:flex;align-items:center;gap:8px;font-size:13px;color:#1E293B;">'
    + '<svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#3B82F6" stroke-width="2"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>'
    + 'Konum: ' + konum + '</div>'
    + '<div style="display:flex;align-items:center;gap:8px;font-size:13px;color:#1E293B;">'
    + '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'
    + 'İlerleme: %' + pct + '</div>'
    + '<div style="display:flex;align-items:center;gap:8px;font-size:13px;color:#1E293B;">'
    + '<svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="#3B82F6" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>'
    + 'İşçi Sayısı: ' + isci + '</div>'
    + '</div>';
}

function birimToggle(tip) {
  const birimler = JSON.parse(localStorage.getItem('birim_sistemi') || '{}');
  const pairs = {uzunluk:['Metre','Feet'], alan:['m²','ft²'], agirlik:['kg','lb']};
  const pair  = pairs[tip] || [];
  const cur   = birimler[tip] || pair[0];
  const next  = (cur === pair[0]) ? pair[1] : pair[0];
  birimler[tip] = next;
  localStorage.setItem('birim_sistemi', JSON.stringify(birimler));
  const tog = document.getElementById('tog-' + tip);
  const lbl = document.getElementById('tog-label-' + tip);
  const on  = (next === pair[0]);
  if (tog) {
    tog.style.background = on ? '#3B82F6' : '#CBD5E1';
    tog.children[0].style.left = on ? '23px' : '3px';
  }
  if (lbl) lbl.textContent = next;
  showToast(tip.charAt(0).toUpperCase()+tip.slice(1)+' birimi: '+next, 'success');
}

function birimSec(tip, deger) {
  const birimler = JSON.parse(localStorage.getItem('birim_sistemi') || '{}');
  birimler[tip] = deger;
  localStorage.setItem('birim_sistemi', JSON.stringify(birimler));
  showToast(tip.charAt(0).toUpperCase()+tip.slice(1)+' birimi: '+deger, 'success');
}

function calismaGunToggle(gun, btn) {
  const saatler = JSON.parse(localStorage.getItem('calisma_saatleri') || '{"baslangic":"07:00","bitis":"18:00","gunler":["Pzt","Sal","Çar","Per","Cum"]}');
  const idx = saatler.gunler.indexOf(gun);
  if (idx === -1) {
    saatler.gunler.push(gun);
    btn.style.background = '#3B82F6'; btn.style.color = 'white';
  } else {
    saatler.gunler.splice(idx, 1);
    btn.style.background = '#1E293B'; btn.style.color = 'white';
  }
  localStorage.setItem('calisma_saatleri', JSON.stringify(saatler));
}

function calismaGunuKaydet() {
  const saatler = JSON.parse(localStorage.getItem('calisma_saatleri') || '{}');
  const bas = document.getElementById('saatBaslangic');
  const bit = document.getElementById('saatBitis');
  if (bas) saatler.baslangic = bas.value;
  if (bit) saatler.bitis     = bit.value;
  localStorage.setItem('calisma_saatleri', JSON.stringify(saatler));
}

// ─────────────────────────────────────────────────
// YARDIMCI FONKSİYONLAR — AI Asistan
// ─────────────────────────────────────────────────

function aiYanitStilSec(stil) {
  localStorage.setItem('ai_yanit_stili', stil);
  ['kisa','normal','ayrintili'].forEach(k => {
    const el = document.getElementById('aiStil-' + k);
    if (!el) return;
    el.style.border     = (k === stil) ? '2px solid #6366F1' : '1px solid #E2E8F0';
    el.style.background = (k === stil) ? '#EEF2FF'           : '#FFFFFF';
    el.style.color      = (k === stil) ? '#4338CA'           : '#1E293B';
  });
}

function aiKonusmaTonuSec(ton) {
  localStorage.setItem('ai_konusma_tonu', ton);
  ['saha_arkadasi','hizli_bakis','hikaye_modu'].forEach(k => {
    const el = document.getElementById('aiTon-' + k);
    if (!el) return;
    el.style.border     = (k === ton) ? '2px solid #6366F1' : '1px solid #E2E8F0';
    el.style.background = (k === ton) ? '#EEF2FF'           : '#FFFFFF';
    el.style.color      = (k === ton) ? '#4338CA'           : '#1E293B';
  });
}

function hizliKomutListesiGuncelle() {
  const liste = document.getElementById('hizliKomutListesi');
  if (!liste) return;
  const komutlar = JSON.parse(localStorage.getItem('ai_hizli_komutlar') || JSON.stringify(AI_QUICK_COMMANDS));
  if (!komutlar.length) {
    liste.innerHTML = '<div style="font-size:13px;color:#94A3B8;text-align:center;padding:16px 0;">Henüz komut eklenmedi</div>';
    return;
  }
  liste.innerHTML = komutlar.map((k, i) => `
    <div style="display:flex;align-items:center;gap:10px;background:#F8FAFC;border-radius:8px;padding:10px 12px;margin-bottom:6px;">
      <span style="color:#CBD5E1;font-size:16px;cursor:grab;user-select:none;">⠿</span>
      <span style="flex:1;font-size:14px;color:#1E293B;">${k}</span>
      <button onclick="hizliKomutSil(${i})"
        style="background:none;border:none;cursor:pointer;color:#94A3B8;font-size:16px;padding:0;line-height:1;transition:color 0.15s;"
        onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='#94A3B8'">🗑</button>
    </div>`).join('');
}

function hizliKomutEkleGoster() {
  const komutlar = JSON.parse(localStorage.getItem('ai_hizli_komutlar') || JSON.stringify(AI_QUICK_COMMANDS));
  if (komutlar.length >= 6) { showToast('Maksimum 6 hızlı komut eklenebilir', 'error'); return; }
  const inputDiv = document.getElementById('hizliKomutInput');
  if (inputDiv) { inputDiv.style.display = 'block'; document.getElementById('hizliKomutYeni').focus(); }
}

function hizliKomutEkle() {
  const input = document.getElementById('hizliKomutYeni');
  if (!input || !input.value.trim()) return;
  const komutlar = JSON.parse(localStorage.getItem('ai_hizli_komutlar') || JSON.stringify(AI_QUICK_COMMANDS));
  if (komutlar.length >= 6) { showToast('Maksimum 6 hızlı komut', 'error'); return; }
  komutlar.push(input.value.trim());
  localStorage.setItem('ai_hizli_komutlar', JSON.stringify(komutlar));
  input.value = '';
  const inputDiv = document.getElementById('hizliKomutInput');
  if (inputDiv) inputDiv.style.display = 'none';
  hizliKomutListesiGuncelle();
  showToast('Komut eklendi', 'success');
}

function hizliKomutSil(idx) {
  const komutlar = JSON.parse(localStorage.getItem('ai_hizli_komutlar') || JSON.stringify(AI_QUICK_COMMANDS));
  komutlar.splice(idx, 1);
  localStorage.setItem('ai_hizli_komutlar', JSON.stringify(komutlar));
  hizliKomutListesiGuncelle();
  showToast('Komut silindi', 'info');
}

function aiSesToggle(cb) {
  localStorage.setItem('ai_ses_asistan', cb.checked);
  const ayarlar = document.getElementById('sesAyarlari');
  const track   = document.getElementById('sesTrack');
  const knob    = document.getElementById('sesKnob');
  if (ayarlar) ayarlar.style.display = cb.checked ? 'block' : 'none';
  if (track)   track.style.background = cb.checked ? '#6366f1' : '#CBD5E1';
  if (knob)    knob.style.left        = cb.checked ? '23px' : '3px';
}

// ─────────────────────────────────────────────────
// YARDIMCI FONKSİYONLAR — Bildirimler
// ─────────────────────────────────────────────────

function epostaToggleAyar(cb) {
  const bil = JSON.parse(localStorage.getItem('bildirim_kanallar') || '{}');
  bil.eposta = cb.checked;
  localStorage.setItem('bildirim_kanallar', JSON.stringify(bil));
  const ayarlar = document.getElementById('epostaAyarlar');
  const span    = document.getElementById('epostaToggleSpan');
  const knob    = document.getElementById('epostaToggleKnob');
  if (ayarlar) ayarlar.style.display  = cb.checked ? 'block' : 'none';
  if (span)    span.style.background  = cb.checked ? '#6366f1' : '#CBD5E1';
  if (knob)    knob.style.left        = cb.checked ? '23px' : '3px';
}

function bildirimKaydet(key, val) {
  const bil = JSON.parse(localStorage.getItem('bildirim_kanallar') || '{}');
  bil[key] = val;
  localStorage.setItem('bildirim_kanallar', JSON.stringify(bil));
}

// ─────────────────────────────────────────────────
// YARDIMCI FONKSİYONLAR — Plan & Kullanım
// ─────────────────────────────────────────────────

async function ayarlarKullanımYukle() {
  const token = localStorage.getItem('bai_token');
  const kart  = document.getElementById('kullanımKarti');
  if (!kart || !token) return;
  try {
    const res  = await fetch(`/kullanim-durumu?token=${token}`);
    const data = await res.json();
    if (!res.ok) throw new Error();
    const k = data.kullanim;
    const metrikler = [
      {label:'AI Sorgu (bugün)',         used: k.sor.kullanilan,           limit: k.sor.limit},
      {label:'Kamera Analizi (bu hafta)', used: k.kamera.kullanilan,        limit: k.kamera.limit},
      {label:'Haftalık Rapor (bu ay)',    used: k.gunluk_rapor.kullanilan,  limit: k.gunluk_rapor.limit}
    ];
    kart.innerHTML = `
      <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:16px;">Kullanım İstatistikleri</div>
      ${metrikler.map(m => {
        const pct   = m.limit === null ? 100 : Math.min(100, Math.round((m.used / m.limit) * 100));
        const label = m.limit === null ? `${m.used} / ∞` : `${m.used} / ${m.limit}`;
        return `
          <div style="margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
              <span style="font-size:13px;color:#64748B;font-weight:500;">${m.label}</span>
              <span style="font-size:13px;font-weight:700;color:#0F172A;">${label}</span>
            </div>
            <div style="height:6px;background:#E2E8F0;border-radius:3px;overflow:hidden;">
              <div style="height:100%;width:${pct}%;background:${m.limit===null?'#3B82F6':'#6366f1'};border-radius:3px;transition:width 0.4s;"></div>
            </div>
          </div>`;
      }).join('')}`;
  } catch(e) {
    if (kart) kart.innerHTML = '<div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:16px;">Kullanım İstatistikleri</div><div style="font-size:13px;color:#94A3B8;text-align:center;padding:16px;">Veri yüklenemedi</div>';
  }
}

async function ayarlarFaturaYukle() {
  const token = localStorage.getItem('bai_token');
  const kart  = document.getElementById('faturaKarti');
  if (!kart || !token) return;
  try {
    const res  = await fetch(`/odeme-bildirimi?token=${token}`);
    const data = await res.json();
    const odemeler = data.odemeler || [];
    if (!odemeler.length) {
      kart.innerHTML = '<div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:12px;">Fatura Geçmişi</div><div style="text-align:center;padding:24px;color:#94A3B8;font-size:13px;">Henüz ödeme geçmişi yok</div>';
      return;
    }
    kart.innerHTML = `
      <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:12px;">Fatura Geçmişi</div>
      <table style="width:100%;border-collapse:collapse;">
        <thead>
          <tr style="border-bottom:1px solid #E2E8F0;">
            <th style="text-align:left;font-size:12px;font-weight:600;color:#64748B;padding-bottom:10px;">Tarih</th>
            <th style="text-align:left;font-size:12px;font-weight:600;color:#64748B;padding-bottom:10px;">Tutar</th>
            <th style="text-align:left;font-size:12px;font-weight:600;color:#64748B;padding-bottom:10px;">Durum</th>
          </tr>
        </thead>
        <tbody>
          ${odemeler.map(o => `
            <tr style="border-bottom:1px solid #F1F5F9;">
              <td style="padding:10px 0;font-size:13px;color:#1E293B;">${o.tarih||'—'}</td>
              <td style="padding:10px 0;font-size:13px;color:#1E293B;font-weight:600;">${o.tutar||'—'}</td>
              <td style="padding:10px 0;">
                <span style="background:${o.durum==='onaylandi'?'#F0FDF4':'#FFFBEB'};color:${o.durum==='onaylandi'?'#16A34A':'#D97706'};font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;">
                  ${o.durum==='onaylandi'?'Onaylandı':'Bekliyor'}
                </span>
              </td>
            </tr>`).join('')}
        </tbody>
      </table>`;
  } catch(e) {
    if (kart) kart.innerHTML = '<div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:12px;">Fatura Geçmişi</div><div style="text-align:center;padding:24px;color:#94A3B8;font-size:13px;">Henüz ödeme geçmişi yok</div>';
  }
}

// ─────────────────────────────────────────────────
// YARDIMCI FONKSİYONLAR — Güvenlik
// ─────────────────────────────────────────────────

function sifreGoster(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.type     = input.type === 'password' ? 'text' : 'password';
  btn.textContent = input.type === 'text' ? '🙈' : '👁';
}

async function sifreGuncelle() {
  const mevcut = document.getElementById('mevcutSifre')?.value;
  const yeni   = document.getElementById('yeniSifre')?.value;
  const tekrar = document.getElementById('yeniSifreTekrar')?.value;
  if (!mevcut || !yeni || !tekrar)      { showToast('Tüm alanları doldurun', 'error'); return; }
  if (yeni !== tekrar)                  { showToast('Yeni şifreler eşleşmiyor', 'error'); return; }
  if (yeni.length < 6)                  { showToast('Şifre en az 6 karakter olmalı', 'error'); return; }
  const token = localStorage.getItem('bai_token');
  try {
    const res  = await fetch('/sifre-guncelle', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({token, mevcut_sifre: mevcut, yeni_sifre: yeni})
    });
    const data = await res.json();
    if (res.ok) {
      showToast('Şifre başarıyla güncellendi', 'success');
      ['mevcutSifre','yeniSifre','yeniSifreTekrar'].forEach(id => {
        const el = document.getElementById(id); if (el) el.value = '';
      });
      const bar = document.getElementById('sifreGucBar');
      if (bar) bar.style.display = 'none';
    } else { showToast(data.hata || 'Şifre güncellenemedi', 'error'); }
  } catch(e) { showToast('Bağlantı hatası', 'error'); }
}

function hesapSilOnay() {
  if (!confirm('Hesabınız kalıcı olarak silinecek. Devam et?')) return;
  const sifre = prompt('Silmek için şifrenizi girin:');
  if (!sifre) return;
  showToast('Bu işlem için destek ekibiyle iletişime geçin', 'info');
}

// ─────────────────────────────────────────────────
// YARDIMCI FONKSİYONLAR — Dil
// ─────────────────────────────────────────────────

function ayarlarDilSec(dil) {
  localStorage.setItem('ayarlar_dil', dil);
  if (typeof dilDegistir === 'function') dilDegistir(dil);
  ['TR','EN'].forEach(d => {
    const btn = document.getElementById('dil'+d);
    if (!btn) return;
    const aktif = (d.toLowerCase() === dil);
    btn.style.border     = aktif ? '1.5px solid #6366f1' : '1.5px solid #E2E8F0';
    btn.style.background = aktif ? '#EEF2FF'             : '#F8FAFC';
    btn.style.color      = aktif ? '#6366F1'             : '#64748B';
  });
}

// ═══════════════════════════════════════════════════
// 👤 PROFİL KAYDET
// ═══════════════════════════════════════════════════

function profilKaydet() {
  const adSoyad = document.getElementById('ayarlarAdSoyad')?.value.trim();
  const telefon = document.getElementById('ayarlarTelefon')?.value.trim();
  const rol     = document.getElementById('ayarlarRol')?.value;
  if (!adSoyad) { showToast('Ad Soyad alanı boş bırakılamaz', 'error'); return; }

  const user = JSON.parse(localStorage.getItem('bai_user') || '{}');
  user.full_name = adSoyad;
  user.telefon   = telefon;
  user.rol       = rol;
  localStorage.setItem('bai_user', JSON.stringify(user));
  if (rol) localStorage.setItem('bai_rol', rol);

  if (aktifKullanici) { aktifKullanici.full_name = adSoyad; aktifKullanici.telefon = telefon; }

  // Header güncelle
  const headerName = document.getElementById('headerUserName');
  if (headerName) headerName.textContent = adSoyad;
  const headerAvt = document.getElementById('headerAvatar');
  if (headerAvt) {
    headerAvt.textContent = adSoyad.split(' ').filter(Boolean).map(w=>w[0]).join('').toUpperCase().slice(0,2);
  }
  showToast('Profil kaydedildi', 'success');
}

// ═══════════════════════════════════════════════════
// 🔑 ŞİFRE GÜCÜ
// ═══════════════════════════════════════════════════

function sifreGucuHesapla(input) {
  const val  = input.value;
  const bar  = document.getElementById('sifreGucBar');
  const fill = document.getElementById('sifreGucDolgu');
  const yazi = document.getElementById('sifreGucYazi');
  if (!bar || !fill || !yazi) return;
  if (!val) { bar.style.display = 'none'; return; }
  bar.style.display = 'block';
  if (val.length <= 3) {
    fill.style.width = '33%'; fill.style.background = '#EF4444';
    yazi.textContent = 'Zayıf'; yazi.style.color = '#EF4444';
  } else if (val.length <= 7) {
    fill.style.width = '66%'; fill.style.background = '#F59E0B';
    yazi.textContent = 'Orta'; yazi.style.color = '#F59E0B';
  } else {
    fill.style.width = '100%'; fill.style.background = '#22C55E';
    yazi.textContent = 'Güçlü'; yazi.style.color = '#22C55E';
  }
}

// ═══════════════════════════════════════════════════
// 👤 AVATAR DROPDOWN MENU
// ═══════════════════════════════════════════════════

function avatarMenuAc() {
  const menu = document.getElementById('avatarMenu');
  if (!menu) return;
  const visible = menu.style.display !== 'none';
  menu.style.display = visible ? 'none' : 'block';

  if (!visible) {
    // Kullanıcı bilgilerini doldur
    const user  = JSON.parse(localStorage.getItem('bai_user') || '{}');
    const kUser = aktifKullanici || user;
    const isim  = kUser.full_name || 'Kullanıcı';
    const email = kUser.email     || '';
    const initials = isim.split(' ').filter(Boolean).map(w=>w[0]).join('').toUpperCase().slice(0,2) || 'U';
    const rolLabel = localStorage.getItem('bai_rol') === 'muhendis' ? 'Mühendis' : 'Şantiye Şefi';

    const amAvatar = document.getElementById('amAvatar');
    const amName   = document.getElementById('amName');
    const amEmail  = document.getElementById('amEmail');
    const amRole   = document.getElementById('amRole');
    if (amAvatar) amAvatar.textContent = initials;
    if (amName)   amName.textContent   = isim;
    if (amEmail)  amEmail.textContent  = email;
    if (amRole)   amRole.textContent   = rolLabel;

    // Aktif şantiye
    const varSantiye    = JSON.parse(localStorage.getItem('varsayilan_santiye') || 'null');
    const amSantiyeAd   = document.getElementById('amSantiyeAd');
    const amSantiyeBar  = document.getElementById('amSantiyeBar');
    const amSantiyeAlt  = document.getElementById('amSantiyeAlt');
    if (varSantiye && amSantiyeAd) {
      amSantiyeAd.textContent  = varSantiye.ad || '—';
      if (amSantiyeBar) setTimeout(() => amSantiyeBar.style.width = (varSantiye.ilerleme||0)+'%', 50);
      if (amSantiyeAlt) amSantiyeAlt.textContent = `%${varSantiye.ilerleme||0} · ${varSantiye.isci_sayisi||0} işçi`;
    } else if (amSantiyeAd) {
      amSantiyeAd.textContent = 'Varsayılan şantiye seçilmedi';
    }

    // Dışarı tıklayınca kapat
    setTimeout(() => {
      document.addEventListener('click', function _amHandler(e) {
        const m = document.getElementById('avatarMenu');
        if (m && !m.contains(e.target) && !e.target.closest('[onclick*="avatarMenuAc"]')) {
          m.style.display = 'none';
          document.removeEventListener('click', _amHandler);
        }
      });
    }, 0);
  }
}

function temaDegistir() {
  showToast('Karanlık mod yakında eklenecek', 'info');
  // Toggle'ı geri al
  const cb = document.getElementById('karanlikModToggle');
  if (cb) cb.checked = false;
}
</script>
"""
