(function () {
  var DAILY_REPORT_SECTIONS = {
    ilerleme: 'İlerleme',
    isg_ihlaller: 'İSG / İhlaller',
    kalite_kusurlar: 'Kalite / Kusurlar',
    malzeme_ekipman: 'Malzeme / Ekipman',
    gecikmeler_engeller: 'Gecikmeler / Engeller',
    yarin_yapilacaklar: 'Yarın Yapılacaklar'
  };

  var SOURCE_META = {
    manual: { label: 'Manuel Kanıt', bg: '#FFF7ED', color: '#F97316' },
    kamera: { label: 'Kamera Analizi', bg: '#EFF6FF', color: '#2563EB' },
    rapor: { label: 'AI Raporu', bg: '#ECFDF5', color: '#059669' }
  };

  var IMAGE_MIME_PREFIX = 'image/';
  var VIDEO_MIME_PREFIX = 'video/';
  var IMAGE_EXT_RE = /\.(jpe?g|png|gif|bmp|webp)$/i;
  var VIDEO_EXT_RE = /\.(mp4|mov|webm|avi|mkv|m4v)$/i;
  var MAX_IMAGE_BYTES = 25 * 1024 * 1024;
  var MAX_VIDEO_BYTES = 150 * 1024 * 1024;

  var _kpManualUploadState = { uploading: false, lastPayload: null };

  // Shared with manual_archive.js — both files duplicate these pure utilities
  // to stay module-free and preserve browser global behavior.
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
    var stored = getStoredSite();
    return stored && stored.id ? stored : null;
  }

  function getActiveSiteId() {
    var site = getActiveSite();
    return site && site.id ? Number(site.id) : null;
  }

  function getActiveSiteName() {
    var site = getActiveSite();
    return site && site.ad ? site.ad : 'Şantiye seçilmedi';
  }

  function apiJson(url, options) {
    return fetch(url, options).then(async function (res) {
      var data = {};
      try { data = await res.json(); } catch (err) { data = {}; }
      if (!res.ok) throw new Error(data.detail || data.mesaj || 'İşlem tamamlanamadı.');
      return data;
    });
  }

  function pad(num) {
    return String(num).padStart(2, '0');
  }

  function toDatetimeLocal(value) {
    var date = value ? new Date(value) : new Date();
    if (Number.isNaN(date.getTime())) return '';
    return date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate()) + 'T' + pad(date.getHours()) + ':' + pad(date.getMinutes());
  }

  function formatDateTime(value, dateOnly) {
    if (!value) return '—';
    var date = new Date(value);
    if (Number.isNaN(date.getTime())) return esc(value);
    return date.toLocaleString('tr-TR', dateOnly ? { year: 'numeric', month: '2-digit', day: '2-digit' } : {
      year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'
    });
  }

  function formatBytes(bytes) {
    var size = Number(bytes || 0);
    if (!size) return '0 KB';
    var units = ['B', 'KB', 'MB', 'GB'];
    var power = Math.min(Math.floor(Math.log(size) / Math.log(1024)), units.length - 1);
    var value = size / Math.pow(1024, power);
    return value.toFixed(value >= 10 || power === 0 ? 0 : 1) + ' ' + units[power];
  }

  function ensureArray(value) {
    return Array.isArray(value) ? value : [];
  }

  function formatSnippet(value, maxLen) {
    var text = String(value || '').replace(/\s+/g, ' ').trim();
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
    var isVideo = record.media_type === 'video';
    var url = record.thumbnail_url || record.file_url || '';
    var height = compact ? '96px' : '220px';
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
      var aDate = new Date(a.captured_at || a.uploaded_at || a.created_at || 0).getTime() || 0;
      var bDate = new Date(b.captured_at || b.uploaded_at || b.created_at || 0).getTime() || 0;
      return bDate - aDate;
    });
  }

  function mergeRecords(existing, incoming) {
    var map = new Map();
    ensureArray(existing).forEach(function (item) { map.set(String(item.id), item); });
    ensureArray(incoming).forEach(function (item) { map.set(String(item.id), item); });
    return sortByNewest(Array.from(map.values()));
  }

  // Duplicated from manual_archive.js — needed by kpManualDetayKaydet and kpManualAiOneriGetir.
  function openDefaultDetailModal(title, contentHtml) {
    var modal = document.getElementById('arsivDetayModal');
    var titleEl = document.getElementById('arsivDetayBaslik');
    var contentEl = document.getElementById('arsivDetayIcerik');
    if (!modal || !contentEl) return;
    modal.style.display = 'flex';
    if (titleEl) titleEl.textContent = title;
    contentEl.innerHTML = contentHtml;
  }

  function removeManualRecordFromState(id) {
    window._kpManuelKayitlar = ensureArray(window._kpManuelKayitlar).filter(function (item) { return Number(item.id) !== Number(id); });
    if (!window._arsivData) return;
    window._arsivData.manual_evidence = ensureArray(window._arsivData.manual_evidence).filter(function (item) { return Number(item.id) !== Number(id); });
    window._arsivData.arsiv_kayitlari = ensureArray(window._arsivData.arsiv_kayitlari).filter(function (item) {
      return !(item.record_type === 'manual' && Number(item.id) === Number(id));
    });
  }

  function syncManualRecords(records) {
    window._kpManuelKayitlar = mergeRecords(window._kpManuelKayitlar, records);
    if (!window._arsivData) {
      window._arsivData = { raporlar: [], kamera_analizler: [], manual_evidence: [], arsiv_kayitlari: [], filtre_secenekleri: {} };
    }
    window._arsivData.manual_evidence = mergeRecords(window._arsivData.manual_evidence, records);
    window._arsivData.arsiv_kayitlari = mergeRecords(window._arsivData.arsiv_kayitlari, records);
  }

  function findArchiveRecord(sourceType, sourceId) {
    var numericId = Number(sourceId);
    if (sourceType === 'manual') {
      return ensureArray(window._kpManuelKayitlar).find(function (item) { return Number(item.id) === numericId; }) || null;
    }
    return ensureArray((window._arsivData || {}).arsiv_kayitlari).find(function (item) {
      return Number(item.id) === numericId && ((sourceType === 'kamera' && item.record_type === 'kamera') || (sourceType === 'rapor' && item.record_type === 'rapor'));
    }) || null;
  }

  function renderManualFileList(files) {
    var target = document.getElementById('kpManualSelectedFiles');
    if (!target) return;
    if (!files.length) {
      target.innerHTML = '<div style="font-size:12px;color:#94A3B8;">Henüz dosya seçilmedi. Fotoğraf ve video birlikte yüklenebilir.</div>';
      return;
    }
    target.innerHTML = files.map(function (file) {
      var typeText = isVideoFile(file) ? 'Video' : 'Fotoğraf';
      return '<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 12px;border:1px solid #E2E8F0;border-radius:10px;background:#0F172A;color:#E2E8F0;"><div style="min-width:0;"><div style="font-size:12px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + esc(file.name) + '</div><div style="font-size:11px;color:#94A3B8;margin-top:4px;">' + typeText + ' • ' + formatBytes(file.size) + '</div></div><span style="flex-shrink:0;font-size:10px;font-weight:800;background:' + (isVideoFile(file) ? '#1D4ED8' : '#EA580C') + ';color:white;padding:4px 8px;border-radius:999px;letter-spacing:0.04em;">' + typeText.toUpperCase() + '</span></div>';
    }).join('');
  }

  function setManualUploadStatus(message, percent, tone) {
    var box = document.getElementById('kpManualUploadStatus');
    if (!box) return;
    var safePercent = Math.max(0, Math.min(100, Number(percent || 0)));
    var fill = tone === 'error' ? '#EF4444' : tone === 'success' ? '#22C55E' : '#F97316';
    box.style.display = 'block';
    box.innerHTML = '<div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px;"><span style="font-size:12px;font-weight:700;color:#0F172A;">' + esc(message || 'Yükleniyor...') + '</span><span style="font-size:11px;font-weight:700;color:#64748B;">' + safePercent + '%</span></div><div style="height:9px;border-radius:999px;background:#E2E8F0;overflow:hidden;"><div style="height:100%;width:' + safePercent + '%;background:' + fill + ';transition:width 0.2s ease;"></div></div>';
  }

  function clearManualUploadFeedback() {
    var status = document.getElementById('kpManualUploadStatus');
    var error = document.getElementById('kpManualUploadError');
    if (status) status.style.display = 'none';
    if (error) { error.style.display = 'none'; error.innerHTML = ''; }
  }

  function showManualUploadError(message) {
    var box = document.getElementById('kpManualUploadError');
    if (!box) return;
    box.style.display = 'block';
    box.innerHTML = '<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding:12px 14px;border:1px solid #FECACA;background:#FEF2F2;border-radius:12px;"><div style="min-width:0;"><div style="font-size:12px;font-weight:800;color:#B91C1C;">Yükleme tamamlanamadı</div><div style="font-size:12px;color:#7F1D1D;margin-top:4px;line-height:1.5;">' + esc(message) + '</div></div><button type="button" onclick="kpManualRetrySonYukleme()" style="flex-shrink:0;background:#B91C1C;color:white;border:none;border-radius:8px;padding:8px 12px;font-size:12px;font-weight:700;cursor:pointer;">Tekrar dene</button></div>';
  }

  function ensureManualPanel() {
    var wrap = document.getElementById('kpManuelForm');
    if (!wrap) return;
    var cameraOptions = ['<option value="">Alan / kamera seçin (opsiyonel)</option>'].concat(ensureArray(window._kpCameraList).map(function (cam) {
      return '<option value="' + esc(cam.id) + '">' + esc(cam.name || ('Kamera #' + cam.id)) + '</option>';
    })).join('');
    wrap.innerHTML = ''
      + '<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:14px;margin-bottom:14px;flex-wrap:wrap;"><div><div style="font-size:14px;font-weight:800;color:#0F172A;">Manuel Kanıt Yükle</div><div style="font-size:12px;color:#64748B;margin-top:4px;">Kayıt otomatik olarak <span style="font-weight:800;color:#F97316;">' + esc(getActiveSiteName()) + '</span> şantiyesine bağlanır ve arşive düşer.</div></div><button type="button" onclick="kpManuelPanelKapat()" style="background:#F8FAFC;border:1px solid #E2E8F0;color:#475569;padding:8px 12px;border-radius:10px;cursor:pointer;font-size:12px;font-weight:700;">Kapat</button></div>'
      + '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;">'
      + '<div style="grid-column:1 / -1;"><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Dosyalar</label><input id="kpManualFilesInput" type="file" accept="image/*,video/*" multiple onchange="kpManualFilesSecildi(event)" style="width:100%;padding:11px 12px;border:1.5px dashed #CBD5E1;border-radius:12px;background:#F8FAFC;font-size:12px;color:#334155;box-sizing:border-box;"><div id="kpManualSelectedFiles" style="display:grid;gap:8px;margin-top:10px;"></div></div>'
      + '<div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Kısa başlık</label><input id="kpManualTitle" type="text" placeholder="Örn. İskele korkuluğu eksik" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div>'
      + '<div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Olay tipi</label><input id="kpManualEventType" list="kpManualEventTypeList" type="text" placeholder="Örn. İSG ihlali" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"><datalist id="kpManualEventTypeList"><option value="İSG ihlali"></option><option value="İlerleme"></option><option value="Kalite kusuru"></option><option value="Malzeme teslimi"></option><option value="Gecikme"></option><option value="Kaza / Olay"></option></datalist></div>'
      + '<div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Alan / Bölge</label><input id="kpManualZone" type="text" placeholder="Örn. Blok B - 3. kat" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div>'
      + '<div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">İlgili kamera</label><select id="kpManualCamera" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;">' + cameraOptions + '</select></div>'
      + '<div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Çekim zamanı</label><input id="kpManualCapturedAt" type="datetime-local" value="' + esc(toDatetimeLocal()) + '" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div>'
      + '<div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Etiketler</label><input id="kpManualTags" type="text" placeholder="iskele, emniyet, blok-b" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div>'
      + '<div style="grid-column:1 / -1;"><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Açıklama</label><textarea id="kpManualDescription" placeholder="Kanıtla ilgili kısa açıklama..." style="width:100%;min-height:96px;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;font-family:inherit;resize:vertical;"></textarea></div>'
      + '</div>'
      + '<div id="kpManualUploadStatus" style="display:none;margin-top:14px;"></div><div id="kpManualUploadError" style="display:none;margin-top:12px;"></div>'
      + '<div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:16px;flex-wrap:wrap;"><div style="font-size:12px;color:#64748B;">Fotoğraf için 25 MB, video için 150 MB sınırı uygulanır. EXIF tarihi varsa otomatik okunur.</div><div style="display:flex;gap:8px;flex-wrap:wrap;"><button type="button" onclick="kpManualRetrySonYukleme()" style="background:#FFF7ED;border:1px solid #FED7AA;color:#F97316;padding:10px 14px;border-radius:10px;cursor:pointer;font-size:12px;font-weight:700;">Son yüklemeyi tekrar dene</button><button type="button" onclick="kpManuelKaydet()" style="background:#0F172A;border:none;color:white;padding:10px 16px;border-radius:10px;cursor:pointer;font-size:12px;font-weight:800;letter-spacing:0.02em;">Yükle ve arşive ekle</button></div></div>';
    renderManualFileList([]);
  }

  function collectManualPayload() {
    var filesInput = document.getElementById('kpManualFilesInput');
    var files = Array.from((filesInput && filesInput.files) || []);
    if (!files.length) throw new Error('En az bir fotoğraf veya video seçmelisiniz.');
    if (!getActiveSiteId()) throw new Error('Önce aktif bir şantiye seçmelisiniz.');
    files.forEach(function (file) {
      if (!isImageFile(file) && !isVideoFile(file)) throw new Error('Desteklenmeyen dosya türü: ' + file.name);
      var limit = isVideoFile(file) ? MAX_VIDEO_BYTES : MAX_IMAGE_BYTES;
      if (file.size > limit) throw new Error(file.name + ' için dosya sınırı aşıldı.');
    });
    return {
      files: files,
      santiye_id: getActiveSiteId(),
      title: (document.getElementById('kpManualTitle') || {}).value || '',
      description: (document.getElementById('kpManualDescription') || {}).value || '',
      event_type: (document.getElementById('kpManualEventType') || {}).value || '',
      zone_label: (document.getElementById('kpManualZone') || {}).value || '',
      camera_id: (document.getElementById('kpManualCamera') || {}).value || '',
      captured_at: (document.getElementById('kpManualCapturedAt') || {}).value || '',
      tags: (document.getElementById('kpManualTags') || {}).value || ''
    };
  }

  function uploadManualEvidence(payload) {
    var token = getToken();
    if (!token) return Promise.reject(new Error('Oturum bilgisi bulunamadı.'));
    return new Promise(function (resolve, reject) {
      var formData = new FormData();
      formData.append('token', token);
      formData.append('santiye_id', String(payload.santiye_id));
      formData.append('title', payload.title || '');
      formData.append('description', payload.description || '');
      formData.append('event_type', payload.event_type || '');
      formData.append('zone_label', payload.zone_label || '');
      if (payload.camera_id) formData.append('camera_id', String(payload.camera_id));
      formData.append('captured_at', payload.captured_at || '');
      formData.append('tags', payload.tags || '');
      payload.files.forEach(function (file) { formData.append('files', file, file.name); });

      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/manual-evidence', true);
      xhr.upload.addEventListener('progress', function (event) {
        if (!event.lengthComputable) {
          setManualUploadStatus('Dosyalar yükleniyor...', 10, 'info');
          return;
        }
        var percent = Math.round((event.loaded / event.total) * 100);
        setManualUploadStatus(payload.files.length + ' dosya yükleniyor...', percent, 'info');
      });
      xhr.onload = function () {
        var data = {};
        try { data = JSON.parse(xhr.responseText || '{}'); } catch (err) { data = {}; }
        if (xhr.status >= 200 && xhr.status < 300) {
          setManualUploadStatus('Yükleme tamamlandı', 100, 'success');
          resolve(data);
          return;
        }
        reject(new Error(data.detail || data.mesaj || 'Yükleme başarısız oldu.'));
      };
      xhr.onerror = function () {
        reject(new Error('Bağlantı kesildi. Lütfen tekrar deneyin.'));
      };
      xhr.send(formData);
    });
  }

  function renderManualCards() {
    var container = document.getElementById('kpManuelKartlar');
    var empty = document.getElementById('kpManuelEmpty');
    var badge = document.getElementById('kpManuelBadge');
    var statManual = document.getElementById('kpStatManuel');
    if (!container) return;
    var records = sortByNewest(window._kpManuelKayitlar);
    if (badge) badge.textContent = String(records.length);
    if (statManual) statManual.textContent = String(records.length);
    if (!records.length) {
      container.innerHTML = '';
      container.style.display = 'none';
      if (empty) empty.style.display = 'block';
      return;
    }
    if (empty) empty.style.display = 'none';
    container.style.display = 'grid';
    container.style.gridTemplateColumns = 'repeat(auto-fill,minmax(280px,1fr))';
    container.style.gap = '14px';
    container.innerHTML = records.map(function (record) {
      var meta = sourceMeta('manual');
      var eventText = record.event_type || 'Belirtilmedi';
      var areaText = record.zone_label || record.camera_name || 'Alan belirtilmedi';
      var tags = ensureArray(record.tags).slice(0, 3).map(function (tag) {
        return '<span style="font-size:10px;font-weight:700;color:#475569;background:#F8FAFC;border:1px solid #E2E8F0;padding:4px 8px;border-radius:999px;">#' + esc(tag) + '</span>';
      }).join('');
      return '<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:16px;padding:14px;box-shadow:0 10px 28px rgba(15,23,42,0.07);display:flex;flex-direction:column;gap:12px;"><div style="display:flex;align-items:center;justify-content:space-between;gap:10px;"><div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;"><span style="font-size:10px;font-weight:800;background:' + meta.bg + ';color:' + meta.color + ';padding:4px 8px;border-radius:999px;letter-spacing:0.04em;">' + meta.label.toUpperCase() + '</span><span style="font-size:10px;font-weight:800;background:#0F172A;color:white;padding:4px 8px;border-radius:999px;letter-spacing:0.04em;">' + esc(mediaLabel(record).toUpperCase()) + '</span></div><div style="font-size:11px;color:#64748B;font-weight:700;">' + esc(formatDateTime(record.captured_at)) + '</div></div>' + mediaPreviewHtml(record, true) + '<div><div style="font-size:15px;font-weight:800;color:#0F172A;line-height:1.35;">' + esc(formatSnippet(record.title || 'Manuel kanıt', 72)) + '</div><div style="font-size:12px;color:#64748B;line-height:1.55;margin-top:6px;">' + esc(formatSnippet(record.description || 'Açıklama girilmemiş.', 132)) + '</div></div><div style="display:flex;flex-wrap:wrap;gap:6px;"><span style="font-size:10px;font-weight:700;color:#2563EB;background:#EFF6FF;padding:4px 8px;border-radius:999px;">' + esc(eventText) + '</span><span style="font-size:10px;font-weight:700;color:#475569;background:#F8FAFC;padding:4px 8px;border-radius:999px;border:1px solid #E2E8F0;">' + esc(areaText) + '</span>' + tags + '</div><div style="display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;"><div style="font-size:11px;color:#64748B;font-weight:700;">' + esc(record.santiye_adi || getActiveSiteName()) + ' • ' + esc(record.uploaded_by || 'Saha personeli') + '</div><div style="display:flex;gap:8px;flex-wrap:wrap;"><button type="button" onclick="arsivDetayGoster(\'manual\',' + record.id + ')" style="background:#0F172A;color:white;border:none;border-radius:9px;padding:8px 10px;font-size:11px;font-weight:800;cursor:pointer;">Görüntüle</button><button type="button" onclick="kpDailyReportBaglaModalAc(\'manual\',' + record.id + ')" style="background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE;border-radius:9px;padding:8px 10px;font-size:11px;font-weight:800;cursor:pointer;">Günlük rapora ekle</button><button type="button" onclick="kpManualAiOneriAc(' + record.id + ')" style="background:#FFF7ED;color:#F97316;border:1px solid #FED7AA;border-radius:9px;padding:8px 10px;font-size:11px;font-weight:800;cursor:pointer;">AI öneri al</button><button type="button" onclick="kpManuelSil(' + record.id + ')" style="background:#FEF2F2;color:#DC2626;border:1px solid #FECACA;border-radius:9px;padding:8px 10px;font-size:11px;font-weight:800;cursor:pointer;">Sil</button></div></div></div>';
    }).join('');
  }

  function buildManualDetail(record) {
    var preview = record.media_type === 'video'
      ? '<video controls preload="metadata" poster="' + esc(record.thumbnail_url || '') + '" style="width:100%;max-height:320px;border-radius:16px;background:#0F172A;"><source src="' + esc(record.file_url || '') + '" type="' + esc(record.mime_type || 'video/mp4') + '"></video>'
      : mediaPreviewHtml(record, false);
    var suggestions = record.ai_suggestions && record.ai_suggestions.draft ? record.ai_suggestions.draft : null;
    var suggestionBox = suggestions
      ? '<div style="margin-top:12px;padding:14px;border-radius:14px;background:#FFF7ED;border:1px solid #FED7AA;"><div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;"><div style="font-size:13px;font-weight:800;color:#C2410C;">AI taslak önerileri</div><button type="button" onclick="kpManualOneriUygulaTumu()" style="background:#C2410C;color:white;border:none;border-radius:8px;padding:8px 10px;font-size:11px;font-weight:800;cursor:pointer;">Forma doldur</button></div><div style="display:grid;gap:8px;margin-top:10px;"><div style="font-size:12px;color:#7C2D12;"><strong>Başlık:</strong> ' + esc(suggestions.title || '—') + '</div><div style="font-size:12px;color:#7C2D12;"><strong>Açıklama:</strong> ' + esc(suggestions.description || '—') + '</div><div style="font-size:12px;color:#7C2D12;"><strong>Olay tipi:</strong> ' + esc(suggestions.event_type || '—') + '</div><div style="font-size:12px;color:#7C2D12;"><strong>Etiketler:</strong> ' + esc(ensureArray(suggestions.tags).join(', ') || '—') + '</div></div><div style="font-size:11px;color:#9A3412;margin-top:10px;">Bu öneriler sadece taslaktır. Alanlara uygulanır ama siz kaydetmeden kalıcı olmaz.</div></div>'
      : '<div id="kpManualSuggestionHint" style="margin-top:12px;padding:12px 14px;border-radius:12px;background:#F8FAFC;border:1px solid #E2E8F0;font-size:12px;color:#64748B;">Henüz AI önerisi alınmadı.</div>';
    return '<div style="display:grid;gap:16px;">' + preview + '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;"><div><div style="font-size:11px;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Şantiye</div><div style="font-size:13px;font-weight:700;color:#0F172A;">' + esc(record.santiye_adi || 'Bağlı değil') + '</div></div><div><div style="font-size:11px;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Yükleyen</div><div style="font-size:13px;font-weight:700;color:#0F172A;">' + esc(record.uploaded_by || '—') + '</div></div><div><div style="font-size:11px;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Çekim zamanı</div><div style="font-size:13px;font-weight:700;color:#0F172A;">' + esc(formatDateTime(record.captured_at)) + '</div></div><div><div style="font-size:11px;font-weight:800;color:#64748B;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Dosya</div><div style="font-size:13px;font-weight:700;color:#0F172A;">' + esc(record.file_name || '—') + ' • ' + esc(formatBytes(record.file_size)) + '</div></div></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;"><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Başlık</label><input id="kpManualDetailTitle" type="text" value="' + esc(record.title || '') + '" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Olay tipi</label><input id="kpManualDetailEventType" type="text" value="' + esc(record.event_type || '') + '" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Alan / Bölge</label><input id="kpManualDetailZone" type="text" value="' + esc(record.zone_label || '') + '" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Çekim zamanı</label><input id="kpManualDetailCapturedAt" type="datetime-local" value="' + esc(toDatetimeLocal(record.captured_at || record.uploaded_at)) + '" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div></div><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Etiketler</label><input id="kpManualDetailTags" type="text" value="' + esc(ensureArray(record.tags).join(', ')) + '" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Açıklama</label><textarea id="kpManualDetailDescription" style="width:100%;min-height:110px;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;font-family:inherit;resize:vertical;">' + esc(record.description || '') + '</textarea></div>' + suggestionBox + '<div style="display:flex;gap:8px;flex-wrap:wrap;"><button type="button" onclick="kpManualDetayKaydet(' + record.id + ')" style="background:#0F172A;color:white;border:none;border-radius:10px;padding:10px 14px;font-size:12px;font-weight:800;cursor:pointer;">Taslağı kaydet</button><button type="button" onclick="kpManualAiOneriGetir(' + record.id + ')" style="background:#FFF7ED;color:#F97316;border:1px solid #FED7AA;border-radius:10px;padding:10px 14px;font-size:12px;font-weight:800;cursor:pointer;">AI öneri al</button><button type="button" onclick="kpDailyReportBaglaModalAc(\'manual\',' + record.id + ')" style="background:#EFF6FF;color:#1D4ED8;border:1px solid #BFDBFE;border-radius:10px;padding:10px 14px;font-size:12px;font-weight:800;cursor:pointer;">Günlük rapora ekle</button></div></div>';
  }

  function updateCurrentManualRecord(record) {
    window._kpManualDetailRecord = record;
    syncManualRecords([record]);
    renderManualCards();
    if (document.getElementById('arsivPage') && document.getElementById('arsivPage').style.display === 'flex') {
      window.arsivIstatistikGuncelle();
      window.arsivRenderListe();
    }
  }

  function fillManualSuggestionIntoForm() {
    if (!window._kpManualDetailRecord || !window._kpManualDetailRecord.ai_suggestions || !window._kpManualDetailRecord.ai_suggestions.draft) return;
    var draft = window._kpManualDetailRecord.ai_suggestions.draft;
    var title = document.getElementById('kpManualDetailTitle');
    var description = document.getElementById('kpManualDetailDescription');
    var eventType = document.getElementById('kpManualDetailEventType');
    var tags = document.getElementById('kpManualDetailTags');
    if (title && draft.title) title.value = draft.title;
    if (description && draft.description) description.value = draft.description;
    if (eventType && draft.event_type) eventType.value = draft.event_type;
    if (tags && ensureArray(draft.tags).length) tags.value = ensureArray(draft.tags).join(', ');
    if (typeof window.showToast === 'function') window.showToast('AI önerileri forma uygulandı. Kaydetmeden kalıcı olmaz.', 'info');
  }

  function ensureDailyReportModal() {
    if (document.getElementById('kpDailyReportLinkModal')) return;
    var modal = document.createElement('div');
    modal.id = 'kpDailyReportLinkModal';
    modal.style.cssText = 'display:none;position:fixed;inset:0;background:rgba(15,23,42,0.7);z-index:10001;align-items:center;justify-content:center;padding:16px;backdrop-filter:blur(6px);';
    modal.innerHTML = '<div style="width:100%;max-width:520px;background:#FFFFFF;border:1px solid #E2E8F0;border-radius:18px;box-shadow:0 24px 80px rgba(15,23,42,0.22);overflow:hidden;"><div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:18px 20px;border-bottom:1px solid #E2E8F0;background:#0F172A;"><div><div style="font-size:15px;font-weight:800;color:white;">Günlük rapora ekle</div><div id="kpDailyReportModalSub" style="font-size:12px;color:#CBD5E1;margin-top:4px;">Kanıt günlük raporun ilgili bölümüne bağlanacak.</div></div><button type="button" onclick="kpDailyReportBaglaKapat()" style="width:34px;height:34px;border:none;border-radius:10px;background:rgba(255,255,255,0.1);color:white;font-size:18px;cursor:pointer;">×</button></div><div style="padding:18px 20px;display:grid;gap:12px;"><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Kayıt</label><div id="kpDailyReportModalTitle" style="font-size:14px;font-weight:800;color:#0F172A;">—</div></div><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;"><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Rapor tarihi</label><input id="kpDailyReportDate" type="date" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;"></div><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Bölüm</label><select id="kpDailyReportSection" style="width:100%;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;">' + Object.keys(DAILY_REPORT_SECTIONS).map(function (key) { return '<option value="' + esc(key) + '">' + esc(DAILY_REPORT_SECTIONS[key]) + '</option>'; }).join('') + '</select></div></div><div><label style="display:block;font-size:11px;font-weight:800;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;">Not</label><textarea id="kpDailyReportNote" placeholder="Bu kanıtın günlük rapora nasıl yansımasını istediğinizi kısaca yazın..." style="width:100%;min-height:90px;padding:10px 12px;border:1.5px solid #E2E8F0;border-radius:10px;background:#F8FAFC;font-size:13px;color:#0F172A;box-sizing:border-box;font-family:inherit;resize:vertical;"></textarea></div><div id="kpDailyReportModalStatus" style="display:none;"></div><div style="display:flex;justify-content:flex-end;gap:8px;flex-wrap:wrap;"><button type="button" onclick="kpDailyReportBaglaKapat()" style="background:#F8FAFC;border:1px solid #E2E8F0;color:#475569;padding:10px 14px;border-radius:10px;cursor:pointer;font-size:12px;font-weight:700;">Vazgeç</button><button type="button" onclick="kpDailyReportBaglaKaydet()" style="background:#0F172A;border:none;color:white;padding:10px 14px;border-radius:10px;cursor:pointer;font-size:12px;font-weight:800;">Günlük rapora ekle</button></div></div></div>';
    modal.addEventListener('click', function (event) {
      if (event.target === modal) window.kpDailyReportBaglaKapat();
    });
    document.body.appendChild(modal);
  }

  // Bridge for manual_archive.js — arsivDetayGoster (which stays in archive) calls this
  // to build the detail view HTML for a manual record.
  window.kpBuildManualDetail = buildManualDetail;

  // Bridge for manual_archive.js — arsivSil calls this when deleting a manual record.
  window.kpRemoveManualRecord = removeManualRecordFromState;

  window.kpManualFilesSecildi = function (event) { renderManualFileList(Array.from(((event && event.target) || {}).files || [])); };
  window.kpManuelPanelKapat = function () { var panel = document.getElementById('kpManuelForm'); if (panel) panel.style.display = 'none'; };
  window.kpManuelEkleAc = function () { ensureManualPanel(); var panel = document.getElementById('kpManuelForm'); if (!panel) return; panel.style.display = panel.style.display === 'none' ? 'block' : 'none'; if (panel.style.display !== 'none') { clearManualUploadFeedback(); panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); } };
  window.kpManuelKaydet = async function () { if (_kpManualUploadState.uploading) return; try { var payload = collectManualPayload(); _kpManualUploadState.lastPayload = payload; _kpManualUploadState.uploading = true; clearManualUploadFeedback(); setManualUploadStatus('Yükleme hazırlanıyor...', 3, 'info'); var data = await uploadManualEvidence(payload); syncManualRecords(data.kayitlar || []); renderManualCards(); if (typeof window.showToast === 'function') window.showToast(data.mesaj || 'Manuel kanıt kaydedildi.', 'success'); var panel = document.getElementById('kpManuelForm'); if (panel) panel.style.display = 'none'; ensureManualPanel(); if (document.getElementById('arsivPage') && document.getElementById('arsivPage').style.display === 'flex') { window.arsivIstatistikGuncelle(); window.arsivRenderListe(); } } catch (err) { showManualUploadError(err.message || 'Yükleme sırasında hata oluştu.'); if (typeof window.showToast === 'function') window.showToast(err.message || 'Yükleme sırasında hata oluştu.', 'error'); } finally { _kpManualUploadState.uploading = false; } };
  window.kpManualRetrySonYukleme = async function () { if (!_kpManualUploadState.lastPayload) { if (typeof window.showToast === 'function') window.showToast('Tekrar denenecek bir yükleme bulunamadı.', 'warning'); return; } if (_kpManualUploadState.uploading) return; try { _kpManualUploadState.uploading = true; clearManualUploadFeedback(); setManualUploadStatus('Son yükleme tekrar deneniyor...', 4, 'info'); var data = await uploadManualEvidence(_kpManualUploadState.lastPayload); syncManualRecords(data.kayitlar || []); renderManualCards(); if (typeof window.showToast === 'function') window.showToast('Yükleme başarıyla tekrarlandı.', 'success'); } catch (err) { showManualUploadError(err.message || 'Yükleme tekrar edilemedi.'); } finally { _kpManualUploadState.uploading = false; } };
  window.kpManuelYukle = async function () { ensureManualPanel(); var token = getToken(); if (!token) return; var container = document.getElementById('kpManuelKartlar'); var empty = document.getElementById('kpManuelEmpty'); if (container) { container.style.display = 'grid'; container.innerHTML = '<div style="grid-column:1 / -1;padding:24px;text-align:center;color:#94A3B8;font-size:13px;">Manuel kanıtlar yükleniyor...</div>'; } if (empty) empty.style.display = 'none'; try { var url = '/manual-evidence?token=' + encodeURIComponent(token); if (getActiveSiteId()) url += '&santiye_id=' + encodeURIComponent(getActiveSiteId()); var data = await apiJson(url); window._kpManuelKayitlar = sortByNewest(data.kayitlar || []); renderManualCards(); } catch (err) { window._kpManuelKayitlar = []; renderManualCards(); if (container) { container.style.display = 'block'; container.innerHTML = '<div style="padding:24px;text-align:center;color:#EF4444;font-size:13px;">Manuel kanıtlar yüklenemedi.</div>'; } } };
  window.kpRenderManuelKartlar = renderManualCards;
  window.kpManuelSil = async function (id) { if (!window.confirm('Bu manuel kanıt arşivden kaldırılacak. Devam edilsin mi?')) return; try { await apiJson('/manual-evidence/' + id + '?token=' + encodeURIComponent(getToken()), { method: 'DELETE' }); removeManualRecordFromState(id); renderManualCards(); if (document.getElementById('arsivPage') && document.getElementById('arsivPage').style.display === 'flex') { window.arsivIstatistikGuncelle(); window.arsivRenderListe(); } if (window._kpManualDetailRecord && Number(window._kpManualDetailRecord.id) === Number(id) && typeof window.arsivDetayKapat === 'function') window.arsivDetayKapat(); if (typeof window.showToast === 'function') window.showToast('Manuel kanıt silindi.', 'success'); } catch (err) { if (typeof window.showToast === 'function') window.showToast(err.message || 'Silme işlemi başarısız oldu.', 'error'); } };
  window.kpManualDetayKaydet = async function (id) { if (!window._kpManualDetailRecord) return; try { var payload = { token: getToken(), title: (document.getElementById('kpManualDetailTitle') || {}).value || '', description: (document.getElementById('kpManualDetailDescription') || {}).value || '', event_type: (document.getElementById('kpManualDetailEventType') || {}).value || '', zone_label: (document.getElementById('kpManualDetailZone') || {}).value || '', captured_at: (document.getElementById('kpManualDetailCapturedAt') || {}).value || '', tags: (document.getElementById('kpManualDetailTags') || {}).value || '' }; var data = await apiJson('/manual-evidence/' + id, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }); updateCurrentManualRecord(data); openDefaultDetailModal('Manuel Kanıt', buildManualDetail(data)); if (typeof window.showToast === 'function') window.showToast('Manuel kanıt güncellendi.', 'success'); } catch (err) { if (typeof window.showToast === 'function') window.showToast(err.message || 'Güncelleme tamamlanamadı.', 'error'); } };
  window.kpManualAiOneriGetir = async function (id) { try { var suggestions = await apiJson('/manual-evidence/' + id + '/ai-suggestions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token: getToken() }) }); if (window._kpManualDetailRecord && Number(window._kpManualDetailRecord.id) === Number(id)) { window._kpManualDetailRecord.ai_suggestions = suggestions; openDefaultDetailModal('Manuel Kanıt', buildManualDetail(window._kpManualDetailRecord)); } var record = findArchiveRecord('manual', id); if (record) record.ai_suggestions = suggestions; if (typeof window.showToast === 'function') window.showToast('AI taslak önerileri hazır.', 'success'); } catch (err) { if (typeof window.showToast === 'function') window.showToast(err.message || 'AI önerileri alınamadı.', 'error'); } };
  window.kpManualAiOneriAc = function (id) { window.arsivDetayGoster('manual', id); setTimeout(function () { window.kpManualAiOneriGetir(id); }, 160); };
  window.kpManualOneriUygulaTumu = fillManualSuggestionIntoForm;
  window.kpDailyReportBaglaModalAc = function (sourceType, sourceId) { ensureDailyReportModal(); var modal = document.getElementById('kpDailyReportLinkModal'); var record = findArchiveRecord(sourceType, sourceId) || findArchiveRecord('manual', sourceId); var titleEl = document.getElementById('kpDailyReportModalTitle'); var subEl = document.getElementById('kpDailyReportModalSub'); var statusEl = document.getElementById('kpDailyReportModalStatus'); modal.dataset.sourceType = sourceType; modal.dataset.sourceId = String(sourceId); modal.dataset.santiyeId = String((record && record.santiye_id) || getActiveSiteId() || ''); if (titleEl) titleEl.textContent = (record && (record.title || record.ozet)) || ('Kayıt #' + sourceId); if (subEl) subEl.textContent = ((record && record.santiye_adi) || getActiveSiteName()) + ' • ' + ((record && record.event_type) || 'Genel kayıt'); if (statusEl) { statusEl.style.display = 'none'; statusEl.innerHTML = ''; } var dateInput = document.getElementById('kpDailyReportDate'); if (dateInput) dateInput.value = new Date().toISOString().slice(0, 10); var note = document.getElementById('kpDailyReportNote'); if (note) note.value = ''; modal.style.display = 'flex'; };
  window.kpDailyReportBaglaKapat = function () { var modal = document.getElementById('kpDailyReportLinkModal'); if (modal) modal.style.display = 'none'; };
  window.kpDailyReportBaglaKaydet = async function () { var modal = document.getElementById('kpDailyReportLinkModal'); if (!modal) return; var statusEl = document.getElementById('kpDailyReportModalStatus'); try { var payload = { token: getToken(), source_type: modal.dataset.sourceType || 'manual', source_id: Number(modal.dataset.sourceId || 0), report_date: (document.getElementById('kpDailyReportDate') || {}).value || new Date().toISOString().slice(0, 10), section_key: (document.getElementById('kpDailyReportSection') || {}).value || 'ilerleme', note: (document.getElementById('kpDailyReportNote') || {}).value || '', santiye_id: modal.dataset.santiyeId ? Number(modal.dataset.santiyeId) : null }; if (statusEl) { statusEl.style.display = 'block'; statusEl.innerHTML = '<div style="padding:10px 12px;border-radius:10px;background:#F8FAFC;border:1px solid #E2E8F0;font-size:12px;color:#475569;">Günlük rapora ekleniyor...</div>'; } var data = await apiJson('/daily-reports/items', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }); if (statusEl) { statusEl.style.display = 'block'; statusEl.innerHTML = '<div style="padding:10px 12px;border-radius:10px;background:#ECFDF5;border:1px solid #BBF7D0;font-size:12px;color:#166534;">' + esc(data.mesaj || 'Günlük rapora eklendi.') + '</div>'; } if (typeof window.showToast === 'function') window.showToast(data.mesaj || 'Günlük rapora eklendi.', 'success'); setTimeout(window.kpDailyReportBaglaKapat, 500); } catch (err) { if (statusEl) { statusEl.style.display = 'block'; statusEl.innerHTML = '<div style="padding:10px 12px;border-radius:10px;background:#FEF2F2;border:1px solid #FECACA;font-size:12px;color:#B91C1C;">' + esc(err.message || 'İşlem tamamlanamadı.') + '</div>'; } if (typeof window.showToast === 'function') window.showToast(err.message || 'Günlük rapora ekleme başarısız oldu.', 'error'); } };

  ensureManualPanel();
})();
