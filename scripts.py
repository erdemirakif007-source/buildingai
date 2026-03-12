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
            <div class="nav-item" id="nav-deprem" onclick="${depremOnclick}"${depremLock}><span class="nav-icon">🌍</span><span class="nav-label">Deprem Analizi${depremKilit?' 🔒':''}</span></div>`;
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
            <div class="nav-item" id="nav-santiye" onclick="${santiyeOnclick}"${santiyeLock}><span class="nav-icon">🏗️</span><span class="nav-label">Şantiye Yönetimi${santiyeKilit?' 🔒':''}</span></div>`;
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
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : "Sivas";
    const tempEl = document.getElementById('temp');
    const condEl = document.getElementById('condition');
    try {
        const res = await fetch(`/hava?sehir=${sehir}`);
        const data = await res.json();
        if (tempEl) tempEl.innerText = data.temp;
        if (condEl) condEl.innerText = data.cond;
    } catch (e) {
        if (condEl) condEl.innerText = "Bağlantı Yok";
    }
}

// --- 🌑 SIDEBAR KONTROLLERİ ---
function toggleSidebar() {
    const side = document.getElementById('sidebar');
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
    const payload = { soru: soru, hava: hava, resim_base64: secilenResimBase64, dil: aktifDil, token };

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

        const t = TRANSLATIONS[aktifDil];
        const formatliCevap = markdownToHtml(data.cevap);
        resBox.innerHTML = `
            <div class="res-title">${t.aiAnaliz}</div>
            <div id="analizMetni" style="color:#ddd; font-size:0.95rem; line-height:1.7; margin-top:10px;">${formatliCevap}</div>
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
let modalResolve;

function openModal(title, fields) {
    document.getElementById('modalTitle').innerText = title;
    const body = document.getElementById('modalBody');
    body.innerHTML = '';
    fields.forEach(f => {
        body.innerHTML += `
            <label style="display:block; margin-top:10px; color:#aaa; font-size:0.8rem;">${f.label}</label>
            <input type="number" step="any" class="modal-input" id="field_${f.key}" placeholder="${f.placeholder}"
            style="width:100%; background:rgba(255,255,255,0.05); border:1px solid #444; border-radius:10px; padding:12px; color:white; margin-top:5px; outline:none; box-sizing:border-box;">
        `;
    });
    document.getElementById('inputModal').style.display = 'flex';
    setTimeout(() => document.getElementById('inputModal').classList.add('active'), 10);
    return new Promise((resolve) => { modalResolve = resolve; });
}

function submitModal() {
    const inputs = {};
    document.querySelectorAll('.modal-input').forEach(i => {
        inputs[i.id.replace('field_', '')] = i.value;
    });
    document.getElementById('inputModal').classList.remove('active');
    setTimeout(() => document.getElementById('inputModal').style.display = 'none', 300);
    if (modalResolve) modalResolve(inputs);
}

function closeModal() {
    document.getElementById('inputModal').classList.remove('active');
    setTimeout(() => document.getElementById('inputModal').style.display = 'none', 300);
    if (modalResolve) modalResolve(null);
}

// --- 🧮 MÜHENDİSLİK HESAPLAMALARI ---
async function runCalc(type) {
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

    const dataInput = await openModal(title, fields);
    if (!dataInput) return;

    const resBox = document.getElementById('result');
    resBox.innerHTML = "<i>Şefim, hesaplanıyor...</i>";

    try {
        const response = await fetch(`/hesapla?tip=${type}&v1=${dataInput.v1 || 0}&v2=${dataInput.v2 || 0}&v3=${dataInput.v3 || 0}`);
        const data = await response.json();
        resBox.innerHTML = `<div class="res-title">📊 ANALİZ SONUCU</div><div class="res-value">${data.sonuc}</div><div class="res-detail">${data.detay}</div>`;
    } catch (e) {
        resBox.innerHTML = "⚠️ HESAPLAMA HATASI";
    }
}

// --- 📝 MARKDOWN → HTML ---
function markdownToHtml(text) {
    return text
        .replace(/## 📋(.+)/g, '<h3 style="color:#e67e22; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(230,126,34,0.3); padding-bottom:6px;">📋$1</h3>')
        .replace(/## ⚠️(.+)/g, '<h3 style="color:#f39c12; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(243,156,18,0.3); padding-bottom:6px;">⚠️$1</h3>')
        .replace(/## 🛡️(.+)/g, '<h3 style="color:#2ecc71; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(46,204,113,0.3); padding-bottom:6px;">🛡️$1</h3>')
        .replace(/## 📐(.+)/g, '<h3 style="color:#3498db; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(52,152,219,0.3); padding-bottom:6px;">📐$1</h3>')
        .replace(/## (.+)/g, '<h3 style="color:#e67e22; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(230,126,34,0.3); padding-bottom:6px;">$1</h3>')
        .replace(/\*\*(.+?)\*\*/g, '<strong style="color:#fff;">$1</strong>')
        .replace(/^\* (.+)/gm, '<li style="margin:4px 0; color:#ddd;">$1</li>')
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

async function kameraAnalizGonder(base64) {
    const token = localStorage.getItem('bai_token');
    const analiz_tipi = document.getElementById('kameraAnalizTipi').value;
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'Sivas';
    const hava = (document.getElementById('temp') ? document.getElementById('temp').innerText : '') + ' ' +
                 (document.getElementById('condition') ? document.getElementById('condition').innerText : '');
    const resBox = document.getElementById('result');
    kameraKapat();
    resBox.innerHTML = '<i>📸 Fotoğraf analiz ediliyor...</i>';

    // Store image for bounding box overlay
    const imgData = 'data:image/jpeg;base64,' + base64;

    try {
        const res = await fetch('/kamera-analiz', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, resim_base64: base64, analiz_tipi, hava, sehir, dil: aktifDil})
        });

        if (res.status === 429) {
            const err = await res.json();
            resBox.innerHTML = `<div style="text-align:center;padding:20px"><div style="font-size:2rem">🔒</div><strong style="color:#e74c3c">Limit doldu!</strong><div style="color:#aaa;margin-top:8px">${err.detail}</div></div>`;
            return;
        }

        const data = await res.json();
        const p = data.parsed;
        const t = TRANSLATIONS[aktifDil];

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

                <!-- Bounding Box Canvas -->
                <div style="position:relative;margin:16px 0;border-radius:12px;overflow:hidden;">
                    <img id="analizImg" src="${imgData}" style="width:100%;display:block;border-radius:12px;">
                    <canvas id="bbCanvas" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;"></canvas>
                </div>

                <!-- Skor -->
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

            // Draw bounding boxes
            const img = document.getElementById('analizImg');
            img.onload = () => drawBoundingBoxes(p.ihlaller || []);
            if (img.complete) drawBoundingBoxes(p.ihlaller || []);

        } else if (analiz_tipi === 'ilerleme' && p) {
            const yuzde = Math.min(100, Math.max(0, p.ilerleme_yuzdesi || 0));
            const renk = yuzde >= 71 ? '#2ecc71' : yuzde >= 31 ? '#f59e0b' : '#ef4444';
            const tamamlanan = (p.tamamlanan_isler || []).map(i => `<li style="color:#86efac;margin:4px 0;font-size:0.88rem;">✅ ${i}</li>`).join('');
            const devam = (p.devam_eden_isler || []).map(i => `<li style="color:#93c5fd;margin:4px 0;font-size:0.88rem;">🔄 ${i}</li>`).join('');
            const gecikmeler = (p.olasi_gecikmeler || []).map(i => `<li style="color:#fcd34d;margin:4px 0;font-size:0.88rem;">⚠️ ${i}</li>`).join('');

            resBox.innerHTML = `
                <div class="res-title">📅 İLERLEME TAKİBİ</div>

                <!-- Animasyonlu Daire -->
                <div style="display:flex;justify-content:center;margin:24px 0;">
                    <div style="position:relative;width:140px;height:140px;">
                        <svg width="140" height="140" style="transform:rotate(-90deg)">
                            <circle cx="70" cy="70" r="58" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="12"/>
                            <circle id="progressCircle" cx="70" cy="70" r="58" fill="none" stroke="${renk}" stroke-width="12"
                                stroke-dasharray="${2 * Math.PI * 58}"
                                stroke-dashoffset="${2 * Math.PI * 58}"
                                stroke-linecap="round"
                                style="transition:stroke-dashoffset 1.5s cubic-bezier(0.19,1,0.22,1)"/>
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

            // Animate progress
            setTimeout(() => {
                const circle = document.getElementById('progressCircle');
                const numEl = document.getElementById('progressNum');
                if (circle) {
                    const circumference = 2 * Math.PI * 58;
                    circle.style.strokeDashoffset = circumference * (1 - yuzde / 100);
                }
                if (numEl) {
                    let current = 0;
                    const step = yuzde / 60;
                    const timer = setInterval(() => {
                        current = Math.min(yuzde, current + step);
                        numEl.textContent = Math.round(current) + '%';
                        if (current >= yuzde) clearInterval(timer);
                    }, 25);
                }
            }, 100);

        } else if (analiz_tipi === 'genel' && p && p.kategoriler) {
            const k = p.kategoriler;
            const durumRenk = (d) => d === 'iyi' ? '#2ecc71' : d === 'orta' ? '#f59e0b' : d === 'kotu' ? '#ef4444' : '#94a3b8';
            const seviyeRenk = (s) => s === 'dusuk' ? '#2ecc71' : s === 'orta' ? '#f59e0b' : '#ef4444';

            resBox.innerHTML = `
                <div class="res-title">🔍 GENEL ANALİZ</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:16px;">
                    <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                            <span style="font-size:1.2rem;">🦺</span>
                            <span style="color:${durumRenk(k.guvenlik?.durum)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.guvenlik?.durum || '-'}</span>
                        </div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Güvenlik</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.guvenlik?.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                            <span style="font-size:1.2rem;">📅</span>
                            <span style="color:${durumRenk(k.ilerleme?.durum)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.ilerleme?.durum || '-'}</span>
                        </div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">İlerleme</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.ilerleme?.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(249,115,22,0.08);border:1px solid rgba(249,115,22,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                            <span style="font-size:1.2rem;">📦</span>
                            <span style="color:var(--primary);font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.malzeme?.durum || '-'}</span>
                        </div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Malzeme</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.malzeme?.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                            <span style="font-size:1.2rem;">⚠️</span>
                            <span style="color:${seviyeRenk(k.risk?.seviye)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.risk?.seviye || '-'}</span>
                        </div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Risk</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.risk?.ozet || ''}</div>
                    </div>
                </div>
                <div id="analizMetni" style="display:none;">${data.cevap || ''}</div>
                <button onclick="pdfIndir()" style="width:100%;margin-top:16px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">📄 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
        } else {
            // Fallback to markdown
            resBox.innerHTML = `
                <div class="res-title">📸 KAMERA ANALİZİ</div>
                <div id="analizMetni" style="color:#ddd;font-size:0.95rem;line-height:1.7;margin-top:10px;">${markdownToHtml(data.cevap)}</div>
                <button onclick="pdfIndir()" style="width:100%;margin-top:15px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">📄 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
        }

        // Store for analizMetni compatibility
        sonAiCevabi = data.cevap;

    } catch(e) {
        resBox.innerHTML = `<div style="color:#e74c3c;">Analiz hatası: ${e.message}</div>`;
    }
}

// Bounding box çizici
function drawBoundingBoxes(ihlaller) {
    const canvas = document.getElementById('bbCanvas');
    const img = document.getElementById('analizImg');
    if (!canvas || !img) return;
    canvas.width = img.naturalWidth || img.offsetWidth;
    canvas.height = img.naturalHeight || img.offsetHeight;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ihlaller.forEach((ih, i) => {
        const x = ih.x * canvas.width;
        const y = ih.y * canvas.height;
        const w = ih.w * canvas.width;
        const h = ih.h * canvas.height;
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, w, h);
        ctx.fillStyle = 'rgba(239,68,68,0.8)';
        ctx.fillRect(x, y - 22, Math.min(w, 200), 22);
        ctx.fillStyle = 'white';
        ctx.font = 'bold 12px Arial';
        ctx.fillText(`${i+1}. ${ih.aciklama}`, x + 4, y - 6);
    });
}

// --- 📁 ARŞİV ---
async function arsivAc() {
    const token = localStorage.getItem('bai_token');
    if (!token) return;
    document.getElementById('arsivModal').style.display = 'flex';
    document.getElementById('arsivIcerik').innerHTML = `<i>${aktifDil === 'tr' ? 'Yükleniyor...' : 'Loading...'}</i>`;
    try {
        const res = await fetch(`/arsiv?token=${token}`);
        const data = await res.json();
        let html = '';
        if (data.raporlar.length > 0) {
            html += `<h3 style="color:#e67e22; margin:10px 0 12px 0;">📊 ${aktifDil === 'tr' ? 'AI Raporları' : 'AI Reports'} (${data.raporlar.length})</h3>`;
            data.raporlar.forEach(r => {
                html += `<div onclick="arsivDetayGoster('rapor',${r.id})" style="background:#1a1d21; border-radius:10px; padding:12px; margin-bottom:8px; cursor:pointer; border:1px solid rgba(230,126,34,0.2);">
                    <div style="color:#e67e22; font-size:0.8rem;">📄 ${r.tarih || r.created_at.slice(0,10)}</div>
                    <div style="color:#ddd; font-size:0.85rem; margin-top:4px;">${r.ozet}</div></div>`;
            });
        }
        if (data.kamera_analizler.length > 0) {
            html += `<h3 style="color:#3498db; margin:20px 0 12px 0;">📸 ${aktifDil === 'tr' ? 'Kamera Analizleri' : 'Camera Analyses'} (${data.kamera_analizler.length})</h3>`;
            data.kamera_analizler.forEach(k => {
                const ikon = k.tip === 'guvenlik' ? '🦺' : k.tip === 'ilerleme' ? '📅' : '🔍';
                html += `<div onclick="arsivDetayGoster('kamera',${k.id})" style="background:#1a1d21; border-radius:10px; padding:12px; margin-bottom:8px; cursor:pointer; border:1px solid rgba(52,152,219,0.2);">
                    <div style="color:#3498db; font-size:0.8rem;">${ikon} ${k.tip} — ${k.sehir} — ${k.created_at.slice(0,10)}</div>
                    <div style="color:#ddd; font-size:0.85rem; margin-top:4px;">${k.ozet}</div></div>`;
            });
        }
        if (!html) html = `<div style="text-align:center; color:#aaa; padding:40px;">${aktifDil === 'tr' ? 'Henüz kayıt yok.' : 'No records yet.'}</div>`;
        document.getElementById('arsivIcerik').innerHTML = html;
    } catch(e) {
        document.getElementById('arsivIcerik').innerHTML = '<div style="color:#e74c3c;">Arşiv yüklenemedi.</div>';
    }
}

async function arsivDetayGoster(tip, id) {
    const token = localStorage.getItem('bai_token');
    const res = await fetch(`/arsiv/${tip}/${id}?token=${token}`);
    const data = await res.json();
    const icerik = data.content || data.sonuc || '';
    document.getElementById('arsivIcerik').innerHTML = `
        <button onclick="arsivAc()" style="background:rgba(255,255,255,0.1); border:none; color:white; padding:8px 15px; border-radius:8px; cursor:pointer; margin-bottom:15px;">← ${aktifDil === 'tr' ? 'Geri' : 'Back'}</button>
        <div style="color:#ddd; font-size:0.95rem; line-height:1.7;">${markdownToHtml(icerik)}</div>`;
}

function arsivKapat() { document.getElementById('arsivModal').style.display = 'none'; }

let secilenPlan = 'free';

function switchPanel(panel) {
    document.getElementById('panel-login').style.display = 'none';
    document.getElementById('panel-register').style.display = 'none';
    document.getElementById('panel-forgot').style.display = 'none';
    document.getElementById('panel-' + panel).style.display = 'block';
}

function selectPlan(plan) {
    secilenPlan = plan;
    document.getElementById('plan-free').classList.toggle('selected', plan === 'free');
    document.getElementById('plan-pro').classList.toggle('selected', plan === 'pro');
}

// --- KAYIT SİSTEMİ ---
async function kayitOl() {
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
    if (pass.length < 6) {
        msg.innerHTML = '<div class="msg-error">Şifre en az 6 karakter olmalı.</div>';
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
            body: JSON.stringify({ email, password: pass, full_name: name, plan: secilenPlan })
        });
        const data = await response.json();

        if (response.ok) {
            msg.innerHTML = '<div class="msg-success">✅ Hesabınız oluşturuldu! Giriş yapabilirsiniz.</div>';
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
                            <div id="analizMetni" style="color:#ddd; font-size:0.95rem; line-height:1.7; margin-top:10px;">${markdownToHtml(data.rapor)}</div>
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
function gunlukRaporKapat() {
    document.getElementById('gunlukRaporModal').style.display = 'none';
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
        sonucDiv.innerHTML = '<div class="msg-error">Yapılan işleri yazın.</div>';
        return;
    }

    const veriler = `Tarih: ${tarih || 'Bugün'}, İşçi sayısı: ${isci || 'Belirtilmedi'}, Yapılanlar: ${yapilanlar}, Sorunlar: ${sorunlar || 'Yok'}, Yarın: ${yarin || 'Belirtilmedi'}, İSG durumu: ${isg}`;
    const hava = (document.getElementById('condition')?.innerText || '');

    sonucDiv.innerHTML = '<div class="msg-success">🤖 Rapor oluşturuluyor...</div>';

    try {
        const token = localStorage.getItem('bai_token');
        const res = await fetch('/gunluk-rapor-olustur', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ veriler, hava, dil: aktifDil, token })
        });
        if (res.status === 429) {
            const data = await res.json();
            sonucDiv.innerHTML = `<div style="text-align:center; padding:20px;"><div style="font-size:2rem; margin-bottom:10px;">⚡</div><div style="color:#e67e22; font-size:1.1rem; font-weight:bold; margin-bottom:10px;">Limit Doldu!</div><div style="color:#aaa; margin-bottom:20px;">${data.detail}</div><button onclick="proYukselt()" style="background:#e67e22; color:white; border:none; padding:12px 30px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:1rem;">⚡ Pro'ya Geç — 10$/ay</button></div>`;
            return;
        }
        const data = await res.json();
        if (res.ok) {
            // Also put it in analizMetni so kaydet works
            document.getElementById('result').innerHTML = `
                <div class="res-title">📋 Günlük Rapor</div>
                <div id="analizMetni" style="color:#ddd; font-size:0.95rem; line-height:1.7; margin-top:10px;">${markdownToHtml(data.rapor)}</div>
            `;
            sonucDiv.innerHTML = `
                <div style="background:rgba(255,255,255,0.05); border-radius:10px; padding:15px; margin-top:10px; color:#f0f0f0; font-size:0.9rem; line-height:1.6;">${markdownToHtml(data.rapor)}</div>
                <div style="display:flex; gap:10px; margin-top:10px;">
                    <button onclick="gunlukRaporuKaydet(); gunlukRaporKapat();" style="flex:1; padding:10px; background:#2ecc71; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">💾 Arşive Kaydet</button>
                    <button onclick="gunlukRaporKapat()" style="flex:1; padding:10px; background:#444; color:white; border:none; border-radius:10px; cursor:pointer;">Kapat</button>
                </div>
            `;
        } else {
            sonucDiv.innerHTML = `<div class="msg-error">${data.detail}</div>`;
        }
    } catch(e) {
        sonucDiv.innerHTML = '<div class="msg-error">Bağlantı hatası.</div>';
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
            const badge = document.getElementById('profilePlan');
            if (badge) badge.innerHTML = planBadgeHTML(data.plan);
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
            body: JSON.stringify({ token })
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
    document.getElementById('navSidebar').classList.remove('mobile-open');
    document.getElementById('navOverlay').classList.remove('active');
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
    setActiveNav(page);
    const titleEl = document.getElementById('headerTitle');
    if (titleEl) titleEl.textContent = PAGE_TITLES[page] || '';
    // Close mobile nav if open
    closeMobileNav();
    // Perform action
    if (page === 'kamera') kameraAc('genel');
    else if (page === 'hesaplama') toggleSidebar();
    else if (page === 'arsiv') toggleHistory();
    else if (page === 'gunluk') document.getElementById('gunlukRaporModal').style.display = 'flex';
    else if (page === 'sesli') sesliRaporBaslat();
    else if (page === 'fiyat') fiyatModalAc();
    else if (page === 'stok') stokModalAc();
    else if (page === 'deprem') depremModalAc();
    else if (page === 'santiye') santiyeModalAc();
    // home: do nothing (scroll to top)
    else window.scrollTo({ top: 0, behavior: 'smooth' });
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
function stokModalAc() {
    document.getElementById('stokModal').style.display = 'flex';
    stokYukle();
}
function stokModalKapat() {
    document.getElementById('stokModal').style.display = 'none';
}

async function stokYukle() {
    const token = localStorage.getItem('bai_token');
    try {
        const res = await fetch(`/stok?token=${token}`);
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
        kartDiv.innerHTML = Object.entries(data.stok).map(([m, s]) => {
            const uyariRenk = s.bitis_gun && s.bitis_gun <= 7 ? '#ef4444' : s.bitis_gun && s.bitis_gun <= 14 ? '#f59e0b' : '#2ecc71';
            return `<div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:14px; cursor:pointer;" onclick="document.getElementById('stokGecmisMalzeme').value='${m}'; stokGecmisYukle();">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:1.3rem;">${malzemeIkon[m]}</span>
                    ${s.bitis_gun ? `<span style="color:${uyariRenk}; font-size:0.72rem; font-weight:700;">${s.bitis_gun}g</span>` : '<span style="color:#555; font-size:0.72rem;">—</span>'}
                </div>
                <div style="color:white; font-weight:700; font-size:0.9rem; margin-bottom:4px;">${malzemeAd[m]}</div>
                <div style="color:var(--primary); font-size:1.1rem; font-weight:800;">${s.mevcut}</div>
                <div style="display:flex; justify-content:space-between; margin-top:6px;">
                    <span style="color:#2ecc71; font-size:0.7rem;">↑ ${s.toplam_giris}</span>
                    <span style="color:#ef4444; font-size:0.7rem;">↓ ${s.toplam_cikis}</span>
                </div>
            </div>`;
        }).join('');

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
            liste.innerHTML = '<div style="color:#555; text-align:center; padding:20px; font-size:0.85rem;">Henüz hareket yok.</div>';
            return;
        }
        liste.innerHTML = data.gecmis.map(k => `
            <div style="display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05);">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:1rem;">${k.tip === 'giris' ? '📥' : '📤'}</span>
                    <div>
                        <div style="color:${k.tip === 'giris' ? '#2ecc71' : '#ef4444'}; font-weight:700; font-size:0.85rem;">${k.tip === 'giris' ? '+' : '-'}${k.miktar} ${k.birim}</div>
                        <div style="color:#555; font-size:0.72rem;">${k.tedarikci || ''} ${k.notlar || ''}</div>
                    </div>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="color:#666; font-size:0.72rem;">${k.tarih}</span>
                    <button onclick="stokSil(${k.id})" style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.2); color:#ef4444; border-radius:6px; padding:2px 8px; cursor:pointer; font-size:0.72rem;">Sil</button>
                </div>
            </div>
        `).join('');
    } catch(e) {}
}

async function stokKaydet() {
    const token = localStorage.getItem('bai_token');
    const malzeme = document.getElementById('stokMalzeme').value;
    const tip = document.getElementById('stokTip').value;
    const miktar = document.getElementById('stokMiktar').value;
    const birim = document.getElementById('stokBirim').value;
    const tedarikci = document.getElementById('stokTedarikci').value;
    const fiyat = document.getElementById('stokFiyat').value;
    const notlar = document.getElementById('stokNotlar').value;
    const msg = document.getElementById('stokMsg');
    if (!miktar) { msg.innerHTML = '<span style="color:#e74c3c;">Miktar girin.</span>'; return; }
    try {
        const res = await fetch('/stok-ekle', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, malzeme, tip, miktar, birim, tedarikci, fiyat, notlar})
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

// --- 🏗️ ŞANTİYE DASHBOARD ---
let santiyeHaritaObj = null;
let santiyeVerisi = [];
let santiyeSiralaKolon = 'ad';
let santiyeSiralaYon = 'asc';

function santiyeModalAc() {
    if (aktifRol !== 'muteahhit') return;
    const m = document.getElementById('santiyeModal');
    m.style.display = 'block';
    santiyeYukle();
    setTimeout(() => santiyeHaritaBaslat(), 300);
}
function santiyeModalKapat() {
    document.getElementById('santiyeModal').style.display = 'none';
}
function santiyeEkleModalAc(santiye) {
    const fm = document.getElementById('santiyeFormModal');
    fm.style.display = 'flex';
    document.getElementById('santiyeFormId').value = santiye ? santiye.id : '';
    document.getElementById('santiyeFormBaslik').textContent = santiye ? 'Şantiye Düzenle' : 'Yeni Şantiye Ekle';
    document.getElementById('santiyeFormAd').value = santiye ? santiye.ad : '';
    document.getElementById('santiyeFormKonum').value = santiye ? santiye.konum : '';
    document.getElementById('santiyeFormLat').value = santiye ? (santiye.lat || '') : '';
    document.getElementById('santiyeFormLon').value = santiye ? (santiye.lon || '') : '';
    document.getElementById('santiyeFormIlerleme').value = santiye ? santiye.ilerleme : 0;
    document.getElementById('santiyeFormIsci').value = santiye ? santiye.isci_sayisi : 0;
    document.getElementById('santiyeFormDurum').value = santiye ? santiye.durum : 'iyi';
    document.getElementById('santiyeFormIsg').value = santiye ? (santiye.isg_durumu || '') : '';
    document.getElementById('santiyeFormNotlar').value = santiye ? (santiye.notlar || '') : '';
    document.getElementById('santiyeFormMsg').innerHTML = '';
}
function santiyeFormKapat() {
    document.getElementById('santiyeFormModal').style.display = 'none';
}
function santiyeHaritaBaslat() {
    if (santiyeHaritaObj) { santiyeHaritaObj.invalidateSize(); return; }
    santiyeHaritaObj = L.map('santiyeHarita').setView([39.0, 35.0], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap', maxZoom: 18
    }).addTo(santiyeHaritaObj);
}
async function santiyeYukle() {
    const token = localStorage.getItem('bai_token');
    try {
        const res = await fetch('/santiyeler', { headers: { 'Authorization': 'Bearer ' + token } });
        const data = await res.json();
        santiyeVerisi = data.santiyeler || [];
        santiyeOzetGoster();
        santiyeKartlarGoster();
        santiyeTabloCiz();
        santiyeHaritaGuncelle();
    } catch(e) {
        console.error('Santiye yükleme hatası:', e);
    }
}
function santiyeOzetGoster() {
    const toplam = santiyeVerisi.length;
    const iyi = santiyeVerisi.filter(s => s.durum === 'iyi').length;
    const dikkat = santiyeVerisi.filter(s => s.durum === 'dikkat').length;
    const sorun = santiyeVerisi.filter(s => s.durum === 'sorun').length;
    const toplamIsci = santiyeVerisi.reduce((a, s) => a + (s.isci_sayisi || 0), 0);
    const ortIlerleme = toplam ? Math.round(santiyeVerisi.reduce((a, s) => a + (s.ilerleme || 0), 0) / toplam) : 0;
    document.getElementById('santiyeOzet').innerHTML = `
        <div style="background:rgba(255,255,255,0.05); border-radius:14px; padding:16px; text-align:center; border:1px solid rgba(255,255,255,0.08);">
            <div style="font-size:2rem; font-weight:800; color:#e67e22;">${toplam}</div>
            <div style="color:#aaa; font-size:0.8rem; margin-top:4px;">Toplam Şantiye</div>
        </div>
        <div style="background:rgba(46,204,113,0.1); border-radius:14px; padding:16px; text-align:center; border:1px solid rgba(46,204,113,0.2);">
            <div style="font-size:2rem; font-weight:800; color:#2ecc71;">${iyi}</div>
            <div style="color:#aaa; font-size:0.8rem; margin-top:4px;">✅ İyi Durumda</div>
        </div>
        <div style="background:rgba(243,156,18,0.1); border-radius:14px; padding:16px; text-align:center; border:1px solid rgba(243,156,18,0.2);">
            <div style="font-size:2rem; font-weight:800; color:#f39c12;">${dikkat}</div>
            <div style="color:#aaa; font-size:0.8rem; margin-top:4px;">⚠️ Dikkat Gereken</div>
        </div>
        <div style="background:rgba(231,76,60,0.1); border-radius:14px; padding:16px; text-align:center; border:1px solid rgba(231,76,60,0.2);">
            <div style="font-size:2rem; font-weight:800; color:#e74c3c;">${sorun}</div>
            <div style="color:#aaa; font-size:0.8rem; margin-top:4px;">❌ Sorunlu</div>
        </div>`;
}
function santiyeKartlarGoster() {
    const durumRenk = { iyi: '#2ecc71', dikkat: '#f39c12', sorun: '#e74c3c' };
    const durumIcon = { iyi: '✅', dikkat: '⚠️', sorun: '❌' };
    document.getElementById('santiyeKartlar').innerHTML = santiyeVerisi.length === 0
        ? '<div style="color:#666; grid-column:1/-1; text-align:center; padding:40px;">Henüz şantiye eklenmemiş.</div>'
        : santiyeVerisi.map(s => `
        <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:16px; padding:18px; position:relative; border-top:3px solid ${durumRenk[s.durum] || '#555'};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px;">
                <div>
                    <div style="font-weight:700; font-size:1rem; color:white;">${s.ad}</div>
                    <div style="color:#aaa; font-size:0.8rem; margin-top:2px;">📍 ${s.konum}</div>
                </div>
                <span style="color:${durumRenk[s.durum] || '#aaa'}; font-size:1.3rem;">${durumIcon[s.durum] || '—'}</span>
            </div>
            <div style="background:rgba(255,255,255,0.06); border-radius:6px; height:6px; margin-bottom:8px; overflow:hidden;">
                <div style="background:linear-gradient(90deg,#e67e22,#f39c12); height:100%; width:${s.ilerleme || 0}%; border-radius:6px;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; color:#aaa; font-size:0.78rem; margin-bottom:12px;">
                <span>İlerleme: <b style="color:white;">${s.ilerleme || 0}%</b></span>
                <span>👷 <b style="color:white;">${s.isci_sayisi || 0}</b> kişi</span>
            </div>
            ${s.isg_durumu ? `<div style="color:#aaa; font-size:0.78rem; margin-bottom:10px;">🦺 ${s.isg_durumu}</div>` : ''}
            <div style="display:flex; gap:8px;">
                <button onclick="santiyeEkleModalAc(${JSON.stringify(s).replace(/"/g,'&quot;')})" style="flex:1; background:rgba(230,126,34,0.15); border:1px solid rgba(230,126,34,0.3); color:#e67e22; padding:7px; border-radius:8px; cursor:pointer; font-size:0.8rem;">✏️ Düzenle</button>
                <button onclick="santiyeSilOnay(${s.id},'${s.ad.replace(/'/g,"\\'")}')" style="flex:1; background:rgba(231,76,60,0.1); border:1px solid rgba(231,76,60,0.2); color:#e74c3c; padding:7px; border-radius:8px; cursor:pointer; font-size:0.8rem;">🗑️ Sil</button>
            </div>
        </div>`).join('');
}
function santiyeTabloCiz() {
    const sorted = [...santiyeVerisi].sort((a, b) => {
        const va = a[santiyeSiralaKolon] ?? '';
        const vb = b[santiyeSiralaKolon] ?? '';
        return santiyeSiralaYon === 'asc' ? (va > vb ? 1 : -1) : (va < vb ? 1 : -1);
    });
    const cols = [
        { key: 'ad', label: 'Ad' },
        { key: 'konum', label: 'Konum' },
        { key: 'ilerleme', label: 'İlerleme' },
        { key: 'isci_sayisi', label: 'İşçi' },
        { key: 'durum', label: 'Durum' }
    ];
    const thStyle = 'padding:8px 10px; text-align:left; color:#aaa; font-size:0.78rem; border-bottom:1px solid rgba(255,255,255,0.07); cursor:pointer; white-space:nowrap; user-select:none;';
    const tdStyle = 'padding:8px 10px; font-size:0.82rem; color:#ddd; border-bottom:1px solid rgba(255,255,255,0.04);';
    const durumRenk = { iyi: '#2ecc71', dikkat: '#f39c12', sorun: '#e74c3c' };
    document.getElementById('santiyeTablo').innerHTML = `
        <table style="width:100%; border-collapse:collapse;">
            <thead><tr>${cols.map(c => `<th style="${thStyle}" onclick="santiyeSirala('${c.key}')">${c.label}${santiyeSiralaKolon===c.key ? (santiyeSiralaYon==='asc'?' ↑':' ↓') : ''}</th>`).join('')}</tr></thead>
            <tbody>${sorted.map(s => `
                <tr>
                    <td style="${tdStyle}">${s.ad}</td>
                    <td style="${tdStyle}">${s.konum}</td>
                    <td style="${tdStyle}">${s.ilerleme || 0}%</td>
                    <td style="${tdStyle}">${s.isci_sayisi || 0}</td>
                    <td style="${tdStyle}; color:${durumRenk[s.durum] || '#aaa'};">${s.durum}</td>
                </tr>`).join('')}
            </tbody>
        </table>`;
}
function santiyeSirala(kolon) {
    if (santiyeSiralaKolon === kolon) santiyeSiralaYon = santiyeSiralaYon === 'asc' ? 'desc' : 'asc';
    else { santiyeSiralaKolon = kolon; santiyeSiralaYon = 'asc'; }
    santiyeTabloCiz();
}
function santiyeHaritaGuncelle() {
    if (!santiyeHaritaObj) return;
    santiyeHaritaObj.eachLayer(l => { if (l instanceof L.Marker) santiyeHaritaObj.removeLayer(l); });
    const durumRenk = { iyi: '#2ecc71', dikkat: '#f39c12', sorun: '#e74c3c' };
    santiyeVerisi.filter(s => s.lat && s.lon).forEach(s => {
        L.marker([s.lat, s.lon], {
            icon: L.divIcon({
                html: `<div style="background:${durumRenk[s.durum]||'#e67e22'}; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:0.65rem; font-weight:800; border:2px solid white; box-shadow:0 0 8px rgba(0,0,0,0.4);">🏗️</div>`,
                iconSize: [28, 28], iconAnchor: [14, 14]
            })
        }).addTo(santiyeHaritaObj).bindPopup(`<b>${s.ad}</b><br>📍 ${s.konum}<br>İlerleme: ${s.ilerleme||0}%<br>👷 ${s.isci_sayisi||0} kişi`);
    });
}
async function santiyeKaydet() {
    const token = localStorage.getItem('bai_token');
    const id = document.getElementById('santiyeFormId').value;
    const msg = document.getElementById('santiyeFormMsg');
    const body = {
        ad: document.getElementById('santiyeFormAd').value.trim(),
        konum: document.getElementById('santiyeFormKonum').value.trim(),
        lat: parseFloat(document.getElementById('santiyeFormLat').value) || null,
        lon: parseFloat(document.getElementById('santiyeFormLon').value) || null,
        ilerleme: parseInt(document.getElementById('santiyeFormIlerleme').value) || 0,
        isci_sayisi: parseInt(document.getElementById('santiyeFormIsci').value) || 0,
        durum: document.getElementById('santiyeFormDurum').value,
        isg_durumu: document.getElementById('santiyeFormIsg').value.trim(),
        notlar: document.getElementById('santiyeFormNotlar').value.trim()
    };
    if (!body.ad || !body.konum) { msg.innerHTML = '<div class="msg-error">Şantiye adı ve konum zorunludur.</div>'; return; }
    try {
        const url = id ? `/santiye-guncelle/${id}` : '/santiye-ekle';
        const res = await fetch(url, { method: 'POST', headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        const data = await res.json();
        if (res.ok) {
            msg.innerHTML = '<div class="msg-success">✅ Kaydedildi!</div>';
            setTimeout(() => { santiyeFormKapat(); santiyeYukle(); }, 800);
        } else {
            const detail = data.detail || 'Hata oluştu.';
            if (detail.startsWith('PLAN_YETERSIZ:')) {
                const parts = detail.split(':');
                santiyeFormKapat();
                planKilit(parts[1] || 'santiye');
            } else {
                msg.innerHTML = `<div class="msg-error">❌ ${detail}</div>`;
            }
        }
    } catch(e) {
        msg.innerHTML = `<div class="msg-error">❌ Bağlantı hatası.</div>`;
    }
}
async function santiyeSilOnay(id, ad) {
    if (!confirm(`"${ad}" şantiyesini silmek istediğinizden emin misiniz?`)) return;
    const token = localStorage.getItem('bai_token');
    try {
        const res = await fetch(`/santiye-sil/${id}`, { method: 'DELETE', headers: { 'Authorization': 'Bearer ' + token } });
        if (res.ok) santiyeYukle();
        else alert('Silme işlemi başarısız.');
    } catch(e) { alert('Bağlantı hatası.'); }
}

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
            localStorage.removeItem('bai_token');
        }
    }
    havaGuncelle();
});
</script>
"""
