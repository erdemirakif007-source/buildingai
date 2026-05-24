// hiyerarsi.js — Metraj Yönetimi Yönetim Sayfası
// Bina → Kat → Mahal → iş Kalemi ağacı + CRUD + Excel import
// Auth: localStorage.bai_token  |  API: /api/v2/

/* ══════════════════════════════════════════════
   DURUM (STATE)
══════════════════════════════════════════════ */
var _hiy = {
  santiyeId: null,
  santiyeAd: '',
  agac: null,   // GET /hiyerarsi yanıtı
  secili: null,   // { tip:'bina'|'kat'|'mahal'|'mahalsiz', id, bina?, kat?, mahal? }
  acikNodes: {},     // sayfa yenilenene kadar acik kalan agac dugumleri
  modalTip: null,   // 'bina'|'kat'|'mahal'|'isKalemi'|'ilerleme'|'excel'
  modalDuzenleId: null,
  modalParentId: null,
  _isKalemiMahalId: null,
  _isKalemiSantiyeId: null,
  modalMetraj: 0,   // açık iş kaleminin metrajı (malzeme modalı için)
  _onerMap: {},     // {fiyat_takip_id: {carpan, guncel_fiyat}} katalog çarpan haritası
  varyasyon: 'gorsel',          // 'klasik' | 'gorsel'
  cepheSeciliKatId: null,       // görsel modda seçili kat id
  bimModel: null,               // görsel modda yüklü BIM modeli (null=yok, obj=var)
  bimModelYuklendi: false,      // BIM API kontrolü yapıldı mı (iframe yeniden yüklenmesin)
};

/* ══════════════════════════════════════════════
   AUTH / HTTP YARDIMCILARI
══════════════════════════════════════════════ */
function _hiyToken() { return localStorage.getItem('bai_token') || ''; }

function _hiyHeaders() {
  return { 'Authorization': 'Bearer ' + _hiyToken(), 'Content-Type': 'application/json' };
}

async function _hiyGet(url) {
  var sep = url.indexOf('?') >= 0 ? '&' : '?';
  var r = await fetch(url + sep + 'token=' + encodeURIComponent(_hiyToken()));
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function _hiyPost(url, body) {
  var r = await fetch(url, { method: 'POST', headers: _hiyHeaders(), body: JSON.stringify(body) });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function _hiyPatch(url, body) {
  var r = await fetch(url, { method: 'PATCH', headers: _hiyHeaders(), body: JSON.stringify(body) });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function _hiyDelete(url) {
  var r = await fetch(url, { method: 'DELETE', headers: _hiyHeaders() });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function _hiyPut(url, body) {
  var r = await fetch(url, { method: 'PUT', headers: _hiyHeaders(), body: JSON.stringify(body) });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

/* ══════════════════════════════════════════════
   TOAST / BiLDiRiM
══════════════════════════════════════════════ */
function _hiyToast(msg, tip) {
  tip = tip || 'info';
  if (typeof showToast === 'function') { showToast(msg, tip); return; }
  // Yedek: basit bildirim
  var existing = document.getElementById('_hiyToastFallback');
  if (existing) existing.remove();
  var colors = {
    success: { bg: 'rgba(34,197,94,0.15)', border: 'rgba(34,197,94,0.4)' },
    error: { bg: 'rgba(239,68,68,0.15)', border: 'rgba(239,68,68,0.4)' },
    warning: { bg: 'rgba(249,115,22,0.15)', border: 'rgba(249,115,22,0.5)' },
    info: { bg: 'rgba(56,189,248,0.15)', border: 'rgba(56,189,248,0.4)' },
  };
  var c = colors[tip] || colors.info;
  var t = document.createElement('div');
  t.id = '_hiyToastFallback';
  t.style.cssText = 'position:fixed;top:70px;right:20px;z-index:99999;background:' + c.bg + ';border:1px solid ' + c.border + ';backdrop-filter:blur(16px);border-radius:14px;padding:13px 18px;color:#fff;font-size:13px;font-weight:500;display:flex;align-items:center;gap:10px;box-shadow:0 8px 32px rgba(0,0,0,0.4);max-width:320px;font-family:sans-serif;animation:hiyToastIn 0.3s ease;';
  t.innerHTML = '<span>' + _escH(msg) + '</span><button onclick="this.parentElement.remove()" style="background:none;border:none;color:#aaa;cursor:pointer;font-size:15px;margin-left:auto;padding:0 0 0 8px;">x</button>';
  var style = document.createElement('style');
  style.textContent = '@keyframes hiyToastIn{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}';
  document.head.appendChild(style);
  document.body.appendChild(t);
  setTimeout(function () { if (t.parentElement) t.remove(); }, 4000);
}

/* ══════════════════════════════════════════════
   FORMAT YARDIMCILARI
══════════════════════════════════════════════ */
function _hiyPara(tl) {
  return new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(tl || 0) + ' ₺';
}

function _hiyNum(n) {
  return new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 2 }).format(n || 0);
}

function _hiyBirimDuzelt(birim) {
  return String(birim || '')
    .replace(/m²/g, 'm²')
    .replace(/m³/g, 'm³')
    .replace(/takım/g, 'takım');
}

function _escH(s) {
  if (s == null) return '';
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/* ══════════════════════════════════════════════
   SAYFA AÇ / KAPAT
══════════════════════════════════════════════ */
function hiyerarsiPageAc() {
  // Diğer sayfaları kapat
  if (typeof tumSayfalariGizle === 'function') {
    tumSayfalariGizle();
  } else {
    var gizle = ['content', 'aiCommandBar', 'santiyePage', 'fiyatPage', 'stokPage',
      'arsivPage', 'sahaKayitlariPage', 'kameraPage', 'hakedisPage', 'engineerDashboard'];
    gizle.forEach(function (pid) {
      var el = document.getElementById(pid);
      if (el) el.style.display = 'none';
    });
  }

  var page = document.getElementById('hiyerarsiPage');
  if (!page) return;
  page.style.display = 'flex';

  _hiy.santiyeId = localStorage.getItem('bai_aktif_santiye');
  _hiy.santiyeAd = localStorage.getItem('bai_aktif_santiye_ad') || 'Åantiye';

  if (!_hiy.santiyeId) {
    page.innerHTML = '<div class="hiy-loading"><div class="hiy-empty-title">Aktif şantiye seçilmedi</div><div class="hiy-empty-desc">önce bir şantiye seçin.</div></div>';
    return;
  }

  _hiyerarsiSayfaRender();
  _hiyerarsiVeriYukle();
}

function hiyerarsiPageKapat() {
  var page = document.getElementById('hiyerarsiPage');
  if (page) page.style.display = 'none';
}

/* ══════════════════════════════════════════════
   SAYFA iÇERiÄi RENDER
══════════════════════════════════════════════ */
function _hiyerarsiSayfaRender() {
  var page = document.getElementById('hiyerarsiPage');
  page.innerHTML = [
    '<div class="hiy-mobile-overlay" id="hiyMobOv" onclick="hiyMobilePanelKapat()"></div>',
    '<div class="hiy-modal-overlay" id="hiyMdOv">',
    '  <div class="hiy-modal" id="hiyMd">',
    '    <div class="hiy-modal-header">',
    '      <span class="hiy-modal-title" id="hiyMdBaslik">-</span>',
    '      <button class="hiy-modal-close" onclick="hiyModalKapat()">x</button>',
    '    </div>',
    '    <div class="hiy-modal-body" id="hiyMdBody"></div>',
    '    <div class="hiy-modal-footer">',
    '      <button class="hiy-modal-btn hiy-modal-btn-cancel" onclick="hiyModalKapat()">Iptal</button>',
    '      <button class="hiy-modal-btn hiy-modal-btn-confirm" id="hiyMdKaydetBtn" onclick="hiyModalKaydet()">Kaydet</button>',
    '    </div>',
    '  </div>',
    '</div>',
    '<div id="hiyBimOv" style="display:none;position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,0.75);align-items:center;justify-content:center;">',
    '  <div style="background:#1E293B;border-radius:16px;width:90vw;height:85vh;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 24px 64px rgba(0,0,0,0.5);">',
    '    <div style="display:flex;align-items:center;justify-content:space-between;padding:14px 20px;border-bottom:1px solid #334155;flex-shrink:0;">',
    '      <div>',
    '        <div id="hiyBimBaslik" style="color:#F1F5F9;font-weight:700;font-size:15px;">3D BIM Modeli</div>',
    '        <div id="hiyBimAlt" style="color:#94A3B8;font-size:12px;margin-top:2px;"></div>',
    '      </div>',
    '      <button onclick="hiyBimModalKapat()" style="background:rgba(255,255,255,0.08);border:1px solid #475569;color:#CBD5E1;border-radius:8px;width:32px;height:32px;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;line-height:1;">&#x2715;</button>',
    '    </div>',
    '    <iframe id="hiyBimIframe" src="" style="flex:1;border:none;width:100%;height:100%;background:#0F172A;"></iframe>',
    '  </div>',
    '</div>',
    '<div class="hiy-layout">',
    '  <div class="hiy-tree-panel" id="hiyTreePanel">',
    '    <div class="hiy-tree-header">',
    '      <div class="hiy-tree-site-name">🏗️ ' + _escH(_hiy.santiyeAd) + '</div>',
    '      <button class="hiy-btn hiy-btn-primary" style="width:100%;justify-content:center;" onclick="hiyBinaModalAc()">+ Bina Ekle</button>',
    '    </div>',
    '    <div class="hiy-tree-scroll" id="hiyAgacKap">',
    '      <div class="hiy-loading"><div class="hiy-spinner"></div><span>Yukleniyor...</span></div>',
    '    </div>',
    '  </div>',
    '  <div class="hiy-content-panel">',
    '    <div class="hiy-content-header" id="hiyCtxHd">',
    '      <div style="display:flex;align-items:center;gap:10px;">',
    '        <button class="hiy-mobile-toggle" onclick="hiyMobilePanelAc()">☰</button>',
    '        <div class="hiy-breadcrumb" id="hiyBc">',
    '          <span class="hiy-breadcrumb-item" onclick="hiyerarsiPageAc()">🏗️ ' + _escH(_hiy.santiyeAd) + '</span>',
    '        </div>',
    '      </div>',
    '      <div class="hiy-content-actions" id="hiyCtxAkt"></div>',
    '    </div>',
    '    <div id="hiyVaryasyonBar" style="display:none;padding:8px 16px;background:#F8FAFC;border-bottom:1px solid #E2E8F0;flex-shrink:0;display:none;align-items:center;gap:10px;">',
    '      <span style="font-size:10px;color:#94A3B8;font-weight:700;letter-spacing:.07em;text-transform:uppercase;">VARYASYON</span>',
    '      <div style="display:inline-flex;background:#EEF2F7;border-radius:7px;border:1px solid #E2E8F0;padding:2px;gap:1px;" id="hiyVarToggle">',
    '        <button id="hiyVarBtnKlasik" onclick="hiyVaryasyonDegistir(\'klasik\')" style="padding:4px 12px;border-radius:5px;border:none;font-size:11.5px;font-weight:500;cursor:pointer;font-family:inherit;background:transparent;color:#64748B;">Klasik · ağaç + tablo</button>',
    '        <button id="hiyVarBtnGorsel" onclick="hiyVaryasyonDegistir(\'gorsel\')" style="padding:4px 12px;border-radius:5px;border:none;font-size:11.5px;font-weight:600;cursor:pointer;font-family:inherit;background:#fff;color:#0F172A;box-shadow:0 1px 2px rgba(15,23,42,.08);">Görsel · ilerleme haritası</button>',
    '      </div>',
    '      <span id="hiyVar3dBtn" style="display:none;"><button onclick="hiyBimGoruntule()" style="display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:7px;border:1px solid #BFDBFE;background:#EFF6FF;color:#2563EB;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit;"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>3D BIM</button></span>',
    '    </div>',
    '    <div class="hiy-content-scroll" id="hiyCtxBody">',
    '      <div class="hiy-empty">',
    '        <div class="hiy-empty-title">Sol panelden bir konum secin</div>',
    '        <div class="hiy-empty-desc">Bina, kat veya mahal secerek o konuma ait is kalemlerini goruntuleyin.</div>',
    '      </div>',
    '    </div>',
    '  </div>',
    '</div>',
  ].join('\n');
}
/* VERi YÜKLEME
══════════════════════════════════════════════ */
async function _hiyerarsiVeriYukle() {
  try {
    var veri = await _hiyGet('/api/v2/santiye/' + _hiy.santiyeId + '/hiyerarsi');
    _hiy.agac = veri;
    _hiyAgacRender(veri);
  } catch (e) {
    var kap = document.getElementById('hiyAgacKap');
    if (kap) kap.innerHTML = '<div class="hiy-empty"><div class="hiy-empty-title">Yüklenemedi</div><div class="hiy-empty-desc">' + _escH(e.message) + '</div></div>';
  }
}

/* ══════════════════════════════════════════════
   AÄAÇ RENDER
══════════════════════════════════════════════ */
function _hiyNodeAcik(cid) {
  return !!(_hiy.acikNodes && _hiy.acikNodes[cid]);
}

function _hiyIsKalemiSayisi(list) {
  return (list || []).length;
}

function _hiyKatKalemSayisi(kat) {
  var toplam = 0;
  (kat.mahaller || []).forEach(function (mahal) { toplam += _hiyIsKalemiSayisi(mahal.is_kalemleri); });
  return toplam;
}

function _hiyBinaKalemSayisi(bina) {
  var toplam = 0;
  (bina.katlar || []).forEach(function (kat) { toplam += _hiyKatKalemSayisi(kat); });
  return toplam;
}

function _hiyAgacRender(veri) {
  var kap = document.getElementById('hiyAgacKap');
  if (!kap) return;

  if (!veri.binalar || veri.binalar.length === 0) {
    kap.innerHTML = '<div class="hiy-empty" style="padding:30px 14px;"><div class="hiy-empty-title" style="font-size:13px;">Henuz bina yok</div><div class="hiy-empty-desc" style="font-size:11px;">Yukaridaki "Bina Ekle" butonunu kullanin.</div></div>';
    return;
  }

  var html = '';
  veri.binalar.forEach(function (bina) {
    var cid = 'hiyC-b' + bina.id;
    var acik = _hiyNodeAcik(cid);
    html += '<div class="hiy-tree-row hiy-level-bina" id="hiyRow-b' + bina.id + '" onclick="hiyBinaRowTikla(' + bina.id + ')">'
      + '<span class="hiy-tree-toggle ' + (acik ? 'open' : '') + '" id="hiyTg-' + cid + '">' + (acik ? '&#9660;' : '&#9654;') + '</span>'
      + '<span class="hiy-tree-icon">🏢</span>'
      + '<span class="hiy-tree-label" title="' + _escH(bina.ad) + '">' + _escH(bina.ad) + '</span>'
      + '<span class="hiy-tree-badge">' + _hiyBinaKalemSayisi(bina) + '</span>'
      + '<span class="hiy-tree-actions">'
      + '<button class="hiy-tree-add-inline" onclick="event.stopPropagation();hiyKatModalAc(' + bina.id + ')">Kat Ekle</button>'
      + '<button class="hiy-tree-action-btn" title="Düzenle" onclick="hiyBinaDuzenle(event,' + bina.id + ')">✏️</button>'
      + '<button class="hiy-tree-action-btn danger" title="Sil" onclick="hiyBinaSil(event,' + bina.id + ')">🗑️</button>'
      + '</span>'
      + '</div>'
      + '<div class="hiy-tree-children ' + (acik ? 'open' : '') + '" id="' + cid + '" ' + (acik ? 'style="max-height:3000px"' : '') + '>'
      + _hiyKatlarHtml(bina)
      + '</div>';
  });

  var mahalsiz = veri.mahalsiz_is_kalemleri || [];
  if (mahalsiz.length > 0) {
    html += '<div class="hiy-tree-row" id="hiyRow-mahalsiz" onclick="hiyMahalsizSecildi()">'
      + '<span class="hiy-tree-toggle hiy-tree-toggle-empty"></span>'
      + '<span class="hiy-tree-icon">📋</span>'
      + '<span class="hiy-tree-label">Genel İş Kalemleri</span>'
      + '<span class="hiy-tree-badge">' + mahalsiz.length + '</span>'
      + '</div>';
  }

  kap.innerHTML = html;
  _hiySeciliSatirIsaretle();
}

function _hiyKatlarHtml(bina) {
  if (!bina.katlar || bina.katlar.length === 0) return '';
  var html = '';
  bina.katlar.forEach(function (kat) {
    var cid = 'hiyC-k' + kat.id;
    var acik = _hiyNodeAcik(cid);
    var etiket = kat.etiket || ('Kat ' + kat.kat_no);
    html += '<div class="hiy-tree-row hiy-level-kat" id="hiyRow-k' + kat.id + '" onclick="hiyKatRowTikla(' + kat.id + ',' + bina.id + ')">'
      + '<span class="hiy-tree-toggle ' + (acik ? 'open' : '') + '" id="hiyTg-' + cid + '">' + (acik ? '&#9660;' : '&#9654;') + '</span>'
      + '<span class="hiy-tree-icon">🏠</span>'
      + '<span class="hiy-tree-label" title="' + _escH(etiket) + '">' + _escH(etiket) + '</span>'
      + '<span class="hiy-tree-badge">' + _hiyKatKalemSayisi(kat) + '</span>'
      + '<span class="hiy-tree-actions">'
      + '<button class="hiy-tree-add-inline" onclick="event.stopPropagation();hiyMahalModalAc(' + kat.id + ',' + bina.id + ')">Mahal Ekle</button>'
      + '<button class="hiy-tree-action-btn" title="Düzenle" onclick="hiyKatDuzenle(event,' + kat.id + ',' + bina.id + ')">✏️</button>'
      + '<button class="hiy-tree-action-btn danger" title="Sil" onclick="hiyKatSil(event,' + kat.id + ')">🗑️</button>'
      + '</span>'
      + '</div>'
      + '<div class="hiy-tree-children ' + (acik ? 'open' : '') + '" id="' + cid + '" ' + (acik ? 'style="max-height:3000px"' : '') + '>'
      + _hiyMahallerHtml(kat, bina)
      + '</div>';
  });
  return html;
}

function _hiyMahallerHtml(kat, bina) {
  if (!kat.mahaller || kat.mahaller.length === 0) return '';
  var html = '';
  kat.mahaller.forEach(function (mahal) {
    var sayac = (mahal.is_kalemleri || []).length;
    html += '<div class="hiy-tree-row hiy-level-mahal" id="hiyRow-m' + mahal.id + '" onclick="hiyMahalSecildi(' + mahal.id + ',' + kat.id + ',' + bina.id + ')">'
      + '<span class="hiy-tree-toggle hiy-tree-toggle-empty"></span>'
      + '<span class="hiy-tree-icon">🚪</span>'
      + '<span class="hiy-tree-label" title="' + _escH(mahal.ad) + '">' + _escH(mahal.ad) + '</span>'
      + '<span class="hiy-tree-badge">' + sayac + '</span>'
      + '<span class="hiy-tree-actions">'
      + '<button class="hiy-tree-action-btn" title="Düzenle" onclick="hiyMahalDuzenle(event,' + mahal.id + ',' + kat.id + ',' + bina.id + ')">✏️</button>'
      + '<button class="hiy-tree-action-btn danger" title="Sil" onclick="hiyMahalSil(event,' + mahal.id + ')">🗑️</button>'
      + '</span>'
      + '</div>';
  });
  return html;
}

function hiyBinaRowTikla(binaId) {
  hiyBinaSecildi(binaId);
  hiyAgacToggleId('hiyC-b' + binaId);
}

function hiyKatRowTikla(katId, binaId) {
  hiyKatSecildi(katId, binaId);
  hiyAgacToggleId('hiyC-k' + katId);
}

function hiyAgacToggle(e, cid) {
  if (e) e.stopPropagation();
  hiyAgacToggleId(cid);
}

function hiyAgacToggleId(cid) {
  var children = document.getElementById(cid);
  var toggle = document.getElementById('hiyTg-' + cid);
  if (!children) return;
  var acik = !children.classList.contains('open');
  if (!_hiy.acikNodes) _hiy.acikNodes = {};
  _hiy.acikNodes[cid] = acik;
  if (acik) {
    var targetH = children.scrollHeight;
    _hiyUstContainerGuncelle(children, targetH);
    children.classList.add('open');
    children.style.maxHeight = '0px';
    children.offsetHeight;
    children.style.maxHeight = targetH + 'px';
  } else {
    var collapseH = children.scrollHeight;
    children.style.maxHeight = collapseH + 'px';
    children.offsetHeight;
    children.classList.remove('open');
    children.style.maxHeight = '0px';
    _hiyUstContainerGuncelle(children, -collapseH);
  }
  if (toggle) {
    toggle.classList.toggle('open', acik);
    toggle.innerHTML = acik ? '&#9660;' : '&#9654;';
  }
}

function _hiyUstContainerGuncelle(el, delta) {
  var parent = el.parentElement;
  while (parent) {
    if (parent.classList && parent.classList.contains('hiy-tree-children') && parent.classList.contains('open')) {
      var mevcut = parseFloat(parent.style.maxHeight) || parent.scrollHeight;
      parent.style.maxHeight = Math.max(0, mevcut + delta) + 'px';
    }
    parent = parent.parentElement;
  }
}

function _hiySeciliSatirIsaretle() {
  if (!_hiy.secili) return;
  var id = null;
  if (_hiy.secili.tip === 'bina') id = 'hiyRow-b' + _hiy.secili.id;
  else if (_hiy.secili.tip === 'kat') id = 'hiyRow-k' + _hiy.secili.id;
  else if (_hiy.secili.tip === 'mahal') id = 'hiyRow-m' + _hiy.secili.id;
  else if (_hiy.secili.tip === 'mahalsiz') id = 'hiyRow-mahalsiz';
  var row = id ? document.getElementById(id) : null;
  if (row) row.classList.add('selected');
}
function _hiySecimTemizle() {
  document.querySelectorAll('.hiy-tree-row.selected').forEach(function (el) { el.classList.remove('selected'); });
}

function hiyBinaSecildi(binaId) {
  _hiySecimTemizle();
  var row = document.getElementById('hiyRow-b' + binaId);
  if (row) row.classList.add('selected');
  var bina = (_hiy.agac.binalar || []).find(function (b) { return b.id === binaId; });
  if (!bina) return;
  _hiy.secili = { tip: 'bina', id: binaId, bina: bina };
  _hiyBcGuncelle([{ ad: bina.ad, icon: '🏢' }]);
  _hiyActionsGuncelle(null);
  _hiyBinaIcerigiGoster(bina);
}

function hiyKatSecildi(katId, binaId) {
  _hiySecimTemizle();
  var row = document.getElementById('hiyRow-k' + katId);
  if (row) row.classList.add('selected');
  var bina = (_hiy.agac.binalar || []).find(function (b) { return b.id === binaId; });
  var kat = bina ? (bina.katlar || []).find(function (k) { return k.id === katId; }) : null;
  if (!kat) return;
  _hiy.secili = { tip: 'kat', id: katId, bina: bina, kat: kat };
  _hiyBcGuncelle([
    { ad: bina.ad, icon: '🏢', onclick: 'hiyBinaSecildi(' + binaId + ')' },
    { ad: kat.etiket || ('Kat ' + kat.kat_no), icon: '🏠' },
  ]);
  _hiyActionsGuncelle(null);
  _hiyKatIcerigiGoster(bina, kat);
}

function hiyMahalSecildi(mahalId, katId, binaId) {
  _hiySecimTemizle();
  var row = document.getElementById('hiyRow-m' + mahalId);
  if (row) row.classList.add('selected');
  var bina = (_hiy.agac.binalar || []).find(function (b) { return b.id === binaId; });
  var kat = bina ? (bina.katlar || []).find(function (k) { return k.id === katId; }) : null;
  var mahal = kat ? (kat.mahaller || []).find(function (m) { return m.id === mahalId; }) : null;
  if (!mahal) return;
  _hiy.secili = { tip: 'mahal', id: mahalId, bina: bina, kat: kat, mahal: mahal };
  _hiyBcGuncelle([
    { ad: bina.ad, icon: '🏢', onclick: 'hiyBinaSecildi(' + binaId + ')' },
    { ad: kat.etiket || ('Kat ' + kat.kat_no), icon: '🏠', onclick: 'hiyKatSecildi(' + katId + ',' + binaId + ')' },
    { ad: mahal.ad, icon: '🚪' },
  ]);
  _hiyActionsGuncelle(mahal.id);
  _hiyMahalIcerigiGoster(bina, kat, mahal);
}

function hiyMahalsizSecildi() {
  _hiySecimTemizle();
  var row = document.getElementById('hiyRow-mahalsiz');
  if (row) row.classList.add('selected');
  _hiy.secili = { tip: 'mahalsiz' };
  _hiyBcGuncelle([{ ad: 'Genel İş Kalemleri', icon: '📋' }]);
  _hiyActionsGuncelle(null);
  var kalemler = (_hiy.agac && _hiy.agac.mahalsiz_is_kalemleri) ? _hiy.agac.mahalsiz_is_kalemleri : [];
  var body = document.getElementById('hiyCtxBody');
  if (!body) return;
  if (kalemler.length === 0) {
    body.innerHTML = '<div class="hiy-empty"><div class="hiy-empty-icon">📋</div><div class="hiy-empty-title">Genel iş kalemi yok</div></div>';
  } else {
    body.innerHTML = '<div class="hiy-table-wrap">' + _hiyTabelaHtml(kalemler, false) + '</div>';
  }
}

/* ══════════════════════════════════════════════
   BREADCRUMB
══════════════════════════════════════════════ */
function _hiyBcGuncelle(adimlar) {
  var el = document.getElementById('hiyBc');
  if (!el) return;
  var html = '<span class="hiy-breadcrumb-item" onclick="hiyerarsiPageAc()">🏗️ ' + _escH(_hiy.santiyeAd) + '</span>';
  adimlar.forEach(function (a, i) {
    html += '<span class="hiy-breadcrumb-sep">›</span>';
    var son = i === adimlar.length - 1;
    if (a.onclick && !son) {
      html += '<span class="hiy-breadcrumb-item" onclick="' + a.onclick + '">' + (a.icon ? a.icon + ' ' : '') + _escH(a.ad) + '</span>';
    } else {
      html += '<span class="hiy-breadcrumb-item current">' + (a.icon ? a.icon + ' ' : '') + _escH(a.ad) + '</span>';
    }
  });
  el.innerHTML = html;
}

/* ══════════════════════════════════════════════
   CONTENT ACTIONS (sağ üst butonlar)
══════════════════════════════════════════════ */
function _hiyActionsGuncelle(mahalId) {
  var el = document.getElementById('hiyCtxAkt');
  if (!el) return;
  var ekleOnclick = mahalId
    ? 'hiyIsKalemiModalAc(null,' + mahalId + ',null)'
    : 'hiyIsKalemiModalAc(null,null,' + _hiy.santiyeId + ')';
  el.innerHTML = '<button class="hiy-btn hiy-btn-secondary" onclick="hiyBimGoruntule()" style="color:#3B82F6;border-color:#BFDBFE;">'
    + '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 2 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>'
    + '3D BIM Görüntüle</button>'
    + ' <button class="hiy-btn hiy-btn-secondary" onclick="hiyExcelModalAc()">'
    + '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
    + 'Excel\'den Yükle</button>'
    + '<button class="hiy-btn hiy-btn-primary" onclick="' + ekleOnclick + '">+ iş Kalemi Ekle</button>';
}

/* ══════════════════════════════════════════════
   SAÄ PANEL iÇERiKLER
══════════════════════════════════════════════ */
function _hiyBinaIcerigiGoster(bina) {
  _hiyCepheVaryasyonBarGoster(true);
  var body = document.getElementById('hiyCtxBody');
  if (_hiy.varyasyon === 'gorsel') {
    _hiyCepheHaritasiRender(bina);
    return;
  }
  if (body) body.classList.remove('gorsel-mod');
  var tumKalemler = [];
  (bina.katlar || []).forEach(function (kat) {
    (kat.mahaller || []).forEach(function (mahal) {
      (mahal.is_kalemleri || []).forEach(function (ik) {
        tumKalemler.push(Object.assign({}, ik, { _mahalAd: mahal.ad, _katAd: kat.etiket || 'Kat ' + kat.kat_no }));
      });
    });
  });
  if (!body) return;
  if (tumKalemler.length === 0) {
    body.innerHTML = '<div class="hiy-empty"><div class="hiy-empty-icon">📋</div><div class="hiy-empty-title">Bu binada henüz iş kalemi yok</div><div class="hiy-empty-desc">Kat ve mahal oluşturup iş kalemi ekleyin.</div></div>';
    return;
  }
  body.innerHTML = '<div class="hiy-table-wrap">' + _hiyTabelaHtml(tumKalemler, true) + '</div>';
}

function _hiyKatIcerigiGoster(bina, kat) {
  _hiyCepheVaryasyonBarGoster(true);
  var body = document.getElementById('hiyCtxBody');
  if (_hiy.varyasyon === 'gorsel') {
    _hiy.cepheSeciliKatId = kat.id;
    _hiyCepheHaritasiRender(bina);
    return;
  }
  if (body) body.classList.remove('gorsel-mod');
  var tumKalemler = [];
  (kat.mahaller || []).forEach(function (mahal) {
    (mahal.is_kalemleri || []).forEach(function (ik) {
      tumKalemler.push(Object.assign({}, ik, { _mahalAd: mahal.ad }));
    });
  });
  if (!body) return;
  if (tumKalemler.length === 0) {
    body.innerHTML = '<div class="hiy-empty"><div class="hiy-empty-icon">📋</div><div class="hiy-empty-title">Bu katta henüz iş kalemi yok</div><div class="hiy-empty-desc">Mahal seçerek veya "İş Kalemi Ekle" butonunu kullanarak ekleyin.</div></div>';
    return;
  }
  body.innerHTML = '<div class="hiy-table-wrap">' + _hiyTabelaHtml(tumKalemler, false) + '</div>';
}

function _hiyMahalIcerigiGoster(bina, kat, mahal) {
  _hiyCepheVaryasyonBarGoster(false);
  var body = document.getElementById('hiyCtxBody');
  if (body) body.classList.remove('gorsel-mod');
  if (!body) return;
  var kalemler = mahal.is_kalemleri || [];
  if (kalemler.length === 0) {
    body.innerHTML = '<div class="hiy-empty">'
      + '<div class="hiy-empty-icon">📋</div>'
      + '<div class="hiy-empty-title">Bu mahalde henüz iş kalemi yok</div>'
      + '<div class="hiy-empty-desc">Sağ üstteki butonları kullanarak ekleyin.</div>'
      + '<div style="display:flex;gap:10px;margin-top:8px;">'
      + '<button class="hiy-btn hiy-btn-secondary" onclick="hiyExcelModalAc()">Excel\'den Yükle</button>'
      + '<button class="hiy-btn hiy-btn-primary" onclick="hiyIsKalemiModalAc(null,' + mahal.id + ',null)">+ iş Kalemi Ekle</button>'
      + '</div></div>';
    return;
  }
  body.innerHTML = '<div class="hiy-table-wrap">' + _hiyTabelaHtml(kalemler, false) + '</div>';
}

/* ══════════════════════════════════════════════
   TABLO HTML
══════════════════════════════════════════════ */
function _hiyTabelaHtml(kalemler, mahalSutun) {
  var mahalTh = mahalSutun ? '<th>Mahal</th>' : '';
  var rows = '';
  kalemler.forEach(function (ik) {
    var badge = _hiyBadge(ik.durum);
    var ilerleme = ik.son_ilerleme_yuzde != null ? ik.son_ilerleme_yuzde : 0;
    var w = Math.min(100, Math.max(0, ilerleme));
    var mahalTd = mahalSutun ? '<td>' + _escH(ik._mahalAd || '-') + '</td>' : '';
    rows += '<tr>'
      + '<td style="color:#94A3B8;font-size:11px;">' + _escH(ik.poz_no || '—') + '</td>'
      + '<td style="font-weight:500;max-width:180px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="' + _escH(ik.tanim) + '">' + _escH(ik.tanim) + '</td>'
      + mahalTd
      + '<td>' + _escH(_hiyBirimDuzelt(ik.birim)) + '</td>'
      + '<td style="text-align:right;">' + _hiyNum(ik.metraj) + '</td>'
      + '<td style="text-align:right;">' + _hiyPara(ik.birim_fiyat_tl) + '</td>'
      + '<td style="text-align:right;font-weight:600;">' + _hiyPara(ik.toplam_fiyat_tl) + '</td>'
      + '<td><div style="display:flex;align-items:center;gap:5px;">'
      + '<div class="hiy-progress-wrap"><div class="hiy-progress-bar" style="width:' + w + '%"></div></div>'
      + '<span class="hiy-progress-pct" onclick="hiyIlerlemeModalAc(' + ik.id + ')" style="cursor:pointer;" title="ilerleme geçmişi">%' + ilerleme + '</span>'
      + '</div></td>'
      + '<td>' + badge + '</td>'
      + '<td><div class="hiy-row-actions">'
      + '<button class="hiy-icon-btn" title="Malzeme Fiyatları" data-tanim="' + _escH(ik.tanim) + '" data-metraj="' + (ik.metraj || 0) + '" onclick="hiyMalzemeBolumuGoster(' + ik.id + ',this.dataset.tanim,parseFloat(this.dataset.metraj||0))">💰</button>'
      + '<button class="hiy-icon-btn" title="Düzenle" onclick="hiyIsKalemiDuzenle(' + ik.id + ')">✏️</button>'
      + '<button class="hiy-icon-btn danger" title="Sil" onclick="hiyIsKalemiSil(' + ik.id + ')">🗑️</button>'
      + '</div></td>'
      + '</tr>';
  });
  return '<table class="hiy-table"><thead><tr>'
    + '<th>Poz No</th><th>Tanım</th>'
    + mahalTh
    + '<th>Birim</th>'
    + '<th style="text-align:right;">Metraj</th>'
    + '<th style="text-align:right;">Birim Fiyat</th>'
    + '<th style="text-align:right;">Toplam</th>'
    + '<th>ilerleme</th><th>Durum</th><th></th>'
    + '</tr></thead><tbody>' + rows + '</tbody></table>';
}

function _hiyBadge(durum) {
  var map = {
    planli: ['hiy-badge-planli', 'Planlı'],
    devam_eden: ['hiy-badge-devam', 'Devam Ediyor'],
    tamamlandi: ['hiy-badge-tamamlandi', 'Tamamlandı'],
    iptal: ['hiy-badge-iptal', 'iptal'],
  };
  var kv = map[durum] || ['hiy-badge-planli', durum || '—'];
  return '<span class="hiy-badge ' + kv[0] + '">' + kv[1] + '</span>';
}

/* ══════════════════════════════════════════════
   MODAL YARDIMCILARI
══════════════════════════════════════════════ */
function hiyModalAc(baslik) {
  document.getElementById('hiyMdBaslik').textContent = baslik;
  var btn = document.getElementById('hiyMdKaydetBtn');
  if (btn) { btn.disabled = false; btn.textContent = 'Kaydet'; }
  var ov = document.getElementById('hiyMdOv');
  ov.style.display = 'flex';
  requestAnimationFrame(function () { ov.classList.add('active'); });
}

function hiyModalKapat() {
  var ov = document.getElementById('hiyMdOv');
  if (!ov) return;
  ov.classList.remove('active');
  setTimeout(function () { ov.style.display = 'none'; }, 260);
  _hiy.modalTip = null; _hiy.modalDuzenleId = null;
  _hiy.modalParentId = null; _hiy._isKalemiMahalId = null; _hiy._isKalemiSantiyeId = null;
}

function _hiyField(label, id, type, value, extra) {
  value = value == null ? '' : String(value);
  extra = extra || '';
  return '<label class="hiy-field-label">' + label + '</label>'
    + '<input type="' + (type || 'text') + '" class="hiy-field-input" id="' + id + '" value="' + _escH(value) + '" ' + extra + '>';
}

function _hiySelect(label, id, opts, selected) {
  selected = selected || '';
  var optsHtml = opts.map(function (o) {
    return '<option value="' + o[0] + '"' + (o[0] === selected ? ' selected' : '') + '>' + o[1] + '</option>';
  }).join('');
  return '<label class="hiy-field-label">' + label + '</label>'
    + '<select class="hiy-field-select" id="' + id + '">' + optsHtml + '</select>';
}

function _hiyVal(id) { var el = document.getElementById(id); return el ? el.value : ''; }
function _hiyFloatVal(id) { var v = parseFloat(_hiyVal(id)); return isNaN(v) ? null : v; }
function _hiyIntVal(id) { var v = parseInt(_hiyVal(id)); return isNaN(v) ? null : v; }

/* ══════════════════════════════════════════════
   BiNA MODAL
══════════════════════════════════════════════ */
function hiyBinaModalAc(binaId, mevcut) {
  _hiy.modalTip = 'bina';
  _hiy.modalDuzenleId = binaId || null;
  hiyModalAc(binaId ? 'Bina Düzenle' : 'Yeni Bina Ekle');
  document.getElementById('hiyMdBody').innerHTML =
    _hiyField('Bina Adı *', 'hF_ad', 'text', mevcut && mevcut.ad || '', 'placeholder="ör: A Blok"')
    + _hiySelect('Bina Tipi', 'hF_bina_tipi', [['konut', 'Konut'], ['ticari', 'Ticari'], ['sanayi', 'Sanayi'], ['karma', 'Karma']], mevcut && mevcut.bina_tipi || 'konut')
    + _hiyField('Toplam Kat', 'hF_toplam_kat', 'number', mevcut && mevcut.toplam_kat || '', 'min="0" step="1" placeholder="isteğe bağlı"');
}

async function _hiyBinaKaydet() {
  var ad = _hiyVal('hF_ad').trim();
  if (!ad) { _hiyToast('Bina adı zorunludur.', 'warning'); return; }
  var body = { ad: ad, bina_tipi: _hiyVal('hF_bina_tipi') || 'konut', toplam_kat: _hiyIntVal('hF_toplam_kat') };
  try {
    if (_hiy.modalDuzenleId) {
      await _hiyPatch('/api/v2/binalar/' + _hiy.modalDuzenleId, body);
      _hiyToast('Bina güncellendi.', 'success');
    } else {
      await _hiyPost('/api/v2/santiye/' + _hiy.santiyeId + '/binalar', body);
      _hiyToast('Bina eklendi.', 'success');
    }
    hiyModalKapat(); await _hiyerarsiVeriYukle();
  } catch (e) { _hiyToast('Hata: ' + e.message, 'error'); }
}

function hiyBinaDuzenle(e, binaId) {
  e.stopPropagation();
  var bina = (_hiy.agac && _hiy.agac.binalar || []).find(function (b) { return b.id === binaId; });
  hiyBinaModalAc(binaId, bina);
}

async function hiyBinaSil(e, binaId) {
  e.stopPropagation();
  var bina = (_hiy.agac && _hiy.agac.binalar || []).find(function (b) { return b.id === binaId; });
  var ad = bina ? bina.ad : 'bu bina';
  if (!confirm('"' + ad + '" ve altındaki tüm katları, mahalleri ve iş kalemlerini silmek istediğinize emin misiniz?')) return;
  try {
    await _hiyDelete('/api/v2/binalar/' + binaId);
    _hiyToast('Bina silindi.', 'success');
    await _hiyerarsiVeriYukle();
    var bc = document.getElementById('hiyBc');
    if (bc) bc.innerHTML = '<span class="hiy-breadcrumb-item">🏗️ ' + _escH(_hiy.santiyeAd) + '</span>';
    var body = document.getElementById('hiyCtxBody');
    if (body) body.innerHTML = '<div class="hiy-empty"><div class="hiy-empty-title">Sol panelden bir konum seçin</div></div>';
    var akt = document.getElementById('hiyCtxAkt');
    if (akt) akt.innerHTML = '';
  } catch (e) { _hiyToast('Silinemedi: ' + e.message, 'error'); }
}

/* ══════════════════════════════════════════════
   KAT MODAL
══════════════════════════════════════════════ */
function hiyKatModalAc(binaId, katId, mevcut) {
  _hiy.modalTip = 'kat';
  _hiy.modalDuzenleId = katId || null;
  _hiy.modalParentId = binaId;
  hiyModalAc(katId ? 'Kat Düzenle' : 'Yeni Kat Ekle');
  document.getElementById('hiyMdBody').innerHTML =
    _hiyField('Kat No *', 'hF_kat_no', 'number', mevcut && mevcut.kat_no != null ? mevcut.kat_no : '', 'step="1"')
    + _hiyField('Etiket', 'hF_etiket', 'text', mevcut && mevcut.etiket || '', 'placeholder="ör: Zemin Kat, 1. Normal Kat, Çatı"')
    + _hiyField('Brüt Alan (m²)', 'hF_brut_alan', 'number', mevcut && mevcut.brut_alan_m2 || '', 'min="0" step="any"');
}

async function _hiyKatKaydet() {
  var kat_no = _hiyIntVal('hF_kat_no');
  if (kat_no == null) { _hiyToast('Kat numarası zorunludur.', 'warning'); return; }
  var body = { kat_no: kat_no, etiket: _hiyVal('hF_etiket').trim() || null, brut_alan_m2: _hiyFloatVal('hF_brut_alan') };
  try {
    if (_hiy.modalDuzenleId) {
      await _hiyPatch('/api/v2/katlar/' + _hiy.modalDuzenleId, body);
      _hiyToast('Kat güncellendi.', 'success');
    } else {
      await _hiyPost('/api/v2/bina/' + _hiy.modalParentId + '/katlar', body);
      _hiyToast('Kat eklendi.', 'success');
    }
    hiyModalKapat(); await _hiyerarsiVeriYukle();
  } catch (e) { _hiyToast('Hata: ' + e.message, 'error'); }
}

function hiyKatDuzenle(e, katId, binaId) {
  e.stopPropagation();
  var bina = (_hiy.agac && _hiy.agac.binalar || []).find(function (b) { return b.id === binaId; });
  var kat = bina ? (bina.katlar || []).find(function (k) { return k.id === katId; }) : null;
  hiyKatModalAc(binaId, katId, kat);
}

async function hiyKatSil(e, katId) {
  e.stopPropagation();
  if (!confirm('Bu katı ve altındaki tüm mahalleri ve iş kalemlerini silmek istediğinize emin misiniz?')) return;
  try {
    await _hiyDelete('/api/v2/katlar/' + katId);
    _hiyToast('Kat silindi.', 'success');
    await _hiyerarsiVeriYukle();
  } catch (e) { _hiyToast('Silinemedi: ' + e.message, 'error'); }
}

/* ══════════════════════════════════════════════
   MAHAL MODAL
══════════════════════════════════════════════ */
function hiyMahalModalAc(katId, binaId, mahalId, mevcut) {
  _hiy.modalTip = 'mahal';
  _hiy.modalDuzenleId = mahalId || null;
  _hiy.modalParentId = katId;
  hiyModalAc(mahalId ? 'Mahal Düzenle' : 'Yeni Mahal Ekle');
  document.getElementById('hiyMdBody').innerHTML =
    _hiyField('Mahal Adı *', 'hF_ad', 'text', mevcut && mevcut.ad || '', 'placeholder="ör: Daire 1, Koridor"')
    + _hiySelect('Mahal Tipi', 'hF_mahal_tipi', [
      ['genel', 'Genel'], ['salon', 'Salon'], ['yatak_odasi', 'Yatak Odası'],
      ['banyo', 'Banyo'], ['mutfak', 'Mutfak'], ['koridor', 'Koridor'],
      ['merdiven', 'Merdiven'], ['depo', 'Depo'], ['ofis', 'Ofis'],
    ], mevcut && mevcut.mahal_tipi || 'genel')
    + _hiyField('Alan (m²)', 'hF_alan', 'number', mevcut && mevcut.alan_m2 || '', 'min="0" step="any"');
}

async function _hiyMahalKaydet() {
  var ad = _hiyVal('hF_ad').trim();
  if (!ad) { _hiyToast('Mahal adı zorunludur.', 'warning'); return; }
  var body = { ad: ad, mahal_tipi: _hiyVal('hF_mahal_tipi') || 'genel', alan_m2: _hiyFloatVal('hF_alan') };
  try {
    if (_hiy.modalDuzenleId) {
      await _hiyPatch('/api/v2/mahaller/' + _hiy.modalDuzenleId, body);
      _hiyToast('Mahal güncellendi.', 'success');
    } else {
      await _hiyPost('/api/v2/kat/' + _hiy.modalParentId + '/mahaller', body);
      _hiyToast('Mahal eklendi.', 'success');
    }
    hiyModalKapat(); await _hiyerarsiVeriYukle();
  } catch (e) { _hiyToast('Hata: ' + e.message, 'error'); }
}

function hiyMahalDuzenle(e, mahalId, katId, binaId) {
  e.stopPropagation();
  var bina = (_hiy.agac && _hiy.agac.binalar || []).find(function (b) { return b.id === binaId; });
  var kat = bina ? (bina.katlar || []).find(function (k) { return k.id === katId; }) : null;
  var mahal = kat ? (kat.mahaller || []).find(function (m) { return m.id === mahalId; }) : null;
  hiyMahalModalAc(katId, binaId, mahalId, mahal);
}

async function hiyMahalSil(e, mahalId) {
  e.stopPropagation();
  if (!confirm('Bu mahali ve altındaki tüm iş kalemlerini silmek istediğinize emin misiniz?')) return;
  try {
    await _hiyDelete('/api/v2/mahaller/' + mahalId);
    _hiyToast('Mahal silindi.', 'success');
    await _hiyerarsiVeriYukle();
  } catch (e) { _hiyToast('Silinemedi: ' + e.message, 'error'); }
}

/* ══════════════════════════════════════════════
   iÅ KALEMi MODAL
══════════════════════════════════════════════ */
// Autocomplete state
var _hiyAcTimer = null;
var _hiyAcSerbest = false;

function hiyIsKalemiModalAc(isKalemiId, mahalId, santiyeId, mevcut) {
  _hiy.modalTip = 'isKalemi';
  _hiy.modalDuzenleId = isKalemiId || null;
  _hiy._isKalemiMahalId = mahalId || null;
  _hiy._isKalemiSantiyeId = santiyeId || null;
  _hiyAcSerbest = !!isKalemiId; // Düzenleme modunda serbest giriş varsayılan
  hiyModalAc(isKalemiId ? 'iş Kalemi Düzenle' : 'Yeni iş Kalemi Ekle');

  var tanim = mevcut && mevcut.tanim || '';
  var katalogId = mevcut && mevcut.katalog_id || '';

  document.getElementById('hiyMdBody').innerHTML =
    _hiyField('Poz No', 'hF_poz', 'text', mevcut && mevcut.poz_no || '', 'placeholder="ör: 04.613/2A (opsiyonel)"')
    + _hiyTanimFieldHtml(tanim, !!isKalemiId)
    + '<input type="hidden" id="hF_katalog_id" value="' + _escH(String(katalogId)) + '">'
    + _hiySelect('Birim *', 'hF_birim', [['m²', 'm²'], ['m³', 'm³'], ['kg', 'kg'], ['mt', 'mt'], ['adet', 'adet'], ['ton', 'ton'], ['lt', 'lt'], ['takım', 'takım']], _hiyBirimDuzelt(mevcut && mevcut.birim) || 'm²')
    + _hiyField('Metraj *', 'hF_metraj', 'number', mevcut && mevcut.metraj || '0', 'min="0" step="any" oninput="hiyToplamHesapla()"')
    + _hiyField('Birim Fiyat (₺) *', 'hF_fiyat', 'number', mevcut && mevcut.birim_fiyat_tl || '0', 'min="0" step="0.01" oninput="hiyToplamHesapla()"')
    + '<div class="hiy-total-preview" id="hiyToplam"><span>Toplam Tutar</span><strong>0,00 ₺</strong></div>'
    + _hiySelect('Durum', 'hF_durum', [['planli', 'Planlı'], ['devam_eden', 'Devam Ediyor'], ['tamamlandi', 'Tamamlandı'], ['iptal', 'iptal']], mevcut && mevcut.durum || 'planli');

  hiyToplamHesapla();
  _hiyAcGuncelle();
}

function _hiyTanimFieldHtml(value, serbest) {
  var ph = serbest ? 'İş kalemi tanımı' : 'Katalogda ara veya yazarak giriş yap...';
  return '<label class="hiy-field-label">Tanım *</label>'
    + '<div class="hiy-ac-wrap">'
    + '<input type="text" class="hiy-field-input" id="hF_tanim" autocomplete="off"'
    + ' value="' + _escH(value) + '"'
    + ' placeholder="' + ph + '"'
    + ' oninput="_hiyTanimInput(this.value)"'
    + ' onkeydown="_hiyAcKeydown(event)"'
    + ' onfocus="if(!_hiyAcSerbest&&this.value.length>=2)_hiyAcGoster()">'
    + '<div class="hiy-ac-dropdown" id="hiyAcDropdown" style="display:none;"></div>'
    + '</div>'
    + '<div class="hiy-ac-toolbar">'
    + '<span class="hiy-ac-badge" id="hiyAcBadge" style="display:none;"></span>'
    + '<a href="#" class="hiy-ac-serbest-link" id="hiyAcSerbestLink"'
    + ' onclick="_hiySerbestGiris();return false;">Katalogda bulamadım, serbest giriş</a>'
    + '</div>';
}

function _hiyAcGuncelle() {
  var badge = document.getElementById('hiyAcBadge');
  var link = document.getElementById('hiyAcSerbestLink');
  var katalogId = _hiyVal('hF_katalog_id');
  if (!badge || !link) return;
  if (katalogId) {
    badge.style.display = 'inline-flex';
    badge.innerHTML = '📋 Katalogdan seçildi  <a href="#" onclick="_hiySerbest();return false;" style="color:#94a3b8;font-size:10px;text-decoration:none;">✕ temizle</a>';
    link.style.display = 'none';
  } else if (_hiyAcSerbest) {
    badge.style.display = 'inline-flex';
    badge.textContent = '✏️ Serbest giriş';
    link.style.display = 'none';
  } else {
    badge.style.display = 'none';
    link.style.display = 'inline';
  }
}

function _hiyTanimInput(val) {
  var hiddenId = document.getElementById('hF_katalog_id');
  if (hiddenId && hiddenId.value) {
    hiddenId.value = '';
    _hiyAcSerbest = false;
    _hiyAcGuncelle();
  }
  clearTimeout(_hiyAcTimer);
  if (_hiyAcSerbest || val.trim().length < 2) { _hiyAcKapat(); return; }
  _hiyAcTimer = setTimeout(function () { _hiyAcAra(val.trim()); }, 300);
}

async function _hiyAcAra(q) {
  var dd = document.getElementById('hiyAcDropdown');
  if (!dd) return;
  dd.style.display = 'block';
  dd.innerHTML = '<div class="hiy-ac-loading">Aranıyor…</div>';
  try {
    var token = localStorage.getItem('bai_token') || '';
    var res = await fetch('/api/katalog/ara?q=' + encodeURIComponent(q) + '&tip=is_kalemi', {
      headers: { 'Authorization': 'Bearer ' + token }
    });
    if (!res.ok) throw new Error('Sunucu hatası');
    var data = await res.json();
    var items = (data.sonuclar || []).filter(function (s) { return s.tip === 'is_kalemi'; });
    _hiyAcListeGoster(items);
  } catch (e) {
    if (dd) dd.innerHTML = '<div class="hiy-ac-empty">Arama başarısız</div>';
  }
}

function _hiyAcListeGoster(items) {
  var dd = document.getElementById('hiyAcDropdown');
  if (!dd) return;
  if (!items || items.length === 0) {
    dd.style.display = 'block';
    dd.innerHTML = '<div class="hiy-ac-empty">Sonuç bulunamadı</div>'
      + '<div class="hiy-ac-serbest-row" onclick="_hiySerbestGiris()">✏️ Serbest giriş olarak devam et</div>';
    return;
  }
  var html = items.map(function (item) {
    var safeId = Number(item.id);
    var safePoz = _escH(item.poz_no || '');
    var safeAd = _escH(item.ad);
    var safeBirim = _escH(item.birim || '');
    return '<div class="hiy-ac-item" tabindex="-1"'
      + ' onmousedown="_hiyAcSec(' + safeId + ');return false;"'
      + ' data-id="' + safeId + '" data-poz="' + safePoz + '" data-ad="' + safeAd + '" data-birim="' + safeBirim + '">'
      + '<div class="hiy-ac-item-main">'
      + '<span class="hiy-ac-poz">' + safePoz + '</span>'
      + '<span class="hiy-ac-ad">' + safeAd + '</span>'
      + '</div>'
      + '<span class="hiy-ac-birim">' + safeBirim + '</span>'
      + '</div>';
  }).join('');
  html += '<div class="hiy-ac-serbest-row" onclick="_hiySerbestGiris()">✏️ Serbest giriş olarak devam et</div>';
  dd.style.display = 'block';
  dd.innerHTML = html;
}

function _hiyAcSec(id) {
  var dd = document.getElementById('hiyAcDropdown');
  if (!dd) return;
  var item = dd.querySelector('[data-id="' + id + '"]');
  if (!item) return;
  var poz = item.dataset.poz || '';
  var ad = item.dataset.ad || '';
  var birim = item.dataset.birim || '';
  _hiyAcKapat();
  var tInput = document.getElementById('hF_tanim');
  if (tInput) tInput.value = ad;
  var pInput = document.getElementById('hF_poz');
  if (pInput) pInput.value = poz;
  var bSel = document.getElementById('hF_birim');
  if (bSel && birim) {
    var b = _hiyBirimDuzelt(birim);
    var found = false;
    for (var i = 0; i < bSel.options.length; i++) {
      if (bSel.options[i].value === b) { bSel.value = b; found = true; break; }
    }
    if (!found) {
      var opt = document.createElement('option');
      opt.value = b; opt.text = b;
      bSel.appendChild(opt);
      bSel.value = b;
    }
  }
  var hiddenId = document.getElementById('hF_katalog_id');
  if (hiddenId) hiddenId.value = String(id);
  _hiyAcSerbest = false;
  _hiyAcGuncelle();
}

function _hiySerbestGiris() {
  _hiyAcKapat();
  _hiyAcSerbest = true;
  var hiddenId = document.getElementById('hF_katalog_id');
  if (hiddenId) hiddenId.value = '';
  _hiyAcGuncelle();
  var tInput = document.getElementById('hF_tanim');
  if (tInput) { tInput.placeholder = 'İş kalemi tanımı'; tInput.focus(); }
}

function _hiySerbest() {
  var hiddenId = document.getElementById('hF_katalog_id');
  if (hiddenId) hiddenId.value = '';
  _hiyAcSerbest = false;
  _hiyAcGuncelle();
  var tInput = document.getElementById('hF_tanim');
  if (tInput) { tInput.value = ''; tInput.placeholder = 'Katalogda ara veya yazarak giriş yap...'; tInput.focus(); }
}

function _hiyAcKapat() {
  var dd = document.getElementById('hiyAcDropdown');
  if (dd) dd.style.display = 'none';
}

function _hiyAcKeydown(e) {
  var dd = document.getElementById('hiyAcDropdown');
  if (!dd || dd.style.display === 'none') return;
  var items = dd.querySelectorAll('.hiy-ac-item');
  var focused = dd.querySelector('.hiy-ac-item:focus');
  var idx = -1;
  items.forEach(function (el, i) { if (el === focused) idx = i; });
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    var next = items[idx + 1] || items[0];
    if (next) next.focus();
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    var prev = items[idx - 1] || items[items.length - 1];
    if (prev) prev.focus();
  } else if (e.key === 'Escape') {
    _hiyAcKapat();
  } else if (e.key === 'Enter' && focused) {
    e.preventDefault();
    focused.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
  }
}

function hiyToplamHesapla() {
  var m = parseFloat(_hiyVal('hF_metraj')) || 0;
  var f = parseFloat(_hiyVal('hF_fiyat')) || 0;
  var el = document.getElementById('hiyToplam');
  if (el) el.innerHTML = '<span>Toplam Tutar</span><strong>' + _hiyPara(m * f) + '</strong>';
}

async function _hiyIsKalemiKaydet() {
  var tanim = _hiyVal('hF_tanim').trim();
  if (!tanim) { _hiyToast('Tanım zorunludur.', 'warning'); return; }
  var metraj = _hiyFloatVal('hF_metraj');
  if (metraj == null || metraj < 0) { _hiyToast('Geçerli bir metraj girin.', 'warning'); return; }
  var birim_fiyat_tl = _hiyFloatVal('hF_fiyat');
  if (birim_fiyat_tl == null || birim_fiyat_tl < 0) { _hiyToast('Geçerli bir birim fiyat girin.', 'warning'); return; }
  var katalogIdStr = _hiyVal('hF_katalog_id').trim();
  var body = {
    poz_no: _hiyVal('hF_poz').trim() || null,
    tanim: tanim,
    birim: _hiyBirimDuzelt(_hiyVal('hF_birim')) || 'm²',
    metraj: metraj,
    birim_fiyat_tl: birim_fiyat_tl,
    durum: _hiyVal('hF_durum') || 'planli',
  };
  if (katalogIdStr) body.katalog_id = parseInt(katalogIdStr, 10);
  try {
    if (_hiy.modalDuzenleId) {
      await _hiyPatch('/api/v2/is-kalemleri/' + _hiy.modalDuzenleId, body);
      _hiyToast('iş kalemi güncellendi.', 'success');
    } else if (_hiy._isKalemiMahalId) {
      await _hiyPost('/api/v2/mahal/' + _hiy._isKalemiMahalId + '/is-kalemleri', body);
      _hiyToast('iş kalemi eklendi.', 'success');
    } else {
      await _hiyPost('/api/v2/santiye/' + _hiy.santiyeId + '/is-kalemleri', body);
      _hiyToast('iş kalemi eklendi.', 'success');
    }
    hiyModalKapat();
    await _hiyerarsiVeriYukle();
    _hiySeciliYenile();
  } catch (e) { _hiyToast('Hata: ' + e.message, 'error'); }
}
async function hiyIsKalemiDuzenle(isKalemiId) {
  var mevcut = null;
  if (_hiy.agac) {
    outer: for (var i = 0; i < (_hiy.agac.binalar || []).length; i++) {
      var bina = _hiy.agac.binalar[i];
      for (var j = 0; j < (bina.katlar || []).length; j++) {
        var kat = bina.katlar[j];
        for (var k = 0; k < (kat.mahaller || []).length; k++) {
          var mahal = kat.mahaller[k];
          var found = (mahal.is_kalemleri || []).find(function (ik) { return ik.id === isKalemiId; });
          if (found) { mevcut = found; break outer; }
        }
      }
    }
    if (!mevcut) mevcut = (_hiy.agac.mahalsiz_is_kalemleri || []).find(function (ik) { return ik.id === isKalemiId; });
  }
  hiyIsKalemiModalAc(isKalemiId, null, null, mevcut);
}

async function hiyIsKalemiSil(isKalemiId) {
  if (!confirm('Bu iş kalemini silmek istediğinize emin misiniz?')) return;
  try {
    await _hiyDelete('/api/v2/is-kalemleri/' + isKalemiId);
    _hiyToast('iş kalemi silindi.', 'success');
    await _hiyerarsiVeriYukle();
    _hiySeciliYenile();
  } catch (e) { _hiyToast('Silinemedi: ' + e.message, 'error'); }
}

function _hiySeciliYenile() {
  // Seçili konumu yenile (veri yüklendikten sonra çağrılır)
  var s = _hiy.secili;
  if (!s || !_hiy.agac) return;
  if (s.tip === 'mahal') {
    var bina = (_hiy.agac.binalar || []).find(function (b) { return b.id === s.bina.id; });
    var kat = bina ? (bina.katlar || []).find(function (k) { return k.id === s.kat.id; }) : null;
    var mahal = kat ? (kat.mahaller || []).find(function (m) { return m.id === s.id; }) : null;
    if (mahal) _hiyMahalIcerigiGoster(bina, kat, mahal);
  } else if (s.tip === 'kat') {
    var bina = (_hiy.agac.binalar || []).find(function (b) { return b.id === s.bina.id; });
    var kat = bina ? (bina.katlar || []).find(function (k) { return k.id === s.id; }) : null;
    if (kat) _hiyKatIcerigiGoster(bina, kat);
  } else if (s.tip === 'bina') {
    var bina = (_hiy.agac.binalar || []).find(function (b) { return b.id === s.id; });
    if (bina) _hiyBinaIcerigiGoster(bina);
  }
}

/* ══════════════════════════════════════════════
   iLERLEME MODAL
══════════════════════════════════════════════ */
async function hiyIlerlemeModalAc(isKalemiId) {
  _hiy.modalTip = 'ilerleme';
  _hiy.modalParentId = isKalemiId;
  hiyModalAc('ilerleme Kaydı');

  var bugun = new Date().toISOString().slice(0, 10);
  document.getElementById('hiyMdBody').innerHTML =
    '<div id="hiyIlLst"><div class="hiy-loading" style="padding:16px 0;"><div class="hiy-spinner"></div></div></div>'
    + '<hr style="margin:14px 0;border:none;border-top:1px solid #E2E8F0;">'
    + '<div style="font-size:11px;font-weight:700;color:#374151;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.05em;">Yeni Kayıt Ekle</div>'
    + _hiyField('Yüzde (%) *', 'hF_yuzde', 'number', '', 'min="0" max="100" step="0.5" placeholder="0 — 100"')
    + _hiyField('Tarih *', 'hF_tarih', 'date', bugun)
    + _hiyField('Notlar', 'hF_notlar', 'text', '', 'placeholder="isteğe bağlı"');

  // Geçmiş kayıtları yükle
  try {
    var veri = await _hiyGet('/api/v2/is-kalemleri/' + isKalemiId + '/ilerleme');
    var kayitlar = veri.ilerleme_kayitlari || [];
    var kap = document.getElementById('hiyIlLst');
    if (kap) {
      if (kayitlar.length === 0) {
        kap.innerHTML = '<div style="font-size:12px;color:#94A3B8;padding:4px 0;">Henüz ilerleme kaydı yok.</div>';
      } else {
        var rows = kayitlar.map(function (k) {
          return '<div class="hiy-ilerleme-row">'
            + '<span class="hiy-ilerleme-yuzde">%' + k.yuzde + '</span>'
            + '<span class="hiy-ilerleme-tarih">' + _escH(k.tarih) + '</span>'
            + '<span class="hiy-ilerleme-notlar">' + _escH(k.notlar || '') + '</span>'
            + '</div>';
        }).join('');
        kap.innerHTML = '<div style="font-size:11px;font-weight:700;color:#374151;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.05em;">Geçmiş</div>'
          + '<div class="hiy-ilerleme-list">' + rows + '</div>';
      }
    }
  } catch (e) {
    var kap = document.getElementById('hiyIlLst');
    if (kap) kap.innerHTML = '<div style="color:#DC2626;font-size:12px;">Yüklenemedi: ' + _escH(e.message) + '</div>';
  }
}

async function _hiyIlerlemeKaydet() {
  var yuzde = _hiyFloatVal('hF_yuzde');
  var tarih = _hiyVal('hF_tarih');
  if (yuzde == null || yuzde < 0 || yuzde > 100) { _hiyToast('Yüzde 0-100 arasında olmalıdır.', 'warning'); return; }
  if (!tarih) { _hiyToast('Tarih zorunludur.', 'warning'); return; }
  var body = { yuzde: yuzde, tarih: tarih, notlar: _hiyVal('hF_notlar').trim() || null };
  try {
    await _hiyPost('/api/v2/is-kalemleri/' + _hiy.modalParentId + '/ilerleme', body);
    _hiyToast('ilerleme kaydedildi.', 'success');
    hiyModalKapat();
    await _hiyerarsiVeriYukle();
    _hiySeciliYenile();
  } catch (e) { _hiyToast('Hata: ' + e.message, 'error'); }
}

/* ══════════════════════════════════════════════
   EXCEL MODAL
══════════════════════════════════════════════ */
function hiyExcelModalAc() {
  _hiy.modalTip = 'excel';
  hiyModalAc("Excel'den iş Kalemi Yükle");
  document.getElementById('hiyMdBody').innerHTML =
    '<div style="margin-bottom:14px;padding:13px;background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;font-size:12px;color:#64748B;line-height:1.6;">'
    + '<div style="font-weight:700;color:#374151;margin-bottom:5px;">Beklenen Sütun Başlıkları (1. satır):</div>'
    + '<div><b>Zorunlu:</b> poz_no &nbsp;|&nbsp; tanim &nbsp;|&nbsp; birim &nbsp;|&nbsp; metraj &nbsp;|&nbsp; birim_fiyat</div>'
    + '<div style="margin-top:4px;"><b>Opsiyonel:</b> bina_adi &nbsp;|&nbsp; kat_no &nbsp;|&nbsp; mahal_adi</div>'
    + '<div style="margin-top:4px;color:#94A3B8;">Opsiyonel sütunlar varsa metraj yapısı otomatik oluşturulur.</div>'
    + '</div>'
    + '<label class="hiy-field-label">Excel Dosyası (.xlsx) *</label>'
    + '<input type="file" class="hiy-field-input" id="hF_excel" accept=".xlsx" style="padding:8px;">'
    + '<div id="hiyExcelSonuc"></div>';
}

async function _hiyExcelKaydet() {
  var fileInput = document.getElementById('hF_excel');
  if (!fileInput || !fileInput.files || !fileInput.files.length) {
    _hiyToast('Lütfen bir Excel dosyası seçin.', 'warning'); return;
  }
  var formData = new FormData();
  formData.append('file', fileInput.files[0]);

  var btn = document.getElementById('hiyMdKaydetBtn');
  if (btn) { btn.disabled = true; btn.textContent = 'Yükleniyor…'; }

  try {
    var r = await fetch(
      '/api/v2/santiye/' + _hiy.santiyeId + '/is-kalemleri/excel-import',
      { method: 'POST', headers: { 'Authorization': 'Bearer ' + _hiyToken() }, body: formData }
    );
    var sonuc = await r.json();
    var div = document.getElementById('hiyExcelSonuc');
    if (div) {
      var cls = sonuc.hatali > 0 ? 'partial' : 'success';
      var html = '<div class="hiy-excel-result ' + cls + '">';
      html += '<div><strong>' + sonuc.basarili + '</strong> iş kalemi başarıyla yüklendi.';
      if (sonuc.hatali > 0) html += ' <strong>' + sonuc.hatali + '</strong> satır hatalı.';
      html += '</div>';
      if (sonuc.hatalar && sonuc.hatalar.length > 0) {
        html += '<div class="hiy-excel-errors">';
        sonuc.hatalar.forEach(function (h) {
          html += '<div class="hiy-excel-error-row">Satır ' + h.satir + ': ' + _escH(h.sebep) + '</div>';
        });
        html += '</div>';
      }
      html += '</div>';
      div.innerHTML = html;
    }
    if (sonuc.basarili > 0) {
      await _hiyerarsiVeriYukle();
      _hiyToast(sonuc.basarili + ' iş kalemi yüklendi.', 'success');
    }
  } catch (e) {
    _hiyToast('Yükleme hatası: ' + e.message, 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = 'Kaydet'; }
  }
}

/* ══════════════════════════════════════════════
   MODAL KAYDET — DISPATCHER
══════════════════════════════════════════════ */
function hiyModalKaydet() {
  var tip = _hiy.modalTip;
  if (tip === 'bina') _hiyBinaKaydet();
  else if (tip === 'kat') _hiyKatKaydet();
  else if (tip === 'mahal') _hiyMahalKaydet();
  else if (tip === 'isKalemi') _hiyIsKalemiKaydet();
  else if (tip === 'ilerleme') _hiyIlerlemeKaydet();
  else if (tip === 'excel') _hiyExcelKaydet();
  else if (tip === 'malzemeEkle') _hiyMalzemeEkleKaydet();
  else if (tip === 'malzemeOner') _hiyMalzemeOnerEkle();
}

/* ══════════════════════════════════════════════
   MOBiL PANEL
══════════════════════════════════════════════ */
/* ═══════════════════════════════════════════════════════
   MALZEME FİYATLARI BÖLÜMÜ
═══════════════════════════════════════════════════════ */

async function hiyMalzemeBolumuGoster(isKalemiId, isKalemiAdi) {
  var mevcut = document.getElementById('hiyMalzemePanel');
  if (mevcut) {
    if (mevcut.dataset.isKalemiId === String(isKalemiId)) { mevcut.remove(); return; }
    mevcut.remove();
  }
  var panel = document.createElement('div');
  panel.id = 'hiyMalzemePanel';
  panel.dataset.isKalemiId = String(isKalemiId);
  panel.className = 'hiy-mal-panel';
  panel.innerHTML =
    '<div class="hiy-mal-header">'
    + '<span class="hiy-mal-baslik">Malzeme Fiyatları — ' + _escH(isKalemiAdi) + '</span>'
    + '<div class="hiy-mal-header-btns">'
    + '<button class="hiy-btn-sm hiy-btn-secondary" onclick="hiyMalzemeOnerilen(' + isKalemiId + ')">💡 Önerilen Malzemeleri Ekle</button>'
    + '<button class="hiy-btn-sm hiy-btn-primary" onclick="hiyMalzemeEkleModalAc(' + isKalemiId + ')">+ Malzeme Ekle</button>'
    + '<button class="hiy-icon-btn" title="Kapat" onclick="document.getElementById(\'hiyMalzemePanel\').remove()">✕</button>'
    + '</div></div>'
    + '<div id="hiyMalIcerik"><div class="hiy-loading" style="padding:20px 0;"><div class="hiy-spinner"></div></div></div>';
  var ctxBody = document.getElementById('hiyCtxBody');
  if (ctxBody) ctxBody.appendChild(panel);
  await _hiyMalzemeVeriYukle(isKalemiId);
}

async function _hiyMalzemeVeriYukle(isKalemiId) {
  var panel = document.getElementById('hiyMalzemePanel');
  if (!panel || panel.dataset.isKalemiId !== String(isKalemiId)) return;
  var icerik = document.getElementById('hiyMalIcerik');
  try {
    var data = await _hiyGet('/api/v2/is-kalemleri/' + isKalemiId + '/malzemeler');
    if (!panel.isConnected) return;
    if (icerik) icerik.innerHTML = _hiyMalzemeIcerikHtml(data, isKalemiId);
  } catch (e) {
    if (icerik) icerik.innerHTML = '<div style="color:#DC2626;padding:12px;">Yüklenemedi: ' + _escH(e.message) + '</div>';
  }
}

function _hiyMalzemeIcerikHtml(data, isKalemiId) {
  var malzemeler = data.malzemeler || [];
  var html = '';
  if (malzemeler.length === 0) {
    html = '<div class="hiy-mal-bos">Henüz malzeme eklenmedi. '
      + '<a href="#" onclick="hiyMalzemeOnerilen(' + isKalemiId + ');return false;">Önerilen malzemeleri eklemek için tıklayın.</a>'
      + '</div>';
  } else {
    html = '<div class="hiy-table-wrap"><table class="hiy-table">'
      + '<thead><tr>'
      + '<th>Malzeme</th>'
      + '<th style="text-align:right;">Miktar</th>'
      + '<th>Birim</th>'
      + '<th style="text-align:right;">Birim Fiyat</th>'
      + '<th style="text-align:right;">Toplam</th>'
      + '<th>Fark</th>'
      + '<th></th>'
      + '</tr></thead><tbody>';

    malzemeler.forEach(function (m) {
      var fiyatCell;
      if (m.kullanici_fiyat != null) {
        fiyatCell = '<strong title="Kullanıcı fiyatı">' + _hiyPara(m.kullanici_fiyat) + '</strong>';
      } else if (m.bolgesel_fiyat != null) {
        fiyatCell = '<em class="hiy-mal-piyasa" title="Piyasa tahmini">' + _hiyPara(m.bolgesel_fiyat) + '</em>';
      } else {
        fiyatCell = '<span style="color:#94A3B8;">—</span>';
      }

      var farkCell;
      if (m.fark_yuzdesi != null) {
        if (m.fark_yuzdesi > 0) farkCell = '<span class="hiy-mal-fark-kirmizi">+%' + m.fark_yuzdesi + '</span>';
        else if (m.fark_yuzdesi < 0) farkCell = '<span class="hiy-mal-fark-yesil">%' + m.fark_yuzdesi + '</span>';
        else farkCell = '<span class="hiy-mal-fark-gri">—</span>';
      } else {
        farkCell = '<span class="hiy-mal-fark-gri">—</span>';
      }

      html += '<tr>'
        + '<td><span class="hiy-mal-ad">' + _escH(m.malzeme_ad) + '</span></td>'
        + '<td style="text-align:right;">'
        + '<span class="hiy-mal-miktar-val" onclick="hiyMalMiktarDuzenle(' + isKalemiId + ',' + m.malzeme_id + ',this)">'
        + _hiyNum(m.miktar) + '</span></td>'
        + '<td>' + _escH(m.birim || '') + '</td>'
        + '<td style="text-align:right;">' + fiyatCell + '</td>'
        + '<td style="text-align:right;font-weight:600;">'
        + (m.toplam_maliyet != null ? _hiyPara(m.toplam_maliyet) : '—') + '</td>'
        + '<td>' + farkCell + '</td>'
        + '<td><button class="hiy-icon-btn danger" title="Kaldır" '
        + 'onclick="hiyMalzemeSil(' + isKalemiId + ',' + m.malzeme_id + ')">✕</button></td>'
        + '</tr>';
    });

    html += '</tbody></table></div>';

    var farkOzetHtml = '';
    if (data.toplam_fark_yuzdesi != null) {
      if (data.toplam_fark_yuzdesi > 0)
        farkOzetHtml = ' <span class="hiy-mal-fark-kirmizi">+%' + data.toplam_fark_yuzdesi + ' piyasa üstü</span>';
      else if (data.toplam_fark_yuzdesi < 0)
        farkOzetHtml = ' <span class="hiy-mal-fark-yesil">%' + data.toplam_fark_yuzdesi + ' piyasa altı</span>';
    }
    html += '<div class="hiy-mal-ozet">'
      + '<span>Piyasa Tahmini: <strong>' + _hiyPara(data.toplam_bolgesel_maliyet) + '</strong></span>'
      + '<span>Gerçek Maliyet: <strong>' + _hiyPara(data.toplam_kullanici_maliyet) + '</strong>' + farkOzetHtml + '</span>'
      + '</div>';
  }
  return html;
}

function hiyMalMiktarDuzenle(isKalemiId, malzemeId, el) {
  var mevcutDeger = parseFloat(String(el.textContent).replace(',', '.')) || 1;
  var inp = document.createElement('input');
  inp.type = 'number';
  inp.value = mevcutDeger;
  inp.min = '0';
  inp.step = 'any';
  inp.className = 'hiy-mal-miktar-inp';
  inp.onkeydown = function (e) {
    if (e.key === 'Enter') inp.blur();
    if (e.key === 'Escape') { if (inp.parentNode) inp.parentNode.replaceChild(el, inp); }
  };
  inp.onblur = async function () {
    var yeni = parseFloat(inp.value);
    if (inp.parentNode) inp.parentNode.replaceChild(el, inp);
    if (isNaN(yeni) || yeni < 0) return;
    el.textContent = _hiyNum(yeni);
    try {
      await _hiyPut('/api/v2/is-kalemleri/' + isKalemiId + '/malzeme/' + malzemeId, { miktar: yeni });
      _hiyToast('Miktar güncellendi.', 'success');
      await _hiyMalzemeVeriYukle(isKalemiId);
    } catch (e) { _hiyToast('Güncellenemedi: ' + e.message, 'error'); }
  };
  el.parentNode.replaceChild(inp, el);
  inp.select();
  inp.focus();
}

async function hiyMalzemeSil(isKalemiId, malzemeId) {
  if (!confirm('Bu malzemeyi kaldırmak istediğinize emin misiniz?')) return;
  try {
    await _hiyDelete('/api/v2/is-kalemleri/' + isKalemiId + '/malzeme/' + malzemeId);
    _hiyToast('Malzeme kaldırıldı.', 'success');
    await _hiyMalzemeVeriYukle(isKalemiId);
  } catch (e) { _hiyToast('Kaldırılamadı: ' + e.message, 'error'); }
}

async function hiyMalzemeEkleModalAc(isKalemiId) {
  _hiy.modalTip = 'malzemeEkle';
  _hiy.modalParentId = isKalemiId;
  _hiy._malKatalog = [];
  hiyModalAc('Malzeme Ekle');
  document.getElementById('hiyMdBody').innerHTML =
    '<input type="text" id="hiyMalAra" class="hiy-field-input" placeholder="Malzeme ara..." oninput="hiyMalFiltrele()" style="margin-bottom:10px;">'
    + '<div id="hiyMalListKap" class="hiy-mal-liste-kap"><div class="hiy-loading"><div class="hiy-spinner"></div></div></div>'
    + _hiyField('Miktar *', 'hF_malMiktar', 'number', '1', 'min="0" step="any"');
  try {
    var veri = await _hiyGet('/api/v2/malzemeler-katalog');
    _hiy._malKatalog = veri.malzemeler || [];
    hiyMalFiltrele();
  } catch (e) {
    var kap = document.getElementById('hiyMalListKap');
    if (kap) kap.innerHTML = '<div style="color:#DC2626;font-size:12px;">Yüklenemedi: ' + _escH(e.message) + '</div>';
  }
}

function hiyMalFiltrele() {
  var ara = (_hiyVal('hiyMalAra') || '').toLowerCase().trim();
  var katalog = _hiy._malKatalog || [];
  var liste = ara
    ? katalog.filter(function (m) { return m.ad.toLowerCase().includes(ara) || m.kategori.toLowerCase().includes(ara); })
    : katalog;
  var kap = document.getElementById('hiyMalListKap');
  if (!kap) return;
  if (liste.length === 0) {
    kap.innerHTML = '<div style="color:#94A3B8;font-size:12px;padding:8px 0;">Sonuç bulunamadı.</div>';
    return;
  }
  kap.innerHTML = liste.map(function (m) {
    return '<label class="hiy-mal-liste-satir">'
      + '<input type="radio" name="hiyMalSec" value="' + m.id + '"> '
      + '<span class="hiy-mal-liste-ad">' + _escH(m.ad) + '</span>'
      + ' <span class="hiy-mal-liste-birim">(' + _escH(m.birim) + ')</span>'
      + '</label>';
  }).join('');
}

async function _hiyMalzemeEkleKaydet() {
  var secili = document.querySelector('input[name="hiyMalSec"]:checked');
  if (!secili) { _hiyToast('Lütfen bir malzeme seçin.', 'warning'); return; }
  var malzemeId = parseInt(secili.value);
  var miktar = _hiyFloatVal('hF_malMiktar');
  if (miktar == null || miktar <= 0) { _hiyToast('Geçerli bir miktar girin.', 'warning'); return; }
  var m = (_hiy._malKatalog || []).find(function (x) { return x.id === malzemeId; });
  try {
    await _hiyPost('/api/v2/is-kalemleri/' + _hiy.modalParentId + '/malzeme-ekle', {
      malzeme_id: malzemeId, miktar: miktar, birim: m ? m.birim : null,
    });
    _hiyToast('Malzeme eklendi.', 'success');
    hiyModalKapat();
    await _hiyMalzemeVeriYukle(_hiy.modalParentId);
  } catch (e) { _hiyToast('Hata: ' + e.message, 'error'); }
}

async function hiyMalzemeOnerilen(isKalemiId) {
  _hiy.modalTip = 'malzemeOner';
  _hiy.modalParentId = isKalemiId;
  hiyModalAc('Önerilen Malzemeleri Ekle');
  document.getElementById('hiyMdBody').innerHTML =
    '<div id="hiyOnerListKap"><div class="hiy-loading"><div class="hiy-spinner"></div></div></div>';
  try {
    var sonuclar = await Promise.all([
      _hiyGet('/api/v2/is-kalemleri/' + isKalemiId + '/malzeme-oner'),
      _hiyGet('/api/v2/is-kalemleri/' + isKalemiId + '/csb-malzemeler'),
    ]);
    var veri = sonuclar[0];
    var mevcutVeri = sonuclar[1];
    var oneriler = veri.oneriler || [];
    var kaynak = veri.kaynak || 'keyword';
    var mevcutIds = new Set((mevcutVeri.malzemeler || []).map(function (m) { return m.malzeme_katalog_id; }));

    console.group('[hiyMalzemeOnerilen] debug — isKalemiId=' + isKalemiId);
    console.log('csb-malzemeler raw:', mevcutVeri.malzemeler);
    console.table((mevcutVeri.malzemeler || []).map(function (m) {
      return { malzeme_katalog_id: m.malzeme_katalog_id, tip: typeof m.malzeme_katalog_id, ad: m.ad };
    }));
    console.log('malzeme-oner raw:', oneriler);
    console.table(oneriler.map(function (o) {
      return { malzeme_katalog_id: o.malzeme_katalog_id, tip: typeof o.malzeme_katalog_id, ad: o.malzeme_ad, kaynak: kaynak };
    }));
    console.log('mevcutIds Set:', mevcutIds);
    console.groupEnd();

    var kap = document.getElementById('hiyOnerListKap');
    if (!kap) return;
    if (oneriler.length === 0) {
      kap.innerHTML = '<div style="color:#94A3B8;font-size:12px;padding:8px 0;">Bu iş kalemi için öneri bulunamadı.</div>';
      return;
    }

    var baslik = kaynak === 'katalog'
      ? '<div class="hiy-oner-baslik"><span class="hiy-oner-kaynak-badge katalog">📋 Katalog İlişkisi</span> Zorunlu malzemeler kaldırılamaz.</div>'
      : '<div class="hiy-oner-baslik"><span class="hiy-oner-kaynak-badge keyword">🔍 Tahmini</span> İş kalemi adına göre tahmin edilen malzemeler.</div>';

    kap.innerHTML = baslik + oneriler.map(function (o) {
      var isKatalog = kaynak === 'katalog';
      var cbVal = isKatalog ? (o.malzeme_katalog_id || '') : (o.malzeme_id || '');
      var zorunlu = isKatalog && o.zorunlu;
      var zatenEkli = isKatalog && mevcutIds.has(o.malzeme_katalog_id);

      if (zatenEkli) {
        var satir = '<label class="hiy-oner-satir ekli">';
        satir += '<input type="checkbox" checked disabled style="margin-top:2px;flex-shrink:0;">';
        satir += '<span class="hiy-oner-satir-icerik">';
        if (o.poz_no) satir += '<span class="hiy-oner-poz">' + _escH(o.poz_no) + '</span>';
        satir += '<span class="hiy-mal-liste-ad">' + _escH(o.malzeme_ad) + '</span>';
        satir += '<span class="hiy-mal-liste-birim">' + _escH(o.birim || '') + '</span>';
        satir += '<span class="hiy-oner-ekli-badge">zaten ekli</span>';
        satir += '</span></label>';
        return satir;
      }

      var cbClass = 'hiy-onerilen-cb' + (isKatalog ? ' katalog-cb' : '');
      var satir = '<label class="hiy-oner-satir' + (zorunlu ? ' zorunlu' : '') + '">';
      satir += '<input type="checkbox" class="' + cbClass + '" checked'
        + (zorunlu ? ' data-zorunlu="1" onchange="hiyZorunluCbDegisti(this)"' : '')
        + ' value="' + _escH(String(cbVal)) + '"'
        + ' data-birim="' + _escH(o.birim || '') + '"'
        + ' data-miktar="' + _escH(String(o.miktar || 1)) + '"'
        + ' data-kaynak="' + _escH(kaynak) + '"'
        + (isKatalog ? ' data-katalog-malzeme-id="' + _escH(String(o.malzeme_katalog_id || '')) + '"' : '')
        + ' style="margin-top:2px;flex-shrink:0;">';

      satir += '<span class="hiy-oner-satir-icerik">';
      if (isKatalog && o.poz_no) {
        satir += '<span class="hiy-oner-poz">' + _escH(o.poz_no) + '</span>';
      }
      satir += '<span class="hiy-mal-liste-ad">' + _escH(o.malzeme_ad) + '</span>';
      satir += '<span class="hiy-mal-liste-birim">' + _escH(o.birim || '') + '</span>';
      if (isKatalog && o.miktar != null && o.miktar !== 1) {
        satir += '<span class="hiy-oner-miktar">× ' + o.miktar + '</span>';
      }
      if (zorunlu) {
        satir += '<span class="hiy-oner-zorunlu-badge">zorunlu</span>';
      }
      if (!isKatalog && o.neden) {
        satir += '<span class="hiy-oner-neden">' + _escH(o.neden) + '</span>';
      }
      satir += '</span></label>';
      return satir;
    }).join('');
  } catch (e) {
    var kap2 = document.getElementById('hiyOnerListKap');
    if (kap2) kap2.innerHTML = '<div style="color:#DC2626;font-size:12px;">Yüklenemedi: ' + _escH(e.message) + '</div>';
  }
}

function hiyZorunluCbDegisti(cb) {
  if (!cb.checked) {
    if (!confirm('Bu malzeme katalog ilişkisine göre zorunludur, kaldırmak istediğinize emin misiniz?')) {
      cb.checked = true;
    }
  }
}

async function _hiyMalzemeOnerEkle() {
  var cbs = document.querySelectorAll('.hiy-onerilen-cb:checked');
  if (cbs.length === 0) { _hiyToast('Lütfen en az bir malzeme seçin.', 'warning'); return; }
  var btn = document.getElementById('hiyMdKaydetBtn');
  if (btn) { btn.disabled = true; btn.textContent = 'Ekleniyor...'; }
  var basarili = 0, hata = 0;

  for (var i = 0; i < cbs.length; i++) {
    var cb = cbs[i];
    var kaynak = cb.dataset.kaynak || 'keyword';
    try {
      if (kaynak === 'katalog') {
        var katalogMalzemeId = parseInt(cb.dataset.katalogMalzemeId || cb.value, 10);
        await _hiyPatch('/api/v2/is-kalemleri/' + _hiy.modalParentId + '/malzemeler', {
          ekle: [{ malzeme_katalog_id: katalogMalzemeId, miktar: parseFloat(cb.dataset.miktar) || 1.0 }]
        });
      } else {
        await _hiyPost('/api/v2/is-kalemleri/' + _hiy.modalParentId + '/malzeme-ekle', {
          malzeme_id: parseInt(cb.value, 10),
          miktar: 1.0,
          birim: cb.dataset.birim || null,
        });
      }
      basarili++;
    } catch (_) { hata++; }
  }

  var msg = basarili + ' malzeme eklendi.';
  if (hata > 0) msg += ' (' + hata + ' eklenemedi)';
  _hiyToast(msg, hata > 0 ? 'warning' : 'success');
  hiyModalKapat();
  await _hiyMalzemeVeriYukle(_hiy.modalParentId);
}

function hiyMobilePanelAc() {
  var panel = document.getElementById('hiyTreePanel');
  var ov = document.getElementById('hiyMobOv');
  if (panel) panel.classList.add('mobile-open');
  if (ov) { ov.style.display = 'block'; ov.classList.add('visible'); }
}

function hiyMobilePanelKapat() {
  var panel = document.getElementById('hiyTreePanel');
  var ov = document.getElementById('hiyMobOv');
  if (panel) panel.classList.remove('mobile-open');
  if (ov) { ov.style.display = 'none'; ov.classList.remove('visible'); }
}

/* ══════════════════════════════════════════════
   BIM GÖRÜNTÜLEYICI
══════════════════════════════════════════════ */
async function hiyBimGoruntule() {
  if (!_hiy.santiyeId) {
    _hiyToast('Aktif şantiye seçili değil.', 'warning');
    return;
  }
  try {
    var veri = await _hiyGet('/api/bim/models?santiye_id=' + _hiy.santiyeId);
    var modeller = veri.modeller || [];
    if (modeller.length === 0) {
      _hiyToast('Bu şantiye için henüz 3D model yüklenmemiş.', 'warning');
      return;
    }
    var model = modeller[0];
    var ov = document.getElementById('hiyBimOv');
    var baslik = document.getElementById('hiyBimBaslik');
    var alt = document.getElementById('hiyBimAlt');
    var iframe = document.getElementById('hiyBimIframe');
    if (!ov || !iframe) return;
    if (baslik) baslik.textContent = model.orijinal_dosya_adi || '3D BIM Modeli';
    if (alt) alt.textContent = _hiy.santiyeAd + (modeller.length > 1 ? ' — ' + modeller.length + ' model mevcut' : '');
    iframe.src = '/bim-viewer?model_id=' + model.id + '&santiye_id=' + _hiy.santiyeId + '&token=' + encodeURIComponent(_hiyToken());
    ov.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  } catch (e) {
    _hiyToast('BIM modelleri yüklenemedi: ' + e.message, 'error');
  }
}

function hiyBimModalKapat() {
  var ov = document.getElementById('hiyBimOv');
  var iframe = document.getElementById('hiyBimIframe');
  if (ov) ov.style.display = 'none';
  if (iframe) iframe.src = '';
  document.body.style.overflow = '';
}

/* ══════════════════════════════════════════════
   COMPACT BIM KUTUSU (Görsel varyasyon)
══════════════════════════════════════════════ */

// HTML üretici — DURUM A (upload) veya DURUM B (iframe)
function _hiyCepheBimKutuHtml(katlar, model) {
  if (model) {
    // DURUM B — Model yüklü
    var binaId = (_hiy.secili && _hiy.secili.bina) ? _hiy.secili.bina.id : 0;
    var sorted = (katlar || []).slice().sort(function(a,b){ return b.kat_no - a.kat_no; }).slice(0, 8);
    var katDotlari = sorted.map(function(k) {
      var durum = _hiyCepheKatDurum(k);
      var renk = durum==='tamam' ? '#22C55E' : durum==='devam' ? '#F59E0B' : '#475569';
      var isSecili = k.id === _hiy.cepheSeciliKatId;
      return '<button onclick="hiyCepheKatSec('+k.id+','+binaId+')" title="'+_escH(k.etiket||'Kat '+k.kat_no)+'"'
        +' style="display:inline-flex;align-items:center;gap:3px;padding:3px 7px;border-radius:4px;cursor:pointer;'
        +'border:'+(isSecili?'1px solid #FF6B2C':'1px solid #334155')+';'
        +'background:'+(isSecili?'rgba(249,115,22,.18)':'rgba(255,255,255,.04)')+';'
        +'color:#CBD5E1;font-size:9px;font-weight:700;font-family:monospace;transition:all .15s;">'
        +'<span style="width:5px;height:5px;border-radius:50%;background:'+renk+';display:inline-block;flex-shrink:0;"></span>'
        +_escH(_hiyCepheKatKisa(k.etiket, k.kat_no))
        +'</button>';
    }).join('');

    return '<div style="display:flex;flex-direction:column;height:100%;">'
      // header
      +'<div style="display:flex;align-items:center;justify-content:space-between;padding:7px 10px;'
      +'border-bottom:1px solid #1E293B;flex-shrink:0;background:#0F172A;">'
      +'<div style="display:flex;align-items:center;gap:6px;min-width:0;">'
      +'<span style="width:7px;height:7px;border-radius:50%;background:#22C55E;flex-shrink:0;'
      +'animation:hiyCepheBimPulse 2s ease-in-out infinite;"></span>'
      +'<span style="font-size:10.5px;font-weight:700;color:#CBD5E1;letter-spacing:.04em;flex-shrink:0;">BIM · 3D</span>'
      +'<span style="font-size:10px;color:#475569;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:180px;">'
      +_escH(model.orijinal_dosya_adi || 'model.ifc')
      +'</span></div>'
      +'<button onclick="hiyBimGoruntule()" title="Tam ekran aç" style="'
      +'background:rgba(255,255,255,.07);border:1px solid #334155;border-radius:5px;'
      +'width:24px;height:24px;display:flex;align-items:center;justify-content:center;'
      +'color:#94A3B8;cursor:pointer;font-size:14px;line-height:1;flex-shrink:0;">⛶</button>'
      +'</div>'
      // iframe
      +'<div style="flex:1;position:relative;overflow:hidden;min-height:0;">'
      +'<iframe src="/bim-viewer?model_id='+model.id+'&santiye_id='+(_hiy.santiyeId||0)+'&compact=true&token='+encodeURIComponent(_hiyToken())+'"'
      +' id="hiyCepheBimIframe" title="BIM 3D önizleme" loading="lazy"'
      +' style="width:100%;height:100%;border:none;background:#1E293B;display:block;"></iframe>'
      +'</div>'
      // kat noktaları
      +(katDotlari
        ? '<div style="display:flex;gap:4px;flex-wrap:wrap;padding:6px 8px;'
          +'background:#0A1628;border-top:1px solid #1E293B;flex-shrink:0;">'
          +katDotlari+'</div>'
        : '')
      +'</div>';
  }

  // DURUM A — Model yüklenmemiş
  return '<div style="display:flex;flex-direction:column;height:100%;justify-content:center;align-items:center;padding:24px 16px;">'
    +'<input type="file" id="hiyCepheBimFileInput" accept=".ifc" style="display:none">'
    +'<div id="hiyCepheBimDropZone" class="hiy-bim-drop-zone"'
    +' onclick="document.getElementById(\'hiyCepheBimFileInput\').click()">'
    +'<svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    +'<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>'
    +'<line x1="12" y1="11" x2="12" y2="17"/><polyline points="9 14 12 11 15 14"/>'
    +'</svg>'
    +'<div style="text-align:center;">'
    +'<div style="font-size:13px;font-weight:600;color:#94A3B8;margin-bottom:4px;">IFC dosyasını sürükleyin</div>'
    +'<div style="font-size:11px;color:#475569;">veya tıklayarak seçin <span style="color:#334155;">(.ifc)</span></div>'
    +'</div>'
    +'<div id="hiyCepheBimProgress" style="display:none;width:100%;max-width:260px;">'
    +'<div style="font-size:11px;color:#60A5FA;text-align:center;margin-bottom:6px;" id="hiyCepheBimProgressMsg">Yükleniyor...</div>'
    +'<div style="height:3px;background:#1E293B;border-radius:99;overflow:hidden;">'
    +'<div id="hiyCepheBimProgressBar" style="height:100%;background:#3B82F6;border-radius:99;width:0%;transition:width .3s;"></div>'
    +'</div></div>'
    +'</div>'
    +'<div style="font-size:10px;color:#1E3A5F;margin-top:14px;text-align:center;">IFC 2x3 · IFC 4 desteklenir</div>'
    +'</div>';
}

// BIM modelini API'den çek ve kutuyu render et
async function _hiyCepheBimKutuYukle(bina) {
  var kutu = document.getElementById('hiyCepheBimKutu');
  if (!kutu || !_hiy.santiyeId) return;
  var katlar = (bina && bina.katlar) ? bina.katlar
    : (_hiy.secili && _hiy.secili.bina) ? (_hiy.secili.bina.katlar || []) : [];
  try {
    var veri = await _hiyGet('/api/bim/models?santiye_id=' + _hiy.santiyeId);
    var model = (veri.modeller || [])[0] || null;
    _hiy.bimModel = model;
    _hiy.bimModelYuklendi = true;
    kutu.innerHTML = _hiyCepheBimKutuHtml(katlar, model);
    if (!model) _hiyCepheBimUploadBaglanti();
  } catch (e) {
    _hiy.bimModel = null;
    _hiy.bimModelYuklendi = true;
    kutu.innerHTML = _hiyCepheBimKutuHtml(katlar, null);
    _hiyCepheBimUploadBaglanti();
  }
}

// Drag & drop ve file input event'lerini bağla
function _hiyCepheBimUploadBaglanti() {
  var dropZone = document.getElementById('hiyCepheBimDropZone');
  var fileInput = document.getElementById('hiyCepheBimFileInput');
  if (!dropZone || !fileInput) return;

  dropZone.addEventListener('dragover', function(e) {
    e.preventDefault(); e.stopPropagation();
    dropZone.classList.add('hiy-bim-drop-active');
  });
  dropZone.addEventListener('dragleave', function(e) {
    e.preventDefault(); e.stopPropagation();
    dropZone.classList.remove('hiy-bim-drop-active');
  });
  dropZone.addEventListener('drop', function(e) {
    e.preventDefault(); e.stopPropagation();
    dropZone.classList.remove('hiy-bim-drop-active');
    var files = e.dataTransfer && e.dataTransfer.files;
    if (files && files[0]) _hiyCepheBimDosyaYukle(files[0]);
  });
  fileInput.addEventListener('change', function() {
    if (fileInput.files && fileInput.files[0]) _hiyCepheBimDosyaYukle(fileInput.files[0]);
  });
}

// IFC dosyasını sunucuya yükle
async function _hiyCepheBimDosyaYukle(file) {
  var progressEl  = document.getElementById('hiyCepheBimProgress');
  var progressMsg = document.getElementById('hiyCepheBimProgressMsg');
  var progressBar = document.getElementById('hiyCepheBimProgressBar');
  if (progressEl)  progressEl.style.display  = 'block';
  if (progressMsg) progressMsg.textContent   = 'Dosya yükleniyor...';
  if (progressBar) progressBar.style.width   = '0%';

  try {
    var formData = new FormData();
    formData.append('file', file);
    formData.append('santiye_id', String(_hiy.santiyeId));

    await new Promise(function(resolve, reject) {
      var xhr = new XMLHttpRequest();
      xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable && progressBar && progressMsg) {
          var pct = Math.round(e.loaded / e.total * 100);
          progressBar.style.width = pct + '%';
          progressMsg.textContent = 'Yükleniyor... %' + pct;
        }
      });
      xhr.addEventListener('load', function() {
        if (xhr.status >= 200 && xhr.status < 300) { resolve(xhr); }
        else { reject(new Error(xhr.responseText || 'Yükleme hatası')); }
      });
      xhr.addEventListener('error', function() { reject(new Error('Ağ hatası')); });
      xhr.open('POST', '/api/bim/upload');
      xhr.setRequestHeader('Authorization', 'Bearer ' + _hiyToken());
      xhr.timeout = 5 * 60 * 1000;
      xhr.send(formData);
    });

    _hiyToast('BIM modeli başarıyla yüklendi!', 'success');
    _hiy.bimModelYuklendi = false; // force refresh
    var bina = (_hiy.secili && _hiy.secili.bina) ? _hiy.secili.bina : null;
    await _hiyCepheBimKutuYukle(bina);
  } catch (e) {
    if (progressEl) progressEl.style.display = 'none';
    _hiyToast('Yükleme hatası: ' + (e.message || 'Bilinmeyen hata'), 'error');
  }
}

/* ══════════════════════════════════════════════
   GÖRSEL CEPHE HARİTASI
══════════════════════════════════════════════ */

function _hiyCepheVaryasyonBarGoster(goster) {
  var bar = document.getElementById('hiyVaryasyonBar');
  if (!bar) return;
  bar.style.display = goster ? 'flex' : 'none';
  var btn3d = document.getElementById('hiyVar3dBtn');
  if (btn3d) btn3d.style.display = goster ? 'inline-flex' : 'none';
  _hiyCepheToggleGuncelle();
}

function _hiyCepheToggleGuncelle() {
  var kb = document.getElementById('hiyVarBtnKlasik');
  var gb = document.getElementById('hiyVarBtnGorsel');
  if (!kb || !gb) return;
  var aktif = { background:'#fff', color:'#0F172A', fontWeight:'600', boxShadow:'0 1px 2px rgba(15,23,42,.08)' };
  var pasif = { background:'transparent', color:'#64748B', fontWeight:'500', boxShadow:'none' };
  var isK = _hiy.varyasyon === 'klasik';
  Object.assign(kb.style, isK ? aktif : pasif);
  Object.assign(gb.style, isK ? pasif : aktif);
}

function hiyVaryasyonDegistir(v) {
  _hiy.varyasyon = v;
  _hiyCepheToggleGuncelle();
  var s = _hiy.secili;
  if (!s) return;
  if (s.tip === 'bina' && s.bina) { _hiyBinaIcerigiGoster(s.bina); }
  else if (s.tip === 'kat' && s.bina && s.kat) { _hiyKatIcerigiGoster(s.bina, s.kat); }
}

// -- Yardımcılar --

function _hiyCepheKatPct(kat) {
  var list = [];
  (kat.mahaller || []).forEach(function(m){ list = list.concat(m.is_kalemleri || []); });
  if (!list.length) return 0;
  return Math.round(list.reduce(function(s,k){ return s+(k.son_ilerleme_yuzde||0); },0) / list.length);
}

function _hiyCepheKatDurum(kat) {
  var list = [];
  (kat.mahaller || []).forEach(function(m){ list = list.concat(m.is_kalemleri || []); });
  if (!list.length) return 'planli';
  if (list.every(function(k){ return k.durum==='tamamlandi'; })) return 'tamam';
  if (list.some(function(k){ return k.durum==='devam_eden'; })) return 'devam';
  return 'planli';
}

function _hiyCepheKatKisa(etiket, katNo) {
  var e = (etiket || ('Kat ' + katNo)).trim();
  if (/çatı/i.test(e))  return 'ÇT';
  if (/bodrum/i.test(e)) return 'B' + (e.match(/\d+/)||[''])[0];
  if (/zemin/i.test(e))  return 'ZM';
  var m = e.match(/(\d+)/);
  if (m) return 'K'+m[1];
  return e.slice(0,2).toUpperCase();
}

function _hiyCepheDaireSayisi(kat) {
  var daire = (kat.mahaller||[]).filter(function(m){
    return /daire|konut|rezidans/i.test((m.mahal_tipi||'')+' '+(m.ad||''));
  }).length;
  return Math.max(1, daire || Math.min(5, (kat.mahaller||[]).length));
}

// -- SVG bina çizici (her kat için widthFactor/xOffsetFactor destekli) --
function _hiyCepheBinaSvg(katlar, seciliKatId, binaId) {
  var SW = 186, FH = 46, ROOF = 22, GND = 26, ANT = 16, MRG = 14;
  var sorted = katlar.slice().sort(function(a,b){ return b.kat_no-a.kat_no; });
  var totalH = ANT + ROOF + sorted.length*FH + GND;
  var wallTop = ANT + ROOF;
  var groundY = wallTop + sorted.length*FH;
  var IW = SW - MRG*2;

  function rect(kat) {
    var wf = Math.min(1, Math.max(0.25, kat.widthFactor||1));
    var xof= Math.min(1-wf, Math.max(0, kat.xOffsetFactor||0));
    return { x1: MRG + xof*IW, x2: MRG + xof*IW + wf*IW, w: wf*IW };
  }

  var rects = sorted.map(rect);
  var s = '<svg xmlns="http://www.w3.org/2000/svg" width="'+SW+'" height="'+totalH+'" viewBox="0 0 '+SW+' '+totalH+'" style="display:block;">';
  s += '<defs><pattern id="hcg" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M 8 0 L 0 0 0 8" stroke="#E5E7EB" stroke-width=".4" fill="none"/></pattern></defs>';
  s += '<rect width="'+SW+'" height="'+totalH+'" fill="url(#hcg)" opacity=".4"/>';

  // anten
  s += '<line x1="'+(SW/2)+'" y1="0" x2="'+(SW/2)+'" y2="'+ANT+'" stroke="#334155" stroke-width="1.5" stroke-linecap="round"/>';
  s += '<circle cx="'+(SW/2)+'" cy="3" r="2.5" fill="#FF6B2C"/>';

  // çatı
  if (sorted.length > 0) {
    var tr = rects[0];
    s += '<polygon points="'+tr.x1+','+wallTop+' '+tr.x2+','+wallTop+' '+(tr.x2-10)+','+ANT+' '+(tr.x1+10)+','+ANT+'" fill="#1E293B"/>';
    s += '<rect x="'+tr.x1+'" y="'+wallTop+'" width="'+tr.w+'" height="4" fill="#0F172A"/>';
  }

  // katlar
  sorted.forEach(function(kat, i) {
    var r = rects[i];
    var y = wallTop + 4 + i*FH;
    var pct = _hiyCepheKatPct(kat);
    var durum = _hiyCepheKatDurum(kat);
    var isAkt = seciliKatId === kat.id;
    var isTam = durum === 'tamam';
    var isDevam = durum === 'devam';
    var isGnd = i === sorted.length-1;

    // taban dikdörtgen — tıklanabilir
    s += '<rect x="'+r.x1+'" y="'+y+'" width="'+r.w+'" height="'+FH+'"'
      +' fill="'+(isAkt?'#FFF2EB':'#F8FAFC')+'" stroke="'+(isAkt?'#FF6B2C':isTam?'#86EFAC':'#D1D5DB')+'"'
      +' stroke-width="'+(isAkt?1.5:1)+'" rx="1" style="cursor:pointer;"'
      +' onclick="hiyCepheKatSec('+kat.id+','+binaId+')" />';

    // ilerleme dolgusu
    if (pct > 0 && pct < 100) {
      var ph = FH*pct/100;
      s += '<rect x="'+r.x1+'" y="'+(y+FH-ph)+'" width="'+r.w+'" height="'+ph+'" fill="#FF6B2C" opacity=".15" pointer-events="none"/>';
    }
    if (isTam) s += '<rect x="'+r.x1+'" y="'+y+'" width="'+r.w+'" height="'+FH+'" fill="#16A34A" opacity=".09" pointer-events="none"/>';

    // pencereler
    var nd = _hiyCepheDaireSayisi(kat);
    var wg = 4, ww = (r.w - 12 - wg*(nd-1))/nd, wh = FH-18, wy = y+7;
    for (var u=0; u<nd; u++) {
      var wx = r.x1+6+u*(ww+wg);
      s += '<rect x="'+wx+'" y="'+wy+'" width="'+ww+'" height="'+wh+'" rx="1"'
        +' fill="'+(isTam?'#FF6B2C':isAkt?'#FFE8D9':'#CBD5E1')+'"'
        +' stroke="'+(isTam?'#E85B1E':isAkt?'#FFD0B5':'#94A3B8')+'" stroke-width=".5" pointer-events="none"/>';
    }

    // ayırıcı çizgi
    if (i < sorted.length-1) s += '<line x1="'+r.x1+'" y1="'+(y+FH)+'" x2="'+r.x2+'" y2="'+(y+FH)+'" stroke="#D1D5DB" stroke-width=".4"/>';

    // aktif kenar çubuğu
    if (isAkt) s += '<rect x="'+(r.x1-5)+'" y="'+(y+3)+'" width="3" height="'+(FH-6)+'" rx="1.5" fill="#FF6B2C" pointer-events="none"/>';

    // durum rozeti
    if (isTam) {
      s += '<circle cx="'+(r.x2-8)+'" cy="'+(y+8)+'" r="5" fill="#16A34A" pointer-events="none"/>';
      s += '<path d="M '+(r.x2-10)+' '+(y+8)+' L '+(r.x2-8)+' '+(y+10.5)+' L '+(r.x2-5)+' '+(y+6)+'" stroke="#fff" stroke-width="1.2" fill="none" pointer-events="none"/>';
    } else if (isDevam) {
      s += '<circle cx="'+(r.x2-8)+'" cy="'+(y+8)+'" r="5" fill="#D97706" pointer-events="none"/>';
    }

    // zemin kat kapı
    if (isGnd) {
      var mid = SW/2;
      s += '<rect x="'+(mid-7)+'" y="'+(y+FH-16)+'" width="14" height="16" fill="#1E293B" pointer-events="none"/>';
      s += '<rect x="'+(mid-10)+'" y="'+(y+FH-20)+'" width="20" height="4" fill="#FF6B2C" rx=".5" pointer-events="none"/>';
    }

    // kat etiketi (sağda)
    var lbl = _escH(_hiyCepheKatKisa(kat.etiket, kat.kat_no));
    s += '<text x="'+(r.x2+4)+'" y="'+(y+FH/2+4)+'" font-size="9" fill="'+(isAkt?'#FF6B2C':'#94A3B8')+'" font-weight="'+(isAkt?700:400)+'" pointer-events="none">'+lbl+'</text>';
  });

  // zemin
  s += '<line x1="0" y1="'+groundY+'" x2="'+SW+'" y2="'+groundY+'" stroke="#94A3B8" stroke-width=".8"/>';
  s += '<rect x="0" y="'+groundY+'" width="'+SW+'" height="'+GND+'" fill="#F1F3F5"/>';
  s += '<text x="4" y="'+(groundY+11)+'" font-size="7" fill="#94A3B8">±0.00</text>';
  s += '<text x="'+(SW-4)+'" y="'+(groundY+11)+'" font-size="7" fill="#94A3B8" text-anchor="end">N →</text>';
  s += '</svg>';
  return s;
}

// -- Sağ panel: kat listesi --
function _hiyCepheKatListesiHtml(katlar, binaId, seciliKatId) {
  var sorted = katlar.slice().sort(function(a,b){ return b.kat_no-a.kat_no; });
  var html = '<div style="display:flex;flex-direction:column;">';
  // tablo başlığı
  html += '<div style="display:grid;grid-template-columns:24px 1fr 70px 20px;gap:8px;padding:7px 12px;'
    +'background:#F8FAFC;border-bottom:1px solid #EEF0F3;font-size:9.5px;font-weight:700;'
    +'color:#94A3B8;text-transform:uppercase;letter-spacing:.07em;">'
    +'<span>Kat</span><span>Durum</span><span style="text-align:right;">İlerleme</span><span></span></div>';

  sorted.forEach(function(kat) {
    var pct = _hiyCepheKatPct(kat);
    var durum = _hiyCepheKatDurum(kat);
    var isAkt = seciliKatId === kat.id;
    var durumMeta = durum==='tamam' ? {lbl:'Tamamlandı',dot:'#16A34A',bar:'#16A34A'}
                  : durum==='devam' ? {lbl:'Devam ediyor',dot:'#D97706',bar:'#FF6B2C'}
                  : {lbl:'Planlı',dot:'#94A3B8',bar:'#CBD5E1'};
    var nd = _hiyCepheDaireSayisi(kat);
    html += '<button onclick="hiyCepheKatSec('+kat.id+','+binaId+')" style="'
      +'display:grid;grid-template-columns:24px 1fr 70px 20px;gap:8px;padding:9px 12px;'
      +'background:'+(isAkt?'#FFF2EB':'transparent')+';border:0;'
      +'border-left:'+(isAkt?'2px solid #FF6B2C':'2px solid transparent')+';'
      +'border-bottom:1px solid #EEF0F3;cursor:pointer;text-align:left;font-family:inherit;width:100%;">'
      // rozet
      +'<span style="width:22px;height:22px;border-radius:5px;display:grid;place-items:center;font-size:9px;font-weight:700;font-family:monospace;'
      +'background:'+(isAkt?'#FF6B2C':'#F1F5F9')+';color:'+(isAkt?'#fff':'#94A3B8')+';">'
      +_escH(_hiyCepheKatKisa(kat.etiket, kat.kat_no))+'</span>'
      // isim + durum
      +'<div style="min-width:0;">'
      +'<div style="font-size:12px;font-weight:600;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'
      +_escH(kat.etiket||'Kat '+kat.kat_no)+'</div>'
      +'<div style="font-size:10px;color:'+durumMeta.dot+';display:flex;align-items:center;gap:4px;margin-top:1px;">'
      +'<span style="width:5px;height:5px;border-radius:50%;background:'+durumMeta.dot+';display:inline-block;"></span>'
      +durumMeta.lbl
      +(nd>0?' <span style="color:#94A3B8">· '+nd+' daire</span>':'')
      +'</div></div>'
      // progress
      +'<div style="display:flex;flex-direction:column;gap:2px;">'
      +'<div style="height:3px;background:#F1F3F5;border-radius:99;overflow:hidden;">'
      +'<div style="width:'+pct+'%;height:100%;background:'+durumMeta.bar+';border-radius:99;transition:width .4s;"></div></div>'
      +'<span style="font-size:9.5px;color:#94A3B8;text-align:right;font-family:monospace;">%'+pct+'</span>'
      +'</div>'
      // ok
      +'<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="'+(isAkt?'#FF6B2C':'#CBD5E1')+'" stroke-width="2"><polyline points="9 6 15 12 9 18"/></svg>'
      +'</button>';
  });
  html += '</div>';
  return html;
}

// -- Seçili kat iş kalemi özeti (alt panel) --
function _hiyCepheKatOzetHtml(kat) {
  var kalemler = [];
  (kat.mahaller||[]).forEach(function(m){ kalemler=kalemler.concat(m.is_kalemleri||[]); });
  if (!kalemler.length) return '<div style="padding:12px 16px;font-size:12px;color:#94A3B8;">Bu kat için iş kalemi henüz planlanmadı.</div>';

  var RENKLER = ['#FF6B2C','#2563EB','#16A34A','#7C3AED','#D97706','#0891B2'];
  var html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px 16px;padding:14px 16px;">';
  kalemler.slice(0,6).forEach(function(ik, i) {
    var pct = Math.round(ik.son_ilerleme_yuzde||0);
    var renk = RENKLER[i%RENKLER.length];
    html += '<div style="display:flex;align-items:center;gap:7px;min-width:0;">'
      +'<span style="width:7px;height:7px;border-radius:2px;background:'+renk+';flex-shrink:0;"></span>'
      +'<div style="min-width:0;flex:1;">'
      +'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:4px;">'
      +'<span style="font-size:11px;font-weight:500;color:#0F172A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">'+_escH(ik.tanim.split('(')[0].trim())+'</span>'
      +'<span style="font-size:10.5px;font-weight:700;color:#475569;flex-shrink:0;font-family:monospace;">%'+pct+'</span>'
      +'</div>'
      +'<div style="display:flex;align-items:center;gap:5px;margin-top:3px;">'
      +'<div style="flex:1;height:3px;background:#F1F3F5;border-radius:99;overflow:hidden;">'
      +'<div style="width:'+pct+'%;height:100%;background:'+renk+';border-radius:99;"></div></div>'
      +'<span style="font-size:9px;color:#94A3B8;font-family:monospace;">'+ik.metraj+' '+_escH(ik.birim)+'</span>'
      +'</div></div></div>';
  });
  html += '</div>';
  return html;
}

// -- Ana render fonksiyonu --
function _hiyCepheHaritasiRender(bina) {
  var body = document.getElementById('hiyCtxBody');
  if (!body) return;
  body.classList.add('gorsel-mod');

  var katlar = bina.katlar || [];
  var binaId = bina.id;
  var sid = _hiy.cepheSeciliKatId;

  // Seçili kat yoksa en aktif/üst katı seç
  if (!sid || !katlar.find(function(k){ return k.id===sid; })) {
    var devam = katlar.find(function(k){ return _hiyCepheKatDurum(k)==='devam'; });
    sid = devam ? devam.id : (katlar.length ? katlar[katlar.length-1].id : null);
    _hiy.cepheSeciliKatId = sid;
  }

  var seciliKat = sid ? katlar.find(function(k){ return k.id===sid; }) : null;

  // Genel ilerleme
  var allPct = katlar.length ? katlar.reduce(function(s,k){ return s+_hiyCepheKatPct(k); },0)/katlar.length : 0;
  var tamam = katlar.filter(function(k){ return _hiyCepheKatDurum(k)==='tamam'; }).length;
  var devam = katlar.filter(function(k){ return _hiyCepheKatDurum(k)==='devam'; }).length;
  var planli= katlar.filter(function(k){ return _hiyCepheKatDurum(k)==='planli'; }).length;

  // Donut SVG
  var donutR = 14, donutC = 2*Math.PI*donutR;
  var donutOff = donutC - (allPct/100)*donutC;
  var donutSvg = '<svg width="38" height="38" viewBox="0 0 38 38">'
    +'<circle cx="19" cy="19" r="'+donutR+'" fill="none" stroke="#F1F3F5" stroke-width="4"/>'
    +'<circle cx="19" cy="19" r="'+donutR+'" fill="none" stroke="#FF6B2C" stroke-width="4"'
    +' stroke-dasharray="'+donutC+'" stroke-dashoffset="'+donutOff+'" stroke-linecap="round"'
    +' transform="rotate(-90 19 19)"/>'
    +'<text x="19" y="22" text-anchor="middle" font-size="9" font-weight="700" fill="#0F172A">'+Math.round(allPct)+'%</text>'
    +'</svg>';

  var html = '<div style="display:flex;flex-direction:column;height:100%;overflow:hidden;">';

  // -- Üst: özet şerit --
  html += '<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 16px;'
    +'background:#fff;border-bottom:1px solid #EEF0F3;flex-shrink:0;gap:12px;">'
    +'<div style="display:flex;align-items:center;gap:10px;">'
    +donutSvg
    +'<div>'
    +'<div style="font-size:13px;font-weight:700;color:#0F172A;">'+_escH(bina.ad)+'</div>'
    +'<div style="font-size:11px;color:#94A3B8;margin-top:1px;">'+katlar.length+' kat · ilerleme haritası</div>'
    +'</div></div>'
    +'<div style="display:flex;align-items:center;gap:14px;font-size:11px;color:#64748B;">'
    +'<span style="display:inline-flex;align-items:center;gap:4px;"><span style="width:7px;height:7px;border-radius:50%;background:#16A34A;display:inline-block;"></span>Tamamlanan <b style="color:#0F172A;font-family:monospace;">'+tamam+'</b></span>'
    +'<span style="display:inline-flex;align-items:center;gap:4px;"><span style="width:7px;height:7px;border-radius:50%;background:#D97706;display:inline-block;"></span>Devam <b style="color:#0F172A;font-family:monospace;">'+devam+'</b></span>'
    +'<span style="display:inline-flex;align-items:center;gap:4px;"><span style="width:7px;height:7px;border-radius:50%;background:#CBD5E1;display:inline-block;"></span>Planlı <b style="color:#0F172A;font-family:monospace;">'+planli+'</b></span>'
    +'</div></div>';

  // -- Orta: BIM kutusu + kat listesi --
  html += '<div style="display:grid;grid-template-columns:400px 1fr;flex:1;overflow:hidden;min-height:0;">';

  // BIM kutusu sol (async ile doldurulacak)
  html += '<div id="hiyCepheBimKutu" style="background:#1E293B;border-right:1px solid #0F172A;'
    +'display:flex;flex-direction:column;overflow:hidden;">'
    +'<div style="display:flex;align-items:center;justify-content:center;height:100%;gap:8px;color:#475569;font-size:12px;">'
    +'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2" style="animation:hiySpinAnim 1s linear infinite;flex-shrink:0;">'
    +'<path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>BIM yükleniyor...</div>'
    +'</div>';

  // Kat listesi sağ
  html += '<div style="overflow-y:auto;display:flex;flex-direction:column;" id="hiyCepheKatListKap">'
    +_hiyCepheKatListesiHtml(katlar, binaId, sid)
    +'</div>';

  html += '</div>';

  // -- Alt: seçili kat disiplin kırılımı --
  if (seciliKat) {
    html += '<div style="border-top:1px solid #EEF0F3;background:#FAFBFC;flex-shrink:0;">'
      +'<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 16px 0;">'
      +'<div style="display:flex;align-items:center;gap:8px;">'
      +'<div style="width:26px;height:26px;border-radius:7px;background:#FFF2EB;display:grid;place-items:center;">'
      +'<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#FF6B2C" stroke-width="1.75"><path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/><path d="M3 18l9 5 9-5"/></svg>'
      +'</div>'
      +'<div style="font-size:12.5px;font-weight:600;color:#0F172A;">'
      +_escH(seciliKat.etiket||'Kat '+seciliKat.kat_no)
      +'<span style="color:#94A3B8;font-weight:400;font-size:11px;"> · disiplin kırılımı</span>'
      +'</div></div>'
      +'<button onclick="hiyKatSecildi('+seciliKat.id+','+binaId+')" style="font-size:11px;color:#FF6B2C;background:transparent;border:none;cursor:pointer;display:flex;align-items:center;gap:3px;font-family:inherit;">Klasik görünüm <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#FF6B2C" stroke-width="2"><polyline points="9 6 15 12 9 18"/></svg></button>'
      +'</div>'
      +_hiyCepheKatOzetHtml(seciliKat)
      +'</div>';
  }

  html += '</div>';
  body.innerHTML = html;

  // BIM kutusu — cache varsa direkt render, yoksa API'den çek
  if (!_hiy.bimModelYuklendi) {
    _hiyCepheBimKutuYukle(bina);
  } else {
    var _bimKutu = document.getElementById('hiyCepheBimKutu');
    if (_bimKutu) {
      _bimKutu.innerHTML = _hiyCepheBimKutuHtml(katlar, _hiy.bimModel);
      if (!_hiy.bimModel) _hiyCepheBimUploadBaglanti();
    }
  }
}

// -- Kat tıklama handler (SVG onclick tarafından çağrılır) --
function hiyCepheKatSec(katId, binaId) {
  _hiy.cepheSeciliKatId = katId;
  var bina = (_hiy.agac && _hiy.agac.binalar||[]).find(function(b){ return b.id===binaId; });
  if (!bina) return;
  var kat = (bina.katlar||[]).find(function(k){ return k.id===katId; });
  if (!kat) return;
  // breadcrumb + ağaç seçimi güncelle
  _hiySecimTemizle();
  var row = document.getElementById('hiyRow-k'+katId);
  if (row) row.classList.add('selected');
  _hiy.secili = { tip:'kat', id:katId, bina:bina, kat:kat };
  _hiyBcGuncelle([
    { ad: bina.ad, icon: '🏢', onclick: 'hiyBinaSecildi('+binaId+')' },
    { ad: kat.etiket||('Kat '+kat.kat_no), icon: '🏠' },
  ]);
  _hiyActionsGuncelle(null);
  _hiyCepheHaritasiRender(bina);
}
