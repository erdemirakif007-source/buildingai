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
            dilDegistir(aktifDil);
            havaGuncelle();
            kullanımDurumuGoster();
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

async function kameraAnalizGonder(base64) {
    const token = localStorage.getItem('bai_token');
    const analiz_tipi = document.getElementById('kameraAnalizTipi').value;
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'Sivas';
    const hava = (document.getElementById('temp') ? document.getElementById('temp').innerText : '') + ' ' +
                 (document.getElementById('condition') ? document.getElementById('condition').innerText : '');
    const resBox = document.getElementById('result');
    kameraKapat();
    resBox.innerHTML = `<i>📸 ${aktifDil === 'tr' ? 'Fotoğraf analiz ediliyor...' : 'Analyzing photo...'}</i>`;
    try {
        const res = await fetch('/kamera-analiz', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token, resim_base64: base64, analiz_tipi, hava, sehir, dil: aktifDil })
        });
        if (res.status === 429) {
            const err = await res.json();
            resBox.innerHTML = `<div style="color:#e74c3c; padding:20px; text-align:center;"><div style="font-size:2rem;">🔒</div><strong>${aktifDil === 'tr' ? 'Günlük limit doldu!' : 'Daily limit reached!'}</strong><div style="color:#aaa; margin-top:8px; font-size:0.9rem;">${err.detail}</div></div>`;
            return;
        }
        const data = await res.json();
        const cevapMetni = data.cevap || data.detail || JSON.stringify(data);
        const t = TRANSLATIONS[aktifDil];
        resBox.innerHTML = `
            <div class="res-title">📸 ${aktifDil === 'tr' ? 'KAMERA ANALİZİ' : 'CAMERA ANALYSIS'}</div>
            <div id="analizMetni" style="color:#ddd; font-size:0.95rem; line-height:1.7; margin-top:10px;">${markdownToHtml(cevapMetni)}</div>
            <button onclick="pdfIndir()" style="margin-top:15px; background:#8b5cf6; color:white; border:none; padding:12px 20px; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">📄 ${aktifDil === 'tr' ? 'PDF Rapor İndir' : 'Download PDF Report'}</button>
            <button onclick="gunlukRaporuKaydet()" style="margin-top:10px; background:#27ae60; color:white; border:none; padding:12px 20px; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">${t.saveBtn}</button>
        `;
    } catch(e) {
        resBox.innerHTML = `<div style="color:#e74c3c;">Analiz hatası: ${e.message}</div>`;
    }
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
        btn.textContent = '🎤 Sesli Rapor';
        btn.style.background = 'linear-gradient(135deg,#8e44ad,#6c3483)';
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
        btn.textContent = '⏹️ Kaydı Durdur';
        btn.style.background = 'linear-gradient(135deg,#e74c3c,#c0392b)';
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

// --- 📊 KULLANIM DURUMU & PRO ---
async function kullanımDurumuGoster() {
    const token = localStorage.getItem('bai_token');
    if (!token) return;
    try {
        const res = await fetch(`/kullanim-durumu?token=${token}`);
        const data = await res.json();
        if (res.ok) {
            const k = data.kullanim;
            const sorEl = document.getElementById('statSorgu');
            if (sorEl) sorEl.textContent = data.plan === 'pro' ? '∞' : `${k.sor.kullanilan}/10`;
            const badge = document.getElementById('profilePlan');
            if (badge) {
                badge.textContent = data.plan === 'pro' ? '⚡ PRO PLAN' : 'ÜCRETSİZ PLAN';
                badge.style.background = data.plan === 'pro' ? 'rgba(46,204,113,0.2)' : 'rgba(230,126,34,0.2)';
                badge.style.borderColor = data.plan === 'pro' ? '#2ecc71' : 'var(--primary)';
                badge.style.color = data.plan === 'pro' ? '#2ecc71' : 'var(--primary)';
            }
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
                dilDegistir(aktifDil);
                havaGuncelle();
                kullanımDurumuGoster();
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
