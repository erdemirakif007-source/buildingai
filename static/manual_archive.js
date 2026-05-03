(function () {
  const SOURCE_META = {
    manual: { label: 'Manuel Kanıt', bg: '#FFF7ED', color: '#F97316' },
    kamera: { label: 'Kamera Analizi', bg: '#EFF6FF', color: '#2563EB' },
    rapor: { label: 'AI Raporu', bg: '#ECFDF5', color: '#059669' }
  };

  const SOURCE_FILTER_LABELS = {
    manual: 'Manuel',
    ai: 'AI Analizi',
    report: 'AI Raporu'
  };

  const MEDIA_FILTER_LABELS = {
    photo: 'Fotoğraf',
    video: 'Video',
    report: 'Rapor'
  };

  const IMAGE_MIME_PREFIX = 'image/';
  const VIDEO_MIME_PREFIX = 'video/';
  const IMAGE_EXT_RE = /\.(jpe?g|png|gif|bmp|webp)$/i;
  const VIDEO_EXT_RE = /\.(mp4|mov|webm|avi|mkv|m4v)$/i;
  const MAX_IMAGE_BYTES = 25 * 1024 * 1024;
  const MAX_VIDEO_BYTES = 150 * 1024 * 1024;

  let _kpArsivContext = { santiye_id: null, siteScoped: false };
  let _kpArsivViewMode = 'list';
  let _kpArsivFilterTimer = null;

  const _oldArsivDetayGoster = window.arsivDetayGoster;
  const _oldKpSantiyeBilgisiGuncelle = window.kpSantiyeBilgisiGuncelle;
  const _oldKpProjeSec = window.kpProjeSec;
  const _oldGunlukRaporAc = window.gunlukRaporAc;

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function safeJson(value, fallback) {
    try { return JSON.parse(value); } catch (err) { return fallback; }
  }

  function getToken() {
    return localStorage.getItem('bai_token') || '';
  }

  function getStoredSite() {
    return safeJson(localStorage.getItem('varsayilan_santiye') || 'null', null);
  }

  function persistSite(site) {
    if (site && site.id) localStorage.setItem('varsayilan_santiye', JSON.stringify(site));
  }

  function getActiveSite() {
    if (window._kpAktifSantiye && window._kpAktifSantiye.id) return window._kpAktifSantiye;
    const stored = getStoredSite();
    return stored && stored.id ? stored : null;
  }

  function getActiveSiteId() {
    const site = getActiveSite();
    return site && site.id ? Number(site.id) : null;
  }

  function getActiveSiteName() {
    const site = getActiveSite();
    return site && site.ad ? site.ad : 'Şantiye seçilmedi';
  }

  function apiJson(url, options) {
    return fetch(url, options).then(async function (res) {
      let data = {};
      try { data = await res.json(); } catch (err) { data = {}; }
      if (!res.ok) throw new Error(data.detail || data.mesaj || 'İşlem tamamlanamadı.');
      return data;
    });
  }

  function pad(num) {
    return String(num).padStart(2, '0');
  }

  function toDatetimeLocal(value) {
    const date = value ? new Date(value) : new Date();
    if (Number.isNaN(date.getTime())) return '';
    return date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate()) + 'T' + pad(date.getHours()) + ':' + pad(date.getMinutes());
  }

  function formatDateTime(value, dateOnly) {
    if (!value) return '—';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return esc(value);
    return date.toLocaleString('tr-TR', dateOnly ? { year: 'numeric', month: '2-digit', day: '2-digit' } : {
      year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'
    });
  }

  function formatBytes(bytes) {
    const size = Number(bytes || 0);
    if (!size) return '0 KB';
    const units = ['B', 'KB', 'MB', 'GB'];
    const power = Math.min(Math.floor(Math.log(size) / Math.log(1024)), units.length - 1);
    const value = size / Math.pow(1024, power);
    return value.toFixed(value >= 10 || power === 0 ? 0 : 1) + ' ' + units[power];
  }

  function ensureArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function formatSnippet(value, maxLen) {
    const text = String(value || '').replace(/\s+/g, ' ').trim();
    if (!text) return '';
    return text.length > maxLen ? text.slice(0, maxLen - 3) + '...' : text;
  }

  function isImageFile(file) {
    return !!file && ((file.type || '').startsWith(IMAGE_MIME_PREFIX) || IMAGE_EXT_RE.test(file.name || ''));
  }

  function isVideoFile(file) {
    return !!file && ((file.type || '').startsWith(VIDEO_MIME_PREFIX) || VIDEO_EXT_RE.test(file.name || ''));
  }

  function mediaLabel(record) {
    if ((record.media_type || '') === 'video') return 'Video';
    if ((record.media_type || '') === 'report') return 'Rapor';
    return 'Fotoğraf';
  }

  function sourceMeta(recordType) {
    return SOURCE_META[recordType] || SOURCE_META.manual;
  }

  function mediaPreviewHtml(record, compact) {
    const isVideo = record.media_type === 'video';
    const url = record.thumbnail_url || record.file_url || '';
    const height = compact ? '96px' : '220px';
    if (record.record_type === 'rapor') {
      return '<div style="height:' + height + ';border-radius:14px;background:linear-gradient(135deg,#0F172A,#1E293B);display:flex;align-items:center;justify-content:center;color:#E2E8F0;font-size:12px;font-weight:700;letter-spacing:0.04em;">RAPOR</div>';
    }
    if (isVideo && url) {
      return '<div style="position:relative;height:' + height + ';border-radius:14px;overflow:hidden;background:#0F172A;"><img src="' + esc(url) + '" style="width:100%;height:100%;object-fit:cover;display:block;opacity:0.78;"><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,rgba(15,23,42,0.12),rgba(15,23,42,0.38));"><div style="width:42px;height:42px;border-radius:999px;background:rgba(15,23,42,0.72);display:flex;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,0.18);"><svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z"></path></svg></div></div></div>';
    }
    if (url) return '<img src="' + esc(url) + '" style="width:100%;height:' + height + ';object-fit:cover;border-radius:14px;display:block;background:#0F172A;">';
    return '<div style="height:' + height + ';border-radius:14px;background:linear-gradient(135deg,#E2E8F0,#F8FAFC);display:flex;align-items:center;justify-content:center;color:#64748B;font-size:12px;font-weight:700;">Önizleme yok</div>';
  }

  function sortByNewest(list) {
    return ensureArray(list).slice().sort(function (a, b) {
      const aDate = new Date(a.captured_at || a.uploaded_at || a.created_at || 0).getTime() || 0;
      const bDate = new Date(b.captured_at || b.uploaded_at || b.created_at || 0).getTime() || 0;
      return bDate - aDate;
    });
  }

  function mergeRecords(existing, incoming) {
    const map = new Map();
    ensureArray(existing).forEach(function (item) { map.set(String(item.id), item); });
    ensureArray(incoming).forEach(function (item) { map.set(String(item.id), item); });
    return sortByNewest(Array.from(map.values()));
  }

  function openDefaultDetailModal(title, contentHtml) {
    const modal = document.getElementById('arsivDetayModal');
    const titleEl = document.getElementById('arsivDetayBaslik');
    const contentEl = document.getElementById('arsivDetayIcerik');
    if (!modal || !contentEl) return;
    modal.style.display = 'flex';
    if (titleEl) titleEl.textContent = title;
    contentEl.innerHTML = contentHtml;
  }

  function fillSelectOptions(selectId, items, placeholder, labelFn) {
    const select = document.getElementById(selectId);
    if (!select) return;
    const current = select.value;
    const normalized = ensureArray(items);
    select.innerHTML = '<option value="">' + esc(placeholder) + '</option>' + normalized.map(function (item) {
      const value = typeof item === 'object' ? item.id : item;
      const label = labelFn ? labelFn(item) : (typeof item === 'object' ? item.ad : item);
      return '<option value="' + esc(value) + '">' + esc(label) + '</option>';
    }).join('');
    if (current && Array.from(select.options).some(function (option) { return option.value === current; })) select.value = current;
  }

  function ensureArchiveUi() {
    const tabRow = document.getElementById('arsivTabKamera') && document.getElementById('arsivTabKamera').parentElement;
    if (tabRow && !document.getElementById('arsivTabManual')) {
      const btn = document.createElement('button');
      btn.id = 'arsivTabManual';
      btn.type = 'button';
      btn.setAttribute('onclick', "arsivTabSec('manual')");
      btn.style.cssText = 'font-size:12px;font-weight:700;padding:6px 14px;border-radius:8px;border:1.5px solid #E2E8F0;background:white;color:#64748B;cursor:pointer;transition:all 0.15s;';
      btn.textContent = 'Manuel Kanıtlar';
      tabRow.appendChild(btn);
    }
    const totalStat = document.getElementById('arsivStatToplam');
    if (totalStat && !document.getElementById('arsivStatManual')) {
      const statRow = totalStat.parentElement && totalStat.parentElement.parentElement;
      if (statRow) {
        const manualStat = document.createElement('div');
        manualStat.style.cssText = 'background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 14px;text-align:center;';
        manualStat.innerHTML = '<div id="arsivStatManual" style="font-size:18px;font-weight:800;color:#F97316;">—</div><div style="font-size:10px;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">Manuel Kanıt</div>';
        statRow.insertBefore(manualStat, totalStat.parentElement);
      }
    }
    if (document.getElementById('arsivAdvancedFilters')) return;
    const searchInput = document.getElementById('arsivAramaInput');
    if (!searchInput || !searchInput.parentElement || !searchInput.parentElement.parentElement) return;
    const row = searchInput.parentElement.parentElement;
    const filters = document.createElement('div');
    filters.id = 'arsivAdvancedFilters';
    filters.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin-top:12px;';
    filters.innerHTML = '<select id="arsivSantiyeFilter" onchange="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"></select><select id="arsivMedyaFilter" onchange="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"></select><select id="arsivKaynakFilter" onchange="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"></select><select id="arsivOlayFilter" onchange="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"></select><input id="arsivAlanFilter" type="text" placeholder="Alan / kamera" oninput="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"><select id="arsivYukleyenFilter" onchange="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"></select><select id="arsivDurumFilter" onchange="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"></select><input id="arsivTarihBaslangic" type="date" onchange="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"><input id="arsivTarihBitis" type="date" onchange="arsivFiltrele()" style="padding:8px 10px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:12px;color:#0F172A;"><div style="display:flex;align-items:center;gap:8px;justify-content:flex-end;"><button id="arsivViewList" type="button" onclick="arsivGorunumSec(\'list\')" style="padding:8px 12px;border-radius:10px;border:1.5px solid #0F172A;background:#0F172A;color:white;font-size:12px;font-weight:800;cursor:pointer;">Liste</button><button id="arsivViewGallery" type="button" onclick="arsivGorunumSec(\'gallery\')" style="padding:8px 12px;border-radius:10px;border:1.5px solid #E2E8F0;background:white;color:#64748B;font-size:12px;font-weight:800;cursor:pointer;">Galeri</button></div>';
    row.insertAdjacentElement('afterend', filters);
  }

  function currentArchiveFilters() {
    // NOTE: 'karar' tab intentionally falls through to '' — karar kayıtları client-side filtreleniyor (arsivRenderListe içinde), backend bu source_type'ı tanımıyor.
    const sourceFromTab = window._arsivAktifTab === 'manual' ? 'manual' : window._arsivAktifTab === 'kamera' ? 'ai' : window._arsivAktifTab === 'rapor' ? 'report' : '';
    return {
      arama: (document.getElementById('arsivAramaInput') || {}).value || '',
      santiye_id: (document.getElementById('arsivSantiyeFilter') || {}).value || '',
      medya_turu: (document.getElementById('arsivMedyaFilter') || {}).value || '',
      kaynak_turu: sourceFromTab || ((document.getElementById('arsivKaynakFilter') || {}).value || ''),
      olay_tipi: (document.getElementById('arsivOlayFilter') || {}).value || '',
      tarih_baslangic: (document.getElementById('arsivTarihBaslangic') || {}).value || '',
      tarih_bitis: (document.getElementById('arsivTarihBitis') || {}).value || '',
      alan_kamera: (document.getElementById('arsivAlanFilter') || {}).value || '',
      yukleyen: (document.getElementById('arsivYukleyenFilter') || {}).value || '',
      durum: (document.getElementById('arsivDurumFilter') || {}).value || ''
    };
  }

  function applyArchiveContextDefaults(force) {
    ensureArchiveUi();
    const siteSelect = document.getElementById('arsivSantiyeFilter');
    const defaultSiteId = _kpArsivContext.santiye_id || getActiveSiteId();
    if (!siteSelect || !defaultSiteId) return;
    if (force || !siteSelect.value) siteSelect.value = String(defaultSiteId);
  }

  function hydrateArchiveFilterOptions() {
    const options = (window._arsivData || {}).filtre_secenekleri || {};
    fillSelectOptions('arsivSantiyeFilter', options.santiyeler || [], 'Şantiye filtresi', function (item) { return item.ad; });
    fillSelectOptions('arsivMedyaFilter', options.medya_turleri || [], 'Medya türü', function (item) { return MEDIA_FILTER_LABELS[item] || item; });
    fillSelectOptions('arsivKaynakFilter', options.kaynak_turleri || [], 'Kaynak türü', function (item) { return SOURCE_FILTER_LABELS[item] || item; });
    fillSelectOptions('arsivOlayFilter', options.olay_tipleri || [], 'Olay tipi');
    fillSelectOptions('arsivYukleyenFilter', options.yukleyenler || [], 'Yükleyen kişi');
    fillSelectOptions('arsivDurumFilter', options.durumlar || [], 'Durum');
    applyArchiveContextDefaults(!_kpArsivContext.siteScoped);
  }

  function buildArchiveCard(record) {
    const meta = sourceMeta(record.record_type);
    const eventText = record.event_type || 'Tür belirtilmedi';
    const area = record.zone_label || record.camera_name || record.santiye_adi || 'Alan belirtilmedi';
    const wrapperStyle = _kpArsivViewMode === 'gallery' ? 'background:#FFFFFF;border:1px solid #E2E8F0;border-radius:18px;padding:14px;box-shadow:0 12px 32px rgba(15,23,42,0.07);display:flex;flex-direction:column;gap:12px;' : 'background:#FFFFFF;border:1px solid #E2E8F0;border-radius:18px;padding:14px;box-shadow:0 12px 32px rgba(15,23,42,0.07);display:grid;grid-template-columns:minmax(180px,240px) 1fr;gap:14px;align-items:flex-start;';
    return '<div style="' + wrapperStyle + '"><div>' + mediaPreviewHtml(record, _kpArsivViewMode !== 'gallery') + '</div><div style="min-width:0;display:flex;flex-direction:column;gap:10px;"><div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap;"><div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;"><span style="font-size:10px;font-weight:800;background:' + meta.bg + ';color:' + meta.color + ';padding:4px 8px;border-radius:999px;letter-spacing:0.04em;">' + esc(meta.label.toUpperCase()) + '</span><span style="font-size:10px;font-weight:800;background:#0F172A;color:white;padding:4px 8px;border-radius:999px;letter-spacing:0.04em;">' + esc(mediaLabel(record).toUpperCase()) + '</span>' + (record.status ? '<span style="font-size:10px;font-weight:800;background:#F8FAFC;color:#475569;padding:4px 8px;border-radius:999px;border:1px solid #E2E8F0;letter-spacing:0.04em;">' + esc(record.status.toUpperCase()) + '</span>' : '') + '</div><div style="font-size:11px;color:#64748B;font-weight:700;">' + esc(formatDateTime(record.captured_at || record.created_at)) + '</div></div><div style="font-size:16px;font-weight:800;color:#0F172A;line-height:1.35;">' + esc(formatSnippet(record.title || 'Kayıt', 92)) + '</div><div style="font-size:13px;color:#64748B;line-height:1.6;">' + esc(formatSnippet(record.description || record.ozet || 'Açıklama bulunmuyor.', 190)) + '</div><div style="display:flex;flex-wrap:wrap;gap:6px;"><span style="font-size:10px;font-weight:700;color:#2563EB;background:#EFF6FF;padding:4px 8px;border-radius:999px;">' + esc(eventText) + '</span><span style="font-size:10px;font-weight:700;color:#475569;background:#F8FAFC;padding:4px 8px;border-radius:999px;border:1px solid #E2E8F0;">' + esc(area) + '</span><span style="font-size:10px;font-weight:700;color:#475569;background:#F8FAFC;padding:4px 8px;border-radius:999px;border:1px solid #E2E8F0;">' + esc(record.uploaded_by || '—') + '</span></div><div style="font-size:11px;color:#64748B;font-weight:700;">' + esc(record.santiye_adi || 'Şantiye belirtilmedi') + '</div><div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:auto;"><button type="button" onclick="arsivDetayGoster(\'' + record.record_type + '\',' + record.id + ')" style="background:#0F172A;color:white;border:none;border-radius:10px;padding:9px 12px;font-size:11px;font-weight:800;cursor:pointer;">Görüntüle</button><button type="button" onclick="kpDailyReportBaglaModalAc(\'' + record.record_type + '\',' + record.id + ')" style="background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE;border-radius:10px;padding:9px 12px;font-size:11px;font-weight:800;cursor:pointer;">Günlük rapora ekle</button>' + (record.record_type === 'manual' ? '<button type="button" onclick="kpManualAiOneriAc(' + record.id + ')" style="background:#FFF7ED;color:#F97316;border:1px solid #FED7AA;border-radius:10px;padding:9px 12px;font-size:11px;font-weight:800;cursor:pointer;">AI öneri al</button>' : '') + '<button type="button" onclick="arsivSil(\'' + record.record_type + '\',' + record.id + ')" style="background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;border-radius:10px;padding:9px 12px;font-size:11px;font-weight:800;cursor:pointer;">Sil</button></div></div></div>';
  }

  window.arsivDetayGoster = async function (tip, id) { if (tip !== 'manual') { if (_oldArsivDetayGoster) return _oldArsivDetayGoster(tip, id); return; } openDefaultDetailModal('Manuel Kanıt', '<div style="text-align:center;padding:40px;color:#64748B;">Yükleniyor...</div>'); try { const data = await apiJson('/arsiv/manual/' + id + '?token=' + encodeURIComponent(getToken())); window._kpManualDetailRecord = data; openDefaultDetailModal('Manuel Kanıt', typeof window.kpBuildManualDetail === 'function' ? window.kpBuildManualDetail(data) : ''); } catch (err) { openDefaultDetailModal('Manuel Kanıt', '<div style="padding:28px;color:#DC2626;font-size:13px;">' + esc(err.message || 'Kayıt yüklenemedi.') + '</div>'); } };
  window.kpArsivAc = function () { _kpArsivContext = { santiye_id: getActiveSiteId(), siteScoped: true }; if (typeof window.setActiveNav === 'function') window.setActiveNav('arsiv'); const headerTitle = document.getElementById('headerTitle'); const tbTitle = document.getElementById('tbPageTitle'); if (headerTitle) headerTitle.textContent = '📁 Arşiv'; if (tbTitle) tbTitle.textContent = '📁 Arşiv'; window.arsivPageAc(_kpArsivContext); };
  window.arsivPageAc = function (context) { ['content', 'aiCommandBar', 'santiyePage', 'fiyatPage', 'stokPage', 'kameraPage'].forEach(function (pid) { const el = document.getElementById(pid); if (el) el.style.display = 'none'; }); const page = document.getElementById('arsivPage'); if (!page) return; page.style.display = 'flex'; ensureArchiveUi(); if (context && typeof context === 'object') _kpArsivContext = { santiye_id: context.santiye_id || null, siteScoped: !!context.siteScoped }; else if (!_kpArsivContext.santiye_id && getActiveSiteId()) _kpArsivContext = { santiye_id: getActiveSiteId(), siteScoped: true }; applyArchiveContextDefaults(true); window.arsivVeriYukle(); };
  window.arsivAc = function () { window.arsivPageAc(); };
  window.arsivVeriYukle = async function () { const token = getToken(); const content = document.getElementById('arsivIcerik'); ensureArchiveUi(); if (!token || !content) return; content.innerHTML = '<div style="text-align:center;padding:60px 20px;color:#94A3B8;"><div style="font-size:32px;margin-bottom:8px;">📁</div><div style="font-size:14px;font-weight:600;">Arşiv yükleniyor...</div></div>'; try { const filters = currentArchiveFilters(); const params = new URLSearchParams(); params.set('token', token); Object.keys(filters).forEach(function (key) { if (filters[key]) params.set(key, filters[key]); }); const data = await apiJson('/arsiv?' + params.toString()); window._arsivData = data; hydrateArchiveFilterOptions(); window.arsivIstatistikGuncelle(); window.arsivRenderListe(); } catch (err) { content.innerHTML = '<div style="text-align:center;padding:40px;color:#EF4444;font-size:13px;">' + esc(err.message || 'Arşiv yüklenemedi.') + '</div>'; } };
  window.arsivIstatistikGuncelle = function () { const records = ensureArray((window._arsivData || {}).arsiv_kayitlari); const raporCount = records.filter(function (item) { return item.record_type === 'rapor'; }).length; const kameraCount = records.filter(function (item) { return item.record_type === 'kamera'; }).length; const manualCount = records.filter(function (item) { return item.record_type === 'manual'; }).length; const totalCount = records.length; const setText = function (id, value) { const el = document.getElementById(id); if (el) el.textContent = String(value); }; setText('arsivStatRapor', raporCount); setText('arsivStatKamera', kameraCount); setText('arsivStatManual', manualCount); setText('arsivStatToplam', totalCount); const subtitle = document.getElementById('arsivSubtitle'); const siteSelect = document.getElementById('arsivSantiyeFilter'); const siteName = siteSelect && siteSelect.selectedOptions && siteSelect.selectedOptions[0] ? siteSelect.selectedOptions[0].textContent : ''; if (subtitle) subtitle.textContent = totalCount + ' kayıt görüntüleniyor' + (siteName && siteName !== 'Şantiye filtresi' ? ' • ' + siteName : ''); };
  window.arsivTabSec = function (tab) { window._arsivAktifTab = tab; ['tumu', 'rapor', 'kamera', 'manual', 'karar'].forEach(function (name) { const btn = document.getElementById('arsivTab' + name.charAt(0).toUpperCase() + name.slice(1)); if (!btn) return; const active = name === tab; btn.style.background = active ? '#0F172A' : 'white'; btn.style.color = active ? 'white' : '#64748B'; btn.style.borderColor = active ? '#0F172A' : '#E2E8F0'; }); window.arsivVeriYukle(); };
  window.arsivFiltrele = function () { clearTimeout(_kpArsivFilterTimer); _kpArsivFilterTimer = setTimeout(function () { window.arsivVeriYukle(); }, 180); };
  window.arsivGorunumSec = function (mode) { _kpArsivViewMode = mode === 'gallery' ? 'gallery' : 'list'; const listBtn = document.getElementById('arsivViewList'); const galleryBtn = document.getElementById('arsivViewGallery'); if (listBtn) { const active = _kpArsivViewMode === 'list'; listBtn.style.background = active ? '#0F172A' : 'white'; listBtn.style.color = active ? 'white' : '#64748B'; listBtn.style.borderColor = active ? '#0F172A' : '#E2E8F0'; } if (galleryBtn) { const active = _kpArsivViewMode === 'gallery'; galleryBtn.style.background = active ? '#0F172A' : 'white'; galleryBtn.style.color = active ? 'white' : '#64748B'; galleryBtn.style.borderColor = active ? '#0F172A' : '#E2E8F0'; } if (window._arsivData) window.arsivRenderListe(); };
  window.arsivRenderListe = function () { const content = document.getElementById('arsivIcerik'); if (!content) return; if (window._arsivAktifTab === 'karar') { const kararlar = ensureArray((window._arsivData || {}).kararlar); if (!kararlar.length) { content.innerHTML = '<div style="text-align:center;padding:60px 20px;color:#94A3B8;"><div style="font-size:40px;margin-bottom:10px;">📭</div><div style="font-size:14px;font-weight:700;color:#64748B;">Kayıt bulunamadı</div><div style="font-size:12px;margin-top:4px;">Henüz onaylanmış veya reddedilmiş karar kaydı yok.</div></div>'; return; } content.innerHTML = '<div style="display:grid;gap:14px;">' + kararlar.map(buildArchiveCard).join('') + '</div>'; return; } const records = ensureArray((window._arsivData || {}).arsiv_kayitlari); if (!records.length) { content.innerHTML = '<div style="text-align:center;padding:60px 20px;color:#94A3B8;"><div style="font-size:40px;margin-bottom:10px;">📭</div><div style="font-size:14px;font-weight:700;color:#64748B;">Kayıt bulunamadı</div><div style="font-size:12px;margin-top:4px;">Filtreleri genişletin veya yeni manuel kanıt ekleyin.</div></div>'; return; } content.innerHTML = '<div style="display:' + (_kpArsivViewMode === 'gallery' ? 'grid' : 'flex') + ';' + (_kpArsivViewMode === 'gallery' ? 'grid-template-columns:repeat(auto-fill,minmax(300px,1fr));' : 'flex-direction:column;') + 'gap:14px;">' + records.map(buildArchiveCard).join('') + '</div>'; };
  window.arsivSil = async function (tip, id) { if (!window.confirm('Bu kayıt arşivden kaldırılacak. Devam edilsin mi?')) return; const token = getToken(); let endpoint = ''; if (tip === 'manual') endpoint = '/manual-evidence/' + id + '?token=' + encodeURIComponent(token); else if (tip === 'rapor') endpoint = '/rapor-sil/' + id + '?token=' + encodeURIComponent(token); else endpoint = '/kanit-sil/' + id + '?token=' + encodeURIComponent(token); try { await apiJson(endpoint, { method: 'DELETE' }); if (tip === 'manual') { if (typeof window.kpRemoveManualRecord === 'function') window.kpRemoveManualRecord(id); if (typeof window.kpRenderManuelKartlar === 'function') window.kpRenderManuelKartlar(); } else if (tip === 'kamera') { window._kpTumAnaliz = ensureArray(window._kpTumAnaliz).filter(function (item) { return Number(item.id) !== Number(id); }); localStorage.removeItem('bai_thumb_' + id); localStorage.removeItem('bai_yolo_' + id); if (typeof window.kpRenderAiKartlar === 'function') window.kpRenderAiKartlar(window._kpTumAnaliz); } if (window._arsivData) window._arsivData.arsiv_kayitlari = ensureArray(window._arsivData.arsiv_kayitlari).filter(function (item) { return !(item.record_type === tip && Number(item.id) === Number(id)); }); if (typeof window.arsivDetayKapat === 'function') window.arsivDetayKapat(); window.arsivIstatistikGuncelle(); window.arsivRenderListe(); if (typeof window.showToast === 'function') window.showToast('Kayıt silindi.', 'success'); } catch (err) { if (typeof window.showToast === 'function') window.showToast(err.message || 'Silme işlemi başarısız oldu.', 'error'); } };
  window.kpSantiyeBilgisiGuncelle = async function () { if (_oldKpSantiyeBilgisiGuncelle) await _oldKpSantiyeBilgisiGuncelle(); const list = ensureArray(window._kpSantiyeler); const stored = getStoredSite(); if (list.length) { const matched = stored && stored.id ? list.find(function (site) { return Number(site.id) === Number(stored.id); }) : null; window._kpAktifSantiye = matched || window._kpAktifSantiye || list[0]; persistSite(window._kpAktifSantiye); if (typeof window.kpProjeBarGuncelle === 'function') window.kpProjeBarGuncelle(); } window.kpManuelYukle(); };
  window.kpProjeSec = function (id) { if (_oldKpProjeSec) _oldKpProjeSec(id); const list = ensureArray(window._kpSantiyeler); const selected = list.find(function (site) { return Number(site.id) === Number(id); }); if (selected) { window._kpAktifSantiye = selected; persistSite(selected); if (typeof window.kpProjeBarGuncelle === 'function') window.kpProjeBarGuncelle(); } window.kpManuelYukle(); };
  window.kpAnalizGonder = async function (base64, analiz_tipi) { const token = getToken(); const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'İstanbul'; try { const res = await fetch('/kamera-analiz', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: token, resim_base64: base64, analiz_tipi: analiz_tipi, hava: '', sehir: sehir, dil: window.aktifDil, santiye_id: getActiveSiteId() }) }); const data = await res.json(); if (!res.ok) { if (typeof window.showToast === 'function') window.showToast(data.detail || 'Analiz hatası oluştu.', 'error'); return null; } return data; } catch (err) { if (typeof window.showToast === 'function') window.showToast(err.message || 'Analiz hatası oluştu.', 'error'); return null; } };
  window.kameraAnalizGonder = async function (base64) { const token = getToken(); const analizTipi = document.getElementById('kameraAnalizTipi') ? document.getElementById('kameraAnalizTipi').value : 'genel'; const sehir = document.getElementById('citySelect') ? document.getElementById('citySelect').value : 'İstanbul'; const hava = (document.getElementById('temp') ? document.getElementById('temp').innerText : '') + ' ' + (document.getElementById('condition') ? document.getElementById('condition').innerText : ''); const resultBox = document.getElementById('result'); if (typeof window.kameraKapat === 'function') window.kameraKapat(); if (resultBox) resultBox.innerHTML = '<i>📸 Fotoğraf analiz ediliyor...</i>'; try { const res = await fetch('/kamera-analiz', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: token, resim_base64: base64, analiz_tipi: analizTipi, hava: hava, sehir: sehir, dil: window.aktifDil, santiye_id: getActiveSiteId() }) }); const data = await res.json(); if (!res.ok) { if (resultBox) resultBox.innerHTML = '<div style="text-align:center;padding:20px;color:#DC2626;">' + esc(data.detail || 'Analiz tamamlanamadı.') + '</div>'; return; } if (resultBox) resultBox.innerHTML = '<div class="res-title">📷 Kamera Analizi</div><div id="analizMetni" style="color:#1E293B;font-size:0.95rem;line-height:1.7;margin-top:10px;">' + (window.markdownToHtml ? window.markdownToHtml(data.cevap || data.sonuc || data.analiz_metni || '') : esc(data.cevap || data.sonuc || data.analiz_metni || '')) + '</div>'; if (typeof window.showToast === 'function') window.showToast('Analiz seçili şantiyeye bağlandı.', 'success'); } catch (err) { if (resultBox) resultBox.innerHTML = '<div style="text-align:center;padding:20px;color:#DC2626;">Bağlantı hatası oluştu.</div>'; } };
  window.kpLoguIndirv = function () { const rows = ['ID,Kaynak,Başlık,Açıklama,Şantiye,Tarih']; ensureArray(window._kpTumAnaliz).forEach(function (item) { rows.push([item.id, 'kamera', '"' + String(item.ozet || '').replace(/"/g, '""') + '"', '"' + String(item.ozet || '').replace(/"/g, '""') + '"', item.santiye_adi || '', item.created_at || ''].join(',')); }); ensureArray(window._kpManuelKayitlar).forEach(function (item) { rows.push([item.id, 'manual', '"' + String(item.title || '').replace(/"/g, '""') + '"', '"' + String(item.description || '').replace(/"/g, '""') + '"', item.santiye_adi || '', item.captured_at || item.uploaded_at || ''].join(',')); }); const blob = new Blob([rows.join('\n')], { type: 'text/csv;charset=utf-8;' }); const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href = url; link.download = 'kamera-analiz-logu.csv'; link.click(); URL.revokeObjectURL(url); };
  window.gunlukRaporAc = function () { if (_oldGunlukRaporAc) _oldGunlukRaporAc(); const dateEl = document.getElementById('grTarih'); if (dateEl && !dateEl.value) dateEl.value = new Date().toISOString().slice(0, 10); };
})();
