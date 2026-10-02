

// ── Token Auth Interceptor ──────────────────────────────────────────────────
// Tüm fetch çağrılarına otomatik Authorization header ekler;
// URL'deki token= / &token= parametrelerini temizler.
(function () {
  const _orig = window.fetch.bind(window);
  window.fetch = function (url, opts) {
    if (typeof url === 'string') {
      url = url
        .replace(/([?&])token=[^&#]*&?/g, (match, sep) => sep === '?' ? '?' : '')
        .replace(/\?&/g, '?')
        .replace(/[?&](#|$)/, '$1');
    }
    const tok = localStorage.getItem('bai_token');
    if (tok) {
      opts = opts ? Object.assign({}, opts) : {};
      opts.headers = Object.assign({ 'Authorization': 'Bearer ' + tok }, opts.headers || {});
    }
    return _orig(url, opts);
  };
}());
// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

// --- 🏠 DİL SİSTEMİ ---
const TRANSLATIONS = {
    tr: {
        loginTitle: " BuildingAI",
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
        backLink: "? Giriş sayfasına dön",
        planLabel: "Plan seçin:",
        inputPlaceholder: "Soru sor, hesap seç veya fotoğraf yükle...",
        systemReady: "Sistem Hazır",
        systemReadyDesc: "Veriler yüklendi. Hesaplama bekleniyor...",
        aiAnaliz: "🧠  AI ANALİZİ",
        translateBtn: "🇬Ÿ‡§ Translate to English Technical Report",
        saveBtn: "💾 Günlük Rapor Olarak Kaydet",
        readBtn: "🔊 OKU",
        stopBtn: "🛑 DURDUR",
        thinking: "Şefim, yapay zeka analiz ediyor...",
        aiLang: "tr",
    },
    en: {
        loginTitle: " BuildingAI",
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
        backLink: "? Back to login",
        planLabel: "Choose a plan:",
        inputPlaceholder: "Ask a question, select a calculation or upload a photo...",
        systemReady: "System Ready",
        systemReadyDesc: "Data loaded. Awaiting calculation...",
        aiAnaliz: "🧠  AI ANALYSIS",
        translateBtn: "🇬Ÿ‡· Türkçe Rapora Çevir",
        saveBtn: "💾 Save as Daily Report",
        readBtn: "🔊 READ",
        stopBtn: "🛑 STOP",
        thinking: "Analyzing with AI...",
        aiLang: "en",
    }
};

let aktifDil = 'tr';

let aktifRol = localStorage.getItem('bai_rol') || null;
function isEngineerRole(rol) { return rol === 'muhendis'; }
function isContractorRole(rol) { return rol === 'muteahhit' || rol === 'mutahhit' || rol === 'proje_muduru'; }
function getRoleLabel(rol) {
    if (rol === 'muhendis') return 'Mühendis';
    if (rol === 'mutahhit' || rol === 'muteahhit') return 'Müteahhit';
    if (rol === 'proje_muduru') return 'Proje Müdürü';
    return 'Şantiye Şefi';
}
function getWorkspaceRoleLabel(rol) {
    if (rol === 'mutahhit' || rol === 'muteahhit' || rol === 'proje_muduru') return 'Müteahhit';
    return 'Şantiye Şefi';
}
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
        setTimeout(() => {
            el.style.display = 'none';
            navSidebarGuncelle(rol);
            routeInitialPath();
            syncProfileToServer({ role: rol }, { silent: true });
        }, 400);
    }, 600);
}

function applyServerUserProfile(data) {
    if (!data) return;
    const current = JSON.parse(localStorage.getItem('bai_user') || '{}');
    const nextUser = {
        ...current,
        ...data,
        is_admin: Boolean(data.is_admin ?? current.is_admin),
        rol: data.role || data.rol || current.rol || current.role || localStorage.getItem('bai_rol') || '',
    };
    if (nextUser.role && !nextUser.rol) nextUser.rol = nextUser.role;
    if (nextUser.rol && !nextUser.role) nextUser.role = nextUser.rol;
    localStorage.setItem('bai_user', JSON.stringify(nextUser));
    if (nextUser.role) localStorage.setItem('bai_rol', nextUser.role);
    if (typeof aktifKullanici !== 'undefined' && aktifKullanici) {
        Object.assign(aktifKullanici, nextUser);
    }
    const roleLabel = getWorkspaceRoleLabel(nextUser.role || nextUser.rol);
    const headerRole = document.getElementById('headerUserRole');
    const amRole = document.getElementById('amRole');
    if (headerRole) headerRole.textContent = roleLabel;
    if (amRole) amRole.textContent = roleLabel;
    // Badge isim + avatar güncelle
    const displayName = nextUser.full_name || nextUser.email || '';
    const shortName = displayName.includes('@') ? displayName.split('@')[0] : displayName;
    const headerName = document.getElementById('headerUserName');
    const headerAvatar = document.getElementById('headerAvatar');
    if (headerName && shortName) {
        headerName.textContent = shortName.charAt(0).toUpperCase() + shortName.slice(1);
    }
    if (headerAvatar && shortName) {
        const parts = shortName.trim().split(/\s+/);
        headerAvatar.textContent = parts.length >= 2
            ? (parts[0][0] + parts[parts.length-1][0]).toUpperCase()
            : shortName.slice(0,2).toUpperCase();
    }
    if (nextUser.avatar_url) {
        avatarGuncelle(nextUser.avatar_url, nextUser.avatar_position, nextUser.avatar_scale);
    }
    updateSidebarOrganizationName(nextUser);
    _applyOwnerUI();
    setTimeout(globalSantiyeSeciciDoldur, 500);
}

async function globalSantiyeSeciciDoldur() {
    const select = document.getElementById('globalSantiyeSecici');
    if (!select) return;
    try {
        const token = localStorage.getItem('bai_token');
        const r = await fetch('/santiyeler', {headers: {'Authorization': 'Bearer ' + token}});
        const d = await r.json();
        if (!r.ok) throw new Error(d.detail || 'Projeler alınamadı');
        const santiyeler = d.santiyeler || [];
        const mevcut = localStorage.getItem('bai_aktif_santiye') || '';
        select.querySelectorAll('option:not(:first-child)').forEach(o => o.remove());
        santiyeler.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s.id;
            opt.textContent = ' ' + (s.ad || s.isim || s.name || 'Şantiye');
            if (s.sehir) opt.setAttribute('data-sehir', s.sehir);
            if (s.konum) opt.setAttribute('data-konum', s.konum);
            if (s.lat) opt.setAttribute('data-lat', s.lat);
            if (s.lon) opt.setAttribute('data-lon', s.lon);
            select.appendChild(opt);
        });
        const selected = santiyeler.find(s => Number(s.id) === Number(mevcut)) || santiyeler[0];
        select.value = selected ? String(selected.id) : '';
        globalSantiyeDegisti();
    } catch(e) { console.log('Şantiye listesi yüklenemedi:', e); }
}

function globalSantiyeDegisti() {
    const select = document.getElementById('globalSantiyeSecici');
    const santiyeId = select.value || '';
    const santiyeAd = select.options[select.selectedIndex].textContent.trim() || '';
    const sehir = select.options[select.selectedIndex].getAttribute('data-sehir') || '';
    const lat = select.options[select.selectedIndex].getAttribute('data-lat') || '';
    const lon = select.options[select.selectedIndex].getAttribute('data-lon') || '';

    // localStorage'a kaydet
    if (santiyeId) {
        localStorage.setItem('bai_aktif_santiye', santiyeId);
        localStorage.setItem('bai_aktif_santiye_ad', santiyeAd);
        localStorage.setItem('bai_aktif_santiye_sehir', sehir);
        window._aktifSantiyeSehir = sehir;
        window._kpAktifSantiye = { id: Number(santiyeId), ad: santiyeAd, sehir: sehir, lat: lat, lon: lon };
        localStorage.setItem('varsayilan_santiye', JSON.stringify(window._kpAktifSantiye));
        if (lat) localStorage.setItem('bai_aktif_santiye_lat', lat);
        if (lon) localStorage.setItem('bai_aktif_santiye_lon', lon);
    } else {
        localStorage.removeItem('bai_aktif_santiye');
        localStorage.removeItem('bai_aktif_santiye_ad');
        localStorage.removeItem('bai_aktif_santiye_sehir');
        localStorage.removeItem('varsayilan_santiye');
        window._aktifSantiyeSehir = '';
        window._kpAktifSantiye = null;
    }

    // Global değişkenlere kaydet
    window._aktifSantiyeId = santiyeId;
    window._baiProjectEpoch = (window._baiProjectEpoch || 0) + 1;
    window._aktifSantiyeSehir = sehir;
    window._aktifSantiyeLat = lat;
    window._aktifSantiyeLon = lon;

    // Hava durumu güncelle
    if (typeof fiyatHavaDurumuGuncelle === 'function') {
        fiyatHavaDurumuGuncelle(sehir, lat, lon);
    }

    // --- Sayfa bazlı yenileme ---

    // 1. Stok sayfası: kendi dropdown'ını senkronize et ve yenile
    const stokSantiye = document.getElementById('stokSantiye');
    const stokPage = document.getElementById('stokPage') || document.getElementById('stokContent');
    if (stokSantiye) stokSantiye.value = santiyeId;
    const _aktifSayfaId = document.querySelector('.sayfa.aktif')?.id;
    const _stokSayfaAktif = (stokPage && stokPage.style.display !== 'none') || _aktifSayfaId === 'stokSayfa' || _aktifSayfaId === 'stokPage';
    if (typeof stokYukle === 'function') stokYukle(santiyeId);

    const hakedisSantiye = document.getElementById('hakedisSantiyeSelect');
    const hakedisPage = document.getElementById('hakedisPage');
    if (hakedisSantiye) hakedisSantiye.value = santiyeId;
    if (hakedisPage && hakedisPage.style.display !== 'none') {
        if (typeof hakedisListeYukle === 'function') hakedisListeYukle();
    }

    const hiyerarsiPage = document.getElementById('hiyerarsiPage');
    if (hiyerarsiPage && hiyerarsiPage.style.display !== 'none') {
        if (typeof hiyerarsiPageAc === 'function') hiyerarsiPageAc();
        else if (typeof metrajOzetYukle === 'function') metrajOzetYukle(santiyeId);
    }

    // 2. ISG/Güvenlik sayfası: kendi dropdown'ını senkronize et
    const guvenlikSantiye = document.getElementById('guvenlikSantiye');
    if (guvenlikSantiye) guvenlikSantiye.value = santiyeId;
    const guvenlikPage = document.getElementById('guvenlikPage') || document.getElementById('isgPage');
    if (guvenlikPage && guvenlikPage.style.display !== 'none') {
        if (typeof guvenlikSantiyeDegisti === 'function') guvenlikSantiyeDegisti();
    }

    // 3. Fiyat sayfası - satın alma tabı
    const saTab = document.getElementById('satinAlmaTab');
    if (saTab && saTab.style.display !== 'none') {
        const saFiltre = document.getElementById('saFiltreSantiye');
        if (saFiltre) saFiltre.value = santiyeId;
        if (typeof saFiltreUygula === 'function') saFiltreUygula();
    }

    // 4. Kamera sayfası yenile (eğer açıksa)
    const kameraPage = document.getElementById('kameraPage') || document.getElementById('cameraPage');
    if (kameraPage && kameraPage.style.display !== 'none') {
        if (typeof kameraYukle === 'function') kameraYukle();
        else if (typeof loadCameraPage === 'function') loadCameraPage();
    }

    // 5. Fiyat sayfası: bölgesel grafikler santiyeye göre yenile
    const _fpPage = document.getElementById('fiyatPage');
    if (_fpPage && _fpPage.style.display !== 'none') {
        if (typeof fiyatPageYukle === 'function') fiyatPageYukle();
    }
}

async function avatarYukle(input) {
    const file = input.files[0];
    if (!file) return;

    const status = document.getElementById('avatarUploadStatus');
    if (file.size > 2 * 1024 * 1024) {
        if (status) status.textContent = 'Dosya 2MB\'dan küçük olmalı';
        if (status) status.style.color = '#EF4444';
        input.value = '';
        return;
    }

    if (status) { status.textContent = 'Yükleniyor...'; status.style.color = '#94A3B8'; }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const token = localStorage.getItem('bai_token');
        formData.append('token', token || '');
        const resp = await fetch('/profil-foto', {
            method: 'POST',
            body: formData
        });
        const data = await resp.json();
        if (data.status === 'success' && data.avatar_url) {
            const u = JSON.parse(localStorage.getItem('bai_user') || '{}');
            u.avatar_url = data.avatar_url;
            u.avatar_position = u.avatar_position || '50% 50%';
            u.avatar_scale = u.avatar_scale || '1';
            localStorage.setItem('bai_user', JSON.stringify(u));

            avatarGuncelle(data.avatar_url, u.avatar_position, u.avatar_scale);

            if (status) { status.textContent = 'Yüklendi!'; status.style.color = '#10B981'; }
            avatarPozisyonEditorGoster(data.avatar_url);
        } else {
            if (status) { status.textContent = data.detail || 'Hata oluştu'; status.style.color = '#EF4444'; }
        }
    } catch(e) {
        if (status) { status.textContent = 'Bağlantı hatası'; status.style.color = '#EF4444'; }
    }
    input.value = '';
}

function avatarGuncelle(url, position, scale) {
    position = position || '50% 50%';
    scale = parseFloat(scale) || 1;

    const profilAvatar = document.getElementById('profilAvatarImg');
    const profilInitials = document.getElementById('profilAvatarInitials');
    if (url) {
        if (profilAvatar) {
            profilAvatar.src = url;
            profilAvatar.style.display = 'block';
            profilAvatar.style.objectPosition = position;
            profilAvatar.style.transform = 'scale(' + scale + ')';
            profilAvatar.style.transformOrigin = position;
        }
        if (profilInitials) profilInitials.style.display = 'none';
    }

    const headerAvatar = document.getElementById('headerAvatar');
    if (headerAvatar && url) {
        headerAvatar.innerHTML = '<img src="' + url + '" style="width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:' + position + ';transform:scale(' + scale + ');transform-origin:' + position + ';">';
    }
}

function avatarPozisyonEditorGoster(url) {
    const eski = document.getElementById('avatarPozisyonEditor');
    if (eski) eski.remove();

    const u = JSON.parse(localStorage.getItem('bai_user') || '{}');
    const mevcutPos = u.avatar_position || '50% 50%';
    const parts = mevcutPos.split(' ');
    const xVal = parseInt(parts[0]) || 50;
    const yVal = parseInt(parts[1]) || 50;
    const scaleVal = parseFloat(u.avatar_scale) || 1;

    const container = document.createElement('div');
    container.id = 'avatarPozisyonEditor';
    container.style.cssText = 'margin-top:15px;padding:15px;background:#FFFFFF;box-shadow:0 4px 12px rgba(0,0,0,0.1);border-radius:12px;border:1px solid #E2E8F0;max-width:320px;';

    container.innerHTML = `
        <div style="font-size:13px;color:#334155;margin-bottom:10px;font-weight:500;">Fotograf Ayarla</div>
        <div style="width:80px;height:80px;border-radius:50%;overflow:hidden;margin:0 auto 12px;border:2px solid #6366F1;">
            <img id="pozisyonOnizleme" src="${url}" style="width:100%;height:100%;object-fit:cover;object-position:${xVal}% ${yVal}%;transform:scale(${scaleVal});transform-origin:${xVal}% ${yVal}%;">
        </div>
        <div style="margin-bottom:8px;">
            <label style="font-size:11px;color:#64748B;">Yatay: <span id="xPosLabel">${xVal}%</span></label>
            <input type="range" id="avatarPosX" min="0" max="100" value="${xVal}" style="width:100%;accent-color:#6366F1;" oninput="avatarPozisyonOncele()">
        </div>
        <div style="margin-bottom:8px;">
            <label style="font-size:11px;color:#64748B;">Dikey: <span id="yPosLabel">${yVal}%</span></label>
            <input type="range" id="avatarPosY" min="0" max="100" value="${yVal}" style="width:100%;accent-color:#6366F1;" oninput="avatarPozisyonOncele()">
        </div>
        <div style="margin-bottom:12px;">
            <label style="font-size:11px;color:#64748B;">Boyut: <span id="scalePosLabel">${scaleVal.toFixed(1)}x</span></label>
            <input type="range" id="avatarPosScale" min="1" max="2.5" step="0.05" value="${scaleVal}" style="width:100%;accent-color:#6366F1;" oninput="avatarPozisyonOncele()">
        </div>
        <button onclick="avatarPozisyonKaydet()" style="background:#6366F1;color:#fff;border:none;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;width:100%;">Kaydet</button>
    `;

    const uploadBtn = document.getElementById('avatarFileInput');
    if (uploadBtn && uploadBtn.parentElement) {
        uploadBtn.parentElement.after(container);
    }
}

function avatarPozisyonOncele() {
    const x = document.getElementById('avatarPosX').value;
    const y = document.getElementById('avatarPosY').value;
    const s = parseFloat(document.getElementById('avatarPosScale').value);
    document.getElementById('xPosLabel').textContent = x + '%';
    document.getElementById('yPosLabel').textContent = y + '%';
    document.getElementById('scalePosLabel').textContent = s.toFixed(1) + 'x';
    const preview = document.getElementById('pozisyonOnizleme');
    if (preview) {
        preview.style.objectPosition = x + '% ' + y + '%';
        preview.style.transform = 'scale(' + s + ')';
        preview.style.transformOrigin = x + '% ' + y + '%';
    }
}

async function avatarPozisyonKaydet() {
    const x = document.getElementById('avatarPosX').value;
    const y = document.getElementById('avatarPosY').value;
    const s = document.getElementById('avatarPosScale').value;
    const pos = x + '% ' + y + '%';

    try {
        const token = localStorage.getItem('bai_token');
        const resp = await fetch('/profil-foto-pozisyon', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
            body: JSON.stringify({ position: pos, scale: s })
        });
        const data = await resp.json();
        if (data.status === 'success') {
            const u = JSON.parse(localStorage.getItem('bai_user') || '{}');
            u.avatar_position = pos;
            u.avatar_scale = s;
            localStorage.setItem('bai_user', JSON.stringify(u));
            avatarGuncelle(u.avatar_url, pos, s);

            const editor = document.getElementById('avatarPozisyonEditor');
            if (editor) editor.remove();

            const status = document.getElementById('avatarUploadStatus');
            if (status) { status.textContent = 'Pozisyon kaydedildi!'; status.style.color = '#10B981'; }
        }
    } catch(e) {
        console.error('Pozisyon kaydetme hatası:', e);
    }
}

function _applyOwnerUI() {
  const u = JSON.parse(localStorage.getItem('bai_user') || '{}');
  const isOwner = u.is_owner === true || u.is_admin === true;
  const ownerOnlyIds = [
    'btnYeniSantiyeHeader', 'btnMuhendisDavetEt', 'btnYeniSantiyeModal', 'spHeaderBtn',
    'btnYeniKameraEkle', 'santiyeSilBtn', 'btnAcilPersonelEkle',
  ];
  ownerOnlyIds.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = isOwner ? '' : 'none';
  });
}

function updateSidebarOrganizationName(userData = null) {
    const el = document.getElementById('sidebarOrgName');
    if (!el) return;
    const user = userData || JSON.parse(localStorage.getItem('bai_user') || '{}');
    const orgName = (user.organization_name || '').trim();
    el.textContent = orgName;
    el.style.display = orgName ? 'block' : 'none';
}

async function syncProfileToServer(partial = {}, options = {}) {
  const { silent = false } = options;
  const token = localStorage.getItem('bai_token') || '';
  if (!token) return null;

  const user = JSON.parse(localStorage.getItem('bai_user') || '{}');
  const payload = { token };
  const isAdmin = Boolean(user.is_admin);
  const hasExplicitRole = Object.prototype.hasOwnProperty.call(partial, 'role') || Object.prototype.hasOwnProperty.call(partial, 'rol');
  const currentName = partial.full_name ?? user.full_name ?? (aktifKullanici.full_name || '');
  const currentPhone = partial.telefon ?? user.telefon ?? (aktifKullanici.telefon || '');
  const currentRole = hasExplicitRole ? (partial.role ?? partial.rol) : '';

  if (currentName) payload.full_name = currentName;
  if (currentPhone || Object.prototype.hasOwnProperty.call(partial, 'telefon')) payload.telefon = currentPhone || '';
  if (Object.prototype.hasOwnProperty.call(partial, 'sirket_adi')) payload.sirket_adi = partial.sirket_adi || '';
  if (isAdmin && currentRole) payload.role = currentRole;

  try {
        const res = await fetch('/profil', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Profil kaydedilemedi.');
        applyServerUserProfile(data);
        return data;
    } catch (err) {
        if (!silent) showToast(err.message || 'Profil sunucuya kaydedilemedi.', 'warning');
        return null;
    }
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
    const plan = window._kullaniciPlan || 'baslangic';
    const oz   = window._planOzellikler || {};
    const stokKilit   = !oz.stok;
    const depremKilit = !oz.deprem_analiz;
    const fiyatKilit  = !oz.fiyat_takip;
    const santiyeKilit = (oz.santiye_max === 0);

    const stokOnclick   = stokKilit ? `planKilit('stok')`          : `navGit('stok')`;
    const depremOnclick = depremKilit ? `planKilit('deprem_analiz')` : `navGit('deprem')`;
    const fiyatOnclick  = fiyatKilit ? `planKilit('fiyat_takip')`  : `navGit('fiyat')`;
    const stokLock      = stokKilit ? ' style="opacity:0.5"' : '';
    const depremLock    = depremKilit ? ' style="opacity:0.5"' : '';
    const fiyatLock     = fiyatKilit ? ' style="opacity:0.5"' : '';

    if (rol === 'muhendis') {
        nav.innerHTML = `
            <div class="nav-item active" id="nav-home" onclick="navGit('home')"><span class="nav-icon">🏠</span><span class="nav-label">Ana Sayfa</span></div>
            <div class="nav-item" id="nav-kamera" onclick="navGit('kamera')"><span class="nav-icon">📷</span><span class="nav-label">Kamera Analizi</span></div>
            <div class="nav-item" id="nav-saha-kayitlari" onclick="navGit('saha-kayitlari')"><span class="nav-icon">📋</span><span class="nav-label">Saha Kayıtları</span></div>
            <div class="nav-item" id="nav-hesaplama" onclick="navGit('hesaplama')"><span class="nav-icon">🧮</span><span class="nav-label">Mühendislik Paneli</span></div>
            <div class="nav-item" id="nav-gunluk" onclick="navGit('gunluk')"><span class="nav-icon">📝</span><span class="nav-label">Günlük Rapor</span></div>
            <div class="nav-item" id="nav-sesli" onclick="navGit('sesli')"><span class="nav-icon">🎤</span><span class="nav-label">Sesli Rapor</span></div>
            <div class="nav-item" id="nav-arsiv" onclick="navGit('arsiv')"><span class="nav-icon">📁</span><span class="nav-label">Arşiv</span></div>
            <div class="nav-item" id="nav-fiyat" onclick="${fiyatOnclick}"${fiyatLock}><span class="nav-icon">🏠</span><span class="nav-label">Fiyat Takibi${fiyatKilit ? ' 🔒':''}</span></div>
            <div class="nav-item" id="nav-stok" onclick="${stokOnclick}"${stokLock}><span class="nav-icon">🏠</span><span class="nav-label">Stok Takibi${stokKilit ? ' 🔒':''}</span></div>
            <div class="nav-item" id="nav-deprem" onclick="${depremOnclick}"${depremLock}><span class="nav-icon">🏠</span><span class="nav-label">Deprem Analizi${depremKilit ? ' 🔒':''}</span></div>
            <div class="nav-item" id="nav-pdf" onclick="pdfIndir()"><span class="nav-icon">📄</span><span class="nav-label">PDF İndir</span></div>
            <div class="nav-item" id="nav-haftalik" onclick="haftalikRaporIndir()"><span class="nav-icon">📊</span><span class="nav-label">Haftalık Rapor</span></div>`;
    } else {
        const santiyeOnclick = santiyeKilit ? `planKilit('santiye')` : `navGit('santiye')`;
        const santiyeLock    = santiyeKilit ? ' style="opacity:0.5"' : '';
        nav.innerHTML = `
            <div class="nav-item active" id="nav-home" onclick="navGit('home')"><span class="nav-icon"></span><span class="nav-label">Şantiye Dashboard</span></div>
            <div class="nav-item" id="nav-kamera" onclick="navGit('kamera')"><span class="nav-icon">📷</span><span class="nav-label">Saha Analizi</span></div>
            <div class="nav-item" id="nav-saha-kayitlari" onclick="navGit('saha-kayitlari')"><span class="nav-icon">🏠</span><span class="nav-label">Saha Kayıtları</span></div>
            <div class="nav-item" id="nav-gunluk" onclick="navGit('gunluk')"><span class="nav-icon">📝</span><span class="nav-label">Günlük Rapor</span></div>
            <div class="nav-item" id="nav-sesli" onclick="navGit('sesli')"><span class="nav-icon">🎤</span><span class="nav-label">Sesli Rapor</span></div>
            <div class="nav-item" id="nav-arsiv" onclick="navGit('arsiv')"><span class="nav-icon">📁</span><span class="nav-label">Arşiv</span></div>
            <div class="nav-item" id="nav-hesaplama" onclick="navGit('hesaplama')"><span class="nav-icon">🧮</span><span class="nav-label">Hesaplamalar</span></div>
            <div class="nav-item" id="nav-fiyat" onclick="${fiyatOnclick}"${fiyatLock}><span class="nav-icon">🏠</span><span class="nav-label">Fiyat Takibi${fiyatKilit ? ' 🔒':''}</span></div>
            <div class="nav-item" id="nav-stok" onclick="${stokOnclick}"${stokLock}><span class="nav-icon">🏠</span><span class="nav-label">Stok Takibi${stokKilit ? ' 🔒':''}</span></div>
            <div class="nav-item" id="nav-deprem" onclick="${depremOnclick}"${depremLock}><span class="nav-icon">🏠</span><span class="nav-label">Deprem Analizi${depremKilit ? ' 🔒':''}</span></div>
            <div class="nav-item" id="nav-santiye" onclick="${santiyeOnclick}"${santiyeLock}><span class="nav-icon"></span><span class="nav-label">Şantiye Yönetimi${santiyeKilit ? ' 🔒':''}</span></div>
            <div class="nav-item" id="nav-hakedis" onclick="navGit('hakedis')"><span class="nav-icon">📋</span><span class="nav-label">Hakediş</span></div>
            <div class="nav-item" id="nav-pdf" onclick="pdfIndir()"><span class="nav-icon">📄</span><span class="nav-label">PDF İndir</span></div>
            <div class="nav-item" id="nav-haftalik" onclick="haftalikRaporIndir()"><span class="nav-icon">📊</span><span class="nav-label">Haftalık Rapor</span></div>`;
    }
    setDashboardVisibility(rol);
    document.getElementById('result').innerHTML = isEngineerRole(rol)
        ? '<div class="res-title">👷 Mühendis Paneli Hazır</div><div class="res-detail">Kamera analizi, hesaplamalar ve raporlama araçlarına hazırsınız.</div>'
        : '<div class="res-title"> Yönetici Paneli Hazır</div><div class="res-detail">Doğrulanmış veri ile karar desteği, rapor bütünlüğü ve saha risk özetine hazırsınız.</div>';
    if (isEngineerRole(rol)) {
        setTimeout(() => loadEngineerDashboard(), 0);
    } else if (isContractorRole(rol)) {
        setTimeout(() => loadContractorDashboard(), 0);
    }
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

    btn.innerText = "â³ Kontrol Ediliyor...";

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
            applyServerUserProfile({ ...data, email });
            document.getElementById('auth-overlay').style.display = 'none';
            document.getElementById('mainApp').style.display = 'block';
            document.getElementById('navSidebar').style.display = 'flex';
            document.getElementById('topHeader').style.display = 'flex';
            dilDegistir(aktifDil);
            havaGuncelle();
            kullanımDurumuGoster();
            const kayitliRolGiris = data.role || localStorage.getItem('bai_rol');
            if (kayitliRolGiris) { navSidebarGuncelle(kayitliRolGiris); routeInitialPath(); }
            else setTimeout(() => rolEkraniniGoster(), 300);
            fiyatAlertBadgeGuncelle();
            setInterval(fiyatAlertBadgeGuncelle, 5 * 60 * 1000);
        } else {
            alert("Hata: " + (data.detail || "Bilgiler yanlış."));
            btn.innerText = "Şantiyeye Giriş Yap";
        }
    } catch (e) {
        alert("Sunucuya bağlanılamadı. app.py çalışıyor mu");
        btn.innerText = "Şantiyeye Giriş Yap";
    }
}

// --- 🌤¸ HAVA DURUMU ---
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
        if (widget) widget.textContent = `? ${data.cond} ${data.temp}?`;
    } catch (e) {
        if (condEl) condEl.innerText = "Bağlantı Yok";
        if (widget) widget.textContent = "? --";
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

// --- 🗂¸ ARŞİV KONTROLLERİ ---
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
    const token = localStorage.getItem('bai_token') || '';
    try {
        const response = await fetch('/rapor_listesi?token=' + token);
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
    resBox.innerHTML = `<i>â³ ${secilenTarih} tarihli rapor getiriliyor...</i>`;
    const token = localStorage.getItem('bai_token') || '';
    try {
        const response = await fetch('/rapor_getirtarih=' + encodeURIComponent(secilenTarih) + '&token=' + token);
        const data = await response.json();
        resBox.innerHTML = `
            <div class="res-title" style="color:#f1c40f;">ANTYE GNL: ${secilenTarih}</div>
            <div class="res-detail" style="color:#fff; font-size:1.1rem; border-top:none; white-space:pre-wrap; line-height:1.6;">${data.icerik}</div>
        `;
    } catch (e) {
        resBox.innerHTML = `<div class="res-title" style="color:#e74c3c;"> ARV BALANTI HATASI</div>`;
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
        resBox.innerHTML += `<div style="margin-top:15px; padding:10px; background:rgba(46,204,113,0.2); color:#2ecc71; border-radius:10px; text-align:center; font-weight:bold;">? ${data.mesaj}</div>`;
    } catch (e) {
        alert("Rapor kaydedilemedi!");
    }
}

// ---  DRAG & DROP ?? antiyeye zel RAG Dosya Ykleme ---
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
        label.textContent = gecerli.map(f => `🏗 ${f.name}`).join('  ?  ');
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

// ---  CHAT HUB  /api/chat balants ---
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
            <span class="chat-header-title"> Şantiye AI</span>
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
        div.innerHTML = `<div class="chat-avatar"></div><div class="chat-bubble chat-bubble--ai chat-bubble--thinking"><span class="chat-dots"><span></span><span></span><span></span></span><span style="font-size:11px;color:var(--text-3);margin-left:8px;">Analiz ediyor...</span></div>`;
    } else {
        div.className = 'chat-msg chat-msg--ai';
        let metaHtml = '';
        if (meta && meta.kritik_uyari && meta.kritik_uyari.length > 0) {
            metaHtml = `<div class="chat-uyari">${meta.kritik_uyari.map(u => `<span>${u}</span>`).join('')}</div>`;
        }
        div.innerHTML = `<div class="chat-avatar"></div><div class="chat-bubble chat-bubble--ai"><div class="chat-text">${markdownToHtml(icerik)}</div>${metaHtml}<span class="chat-time">${zaman}</span></div>`;
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
            chatMesajEkle('ai', '? **Limit doldu!** Profesyonel plana geçerek sınırsız kullanın.');
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
        chatMesajEkle('ai', '?? Bağlantı hatası. Lütfen tekrar deneyin.');
    }
}

function sonucGoster(html) {
    const resBox = document.getElementById('result');
    if (!resBox) return;
    resBox.innerHTML = `
        <div class="result-header">
            <div class="result-live-dot"></div>
            <div class="result-title"> AI Yanıtı</div>
            <div class="result-live-tag">LIVE</div>
        </div>
        <div class="result-body">${html}</div>`;
}

// --- 🧠  ANA SORU SİSTEMİ ---
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
            resBox.innerHTML = `<div style="text-align:center; padding:20px;"><div style="font-size:2rem; margin-bottom:10px;">?</div><div style="color:#e67e22; font-size:1.1rem; font-weight:bold; margin-bottom:10px;">Limit Doldu!</div><div style="color:#aaa; margin-bottom:20px;">${data.detail}</div><button onclick="profesyonelYukselt()" style="background:#e67e22; color:white; border:none; padding:12px 30px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:1rem;">Profesyonel'e Geç</button></div>`;
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
            <button onclick="pdfIndir()" style="margin-top:10px; background:#8b5cf6; color:white; border:none; padding:12px 20px; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">🏗 ${aktifDil === 'tr' ? 'PDF Rapor ?ndir' : 'Download PDF Report'}</button>
            <button onclick="gunlukRaporuKaydet()" style="margin-top:10px; background:#27ae60; color:white; border:none; padding:12px 20px; border-radius:10px; cursor:pointer; font-weight:bold; width:100%;">${t.saveBtn}</button>
        `;

        secilenResimBase64 = null;
        const imgBtn = document.getElementById('imgBtn');
        if (imgBtn) imgBtn.classList.remove('active-img');
        document.getElementById('soruInput').placeholder = "Soru sor, hesap seç veya fotoğraf yükle...";
    } catch (e) {
        resBox.innerHTML = " BALANTI HATASI";
    }
}

// --- 🇬Ÿ‡§ İNGİLİZCE ÇEVİRİ ---
async function ingilizceyeCevir() {
    const analizMetni = document.getElementById('analizMetni').innerText;
    const resBox = document.getElementById('result');
    resBox.innerHTML += "<div id='ceviriLoading'><i>â³ Generating Technical Report in English...</i></div>";

    try {
        const response = await fetch('/cevir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ metin: analizMetni })
        });
        const data = await response.json();
        document.getElementById('ceviriLoading').remove();
        resBox.innerHTML = `
            <div class="res-title" style="color:#3498db;">🇬Ÿ‡§ TECHNICAL REPORT</div>
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
    if (okuBtn) { okuBtn.disabled = true; okuBtn.innerText = 'â³...'; }

    metin = metin.replace(/\u00B0C/g, " santigrat derece").replace(/\u00B0F/g, " fahrenheit derece").replace(/\u00B0/g, " derece");

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

// --- 🏠 SESLİ DİNLEME ---
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
    recognition.onstart = () => { btn.classList.add('recording'); btn.innerHTML = '🎙'; };
    recognition.onend = () => { btn.classList.remove('recording'); btn.innerHTML = '🏠'; };
    recognition.onresult = (event) => {
        document.getElementById('soruInput').value = event.results[0][0].transcript;
    };
    recognition.start();
}

// --- 🏠 MODAL SİSTEMİ ---
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
        const url = '/hesaplatip=' + type + '&v1=' + (inputs.v1||0) + '&v2=' + (inputs.v2||0) + '&v3=' + (inputs.v3||0);
        const res = await fetch(url);
        const data = await res.json();
        document.getElementById('modalResultValue').textContent = data.sonuc || '';
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

// --- 🏠 MÜHENDİSLİK HESAPLAMALARI ---
function runCalc(type) {
    let title, fields;

    if (type === 'beton') {
        title = "🧱 Beton Metrajı";
        fields = [{key:'v1',label:'Boy (m)',placeholder:'5'}, {key:'v2',label:'En (m)',placeholder:'0.5'}, {key:'v3',label:'Yükseklik (m)',placeholder:'2.8'}];
    } else if (type === 'demir_ag') {
        title = "âš–ï¸ Donatı Ağırlığı";
        fields = [{key:'v1',label:'Çap (mm)',placeholder:'14'}, {key:'v2',label:'Uzunluk (m)',placeholder:'120'}];
    } else if (type === 'as_alan') {
        title = "🏠 Donatı Alanı (As)";
        fields = [{key:'v1',label:'Çap (mm)',placeholder:'14'}, {key:'v2',label:'Adet',placeholder:'4'}];
    } else if (type === 'etriye') {
        title = "🧱 Etriye Boyu";
        fields = [{key:'v1',label:'Boy (cm)',placeholder:'30'}, {key:'v2',label:'En (cm)',placeholder:'25'}, {key:'v3',label:'Çap (mm)',placeholder:'8'}];
    } else if (type === 'tugla') {
        title = "🧱 Tuğla Hesabı";
        fields = [{key:'v1',label:'Duvar Boy (m)',placeholder:'5'}, {key:'v2',label:'Duvar Yükseklik (m)',placeholder:'2.8'}];
    } else if (type === 'seramik') {
        title = "🏠 Seramik & Parke";
        fields = [{key:'v1',label:'Alan (m?)',placeholder:'50'}];
    } else if (type === 'boya') {
        title = "🧱 Boya & Sıva";
        fields = [{key:'v1',label:'Alan (m?)',placeholder:'100'}];
    } else if (type === 'kubaj') {
        title = "🧱 Hafriyat Küpajı";
        fields = [{key:'v1',label:'Uzunluk (m)',placeholder:'10'}, {key:'v2',label:'Genişlik (m)',placeholder:'5'}, {key:'v3',label:'Derinlik (m)',placeholder:'2'}];
    } else if (type === 'egim') {
        title = "🏠 Eğim & Açı";
        fields = [{key:'v1',label:'Yükseklik Farkı (m)',placeholder:'1'}, {key:'v2',label:'Yatay Mesafe (m)',placeholder:'10'}];
    } else {
        return;
    }

    openModal(title, fields, type);
}

// --- 🏠 MARKDOWN ?? HTML ---
function markdownToHtml(text) {
    return text
        .replace(/## 📋(.+)/g, '<h3 style="color:#e67e22; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(230,126,34,0.3); padding-bottom:6px;">📋$1</h3>')
        .replace(/## ⚠️(.+)/g, '<h3 style="color:#f39c12; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(243,156,18,0.3); padding-bottom:6px;">⚠️$1</h3>')
        .replace(/## 🛡️(.+)/g, '<h3 style="color:#2ecc71; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(46,204,113,0.3); padding-bottom:6px;">🛡️$1</h3>')
        .replace(/## 📐(.+)/g, '<h3 style="color:#3498db; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(52,152,219,0.3); padding-bottom:6px;">📐$1</h3>')
        .replace(/## (.+)/g, '<h3 style="color:#e67e22; margin:20px 0 8px 0; font-size:1.1rem; border-bottom:1px solid rgba(230,126,34,0.3); padding-bottom:6px;">$1</h3>')
        .replace(/\*\*(.+)\*\*/g, '<strong>$1</strong>')
        .replace(/^\* (.+)/gm, '<li style="margin:4px 0; color:inherit;">$1</li>')
        .replace(/(<li.*<\/li>\n)+/g, '<ul style="padding-left:20px; margin:8px 0;">$&</ul>')
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

// â"€â"€ YOLO Sonuç Paneli â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function _yoloPaneliOlustur(y) {
  const riskRenk = y.risk_level === 'Y?KSEK' ? '#ef4444'
                 : y.risk_level === 'ORTA' ? '#f59e0b'
                 :                             '#22c55e';
  const riskIcon = y.risk_level === 'Y?KSEK' ? '?'
                 : y.risk_level === 'ORTA' ? '?'
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
          <div style="font-size:18px;font-weight:800;color:${riskRenk};">${riskIcon} ${y.risk_level||''}</div>
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
        body: JSON.stringify({token, resim_base64: base64, analiz_tipi, hava, sehir, dil: aktifDil, santiye_id: kpCameraActiveSiteId()})
    });
    const yoloPromise = fetch('/yolo/frame', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({token, resim_base64: base64, santiye_id: kpCameraActiveSiteId()})
    });

    try {
        const res = await aiPromise;

        const data = await res.json();
        if (!res.ok) {
            const mesaj = res.status === 429
                ? `<div style="font-size:2rem">📁</div><strong style="color:#e74c3c">Limit doldu!</strong><div style="color:#aaa;margin-top:8px">${data.detail}</div>`
                : res.status === 503
                ? `<div style="font-size:2rem">â³</div><strong style="color:#f59e0b">AI servisi yoğun</strong><div style="color:#aaa;margin-top:8px">${data.detail || 'Lütfen birkaç saniye sonra tekrar deneyin.'}</div>`
                : `<div style="font-size:2rem">âŒ</div><strong style="color:#e74c3c">Hata</strong><div style="color:#aaa;margin-top:8px">${data.detail || 'Bilinmeyen hata'}</div>`;
            resBox.innerHTML = `<div style="text-align:center;padding:20px">${mesaj}</div>`;
            return;
        }
        const p = data.parsed;
        const t = TRANSLATIONS[aktifDil];

        //  Ortak foto blou ?? tm tipler iin 
        const fotoBlok = `
            <div id="analizImgWrap" style="position:relative;display:inline-block;width:100%;margin:12px 0 16px;border-radius:12px;overflow:hidden;line-height:0;">
                <img id="analizImg" src="${imgData}" style="width:100%;display:block;border-radius:12px;">
                <canvas id="bbCanvas" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:50;"></canvas>
            </div>`;

        if (analiz_tipi === 'guvenlik' && p) {
            const skor = p.guvenlik_skoru || 0;
            const skorRenk = skor >= 70 ? '#2ecc71' : skor >= 40 ? '#f39c12' : '#e74c3c';
            const ihlaller = (p.ihlaller || []).map(ih =>
                `<div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:10px;padding:10px 14px;margin-bottom:8px;color:#fca5a5;font-size:0.88rem;">📅 ${ih.aciklama}</div>`
            ).join('');
            const uygunlar = (p.uygun_unsurlar || []).map(u =>
                `<div style="background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.25);border-radius:10px;padding:10px 14px;margin-bottom:8px;color:#86efac;font-size:0.88rem;">? ${u}</div>`
            ).join('');
            const onlemler = (p.acil_onlemler || []).map(o =>
                `<div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.25);border-radius:10px;padding:10px 14px;margin-bottom:8px;color:#fcd34d;font-size:0.88rem;">?? ${o}</div>`
            ).join('');

            resBox.innerHTML = `
                <div class="res-title">👷 GÜVENLİK ANALİZİ</div>
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
                <button onclick="pdfIndir()" style="width:100%;margin-top:8px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">🏗 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
            // Hibrit analiz kutularn iz (YOLO + Gemini ?? visual_data varsa kullan)
            _drawAnalizFromResponse(data);

        } else if (analiz_tipi === 'ilerleme' && p) {
            const yuzde = Math.min(100, Math.max(0, p.ilerleme_yuzdesi || 0));
            const renk = yuzde >= 71 ? '#2ecc71' : yuzde >= 31 ? '#f59e0b' : '#ef4444';
            const tamamlanan = (p.tamamlanan_isler || []).map(i => `<li style="color:#86efac;margin:4px 0;font-size:0.88rem;">? ${i}</li>`).join('');
            const devam = (p.devam_eden_isler || []).map(i => `<li style="color:#93c5fd;margin:4px 0;font-size:0.88rem;">🚨 ${i}</li>`).join('');
            const gecikmeler = (p.olasi_gecikmeler || []).map(i => `<li style="color:#fcd34d;margin:4px 0;font-size:0.88rem;">?? ${i}</li>`).join('');

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
                <button onclick="pdfIndir()" style="width:100%;margin-top:8px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">🏗 PDF Rapor İndir</button>
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
                <div class="res-title">🔐 GENEL ANALİZ</div>
                ${fotoBlok}
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                    <div style="background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><span style="font-size:1.2rem;">👷</span><span style="color:${durumRenk(k.guvenlik.durum)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.guvenlik.durum || '-'}</span></div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Güvenlik</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.guvenlik.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><span style="font-size:1.2rem;">📅</span><span style="color:${durumRenk(k.ilerleme.durum)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.ilerleme.durum || '-'}</span></div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">İlerleme</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.ilerleme.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(249,115,22,0.08);border:1px solid rgba(249,115,22,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><span style="font-size:1.2rem;">🏠</span><span style="color:var(--primary);font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.malzeme.durum || '-'}</span></div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Malzeme</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.malzeme.ozet || ''}</div>
                    </div>
                    <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:14px;padding:16px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;"><span style="font-size:1.2rem;">??</span><span style="color:${seviyeRenk(k.risk.seviye)};font-size:0.75rem;font-weight:700;text-transform:uppercase;">${k.risk.seviye || '-'}</span></div>
                        <div style="color:white;font-weight:700;font-size:0.9rem;margin-bottom:4px;">Risk</div>
                        <div style="color:#aaa;font-size:0.78rem;line-height:1.4;">${k.risk.ozet || ''}</div>
                    </div>
                </div>
                <div id="analizMetni" style="display:none;">${data.cevap || ''}</div>
                <button onclick="pdfIndir()" style="width:100%;margin-top:16px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">🏗 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
            _drawAnalizFromResponse(data);
        } else {
            resBox.innerHTML = `
                <div class="res-title">📸 KAMERA ANALİZİ</div>
                ${fotoBlok}
                <div id="analizMetni" style="color:#1E293B;font-size:0.95rem;line-height:1.7;margin-top:10px;">${markdownToHtml(data.cevap)}</div>
                <button onclick="pdfIndir()" style="width:100%;margin-top:15px;padding:12px;background:#8b5cf6;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">🏗 PDF Rapor İndir</button>
                <button onclick="gunlukRaporuKaydet()" style="width:100%;margin-top:8px;padding:12px;background:#27ae60;color:white;border:none;border-radius:10px;cursor:pointer;font-weight:bold;">💾 Kaydet</button>
            `;
            _drawAnalizFromResponse(data);
        }

        sonAiCevabi = data.cevap;

        // YOLO stats paneli: allSettled ?? biri kerse dieri almaya devam eder.
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

// ihlaller-only izici (eski yollar iin uyumluluk katman ?? drawAnaliz'e ynlendirir)
function drawBoundingBoxes(ihlaller) {
    drawAnaliz(null, { parsed: { ihlaller } });
}

// YOLO-only izici (eski yollar iin uyumluluk katman ?? drawAnaliz'e ynlendirir)
function drawYoloBoundingBoxes(tespitler) {
    drawAnaliz({ tespitler }, null);
}

// ═══════════════════════════════════════════════════════════════════════════
//  Visual Fusion ?? Hibrit Analiz Canvas izicisi (GNCEL & KESN ZM)
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
            const label = '? ' + (ih.aciklama || 'İHLAL').toUpperCase();
            _drawBox(ctx, ih.x * dispW, ih.y * dispH, ih.w * dispW, ih.h * dispH, '#F97316', label, true);
        });
    }

    if (img.complete && img.naturalWidth > 0) {
        _paint();
    } else {
        img.onload = _paint;
    }
}

// --- 🏠 ARŞİV SAYFASI ---
let _arsivData = { raporlar: [], kamera_analizler: [] };
let _arsivAktifTab = 'tumu';

function arsivPageAc() {
  ['content','aiCommandBar','santiyePage','fiyatPage','stokPage','kameraPage','sahaKayitlariPage','hiyerarsiPage','hakedisPage','engineerDashboard','contractorDashboard'].forEach(pid => {
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
  document.getElementById('arsivIcerik').innerHTML = '<div style="text-align:center;padding:60px 20px;color:#94A3B8;"><div style="font-size:32px;margin-bottom:8px;">🏠</div><div style="font-size:14px;font-weight:600;">Yükleniyor...</div></div>';
  try {
    const res = await fetch('/arsivtoken=' + token);
    _arsivData = await res.json();
    arsivIstatistikGuncelle();
    arsivRenderListe();
  } catch(e) {
    document.getElementById('arsivIcerik').innerHTML = '<div style="text-align:center;padding:40px;color:#EF4444;font-size:13px;">Arşiv yüklenemedi.</div>';
  }
}

function arsivIstatistikGuncelle() {
  const reportCount = (_arsivData.raporlar || []).length;
  const cameraCount = (_arsivData.kamera_analizler || []).length;
  const decisionCount = (_arsivData.kararlar || []).length;
  const totalCount = reportCount + cameraCount + decisionCount;
  const setValue = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  };
  setValue('arsivStatRapor', reportCount);
  setValue('arsivStatKamera', cameraCount);
  setValue('arsivStatKarar', decisionCount);
  setValue('arsivStatToplam', totalCount);
  const sub = document.getElementById('arsivSubtitle');
  if (sub) sub.textContent = `Toplam ${totalCount} kayıt arşivde izleniyor`;
}

function arsivFiltrele() { arsivRenderListe(); }

async function arsivDetayGoster(tip, id) {
  const token = localStorage.getItem('bai_token');
  const modal = document.getElementById('arsivDetayModal');
  const contentEl = document.getElementById('arsivDetayIcerik');
  const titleEl = document.getElementById('arsivDetayBaslik');
  if (!modal || !contentEl) return;
  modal.style.display = 'flex';
  contentEl.innerHTML = '<div style="text-align:center;padding:40px;color:#64748B;">Yükleniyor...</div>';
  try {
    const res = await fetch(`/arsiv/${tip}/${id}?token=${token}`);
    const data = await res.json();
    const content = data.content || data.sonuc || '';
    if (titleEl) {
      titleEl.textContent =
        tip === 'rapor' ? 'AI Raporu' :
        tip === 'kamera' ? 'Kamera Analizi' :
        'Karar Geçmişi';
    }
    contentEl.innerHTML = typeof markdownToHtml === 'function' ? markdownToHtml(content) : engineerEscapeHtml(content);
  } catch (err) {
    contentEl.innerHTML = '<div style="color:#EF4444;">Kayıt detayı yüklenemedi.</div>';
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
  if (tip === 'karar') {
    if (typeof showToast === 'function') showToast('Karar geçmişi kaydı silinmez; filtreleyerek izleyebilirsiniz.', 'info');
    return;
  }
  if (!confirm('Bu kaydı kalıcı olarak silmek istediğinize emin misiniz')) return;
  const token = localStorage.getItem('bai_token');
  const endpoint = tip === 'rapor' ? `/rapor-sil/${id}` : `/kanit-sil/${id}`;
  try {
    const res = await fetch(`${endpoint}?token=${token}`, { method: 'DELETE' });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Hata');
    }
    if (typeof showToast === 'function') showToast('Kayıt silindi', 'success');
    if (tip === 'kamera') {
      _kpTumAnaliz = (_kpTumAnaliz || []).filter((item) => item.id !== id);
      localStorage.removeItem(`bai_thumb_${id}`);
      localStorage.removeItem(`bai_yolo_${id}`);
      if (typeof kpRenderAiKartlar === 'function') kpRenderAiKartlar(_kpTumAnaliz);
    }
    if (tip === 'rapor') _arsivData.raporlar = (_arsivData.raporlar || []).filter((item) => item.id !== id);
    if (tip === 'kamera') _arsivData.kamera_analizler = (_arsivData.kamera_analizler || []).filter((item) => item.id !== id);
    arsivIstatistikGuncelle();
    arsivRenderListe();
    arsivDetayKapat();
  } catch (err) {
    if (typeof showToast === 'function') showToast(`Hata: ${err.message}`, 'error');
  }
}

let secilenPlan = 'baslangic';
let selectedPlan = 'baslangic';

function normalizePlan(plan) {
  const value = String(plan || 'baslangic').toLowerCase();
  if (value.includes('max')) return 'profesyonel';
  if (value.includes('free') || value === 'pro') return 'baslangic';
  return ['baslangic', 'profesyonel', 'admin'].includes(value) ? value : 'baslangic';
}

// Active panel tracker
let _activePanel = 'login';

function switchPanel(panel) {
    if (panel === _activePanel) return;
    const outEl = document.getElementById('panel-' + _activePanel);
    const inEl  = document.getElementById('panel-' + panel);
    if (!outEl || !inEl) return;

    // Register paneline geçince adım seçimi sıfırla
    if (panel === 'register') {
        const s1 = document.getElementById('reg-step-select');
        const s2 = document.getElementById('reg-step-muteahhit');
        if (s1) s1.style.display = 'block';
        if (s2) s2.style.display = 'none';
        const msg = document.getElementById('regMsg');
        if (msg) msg.innerHTML = '';
    }

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
            redirect_uri_mismatch: 'Google yönlendirme adresi eşleşmiyor. Google Cloud Console redirect URI ayarını kontrol edin.',
            invalid_client: 'Google OAuth client bilgileri geçersiz.',
            invalid_grant: 'Google doğrulama kodu geçersiz veya süresi dolmuş. Tekrar deneyin.',
            missing_client_secret: 'Google OAuth client secret eksik.',
            oauth_token_exchange_failed: 'Google token değişimi başarısız. Sunucu loglarını kontrol edin.',
            userinfo_failed:'Google bilgileri alınamadı. Tekrar deneyin.',
            no_email:       'Google hesabından e-posta alınamadı.',
            email_not_verified: 'Google e-posta adresi doğrulanmamış.',
            account_link_required: 'Bu e-posta ile yerel hesabınız var. Şifrenizle giriş yapın; Google hesabı otomatik bağlanmaz.',
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
function regSelectRole(rol) {
    if (rol === 'davet') {
        showToast('Müteahhitinizden aldığınız davet linkini tarayıcınıza yapıştırın. Örnek: buildingai.com.tr/davet/XXXXX', 'info');
        return;
    }
    if (rol === 'davet') {
        showToast('Davet sistemi yakında aktif olacak. Müteahhitinizden davet beklentisi.', 'info');
        return;
    }
    document.getElementById('reg-step-select').style.display = 'none';
    document.getElementById('reg-step-muteahhit').style.display = 'block';
    setTimeout(() => document.getElementById('regName').focus(), 100);
}

function regGeriDon() {
    document.getElementById('reg-step-muteahhit').style.display = 'none';
    document.getElementById('reg-step-select').style.display = 'block';
    document.getElementById('regMsg').innerHTML = '';
}

async function kayitOl() {
    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const pass = document.getElementById('regPass').value;
    const passConfirm = document.getElementById('regPassConfirm').value;
    const sirketAdi = document.getElementById('regCompany').value.trim();
    const telefon = (document.getElementById('regTelefon').value || '').trim();
    const btn = document.getElementById('regBtn');
    const msg = document.getElementById('regMsg');

    if (!name || !email || !pass || !sirketAdi) {
        msg.innerHTML = '<div class="msg-error">Ad soyad, e-posta, şifre ve şirket adı zorunludur.</div>';
        return;
    }
    if (pass.length < 8) {
        msg.innerHTML = '<div class="msg-error">Şifre en az 8 karakter olmalı.</div>';
        return;
    }
    if (pass !== passConfirm) {
        msg.innerHTML = '<div class="msg-error">Şifreler eşleşmiyor.</div>';
        return;
    }

    btn.innerText = 'â³ Kaydediliyor...';
    btn.disabled = true;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password: pass, full_name: name, sirket_adi: sirketAdi, telefon: telefon || null })
        });
        const data = await response.json();

        if (response.ok) {
            // /register returns only the public user profile; obtain a real session.
            const loginResponse = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password: pass })
            });
            const session = await loginResponse.json();
            if (!loginResponse.ok || !session.token) {
                throw new Error(session.detail || 'Hesap oluşturuldu; lütfen giriş yapın.');
            }
            localStorage.setItem('bai_token', session.token);
            localStorage.setItem('bai_token_expiry', Date.now() + 7 * 24 * 60 * 60 * 1000);
            applyServerUserProfile(session);
            aktifKullanici = session;

            msg.innerHTML = '<div class="msg-success">? Hesabınız oluşturuldu!</div>';
            setTimeout(() => {
                document.getElementById('auth-overlay').style.display = 'none';
                document.getElementById('mainApp').style.display = 'block';
                document.getElementById('navSidebar').style.display = 'flex';
                document.getElementById('topHeader').style.display = 'flex';
                dilDegistir(aktifDil);
                havaGuncelle();
                showToast('Hoş geldiniz! İlk şantiyenizi oluşturabilirsiniz.', 'success');
            }, 800);
        } else {
            const detail = Array.isArray(data.detail)
                ? data.detail.map(item => item.msg || 'Geçersiz alan').join(' ')
                : data.detail;
            msg.textContent = detail || 'Kayıt başarısız.';
        }
    } catch (e) {
        msg.textContent = e.message || 'Sunucu bağlantı hatası.';
    }

    btn.innerText = 'Hesabı Oluştur ?';
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

async function sifreResetGuncelle() {
    const kod = document.getElementById('resetKod').value.trim();
    const yeniSifre = document.getElementById('resetYeniSifre').value;
    const tekrar = document.getElementById('resetYeniSifreTekrar').value;
    if (kod.length !== 6) { document.getElementById('resetMsg').innerHTML = '<div class="msg-error">6 haneli kodu girin.</div>'; return; }
    if (yeniSifre.length < 8) { document.getElementById('resetMsg').innerHTML = '<div class="msg-error">Şifre en az 8 karakter.</div>'; return; }
    if (yeniSifre !== tekrar) { document.getElementById('resetMsg').innerHTML = '<div class="msg-error">Şifreler eşleşmiyor.</div>'; return; }
    try {
        const res = await fetch('/sifre-guncelle', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: kod, email: document.getElementById("forgotEmail").value.trim(), yeni_sifre: yeniSifre }) });
        const data = await res.json();
        if (res.ok) {
            document.getElementById('resetMsg').innerHTML = '<div class="msg-success">? Şifreniz güncellendi!</div>';
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
  const plan = normalizePlan(document.getElementById('planBadge').innerText || '');
  const label = document.getElementById('planLabel');
  if (!label) return;

  if (plan.includes('admin') || window.isAdmin) {
    label.innerText = 'Admin';
    label.style.color = '#ef4444';
  } else if (plan.includes('profesyonel')) {
    label.innerText = 'Profesyonel';
    label.style.color = '#f59e0b';
  } else {
    label.innerText = 'Başlangıç';
    label.style.color = '#8b8fa8';
  }
}

// ── Fiyat Alert Zil ──────────────────────────────────────────────────────────

async function fiyatAlertBadgeGuncelle() {
  const token = localStorage.getItem('bai_token') || '';
  if (!token) return;
  const rol = localStorage.getItem('bai_rol') || '';
  if (!isContractorRole(rol)) return;
  try {
    const res = await fetch('/api/fiyat/alertler?limit=1&status=pending', {
      headers: { Authorization: 'Bearer ' + token }
    });
    if (!res.ok) return;
    const data = await res.json();
    const sayi = data.unread_count || 0;
    const badge = document.getElementById('fiyatAlertBadge');
    const icon = document.getElementById('fiyatAlertBellIcon');
    if (!badge) return;
    if (sayi > 0) {
      badge.textContent = sayi > 99 ? '99+' : String(sayi);
      badge.style.display = 'block';
      if (icon) icon.style.color = '#EF4444';
    } else {
      badge.style.display = 'none';
      if (icon) icon.style.color = '#64748B';
    }
  } catch (_) {}
}

function fiyatAlertBellTikla() {
  navGit('home');
  setTimeout(() => {
    const rol = localStorage.getItem('bai_rol') || '';
    if (isContractorRole(rol)) {
      if (typeof loadContractorDashboard === 'function') loadContractorDashboard(true);
      const panel = document.getElementById('contractorFiyatAlertPanel');
      if (panel) panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      const engineerDash = document.getElementById('engineerDashboard');
      if (engineerDash && engineerDash.style.display !== 'none') {
        const filterBtn = document.querySelector('.karar-filter-btn[data-filter="pending"]');
        if (filterBtn) filterBtn.click();
      }
      if (typeof loadEngineerDashboard === 'function') loadEngineerDashboard(true);
    }
    const badge = document.getElementById('fiyatAlertBadge');
    if (badge) badge.style.display = 'none';
    const icon = document.getElementById('fiyatAlertBellIcon');
    if (icon) icon.style.color = '#64748B';
  }, 300);
}

// ─────────────────────────────────────────────────────────────────────────────

function openProfile() {
    if (!aktifKullanici) return;
    const modal = document.getElementById('profileModal');
    modal.style.display = 'flex';

    const initials = aktifKullanici.full_name ? aktifKullanici.full_name.charAt(0).toUpperCase() : 'U';
    document.getElementById('profileAvatar').innerText = initials;
    document.getElementById('profileName').innerText = aktifKullanici.full_name || 'Kullanıcı';
    document.getElementById('profileEmail').innerText = aktifKullanici.email || '';
    document.getElementById('profilePlan').innerText = aktifKullanici.plan === 'profesyonel' ? 'PROFESYONEL PLAN' : 'BA?LANGI? PLAN';

    fetch('/rapor_listesi?token=' + (localStorage.getItem('bai_token') || '')).then(r => r.json()).then(data => {
        document.getElementById('statRapor').innerText = data.raporlar ? data.raporlar.length : 0;
    }).catch(() => {});
    kullanımDurumuGoster();
}

function closeProfile() {
    document.getElementById('profileModal').style.display = 'none';
}

// --- 🏗 PDF İNDİR ---
async function pdfIndir() {
    const analiz = document.getElementById('analizMetni') ? document.getElementById('analizMetni').innerText : "";
    const ingilizce = document.getElementById('englishMetni') ? document.getElementById('englishMetni').innerText : "";
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : "Sivas";
    const hava = (document.getElementById('temp') ? document.getElementById('temp').innerText : "") + " " +
                 (document.getElementById('condition') ? document.getElementById('condition').innerText : "");

    if (!analiz) {
        alert(aktifDil === 'tr' ? "?nce bir analiz yap?n!" : "Please run an analysis first!");
        return;
    }

    const btn = event.target;
    btn.innerText = aktifDil === 'tr' ? "Haz?rlan?yor..." : "Preparing...";
    btn.disabled = true;

    try {
        const response = await fetch('/pdf-indir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                kullanici_adi: aktifKullanici ? aktifKullanici.full_name : "M?hendis",
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

        btn.innerText = aktifDil === 'tr' ? "PDF ?ndirildi!" : "PDF Downloaded!";
        setTimeout(() => {
            btn.innerText = aktifDil === 'tr' ? "PDF Rapor ?ndir" : "Download PDF Report";
            btn.disabled = false;
        }, 2000);
    } catch (e) {
        alert(aktifDil === 'tr' ? "PDF olu?turulurken hata olu?tu." : "Error creating PDF.");
            btn.innerText = aktifDil === 'tr' ? "PDF Rapor ?ndir" : "Download PDF Report";
        btn.disabled = false;
    }
}

async function cikisYap() {
    await fetch("/logout", { method: "POST" });
    aktifKullanici = null;
    localStorage.removeItem('bai_token');
    localStorage.removeItem('bai_user');
    localStorage.removeItem('bai_rol');
    localStorage.removeItem('bai_aktif_santiye');
    localStorage.removeItem('bai_aktif_santiye_ad');
    localStorage.removeItem('bai_aktif_santiye_sehir');
    localStorage.removeItem('bai_aktif_santiye_lat');
    localStorage.removeItem('bai_aktif_santiye_lon');
    closeProfile();
    document.getElementById('mainApp').style.display = 'none';
    document.getElementById('navSidebar').style.display = 'none';
    document.getElementById('topHeader').style.display = 'none';
    document.getElementById('auth-overlay').style.display = 'flex';
    document.getElementById('loginEmail').value = '';
    document.getElementById('loginPass').value = '';
    switchPanel('login');
}

// --- 🏠 SESLİ RAPOR ---
let sesliRaporMediaRecorder = null;
let sesliRaporChunks = [];

async function sesliRaporBaslat() {
    const btn = document.getElementById('sesliRaporBtn');

    if (sesliRaporMediaRecorder && sesliRaporMediaRecorder.state === 'recording') {
        sesliRaporMediaRecorder.stop();
        btn.classList.remove('active');
        const icon = btn.querySelector('.qa-icon'); if (icon) icon.textContent = '🏠';
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
                resBox.innerHTML = '<div class="res-title">🏠 Ses işleniyor...</div><div class="res-detail">Yapay zeka sesinizi analiz ediyor...</div>';
                try {
                    const hava = (document.getElementById('condition').innerText || '');
                    const sesliToken = localStorage.getItem('bai_token') || '';
                    const res = await fetch('/sesli-rapor', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ audio_base64: base64, hava, dil: aktifDil, token: sesliToken })
                    });
                    if (res.status === 429) {
                        const err = await res.json();
                        resBox.innerHTML = `<div style="text-align:center; padding:20px;"><div style="font-size:2rem; margin-bottom:10px;">?</div><div style="color:#e67e22; font-size:1.1rem; font-weight:bold; margin-bottom:10px;">Limit Doldu!</div><div style="color:#aaa; margin-bottom:20px;">${err.detail}</div><button onclick="profesyonelYukselt()" style="background:#e67e22; color:white; border:none; padding:12px 30px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:1rem;">Profesyonel'e Geç</button></div>`;
                        return;
                    }
                    const data = await res.json();
                    if (res.ok) {
                        resBox.innerHTML = `
                            <div class="res-title">🏠 Sesli Rapor Oluşturuldu</div>
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
        const icon = btn.querySelector('.qa-icon'); if (icon) icon.textContent = 'â¹ï¸';
        const label = btn.querySelector('.qa-label'); if (label) label.textContent = 'Durdur';
    } catch(e) {
        alert('Mikrofon erişimi reddedildi.');
    }
}

// --- 🏠 GÜNLÜK RAPOR ---
function gunlukRaporAc() {
    const modal = document.getElementById('gunlukRaporModal');
    if (!modal) return;
    modal.style.display = 'flex';
    // Set today's date
    const tarihEl = document.getElementById('grTarih');
    if (tarihEl && !tarihEl.value) {
        tarihEl.value = new Date().toISOString().split('T')[0];
    }
    let manual = document.getElementById('grManualActions');
    if (!manual) {
        manual = document.createElement('div');
        manual.id = 'grManualActions';
        manual.style.cssText = 'padding:12px 18px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;margin:12px 0;display:flex;gap:8px;flex-wrap:wrap;align-items:center';
        manual.innerHTML = '<button type="button" onclick="gunlukRaporManuelKaydet()" style="background:#0f172a;color:#fff;border:0;border-radius:8px;padding:10px 14px;cursor:pointer">Taslak kaydet</button><button type="button" onclick="gunlukRaporGecmisiYukle()" style="background:#fff;border:1px solid #cbd5e1;border-radius:8px;padding:10px 14px;cursor:pointer">Geçmiş raporlar</button><div id="grManualMessage" role="status" style="width:100%;font-size:13px"></div><div id="grManualHistory" style="width:100%;max-height:160px;overflow:auto"></div>';
        (document.getElementById('grYapilanlar')?.parentElement || modal.firstElementChild).appendChild(manual);
    }
    gunlukRaporGecmisiYukle();
}

async function gunlukRaporManuelKaydet() {
    const siteId = localStorage.getItem('bai_aktif_santiye');
    const date = document.getElementById('grTarih')?.value;
    const done = document.getElementById('grYapilanlar')?.value.trim();
    const issues = document.getElementById('grSorunlar')?.value.trim();
    const next = document.getElementById('grYarin')?.value.trim();
    const message = document.getElementById('grManualMessage');
    if (!siteId || !date || !done) { message.textContent = 'Proje, tarih ve yapılan işleri tamamlayın.'; return; }
    const button = document.querySelector('#grManualActions button');
    button.disabled = true;
    try {
        const response = await fetch('/daily-reports/manual', {method:'POST', headers:{'Authorization':'Bearer '+localStorage.getItem('bai_token'),'Content-Type':'application/json'},
            body:JSON.stringify({santiye_id:Number(siteId), report_date:date, summary:`Yapılan işler: ${done}\nSorunlar: ${issues || 'Belirtilmedi'}\nSonraki işler: ${next || 'Belirtilmedi'}`})});
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Rapor kaydedilemedi.');
        message.textContent = 'Taslak kaydedildi.';
        await gunlukRaporGecmisiYukle();
    } catch (error) { message.textContent = `${error.message} Girdileriniz korunuyor; tekrar deneyin.`; }
    finally { button.disabled = false; }
}

async function gunlukRaporGecmisiYukle() {
    const history = document.getElementById('grManualHistory');
    const siteId = localStorage.getItem('bai_aktif_santiye');
    const epoch = window._baiProjectEpoch || 0;
    if (!history) return;
    if (!siteId) { history.textContent = 'Raporları görmek için proje seçin.'; return; }
    try {
        const response = await fetch(`/daily-reports?santiye_id=${encodeURIComponent(siteId)}`, {headers:{'Authorization':'Bearer '+localStorage.getItem('bai_token')}});
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Rapor listesi alınamadı.');
        if (epoch !== (window._baiProjectEpoch || 0)) return;
        history.innerHTML = (data.raporlar || []).length ? data.raporlar.map(r => `<div style="border-top:1px solid #e2e8f0;padding:8px 0"><strong>${_hakedisEscape(r.report_date)}</strong> · ${r.status === 'draft' ? 'Taslak' : _hakedisEscape(r.status)}<div style="white-space:pre-wrap">${_hakedisEscape(r.summary || 'Özet yok')}</div></div>`).join('') : 'Bu projede kayıtlı günlük rapor yok.';
    } catch (error) { history.textContent = `${error.message} Tekrar deneyin.`; }
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
    const hava = (document.getElementById('condition').innerText || '');

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
            sonucDiv.innerHTML = `<div style="text-align:center; padding:16px; background:#FEF3C7; border-radius:10px; font-size:0.85rem; color:#92400E;">${data.detail}<br><button onclick="profesyonelYukselt()" style="margin-top:10px; background:#0D1117; color:white; border:none; padding:10px 20px; border-radius:8px; cursor:pointer; font-weight:700; font-size:0.82rem;">Profesyonel'e Geç</button></div>`;
            return;
        }
        const data = await res.json();
        if (res.ok) {
            document.getElementById('result').innerHTML = `
                <div class="res-title">🏠 Günlük Rapor</div>
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

// --- 🏠 PLAN SİSTEMİ ---
const PLAN_BILGI = {
    profesyonel: {
        ad: 'Profesyonel', renk: '#f1c40f', icon: '', fiyat: '1.990 TL/ay',
        ozellikler: ['Sınırsız AI Sorgu', 'Sınırsız Kamera', 'Haftalık Rapor', 'Şantiye Yönetimi', 'Stok & Fiyat Takibi', 'Deprem Analizi', 'Öncelikli Destek'],
    },
};
const OZELLIK_ACIKLAMA = {
    stok:            { ad: 'Stok Takibi',             icon: '🏠', gereken: 'profesyonel' },
    deprem_analiz:   { ad: 'Deprem Analizi',           icon: '🏠', gereken: 'profesyonel' },
    fiyat_takip:     { ad: 'Fiyat Takibi',             icon: '🏠', gereken: 'profesyonel' },
    santiye:         { ad: 'Şantiye Dashboard',        icon: '', gereken: 'profesyonel' },
    haftalik_rapor:  { ad: 'Haftalık Rapor',           icon: '🌍', gereken: 'profesyonel' },
    kamera_gelismis: { ad: 'Gelişmiş Kamera Limiti',   icon: '🏠', gereken: 'profesyonel' },
};

function planKilit(ozellik) {
    const el = document.getElementById('planKilitModal');
    if (!el) return;
    const oz = OZELLIK_ACIKLAMA[ozellik] || { ad: ozellik, icon: '📁', gereken: 'profesyonel' };
    const hedefPlan = oz.gereken;
    const pb = PLAN_BILGI[hedefPlan] || PLAN_BILGI.profesyonel;
    const ozellikListesi = pb.ozellikler.map(o => `<li style="padding:4px 0; color:#ccc; font-size:0.9rem;">? ${o}</li>`).join('');
    el.innerHTML = `
        <div style="background:#1a1a2e; border:1px solid ${pb.renk}; border-radius:20px; padding:36px 32px; max-width:420px; width:90%; position:relative; text-align:center;">
            <button onclick="planKilitKapat()" style="position:absolute; top:14px; right:16px; background:none; border:none; color:#aaa; font-size:1.4rem; cursor:pointer;">?</button>
            <div style="font-size:3rem; margin-bottom:12px;">📁</div>
            <h2 style="color:white; margin:0 0 6px 0; font-size:1.3rem;">${oz.icon} ${oz.ad}</h2>
            <p style="color:#aaa; margin:0 0 16px 0; font-size:0.9rem;">Bu özelliği kullanmak için yükseltme gerekiyor.</p>
            <div style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:18px; margin-bottom:20px; text-align:left;">
                <div style="font-size:0.85rem; color:#aaa; margin-bottom:8px; text-align:center;">
                    <span style="color:${pb.renk}; font-weight:700; font-size:1.1rem;">${pb.ad} PLAN</span>
                    &nbsp;? <b style="color:white;">${pb.fiyat}</b> ile açılır
                </div>
                <ul style="list-style:none; padding:0; margin:0;">${ozellikListesi}</ul>
            </div>
            <button onclick="odemePaneliAc('${hedefPlan}')" style="width:100%; padding:14px; background:linear-gradient(135deg,${pb.renk},${pb.renk}cc); border:none; color:#111; border-radius:14px; cursor:pointer; font-weight:700; font-size:1rem; margin-bottom:10px; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
                ${pb.ad} Planına Geç
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
    plan = plan || 'profesyonel';
    planKilitKapat();
    const pb = PLAN_BILGI[plan] || PLAN_BILGI.profesyonel;
    const el = document.getElementById('odemeModal');
    if (!el) return;
    el.innerHTML = `
        <div style="background:#1a1a2e; border:1px solid ${pb.renk}; border-radius:20px; padding:32px; max-width:460px; width:90%; position:relative;">
            <button onclick="odemeModalKapat()" style="position:absolute; top:14px; right:16px; background:none; border:none; color:#aaa; font-size:1.4rem; cursor:pointer;">?</button>
            <h2 style="color:${pb.renk}; margin:0 0 4px 0; font-size:1.35rem;">${pb.ad} Plana Geç</h2>
            <p style="color:#aaa; font-size:0.88rem; margin:0 0 18px 0;">IBAN'a ödeme yapın, formu doldurun ?? 24 saat içinde aktifleştireceğiz.</p>
            <div style="background:#111; border:1px solid #333; border-radius:10px; padding:12px; display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                <span style="color:#f1c40f; font-family:monospace; font-size:0.88rem; word-break:break-all;">TR80 0001 0090 1095 7865 2050 01</span>
                <button onclick="navigator.clipboard.writeText('TR80 0001 0090 1095 7865 2050 01').then(()=>{document.getElementById('odemeModalMsg').textContent='? Kopyalandı!';document.getElementById('odemeModalMsg').style.color='#2ecc71';})" style="background:${pb.renk}; border:none; color:#111; border-radius:8px; padding:5px 10px; cursor:pointer; font-size:0.78rem; white-space:nowrap; margin-left:8px;">Kopyala</button>
            </div>
            <p style="color:#555; font-size:0.8rem; margin:0 0 4px 0;">Ad: Mehmet Akif Erdemir</p>
            <p style="color:#aaa; font-size:0.85rem; margin:0 0 16px 0;">Fiyat: <b style="color:white;">${pb.fiyat}</b></p>
            <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:16px;">
                <input type="text" id="odemeAdSoyad" placeholder="Ad Soyad *" style="background:#111; border:1px solid #333; border-radius:10px; padding:11px 14px; color:white; font-size:0.9rem; outline:none;">
                <input type="text" id="odemeTelefon" placeholder="Telefon (opsiyonel)" style="background:#111; border:1px solid #333; border-radius:10px; padding:11px 14px; color:white; font-size:0.9rem; outline:none;">
                <textarea id="odemeAciklama2" placeholder="Açıklama ? havale açıklamanıza yazdığınız bilgiyi yazın" rows="2" style="background:#111; border:1px solid #333; border-radius:10px; padding:11px 14px; color:white; font-size:0.9rem; resize:none; outline:none;"></textarea>
            </div>
            <button onclick="odemeBildir('${plan}')" style="width:100%; padding:14px; background:linear-gradient(135deg,#27ae60,#2ecc71); border:none; color:white; border-radius:14px; cursor:pointer; font-weight:700; font-size:1rem; transition:0.3s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">
                ? Ödemeyi Yaptım, Bildiri Gönder
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
    plan = plan || 'profesyonel';
    const ad_soyad = document.getElementById('odemeAdSoyad').value.trim();
    const telefon  = document.getElementById('odemeTelefon').value.trim();
    const aciklama = document.getElementById('odemeAciklama2').value.trim();
    const msgEl    = document.getElementById('odemeModalMsg');
    if (!ad_soyad) { msgEl.textContent = 'â— Ad soyad zorunlu.'; msgEl.style.color='#e74c3c'; return; }
    msgEl.textContent = 'â³ Gönderiliyor...'; msgEl.style.color='#aaa';
    try {
        const res = await fetch('/odeme-bildir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token, plan, ad_soyad, telefon, aciklama })
        });
        const data = await res.json();
        if (res.ok) {
            msgEl.textContent = '? ' + data.mesaj;
            msgEl.style.color = '#2ecc71';
        } else {
            msgEl.textContent = 'âŒ ' + (data.detail || 'Bir hata oluştu.');
            msgEl.style.color = '#e74c3c';
        }
    } catch(e) {
        msgEl.textContent = 'âŒ Bağlantı hatası.';
        msgEl.style.color = '#e74c3c';
    }
}
function planBadgeHTML(plan) {
    if (plan === 'admin') return '<span style="background:rgba(231,76,60,0.15); border:1px solid #e74c3c; color:#e74c3c; border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:700;">📋¸ ADMİN</span>';
    if (plan === 'profesyonel') return '<span style="background:rgba(241,196,15,0.15); border:1px solid #f1c40f; color:#f1c40f; border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:700;">PROFESYONEL</span>';
    return '<span style="background:rgba(230,126,34,0.15); border:1px solid #e67e22; color:#e67e22; border-radius:20px; padding:3px 10px; font-size:0.78rem; font-weight:700;">BAŞLANGIÇ</span>';
}

// --- 🏠 KULLANIM DURUMU & PLAN ---
async function kullanımDurumuGoster() {
    const token = localStorage.getItem('bai_token');
    if (!token) return;
    try {
        const res = await fetch(`/kullanim-durumu?token=${token}`);
        const data = await res.json();
        if (res.ok) {
            data.plan = normalizePlan(data.plan);
            window._kullaniciPlan = data.plan;
            window._planOzellikler = data.plan_ozellikleri || {};
            const k = data.kullanim;
            const sorEl = document.getElementById('statSorgu');
            if (sorEl) {
                const sorLimit = k.sor.limit;
                sorEl.textContent = sorLimit === null ? "?" : `${k.sor.kullanilan}/${sorLimit}`;
            }

            // â"€â"€ KPI Dashboard Cards â"€â"€
            function setKpi(valId, barId, used, limit, labelFn) {
                const vEl = document.getElementById(valId);
                const bEl = document.getElementById(barId);
                if (!vEl) return;
                const pct = limit === null ? 0 : Math.min(100, Math.round((used / limit) * 100));
                vEl.textContent = limit === null ? `${used} / ?` : (labelFn ? labelFn(used, limit) : `${used} / ${limit}`);
                if (bEl) setTimeout(() => bEl.style.width = (limit === null ? 10 : pct) + '%', 100);
            }
            setKpi('kpiAiVal', 'kpiAiBar', k.sor.kullanilan, k.sor.limit);
            setKpi('kpiKameraVal', 'kpiKameraBar', k.kamera.kullanilan, k.kamera.limit);
            setKpi('kpiRaporVal', 'kpiRaporBar', k.gunluk_rapor.kullanilan, k.gunluk_rapor.limit);
            const planEl = document.getElementById('kpiPlanVal');
            if (planEl) {
                const planLabels = {baslangic:'Başlangıç', profesyonel:'Profesyonel', admin:'📋¸ Admin'};
                planEl.textContent = planLabels[data.plan] || data.plan;
                planEl.style.color = data.plan === 'profesyonel' ? '#f1c40f' : data.plan === 'admin' ? '#22c55e' : '#94a3b8';
            }
            const badge = document.getElementById('profilePlan');
            if (badge) badge.innerHTML = planBadgeHTML(data.plan);
            const topBadge = document.getElementById('planBadge');
            if (topBadge) {
                if (data.plan === 'admin') topBadge.innerHTML = '📋¸ ADMIN';
                else if (data.plan === 'profesyonel') topBadge.innerHTML = 'PROFESYONEL';
                else topBadge.innerHTML = 'BAŞLANGIÇ';
            }
            updatePlanLabel();
            const kayitliRol = localStorage.getItem('bai_rol');
            if (kayitliRol) { navSidebarGuncelle(kayitliRol); routeInitialPath(); }
        }
    } catch(e) {}
}

function profesyonelYukselt(aciklama) {
    const msg = aciklama || localStorage.getItem('bai_user') && JSON.parse(localStorage.getItem('bai_user') || '{}').email || '';
    const el = document.getElementById('odemeAciklama');
    if (el) el.value = msg;
    document.getElementById('odemeMsg').textContent = '';
    document.getElementById('profesyonelModal').style.display = 'flex';
}

function profesyonelModalKapat() {
    document.getElementById('profesyonelModal').style.display = 'none';
}

function ibanKopyala() {
    const iban = document.getElementById('ibanText').textContent.trim();
    navigator.clipboard.writeText(iban).then(() => {
        document.getElementById('odemeMsg').textContent = '? IBAN kopyalandı!';
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
    msgEl.textContent = 'â³ Gönderiliyor...';
    msgEl.style.color = '#aaa';
    try {
        const res = await fetch('/odeme-bildirimi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token, plan: selectedPlan || 'profesyonel' })
        });
        const data = await res.json();
        if (res.ok) {
            msgEl.textContent = '? ' + data.mesaj;
            msgEl.style.color = '#2ecc71';
        } else {
            msgEl.textContent = 'âŒ ' + (data.detail || 'Bir hata oluştu.');
            msgEl.style.color = '#e74c3c';
        }
    } catch(e) {
        msgEl.textContent = 'âŒ Bağlantı hatası.';
        msgEl.style.color = '#e74c3c';
    }
}

// --- 🗺¸ NAV SIDEBAR ---
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
    btn.textContent = navCollapsed ? '?' : '?';
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
  document.querySelector('.quick-btn[onclick="guvenlikAc()"]').classList.add('active');

  // Global şantiye seçiciden oku
  const globalSantiye = document.getElementById('globalSantiyeSecici');
  const guvenlikSantiye = document.getElementById('guvenlikSantiye');
  if (globalSantiye && guvenlikSantiye && globalSantiye.value) {
      guvenlikSantiye.value = globalSantiye.value;
  }

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
    home: '🏠  Ana Sayfa',
    kamera: '🏠 Kamera Analizi',
    'saha-kayitlari': 'Saha Kayıtları',
    hesaplama: '🏠 Hesaplama',
    arsiv: '🏠 Arşiv',
    gunluk: '🏠 Günlük Rapor',
    sesli: '🏠 Sesli Rapor',
    hiyerarsi: '🏠—ï¸ Metraj Yönetimi',
    hakedis: '📋 Hakediş',
};

function tumSayfalariGizle() {
    const sayfalar = document.querySelectorAll('[id$="Page"], [id$="page"], [id$="Sayfa"]');
    sayfalar.forEach(s => {
        if (s.id && s.id.toLowerCase().includes('modal')) return;
        s.style.display = 'none';
    });

    ['content', 'aiCommandBar', 'engineerDashboard', 'contractorDashboard'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = 'none';
    });

    const hBtn = document.getElementById('spHeaderBtn');
    if (hBtn) hBtn.style.display = 'none';
}

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
    else if (page === 'saha-kayitlari') sahaKayitlariPageAc();
    else if (page === 'hesaplama') toggleSidebar();
    else if (page === 'arsiv') arsivPageAc();
    else if (page === 'gunluk') gunlukRaporAc();
    else if (page === 'sesli') sesliRaporBaslat();
    else if (page === 'fiyat') fiyatPageAc();
    else if (page === 'stok') stokPageAc();
    else if (page === 'deprem') depremModalAc();
    else if (page === 'hiyerarsi') hiyerarsiPageAc();
    else if (page === 'hakedis') hakedisPageAc();
    else if (page === 'santiye') santiyePageAc();
    // home: kapat diğer sayfaları
    else {
        santiyePageKapat();
        fiyatPageKapat();
        stokPageKapat();
        sahaKayitlariPageKapat();
        kameraPageKapat();
        arsivKapat();
        hiyerarsiPageKapat();
        hakedisPageKapat();
        const aktifDashboardRol = localStorage.getItem('bai_rol');
        if (isEngineerRole(aktifDashboardRol)) loadEngineerDashboard(true);
        else if (isContractorRole(aktifDashboardRol)) loadContractorDashboard(true);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

async function routeInitialPath() {
    const params = new URLSearchParams(window.location.search);
    const module = params.get('workspace_module');
    const allowed = ['hiyerarsi', 'hakedis', 'stok', 'fiyat'];
    if (allowed.includes(module)) {
        const requestedSite = Number(params.get('site'));
        if (Number.isSafeInteger(requestedSite) && requestedSite > 0) {
            try {
                const token = localStorage.getItem('bai_token');
                const response = await fetch('/santiyeler', {headers: {'Authorization': 'Bearer ' + token}});
                if (!response.ok) throw new Error('Şantiye listesi alınamadı.');
                const result = await response.json();
                const site = (result.santiyeler || []).find(item => Number(item.id) === requestedSite);
                if (!site) throw new Error('Bu şantiyeye erişiminiz yok.');
                localStorage.setItem('bai_aktif_santiye', String(site.id));
                localStorage.setItem('bai_aktif_santiye_ad', site.ad || 'Şantiye');
                window._aktifSantiyeId = String(site.id);
                window._aktifSantiyeAd = site.ad || 'Şantiye';
                await globalSantiyeSeciciDoldur();
            } catch (error) {
                showToast(error.message, 'error');
                return;
            }
        }
        navGit(module);
        return;
    }
    if (window.location.pathname === '/saha-kayitlari') {
        setTimeout(() => navGit('saha-kayitlari'), 0);
    }
}

// --- 🏠 FİYAT TAKİBİ ---
let fiyatGrafigi = null;

function fiyatModalAc() {
    document.getElementById('fiyatModal').style.display = 'flex';
    fiyatlarYukle();

    // Özel malzemeleri dropdown'a ekle
    (async function() {
        const select = document.getElementById('fiyatMalzemeSelect');
        if (!select) return;
        select.querySelectorAll('option[data-ozel]').forEach(o => o.remove());
        try {
            const token = localStorage.getItem('bai_token');
            const resp = await fetch('/ozel-malzemeler', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            const data = await resp.json();
            if (data.status === 'success' && data.malzemeler && data.malzemeler.length > 0) {
                const sep = document.createElement('option');
                sep.disabled = true;
                sep.textContent = 'â"€â"€ Özel Malzemeler â"€â"€';
                sep.setAttribute('data-ozel', 'true');
                select.appendChild(sep);
                data.malzemeler.forEach(m => {
                    const opt = document.createElement('option');
                    opt.value = m.malzeme_key;
                    opt.textContent = m.ad + ' (' + m.birim + ')';
                    opt.setAttribute('data-ozel', 'true');
                    select.appendChild(opt);
                });
            }
        } catch(e) { console.log('Özel malzemeler yüklenemedi:', e); }
    })();
}

function fiyatModalKapat() {
    document.getElementById('fiyatModal').style.display = 'none';
}

// --- 🏠 STOK TAKİBİ ---
async function stokModalAc() {
    document.getElementById('stokModal').style.display = 'flex';
    await stokSantiyeleriModalYukle();
    const aktifId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
    stokYukleModal(aktifId ? parseInt(aktifId) : null);
    stokGecmisModalYukle();
}

async function stokSantiyeleriModalYukle() {
    const token = localStorage.getItem('bai_token');
    const sel = document.getElementById('stokSantiyeM');
    if (!sel) return;
    try {
        const res = await fetch(`/santiyeler?token=${token}`);
        const data = await res.json();
        const santiyeler = data.santiyeler || [];
        const aktifId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
        sel.innerHTML = '<option value="">🏠 Şantiye Seçin... (zorunlu)</option>' +
            santiyeler.map(s => `<option value="${s.id}"${String(s.id) === String(aktifId) ? ' selected' : ''}>${s.ad}</option>`).join('');
    } catch(e) {}
}

function stokSantiyeModalDegisti() {
    const santiyeId = document.getElementById('stokSantiyeM').value;
    stokYukleModal(santiyeId ? parseInt(santiyeId) : null);
    stokGecmisModalYukle();
}

async function stokYukleModal(santiyeId) {
    const token = localStorage.getItem('bai_token');
    try {
        const url = santiyeId ? `/stok?token=${token}&santiye_id=${santiyeId}` : `/stok?token=${token}`;
        const res = await fetch(url);
        const data = await res.json();
        const kartlar = document.getElementById('stokKartlarM');
        const uyarilar = document.getElementById('stokUyarilarM');
        if (!kartlar) return;
        const stoklar = data.stok || [];
        if (!stoklar.length) { kartlar.innerHTML = '<div style="color:#94A3B8;text-align:center;padding:16px;font-size:0.85rem;">Stok kaydı yok.</div>'; return; }
        kartlar.innerHTML = stoklar.map(s => `<div style="background:rgba(255,255,255,0.06);border-radius:10px;padding:12px;"><div style="color:white;font-weight:700;font-size:0.9rem;">${s.malzeme_ad || s.malzeme}</div><div style="color:#94A3B8;font-size:0.8rem;">${s.toplam_miktar} ${s.birim || ''}</div></div>`).join('');
        if (uyarilar) {
            const kritik = stoklar.filter(s => s.min_miktar && s.toplam_miktar < s.min_miktar);
            uyarilar.innerHTML = kritik.map(s => `<div style="background:#7f1d1d;color:#fca5a5;padding:8px 12px;border-radius:8px;font-size:0.8rem;margin-bottom:6px;">⚠️ ${s.malzeme_ad || s.malzeme}: ${s.toplam_miktar} (min ${s.min_miktar})</div>`).join('');
        }
    } catch(e) {}
}

async function stokGecmisModalYukle() {
    const token = localStorage.getItem('bai_token');
    const malzeme = document.getElementById('stokGecmisMalzemeM')?.value || '';
    const aktifSantiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
    try {
        let url = `/stok-hareketler?token=${token}&limit=50`;
        if (malzeme) url += `&malzeme=${encodeURIComponent(malzeme)}`;
        if (aktifSantiyeId) url += `&santiye_id=${aktifSantiyeId}`;
        const res = await fetch(url);
        const data = await res.json();
        const liste = document.getElementById('stokGecmisListeM');
        if (!liste) return;
        if (!data.hareketler || data.hareketler.length === 0) {
            liste.innerHTML = '<div style="color:#94A3B8;text-align:center;padding:16px;font-size:0.85rem;">Henüz hareket kaydı yok.</div>';
            return;
        }
        liste.innerHTML = data.hareketler.map(h => {
            const isGiris = h.tip === 'giris';
            const badgeColor = isGiris ? '#16A34A' : '#DC2626';
            const badgeLabel = isGiris ? 'Giriş' : 'Çıkış';
            const tarih = h.created_at ? h.created_at.substring(0, 10) : '';
            return `<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.07);gap:8px;">
                <div style="flex:1;min-width:0;">
                    <span style="color:${badgeColor};font-size:10px;font-weight:700;margin-right:6px;">${badgeLabel}</span>
                    <span style="color:white;font-size:0.82rem;font-weight:700;">${h.malzeme_ad || h.malzeme} · ${h.miktar} ${h.birim || ''}</span>
                    <div style="color:#94A3B8;font-size:0.72rem;display:flex;gap:6px;flex-wrap:wrap;margin-top:2px;">
                        ${h.tedarikci ? `<span>🏭 ${h.tedarikci}</span>` : ''}
                        ${h.notlar ? `<span>📝 ${h.notlar}</span>` : ''}
                    </div>
                </div>
                <span style="color:#94A3B8;font-size:0.72rem;white-space:nowrap;">${tarih}</span>
            </div>`;
        }).join('');
    } catch(e) { console.error('stokGecmisModalYukle hatası:', e); }
}

async function stokSantiyeleriYukle() {
    const token = localStorage.getItem('bai_token');
    const sel = document.getElementById('stokSantiye');
    if (!sel) return;
    try {
        const res = await fetch(`/santiyeler?token=${token}`);
        const data = await res.json();
        const santiyeler = data.santiyeler || [];
        sel.innerHTML = '<option value="">🏠 Şantiye Seçin... (zorunlu)</option>' +
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

async function stokKaydetModal() {
    const token = localStorage.getItem('bai_token');
    const modal = document.getElementById('stokModal');
    const q = id => modal.querySelector('#' + id);
    const santiye_id = q('stokSantiyeM')?.value
        || window._aktifSantiyeId
        || localStorage.getItem('bai_aktif_santiye')
        || null;
    const malzeme = q('stokMalzeme')?.value;
    const tip = q('stokTip')?.value || 'giris';
    const miktar = q('stokMiktar')?.value;
    const birim = q('stokBirim')?.value || '';
    const tedarikci = q('stokTedarikci')?.value || '';
    const fiyat = q('stokFiyat')?.value || '';
    const notlar = q('stokNotlar')?.value || '';
    const msg = q('stokMsgM');
    if (!santiye_id) { alert('Lütfen bir şantiye seçin'); return; }
    if (!malzeme) { if (msg) msg.innerHTML = '<span style="color:#e74c3c;">Malzeme seçin.</span>'; return; }
    if (!miktar) { if (msg) msg.innerHTML = '<span style="color:#e74c3c;">Miktar girin.</span>'; return; }
    try {
        const res = await fetch('/stok-ekle', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, santiye_id: parseInt(santiye_id), malzeme, malzeme_ad: malzeme, tip, miktar, birim, tedarikci, fiyat, notlar})
        });
        const data = await res.json();
        if (res.ok) {
            if (msg) msg.innerHTML = '<span style="color:#2ecc71;">✓ ' + data.mesaj + '</span>';
            stokYukleModal(santiye_id ? parseInt(santiye_id) : null);
            stokGecmisModalYukle();
        } else {
            const detail = data.detail || 'Hata.';
            if (msg) msg.innerHTML = '<span style="color:#e74c3c;">' + detail + '</span>';
        }
    } catch(e) {
        if (msg) msg.innerHTML = '<span style="color:#e74c3c;">Bağlantı hatası.</span>';
    }
}

async function stokYukle(santiyeId) {
    const token = localStorage.getItem('bai_token');
    try {
        const url = santiyeId ? `/stok?token=${token}&santiye_id=${santiyeId}` : `/stok?token=${token}`;
        const res = await fetch(url);
        const data = await res.json();

        // Uyarılar (gizli div, işlevsel)
        const uyariDiv = document.getElementById('stokUyarilar');
        if (uyariDiv) uyariDiv.innerHTML = '';

        // Ana panel kritik stok sayacı
        const _uyariSayi = (data.uyarilar || []).length;
        const _watchlistEl = document.getElementById('contractorMetricWatchlistValue');
        if (_watchlistEl) _watchlistEl.textContent = _uyariSayi;

        // Stat kartları (toplamDeger ve kritikler data'dan, sayı render sonrası)
        const tumStok = data.stok || {};
        const malzemeler = Object.values(tumStok);
        const toplamDeger = malzemeler.reduce((s,m) => s + (m.stok_degeri_tl||0), 0);
        const kritikler = malzemeler.filter(m => m.uyari);
        const el = id => document.getElementById(id);
        if (el('statToplamDeger'))
            el('statToplamDeger').innerHTML = toplamDeger.toLocaleString('tr-TR', {maximumFractionDigits:0}) + ' &#8378;';

        // Malzeme satır listesi
        const container = document.getElementById('stokListeSatirlar');
        if (!container) { stokGecmisYukle(); return; }
        const filtre = window._stokFiltre || 'hepsi';
        let html = '';
        if (data.gruplar && data.gruplar.length > 0) {
            data.gruplar.forEach(g => {
                html += `<div style="padding:6px 16px; background:#F8F9FA; font-size:11px; font-weight:700; color:#6B7280; letter-spacing:0.05em; border-bottom:1px solid #E8ECF0;">${g.santiye_adi}</div>`;
                Object.entries(g.stok||{}).forEach(([m,s]) => { html += stokSatirHtml(m, s, filtre); });
            });
        } else if (data.stok) {
            Object.entries(data.stok).forEach(([m,s]) => { html += stokSatirHtml(m, s, filtre); });
        }
        if (!html) html = `<div style="padding:40px; text-align:center; color:#9CA3AF; font-size:13px;">Henuz stok kaydi yok.</div>`;
        container.innerHTML = html;

        // Gerçek görünen satır sayısını DOM'dan al
        const gercekSayi = container.querySelectorAll('div[style*="grid-template-columns"]').length;
        if (el('statMalzemeSayisi'))
            el('statMalzemeSayisi').textContent = gercekSayi + ' malzeme';
        if (el('statKritik'))
            el('statKritik').textContent = kritikler.length + ' / ' + gercekSayi;
        if (el('statKritikAd') && kritikler.length > 0)
            el('statKritikAd').textContent = kritikler[0].malzeme_ad;
        // Ilk veri satirinin border-top'unu kaldir
        const ilkSatir = container.querySelector('div[style*="border-top:1px solid #F3F4F6"]');
        if (ilkSatir) ilkSatir.style.borderTop = 'none';
        setTimeout(() => _stokSparklines(data), 80);

        stokGecmisYukle();

        // Esik malzeme select'ini gercek stok key'leriyle doldur
        try {
            const esikSel = document.getElementById('esikMalzeme');
            if (esikSel && esikSel.tagName === 'SELECT') {
                const tumKeys = [];
                if (data.gruplar && data.gruplar.length > 0) {
                    data.gruplar.forEach(g => Object.entries(g.stok||{}).forEach(([k,v]) => tumKeys.push({key:k, ad:v.malzeme_ad||k})));
                } else if (data.stok) {
                    Object.entries(data.stok).forEach(([k,v]) => tumKeys.push({key:k, ad:v.malzeme_ad||k}));
                }
                const mevcut = esikSel.value;
                esikSel.innerHTML = '<option value="">Malzeme sec...</option>' +
                    tumKeys.map(item => `<option value="${item.key}">${item.ad}</option>`).join('');
                if (mevcut) esikSel.value = mevcut;
            }
        } catch(selErr) {}
    } catch(e) {
        const c = document.getElementById('stokListeSatirlar');
        if (c) c.innerHTML = '<div style="color:#9CA3AF; text-align:center; padding:40px; font-size:13px;">Stok verisi yuklenemedi.</div>';
    }
}

function stokSatirHtml(m, s, filtre) {
  if (filtre==='kritik' && !s.uyari) return '';
  if (filtre==='dusuk' && (s.bitis_gun||999) > 14) return '';

  const sc = s.uyari
    ? {color:'#DC2626', bg:'#FEF2F2', border:'#FECACA'}
    : (s.bitis_gun||999)<=14
    ? {color:'#D97706', bg:'#FFFBEB', border:'#FDE68A'}
    : {color:'#16A34A', bg:'#F0FDF4', border:'#BBF7D0'};

  const gunText = s.bitis_gun ? s.bitis_gun+'g' : '--';
  const sparkId = 'sp_'+m.replace(/[^a-zA-Z0-9]/g,'_');

  const ik = _stokIkonSvg(m);

  const mEsc = m.replace(/'/g,"'");
  return `<div style="display:grid;
    grid-template-columns:2fr 100px 90px 70px 100px 100px 88px;
    padding:12px 16px; border-bottom:1px solid #F9FAFB;
    align-items:center; cursor:pointer;
    transition:background .12s;"
    onclick="malzemeDetayAc('${mEsc}')"
    onmouseover="this.style.background='#F9FAFB'"
    onmouseout="this.style.background='white'">

    <div style="display:flex;align-items:center;gap:10px;">
      <div style="width:34px;height:34px;border-radius:9px;
        background:${ik.ikonBg};
        display:flex;align-items:center;justify-content:center;
        flex-shrink:0;">
        ${ik.ikonSvg}
      </div>
      <div>
        <div style="font-size:13px;font-weight:600;
          color:#111827;line-height:1.3;
          font-family:'Plus Jakarta Sans',sans-serif;">
          ${s.malzeme_ad||m}</div>
        <div style="font-size:11px;color:#9CA3AF;margin-top:1px;
          font-family:'Plus Jakarta Sans',sans-serif;">
          ${s.tedarikci||'&mdash;'}</div>
      </div>
    </div>

    <div>
      <span style="font-size:14px;font-weight:700;
        color:#111827;
        font-family:'Plus Jakarta Sans',sans-serif;">
        ${(s.mevcut||0).toLocaleString('tr-TR')}</span>
      <span style="font-size:11px;color:#9CA3AF;
        margin-left:3px;
        font-family:'Plus Jakarta Sans',sans-serif;">
        ${s.birim||''}</span>
    </div>

    <div style="position:relative;">
      <canvas id="${sparkId}" width="80" height="28"
        style="display:block;"></canvas>
    </div>

    <div style="font-size:13px;color:#6B7280;
      font-family:'JetBrains Mono',monospace;">
      ${(s.min_esik > 0) ? s.min_esik : '&mdash;'}
    </div>

    <div style="font-size:13px;color:#374151;
      font-family:'Plus Jakarta Sans',sans-serif;">
      ${s.son_fiyat
        ? s.son_fiyat.toLocaleString('tr-TR',
            {maximumFractionDigits:0})+' &#8378;'
        : '&mdash;'}
    </div>

    <div style="font-size:13px;font-weight:600;
      color:#111827;
      font-family:'Plus Jakarta Sans',sans-serif;">
      ${s.stok_degeri_tl
        ? s.stok_degeri_tl.toLocaleString('tr-TR',
            {maximumFractionDigits:0})+' &#8378;'
        : '&mdash;'}
    </div>

    <div>
      <span style="display:inline-flex;align-items:center;
        gap:4px;padding:3px 10px;border-radius:20px;
        background:${sc.bg};color:${sc.color};
        font-size:11px;font-weight:700;
        font-family:'Plus Jakarta Sans',sans-serif;
        border:1px solid ${sc.border};">
        <span style="width:6px;height:6px;border-radius:50%;
          background:${sc.color};flex-shrink:0;"></span>
        ${gunText}
      </span>
    </div>
  </div>`;
}

// ══════ MALZEME DETAY PANELİ ══════
window._detayMalzeme = null;

async function malzemeDetayAc(malzemeKey) {
  const token = localStorage.getItem('bai_token');
  const aktifSantiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';

  const tablar = document.querySelector('#stokPage > div:last-child > div[style*="grid-template-columns:1fr 1fr"]');
  const girisForm = document.getElementById('stokGirisForm');
  const sarfForm = document.getElementById('stokSarfForm');
  const detayPanel = document.getElementById('malzemeDetayPanel');

  if (tablar) tablar.style.display = 'none';
  if (girisForm) girisForm.style.display = 'none';
  if (sarfForm) sarfForm.style.display = 'none';
  if (detayPanel) detayPanel.style.display = 'flex';

  try {
    const stokUrl = aktifSantiyeId
      ? `/stok?token=${token}&santiye_id=${aktifSantiyeId}`
      : `/stok?token=${token}`;
    const stokRes = await fetch(stokUrl);
    const stokData = await stokRes.json();

    const malzeme = stokData.stok ? stokData.stok[malzemeKey] : null;
    if (!malzeme) {
      document.getElementById('detayHareketler').innerHTML =
        '<div style="padding:16px;text-align:center;color:#DC2626;font-size:12px;">Malzeme bulunamadı.</div>';
      return;
    }

    window._detayMalzeme = { key: malzemeKey, ...malzeme };

    document.getElementById('detayMalzemeAd').textContent = malzeme.malzeme_ad || malzemeKey;
    document.getElementById('detayTedarikci').textContent = malzeme.tedarikci || '—';
    document.getElementById('detayStok').innerHTML =
      (malzeme.mevcut||0).toLocaleString('tr-TR') + ' <span style="font-size:12px;color:#9CA3AF;font-weight:400;">' + (malzeme.birim||'') + '</span>';
    document.getElementById('detayDeger').innerHTML =
      (malzeme.stok_degeri_tl||0).toLocaleString('tr-TR', {maximumFractionDigits:0}) + ' &#8378;';
    document.getElementById('detayFiyat').innerHTML =
      malzeme.son_fiyat ? malzeme.son_fiyat.toLocaleString('tr-TR', {maximumFractionDigits:0}) + ' &#8378;' : '—';
    document.getElementById('detayMin').textContent =
      malzeme.min_esik || (malzeme.min_esik===0 ? '0' : '—');

    const sc = malzeme.uyari
      ? {color:'#DC2626', bg:'#FEF2F2', border:'#FECACA', text:'Kritik'}
      : (malzeme.bitis_gun||999)<=14
      ? {color:'#D97706', bg:'#FFFBEB', border:'#FDE68A', text:'Düşük'}
      : {color:'#16A34A', bg:'#F0FDF4', border:'#BBF7D0', text:'Normal'};
    document.getElementById('detayDurumBadge').innerHTML =
      `<span style="padding:4px 12px;border-radius:20px;font-size:11px;font-weight:700;
        background:${sc.bg};color:${sc.color};border:1px solid ${sc.border};
        font-family:'Plus Jakarta Sans',sans-serif;">${sc.text}</span>`;

    document.getElementById('detayStokEkleBtn').onclick = function() {
      malzemeDetayKapat();
      stokTabDegis('giris');
      const inp = document.getElementById('stokMalzemeInput');
      if (inp) { inp.value = malzeme.malzeme_ad || malzemeKey; stokMalzemeSecildi('giris'); }
    };
    document.getElementById('detaySarfBtn').onclick = function() {
      malzemeDetayKapat();
      stokTabDegis('sarf');
      const inp = document.getElementById('sarfMalzemeInput');
      if (inp) { inp.value = malzeme.malzeme_ad || malzemeKey; stokMalzemeSecildi('sarf'); }
    };

    _detayTrendCiz(malzeme);
    _detayHareketlerYukle(malzemeKey, malzeme.malzeme_ad);

  } catch(e) {
    console.error('Detay yükleme hatası:', e);
  }
}

function malzemeDetayKapat() {
  const detayPanel = document.getElementById('malzemeDetayPanel');
  if (detayPanel) detayPanel.style.display = 'none';

  const sagPanel = detayPanel ? detayPanel.parentElement : null;
  if (sagPanel) {
    const tablar = sagPanel.querySelector('div[style*="grid-template-columns:1fr 1fr"]');
    if (tablar) tablar.style.display = 'grid';
  }

  const girisBtn = document.getElementById('tabGiris');
  const isGiris = girisBtn && girisBtn.style.background.includes('E15A1F');
  const girisForm = document.getElementById('stokGirisForm');
  const sarfForm = document.getElementById('stokSarfForm');
  if (isGiris) {
    if (girisForm) girisForm.style.display = 'flex';
    if (sarfForm) sarfForm.style.display = 'none';
  } else {
    if (girisForm) girisForm.style.display = 'none';
    if (sarfForm) sarfForm.style.display = 'flex';
  }

  window._detayMalzeme = null;
}

function _detayTrendCiz(malzeme) {
  const canvas = document.getElementById('detayTrendCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width = canvas.offsetWidth * 2;
  const h = canvas.height = 160;
  ctx.scale(2, 2);
  const dw = w/2, dh = h/2;
  ctx.clearRect(0, 0, dw, dh);

  const trend = malzeme.trend_7g || malzeme.trend || [];
  if (trend.length < 2) {
    ctx.fillStyle = '#9CA3AF';
    ctx.font = '12px "Plus Jakarta Sans", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Yeterli trend verisi yok', dw/2, dh/2);
    return;
  }

  const pad = {top:10, right:10, bottom:24, left:40};
  const pw = dw - pad.left - pad.right;
  const ph = dh - pad.top - pad.bottom;
  const min = Math.min(...trend) * 0.9;
  const max = Math.max(...trend) * 1.1 || 1;

  ctx.strokeStyle = '#F3F4F6';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = pad.top + (ph / 4) * i;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(dw - pad.right, y);
    ctx.stroke();
    const val = max - ((max - min) / 4) * i;
    ctx.fillStyle = '#9CA3AF';
    ctx.font = '9px "JetBrains Mono", monospace';
    ctx.textAlign = 'right';
    ctx.fillText(Math.round(val).toLocaleString('tr-TR'), pad.left - 6, y + 3);
  }

  const points = trend.map((v, i) => ({
    x: pad.left + (pw / (trend.length - 1)) * i,
    y: pad.top + ph - ((v - min) / (max - min)) * ph
  }));

  ctx.beginPath();
  ctx.strokeStyle = '#E15A1F';
  ctx.lineWidth = 2;
  ctx.lineJoin = 'round';
  ctx.lineCap = 'round';
  points.forEach((p, i) => { if (i===0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y); });
  ctx.stroke();

  ctx.lineTo(points[points.length-1].x, pad.top + ph);
  ctx.lineTo(points[0].x, pad.top + ph);
  ctx.closePath();
  ctx.fillStyle = 'rgba(225, 90, 31, 0.06)';
  ctx.fill();

  points.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
    ctx.fillStyle = '#E15A1F';
    ctx.fill();
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 1.5;
    ctx.stroke();
  });
}

async function _detayHareketlerYukle(malzemeKey, malzemeAd) {
  const container = document.getElementById('detayHareketler');
  if (!container) return;
  const token = localStorage.getItem('bai_token');
  const aktifSantiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';

  try {
    let url = `/stok-hareketler?token=${token}&limit=20`;
    if (malzemeAd) url += `&malzeme=${encodeURIComponent(malzemeAd)}`;
    if (aktifSantiyeId) url += `&santiye_id=${aktifSantiyeId}`;

    const res = await fetch(url);
    const data = await res.json();

    if (!data.hareketler || data.hareketler.length === 0) {
      container.innerHTML = '<div style="padding:20px;text-align:center;color:#9CA3AF;font-size:12px;">Bu malzemeye ait hareket yok.</div>';
      return;
    }

    container.innerHTML = data.hareketler.map(h => {
      const giris = h.tip === 'giris';
      const renk = giris ? '#16A34A' : '#2563EB';
      const bg = giris ? '#F0FDF4' : '#EFF6FF';
      const tarih = (h.created_at||'').substring(0,10);
      return `<div style="display:flex; align-items:center; gap:10px;
        padding:10px 0; border-bottom:1px solid #F9FAFB;">
        <div style="width:28px; height:28px; border-radius:50%;
          background:${bg}; display:flex; align-items:center;
          justify-content:center; flex-shrink:0;">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none"
            stroke="${renk}" stroke-width="2.5">
            ${giris ? '<path d="M12 19V5M5 12l7-7 7 7"/>' : '<path d="M12 5v14M5 12l7 7 7-7"/>'}
          </svg>
        </div>
        <div style="flex:1;min-width:0;">
          <div style="font-size:12px;color:#374151;font-weight:500;">
            ${giris ? 'Giriş' : 'Sarf'}${h.tedarikci ? ' · '+h.tedarikci : ''}</div>
          <div style="font-size:11px;color:#9CA3AF;">${tarih}</div>
        </div>
        <div style="font-size:13px;font-weight:700;color:${renk};
          font-family:'Plus Jakarta Sans',sans-serif;">
          ${giris?'+':'-'}${(h.miktar||0).toLocaleString('tr-TR')} ${h.birim||''}
        </div>
      </div>`;
    }).join('');
  } catch(e) {
    container.innerHTML = '<div style="padding:16px;text-align:center;color:#DC2626;font-size:12px;">Yüklenemedi.</div>';
  }
}

function _stokIkonSvg(m) {
  const k = (m||'').toLowerCase();
  if (k.includes('demir')||k.includes('çelik')||k.includes('celik'))
    return {ikonBg:'#FEF3C7', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'};
  if (k.includes('cimento')||k.includes('çimento')||k.includes('cement'))
    return {ikonBg:'#F3F4F6', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>'};
  if (k.includes('beton'))
    return {ikonBg:'#EFF6FF', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>'};
  if (k.includes('tuğla')||k.includes('tugla'))
    return {ikonBg:'#FEF2F2', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2"><rect x="2" y="8" width="20" height="5" rx="1"/><rect x="2" y="14" width="20" height="5" rx="1"/><line x1="7" y1="8" x2="7" y2="13"/><line x1="12" y1="14" x2="12" y2="19"/><line x1="17" y1="8" x2="17" y2="13"/></svg>'};
  if (k.includes('kum')||k.includes('agrega'))
    return {ikonBg:'#FFFBEB', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 3v9l6 3"/></svg>'};
  if (k.includes('seramik')||k.includes('fayans'))
    return {ikonBg:'#F0FDF4', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2"><rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="8" rx="1"/><rect x="3" y="13" width="8" height="8" rx="1"/><rect x="13" y="13" width="8" height="8" rx="1"/></svg>'};
  if (k.includes('boya'))
    return {ikonBg:'#FDF4FF', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#A855F7" stroke-width="2"><path d="M19 11V9a7 7 0 0 0-14 0v2"/><rect x="5" y="11" width="14" height="10" rx="2"/><circle cx="12" cy="16" r="1"/></svg>'};
  if (k.includes('ahşap')||k.includes('ahsap')||k.includes('tahta'))
    return {ikonBg:'#FEF9C3', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#CA8A04" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><line x1="8" y1="6" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="18"/></svg>'};
  if (k.includes('cam'))
    return {ikonBg:'#EFF6FF', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18" stroke-opacity="0.5"/></svg>'};
  if (k.includes('pvc')||k.includes('boru'))
    return {ikonBg:'#F0FDF4', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>'};
  return {ikonBg:'#F3F4F6', ikonSvg:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>'};
}

function _stokSparklines(data) {
  const stok = data.stok || {};
  Object.entries(stok).forEach(([m, s]) => {
    const id = 'sp_' + m.replace(/[^a-zA-Z0-9]/g,'_');
    const c = document.getElementById(id);
    if (!c) return;

    // Gerçek trend: toplam_giris/toplam_cikis bazlı
    // 7 nokta: 6. gün giriş etkisi, 7. gün mevcut
    const giris = s.toplam_giris || 0;
    const cikis = s.toplam_cikis || 0;
    const mevcut = s.mevcut || 0;

    // Yeterli veri yoksa düz çizgi
    if (giris === 0 && cikis === 0) {
      const ctx = c.getContext('2d');
      ctx.clearRect(0, 0, c.width, c.height);
      ctx.beginPath();
      ctx.strokeStyle = '#E2E8F0';
      ctx.lineWidth = 1.5;
      ctx.moveTo(0, c.height/2);
      ctx.lineTo(c.width, c.height/2);
      ctx.stroke();
      return;
    }

    // Gerçek trend hesabı
    const pts = [];
    for (let i = 0; i < 7; i++) {
      const gunGiris = (giris / 7) * (i + 1);
      const gunCikis = (cikis / 7) * (i + 1);
      pts.push(Math.max(0, gunGiris - gunCikis));
    }
    pts[6] = mevcut;

    const color = s.uyari ? '#EF4444' :
      (s.bitis_gun||999) <= 14 ? '#F59E0B' : '#22C55E';

    const ctx = c.getContext('2d');
    const W = c.width, H = c.height;
    const mn = Math.min(...pts);
    const mx = Math.max(...pts) || 1;

    ctx.clearRect(0, 0, W, H);
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.8;
    ctx.lineJoin = 'round';
    pts.forEach((p, i) => {
      const x = (i / 6) * W;
      const y = H - ((p - mn) / (mx - mn || 1)) * (H - 4) - 2;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Alan dolgusu
    ctx.lineTo(W, H);
    ctx.lineTo(0, H);
    ctx.closePath();
    ctx.fillStyle = color + '18';
    ctx.fill();

    // Hover tooltip
    const wrapper = c.parentElement;
    if (!wrapper._tooltipAdded) {
      wrapper._tooltipAdded = true;
      wrapper.style.position = 'relative';

      const tip = document.createElement('div');
      tip.style.cssText = `
        position:absolute; bottom:calc(100% + 6px); left:50%;
        transform:translateX(-50%);
        background:#1A1D23; color:white;
        padding:4px 8px; border-radius:6px;
        font-size:11px; font-weight:600;
        white-space:nowrap; pointer-events:none;
        opacity:0; transition:opacity 0.15s; z-index:100;
        font-family:'Plus Jakarta Sans',sans-serif;`;
      wrapper.appendChild(tip);

      c.addEventListener('mousemove', (e) => {
        const rect = c.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const idx = Math.min(6,
          Math.round((x / W) * 6));
        const val = pts[idx];
        tip.textContent = val.toLocaleString('tr-TR',
          {maximumFractionDigits:1}) +
          ' ' + (s.birim || '');
        tip.style.opacity = '1';
        tip.style.left = (x / W * 100) + '%';
      });

      c.addEventListener('mouseleave', () => {
        tip.style.opacity = '0';
      });
    }
  });
}

window._stokFiltre = 'hepsi';

function stokFiltrele(tip) {
  window._stokFiltre = tip;
  const map = {hepsi:'filterHepsi', dusuk:'filterDusuk', kritik:'filterKritik'};
  Object.entries(map).forEach(([k,id]) => {
    const b = document.getElementById(id);
    if (!b) return;
    const aktif = k===tip;
    b.style.background = aktif ? '#1A1D23' : 'white';
    b.style.color = aktif ? 'white' : '#6B7280';
    b.style.border = aktif ? 'none' : '1px solid #E8ECF0';
  });
  const sid = window._aktifSantiyeId||null;
  stokYukle(sid ? parseInt(sid) : null);
}

function stokAramaYap(q) {
  document.querySelectorAll('#stokListeSatirlar > div[style*="grid-template-columns"]').forEach(r => {
    r.style.display = r.textContent.toLowerCase().includes(q.toLowerCase()) ? 'grid' : 'none';
  });
}

function stokTumHareketler() {
  console.log('Tum hareketler - ileride eklenecek');
}

function stokGecmisMalzemeFiltrele(malzeme) {
    const sel = document.getElementById('stokGecmisMalzeme');
    if (sel) sel.value = malzeme;
    stokGecmisYukle();
}

function _stokHareketHtml(h) {
  const giris = h.tip==='giris';
  const renk = giris ? '#16A34A' : '#2563EB';
  const bg   = giris ? '#F0FDF4' : '#EFF6FF';
  let alt;
  if (giris) {
    alt = [h.tedarikci, h.notlar].filter(Boolean).join(' · ');
  } else {
    const notlarParcalar = (h.notlar||'').split(' | ').map(p => p.replace(/^[İi]ş\s+[Kk]alemi:\s*/,'').trim()).filter(Boolean);
    alt = notlarParcalar.join(' · ') || h.kaynak || '';
  }
  const tarihHam = (h.created_at||'').substring(0,16);
  const tarih = tarihHam.includes('T')
    ? tarihHam.replace('T',' · ')
    : tarihHam.replace(' ', ' · ');
  return `<div style="display:flex; align-items:center; gap:12px; padding:14px 20px; border-bottom:1px solid #F9FAFB;">
    <div style="width:32px; height:32px; border-radius:50%; background:${bg}; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="${renk}" stroke-width="2.5">
        ${giris ? '<path d="M12 19V5M5 12l7-7 7 7"/>' : '<path d="M12 5v14M5 12l7 7 7-7"/>'}
      </svg>
    </div>
    <div style="flex:1; min-width:0;">
      <div style="font-size:13px; font-weight:600; color:#111827; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; font-family:'Plus Jakarta Sans',sans-serif;">${h.malzeme_ad||h.malzeme}</div>
      <div style="font-size:11px; color:#9CA3AF; margin-top:2px; font-family:'Plus Jakarta Sans',sans-serif;">${alt||'&mdash;'}</div>
    </div>
    <div style="text-align:right; flex-shrink:0;">
      <div style="font-size:13px; font-weight:700; color:${renk}; font-family:'Plus Jakarta Sans',sans-serif;">${giris?'+':'-'}${(h.miktar||0).toLocaleString('tr-TR')}${h.birim ? ' '+h.birim : ''}</div>
      <div style="font-size:11px; color:#9CA3AF; margin-top:2px;">${tarih}</div>
    </div>
    <button onclick="stokHareketSil(${h.id})" style="background:none; border:none; padding:4px 6px; cursor:pointer; color:#E2E8F0; transition:color 0.1s; flex-shrink:0;" onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='#E2E8F0'">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="3 6 5 6 21 6"/>
        <path d="M19 6l-1 14H6L5 6"/>
        <path d="M10 11v6M14 11v6"/>
        <path d="M9 6V4h6v2"/>
      </svg>
    </button>
  </div>`;
}

async function stokGecmisYukle() {
    const token = localStorage.getItem('bai_token');
    const malzemeEl = document.getElementById('stokGecmisMalzeme');
    const malzeme = malzemeEl ? malzemeEl.value : '';
    const aktifSantiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
    try {
        let url = `/stok-hareketler?token=${token}&limit=50`;
        if (malzeme) url += `&malzeme=${encodeURIComponent(malzeme)}`;
        if (aktifSantiyeId) url += `&santiye_id=${aktifSantiyeId}`;
        const res = await fetch(url);
        const data = await res.json();

        // Haftalık stat
        const birHaftaOnce = new Date(Date.now()-7*24*60*60*1000);
        const buHafta = (data.hareketler||[]).filter(h => new Date(h.created_at) >= birHaftaOnce);
        const girisler = buHafta.filter(h=>h.tip==='giris');
        const cikislar = buHafta.filter(h=>h.tip==='cikis');
        const girisT = girisler.reduce((s,h)=>s+(h.fiyat||0)*(h.miktar||0),0);
        const cikisT = cikislar.reduce((s,h)=>s+(h.fiyat||0)*(h.miktar||0),0);
        const el = id => document.getElementById(id);
        if (el('statHaftaGiris'))
            el('statHaftaGiris').innerHTML = (girisT>0 ? '+' : '') + girisT.toLocaleString('tr-TR',{maximumFractionDigits:0}) + ' &#8378;';
        if (el('statHaftaGirisSay'))
            el('statHaftaGirisSay').textContent = girisler.length + ' sevkiyat';
        if (el('statHaftaCikis'))
            el('statHaftaCikis').innerHTML = (cikisT>0 ? '-' : '') + cikisT.toLocaleString('tr-TR',{maximumFractionDigits:0}) + ' &#8378;';
        if (el('statHaftaCikisSay'))
            el('statHaftaCikisSay').textContent = cikislar.length + ' sarf';

        const liste = document.getElementById('stokGecmisListe');
        if (!liste) return;
        if (!data.hareketler || data.hareketler.length === 0) {
            liste.innerHTML = '<div style="color:#9CA3AF; text-align:center; padding:24px; font-size:13px;">Henüz hareket kaydı yok.</div>';
            return;
        }
        liste.innerHTML = data.hareketler.map(h => _stokHareketHtml(h)).join('');
    } catch(e) { console.error('stokGecmisYukle hatası:', e); }
}

async function stokHareketSil(hareketId) {
  if (!confirm('Bu hareketi silmek istediğinizden emin misiniz?')) return;
  const token = localStorage.getItem('bai_token');
  const res = await fetch(`/stok-hareket/${hareketId}`, {
    method: 'DELETE',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token})
  });
  if (res.ok) {
    stokGecmisYukle();
    stokYukle(window._aktifSantiyeId ? parseInt(window._aktifSantiyeId) : null);
  } else {
    alert('Silinemedi');
  }
}

async function stokKaydet() {
    const token = localStorage.getItem('bai_token');
    const santiye_id = document.getElementById('stokSantiye')?.value
        || window._aktifSantiyeId
        || localStorage.getItem('bai_aktif_santiye')
        || null;
    const malzeme = document.getElementById('stokMalzemeInput').value.trim();
    const miktar = document.getElementById('stokMiktar').value;
    const birim = document.getElementById('stokBirim').value.trim();
    const tedarikci = document.getElementById('stokTedarikci').value;
    const fiyat = document.getElementById('stokFiyat').value;
    const notlar = document.getElementById('stokNotlar').value;
    const msg = document.getElementById('stokMsg');
    if (!santiye_id) { alert('Lütfen üstten bir şantiye seçin'); msg.innerHTML = '<span style="color:#e74c3c;">Şantiye seçin.</span>'; return; }
    if (!malzeme) { msg.innerHTML = '<span style="color:#e74c3c;">Malzeme seçin.</span>'; return; }
    if (!miktar) { msg.innerHTML = '<span style="color:#e74c3c;">Miktar girin.</span>'; return; }
    try {
        const res = await fetch('/stok-ekle', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, santiye_id: parseInt(santiye_id), malzeme, malzeme_ad: malzeme, tip: 'giris', miktar, birim, tedarikci, fiyat, notlar})
        });
        const data = await res.json();
        if (res.ok) {
            msg.innerHTML = '<span style="color:#2ecc71;">✓ ' + data.mesaj + '</span>';
            document.getElementById('stokMalzemeInput').value = '';
            document.getElementById('stokBirim').value = '';
            document.getElementById('stokMiktar').value = '';
            document.getElementById('stokTedarikci').value = '';
            document.getElementById('stokFiyat').value = '';
            document.getElementById('stokNotlar').value = '';
            stokYukle(santiye_id ? parseInt(santiye_id) : null);
            stokGecmisYukle();
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
    if (!confirm('Bu kaydı silmek istediğinizden emin misiniz')) return;
    try {
        await fetch(`/stok-sil/${id}?token=${token}`, {method: 'DELETE'});
        stokGecmisYukle();
        stokYukle();
    } catch(e) {}
}

function stokTabDegis(tab) {
  const girisForm = document.getElementById('stokGirisForm');
  const sarfForm = document.getElementById('stokSarfForm');
  const tabG = document.getElementById('tabGiris');
  const tabS = document.getElementById('tabSarf');
  if (!girisForm || !sarfForm) return;
  if (tab === 'giris') {
    girisForm.style.display = 'flex';
    sarfForm.style.display = 'none';
    if (tabG) { tabG.style.background='#E15A1F'; tabG.style.color='white'; }
    if (tabS) { tabS.style.background='#F8F9FA'; tabS.style.color='#6B7280'; }
  } else {
    girisForm.style.display = 'none';
    sarfForm.style.display = 'flex';
    if (tabS) { tabS.style.background='#374151'; tabS.style.color='white'; }
    if (tabG) { tabG.style.background='#F8F9FA'; tabG.style.color='#6B7280'; }
    if (typeof stokIsKalemleriYukle === 'function') stokIsKalemleriYukle();
  }
}

async function sarfKaydet() {
  const token = localStorage.getItem('bai_token');
  const santiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || null;
  const malzeme = document.getElementById('sarfMalzemeInput').value.trim();
  const miktar = parseFloat(document.getElementById('sarfMiktar').value);
  const birim = document.getElementById('sarfBirim').value.trim();
  const aciklama = document.getElementById('sarfAciklama').value.trim();
  const notlarRaw = document.getElementById('sarfNotlar').value.trim();
  const isKalemiSel = document.getElementById('sarfIsKalemi');
  const isKalemiId = isKalemiSel ? isKalemiSel.value : '';
  const isKalemiAd = isKalemiSel && isKalemiId ? isKalemiSel.options[isKalemiSel.selectedIndex].text : '';
  const msg = document.getElementById('sarfMsg');

  if (!malzeme) { if(msg) msg.innerHTML='<span style="color:#e74c3c;">Malzeme seçin.</span>'; else alert('Malzeme seçin'); return; }
  if (!miktar || miktar <= 0) { if(msg) msg.innerHTML='<span style="color:#e74c3c;">Geçerli miktar girin.</span>'; else alert('Geçerli miktar girin'); return; }

  const notlarParcalar = [];
  if (aciklama) notlarParcalar.push(aciklama);
  if (isKalemiAd) notlarParcalar.push(`İş Kalemi: ${isKalemiAd}`);
  if (notlarRaw) notlarParcalar.push(notlarRaw);
  const notlar = notlarParcalar.join(' | ');

  try {
    const res = await fetch('/stok-ekle', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({token, malzeme, malzeme_ad: malzeme, miktar, birim, tip: 'cikis', notlar, kaynak: 'sarf',
        santiye_id: santiyeId ? parseInt(santiyeId) : null,
        is_kalemi_id: isKalemiId ? parseInt(isKalemiId) : null})
    });
    const data = await res.json();
    if (res.ok) {
      if(msg) msg.innerHTML = '<span style="color:#16a34a;">✓ Sarf kaydedildi.</span>';
      document.getElementById('sarfMalzemeInput').value = '';
      document.getElementById('sarfBirim').value = '';
      document.getElementById('sarfMiktar').value = '';
      document.getElementById('sarfAciklama').value = '';
      document.getElementById('sarfNotlar').value = '';
      if(isKalemiSel) isKalemiSel.value = '';
      stokYukle(santiyeId ? parseInt(santiyeId) : null);
    } else {
      const detail = data.detail || 'Hata oluştu';
      if (detail.startsWith('PLAN_YETERSIZ:')) {
        planKilit(detail.split(':')[1] || 'stok');
      } else {
        if(msg) msg.innerHTML = `<span style="color:#e74c3c;">${detail}</span>`;
        else alert('❌ ' + detail);
      }
    }
  } catch(e) {
    if(msg) msg.innerHTML='<span style="color:#e74c3c;">Bağlantı hatası.</span>';
  }
}

async function esikKaydet() {
  const malzeme = document.getElementById('esikMalzeme').value;
  const minMiktar = parseFloat(document.getElementById('esikMinMiktar').value);
  const santiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || null;
  const token = localStorage.getItem('bai_token');

  if (!minMiktar || minMiktar < 0) {
    alert('Geçerli bir minimum miktar girin'); return;
  }

  const res = await fetch('/stok-esik-ayarla', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({token, malzeme, min_miktar: minMiktar, santiye_id: santiyeId ? parseInt(santiyeId) : null})
  });
  const data = await res.json();
  if (res.ok) {
    alert(`✅ ${malzeme} için minimum eşik ${minMiktar} olarak ayarlandı`);
    document.getElementById('esikMinMiktar').value = '';
    stokYukle(santiyeId ? parseInt(santiyeId) : null);
  } else {
    alert('❌ ' + (data.detail || 'Hata oluştu'));
  }
}

let _qrStream = null;
let _qrInterval = null;

async function qrBaslat() {
    const modal = document.getElementById('qrModal');
    const video = document.getElementById('qrVideo');
    const durum = document.getElementById('qrDurum');
    if (modal) modal.style.display = 'flex';
    if (durum) durum.textContent = 'Kamera başlatılıyor...';
    try {
        _qrStream = await navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment'}});
        video.srcObject = _qrStream;
        await video.play();
        if (durum) durum.textContent = 'QR kodu kameraya gösterin...';
        _qrInterval = setInterval(() => {
            if (!video || video.readyState !== video.HAVE_ENOUGH_DATA) return;
            const canvas = document.getElementById('qrCanvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            if (typeof jsQR === 'undefined') return;
            const code = jsQR(imageData.data, imageData.width, imageData.height);
            if (code) qrSonuc(code.data);
        }, 200);
    } catch(e) {
        if (durum) durum.textContent = 'Kamera erişimi reddedildi veya desteklenmiyor.';
    }
}

function qrSonuc(data) {
    qrIptal();
    if (data.startsWith('BAI_MALZEME:')) {
        const malzemeKod = data.replace('BAI_MALZEME:', '').trim().toLowerCase();
        const select = document.getElementById('stokMalzeme');
        if (select) select.value = malzemeKod;
        const sarfSelect = document.getElementById('sarfMalzeme');
        if (sarfSelect) sarfSelect.value = malzemeKod;
        const malzemeAd = malzemeKod.charAt(0).toUpperCase() + malzemeKod.slice(1);
        const msg = document.getElementById('sarfMsg') || document.getElementById('stokMsg');
        if (msg) msg.innerHTML = `<span style="color:#22C55E;">✅ ${malzemeAd} seçildi</span>`;
    } else {
        const notlar = document.getElementById('stokNotlar');
        if (notlar) notlar.value = data;
        const msg = document.getElementById('stokMsg');
        if (msg) msg.innerHTML = `<span style="color:#F59E0B;">QR okundu: ${data}</span>`;
    }
}

function qrIptal() {
    if (_qrInterval) { clearInterval(_qrInterval); _qrInterval = null; }
    if (_qrStream) { _qrStream.getTracks().forEach(t => t.stop()); _qrStream = null; }
    const modal = document.getElementById('qrModal');
    if (modal) modal.style.display = 'none';
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
            resBox.innerHTML = `<div style="color:#f59e0b; padding:16px;">?? "${komut.santiye_adi}" adında şantiye bulunamadı.</div>`;
            return;
        }
        const tip = komut.islem === 'cikar' ? 'cikis' : 'giris';
        const ekRes = await fetch('/stok-ekle', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, santiye_id: enIyi.id, malzeme: komut.malzeme, tip, miktar: komut.miktar, birim: komut.birim || '', notlar: 'AI komutu'})
        });
        if (ekRes.ok) {
            const islemAdi = tip === 'giris' ? 'eklendi' : 'd???ld?';
            resBox.innerHTML = `<div style="background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.3); border-radius:12px; padding:16px; color:#4ade80; font-weight:600;">? ${enIyi.ad} şantiyesine ${komut.miktar}${komut.birim ? ' '+komut.birim : ''} ${komut.malzeme} ${islemAdi}.</div>`;
            showToast(`${enIyi.ad}: ${komut.miktar} ${komut.malzeme} ${islemAdi}`, 'success');
        } else {
            resBox.innerHTML = `<div style="color:#ef4444; padding:16px;">âŒ Stok kaydedilemedi.</div>`;
        }
    } catch(e) {
        resBox.innerHTML = `<div style="color:#ef4444; padding:16px;">âŒ Hata: ${e.message}</div>`;
    }
}

// --- 🏠 DEPREM ANALİZİ ---
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
        attribution: '? OpenStreetMap',
        maxZoom: 18
    }).addTo(depremHaritaObj);
    depremHaritaObj.on('click', function(e) {
        const lat = e.latlng.lat.toFixed(4);
        const lon = e.latlng.lng.toFixed(4);
        document.getElementById('depremLat').value = lat;
        document.getElementById('depremLon').value = lon;
        document.getElementById('depremKonumMsg').innerHTML = `🏠 Seçilen konum: ${lat}, ${lon}`;
        if (depremMarker) depremHaritaObj.removeLayer(depremMarker);
        depremMarker = L.marker([lat, lon]).addTo(depremHaritaObj)
            .bindPopup(' Şantiye Konumu').openPopup();
    });
    depremSonYukle();
}

async function depremSonYukle() {
    try {
        const res = await fetch('/deprem-sonlat=39.0&lon=35.0&radius=800');
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
    msg.innerHTML = 'â³ Konum aranıyor...';
    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/searchq=${encodeURIComponent(adres+' Türkiye')}&format=json&limit=1`);
        const data = await res.json();
        if (data && data[0]) {
            const lat = parseFloat(data[0].lat).toFixed(4);
            const lon = parseFloat(data[0].lon).toFixed(4);
            document.getElementById('depremLat').value = lat;
            document.getElementById('depremLon').value = lon;
            msg.innerHTML = `? Konum bulundu: ${data[0].display_name.substring(0,60)}...`;
            depremHaritaObj.setView([lat, lon], 10);
            if (depremMarker) depremHaritaObj.removeLayer(depremMarker);
            depremMarker = L.marker([lat, lon]).addTo(depremHaritaObj)
                .bindPopup(' Şantiye Konumu').openPopup();
        } else {
            msg.innerHTML = 'âŒ Konum bulunamadı, koordinat girin.';
        }
    } catch(e) {
        msg.innerHTML = 'âŒ Konum arama hatası.';
    }
}

async function depremAnalizBaslat() {
    const token = localStorage.getItem('bai_token');
    const lat = parseFloat(document.getElementById('depremLat').value);
    const lon = parseFloat(document.getElementById('depremLon').value);
    const adres = document.getElementById('depremAdres').value;
    if (!lat || !lon) {
        document.getElementById('depremKonumMsg').innerHTML = 'âŒ Önce konum seçin veya koordinat girin.';
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
        document.getElementById('fayMesafe').textContent = fay.mesafe_km ? `${fay.mesafe_km} km uzakl?kta` : '-';
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
            `<div style="color:#fcd34d; font-size:0.85rem; padding:4px 0; border-bottom:1px solid rgba(245,158,11,0.1);">? ${o}</div>`
        ).join('');

        if (depremMarker) depremHaritaObj.removeLayer(depremMarker);
        depremMarker = L.marker([lat, lon], {
            icon: L.divIcon({
                html: `<div style="background:${skorRenk}; color:white; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:0.75rem; border:3px solid white; box-shadow:0 0 10px ${skorRenk};">${skor}</div>`,
                iconSize: [36,36], iconAnchor: [18,18]
            })
        }).addTo(depremHaritaObj).bindPopup(` Şantiye ? Risk: ${d.risk_seviyesi}`).openPopup();
        depremHaritaObj.setView([lat, lon], 9);

    } catch(e) {
        document.getElementById('depremLoading').style.display = 'none';
        document.getElementById('depremKonumMsg').innerHTML = `âŒ Hata: ${e.message}`;
    }
}

// ═══════════════════════════════════════════════════════════════
//   ŞANTİYELERİM ?? Premium Glassmorphism Dashboard
//     CartoDB Dark Matter ?? Chart.js ?? Mini-Harita Koordinat Seçici
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

// â"€â"€ MODAL AÇMA / KAPAMA â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
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

// â"€â"€ FORM MODAL â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function santiyeEkleModalAc(santiye) {
    const fm = document.getElementById('santiyeFormModal');
    if (!fm) return;
    fm.style.display = 'flex';
    document.getElementById('santiyeFormId').value        = santiye ? santiye.id : '';
    document.getElementById('santiyeFormBaslik').textContent = santiye ? 'Şantiye Düzenle' : 'Yeni Şantiye Ekle';
    document.getElementById('santiyeFormAd').value        = santiye ? santiye.ad : '';
    const _ilEl = document.getElementById('santiyeFormIl');
    if (_ilEl) _ilEl.value = santiye ? (santiye.sehir || '') : '';
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
    // Mini-haritayı başlat (100ms gecikme ?? DOM hazır olsun)
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
                <span>🏗</span><span style="max-width:120px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${f.name}</span>
            </div>`).join('');
    }
}

function santiyeSilOnay() {
    const id = document.getElementById('santiyeFormId').value;
    const ad = document.getElementById('santiyeFormAd').value || 'Bu şantiye';
    if (!id) return;
    // Custom onay UI ?? modal içinde confirm() çalışmayabilir
    const silBlok = document.getElementById('santiyeSilBlok');
    if (!silBlok) return;
    silBlok.innerHTML = `
        <div style="font-size:13px; font-weight:700; color:#DC2626; margin-bottom:8px;">?? Emin misiniz</div>
        <div style="font-size:12px; color:#64748B; margin-bottom:12px;">"${ad}" kalıcı olarak silinecek.</div>
        <div style="display:flex; gap:8px;">
            <button onclick="santiyeSilYap(${id},'${ad.replace(/'/g,"'")}')"
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
                🚀 Şantiyeyi Sil
            </button>
        </div>`;
}

async function santiyeSilYap(id, ad) {
    const token = localStorage.getItem('bai_token');
    const silBlok = document.getElementById('santiyeSilBlok');
    if (silBlok) silBlok.innerHTML = '<div style="font-size:13px;color:#64748B;text-align:center;padding:8px;">â³ Siliniyor...</div>';
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
    if (inp) inp.value = '';
    const alan = document.getElementById('santiyeFotoAlani');
    if (alan) alan.style.borderStyle = 'dashed';
}

// â"€â"€ ANA LİSTE HARİTASI ?? CartoDB Dark Matter â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function santiyeHaritaBaslat() {
    if (santiyeHaritaObj) { santiyeHaritaObj.invalidateSize(); return; }
    santiyeHaritaObj = L.map('santiyeHarita', { zoomControl: true, attributionControl: false })
        .setView([39.0, 35.0], 6);
    L.tileLayer(_CARTO_DARK, { attribution: _CARTO_ATTR, maxZoom: 19, subdomains: 'abcd' })
        .addTo(santiyeHaritaObj);
}

// â"€â"€ FORM MİNİ-HARİTASI ?? Koordinat Seçici â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
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

// â"€â"€ VERİ YÜKLE â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
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

// â"€â"€ KPI KARTLARI â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function santiyeOzetGoster() {
    const toplam     = santiyeVerisi.length;
    const iyi        = santiyeVerisi.filter(s => s.durum === 'iyi').length;
    const dikkat     = santiyeVerisi.filter(s => s.durum === 'dikkat').length;
    const sorun      = santiyeVerisi.filter(s => s.durum === 'sorun').length;
    const toplamIsci = santiyeVerisi.reduce((a, s) => a + (s.isci_sayisi || 0), 0);

    const altBaslik = document.getElementById('santiyeAltBaslik');
    if (altBaslik) altBaslik.textContent = `${toplam} aktif proje ?? Gerçek zamanlı izleme`;

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

// â"€â"€ PROJE KARTLARI â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function santiyeKartlarGoster() {
    const el = document.getElementById('santiyeKartlar');
    if (!el) return;

    if (santiyeVerisi.length === 0) {
        el.innerHTML = `
            <div style="grid-column:1/-1; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:60px 20px; gap:16px; color:#475569;">
                <div style="font-size:56px;margin-bottom:12px;"></div>
                <div style="font-size:15px; font-weight:600; color:#64748b;">Henüz şantiye eklenmedi</div>
                <div style="font-size:12.5px; color:#475569;">Projenizi sisteme ekleyerek takibe başlayın</div>
                <button onclick="santiyeEkleModalAc(null)" style="margin-top:4px; background:linear-gradient(135deg,rgba(249,115,22,0.20),rgba(249,115,22,0.10)); border:1px solid rgba(249,115,22,0.35); color:#fb923c; padding:10px 22px; border-radius:10px; cursor:pointer; font-weight:700; font-size:13px; font-family:inherit; transition:all 0.2s;">İlk Şantiyeni Ekle ?</button>
            </div>`;
        return;
    }

    const durumCfg = {
        iyi:    { renk: '#22c55e', badge: '🟢 İyi',     borderTop: '#22c55e' },
        dikkat: { renk: '#f59e0b', badge: '🟡 Dikkat',  borderTop: '#f59e0b' },
        sorun:  { renk: '#ef4444', badge: '🔴 Kritik',  borderTop: '#ef4444' },
    };

    el.innerHTML = santiyeVerisi.map(s => {
        const cfg = durumCfg[s.durum] || {renk:'#94a3b8', badge:'Değerlendirilmedi', borderTop:'#94a3b8'};
        const pct = Math.min(100, Math.max(0, s.ilerleme || 0));
        // Progress bar rengi
        const barRenk = pct < 31 ? 'linear-gradient(90deg,#ef4444,#f87171)'
                      : pct < 71 ? 'linear-gradient(90deg,#f59e0b,#fbbf24)'
                      :             'linear-gradient(90deg,#22c55e,#4ade80)';
        // Güvenli JSON serialize (onclick için)
        const safeJson = JSON.stringify(s).replace(/[\r\n]/g,'').replace(/'/g,"'").replace(/"/g,'&quot;');
        return `
        <div class="s-kart" style="backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); border-top:2px solid ${cfg.borderTop};">
            <!-- Başlık + Durum Badge -->
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; margin-bottom:10px;">
                <div style="min-width:0;">
                    <div style="font-weight:700; font-size:14.5px; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${s.ad}</div>
                    <div style="font-size:11.5px; color:#64748b; margin-top:3px; display:flex; align-items:center; gap:4px;"><span>🏠</span><span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${s.konum || '?'}</span></div>
                </div>
                <span style="flex-shrink:0; font-size:11px; font-weight:700; padding:3px 9px; border-radius:20px; background:${cfg.renk}1a; border:1px solid ${cfg.renk}44; color:${cfg.renk}; white-space:nowrap;">${cfg.badge}</span>
            </div>
            <!-- İlerleme Bar -->
            <div style="margin-bottom:4px; display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:10.5px; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">İlerleme</span>
                <span style="font-size:12px; font-weight:700; color:#fff;" title="${s.ilerleme_yontemi || 'İlerleme için dayanak yok'}">${s.ilerleme == null ? 'Veri yok' : pct + '%'}</span>
            </div>
            <div style="background:rgba(255,255,255,0.06); border-radius:6px; height:5px; margin-bottom:12px; overflow:hidden;">
                <div class="s-progress-bar" style="background:${barRenk}; height:100%; width:0%; border-radius:6px; transition:width 1.1s cubic-bezier(0.4,0,0.2,1);" data-target="${pct}"></div>
            </div>
            <!-- Meta bilgi -->
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px; font-size:11.5px; color:#64748b;">
                <span style="display:flex; align-items:center; gap:4px;">👷 <b style="color:#94a3b8;">${s.isci_sayisi || 0}</b> kişi</span>
                <span style="display:flex; align-items:center; gap:4px;">İSG: <span style="color:#94a3b8;">${s.isg_durumu || 'Değerlendirilmedi'}</span></span>
            </div>
            <!-- Footer -->
            <div style="border-top:1px solid rgba(255,255,255,0.05); padding-top:10px; display:flex; gap:8px;">
                <button onclick="santiyeEkleModalAc(${safeJson})"
                    style="flex:1; background:rgba(99,102,241,0.10); border:1px solid rgba(99,102,241,0.22); color:#818cf8; padding:7px; border-radius:8px; cursor:pointer; font-size:12px; font-weight:600; transition:all 0.18s; font-family:inherit;"
                    onmouseover="this.style.background='rgba(99,102,241,0.22)'" onmouseout="this.style.background='rgba(99,102,241,0.10)'">âœï¸ Düzenle</button>
                <button onclick="santiyeSilOnay(${s.id},'${(s.ad||'').replace(/'/g,"'")}')"
                    style="flex:0 0 auto; background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.18); color:#f87171; padding:7px 12px; border-radius:8px; cursor:pointer; font-size:12px; transition:all 0.18s;"
                    onmouseover="this.style.background='rgba(239,68,68,0.20)'" onmouseout="this.style.background='rgba(239,68,68,0.08)'">🗑¸</button>
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

// â"€â"€ CHART.JS ?? İlerleme Bar + İşçi Doughnut + Durum Özeti â"€â"€â"€
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
         ? santiyeVerisi.map(s => s.ad.length > 16 ? s.ad.slice(0,16)+'?' : s.ad)
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

    // â"€â"€ Grafik 1: Yatay Bar â"€â"€
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

    // â"€â"€ Grafik 2: Doughnut â"€â"€
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

    // â"€â"€ Grafik 3: Durum Özeti â"€â"€
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

// â"€â"€ HARİTA MARKERLARI â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
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
                html: `<div style="background:${renk}; color:white; border-radius:50%; width:30px; height:30px; display:flex; align-items:center; justify-content:center; font-size:13px; border:2.5px solid rgba(255,255,255,0.85); box-shadow:0 0 12px ${renk}88;"></div>`,
                iconSize: [30, 30], iconAnchor: [15, 15], className: ''
            })
        }).addTo(santiyeHaritaObj)
        .bindPopup(`<div style="font-family:system-ui;min-width:160px;"><b>${s.ad}</b><br><small>🏠 ${s.konum}</small><br>İlerleme: <b>${s.ilerleme||0}%</b><br>👷 ${s.isci_sayisi||0} kişi</div>`);
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

// â"€â"€ KAYDET â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
async function santiyeKaydet() {
    const token = localStorage.getItem('bai_token');
    const id    = document.getElementById('santiyeFormId').value;
    const msg   = document.getElementById('santiyeFormMsg');
    const btn   = document.querySelector('#santiyeFormModal button[onclick="santiyeKaydet()"]');

    const body = {
        ad:          document.getElementById('santiyeFormAd').value.trim(),
        sehir:       (document.getElementById('santiyeFormIl')?.value || '').trim() || null,
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

    if (!body.ad) {
        msg.innerHTML = '<div style="color:#f87171; font-size:12px;">⚠️ Şantiye adı zorunludur.</div>';
        return;
    }
    if (btn) { btn.textContent = 'â³ Kaydediliyor...'; btn.disabled = true; }

    try {
        const url = id ? `/santiye-guncelle/${id}` : '/santiye-ekle';
        const res  = await fetch(url, {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        const data = await res.json();

        if (res.ok) {
            msg.innerHTML = '<div style="color:#4ade80; font-size:12px;">? Kaydedildi!</div>';

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
                        showToast('Dosyalar AI belleğine yüklendi ?', 'success');
                    } catch(_) {
                        showToast('Dosya yüklemesi başarısız.', 'error');
                    }
                }
            }

            if (data.id && !id) localStorage.setItem('bai_aktif_santiye', String(data.id));
            santiyeFormKapat();
            await Promise.all([santiyeYukle(), santiyePageYukle(), globalSantiyeSeciciDoldur()]);
        } else {
            const detail = data.detail || 'Hata oluştu.';
            if (detail.startsWith('PLAN_YETERSIZ:')) {
                santiyeFormKapat();
                planKilit(detail.split(':')[1] || 'santiye');
            } else {
                msg.innerHTML = `<div style="color:#f87171; font-size:12px;">âŒ ${detail}</div>`;
            }
        }
    } catch(e) {
        msg.innerHTML = '<div style="color:#f87171; font-size:12px;">âŒ Bağlantı hatası.</div>';
    } finally {
        if (btn) { btn.textContent = '💾 Şantiyeyi Kaydet'; btn.disabled = false; }
    }
}

// â"€â"€ SİL â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

async function fiyatlarYukle() {
    const sehir = document.getElementById('citySelect').value || 'genel';
    try {
        const res = await fetch(`/fiyatlarsehir=${sehir}`);
        const data = await res.json();

        const uyariDiv = document.getElementById('uyarilar');
        if (data.uyarilar && data.uyarilar.length > 0) {
            uyariDiv.innerHTML = data.uyarilar.map(u => {
                const artti = parseFloat(u.degisim) > 0;
                return `<div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:10px; padding:10px 14px; margin-bottom:8px; color:#fca5a5; font-size:0.85rem; display:flex; align-items:center; gap:8px;">
                    <span>${artti ? '🌍' : '🏠‰'}</span>
                    <span><b>${u.malzeme}</b> bu hafta <b>${u.degisim}%</b> ${artti ? 'arttı' : 'düştü'} ? ${u.tarih}</span>
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
                    <span style="font-size:1.3rem;">${malzemeIkon[m] || '🏠'}</span>
                    <span style="color:#555; font-size:0.72rem;">${f.tarih || '-'}</span>
                </div>
                <div style="color:white; font-weight:700; font-size:0.9rem; margin-bottom:2px;">${malzemeAd[m]}</div>
                <div style="color:var(--primary); font-size:1.2rem; font-weight:800;">${f.fiyat ? '₺'+f.fiyat : '?'}</div>
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
    const malzeme = document.getElementById('fiyatMalzemeSelect').value;
    const fiyat = document.getElementById('fiyatDeger').value;
    const sehir = document.getElementById('fiyatSehir').value;
    const msg = document.getElementById('fiyatMsg');

    if (!fiyat) { msg.innerHTML = '<span style="color:#e74c3c;">Fiyat girin.</span>'; return; }

    const birimler = {beton:'m³', demir:'ton', celik_hasir:'ton', cimento:'çuval', kum:'ton', tugla:'adet', gazbeton:'m³'};
    try {
        const res = await fetch('/fiyat-gir', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({token, malzeme, fiyat, birim: birimler[malzeme], sehir})
        });
        const data = await res.json();
        if (res.ok) {
            msg.innerHTML = '<span style="color:#2ecc71;">? ' + data.mesaj + '</span>';
            document.getElementById('fiyatDeger').value = '';
            fiyatlarYukle();
        } else {
            msg.innerHTML = '<span style="color:#e74c3c;">' + (data.detail || 'Hata.') + '</span>';
        }
    } catch(e) {
        msg.innerHTML = '<span style="color:#e74c3c;">Bağlantı hatası.</span>';
    }
}

// --- 🏠™ TEMA ---
function temaToggle() {
    document.body.classList.toggle('light-mode');
    localStorage.setItem('tema', document.body.classList.contains('light-mode') ? 'light' : 'dark');
}

const kayitliTema = localStorage.getItem('tema');
if (kayitliTema === 'light') document.body.classList.add('light-mode');

// --- 🏠 HAFTALIK RAPOR ---
async function haftalikRaporIndir() {
    const token = localStorage.getItem('bai_token');
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'Türkiye';
    const resBox = document.getElementById('result');
    resBox.innerHTML = '<div style="text-align:center; padding:20px;"><div style="font-size:2rem;">🏠</div><div style="color:#aaa; margin-top:8px;">Haftalık rapor hazırlanıyor...<br><small>AI analiz yapıyor, PDF oluşturuluyor...</small></div></div>';
    try {
        const res = await fetch('/haftalik-rapor-olustur', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token, sehir})
        });
        if (!res.ok) {
            const err = await res.json();
            resBox.innerHTML = `<div style="color:#e74c3c;">âŒ ${err.detail || 'Rapor oluşturulamadı.'}</div>`;
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
        resBox.innerHTML = '<div style="text-align:center; padding:20px;"><div style="font-size:2rem;">?</div><div style="color:#2ecc71; margin-top:8px; font-weight:700;">Haftalık rapor indirildi!</div></div>';
    } catch(e) {
        resBox.innerHTML = `<div style="color:#e74c3c;">âŒ Hata: ${e.message}</div>`;
    }
}

// --- SAYFA YÜKLENME ---
document.addEventListener('DOMContentLoaded', async () => {
    sesYukle();
    // Günlük rapor tarih alanını bugünle doldur
    const grTarih = document.getElementById('grTarih');
    if (grTarih) grTarih.value = new Date().toISOString().split('T')[0];

    // â"€â"€ Google OAuth callback handler â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
    const urlParams = new URLSearchParams(window.location.search);
    const fragmentParams = new URLSearchParams(window.location.hash.slice(1));
    const oauthToken = fragmentParams.get('oauth_token') || urlParams.get('oauth_token');
    const oauthError = urlParams.get('oauth_error');

    if (oauthToken) {
        // OAuth başarılı: token'ı kaydet ve dashboard'ı göster
        localStorage.setItem('bai_token', oauthToken);
        localStorage.setItem('bai_token_expiry', Date.now() + 7 * 24 * 60 * 60 * 1000);
        window.history.replaceState({}, document.title, '/app');
        showToast('Google ile giriş başarılı! Hoş geldiniz.', 'success');
        // Dashboard'ı göster (auth overlay'i kapat)
        const overlay = document.getElementById('auth-overlay');
        const app = document.getElementById('mainApp');
        const nav = document.getElementById('navSidebar');
        const header = document.getElementById('topHeader');
        if (overlay) overlay.style.display = 'none';
        if (app) app.style.display = 'block';
        if (nav) nav.style.display = 'flex';
        if (header) header.style.display = 'flex';
        // Token ile kullanıcı bilgilerini yükle
        try {
            const resp = await fetch('/beni-tanı', { headers: { 'Authorization': 'Bearer ' + oauthToken } });
            if (resp.ok) {
                const userData = await resp.json();
                aktifKullanici = { ...userData };
                applyServerUserProfile(userData);
                const rol = userData.role || localStorage.getItem('bai_rol');
                if (rol) {
                    localStorage.setItem('bai_rol', rol);
                    navSidebarGuncelle(rol);
                    routeInitialPath();
                    if (isContractorRole(rol)) setTimeout(() => loadContractorDashboard(true), 0);
                    else if (isEngineerRole(rol)) setTimeout(() => loadEngineerDashboard(true), 0);
                } else {
                    rolEkraniniGoster();
                }
                fiyatAlertBadgeGuncelle();
                setInterval(fiyatAlertBadgeGuncelle, 5 * 60 * 1000);
                dilDegistir(aktifDil);
                havaGuncelle();
                kullanımDurumuGoster();
                return;
            }
        } catch(e) { console.warn('OAuth profile load error', e); }
        return;
    } else if (oauthError) {
        const msgs = {
            cancelled:      'Google girişi iptal edildi.',
            token_failed:   'Google doğrulama başarısız. Tekrar deneyin.',
            redirect_uri_mismatch: 'Google yönlendirme adresi eşleşmiyor. Google Cloud Console redirect URI ayarını kontrol edin.',
            invalid_client: 'Google OAuth client bilgileri geçersiz.',
            invalid_grant: 'Google doğrulama kodu geçersiz veya süresi dolmuş. Tekrar deneyin.',
            missing_client_secret: 'Google OAuth client secret eksik.',
            oauth_token_exchange_failed: 'Google token değişimi başarısız. Sunucu loglarını kontrol edin.',
            userinfo_failed:'Google bilgileri alınamadı.',
            no_email:       'Google hesabından e-posta alınamadı.',
            email_not_verified: 'Google e-posta adresi doğrulanmamış.',
            account_link_required: 'Bu e-posta ile yerel hesabınız var. Şifrenizle giriş yapın; Google hesabı otomatik bağlanmaz.',
        };
        showToast(msgs[oauthError] || 'Google girişi başarısız.', 'error');
        window.history.replaceState({}, document.title, '/app');
    }
    // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

    // 🔐 Otomatik giriş ?? token varsa kontrol et
    const token = localStorage.getItem('bai_token');
    if (token) {
        try {
            const res = await fetch('/beni-tanı', { headers: { 'Authorization': 'Bearer ' + token } });
            if (res.ok) {
                const data = await res.json();
                aktifKullanici = data;
                applyServerUserProfile(data);
                document.getElementById('auth-overlay').style.display = 'none';
                document.getElementById('mainApp').style.display = 'block';
                document.getElementById('navSidebar').style.display = 'flex';
                document.getElementById('topHeader').style.display = 'flex';
                dilDegistir(aktifDil);
                havaGuncelle();
                kullanımDurumuGoster();
                const kayitliRol = data.role || localStorage.getItem('bai_rol');
                if (kayitliRol) {
                    localStorage.setItem('bai_rol', kayitliRol);
                    navSidebarGuncelle(kayitliRol);
                    routeInitialPath();
                    if (isContractorRole(kayitliRol)) setTimeout(() => loadContractorDashboard(true), 0);
                    else if (isEngineerRole(kayitliRol)) setTimeout(() => loadEngineerDashboard(true), 0);
                    else rolEkraniniGoster();
                } else {
                    rolEkraniniGoster();
                }
                fiyatAlertBadgeGuncelle();
                setInterval(fiyatAlertBadgeGuncelle, 5 * 60 * 1000);
                return;
            } else {
                localStorage.removeItem('bai_token');
                localStorage.removeItem('bai_user');
            }
        } catch(e) {
            // Network hatası (offline/PWA) ? token geçerliyse uygulamayı göster
            const expiry = localStorage.getItem('bai_token_expiry');
            if (expiry && Date.now() < parseInt(expiry)) {
                const cachedUser = localStorage.getItem('bai_user');
                if (cachedUser) {
                    aktifKullanici = JSON.parse(cachedUser);
                    updateSidebarOrganizationName(aktifKullanici);
                }
                document.getElementById('auth-overlay').style.display = 'none';
                document.getElementById('mainApp').style.display = 'block';
                document.getElementById('navSidebar').style.display = 'flex';
                document.getElementById('topHeader').style.display = 'flex';
                dilDegistir(aktifDil);
                const kayitliRol = localStorage.getItem('bai_rol');
                if (kayitliRol) { navSidebarGuncelle(kayitliRol); routeInitialPath(); }
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
    info:    { bg: 'rgba(56,189,248,0.15)',  border: 'rgba(56,189,248,0.4)',  icon: 'â„¹ï¸' },
    warning: { bg: 'rgba(249,115,22,0.15)',  border: 'rgba(249,115,22,0.5)',  icon: '??' },
    success: { bg: 'rgba(34,197,94,0.15)',   border: 'rgba(34,197,94,0.4)',   icon: '?' },
    error:   { bg: 'rgba(239,68,68,0.15)',   border: 'rgba(239,68,68,0.4)',   icon: 'âŒ' },
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
    <button onclick="this.parentElement.remove()" style="background:none;border:none;color:#aaa;cursor:pointer;font-size:16px;margin-left:auto;padding:0 0 0 10px;">âœ•</button>`;

  const style = document.createElement('style');
  style.textContent = '@keyframes toastIn{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}';
  document.head.appendChild(style);
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

// Legacy shim ?? yeni dashboard'a yönlendirir
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
    btn.textContent = '? Tamam';
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
  const sehir = document.getElementById('citySelect').value || 'Sivas';
  const satirlar = document.getElementById('gv-hava-satirlar');
  const riskEl = document.getElementById('gv-hava-risk');
  const riskLabel = document.getElementById('gv-risk-label');
  const riskText = document.getElementById('gv-risk-text');
  const onerisiText = document.getElementById('gv-ai-onerisi-text');
  if (!satirlar) return;

  fetch('/havasehir=' + sehir)
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
        riskSeviye = 'YÜKSEK'; riskRenk = '#DC2626'; riskBg = '#FEF2F2'; riskIkon = 'â›"';
        riskAciklama = ruzgar >= 30 ? 'Kuvvetli rüzgar ? Vinç operasyonları durdurulmalı!' : 'Don riski ?? Beton dökümü tehlikeli!';
      } else if (ruzgar >= 15 || nem >= 90 || durum.includes('yağmur') || durum.includes('rain') || temp <= 5) {
        riskSeviye = 'ORTA'; riskRenk = '#D97706'; riskBg = '#FFFBEB'; riskIkon = '??';
        riskAciklama = 'Dikkat edilmesi gereken hava koşulları var. Yüksekte çalışmada önlem alın.';
      }
      if (riskEl) riskEl.style.background = riskBg;
      if (riskLabel) { riskLabel.textContent = riskSeviye + ' RİSK'; riskLabel.style.color = riskRenk; }
      if (riskText) riskText.textContent = riskAciklama;

      // Tahmin tablosu (bugün + 4 gün simüle)
      const gunler = ['Bugün', 'Yarın', '2 Gün', '3 Gün', '5 Gün'];
      const ikonlar = durum.includes('yağmur') || durum.includes('rain') ? ['🌧','🌧','?','â˜€ï¸','â˜€ï¸'] :
                      ruzgar >= 15 ? ['🌬','?','â˜€ï¸','â˜€ï¸','?'] : ['â˜€ï¸','â˜€ï¸','?','🌧','â˜€ï¸'];
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
          <td style="padding:7px 4px; text-align:center; color:#0F172A;">${Math.round(temp - i * 2 + i)}?C</td>
          <td style="padding:7px 4px; text-align:center; color:#64748B;">${Math.round(ruzgar + (i % 3) - 1)} km/h</td>
          <td style="padding:7px 4px; color:${uyarilar[i] === 'Normal' ? '#16A34A' : '#D97706'}; font-size:0.75rem;">${uyarilar[i]}</td>
        </tr>
      `).join('');

      // AI Önerisi
      let oneri = 'Hava koşulları çalışma için uygun. Beton dökümü ve yüksek irtifa çalışmalarına devam edilebilir.';
      if (riskSeviye === 'YÜKSEK') oneri = 'Bugün yüksek rüzgar ?? vinç ve iskele çalışmaları durdurulmalı. İç mekan işlerine odaklanın.';
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
    div.innerHTML = `<div style="color:#94A3B8; font-size:0.72rem;">${tarih}</div><div style="color:#0F172A; font-weight:600; margin-top:2px;">${yeniOlay.tur} ? <span style="color:#64748B; font-weight:400;">${aciklama.substring(0,60)}${aciklama.length > 60 ? '...' : ''}</span></div><div style="color:#D97706; font-size:0.7rem; margin-top:3px;">${yeniOlay.durum}</div>`;
    liste.insertBefore(div, liste.firstChild);
  }

  document.getElementById('olayAciklama').value = '';
  document.getElementById('olayFotoOnizleme').innerHTML = '🏠';
  if (msg) msg.innerHTML = '<span style="color:#16A34A;">? Olay kaydedildi.</span>';
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
  const _apuOwner = (()=>{const _u=JSON.parse(localStorage.getItem('bai_user')||'{}');return _u.is_owner===true||_u.is_admin===true;})();
  liste.innerHTML = _acilPersonelListesi.map((p, i) => `
    <div style="display:flex; align-items:center; gap:8px; padding:8px 10px; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px;">
      <span style="font-size:1rem;">👷</span>
      <div style="flex:1; font-size:0.8rem;">
        <div style="color:#0F172A; font-weight:600;">${p.ad}</div>
        <div style="color:#64748B;">${p.tel}</div>
      </div>
      ${_apuOwner ? `<button onclick="_acilPersonelSil(${i})" style="background:#FEF2F2; border:1px solid #FECACA; color:#DC2626; border-radius:6px; padding:2px 8px; font-size:0.72rem; cursor:pointer;">Sil</button>` : ''}
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
  const nokta = document.getElementById('toplanmaNoktasi').value;
  if (!nokta) { showToast('Toplanma noktası boş olamaz.', 'warning'); return; }
  localStorage.setItem('toplanma_noktasi', nokta);
  showToast('🏠 Toplanma noktası kaydedildi.', 'success');
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
// AI OMNI-COMMAND BAR ?? Yeni Fonksiyonlar
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
      <span style="color:#6366f1;font-size:12px;">?</span> ${cmd}
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
      <span style="color:#6366f1;flex-shrink:0;margin-top:2px;">âœ¦</span>
      <div style="flex:1;">
        <span style="font-size:11px;color:#94A3B8;margin-right:6px;">"${savedQuery}" ?</span>
        <span style="font-size:13px;color:#1E293B;line-height:1.6;">${cevap}</span>
      </div>
      <button onclick="aiResultKapat()" style="background:none;border:none;cursor:pointer;color:#94A3B8;font-size:14px;flex-shrink:0;">âœ•</button>
    </div>`;
  } catch (err) {
    content.innerHTML = `<span style="color:rgba(239,68,68,0.8);font-size:13px;">? Bağlantı hatası. Lütfen tekrar deneyin.</span>`;
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

// Saha Günlüğü ? /rapor_listesi son 5 kayıt
let _engineerDashboardLoading = false;
let _engineerDashboardLoaded = false;
let _engineerDashboardSnapshot = null;
let _engineerDecisionItems = [];
let _engineerFocusedDecisionId = null;
let _engineerSelectedDecisionIds = new Set();

function engineerEscapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function engineerGetField(obj, keys, fallback = '') {
  if (!obj || typeof obj !== 'object') return fallback;
  for (const key of keys) {
    const value = obj[key];
    if (value !== undefined && value !== null && value !== '') return value;
  }
  return fallback;
}

function engineerParseDate(value) {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

function engineerFormatDate(value) {
  const parsed = engineerParseDate(value);
  if (!parsed) return value ? String(value) : 'Zaman bilgisi yok';
  return parsed.toLocaleString('tr-TR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function engineerSortValue(value) {
  const parsed = engineerParseDate(value);
  return parsed ? parsed.getTime() : 0;
}

function engineerIsUnlinkedEvidence(item) {
  if (!item || typeof item !== 'object') return false;
  if (typeof item.is_unlinked === 'boolean') return item.is_unlinked;
  if (typeof item.unlinked === 'boolean') return item.unlinked;
  if (typeof item.is_linked === 'boolean') return !item.is_linked;
  if (typeof item.linked === 'boolean') return !item.linked;
  if (typeof item.report_linked === 'boolean') return !item.report_linked;
  if (item.report_id || item.rapor_id || item.linked_report_id || item.report_uuid) return false;
  return true;
}

function engineerAlertTone(alert) {
  const raw = String(engineerGetField(alert, ['severity', 'seviye', 'status', 'durum'], 'info')).toLowerCase();
  if (raw.includes('kritik') || raw.includes('critical') || raw.includes('high')) return 'danger';
  if (raw.includes('uyari') || raw.includes('warning') || raw.includes('medium')) return 'warning';
  if (raw.includes('tamam') || raw.includes('resolved') || raw.includes('ok')) return 'success';
  return 'info';
}

function engineerAlertLabel(alert) {
  const raw = engineerGetField(alert, ['status_label', 'badge', 'severity_label', 'seviye_label'], '');
  if (raw) return raw;
  const tone = engineerAlertTone(alert);
  if (tone === 'danger') return 'Kritik';
  if (tone === 'warning') return 'Uyarı';
  if (tone === 'success') return 'Tamam';
  return 'Bilgi';
}

function engineerLoopIcon(kind) {
  if (kind === 'alert') {
    return `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
        <path d="M12 9v4"></path>
        <path d="M12 17h.01"></path>
        <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
      </svg>`;
  }
  return `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
      <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"></path>
      <circle cx="12" cy="13" r="3"></circle>
    </svg>`;
}

function engineerEvidencePlaceholder() {
  return `
    <div class="engineer-evidence-thumb is-placeholder">
      <div class="engineer-evidence-thumb__placeholder">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"></path>
          <circle cx="12" cy="13" r="3"></circle>
        </svg>
        <span>Görsel yok</span>
      </div>
    </div>`;
}

function engineerSetStat(cardId, valueId, count) {
  const card = document.getElementById(cardId);
  const value = document.getElementById(valueId);
  const safeCount = Number.isFinite(Number(count)) ? Number(count) : 0;
  if (value) value.textContent = String(safeCount);
  if (card) card.setAttribute('data-tone', safeCount > 0 ? 'warning' : 'success');
}

function engineerBuildDecisionSummary(item) {
  if (!item) return 'AI saha kaydi hazir.';
  const parts = [];
  if (item.zone) parts.push(`${item.zone} noktasinda`);
  if (item.kind === 'evidence') {
    if (item.material) parts.push(`${item.material} tespit edildi`);
    else if (item.plate) parts.push(`${item.plate} plakali kayit inceleniyor`);
    else parts.push('gorsel inceleme bekliyor');
  } else {
    if (item.material) parts.push(`${item.material} hareketi izlendi`);
    if (item.deltaLabel) parts.push(`degisim ${item.deltaLabel}`);
  }
  if (item.timeLabel) parts.push(`saat ${item.timeLabel}`);
  return parts.filter(Boolean).join(', ') || item.aiSummary || 'AI saha kaydi hazir.';
}

function engineerInferDecisionCategory(item) {
  // MalzemeUyari items (kind='alert') are stock/material alerts ?? always Stok
  if (item.kind === 'alert') return 'Stok';
  const text = String([
    item.title,
    item.material,
    item.zone,
    item.aiSummary
  ].filter(Boolean).join(' ')).toLowerCase();
  if (/isg|baret|kask|guvenlik|risk|ihlal|ppe|helmet|safety/.test(text)) return 'ISG';
  if (/beton|demir|stok|malzeme|irsaliye|mikser|cement|c30/.test(text)) return 'Stok';
  return 'Rapor';
}

function engineerUpdateBatchBar() {
  const statusEl = document.getElementById('engineerBatchStatus');
  const button = document.getElementById('engineerBatchApproveBtn');
  const selectedCount = _engineerSelectedDecisionIds.size;
  if (statusEl) statusEl.textContent = `${selectedCount} kart secili`;
  if (button) button.disabled = selectedCount === 0;
}

function engineerUpdateFocusMode() {
  const cards = document.querySelectorAll('.engineer-action-card');
  cards.forEach((card) => {
    const isFocused = card.getAttribute('data-card-id') === _engineerFocusedDecisionId;
    card.classList.toggle('is-focused', !!_engineerFocusedDecisionId && isFocused);
    card.classList.toggle('is-dimmed', !!_engineerFocusedDecisionId && !isFocused);
  });
}

function engineerRenderOpenLoops() {
  // Replaced by kararTerminalRenderListe
}

function engineerRenderEvidenceGrid(items) {
  kararTerminalRenderListe(items);
}

// Capitalize each word with Turkish locale so "i" ?? "İ" not "I"
function kararTerminalCapTitle(str) {
  if (!str) return '';
  return str.trim().split(/\s+/).map((w) =>
    w.charAt(0).toLocaleUpperCase('tr-TR') + w.slice(1)
  ).join(' ');
}

function kararTerminalUpdateBadge(count) {
  const badge = document.getElementById('kararTerminalBadge');
  if (!badge) return;
  if (count > 0) {
    badge.textContent = `${count} bekliyor`;
    badge.style.display = '';
  } else {
    badge.style.display = 'none';
  }
}

function engineerFocusDecision(id) {
  _engineerFocusedDecisionId = id;
  engineerUpdateFocusMode();
  engineerRenderSecretaryState(engineerFindDecisionItem(id));
}

function engineerToggleDecisionSelection(id, checked) {
  if (checked) _engineerSelectedDecisionIds.add(id);
  else _engineerSelectedDecisionIds.delete(id);
  engineerUpdateBatchBar();
}

async function engineerBulkApproveSelected() {
  const selectedIds = Array.from(_engineerSelectedDecisionIds);
  if (!selectedIds.length) return;
  const buckets = { ISG: 0, Stok: 0, Operasyon: 0 };
  for (const id of selectedIds) {
    const item = engineerFindDecisionItem(id);
    if (item) buckets[item.category] = (buckets[item.category] || 0) + 1;
    await engineerProcessDecision(id, 'approve', true);
  }
  _engineerSelectedDecisionIds = new Set();
  engineerUpdateBatchBar();
  const summary = Object.entries(buckets)
    .filter(([, count]) => count > 0)
    .map(([label, count]) => `${count} ${label}`)
    .join(', ');
  engineerRenderSecretaryState(
    engineerFindDecisionItem(_engineerFocusedDecisionId),
    `Hizli muhur tamamlandi. Secilen olaylar gunluk raporda su basliklara dagitildi: ${summary || 'Operasyon'}.`
  );
  if (typeof showToast === 'function') showToast('Toplu onay tamamlandi.', 'success');
}

function engineerAssistantSetResponse(content, state = 'content') {
  const box = document.getElementById('engineerAssistantResponse');
  if (!box) return;
  box.classList.remove('is-empty', 'is-loading');
  if (state === 'empty') {
    box.classList.add('is-empty');
    box.textContent = content || '';
    return;
  }
  if (state === 'loading') {
    box.classList.add('is-loading');
    box.textContent = content || 'Teknik sekreter taslagi isliyor...';
    return;
  }
  box.innerHTML = content;
}

function engineerAssistantUseSuggestion(prompt) {
  const input = document.getElementById('engineerAssistantInput');
  if (!input) return;
  input.value = prompt;
  engineerAssistantSend();
}

function engineerSecretaryTool(mode) {
  const input = document.getElementById('engineerAssistantInput');
  if (mode === 'ocr') {
    if (typeof kameraAc === 'function') kameraAc('ocr');
    if (input) input.value = 'OCR ciktisini secili rapor taslagina ekle';
    engineerAssistantSend();
    return;
  }
  if (input) input.value = 'Sesli not: secili kart icin saha akisi sorunsuz ilerledi bilgisini ekle.';
  engineerAssistantSend();
}

async function engineerAssistantSend() {
  const input = document.getElementById('engineerAssistantInput');
  const token = localStorage.getItem('bai_token') || '';
  const soru = input ? input.value.trim() : '';
  const selectedItem = engineerFindDecisionItem(_engineerFocusedDecisionId);
  if (!soru) return;
  if (input) input.value = '';
  engineerAssistantSetResponse('Teknik sekreter taslagi isliyor...', 'loading');

  if (selectedItem && !navigator.onLine) {
    engineerApplySecretaryNote(soru);
    return;
  }

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        soru: engineerBuildAssistantPrompt(soru, selectedItem),
        session_id: typeof chatSessionId !== 'undefined' ? chatSessionId : null,
        token
      })
    });
    const data = await res.json();
    if (!res.ok) {
      const msg = data.detail || data.message || 'Yanit alinamadi.';
      if (selectedItem) engineerApplySecretaryNote(soru);
      else engineerAssistantSetResponse(engineerEscapeHtml(msg));
      return;
    }
    const cevap = data.cevap || data.answer || 'Yanit alinamadi.';
    if (selectedItem) {
      selectedItem.draft = typeof cevap === 'string' && cevap.trim() ? cevap.trim() : `${selectedItem.draft} ${soru}`.trim();
      engineerRenderSecretaryState(selectedItem, 'AI taslagi guncelledi.');
    } else {
      engineerAssistantSetResponse(typeof markdownToHtml === 'function' ? markdownToHtml(cevap) : engineerEscapeHtml(cevap));
    }
  } catch (err) {
    if (selectedItem) engineerApplySecretaryNote(soru);
    else engineerAssistantSetResponse('AI gorev asistanina su anda ulasilamiyor.');
  }
}

let _contractorDashboardLoading = false;
let _contractorDashboardLoaded = false;
let _contractorDashboardSnapshot = null;
let _contractorDashboardActiveFilter = null;
let _contractorAdvancedAnalysisAvailable = true;
const CONTRACTOR_AI_SYSTEM_PROMPT = 'Sen bir yönetici karar destek asistanısın. Sadece doğrulanmış saha verisine dayan, operasyonel etkiyi özetle, finansal spekülasyon yapma, ham veri ve log gösterme.';

function setDashboardVisibility(role) {
  const engineer = document.getElementById('engineerDashboard');
  const contractor = document.getElementById('contractorDashboard');
  if (engineer) engineer.style.display = isContractorRole(role) ? 'none' : '';
  if (contractor) contractor.style.display = isContractorRole(role) ? '' : 'none';
  const mobileRailBtn = document.getElementById('contractorRailToggleMobile');
  if (mobileRailBtn) mobileRailBtn.style.display = isContractorRole(role) ? '' : 'none';
}

function contractorSetResponse(content, state = 'content') {
  const box = document.getElementById('contractorAssistantResponse');
  if (!box) return;
  box.classList.remove('is-empty', 'is-loading');
  const cleanedContent = contractorPolishText(content);

  if (state === 'empty') {
    box.classList.add('is-empty');
    box.textContent = cleanedContent || '';
    return;
  }
  if (state === 'loading') {
    box.classList.add('is-loading');
    box.textContent = cleanedContent || 'AI yönetici özeti hazırlanıyor...';
    return;
  }
  box.innerHTML = cleanedContent;
}

function contractorSetCommandMode(mode = 'idle', hint = '') {
  const label = document.getElementById('contractorCommandModeLabel');
  const hintEl = document.getElementById('contractorCommandHint');
  if (label) {
    label.textContent =
      mode === 'local' ? 'Yerel filtre aktif' :
      mode === 'ai' ? 'Gelişmiş analiz çalışıyor' :
      mode === 'offline' ? 'Sadece filtreleme aktif' :
      'Komut bekleniyor';
  }
  if (hintEl) {
    hintEl.textContent = hint || (
      mode === 'local' ? 'Komut tarayıcı içinde işlendi; yanıt anında verildi.' :
      mode === 'ai' ? 'Komut yerel filtreyi aşınca gelişmiş analiz katmanına gönderildi.' :
      mode === 'offline' ? 'İnternet veya API erişimi olmadığında sistem yalnızca yerel komutları işler.' :
      'Filtre, yönlendirme veya gelişmiş analiz isteyebilirsiniz.'
    );
  }
}

function contractorNormalizeText(value) {
  return String(value || '')
    .toLocaleLowerCase('tr-TR')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

function contractorDateBucket(value) {
  if (!value) return '';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return '';
  const today = new Date();
  const current = new Date(today.getFullYear(), today.getMonth(), today.getDate()).getTime();
  const target = new Date(parsed.getFullYear(), parsed.getMonth(), parsed.getDate()).getTime();
  const diff = Math.round((current - target) / 86400000);
  if (diff === 0) return 'today';
  if (diff === 1) return 'yesterday';
  return '';
}

async function contractorAssistantSend() {
  const input = document.getElementById('contractorAssistantInput');
  const token = localStorage.getItem('bai_token') || '';
  const soru = input ? input.value.trim() : '';
  if (!soru) return;
  if (input) input.value = '';

  const localResult = contractorHandleLocalCommand(soru);
  if (localResult) {
    contractorSetCommandMode('local');
    if (localResult.kind === 'navigate') {
      navGit(localResult.page);
    } else if (typeof localResult.action === 'function') {
      localResult.action();
    }
    contractorSetResponse(localResult.message || 'Komut yerel olarak işlendi.');
    return;
  }

  if (!navigator.onLine || !_contractorAdvancedAnalysisAvailable) {
    contractorSetCommandMode('offline');
    contractorSetResponse('Gelişmiş analiz şu an yapılamıyor, sadece filtreleme aktif.');
    return;
  }

  contractorSetCommandMode('ai');
  contractorSetResponse('AI yönetici özeti hazırlanıyor...', 'loading');
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        soru: `${CONTRACTOR_AI_SYSTEM_PROMPT}\n\nDoğrulanmış dashboard özeti:\n${contractorBuildAssistantContext()}\n\nKullanıcı isteği: ${soru}`,
        session_id: typeof chatSessionId !== 'undefined' ? `${chatSessionId}-contractor` : 'contractor-dashboard',
        token
      })
    });
    const data = await res.json();
    if (!res.ok) {
      _contractorAdvancedAnalysisAvailable = false;
      contractorSetCommandMode('offline');
      contractorSetResponse(engineerEscapeHtml(data.detail || data.message || 'Yanıt alınamadı.'));
      return;
    }
    _contractorAdvancedAnalysisAvailable = true;
    const cevap = data.cevap || data.answer || 'Yanıt alınamadı.';
    contractorSetResponse(typeof markdownToHtml === 'function' ? markdownToHtml(cevap) : engineerEscapeHtml(cevap));
  } catch (err) {
    _contractorAdvancedAnalysisAvailable = false;
    contractorSetCommandMode('offline');
    contractorSetResponse('Gelişmiş analiz şu an yapılamıyor, sadece filtreleme aktif.');
  }
}

function contractorAssistantUseSuggestion(prompt) {
  const input = document.getElementById('contractorAssistantInput');
  if (!input) return;
  input.value = prompt;
  contractorAssistantSend();
}

function contractorNormalizeTone(tone) {
  if (tone === 'critical' || tone === 'warning' || tone === 'success' || tone === 'info') return tone;
  return 'neutral';
}

function contractorShortDate(value) {
  if (!value) return 'Tarih yok';
  const parsed = new Date(value.includes('T') ? value : `${value}T00:00:00`);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleDateString('tr-TR', { day: '2-digit', month: 'short' });
}

function contractorUniqueValues(values) {
  return Array.from(new Set((values || []).filter(Boolean)));
}

function contractorGetActiveSites() {
  const sites = _contractorDashboardSnapshot.field_summary.active_sites;
  return Array.isArray(sites) ? sites : [];
}

function contractorGetExecutiveHero() {
  return _contractorDashboardSnapshot.executive_summary.hero || {};
}

function contractorFormatSummaryText(value) {
  const escaped = engineerEscapeHtml(value || '');
  return escaped
    .replace(/\b(Durum)\b/g, '<strong>$1</strong>')
    .replace(/\b(Risk)\b/g, '<strong>$1</strong>')
    .replace(/\b(Beklenti)\b/g, '<strong>$1</strong>');
}

function contractorPolishText(value) {
  let text = String(value || '').trim();
  if (!text) return text;

  text = text
    .replace(/Ana gerçek yalnızca onaylı veri/gi, 'Günün saha resmi')
    .replace(/yalnızca onaylanan veriyi baz alıyor/gi, 'saha ritmini net biçimde gösteriyor')
    .replace(/yalnızca onaylı akıştan kuruluyor/gi, 'saha ritmini net biçimde gösteriyor')
    .replace(/Yönetici ekranındaki ana gerçek yalnızca onaylanan kayıtlarla oluşuyor/gi, 'Sahadaki görünüm karar almaya uygun ve net ilerliyor')
    .replace(/kayıt bulunamadı/gi, 'saha temiz ilerliyor')
    .replace(/kayıt bulunmuyor/gi, 'ayrı bir istisna görünmüyor')
    .replace(/görünmüyor/gi, 'öne çıkmıyor')
    .replace(/Kritik Uyarı/gi, 'Stratejik Öneri')
    .replace(/Aksiyon önerisi/gi, 'Stratejik öneri');

  if (/doğrulanmış.*istisna bulunmuyor|saha olayı bulunmuyor|saha kümesi görünmüyor/i.test(text)) {
    text = text
      .replace(/doğrulanmış\s+/gi, '')
      .replace(/bir saha istisnası bulunmuyor/gi, 'ayrı bir istisna öne çıkmıyor')
      .replace(/bir saha olayı bulunmuyor/gi, 'ayrı bir saha başlığı öne çıkmıyor')
      .replace(/bir saha kümesi görünmüyor/gi, 'ayrı bir saha kümesi öne çıkmıyor');
  }

  return text;
}

function contractorApplyMetricLabels() {
  const criticalLabel = document.querySelector('#contractorMetricCritical .contractor-metric-card__label');
  const integrityLabel = document.querySelector('#contractorMetricIntegrity .contractor-metric-card__label');
  const watchLabel = document.querySelector('#contractorMetricWatchlist .contractor-metric-card__label');
  if (criticalLabel) criticalLabel.textContent = 'Doğrulanmış İstisna';
  if (integrityLabel) integrityLabel.textContent = 'Rapor Bütünlüğü';
  if (watchLabel) watchLabel.textContent = 'Malzeme Uyarısı';
}

function contractorSyncRoleLabels(roleLabel) {
  const label = roleLabel || _contractorDashboardSnapshot.access_role_label || getWorkspaceRoleLabel(localStorage.getItem('bai_rol'));
  const headerRole = document.getElementById('headerUserRole');
  const amRole = document.getElementById('amRole');
  if (headerRole) headerRole.textContent = label;
  if (amRole) amRole.textContent = label;
}

function contractorBuildLocalNarrative(filterKey, groups) {
  const snapshot = _contractorDashboardSnapshot || {};
  const buffer = snapshot.verification_buffer || {};
  const activeSites = contractorGetActiveSites();
  const activeSiteNames = contractorUniqueValues(activeSites.map((site) => site.name || '')).slice(0, 3);
  const matchedSiteNames = contractorUniqueValues((groups || []).map((group) => group.site_name || '')).slice(0, 3);
  const sitePhrase = (matchedSiteNames.length ? matchedSiteNames : activeSiteNames).join(', ');
  const draftRecords = Number(buffer.records.DRAFT || 0);
  const draftReports = Number(buffer.reports.DRAFT || 0);
  const repeatedCount = (groups || []).filter((group) => group.repeated_zone || Number(group.verified_issue_count || 0) >= 2).length;

  if (filterKey === 'today') {
    if (groups.length) {
      return `Bugün aktif şantiyelerde doğrulanmış akış ${matchedSiteNames.length || groups.length} odakta yoğunlaşıyor: ${sitePhrase}. Taslakta ${draftRecords} kayıt ve ${draftReports} rapor süreçte; ana gerçek hâlâ yalnızca onaylı akıştan kuruluyor. ${repeatedCount ? 'Tekrarlayan alanlar için kontrollü izleme sürmeli.' : 'Kritik bir engel görünmüyor.'}`;
    }
    return `Bugün aktif şantiyelerde yeni doğrulanmış bir saha istisnası görünmüyor. ${activeSiteNames.length ? `${activeSiteNames.join(', ')} tarafında akış stabil.` : 'Şantiye akışı sakin.'} Taslakta ${draftRecords} kayıt süreçte kalsa da yönetici özeti yalnızca onaylanan veriyi baz alıyor.`;
  }

  if (filterKey === 'safety') {
    if (groups.length) {
      return `İSG filtresinde aktif şantiyelerden ${sitePhrase} öne çıkıyor. ${groups.length} doğrulanmış küme tarandı; ${repeatedCount ? `${repeatedCount} alan tekrar eden risk davranışı gösteriyor.` : 'Tekrarlayan kritik ihlal görünmüyor.'} Taslaktaki ${draftRecords} kayıt sadece süreç tamponunda izleniyor.`;
    }
    return `Aktif şantiyelerde doğrulanmış İSG odaklı yeni bir istisna görünmüyor. Yönetici ekranında kritik ihlal sinyali yok; taslaktaki ${draftRecords} kayıt süreçte tutuluyor.`;
  }

  if (filterKey === 'stock') {
    if (groups.length) {
      return `Stok ve malzeme filtresinde aktif şantiyelerden ${sitePhrase} öne çıkıyor. Doğrulanmış tedarik sinyalleri operasyon etkisi yaratabilecek alanlara daraltıldı. Taslaktaki ${draftReports} rapor henüz ana gerçeğe dahil edilmedi; stok tamponu yerelden hızla izlenebilir.`;
    }
    return `Aktif şantiyelerde doğrulanmış stok veya malzeme odaklı yeni bir saha kümesi görünmüyor. Malzeme uyarıları yine de taslak süreçten bağımsız olarak izlenmeye devam ediyor.`;
  }

  return contractorGetExecutiveHero().body || 'Doğrulanmış saha özeti hazır.';
}

function contractorSetMetric(cardId, valueId, contextId, noteId, metric, fallbackSuffix = '') {
  const card = document.getElementById(cardId);
  const valueEl = document.getElementById(valueId);
  const contextEl = document.getElementById(contextId);
  const noteEl = document.getElementById(noteId);
  let tone = contractorNormalizeTone(metric.tone);
  const numericValue = Number(metric.value ?? 0);
  if (cardId === 'contractorMetricCritical' && numericValue > 0) tone = numericValue >= 2 ? 'critical' : 'warning';
  if (cardId === 'contractorMetricIntegrity' && numericValue > 0 && numericValue < 35) tone = 'critical';
  const suffix = metric.suffix ?? fallbackSuffix;
  if (card) card.setAttribute('data-tone', tone);
  if (valueEl) valueEl.textContent = `${metric.value ?? 0}${suffix}`;
  if (contextEl) contextEl.textContent = metric.context || '';
  if (noteEl) noteEl.textContent = metric.note || '';
}

function contractorRenderInsights(items) {
  const fallbackBody = Array.isArray(items) && items.length
     ? items.map((item) => item.body || '').filter(Boolean).join(' ')
    : '';
  contractorRenderExecutiveSummary(_contractorDashboardSnapshot.executive_summary || {}, {
    body: fallbackBody || contractorGetExecutiveHero().body || 'Bugun dogrulanmis yonetici ozeti olusmadi; saha akisi su an sakin gorunuyor.',
    tone: contractorGetExecutiveHero().tone || (items?.[0].tone || 'neutral'),
    footerItems: contractorBuildExecutiveMeta(),
  });
  return;
  const el = document.getElementById('contractorInsightList');
  if (!el) return;
  if (!items.length) {
    el.innerHTML = '<div class="contractor-empty-state">Bugün doğrulanmış bir yönetici özeti oluşmadı; saha akışı şu an sakin görünüyor.</div>';
    return;
  }
  el.innerHTML = items.map((item) => {
    const tone = contractorNormalizeTone(item.tone);
    return `
      <article class="contractor-insight-card" data-tone="${engineerEscapeHtml(tone)}">
        <div class="contractor-insight-card__title">
          <strong>${engineerEscapeHtml(item.title || 'Özet')}</strong>
        </div>
        <div class="contractor-insight-card__body">${engineerEscapeHtml(item.body || '')}</div>
      </article>`;
  }).join('');
}

function contractorBuildActionEvidence(item) {
  const snapshot = _contractorDashboardSnapshot || {};
  const metrics = Array.isArray(snapshot.top_metrics) ? snapshot.top_metrics : [];
  const criticalMetric = metrics.find((metric) => metric.id === 'critical_exceptions');
  const integrityMetric = metrics.find((metric) => metric.id === 'report_integrity');
  const materialMetric = metrics.find((metric) => metric.id === 'material_watchlist');
  const firstGroup = Array.isArray(snapshot.field_summary.groups) ? snapshot.field_summary.groups[0] : null;
  const activeSites = snapshot.field_summary.active_site_count ?? contractorGetActiveSites().length ?? 0;
  const localContext = snapshot.local_filter_context || {};
  const itemId = String(item.id || '');

  if (Array.isArray(item.evidence_points) && item.evidence_points.length) {
    return item.evidence_points;
  }

  if (itemId.includes('material')) {
    return [
      { label: 'Analiz Sonucu', value: contractorPolishText(item.body || 'Malzeme tamponunun güçlendirilmesi öneriliyor.') },
      { label: 'Mevcut Malzeme Sinyali', value: `${materialMetric.value ?? 0}` },
      { label: 'Rapor Bütünlüğü', value: `${integrityMetric.value ?? 0}%` },
      { label: 'Aktif Şantiye', value: `${activeSites}` },
      { label: 'Risk', value: contractorPolishText(materialMetric.note || 'Teslim sırası gevşerse stok tamponu baskı görebilir.') },
    ];
  }

  if (itemId.includes('draft')) {
    return [
      { label: 'Analiz Sonucu', value: contractorPolishText(item.body || 'Akış ritmini hızlandırmak öneriliyor.') },
      { label: 'Rapor Bütünlüğü', value: `${integrityMetric.value ?? 0}%` },
      { label: 'Bugünkü Saha Kaydı', value: `${localContext.today_verified_records ?? 0}` },
      { label: 'Aktif Şantiye', value: `${activeSites}` },
      { label: 'Risk', value: contractorPolishText(integrityMetric.note || 'Akış temposu yavaşlarsa karar ritmi de gecikebilir.') },
    ];
  }

  if (itemId.includes('repeat') || itemId.includes('zone')) {
    return [
      { label: 'Analiz Sonucu', value: contractorPolishText(item.body || 'Bu odak için derin saha turu öneriliyor.') },
      { label: 'Odak Alan', value: firstGroup.zone_label || 'Odak alan izleniyor' },
      { label: 'Doğrulanmış Sinyal', value: `${firstGroup.verified_issue_count ?? criticalMetric.value ?? 0}` },
      { label: 'Son Güncelleme', value: firstGroup.last_verified_at || 'Gün içi akış' },
      { label: 'Risk', value: contractorPolishText(criticalMetric.note || 'Yoğunlaşan alan kapanış temposunu baskılayabilir.') },
    ];
  }

  return [
    { label: 'Analiz Sonucu', value: contractorPolishText(item.body || 'Sakin tabloyu taramak öneriliyor.') },
    { label: 'Aktif Şantiye', value: `${activeSites}` },
    { label: 'Malzeme Sinyali', value: `${materialMetric.value ?? 0}` },
    { label: 'İSG Sinyali', value: `${localContext.today_safety_signals ?? 0}` },
    { label: 'Risk', value: contractorPolishText(criticalMetric.note || 'Belirgin bir baskı görünmüyor; rutin tempo korunabilir.') },
  ];
}

function contractorToggleActionEvidence(id) {
  const panel = document.getElementById(id);
  if (!panel) return;
  const willExpand = panel.hasAttribute('hidden');
  panel.toggleAttribute('hidden');
  const trigger = document.querySelector(`[data-evidence-target="${id}"]`);
  if (trigger) trigger.setAttribute('aria-expanded', willExpand ? 'true' : 'false');
}

let _contractorDashboardDefaultHtml = null;

function contractorRestoreDefaultDashboard(root) {
  if (!root) return;
  if (_contractorDashboardDefaultHtml && root.dataset.onboarding === 'true') {
    root.innerHTML = _contractorDashboardDefaultHtml;
  } else if (!_contractorDashboardDefaultHtml && root.innerHTML) {
    _contractorDashboardDefaultHtml = root.innerHTML;
  }
  root.dataset.onboarding = 'false';
}

async function contractorFetchActiveSiteCount(token) {
  if (!token) return null;
  try {
    const res = await fetch('/santiyeler', {
      method: 'GET',
      headers: { Authorization: 'Bearer ' + token },
    });
    if (!res.ok) return null;
    const data = await res.json();
    return Array.isArray(data.santiyeler) ? data.santiyeler.length : 0;
  } catch (err) {
    console.warn('[ContractorOnboarding] site count check failed:', err.message || err);
    return null;
  }
}

function contractorInviteSoon() {
  navGit('santiye');
  setTimeout(() => {
    if (typeof davetModalAc === 'function') davetModalAc();
  }, 150);
}

function contractorRenderOnboarding(root) {
  if (!root) return;
  if (!_contractorDashboardDefaultHtml) _contractorDashboardDefaultHtml = root.innerHTML;
  root.dataset.onboarding = 'true';
  _contractorDashboardSnapshot = null;
  _contractorDashboardActiveFilter = null;
  root.innerHTML = `
    <div style="min-height:calc(100vh - 180px);display:flex;align-items:center;justify-content:center;padding:24px;">
      <section style="width:min(760px,100%);background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:28px;box-shadow:0 14px 40px rgba(15,23,42,0.08);">
        <div style="font-size:28px;font-weight:800;color:#0F172A;margin-bottom:8px;">🏠‰ BuildingAI'ye Hoş Geldiniz!</div>
        <div style="font-size:14px;color:#64748B;line-height:1.7;margin-bottom:24px;">Başlamak için ilk çalışma alanınızı kurun. Şantiye oluşunca yönetici dashboard'u otomatik açılır.</div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <button type="button" onclick="navGit('santiye')" style="width:100%;display:flex;align-items:center;gap:14px;text-align:left;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:16px;cursor:pointer;">
            <span style="width:38px;height:38px;border-radius:10px;background:#DBEAFE;color:#1D4ED8;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;flex-shrink:0;">1</span>
            <span style="display:flex;flex-direction:column;gap:3px;">
              <span style="font-size:15px;font-weight:800;color:#0F172A;">İlk Şantiyenizi Oluşturun</span>
              <span style="font-size:13px;color:#64748B;">Projenizi takibe alın</span>
            </span>
          </button>
          <button type="button" onclick="contractorInviteSoon()" style="width:100%;display:flex;align-items:center;gap:14px;text-align:left;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:16px;cursor:pointer;">
            <span style="width:38px;height:38px;border-radius:10px;background:#EEF2FF;color:#4F46E5;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;flex-shrink:0;">2</span>
            <span style="display:flex;flex-direction:column;gap:3px;">
              <span style="font-size:15px;font-weight:800;color:#0F172A;">Mühendis Davet Edin</span>
              <span style="font-size:13px;color:#64748B;">Ekibinizi oluşturun</span>
            </span>
          </button>
          <button type="button" onclick="navGit('stok')" style="width:100%;display:flex;align-items:center;gap:14px;text-align:left;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:16px;cursor:pointer;">
            <span style="width:38px;height:38px;border-radius:10px;background:#DCFCE7;color:#15803D;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;flex-shrink:0;">3</span>
            <span style="display:flex;flex-direction:column;gap:3px;">
              <span style="font-size:15px;font-weight:800;color:#0F172A;">Stok Takibi Başlatın</span>
              <span style="font-size:13px;color:#64748B;">Malzemelerinizi yönetin</span>
            </span>
          </button>
        </div>
      </section>
    </div>`;
}

async function sahaGunluguYukle() {
  const el = document.getElementById('sahaGunluguListe');
  if (!el) return;
  const token = localStorage.getItem('bai_token') || '';
  try {
    const res = await fetch(`/rapor_listesitoken=${token}`);
    const data = await res.json();
    const raporlar = data.raporlar || data.items || data.list || [];
    if (!raporlar.length) {
      el.innerHTML = '<div style="color:#94A3B8;font-size:12px;text-align:center;padding:24px;">Henüz kayıt bulunmuyor.</div>';
      return;
    }
    const son5 = raporlar.slice(-5).reverse();
    const durumCfg = {
      'dogrulandi': { bg: '#F0FDF4', border: '#86EFAC', txt: '#16A34A', lbl: 'İşlendi',    ikon: '?',  ikonBg: '#DCFCE7', ikonTxt: '#16A34A' },
      'uyari':      { bg: '#FFF7ED', border: '#FED7AA', txt: '#EA580C', lbl: 'Uyarı',     ikon: '?',  ikonBg: '#FFEDD5', ikonTxt: '#EA580C' },
      'bekleniyor': { bg: '#FEF9F0', border: '#FDE68A', txt: '#B45309', lbl: 'İşleniyor', ikon: 'â³', ikonBg: '#FEF3C7', ikonTxt: '#B45309' },
    };
    el.innerHTML = son5.map(r => {
      const baslik = typeof r === 'string' ? r : (r.baslik || r.ad || r.tip || 'Rapor');
      const zaman  = typeof r === 'string' ? '' : (r.tarih || r.zaman || '');
      const durum  = typeof r === 'object' ? ((r.durum || '').toLowerCase() || 'dogrulandi') : 'dogrulandi';
      const cfg    = durumCfg[durum] || durumCfg['dogrulandi'];
      const isKamera = baslik.toLowerCase().includes('kamera') || baslik.toLowerCase().includes('fotoğraf') || baslik.toLowerCase().includes('ocr');
      return `<div class="saha-row" style="display:flex;align-items:center;gap:12px;padding:10px 8px;border-radius:10px;transition:background 0.15s;">
        <div style="width:36px;height:36px;border-radius:8px;background:${isKamera ? '#EFF6FF' : '#F0FDF4'};display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:16px;">
          ${isKamera ? '🏠' : '🏗'}
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

// AI Uyarılar ? /kullanim-durumu uyari alanı
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
      'kritik': { border: '#EF4444', bg: '#FFF5F5', ikonBg: '#FEE2E2', ikon: '?', txt: '#DC2626' },
      'uyari':  { border: '#F97316', bg: '#FFF7ED', ikonBg: '#FFEDD5', ikon: '?', txt: '#EA580C' },
      'bilgi':  { border: '#3B82F6', bg: '#EFF6FF', ikonBg: '#DBEAFE', ikon: 'â„¹', txt: '#2563EB' },
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
// KAMERA ANALİZİ SAYFASI ?? Tam Dashboard
// ══════════════════════════════════════════════════
let _kpAktifTip = 'genel';           // seçili analiz tipi
let _kpAktifChip = 'all';            // aktif filtre chip
let _kpTumAnaliz = [];               // cache
let _kpManuelKayitlar = [];          // localStorage'dan yüklenir
let _kpCameraList    = [];           // registered cameras
let _kpSortDesc      = true;         // true = en yeni önce
let _kpViewMode      = 'primary2';   // 'primary2' | 'grid4' | 'all'

function kpCameraDebug(label, data) {
  try {
    console.debug('[kamera-analiz]', label, data);
  } catch(e) {}
}

function kpGetVisibleAnaliz() {
  return (_kpTumAnaliz || []).filter(k => !k.archived);
}

function kameraPageAc() {
  ['content','aiCommandBar','santiyePage','fiyatPage','stokPage','arsivPage','sahaKayitlariPage','hiyerarsiPage','hakedisPage','engineerDashboard','contractorDashboard'].forEach(pid => {
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
}

async function sahaKayitlariPageAc() {
  ['content','aiCommandBar','santiyePage','fiyatPage','stokPage','arsivPage','kameraPage','hiyerarsiPage','hakedisPage','engineerDashboard','contractorDashboard'].forEach(pid => {
    const el = document.getElementById(pid);
    if (el) el.style.display = 'none';
  });
  const page = document.getElementById('sahaKayitlariPage');
  if (!page) return;
  page.style.display = 'flex';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Saha Kayıtları';
  if (typeof kpSantiyeBilgisiGuncelle === 'function') await kpSantiyeBilgisiGuncelle();
  if (typeof kpSahaFilterSantiyeDoldur === 'function') kpSahaFilterSantiyeDoldur();
  if (typeof kpManuelYukle === 'function') kpManuelYukle();
}

function sahaKayitlariPageKapat() {
  const page = document.getElementById('sahaKayitlariPage');
  if (page) page.style.display = 'none';
}

function engineerPageAc() {
  var baiUser = JSON.parse(localStorage.getItem('bai_user') || '{}');
  var rol = localStorage.getItem('bai_rol') || '';
  var isAdmin = baiUser.is_admin === true;
  if (!isEngineerRole(rol) && !isAdmin) {
    console.warn('Mühendislik paneline erişim yetkiniz yok');
    return;
  }
  ['content','aiCommandBar','santiyePage','fiyatPage','stokPage',
   'arsivPage','kameraPage','sahaKayitlariPage','hiyerarsiPage','hakedisPage','ayarlarPage','contractorDashboard'].forEach(function(pid) {
    var el = document.getElementById(pid);
    if (el) el.style.display = 'none';
  });
  var eng = document.getElementById('engineerDashboard');
  if (eng) eng.style.display = '';
  if (typeof loadEngineerDashboard === 'function') loadEngineerDashboard(true);
}

// â"€â"€ Santiye bilgisini üst barda güncelle (API'den çek)
let _kpSantiyeler = [];
let _kpAktifSantiye = null;

function kpCameraActiveSiteId() {
  const globalId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
  if (globalId) return Number(globalId);
  if (_kpAktifSantiye && _kpAktifSantiye.id) return Number(_kpAktifSantiye.id);
  try {
    const stored = JSON.parse(localStorage.getItem('varsayilan_santiye') || 'null');
    if (stored && stored.id) return Number(stored.id);
  } catch(e) {}
  return null;
}

async function kpSantiyeBilgisiGuncelle() {
  const token = localStorage.getItem('bai_token');
  if (!token) return;
  try {
    const res = await fetch('/santiyeler?token=' + token);
    const data = await res.json();
    _kpSantiyeler = data.santiyeler || [];
    const globalId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
    _kpAktifSantiye = (globalId ? _kpSantiyeler.find(s => Number(s.id) === Number(globalId)) : null)
      || _kpSantiyeler.find(s => s.aktif)
      || _kpSantiyeler[0]
      || null;
    window._kpSantiyeler = _kpSantiyeler;
    window._kpAktifSantiye = _kpAktifSantiye;
    if (_kpAktifSantiye && _kpAktifSantiye.id) {
      localStorage.setItem('varsayilan_santiye', JSON.stringify(_kpAktifSantiye));
    }
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
  if (nameEl) nameEl.textContent = _kpAktifSantiye.ad || '?';
  if (durEl) durEl.style.display = 'inline-flex';
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
  window._kpAktifSantiye = _kpAktifSantiye;
  if (_kpAktifSantiye && _kpAktifSantiye.id) {
    localStorage.setItem('varsayilan_santiye', JSON.stringify(_kpAktifSantiye));
  }
  kpProjeBarGuncelle();
  const dd = document.getElementById('kpProjeDropdownMenu');
  if (dd) dd.style.display = 'none';
  kpCameraListYukle();
  kameraPageYukle();
}

// â"€â"€ Kamera grid görüntüleme modu: 'primary2' | 'grid4' | 'all'
function kpKameraGoruntuleme(mod) {
  _kpViewMode = mod;
  ['primary2','grid4','all'].forEach(m => {
    const btn = document.getElementById('kpViewBtn-' + m);
    if (!btn) return;
    const isActive = m === mod;
    btn.style.background = isActive ? '#0F172A' : '#F1F5F9';
    const spanEl = btn.querySelector('span');
    if (spanEl) spanEl.style.color = isActive ? 'white' : '#475569';
    // Re-color all SVG fill/stroke children
    btn.querySelectorAll('svg, svg *').forEach(el => {
      const tag = el.tagName.toLowerCase();
      if (tag === 'svg') {
        el.setAttribute('fill', isActive ? 'white' : '#475569');
        el.setAttribute('stroke', isActive ? 'white' : '#475569');
      } else {
        if (el.hasAttribute('fill')   && el.getAttribute('fill')   !== 'none') el.setAttribute('fill',   isActive ? 'white' : '#475569');
        if (el.hasAttribute('stroke') && el.getAttribute('stroke') !== 'none') el.setAttribute('stroke', isActive ? 'white' : '#475569');
      }
    });
  });
  kpRenderCameraGrid(_kpCameraList);
}

function kpKameraFullscreen() {
  const el = document.getElementById('kpCameraGrid');
  if (el && el.requestFullscreen) el.requestFullscreen();
}

// â"€â"€ Yeni kamera ekle modal
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
  const ad = (document.getElementById('ykAd') || {}).value.trim();
  if (!ad) { showToast('Kamera adı zorunludur.', 'error'); return; }
  const url    = (document.getElementById('ykUrl')   || {}).value.trim() || '';
  const konum  = (document.getElementById('ykKonum') || {}).value.trim() || '';
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

// â"€â"€ Kamera listesi yükle ve render et
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

  const mode = _kpViewMode || 'primary2';

  // Layout config per mode
  const cfg = {
    primary2: { cols: 'repeat(2,1fr)', count: 2,    minH: '230px', iconSize: 44, gap: '14px' },
    grid4:    { cols: 'repeat(2,1fr)', count: 4,    minH: '168px', iconSize: 34, gap: '12px' },
    all:      { cols: 'repeat(auto-fit,minmax(200px,1fr))', count: null, minH: '148px', iconSize: 28, gap: '12px' },
  };
  const { cols, count, minH, iconSize, gap } = cfg[mode] || cfg['primary2'];

  grid.style.display = 'grid';
  grid.style.gridTemplateColumns = cols;
  grid.style.gap = gap;

  // Update hidden-camera badge in header
  const hiddenBadge = document.getElementById('kpHiddenCamBadge');
  const total = (liste || []).length;
  if (hiddenBadge) {
    const shown = count ? Math.min(total, count) : total;
    const hidden = total - shown;
    if (hidden > 0) {
      hiddenBadge.textContent = '+' + hidden + ' kamera';
      hiddenBadge.style.display = 'inline-block';
    } else {
      hiddenBadge.style.display = 'none';
    }
  }

  const cardShell = `position:relative;background:#0F172A;border:1px solid #1E293B;border-radius:14px;overflow:hidden;min-height:${minH};display:flex;flex-direction:column;justify-content:space-between;box-shadow:inset 0 1px 0 rgba(255,255,255,0.03), 0 10px 24px rgba(15,23,42,0.18);cursor:pointer;transition:border-color 0.2s ease, transform 0.2s ease;`;
  const bodyShell = `flex:1;display:flex;align-items:center;justify-content:center;padding:18px 16px;background:radial-gradient(circle at top, rgba(59,130,246,0.12), transparent 58%), linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0));`;
  const footerShell = 'padding:10px 12px;background:rgba(2,6,23,0.82);border-top:1px solid rgba(148,163,184,0.12);display:flex;align-items:flex-end;justify-content:space-between;gap:10px;';

  const renderPlaceholder = label => `
    <div onclick="yeniKameraEkleAc()" title="Kamera eklemek için tıklayın"
      style="${cardShell}"
      onmouseover="this.style.borderColor='#F97316';this.style.transform='translateY(-1px)'"
      onmouseout="this.style.borderColor='#1E293B';this.style.transform='none'">
      <div style="${bodyShell}flex-direction:column;gap:10px;">
        <svg width="${iconSize}" height="${iconSize}" fill="none" viewBox="0 0 24 24" stroke="rgba(148,163,184,0.72)" stroke-width="1.6">
          <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
          <circle cx="12" cy="13" r="3"/>
        </svg>
        <div style="font-size:11px;font-weight:600;color:#94A3B8;">Kamera Ekle</div>
      </div>
      <div style="${footerShell}">
        <div style="min-width:0;">
          <div style="font-size:11px;font-weight:800;color:#FFFFFF;line-height:1.25;letter-spacing:0.02em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${label}</div>
        </div>
        <span style="width:8px;height:8px;border-radius:999px;background:#334155;flex-shrink:0;"></span>
      </div>
    </div>
  `;

  const allPlaceholders = ['CAM-01 ANA GİRİŞ','CAM-02 AÇIK DEPO','CAM-03 KUZEY CEPHE','CAM-04 BATI CEPHE','CAM-05 İÇ ALAN','CAM-06 GÜNEY GİRİŞ'];

  if (!liste || liste.length === 0) {
    const slots = count ? allPlaceholders.slice(0, count) : allPlaceholders;
    grid.innerHTML = slots.map(renderPlaceholder).join('');
    return;
  }

  // Slice list to displayable count; pad remainder with placeholders
  const displayList = count ? liste.slice(0, count) : liste;
  const padCount    = count ? Math.max(0, count - displayList.length) : 0;

  const realCards = displayList.map(c => `
    <div style="${cardShell}"
      onmouseover="this.style.borderColor='#F97316';this.style.transform='translateY(-1px)'"
      onmouseout="this.style.borderColor='#1E293B';this.style.transform='none'">
      <div style="${bodyShell}position:relative;">
        <div style="position:absolute;top:12px;right:12px;display:flex;align-items:center;gap:6px;">
          <span style="width:8px;height:8px;border-radius:999px;background:${c.aktif ? '#10B981' : '#EF4444'};box-shadow:0 0 0 4px rgba(15,23,42,0.25);animation:${c.aktif ? 'kpPulse 1.8s infinite' : 'none'};"></span>
          ${(()=>{const _u=JSON.parse(localStorage.getItem('bai_user')||'{}');return (_u.is_owner||_u.is_admin) ? `<button onclick="event.stopPropagation();kpCameraSil(${c.id},'${(c.name || '').replace(/'/g,'')}')" title="Sil" style="width:28px;height:28px;display:flex;align-items:center;justify-content:center;background:rgba(15,23,42,0.72);border:1px solid rgba(148,163,184,0.18);border-radius:8px;color:#F8FAFC;cursor:pointer;"><svg width="12" height="12" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg></button>`:''})()}
        </div>
        <div style="display:flex;flex-direction:column;align-items:center;gap:10px;">
          <div style="width:${iconSize + 8}px;height:${iconSize + 8}px;border-radius:16px;background:rgba(148,163,184,0.08);border:1px solid rgba(148,163,184,0.14);display:flex;align-items:center;justify-content:center;">
            <svg width="${iconSize}" height="${iconSize}" fill="none" viewBox="0 0 24 24" stroke="#94A3B8" stroke-width="1.6">
              <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/>
              <circle cx="12" cy="13" r="3"/>
            </svg>
          </div>
          <div style="font-size:10px;font-weight:600;color:#64748B;text-align:center;max-width:100%;padding:0 10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${c.url ? c.url.substring(0, 34) + (c.url.length > 34 ? '...' : '') : 'Canlı yayın hazırlanıyor'}</div>
        </div>
      </div>
      <div style="${footerShell}">
        <div style="min-width:0;">
          <div style="font-size:11px;font-weight:800;color:#FFFFFF;line-height:1.25;letter-spacing:0.02em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${c.name || 'AI Kamera Kaydı'}</div>
          ${c.location ? `<div style="font-size:10px;color:#94A3B8;line-height:1.35;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${c.location}</div>` : ''}
        </div>
      </div>
    </div>
  `).join('');

  const padCards = allPlaceholders.slice(displayList.length, displayList.length + padCount).map(renderPlaceholder).join('');
  grid.innerHTML = realCards + padCards;
}

async function kpCameraSil(id, ad) {
  if (!confirm(`"${ad}" kamerasını silmek istediğinize emin misiniz`)) return;
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
  if (cmdBar) cmdBar.style.display  = 'block';
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

function kpAiEsc(value) {
  return String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
}

function kpAiNormalizeText(value) {
  return String(value ?? '')
    .replace(/```(:json)/gi, '')
    .replace(/```/g, '')
    .replace(/\*\*(.*)\*\*/g, '$1')
    .replace(/__(.*)__/g, '$1')
    .replace(/^\s*#{1,6}\s+/gm, '')
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]{2,}/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function kpAiTryJson(value) {
  if (!value) return null;
  if (typeof value === 'object') return value;
  const text = String(value).trim();
  const candidates = [];
  candidates.push(text);
  const fenced = text.match(/```json\s*([\s\S]*)\s*```/i);
  if (fenced) candidates.push(fenced[1]);
  const first = text.indexOf('{');
  const last = text.lastIndexOf('}');
  if (first >= 0 && last > first) candidates.push(text.slice(first, last + 1));
  for (const candidate of candidates) {
    try { return JSON.parse(candidate); } catch(e) {}
  }
  return null;
}

function kpAiStripJsonFromText(value) {
  let text = String(value ?? '');
  text = text.replace(/```json\s*[\s\S]*```/gi, '');
  const first = text.indexOf('{');
  const last = text.lastIndexOf('}');
  if (first >= 0 && last > first) text = (text.slice(0, first) + '\n' + text.slice(last + 1)).trim();
  return kpAiNormalizeText(text);
}

function kpAiCanonicalHeading(value) {
  const key = String(value || '').replace(/[^\p{L}\p{N}\s]/gu, '').trim().toLocaleLowerCase('tr-TR');
  if (/genel|durum|overview|özet|ozet/.test(key)) return 'summary';
  if (/tespit|nesne|object|detection/.test(key)) return 'detections';
  if (/risk|sorun|ihlal|problem|issue/.test(key)) return 'risks';
  if (/öner|oner|aksiyon|önlem|onlem|recommend|action/.test(key)) return 'recommendations';
  if (/teknik|not|technical/.test(key)) return 'notes';
  return '';
}

function kpAiMarkdownSections(value) {
  const text = kpAiStripJsonFromText(value);
  const sections = {};
  let current = 'intro';
  text.split('\n').forEach(line => {
    const heading = line.match(/^\s*#{1,6}\s*(.+)\s*$/);
    if (heading) {
      current = kpAiCanonicalHeading(heading[1]) || 'notes';
      if (!sections[current]) sections[current] = [];
      return;
    }
    if (!sections[current]) sections[current] = [];
    sections[current].push(line);
  });
  Object.keys(sections).forEach(key => {
    sections[key] = kpAiNormalizeText(sections[key].join('\n'));
  });
  return sections;
}

function kpAiArray(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value.filter(Boolean);
  if (typeof value === 'string') return value.split(/\n|;|,/).map(x => x.trim()).filter(Boolean);
  if (typeof value === 'object') return Object.values(value).filter(Boolean);
  return [value];
}

function kpAiUnique(items) {
  const seen = new Set();
  return kpAiArray(items).filter(item => {
    const label = typeof item === 'object'
       ? (item.aciklama || item.label || item.class || item.name || item.ozet || item.description || item.type || JSON.stringify(item))
      : item;
    const key = kpAiNormalizeText(label).toLocaleLowerCase('tr-TR');
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function kpAiSectionItems(text) {
  if (!text) return [];
  return kpAiNormalizeText(text)
    .split(/\n|\?/)
    .map(line => line.replace(/^\s*[-*]\s*/, '').trim())
    .filter(line => line.length > 2);
}

function kpAiIsAdminUser() {
  try {
    const user = JSON.parse(localStorage.getItem('bai_user') || '{}');
    const role = String(user.role || user.rol || localStorage.getItem('bai_rol') || '').toLowerCase();
    return user.is_admin === true || user.is_owner === true || role === 'admin' || role === 'developer';
  } catch(e) {
    return false;
  }
}

function kpAiParsedPayload(record, rawText) {
  const rawPayload = record && (record.ai_result_json || record.ihlaller || record.ai_suggestion_json);
  const payload = kpAiTryJson(rawPayload) || {};
  const parsed = payload.parsed && typeof payload.parsed === 'object'
     ? payload.parsed
    : (kpAiTryJson(rawText) || {});
  const visual = payload.visual_data && typeof payload.visual_data === 'object' ? payload.visual_data : {};
  return { payload, parsed, visual };
}

function kpAiIsNonSite(record, parsed, rawText) {
  const joined = [
    record.ai_summary,
    record.ozet,
    record.description,
    rawText,
    parsed.kategori,
    parsed.category,
    parsed.gorsel_tipi,
    parsed.image_type,
    parsed.uygunluk,
    parsed.not_site_reason
  ].filter(Boolean).join(' ').toLocaleLowerCase('tr-TR');
  if (parsed.is_construction_site === false || parsed.construction_site === false || parsed.saha_gorseli === false) return true;
  if (parsed.site_image === false || parsed.is_site_image === false || parsed.saha_kaydi_uygun === false) return true;
  return /(şantiye dışı|santiye disi|inşaat sahası değil|insaat sahasi degil|construction site değil|not a construction|not construction|not a site image|saha kaydı oluşturmaya uygun değil)/i.test(joined);
}

function kpAiSection(title, bodyHtml) {
  return '<section style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:14px;display:grid;gap:10px;">'
    + '<div style="font-size:11px;font-weight:900;color:#475569;text-transform:uppercase;letter-spacing:0.06em;">' + kpAiEsc(title) + '</div>'
    + bodyHtml
    + '</section>';
}

function kpAiListHtml(items, emptyText) {
  const arr = kpAiArray(items).map(item => {
    if (typeof item === 'object') {
      const label = item.aciklama || item.label || item.class || item.name || item.ozet || item.description || item.type || item.risk || '';
      if (label) {
        const confidence = item.confidence ? ' (' + Math.round(Number(item.confidence) * 100) + '%)' : '';
        return String(label).replace(/_/g, ' ') + confidence;
      }
      return Object.entries(item)
        .filter(([key]) => !['box', 'bbox', 'normalized_boxes', 'yolo_boxes'].includes(key))
        .map(([key, val]) => key + ': ' + val)
        .join(', ');
    }
    return item;
  }).filter(Boolean);
  if (!arr.length) return '<div style="font-size:13px;color:#64748B;line-height:1.6;">' + kpAiEsc(emptyText || 'Belirgin kayıt yok.') + '</div>';
  return '<ul style="margin:0;padding-left:18px;display:grid;gap:6px;font-size:13px;color:#334155;line-height:1.55;">'
    + arr.map(x => '<li>' + kpAiEsc(kpAiNormalizeText(x)) + '</li>').join('')
    + '</ul>';
}

function kpAiParagraphsHtml(text, emptyText) {
  const clean = kpAiNormalizeText(text);
  if (!clean) return '<div style="font-size:13px;color:#64748B;line-height:1.6;">' + kpAiEsc(emptyText || 'AI bu bölüm için net bir açıklama üretmedi.') + '</div>';
  return clean.split(/\n{2,}/).map(p => '<p style="margin:0;color:#334155;font-size:13px;line-height:1.65;">' + kpAiEsc(p) + '</p>').join('');
}

function kpAiTechnicalHtml(text, emptyText) {
  const clean = kpAiNormalizeText(text);
  if (!clean) return '<div style="font-size:13px;color:#64748B;line-height:1.6;">' + kpAiEsc(emptyText || 'Teknik not bulunamadı.') + '</div>';
  const paragraphs = clean.split(/\n{2,}/).filter(Boolean);
  const preview = paragraphs.slice(0, 2).join('\n\n');
  const rest = paragraphs.slice(2).join('\n\n');
  const previewHtml = kpAiParagraphsHtml(preview);
  if (!rest || clean.length < 520) return previewHtml;
  return previewHtml
    + '<details style="margin-top:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:10px;">'
    + '<summary style="cursor:pointer;font-size:12px;font-weight:800;color:#475569;">Detaylı teknik yorumu göster</summary>'
    + '<div style="display:grid;gap:8px;margin-top:10px;">' + kpAiParagraphsHtml(rest) + '</div>'
    + '</details>';
}

function kpAiScoreCardsHtml(parsed) {
  const categories = parsed.kategoriler || parsed.categories || {};
  const entries = Object.entries(categories).filter(([,v]) => v && typeof v === 'object');
  if (!entries.length) return '';
  return '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px;">'
    + entries.map(([key, val]) => {
      const score = val.skor ?? val.score ?? val.puan ?? '—';
      const label = ({guvenlik:'Güvenlik', ilerleme:'İlerleme', malzeme:'Malzeme', risk:'Risk', kalite:'Kalite'}[key] || key);
      const note = val.durum || val.status || val.ozet || val.summary || '';
      return '<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:10px;">'
        + '<div style="font-size:18px;font-weight:900;color:#0F172A;">' + kpAiEsc(score) + '</div>'
        + '<div style="font-size:10px;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:0.05em;">' + kpAiEsc(label) + '</div>'
        + (note ? '<div style="font-size:11px;color:#64748B;margin-top:4px;line-height:1.35;">' + kpAiEsc(kpAiNormalizeText(note)) + '</div>' : '')
        + '</div>';
    }).join('')
    + '</div>';
}

function kpAiBuildReportHtml(record, rawText, yolo, thumb) {
  const { payload, parsed, visual } = kpAiParsedPayload(record, rawText);
  const nonSite = kpAiIsNonSite(record, parsed, rawText);
  const mdSections = kpAiMarkdownSections(rawText || record.description || record.ozet || '');
  const cleanBody = kpAiStripJsonFromText(rawText || record.description || record.ozet || '');
  const summary = parsed.ozet || parsed.summary || record.ai_summary || record.ozet || mdSections.summary || mdSections.intro || '';
  const risks = kpAiUnique([]
    .concat(kpAiArray(parsed.ihlaller || parsed.riskler || parsed.risks || parsed.safety_risks || parsed.normalized_boxes || visual.gemini_risk_boxes || []))
    .concat(kpAiSectionItems(mdSections.risks)));
  const recommendations = kpAiUnique([]
    .concat(kpAiArray(parsed.oneriler || parsed.öneriler || parsed.acil_onlemler || parsed.recommendations || parsed.actions || []))
    .concat(kpAiSectionItems(mdSections.recommendations)));
  const notes = parsed.teknik_notlar || parsed.technical_notes || parsed.notlar || parsed.notes || mdSections.notes || '';
  const mdDetections = kpAiSectionItems(mdSections.detections);
  const detections = kpAiUnique([]
    .concat(kpAiArray(parsed.tespitler || parsed.detected_objects || parsed.objects || visual.yolo_boxes || []))
    .concat(mdDetections)
    .concat(risks));
  const onemliAnlar = kpAiArray(parsed.onemli_anlar || parsed.important_moments || []);
  const isVideo = record.source === 'video_upload';
  const riskLevel = record.risk_level || parsed.risk_level || parsed.risk_seviyesi || (parsed.risk && parsed.risk.seviye) || (yolo && yolo.risk_level) || '';
  const typeLabel = record.detected_type || record.tip || record.event_type || 'genel';
  const riskTone = String(riskLevel).toLocaleLowerCase('tr-TR');
  const riskColor = riskTone.includes('yüksek') || riskTone.includes('high') ? '#DC2626' : riskTone.includes('orta') || riskTone.includes('medium') ? '#D97706' : '#15803D';
  const debugHtml = kpAiIsAdminUser()
     ? '<details style="background:#0F172A;border:1px solid #334155;border-radius:12px;padding:12px;"><summary style="cursor:pointer;color:#CBD5E1;font-size:12px;font-weight:800;">Ham AI Verisi</summary><pre style="white-space:pre-wrap;color:#CBD5E1;font-size:11px;line-height:1.5;overflow:auto;margin:12px 0 0;">' + kpAiEsc(JSON.stringify(payload && Object.keys(payload).length ? payload : (kpAiTryJson(rawText) || rawText || {}), null, 2)) + '</pre></details>'
    : '';
  const nonSiteWarning = nonSite
     ? '<div style="background:#FFF7ED;border:1px solid #FED7AA;color:#9A3412;border-radius:12px;padding:12px;font-size:13px;font-weight:700;line-height:1.5;">Bu görsel saha kaydı oluşturmaya uygun görünmüyor.</div>'
    : '';
  const storedVideo = isVideo ? (localStorage.getItem('bai_video_' + record.id) || '') : '';
  const imageHtml = storedVideo
    ? '<video src="' + kpAiEsc(storedVideo) + '" controls style="width:100%;max-height:360px;border-radius:12px;background:#0F172A;display:block;"></video>'
    : thumb
      ? '<img src="' + kpAiEsc(thumb) + '" style="width:100%;max-height:360px;object-fit:contain;border-radius:12px;background:#0F172A;display:block;">'
      : isVideo
        ? '<div style="height:180px;border-radius:12px;background:#0F172A;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;color:#94A3B8;font-size:13px;"><svg width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="#475569" stroke-width="1.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>Video önizleme bu oturumda mevcut değil</div>'
        : '<div style="height:180px;border-radius:12px;background:#F8FAFC;border:1px solid #E2E8F0;display:flex;align-items:center;justify-content:center;color:#94A3B8;font-size:13px;">Görsel önizleme yok</div>';
  return {
    nonSite,
    html: '<div style="display:grid;gap:14px;">'
      + '<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;">'
      + '<span style="background:' + (nonSite ? '#FFF7ED' : '#EFF6FF') + ';color:' + (nonSite ? '#C2410C' : '#1D4ED8') + ';border:1px solid ' + (nonSite ? '#FED7AA' : '#BFDBFE') + ';font-size:11px;font-weight:900;padding:5px 10px;border-radius:999px;">' + (nonSite ? 'Şantiye Dışı Görsel' : isVideo ? 'AI Video Analizi' : 'AI Fotoğraf Analizi') + '</span>'
      + '<span style="background:#F8FAFC;color:#475569;border:1px solid #E2E8F0;font-size:11px;font-weight:800;padding:5px 10px;border-radius:999px;">' + kpAiEsc(typeLabel) + '</span>'
      + (riskLevel ? '<span style="background:#FEF2F2;color:' + riskColor + ';border:1px solid #FECACA;font-size:11px;font-weight:900;padding:5px 10px;border-radius:999px;">Risk: ' + kpAiEsc(riskLevel) + '</span>' : '')
      + '</div>'
      + nonSiteWarning
      + kpAiScoreCardsHtml(parsed)
      + kpAiSection('Kısa Özet', kpAiParagraphsHtml(summary, 'Kısa özet bulunamadı.'))
      + kpAiSection('Tespitler', kpAiListHtml(detections, 'Belirgin nesne veya tespit listelenmedi.'))
      + kpAiSection('Riskler ve Sorunlar', kpAiListHtml(risks, nonSite ? 'Bu görsel saha olayı olarak sınıflandırılmadı.' : 'Belirgin risk listelenmedi.'))
      + kpAiSection('Öneriler', kpAiListHtml(recommendations, nonSite ? 'Saha kaydı oluşturmayın; doğru saha görseli yükleyin.' : 'Öneri bulunamadı.'))
      + kpAiSection('Teknik Notlar', kpAiTechnicalHtml(notes, 'Teknik not bulunamadı.'))
      + (onemliAnlar.length ? kpAiSection('Önemli Anlar', onemliAnlar.map(a => {
          const zaman = typeof a === 'object' ? (a.zaman || a.time || '') : '';
          const aciklama = typeof a === 'object' ? (a.aciklama || a.description || String(a)) : String(a);
          return '<div style="display:flex;gap:10px;align-items:flex-start;padding:8px 0;border-bottom:1px solid #F1F5F9;">'
            + (zaman ? '<span style="background:#F0FDF4;color:#15803D;border:1px solid #BBF7D0;border-radius:999px;font-size:11px;font-weight:800;padding:3px 9px;white-space:nowrap;">' + kpAiEsc(zaman) + '</span>' : '')
            + '<span style="font-size:13px;color:#334155;line-height:1.5;">' + kpAiEsc(aciklama) + '</span>'
            + '</div>';
        }).join('')) : '')
      + kpAiSection('İlgili Görsel / Kaynak', imageHtml)
      + debugHtml
      + '</div>'
  };
}

async function kpCameraCreateSahaKaydiFromAnalysis(analysisId, options = {}) {
  const record = (_kpTumAnaliz || []).find(k => Number(k.id) === Number(analysisId)) || {};
  const nonSite = options.nonSite || kpAiIsNonSite(record, {}, record.ozet || record.description || '');
  if (nonSite && !window.confirm('Bu görsel şantiye dışı görsel olarak işaretlendi. Yine de bekleyen saha kaydı oluşturulsun mu')) return;
  try {
    const token = localStorage.getItem('bai_token') || '';
    const res = await fetch('/api/camera-analysis/' + analysisId + '/create-saha-kaydi', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, santiye_id: kpCameraActiveSiteId() || record.santiye_id || null })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Saha kaydı oluşturulamadı.');
    if (typeof showToast === 'function') showToast('Bekleyen saha kaydı oluşturuldu.', 'success');
    const actionEl = document.getElementById('kpAiActionState-' + analysisId);
    const recordId = data && data.kayit && data.kayit.id ? Number(data.kayit.id) : 0;
    if (actionEl) {
      actionEl.innerHTML = '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
        + '<span style="font-size:12px;font-weight:900;color:#15803D;background:#DCFCE7;border:1px solid #BBF7D0;border-radius:999px;padding:7px 10px;">Saha kaydı oluşturuldu</span>'
        + '<button type="button" onclick="if (typeof navGit === \'function\') navGit(\'saha-kayitlari\');" style="font-size:12px;font-weight:800;color:#0F172A;background:#FFFFFF;border:1px solid #E2E8F0;padding:8px 12px;border-radius:10px;cursor:pointer;">Saha kaydına git</button>'
        + '</div>';
      if (recordId) actionEl.dataset.sahaKaydiId = String(recordId);
    }
    if (typeof kpManuelYukle === 'function') kpManuelYukle();
    return data;
  } catch(e) {
    if (typeof showToast === 'function') showToast(e.message || 'Saha kaydı oluşturulamadı.', 'error');
    return null;
  }
}

if (!window.kpKameraAnalizdenSahaKaydiOlustur) {
  window.kpKameraAnalizdenSahaKaydiOlustur = kpCameraCreateSahaKaydiFromAnalysis;
}

// â"€â"€ Kart Detay Modal ?? temiz AI raporu + görsel + aksiyonlar
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
  modal.innerHTML = '<div style="background:#F8FAFC;border-radius:20px;width:100%;max-width:860px;max-height:92vh;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 28px 80px rgba(0,0,0,0.55);">'
    + '<div style="display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid rgba(255,255,255,0.07);flex-shrink:0;">'
    + '<div style="display:flex;align-items:center;gap:8px;">'
    + '<div style="width:8px;height:8px;border-radius:50%;background:#818cf8;"></div>'
    + '<span style="font-size:14px;font-weight:800;color:#0F172A;">AI Analiz Detayı</span>'
    + '</div>'
    + '<button onclick="kpKartDetayKapat()" style="width:32px;height:32px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;cursor:pointer;font-size:18px;color:#64748B;display:flex;align-items:center;justify-content:center;line-height:1;">×</button>'
    + '</div>'
    + '<div id="kpKartDetayIcerik" style="overflow-y:auto;flex:1;padding:20px;">'
    + '<div style="text-align:center;padding:48px;color:#475569;font-size:13px;">Yükleniyor...</div>'
    + '</div></div>';

  // Yerel önbellekten oku
  const thumb   = localStorage.getItem('bai_thumb_' + id);
  const yoloRaw = localStorage.getItem('bai_yolo_'  + id);
  const yolo    = yoloRaw ? (() => { try { return JSON.parse(yoloRaw); } catch(e) { return null; } })() : null;

  // Sunucudan AI içerik çek
  let aiContent = '', aiTip = 'genel', tarih = '', data = {};
  try {
    const res  = await fetch('/arsiv/kamera/' + id + '?token=' + token);
    data = await res.json();
    aiContent = data.content || data.sonuc || '';
    aiTip  = data.analiz_tipi || 'genel';
    tarih  = data.created_at ? new Date(data.created_at).toLocaleString('tr-TR') : '';
  } catch(e) { /* sunucu hatası ?? içerik boş kalır */ }

  const localRecord = (_kpTumAnaliz || []).find(k => Number(k.id) === Number(id)) || {};
  const record = Object.assign({}, localRecord, data || {});
  record.tip = record.tip || record.analiz_tipi || aiTip;
  record.ozet = record.ozet || record.ai_summary || record.description || '';
  const thumbFromRecord = localStorage.getItem('bai_thumb_' + id) || record.thumbnail_url || record.file_url || record.photo_url || '';
  const report = kpAiBuildReportHtml(record, aiContent, yolo, thumbFromRecord || thumb);
  const riskLevel = record.risk_level || (yolo ? yolo.risk_level : null);
  const tipRenk   = aiTip === 'guvenlik' ? '#D97706' : aiTip === 'ilerleme' ? '#2563EB' : '#7C3AED';
  const tipEtiket = aiTip === 'guvenlik' ? 'İş Güvenliği' : aiTip === 'ilerleme' ? 'İlerleme Takibi' : 'Genel Analiz';

  document.getElementById('kpKartDetayIcerik').innerHTML =
    '<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:14px;">'
    + '<div style="display:flex;gap:6px;flex-wrap:wrap;">'
    + '<span style="background:' + tipRenk + ';color:white;font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;">' + tipEtiket + '</span>'
    + (riskLevel ? '<span style="background:#FEF2F2;color:#B91C1C;font-size:11px;font-weight:800;padding:4px 12px;border-radius:20px;border:1px solid #FECACA;">' + kpAiEsc(riskLevel) + '</span>' : '')
    + '</div><span style="font-size:11px;color:#64748B;font-weight:700;">' + kpAiEsc(tarih) + '</span>'
    + '</div>'
    + report.html
    + kpAiSection('Aksiyonlar',
      '<div id="kpAiActionState-' + id + '" style="display:flex;gap:8px;flex-wrap:wrap;">'
      + '<button onclick="kpKartDetayKapat()" style="font-size:12px;font-weight:800;color:#0F172A;background:#FFFFFF;border:1px solid #E2E8F0;padding:9px 14px;border-radius:10px;cursor:pointer;">İncele tamam</button>'
      + '<button onclick="kpCameraCreateSahaKaydiFromAnalysis(' + id + ', { nonSite: ' + (report.nonSite ? 'true' : 'false') + ' })" style="font-size:12px;font-weight:800;color:white;background:' + (report.nonSite ? '#F97316' : '#0F172A') + ';border:none;padding:9px 14px;border-radius:10px;cursor:pointer;">Saha Kaydı Oluştur</button>'
      + '<button onclick="kpAnalizGizle(' + id + ');kpKartDetayKapat()" style="font-size:12px;font-weight:800;color:#DC2626;background:#FEF2F2;border:1px solid #FECACA;padding:9px 14px;border-radius:10px;cursor:pointer;">Arşivle</button>'
      + '</div>')
    + '</div>';
}

function kpKartDetayKapat() {
  const modal = document.getElementById('kpKartDetayModal');
  if (modal) modal.style.display = 'none';
}

function kpSortToggle() {
  _kpSortDesc = !_kpSortDesc;
  const btn = document.getElementById('kpSortBtn');
  if (btn) btn.textContent = _kpSortDesc ? '?" En Yeni' : '?‘ En Eski';
  kpRenderAiKartlar(_kpTumAnaliz);
}

// â"€â"€ Analiz sil (server-side + client-side)
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

// Bbox çizili thumbnail üret ?? bbox coords absolute pixels in original image
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
  const isVideo = file.type.startsWith('video/');
  const loading = document.getElementById('kpAnalysisLoading');
  if (loading) {
    loading.style.display = 'block';
    const txt = document.getElementById('kpAnalysisLoadingText');
    const sub = document.getElementById('kpAnalysisLoadingSubtext');
    if (txt) txt.textContent = isVideo ? 'Video analiz ediliyor...' : 'AI analiz yapıyor...';
    if (sub) sub.textContent = isVideo ? 'Video yükleniyor ve işleniyor, bu birkaç dakika sürebilir' : 'Fotoğraf işleniyor, lütfen bekleyin';
  }

  try {
    const base64 = await new Promise((res, rej) => {
      const r = new FileReader();
      r.onload = e => res(e.target.result.split(',')[1]);
      r.onerror = rej;
      r.readAsDataURL(file);
    });
    const token = localStorage.getItem('bai_token');
    const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'İstanbul';
    const imgData = isVideo ? null : 'data:image/jpeg;base64,' + base64;
    const selectedSiteId = kpCameraActiveSiteId();
    kpCameraDebug('upload:start', {
      selectedSiteId,
      activeSantiyeId: window._aktifSantiyeId || null,
      activeSahaSite: (_kpAktifSantiye && _kpAktifSantiye.id) || null,
      activeType: _kpAktifTip
    });

    const container = document.getElementById('kpAiKartlar');
    const empty = document.getElementById('kpAiEmpty');
    if (container) {
      container.style.display = 'grid';
      if (empty) empty.style.display = 'none';
      const tempCard = document.createElement('div');
      tempCard.id = 'kpTempCard';
      tempCard.style.cssText = 'background:#FFFFFF;border:1px solid #E6EAF2;border-radius:22px;overflow:hidden;box-shadow:0 16px 34px rgba(15,23,42,0.08), inset 4px 0 0 rgba(244,63,94,0.65);';
      const thumbHtml = isVideo
        ? `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#0F172A;"><svg width="40" height="40" fill="none" viewBox="0 0 24 24" stroke="#FFFFFF" stroke-width="1.5"><polygon points="5 3 19 12 5 21 5 3"/></svg></div>`
        : `<img src="${imgData}" style="width:100%;height:100%;object-fit:cover;opacity:0.58;">`;
      tempCard.innerHTML = `
        <div style="display:flex;gap:16px;align-items:stretch;padding:16px;">
          <div style="width:144px;min-width:144px;height:144px;border-radius:16px;overflow:hidden;position:relative;background:#0F172A;border:1px solid #E2E8F0;">
            ${thumbHtml}
            <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;background:linear-gradient(180deg,rgba(15,23,42,0.10),rgba(15,23,42,0.30));">
              <div style="width:24px;height:24px;border:3px solid #FFFFFF;border-top-color:transparent;border-radius:50%;animation:spin 0.8s linear infinite;"></div>
              <span style="color:white;font-size:11px;font-weight:700;letter-spacing:0.02em;">AI Analiz Ediyor...</span>
            </div>
          </div>
          <div style="min-width:0;flex:1;display:flex;flex-direction:column;gap:12px;justify-content:center;">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
              <div style="height:26px;width:102px;background:#EEF2FF;border-radius:999px;"></div>
              <div style="height:12px;width:66px;background:#E2E8F0;border-radius:999px;"></div>
            </div>
            <div style="height:18px;background:#E2E8F0;border-radius:999px;width:78%;"></div>
            <div style="height:12px;background:#F1F5F9;border-radius:999px;width:64%;"></div>
            <div style="display:flex;align-items:center;gap:10px;margin-top:6px;">
              <div style="width:28px;height:28px;border-radius:999px;background:#E2E8F0;"></div>
              <div style="height:12px;background:#F1F5F9;border-radius:999px;width:82px;"></div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;margin-top:auto;">
              <div style="height:42px;width:124px;background:#0F172A;border-radius:12px;"></div>
              <div style="width:42px;height:42px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;"></div>
            </div>
          </div>
        </div>`;
      container.insertBefore(tempCard, container.firstChild);
    }

    const [aiSettled, yoloSettled] = await Promise.allSettled([
      isVideo
        ? kpVideoAnalizGonder(base64, file.type, _kpAktifTip)
        : kpAnalizGonder(base64, _kpAktifTip),
      isVideo ? Promise.resolve(null) : fetch('/yolo/frame', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, resim_base64: base64, santiye_id: selectedSiteId })
      }).then(r => r.ok ? r.json() : null).catch(() => null)
    ]);

    const aiData = aiSettled.status === 'fulfilled' ? aiSettled.value : null;
    const yoloData = yoloSettled.status === 'fulfilled' ? yoloSettled.value : null;
    kpCameraDebug('upload:response', {
      aiStatus: aiSettled.status,
      yoloStatus: yoloSettled.status,
      analysisId: aiData && (aiData.analiz_id || aiData.id),
      responseSiteId: aiData && aiData.santiye_id,
      hasAnalysisObject: Boolean(aiData && aiData.analysis),
      yoloId: yoloData && yoloData.analiz_id
    });
    if (!aiData || !aiData.analiz_id) {
      if (aiSettled.status === 'rejected') throw (aiSettled.reason || new Error('AI yanıtı alınamadı'));
      if (!aiData) return;
      showToast('Analiz tamamlandı ancak kayıt kimliği dönmedi. Lütfen tekrar deneyin.', 'error');
      return;
    }

    // Video için localStorage'a kaydet (detay panelinde <video> göstermek için)
    if (isVideo && aiData.analiz_id) {
      try {
        const videoDataUrl = file.type + ';base64,' + base64;
        // Sadece ~4MB altındaki videolar için kaydet (localStorage sınırı)
        if (base64.length < 5_400_000) {
          localStorage.setItem('bai_video_' + aiData.analiz_id, 'data:' + videoDataUrl);
        }
      } catch(e) { /* localStorage dolu olabilir, önemli değil */ }
    }

    let ozetMetni = '';
    if (aiData.parsed && typeof aiData.parsed === 'object') {
      ozetMetni = aiData.parsed.ozet || aiData.parsed.summary || '';
      if (!ozetMetni && Array.isArray(aiData.parsed.ihlaller) && aiData.parsed.ihlaller.length) {
        ozetMetni = aiData.parsed.ihlaller
          .map(ihlal => ihlal && ihlal.aciklama ? ihlal.aciklama : '')
          .filter(Boolean)
          .join('. ');
      }
    }
    if (!ozetMetni) ozetMetni = aiData.analiz_metni || aiData.cevap || 'AI analiz kaydı';
    ozetMetni = String(ozetMetni).replace(/\s+/g, ' ').trim();
    if (ozetMetni.length > 150) ozetMetni = ozetMetni.substring(0, 150) + '...';

    const savedAnalysis = aiData.analysis && typeof aiData.analysis === 'object' ? aiData.analysis : null;
    const yeniKayit = savedAnalysis || {
      id: aiData.analiz_id,
      tip: aiData.analiz_tipi || _kpAktifTip || 'genel',
      ozet: ozetMetni || 'AI analiz kaydı',
      sehir,
      status: 'ready',
      thumbnail_url: aiData.thumbnail_url || imgData,
      file_url: aiData.file_url || imgData,
      santiye_id: aiData.santiye_id || selectedSiteId,
      santiye_adi: aiData.santiye_adi || ((_kpAktifSantiye && _kpAktifSantiye.ad) || ''),
      created_at: new Date().toISOString()
    };
    yeniKayit.id = yeniKayit.id || aiData.analiz_id;
    yeniKayit.tip = yeniKayit.tip || yeniKayit.event_type || aiData.analiz_tipi || _kpAktifTip || 'genel';
    yeniKayit.ozet = yeniKayit.ozet || yeniKayit.ai_summary || yeniKayit.description || ozetMetni || 'AI analiz kaydı';
    yeniKayit.status = yeniKayit.status || 'ready';
    yeniKayit.thumbnail_url = yeniKayit.thumbnail_url || aiData.thumbnail_url || imgData;
    yeniKayit.file_url = yeniKayit.file_url || aiData.file_url || imgData;
    yeniKayit.santiye_id = yeniKayit.santiye_id || aiData.santiye_id || selectedSiteId;

    _kpTumAnaliz = [yeniKayit].concat((_kpTumAnaliz || []).filter(k => k.id !== yeniKayit.id));
    if (typeof _arsivData !== 'undefined' && _arsivData) {
      _arsivData.kamera_analizler = [yeniKayit].concat(((_arsivData.kamera_analizler || []).filter(k => k.id !== yeniKayit.id)));
    }

    const tespitler = (yoloData && yoloData.tespitler) ? yoloData.tespitler : [];
    const annotated = await kpBboxThumb(base64, tespitler).catch(() => imgData);
    try {
      localStorage.setItem('bai_thumb_' + aiData.analiz_id, annotated);
      if (yoloData) localStorage.setItem('bai_yolo_' + aiData.analiz_id, JSON.stringify(yoloData));
    } catch(e) {
      showToast('Önizleme önbelleğe alınamadı, kayıt yine de eklendi.', 'warning');
    }

    kpRenderAiKartlar(_kpTumAnaliz);
    kpCameraDebug('upload:rendered-local', {
      savedAnalysisId: yeniKayit.id,
      listLength: (_kpTumAnaliz || []).length,
      selectedSiteId,
      activeChip: _kpAktifChip,
      search: (document.getElementById('kameraArama') || {}).value || '',
      domItemCount: document.querySelectorAll('#kpAiKartlar > div').length
    });
    const gunEl = document.getElementById('kpAnalizGunAdet');
    if (gunEl) {
      const dates = _kpTumAnaliz.map(k => new Date(k.created_at).toDateString());
      gunEl.textContent = new Set(dates).size;
    }
    showToast('AI analiz tamamlandı!', 'success');
    await kameraPageYukle(yeniKayit);
  } catch(e) {
    showToast('Analiz zinciri tamamlanamadı: ' + e.message, 'error');
  } finally {
    const tc = document.getElementById('kpTempCard');
    if (tc) tc.remove();
    if (loading) loading.style.display = 'none';
    event.target.value = '';
  }
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
  const selectedSiteId = kpCameraActiveSiteId();
  try {
    const res = await fetch('/kamera-analiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, resim_base64: base64, analiz_tipi, hava, sehir, dil: aktifDil, santiye_id: selectedSiteId })
    });
    const data = await res.json();
    kpCameraDebug('api:kamera-analiz', {
      ok: res.ok,
      status: res.status,
      selectedSiteId,
      analysisId: data && (data.analiz_id || data.id),
      responseSiteId: data && data.santiye_id,
      hasSummary: Boolean(data && (data.ai_summary || data.analiz_metni || data.cevap))
    });
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
    return data;
  } catch(e) {
    showToast('Analiz hatası: ' + e.message, 'error');
    return null;
  }
}

async function kpVideoAnalizGonder(base64, mimeType, analiz_tipi) {
  const token = localStorage.getItem('bai_token');
  const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'İstanbul';
  const selectedSiteId = kpCameraActiveSiteId();
  try {
    const res = await fetch('/kamera-analiz', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        token,
        video_base64: base64,
        video_mime_type: mimeType,
        analiz_tipi,
        hava: '',
        sehir,
        dil: aktifDil,
        santiye_id: selectedSiteId
      })
    });
    const data = await res.json();
    if (!res.ok) {
      if (res.status === 429) {
        showToast('Limit doldu: ' + (data.detail || ''), 'error');
      } else if (res.status === 503) {
        showToast('AI servisi şu an yoğun, lütfen tekrar deneyin.', 'error');
      } else {
        showToast('Video analiz hatası: ' + (data.detail || res.status), 'error');
      }
      return null;
    }
    return data;
  } catch(e) {
    showToast('Video analiz hatası: ' + e.message, 'error');
    return null;
  }
}

async function kameraPageYukle(preserveRecord) {
  const token = localStorage.getItem('bai_token');
  if (!token) return false;
  try {
    const selectedSiteId = kpCameraActiveSiteId();
    const beforeDomCount = document.querySelectorAll('#kpAiKartlar > div').length;
    const res  = await fetch('/api/camera-analyses?token=' + token);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'AI kayıtları alınamadı');
    _kpTumAnaliz = Array.isArray(data.items)
       ? data.items
      : (Array.isArray(data.kamera_analizler) ? data.kamera_analizler : []);
    if (preserveRecord && preserveRecord.id && !_kpTumAnaliz.some(k => Number(k.id) === Number(preserveRecord.id))) {
      _kpTumAnaliz = [preserveRecord].concat(_kpTumAnaliz);
    }
    if (typeof _arsivData !== 'undefined' && _arsivData) {
      _arsivData.kamera_analizler = _kpTumAnaliz;
    }
    kpRenderAiKartlar(_kpTumAnaliz);
    kpCameraDebug('list:loaded', {
      selectedSiteId,
      currentFilter: { chip: _kpAktifChip, search: (document.getElementById('kameraArama') || {}).value || '' },
      responseLength: _kpTumAnaliz.length,
      preserveRecordId: preserveRecord && preserveRecord.id,
      beforeDomCount,
      afterDomCount: document.querySelectorAll('#kpAiKartlar > div').length
    });
    kpLimitGuncelle();
    // Analiz günlerini hesapla
    const gunEl = document.getElementById('kpAnalizGunAdet');
    if (gunEl) {
      if (_kpTumAnaliz.length > 0) {
        const dates = _kpTumAnaliz.map(k => new Date(k.created_at).toDateString());
        const uniqueDays = new Set(dates).size;
        gunEl.textContent = uniqueDays;
      } else {
        gunEl.textContent = '0';
      }
    }
    return true;
  } catch(e) {
    showToast('AI kayıtları yenilenemedi: ' + e.message, 'error');
    kpRenderAiKartlar(_kpTumAnaliz);
    return false;
  }
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
      (k.ozet || '').toLowerCase().includes(arama.toLowerCase()) ||
      (k.tip || '').toLowerCase().includes(arama.toLowerCase()) ||
      (k.sehir || '').toLowerCase().includes(arama.toLowerCase())
    );
  }
  const beforeDomCount = container.children ? container.children.length : 0;
  const gorunen = filtreli.filter(k => !k.archived);
  kpCameraDebug('render:ai-cards', {
    inputLength: (liste || []).length,
    filteredLength: filtreli.length,
    visibleLength: gorunen.length,
    selectedSiteId: kpCameraActiveSiteId(),
    activeChip: _kpAktifChip,
    search: arama,
    beforeDomCount
  });

  gorunen.sort((a, b) => {
    const da = new Date(a.created_at || 0);
    const db = new Date(b.created_at || 0);
    return _kpSortDesc ? db - da : da - db;
  });

  if (badge) badge.textContent = gorunen.length;
  if (gorunen.length === 0) {
    container.innerHTML = '';
    container.style.display = 'none';
    if (empty) empty.style.display = 'block';
    kpRenderTespitAkisi([]);
    kpRenderStats([]);
    return;
  }

  const containerWidth = container.clientWidth || window.innerWidth || 0;
  const aiKartMobil = containerWidth <= 560;
  container.style.display = 'grid';
  container.style.gridTemplateColumns = 'repeat(auto-fit,minmax(' + (containerWidth <= 640 ? 240 : 320) + 'px,1fr))';
  container.style.gap = '18px';
  if (empty) empty.style.display = 'none';
  kpRenderTespitAkisi(gorunen);
  kpRenderStats(gorunen);

  const cardsHtml = gorunen.map(k => {
    const tip = k.tip || 'genel';
    const parsedForCard = kpAiParsedPayload(k, k.description || k.ozet || '').parsed;
    const nonSite = kpAiIsNonSite(k, parsedForCard, k.description || k.ozet || '');
    const badgeInfo = nonSite
       ? { text: 'ŞANTİYE DIŞI GÖRSEL', color: '#C2410C', bg: '#FFF7ED' }
      : tip === 'guvenlik'
       ? { text: 'UYARI', color: '#F97316', bg: '#FFF7ED' }
      : tip === 'ilerleme'
         ? { text: 'İLERLEME', color: '#2563EB', bg: '#EFF6FF' }
        : { text: 'AI TESPİT', color: '#475569', bg: '#F8FAFC' };
    const dt        = k.created_at ? new Date(k.created_at) : null;
    const tarihSat  = dt ? dt.toLocaleTimeString('tr-TR', {hour:'2-digit',minute:'2-digit',second:'2-digit'}) : '--:--:--';
    const baslikRaw = kpAiStripJsonFromText(k.ozet || k.ai_summary || k.description || '').replace(/#{1,6}\s*/g, '').replace(/\*\*/g, '').replace(/\*/g, '').replace(/`/g, '').trim();
    const baslik = ((baslikRaw.split('.')[0] || baslikRaw || (nonSite ? 'Şantiye dışı görsel' : 'Kamera Kaydı')).substring(0,64));
    const kameraAdi = k.camera_name || k.kamera_adi || k.kamera || 'Kamera Kaydı';
    const konum     = k.location || k.konum || k.sehir || 'Konum belirtilmedi';
    const kullanici = k.user_name || k.kullanici || k.created_by || 'AI Sistem';
    const avatar    = (kullanici.split(' ').map(x => x && x[0] ? x[0] : '').join('').substring(0, 2) || 'AI').toUpperCase();
    const accent    = nonSite ? 'rgba(249,115,22,0.62)' : tip === 'guvenlik' ? 'rgba(244,63,94,0.62)' : tip === 'ilerleme' ? 'rgba(245,158,11,0.60)' : 'rgba(59,130,246,0.58)';
    const thumb     = localStorage.getItem('bai_thumb_' + k.id) || k.thumbnail_url || k.file_url || '';
    const thumbHtml = thumb
       ? '<img src="' + thumb + '" style="width:100%;height:100%;object-fit:cover;display:block;">'
      : '<div style="width:100%;height:100%;background:linear-gradient(135deg,#E0ECFF,#F7FAFF);display:flex;align-items:center;justify-content:center;">'
        + '<svg width="34" height="34" fill="none" viewBox="0 0 24 24" stroke="#3B82F6" stroke-width="1.6"><path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/></svg></div>';

    return '<div onclick="kpKartDetayGoster(' + k.id + ')" style="min-width:0;background:#FFFFFF;border:1px solid #E6EAF2;border-radius:22px;box-shadow:0 16px 34px rgba(15,23,42,0.08), inset 4px 0 0 ' + accent + ';padding:16px;display:flex;flex-direction:' + (aiKartMobil ? 'column' : 'row') + ';gap:16px;align-items:' + (aiKartMobil ? 'stretch' : 'center') + ';cursor:pointer;transition:transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;overflow:visible;" onmouseover="this.style.transform=\'translateY(-2px)\';this.style.boxShadow=\'0 22px 42px rgba(15,23,42,0.12), inset 4px 0 0 ' + accent + '\';this.style.borderColor=\'#D7DEE9\'" onmouseout="this.style.transform=\'none\';this.style.boxShadow=\'0 16px 34px rgba(15,23,42,0.08), inset 4px 0 0 ' + accent + '\';this.style.borderColor=\'#E6EAF2\'">'
      + '<div style="width:' + (aiKartMobil ? '100%' : '148px') + ';min-width:' + (aiKartMobil ? '100%' : '148px') + ';height:' + (aiKartMobil ? '190px' : '148px') + ';border-radius:18px;overflow:hidden;background:#F8FAFC;border:1px solid #E2E8F0;flex-shrink:0;box-shadow:inset 0 1px 0 rgba(255,255,255,0.72);">' + thumbHtml + '</div>'
      + '<div style="min-width:0;flex:1;display:flex;flex-direction:column;gap:12px;align-self:stretch;">'
      + '<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;">'
      + '<div style="display:inline-flex;align-items:center;gap:6px;min-width:0;background:' + badgeInfo.bg + ';color:' + badgeInfo.color + ';border:1px solid rgba(148,163,184,0.12);border-radius:999px;padding:6px 11px;font-size:10px;font-weight:800;letter-spacing:0.03em;text-transform:uppercase;">' + badgeInfo.text + '</div>'
      + '<div style="font-size:12px;font-weight:700;color:#64748B;white-space:nowrap;">' + tarihSat + '</div>'
      + '</div>'
      + '<div style="font-size:16px;font-weight:800;color:#0F172A;line-height:1.18;letter-spacing:-0.01em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">' + baslik + '</div>'
      + '<div style="font-size:12px;color:#64748B;line-height:1.5;display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden;"><span style="font-weight:700;color:#334155;">' + kameraAdi + '</span><span style="color:#94A3B8;"> ? </span>' + konum + '</div>'
      + '<div style="height:2px;"></div>'
      + '<div style="display:flex;align-items:center;gap:10px;">'
      + '<div style="width:32px;height:32px;border-radius:999px;background:#F8FAFC;border:1px solid #E2E8F0;color:#0F172A;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;flex-shrink:0;">' + avatar + '</div>'
      + '<span style="font-size:13px;font-weight:700;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + kullanici + '</span>'
      + '</div>'
      + (nonSite ? '<div style="font-size:12px;color:#9A3412;background:#FFF7ED;border:1px solid #FED7AA;border-radius:10px;padding:8px 10px;line-height:1.4;">Bu görsel saha kaydı oluşturmaya uygun görünmüyor.</div>' : '')
      + '<div style="display:flex;align-items:center;gap:8px;margin-top:auto;padding-top:2px;flex-wrap:wrap;">'
      + '<button onclick="event.stopPropagation();kpKartDetayGoster(' + k.id + ')" style="min-width:118px;height:42px;display:inline-flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#FFFFFF;background:#102A72;border:none;padding:0 18px;border-radius:10px;cursor:pointer;letter-spacing:0.01em;box-shadow:0 10px 22px rgba(16,42,114,0.18);white-space:nowrap;">İNCELE</button>'
      + '<button onclick="event.stopPropagation();kpCameraCreateSahaKaydiFromAnalysis(' + k.id + ', { nonSite: ' + (nonSite ? 'true' : 'false') + ' })" style="height:42px;display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:' + (nonSite ? '#9A3412' : '#0F172A') + ';background:' + (nonSite ? '#FFF7ED' : '#FFFFFF') + ';border:1px solid ' + (nonSite ? '#FED7AA' : '#E2E8F0') + ';padding:0 12px;border-radius:10px;cursor:pointer;white-space:nowrap;">Saha Kaydı Oluştur</button>'
      + '<button onclick="event.stopPropagation();kpAnalizGizle(' + k.id + ')" style="height:42px;display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:#DC2626;background:#FEF2F2;border:1px solid #FECACA;padding:0 12px;border-radius:10px;cursor:pointer;white-space:nowrap;">Arşivle</button>'
      + '</div>'
      + '</div>'
      + '</div>';
  }).join('');

  container.innerHTML = cardsHtml;
  kpCameraDebug('render:ai-cards:done', { afterDomCount: container.children ? container.children.length : 0 });
}

function kpRenderTespitAkisi(liste) {
  const container = document.getElementById('kpTespitAkis');
  if (!container) return;
  liste = (liste || []).filter(k => !kpAiIsNonSite(k, kpAiParsedPayload(k, k.description || k.ozet || '').parsed, k.description || k.ozet || ''));
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
    const rawBaslik = (k.ozet || '').replace(/#{1,6}\s*/g,'').replace(/\*\*/g,'').replace(/\*/g,'').replace(/`/g,'').replace(/[📅???âŒ🔴🟡🟢]/gu,'').trim();
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
  const ihlal  = liste.filter(k => k.tip === 'guvenlik' && !kpAiIsNonSite(k, kpAiParsedPayload(k, k.description || k.ozet || '').parsed, k.description || k.ozet || '')).length;
  const el = (id, val) => { const e = document.getElementById(id); if (e) e.textContent = val; };
  el('kpStatToplam', toplam.toLocaleString('tr-TR'));
  el('kpStatIhlal',  ihlal);
  el('kpStatAi',     toplam);
  const badge = document.getElementById('kpAiBadge');
  if (badge) badge.textContent = toplam;
  // Delta göstergesi
  const deltaEl = document.getElementById('kpStatToplamDelta');
  if (deltaEl) deltaEl.textContent = toplam > 0 ? 'â–² aktif kayıt' : '?';
  const ihlalDelta = document.getElementById('kpStatIhlalDelta');
  if (ihlalDelta) {
    if (ihlal > 0) { ihlalDelta.textContent = '! Dikkat'; ihlalDelta.style.color = '#EF4444'; }
    else { ihlalDelta.textContent = '?'; ihlalDelta.style.color = '#64748B'; }
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
    if (txt) txt.textContent = k.kullanilan + ' / ' + (k.limit === -1 ? 'âˆ' : k.limit);
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
  const blob = new Blob([satirlar.join('n')], { type: 'text/csv;charset=utf-8;' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = 'kamera-analiz-logu.csv';
  a.click();
  URL.revokeObjectURL(url);
  showToast('Log dosyası indiriliyor...', 'success');
}

// ŞANTİYE SAYFASI ?? Tam sayfa liste görünümü
// ══════════════════════════════════════════
let _spVerisi = [];   // cache

function ekipRolLabel(role) {
  if (role === 'muhendis') return 'Mühendis';
  if (role === 'santi_sefi') return 'Şantiye Şefi';
  return role || 'Ekip';
}

async function ekipYukle() {
  const token = localStorage.getItem('bai_token') || '';
  const listEl = document.getElementById('ekipUyeleriListesi');
  const inviteEl = document.getElementById('bekleyenDavetListesi');
  if (!listEl && !inviteEl) return;

  if (listEl) listEl.innerHTML = '<div style="font-size:13px;color:#94A3B8;">Ekip yükleniyor...</div>';
  try {
    const res = await fetch(`/ekip?token=${encodeURIComponent(token)}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Ekip listesi alınamadı');
    const uyeler = Array.isArray(data.uyeler) ? data.uyeler : [];
    const visibleMembers = uyeler.filter((u) => !u.is_owner);
    if (listEl) {
      listEl.innerHTML = visibleMembers.length ? visibleMembers.map((u) => `
        <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:12px 14px;">
          <div style="min-width:0;">
            <div style="font-size:13px;font-weight:800;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${engineerEscapeHtml(u.ad || u.email)}</div>
            <div style="font-size:12px;color:#64748B;margin-top:2px;">${engineerEscapeHtml(u.email)} ? ${engineerEscapeHtml(u.santiye_adi || 'Tüm şantiyeler')}</div>
          </div>
          <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">
            <span style="font-size:11px;font-weight:800;color:#2563EB;background:#DBEAFE;border-radius:999px;padding:4px 9px;white-space:nowrap;">${engineerEscapeHtml(ekipRolLabel(u.rol))}</span>
            <button type="button" onclick="ekipUyeCikar(${Number(u.id)}, '${engineerEscapeHtml(u.email)}')" style="background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;border-radius:8px;padding:6px 9px;font-size:11px;font-weight:800;cursor:pointer;">Çıkar</button>
          </div>
        </div>
      `).join('') : `
        <div style="background:#F8FAFC;border:1px dashed #CBD5E1;border-radius:10px;padding:18px;text-align:center;">
          <div style="font-size:13px;font-weight:700;color:#475569;">Henüz ekip üyesi yok.</div>
          <button type="button" onclick="davetModalAc()" style="margin-top:10px;background:#2563EB;color:white;border:none;border-radius:8px;padding:9px 14px;font-size:13px;font-weight:700;cursor:pointer;">+ Mühendis Davet Et</button>
        </div>`;
    }
  } catch (err) {
    if (listEl) listEl.innerHTML = `<div style="font-size:13px;color:#DC2626;">${engineerEscapeHtml(err.message || 'Ekip listesi alınamadı')}</div>`;
  }

  if (!inviteEl) return;
  try {
    const res = await fetch(`/davetler?token=${encodeURIComponent(token)}`);
    const data = await res.json();
    if (!res.ok) {
      inviteEl.innerHTML = '';
      return;
    }
    const davetler = Array.isArray(data.davetler) ? data.davetler : [];
    inviteEl.innerHTML = davetler.length ? `
      <div style="font-size:12px;font-weight:800;color:#64748B;margin-top:4px;">Bekleyen Davetler</div>
      ${davetler.map((d) => `
        <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;background:#FFFBEB;border:1px solid #FDE68A;border-radius:10px;padding:10px 12px;">
          <div style="font-size:12px;color:#92400E;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${engineerEscapeHtml(d.email)}</div>
          <span style="font-size:11px;font-weight:800;color:#92400E;background:#FEF3C7;border-radius:999px;padding:3px 8px;">${engineerEscapeHtml(ekipRolLabel(d.rol))}</span>
        </div>
      `).join('')}` : '';
  } catch (err) {
    inviteEl.innerHTML = '';
  }
}

async function ekipUyeCikar(memberId, email) {
  const label = email ? ` (${email})` : '';
  if (!confirm(`Bu üyeyi${label} ekipten çıkarmak istediğinize emin misiniz`)) return;
  const token = localStorage.getItem('bai_token') || '';
  try {
    const res = await fetch('/ekip/cikar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, member_id: memberId })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Çıkarma işlemi başarısız');
    showToast('Üye ekipten çıkarıldı', 'success');
    ekipYukle();
  } catch (err) {
    showToast('Hata: ' + (err.message || 'Bilinmeyen hata'), 'error');
  }
}

function davetModalEnsure() {
  let modal = document.getElementById('davetModal');
  if (modal) return modal;
  modal = document.createElement('div');
  modal.id = 'davetModal';
  modal.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(15,23,42,0.55);z-index:9999;align-items:center;justify-content:center;padding:20px;';
  modal.innerHTML = `
    <div style="width:min(560px,100%);background:#FFFFFF;border-radius:12px;border:1px solid #E2E8F0;box-shadow:0 24px 70px rgba(15,23,42,0.25);overflow:hidden;">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:18px 20px;border-bottom:1px solid #E2E8F0;">
        <div>
          <div style="font-size:16px;font-weight:800;color:#0F172A;">Ekibe Davet Et</div>
          <div style="font-size:12px;color:#64748B;margin-top:3px;">Yöntem seçin ve davet gönderin</div>
        </div>
        <button type="button" onclick="davetModalKapat()" style="background:#F1F5F9;border:1px solid #E2E8F0;border-radius:8px;width:34px;height:34px;cursor:pointer;">×</button>
      </div>

      <!-- Sekme seçici -->
      <div style="display:flex;gap:0;border-bottom:1px solid #E2E8F0;">
        <button id="davetTabEmail" onclick="davetTabSec('email')" style="flex:1;padding:12px;font-size:13px;font-weight:700;border:none;border-bottom:2px solid #2563EB;background:#F8FAFC;color:#2563EB;cursor:pointer;">📱 Email ile Davet</button>
        <button id="davetTabLink" ? onclick="davetTabSec('link')" ? style="flex:1;padding:12px;font-size:13px;font-weight:700;border:none;border-bottom:2px solid transparent;background:#FFFFFF;color:#64748B;cursor:pointer;">🔐— Link Oluştur</button>
      </div>

      <div style="padding:20px;display:flex;flex-direction:column;gap:14px;">

        <!-- Email alanı (sadece email modunda) -->
        <div id="davetEmailField">
          <label style="font-size:12px;font-weight:700;color:#64748B;display:block;margin-bottom:6px;">E-posta</label>
          <input id="davetEmail" type="email" placeholder="muhendis@email.com" style="width:100%;box-sizing:border-box;padding:11px 12px;border:1px solid #E2E8F0;border-radius:8px;font-size:14px;">
        </div>

        <div>
          <label style="font-size:12px;font-weight:700;color:#64748B;display:block;margin-bottom:6px;">Rol</label>
          <select id="davetRol" style="width:100%;box-sizing:border-box;padding:11px 12px;border:1px solid #E2E8F0;border-radius:8px;font-size:14px;background:#FFFFFF;">
            <option value="muhendis">Mühendis</option>
            <option value="santi_sefi">Şantiye Şefi</option>
          </select>
        </div>

        <div>
          <div style="font-size:12px;font-weight:700;color:#64748B;margin-bottom:8px;">Şantiye Seçimi</div>
          <label style="display:flex;align-items:center;gap:8px;font-size:13px;color:#334155;margin-bottom:8px;">
            <input id="davetTumSantiyeler" type="checkbox" onchange="davetTumSantiyelerDegisti()"> Tüm şantiyeler (ayrıca seçin)
          </label>
          <div id="davetSantiyeListesi" style="display:flex;flex-direction:column;gap:6px;max-height:180px;overflow:auto;border:1px solid #E2E8F0;border-radius:8px;padding:10px;background:#F8FAFC;"></div>
        </div>

        <div id="davetMsg" style="display:none;font-size:13px;line-height:1.5;padding:10px;border-radius:8px;"></div>
      </div>

      <div style="display:flex;justify-content:flex-end;gap:10px;padding:16px 20px;border-top:1px solid #E2E8F0;background:#F8FAFC;">
        <button type="button" onclick="davetModalKapat()" style="background:#FFFFFF;border:1px solid #CBD5E1;color:#334155;border-radius:8px;padding:10px 14px;font-weight:700;cursor:pointer;">Vazgeç</button>
        <button id="davetGonderBtn" type="button" onclick="davetGonder()" style="background:#2563EB;border:none;color:white;border-radius:8px;padding:10px 16px;font-weight:800;cursor:pointer;">Davet Gönder</button>
      </div>
    </div>`;
  document.body.appendChild(modal);
  return modal;
}

let _davetMod = 'email';

function davetTabSec(mod) {
  _davetMod = mod;
  const emailTab = document.getElementById('davetTabEmail');
  const linkTab  = document.getElementById('davetTabLink');
  const emailField = document.getElementById('davetEmailField');
  const btn = document.getElementById('davetGonderBtn');
  const msg = document.getElementById('davetMsg');
  if (msg) { msg.style.display = 'none'; msg.innerHTML = ''; }

  if (mod === 'email') {
    emailTab.style.borderBottomColor = '#2563EB'; emailTab.style.color = '#2563EB'; emailTab.style.background = '#F8FAFC';
    linkTab.style.borderBottomColor  = 'transparent'; linkTab.style.color  = '#64748B'; linkTab.style.background = '#FFFFFF';
    emailField.style.display = 'block';
    btn.textContent = 'Davet Gönder';
  } else {
    linkTab.style.borderBottomColor  = '#2563EB'; linkTab.style.color  = '#2563EB'; linkTab.style.background = '#F8FAFC';
    emailTab.style.borderBottomColor = 'transparent'; emailTab.style.color = '#64748B'; emailTab.style.background = '#FFFFFF';
    emailField.style.display = 'none';
    btn.textContent = 'Link Oluştur';
  }
}

function davetModalAc() {
  const modal = davetModalEnsure();
  davetTabSec('email');  // Her açılışta email sekmesine sıfırla
  const list = document.getElementById('davetSantiyeListesi');
  if (list) {
    list.innerHTML = (_spVerisi || []).length ? _spVerisi.map((s) => `
      <label style="display:flex;align-items:center;gap:8px;font-size:13px;color:#334155;">
        <input class="davetSantiyeCb" type="checkbox" value="${Number(s.id)}" ${Number(s.id) === Number(localStorage.getItem('bai_aktif_santiye')) ? 'checked' : ''}> ${engineerEscapeHtml(s.ad || 'Şantiye')}
      </label>
    `).join('') : '<div style="font-size:13px;color:#94A3B8;">Henüz şantiye yok. Boş bırakılırsa tüm şantiyeler kabul edilir.</div>';
  }
  const allCb = document.getElementById('davetTumSantiyeler');
  if (allCb) allCb.checked = false;
  davetTumSantiyelerDegisti();
  const emailInput = document.getElementById('davetEmail');
  if (emailInput) emailInput.value = '';
  modal.style.display = 'flex';
}

function davetModalKapat() {
  const modal = document.getElementById('davetModal');
  if (modal) modal.style.display = 'none';
}

function davetTumSantiyelerDegisti() {
  const all = document.getElementById('davetTumSantiyeler').checked;
  document.querySelectorAll('.davetSantiyeCb').forEach((cb) => {
    cb.disabled = all;
    if (all) cb.checked = false;
  });
}

async function davetGonder() {
  const token = localStorage.getItem('bai_token') || '';
  const email = _davetMod === 'email' ? (document.getElementById('davetEmail').value.trim() || '') : '';
  const role = document.getElementById('davetRol').value || 'muhendis';
  const msg = document.getElementById('davetMsg');
  const btn = document.getElementById('davetGonderBtn');
  const all = document.getElementById('davetTumSantiyeler').checked;
  const santiye_ids = all ? [] : Array.from(document.querySelectorAll('.davetSantiyeCb:checked')).map((cb) => Number(cb.value)).filter(Boolean);
  if (!all && !santiye_ids.length) {
    if (msg) { msg.style.display = 'block'; msg.textContent = 'Davet için en az bir proje seçin.'; }
    return;
  }

  if (_davetMod === 'email' && (!email || !email.includes('@'))) {
    if (msg) { msg.style.display = 'block'; msg.style.background = '#FEF2F2'; msg.style.color = '#DC2626'; msg.textContent = 'Geçerli bir e-posta girin.'; }
    return;
  }

  if (msg) { msg.style.display = 'block'; msg.style.background = '#F8FAFC'; msg.style.color = '#64748B'; msg.textContent = _davetMod === 'link' ? 'Link oluşturuluyor...' : 'Davet gönderiliyor...'; }
  if (btn) { btn.disabled = true; }

  try {
    const body = { token, role, santiye_ids };
    if (_davetMod === 'email') body.email = email;

    const res = await fetch('/davet-gonder', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'İşlem başarısız');

    if (msg) {
      msg.style.background = '#F0FDF4';
      msg.style.color = '#15803D';
      if (_davetMod === 'link') {
        msg.innerHTML = `<div style="margin-bottom:8px;font-weight:700;">🔐— Davet linkiniz hazır! Kopyalayıp WhatsApp'tan gönderin:</div>`
          + `<div style="display:flex;align-items:center;gap:8px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:8px;padding:10px 12px;">`
          + `<span id="davetLinkText" style="flex:1;word-break:break-all;font-size:13px;color:#2563EB;">${engineerEscapeHtml(data.davet_url || '')}</span>`
          + `<button onclick="navigator.clipboard.writeText('${engineerEscapeHtml(data.davet_url || '')}').then(()=>this.textContent='? Kopyalandı')" style="white-space:nowrap;background:#2563EB;color:#fff;border:none;border-radius:6px;padding:6px 10px;font-size:12px;font-weight:700;cursor:pointer;">Kopyala</button>`
          + `</div>`;
      } else {
        msg.innerHTML = `? Davet e-postası gönderildi: <b>${engineerEscapeHtml(email)}</b>`
          + (data.email_sent ? '' : `<br><span style="color:#64748B;font-size:12px;">Not: SMTP ayarlı değil, link elle paylaşılabilir:</span><br><span style="word-break:break-all;color:#2563EB;font-size:12px;">${engineerEscapeHtml(data.davet_url || '')}</span>`);
      }
    }
    ekipYukle();
  } catch (err) {
    if (msg) { msg.style.background = '#FEF2F2'; msg.style.color = '#DC2626'; msg.textContent = err.message || 'İşlem başarısız'; }
  } finally {
    if (btn) { btn.disabled = false; }
  }
}

function santiyePageAc() {
  // Ana içerik + command bar + diğer sayfaları gizle
  const content   = document.getElementById('content');
  const cmdBar    = document.getElementById('aiCommandBar');
  const spPage    = document.getElementById('santiyePage');
  if (!spPage) return;
  ['content','aiCommandBar','fiyatPage','stokPage','kameraPage','sahaKayitlariPage','arsivPage','hiyerarsiPage','hakedisPage','engineerDashboard','contractorDashboard'].forEach(pid => {
    const el = document.getElementById(pid);
    if (el) el.style.display = 'none';
  });
  spPage.style.display = 'flex';

  // Header başlık güncelle
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Şantiye Yönetimi Genel Bakış';

  // "+ Yeni Şantiye" butonunu header'da göster (sadece owner)
  const _spOwner = (() => { const u = JSON.parse(localStorage.getItem('bai_user') || '{}'); return u.is_owner === true || u.is_admin === true; })();
  let hBtn = document.getElementById('spHeaderBtn');
  if (!hBtn && _spOwner) {
    hBtn = document.createElement('button');
    hBtn.id = 'spHeaderBtn';
    hBtn.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> Yeni Şantiye';
    hBtn.style.cssText = 'background:#3B82F6;border:none;color:white;font-size:13px;font-weight:700;padding:8px 16px;border-radius:10px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:background 0.15s;';
    hBtn.onmouseover = () => hBtn.style.background = '#2563EB';
    hBtn.onmouseout  = () => hBtn.style.background = '#3B82F6';
    hBtn.onclick     = () => santiyeEkleModalAc(null);
    const headerRight = document.querySelector('#contentHeader > div:last-child');
    if (headerRight) headerRight.prepend(hBtn);
  } else if (hBtn) { hBtn.style.display = _spOwner ? 'flex' : 'none'; }
  _applyOwnerUI();

  santiyePageYukle();
}

function santiyePageKapat() {
  const content  = document.getElementById('content');
  const cmdBar   = document.getElementById('aiCommandBar');
  const spPage   = document.getElementById('santiyePage');
  if (spPage) spPage.style.display  = 'none';
  if (content) content.style.display = 'flex';
  if (cmdBar) cmdBar.style.display  = 'block';

  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Genel Bakış';

  const hBtn = document.getElementById('spHeaderBtn');
  if (hBtn) hBtn.style.display = 'none';
}

// ══════ FİYAT TAKİBİ SAYFASI ══════
const _fpCharts = {};
window._fpMalzemeMapDetay = {};

function _fpLog(step, data) {
  console.log('[FiyatTakip]', step, data || '');
}

function _fpWarn(step, data) {
  console.warn('[FiyatTakip]', step, data || '');
}

// â"€â"€ Scrape veri yardımcıları â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
window._fpMalzemeMap = {}; // kategori → malzeme_id (ilk kayıt)

function _fpAktifIl() {
  const selected = document.getElementById('globalSantiyeSecici')?.selectedOptions?.[0];
  const sources = [];
  // 1. En doğru kaynak: şu an seçili option'ın data-sehir'i
  if (selected?.getAttribute('data-sehir')) sources.push({ source: 'data-sehir', value: selected.getAttribute('data-sehir') });
  // 2. Şantiye değişince güncellenen global nesne
  if (window._kpAktifSantiye?.sehir) sources.push({ source: '_kpAktifSantiye.sehir', value: window._kpAktifSantiye.sehir });
  // 3. Şantiye değişince güncellenen localStorage
  const lsSehir = localStorage.getItem('bai_aktif_santiye_sehir');
  if (lsSehir) sources.push({ source: 'localStorage.bai_aktif_santiye_sehir', value: lsSehir });
  // 4. sehir yoksa konum'dan parse et (ilk virgülden önceki kısım)
  const konum = selected?.getAttribute('data-konum') || '';
  if (konum) {
    const parsed = konum.split(',')[0].trim();
    if (parsed) sources.push({ source: 'data-konum.parse', value: parsed });
  }
  // 5. Sayfa yüklendiğinde set edilen, eskiyebilir
  if (window._aktifSantiyeSehir) sources.push({ source: 'window._aktifSantiyeSehir', value: window._aktifSantiyeSehir });
  try {
    const storedSite = JSON.parse(localStorage.getItem('varsayilan_santiye') || '{}');
    if (storedSite?.sehir) sources.push({ source: 'localStorage.varsayilan_santiye.sehir', value: storedSite.sehir });
  } catch(e) {
    _fpWarn('varsayilan_santiye parse edilemedi', e);
  }
  const citySelect = document.getElementById('citySelect');
  if (citySelect?.value) sources.push({ source: 'citySelect.value', value: citySelect.value });
  const found = sources.find(s => String(s.value || '').trim());
  const il = found ? String(found.value).trim() : 'İstanbul';
  _fpLog('aktif il cikarimi', { il, selectedSource: found?.source || 'default:İstanbul', sources });
  return il;
}

function _fpGunToDonem(gun) {
  const g = parseInt(gun) || 90;
  if (g <= 30) return '1ay';
  if (g <= 90) return '3ay';
  if (g <= 180) return '6ay';
  return '1yil';
}

async function _fpMalzemeIdsYukle() {
  try {
    const token = localStorage.getItem('bai_token');
    _fpLog('_fpMalzemeIdsYukle basladi', { hasToken: !!token });
    const resp = await fetch('/api/malzemeler', { headers: { 'Authorization': 'Bearer ' + token } });
    _fpLog('/api/malzemeler status', { status: resp.status, ok: resp.ok });
    if (!resp.ok) {
      _fpWarn('/api/malzemeler basarisiz', { status: resp.status, text: await resp.text() });
      return;
    }
    const data = await resp.json();
    _fpLog('/api/malzemeler response', data);
    const byKategori = {};
    for (const m of (data.malzemeler || [])) {
      const current = byKategori[m.kategori];
      const mScore = (Number(m.scrape_kayit_sayisi || 0) > 0 ? 1000000 : 0) + Number(m.scrape_kayit_sayisi || 0);
      const currentScore = current ? ((Number(current.scrape_kayit_sayisi || 0) > 0 ? 1000000 : 0) + Number(current.scrape_kayit_sayisi || 0)) : -1;
      if (!current || mScore > currentScore) byKategori[m.kategori] = m;
    }
    const map = {};
    for (const [kategori, m] of Object.entries(byKategori)) map[kategori] = m.id;
    window._fpMalzemeMap = map;
    window._fpMalzemeMapDetay = byKategori;
    const mapByAd = {};
    for (const m of (data.malzemeler || [])) {
      if (m.ad) mapByAd[m.ad.toLowerCase()] = m.id;
    }
    window._fpMalzemeMapByAd = mapByAd;
    window._fpTumMalzemeler = data.malzemeler || [];
    _fpLog('_fpMalzemeMap hazir', { map, detay: byKategori });
  } catch(e) {
    _fpWarn('_fpMalzemeIdsYukle hata', e);
  }
}

function _fpHideAll() {
  if (typeof tumSayfalariGizle === 'function') {
    tumSayfalariGizle();
    return;
  }
  ['content','aiCommandBar','santiyePage','fiyatPage','stokPage','kameraPage','sahaKayitlariPage','arsivPage','hiyerarsiPage','hakedisPage','engineerDashboard'].forEach(id => {
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
  if (cmdBar) cmdBar.style.display  = 'block';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Genel Bakış';
}

async function aiPiyasaGuncelle(ev) {
    const btn = ev ? ev.target : null;
    const eskiText = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Güncelleniyor...'; }

    try {
        const token = localStorage.getItem('bai_token');
        const resp = await fetch('/fiyat-ai-guncelle', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ token: token })
        });
        const data = await resp.json();
        if (data.status === 'success' || data.basarili) {
            if (btn) { btn.textContent = 'Güncellendi!'; btn.style.background = '#10B981'; }
            setTimeout(() => {
                if (typeof fiyatPageYukle === 'function') fiyatPageYukle();
                if (btn) { btn.textContent = eskiText; btn.style.background = 'linear-gradient(135deg,#6366F1,#8B5CF6)'; btn.disabled = false; }
            }, 2000);
        } else {
            if (btn) { btn.textContent = 'Hata: ' + (data.detail || 'Bilinmeyen hata'); btn.style.background = '#EF4444'; }
            setTimeout(() => { if (btn) { btn.textContent = eskiText; btn.style.background = 'linear-gradient(135deg,#6366F1,#8B5CF6)'; btn.disabled = false; } }, 3000);
        }
    } catch(e) {
        if (btn) { btn.textContent = 'Bağlantı hatası'; btn.style.background = '#EF4444'; }
        setTimeout(() => { if (btn) { btn.textContent = eskiText; btn.style.background = 'linear-gradient(135deg,#6366F1,#8B5CF6)'; btn.disabled = false; } }, 3000);
    }
}

// â"€â"€ Fiyat Gir Modal â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function fiyatGirModalAc() {
    if (document.getElementById('fiyatGirModal')) {
        document.getElementById('fiyatGirModal').remove();
        return;
    }

    // ── Helpers ──────────────────────────────────────────────────────────────
    function _mkEl(tag, css, attrs) {
        var el = document.createElement(tag);
        if (css) el.style.cssText = css;
        if (attrs) Object.keys(attrs).forEach(function(k) { el.setAttribute(k, attrs[k]); });
        return el;
    }
    function _mkLabel(text) {
        var lbl = _mkEl('label', 'font-size:12px;color:#64748B;display:block;margin-bottom:4px;');
        lbl.textContent = text;
        return lbl;
    }
    function _mkInput(id, type, placeholder, css) {
        var inp = _mkEl('input', css || 'width:100%;padding:10px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:14px;box-sizing:border-box;');
        inp.id = id;
        inp.type = type;
        if (placeholder) inp.placeholder = placeholder;
        return inp;
    }
    var fieldCss = 'width:100%;padding:10px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:14px;box-sizing:border-box;';

    // ── Backdrop ─────────────────────────────────────────────────────────────
    var backdrop = _mkEl('div', 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.55);z-index:9998;display:flex;align-items:center;justify-content:center;');
    backdrop.id = 'fiyatGirModal';
    backdrop.addEventListener('click', function(e) { if (e.target === backdrop) backdrop.remove(); });

    // ── Panel ─────────────────────────────────────────────────────────────────
    var panel = _mkEl('div', 'background:#FFFFFF;border-radius:16px;padding:24px;width:440px;max-width:92vw;border:1px solid #E2E8F0;box-shadow:0 20px 60px rgba(0,0,0,0.25);z-index:9999;box-sizing:border-box;max-height:90vh;overflow-y:auto;');

    // Title row
    var titleRow = _mkEl('div', 'display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;');
    var title = _mkEl('h3', 'margin:0;color:#0F172A;font-size:16px;');
    title.textContent = 'Manuel Fiyat Girişi';
    var closeBtn = _mkEl('button', 'background:none;border:none;color:#64748B;font-size:20px;cursor:pointer;line-height:1;');
    closeBtn.textContent = '×';
    closeBtn.addEventListener('click', function() { backdrop.remove(); });
    titleRow.appendChild(title);
    titleRow.appendChild(closeBtn);
    panel.appendChild(titleRow);

    // Malzeme select
    var malzemeWrap = _mkEl('div', 'margin-bottom:12px;');
    malzemeWrap.appendChild(_mkLabel('Malzeme'));
    var select = _mkEl('select', fieldCss);
    select.id = 'fiyatGirMalzeme';
    var loadingOpt = document.createElement('option');
    loadingOpt.value = '';
    loadingOpt.textContent = 'Yükleniyor...';
    select.appendChild(loadingOpt);
    malzemeWrap.appendChild(select);
    panel.appendChild(malzemeWrap);

    // Fiyat + Tarih row
    var row1 = _mkEl('div', 'display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;');
    var fiyatWrap = _mkEl('div', '');
    fiyatWrap.appendChild(_mkLabel('Fiyat (₺)'));
    var fiyatInp = _mkInput('fiyatGirDeger', 'number', '28500', fieldCss);
    fiyatInp.setAttribute('step', '0.01');
    fiyatInp.setAttribute('min', '0');
    fiyatWrap.appendChild(fiyatInp);
    var tarihWrap = _mkEl('div', '');
    tarihWrap.appendChild(_mkLabel('Tarih'));
    var tarihInp = _mkInput('fiyatGirTarih', 'date', '', fieldCss);
    tarihInp.value = new Date().toISOString().slice(0, 10);
    tarihWrap.appendChild(tarihInp);
    row1.appendChild(fiyatWrap);
    row1.appendChild(tarihWrap);
    panel.appendChild(row1);

    // Tedarikçi
    var tedWrap = _mkEl('div', 'margin-bottom:12px;');
    tedWrap.appendChild(_mkLabel('Tedarikçi (isteğe bağlı)'));
    tedWrap.appendChild(_mkInput('fiyatGirTedarikci', 'text', 'ABC İnşaat Malzemeleri', fieldCss));
    panel.appendChild(tedWrap);

    // Miktar + İl row
    var row2 = _mkEl('div', 'display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;');
    var miktarWrap = _mkEl('div', '');
    miktarWrap.appendChild(_mkLabel('Miktar (isteğe bağlı)'));
    var miktarInp = _mkInput('fiyatGirMiktar', 'number', '5', fieldCss);
    miktarInp.setAttribute('step', '0.01');
    miktarInp.setAttribute('min', '0');
    miktarWrap.appendChild(miktarInp);
    var ilWrap = _mkEl('div', '');
    ilWrap.appendChild(_mkLabel('İl'));
    var ilInp = _mkInput('fiyatGirSehir', 'text', 'İstanbul', fieldCss);
    ilInp.setAttribute('readonly', '');
    var _sehir = (_fpAktifIl() || '').replace(/^["'\s]+|["'\s]+$/g, '') || 'İstanbul';
    ilInp.value = _sehir;
    ilWrap.appendChild(ilInp);
    row2.appendChild(miktarWrap);
    row2.appendChild(ilWrap);
    panel.appendChild(row2);

    // Hata / Başarı mesajları
    var hataEl = _mkEl('div', 'color:#EF4444;font-size:12px;margin-bottom:8px;display:none;');
    hataEl.id = 'fiyatGirHata';
    var basariEl = _mkEl('div', 'color:#10B981;font-size:12px;margin-bottom:8px;display:none;');
    basariEl.id = 'fiyatGirBasari';
    panel.appendChild(hataEl);
    panel.appendChild(basariEl);

    // Kaydet butonu
    var kaydetBtn = _mkEl('button', 'width:100%;padding:10px;background:#10B981;color:#fff;border:none;border-radius:8px;cursor:pointer;font-size:14px;font-weight:500;');
    kaydetBtn.textContent = 'Kaydet';
    kaydetBtn.addEventListener('click', fiyatGirKaydet);
    panel.appendChild(kaydetBtn);

    backdrop.appendChild(panel);
    document.body.appendChild(backdrop);

    // ── Malzeme listesini API'den yükle ──────────────────────────────────────
    (async function() {
        console.log('[FiyatGir] malzeme yükleniyor...');
        try {
            const token = localStorage.getItem('bai_token');
            const resp = await fetch('/api/malzemeler', {
                headers: { 'Authorization': 'Bearer ' + token }
            });
            console.log('[FiyatGir] /api/malzemeler status:', resp.status, resp.ok);
            const sel = document.getElementById('fiyatGirMalzeme');
            if (!sel) return;
            if (!resp.ok) {
                sel.options[0].textContent = 'Yüklenemedi (' + resp.status + ')';
                return;
            }
            const data = await resp.json();
            console.log('[FiyatGir] malzeme sayısı:', (data.malzemeler || []).length);
            const liste = data.malzemeler || [];
            if (liste.length === 0) {
                sel.options[0].textContent = 'Malzeme bulunamadı';
                return;
            }
            // Seçenekleri temizle ve doldur
            while (sel.options.length) sel.remove(0);
            var defaultOpt = document.createElement('option');
            defaultOpt.value = '';
            defaultOpt.textContent = '-- Malzeme seçin --';
            sel.appendChild(defaultOpt);

            var _aktifIds = window._fpAktifMalzemeIds;
            var aktifMalzemeler = window._fpAktifMalzemeler ||
                ['demir','celik_hasir','filmasin','cimento','kum','gazbeton'].map(function(k){return {malzeme:k,ozel:false};});
            var _defaultKats = new Set(['demir','celik_hasir','filmasin','cimento','kum','gazbeton']);
            var katAd = {demir:'Demir',celik_hasir:'Çelik Hasır',filmasin:'Filmaşin',cimento:'Çimento',beton:'Beton',kum:'Kum',gazbeton:'Gazbeton',tugla:'Tuğla',ozel:'Özel Malzemeler'};
            var byKat = {};
            liste.forEach(function(m) {
                var kat = m.kategori;
                if (_aktifIds && _aktifIds.size > 0) {
                    if (!_aktifIds.has(m.id)) return;
                } else {
                    if (kat !== 'ozel' && !_defaultKats.has(kat)) return;
                    if (kat === 'ozel') return;
                }
                if (!byKat[kat]) byKat[kat] = [];
                byKat[kat].push(m);
            });
            // Çimento alt_kategori filtresi: spesifik ID'ler aktifken gerek yok
            if (byKat['cimento'] && (!_aktifIds || _aktifIds.size === 0)) {
                var mainC = byKat['cimento'].filter(function(m) { return !m.alt_kategori; });
                byKat['cimento'] = mainC.length ? mainC : [byKat['cimento'][0]];
            }
            var _katSirasi = ['demir','celik_hasir','filmasin','cimento','kum','gazbeton','tugla','beton','ozel'];
            var siralanmis = _katSirasi.filter(function(k) { return byKat[k]; })
                .concat(Object.keys(byKat).filter(function(k) { return !_katSirasi.includes(k); }));
            siralanmis.forEach(function(kat) {
                var grp = document.createElement('optgroup');
                grp.label = katAd[kat] || (kat.charAt(0).toUpperCase() + kat.slice(1));
                byKat[kat].forEach(function(m) {
                    var opt = document.createElement('option');
                    opt.value = String(m.id);
                    opt.textContent = m.ad + ' (' + m.birim + ')';
                    grp.appendChild(opt);
                });
                sel.appendChild(grp);
            });
            console.log('[FiyatGir] dropdown dolduruldu, toplam option:', sel.options.length);
        } catch(e) {
            console.error('[FiyatGir] hata:', e);
            var sel2 = document.getElementById('fiyatGirMalzeme');
            if (sel2 && sel2.options.length) sel2.options[0].textContent = 'Bağlantı hatası: ' + e.message;
        }
    })();
}

async function fiyatGirKaydet() {
    const malzemeId = parseInt(document.getElementById('fiyatGirMalzeme').value);
    const fiyat = document.getElementById('fiyatGirDeger').value;
    const tarih = document.getElementById('fiyatGirTarih').value;
    const tedarikci = (document.getElementById('fiyatGirTedarikci').value || '').trim() || null;
    const miktarRaw = document.getElementById('fiyatGirMiktar').value;
    const miktar = miktarRaw ? parseFloat(miktarRaw) : null;
    const hata = document.getElementById('fiyatGirHata');
    const basari = document.getElementById('fiyatGirBasari');

    hata.style.display = 'none';
    basari.style.display = 'none';

    if (!malzemeId || !fiyat || parseFloat(fiyat) <= 0) {
        hata.textContent = 'Malzeme seçin ve geçerli bir fiyat girin';
        hata.style.display = 'block';
        return;
    }

    try {
        const token = localStorage.getItem('bai_token');
        const resp = await fetch('/api/fiyat/kullanici', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
            body: JSON.stringify({
                malzeme_id: malzemeId,
                fiyat: parseFloat(fiyat),
                tarih: tarih || new Date().toISOString().slice(0,10),
                tedarikci,
                miktar
            })
        });
        const data = await resp.json();
        if (!resp.ok) {
            hata.textContent = data.detail || data.mesaj || 'Hata: ' + resp.status;
            hata.style.display = 'block';
            return;
        }
        if (data.status === 'success') {
            basari.textContent = 'Fiyat kaydedildi! (ID: ' + data.id + ')';
            basari.style.display = 'block';
            document.getElementById('fiyatGirDeger').value = '';
            document.getElementById('fiyatGirTedarikci').value = '';
            document.getElementById('fiyatGirMiktar').value = '';
            setTimeout(() => {
                if (typeof fiyatPageYukle === 'function') fiyatPageYukle();
            }, 500);
        } else {
            hata.textContent = data.detail || 'Hata oluştu';
            hata.style.display = 'block';
        }
    } catch(e) {
        hata.textContent = 'Bağlantı hatası';
        hata.style.display = 'block';
    }
}

// ── Malzeme Katalog Verisi ───────────────────────────────────────────────────
var MALZEME_KATALOG = [
  { kategori: 'Kaba İnşaat', malzemeler: [], subgruplar: [
    { baslik: 'Demir', malzemeler: [
      {ad: 'Nervürlü Demir Ø8',  birim: 'ton', scrape_ad: 'Nervürlü Demir Ø8'},
      {ad: 'Nervürlü Demir Ø10', birim: 'ton', scrape_ad: 'Nervürlü Demir Ø10'},
      {ad: 'Nervürlü Demir Ø12', birim: 'ton', scrape_ad: 'Nervürlü Demir Ø12'},
    ]},
    { baslik: 'Çelik Hasır', malzemeler: [
      {ad: 'Çelik Hasır Q131', birim: 'ton', scrape_ad: 'Çelik Hasır Q131'},
      {ad: 'Çelik Hasır Q188', birim: 'ton', scrape_ad: 'Çelik Hasır Q188'},
    ]},
    { baslik: 'Filmaşin', malzemeler: [
      {ad: 'Filmaşin', birim: 'ton', scrape_ad: 'Filmaşin'},
    ]},
    { baslik: 'Çimento', malzemeler: [], dinamik: 'cimento' },
    { baslik: 'Kum', malzemeler: [
      {ad: 'Şap Kumu', birim: 'ton', scrape_ad: 'Şap Kumu'},
      {ad: 'Kaba Kum', birim: 'ton', scrape_ad: 'Kaba Kum'},
    ]},
    { baslik: 'Gazbeton', malzemeler: [
      {ad: 'Gazbeton G2/400 Düz Blok', birim: 'adet', scrape_ad: 'Gazbeton Düz Duvar Bloğu'},
    ]},
    { baslik: 'Hazır Beton', malzemeler: [
      {ad: 'C16/20 Hazır Beton', birim: 'm3'}, {ad: 'C20/25 Hazır Beton', birim: 'm3'},
      {ad: 'C25/30 Hazır Beton', birim: 'm3'}, {ad: 'C30/37 Hazır Beton', birim: 'm3'},
      {ad: 'C35/45 Hazır Beton', birim: 'm3'}, {ad: 'C40/50 Hazır Beton', birim: 'm3'},
      {ad: 'C45/55 Hazır Beton', birim: 'm3'}, {ad: 'C50/60 Hazır Beton', birim: 'm3'},
    ]},
    { baslik: 'Tuğla', malzemeler: [
      {ad: "Tuğla 8.5'luk", birim: 'adet'}, {ad: "Tuğla 10'luk", birim: 'adet'},
      {ad: "Tuğla 13.5'luk", birim: 'adet'}, {ad: "Tuğla 19'luk", birim: 'adet'},
      {ad: 'Tuğla Yığma', birim: 'adet'}, {ad: "Bims 10'luk", birim: 'adet'},
    ]},
  ]},
  { kategori: 'İnce İşçilik', malzemeler: [
    {ad: 'Seramik Yer 30x30', birim: 'm²'}, {ad: 'Seramik Yer 60x60', birim: 'm²'},
    {ad: 'Seramik Duvar', birim: 'm²'}, {ad: 'Fayans 20x25', birim: 'm²'}, {ad: 'Fayans 25x40', birim: 'm²'},
    {ad: 'Boya İç Cephe', birim: 'kg'}, {ad: 'Boya Dış Cephe', birim: 'kg'},
    {ad: 'Alçı Sıva', birim: 'torba'}, {ad: 'Parke / Laminat', birim: 'm²'},
    {ad: 'Mermer / Granit', birim: 'm²'}, {ad: 'Mozaik Taşı', birim: 'm²'}, {ad: 'Derz Dolgusu', birim: 'kg'}
  ]},
  { kategori: 'Yalıtım', malzemeler: [
    {ad: 'EPS (Strafor) Mantolama', birim: 'm²'}, {ad: 'XPS Levha', birim: 'm²'},
    {ad: 'Taş Yünü', birim: 'm²'}, {ad: 'Cam Yünü', birim: 'm²'}, {ad: 'Su Yalıtım Membranı', birim: 'm²'}
  ]},
  { kategori: 'Tesisat', malzemeler: [
    {ad: 'PPR Boru 20mm', birim: 'metre'}, {ad: 'PPR Boru 25mm', birim: 'metre'}, {ad: 'PPR Boru 32mm', birim: 'metre'},
    {ad: 'PVC Boru 50mm', birim: 'metre'}, {ad: 'PVC Boru 75mm', birim: 'metre'},
    {ad: 'PVC Boru 100mm', birim: 'metre'}, {ad: 'PVC Boru 125mm', birim: 'metre'},
    {ad: 'Pirinç Vana', birim: 'adet'}, {ad: 'Klozet / Lavabo', birim: 'adet'}, {ad: 'Batarya', birim: 'adet'}
  ]},
  { kategori: 'Elektrik', malzemeler: [
    {ad: 'NYM Kablo 2x1.5', birim: 'metre'}, {ad: 'NYM Kablo 3x1.5', birim: 'metre'}, {ad: 'NYM Kablo 3x2.5', birim: 'metre'},
    {ad: 'Priz / Anahtar', birim: 'adet'}, {ad: 'Sigorta Otomatiği', birim: 'adet'}, {ad: 'Aydınlatma Armatürü', birim: 'adet'}
  ]},
  { kategori: 'Çatı', malzemeler: [
    {ad: 'Kiremit Marsilya', birim: 'adet'}, {ad: 'Kiremit Oluklu', birim: 'adet'},
    {ad: 'Çatı Paneli Sandviç', birim: 'm²'}, {ad: 'Ahşap Çatı Makası', birim: 'm³'}
  ]},
  { kategori: 'Demir / Çelik', malzemeler: [
    {ad: 'Profil Demir Kutu', birim: 'kg'}, {ad: 'Profil Demir U', birim: 'kg'}, {ad: 'Profil Demir L', birim: 'kg'},
    {ad: 'Sac Levha', birim: 'kg'}, {ad: 'Çivi / Vida', birim: 'kg'}
  ]}
];
var _katalogSecilen = {};
var _aktifKatalog = MALZEME_KATALOG;  // dinamik olarak yeniden oluşturulur

function _buildDynamicKatalog() {
  var malzemeler = window._fpTumMalzemeler || [];
  if (!malzemeler.length) return MALZEME_KATALOG;

  // Sıralama: önce scrape verisi olanlar, sonra diğerleri
  var katMap = new Map();
  for (var m of malzemeler) {
    var kat = (m.kategori || 'Diğer');
    var altKat = (m.alt_kategori || '');
    if (!katMap.has(kat)) katMap.set(kat, new Map());
    var altMap = katMap.get(kat);
    if (!altMap.has(altKat)) altMap.set(altKat, []);
    altMap.get(altKat).push({ ad: m.ad, birim: m.birim || '', scrape_ad: m.ad, scrape_kayit_sayisi: m.scrape_kayit_sayisi || 0 });
  }

  var result = [];
  for (var [kategori, altMap] of katMap) {
    var altKeys = Array.from(altMap.keys());
    if (altKeys.length === 1 && altKeys[0] === '') {
      // alt_kategori yok — düz liste
      result.push({ kategori: kategori, malzemeler: altMap.get('') });
    } else {
      var subgruplar = [];
      for (var [altKat, malzList] of altMap) {
        subgruplar.push({ baslik: altKat || 'Genel', malzemeler: malzList });
      }
      result.push({ kategori: kategori, malzemeler: [], subgruplar: subgruplar });
    }
  }
  return result;
}

// ── Malzeme Ekle Modal ───────────────────────────────────────────────────────
function ozelMalzemeModalAc() {
  var modal = document.getElementById('ozelMalzemeModal');
  if (modal) modal.style.display = 'flex';
  _katalogSecilen = {};
  // Her açılışta DB'den gelen listeyle katalogu yeniden oluştur
  _aktifKatalog = _buildDynamicKatalog();
  var sel = document.getElementById('katalogKategoriSelect');
  if (sel) {
    sel.innerHTML = '';
    _aktifKatalog.forEach(function(kat, i) {
      var opt = document.createElement('option');
      opt.value = String(i);
      opt.textContent = kat.kategori;
      sel.appendChild(opt);
    });
  }
  malzemeTabSec('katalog');
  // Özel form alanlarını temizle
  var adEl = document.getElementById('ozelMalzemeAd');
  var birimEl = document.getElementById('ozelMalzemeBirim');
  var hataEl = document.getElementById('ozelMalzemeHata');
  if (adEl) adEl.value = '';
  if (birimEl) birimEl.value = '';
  if (hataEl) hataEl.style.display = 'none';
}

function ozelMalzemeModalKapat() {
  var modal = document.getElementById('ozelMalzemeModal');
  if (modal) modal.style.display = 'none';
}

function malzemeTabSec(tab) {
  var katalogView = document.getElementById('katalogView');
  var ozelView = document.getElementById('ozelView');
  var katalogBtn = document.getElementById('katalogTabBtn');
  var ozelBtn = document.getElementById('ozelTabBtn');
  if (tab === 'katalog') {
    if (katalogView) katalogView.style.display = 'block';
    if (ozelView) ozelView.style.display = 'none';
    if (katalogBtn) { katalogBtn.style.background='#FFFFFF'; katalogBtn.style.color='#6366F1'; katalogBtn.style.boxShadow='0 1px 3px rgba(0,0,0,0.1)'; katalogBtn.style.fontWeight='600'; }
    if (ozelBtn) { ozelBtn.style.background='transparent'; ozelBtn.style.color='#64748B'; ozelBtn.style.boxShadow='none'; ozelBtn.style.fontWeight='500'; }
    katalogKategoriDegis();
  } else {
    if (katalogView) katalogView.style.display = 'none';
    if (ozelView) ozelView.style.display = 'flex';
    if (ozelBtn) { ozelBtn.style.background='#FFFFFF'; ozelBtn.style.color='#6366F1'; ozelBtn.style.boxShadow='0 1px 3px rgba(0,0,0,0.1)'; ozelBtn.style.fontWeight='600'; }
    if (katalogBtn) { katalogBtn.style.background='transparent'; katalogBtn.style.color='#64748B'; katalogBtn.style.boxShadow='none'; katalogBtn.style.fontWeight='500'; }
    setTimeout(function() { var el = document.getElementById('ozelMalzemeAd'); if (el) el.focus(); }, 80);
  }
}

function _katalogKartOlustur(katIdx, flatIdx, m, seciliSet) {
  var secili = seciliSet.has(flatIdx);
  var kart = document.createElement('div');
  kart.style.cssText = 'padding:10px 12px;border:2px solid ' + (secili ? '#6366F1' : '#E2E8F0') + ';border-radius:10px;cursor:pointer;background:' + (secili ? '#EEF2FF' : '#F8FAFC') + ';transition:all 0.15s;user-select:none;';
  kart.dataset.idx = String(flatIdx);
  var adDiv = document.createElement('div');
  adDiv.style.cssText = 'font-size:13px;font-weight:' + (secili ? '600' : '500') + ';color:' + (secili ? '#4F46E5' : '#0F172A') + ';margin-bottom:3px;line-height:1.3;';
  adDiv.textContent = m.ad;
  var birimDiv = document.createElement('div');
  birimDiv.style.cssText = 'font-size:11px;color:#94A3B8;';
  birimDiv.textContent = m.birim;
  kart.appendChild(adDiv);
  kart.appendChild(birimDiv);
  kart.addEventListener('click', function() {
    var idx = parseInt(this.dataset.idx);
    var ki = parseInt(document.getElementById('katalogKategoriSelect').value) || 0;
    if (!_katalogSecilen[ki]) _katalogSecilen[ki] = new Set();
    var aDiv = this.querySelector('div');
    if (_katalogSecilen[ki].has(idx)) {
      _katalogSecilen[ki].delete(idx);
      this.style.border = '2px solid #E2E8F0';
      this.style.background = '#F8FAFC';
      if (aDiv) { aDiv.style.fontWeight = '500'; aDiv.style.color = '#0F172A'; }
    } else {
      _katalogSecilen[ki].add(idx);
      this.style.border = '2px solid #6366F1';
      this.style.background = '#EEF2FF';
      if (aDiv) { aDiv.style.fontWeight = '600'; aDiv.style.color = '#4F46E5'; }
    }
    katalogSecilenGuncelle();
  });
  return kart;
}

async function katalogKategoriDegis() {
  var sel = document.getElementById('katalogKategoriSelect');
  var grid = document.getElementById('katalogMalzemeGrid');
  if (!sel || !grid) return;
  var katIdx = parseInt(sel.value) || 0;
  var kat = _aktifKatalog[katIdx];
  if (!kat) return;

  // Subgruplu kategoriler: flat malzeme listesini oluştur
  if (kat.subgruplar) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;color:#94A3B8;font-size:12px;padding:16px;">Yükleniyor...</div>';
    for (var sg of kat.subgruplar) {
      if (sg.dinamik === 'cimento') {
        // DB'den tüm çimento markalarını çek
        var cimentoListesi = (window._fpTumMalzemeler || [])
          .filter(function(m) { return m.kategori === 'cimento'; })
          .map(function(m) { return { ad: m.ad, birim: m.birim || 'torba', scrape_ad: m.ad }; });
        if (!cimentoListesi.length) {
          // Fallback: API isteği
          try {
            var token = localStorage.getItem('bai_token');
            var r = await fetch('/api/malzemeler', { headers: { 'Authorization': 'Bearer ' + token } });
            if (r.ok) {
              var d = await r.json();
              cimentoListesi = (d.malzemeler || [])
                .filter(function(m) { return m.kategori === 'cimento'; })
                .map(function(m) { return { ad: m.ad, birim: m.birim || 'torba', scrape_ad: m.ad }; });
            }
          } catch(_) {}
        }
        if (!cimentoListesi.length) {
          cimentoListesi = [
            {ad: 'Akçansa CEM I 32,5', birim: 'torba', scrape_ad: 'Akçansa CEM I 32,5'},
            {ad: 'Akçansa CEM I 52,5', birim: 'torba', scrape_ad: 'Akçansa CEM I 52,5'},
            {ad: 'Safi CEM IV/B (P) 32,5', birim: 'torba', scrape_ad: 'Safi CEM IV/B (P) 32,5'},
            {ad: 'Votorantim CEM II/C-M (P-LL) 32,5 R', birim: 'torba', scrape_ad: 'Votorantim CEM II/C-M (P-LL) 32,5 R'},
            {ad: 'Votorantim CEM II/A-LL 42,5 R', birim: 'torba', scrape_ad: 'Votorantim CEM II/A-LL 42,5 R'},
            {ad: 'Altın Çimento CEM II B-M (P-LL) 32,5', birim: 'torba', scrape_ad: 'Altın Çimento CEM II B-M (P-LL) 32,5'},
            {ad: 'Bursa Çimento CEM II/A-M (P-L) 42,5 R', birim: 'torba', scrape_ad: 'Bursa Çimento CEM II/A-M (P-L) 42,5 R'},
            {ad: 'TFK CEM IV B(V) 32,5 R', birim: 'torba', scrape_ad: 'TFK CEM IV B(V) 32,5 R'},
            {ad: 'TFK CEM II B-V 42,5 R', birim: 'torba', scrape_ad: 'TFK CEM II B-V 42,5 R'},
          ];
        }
        sg.malzemeler = cimentoListesi;
      }
    }
    // Flat malzeme listesini güncelle
    kat.malzemeler = [];
    kat._subgrupRanges = [];
    kat.subgruplar.forEach(function(sg) {
      var start = kat.malzemeler.length;
      kat.malzemeler = kat.malzemeler.concat(sg.malzemeler);
      kat._subgrupRanges.push({ baslik: sg.baslik, start: start, end: kat.malzemeler.length });
    });
  }

  if (!_katalogSecilen[katIdx]) _katalogSecilen[katIdx] = new Set();
  grid.innerHTML = '';

  if (kat._subgrupRanges) {
    kat._subgrupRanges.forEach(function(sg) {
      if (sg.end === sg.start) return;
      var header = document.createElement('div');
      header.style.cssText = 'grid-column:1/-1;font-size:11px;font-weight:700;color:#334155;padding:10px 0 5px;border-bottom:1px solid #E2E8F0;letter-spacing:0.03em;text-transform:uppercase;margin-top:4px;';
      header.textContent = sg.baslik;
      grid.appendChild(header);
      for (var i = sg.start; i < sg.end; i++) {
        grid.appendChild(_katalogKartOlustur(katIdx, i, kat.malzemeler[i], _katalogSecilen[katIdx]));
      }
    });
  } else {
    kat.malzemeler.forEach(function(m, i) {
      grid.appendChild(_katalogKartOlustur(katIdx, i, m, _katalogSecilen[katIdx]));
    });
  }

  katalogSecilenGuncelle();
}

function katalogSecilenGuncelle() {
  var toplam = 0;
  Object.keys(_katalogSecilen).forEach(function(k) { toplam += _katalogSecilen[k].size; });
  var el = document.getElementById('katalogSecilen');
  if (el) el.textContent = toplam > 0 ? toplam + ' malzeme seçildi' : '';
}

async function katalogMalzemeKaydet() {
  var hataEl = document.getElementById('katalogHata');
  var btn = document.getElementById('katalogKaydetBtn');
  if (hataEl) hataEl.style.display = 'none';
  var secilenler = [];
  Object.keys(_katalogSecilen).forEach(function(ki) {
    var kat = _aktifKatalog[parseInt(ki)];
    if (!kat) return;
    _katalogSecilen[ki].forEach(function(mi) { secilenler.push(kat.malzemeler[mi]); });
  });
  if (secilenler.length === 0) {
    if (hataEl) { hataEl.textContent = 'En az bir malzeme seçin.'; hataEl.style.display = 'block'; }
    return;
  }
  if (btn) { btn.disabled = true; btn.textContent = 'Ekleniyor (' + secilenler.length + ')...'; }
  var token = localStorage.getItem('bai_token');
  var hatalar = [];
  for (var i = 0; i < secilenler.length; i++) {
    var m = secilenler[i];
    try {
      var resp = await fetch('/ozel-malzeme-ekle', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
        body: JSON.stringify({ ad: m.scrape_ad || m.ad, birim: m.birim })
      });
      if (!resp.ok) {
        var d = await resp.json();
        var det = (d.detail || '').toLowerCase();
        if (det.indexOf('mevcut') !== -1 || det.indexOf('zaten') !== -1 || det.indexOf('duplicate') !== -1) continue;
        hatalar.push(m.ad + ': ' + (d.detail || resp.status));
      }
    } catch(_) { hatalar.push(m.ad + ': bağlantı hatası'); }
  }
  if (btn) { btn.disabled = false; btn.textContent = 'Seçilenleri Ekle'; }
  if (hatalar.length > 0 && hatalar.length >= secilenler.length) {
    if (hataEl) { hataEl.textContent = hatalar[0]; hataEl.style.display = 'block'; }
    return;
  }
  ozelMalzemeModalKapat();
  if (typeof fiyatPageYukle === 'function') fiyatPageYukle();
}

async function ozelMalzemeKaydet() {
  const adEl    = document.getElementById('ozelMalzemeAd');
  const birimEl = document.getElementById('ozelMalzemeBirim');
  const hataEl  = document.getElementById('ozelMalzemeHata');
  const btn     = document.getElementById('ozelMalzemeKaydetBtn');
  const ad    = adEl.value.trim();
  const birim = birimEl.value.trim();
  if (!ad) {
    if (hataEl) { hataEl.textContent = 'Malzeme adı zorunlu.'; hataEl.style.display = 'block'; }
    return;
  }
  if (!birim) {
    if (hataEl) { hataEl.textContent = 'Birim zorunlu.'; hataEl.style.display = 'block'; }
    return;
  }
  if (hataEl) hataEl.style.display = 'none';
  if (btn) { btn.disabled = true; btn.textContent = 'Kaydediliyor...'; }
  const token = localStorage.getItem('bai_token');
  try {
    const resp = await fetch('/ozel-malzeme-ekle', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
      body: JSON.stringify({ ad, birim })
    });
    const data = await resp.json();
    if (resp.ok) {
      ozelMalzemeModalKapat();
      if (typeof fiyatPageYukle === 'function') fiyatPageYukle();
    } else {
      if (hataEl) { hataEl.textContent = data.detail || 'Hata oluştu.'; hataEl.style.display = 'block'; }
      if (btn) { btn.disabled = false; btn.textContent = 'Kaydet'; }
    }
  } catch(_) {
    if (hataEl) { hataEl.textContent = 'Bağlantı hatası.'; hataEl.style.display = 'block'; }
    if (btn) { btn.disabled = false; btn.textContent = 'Kaydet'; }
  }
}

async function ozelMalzemeSil(id) {
  if (!confirm('Bu malzemeyi silmek istediğinizden emin misiniz')) return;
  const token = localStorage.getItem('bai_token');
  try {
    await fetch('/ozel-malzeme-sil', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    });
    if (typeof fiyatPageYukle === 'function') fiyatPageYukle();
  } catch(_) {}
}

// â"€â"€ Tooltip show helper â"€â"€ positions based on screen column â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function _fpTipShow(el) {
  var t = el.querySelector('.fp-tip');
  if (!t) return;
  var r = el.getBoundingClientRect();
  if (r.left < window.innerWidth / 3) {
    t.style.left = '0'; t.style.right = 'auto';
  } else {
    t.style.right = '0'; t.style.left = 'auto';
  }
  t.style.display = 'block';
}

// â"€â"€ Chart card HTML helper â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function _fiyatGrafikKartHTML(m) {
  const canvasId = m.canvas  || `grafik_${m.malzeme}`;
  const labelId  = m.label   || `label_${m.malzeme}`;
  const periodId = m.period  || `period_${m.malzeme}`;
  const birimText = m.birim ? ` (${m.birim})` : '';
  const silBtn = m.ozel ? `<button onclick="ozelMalzemeSil(${m.id})" title="Kaldır" style="background:none;border:none;cursor:pointer;color:#CBD5E1;font-size:16px;padding:2px 4px;line-height:1;transition:color 0.15s;" onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='#CBD5E1'">&times;</button>` : '';
  const infoIcon = m.tooltip ? `<span style="position:relative;display:inline-flex;flex-shrink:0;vertical-align:middle;" onmouseenter="_fpTipShow(this)" onmouseleave="this.querySelector('.fp-tip').style.display='none'"><span style="display:inline-flex;align-items:center;justify-content:center;width:14px;height:14px;border-radius:50%;background:#CBD5E1;color:#475569;font-size:9px;font-weight:700;cursor:default;line-height:1;user-select:none;flex-shrink:0;">i</span><div class="fp-tip" style="display:none;position:absolute;top:18px;z-index:9999;background:#1E293B;color:#F1F5F9;font-size:11px;font-weight:400;padding:8px 10px;border-radius:8px;width:220px;white-space:normal;line-height:1.45;box-shadow:0 4px 20px rgba(0,0,0,0.3);pointer-events:none;">${m.tooltip}</div></span>` : '';
  return `
    <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:14px;box-shadow:0 1px 3px rgba(0,0,0,0.04);min-width:0;">
      <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px;gap:6px;">
        <div style="min-width:0;overflow:visible;flex:1;">
          <div style="display:flex;align-items:center;gap:4px;">${infoIcon}<div style="font-size:13px;font-weight:700;color:#0F172A;word-break:break-word;">${m.ad}${m.ozel ? ' <span style="font-size:10px;font-weight:500;color:#6366F1;border:1px solid #C7D2FE;border-radius:4px;padding:1px 5px;">Özel</span>' : ''}</div></div>
          <div style="font-size:11px;color:#94A3B8;margin-top:2px;">
            Son fiyat: <span id="${labelId}" style="color:#EF4444;font-weight:600;">?</span>${birimText}
            <span id="fpBadge_${m.malzeme}" style="display:none;font-size:11px;font-weight:600;padding:1px 6px;border-radius:10px;margin-left:2px;vertical-align:middle;"></span>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:3px;flex-shrink:0;">
          <select id="${periodId}" onchange="fiyatGrafikYukle('${m.malzeme}','${canvasId}','${labelId}',this.value)"
            style="font-size:11px;font-weight:600;color:#475569;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:7px;padding:4px 6px;cursor:pointer;outline:none;">
            <option value="30">1 Ay</option>
            <option value="90" selected>3 Ay</option>
            <option value="180">6 Ay</option>
          </select>
          <button onclick="fpMiniPlusTikla('${m.malzeme}')" title="Fiyat gir"
            style="background:#F0FDF4;border:1px solid #BBF7D0;color:#16A34A;font-size:15px;font-weight:700;width:26px;height:26px;border-radius:7px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;line-height:1;flex-shrink:0;padding:0;transition:all 0.15s;"
            onmouseover="this.style.background='#DCFCE7';this.style.borderColor='#86EFAC'" onmouseout="this.style.background='#F0FDF4';this.style.borderColor='#BBF7D0'">+</button>
          ${silBtn}
        </div>
      </div>
      <canvas id="${canvasId}" height="140"></canvas>
      <div id="fpMini_${m.malzeme}" style="display:none;margin-top:10px;padding:10px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:9px;">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
          <div>
            <div style="font-size:11px;color:#64748B;margin-bottom:3px;font-weight:500;">Fiyat (₺)</div>
            <input id="fpMiniPrice_${m.malzeme}" type="number" placeholder="28500" min="0" step="0.01"
              style="width:100%;padding:7px 9px;background:#fff;border:1px solid #E2E8F0;border-radius:7px;font-size:13px;color:#0F172A;box-sizing:border-box;outline:none;"
              onfocus="this.style.borderColor='#10B981'" onblur="this.style.borderColor='#E2E8F0'"
              onkeydown="if(event.key==='Enter')fpMiniKaydet('${m.malzeme}')"/>
          </div>
          <div>
            <div style="font-size:11px;color:#64748B;margin-bottom:3px;font-weight:500;">Tarih</div>
            <input id="fpMiniDate_${m.malzeme}" type="date"
              style="width:100%;padding:7px 9px;background:#fff;border:1px solid #E2E8F0;border-radius:7px;font-size:13px;color:#0F172A;box-sizing:border-box;outline:none;"
              onfocus="this.style.borderColor='#10B981'" onblur="this.style.borderColor='#E2E8F0'"/>
          </div>
        </div>
        <div style="margin-bottom:8px;">
          <div style="font-size:11px;color:#64748B;margin-bottom:3px;font-weight:500;">Tedarikçi (opsiyonel)</div>
          <input id="fpMiniTedarikci_${m.malzeme}" type="text" placeholder="Tedarikçi adı"
            style="width:100%;padding:7px 9px;background:#fff;border:1px solid #E2E8F0;border-radius:7px;font-size:13px;color:#0F172A;box-sizing:border-box;outline:none;"
            onfocus="this.style.borderColor='#10B981'" onblur="this.style.borderColor='#E2E8F0'"
            onkeydown="if(event.key==='Enter')fpMiniKaydet('${m.malzeme}')"/>
        </div>
        <div id="fpMiniErr_${m.malzeme}" style="display:none;color:#EF4444;font-size:11px;margin-bottom:6px;"></div>
        <div style="display:flex;gap:6px;">
          <button onclick="fpMiniKaydet('${m.malzeme}')"
            style="flex:1;padding:7px;background:#10B981;color:#fff;border:none;border-radius:7px;font-size:12px;font-weight:600;cursor:pointer;transition:background 0.15s;"
            onmouseover="this.style.background='#059669'" onmouseout="this.style.background='#10B981'">Kaydet</button>
          <button onclick="fpMiniPlusTikla('${m.malzeme}')"
            style="padding:7px 12px;background:#F1F5F9;color:#64748B;border:1px solid #E2E8F0;border-radius:7px;font-size:12px;cursor:pointer;transition:background 0.15s;"
            onmouseover="this.style.background='#E2E8F0'" onmouseout="this.style.background='#F1F5F9'">İptal</button>
        </div>
      </div>
    </div>`;
}

// â"€â"€ Tab button HTML helper â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
function _fiyatTabButonHTML(m) {
  const q = `${m.ad} fiyat trendi ve tahminleri`;
  return `<button onclick="fiyatGrafikleriGeriGetir();fiyatAiQuick('${q.replace(/'/g, "'")}')"
    style="background:#F1F5F9;border:1px solid #E2E8F0;color:#475569;font-size:12px;font-weight:500;padding:5px 12px;border-radius:20px;cursor:pointer;transition:all 0.15s;"
    onmouseover="this.style.background='#E2E8F0'" onmouseout="this.style.background='#F1F5F9'">${m.ad}</button>`;
}

// ── Grouped layout helpers ──────────────────────────────────────────────────
const _FP_KAPALI_GRUPLAR = new Set(['Çimento']);
const _FP_GRUP_SIRASI = ['Beton', 'Demir', 'Çelik Hasır', 'Filmaşin', 'Çimento', 'Kum', 'Gazbeton'];

function _fiyatGruplarHTML(malzemeler) {
  const grupMap = {};
  for (const m of malzemeler) {
    const grp = m.ozel ? 'Diğer Malzemeler' : (m.kategori_grup || 'Diğer Malzemeler');
    if (!grupMap[grp]) grupMap[grp] = [];
    grupMap[grp].push(m);
  }
  const sirali = [
    ..._FP_GRUP_SIRASI.filter(g => grupMap[g]),
    ...Object.keys(grupMap).filter(g => !_FP_GRUP_SIRASI.includes(g))
  ];

  // Tek bir 3-sütunluk flat grid; grup başlıkları tüm sütunları kapsar,
  // kartlar her zaman 1/3 genişliğinde — tek kartlı gruplar da dahil.
  let parts = ['<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start;">'];

  for (const grup of sirali) {
    const items = grupMap[grup];
    const kapali = _FP_KAPALI_GRUPLAR.has(grup);
    const grupId = 'fpGrup_' + grup.replace(/[^a-zA-Z0-9]/g, '_');

    // Grup başlığı — tüm sütunları kaplar
    parts.push(`<div id="fpGrupHeader_${grupId}" style="grid-column:1/-1;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div onclick="fpGroupToggle('${grupId}')" style="display:flex;align-items:center;justify-content:space-between;padding:11px 16px;cursor:pointer;background:#F8FAFC;user-select:none;transition:background 0.15s;" onmouseover="this.style.background='#F1F5F9'" onmouseout="this.style.background='#F8FAFC'">
          <div style="font-size:13px;font-weight:700;color:#334155;letter-spacing:0.01em;">${grup}</div>
          <div style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:11px;color:#94A3B8;">${items.length} ürün</span>
            <svg id="fpGrupArrow_${grupId}" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="transition:transform 0.2s;transform:${kapali ? 'rotate(-90deg)' : 'rotate(0deg)'}"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
        </div>
      </div>`);

    // Kartlar — grid'de birer hücre, display:none ile tamamen kaldırılır
    for (const m of items) {
      parts.push(`<div class="fp-kart-item" data-grup="${grupId}" style="display:${kapali ? 'none' : 'block'};min-width:0;">${_fiyatGrafikKartHTML(m)}</div>`);
    }
  }

  parts.push('</div>');
  return parts.join('');
}

function fpGroupToggle(grupId) {
  const items = document.querySelectorAll(`.fp-kart-item[data-grup="${grupId}"]`);
  const a = document.getElementById('fpGrupArrow_' + grupId);
  if (!items.length) return;
  const opening = items[0].style.display === 'none';
  items.forEach(el => { el.style.display = opening ? 'block' : 'none'; });
  if (a) a.style.transform = opening ? 'rotate(0deg)' : 'rotate(-90deg)';
}

function fpMiniPlusTikla(key) {
  const mini = document.getElementById('fpMini_' + key);
  if (!mini) return;
  const isOpen = mini.style.display !== 'none';
  mini.style.display = isOpen ? 'none' : 'block';
  if (!isOpen) {
    const d = document.getElementById('fpMiniDate_' + key);
    if (d && !d.value) d.value = new Date().toISOString().slice(0, 10);
    const p = document.getElementById('fpMiniPrice_' + key);
    if (p) setTimeout(() => p.focus(), 50);
  }
}

async function fpMiniKaydet(key) {
  const malzemeId = (window._fpMalzemeMap || {})[key];
  const priceEl = document.getElementById('fpMiniPrice_' + key);
  const dateEl  = document.getElementById('fpMiniDate_' + key);
  const tedEl   = document.getElementById('fpMiniTedarikci_' + key);
  const errEl   = document.getElementById('fpMiniErr_' + key);
  if (errEl) errEl.style.display = 'none';
  if (!malzemeId) {
    if (errEl) { errEl.textContent = 'Bu malzeme için veri kaynağı bulunamadı.'; errEl.style.display = 'block'; }
    return;
  }
  const fiyat = parseFloat(priceEl ? priceEl.value : '');
  if (!fiyat || fiyat <= 0) {
    if (errEl) { errEl.textContent = 'Geçerli bir fiyat girin.'; errEl.style.display = 'block'; }
    return;
  }
  const tarih = (dateEl ? dateEl.value : '') || new Date().toISOString().slice(0, 10);
  const tedarikci = ((tedEl ? tedEl.value : '') || '').trim() || null;
  const il = (_fpAktifIl() || '').replace(/^["'s]+|["'s]+$/g, '') || 'İstanbul';
  const kaydetBtn = document.querySelector('#fpMini_' + key + ' button');
  if (kaydetBtn) { kaydetBtn.textContent = 'Kaydediliyor...'; kaydetBtn.disabled = true; }
  try {
    const token = localStorage.getItem('bai_token');
    const resp = await fetch('/api/fiyat/kullanici', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
      body: JSON.stringify({ malzeme_id: malzemeId, fiyat, tarih, tedarikci, il })
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.detail || String(resp.status));
    if (priceEl) priceEl.value = '';
    if (tedEl) tedEl.value = '';
    fpMiniPlusTikla(key);
    const m = (window._fpAktifMalzemeler || []).find(x => x.malzeme === key);
    if (m) {
      const canvasId = m.canvas || 'grafik_' + key;
      const labelId  = m.label  || 'label_' + key;
      const pEl = document.getElementById(m.period || 'period_' + key);
      fiyatGrafikYukle(key, canvasId, labelId, pEl ? pEl.value : 90);
    }
  } catch(e) {
    if (errEl) { errEl.textContent = 'Hata: ' + e.message; errEl.style.display = 'block'; }
    if (kaydetBtn) { kaydetBtn.textContent = 'Kaydet'; kaydetBtn.disabled = false; }
  }
}

function fiyatAiOnerileriGoster() {
    const panel = document.getElementById('fiyatAiOneriler');
    const container = document.getElementById('fiyatAiOneriButonlari');
    if (!panel || !container) return;

    const oneriler = [
        {text: 'Demir fiyat trendi', query: 'Demir (Çelik) fiyat trendi ve tahminleri'},
        {text: 'Beton fiyat analizi', query: 'Beton fiyat trendi ve önümüzdeki ay tahmini'},
        {text: 'Çimento fiyatları', query: 'Çimento fiyat trendi ve tahminleri'},
        {text: 'Tuğla fiyatları', query: 'Tuğla fiyat trendi ve tahminleri'},
        {text: 'Kum fiyatları', query: 'Kum fiyat trendi ve tahminleri'},
        {text: 'Malzeme karşılaştır', query: 'Tüm malzemelerin fiyat karşılaştırması ve trend analizi'},
        {text: 'Satın alma zamanı', query: 'Hangi malzemeler için şu an satın alma zamanı'},
        {text: 'Maliyet tahmini', query: 'Önümüzdeki 3 ay için toplam inşaat malzeme maliyet tahmini'},
    ];

    container.innerHTML = oneriler.map(o =>
        `<button onclick="fiyatAiOneriSec('${o.query.replace(/'/g, "'")}')" style="padding:6px 12px;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:20px;color:#334155;font-size:12px;cursor:pointer;white-space:nowrap;transition:all 0.15s;"
         onmouseover="this.style.background='#6366F1';this.style.color='#fff';this.style.borderColor='#6366F1'"
         onmouseout="this.style.background='#F1F5F9';this.style.color='#334155';this.style.borderColor='#E2E8F0'"
        >${o.text}</button>`
    ).join('');

    panel.style.display = 'block';
}

function fiyatAiOnerileriGizle() {
    const panel = document.getElementById('fiyatAiOneriler');
    if (panel) {
        setTimeout(() => { panel.style.display = 'none'; }, 200);
    }
}

function fiyatAiOneriSec(query) {
    const input = document.getElementById('fiyatAiInput');
    if (input) input.value = query;
    const panel = document.getElementById('fiyatAiOneriler');
    if (panel) panel.style.display = 'none';
    if (typeof fiyatAiGonder === 'function') fiyatAiGonder();
}

async function fiyatHavaDurumuGuncelle(sehir, lat, lon) {
    const el = document.getElementById('globalHavaDurumu');
    if (!el) return;

    // Eğer parametre verilmediyse global değişkenlerden oku
    sehir = sehir || window._aktifSantiyeSehir || '';
    lat = lat || window._aktifSantiyeLat || '';
    lon = lon || window._aktifSantiyeLon || '';

    if (!sehir && !lat) { el.innerHTML = ''; return; }

    try {
        const params = new URLSearchParams();
        if (lat && lon) {
            params.set('lat', lat);
            params.set('lon', lon);
        } else {
            params.set('sehir', sehir);
        }
        const url = '/hava?' + params.toString();

        const r = await fetch(url);
        const d = await r.json();
        const pill = document.getElementById('globalHavaDurumuPill');
        if (d && d.sicaklik !== undefined) {
            const lokasyon = sehir || (d.sehir || '');
            el.textContent = (lokasyon ? lokasyon + '  ' : '') + d.sicaklik + '°C';
            if (pill) pill.style.display = 'flex';
        } else {
            el.textContent = '';
            if (pill) pill.style.display = 'none';
        }
    } catch(e) { el.innerHTML = ''; }
}

async function fiyatPageYukle() {
  fiyatHavaDurumuGuncelle(window._aktifSantiyeSehir || '?stanbul');
  await _fpMalzemeIdsYukle();

  const malzemeler = [
    // ─── Demir ───
    { malzeme:'demir_o8',           scrape_ad:'Nervürlü Demir Ø8',                    ad:'Nervürlü Demir Ø8',                birim:'ton',   kategori_grup:'Demir',
      tooltip:'Nervürlü Demir Ø8 — İl bazlı fabrika teslim fiyatı (KDV %20 dahil)' },
    { malzeme:'demir_o10',          scrape_ad:'Nervürlü Demir Ø10',                   ad:'Nervürlü Demir Ø10',               birim:'ton',   kategori_grup:'Demir',
      tooltip:'Nervürlü Demir Ø10 — İl bazlı fabrika teslim fiyatı (KDV %20 dahil)' },
    { malzeme:'demir_o12',          scrape_ad:'Nervürlü Demir Ø12',                   ad:'Nervürlü Demir Ø12',               birim:'ton',   kategori_grup:'Demir',
      tooltip:'Nervürlü Demir Ø12 — İl bazlı fabrika teslim fiyatı (KDV %20 dahil)' },
    // ─── Çelik Hasır ───
    { malzeme:'hasir_q131',         scrape_ad:'Çelik Hasır Q131',                     ad:'Çelik Hasır Q131',                 birim:'ton',   kategori_grup:'Çelik Hasır',
      tooltip:'Q131 ulusal endeks fiyatı' },
    { malzeme:'hasir_q188',         scrape_ad:'Çelik Hasır Q188',                     ad:'Çelik Hasır Q188',                 birim:'ton',   kategori_grup:'Çelik Hasır',
      tooltip:'Q188 ulusal endeks fiyatı' },
    // ─── Filmaşin ───
    { malzeme:'filmasin',           scrape_ad:'Filmaşin',                             ad:'Filmaşin',                         birim:'ton',   kategori_grup:'Filmaşin',
      tooltip:'USD/ton, günlük kurla TL\'ye çevrilmiş' },
    // ─── Çimento (varsayılan kapalı) ───
    { malzeme:'cim_akcansa_32',     scrape_ad:'Akçansa CEM I 32,5',                   ad:'Akçansa CEM I 32,5',               birim:'torba', kategori_grup:'Çimento',
      tooltip:'Akçansa CEM I 32,5' },
    { malzeme:'cim_safi_32',        scrape_ad:'Safi CEM IV/B (P) 32,5',               ad:'Safi CEM IV/B (P) 32,5',           birim:'torba', kategori_grup:'Çimento',
      tooltip:'Safi CEM IV/B (P) 32,5' },
    { malzeme:'cim_vot_32',         scrape_ad:'Votorantim CEM II/C-M (P-LL) 32,5 R', ad:'Votorantim CEM II/C-M 32,5 R',    birim:'torba', kategori_grup:'Çimento',
      tooltip:'Votorantim CEM II/C-M (P-LL) 32,5 R' },
    { malzeme:'cim_akcansa_52',     scrape_ad:'Akçansa CEM I 52,5',                   ad:'Akçansa CEM I 52,5',               birim:'torba', kategori_grup:'Çimento',
      tooltip:'Akçansa CEM I 52,5' },
    { malzeme:'cim_altin_32',       scrape_ad:'Altın Çimento CEM II B-M (P-LL) 32,5', ad:'Altın Çimento CEM II B-M 32,5',  birim:'torba', kategori_grup:'Çimento',
      tooltip:'Altın Çimento CEM II B-M (P-LL) 32,5' },
    { malzeme:'cim_bursa_42',       scrape_ad:'Bursa Çimento CEM II/A-M (P-L) 42,5 R', ad:'Bursa Çimento CEM II/A-M 42,5 R', birim:'torba', kategori_grup:'Çimento',
      tooltip:'Bursa Çimento CEM II/A-M (P-L) 42,5 R' },
    { malzeme:'cim_tfk_32',         scrape_ad:'TFK CEM IV B(V) 32,5 R',               ad:'TFK CEM IV B(V) 32,5 R',           birim:'torba', kategori_grup:'Çimento',
      tooltip:'TFK CEM IV B(V) 32,5 R' },
    { malzeme:'cim_tfk_42',         scrape_ad:'TFK CEM II B-V 42,5 R',                ad:'TFK CEM II B-V 42,5 R',            birim:'torba', kategori_grup:'Çimento',
      tooltip:'TFK CEM II B-V 42,5 R' },
    { malzeme:'cim_vot_42',         scrape_ad:'Votorantim CEM II/A-LL 42,5 R',        ad:'Votorantim CEM II/A-LL 42,5 R',   birim:'torba', kategori_grup:'Çimento',
      tooltip:'Votorantim CEM II/A-LL 42,5 R' },
    // ─── Kum ───
    { malzeme:'kum_sap',            scrape_ad:'Şap Kumu',                             ad:'Şap Kumu',                         birim:'ton',   kategori_grup:'Kum',
      tooltip:'Şap Kumu ton fiyatı' },
    { malzeme:'kum_kaba',           scrape_ad:'Kaba Kum',                             ad:'Kaba Kum',                         birim:'ton',   kategori_grup:'Kum',
      tooltip:'Kaba Kum ton fiyatı' },
    // ─── Gazbeton ───
    { malzeme:'gazbeton',           scrape_ad:'Gazbeton Düz Duvar Bloğu',             ad:'Gazbeton Düz Duvar Bloğu',         birim:'adet',  kategori_grup:'Gazbeton',
      tooltip:'G2/400 Düz Duvar Bloğu, adet fiyatı' },
  ];

  // Her spesifik malzeme için scrape_ad → malzeme_id eşleştirmesi
  for (const m of malzemeler) {
    if (m.scrape_ad) {
      const id = (window._fpMalzemeMapByAd || {})[m.scrape_ad.toLowerCase()];
      if (id) window._fpMalzemeMap[m.malzeme] = id;
    }
  }

  // Fetch org-specific custom materials and append
  try {
    const token = localStorage.getItem('bai_token');
    if (token) {
      const r = await fetch('/ozel-malzemeler', { headers: { 'Authorization': 'Bearer ' + token } });
      if (r.ok) {
        const body = await r.json();
        for (const om of (body.malzemeler || [])) {
          malzemeler.push({
            malzeme: om.key,
            canvas:  `ozelGrafik_${om.key}`,
            label:   `ozelLabel_${om.key}`,
            period:  `ozelPeriod_${om.key}`,
            ad:      om.ad,
            ozel:    true,
            id:      om.id,
            birim:   om.birim,
          });
          // Scrape verisi olan malzemeler için doğrudan malzeme_id eşle
          if (window._fpMalzemeMapByAd && om.ad) {
            const scrapeId = window._fpMalzemeMapByAd[om.ad.toLowerCase()];
            if (scrapeId) window._fpMalzemeMap[om.key] = scrapeId;
          }
        }
      }
    }
  } catch(_) {}

  window._fpAktifMalzemeler = malzemeler;

  // Build ID set for active materials (used by "Fiyat Gir" dropdown filter)
  {
    const _idSet = new Set();
    for (const m of malzemeler) {
      const mid = (window._fpMalzemeMapByAd || {})[((m.scrape_ad || m.ad) || '').toLowerCase()];
      if (mid) _idSet.add(mid);
    }
    window._fpAktifMalzemeIds = _idSet;
  }

  // Generate grouped chart cards
  const grafikAlani = document.getElementById('fiyatGrafiklerAlani');
  if (grafikAlani) grafikAlani.innerHTML = _fiyatGruplarHTML(malzemeler);

  // Generate material tab buttons dynamically
  const tabAlani = document.getElementById('fiyatMalzemeTablar');
  if (tabAlani) tabAlani.innerHTML = malzemeler.map(_fiyatTabButonHTML).join('');

  // Load all charts
  for (const m of malzemeler) {
    const canvasId = m.canvas  || `grafik_${m.malzeme}`;
    const labelId  = m.label   || `label_${m.malzeme}`;
    const periodId = m.period  || `period_${m.malzeme}`;
    const pEl = document.getElementById(periodId);
    const gun = pEl ? (pEl.value || 90) : 90;
    await fiyatGrafikYukle(m.malzeme, canvasId, labelId, gun);
  }
  await _fpMarkaKarsilastirmaYukle();
}

async function fiyatGrafikYukle(malzeme, canvasId, labelId, gun) {
  try {
    const _fpDateKey = (value) => {
      if (!value) return '';
      if (typeof value === 'string' && /^\d{4}-\d{2}-\d{2}/.test(value)) return value.slice(0, 10);
      const dt = new Date(value);
      if (Number.isNaN(dt.getTime())) return String(value).slice(0, 10);
      const y = dt.getFullYear();
      const m = String(dt.getMonth() + 1).padStart(2, '0');
      const d = String(dt.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    };
    const _fpShortDate = (value) => {
      const key = _fpDateKey(value);
      return key ? key.slice(5) : '';
    };
    const _fpSortByTarih = (rows) => [...(rows || [])].sort((a, b) => _fpDateKey(a.tarih).localeCompare(_fpDateKey(b.tarih)));
    const _fpToIndexed = (keys, values, allLabels) => allLabels.map(lbl => {
      const idx = keys.indexOf(lbl);
      if (idx === -1) return null;
      const v = Number(values[idx]);
      return Number.isFinite(v) ? v : null;
    });

    _fpLog('fiyatGrafikYukle basladi', { malzeme, canvasId, labelId, gun, map: window._fpMalzemeMap });
    const res  = await fetch(`/fiyat-gecmis/${malzeme}?gun=${gun}`);
    _fpLog('/fiyat-gecmis status', { malzeme, status: res.status, ok: res.ok });
    const data = await res.json();
    _fpLog('/fiyat-gecmis response', { malzeme, data });
    const gecmis = _fpSortByTarih(data.gecmis || []);

    const canvas = document.getElementById(canvasId);
    if (!canvas) return 0;

    // Son fiyatı label'e yaz
    const sonFiyat = gecmis.length > 0 ? parseFloat(gecmis[gecmis.length-1].fiyat) : null;
    const labelEl  = document.getElementById(labelId);
    // Bolgesel piyasa verisi: lokal gecmis olmasa bile scrape cizgisi cizilebilmeli.
    let bolgesalLabels = [], bolgesalData = [], farkYuzdesi = null;
    let kullaniciLabels = [], kullaniciData = [];
    const _fpMalzemeId = window._fpMalzemeMap[malzeme];
    const _fpIl = _fpAktifIl();
    _fpLog('bolgesel grafik on kontrol', { malzeme, malzemeId: _fpMalzemeId, il: _fpIl, mapDetay: window._fpMalzemeMapDetay?.[malzeme] });
    if (_fpMalzemeId && _fpIl) {
      try {
        const _fpToken = localStorage.getItem('bai_token');
        const _fpDonem = _fpGunToDonem(gun);
        const _fpParams = new URLSearchParams({
          malzeme_id: String(_fpMalzemeId),
          il: _fpIl,
          donem: _fpDonem
        });
        const _fpUrl = `/api/fiyat/grafik?${_fpParams.toString()}`;
        _fpLog('/api/fiyat/grafik cagriliyor', { malzeme, url: _fpUrl });
        const _fpResp = await fetch(_fpUrl, { headers: { 'Authorization': 'Bearer ' + _fpToken } });
        _fpLog('/api/fiyat/grafik status', { malzeme, status: _fpResp.status, ok: _fpResp.ok });
        const _fpJson = await _fpResp.json();
        _fpLog('/api/fiyat/grafik response', { malzeme, response: _fpJson });
        if (_fpResp.ok) {
          const _fpBolgeselRows = _fpSortByTarih(_fpJson.bolgesel_tahmin || []);
          bolgesalLabels = _fpBolgeselRows.map(d => _fpDateKey(d.tarih));
          bolgesalData   = _fpBolgeselRows.map(d => Number(d.fiyat));
          farkYuzdesi    = _fpJson.fark_yuzdesi;
          const _fpKullaniciRows = _fpSortByTarih(_fpJson.kullanici_fiyat || []);
          kullaniciLabels = _fpKullaniciRows.map(d => _fpDateKey(d.tarih));
          kullaniciData   = _fpKullaniciRows.map(d => Number(d.fiyat));
          _fpLog('bolgesel veri tarih sirasi', {
            malzeme,
            count: _fpBolgeselRows.length,
            first: _fpBolgeselRows[0]?.tarih,
            last: _fpBolgeselRows[_fpBolgeselRows.length - 1]?.tarih,
            labels: bolgesalLabels
          });
        }
      } catch(e) {
        _fpWarn('/api/fiyat/grafik hata', { malzeme, error: e });
      }
    } else {
      _fpWarn('/api/fiyat/grafik atlandi', { malzeme, malzemeId: _fpMalzemeId, il: _fpIl });
    }
    if (labelEl) labelEl.textContent = sonFiyat ? '₺' + sonFiyat.toLocaleString('tr-TR') : '?';
    // Kullanıcının girdiği en son fiyatı label'e yaz (öncelikli)
    if (kullaniciData.length > 0 && labelEl) {
      labelEl.textContent = '₺' + kullaniciData[kullaniciData.length - 1].toLocaleString('tr-TR');
    }

    // Hiç veri yoksa mesaj göster ve çık
    if (gecmis.length === 0 && bolgesalData.length === 0 && kullaniciData.length === 0) {
      if (_fpCharts[canvasId]) { _fpCharts[canvasId].destroy(); delete _fpCharts[canvasId]; }
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#94A3B8';
      ctx.font = '13px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('Henüz fiyat verisi yok', canvas.width / 2, canvas.height / 2);
      _fpWarn('grafik icin veri yok', { malzeme, gecmisCount: gecmis.length, bolgeselCount: bolgesalData.length });
      return 0;
    }

    // Az veri varsa örnek veri üret
    let gecmisLabels, gecmisData;
    if (gecmis.length >= 2) {
      gecmisLabels = gecmis.map(d => _fpDateKey(d.tarih));
      gecmisData   = gecmis.map(d => parseFloat(d.fiyat));
    } else if (gecmis.length === 1) {
      const baz = malzeme==='demir' ? 220 : malzeme==='beton' ? 250 : 1800;
      gecmisLabels = Array.from({length:8}, (_,i) => {
        const d = new Date(); d.setDate(d.getDate() - (7-i)*10);
        return _fpDateKey(d);
      });
      gecmisData = gecmisLabels.map((_,i) => Math.round(baz + (Math.random()-0.5)*baz*0.12 + i*baz*0.01));
      if (labelEl) labelEl.textContent = gecmisData[gecmisData.length-1].toLocaleString('tr-TR');
    } else {
      gecmisLabels = [];
      gecmisData = [];
      if (labelEl && bolgesalData.length > 0) labelEl.textContent = bolgesalData[bolgesalData.length - 1].toLocaleString('tr-TR');
    }

    let satinAlmaData = [];
    try {
        const token = localStorage.getItem('bai_token');
        const saParams = new URLSearchParams({ limit: '50' });
        if (window._aktifSantiyeId) saParams.set('santiye_id', String(window._aktifSantiyeId));
        const saUrl = `/api/satin-almalar?${saParams.toString()}`;
        const saRes = await fetch(saUrl, {headers: {'Authorization': 'Bearer ' + token}});
        const saData = await saRes.json();
        if (saData.kayitlar) {
            satinAlmaData = saData.kayitlar
                .filter(k => k.malzeme_ad && k.malzeme_ad.toLowerCase().includes(malzeme.toLowerCase()))
                .map(k => ({ tarih: k.tarih, fiyat: k.birim_fiyat }))
                .sort((a,b) => new Date(a.tarih) - new Date(b.tarih));
        }
    } catch(e) {}

    const satinAlmaLabels = satinAlmaData.map(d => {
      const dt = d.tarih ? new Date(d.tarih) : new Date();
      return _fpDateKey(dt);
    });

    if ((farkYuzdesi === null || farkYuzdesi === undefined) && sonFiyat && bolgesalData.length > 0) {
      const sonBolgesel = bolgesalData[bolgesalData.length - 1];
      if (sonBolgesel > 0) farkYuzdesi = ((sonFiyat - sonBolgesel) / sonBolgesel) * 100;
      _fpLog('badge farki lokal gecmisten hesaplandi', { malzeme, sonFiyat, sonBolgesel, farkYuzdesi });
    }
    const badgeEl = document.getElementById('fpBadge_' + malzeme);
    if (badgeEl) {
      if (farkYuzdesi !== null && bolgesalData.length > 0) {
        const isGood = farkYuzdesi <= 0;
        badgeEl.textContent = (farkYuzdesi > 0 ? '+' : '') + farkYuzdesi.toFixed(1) + '% piyasaya göre';
        badgeEl.style.background = isGood ? '#DCFCE7' : '#FEE2E2';
        badgeEl.style.color = isGood ? '#16A34A' : '#DC2626';
        badgeEl.style.display = 'inline-block';
      } else {
        badgeEl.style.display = 'none';
      }
    }

    const allLabels = [...new Set([...gecmisLabels, ...satinAlmaLabels, ...bolgesalLabels, ...kullaniciLabels])]
      .filter(Boolean)
      .sort((a, b) => a.localeCompare(b))
      .map(l => _fpShortDate(l));

    const gecmisShortLabels    = gecmisLabels.map(_fpShortDate);
    const satinAlmaShortLabels = satinAlmaLabels.map(_fpShortDate);
    const bolgesalShortLabels  = bolgesalLabels.map(_fpShortDate);
    const kullaniciShortLabels = kullaniciLabels.map(_fpShortDate);

    const gecmisChartData    = _fpToIndexed(gecmisShortLabels, gecmisData, allLabels);
    const satinAlmaChartData = _fpToIndexed(satinAlmaShortLabels, satinAlmaData.map(d => d.fiyat), allLabels);
    const bolgesalChartData  = _fpToIndexed(bolgesalShortLabels, bolgesalData, allLabels);
    const kullaniciChartData = _fpToIndexed(kullaniciShortLabels, kullaniciData, allLabels);

    _fpLog('Chart.js category mode', {
      malzeme,
      labelCount: allLabels.length,
      gecmisCount: gecmisData.length,
      bolgeselCount: bolgesalData.length,
      bolgesalChartData
    });

    // Chart
    if (_fpCharts[canvasId]) { _fpCharts[canvasId].destroy(); delete _fpCharts[canvasId]; }
    _fpCharts[canvasId] = new Chart(canvas, {
      type: 'line',
      data: {
        labels: allLabels,
        datasets: [
          {
            label: 'Geçmiş',
            data: gecmisChartData,
            borderColor: '#EF4444',
            backgroundColor: 'rgba(239,68,68,0.08)',
            borderWidth: 2,
            pointRadius: 0,
            fill: true,
            tension: 0.3,
            spanGaps: true
          },
          ...(satinAlmaData.length > 0 ? [{
            label: 'Satın Alma',
            data: satinAlmaChartData,
            borderColor: '#3B82F6',
            backgroundColor: 'rgba(59,130,246,0.1)',
            borderWidth: 2,
            pointRadius: 4,
            pointBackgroundColor: '#3B82F6',
            tension: 0.3,
            fill: false,
            spanGaps: true
          }] : []),
          ...(bolgesalData.length > 0 ? [{
            label: 'Bölgesel Piyasa',
            data: bolgesalChartData,
            borderColor: '#F97316',
            backgroundColor: 'rgba(249,115,22,0.05)',
            borderWidth: 2,
            borderDash: [6,3],
            pointRadius: 0,
            fill: false,
            tension: 0.3,
            spanGaps: true
          }] : []),
          ...(kullaniciData.length > 0 ? [{
            label: 'Fiyatınız',
            data: kullaniciChartData,
            borderColor: '#EF4444',
            backgroundColor: 'rgba(239,68,68,0.15)',
            borderWidth: 2.5,
            pointRadius: 5,
            pointBackgroundColor: '#EF4444',
            fill: false,
            tension: 0.3,
            spanGaps: true
          }] : [])
        ]
      },
      options: {
        responsive: true,
        animation: { duration: 400 },
        plugins: {
          legend: { display: false },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              title: items => items?.[0]?.label ?? ''
            }
          }
        },
        scales: {
          x: {
            ticks: {
              color: '#94A3B8',
              font: { size: 10 },
              maxTicksLimit: 6
            },
            grid: { color: 'rgba(0,0,0,0.04)' }
          },
          y: {
            beginAtZero: false,
            ticks: { color: '#94A3B8', font: { size: 10 }, callback: v => '₺' + v.toLocaleString('tr-TR') },
            grid: { color: 'rgba(0,0,0,0.04)' }
          }
        }
      }
    });

    // Çimento: kullanıcının girdiği fiyat yoksa en ucuz markayı göster
    if (malzeme === 'cimento' && labelEl && kullaniciData.length === 0) {
      try {
        const _cToken = localStorage.getItem('bai_token');
        const _cResp = await fetch('/api/fiyat/marka-karsilastirma?alt_kategori=cimento', {
          headers: { 'Authorization': 'Bearer ' + _cToken }
        });
        if (_cResp.ok) {
          const _cData = await _cResp.json();
          const _cUrunler = _cData.urunler || [];
          if (_cUrunler.length > 0) {
            const baslikEl = document.getElementById('fpFiyatBaslik_cimento');
            if (baslikEl) baslikEl.textContent = 'En ucuz';
            labelEl.textContent = '₺' + parseFloat(_cUrunler[0].fiyat).toLocaleString('tr-TR', {minimumFractionDigits:2, maximumFractionDigits:2});
          }
        }
      } catch(_) {}
    }
  } catch(e) {
    _fpWarn('fiyatGrafikYukle genel hata', { malzeme, canvasId, error: e });
  }
}


async function _fpMarkaKarsilastirmaYukle() {
  const container = document.getElementById('fpMarkaKarsilastirmaPanel');
  if (!container) return;
  try {
    const token = localStorage.getItem('bai_token');
    const resp = await fetch('/api/fiyat/marka-karsilastirma?alt_kategori=cimento', {
      headers: { 'Authorization': 'Bearer ' + token }
    });
    if (!resp.ok) { container.style.display = 'none'; return; }
    const data = await resp.json();
    const urunler = data.urunler || [];
    if (urunler.length === 0) { container.style.display = 'none'; return; }
    container.style.display = 'block';
    const rows = urunler.map((u, i) => `
      <tr style="border-bottom:1px solid #F1F5F9;">
        <td style="padding:8px 12px;font-size:13px;color:#94A3B8;">${i + 1}</td>
        <td style="padding:8px 12px;font-size:13px;color:#0F172A;font-weight:500;">${u.malzeme_ad}</td>
        <td style="padding:8px 12px;font-size:13px;color:#0F172A;text-align:right;font-weight:600;">₺${parseFloat(u.fiyat).toLocaleString('tr-TR', {minimumFractionDigits:2, maximumFractionDigits:2})}</td>
        <td style="padding:8px 12px;font-size:12px;color:#64748B;text-align:right;">${u.birim}</td>
        <td style="padding:8px 12px;font-size:11px;color:#94A3B8;">${(u.son_guncelleme || '').slice(0, 10)}</td>
      </tr>`).join('');
    container.innerHTML = `
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:14px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:4px;">&#127981; Çimento Marka Karşılaştırması</div>
        <div style="font-size:11px;color:#94A3B8;margin-bottom:14px;"></div>
        <div style="overflow-x:auto;">
          <table style="width:100%;border-collapse:collapse;">
            <thead>
              <tr style="background:#F8FAFC;border-bottom:2px solid #E2E8F0;">
                <th style="padding:8px 12px;text-align:left;font-size:11px;color:#64748B;font-weight:600;">#</th>
                <th style="padding:8px 12px;text-align:left;font-size:11px;color:#64748B;font-weight:600;">ÜRÜN</th>
                <th style="padding:8px 12px;text-align:right;font-size:11px;color:#64748B;font-weight:600;">FİYAT</th>
                <th style="padding:8px 12px;text-align:right;font-size:11px;color:#64748B;font-weight:600;">BİRİM</th>
                <th style="padding:8px 12px;text-align:left;font-size:11px;color:#64748B;font-weight:600;">TARİH</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>`;
  } catch(e) { if (container) container.style.display = 'none'; }
}

async function fiyatAiGonder() {
  const inp = document.getElementById('fiyatAiInput');
  const res = document.getElementById('fiyatAiResult');
  const soru = inp.value.trim();
  if (!soru || !res) return;
  res.style.display = 'block';
  res.innerHTML = '<span style="color:#94A3B8;">â³ AI yanıtlıyor...</span>';
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
  if (sp) sp.style.display = 'grid';
  const content = document.getElementById('content');
  if (content) {
    content.style.padding = '0';
    content.style.overflow = 'hidden';
    content.style.gap = '0';
  }
  const stokPageEl = document.getElementById('stokPage');
  if (stokPageEl) stokPageEl.style.width = '100%';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Malzeme Stok Takibi';
  const aktifSantiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
  const globalSantiye = document.getElementById('globalSantiyeSecici');
  const stokSantiye = document.getElementById('stokSantiye');
  if (globalSantiye && stokSantiye && globalSantiye.value) {
      stokSantiye.value = globalSantiye.value;
  }
  stokSantiyeleriYukle().then(() => {
    stokYukle(aktifSantiyeId ? parseInt(aktifSantiyeId) : null);
    stokGecmisYukle();
  });
  stokKatalogYukle();
  stokIsKalemleriYukle();
}

async function stokKatalogYukle() {
  const token = localStorage.getItem('bai_token');
  try {
    const res = await fetch(`/api/katalog/malzemeler?token=${token}`);
    const data = await res.json();
    window._katalogMalzemeMap = {};
    const dl = document.getElementById('katalogMalzemeListesi');
    if (!dl) return;
    dl.innerHTML = '';
    (data.malzemeler || []).forEach(m => {
      window._katalogMalzemeMap[m.ad] = {birim: m.birim, kategori: m.kategori, id: m.id};
      const opt = document.createElement('option');
      opt.value = m.ad;
      opt.label = m.kategori ? `${m.ad} — ${m.kategori}` : m.ad;
      dl.appendChild(opt);
    });
  } catch(e) {}
}

function stokMalzemeSecildi(form) {
  const inputId = form === 'giris' ? 'stokMalzemeInput' : 'sarfMalzemeInput';
  const birimId = form === 'giris' ? 'stokBirim' : 'sarfBirim';
  const input = document.getElementById(inputId);
  const birimInput = document.getElementById(birimId);
  if (!input || !birimInput) return;
  const entry = window._katalogMalzemeMap && window._katalogMalzemeMap[input.value];
  if (entry && entry.birim) birimInput.value = entry.birim;
}

async function stokIsKalemleriYukle() {
  const token = localStorage.getItem('bai_token');
  const santiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye');
  const sel = document.getElementById('sarfIsKalemi');
  if (!sel || !santiyeId) return;
  try {
    const res = await fetch(`/api/v2/santiye/${santiyeId}/is-kalemleri?token=${token}`);
    const data = await res.json();
    sel.innerHTML = '<option value="">İş Kalemi Seç (opsiyonel)</option>';
    (data.is_kalemleri || []).forEach(ik => {
      const opt = document.createElement('option');
      opt.value = ik.id;
      opt.textContent = ik.poz_no ? `${ik.poz_no} — ${ik.tanim}` : ik.tanim;
      sel.appendChild(opt);
    });
  } catch(e) {}
}

async function stokAiSor() {
  const input = document.getElementById('stokAiBarInput');
  const yanitDiv = document.getElementById('stokAiYanit');
  const yanitIcerik = document.getElementById('stokAiYanitIcerik');
  if (!input || !input.value.trim()) return;

  const soru = input.value.trim();
  input.value = '';

  yanitDiv.style.display = 'block';
  yanitIcerik.innerHTML = '<span style="color:#9CA3AF;">Düşünüyorum...</span>';

  const token = localStorage.getItem('bai_token');
  const aktifSantiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';

  try {
    const res = await fetch('/ai-komut', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        token: token,
        komut: soru,
        santiye_id: aktifSantiyeId ? parseInt(aktifSantiyeId) : null,
        sayfa: 'stok'
      })
    });
    const data = await res.json();

    if (data.yanit) {
      yanitIcerik.textContent = data.yanit;
    } else if (data.error) {
      yanitIcerik.innerHTML = '<span style="color:#DC2626;">Hata: ' + data.error + '</span>';
    } else {
      yanitIcerik.textContent = JSON.stringify(data);
    }

    if (data.islem_yapildi) {
      stokYukle(aktifSantiyeId ? parseInt(aktifSantiyeId) : null);
    }
  } catch(e) {
    yanitIcerik.innerHTML = '<span style="color:#DC2626;">Bağlantı hatası.</span>';
  }
}

function stokPageKapat() {
  const sp = document.getElementById('stokPage');
  if (sp) sp.style.display = 'none';
  const content = document.getElementById('content');
  const cmdBar  = document.getElementById('aiCommandBar');
  if (content) {
    content.style.display = 'flex';
    content.style.padding = '';
    content.style.overflow = '';
    content.style.gap = '';
  }
  if (cmdBar) cmdBar.style.display  = 'block';
  const titleEl = document.getElementById('contentTitle');
  if (titleEl) titleEl.textContent = 'Genel Bakış';
}

async function stokAiGonder() {
  const inp = document.getElementById('stokAiInput');
  const res = document.getElementById('stokAiResult');
  const soru = inp.value.trim();
  if (!soru || !res) return;
  res.style.display = 'block';
  res.innerHTML = '<span style="color:#94A3B8;">â³ AI yanıtlıyor...</span>';
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
  ekipYukle();
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
    iyi:    { bg:'#F0FDF4', border:'#86EFAC', txt:'#16A34A', icon:'',  lbl:'İyi (manuel)'    },
    dikkat: { bg:'#FFF7ED', border:'#FED7AA', txt:'#EA580C', icon:'?',  lbl:'Gecikme Riski'},
    sorun:  { bg:'#FEF2F2', border:'#FECACA', txt:'#DC2626', icon:'âœ•',  lbl:'Kritik Sorun' },
  };

  // İmaj gradients ?? durum rengine göre
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
    const cfg = durumCfg[s.durum] || {bg:'#F1F5F9', border:'#CBD5E1', txt:'#475569', icon:'', lbl:'Takvim değerlendirmesi yok'};
    return `<span class="sp-badge" style="background:${cfg.bg};color:${cfg.txt};border:1px solid ${cfg.border};">
      <span>${cfg.icon}</span>${cfg.lbl}
    </span>`;
  }

  function hiyerarsiButton(s) {
    const id = String(s.id || '').replace(/'/g, "'");
    const ad = String(s.ad || '').replace(/[\r\n]/g, '').replace(/'/g, "'").replace(/"/g, '&quot;');
    return `<button onclick="event.stopPropagation(); document.getElementById('globalSantiyeSecici').value='${id}'; globalSantiyeDegisti(); navGit('hiyerarsi');"
      style="margin-top:10px;width:100%;display:flex;align-items:center;justify-content:center;gap:6px;background:#EFF6FF;border:1px solid #BFDBFE;color:#2563EB;border-radius:8px;padding:8px 10px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit;">
      Metraj Yönetimi
    </button>`;
  }

  // Boş durum
  if (liste.length === 0) {
    const empty = `<div style="grid-column:1/-1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:60px 20px;gap:14px;">
      <div style="font-size:52px;"></div>
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
      const pct = s.ilerleme == null ? null : Math.min(100, Math.max(0, s.ilerleme));
      return `<div class="sp-kart-horiz" onclick="santiyeEkleModalAc(${JSON.stringify(s).replace(/"/g,'&quot;')})">
        ${imgDiv(s, i, '110px', '90px', '10px')}
        <div style="flex:1;min-width:0;">
          <div style="font-size:14px;font-weight:700;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${s.ad || 'Şantiye'}</div>
          <div style="font-size:11px;color:#94A3B8;margin-top:3px;display:flex;align-items:center;gap:3px;">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            ${s.konum || '?'}
          </div>
          ${pct == null ? '<div>İlerleme: veri yok</div>' : progressBar(pct)}
          ${badge(s)}
          ${hiyerarsiButton(s)}
        </div>
      </div>`;
    }).join('');
  }

  // Dikey grid (tümü)
  const gridEl = document.getElementById('santiyePageGrid');
  if (gridEl) {
    gridEl.innerHTML = liste.map((s, i) => {
      const pct = s.ilerleme == null ? null : Math.min(100, Math.max(0, s.ilerleme));
      return `<div class="sp-kart-vert" onclick="santiyeEkleModalAc(${JSON.stringify(s).replace(/"/g,'&quot;')})">
        ${imgDiv(s, i, '100%', '160px', '0')}
        <div style="padding:12px 14px;">
          <div style="font-size:13px;font-weight:700;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${s.ad || 'Şantiye'}</div>
          <div style="font-size:11px;color:#94A3B8;margin-top:2px;display:flex;align-items:center;gap:3px;">
            <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            ${s.konum || '?'}
          </div>
          ${pct == null ? '<div>İlerleme: veri yok</div>' : progressBar(pct)}
          ${badge(s)}
          ${hiyerarsiButton(s)}
        </div>
      </div>`;
    }).join('');
  }
}

// Dashboard modülleri ?? auth tamamlanınca otomatik yükle
window.addEventListener('load', function() {
  setTimeout(function() {
    const token = localStorage.getItem('bai_token');
    const rol = localStorage.getItem('bai_rol');
    if (token && isEngineerRole(rol) && document.getElementById('engineerDashboard')) {
      loadEngineerDashboard();
      return;
    }
    if (token && isContractorRole(rol) && document.getElementById('contractorDashboard')) {
      loadContractorDashboard();
      return;
    }
    if (token && document.getElementById('sahaGunluguListe')) {
      sahaGunluguYukle();
      aiAlertsYukle();
    }
  }, 2000);
});

// â"€â"€ Content Header: tarih, kullanıcı adı, online durum â"€â"€
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
    if (statusBtn) { statusBtn.style.borderColor='#10B981'; }
    const svg = statusBtn && statusBtn.querySelector('svg');
    if (svg) svg.style.stroke = '#10B981';
    if (statusText) statusText.style.color = '#10B981';
    if (queueBadge) queueBadge.style.display = 'none';
  } else {
    if (statusText) statusText.textContent = 'İnternet Yok';
    if (statusBtn) { statusBtn.style.borderColor='#F97316'; }
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
// 🔐§ AYARLAR SAYFASI ?? ANA ROUTER
// ═══════════════════════════════════════════════════

function sayfaGoster(sayfa) {
  // Avatar menüyü kapat
  const menu = document.getElementById('avatarMenu');
  if (menu) menu.style.display = 'none';

  if (sayfa === 'ayarlar') {
    // Diğer sayfaları kapat (içerik+cmdBar gösterme)
    ['santiyePage','fiyatPage','stokPage','kameraPage','arsivPage','sahaKayitlariPage','hiyerarsiPage','hakedisPage','engineerDashboard','contractorDashboard'].forEach(pid => {
      const el = document.getElementById(pid);
      if (el) el.style.display = 'none';
    });
    const content    = document.getElementById('content');
    const cmdBar     = document.getElementById('aiCommandBar');
    const ayarlarPage = document.getElementById('ayarlarPage');
    if (content)      content.style.display    = 'none';
    if (cmdBar)       cmdBar.style.display     = 'none';
    if (ayarlarPage) ayarlarPage.style.display = 'flex';
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

// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
// KATEGORİ GÖSTERİCİ
// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

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
  const plan   = normalizePlan(window._kullaniciPlan || user.plan || 'baslangic');
  const initials = isim ? isim.split(' ').filter(Boolean).map(w => w[0]).join('').toUpperCase().slice(0,2) : 'U';
  const orgName = kUser.organization_name || user.organization_name || '';
  const orgId = kUser.organization_id || user.organization_id || '';
  const orgOwnerId = kUser.organization_owner_user_id || user.organization_owner_user_id || '';
  const currentUserId = kUser.id || kUser.user_id || user.id || user.user_id || '';
  const canEditCompany = Boolean(orgOwnerId && currentUserId && String(orgOwnerId) === String(currentUserId));

  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  // 1. PROFİL & HESAP
  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  if (id === 'profil') {
    const planLabel = {baslangic:'Başlangıç', profesyonel:'Profesyonel', admin:'📋¸ Admin'};
    const rolKayitli = localStorage.getItem('bai_rol') || 'santi_sefi';
    const isAdmin = Boolean(user.is_admin);
    const companyFieldHtml = canEditCompany ? `
            <input id="ayarlarSirketAdi" type="text" value="${String(orgName).replace(/"/g,'&quot;')}"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;transition:border-color 0.15s;"
              onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#E2E8F0'">` : `
            <div id="ayarlarSirketAdiReadonly"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#64748B;box-sizing:border-box;">
              ${orgName ? String(orgName).replace(/</g,'&lt;').replace(/>/g,'&gt;') : '?'}
            </div>`;
    const rolFieldHtml = isAdmin ? `
            <select id="ayarlarRol"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#1E293B;box-sizing:border-box;outline:none;cursor:pointer;transition:border-color 0.15s;"
              onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#E2E8F0'">
              <option value="muhendis" ? ${rolKayitli==='muhendis' ? 'selected':''}>Mühendis</option>
              <option value="santi_sefi" ? ${(!rolKayitli || rolKayitli==='santi_sefi') ? 'selected':''}>Şantiye Şefi</option>
              <option value="mutahhit" ? ${rolKayitli==='mutahhit' ? 'selected':''}>Müteahhit</option>
              <option value="proje_muduru" ${rolKayitli==='proje_muduru' ? 'selected':''}>Proje Müdürü</option>
            </select>` : `
            <div id="ayarlarRolReadonly"
              style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#64748B;box-sizing:border-box;">
              ${getRoleLabel(rolKayitli)}
            </div>`;
    icerik.innerHTML = `
      <div style="margin-bottom:24px;">
        <div style="font-size:22px;font-weight:700;color:#0F172A;margin-bottom:4px;">Profil &amp; Hesap</div>
        <div style="font-size:13px;color:#64748B;">Kişisel bilgilerini yönet</div>
      </div>

      <!-- Kart 1: Profil Bilgileri -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid #F1F5F9;">
          <div style="width:64px;height:64px;border-radius:50%;background:#0D1117;display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:700;color:white;flex-shrink:0;position:relative;overflow:hidden;">
            <span id="profilAvatarInitials">${initials}</span>
            <img id="profilAvatarImg" style="display:none;position:absolute;top:0;left:0;width:100%;height:100%;border-radius:50%;object-fit:cover;" />
          </div>
          <div>
            <div style="font-size:16px;font-weight:700;color:#0F172A;">${isim || 'Kullanıcı'}</div>
            <div style="font-size:13px;color:#64748B;margin-top:2px;">${email}</div>
            <div style="display:inline-block;margin-top:6px;background:#EEF2FF;color:#6366F1;font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;">${planLabel[plan] || 'Başlangıç'}</div>
          </div>
        </div>
        <div style="margin-bottom:20px;">
            <input type="file" id="avatarFileInput" accept="image/jpeg,image/png" style="display:none" onchange="avatarYukle(this)">
            <button onclick="document.getElementById('avatarFileInput').click()" style="background:#6366F1;color:#fff;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;">
                Fotograf Yukle
            </button>
            <button id="pozisyonAyarlaBtn" onclick="const u=JSON.parse(localStorage.getItem('bai_user')||'{}'); if(u.avatar_url) avatarPozisyonEditorGoster(u.avatar_url); else { const s=document.getElementById('avatarUploadStatus'); if(s){s.textContent='Once fotograf yukleyin';s.style.color='#F59E0B';}}" style="background:transparent;color:#94A3B8;border:1px solid rgba(255,255,255,0.15);padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;margin-left:8px;">
                Pozisyonu Ayarla
            </button>
            <span id="avatarUploadStatus" style="margin-left:10px;font-size:12px;color:#94A3B8;"></span>
        </div>
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
              <span style="position:absolute;right:12px;top:50%;transform:translateY(-50%);color:#94A3B8;font-size:14px;">📁</span>
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
            ${rolFieldHtml}
          </div>
          <div>
            <label style="font-size:12px;font-weight:600;color:#64748B;display:block;margin-bottom:6px;">Şirket Adı</label>
            ${companyFieldHtml}
          </div>
          <div>
            <label style="font-size:12px;font-weight:600;color:#64748B;display:block;margin-bottom:6px;">Organizasyon ID</label>
            <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;width:100%;color:#64748B;box-sizing:border-box;">
              ${orgId || '?'}
            </div>
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
              style="padding:8px 18px;border-radius:20px;border:1.5px solid #6366f1;background:#EEF2FF;color:#6366F1;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.15s;">🇬Ÿ‡· Türkçe</button>
            <button id="dilEN" onclick="ayarlarDilSec('en')"
              style="padding:8px 18px;border-radius:20px;border:1.5px solid #E2E8F0;background:#F8FAFC;color:#64748B;font-size:13px;font-weight:600;cursor:pointer;transition:all 0.15s;">🇬Ÿ‡§ English</button>
          </div>
        </div>
        <div>
          <div style="font-size:12px;font-weight:600;color:#64748B;margin-bottom:8px;">Tarih Formatı</div>
          <select id="tarihFormat" onchange="localStorage.setItem('tarih_format',this.value)"
            style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;font-size:14px;color:#1E293B;outline:none;cursor:pointer;min-width:220px;">
            <option value="DD.MM.YYYY" ${(localStorage.getItem('tarih_format')||'DD.MM.YYYY')==='DD.MM.YYYY' ? 'selected':''}>GG.AA.YYYY (Türkiye)</option>
            <option value="YYYY-MM-DD" ${localStorage.getItem('tarih_format')==='YYYY-MM-DD' ? 'selected':''}>YYYY-MM-DD (ISO)</option>
          </select>
        </div>
      </div>`;
    const _u = JSON.parse(localStorage.getItem('bai_user') || '{}');
    if (_u.avatar_url) avatarGuncelle(_u.avatar_url, _u.avatar_position, _u.avatar_scale);

  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  // 2. ŞANTİYE VARSAYILANLARI
  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  } else if (id === 'santiye') {
    const birimler = JSON.parse(localStorage.getItem('birim_sistemi') || '{}');
    const uz  = birimler.uzunluk || 'Metre';
    const al  = birimler.alan    || 'm?';
    const ag  = birimler.agirlik || 'kg';
    const saatler = JSON.parse(localStorage.getItem('calisma_saatleri') || '{"baslangic":"08:00","bitis":"18:00","gunler":["Pzt","Sal","Çar","Per","Cum"]}');
    const aktifGunler = saatler.gunler || ['Pzt','Sal','Çar','Per','Cum'];
    const gunler = ['Paz','Pzt','Sal','Çar','Per','Cum','Cmt'];
    const birimRows = [
      {tip:'uzunluk', label:'Uzunluk', u1:'Metre', u2:'Feet', cur:uz},
      {tip:'alan',    label:'Alan',    u1:'m?',    u2:'ft?',  cur:al},
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
        + ' style="width:44px;height:24px;border-radius:12px;cursor:pointer;background:' + (on ? '#3B82F6':'#CBD5E1') + ';position:relative;transition:background 0.25s;flex-shrink:0;">'
        + '<div style="position:absolute;top:3px;width:18px;height:18px;border-radius:50%;background:white;box-shadow:0 1px 3px rgba(0,0,0,0.2);transition:left 0.25s;left:' + (on ? '23px':'3px') + ';"></div>'
        + '</div>'
        + '<span id="tog-label-' + b.tip + '" style="font-size:13px;font-weight:600;color:#0F172A;">' + b.cur + '</span>'
        + '</div></div>';
    }).join('') + '</div>';
    const gunlerHTML = gunler.map(function(g) {
      const ak = aktifGunler.includes(g);
      return '<button onclick="calismaGunToggle(\'' + g + '\',this)"'
        + ' style="padding:6px 14px;border-radius:20px;border:none;cursor:pointer;font-size:13px;font-weight:600;'
        + 'background:' + (ak ? '#3B82F6':'#1E293B') + ';color:white;transition:all 0.15s;">' + g + '</button>';
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

  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  // 3. AI ASİSTAN
  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
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
                     border:${yanit===s.k ? '2px solid #6366F1':'1px solid #E2E8F0'};
                     background:${yanit===s.k ? '#EEF2FF':'#FFFFFF'};
                     color:${yanit===s.k ? '#4338CA':'#1E293B'};">
              <div style="font-size:14px;font-weight:700;margin-bottom:6px;">${s.baslik}</div>
              <div style="font-size:12px;color:#64748B;">${s.aciklama}</div>
            </div>`).join('')}
        </div>
      </div>

      <!-- Kart 1b: Konuşma Tonu -->
      <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:24px;margin-bottom:16px;">
        <div style="font-size:15px;font-weight:700;color:#1E293B;margin-bottom:4px;">Konuşma Tonu</div>
        <div style="font-size:12px;color:#64748B;margin-bottom:16px;">AI'ın sana nasıl hitap etmesini istiyorsun</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;">
          ${tonSecenekler.map(t => `
            <div onclick="aiKonusmaTonuSec('${t.k}')" id="aiTon-${t.k}"
              style="padding:16px;border-radius:10px;cursor:pointer;text-align:center;transition:all 0.15s;
                     border:${ton===t.k ? '2px solid #6366F1':'1px solid #E2E8F0'};
                     background:${ton===t.k ? '#EEF2FF':'#FFFFFF'};
                     color:${ton===t.k ? '#4338CA':'#1E293B'};">
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
            <div style="font-size:15px;font-weight:700;color:#1E293B;">🎙 Ses Asistanı</div>
            <div style="font-size:12px;color:#64748B;margin-top:2px;">Yanıtları sesli dinle</div>
          </div>
          <label style="position:relative;display:inline-block;width:44px;height:24px;cursor:pointer;flex-shrink:0;">
            <input type="checkbox" ${sesAcik ? 'checked':''} onchange="aiSesToggle(this)" style="opacity:0;width:0;height:0;position:absolute;">
            <span id="sesTrack" style="position:absolute;inset:0;background:${sesAcik ? '#6366f1':'#CBD5E1'};border-radius:24px;transition:0.3s;"></span>
            <span id="sesKnob" ? style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:${sesAcik ? '23px':'3px'};transition:0.3s;box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
          </label>
        </div>
        <div id="sesAyarlari" style="display:${sesAcik ? 'block':'none'};margin-top:16px;border-top:1px solid #F1F5F9;padding-top:16px;">
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
            <input type="checkbox" ${bellekAcik ? 'checked':''} onchange="localStorage.setItem('ai_bellek',this.checked);this.closest('label').querySelector('span:first-of-type').style.background=this.checked ? '#6366f1':'#CBD5E1';this.closest('label').querySelector('span:last-of-type').style.left=this.checked ? '23px':'3px';" style="opacity:0;width:0;height:0;position:absolute;">
            <span style="position:absolute;inset:0;background:${bellekAcik ? '#6366f1':'#CBD5E1'};border-radius:24px;transition:0.3s;"></span>
            <span style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:${bellekAcik ? '23px':'3px'};transition:0.3s;box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
          </label>
        </div>
        <button onclick="if(confirm('Tüm AI belleği silinecek. Emin misiniz')){localStorage.removeItem('ai_bellek_data');localStorage.removeItem('konusma_gecmisi');showToast('AI belleği temizlendi','success');}"
          style="border:1px solid #EF4444;color:#EF4444;background:transparent;border-radius:8px;padding:8px 16px;font-size:14px;cursor:pointer;font-weight:600;transition:all 0.15s;"
          onmouseover="this.style.background='#FEF2F2'" onmouseout="this.style.background='transparent'">🗑¸ Belleği Temizle</button>
      </div>`;
    hizliKomutListesiGuncelle();

  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  // 4. BİLDİRİM KANALLARI
  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
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
              <span style="font-size:20px;">📱</span>
              <div>
                <div style="font-size:14px;font-weight:600;color:#0F172A;">E-posta</div>
                <div style="font-size:12px;color:#94A3B8;margin-top:1px;">Önemli olaylar için e-posta al</div>
              </div>
            </div>
            <label style="position:relative;display:inline-block;width:44px;height:24px;cursor:pointer;flex-shrink:0;">
              <input type="checkbox" id="epostaToggle" ${epAcik ? 'checked':''} onchange="epostaToggleAyar(this)" style="opacity:0;width:0;height:0;position:absolute;">
              <span id="epostaToggleSpan" style="position:absolute;inset:0;background:${epAcik ? '#6366f1':'#CBD5E1'};border-radius:24px;transition:0.3s;"></span>
              <span id="epostaToggleKnob" style="position:absolute;width:18px;height:18px;background:white;border-radius:50%;top:3px;left:${epAcik ? '23px':'3px'};transition:0.3s;box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
            </label>
          </div>
          <div id="epostaAyarlar" style="display:${epAcik ? 'block':'none'};padding:0 20px 16px 52px;background:#FAFAFA;">
            <div style="display:flex;flex-direction:column;gap:10px;">
              ${[
                {k:'eposta_stok',   label:'Stok uyarıları',       def: bil.eposta_stok !== false},
                {k:'eposta_isg',    label:'ISG ihlalleri',         def: bil.eposta_isg   !== false},
                {k:'eposta_rapor',  label:'Günlük rapor özeti',    def: !!bil.eposta_rapor},
                {k:'eposta_sistem', label:'Sistem bildirimleri',   def: !!bil.eposta_sistem}
              ].map(item => `
                <label style="display:flex;align-items:center;gap:10px;cursor:pointer;font-size:13px;color:#1E293B;">
                  <input type="checkbox" ${item.def ? 'checked':''} onchange="bildirimKaydet('${item.k}',this.checked)"
                    style="width:16px;height:16px;accent-color:#6366f1;cursor:pointer;">
                  ${item.label}
                </label>`).join('')}
            </div>
          </div>
        </div>

        <!-- WhatsApp -->
        <div style="padding:16px 20px;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;justify-content:space-between;">
          <div style="display:flex;align-items:center;gap:12px;">
            <span style="font-size:20px;">📱</span>
            <div>
              <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:14px;font-weight:600;color:#0F172A;">WhatsApp</span>
                <span style="background:#FEF3C7;color:#D97706;font-size:11px;font-weight:600;padding:2px 8px;border-radius:20px;">Yakında</span>
              </div>
              <div style="font-size:12px;color:#94A3B8;margin-top:1px;">WhatsApp entegrasyonu için Profesyonel plan gerekli</div>
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
            <span style="font-size:20px;">📱</span>
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

  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  // 5. PLAN & ÖDEME
  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  } else if (id === 'plan') {
    const planRenk = {
      baslangic:    {bg:'#F1F5F9', color:'#64748B',  label:'Başlangıç'},
      profesyonel:  {bg:'#F0FDF4', color:'#16A34A',  label:'Profesyonel'},
      admin: {bg:'#F0FDF4', color:'#16A34A',  label:'📋¸ Admin'}
    };
    const pr = planRenk[plan] || planRenk.baslangic;
    const upgradePlan = 'profesyonel';
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
        ${(plan !== 'profesyonel' && plan !== 'admin') ? `
          <button onclick="odemePaneliAc('${upgradePlan}')"
            style="background:#6366f1;color:white;border:none;border-radius:8px;padding:10px 20px;font-size:13px;font-weight:700;cursor:pointer;transition:background 0.15s;"
            onmouseover="this.style.background='#4F46E5'" onmouseout="this.style.background='#6366f1'">
            Profesyonel'e Geç
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
          â„¹ï¸ Manuel IBAN ile ödeme aktif
        </div>
        <button onclick="odemePaneliAc('profesyonel')"
          style="border:1.5px solid #6366f1;background:transparent;color:#6366f1;border-radius:8px;padding:10px 20px;font-size:13px;font-weight:700;cursor:pointer;transition:all 0.15s;"
          onmouseover="this.style.background='#EEF2FF'" onmouseout="this.style.background='transparent'">🏠’³ Ödeme Bildir</button>
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

  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  // 6. GÜVENLİK & GİZLİLİK
  // â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
  } else if (id === 'guvenlik') {
    const hasPassword = kUser.has_password !== undefined ? Boolean(kUser.has_password) : Boolean(user.has_password);
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
          onmouseover="this.style.background='#FEF2F2'" onmouseout="this.style.background='transparent'">🗑¸ Hesabımı Sil</button>
        <div style="font-size:12px;color:#94A3B8;margin-top:8px;">Bu işlem geri alınamaz. Tüm verileriniz kalıcı olarak silinir.</div>
      </div>`;
    if (!hasPassword) {
      const currentPassword = document.getElementById('mevcutSifre');
      if (currentPassword && currentPassword.parentElement) currentPassword.parentElement.style.display = 'none';
      const passwordCard = currentPassword ? currentPassword.closest('div[style*="padding:24px"]') : null;
      if (passwordCard) {
        const title = passwordCard.querySelector('div[style*="font-size:15px"]');
        if (title) title.textContent = 'Şifre Belirle';
        const fields = passwordCard.querySelector('div[style*="flex-direction:column"]');
        if (fields) {
          fields.insertAdjacentHTML('beforebegin', '<div style="font-size:13px;color:#64748B;line-height:1.6;margin-bottom:16px;"><div>Bu hesap Google ile oluşturuldu.</div><div>Email ve şifre ile de giriş yapmak isterseniz BuildingAI şifresi belirleyebilirsiniz.</div></div>');
        }
        const newPassword = document.getElementById('yeniSifre');
        if (newPassword) newPassword.placeholder = 'Yeni Şifre';
        const confirmPassword = document.getElementById('yeniSifreTekrar');
        if (confirmPassword) confirmPassword.placeholder = 'Yeni Şifre (Tekrar)';
        const button = passwordCard.querySelector('button[onclick="sifreGuncelle()"]');
        if (button) button.textContent = 'Şifre Belirle';
      }
    }
  }
}

// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
// YARDIMCI FONKSİYONLAR ?? Şantiye Varsayılanları
// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

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
  const pairs = {uzunluk:['Metre','Feet'], alan:['m?','ft?'], agirlik:['kg','lb']};
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

// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
// YARDIMCI FONKSİYONLAR ?? AI Asistan
// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

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
      <span style="color:#CBD5E1;font-size:16px;cursor:grab;user-select:none;">â ¿</span>
      <span style="flex:1;font-size:14px;color:#1E293B;">${k}</span>
      <button onclick="hizliKomutSil(${i})"
        style="background:none;border:none;cursor:pointer;color:#94A3B8;font-size:16px;padding:0;line-height:1;transition:color 0.15s;"
        onmouseover="this.style.color='#EF4444'" onmouseout="this.style.color='#94A3B8'">🚀</button>
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
  if (track) track.style.background = cb.checked ? '#6366f1' : '#CBD5E1';
  if (knob) knob.style.left        = cb.checked ? '23px' : '3px';
}

// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
// YARDIMCI FONKSİYONLAR ?? Bildirimler
// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

function epostaToggleAyar(cb) {
  const bil = JSON.parse(localStorage.getItem('bildirim_kanallar') || '{}');
  bil.eposta = cb.checked;
  localStorage.setItem('bildirim_kanallar', JSON.stringify(bil));
  const ayarlar = document.getElementById('epostaAyarlar');
  const span    = document.getElementById('epostaToggleSpan');
  const knob    = document.getElementById('epostaToggleKnob');
  if (ayarlar) ayarlar.style.display  = cb.checked ? 'block' : 'none';
  if (span) span.style.background  = cb.checked ? '#6366f1' : '#CBD5E1';
  if (knob) knob.style.left        = cb.checked ? '23px' : '3px';
}

function bildirimKaydet(key, val) {
  const bil = JSON.parse(localStorage.getItem('bildirim_kanallar') || '{}');
  bil[key] = val;
  localStorage.setItem('bildirim_kanallar', JSON.stringify(bil));
}

// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
// YARDIMCI FONKSİYONLAR ?? Plan & Kullanım
// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

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
        const label = m.limit === null ? `${m.used} / âˆ` : `${m.used} / ${m.limit}`;
        return `
          <div style="margin-bottom:14px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
              <span style="font-size:13px;color:#64748B;font-weight:500;">${m.label}</span>
              <span style="font-size:13px;font-weight:700;color:#0F172A;">${label}</span>
            </div>
            <div style="height:6px;background:#E2E8F0;border-radius:3px;overflow:hidden;">
              <div style="height:100%;width:${pct}%;background:${m.limit===null ? '#3B82F6':'#6366f1'};border-radius:3px;transition:width 0.4s;"></div>
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
    const res  = await fetch(`/odeme-bildirimitoken=${token}`);
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
              <td style="padding:10px 0;font-size:13px;color:#1E293B;">${o.tarih||'?'}</td>
              <td style="padding:10px 0;font-size:13px;color:#1E293B;font-weight:600;">${o.tutar||'?'}</td>
              <td style="padding:10px 0;">
                <span style="background:${o.durum==='onaylandi' ? '#F0FDF4':'#FFFBEB'};color:${o.durum==='onaylandi' ? '#16A34A':'#D97706'};font-size:11px;font-weight:600;padding:3px 10px;border-radius:20px;">
                  ${o.durum==='onaylandi' ? 'Onaylandı':'Bekliyor'}
                </span>
              </td>
            </tr>`).join('')}
        </tbody>
      </table>`;
  } catch(e) {
    if (kart) kart.innerHTML = '<div style="font-size:15px;font-weight:700;color:#0F172A;margin-bottom:12px;">Fatura Geçmişi</div><div style="text-align:center;padding:24px;color:#94A3B8;font-size:13px;">Henüz ödeme geçmişi yok</div>';
  }
}

// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
// YARDIMCI FONKSİYONLAR ?? Güvenlik
// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

function sifreGoster(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.type     = input.type === 'password' ? 'text' : 'password';
  btn.textContent = input.type === 'text' ? '🙈' : '👁';
}

async function sifreGuncelle() {
  const mevcut = document.getElementById('mevcutSifre').value;
  const yeni   = document.getElementById('yeniSifre').value;
  const tekrar = document.getElementById('yeniSifreTekrar').value;
  const user = JSON.parse(localStorage.getItem('bai_user') || '{}');
  const hasPassword = user.has_password !== false;
  if (hasPassword && !mevcut)           { showToast('Mevcut sifre alanini doldurun', 'error'); return; }
  if (!yeni || !tekrar)                 { showToast('Tum alanlari doldurun', 'error'); return; }
  if (yeni !== tekrar)                  { showToast('Yeni sifreler eslesmiyor', 'error'); return; }
  if (yeni.length < 8)                  { showToast('Sifre en az 8 karakter olmali', 'error'); return; }
  const token = localStorage.getItem('bai_token');
  try {
    const res  = await fetch('/hesap/sifre', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({token, mevcut_sifre: mevcut, yeni_sifre: yeni})
    });
    const data = await res.json();
    if (res.ok) {
      applyServerUserProfile(data);
      showToast(hasPassword ? 'Sifre basariyla guncellendi' : 'Sifre basariyla belirlendi', 'success');
      ['mevcutSifre','yeniSifre','yeniSifreTekrar'].forEach(id => {
        const el = document.getElementById(id); if (el) el.value = '';
      });
      const bar = document.getElementById('sifreGucBar');
      if (bar) bar.style.display = 'none';
      if (!hasPassword) ayarlarKategoriGoster('guvenlik');
    } else { showToast(data.detail || data.hata || 'Sifre guncellenemedi', 'error'); }
  } catch(e) { showToast('Baglanti hatasi', 'error'); }
}

function hesapSilOnay() {
  if (!confirm('Hesabınız kalıcı olarak silinecek. Devam et')) return;
  const sifre = prompt('Silmek için şifrenizi girin:');
  if (!sifre) return;
  showToast('Bu işlem için destek ekibiyle iletişime geçin', 'info');
}

// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
// YARDIMCI FONKSİYONLAR ?? Dil
// â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

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
// 👁¤ PROFİL KAYDET
// ═══════════════════════════════════════════════════

async function profilKaydet() {
  const adSoyad = document.getElementById('ayarlarAdSoyad').value.trim();
  const telefon = document.getElementById('ayarlarTelefon').value.trim();
  const rolEl   = document.getElementById('ayarlarRol');
  const sirketEl = document.getElementById('ayarlarSirketAdi');
  const sirketAdi = sirketEl.value.trim();
  const user = JSON.parse(localStorage.getItem('bai_user') || '{}');
  const isAdmin = Boolean(user.is_admin);
  const rol     = rolEl.value || localStorage.getItem('bai_rol') || user.role || user.rol || 'santi_sefi';
  if (!adSoyad) { showToast('Ad Soyad alanı boş bırakılamaz', 'error'); return; }

  if (sirketEl && !sirketAdi) { showToast('Şirket Adı alanı boş bırakılamaz', 'error'); return; }

  user.full_name = adSoyad;
  user.telefon   = telefon;
  if (sirketEl) user.organization_name = sirketAdi;
  if (isAdmin && rolEl) {
    user.rol       = rol;
    user.role      = rol;
  }
  localStorage.setItem('bai_user', JSON.stringify(user));
  if (isAdmin && rolEl && rol) localStorage.setItem('bai_rol', rol);

  if (aktifKullanici) {
    aktifKullanici.full_name = adSoyad;
    aktifKullanici.telefon = telefon;
    if (sirketEl) aktifKullanici.organization_name = sirketAdi;
    if (isAdmin && rolEl) aktifKullanici.role = rol;
  }

  // Header güncelle
  const headerName = document.getElementById('headerUserName');
  if (headerName) headerName.textContent = adSoyad;
  const headerRole = document.getElementById('headerUserRole');
  if (headerRole) headerRole.textContent = getWorkspaceRoleLabel(rol);
  const headerAvt = document.getElementById('headerAvatar');
  if (headerAvt) {
    headerAvt.textContent = adSoyad.split(' ').filter(Boolean).map(w=>w[0]).join('').toUpperCase().slice(0,2);
  }
  const profilePayload = { full_name: adSoyad, telefon };
  if (sirketEl) profilePayload.sirket_adi = sirketAdi;
  if (isAdmin && rolEl) profilePayload.role = rol;
  await syncProfileToServer(profilePayload, { silent: true });
  updateSidebarOrganizationName(user);
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
// 👁¤ AVATAR DROPDOWN MENU
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
    const rolLabel = getWorkspaceRoleLabel(localStorage.getItem('bai_rol') || kUser.role || kUser.rol);

    const amAvatar = document.getElementById('amAvatar');
    const amName   = document.getElementById('amName');
    const amEmail  = document.getElementById('amEmail');
    const amRole   = document.getElementById('amRole');
    if (amAvatar) amAvatar.textContent = initials;
    if (amName)   amName.textContent   = isim;
    if (amEmail) amEmail.textContent  = email;
    if (amRole)   amRole.textContent   = rolLabel;

    // Aktif şantiye
    const varSantiye    = JSON.parse(localStorage.getItem('varsayilan_santiye') || 'null');
    const amSantiyeAd   = document.getElementById('amSantiyeAd');
    const amSantiyeBar  = document.getElementById('amSantiyeBar');
    const amSantiyeAlt  = document.getElementById('amSantiyeAlt');
    if (varSantiye && amSantiyeAd) {
      amSantiyeAd.textContent  = varSantiye.ad || '?';
      if (amSantiyeBar) setTimeout(() => amSantiyeBar.style.width = (varSantiye.ilerleme||0)+'%', 50);
      if (amSantiyeAlt) amSantiyeAlt.textContent = `%${varSantiye.ilerleme||0} ? ${varSantiye.isci_sayisi||0} işçi`;
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

let _engineerDecisionFilter = 'pending';
let _engineerDecisionExpanded = false;
let _engineerSecretaryCollapsed = false;
let _contractorCommandCollapsed = false;

function engineerDecisionModeToStatus(mode) {
  if (mode === 'approve') return 'approved';
  if (mode === 'reject') return 'rejected';
  if (mode === 'correct') return 'correction_requested';
  return 'pending';
}

function engineerReviewStatusLabel(status) {
  const map = {
    pending: 'Bekliyor',
    in_review: 'İnceleniyor',
    approved: 'Onaylandı',
    rejected: 'Reddedildi',
    correction_requested: 'Düzeltme İstendi',
  };
  return map[status] || 'Bekliyor';
}

function engineerNormalizeCategory(category, sourceType) {
  if (category === 'ISG' || category === 'Stok' || category === 'Rapor') return category;
  if (sourceType === 'alert') return 'Stok';
  if (sourceType === 'report') return 'Rapor';
  return 'ISG';
}

function engineerNormalizeDateParts(value) {
  if (!value) return { dateLabel: 'Tarih yok', timeLabel: '', sortValue: 0, fullLabel: 'Tarih yok' };
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return { dateLabel: value, timeLabel: '', sortValue: 0, fullLabel: value };
  }
  return {
    dateLabel: parsed.toLocaleDateString('tr-TR', { day: '2-digit', month: 'short' }),
    timeLabel: parsed.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }),
    sortValue: parsed.getTime(),
    fullLabel: parsed.toLocaleString('tr-TR', { day: '2-digit', month: 'long', hour: '2-digit', minute: '2-digit' }),
  };
}

function engineerDecisionSortValue(item) {
  return engineerNormalizeDateParts(item.sortTimestamp || item.decidedAt || item.createdAt).sortValue;
}

function _sanitizeDeltaLabel(raw) {
  if (!raw) return '';
  const s = String(raw).trim();
  if (s === 'Anormal veri') return s;
  // Strip % and sign to get the numeric magnitude
  const num = parseFloat(s.replace('%', '').replace(',', '.'));
  if (isNaN(num)) return s;
  if (Math.abs(num) > 999.9) return 'Anormal veri';
  return s;
}

function engineerNormalizeReviewItem(item) {
  const sourceType = String(item.source_type || item.kind || 'evidence').toLowerCase();
  const primaryDate = engineerNormalizeDateParts(item.created_at || item.timestamp || item.createdAt || '');
  const decidedDate = engineerNormalizeDateParts(item.decided_at || item.decidedAt || '');
  const category = engineerNormalizeCategory(item.category, sourceType);
  const status = String(item.status || 'pending').toLowerCase();
  const title = item.title || 'Saha kaydı';
  const siteName = item.site_name || item.siteName || item.zone_label || 'Şantiye etiketi yok';
  const zoneLabel = item.zone_label || item.zoneLabel || '';
  const summary = item.summary || item.record_summary || item.aiSummary || 'AI analizi hazırlanıyor.';
  const note = item.note || '';
  return {
    id: item.id || `${sourceType}-${item.source_id || item.sourceId || 'x'}`,
    decisionId: item.decision_id || item.decisionId || null,
    sourceType,
    sourceId: item.source_id || item.sourceId || null,
    category,
    title,
    summary,
    priority: item.priority || 'Normal',
    deltaLabel: _sanitizeDeltaLabel(item.delta || item.deltaLabel || ''),
    imageUrl: item.image_url || item.imageUrl || item.thumbUrl || '',
    createdAt: item.created_at || item.createdAt || '',
    decidedAt: item.decided_at || item.decidedAt || '',
    dateLabel: primaryDate.dateLabel,
    timeLabel: primaryDate.timeLabel,
    createdLabel: primaryDate.fullLabel,
    decidedLabel: item.decided_at || item.decidedAt ? decidedDate.fullLabel : '',
    sortTimestamp: item.decided_at || item.decidedAt || item.created_at || item.createdAt || '',
    status,
    statusLabel: item.status_label || engineerReviewStatusLabel(status),
    statusTone: item.status_tone || (status === 'approved' ? 'success' : status === 'rejected' ? 'critical' : status === 'correction_requested' ? 'warning' : 'neutral'),
    siteName,
    zoneLabel,
    createdBy: item.created_by || item.createdBy || 'Sistem',
    note,
    recordTypeLabel: item.record_type_label || item.recordTypeLabel || 'KAYIT',
    detailMeta: item.detail_meta || item.detailMeta || {},
    draft: note || item.draft || summary,
  };
}

function engineerCreateDecisionItems(data) {
  // Prefer review_queue/review_history (future unified API) if present
  if (Array.isArray(data.review_queue) && data.review_queue.length > 0) {
    const history = Array.isArray(data.review_history) ? data.review_history : [];
    return data.review_queue.concat(history)
      .map(engineerNormalizeReviewItem)
      .sort((a, b) => engineerDecisionSortValue(b) - engineerDecisionSortValue(a));
  }

  // Current API: /api/dashboard/engineer returns recent_evidence
  const evidence = Array.isArray(data.recent_evidence) ? data.recent_evidence : [];

  const evidenceRaw = evidence.map((item) => ({
    ...item,
    source_type: 'evidence',
    source_id:   item.id,
    title:       item.title || 'Saha Tespiti',
    created_at:  item.captured_at || item.created_at,
    image_url:   item.thumbnail_url || '',
    status: (() => {
      const v = (item.verification_status || '').toUpperCase();
      if (v === 'VERIFIED') return 'approved';
      if (v === 'REJECTED') return 'rejected';
      return 'pending';
    })(),
  }));

  return evidenceRaw
    .map(engineerNormalizeReviewItem)
    .sort((a, b) => engineerDecisionSortValue(b) - engineerDecisionSortValue(a));
}

function engineerGetVisibleDecisionItems() {
  const all = Array.isArray(_engineerDecisionItems) ? _engineerDecisionItems.slice() : [];
  const pending = all.filter((item) => item.status === 'pending' || item.status === 'in_review');
  const history = all.filter((item) => item.status === 'approved' || item.status === 'rejected' || item.status === 'correction_requested');
  if (_engineerDecisionFilter === 'history') return history.sort((a, b) => engineerDecisionSortValue(b) - engineerDecisionSortValue(a));
  if (_engineerDecisionFilter === 'all') {
    return all.sort((a, b) => {
      const aRank = (a.status === 'pending' || a.status === 'in_review') ? 0 : 1;
      const bRank = (b.status === 'pending' || b.status === 'in_review') ? 0 : 1;
      if (aRank !== bRank) return aRank - bRank;
      return engineerDecisionSortValue(b) - engineerDecisionSortValue(a);
    });
  }
  return pending.sort((a, b) => engineerDecisionSortValue(b) - engineerDecisionSortValue(a));
}

function engineerRenderDecisionFilters() {
  document.querySelectorAll('#kararTerminalFilters .karar-filter-btn').forEach((btn) => {
    btn.classList.toggle('is-active', btn.getAttribute('data-filter') === _engineerDecisionFilter);
  });
  const hint = document.getElementById('kararTerminalFilterHint');
  if (hint) {
    hint.textContent =
      _engineerDecisionFilter === 'history'
         ? 'Onaylanan, reddedilen ve düzeltme istenen kayıtlar arşiv mantığıyla listelenir.'
        : _engineerDecisionFilter === 'all'
           ? 'Bekleyen kayıtlar üstte tutulur; geçmiş kararlar altta izlenir.'
          : 'Öncelik: görsel, bağlam, AI özeti, sayısal etki.';
  }
}

function engineerSetDecisionFilter(filter) {
  _engineerDecisionFilter = filter || 'pending';
  engineerRenderDecisionFilters();
  const visible = engineerGetVisibleDecisionItems();
  if (!visible.find((item) => item.id === _engineerFocusedDecisionId)) {
    _engineerFocusedDecisionId = visible[0].id || null;
    _engineerDecisionExpanded = false;
  }
  kararTerminalRenderListe();
}

function engineerToggleSecretaryRail(forceState = null) {
  const rail = document.getElementById('engineerAssistantRail');
  const btn = document.getElementById('engineerRailToggle');
  if (!rail) return;
  _engineerSecretaryCollapsed = typeof forceState === 'boolean' ? !forceState : !_engineerSecretaryCollapsed;
  rail.classList.toggle('is-collapsed', _engineerSecretaryCollapsed);
  if (btn) btn.textContent = _engineerSecretaryCollapsed ? 'Teknik Sekreteri Aç' : 'Teknik Sekreter';
}

function engineerDecisionImpact(item) {
  if (!item) return 'İzleme';
  if (item.deltaLabel) return item.deltaLabel;
  if (item.priority) return item.priority;
  return 'İzleme';
}

function engineerDecisionPriority(item) {
  return item.priority || 'Normal';
}

function engineerDecisionRecordType(item) {
  return item.recordTypeLabel || 'KAYIT';
}

function engineerDecisionAnalysisText(item) {
  if (!item) return 'AI analizi hazırlanıyor.';
  const pieces = [];
  if (item.summary) pieces.push(item.summary.trim());
  if (item.siteName) pieces.push(`Şantiye: ${item.siteName}.`);
  if (item.zoneLabel) pieces.push(`Alan: ${item.zoneLabel}.`);
  if (item.deltaLabel) pieces.push(`Sayısal etki ${item.deltaLabel} olarak izleniyor.`);
  if (item.detailMeta.material) pieces.push(`İlgili malzeme: ${item.detailMeta.material}.`);
  if (item.detailMeta.report_item_count) pieces.push(`Rapor içinde ${item.detailMeta.report_item_count} kayıt derlenmiş durumda.`);
  return pieces.join(' ').replace(/\s+/g, ' ').trim();
}

function engineerDecisionKeyValueRows(item) {
  if (!item) return [];
  const rows = [
    { label: 'Şantiye', value: item.siteName || 'Şantiye etiketi yok' },
    { label: 'Kaynak', value: item.sourceType === 'report' ? 'Günlük rapor' : item.sourceType === 'alert' ? 'Malzeme / stok uyarısı' : 'Saha kanıtı' },
    { label: 'Oluşturan', value: item.createdBy || 'Sistem' },
  ];
  if (item.zoneLabel) rows.push({ label: 'Alan', value: item.zoneLabel });
  if (item.detailMeta.material) rows.push({ label: 'Malzeme', value: item.detailMeta.material });
  if (item.detailMeta.workflow_status) rows.push({ label: 'Akış', value: item.detailMeta.workflow_status });
  if (item.detailMeta.verification_status) rows.push({ label: 'Doğrulama', value: item.detailMeta.verification_status });
  return rows.slice(0, 6);
}

function engineerGenerateSecretaryDraft(item) {
  if (!item) return 'Bir kayıt seçildiğinde burada operasyon notu ve düzeltme talebi hazırlanır.';
  const sourceLabel = item.sourceType === 'report' ? 'günlük rapor kaydı' : item.sourceType === 'alert' ? 'uyarı kaydı' : 'saha kaydı';
  const location = item.zoneLabel || item.siteName || 'ilgili alan';
  return `${item.dateLabel} ${item.timeLabel || ''} için ${location} odağındaki ${sourceLabel} incelendi. Karar sonrası sonuç akışı ve not arşive yazılacaktır.`.trim();
}

function engineerUpdateBottleneckSummary() {
  const summaryEl = document.getElementById('engineerBottleneckSummary');
  const closeEl = document.getElementById('engineerCloseTasksValue');
  const pending = _engineerDecisionItems.filter((item) => item.status === 'pending' || item.status === 'in_review');
  const evidenceCount = pending.filter((item) => item.sourceType === 'evidence').length;
  const reportCount = pending.filter((item) => item.sourceType === 'report').length;
  const safetyCount = pending.filter((item) => item.category === 'ISG').length;
  const materialCount = pending.filter((item) => item.category === 'Stok').length;
  if (closeEl) closeEl.textContent = String(pending.length);
  engineerSetStat('engineerStatEvidence', 'engineerStatEvidenceValue', evidenceCount);
  engineerSetStat('engineerStatReport', 'engineerStatReportValue', reportCount);
  engineerSetStat('engineerStatMaterial', 'engineerStatMaterialValue', safetyCount + materialCount);
  if (summaryEl) {
    if (!pending.length) {
      summaryEl.textContent = 'Bekleyen saha kararı yok. Karar geçmişi filtresinden tamamlanan kayıtları gözden geçirebilirsiniz.';
      return;
    }
    summaryEl.textContent = `Bekleyen ${pending.length} kayıt var. ${safetyCount} İSG, ${materialCount} stok / malzeme ve ${reportCount} rapor kaydı işlem bekliyor. Öncelik sırası: görsel, bağlam, AI özeti, sayısal etki.`;
  }
}

function engineerRenderLoading() {
  const list = document.getElementById('kararTerminalList');
  const detail = document.getElementById('kararTerminalDetail');
  _engineerDecisionItems = [];
  _engineerFocusedDecisionId = null;
  _engineerSelectedDecisionIds = new Set();
  engineerUpdateBottleneckSummary();
  kararTerminalUpdateBadge(0);
  engineerRenderDecisionFilters();
  if (list) {
    list.innerHTML = Array.from({ length: 5 }).map(() => '<div class="karar-skeleton-row"></div>').join('');
  }
  if (detail) {
    detail.innerHTML = '<div class="karar-detail__empty"><span>Kayıt detayı hazırlanıyor.</span></div>';
  }
}

function kararTerminalCategoryTag(item) {
  if (item.category === 'ISG') return 'ISG';
  if (item.category === 'Stok') return 'STK';
  return 'RPR';
}

function engineerFindDecisionItem(id) {
  return _engineerDecisionItems.find((item) => item.id === id) || null;
}

function engineerCollectDecisionNote(item) {
  const detailNote = document.getElementById('kararDecisionNote');
  const assistantInput = document.getElementById('engineerAssistantInput');
  const note = (detailNote.value || assistantInput.value || item.note || '').trim();
  return note;
}

function engineerDetailToggleExpand() {
  _engineerDecisionExpanded = !_engineerDecisionExpanded;
  kararTerminalRenderDetay(engineerFindDecisionItem(_engineerFocusedDecisionId));
}

function engineerRenderSecretaryState(item, extraNote = '') {
  if (!item) {
    engineerAssistantSetResponse('Bir kayıt seçildiğinde burada rapor taslağı, sesli not ve düzeltme desteği görünür.', 'empty');
    return;
  }
  const meta = [
    item.recordTypeLabel || 'Kayıt',
    item.siteName || 'Şantiye etiketi yok',
    item.statusLabel || engineerReviewStatusLabel(item.status),
  ].join(' ?? ');
  const draft = item.draft || engineerGenerateSecretaryDraft(item);
  const noteLine = extraNote || item.note;
  engineerAssistantSetResponse(`
    <div class="engineer-secretary-draft">
      <div class="engineer-secretary-draft__meta">${engineerEscapeHtml(meta)}</div>
      <div class="engineer-secretary-draft__text">${engineerEscapeHtml(draft)}</div>
      ${noteLine ? `<div class="engineer-secretary-note">${engineerEscapeHtml(noteLine)}</div>` : ''}
    </div>
  `);
}

function engineerBuildAssistantPrompt(question, item) {
  const context = item ? [
    `Kayıt başlığı: ${item.title}`,
    `Kayıt türü: ${item.recordTypeLabel}`,
    `Şantiye: ${item.siteName}`,
    `Alan: ${item.zoneLabel || 'Belirtilmedi'}`,
    `AI özeti: ${item.summary}`,
    `Karar notu: ${item.note || 'Henüz not yok'}`,
  ].join('\n') : 'Seçili kayıt yok.';
  return `Rolün teknik sekreter. Türk yönetmelikleri, saha bağlamı ve operasyon akışını bilen kısa, net, uygulanabilir metin üret.\n${context}\nKullanıcı isteği: ${question}`;
}

function engineerApplySecretaryNote(note) {
  const item = engineerFindDecisionItem(_engineerFocusedDecisionId);
  if (!item) {
    engineerAssistantSetResponse('Önce bir kayıt seçin.', 'empty');
    return;
  }
  item.note = note.trim();
  item.draft = `${engineerGenerateSecretaryDraft(item)} Not: ${item.note}`.trim();
  const detailNote = document.getElementById('kararDecisionNote');
  if (detailNote) detailNote.value = item.note;
  engineerRenderSecretaryState(item, 'Karar notu taslağa işlendi.');
}

function kararTerminalRenderListe() {
  const list = document.getElementById('kararTerminalList');
  if (!list) return;
  const visible = engineerGetVisibleDecisionItems();
  const pendingCount = _engineerDecisionItems.filter((item) => item.status === 'pending' || item.status === 'in_review').length;
  kararTerminalUpdateBadge(pendingCount);
  engineerRenderDecisionFilters();

  if (!visible.length) {
    const emptyMessage =
      _engineerDecisionFilter === 'history'
         ? 'Karar geçmişi henüz oluşmadı.'
        : _engineerDecisionFilter === 'all'
           ? 'Gösterilecek kayıt bulunmuyor.'
          : 'Bekleyen karar yok.';
    list.innerHTML = `<div class="karar-terminal__list-empty">${engineerEscapeHtml(emptyMessage)}</div>`;
    _engineerFocusedDecisionId = null;
    kararTerminalRenderDetay(null);
    engineerRenderSecretaryState(null);
    return;
  }

  if (!visible.find((item) => item.id === _engineerFocusedDecisionId)) {
    _engineerFocusedDecisionId = visible[0].id;
    _engineerDecisionExpanded = false;
  }

  list.innerHTML = visible.map((item) => {
    const tag = kararTerminalCategoryTag(item);
    const isActive = item.id === _engineerFocusedDecisionId;
    const rightLabel = item.deltaLabel || item.statusLabel;
    const rightTone = item.deltaLabel
       ? (String(item.deltaLabel).trim().startsWith('-') ? 'down' : 'up')
      : (item.status === 'approved' ? 'up' : item.status === 'rejected' ? 'down' : '');
    return `
      <div class="karar-list-item${isActive ? ' is-active' : ''}" data-id="${engineerEscapeHtml(item.id)}">
        <div class="karar-list-item__tag" data-type="${engineerEscapeHtml(tag)}">${engineerEscapeHtml(tag)}</div>
        <div class="karar-list-item__body">
          <div class="karar-list-item__title">${engineerEscapeHtml(kararTerminalCapTitle(item.title))}</div>
          <div class="karar-list-item__meta">${engineerEscapeHtml(item.dateLabel || '')}${item.timeLabel ? ` ${engineerEscapeHtml(item.timeLabel)}` : ''} ? ${engineerEscapeHtml(item.siteName || 'Şantiye etiketi yok')}</div>
        </div>
        <div class="karar-list-item__right">
          <span class="karar-list-item__change ${rightTone}">${engineerEscapeHtml(rightLabel || 'İncele')}</span>
          <span class="karar-list-item__type-badge">${engineerEscapeHtml(item.category)}</span>
        </div>
      </div>`;
  }).join('');

  list.onclick = (event) => {
    const row = event.target.closest('.karar-list-item');
    if (!row) return;
    kararTerminalSecItem(row.getAttribute('data-id'));
  };

  const selected = engineerFindDecisionItem(_engineerFocusedDecisionId) || visible[0];
  kararTerminalRenderDetay(selected);
  engineerRenderSecretaryState(selected);
}

function kararTerminalSecItem(id) {
  _engineerFocusedDecisionId = id;
  _engineerDecisionExpanded = false;
  document.querySelectorAll('.karar-list-item').forEach((el) => {
    el.classList.toggle('is-active', el.getAttribute('data-id') === id);
  });
  const item = engineerFindDecisionItem(id);
  kararTerminalRenderDetay(item);
  engineerRenderSecretaryState(item);
}

function kararTerminalRenderDetay(item) {
  const detail = document.getElementById('kararTerminalDetail');
  if (!detail) return;
  if (!item) {
    detail.innerHTML = '<div class="karar-detail__empty"><span>Listeden bir kayıt seçin.</span></div>';
    return;
  }

  // Stok kritik uyarıları için özel UI
  if (item.sourceType === 'alert' && item.detailMeta && item.detailMeta.degisim === 'stok_kritik') {
    const isActionable = item.status === 'pending' || item.status === 'in_review';
    const saving = Boolean(item._saving);
    const mevcut = item.detailMeta.yeni || '?';
    const minMiktar = item.detailMeta.onceki || '?';
    detail.innerHTML = `
      <div class="karar-detail__top">
        <div>
          <div class="karar-detail__record-type">Stok Uyarısı</div>
          <div class="karar-detail__record-subline">${engineerEscapeHtml(item.siteName || 'Şantiye etiketi yok')} · Sistem</div>
        </div>
        <div class="karar-detail__record-time">${engineerEscapeHtml(item.createdLabel || item.dateLabel || '')}</div>
      </div>
      <div class="karar-detail__heading-row">
        <h3 class="karar-detail__title">${engineerEscapeHtml(item.title)}</h3>
        <span class="karar-detail__status-badge" data-tone="${engineerEscapeHtml(item.statusTone || 'neutral')}">${engineerEscapeHtml(item.statusLabel || engineerReviewStatusLabel(item.status))}</span>
      </div>
      <div class="karar-detail__supporting" style="font-size:14px;color:#374151;margin:8px 0;line-height:1.6;">
        ${engineerEscapeHtml(item.siteName || '?')} — Mevcut: <strong>${engineerEscapeHtml(String(mevcut))}kg</strong>, Minimum: <strong>${engineerEscapeHtml(String(minMiktar))}kg</strong>
      </div>
      <div class="karar-detail__actions" style="gap:8px;">
        <button type="button" class="karar-btn-approve" ${!isActionable || saving ? 'disabled' : ''} data-action="approve" style="flex:1;">
          ${saving ? 'Kaydediliyor...' : '✅ Sipariş Verildi'}
        </button>
        <button type="button" class="karar-btn-reject" ${!isActionable || saving ? 'disabled' : ''} data-action="reject" style="flex:1;">
          ❌ Ertele
        </button>
      </div>`;
    const actionsBar = detail.querySelector('.karar-detail__actions');
    if (actionsBar) {
      actionsBar.onclick = (e) => {
        const btn = e.target.closest('button[data-action]');
        if (!btn || btn.disabled) return;
        _stokKritikKarar(item, btn.getAttribute('data-action'));
      };
    }
    return;
  }

  const tag = kararTerminalCategoryTag(item);
  const aiAnalysis = engineerDecisionAnalysisText(item);
  const fullAnalysis = engineerEscapeHtml(aiAnalysis);
  const previewAnalysis = engineerEscapeHtml(aiAnalysis.length > 260 && !_engineerDecisionExpanded ? `${aiAnalysis.slice(0, 260).trim()}...` : aiAnalysis);
  const metaRows = engineerDecisionKeyValueRows(item);
  const isActionable = item.status === 'pending' || item.status === 'in_review';
  const saving = Boolean(item._saving);
  const noteValue = engineerEscapeHtml(item.note || '');
  const imageHtml = item.imageUrl
     ? `<img src="${engineerEscapeHtml(item.imageUrl)}" alt="Saha görseli" loading="lazy" onerror="this.parentElement.innerHTML='<div class=&quot;karar-detail__image-placeholder&quot;><span>Görsel yüklenemedi</span></div>'">`
    : `<div class="karar-detail__image-placeholder">
         <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
           <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"></path>
           <circle cx="12" cy="13" r="3"></circle>
         </svg>
         <span>Görsel yok</span>
       </div>`;

  detail.innerHTML = `
    <div class="karar-detail__top">
      <div>
        <div class="karar-detail__record-type">${engineerEscapeHtml(engineerDecisionRecordType(item))}</div>
        <div class="karar-detail__record-subline">${engineerEscapeHtml(item.siteName || 'Şantiye etiketi yok')} ? ${engineerEscapeHtml(item.createdBy || 'Sistem')}</div>
      </div>
      <div class="karar-detail__record-time">${engineerEscapeHtml(item.createdLabel || `${item.dateLabel} ${item.timeLabel}`.trim())}</div>
    </div>
    <div class="karar-detail__image">${imageHtml}</div>
    <div class="karar-detail__heading-row">
      <h3 class="karar-detail__title">${engineerEscapeHtml(kararTerminalCapTitle(item.title))}</h3>
      <span class="karar-detail__status-badge" data-tone="${engineerEscapeHtml(item.statusTone || 'neutral')}">${engineerEscapeHtml(item.statusLabel || engineerReviewStatusLabel(item.status))}</span>
    </div>
    <div class="karar-detail__supporting">${engineerEscapeHtml(item.zoneLabel || tag)}${item.decidedLabel ? ` ? Karar zamanı: ${engineerEscapeHtml(item.decidedLabel)}` : ''}</div>
    <div>
      <div class="karar-detail__analysis-head">
        <div class="karar-detail__analysis-label">AI Analizi</div>
        <button type="button" class="karar-detail__expand-btn" onclick="engineerDetailToggleExpand()">${_engineerDecisionExpanded ? 'Daralt' : 'Detayı Büyüt'}</button>
      </div>
      <div class="karar-detail__analysis-text" data-expanded="${_engineerDecisionExpanded ? 'true' : 'false'}" title="${fullAnalysis}">${previewAnalysis}</div>
    </div>
    <div class="karar-detail__meta-grid">
      <div class="karar-detail__meta-cell">
        <span class="karar-detail__meta-cell__label">Kategori</span>
        <span class="karar-detail__meta-cell__value">${engineerEscapeHtml(item.category || tag)}</span>
      </div>
      <div class="karar-detail__meta-cell">
        <span class="karar-detail__meta-cell__label">Etki</span>
        <span class="karar-detail__meta-cell__value">${engineerEscapeHtml(engineerDecisionImpact(item))}</span>
      </div>
      <div class="karar-detail__meta-cell">
        <span class="karar-detail__meta-cell__label">Öncelik</span>
        <span class="karar-detail__meta-cell__value">${engineerEscapeHtml(engineerDecisionPriority(item))}</span>
      </div>
    </div>
    <div class="karar-detail__fact-grid">
      ${metaRows.map((row) => `
        <div class="karar-detail__fact">
          <span class="karar-detail__fact-label">${engineerEscapeHtml(row.label)}</span>
          <strong class="karar-detail__fact-value">${engineerEscapeHtml(row.value || '?')}</strong>
        </div>
      `).join('')}
    </div>
    <div class="karar-detail__note-box">
      <div class="karar-detail__analysis-head">
        <div class="karar-detail__analysis-label">Karar Notu</div>
        <div class="karar-detail__note-help">Düzeltme isteğinde arşive aynen yazılır.</div>
      </div>
      <textarea id="kararDecisionNote" class="karar-detail__note-input" placeholder="Gerekirse kısa bir açıklama veya düzeltme talebi yazın..." ${isActionable ? '' : 'disabled'}>${noteValue}</textarea>
    </div>
    <div class="karar-detail__actions">
      <button type="button" class="karar-btn-approve" ${!isActionable || saving ? 'disabled' : ''} data-action="approve">${saving ? 'Kaydediliyor...' : 'Onayla'}</button>
      <button type="button" class="karar-btn-reject"  ${!isActionable || saving ? 'disabled' : ''} data-action="reject">Reddet</button>
      <button type="button" class="karar-btn-edit" ? ${!isActionable || saving ? 'disabled' : ''} data-action="correct">Düzelt</button>
    </div>
    <div class="karar-detail__section karar-detail__section--thread" style="display:none;">
      <div class="karar-detail__section-label">Geri Bildirimler</div>
      <div id="engineerThread" class="contractor-feed-drawer__thread"></div>
      <div class="contractor-feed-drawer__thread-input" style="margin-top:12px;">
        <input type="text" id="engineerThreadInput" placeholder="Mesaj yaz..." class="contractor-feed-drawer__thread-input-field">
        <button id="engineerThreadSend" class="contractor-feed-drawer__thread-send">Gönder</button>
      </div>
    </div>`;

  // Wire action buttons via event delegation ?? avoids JSON.stringify quote-escaping bugs in inline onclick
  const actionsBar = detail.querySelector('.karar-detail__actions');
  if (actionsBar) {
    actionsBar.onclick = (e) => {
      const btn = e.target.closest('button[data-action]');
      if (!btn || btn.disabled) return;
      console.debug('[KararTerminal] action click:', btn.getAttribute('data-action'), 'item:', item.id, 'sourceType:', item.sourceType, 'status:', item.status);
      engineerProcessDecision(item.id, btn.getAttribute('data-action'));
    };
  }

  // Thread fetch + handler
  const decisionId = item.decisionId;
  if (!decisionId) return;

  engineerRenderThread(decisionId);
  engineerBindThreadInput(decisionId);
}

function engineerRenderThread(decisionId) {
  const threadEl = document.getElementById('engineerThread');
  const inputEl = document.getElementById('engineerThreadInput');
  const sendEl = document.getElementById('engineerThreadSend');

  if (!threadEl || !decisionId) return;

  if (inputEl) { inputEl.disabled = false; inputEl.value = ''; }
  if (sendEl) sendEl.disabled = false;

  threadEl.innerHTML = '<div style="color:#94A3B8;font-size:13px;padding:12px 0;">Yükleniyor...</div>';

  const token = localStorage.getItem('bai_token');
  fetch('/karar/' + decisionId + '/mesajlartoken=' + token)
    .then(r => r.json())
    .then(data => {
      const mesajlar = data.mesajlar || [];
      if (mesajlar.length === 0) {
        threadEl.innerHTML = '<div style="color:#94A3B8;font-size:13px;padding:12px 0;">Henüz geri bildirim yok. İlk mesajı sen yaz.</div>';
        return;
      }
      threadEl.innerHTML = mesajlar.map(m => {
        const normalizedRole = m.kullanici_rolu === 'mutahhit' ? 'muteahhit' : m.kullanici_rolu;
        const rolLabel = contractorRoleLabel(normalizedRole);
        const rolClass = 'contractor-feed-drawer__thread-role--' + (normalizedRole || 'default');
        const tarih = contractorFormatMessageTime(m.created_at);
        const escapedName = engineerEscapeHtml(m.kullanici_adi || '');
        const escapedMsg = engineerEscapeHtml(m.mesaj || '');
        return `<div class="contractor-feed-drawer__thread-item">
          <div class="contractor-feed-drawer__thread-meta">
            <span class="contractor-feed-drawer__thread-role ${rolClass}">${rolLabel}</span>
            <span style="font-weight:500;">${escapedName}</span>
            <span style="color:#94A3B8;">?</span>
            <span style="color:#94A3B8;font-size:12px;">${tarih}</span>
          </div>
          <div class="contractor-feed-drawer__thread-body">${escapedMsg}</div>
        </div>`;
      }).join('');
    })
    .catch(() => {
      threadEl.innerHTML = '<div style="color:#EF4444;font-size:13px;padding:12px 0;">Mesajlar yüklenemedi.</div>';
    });
}

function engineerBindThreadInput(decisionId) {
  const inputEl = document.getElementById('engineerThreadInput');
  const sendEl = document.getElementById('engineerThreadSend');
  if (!inputEl || !sendEl) return;

  const newSendEl = sendEl.cloneNode(true);
  sendEl.parentNode.replaceChild(newSendEl, sendEl);
  const newInputEl = inputEl.cloneNode(true);
  inputEl.parentNode.replaceChild(newInputEl, inputEl);

  newSendEl.addEventListener('click', function() { engineerSendMessage(decisionId); });
  newInputEl.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); engineerSendMessage(decisionId); }
  });
}

function engineerSendMessage(decisionId) {
  const inputEl = document.getElementById('engineerThreadInput');
  const sendEl = document.getElementById('engineerThreadSend');
  if (!inputEl || !decisionId) return;

  const mesaj = (inputEl.value || '').trim();
  if (!mesaj) return;

  inputEl.disabled = true;
  if (sendEl) sendEl.disabled = true;

  const token = localStorage.getItem('bai_token');
  fetch('/karar/' + decisionId + '/mesajtoken=' + token, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({mesaj})
  })
  .then(r => { if (!r.ok) throw new Error('Mesaj gönderilemedi'); return r.json(); })
  .then(() => { engineerRenderThread(decisionId); inputEl.value = ''; })
  .catch(err => { alert('Mesaj gönderilemedi: ' + (err.message || 'Hata')); })
  .finally(() => { inputEl.disabled = false; if (sendEl) sendEl.disabled = false; inputEl.focus(); });
}

async function engineerPersistDecision(item, status, note = '') {
  const token = localStorage.getItem('bai_token') || '';
  if (!item.sourceType || !item.sourceId) {
    console.warn('[KararTerminal] engineerPersistDecision: sourceType/sourceId eksik', item);
    return { ok: false, message: 'Kayıt kimliği eksik.' };
  }
  console.debug('[KararTerminal] persist:', item.sourceType, item.sourceId, '?', status, note ? `note="${note}"` : '');
  try {
    let url, body;
    if (item.sourceType === 'alert') {
      // MalzemeUyari: approved / rejected / correction_requested all persisted as real states
      url = `/malzeme-uyari/${item.sourceId}/karar`;
      body = JSON.stringify({ token, status, ...(note ? { note } : {}) });
    } else {
      // evidence / report ?? unified endpoint updates both ReviewDecision and the source row
      const srcType = item.sourceType === 'report' ? 'report' : 'evidence';
      url = `/api/review-items/${srcType}/${item.sourceId}/decision`;
      body = JSON.stringify({ token, status, note: note || '' });
    }
    const res = await fetch(url, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || data.message || 'Karar kaydedilemedi.');
    return { ok: true, item: null };
  } catch (err) {
    console.error('[KararTerminal] engineerPersistDecision error:', err);
    return { ok: false, message: err.message || 'Karar kaydedilemedi.' };
  }
}

async function engineerProcessDecision(id, mode, silent = false) {
  const item = engineerFindDecisionItem(id);
  if (!item || item._saving) return;
  const nextStatus = engineerDecisionModeToStatus(mode);
  const note = engineerCollectDecisionNote(item);
  if (nextStatus === 'correction_requested' && !note) {
    const textarea = document.getElementById('kararDecisionNote');
    if (textarea) textarea.focus();
    if (!silent && typeof showToast === 'function') showToast('Düzeltme için kısa bir not ekleyin.', 'warning');
    return;
  }

  item._saving = true;
  kararTerminalRenderDetay(item);
  const result = await engineerPersistDecision(item, nextStatus, note);
  item._saving = false;

  if (!result.ok) {
    kararTerminalRenderDetay(item);
    if (!silent && typeof showToast === 'function') showToast(result.message || 'Karar kaydedilemedi.', 'warning');
    return;
  }

  if (result.item) {
    Object.assign(item, result.item);
  } else {
    item.status = nextStatus;
    item.statusLabel = engineerReviewStatusLabel(nextStatus);
    item.statusTone = nextStatus === 'approved' ? 'success' : nextStatus === 'rejected' ? 'critical' : 'warning';
    item.note = note;
    item.decidedAt = new Date().toISOString();
    item.decidedLabel = engineerNormalizeDateParts(item.decidedAt).fullLabel;
  }

  if (note) {
    item.note = note;
    item.draft = `${engineerGenerateSecretaryDraft(item)} Not: ${note}`.trim();
  }

  engineerUpdateBottleneckSummary();
  const visible = engineerGetVisibleDecisionItems();
  _engineerFocusedDecisionId = visible.find((entry) => entry.id === id).id || visible[0].id || null;
  _engineerDecisionExpanded = false;
  kararTerminalRenderListe();
  engineerRenderSecretaryState(engineerFindDecisionItem(_engineerFocusedDecisionId), nextStatus === 'approved'
     ? 'Kayıt onaylandı ve sonuç akışına alındı.'
    : nextStatus === 'rejected'
       ? 'Kayıt reddedildi ve arşive işlendi.'
      : 'Düzeltme isteği notuyla birlikte kaydedildi.');

  if (!silent && typeof showToast === 'function') {
    showToast(
      nextStatus === 'approved'
         ? 'Kayıt onaylandı.'
        : nextStatus === 'rejected'
           ? 'Kayıt reddedildi.'
          : 'Düzeltme talebi oluşturuldu.',
      'success'
    );
  }
}

function kararTerminalDuzelt(id) {
  const item = engineerFindDecisionItem(id);
  if (!item) return;
  const input = document.getElementById('kararDecisionNote') || document.getElementById('engineerAssistantInput');
  if (input && !input.value.trim()) input.value = `${item.title} için düzeltme notu: `;
  if (input) input.focus();
  engineerRenderSecretaryState(item, 'Düzeltme notunu yazıp Düzelt butonuna tekrar basın.');
}

async function loadEngineerDashboard(force = false) {
  const root = document.getElementById('engineerDashboard');
  if (!root) return;
  if (_engineerDashboardLoading) return;
  if (_engineerDashboardLoaded && !force) {
    setDashboardVisibility(localStorage.getItem('bai_rol'));
    return;
  }

  // Onboarding: org kontrolü (localStorage'dan anlık)
  const _baiUser = JSON.parse(localStorage.getItem('bai_user') || '{}');
  if (!_baiUser.organization_id) {
    setDashboardVisibility(localStorage.getItem('bai_rol'));
    const list = document.getElementById('kararTerminalList');
    const detail = document.getElementById('kararTerminalDetail');
    const _onbMsg = `<div style="text-align:center;padding:48px 24px;"><div style="font-size:20px;font-weight:800;color:#0F172A;margin-bottom:10px;">Henüz bir ekibe dahil değilsiniz</div><div style="font-size:14px;color:#64748B;line-height:1.6;">Müteahhitinizden davet linki veya e-posta daveti isteyerek BuildingAI ekibine katılabilirsiniz.</div></div>`;
    if (list) list.innerHTML = _onbMsg;
    if (detail) detail.innerHTML = '<div class="karar-detail__empty"><span>Ekibe katıldıktan sonra karar akışınız burada görünecek.</span></div>';
    _engineerDashboardLoaded = false;
    return;
  }

  setDashboardVisibility(localStorage.getItem('bai_rol'));
  engineerRenderLoading();
  engineerAssistantSetResponse('Bir kayıt seçildiğinde burada rapor taslağı ve karar notu oluşur.', 'empty');
  _engineerDashboardLoading = true;
  const token = localStorage.getItem('bai_token') || '';

  try {
    const res = await fetch('/api/dashboard/engineer', {
      method: 'GET',
      headers: token ? { Authorization: 'Bearer ' + token } : {},
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Dashboard verisi alınamadı.');

    // Onboarding: şantiye ataması kontrolü
    if ((data.santiye_sayisi  -1) === 0) {
      const list = document.getElementById('kararTerminalList');
      const detail = document.getElementById('kararTerminalDetail');
      const _siteMsg = `<div style="text-align:center;padding:48px 24px;"><div style="font-size:20px;font-weight:800;color:#0F172A;margin-bottom:10px;">Henüz bir şantiyeye atanmadınız</div><div style="font-size:14px;color:#64748B;line-height:1.6;">Müteahhitiniz sizi bir şantiyeye atadığında buradaki karar akışı aktif hale gelecek.</div></div>`;
      if (list) list.innerHTML = _siteMsg;
      if (detail) detail.innerHTML = '<div class="karar-detail__empty"><span>Şantiye ataması yapıldığında kayıtlarınız burada görünecek.</span></div>';
      _engineerDashboardLoaded = true;
      return;
    }

    _engineerDashboardSnapshot = data;
    _engineerDecisionItems = engineerCreateDecisionItems(data);
    _engineerFocusedDecisionId = null;
    _engineerDecisionFilter = _engineerDecisionItems.some((item) => item.status === 'pending' || item.status === 'in_review') ? 'pending' : 'history';
    engineerToggleSecretaryRail(window.innerWidth >= 1024);
    engineerUpdateBottleneckSummary();
    engineerRenderDecisionFilters();
    kararTerminalRenderListe();
    _engineerDashboardLoaded = true;
  } catch (err) {
    _engineerDashboardSnapshot = null;
    _engineerDecisionItems = [];
    _engineerFocusedDecisionId = null;
    engineerUpdateBottleneckSummary();
    kararTerminalUpdateBadge(0);
    const list = document.getElementById('kararTerminalList');
    const detail = document.getElementById('kararTerminalDetail');
    if (list) list.innerHTML = '<div class="karar-terminal__list-empty">Karar terminali yüklenemedi.</div>';
    if (detail) detail.innerHTML = '<div class="karar-detail__empty"><span>Veriler yüklenemedi, sayfayı yenileyin.</span></div>';
    engineerRenderSecretaryState(null);
    _engineerDashboardLoaded = false;
  } finally {
    _engineerDashboardLoading = false;
  }
}

function contractorToggleCommandRail(forceState = null) {
  const rail = document.getElementById('contractorAssistantRail');
  const btn = document.getElementById('contractorRailToggle');
  if (!rail) return;
  _contractorCommandCollapsed = typeof forceState === 'boolean' ? !forceState : !_contractorCommandCollapsed;
  // Desktop: is-collapsed class ile display:none (mevcut davranış korundu)
  rail.classList.toggle('is-collapsed', _contractorCommandCollapsed);
  if (btn) btn.textContent = _contractorCommandCollapsed ? 'AI Panelini Aç' : 'AI Paneli';
  const mobileBtn = document.getElementById('contractorRailToggleMobile');
  if (mobileBtn) mobileBtn.style.display = _contractorCommandCollapsed ? '' : 'none';
  // Mobile: data-open ile transform animasyonu
  const railOpen = !_contractorCommandCollapsed;
  const isMobile = window.innerWidth < 1024;
  rail.setAttribute('data-open', railOpen ? 'true' : 'false');
  const overlay = document.getElementById('contractorRailOverlay');
  if (overlay) {
    overlay.setAttribute('data-visible', (railOpen && isMobile) ? 'true' : 'false');
  }
  const fab = document.getElementById('contractorFab');
  if (fab) {
    fab.setAttribute('data-hidden', railOpen ? 'true' : 'false');
  }
  if (isMobile) {
    document.body.setAttribute('data-rail-open', railOpen ? 'true' : 'false');
  } else {
    document.body.removeAttribute('data-rail-open');
  }
}

function contractorUpdateHeaderHeight() {
  const header = document.getElementById('contentHeader');
  const bar = document.getElementById('aiCommandBar');
  if (header && bar) {
    const h = header.offsetHeight + bar.offsetHeight;
    document.documentElement.style.setProperty('--contractor-header-height', `${h}px`);
  }
}
window.addEventListener('load', contractorUpdateHeaderHeight);
window.addEventListener('resize', contractorUpdateHeaderHeight);

function contractorMetricLookup(metricId) {
  const metrics = Array.isArray(_contractorDashboardSnapshot.kpis) ? _contractorDashboardSnapshot.kpis : [];
  return metrics.find((metric) => metric.id === metricId) || {};
}

function contractorBuildExecutiveMeta(feed = null) {
  const scopedFeed = Array.isArray(feed) ? feed : (Array.isArray(_contractorDashboardSnapshot.today_approved_feed) ? _contractorDashboardSnapshot.today_approved_feed : []);
  const localCtx = _contractorDashboardSnapshot.local_filter_context || {};
  const activeSites = Number(contractorMetricLookup('active_sites').value || 0);
  const approvedToday = Number(contractorMetricLookup('approved_today').value || localCtx.today_approved_total || scopedFeed.length || 0);
  const criticalRisk = Number(contractorMetricLookup('open_critical_risk').value || 0);
  const stockDelta = contractorMetricLookup('critical_stock_delta');
  const labels = [
    { label: `${approvedToday} bugün onaylandı`, tone: approvedToday > 0 ? 'success' : 'neutral' },
    { label: criticalRisk > 0 ? `${criticalRisk} açık kritik risk` : 'Açık kritik risk yok', tone: criticalRisk > 0 ? 'warning' : 'neutral' },
    { label: Number(stockDelta.value || 0) > 0 ? `Kritik stok sapması %${stockDelta.value}` : 'Stok hattı sakin', tone: Number(stockDelta.value || 0) > 0 ? 'info' : 'neutral' },
    { label: `${activeSites} aktif şantiye`, tone: 'neutral' },
  ];
  if (Array.isArray(feed)) labels.unshift({ label: `${feed.length} kayıt görünümü`, tone: 'neutral' });
  return labels.slice(0, 4);
}

function contractorBuildAssistantContext() {
  if (!_contractorDashboardSnapshot) return 'Onaylı sonuç görünümü henüz yüklenmedi.';
  const metrics = Array.isArray(_contractorDashboardSnapshot.kpis) ? _contractorDashboardSnapshot.kpis : [];
  const feed = Array.isArray(_contractorDashboardSnapshot.today_approved_feed) ? _contractorDashboardSnapshot.today_approved_feed : [];
  const brief = Array.isArray(_contractorDashboardSnapshot.site_brief_lines) ? _contractorDashboardSnapshot.site_brief_lines : [];
  return [
    metrics.map((metric) => `${metric.label || 'KPI'}: ${metric.value ?? 0}${metric.suffix || ''}`).join('\n'),
    brief.join('\n'),
    feed.slice(0, 6).map((item) => `${item.time || ''} | ${item.record_type || ''} | ${item.title || ''} | ${item.site_name || ''} | ${item.impact || item.status || ''}`).join('\n'),
  ].filter(Boolean).join('\n');
}

function contractorRenderExecutiveSummary(summaryPayload = {}, options = {}) {
  const el = document.getElementById('contractorInsightList');
  if (!el) return;
  const hero = summaryPayload.hero || {};
  const lines = Array.isArray(options.lines) && options.lines.length
     ? options.lines
    : Array.isArray(_contractorDashboardSnapshot.site_brief_lines)
       ? _contractorDashboardSnapshot.site_brief_lines
      : [];
  const tone = contractorNormalizeTone(options.tone || hero.tone || 'neutral');
  const title = options.title || hero.title || 'Günün Saha Resmi';
  const footerItems = Array.isArray(options.footerItems) ? options.footerItems : contractorBuildExecutiveMeta();
  el.innerHTML = `
    <article class="contractor-summary-hero-card" data-tone="${engineerEscapeHtml(tone)}">
      <div class="contractor-summary-hero-card__top">
        <div class="contractor-summary-hero-card__eyebrow">${engineerEscapeHtml(options.eyebrow || hero.status_label || 'Onaylı sonuç görünümü')}</div>
        <div class="contractor-summary-hero-card__role">${engineerEscapeHtml(options.roleLabel || hero.role_label || (_contractorDashboardSnapshot.access_role_label || 'Yönetici'))}</div>
      </div>
      <div class="contractor-summary-hero-card__title">${engineerEscapeHtml(title)}</div>
      <div class="contractor-summary-lines">
        ${lines.length
           ? lines.slice(0, 5).map((line) => `<div class="contractor-summary-line">${engineerEscapeHtml(line)}</div>`).join('')
          : '<div class="contractor-empty-state">Henüz onaylı saha özeti oluşmadı.</div>'}
      </div>
      <div class="contractor-summary-hero-card__footer">
        ${footerItems.map((item) => `<span class="contractor-summary-hero-card__pill" data-tone="${engineerEscapeHtml(contractorNormalizeTone(item.tone))}">${engineerEscapeHtml(item.label || '')}</span>`).join('')}
      </div>
    </article>`;
}

function contractorRenderChips(items) {
  const el = document.getElementById('contractorInsightChips');
  if (!el) return;
  if (!Array.isArray(items) || !items.length) {
    el.innerHTML = '';
    return;
  }
  el.innerHTML = items.map((item) => {
    const tone = contractorNormalizeTone(item.tone);
    if (item.prompt) {
      return `<button type="button" class="engineer-chip contractor-chip" data-tone="${engineerEscapeHtml(tone)}" onclick='contractorAssistantUseSuggestion(${JSON.stringify(item.prompt)})'>${engineerEscapeHtml(item.label || '')}</button>`;
    }
    return `<span class="engineer-chip contractor-chip is-static" data-tone="${engineerEscapeHtml(tone)}">${engineerEscapeHtml(item.label || '')}</span>`;
  }).join('');
}

function contractorFeedTimeLabel(value) {
  if (!value) return 'Saat yok';
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
}

function contractorCategoryIconSvg(cat) {
  const c = (cat || '').toLowerCase();
  if (c === 'isg') {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L3 7v5c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7L12 2z"/></svg>';
  }
  if (c === 'stok') {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>';
  }
  if (c === 'rapor') {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>';
  }
  return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="9 12 11 14 15 10"/></svg>';
}

function contractorApprovedStatusTone(status) {
  const s = (status || '').toLowerCase();
  if (s.includes('düzelt') || s.includes('correction') || s.includes('istek')) return 'correction';
  if (s.includes('redded') || s.includes('reject')) return 'rejected';
  if (s.includes('onay') || s.includes('approv')) return 'approved';
  return '';
}

function contractorRenderTrend(payload) {
  const el = document.getElementById('contractorTrendBody');
  if (!el) return;
  const items = Array.isArray(payload)
     ? payload
    : Array.isArray(payload.items)
       ? payload.items
      : Array.isArray(_contractorDashboardSnapshot.today_approved_feed)
         ? _contractorDashboardSnapshot.today_approved_feed
        : [];
  // Cache for the drawer ?? only approved/completed items shown to contractor
  _contractorFeedItems = items.slice(0, 10);
  if (!items.length) {
    el.innerHTML = `
      <div style="padding:28px 20px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:10px;">
        <svg style="width:36px;height:36px;color:#CBD5E1;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <div style="font-size:14px;font-weight:700;color:#334155;">Bugün onaylanan kayıt yok</div>
        <div style="font-size:12px;color:#94A3B8;line-height:1.6;max-width:240px;">Mühendis kararları geldikçe kayıtlar burada görüntülenir.</div>
      </div>`;
    return;
  }
  el.innerHTML = `<div class="contractor-approved-feed">${
    _contractorFeedItems.map((item, idx) => {
      const cat = item.category || '';
      const thumb = item.thumbnail || '';
      const statusTone = contractorApprovedStatusTone(item.status);
      const timeText = contractorFeedTimeLabel(item.time || '');
      const metaParts = [item.site_name, item.record_type, timeText].filter(Boolean);
      const rawSummary = item.summary || item.note || '';
      const summaryText = rawSummary.length > 100 ? rawSummary.slice(0, 97) + '?' : rawSummary;
      const thumbHtml = `
        <div class="contractor-approved-card__thumb">
          <div class="contractor-approved-card__thumb-ph" data-cat="${engineerEscapeHtml(cat)}">
            ${contractorCategoryIconSvg(cat)}
            <span>${engineerEscapeHtml(cat || 'Kayıt')}</span>
          </div>
          ${thumb ? `<img src="${engineerEscapeHtml(thumb)}" alt="Kayıt görseli" loading="lazy">` : ''}
        </div>`;
      return `
        <article class="contractor-approved-card" data-category="${engineerEscapeHtml(cat)}" data-feed-idx="${idx}" role="button" tabindex="0" aria-label="${engineerEscapeHtml(item.title || 'Onaylı kayıt')} ? detay için tıklayın">
          ${thumbHtml}
          <div class="contractor-approved-card__content">
            <div class="contractor-approved-card__badges">
              <span class="contractor-approved-card__type-badge" data-cat="${engineerEscapeHtml(cat)}">${engineerEscapeHtml(item.record_type || cat || 'Kayıt')}</span>
              <span class="contractor-approved-card__status-badge" data-status="${engineerEscapeHtml(statusTone)}">${engineerEscapeHtml(item.status || 'Onaylandı')}</span>
            </div>
            <div class="contractor-approved-card__title">${engineerEscapeHtml(item.title || 'Onaylı kayıt')}</div>
            <div class="contractor-approved-card__meta">${engineerEscapeHtml(metaParts.join(' ?? '))}</div>
            ${summaryText ? `<div class="contractor-approved-card__summary">${engineerEscapeHtml(summaryText)}</div>` : ''}
          </div>
          <div class="contractor-approved-card__cta" aria-hidden="true">
            <button type="button" class="contractor-approved-card__incele" tabindex="-1">İncele ?</button>
          </div>
        </article>`;
    }).join('')
  }</div>`;
  contractorFeedWireClicks();
}

function contractorRenderFieldSummary(payload) {
  const el = document.getElementById('contractorFieldSummaryGrid');
  if (!el) return;
  const lines = Array.isArray(payload)
     ? payload
    : Array.isArray(payload.lines)
       ? payload.lines
      : Array.isArray(_contractorDashboardSnapshot.site_brief_lines)
         ? _contractorDashboardSnapshot.site_brief_lines
        : [];
  if (!lines.length) {
    el.innerHTML = '<div class="contractor-empty-state" style="grid-column:1/-1;">Yeterli onaylı veri oluşmadı.</div>';
    return;
  }
  el.innerHTML = lines.slice(0, 5).map((line, index) => `
    <article class="contractor-field-brief-card">
      <div class="contractor-field-brief-card__index">0${index + 1}</div>
      <div class="contractor-field-brief-card__text">${engineerEscapeHtml(line)}</div>
    </article>
  `).join('');
}

function contractorRenderFiyatAlerts(alerts) {
  const panel = document.getElementById('contractorFiyatAlertPanel');
  const body = document.getElementById('contractorFiyatAlertBody');
  const countEl = document.getElementById('contractorFiyatAlertCount');
  if (!panel || !body) return;

  const items = Array.isArray(alerts) ? alerts : [];
  if (!items.length) {
    panel.style.display = 'none';
    return;
  }

  panel.style.display = '';
  if (countEl) countEl.textContent = items.length + ' uyarı';

  const toneColors = {
    danger: { border: '#DC2626', bg: '#FEE2E2', text: '#DC2626', label: 'Kritik' },
    warning: { border: '#D97706', bg: '#FEF3C7', text: '#B45309', label: 'Uyarı' },
    success: { border: '#059669', bg: '#D1FAE5', text: '#047857', label: 'Tamam' },
    info: { border: '#0284C7', bg: '#E0F2FE', text: '#0369A1', label: 'Bilgi' },
  };

  body.innerHTML = `<div style="display:flex;flex-direction:column;gap:0;">${
    items.slice(0, 10).map((item) => {
      const tone = engineerAlertTone(item);
      const c = toneColors[tone] || toneColors.info;
      const label = engineerAlertLabel(item) || c.label;
      const material = engineerGetField(item, ['malzeme', 'title', 'baslik', 'message', 'mesaj', 'summary', 'ozet'], 'Fiyat uyarısı');
      const zone = engineerGetField(item, ['zone_label', 'site_label', 'site_name', 'zone', 'saha_adi'], 'Stok / Tedarik Hattı');
      const timestamp = engineerGetField(item, ['created_at', 'timestamp', 'captured_at', 'tarih'], '');
      const parsedDate = engineerParseDate(timestamp);
      const dateLabel = parsedDate ? parsedDate.toLocaleDateString('tr-TR') : '';
      const timeLabel = parsedDate ? parsedDate.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) : '';
      const previous = engineerGetField(item, ['onceki', 'previous', 'old_value'], '');
      const next = engineerGetField(item, ['yeni', 'new_value', 'current'], '');
      const delta = engineerGetField(item, ['degisim', 'change', 'delta'], '');
      const deltaLabel = delta ? `%${delta}` : (previous && next ? `${previous} → ${next}` : '');
      return `
        <div style="display:flex;align-items:flex-start;gap:12px;padding:14px 20px;border-bottom:1px solid rgba(203,213,225,0.6);border-left:3px solid ${c.border};">
          <div style="flex:1;min-width:0;">
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px;">
              <span style="font-size:10px;font-weight:700;background:${c.bg};color:${c.text};padding:2px 8px;border-radius:6px;letter-spacing:0.04em;">${engineerEscapeHtml(label)}</span>
              <span style="font-size:11px;color:#64748B;">${engineerEscapeHtml(zone)}</span>
              ${deltaLabel ? `<span style="font-size:11px;font-weight:700;color:${c.text};">${engineerEscapeHtml(deltaLabel)}</span>` : ''}
            </div>
            <div style="font-size:13px;font-weight:700;color:#0F172A;line-height:1.5;">${engineerEscapeHtml(material)} Uyarısı</div>
            ${dateLabel ? `<div style="font-size:11px;color:#94A3B8;margin-top:2px;">${engineerEscapeHtml(dateLabel)}${timeLabel ? ' ' + engineerEscapeHtml(timeLabel) : ''}</div>` : ''}
          </div>
        </div>`;
    }).join('')
  }</div>`;
}

function _contractorRenderStokUyariBanner(toplam) {
  const banner = document.getElementById('contractorStokUyariBanner');
  const text = document.getElementById('contractorStokUyariBannerText');
  if (!banner) return;
  if (toplam > 0) {
    if (text) text.textContent = `${toplam} kritik stok uyarısı bekliyor — şantiye kartlarında detaylar görünüyor`;
    banner.style.display = 'flex';
  } else {
    banner.style.display = 'none';
  }
}

async function _stokKritikKarar(item, action) {
  if (!item || item._saving) return;
  const statusVal = action === 'approve' ? 'onaylandi' : 'reddedildi';
  item._saving = true;
  kararTerminalRenderDetay(item);
  const token = localStorage.getItem('bai_token') || '';
  try {
    const res = await fetch(`/malzeme-uyari/${item.sourceId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token },
      body: JSON.stringify({ status: statusVal }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || 'Karar kaydedilemedi.');
    item.status = action === 'approve' ? 'approved' : 'rejected';
    item.statusLabel = action === 'approve' ? 'Onaylandı' : 'Reddedildi';
    item.statusTone = action === 'approve' ? 'success' : 'critical';
    if (typeof showToast === 'function') showToast(action === 'approve' ? 'Sipariş onaylandı.' : 'Uyarı ertelendi.', 'success');
  } catch (err) {
    if (typeof showToast === 'function') showToast((err && err.message) || 'Karar kaydedilemedi.', 'warning');
  } finally {
    item._saving = false;
    if (Array.isArray(_engineerDecisionItems)) {
      _engineerDecisionItems = _engineerDecisionItems.map((i) => (i.id === item.id ? item : i));
    }
    kararTerminalRenderListe();
  }
}

async function contractorLoadFiyatAlerts() {
  const token = localStorage.getItem('bai_token') || '';
  if (!token) return;
  try {
    const res = await fetch('/api/fiyat/alertler?limit=10&status=pending', {
      headers: { Authorization: 'Bearer ' + token }
    });
    if (!res.ok) return;
    const data = await res.json();
    const alerts = Array.isArray(data.items) ? data.items : Array.isArray(data.alertler) ? data.alertler : [];
    contractorRenderFiyatAlerts(alerts);
  } catch (_) {}
}

function contractorRenderActionSuggestions(items) {
  const el = document.getElementById('contractorActionList');
  if (!el) return;
  const safeItems = Array.isArray(items) && items.length ? items : [{
    title: 'Onaylı veri akışı bekleniyor',
    body: 'Mühendis kararları geldikçe öneriler burada belirecek.',
    reason: 'Panel varsayılan olarak onaylı sonuçlardan beslenir.',
    action: 'Bugün onaylanan kayıtları tekrar kontrol edin.',
    scope: 'Genel',
    tone: 'neutral',
    prompt: 'Bugün',
  }];
  el.innerHTML = safeItems.map((item) => `
    <article class="contractor-action-card" data-tone="${engineerEscapeHtml(contractorNormalizeTone(item.tone))}">
      <div class="contractor-action-card__head">
        <div class="contractor-action-card__title">${engineerEscapeHtml(contractorPolishText(item.title || 'Operasyon önerisi'))}</div>
      </div>
      <div class="contractor-action-card__body">${engineerEscapeHtml(contractorPolishText(item.body || ''))}</div>
      <div class="contractor-action-card__evidence is-open">
        <ul class="contractor-action-card__evidence-list">
          <li><strong>Neden:</strong> ${engineerEscapeHtml(item.reason || 'Onaylı sonuç akışı bu öneriyi öne çıkarıyor.')}</li>
          <li><strong>Aksiyon:</strong> ${engineerEscapeHtml(item.action || 'Operasyon planını gözden geçirin.')}</li>
          <li><strong>Kapsam:</strong> ${engineerEscapeHtml(item.scope || 'Genel')}</li>
        </ul>
      </div>
      <div class="contractor-action-card__footer">
        <button type="button" class="contractor-action-card__cta" onclick='contractorAssistantUseSuggestion(${JSON.stringify(item.prompt || item.title || 'Bugün')})'>Öneriyi Aç</button>
      </div>
    </article>
  `).join('');
}

function contractorRenderLoading() {
  contractorSetMetric('contractorMetricApproved', 'contractorMetricApprovedValue', 'contractorMetricApprovedContext', 'contractorMetricApprovedNote', { value: 0, tone: 'neutral', context: 'Yükleniyor', note: 'Onay akışı hazırlanıyor.' });
  contractorSetMetric('contractorMetricCritical', 'contractorMetricCriticalValue', 'contractorMetricCriticalContext', 'contractorMetricCriticalNote', { value: 0, tone: 'neutral', context: 'Yükleniyor', note: 'Kritik risk kümesi hazırlanıyor.' });
  contractorSetMetric('contractorMetricWatchlist', 'contractorMetricWatchlistValue', 'contractorMetricWatchlistContext', 'contractorMetricWatchlistNote', { value: 0, tone: 'neutral', context: 'Yükleniyor', note: 'Stok sapmaları hazırlanıyor.' });
  contractorSetMetric('contractorMetricSites', 'contractorMetricSitesValue', 'contractorMetricSitesContext', 'contractorMetricSitesNote', { value: 0, tone: 'neutral', context: 'Yükleniyor', note: 'Şantiye ağı hazırlanıyor.' });
  const feed = document.getElementById('contractorTrendBody');
  const summary = document.getElementById('contractorFieldSummaryGrid');
  const insight = document.getElementById('contractorInsightList');
  if (feed) feed.innerHTML = Array.from({ length: 3 }).map(() => '<div class="engineer-skeleton contractor-approved-card" style="min-height:140px;"></div>').join('');
  if (summary) summary.innerHTML = Array.from({ length: 3 }).map(() => '<div class="engineer-skeleton contractor-field-brief-card" style="min-height:88px;"></div>').join('');
  if (insight) insight.innerHTML = '<div class="engineer-skeleton contractor-summary-hero-card" style="min-height:220px;"></div>';
  contractorRenderChips([]);
  contractorSetCommandMode('idle', 'Onaylı sonuçlar hazırlanıyor.');
}

function contractorRenderLocked(detail) {
  _contractorDashboardSnapshot = null;
  contractorSetMetric('contractorMetricApproved', 'contractorMetricApprovedValue', 'contractorMetricApprovedContext', 'contractorMetricApprovedNote', { value: 0, tone: 'neutral', context: 'Erişim gerekli', note: detail });
  contractorSetMetric('contractorMetricCritical', 'contractorMetricCriticalValue', 'contractorMetricCriticalContext', 'contractorMetricCriticalNote', { value: 0, tone: 'neutral', context: 'Erişim gerekli', note: detail });
  contractorSetMetric('contractorMetricWatchlist', 'contractorMetricWatchlistValue', 'contractorMetricWatchlistContext', 'contractorMetricWatchlistNote', { value: 0, tone: 'neutral', context: 'Erişim gerekli', note: detail });
  contractorSetMetric('contractorMetricSites', 'contractorMetricSitesValue', 'contractorMetricSitesContext', 'contractorMetricSitesNote', { value: 0, tone: 'neutral', context: 'Erişim gerekli', note: detail });
  contractorRenderExecutiveSummary({}, { lines: [detail], footerItems: [] });
  contractorRenderTrend([]);
  contractorRenderFieldSummary([]);
  contractorRenderActionSuggestions([]);
}

function contractorBuildFilteredBrief(items, label, emptyMessage) {
  if (!items.length) return [emptyMessage];
  return items.slice(0, 5).map((item) => {
    const time = contractorFeedTimeLabel(item.time || '');
    return `${time} ? ${item.title || 'Kayıt'} ? ${item.site_name || 'Şantiye etiketi yok'} ? ${item.impact || item.status || label}`;
  });
}

function contractorApplySnapshotFieldFilter(predicate, options = {}) {
  const sourceFeed = Array.isArray(_contractorDashboardSnapshot.today_approved_feed) ? _contractorDashboardSnapshot.today_approved_feed : [];
  const filtered = typeof predicate === 'function' ? sourceFeed.filter(predicate) : sourceFeed;
  _contractorDashboardActiveFilter = options.filterKey || 'custom';
  const lines = contractorBuildFilteredBrief(filtered, options.chipLabel || 'Filtre', options.emptyMessage || 'Bu filtre için onaylı kayıt bulunmuyor.');
  contractorRenderExecutiveSummary(_contractorDashboardSnapshot.executive_summary || {}, {
    lines,
    tone: options.tone || (filtered.length ? 'info' : 'neutral'),
    footerItems: contractorBuildExecutiveMeta(filtered),
    eyebrow: options.eyebrow || 'Filtreli görünüm',
  });
  contractorRenderTrend(filtered);
  contractorRenderFieldSummary(lines);
  contractorRenderChips([
    { label: options.chipLabel || 'Filtre', tone: options.tone || 'info' },
    { label: 'Temizle', tone: 'neutral', prompt: 'temizle' },
  ]);
  contractorRenderActionSuggestions(Array.isArray(_contractorDashboardSnapshot.action_suggestions) ? _contractorDashboardSnapshot.action_suggestions.filter((item) => {
    const scopeText = contractorNormalizeText(`${item.scope || ''} ${item.title || ''} ${item.body || ''}`);
    if (!filtered.length) return false;
    return filtered.some((feedItem) => scopeText.includes(contractorNormalizeText(feedItem.site_name || '')) || scopeText.includes(contractorNormalizeText(feedItem.category || '')));
  }) : []);
  contractorSetResponse(lines.join(' '));
}

function contractorRestoreSnapshotView() {
  _contractorDashboardActiveFilter = null;
  contractorRenderExecutiveSummary(_contractorDashboardSnapshot.executive_summary || {}, {
    lines: Array.isArray(_contractorDashboardSnapshot.site_brief_lines) ? _contractorDashboardSnapshot.site_brief_lines : [],
    footerItems: contractorBuildExecutiveMeta(),
  });
  contractorRenderChips(contractorBuildExecutiveMeta().map((item) => ({ ...item, prompt: '' })));
  contractorRenderTrend(Array.isArray(_contractorDashboardSnapshot.today_approved_feed) ? _contractorDashboardSnapshot.today_approved_feed : []);
  contractorRenderFieldSummary(Array.isArray(_contractorDashboardSnapshot.site_brief_lines) ? _contractorDashboardSnapshot.site_brief_lines : []);
  contractorRenderActionSuggestions(Array.isArray(_contractorDashboardSnapshot.action_suggestions) ? _contractorDashboardSnapshot.action_suggestions : []);
}

function contractorHandleLocalCommand(rawText) {
  const text = contractorNormalizeText(rawText);
  if (!text) return null;
  const navigate = (page, message) => ({ kind: 'navigate', page, message });

  if (/\btemizle\b|\bsifirla\b|\btumu\b/.test(text)) {
    return {
      kind: 'filter',
      action: () => contractorRestoreSnapshotView(),
      message: 'Yönetici görünümü varsayılan onaylı sonuç akışına döndürüldü.',
    };
  }
  if (/\bisg\b/.test(text)) {
    return {
      kind: 'filter',
      action: () => contractorApplySnapshotFieldFilter(
        (item) => contractorNormalizeText(item.category || '').includes('isg') || contractorNormalizeText(item.record_type || '').includes('isg'),
        { filterKey: 'safety', chipLabel: 'İSG filtresi', tone: 'warning', emptyMessage: 'Bugün onaylanan İSG kaydı bulunmuyor.' }
      ),
      message: 'Onaylı İSG kayıtları öne çıkarıldı.',
    };
  }
  if (/\bstok\b|\bmalzeme\b/.test(text)) {
    return {
      kind: 'filter',
      action: () => contractorApplySnapshotFieldFilter(
        (item) => contractorNormalizeText(item.category || '').includes('stok') || contractorNormalizeText(item.title || '').includes('stok') || contractorNormalizeText(item.title || '').includes('malzeme'),
        { filterKey: 'stock', chipLabel: 'Stok filtresi', tone: 'info', emptyMessage: 'Bugün onaylanan stok kaydı bulunmuyor.' }
      ),
      message: 'Onaylı stok ve malzeme kayıtları öne çıkarıldı.',
    };
  }
  if (/\brapor\b/.test(text) && !/\bac\b|\bgit\b/.test(text)) {
    return {
      kind: 'filter',
      action: () => contractorApplySnapshotFieldFilter(
        (item) => contractorNormalizeText(item.source_type || '').includes('report'),
        { filterKey: 'report', chipLabel: 'Rapor filtresi', tone: 'success', emptyMessage: 'Bugün onaylanan rapor bulunmuyor.' }
      ),
      message: 'Onaylı rapor kayıtları öne çıkarıldı.',
    };
  }
  if (/\bbugun\b/.test(text)) {
    return {
      kind: 'filter',
      action: () => contractorApplySnapshotFieldFilter(
        () => true,
        { filterKey: 'today', chipLabel: 'Bugün filtresi', tone: 'info', emptyMessage: 'Bugün onaylanan kayıt bulunmuyor.' }
      ),
      message: 'Bugün onaylanan kayıt akışı gösteriliyor.',
    };
  }
  if (/\bgunluk rapor\b|\brapor ac\b/.test(text)) return navigate('gunluk', 'Günlük rapor ekranı açıldı.');
  if (/\bkamera\b/.test(text)) return navigate('kamera', 'Kamera analizi ekranı açıldı.');
  if (/\bsantiye\b/.test(text)) return navigate('santiye', 'Şantiye dizini açıldı.');
  if (/\barsiv\b/.test(text)) return navigate('arsiv', 'Arşiv görünümü açıldı.');
  return null;
}

// â"€â"€ Contractor Feed Detail Drawer â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€
// Stores the currently-rendered feed items so click handlers can hydrate
// from existing payload without a second fetch.
let _contractorFeedItems = [];

function contractorDrawerEnsureDom() {
  if (document.getElementById('contractorFeedDrawer')) return;
  const el = document.createElement('div');
  el.id = 'contractorFeedDrawer';
  el.className = 'contractor-feed-drawer';
  el.setAttribute('role', 'dialog');
  el.setAttribute('aria-modal', 'true');
  el.setAttribute('aria-label', 'Onaylı kayıt detayı');
  el.innerHTML = `
    <div class="contractor-feed-drawer__backdrop" id="contractorFeedDrawerBackdrop"></div>
    <div class="contractor-feed-drawer__panel" role="document">
      <div class="contractor-feed-drawer__header">
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;flex:1;min-width:0;">
          <span class="contractor-feed-drawer__eyebrow" id="contractorFeedDrawerEyebrow">Onaylı Kayıt</span>
          <span id="contractorFeedDrawerCategoryBadge" style="display:none;font-size:10px;font-weight:800;padding:2px 8px;border-radius:4px;letter-spacing:0.05em;text-transform:uppercase;"></span>
          <span id="contractorFeedDrawerStatusBadge" style="display:none;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;"></span>
        </div>
        <button type="button" class="contractor-feed-drawer__close" id="contractorFeedDrawerClose" aria-label="Kapat">âœ•</button>
      </div>
      <div class="contractor-feed-drawer__body" id="contractorFeedDrawerBody">
        <!-- BAŞLIK BÖLÜMÜ -->
        <div class="contractor-feed-drawer__section" id="contractorFeedDrawerTitleSection">
          <div id="contractorFeedDrawerTitle" style="font-size:18px;font-weight:800;color:#0F172A;line-height:1.4;"></div>
          <div id="contractorFeedDrawerMeta" style="font-size:13px;color:#64748B;display:flex;flex-wrap:wrap;gap:6px;"></div>
        </div>
        <!-- FOTOÄRAF GALERİSİ (koşullu) -->
        <div class="contractor-feed-drawer__section" id="contractorFeedDrawerGallerySection" style="display:none;">
          <div class="contractor-feed-drawer__section-label">Fotoğraflar</div>
          <div class="contractor-feed-drawer__gallery" id="contractorFeedDrawerGallery"></div>
        </div>
        <!-- AI ÖZETİ -->
        <div class="contractor-feed-drawer__section" id="contractorFeedDrawerSummarySection" style="display:none;">
          <div class="contractor-feed-drawer__section-label">AI Özeti</div>
          <div id="contractorFeedDrawerSummary" class="contractor-feed-drawer__summary"></div>
          <div style="font-size:11px;color:#94A3B8;margin-top:2px;">AI tarafından üretildi</div>
        </div>
        <!-- TEKNİK DETAYLAR -->
        <div class="contractor-feed-drawer__section" id="contractorFeedDrawerTechSection" style="display:none;">
          <div class="contractor-feed-drawer__section-label">Teknik Detaylar</div>
          <div class="contractor-feed-drawer__tech-list" id="contractorFeedDrawerTechList"></div>
        </div>
        <!-- THREAD -->
        <div class="contractor-feed-drawer__section" id="contractorFeedDrawerThreadSection" style="display:none;">
          <div class="contractor-feed-drawer__section-label">Geri Bildirimler</div>
          <div class="contractor-feed-drawer__thread" id="contractorFeedDrawerThread">
            <div style="font-size:12px;color:#94A3B8;text-align:center;padding:16px 0;">Henüz geri bildirim yok.</div>
          </div>
          <div class="contractor-feed-drawer__thread-input">
            <input type="text" id="contractorFeedDrawerThreadInput" placeholder="Mesaj yaz..." />
            <button type="button" class="contractor-feed-drawer__thread-send" id="contractorFeedDrawerThreadSend">Gönder</button>
          </div>
        </div>
      </div>
      <!-- AKSİYON BAR -->
      <div class="contractor-feed-drawer__action-bar" id="contractorFeedDrawerActionBar">
        <button type="button" class="contractor-feed-drawer__action-btn" id="contractorFeedDrawerArchiveBtn" data-variant="primary">Arşivle</button>
      </div>
    </div>`;
  document.body.appendChild(el);

  document.getElementById('contractorFeedDrawerClose').onclick = contractorDrawerClose;
  document.getElementById('contractorFeedDrawerBackdrop').onclick = contractorDrawerClose;
  el.addEventListener('keydown', (e) => { if (e.key === 'Escape') contractorDrawerClose(); });
}

function contractorDrawerOpen(item) {
  contractorDrawerEnsureDom();
  const drawer = document.getElementById('contractorFeedDrawer');
  if (!drawer) return;

  const cat = item.category || '';
  const statusTone = contractorApprovedStatusTone(item.status);
  const timeText = item.time ? new Date(item.time).toLocaleString('tr-TR', { day: '2-digit', month: 'long', hour: '2-digit', minute: '2-digit' }) : '';
  const sourceLabel = item.source_type === 'alert' ? 'Malzeme uyarısı' : item.source_type === 'report' ? 'Günlük rapor' : 'Saha kaydı';

  // HEADER ?? eyebrow + badges
  const eyebrow = document.getElementById('contractorFeedDrawerEyebrow');
  if (eyebrow) eyebrow.textContent = item.record_type || 'Onaylı Kayıt';

  const catBadge = document.getElementById('contractorFeedDrawerCategoryBadge');
  if (catBadge) {
    if (cat) {
      const catBg = cat === 'ISG' ? '#FEE2E2' : cat === 'Stok' ? '#DBEAFE' : '#F1F5F9';
      const catFg = cat === 'ISG' ? '#DC2626' : cat === 'Stok' ? '#1D4ED8' : '#475569';
      catBadge.textContent = cat;
      catBadge.style.cssText = `display:inline-block;font-size:10px;font-weight:800;padding:2px 8px;border-radius:4px;letter-spacing:0.05em;text-transform:uppercase;background:${catBg};color:${catFg};`;
    } else {
      catBadge.style.display = 'none';
    }
  }

  const statusBadge = document.getElementById('contractorFeedDrawerStatusBadge');
  if (statusBadge) {
    const sBg = statusTone === 'success' ? '#DCFCE7' : statusTone === 'danger' ? '#FEE2E2' : '#F1F5F9';
    const sFg = statusTone === 'success' ? '#15803D' : statusTone === 'danger' ? '#DC2626' : '#475569';
    statusBadge.textContent = item.status || 'Onaylandı';
    statusBadge.style.cssText = `display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;background:${sBg};color:${sFg};`;
  }

  // BAŞLIK
  const titleEl = document.getElementById('contractorFeedDrawerTitle');
  if (titleEl) titleEl.textContent = kararTerminalCapTitle(item.title || 'Onaylı kayıt');

  const metaEl = document.getElementById('contractorFeedDrawerMeta');
  if (metaEl) {
    const parts = [
      item.site_name ? engineerEscapeHtml(item.site_name) : null,
      timeText ? engineerEscapeHtml(timeText) : null,
      item.source_type ? engineerEscapeHtml(sourceLabel) : null,
    ].filter(Boolean);
    metaEl.innerHTML = parts.map(p => `<span>${p}</span>`).join('<span style="color:#CBD5E1;">?</span>');
  }

  // GALERİ ?? fotoğraf varsa göster, yoksa gizli kal
  const gallerySection = document.getElementById('contractorFeedDrawerGallerySection');
  const gallery = document.getElementById('contractorFeedDrawerGallery');
  const photos = item.photos || (item.thumbnail ? [item.thumbnail] : []);
  if (gallerySection && gallery) {
    if (photos.length) {
      gallery.innerHTML = photos.map(src =>
        `<div class="contractor-feed-drawer__gallery-item">
          <img src="${engineerEscapeHtml(src)}" alt="Saha görseli" loading="lazy"
               onerror="this.parentElement.style.display='none'">
        </div>`
      ).join('');
      gallerySection.style.display = '';
    } else {
      gallerySection.style.display = 'none';
    }
  }

  // AI ÖZETİ ?? varsa göster
  const summarySection = document.getElementById('contractorFeedDrawerSummarySection');
  const summaryEl = document.getElementById('contractorFeedDrawerSummary');
  const summaryText = item.summary || item.note || '';
  if (summarySection && summaryEl) {
    if (summaryText) {
      summaryEl.textContent = summaryText;
      summarySection.style.display = '';
    } else {
      summarySection.style.display = 'none';
    }
  }

  // TEKNİK DETAYLAR ?? her zaman görünür
  const techSection = document.getElementById('contractorFeedDrawerTechSection');
  const techList = document.getElementById('contractorFeedDrawerTechList');
  if (techSection && techList) {
    techSection.style.display = '';
    const rows = [
      ['Şantiye', item.site_name],
      ['Kategori', cat],
      ['Onay zamanı', timeText],
      ['Kaynak', item.source_type ? sourceLabel : null],
      ['Kayıt tipi', item.record_type],
      ['Etki', item.impact || item.delta],
    ].filter(([, v]) => v);
    techList.innerHTML = rows.length
       ? rows.map(([k, v]) =>
          `<div class="contractor-feed-drawer__tech-row">
            <span class="contractor-feed-drawer__tech-key">${engineerEscapeHtml(k)}</span>
            <span class="contractor-feed-drawer__tech-value">${engineerEscapeHtml(String(v))}</span>
          </div>`
        ).join('')
      : `<div class="contractor-feed-drawer__tech-row">
          <span class="contractor-feed-drawer__tech-key">?</span>
          <span class="contractor-feed-drawer__tech-value">?</span>
        </div>`;
  }

  // THREAD ?? her zaman görünür, backend'den yükle
  const decisionId = item.decision_id || null;
  const token = localStorage.getItem('bai_token');
  const threadEl = document.getElementById('contractorFeedDrawerThread');
  let inputEl = document.getElementById('contractorFeedDrawerThreadInput');
  let sendEl = document.getElementById('contractorFeedDrawerThreadSend');

  if (threadEl) {
    threadEl.innerHTML = '<div style="color:#94A3B8;font-size:13px;padding:12px 0;">Yükleniyor...</div>';
  }

  if (inputEl) {
    inputEl.disabled = !decisionId;
    inputEl.placeholder = decisionId ? 'Mesaj yaz...' : 'Karar ID yok';
    inputEl.value = '';
  }
  if (sendEl) sendEl.disabled = !decisionId;

  if (decisionId && threadEl) {
    fetch('/karar/' + decisionId + '/mesajlartoken=' + token)
      .then(r => r.json())
      .then(data => { contractorRenderThread(data.mesajlar || [], decisionId); })
      .catch(() => {
        threadEl.innerHTML = '<div style="color:#EF4444;font-size:13px;padding:12px 0;">Mesajlar yüklenemedi.</div>';
      });
  } else if (threadEl) {
    threadEl.innerHTML = '<div style="color:#94A3B8;font-size:13px;padding:12px 0;">Henüz geri bildirim yok. İlk mesajı sen yaz.</div>';
  }

  // Gönder butonu ?? her açılışta yeniden bağla (clone ile eski handler'ları temizle)
  inputEl = document.getElementById('contractorFeedDrawerThreadInput');
  sendEl = document.getElementById('contractorFeedDrawerThreadSend');
  if (sendEl && decisionId) {
    const newSendEl = sendEl.cloneNode(true);
    sendEl.parentNode.replaceChild(newSendEl, sendEl);
    newSendEl.addEventListener('click', function() { contractorSendMessage(decisionId); });
  }
  if (inputEl && decisionId) {
    const newInputEl = inputEl.cloneNode(true);
    inputEl.parentNode.replaceChild(newInputEl, inputEl);
    newInputEl.addEventListener('keypress', function(e) {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); contractorSendMessage(decisionId); }
    });
  }

  // Arşivle butonu
  const archiveBtn = document.getElementById('contractorFeedDrawerArchiveBtn');
  if (archiveBtn && decisionId) {
    const newArchiveBtn = archiveBtn.cloneNode(true);
    archiveBtn.parentNode.replaceChild(newArchiveBtn, archiveBtn);
    newArchiveBtn.disabled = false;
    newArchiveBtn.textContent = 'Arşivle';
    newArchiveBtn.addEventListener('click', function() {
      contractorArchiveDecision(decisionId);
    });
  }

  drawer.classList.add('is-open');
  document.body.style.overflow = 'hidden';
  const closeBtn = document.getElementById('contractorFeedDrawerClose');
  if (closeBtn) setTimeout(() => closeBtn.focus(), 50);
}

function contractorDrawerClose() {
  const drawer = document.getElementById('contractorFeedDrawer');
  if (!drawer) return;
  drawer.classList.remove('is-open');
  document.body.style.overflow = '';
}

function contractorRenderThread(mesajlar, decisionId) {
  const threadEl = document.getElementById('contractorFeedDrawerThread');
  if (!threadEl) return;

  if (!mesajlar || mesajlar.length === 0) {
    threadEl.innerHTML = '<div style="color:#94A3B8;font-size:13px;padding:12px 0;">Henüz geri bildirim yok. İlk mesajı sen yaz.</div>';
    return;
  }

  const html = mesajlar.map(m => {
    const normalizedRole = m.kullanici_rolu === 'mutahhit' ? 'muteahhit' : m.kullanici_rolu;
    const rolLabel = contractorRoleLabel(normalizedRole);
    const rolClass = 'contractor-feed-drawer__thread-role contractor-feed-drawer__thread-role--' + (normalizedRole || 'default');
    const tarih = contractorFormatMessageTime(m.created_at);
    const escapedName = engineerEscapeHtml(m.kullanici_adi || '');
    const escapedMsg = engineerEscapeHtml(m.mesaj || '');
    return `<div class="contractor-feed-drawer__thread-item">
      <div class="contractor-feed-drawer__thread-meta">
        <span class="${rolClass}">${rolLabel}</span>
        <span style="font-weight:500;">${escapedName}</span>
        <span style="color:#CBD5E1;">?</span>
        <span style="color:#94A3B8;font-size:12px;">${tarih}</span>
      </div>
      <div class="contractor-feed-drawer__thread-body">${escapedMsg}</div>
    </div>`;
  }).join('');

  threadEl.innerHTML = html;
}

function contractorRoleLabel(role) {
  if (role === 'muhendis') return 'MÜHENDİS';
  if (role === 'muteahhit') return 'MÜTEAHHİT';
  if (role === 'santi_sefi') return 'ŞANTİYE';
  if (role === 'yonetici') return 'YÖNETİCİ';
  if (role === 'admin') return 'ADMIN';
  return 'KULLANICI';
}

function contractorFormatMessageTime(isoString) {
  if (!isoString) return '';
  try {
    const d = new Date(isoString);
    const now = new Date();
    const diffMin = Math.floor((now - d) / 60000);
    if (diffMin < 1) return 'Şimdi';
    if (diffMin < 60) return diffMin + ' dakika önce';
    const diffHour = Math.floor(diffMin / 60);
    if (diffHour < 24) return diffHour + ' saat önce';
    const aylar = ['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu','Eyl','Eki','Kas','Ara'];
    return `${d.getDate()} ${aylar[d.getMonth()]} ${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
  } catch (e) { return ''; }
}

function contractorArchiveDecision(decisionId) {
  if (!decisionId) return;

  if (!confirm('Bu karar arşivlenecek. Ana listeden kaldırılacak ama arşiv sayfasında görünmeye devam edecek. Devam edilsin mi')) {
    return;
  }

  const archiveBtn = document.getElementById('contractorFeedDrawerArchiveBtn');
  if (archiveBtn) {
    archiveBtn.disabled = true;
    archiveBtn.textContent = 'Arşivleniyor...';
  }

  const token = localStorage.getItem('bai_token');

  fetch('/karar/' + decisionId + '/arsivletoken=' + token, { method: 'POST' })
    .then(r => {
      if (!r.ok) {
        return r.json().then(err => { throw new Error(err.detail || 'Arşivleme başarısız'); });
      }
      return r.json();
    })
    .then(() => {
      if (typeof contractorDrawerClose === 'function') contractorDrawerClose();
      loadContractorDashboard();
    })
    .catch(err => {
      alert('Arşivleme başarısız: ' + (err.message || 'Bilinmeyen hata'));
      if (archiveBtn) {
        archiveBtn.disabled = false;
        archiveBtn.textContent = 'Arşivle';
      }
    });
}

function contractorSendMessage(decisionId) {
  const inputEl = document.getElementById('contractorFeedDrawerThreadInput');
  const sendEl = document.getElementById('contractorFeedDrawerThreadSend');
  if (!inputEl || !decisionId) return;
  const mesaj = (inputEl.value || '').trim();
  if (!mesaj) return;

  inputEl.disabled = true;
  if (sendEl) sendEl.disabled = true;

  const token = localStorage.getItem('bai_token');
  fetch('/karar/' + decisionId + '/mesajtoken=' + token, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({mesaj: mesaj})
  })
  .then(r => { if (!r.ok) throw new Error('Mesaj gönderilemedi'); return r.json(); })
  .then(() => fetch('/karar/' + decisionId + '/mesajlartoken=' + token).then(r => r.json()))
  .then(data => {
    contractorRenderThread(data.mesajlar || [], decisionId);
    if (inputEl) inputEl.value = '';
  })
  .catch(err => { alert('Mesaj gönderilemedi: ' + (err.message || 'Hata')); })
  .finally(() => {
    if (inputEl) { inputEl.disabled = false; inputEl.focus(); }
    if (sendEl) sendEl.disabled = false;
  });
}

function contractorFeedWireClicks() {
  const trendBody = document.getElementById('contractorTrendBody');
  if (!trendBody || trendBody._drawerWired) return;
  trendBody._drawerWired = true;
  trendBody.addEventListener('click', (e) => {
    const card = e.target.closest('.contractor-approved-card[data-feed-idx]');
    if (!card) return;
    const idx = parseInt(card.getAttribute('data-feed-idx'), 10);
    const item = _contractorFeedItems[idx];
    if (item) contractorDrawerOpen(item);
  });
  trendBody.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const card = e.target.closest('.contractor-approved-card[data-feed-idx]');
    if (!card) return;
    e.preventDefault();
    const idx = parseInt(card.getAttribute('data-feed-idx'), 10);
    const item = _contractorFeedItems[idx];
    if (item) contractorDrawerOpen(item);
  });
}
// â"€â"€ /Contractor Feed Detail Drawer â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

async function loadContractorDashboard(force = false) {
  const root = document.getElementById('contractorDashboard');
  if (!root) return;
  if (_contractorDashboardLoading) return;

  const activeRole = localStorage.getItem('bai_rol');
  const token = localStorage.getItem('bai_token') || '';
  setDashboardVisibility(activeRole);

  if (!_contractorDashboardLoaded || force || root.dataset.onboarding === 'true') {
    const activeSiteCount = await contractorFetchActiveSiteCount(token);
    if (activeSiteCount === 0) {
      contractorRenderOnboarding(root);
      _contractorDashboardLoaded = false;
      return;
    }
    contractorRestoreDefaultDashboard(root);
  }

  if (_contractorDashboardLoaded && !force) {
    return;
  }

  contractorRenderLoading();
  contractorSetResponse('', 'empty');
  _contractorDashboardLoading = true;

  try {
    if (isContractorRole(activeRole)) {
      await syncProfileToServer({ role: activeRole }, { silent: true });
    }

    const res = await fetch('/api/dashboard/contractor', {
      method: 'GET',
      headers: token ? { Authorization: 'Bearer ' + token } : {},
    });
    const data = await res.json();
    if (res.status === 403) {
      contractorRenderLocked(data.detail || 'Bu görünüm yalnızca yönetici rollerine açıktır.');
      contractorSetResponse(data.detail || 'Yönetici rolü gerekli.');
      _contractorDashboardLoaded = false;
      return;
    }
    if (!res.ok) throw new Error(data.detail || 'Dashboard verisi alınamadı.');
    _contractorDashboardSnapshot = data;
    contractorToggleCommandRail(window.innerWidth >= 1024);

    contractorSetMetric('contractorMetricApproved', 'contractorMetricApprovedValue', 'contractorMetricApprovedContext', 'contractorMetricApprovedNote', contractorMetricLookup('approved_today'));
    contractorSetMetric('contractorMetricCritical', 'contractorMetricCriticalValue', 'contractorMetricCriticalContext', 'contractorMetricCriticalNote', contractorMetricLookup('open_critical_risk'));
    contractorSetMetric('contractorMetricWatchlist', 'contractorMetricWatchlistValue', 'contractorMetricWatchlistContext', 'contractorMetricWatchlistNote', contractorMetricLookup('critical_stock_delta'));
    contractorSetMetric('contractorMetricSites', 'contractorMetricSitesValue', 'contractorMetricSitesContext', 'contractorMetricSitesNote', contractorMetricLookup('active_sites'));

    contractorRestoreSnapshotView();
    contractorSetResponse('', 'empty');
    contractorSetCommandMode('idle', 'Onaylı sonuçlara göre filtreleyebilir veya derin analiz isteyebilirsiniz.');
    contractorLoadFiyatAlerts();
    _contractorRenderStokUyariBanner(Number(data.stok_uyari_toplam || 0));
    _contractorDashboardLoaded = true;
  } catch (err) {
    _contractorDashboardSnapshot = null;
    const errMsg = err.message || 'Dashboard verisi alınamadı.';
    console.error('[ContractorDashboard] load error:', errMsg);
    contractorRenderLocked(errMsg);
    contractorSetCommandMode('offline', 'Bağlantı kurulamadı. Sayfa yenilenince tekrar denenir.');
    // Show compact secondary state instead of raw server error in AI panel
    contractorSetResponse('Veri yüklenemedi. Filtreleme devre dışı; sayfa yenilenince otomatik tekrar denenir.', 'empty');
    _contractorDashboardLoaded = false;
  } finally {
    _contractorDashboardLoading = false;
  }
}

function arsivTabSec(tab) {
  _arsivAktifTab = tab;
  ['tumu', 'rapor', 'kamera', 'karar'].forEach((name) => {
    const btn = document.getElementById(`arsivTab${name.charAt(0).toUpperCase()}${name.slice(1)}`);
    if (!btn) return;
    const active = name === tab;
    btn.style.background = active ? '#0F172A' : '#FFFFFF';
    btn.style.color = active ? '#FFFFFF' : '#64748B';
    btn.style.borderColor = active ? '#0F172A' : '#E2E8F0';
  });
  arsivRenderListe();
}

function arsivKararKartHtml(item) {
  const when = item.decided_at || item.created_at || '';
  const time = when ? engineerNormalizeDateParts(when).fullLabel : 'Tarih yok';
  const title = item.title || item.description || 'Karar kaydı';
  const category = item.event_type || 'Genel';
  const badgeTone = category === 'ISG' ? '#FEE2E2' : category === 'Stok' ? '#FEF3C7' : '#DCFCE7';
  const badgeText = category === 'ISG' ? '#DC2626' : category === 'Stok' ? '#B45309' : '#15803D';
  return `
    <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-left:3px solid ${badgeText};border-radius:12px;padding:14px 16px;display:flex;align-items:flex-start;gap:12px;transition:box-shadow 0.15s;" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
      <div style="flex:1;cursor:pointer;" onclick="arsivDetayGoster('karar', ${Number(item.id || 0)})">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap;">
          <span style="font-size:10px;font-weight:700;background:${badgeTone};color:${badgeText};padding:2px 8px;border-radius:6px;letter-spacing:0.04em;">${engineerEscapeHtml(item.status_label || 'Karar')}</span>
          <span style="font-size:11px;color:#64748B;">${engineerEscapeHtml(item.record_type_label || 'Kayıt')}</span>
          <span style="font-size:11px;color:#94A3B8;">${engineerEscapeHtml(time)}</span>
        </div>
        <div style="font-size:13px;font-weight:700;color:#0F172A;line-height:1.5;">${engineerEscapeHtml(title)}</div>
        <div style="font-size:12px;color:#64748B;line-height:1.6;margin-top:4px;">${engineerEscapeHtml(item.santiye_adi || 'Şantiye etiketi yok')} ? ${engineerEscapeHtml(category)} ? ${engineerEscapeHtml(item.decision_note || item.description || '')}</div>
      </div>
    </div>`;
}

function arsivRenderListe() {
  const q = String((document.getElementById('arsivAramaInput') || {}).value || '').toLocaleLowerCase('tr-TR');
  const includesQuery = (parts) => !q || parts.some((part) => String(part || '').toLocaleLowerCase('tr-TR').includes(q));
  const reports = (_arsivData.raporlar || []).filter((item) => includesQuery([item.ozet, item.tarih]));
  const cameras = (_arsivData.kamera_analizler || []).filter((item) => includesQuery([item.ozet, item.sehir, item.tip]));
  const decisions = (_arsivData.kararlar || []).filter((item) => includesQuery([item.title, item.description, item.decision_note, item.santiye_adi, item.status_label, item.event_type]));

  const showReports = _arsivAktifTab === 'tumu' || _arsivAktifTab === 'rapor';
  const showCameras = _arsivAktifTab === 'tumu' || _arsivAktifTab === 'kamera';
  const showDecisions = _arsivAktifTab === 'tumu' || _arsivAktifTab === 'karar';
  let html = '';

  if (showDecisions && decisions.length) {
    html += `<div style="font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;margin-top:${html ? '24px' : '0'}">Karar Geçmişi (${decisions.length})</div>`;
    html += `<div style="display:flex;flex-direction:column;gap:8px;">${decisions.map(arsivKararKartHtml).join('')}</div>`;
  }

  if (showReports && reports.length) {
    html += `<div style="font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;margin-top:${html ? '24px' : '0'}">AI Raporları (${reports.length})</div>`;
    html += '<div style="display:flex;flex-direction:column;gap:8px;">';
    reports.forEach((item) => {
      const tarih = item.tarih || (item.created_at ? item.created_at.slice(0, 10) : '?');
      const ozet = String(item.ozet || '').replace(/#{1,6}\s*/g, '').replace(/\*\*/g, '').replace(/\*/g, '').replace(/`/g, '').substring(0, 110);
      html += `<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-left:3px solid #F97316;border-radius:12px;padding:14px 16px;display:flex;align-items:flex-start;gap:12px;transition:box-shadow 0.15s;" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
        <div style="flex:1;cursor:pointer;" onclick="arsivDetayGoster('rapor', ${Number(item.id)})">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
            <span style="font-size:10px;font-weight:700;background:#FFF7ED;color:#F97316;padding:2px 8px;border-radius:6px;letter-spacing:0.04em;">AI RAPOR</span>
            <span style="font-size:11px;color:#94A3B8;">${engineerEscapeHtml(tarih)}</span>
          </div>
          <div style="font-size:13px;color:#334155;line-height:1.5;">${engineerEscapeHtml(ozet)}${ozet.length >= 110 ? '...' : ''}</div>
        </div>
        <button onclick="arsivSil('rapor', ${Number(item.id)})" title="Sil" style="width:30px;height:30px;background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#EF4444;font-size:13px;">🚀</button>
      </div>`;
    });
    html += '</div>';
  }

  if (showCameras && cameras.length) {
    html += `<div style="font-size:11px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;margin-top:${html ? '24px' : '0'}">Kamera Analizleri (${cameras.length})</div>`;
    html += '<div style="display:flex;flex-direction:column;gap:8px;">';
    cameras.forEach((item) => {
      const tipRenk = item.tip === 'guvenlik' ? '#D97706' : item.tip === 'ilerleme' ? '#2563EB' : '#7C3AED';
      const tipBg = item.tip === 'guvenlik' ? '#FFFBEB' : item.tip === 'ilerleme' ? '#EFF6FF' : '#F5F3FF';
      const tipAd = item.tip === 'guvenlik' ? 'GÜVENLİK' : item.tip === 'ilerleme' ? 'İLERLEME' : 'GENEL';
      const tarih = item.created_at ? item.created_at.slice(0, 10) : '?';
      const ozet = String(item.ozet || '').replace(/#{1,6}\s*/g, '').replace(/\*\*/g, '').replace(/\*/g, '').replace(/`/g, '').substring(0, 110);
      const thumb = localStorage.getItem(`bai_thumb_${item.id}`);
      html += `<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-left:3px solid ${tipRenk};border-radius:12px;padding:14px 16px;display:flex;align-items:flex-start;gap:12px;transition:box-shadow 0.15s;" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.08)'" onmouseout="this.style.boxShadow='none'">
        ${thumb ? `<img src="${thumb}" style="width:52px;height:40px;object-fit:cover;border-radius:6px;flex-shrink:0;cursor:pointer;" onclick="arsivDetayGoster('kamera', ${Number(item.id)})">` : ''}
        <div style="flex:1;cursor:pointer;" onclick="arsivDetayGoster('kamera', ${Number(item.id)})">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;flex-wrap:wrap;">
            <span style="font-size:10px;font-weight:700;background:${tipBg};color:${tipRenk};padding:2px 8px;border-radius:6px;letter-spacing:0.04em;">${tipAd}</span>
            ${item.sehir ? `<span style="font-size:11px;color:#64748B;">${engineerEscapeHtml(item.sehir)}</span>` : ''}
            <span style="font-size:11px;color:#94A3B8;">${engineerEscapeHtml(tarih)}</span>
          </div>
          <div style="font-size:13px;color:#334155;line-height:1.5;">${engineerEscapeHtml(ozet)}${ozet.length >= 110 ? '...' : ''}</div>
        </div>
        <button onclick="arsivSil('kamera', ${Number(item.id)})" title="Sil" style="width:30px;height:30px;background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;color:#EF4444;font-size:13px;">🚀</button>
      </div>`;
    });
    html += '</div>';
  }

  if (!html) {
    html = `<div style="text-align:center;padding:60px 20px;color:#94A3B8;">
      <div style="font-size:40px;margin-bottom:10px;">🏠</div>
      <div style="font-size:14px;font-weight:600;color:#64748B;">Kayıt bulunamadı</div>
      <div style="font-size:12px;margin-top:4px;">${q ? `"${engineerEscapeHtml(q)}" için sonuç yok` : _arsivAktifTab === 'karar' ? 'Henüz onaylanmış veya reddedilmiş karar kaydı yok.' : 'Henüz arşiv kaydı oluşmadı.'}</div>
    </div>`;
  }

  document.getElementById('arsivIcerik').innerHTML = html;
}

// â"€â"€ Satın Alma & Tedarikçi Tab Fonksiyonları â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€

function satinAlmaTabAc() {
    const satinAlmaTab = document.getElementById('satinAlmaTab');
    const tedarikciTab = document.getElementById('tedarikciTab');

    document.querySelectorAll('#fiyatPage > div:not([id="satinAlmaTab"]):not([id="tedarikciTab"]):not(:first-child)').forEach(el => {
        if (!el.querySelector('.fiyat-tab-bar') && el.id !== 'satinAlmaTab' && el.id !== 'tedarikciTab') {
            el.setAttribute('data-sa-hidden', 'true');
            el.style.display = 'none';
        }
    });

    if (tedarikciTab) tedarikciTab.style.display = 'none';
    if (satinAlmaTab) { satinAlmaTab.style.display = 'flex'; }

    satinAlmaTabYukle();
}

function tedarikciTabAc() {
    const satinAlmaTab = document.getElementById('satinAlmaTab');
    const tedarikciTab = document.getElementById('tedarikciTab');

    document.querySelectorAll('#fiyatPage > div:not([id="satinAlmaTab"]):not([id="tedarikciTab"]):not(:first-child)').forEach(el => {
        if (!el.querySelector('.fiyat-tab-bar') && el.id !== 'satinAlmaTab' && el.id !== 'tedarikciTab') {
            el.setAttribute('data-sa-hidden', 'true');
            el.style.display = 'none';
        }
    });

    if (satinAlmaTab) satinAlmaTab.style.display = 'none';
    if (tedarikciTab) { tedarikciTab.style.display = 'flex'; }

    tedarikciTabYukle();
}

function fiyatGrafikleriGeriGetir() {
    const satinAlmaTab = document.getElementById('satinAlmaTab');
    const tedarikciTab = document.getElementById('tedarikciTab');
    if (satinAlmaTab) satinAlmaTab.style.display = 'none';
    if (tedarikciTab) tedarikciTab.style.display = 'none';

    document.querySelectorAll('#fiyatPage [data-sa-hidden="true"]').forEach(el => {
        el.style.display = '';
        el.removeAttribute('data-sa-hidden');
    });

    const btnGrafikler = document.getElementById('toolbarGrafikler');
    const btnSatinAlma = document.getElementById('toolbarSatinAlma');
    const btnTedarikciler = document.getElementById('toolbarTedarikciler');
    const aktifStyle = 'padding:7px 16px;border-radius:8px;border:none;font-size:13px;font-weight:500;cursor:pointer;transition:all 0.15s;background:#FFFFFF;color:#0F172A;box-shadow:0 1px 2px rgba(0,0,0,0.06);';
    const pasifStyle = 'padding:7px 16px;border-radius:8px;border:none;font-size:13px;font-weight:500;cursor:pointer;transition:all 0.15s;background:transparent;color:#64748B;box-shadow:none;';
    if (btnGrafikler) btnGrafikler.style.cssText = aktifStyle;
    if (btnSatinAlma) btnSatinAlma.style.cssText = pasifStyle;
    if (btnTedarikciler) btnTedarikciler.style.cssText = pasifStyle;
}

function toolbarSec(tab) {
    const btnGrafikler = document.getElementById('toolbarGrafikler');
    const btnSatinAlma = document.getElementById('toolbarSatinAlma');
    const btnTedarikciler = document.getElementById('toolbarTedarikciler');

    const aktifStyle = 'padding:7px 16px;border-radius:8px;border:none;font-size:13px;font-weight:500;cursor:pointer;transition:all 0.15s;background:#FFFFFF;color:#0F172A;box-shadow:0 1px 2px rgba(0,0,0,0.06);';
    const pasifStyle = 'padding:7px 16px;border-radius:8px;border:none;font-size:13px;font-weight:500;cursor:pointer;transition:all 0.15s;background:transparent;color:#64748B;box-shadow:none;';

    if (btnGrafikler) btnGrafikler.style.cssText = (tab === 'grafikler') ? aktifStyle : pasifStyle;
    if (btnSatinAlma) btnSatinAlma.style.cssText = (tab === 'satin-alma') ? aktifStyle : pasifStyle;
    if (btnTedarikciler) btnTedarikciler.style.cssText = (tab === 'tedarikciler') ? aktifStyle : pasifStyle;

    if (tab === 'grafikler') {
        fiyatGrafikleriGeriGetir();
    } else if (tab === 'satin-alma') {
        satinAlmaTabAc();
    } else if (tab === 'tedarikciler') {
        tedarikciTabAc();
    }
}

async function satinAlmaTabYukle() {
    const container = document.getElementById('satinAlmaTab');
    if (!container) return;
    container.innerHTML = '<div style="text-align:center;padding:40px;color:#64748B;">Yükleniyor...</div>';

    const token = localStorage.getItem('bai_token');

    let santiyeler = [], tedarikciler = [], katalog = [], kayitlar = [];

    try {
        const [sRes, tRes, kRes, saRes] = await Promise.all([
            fetch('/santiyeler', {headers: {'Authorization': 'Bearer ' + token}}),
            fetch('/api/tedarikciler', {headers: {'Authorization': 'Bearer ' + token}}),
            fetch('/api/katalog', {headers: {'Authorization': 'Bearer ' + token}}),
            fetch('/api/satin-almalar', {headers: {'Authorization': 'Bearer ' + token}})
        ]);
        const sData = await sRes.json(); santiyeler = sData.santiyeler || sData || [];
        const tData = await tRes.json(); tedarikciler = tData.tedarikciler || [];
        const kData = await kRes.json(); katalog = kData.katalog || [];
        const saData = await saRes.json(); kayitlar = saData.kayitlar || [];
    } catch(e) { console.error('Satın alma veri yükleme hatası:', e); }

    const santiyeOpts = santiyeler.map(s => `<option value="${s.id}">${s.ad || s.isim || s.name || 'Şantiye'}</option>`).join('');
    const tedarikciOpts = tedarikciler.map(t => `<option value="${t.id}">${t.ad}</option>`).join('');

    let katalogOpts = '';
    katalog.forEach(k => {
        if (k.cesitler && k.cesitler.length > 0) {
            katalogOpts += `<optgroup label="${k.ad}">`;
            k.cesitler.forEach(c => {
                katalogOpts += `<option value="${c.id}" data-birim="${c.birim}">${c.ad} (${c.birim})</option>`;
            });
            katalogOpts += '</optgroup>';
        }
    });

    const toplamTutar = kayitlar.reduce((t, k) => t + (k.toplam_tutar || 0), 0);

    let kayitHTML = '';
    if (kayitlar.length === 0) {
        kayitHTML = '<div style="text-align:center;color:#64748B;padding:40px;font-size:14px;">Henüz satın alma kaydı yok. Yukarıdaki butona tıklayarak ilk kaydınızı ekleyin.</div>';
    } else {
        kayitHTML = `<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:13px;">
            <thead><tr style="border-bottom:2px solid #E2E8F0;color:#64748B;text-align:left;">
                <th style="padding:10px;">Tarih</th><th style="padding:10px;">Şantiye</th><th style="padding:10px;">Tedarikçi</th>
                <th style="padding:10px;">Malzeme</th><th style="padding:10px;">Miktar</th><th style="padding:10px;">Birim Fiyat</th>
                <th style="padding:10px;">Toplam</th><th style="padding:10px;">Fatura</th><th style="padding:10px;"></th>
            </tr></thead><tbody>`;

        kayitlar.forEach(k => {
            const tarih = k.tarih ? new Date(k.tarih).toLocaleDateString('tr-TR') : '-';
            kayitHTML += `<tr style="border-bottom:1px solid #F1F5F9;color:#334155;">
                <td style="padding:10px;">${tarih}</td>
                <td style="padding:10px;">${k.santiye_ad || '-'}</td>
                <td style="padding:10px;">${k.tedarikci_ad || '-'}</td>
                <td style="padding:10px;">${k.malzeme_ad || '-'}</td>
                <td style="padding:10px;">${k.miktar} ${k.birim || ''}</td>
                <td style="padding:10px;">?${k.birim_fiyat.toLocaleString('tr-TR') || '-'}</td>
                <td style="padding:10px;font-weight:600;color:#10B981;">?${k.toplam_tutar.toLocaleString('tr-TR') || '-'}</td>
                <td style="padding:10px;">${k.fatura_no || '-'}</td>
                <td style="padding:10px;"><button onclick="satinAlmaSil(${k.id})" style="background:none;border:none;color:#EF4444;cursor:pointer;" title="Sil">🗑¸</button></td>
            </tr>`;
        });
        kayitHTML += '</tbody></table></div>';
    }

    container.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px;padding-top:10px;">
            <div>
                <h2 style="margin:0;color:#0F172A;font-size:20px;font-weight:600;">Satın Alma Kayıtları</h2>
                <p class="sa-ozet" style="margin:4px 0 0;color:#64748B;font-size:13px;">${kayitlar.length} kayıt ?? Toplam ?${toplamTutar.toLocaleString('tr-TR')}</p>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
                <button onclick="faturaUploadAc()" style="background:transparent;color:#6366F1;border:1px solid #6366F1;padding:10px 20px;border-radius:10px;cursor:pointer;font-size:14px;font-weight:500;">
                    Fatura ile Ekle
                </button>
                <button onclick="saFormToggle()" style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;border:none;padding:10px 20px;border-radius:10px;cursor:pointer;font-size:14px;font-weight:500;">
                    + Yeni Kayıt
                </button>
            </div>
        </div>

        <div id="saForm" style="display:none;background:#FFFFFF;border:1px solid #E2E8F0;box-shadow:0 1px 3px rgba(0,0,0,0.05);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;">
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Şantiye</label>
                    <select id="saShantiye" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                        <option value="">Seçiniz</option>${santiyeOpts}
                    </select>
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Tedarikçi</label>
                    <select id="saTedarikci" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                        <option value="">Seçiniz</option>${tedarikciOpts}
                        <option value="__yeni__">+ Yeni Tedarikçi Ekle</option>
                    </select>
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Malzeme *</label>
                    <select id="saMalzeme" onchange="saCesitDegisti()" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                        <option value="">Seçiniz</option>${katalogOpts}
                    </select>
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Miktar *</label>
                    <input id="saMiktar" type="number" step="0.01" min="0" placeholder="ör: 50" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Birim</label>
                    <input id="saBirim" type="text" placeholder="otomatik" readonly style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Birim Fiyat (₺) *</label>
                    <input id="saBirimFiyat" type="number" step="0.01" min="0" placeholder="ör: 27200" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Tarih</label>
                    <input id="saTarih" type="date" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Fatura No</label>
                    <input id="saFaturaNo" type="text" placeholder="ör: FAT-2026-001" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
            </div>
            <div style="margin-top:12px;">
                <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Not</label>
                <input id="saNotlar" type="text" placeholder="ör: Kalite iyi, teslimat hızlı" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
            </div>
            <div id="saHata" style="color:#EF4444;font-size:12px;margin-top:8px;display:none;"></div>
            <div style="display:flex;gap:10px;margin-top:16px;">
                <button onclick="saKaydet()" style="background:#10B981;color:#fff;border:none;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:14px;font-weight:500;">Kaydet</button>
                <button onclick="saFormToggle()" style="background:transparent;color:#64748B;border:1px solid #E2E8F0;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:14px;">İptal</button>
            </div>
        </div>

        <div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
            <select id="saFiltreSantiye" onchange="saFiltreUygula()" style="padding:8px 12px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;">
                <option value="">Tüm Şantiyeler</option>${santiyeOpts}
            </select>
            <select id="saFiltreTedarikci" onchange="saFiltreUygula()" style="padding:8px 12px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;">
                <option value="">Tüm Tedarikçiler</option>${tedarikciOpts}
            </select>
        </div>

        ${kayitlar.length > 0 ? (() => {
            const malzemeGruplari = {};
            const tedarikciGruplari = {};
            kayitlar.forEach(k => {
                const m = k.malzeme_ad || 'Diğer';
                const t = k.tedarikci_ad || 'Belirtilmemiş';
                if (!malzemeGruplari[m]) malzemeGruplari[m] = { toplam: 0, miktar: 0 };
                malzemeGruplari[m].toplam += (k.toplam_tutar || 0);
                malzemeGruplari[m].miktar += (k.miktar || 0);
                if (!tedarikciGruplari[t]) tedarikciGruplari[t] = 0;
                tedarikciGruplari[t] += (k.toplam_tutar || 0);
            });
            const enCokHarcama = Object.entries(malzemeGruplari).sort((a,b) => b[1].toplam - a[1].toplam)[0];
            const enCokTedarikci = Object.entries(tedarikciGruplari).sort((a,b) => b[1] - a[1])[0];
            return `<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-bottom:16px;">
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                    <div style="color:#64748B;font-size:12px;">Toplam Harcama</div>
                    <div style="color:#0F172A;font-size:20px;font-weight:700;margin-top:4px;">?${toplamTutar.toLocaleString('tr-TR')}</div>
                </div>
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                    <div style="color:#64748B;font-size:12px;">Kayıt Sayısı</div>
                    <div style="color:#0F172A;font-size:20px;font-weight:700;margin-top:4px;">${kayitlar.length}</div>
                </div>
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                    <div style="color:#64748B;font-size:12px;">En Çok Harcama</div>
                    <div style="color:#0F172A;font-size:14px;font-weight:600;margin-top:4px;">${enCokHarcama ? enCokHarcama[0] : '-'}</div>
                    <div style="color:#10B981;font-size:12px;">${enCokHarcama ? '?' + enCokHarcama[1].toplam.toLocaleString('tr-TR') : ''}</div>
                </div>
                <div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:16px;box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                    <div style="color:#64748B;font-size:12px;">En Çok Tedarikçi</div>
                    <div style="color:#0F172A;font-size:14px;font-weight:600;margin-top:4px;">${enCokTedarikci ? enCokTedarikci[0] : '-'}</div>
                    <div style="color:#10B981;font-size:12px;">${enCokTedarikci ? '?' + enCokTedarikci[1].toLocaleString('tr-TR') : ''}</div>
                </div>
            </div>`;
        })() : ''}

        <div style="background:#FFFFFF;border:1px solid #E2E8F0;box-shadow:0 1px 3px rgba(0,0,0,0.05);border-radius:12px;overflow:hidden;">
            ${kayitHTML}
        </div>
    `;

    const tarihInput = document.getElementById('saTarih');
    if (tarihInput && !tarihInput.value) tarihInput.value = new Date().toISOString().split('T')[0];
}

function saFormToggle() {
    const f = document.getElementById('saForm');
    if (f) f.style.display = f.style.display === 'none' ? 'block' : 'none';
}

async function saFiltreUygula() {
    const santiyeId = document.getElementById('saFiltreSantiye').value || '';
    const tedarikciId = document.getElementById('saFiltreTedarikci').value || '';
    const token = localStorage.getItem('bai_token');

    let url = '/api/satin-almalar';
    if (santiyeId) url += 'santiye_id=' + santiyeId + '&';
    if (tedarikciId) url += 'tedarikci_id=' + tedarikciId + '&';

    try {
        const r = await fetch(url, {headers: {'Authorization': 'Bearer ' + token}});
        const d = await r.json();
        const kayitlar = d.kayitlar || [];

        const toplamTutar = kayitlar.reduce((t, k) => t + (k.toplam_tutar || 0), 0);

        const ozet = document.querySelector('#satinAlmaTab .sa-ozet');
        if (ozet) ozet.textContent = kayitlar.length + ' kayıt ?? Toplam ?' + toplamTutar.toLocaleString('tr-TR');

        const tbody = document.querySelector('#satinAlmaTab tbody');
        if (tbody) {
            if (kayitlar.length === 0) {
                tbody.innerHTML = '<tr><td colspan="9" style="text-align:center;color:#94A3B8;padding:40px;">Kayıt bulunamadı</td></tr>';
            } else {
                tbody.innerHTML = kayitlar.map(k => {
                    const tarih = k.tarih ? new Date(k.tarih).toLocaleDateString('tr-TR') : '-';
                    return `<tr style="border-bottom:1px solid #F1F5F9;color:#334155;">
                        <td style="padding:10px;">${tarih}</td>
                        <td style="padding:10px;">${k.santiye_ad || '-'}</td>
                        <td style="padding:10px;">${k.tedarikci_ad || '-'}</td>
                        <td style="padding:10px;">${k.malzeme_ad || '-'}</td>
                        <td style="padding:10px;">${k.miktar} ${k.birim || ''}</td>
                        <td style="padding:10px;">?${k.birim_fiyat.toLocaleString('tr-TR') || '-'}</td>
                        <td style="padding:10px;font-weight:600;color:#10B981;">?${k.toplam_tutar.toLocaleString('tr-TR') || '-'}</td>
                        <td style="padding:10px;">${k.fatura_no || '-'}</td>
                        <td style="padding:10px;"><button onclick="satinAlmaSil(${k.id})" style="background:none;border:none;color:#EF4444;cursor:pointer;" title="Sil">🗑¸</button></td>
                    </tr>`;
                }).join('');
            }
        }
    } catch(e) { console.error('Filtre hatası:', e); }
}

function saCesitDegisti() {
    const sel = document.getElementById('saMalzeme');
    const opt = sel.options[sel.selectedIndex];
    const birim = opt.getAttribute('data-birim') || '';
    const bi = document.getElementById('saBirim');
    if (bi && birim) bi.value = birim;
}

async function saKaydet() {
    const hata = document.getElementById('saHata');
    if (hata) hata.style.display = 'none';

    const malzeme = document.getElementById('saMalzeme').value;
    const miktar = document.getElementById('saMiktar').value;
    const birimFiyat = document.getElementById('saBirimFiyat').value;

    if (!malzeme || !miktar || !birimFiyat) {
        if (hata) { hata.textContent = 'Malzeme, miktar ve birim fiyat zorunludur'; hata.style.display = 'block'; }
        return;
    }

    let tedarikciId = document.getElementById('saTedarikci').value || '';
    if (tedarikciId === '__yeni__') {
        const ad = prompt('Tedarikçi adını girin:');
        if (!ad) return;
        try {
            const token = localStorage.getItem('bai_token');
            const r = await fetch('/api/tedarikci-ekle', {
                method: 'POST', headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
                body: JSON.stringify({ad})
            });
            const d = await r.json();
            if (d.status === 'success') tedarikciId = d.tedarikci.id;
            else { if (hata) { hata.textContent = 'Tedarikçi eklenemedi'; hata.style.display = 'block'; } return; }
        } catch(e) { if (hata) { hata.textContent = 'Bağlantı hatası'; hata.style.display = 'block'; } return; }
    }

    const payload = {
        santiye_id: document.getElementById('saShantiye').value || null,
        tedarikci_id: tedarikciId || null,
        cesit_id: malzeme,
        miktar: parseFloat(miktar),
        birim: document.getElementById('saBirim').value || '',
        birim_fiyat: parseFloat(birimFiyat),
        tarih: document.getElementById('saTarih').value || null,
        fatura_no: document.getElementById('saFaturaNo').value || '',
        notlar: document.getElementById('saNotlar').value || ''
    };

    try {
        const token = localStorage.getItem('bai_token');
        const r = await fetch('/api/satin-alma-ekle', {
            method: 'POST', headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const d = await r.json();
        if (d.status === 'success') satinAlmaTabYukle();
        else { if (hata) { hata.textContent = d.detail || 'Hata oluştu'; hata.style.display = 'block'; } }
    } catch(e) { if (hata) { hata.textContent = 'Bağlantı hatası'; hata.style.display = 'block'; } }
}

async function satinAlmaSil(id) {
    if (!confirm('Bu kaydı silmek istediğinize emin misiniz')) return;
    try {
        const token = localStorage.getItem('bai_token');
        await fetch('/api/satin-alma-sil', {
            method: 'POST', headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
            body: JSON.stringify({id})
        });
        satinAlmaTabYukle();
    } catch(e) {}
}

function faturaUploadAc() {
    let modal = document.getElementById('faturaUploadModal');
    if (modal) { modal.remove(); return; }

    const overlay = document.createElement('div');
    overlay.id = 'faturaUploadModal';
    overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.3);z-index:9999;display:flex;align-items:center;justify-content:center;';
    overlay.onclick = function(e) { if (e.target === overlay) overlay.remove(); };

    overlay.innerHTML = `
        <div style="background:#FFFFFF;border-radius:16px;padding:24px;width:600px;max-width:90vw;border:1px solid #E2E8F0;box-shadow:0 20px 60px rgba(0,0,0,0.15);max-height:80vh;overflow-y:auto;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;">
                <h3 style="margin:0;color:#0F172A;font-size:16px;">Fatura ile Otomatik Kayıt</h3>
                <button onclick="document.getElementById('faturaUploadModal').remove()" style="background:none;border:none;color:#64748B;font-size:20px;cursor:pointer;">&times;</button>
            </div>
            <p style="color:#64748B;font-size:13px;margin-bottom:16px;">Fatura veya teklif belgesini yükleyin. AI otomatik olarak malzeme satırlarını, tedarikçi bilgisini ve fiyatları çıkaracak.</p>
            <div id="faturaDropZone" style="border:2px dashed #E2E8F0;border-radius:12px;padding:40px;text-align:center;cursor:pointer;transition:border-color 0.2s;" onclick="document.getElementById('faturaFileInput').click()">
                <input type="file" id="faturaFileInput" accept="image/jpeg,image/png,image/webp,application/pdf" style="display:none" onchange="faturaYukle(this)">
                <div style="font-size:32px;margin-bottom:8px;">🏗</div>
                <div style="color:#64748B;font-size:14px;">Fatura fotoğrafını veya PDF'ini sürükleyin veya tıklayın</div>
                <div style="color:#94A3B8;font-size:12px;margin-top:4px;">JPEG, PNG, WebP, PDF ?? Max 10MB</div>
            </div>
            <div id="faturaParseProgress" style="display:none;text-align:center;padding:20px;">
                <div style="color:#6366F1;font-size:14px;">â³ AI faturayı analiz ediyor...</div>
            </div>
            <div id="faturaParseResult" style="display:none;margin-top:16px;"></div>
        </div>
    `;
    document.body.appendChild(overlay);
}

async function faturaYukle(input) {
    const file = input.files[0];
    if (!file) return;

    const progress = document.getElementById('faturaParseProgress');
    const result = document.getElementById('faturaParseResult');
    const dropZone = document.getElementById('faturaDropZone');

    if (dropZone) dropZone.style.display = 'none';
    if (progress) progress.style.display = 'block';
    if (result) result.style.display = 'none';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const token = localStorage.getItem('bai_token');
        const r = await fetch('/api/fatura-yukle', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + token },
            body: formData
        });
        const d = await r.json();

        if (progress) progress.style.display = 'none';

        if (d.status === 'success' && d.parse_sonucu && d.parse_durumu === 'parsed') {
            faturaParseGoster(d.parse_sonucu);
        } else {
            if (result) {
                result.style.display = 'block';
                result.innerHTML = '<div style="color:#EF4444;padding:16px;background:#FEF2F2;border-radius:8px;">Fatura okunamadı. Lütfen manuel giriş yapın.</div>';
            }
            if (dropZone) dropZone.style.display = 'block';
        }
    } catch(e) {
        if (progress) progress.style.display = 'none';
        if (dropZone) dropZone.style.display = 'block';
        console.error('Fatura yükleme hatası:', e);
    }
    input.value = '';
}

function faturaParseGoster(data) {
    const result = document.getElementById('faturaParseResult');
    if (!result) return;

    const satirlar = data.satirlar || [];
    const tedarikci = data.tedarikci_ad || '';
    const faturaNo = data.fatura_no || '';
    const tarih = data.tarih || new Date().toISOString().split('T')[0];

    const satirHTML = satirlar.map((s, i) => `
        <tr style="border-bottom:1px solid #F1F5F9;">
            <td style="padding:8px;"><input type="checkbox" checked data-index="${i}" class="fatura-satir-check"></td>
            <td style="padding:8px;"><input type="text" value="${s.malzeme_ad || ''}" style="width:100%;padding:4px;border:1px solid #E2E8F0;border-radius:4px;font-size:12px;" data-field="malzeme_ad"></td>
            <td style="padding:8px;"><input type="number" value="${s.miktar || 0}" style="width:80px;padding:4px;border:1px solid #E2E8F0;border-radius:4px;font-size:12px;" data-field="miktar"></td>
            <td style="padding:8px;"><input type="text" value="${s.birim || ''}" style="width:60px;padding:4px;border:1px solid #E2E8F0;border-radius:4px;font-size:12px;" data-field="birim"></td>
            <td style="padding:8px;"><input type="number" value="${s.birim_fiyat || 0}" style="width:100px;padding:4px;border:1px solid #E2E8F0;border-radius:4px;font-size:12px;" data-field="birim_fiyat"></td>
            <td style="padding:8px;font-weight:600;color:#10B981;">?${((s.miktar || 0) * (s.birim_fiyat || 0)).toLocaleString('tr-TR')}</td>
        </tr>
    `).join('');

    result.style.display = 'block';
    result.innerHTML = `
        <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;padding:12px;margin-bottom:12px;color:#166534;font-size:13px;">
            ? Fatura başarıyla okundu! Aşağıdaki bilgileri kontrol edip onaylayın.
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:12px;">
            <div>
                <label style="font-size:11px;color:#64748B;">Tedarikçi</label>
                <input id="faturaTed" type="text" value="${tedarikci}" style="width:100%;padding:6px;border:1px solid #E2E8F0;border-radius:6px;font-size:13px;box-sizing:border-box;">
            </div>
            <div>
                <label style="font-size:11px;color:#64748B;">Fatura No</label>
                <input id="faturaNo" type="text" value="${faturaNo}" style="width:100%;padding:6px;border:1px solid #E2E8F0;border-radius:6px;font-size:13px;box-sizing:border-box;">
            </div>
            <div>
                <label style="font-size:11px;color:#64748B;">Tarih</label>
                <input id="faturaTarih" type="date" value="${tarih}" style="width:100%;padding:6px;border:1px solid #E2E8F0;border-radius:6px;font-size:13px;box-sizing:border-box;">
            </div>
        </div>
        <div style="overflow-x:auto;">
            <table style="width:100%;border-collapse:collapse;font-size:13px;">
                <thead><tr style="border-bottom:2px solid #E2E8F0;color:#64748B;">
                    <th style="padding:8px;width:30px;">?</th><th style="padding:8px;text-align:left;">Malzeme</th>
                    <th style="padding:8px;">Miktar</th><th style="padding:8px;">Birim</th>
                    <th style="padding:8px;">Birim Fiyat</th><th style="padding:8px;">Toplam</th>
                </tr></thead>
                <tbody>${satirHTML}</tbody>
            </table>
        </div>
        <div style="display:flex;gap:10px;margin-top:16px;">
            <button onclick="faturaKayitlariOnayla()" style="background:#10B981;color:#fff;border:none;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:14px;font-weight:500;">Seçilenleri Kaydet</button>
            <button onclick="document.getElementById('faturaUploadModal').remove()" style="background:transparent;color:#64748B;border:1px solid #E2E8F0;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:14px;">İptal</button>
        </div>
    `;
}

async function faturaKayitlariOnayla() {
    const token = localStorage.getItem('bai_token');
    const tedarikciAd = document.getElementById('faturaTed').value.trim() || '';
    const faturaNo = document.getElementById('faturaNo').value.trim() || '';
    const tarih = document.getElementById('faturaTarih').value || '';

    let tedarikciId = null;
    if (tedarikciAd) {
        try {
            const r = await fetch('/api/tedarikci-ekle', {
                method: 'POST',
                headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
                body: JSON.stringify({ad: tedarikciAd})
            });
            const d = await r.json();
            if (d.status === 'success') tedarikciId = d.tedarikci.id;
        } catch(e) {}
    }

    const checkboxes = document.querySelectorAll('.fatura-satir-check:checked');
    let basarili = 0;

    for (const cb of checkboxes) {
        const row = cb.closest('tr');
        const malzemeAd = row.querySelector('[data-field="malzeme_ad"]').value || '';
        const miktar = parseFloat(row.querySelector('[data-field="miktar"]').value) || 0;
        const birim = row.querySelector('[data-field="birim"]').value || '';
        const birimFiyat = parseFloat(row.querySelector('[data-field="birim_fiyat"]').value) || 0;

        if (!malzemeAd || !miktar || !birimFiyat) continue;

        const santiyeId = window._aktifSantiyeId || null;

        try {
            const r = await fetch('/api/satin-alma-ekle', {
                method: 'POST',
                headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
                body: JSON.stringify({
                    santiye_id: santiyeId,
                    tedarikci_id: tedarikciId,
                    malzeme_ad: malzemeAd,
                    miktar, birim, birim_fiyat: birimFiyat,
                    fatura_no: faturaNo,
                    tarih: tarih,
                    notlar: 'Fatura ile otomatik eklendi'
                })
            });
            const d = await r.json();
            if (d.status === 'success') basarili++;
        } catch(e) {}
    }

    document.getElementById('faturaUploadModal').remove();
    if (basarili > 0 && typeof satinAlmaTabYukle === 'function') satinAlmaTabYukle();
}

async function tedarikciTabYukle() {
    const container = document.getElementById('tedarikciTab');
    if (!container) return;
    container.innerHTML = '<div style="text-align:center;padding:40px;color:#64748B;">Yükleniyor...</div>';

    const token = localStorage.getItem('bai_token');
    let tedarikciler = [];
    try {
        const r = await fetch('/api/tedarikciler', {headers: {'Authorization': 'Bearer ' + token}});
        const d = await r.json();
        tedarikciler = d.tedarikciler || [];
    } catch(e) {}

    let satinAlmalar = [];
    try {
        const saR = await fetch('/api/satin-almalar', {headers: {'Authorization': 'Bearer ' + token}});
        const saD = await saR.json();
        satinAlmalar = saD.kayitlar || [];
    } catch(e) {}

    let listHTML = '';
    if (tedarikciler.length === 0) {
        listHTML = '<div style="text-align:center;color:#64748B;padding:40px;font-size:14px;">Henüz tedarikçi eklenmemiş</div>';
    } else {
        listHTML = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;">';
        tedarikciler.forEach(t => {
            const tSatinAlmalar = satinAlmalar.filter(s => s.tedarikci_id === t.id);
            const tToplam = tSatinAlmalar.reduce((acc, s) => acc + (s.toplam_tutar || 0), 0);
            const ozet = tSatinAlmalar.length > 0
                 ? `<div style="margin-top:8px;padding-top:8px;border-top:1px solid #F1F5F9;display:flex;justify-content:space-between;align-items:center;">
                       <span style="color:#64748B;font-size:12px;">${tSatinAlmalar.length} alım</span>
                       <span style="color:#10B981;font-size:12px;font-weight:600;">?${tToplam.toLocaleString('tr-TR', {minimumFractionDigits:2, maximumFractionDigits:2})}</span>
                   </div>`
                : '';
            listHTML += `<div style="background:#FFFFFF;border:1px solid #E2E8F0;box-shadow:0 1px 3px rgba(0,0,0,0.05);border-radius:12px;padding:16px;">
                <div style="display:flex;justify-content:space-between;align-items:start;">
                    <div>
                        <h4 style="margin:0 0 4px;color:#0F172A;font-size:15px;">${t.ad}</h4>
                        <p style="margin:0;color:#334155;font-size:12px;">${t.sehir || ''}</p>
                    </div>
                    <button onclick="tedarikciSilBtn(${t.id})" style="background:none;border:none;color:#EF4444;cursor:pointer;" title="Sil">🗑¸</button>
                </div>
                ${t.yetkili_kisi ? '<div style="margin-top:8px;color:#334155;font-size:13px;">👁¤ ' + t.yetkili_kisi + '</div>' : ''}
                ${t.telefon ? '<div style="color:#334155;font-size:13px;">🏠 ' + t.telefon + '</div>' : ''}
                ${t.email ? '<div style="color:#334155;font-size:13px;">âœ‰ï¸ ' + t.email + '</div>' : ''}
                ${t.vergi_no ? '<div style="color:#64748B;font-size:11px;margin-top:4px;">VKN: ' + t.vergi_no + '</div>' : ''}
                ${ozet}
            </div>`;
        });
        listHTML += '</div>';
    }

    container.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:10px;padding-top:10px;">
            <div>
                <h2 style="margin:0;color:#0F172A;font-size:20px;font-weight:600;">Tedarikçi Yönetimi</h2>
                <p style="margin:4px 0 0;color:#64748B;font-size:13px;">${tedarikciler.length} tedarikçi kayıtlı</p>
            </div>
            <button onclick="tfFormToggle()" style="background:linear-gradient(135deg,#6366F1,#8B5CF6);color:#fff;border:none;padding:10px 20px;border-radius:10px;cursor:pointer;font-size:14px;font-weight:500;">
                + Yeni Tedarikçi
            </button>
        </div>

        <div id="tfForm" style="display:none;background:#FFFFFF;border:1px solid #E2E8F0;box-shadow:0 1px 3px rgba(0,0,0,0.05);border-radius:12px;padding:20px;margin-bottom:20px;">
            <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;">
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Firma Adı *</label>
                    <input id="tfAd" type="text" placeholder="ör: ABC Demir Ltd." style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Yetkili Kişi</label>
                    <input id="tfYetkili" type="text" placeholder="ör: Ahmet Yılmaz" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Telefon</label>
                    <input id="tfTelefon" type="text" placeholder="ör: 0532 xxx xx xx" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">E-posta</label>
                    <input id="tfEmail" type="email" placeholder="ör: info@abc.com" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Şehir</label>
                    <input id="tfSehir" type="text" placeholder="ör: İstanbul" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
                <div>
                    <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Vergi No</label>
                    <input id="tfVergiNo" type="text" placeholder="ör: 1234567890" style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
                </div>
            </div>
            <div style="margin-top:12px;">
                <label style="font-size:12px;color:#64748B;display:block;margin-bottom:4px;">Adres</label>
                <input id="tfAdres" type="text" placeholder="ör: Organize Sanayi Bölgesi..." style="width:100%;padding:8px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;color:#0F172A;font-size:13px;box-sizing:border-box;">
            </div>
            <div id="tfHata" style="color:#EF4444;font-size:12px;margin-top:8px;display:none;"></div>
            <div style="display:flex;gap:10px;margin-top:16px;">
                <button onclick="tfKaydet()" style="background:#10B981;color:#fff;border:none;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:14px;font-weight:500;">Kaydet</button>
                <button onclick="tfFormToggle()" style="background:transparent;color:#64748B;border:1px solid #E2E8F0;padding:10px 24px;border-radius:8px;cursor:pointer;font-size:14px;">İptal</button>
            </div>
        </div>

        ${listHTML}
    `;
}

function tfFormToggle() {
    const f = document.getElementById('tfForm');
    if (f) f.style.display = f.style.display === 'none' ? 'block' : 'none';
}

async function tfKaydet() {
    const hata = document.getElementById('tfHata');
    if (hata) hata.style.display = 'none';

    const ad = document.getElementById('tfAd').value.trim();
    if (!ad) { if (hata) { hata.textContent = 'Firma adı zorunludur'; hata.style.display = 'block'; } return; }

    const payload = {
        ad,
        yetkili_kisi: document.getElementById('tfYetkili').value.trim() || '',
        telefon: document.getElementById('tfTelefon').value.trim() || '',
        email: document.getElementById('tfEmail').value.trim() || '',
        sehir: document.getElementById('tfSehir').value.trim() || '',
        vergi_no: document.getElementById('tfVergiNo').value.trim() || '',
        adres: document.getElementById('tfAdres').value.trim() || ''
    };

    try {
        const token = localStorage.getItem('bai_token');
        const r = await fetch('/api/tedarikci-ekle', {
            method: 'POST', headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const d = await r.json();
        if (d.status === 'success') tedarikciTabYukle();
        else { if (hata) { hata.textContent = d.detail || 'Hata oluştu'; hata.style.display = 'block'; } }
    } catch(e) { if (hata) { hata.textContent = 'Bağlantı hatası'; hata.style.display = 'block'; } }
}

async function tedarikciSilBtn(id) {
    if (!confirm('Bu tedarikçiyi silmek istediğinize emin misiniz')) return;
    try {
        const token = localStorage.getItem('bai_token');
        await fetch('/api/tedarikci-sil', {
            method: 'POST', headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
            body: JSON.stringify({id})
        });
        tedarikciTabYukle();
    } catch(e) {}
}

// ── HAKEDİŞ MODÜLÜ ────────────────────────────────────────────────────────────

function _metrajOzetKurus(kurus) {
    const tl = (kurus || 0) / 100;
    return tl.toLocaleString('tr-TR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' ₺';
}

function _metrajOzetYuzde(yuzde) {
    return (Number(yuzde || 0)).toLocaleString('tr-TR', {maximumFractionDigits: 1}) + '%';
}

function _metrajOzetKartHtml(label, value, subText) {
    return '<div class="metraj-ozet-card">' +
        '<div class="metraj-ozet-label">' + label + '</div>' +
        '<div class="metraj-ozet-value">' + value + '</div>' +
        '<div class="metraj-ozet-sub">' + subText + '</div>' +
        '</div>';
}

function _metrajOzetKartlariGoster(data) {
    const page = document.getElementById('hiyerarsiPage');
    const layout = page ? page.querySelector('.hiy-layout') : null;
    if (!page || !layout) return;
    let box = document.getElementById('metrajOzetKartlari');
    if (!box) {
        box = document.createElement('div');
        box.id = 'metrajOzetKartlari';
        box.className = 'metraj-ozet-wrap';
        layout.parentNode.insertBefore(box, layout);
    }
    const ilerleme = Math.max(0, Math.min(100, Number(data.genel_ilerleme || 0)));
    const sonText = data.son_hakedis_no
         ? 'Son Hakediş: #' + data.son_hakedis_no + ' — ' + _metrajOzetKurus(data.son_hakedis_tutar)
        : 'Son Hakediş: Henüz yok';
    box.innerHTML = [
        '<div class="metraj-ozet-grid">',
        _metrajOzetKartHtml('Toplam Bütçe', _metrajOzetKurus(data.toplam_butce), sonText),
        _metrajOzetKartHtml('Hakediş Toplamı', _metrajOzetKurus(data.toplam_hakedis), sonText),
        _metrajOzetKartHtml('Kalan Bütçe', _metrajOzetKurus(data.kalan_butce), sonText),
        '<div class="metraj-ozet-card">',
        '  <div class="metraj-ozet-label">Genel İlerleme</div>',
        '  <div class="metraj-ozet-value">' + _metrajOzetYuzde(ilerleme) + '</div>',
        '  <div class="metraj-ozet-progress"><span style="width:' + ilerleme + '%"></span></div>',
        '  <div class="metraj-ozet-sub">' + sonText + '</div>',
        '</div>',
        '</div>'
    ].join('');
}

async function metrajOzetYukle(santiyeId) {
    santiyeId = santiyeId || window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
    if (!santiyeId) return;
    const epoch = window._baiProjectEpoch || 0;
    const page = document.getElementById('hiyerarsiPage');
    const layout = page ? page.querySelector('.hiy-layout') : null;
    if (!page || !layout) return;
    let box = document.getElementById('metrajOzetKartlari');
    if (!box) {
        box = document.createElement('div');
        box.id = 'metrajOzetKartlari';
        box.className = 'metraj-ozet-wrap';
        layout.parentNode.insertBefore(box, layout);
    }
    box.innerHTML = '<div class="metraj-ozet-loading">Özet yükleniyor...</div>';
    try {
        const token = localStorage.getItem('bai_token') || '';
        const r = await fetch('/api/metraj/ozet/' + santiyeId + '?token=' + encodeURIComponent(token), {
            headers: {'Authorization': 'Bearer ' + token}
        });
        if (!r.ok) throw new Error(r.status);
        const data = await r.json();
        if (epoch !== (window._baiProjectEpoch || 0) || String(santiyeId) !== String(localStorage.getItem('bai_aktif_santiye'))) return;
        _metrajOzetKartlariGoster(data);
    } catch (e) {
        box.innerHTML = '<div class="metraj-ozet-loading error">Metraj özeti yüklenemedi</div>';
    }
}

(function metrajOzetEntegrasyonuKur() {
    function kur() {
        if (typeof window.hiyerarsiPageAc !== 'function') {
            setTimeout(kur, 200);
            return;
        }
        if (window.hiyerarsiPageAc._metrajOzetli) return;
        const eskiHiyerarsiPageAc = window.hiyerarsiPageAc;
        window.hiyerarsiPageAc = function() {
            const sonuc = eskiHiyerarsiPageAc.apply(this, arguments);
            setTimeout(function() { metrajOzetYukle(); }, 80);
            return sonuc;
        };
        window.hiyerarsiPageAc._metrajOzetli = true;
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', kur);
    else kur();
}());

let _hakedisAktifId = null;

function _hakedisKurus(kurus) {
    if (!kurus && kurus !== 0) return '—';
    const tl = Number(kurus); // API amounts are TL; persisted amounts are integer kuruş.
    return tl.toLocaleString('tr-TR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' ₺';
}

function _hakedisDurumBadge(durum) {
    const map = {
        taslak:        {label: 'Taslak',        bg: '#F1F5F9', color: '#64748B', border: '#CBD5E1'},
        onay_bekliyor: {label: 'Onay Bekliyor', bg: '#FEF9C3', color: '#92400E', border: '#FDE68A'},
        onaylandi:     {label: 'Onaylandı ✓',   bg: '#DCFCE7', color: '#166534', border: '#86EFAC'},
        reddedildi:    {label: 'Reddedildi',    bg: '#FEE2E2', color: '#991B1B', border: '#FCA5A5'},
    };
    const d = map[durum] || {label: durum, bg: '#F1F5F9', color: '#64748B', border: '#CBD5E1'};
    return `<span style="display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700;background:${d.bg};color:${d.color};border:1px solid ${d.border};">${d.label}</span>`;
}

async function hakedisPdfIndir(hakedisId) {
    try {
        var response = await fetch('/api/hakedis/pdf/' + hakedisId, {
            headers: {'Authorization': 'Bearer ' + (localStorage.getItem('bai_token') || '')}
        });
        if (!response.ok) {
            var err = await response.json().catch(function() { return {}; });
            alert(err.detail || 'PDF indirilemedi');
            return;
        }
        var blob = await response.blob();
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = 'hakedis_' + hakedisId + '.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (e) {
        console.error('PDF indirme hatasi:', e);
        alert('PDF indirilemedi');
    }
}

function hakedisPageAc() {
    if (typeof tumSayfalariGizle === 'function') {
        tumSayfalariGizle();
    } else if (typeof _fpHideAll === 'function') {
        _fpHideAll();
    } else {
        const allPages = ['content','aiCommandBar','santiyePage','fiyatPage','stokPage','kameraPage','arsivPage','hiyerarsiPage','sahaKayitlariPage','gunlukRaporPage','engineerDashboard'];
        allPages.forEach(id => { const el = document.getElementById(id); if (el) el.style.display = 'none'; });
    }
    const pg = document.getElementById('hakedisPage');
    if (pg) pg.style.display = 'flex';
    const titleEl = document.getElementById('contentTitle');
    if (titleEl) titleEl.textContent = 'Hakediş Yönetimi';
    const santiyeAdEl = document.getElementById('hakedisAktifSantiyeAd');
    if (santiyeAdEl) santiyeAdEl.textContent = localStorage.getItem('bai_aktif_santiye_ad') || window._aktifSantiyeAd || '—';
    hakedisSantiyeDoldur();
}

function hakedisPageKapat() {
    const pg = document.getElementById('hakedisPage');
    if (pg) pg.style.display = 'none';
}

function hakedisSantiyeDoldur() {
    hakedisListeYukle();
}

async function hakedisListeYukle() {
    const santiyeId = localStorage.getItem('bai_aktif_santiye') || '';
    const epoch = window._baiProjectEpoch || 0;
    const container = document.getElementById('hakedisListeContainer');
    if (!container) return;
    if (!santiyeId) {
        container.innerHTML = '<div style="color:#94A3B8;font-size:13px;text-align:center;padding:24px 0;">Header\'dan santiye secin</div>';
        return;
    }
    container.innerHTML = '<div style="color:#94A3B8;font-size:13px;text-align:center;padding:24px 0;">Yukleniyor...</div>';
    const token = localStorage.getItem('bai_token');
    try {
        const r = await fetch('/api/hakedis/liste/' + santiyeId + '?token=' + token, {headers: {'Authorization': 'Bearer ' + token}});
        if (!r.ok) throw new Error(r.status);
        const d = await r.json();
        if (epoch !== (window._baiProjectEpoch || 0) || String(santiyeId) !== String(localStorage.getItem('bai_aktif_santiye'))) return;
        const liste = d.hakedisler || [];
        if (!liste.length) {
            container.innerHTML = '<div style="color:#94A3B8;font-size:13px;text-align:center;padding:24px 0;">Henuz hakedis yok</div>';
            return;
        }
        container.innerHTML = liste.map(function(h) {
            return '<div class="hkd-kart" onclick="hakedisDetayAc(' + h.id + ')" data-hkd="' + h.id + '" style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:12px 14px;cursor:pointer;transition:border-color .15s;">' +
                '<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">' +
                '<span style="font-size:13px;font-weight:800;color:#0F172A;">Hakedis #' + h.hakedis_no + '</span>' +
                '<div style="display:flex;align-items:center;gap:6px;">' +
                _hakedisDurumBadge(h.durum) +
                (h.durum === 'taslak' ? '<button onclick="event.stopPropagation();hakedisKartSil(' + h.id + ')" title="Sil" style="background:none;border:none;cursor:pointer;color:#EF4444;font-size:15px;padding:0 2px;line-height:1;">🗑</button>' : '') +
                '</div></div>' +
                '<div style="font-size:11px;color:#64748B;margin-bottom:4px;">' + h.donem_baslangic + ' - ' + h.donem_bitis + '</div>' +
                '<div style="font-size:12px;font-weight:700;color:#0F172A;">' + _hakedisKurus(h.toplam_tutar) + '</div>' +
                '</div>';
        }).join('');
    } catch(e) {
        container.innerHTML = '<div style="color:#EF4444;font-size:13px;text-align:center;padding:24px 0;">Yuklenemedi</div>';
    }
}

async function hakedisDetayAc(hakedisId) {
    const siteAtStart = localStorage.getItem('bai_aktif_santiye');
    const epoch = window._baiProjectEpoch || 0;
    _hakedisAktifId = hakedisId;
    document.querySelectorAll('.hkd-kart').forEach(function(el) {
        el.style.borderColor = el.dataset.hkd == hakedisId ? '#0F172A' : '#E2E8F0';
        el.style.background  = el.dataset.hkd == hakedisId ? '#F8FAFC' : '#fff';
    });
    const panel = document.getElementById('hakedisDetayIcerik');
    if (!panel) return;
    panel.innerHTML = '<div style="color:#94A3B8;font-size:13px;text-align:center;padding:40px 0;">Yukleniyor...</div>';
    if (window.innerWidth < 640) {
        var listPan = document.getElementById('hakedisListPanel');
        var detayPan = document.getElementById('hakedisDetayPanel');
        if (listPan) listPan.style.display = 'none';
        if (detayPan) detayPan.style.display = 'flex';
    }
    const token = localStorage.getItem('bai_token');
    try {
        const r = await fetch('/api/hakedis/detay/' + hakedisId + '?token=' + token, {headers: {'Authorization': 'Bearer ' + token}});
        if (!r.ok) throw new Error(r.status);
        const d = await r.json();
        if (epoch !== (window._baiProjectEpoch || 0) || siteAtStart !== localStorage.getItem('bai_aktif_santiye') || String(d.hakedis.santiye_id) !== String(siteAtStart)) return;
        const capResponse = await fetch('/api/v2/payments/' + hakedisId + '/capabilities', {headers: {'Authorization': 'Bearer ' + token}});
        const cap = capResponse.ok ? await capResponse.json() : {can_review:false, can_submit:false, contract_id:null};
        if (epoch !== (window._baiProjectEpoch || 0)) return;
        panel.innerHTML = _hakedisDetayHTML(d.hakedis, d.kalemler, cap);
        if (cap.contract_id) {
            const proof = await fetch('/api/v2/payments/' + hakedisId + '/allocations', {headers: {'Authorization': 'Bearer ' + token}});
            if (proof.ok && epoch === (window._baiProjectEpoch || 0)) {
                const rows = (await proof.json()).allocations || [];
                const box = document.createElement('section');
                box.style.cssText = 'background:#fff;border:1px solid #e2e8f0;border-radius:10px;padding:16px;margin-top:16px';
                box.innerHTML = '<h3 style="margin:0 0 10px">Ölçüm dayanakları</h3>' + rows.map(a => `<p>Ölçüm #${a.measurement.id} · ${_hakedisEscape(a.quantity)} ${_hakedisEscape(a.measurement.unit)} · ${_hakedisEscape(a.amount)} ₺<br>${_hakedisEscape(a.measurement.basis || 'Dayanak belirtilmedi')} · Belge kayıtları: ${_hakedisEscape((a.measurement.evidence_ids || []).join(', ') || 'Yok')}</p>`).join('');
                panel.appendChild(box);
            }
        }
        if (window.innerWidth < 640) {
            var btn = document.getElementById('hakedisGeriBtn');
            if (btn) btn.style.display = 'inline-block';
        }
    } catch(e) {
        panel.innerHTML = '<div style="color:#EF4444;font-size:13px;text-align:center;padding:40px 0;">Yuklenemedi</div>';
    }
}

function _hakedisEscape(value) {
    return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function _hakedisDetayHTML(h, kalemler, cap = {}) {
    var isDraft = h.durum === 'taslak' && !cap.contract_id;
    var durumBtnHtml = '';
    var pdfBtnHtml = (h.durum === 'onaylandi' || h.durum === 'onay_bekliyor')
         ? '<button onclick="hakedisPdfIndir(' + h.id + ')" style="background:#FFFFFF;color:#0F172A;border:1px solid #CBD5E1;border-radius:8px;padding:8px 14px;font-size:12px;font-weight:700;cursor:pointer;">PDF İndir</button>'
        : '';
    if (h.durum === 'taslak' && cap.can_submit) {
        durumBtnHtml = '<button onclick="hakedisDurumGuncelle(' + h.id + ',\'onay_bekliyor\')" style="background:#0F172A;color:#fff;border:none;border-radius:8px;padding:8px 16px;font-size:12px;font-weight:700;cursor:pointer;">Onaya Gonder</button>';
    } else if (h.durum === 'onay_bekliyor' && cap.can_review) {
        durumBtnHtml =
            '<button onclick="hakedisDurumGuncelle(' + h.id + ',\'onaylandi\')" style="background:#16A34A;color:#fff;border:none;border-radius:8px;padding:8px 14px;font-size:12px;font-weight:700;cursor:pointer;">İç kayıt onayı</button>' +
            '<button onclick="hakedisDurumGuncelle(' + h.id + ',\'reddedildi\')" style="background:#DC2626;color:#fff;border:none;border-radius:8px;padding:8px 14px;font-size:12px;font-weight:700;cursor:pointer;">Geri gönder</button>';
    } else if (h.durum === 'onay_bekliyor' && cap.can_submit) {
        durumBtnHtml = '<button onclick="hakedisDurumGuncelle(' + h.id + ',\'taslak\')">Geri çek</button>';
    } else if (h.durum === 'reddedildi' && cap.can_submit) {
        durumBtnHtml = '<button onclick="hakedisDurumGuncelle(' + h.id + ',\'taslak\')" style="background:#F1F5F9;color:#64748B;border:1px solid #E2E8F0;border-radius:8px;padding:8px 14px;font-size:12px;font-weight:600;cursor:pointer;">Taslaga Cek</button>';
    } else if (h.durum === 'onaylandi') {
        durumBtnHtml = '<span style="color:#16A34A;font-size:13px;font-weight:700;">Onaylandi</span>';
    }

    var satirlar = kalemler.map(function(k) {
        return '<tr data-kalem-id="' + k.id + '" style="border-bottom:1px solid #F1F5F9;">' +
            '<td style="padding:8px 10px;font-size:12px;color:#64748B;white-space:nowrap;">' + _hakedisEscape(k.poz_no || '-') + '</td>' +
            '<td style="padding:8px 10px;font-size:12px;color:#0F172A;min-width:140px;">' + _hakedisEscape(k.tanim) + '</td>' +
            '<td style="padding:8px 10px;font-size:12px;color:#64748B;text-align:center;">' + _hakedisEscape(k.birim) + '</td>' +
            '<td style="padding:8px 10px;font-size:12px;color:#0F172A;text-align:right;">' + (k.sozlesme_metraj||0).toLocaleString('tr-TR',{maximumFractionDigits:3}) + '</td>' +
            '<td style="padding:8px 10px;font-size:12px;color:#64748B;text-align:right;">' + (k.onceki_toplam_miktar||0).toLocaleString('tr-TR',{maximumFractionDigits:3}) + '</td>' +
            '<td style="padding:8px 10px;text-align:right;" class="hkd-bu-donem-cell">' +
            (isDraft
                 ? '<input type="number" step="0.001" min="0" value="' + (k.bu_donem_miktar||0) + '" onblur="hakedisKalemGuncelle(' + k.id + ',this)" style="width:80px;padding:5px 7px;border:1px solid #CBD5E1;border-radius:6px;font-size:12px;text-align:right;">'
                : '<span style="font-size:12px;color:#0F172A;">' + (k.bu_donem_miktar||0).toLocaleString('tr-TR',{maximumFractionDigits:3}) + '</span>'
            ) +
            '</td>' +
            '<td style="padding:8px 10px;font-size:12px;color:#0F172A;text-align:right;" class="hkd-kumulatif-miktar">' + (k.kumulatif_miktar||0).toLocaleString('tr-TR',{maximumFractionDigits:3}) + '</td>' +
            '<td style="padding:8px 10px;font-size:12px;color:#64748B;text-align:right;">' + _hakedisKurus(k.birim_fiyat) + '</td>' +
            '<td style="padding:8px 10px;font-size:12px;font-weight:700;color:#0F172A;text-align:right;" class="hkd-bu-donem-tutar">' + _hakedisKurus(k.bu_donem_tutar) + '</td>' +
            '<td style="padding:8px 10px;font-size:12px;font-weight:700;color:#0F172A;text-align:right;" class="hkd-kumulatif-tutar">' + _hakedisKurus(k.kumulatif_tutar) + '</td>' +
            '</tr>';
    }).join('');

    var buDonemToplam  = kalemler.reduce(function(s,k){ return s + (k.bu_donem_tutar||0); }, 0);
    var kumulatifToplam = kalemler.reduce(function(s,k){ return s + (k.kumulatif_tutar||0); }, 0);

    return '<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:16px;">' +
        '<div>' +
        '<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">' +
        '<span style="font-size:16px;font-weight:800;color:#0F172A;">Hakedis #' + h.hakedis_no + '</span>' +
        _hakedisDurumBadge(h.durum) +
        '<button id="hakedisGeriBtn" onclick="hakedisGeriDon()" style="display:none;background:none;border:none;cursor:pointer;color:#64748B;font-size:20px;padding:0;" title="Listeye Don">&#8592;</button>' +
        '</div>' +
        '<div style="font-size:12px;color:#64748B;">Donem: ' + h.donem_baslangic + ' - ' + h.donem_bitis + '</div>' +
        (h.hazirlayan ? '<div style="font-size:12px;color:#94A3B8;">Hazirlayan: ' + h.hazirlayan + '</div>' : '') +
        (h.onaylayan ? '<div style="font-size:12px;color:#94A3B8;">Onaylayan: ' + h.onaylayan + '</div>' : '') +
        '</div>' +
        '<div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">' + pdfBtnHtml + durumBtnHtml + '</div>' +
        '</div>' +
        '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px;">' +
        '<div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">' +
        '<div style="font-size:11px;color:#94A3B8;font-weight:600;margin-bottom:4px;">Onceki Hakedisler</div>' +
        '<div style="font-size:15px;font-weight:800;color:#0F172A;">' + _hakedisKurus(h.onceki_toplam) + '</div>' +
        '</div>' +
        '<div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;padding:12px 18px;flex:1;min-width:140px;">' +
        '<div style="font-size:11px;color:#94A3B8;font-weight:600;margin-bottom:4px;">Bu Donem Toplam</div>' +
        '<div id="hkd-toplam-goster" style="font-size:15px;font-weight:800;color:#0F172A;">' + _hakedisKurus(h.toplam_tutar) + '</div>' +
        '</div>' +
        '</div>' +
        '<div style="background:#fff;border:1px solid #E2E8F0;border-radius:12px;overflow:hidden;">' +
        '<div style="overflow-x:auto;">' +
        '<table id="hakedisKalemTable" style="width:100%;border-collapse:collapse;font-size:12px;">' +
        '<thead><tr style="background:#F8FAFC;border-bottom:2px solid #E2E8F0;">' +
        '<th style="padding:10px;text-align:left;font-size:11px;font-weight:700;color:#64748B;white-space:nowrap;">Poz No</th>' +
        '<th style="padding:10px;text-align:left;font-size:11px;font-weight:700;color:#64748B;">Tanim</th>' +
        '<th style="padding:10px;text-align:center;font-size:11px;font-weight:700;color:#64748B;">Birim</th>' +
        '<th style="padding:10px;text-align:right;font-size:11px;font-weight:700;color:#64748B;white-space:nowrap;">Sozlesme Metraj</th>' +
        '<th style="padding:10px;text-align:right;font-size:11px;font-weight:700;color:#64748B;white-space:nowrap;">Onceki Toplam</th>' +
        '<th style="padding:10px;text-align:right;font-size:11px;font-weight:700;color:#0F172A;white-space:nowrap;">Bu Donem</th>' +
        '<th style="padding:10px;text-align:right;font-size:11px;font-weight:700;color:#64748B;white-space:nowrap;">Kumulatif</th>' +
        '<th style="padding:10px;text-align:right;font-size:11px;font-weight:700;color:#64748B;white-space:nowrap;">Birim Fiyat</th>' +
        '<th style="padding:10px;text-align:right;font-size:11px;font-weight:700;color:#0F172A;white-space:nowrap;">Bu Donem Tutar</th>' +
        '<th style="padding:10px;text-align:right;font-size:11px;font-weight:700;color:#64748B;white-space:nowrap;">Kumulatif Tutar</th>' +
        '</tr></thead>' +
        '<tbody id="hakedisKalemBody">' + satirlar + '</tbody>' +
        '<tfoot><tr style="background:#F8FAFC;border-top:2px solid #E2E8F0;">' +
        '<td colspan="8" style="padding:10px;font-size:12px;font-weight:700;color:#0F172A;">TOPLAM</td>' +
        '<td id="hkd-foot-bu-donem" style="padding:10px;font-size:12px;font-weight:800;color:#0F172A;text-align:right;">' + _hakedisKurus(buDonemToplam) + '</td>' +
        '<td id="hkd-foot-kumulatif" style="padding:10px;font-size:12px;font-weight:800;color:#0F172A;text-align:right;">' + _hakedisKurus(kumulatifToplam) + '</td>' +
        '</tr></tfoot>' +
        '</table></div></div>';
}

function hakedisGeriDon() {
    var listPan  = document.getElementById('hakedisListPanel');
    var detayPan = document.getElementById('hakedisDetayPanel');
    if (listPan) listPan.style.display = 'flex';
    if (detayPan) detayPan.style.display = window.innerWidth >= 640 ? 'flex' : 'none';
    _hakedisAktifId = null;
    var panel = document.getElementById('hakedisDetayIcerik');
    if (panel) panel.innerHTML = '<div style="color:#94A3B8;font-size:14px;text-align:center;padding:60px 0;">Listeden bir hakedis secin</div>';
}

async function hakedisKalemGuncelle(kalemId, inputEl) {
    var buDonemMiktar = parseFloat(inputEl.value) || 0;
    var token = localStorage.getItem('bai_token');
    try {
        var r = await fetch('/api/hakedis/kalem-guncelle', {
            method: 'PATCH',
            headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
            body: JSON.stringify({hakedis_kalem_id: kalemId, bu_donem_miktar: buDonemMiktar})
        });
        if (!r.ok) { var e = await r.json(); alert(e.detail || 'Guncelleme hatasi'); return; }
        var d = await r.json();
        var k = d.kalem;
        var row = document.querySelector('tr[data-kalem-id="' + kalemId + '"]');
        if (row) {
            var km = row.querySelector('.hkd-kumulatif-miktar');
            if (km) km.textContent = (k.kumulatif_miktar||0).toLocaleString('tr-TR',{maximumFractionDigits:3});
            var bdt = row.querySelector('.hkd-bu-donem-tutar');
            if (bdt) bdt.textContent = _hakedisKurus(k.bu_donem_tutar);
            var kt = row.querySelector('.hkd-kumulatif-tutar');
            if (kt) kt.textContent = _hakedisKurus(k.kumulatif_tutar);
        }
        _hakedisFooterGuncelle();
        var toplamEl = document.getElementById('hkd-toplam-goster');
        if (toplamEl && k.hakedis_toplam_tutar !== undefined) toplamEl.textContent = _hakedisKurus(k.hakedis_toplam_tutar);
    } catch(ex) { console.log('Kalem guncelleme hatasi:', ex); }
}

function _hakedisFooterGuncelle() {
    var rows = document.querySelectorAll('#hakedisKalemBody tr');
    var buDon = 0, kum = 0;
    rows.forEach(function(row) {
        var bdt = row.querySelector('.hkd-bu-donem-tutar');
        var kt  = row.querySelector('.hkd-kumulatif-tutar');
        if (bdt) buDon += _hakedisKurusParse(bdt.textContent);
        if (kt) kum   += _hakedisKurusParse(kt.textContent);
    });
    var fbd = document.getElementById('hkd-foot-bu-donem');
    var fkm = document.getElementById('hkd-foot-kumulatif');
    if (fbd) fbd.textContent = _hakedisKurus(buDon);
    if (fkm) fkm.textContent = _hakedisKurus(kum);
}

function _hakedisKurusParse(txt) {
    if (!txt || txt === '-') return 0;
    var cleaned = txt.replace(/[^\d,]/g, '').replace(',', '.');
    return parseFloat(cleaned) || 0;
}

async function hakedisDurumGuncelle(hakedisId, yeniDurum) {
    var token = localStorage.getItem('bai_token');
    try {
        var r = await fetch('/api/hakedis/durum-guncelle/' + hakedisId, {
            method: 'PATCH',
            headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
            body: JSON.stringify({durum: yeniDurum})
        });
        if (!r.ok) { var e = await r.json(); alert(e.detail || 'Durum guncellenemedi'); return; }
        await hakedisDetayAc(hakedisId);
        await hakedisListeYukle();
    } catch(ex) { console.log('Durum guncelleme hatasi:', ex); }
}

function hakedisYeniModalAc() {
    var santiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
    if (!santiyeId) { alert('Header\'dan bir santiye secin.'); return; }
    document.getElementById('hakedisModal').style.display = 'flex';
    var now = new Date();
    var y = now.getFullYear(), m = String(now.getMonth() + 1).padStart(2, '0');
    var lastDay = new Date(y, now.getMonth() + 1, 0).getDate();
    document.getElementById('hakedisDonemBaslangic').value = y + '-' + m + '-01';
    document.getElementById('hakedisDonemBitis').value = y + '-' + m + '-' + String(lastDay).padStart(2, '0');
}

function hakedisModalKapat() {
    document.getElementById('hakedisModal').style.display = 'none';
}

async function hakedisOlustur() {
    var santiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';
    var baslangic = document.getElementById('hakedisDonemBaslangic').value;
    var bitis     = document.getElementById('hakedisDonemBitis').value;
    if (!baslangic || !bitis) { alert('Donem tarihlerini girin.'); return; }
    var token = localStorage.getItem('bai_token');
    try {
        var r = await fetch('/api/hakedis/olustur', {
            method: 'POST',
            headers: {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'},
            body: JSON.stringify({santiye_id: parseInt(santiyeId), donem_baslangic: baslangic, donem_bitis: bitis})
        });
        if (!r.ok) { var e = await r.json(); alert(e.detail || 'Olusturulamadi'); return; }
        var d = await r.json();
        hakedisModalKapat();
        await hakedisListeYukle();
        if (d.hakedis_id) hakedisDetayAc(d.hakedis_id);
    } catch(ex) { alert('Baglanti hatasi.'); }
}

async function hakedisKartSil(hakedisId) {
    if (!confirm('Bu taslak hakedis silinecek. Emin misiniz')) return;
    var token = localStorage.getItem('bai_token');
    try {
        var r = await fetch('/api/hakedis/sil/' + hakedisId, {
            method: 'DELETE',
            headers: {'Authorization': 'Bearer ' + token}
        });
        if (!r.ok) { var e = await r.json(); alert(e.detail || 'Silinemedi'); return; }
        if (_hakedisAktifId === hakedisId) {
            _hakedisAktifId = null;
            var panel = document.getElementById('hakedisDetayIcerik');
            if (panel) panel.innerHTML = '<div style="color:#94A3B8;font-size:14px;text-align:center;padding:60px 0;">Listeden bir hakedis secin</div>';
        }
        await hakedisListeYukle();
    } catch(ex) { alert('Baglanti hatasi.'); }
}

window.addEventListener('resize', function() {
    if (window.innerWidth >= 640) {
        var listPan = document.getElementById('hakedisListPanel');
        var detayPan = document.getElementById('hakedisDetayPanel');
        if (listPan) listPan.style.display = 'flex';
        if (detayPan) detayPan.style.display = 'flex';
    }
});

// ── EXCEL MODAL ──────────────────────────────────────────────────────────────

function excelModalAc(sayfa) {
  window._excelSayfa = sayfa || 'stok';
  const modal = document.getElementById('excelModal');
  if (modal) {
    modal.style.display = 'flex';
    excelTabDegis('export');
  }
}

function excelModalKapat() {
  const modal = document.getElementById('excelModal');
  if (modal) modal.style.display = 'none';
}

function excelTabDegis(tab) {
  const expBtn = document.getElementById('excelTabExport');
  const impBtn = document.getElementById('excelTabImport');
  if (tab === 'export') {
    expBtn.style.color = '#E15A1F';
    expBtn.style.borderBottomColor = '#E15A1F';
    impBtn.style.color = '#9CA3AF';
    impBtn.style.borderBottomColor = 'transparent';
    excelExportIcerik();
  } else {
    impBtn.style.color = '#E15A1F';
    impBtn.style.borderBottomColor = '#E15A1F';
    expBtn.style.color = '#9CA3AF';
    expBtn.style.borderBottomColor = 'transparent';
    excelImportIcerik();
  }
}

function excelExportIcerik() {
  const icerik = document.getElementById('excelModalIcerik');
  icerik.innerHTML = `
    <div style="border:1px solid #E5E7EB; border-radius:12px;
      padding:16px; margin-bottom:14px;">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <div style="width:32px; height:32px; border-radius:8px;
          background:#FFF7ED; display:flex; align-items:center;
          justify-content:center; flex-shrink:0;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
            stroke="#E15A1F" stroke-width="2">
            <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
          </svg>
        </div>
        <div>
          <div style="font-size:14px; font-weight:600; color:#111827;">Stok Durumu Raporu</div>
          <div style="font-size:12px; color:#9CA3AF;">Mevcut stok + hareket geçmişi</div>
        </div>
      </div>
      <div style="display:flex; gap:8px; margin-bottom:12px;">
        <div style="flex:1;">
          <div style="font-size:10.5px; color:#6B7280; font-weight:600;
            text-transform:uppercase; letter-spacing:.05em; margin-bottom:4px;">Başlangıç</div>
          <input type="date" id="excelBaslangic"
            style="width:100%; height:34px; padding:0 10px;
              border:1px solid #E5E7EB; border-radius:7px;
              font-size:13px; font-family:'Plus Jakarta Sans',sans-serif;
              outline:none; color:#374151; box-sizing:border-box;">
        </div>
        <div style="flex:1;">
          <div style="font-size:10.5px; color:#6B7280; font-weight:600;
            text-transform:uppercase; letter-spacing:.05em; margin-bottom:4px;">Bitiş</div>
          <input type="date" id="excelBitis"
            style="width:100%; height:34px; padding:0 10px;
              border:1px solid #E5E7EB; border-radius:7px;
              font-size:13px; font-family:'Plus Jakarta Sans',sans-serif;
              outline:none; color:#374151; box-sizing:border-box;">
        </div>
      </div>
      <button onclick="excelIndir('stok-raporu')"
        style="width:100%; height:38px; background:#E15A1F;
          color:white; border:none; border-radius:8px;
          font-size:13px; font-weight:600; cursor:pointer;
          display:flex; align-items:center; justify-content:center; gap:6px;
          font-family:'Plus Jakarta Sans',sans-serif;"
        onmouseover="this.style.background='#d14f17'"
        onmouseout="this.style.background='#E15A1F'">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
        Raporu İndir
      </button>
    </div>
    <div style="border:1px solid #E5E7EB; border-radius:12px;
      padding:16px;">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <div style="width:32px; height:32px; border-radius:8px;
          background:#EFF6FF; display:flex; align-items:center;
          justify-content:center; flex-shrink:0;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
            stroke="#2563EB" stroke-width="2">
            <line x1="18" y1="20" x2="18" y2="10"/>
            <line x1="12" y1="20" x2="12" y2="4"/>
            <line x1="6" y1="20" x2="6" y2="14"/>
          </svg>
        </div>
        <div>
          <div style="font-size:14px; font-weight:600; color:#111827;">Tedarikçi Karşılaştırma</div>
          <div style="font-size:12px; color:#9CA3AF;">Alım fiyatları vs piyasa</div>
        </div>
      </div>
      <div style="margin-bottom:12px;">
        <div style="font-size:10.5px; color:#6B7280; font-weight:600;
          text-transform:uppercase; letter-spacing:.05em; margin-bottom:8px;">
          Karşılaştırılacak Malzemeler</div>
        <div id="excelMalzemeSecim" style="max-height:150px; overflow-y:auto;
          border:1px solid #F3F4F6; border-radius:8px; padding:4px;">
          <div style="padding:12px; text-align:center; color:#9CA3AF;
            font-size:12px;">Yükleniyor...</div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:6px;">
          <button onclick="excelMalzemeHepsiniSec(true)"
            style="font-size:11px; color:#E15A1F; background:none;
              border:none; cursor:pointer; font-weight:600;
              font-family:'Plus Jakarta Sans',sans-serif;">
            Tümünü Seç</button>
          <button onclick="excelMalzemeHepsiniSec(false)"
            style="font-size:11px; color:#6B7280; background:none;
              border:none; cursor:pointer;
              font-family:'Plus Jakarta Sans',sans-serif;">
            Temizle</button>
        </div>
      </div>
      <button onclick="excelKarsilastirmaIndir()"
        style="width:100%; height:38px; background:#111827;
          color:white; border:none; border-radius:8px;
          font-size:13px; font-weight:600; cursor:pointer;
          display:flex; align-items:center; justify-content:center; gap:6px;
          font-family:'Plus Jakarta Sans',sans-serif;"
        onmouseover="this.style.background='#1F2937'"
        onmouseout="this.style.background='#111827'">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
        Karşılaştırma İndir
      </button>
    </div>
  `;

  const bugun = new Date();
  const birAyOnce = new Date(bugun);
  birAyOnce.setMonth(birAyOnce.getMonth() - 1);
  const fmt = d => d.toISOString().split('T')[0];
  document.getElementById('excelBitis').value = fmt(bugun);
  document.getElementById('excelBaslangic').value = fmt(birAyOnce);

  excelMalzemeListesiYukle();
}

async function excelMalzemeListesiYukle() {
  const container = document.getElementById('excelMalzemeSecim');
  if (!container) return;

  const token = localStorage.getItem('bai_token');
  const aktifSantiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';

  try {
    const url = aktifSantiyeId
      ? `/stok?token=${token}&santiye_id=${aktifSantiyeId}`
      : `/stok?token=${token}`;
    const res = await fetch(url);
    const data = await res.json();

    const malzemeler = data.stok ? Object.entries(data.stok) : [];

    if (malzemeler.length === 0) {
      container.innerHTML = '<div style="padding:12px; text-align:center; color:#9CA3AF; font-size:12px;">Henüz stok kaydı yok.</div>';
      return;
    }

    container.innerHTML = malzemeler.map(([key, m]) => `
      <label style="display:flex; align-items:center; gap:8px;
        padding:8px 10px; border-radius:6px; cursor:pointer;
        transition:background 0.1s;"
        onmouseover="this.style.background='#F9FAFB'"
        onmouseout="this.style.background='transparent'">
        <input type="checkbox" checked value="${key}"
          class="excelMalzemeCheck"
          style="width:16px; height:16px; accent-color:#E15A1F; cursor:pointer;">
        <div style="flex:1; min-width:0;">
          <div style="font-size:13px; font-weight:500; color:#111827;
            font-family:'Plus Jakarta Sans',sans-serif;">
            ${m.malzeme_ad || key}</div>
        </div>
        <div style="font-size:12px; color:#9CA3AF;
          font-family:'Plus Jakarta Sans',sans-serif;">
          ${(m.mevcut||0).toLocaleString('tr-TR')} ${m.birim||''}</div>
      </label>
    `).join('');
  } catch(e) {
    container.innerHTML = '<div style="padding:12px; text-align:center; color:#DC2626; font-size:12px;">Yüklenemedi.</div>';
  }
}

function excelMalzemeHepsiniSec(sec) {
  document.querySelectorAll('.excelMalzemeCheck').forEach(cb => cb.checked = sec);
}

function excelKarsilastirmaIndir() {
  const secili = [...document.querySelectorAll('.excelMalzemeCheck:checked')]
    .map(cb => cb.value);

  if (secili.length === 0) {
    alert('En az bir malzeme seçin.');
    return;
  }

  const token = localStorage.getItem('bai_token');
  const aktifSantiyeId = window._aktifSantiyeId || localStorage.getItem('bai_aktif_santiye') || '';

  let url = `/excel/fiyat-karsilastirma?token=${token}`;
  if (aktifSantiyeId) url += `&santiye_id=${aktifSantiyeId}`;
  url += `&malzemeler=${encodeURIComponent(secili.join(','))}`;

  window.open(url, '_blank');
}

function excelImportIcerik() {
  const icerik = document.getElementById('excelModalIcerik');
  icerik.innerHTML = `
    <div style="border:1px solid #E5E7EB; border-radius:12px;
      padding:16px; margin-bottom:14px;">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <div style="width:32px; height:32px; border-radius:8px;
          background:#F3F4F6; display:flex; align-items:center;
          justify-content:center; flex-shrink:0;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
            stroke="#6B7280" stroke-width="2">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
        </div>
        <div>
          <div style="font-size:14px; font-weight:600; color:#111827;">Şablon İndir</div>
          <div style="font-size:12px; color:#9CA3AF;">Şablonu indir, doldur, geri yükle</div>
        </div>
      </div>
      <button onclick="excelIndir('import-sablonu')"
        style="width:100%; height:38px; background:#F9FAFB;
          color:#374151; border:1px solid #E5E7EB; border-radius:8px;
          font-size:13px; font-weight:600; cursor:pointer;
          display:flex; align-items:center; justify-content:center; gap:6px;
          font-family:'Plus Jakarta Sans',sans-serif;"
        onmouseover="this.style.background='#F3F4F6'"
        onmouseout="this.style.background='#F9FAFB'">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
        Boş Şablonu İndir
      </button>
    </div>
    <div style="border:1px solid #E5E7EB; border-radius:12px;
      padding:16px;">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <div style="width:32px; height:32px; border-radius:8px;
          background:#FFF7ED; display:flex; align-items:center;
          justify-content:center; flex-shrink:0;">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
            stroke="#E15A1F" stroke-width="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
        </div>
        <div>
          <div style="font-size:14px; font-weight:600; color:#111827;">Excel Dosyası Yükle</div>
          <div style="font-size:12px; color:#9CA3AF;">Doldurulmuş şablonu yükle</div>
        </div>
      </div>
      <div id="excelDropZone"
        ondrop="excelDosyaDrop(event)"
        ondragover="event.preventDefault();this.style.borderColor='#E15A1F';this.style.background='rgba(225,90,31,0.04)'"
        ondragleave="this.style.borderColor='#E5E7EB';this.style.background='#F9FAFB'"
        style="border:2px dashed #E5E7EB; border-radius:10px;
          background:#F9FAFB; padding:24px; text-align:center;
          cursor:pointer; transition:all 0.15s;"
        onclick="document.getElementById('excelFileInput').click()">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none"
          stroke="#9CA3AF" stroke-width="1.5"
          style="margin:0 auto 8px; display:block;">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <div style="font-size:13px; color:#374151; font-weight:500;">
          Sürükle bırak veya tıkla</div>
        <div style="font-size:11px; color:#9CA3AF; margin-top:4px;">.xlsx dosyası</div>
      </div>
      <input type="file" id="excelFileInput" accept=".xlsx,.xls"
        style="display:none;" onchange="excelDosyaSecildi(this)">
      <div id="excelImportSonuc" style="margin-top:10px;"></div>
    </div>
  `;
}

async function excelIndir(tip) {
    var token = localStorage.getItem('bai_token');
    var santiyeId = window._aktifSantiyeId || '';
    var url = '';
    if (tip === 'stok-raporu') {
        var bas = document.getElementById('excelBaslangic') ? document.getElementById('excelBaslangic').value : '';
        var bit = document.getElementById('excelBitis') ? document.getElementById('excelBitis').value : '';
        url = '/excel/stok-raporu?token=' + token +
              (santiyeId ? '&santiye_id=' + santiyeId : '') +
              (bas ? '&baslangic=' + bas : '') +
              (bit ? '&bitis=' + bit : '');
    } else if (tip === 'fiyat-karsilastirma') {
        var il = document.getElementById('excelFiyatIl') ? document.getElementById('excelFiyatIl').value : '';
        url = '/excel/fiyat-karsilastirma?token=' + token + '&il=' + encodeURIComponent(il);
    } else if (tip === 'import-sablonu') {
        url = '/excel/import-sablonu?token=' + token;
    }
    var btn = event.target;
    var orijinal = btn.innerHTML;
    btn.innerHTML = '⏳ Hazırlanıyor...';
    btn.disabled = true;
    try {
        var res = await fetch(url);
        if (!res.ok) throw new Error('Sunucu hatası');
        var blob = await res.blob();
        var a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        var cd = res.headers.get('Content-Disposition') || '';
        a.download = cd.split('filename=')[1] ? cd.split('filename=')[1].replace(/"/g,'') : ('buildingai_' + tip + '_' + new Date().toISOString().split('T')[0] + '.xlsx');
        a.click();
        URL.revokeObjectURL(a.href);
    } catch(e) {
        alert('İndirme hatası: ' + e.message);
    } finally {
        btn.innerHTML = orijinal;
        btn.disabled = false;
    }
}

async function excelDosyaSecildi(input) {
    var dosya = input.files[0];
    if (!dosya) return;
    await excelImportYukle(dosya);
}

function excelDosyaDrop(event) {
    event.preventDefault();
    var dosya = event.dataTransfer.files[0];
    if (dosya) excelImportYukle(dosya);
}

async function excelImportYukle(dosya) {
    var token = localStorage.getItem('bai_token');
    var santiyeId = window._aktifSantiyeId || '';
    var sonucDiv = document.getElementById('excelImportSonuc');
    sonucDiv.style.display = 'block';
    sonucDiv.innerHTML = '<div style="padding:12px;background:#f0f9ff;border-radius:8px;color:#0369a1;font-size:13px;">⏳ Yükleniyor: ' + dosya.name + '</div>';
    var form = new FormData();
    form.append('dosya', dosya);
    if (santiyeId) form.append('santiye_id', santiyeId);
    try {
        var res = await fetch('/excel/import-stok?token=' + token, { method: 'POST', body: form });
        var data = await res.json();
        if (res.ok) {
            var hatalarHtml = '';
            if (data.hatalar && data.hatalar.length) {
                hatalarHtml = '<br><details><summary style="cursor:pointer;color:#dc2626;">Hatalar</summary>' +
                    data.hatalar.map(function(h) { return '<div style="font-size:12px;">• ' + h + '</div>'; }).join('') +
                    '</details>';
            }
            sonucDiv.innerHTML = '<div style="padding:12px;background:#f0fdf4;border-radius:8px;border:1px solid #bbf7d0;"><div style="font-weight:600;color:#166534;margin-bottom:8px;">✅ Import tamamlandı</div><div style="font-size:13px;color:#374151;">• ' + data.basarili + ' satır başarıyla eklendi<br>• ' + data.atlanan + ' satır atlandı' + hatalarHtml + '</div></div>';
            if (typeof stokYukle === 'function') stokYukle(santiyeId ? parseInt(santiyeId) : null);
        } else {
            throw new Error(data.detail || 'Hata');
        }
    } catch(e) {
        sonucDiv.innerHTML = '<div style="padding:12px;background:#fef2f2;border-radius:8px;border:1px solid #fecaca;color:#dc2626;font-size:13px;">❌ ' + e.message + '</div>';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('excelModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) excelModalKapat();
        });
    }
});
