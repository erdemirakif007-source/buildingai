/**
 * BIMViewer.ts — Ana Orkestratör Sınıfı
 *
 * BIM Viewer uygulamasının tüm alt sistemlerini koordine eder:
 *  - UI inject: Toolbar, Sidebar, Viewport, Properties Panel, Statusbar
 *  - Three.js sahne başlatma (sceneSetup.ts)
 *  - IFC yükleme (ifcLoader.ts / IFCLoaderEngine)
 *  - Drag & drop, file input, keyboard kısayollar
 *  - FPS sayacı, durum çubuğu güncellemeleri
 *  - Model ağacı (spatial structure), properties panel
 *
 * ─── MIMARI GENEL BAKIŞ ─────────────────────────────────────────────────
 *
 *  BIMViewer
 *  ├── initScene()            → SceneContext (Three.js sahne, kamera, renderer)
 *  ├── IFCLoaderEngine        → IFC → Fragment → THREE.Object3D
 *  ├── UI: toolbar            → File input, dropdown menus, camera presets
 *  ├── UI: sidebar            → Model ağacı (getSpatialStructure)
 *  ├── UI: properties panel   → Seçilen eleman özellikleri
 *  └── UI: statusbar          → FPS, model adı, element sayısı
 */
import * as THREE from 'three';
import { initScene } from './sceneSetup';
import { IFCLoaderEngine } from './ifcLoader';
import { StoreyManager } from './storeyManager';
import { ProgressColoring } from './progressColoring';
import { ClippingPlaneManager } from './clippingPlane';
import { AutoDimensionTool } from './measurementTool';
import { ElementPicker } from './elementPicker';
import { initIfcExportGuide } from '../ui/ifcExportGuide';
import { MappingPanel, addMappingToolbarButton } from '../ui/mappingPanel';
import { getBIMApiClient } from '../api/bimApi';
// ─── Ana Sınıf ────────────────────────────────────────────────────────────────
export class BIMViewer {
    // ─── Constructor ──────────────────────────────────────────────────────────
    /**
     * @param containerId - HTML container element'inin ID'si
     *                      BIMViewer bu element'in içine tam UI'ı inject eder.
     */
    constructor(containerId) {
        this._ctx = null;
        this._engine = null;
        this._initialized = false;
        this._isDisposed = false;
        // ── Durum ────────────────────────────────────────────────────────────────
        this._sidebarCollapsed = false;
        this._propPanelOpen = false;
        this._currentFile = null;
        this._storeyVisibility = new Map();
        // ── StoreyManager ───────────────────────────────────────────────────────
        this._storeyManager = null;
        this._contextMenuEl = null;
        this._contextMenuStoreyId = null;
        // ── ProgressColoring ────────────────────────────────────────────────
        this._progressColoring = null;
        // ── ClippingPlaneManager ─────────────────────────────────────────────
        this._clippingMgr = null;
        /** Y eksenindeki kat kesit düzleminin ID'si (kat kesiti modu için) */
        this._floorSectionPlaneId = null;
        // ── AutoDimensionTool ────────────────────────────────────────────────────
        this._measurementTool = null;
        // ── ElementPicker ─────────────────────────────────────────────────────────
        this._elementPicker = null;
        // ── Slider / Controls çakışma düzeltmesi ─────────────────────────────────
        this._sliderPointerUpBound = null;
        // ── FPS Sayacı ───────────────────────────────────────────────────────────
        this._fpsFrameCount = 0;
        this._fpsLastTime = performance.now();
        this._fpsRafId = null;
        // ── Drag & Drop ──────────────────────────────────────────────────────────
        this._dragDepth = 0; // enter/leave sayacı (child element'lar için)
        // ── Compact Mode ─────────────────────────────────────────────────────────
        this._compact = false;
        // ── MappingPanel ──────────────────────────────────────────────────────────
        this._mappingPanel = null;
        /** URL'den okunan backend model ID'si (sadece compact modda mevcut) */
        this._compactModelId = null;
        /** URL'den okunan şantiye ID'si (sadece compact modda mevcut) */
        this._compactSantiyeId = null;
        /** Progress polling durdurma fonksiyonu */
        this._stopProgressPolling = null;
        this._containerId = containerId;
    }
    // ─── Public API ───────────────────────────────────────────────────────────
    /**
     * Viewer'ı başlatır. Sırasıyla:
     * 1. HTML yapısını inject eder
     * 2. Three.js sahnesini başlatır
     * 3. IFCLoaderEngine'i başlatır
     * 4. Event'leri bağlar
     */
    async initialize() {
        if (this._initialized)
            return;
        console.log('[BIMViewer] Başlatılıyor...');
        // 1. HTML yapısını container'a inject et
        this._buildHTML();
        // Compact mode: URL'de compact=true varsa toolbar/sidebar/statusbar gizle
        this._applyCompactModeIfNeeded();
        // 2. Three.js sahnesini viewport'a mount et
        this._initScene();
        // 3. IFC motor başlat (WASM + Fragment worker)
        await this._initEngine();
        // 4. ElementPicker — IFC element seçimi ve highlight (engine + scene gerektirir)
        this._initElementPicker();
        // 5. Event binding
        this._bindToolbarEvents();
        this._bindDropdowns();
        this._bindDragDrop();
        this._bindKeyboard();
        // 6. FPS sayacını başlat
        this._startFPSCounter();
        // 7. URL'deki model_id'yi otomatik yükle (model_id varsa her zaman, auto_load ile santiye_id de desteklenir)
        {
            const params = new URLSearchParams(window.location.search);
            const modelIdStr = params.get('model_id');
            const santiyeIdStr = params.get('santiye_id');
            const autoLoad = params.get('auto_load') === 'true';
            if (modelIdStr) {
                void this._autoLoadModel(parseInt(modelIdStr, 10));
            }
            else if (autoLoad && santiyeIdStr) {
                void this._autoLoadFirstModel(parseInt(santiyeIdStr, 10));
            }
        }
        this._initialized = true;
        console.log('[BIMViewer] ✓ Hazır.');
    }
    /**
     * IFC dosyasını yükler (dışarıdan çağrılabilir — örn. debug için).
     */
    async loadIFC(file) {
        await this._handleFile(file);
    }
    /**
     * Properties panelini açar ve verilen elemanın özelliklerini gösterir.
     * Faz 3'te raycasting entegrasyonu bunu çağıracak.
     */
    openProperties(data) {
        this._openProperties(data);
    }
    /** Viewer'ı ve tüm kaynakları temizler. */
    async dispose() {
        if (this._isDisposed)
            return;
        this._isDisposed = true;
        if (this._fpsRafId !== null)
            cancelAnimationFrame(this._fpsRafId);
        this._stopProgressPolling?.();
        this._stopProgressPolling = null;
        this._mappingPanel?.destroy();
        this._mappingPanel = null;
        if (this._engine)
            await this._engine.dispose();
        this._clippingMgr?.dispose();
        this._measurementTool?.dispose();
        if (this._elementPicker)
            await this._elementPicker.dispose();
        if (this._sliderPointerUpBound) {
            window.removeEventListener('pointerup', this._sliderPointerUpBound);
            this._sliderPointerUpBound = null;
        }
        if (this._ctx)
            this._ctx.dispose();
        this._ctx = null;
        this._engine = null;
        this._clippingMgr = null;
        this._measurementTool = null;
        this._elementPicker = null;
        console.log('[BIMViewer] Kaynaklar temizlendi.');
    }
    // ─── Compact Mode ─────────────────────────────────────────────────────────
    /** URL'de compact=true varsa toolbar, sidebar ve statusbar'ı gizler. */
    _applyCompactModeIfNeeded() {
        const params = new URLSearchParams(window.location.search);
        if (params.get('compact') !== 'true')
            return;
        this._compact = true;
        const modelIdStr = params.get('model_id');
        const santiyeIdStr = params.get('santiye_id');
        if (modelIdStr)
            this._compactModelId = parseInt(modelIdStr, 10);
        if (santiyeIdStr)
            this._compactSantiyeId = parseInt(santiyeIdStr, 10);
        const toolbar = document.getElementById('bv-toolbar');
        const sidebar = document.getElementById('bv-sidebar');
        const statusbar = document.getElementById('bv-statusbar');
        if (toolbar)
            toolbar.style.display = 'none';
        if (sidebar)
            sidebar.style.display = 'none';
        if (statusbar)
            statusbar.style.display = 'none';
        document.body.style.background = '#1E293B';
        document.body.style.margin = '0';
        document.body.style.overflow = 'hidden';
    }
    /** Compact modda model_id URL parametresinden modeli otomatik yükler.
     *  Backend'de .frag dosyası varsa fragment olarak yükler (10× hızlı),
     *  yoksa IFC parse akışına düşer. */
    async _autoLoadModel(modelId) {
        if (!this._engine)
            return;
        try {
            const token = localStorage.getItem('bai_token') ?? '';
            const response = await fetch(`/api/bim/model/${modelId}/download`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (!response.ok)
                throw new Error(`HTTP ${response.status}`);
            // Content-Disposition başlığından gerçek dosya adını çıkar
            const disposition = response.headers.get('Content-Disposition') ?? '';
            const nameMatch = disposition.match(/filename[^;=\n]*=([^;\n]*)/);
            const serverName = nameMatch ? nameMatch[1].replace(/['"]/g, '').trim() : '';
            const isFrag = serverName.endsWith('.frag');
            const buffer = await response.arrayBuffer();
            if (isFrag) {
                this._showLoading(serverName || `model_${modelId}.frag`);
                this._currentFile = serverName || `model_${modelId}.frag`;
                await this._engine.loadFragment(buffer, `model_${modelId}`);
            }
            else {
                const fileName = serverName || `model_${modelId}.ifc`;
                const file = new File([buffer], fileName);
                await this._handleFile(file);
            }
        }
        catch (err) {
            console.warn('[BIMViewer] Compact auto-load başarısız:', err);
        }
    }
    /** Şantiye ID'sine göre ilk modeli otomatik yükler (auto_load modu). */
    async _autoLoadFirstModel(santiyeId) {
        if (!this._engine)
            return;
        try {
            const token = localStorage.getItem('bai_token') ?? '';
            const response = await fetch(`/api/bim/models?santiye_id=${santiyeId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            if (!response.ok)
                throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (!data.modeller?.length) {
                console.warn('[BIMViewer] Bu şantiye için model bulunamadı:', santiyeId);
                return;
            }
            await this._autoLoadModel(data.modeller[0].id);
        }
        catch (err) {
            console.warn('[BIMViewer] auto_load başarısız:', err);
        }
    }
    // ─── HTML Yapısı ──────────────────────────────────────────────────────────
    _buildHTML() {
        const container = document.getElementById(this._containerId);
        if (!container)
            throw new Error(`Container bulunamadı: #${this._containerId}`);
        container.innerHTML = `
<div class="bv-app" id="bv-app">

  <!-- ── TOOLBAR ── -->
  <header class="bv-toolbar" id="bv-toolbar" role="toolbar" aria-label="BIM Viewer araç çubuğu">
    <!-- Logo -->
    <div class="bv-logo" aria-label="BuildingAI BIM Viewer">
      <div class="bv-logo-icon">B</div>
      <div class="bv-logo-text">BuildingAI <span>BIM</span></div>
    </div>
    <div class="bv-separator"></div>

    <!-- IFC Yükle butonu -->
    <button class="bv-btn bv-btn--primary" id="bv-btn-load" title="IFC dosyası yükle (Ctrl+O)" aria-label="IFC Yükle">
      <span>📂</span> IFC Yükle
    </button>
    <input type="file" id="bv-file-input" accept=".ifc,.IFC" style="display:none" aria-hidden="true" />

    <div class="bv-separator"></div>

    <!-- Görünüm dropdown -->
    <div class="bv-dropdown" id="bv-dropdown-view">
      <button class="bv-btn bv-dropdown-trigger" id="bv-btn-view" aria-haspopup="menu" aria-expanded="false">
        <span>👁</span> Görünüm <span class="bv-chevron">▾</span>
      </button>
      <div class="bv-dropdown-menu" role="menu" aria-label="Görünüm seçenekleri">
        <div class="bv-dropdown-label">Kamera Modu</div>
        <button class="bv-dropdown-item bv-item--camera bv-dropdown-item--active" data-preset="perspective" role="menuitem">
          <span class="bv-item-icon">🎥</span> Perspektif
        </button>

        <div class="bv-dropdown-divider"></div>
        <div class="bv-dropdown-label">Kamera Açısı</div>
        <button class="bv-dropdown-item bv-item--camera" data-preset="top" role="menuitem">
          <span class="bv-item-icon">⬇</span> Üstten
        </button>
        <button class="bv-dropdown-item bv-item--camera" data-preset="front" role="menuitem">
          <span class="bv-item-icon">↙</span> Önden
        </button>
        <button class="bv-dropdown-item bv-item--camera" data-preset="right" role="menuitem">
          <span class="bv-item-icon">→</span> Sağdan
        </button>
        <button class="bv-dropdown-item bv-item--camera" data-preset="isometric" role="menuitem">
          <span class="bv-item-icon">📐</span> İzometrik
        </button>

        <div class="bv-dropdown-divider"></div>
        <div class="bv-dropdown-label">Sahne</div>
        <button class="bv-dropdown-item" id="bv-item-grid" role="menuitemcheckbox" aria-checked="true">
          <span class="bv-item-icon">⬡</span> Grid Göster
          <span class="bv-item-badge" id="bv-grid-badge">Açık</span>
        </button>
      </div>
    </div>

    <!-- Araçlar dropdown -->
    <div class="bv-dropdown" id="bv-dropdown-tools">
      <button class="bv-btn bv-dropdown-trigger" id="bv-btn-tools" aria-haspopup="menu" aria-expanded="false">
        <span>🔧</span> Araçlar <span class="bv-chevron">▾</span>
      </button>
      <div class="bv-dropdown-menu" role="menu" aria-label="Araçlar">
        <button class="bv-dropdown-item" id="bv-item-measure" role="menuitemcheckbox" aria-checked="false">
          <span class="bv-item-icon">📏</span> Ölçüm
          <span class="bv-item-badge" id="bv-measure-badge"></span>
        </button>
        <div class="bv-dropdown-divider"></div>
        <div class="bv-dropdown-label">Kesit Düzlemi</div>
        <button class="bv-dropdown-item bv-item--clip" data-clip-axis="x" role="menuitem">
          <span class="bv-item-icon">↔️</span> X Ekseni Kes
        </button>
        <button class="bv-dropdown-item bv-item--clip" data-clip-axis="y" role="menuitem">
          <span class="bv-item-icon">↕️</span> Y Ekseni Kes
        </button>
        <button class="bv-dropdown-item bv-item--clip" data-clip-axis="z" role="menuitem">
          <span class="bv-item-icon">🔄</span> Z Ekseni Kes
        </button>
        <button class="bv-dropdown-item" id="bv-item-clip-all-remove" role="menuitem">
          <span class="bv-item-icon">🚫</span> Tüm Kesitleri Kaldır
        </button>
        <div class="bv-dropdown-divider"></div>
        <button class="bv-dropdown-item" id="bv-item-unload" disabled role="menuitem">
          <span class="bv-item-icon">🗑</span> Modeli Kaldır
        </button>
      </div>
    </div>

    <!-- Renk Modu dropdown -->
    <div class="bv-dropdown" id="bv-dropdown-color">
      <button class="bv-btn bv-dropdown-trigger" id="bv-btn-color" aria-haspopup="menu" aria-expanded="false">
        <span>🎨</span> Renk <span class="bv-chevron">▾</span>
      </button>
      <div class="bv-dropdown-menu" role="menu" aria-label="Renk modu">
        <div class="bv-dropdown-label">Renk Modu</div>
        <button class="bv-dropdown-item bv-item--color bv-dropdown-item--active" data-color-mode="original" role="menuitem">
          <span class="bv-item-icon">🎨</span> Orijinal
          <span class="bv-item-badge" id="bv-color-badge-original">Aktif</span>
        </button>
        <button class="bv-dropdown-item bv-item--color" data-color-mode="progress" role="menuitem">
          <span class="bv-item-icon">📊</span> İlerleme Durumu
        </button>
        <button class="bv-dropdown-item bv-item--color" data-color-mode="type" role="menuitem">
          <span class="bv-item-icon">🏗</span> IFC Tipi
        </button>
        <button class="bv-dropdown-item bv-item--color" data-color-mode="storey" role="menuitem">
          <span class="bv-item-icon">🏢</span> Kat
        </button>
        <div class="bv-dropdown-divider"></div>
        <div class="bv-dropdown-label">İlerleme</div>
        <button class="bv-dropdown-item" id="bv-item-apply-mock" disabled role="menuitem">
          <span class="bv-item-icon">🔄</span> Mock Veri Uygula
        </button>
        <button class="bv-dropdown-item" id="bv-item-clear-colors" disabled role="menuitem">
          <span class="bv-item-icon">❌</span> Renkleri Temizle
        </button>
      </div>
    </div>

    <div class="bv-toolbar-spacer"></div>

    <!-- IFC Rehberi -->
    <button class="bv-btn bv-btn--icon bv-btn--ghost" id="bv-btn-ifc-guide" title="IFC Export Rehberi" aria-label="IFC Export Rehberini aç" aria-haspopup="dialog">
      ❓
    </button>

    <!-- Fullscreen -->
    <button class="bv-btn bv-btn--icon bv-btn--ghost" id="bv-btn-fullscreen" title="Tam ekran (F11)" aria-label="Tam ekran">
      ⛶
    </button>
  </header>

  <!-- ── WORKSPACE ── -->
  <div class="bv-workspace">

    <!-- Sidebar (sol) -->
    <aside class="bv-sidebar" id="bv-sidebar" aria-label="Model ağacı paneli">
      <div class="bv-sidebar-header">
        <span class="bv-sidebar-title">Model Ağacı</span>
        <button class="bv-sidebar-toggle" id="bv-sidebar-toggle"
                title="Paneli daralt" aria-label="Sidebar kapat/aç">‹</button>
      </div>
      <div class="bv-sidebar-content" id="bv-tree-content" role="tree" aria-label="Model elemanları">
        <div class="bv-tree-empty" id="bv-tree-empty">
          <div class="bv-tree-empty-icon">🏗</div>
          <div class="bv-tree-empty-title">IFC dosyası yükleyin</div>
          <div class="bv-tree-empty-sub">Model yüklendikten sonra<br>kat listesi burada görünür</div>
        </div>
      </div>
    </aside>

    <!-- 3D Viewport -->
    <div class="bv-viewport" id="bv-viewport" role="main" aria-label="3D model görüntüleyici">
      <!-- Boş durum (model yüklenmeden önce) -->
      <div class="bv-viewport-empty" id="bv-viewport-empty" aria-hidden="true">
        <div class="bv-empty-icon">🏛</div>
        <div class="bv-empty-title">3D Görüntüleyici Hazır</div>
        <div class="bv-empty-hint">IFC dosyası açın veya bu alana sürükleyin</div>
      </div>

      <!-- Drag & Drop overlay -->
      <div class="bv-drag-overlay" id="bv-drag-overlay" aria-hidden="true">
        <div class="bv-drag-icon">📄</div>
        <div class="bv-drag-text">IFC dosyasını bırakın</div>
        <div class="bv-drag-sub">.ifc formatı desteklenir</div>
      </div>

      <!-- Loading overlay -->
      <div class="bv-loading-overlay hidden" id="bv-loading-overlay" role="status" aria-live="polite">
        <div class="bv-spinner"></div>
        <div class="bv-loading-info">
          <div class="bv-loading-file" id="bv-loading-file">Yükleniyor...</div>
          <div class="bv-loading-msg" id="bv-loading-msg">Hazırlanıyor...</div>
          <div class="bv-progress-track">
            <div class="bv-progress-fill" id="bv-progress-fill"></div>
          </div>
          <div class="bv-progress-pct" id="bv-progress-pct">0%</div>
        </div>
        <button class="bv-btn bv-btn--ghost bv-loading-cancel" id="bv-btn-cancel-load">
          İptal
        </button>
      </div>

      <!-- Kesit Düzlemi Paneli (sağ üst köşe, akordeon) -->
      <div class="bv-clipping-panel-wrap" id="bv-clipping-panel-wrap" aria-label="Kesit düzlemleri">
        <button class="bv-clipping-panel-header" id="bv-clipping-panel-toggle"
                aria-expanded="false" aria-controls="bv-clipping-panel"
                title="Kesit düzlemleri">
          <span class="bv-clip-hdr-icon">✂️</span>
          <span class="bv-clip-hdr-label">Kesit Düzlemleri</span>
          <span class="bv-clip-hdr-count" id="bv-clip-count">0</span>
          <span class="bv-clip-hdr-chevron">▾</span>
        </button>
        <div class="bv-clipping-panel" id="bv-clipping-panel" hidden>
          <div class="bv-clip-empty">
            <span class="bv-clip-empty-icon">✂️</span>
            <span>Aktif kesit düzlemi yok</span>
          </div>
        </div>
      </div>

      <!-- Ölçüm Paneli (sağ üst köşe, akordeon) -->
      <div class="bv-measure-panel-wrap" id="bv-measure-panel-wrap" aria-label="Ölçümler">
        <button class="bv-clipping-panel-header bv-measure-panel-header" id="bv-measure-panel-toggle"
                aria-expanded="false" aria-controls="bv-measure-panel"
                title="Ölçümler">
          <span class="bv-clip-hdr-icon">📏</span>
          <span class="bv-clip-hdr-label">Ölçümler</span>
          <span class="bv-clip-hdr-count" id="bv-measure-count">0</span>
          <span class="bv-clip-hdr-chevron">▾</span>
        </button>
        <div class="bv-measure-panel" id="bv-measure-panel" hidden>
          <div class="bv-clip-empty" id="bv-measure-empty">
            <span class="bv-clip-empty-icon">📏</span>
            <span>Henüz ölçüm yok</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Properties Panel (sağ, varsayılan gizli) -->
    <aside class="bv-properties closed" id="bv-properties" aria-label="Eleman özellikleri" aria-hidden="true">
      <div class="bv-props-header">
        <span class="bv-props-title">Özellikler</span>
        <button class="bv-btn bv-btn--icon" id="bv-props-close" aria-label="Kapat">✕</button>
      </div>
      <div class="bv-props-content" id="bv-props-content">
        <!-- İçerik dinamik olarak doldurulur -->
      </div>
    </aside>

  </div><!-- /workspace -->

  <!-- ── STATUSBAR ── -->
  <footer class="bv-statusbar" id="bv-statusbar" role="status" aria-live="polite">
    <div class="bv-status-segment">
      <div class="bv-status-dot" id="bv-status-dot"></div>
      <span class="bv-status-label">Model:</span>
      <span class="bv-status-value" id="bv-status-model">Yüklenmedi</span>
    </div>
    <div class="bv-status-segment">
      <span class="bv-status-label">Elementler:</span>
      <span class="bv-status-value" id="bv-status-elements">—</span>
    </div>
    <div class="bv-status-segment">
      <span class="bv-status-label">FPS:</span>
      <span class="bv-status-value bv-status-value--accent" id="bv-status-fps">—</span>
    </div>
  </footer>

</div><!-- /bv-app -->

<!-- Toast container (sabit konumlu) -->
<div class="bv-toast-container" id="bv-toast-container" aria-live="assertive" aria-atomic="true"></div>
`;
        // DOM referanslarını kaydet
        this._viewport = document.getElementById('bv-viewport');
        this._sidebarEl = document.getElementById('bv-sidebar');
        this._propPanel = document.getElementById('bv-properties');
        this._loadingOverlay = document.getElementById('bv-loading-overlay');
        this._dragOverlay = document.getElementById('bv-drag-overlay');
        this._progressFill = document.getElementById('bv-progress-fill');
        this._progressPct = document.getElementById('bv-progress-pct');
        this._loadingMsg = document.getElementById('bv-loading-msg');
        this._loadingFile = document.getElementById('bv-loading-file');
        this._statusModel = document.getElementById('bv-status-model');
        this._statusElements = document.getElementById('bv-status-elements');
        this._statusFps = document.getElementById('bv-status-fps');
        this._statusDot = document.getElementById('bv-status-dot');
        this._treeContent = document.getElementById('bv-tree-content');
        this._propContent = document.getElementById('bv-props-content');
        this._fileInput = document.getElementById('bv-file-input');
        this._toastContainer = document.getElementById('bv-toast-container');
        this._viewportEmpty = document.getElementById('bv-viewport-empty');
    }
    // ─── Sahne Başlatma ───────────────────────────────────────────────────────
    _initScene() {
        if (!this._viewport)
            throw new Error('[BIMViewer] Viewport elementi bulunamadı.');
        this._ctx = initScene(this._viewport);
        // ClippingPlaneManager'ı başlat
        this._clippingMgr = new ClippingPlaneManager(this._ctx.scene, this._ctx.renderer, this._ctx.camera, this._ctx.controls);
        this._clippingMgr.onPlanesChanged = (planes) => {
            this._updateClippingPanelUI(planes);
        };
        // CSS2DRenderer animation loop'a bağla (tool null iken de çalışır)
        this._ctx.onRenderCallbacks.push(() => {
            this._measurementTool?.updateRenderer();
        });
        // Resize olduğunda (fullscreen dahil) fragments LOD sistemini güncelle.
        // Viewport boyutu değişince frustum değişir; update(true) tile görünürlüğünü yeniler.
        this._ctx.onResizeCallbacks.push(() => {
            void this._engine?.fragments?.update(true);
        });
        console.log('[BIMViewer] ✓ Three.js sahnesi başlatıldı.');
    }
    // ─── IFC Motor Başlatma ───────────────────────────────────────────────────
    async _initEngine() {
        if (!this._ctx)
            throw new Error('[BIMViewer] Sahne başlatılmamış.');
        this._engine = new IFCLoaderEngine(this._ctx.scene, this._ctx.camera, this._ctx.controls);
        // Progress callback'i bağla
        this._engine.onProgress = (progress, message) => {
            this._updateProgress(progress, message);
        };
        // Model yüklendi callback'i
        this._engine.onModelLoaded = (modelId, model) => {
            void this._onModelLoaded(modelId, model);
        };
        // Hata callback'i
        this._engine.onError = (error) => {
            this._hideLoading();
            this._showToast({
                type: 'error',
                title: 'Yükleme Hatası',
                message: error.message,
                duration: 8000,
            });
        };
        try {
            await this._engine.init();
            console.log('[BIMViewer] ✓ IFCLoaderEngine başlatıldı.');
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            this._showToast({
                type: 'error',
                title: 'Engine Hatası',
                message: `Fragment engine başlatılamadı: ${msg}`,
                duration: 10000,
            });
        }
    }
    // ─── ElementPicker Başlatma ───────────────────────────────────────────────
    /**
     * ElementPicker'ı başlatır ve callback'lerini bağlar.
     * _initScene() ve _initEngine() çağrıldıktan sonra çağrılmalıdır.
     */
    _initElementPicker() {
        if (!this._ctx || !this._engine) {
            console.warn('[BIMViewer] ElementPicker başlatılamadı: ctx veya engine eksik.');
            return;
        }
        this._elementPicker = new ElementPicker(this._ctx.scene, this._ctx.camera, this._ctx.renderer, this._engine.loadedModels);
        // AutoDimensionTool — ElementPicker'dan sonra başlat (raycasting için kullanır)
        this._measurementTool = new AutoDimensionTool(this._ctx.scene, this._ctx.camera, this._ctx.renderer, this._viewport, this._engine.loadedModels, this._elementPicker);
        this._measurementTool.onDimensionAdded = () => { this._updateMeasurementPanelUI(); };
        this._measurementTool.onDimensionRemoved = () => { this._updateMeasurementPanelUI(); };
        // Element seçilince properties panelini ve MappingPanel'i güncelle
        this._elementPicker.onElementSelect = (info) => {
            // Ölçüm aracı aktifken element seçimi yapma
            if (this._measurementTool?.isActive)
                return;
            if (info) {
                const displayData = {
                    'Tip (IFC)': info.ifcType,
                    'Ad': info.name,
                    'GlobalId': info.globalId,
                    'Kat': info.storey || '—',
                    'expressId': info.expressId,
                    ...info.properties,
                };
                this._openProperties(displayData);
                // MappingPanel'e seçili elementi bildir
                if (this._mappingPanel?.isOpen) {
                    this._mappingPanel.setSelectedElement({
                        globalId: info.globalId,
                        ifcType: info.ifcType,
                        name: info.name,
                        storey: info.storey ?? '—',
                    });
                }
            }
            else {
                this._closeProperties();
                if (this._mappingPanel?.isOpen) {
                    this._mappingPanel.setSelectedElement(null);
                }
            }
        };
        // Hover: statusbar'da element adını göster
        this._elementPicker.onElementHover = (info) => {
            if (info) {
                this._statusElements.title = `${info.ifcType}: ${info.name}`;
            }
            else {
                this._statusElements.title = '';
            }
        };
        // ep:zoom custom event: ElementPicker çift tıkla zoom yaptığında
        // OrbitControls target'ını güncelle
        this._ctx.renderer.domElement.addEventListener('ep:zoom', (e) => {
            const { center } = e.detail;
            if (this._ctx) {
                this._ctx.controls.target.copy(center);
                this._ctx.controls.update();
            }
        });
        console.log('[BIMViewer] ✓ ElementPicker başlatıldı.');
    }
    // ─── Event Binding ────────────────────────────────────────────────────────
    /** Toolbar butonlarını bağlar */
    _bindToolbarEvents() {
        // IFC Yükle butonu
        document.getElementById('bv-btn-load')?.addEventListener('click', () => {
            this._fileInput.click();
        });
        // File input change
        this._fileInput.addEventListener('change', (e) => {
            const input = e.target;
            const file = input.files?.[0];
            if (file) {
                void this._handleFile(file);
                input.value = ''; // Aynı dosyayı tekrar seçebilmek için sıfırla
            }
        });
        // Renk Modu butonlarını bağla
        document.querySelectorAll('.bv-item--color').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const mode = e.currentTarget.dataset['colorMode'];
                if (mode && this._progressColoring) {
                    void this._progressColoring.setColorMode(mode);
                    this._updateColorModeUI(mode);
                }
            });
        });
        // Mock Veri Uygula
        document.getElementById('bv-item-apply-mock')?.addEventListener('click', () => {
            void this._applyMockProgressData();
        });
        // Renkleri Temizle
        document.getElementById('bv-item-clear-colors')?.addEventListener('click', () => {
            void this._progressColoring?.clearColors();
            this._updateColorModeUI('original');
        });
        // ── Ölçüm Panel Toggle ──────────────────────────────────────────────
        document.getElementById('bv-measure-panel-toggle')?.addEventListener('click', () => {
            const panel = document.getElementById('bv-measure-panel');
            const toggleBtn = document.getElementById('bv-measure-panel-toggle');
            if (!panel)
                return;
            const isOpen = !panel.hidden;
            panel.hidden = isOpen;
            toggleBtn?.setAttribute('aria-expanded', String(!isOpen));
            toggleBtn?.classList.toggle('open', !isOpen);
        });
        // ── Ölçüm Aracı Toggle ──────────────────────────────────────────────
        document.getElementById('bv-item-measure')?.addEventListener('click', () => {
            this._toggleMeasurementMode();
        });
        // Sidebar toggle
        document.getElementById('bv-sidebar-toggle')?.addEventListener('click', () => {
            this._toggleSidebar();
        });
        // Properties panel kapat
        document.getElementById('bv-props-close')?.addEventListener('click', () => {
            this._closeProperties();
        });
        // Grid toggle
        document.getElementById('bv-item-grid')?.addEventListener('click', () => {
            this._toggleGrid();
        });
        // Modeli kaldır
        document.getElementById('bv-item-unload')?.addEventListener('click', () => {
            void this._unloadAllModels();
        });
        // ── Kesit Düzlemi butonları ────────────────────────────────────────
        document.querySelectorAll('.bv-item--clip').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const axis = e.currentTarget.dataset['clipAxis'];
                if (axis && this._clippingMgr) {
                    this._clippingMgr.addClippingPlane(axis, 0);
                    this._showToast({
                        type: 'info',
                        title: `✂️ ${axis.toUpperCase()} Ekseni Kesit`,
                        message: 'Düzlemi sürükleyerek taşıyın.',
                        duration: 3000,
                    });
                }
            });
        });
        // Tüm kesit düzlemlerini kaldır
        document.getElementById('bv-item-clip-all-remove')?.addEventListener('click', () => {
            if (this._clippingMgr) {
                this._clippingMgr.removeAllClippingPlanes();
                this._floorSectionPlaneId = null;
                this._showToast({
                    type: 'info',
                    title: '✂️ Kesitler Kaldırıldı',
                    message: 'Tüm kesit düzlemleri kaldırıldı.',
                    duration: 2500,
                });
            }
        });
        // Fullscreen toggle
        document.getElementById('bv-btn-fullscreen')?.addEventListener('click', () => {
            void this._toggleFullscreen();
        });
        // Tam ekran geçişi tamamlandığında renderer/kamera/fragments güncelle.
        // Hem toolbar butonu hem F11 hem de browser fullscreen kontrolleri için.
        // Çift tetikleme: layout reflow'nun tamamlandığından emin olmak için.
        document.addEventListener('fullscreenchange', () => {
            this._forceRendererResize(); // hemen (layout zaten hazır)
            setTimeout(() => this._forceRendererResize(), 100); // güvenli yedek
        });
        // İptal butonu (loading overlay)
        document.getElementById('bv-btn-cancel-load')?.addEventListener('click', () => {
            this._hideLoading();
            this._showToast({ type: 'warning', title: 'İptal Edildi', message: 'Yükleme işlemi iptal edildi.' });
        });
        // Kamera preset'leri
        document.querySelectorAll('.bv-item--camera').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const preset = e.currentTarget.dataset['preset'];
                if (preset)
                    this._setCameraPreset(preset);
            });
        });
        // ── Kesit Düzlemi Panel Toggle ──────────────────────────────────────
        document.getElementById('bv-clipping-panel-toggle')?.addEventListener('click', () => {
            const panel = document.getElementById('bv-clipping-panel');
            const toggleBtn = document.getElementById('bv-clipping-panel-toggle');
            if (!panel)
                return;
            const isOpen = !panel.hidden;
            panel.hidden = isOpen;
            toggleBtn?.setAttribute('aria-expanded', String(!isOpen));
            toggleBtn?.classList.toggle('open', !isOpen);
        });
        // ── IFC Rehberi butonu ─────────────────────────────────────────────
        const toolbarEl = document.getElementById('bv-toolbar');
        if (toolbarEl) {
            initIfcExportGuide(toolbarEl);
        }
    }
    /** Dropdown menü davranışlarını bağlar */
    _bindDropdowns() {
        // Her dropdown trigger'ına tıklama
        document.querySelectorAll('.bv-dropdown').forEach((dropdown) => {
            const trigger = dropdown.querySelector('.bv-dropdown-trigger');
            trigger?.addEventListener('click', (e) => {
                e.stopPropagation();
                const isOpen = dropdown.classList.contains('open');
                // Diğer tüm dropdown'ları kapat
                document.querySelectorAll('.bv-dropdown.open').forEach((d) => {
                    d.classList.remove('open');
                    d.querySelector('.bv-dropdown-trigger')?.setAttribute('aria-expanded', 'false');
                });
                if (!isOpen) {
                    dropdown.classList.add('open');
                    trigger.setAttribute('aria-expanded', 'true');
                }
            });
        });
        // Dışarı tıklanınca tüm dropdown'ları kapat
        document.addEventListener('click', () => {
            document.querySelectorAll('.bv-dropdown.open').forEach((d) => {
                d.classList.remove('open');
                d.querySelector('.bv-dropdown-trigger')?.setAttribute('aria-expanded', 'false');
            });
        });
    }
    /** Drag & Drop event'lerini bağlar */
    _bindDragDrop() {
        const viewport = this._viewport;
        // dragenter: overlay'i göster
        viewport.addEventListener('dragenter', (e) => {
            e.preventDefault();
            this._dragDepth++;
            if (this._dragDepth === 1) {
                this._dragOverlay.classList.add('active');
                this._dragOverlay.setAttribute('aria-hidden', 'false');
            }
        });
        // dragleave: sadece viewport'tan çıkıldığında overlay'i gizle
        viewport.addEventListener('dragleave', (e) => {
            e.preventDefault();
            this._dragDepth--;
            if (this._dragDepth <= 0) {
                this._dragDepth = 0;
                this._dragOverlay.classList.remove('active');
                this._dragOverlay.setAttribute('aria-hidden', 'true');
            }
        });
        // dragover: default browser davranışını engelle (drop izni ver)
        viewport.addEventListener('dragover', (e) => {
            e.preventDefault();
            if (e.dataTransfer)
                e.dataTransfer.dropEffect = 'copy';
        });
        // drop: dosyayı al ve yükle
        viewport.addEventListener('drop', (e) => {
            e.preventDefault();
            this._dragDepth = 0;
            this._dragOverlay.classList.remove('active');
            this._dragOverlay.setAttribute('aria-hidden', 'true');
            const files = Array.from(e.dataTransfer?.files ?? []);
            const ifcFiles = files.filter((f) => /\.(ifc)$/i.test(f.name));
            if (ifcFiles.length === 0) {
                this._showToast({
                    type: 'warning',
                    title: 'Geçersiz Dosya',
                    message: 'Lütfen .ifc uzantılı bir dosya sürükleyin.',
                });
                return;
            }
            if (files.length > 1) {
                this._showToast({
                    type: 'warning',
                    title: 'Birden Fazla Dosya',
                    message: 'Aynı anda tek dosya yüklenebilir. İlk dosya yükleniyor.',
                });
            }
            void this._handleFile(ifcFiles[0]);
        });
    }
    /** Klavye kısayollarını bağlar */
    _bindKeyboard() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+O → Dosya aç
            if (e.ctrlKey && e.key === 'o') {
                e.preventDefault();
                this._fileInput.click();
            }
            // Escape → Dropdown'ları / Properties'i kapat + Ölçüm modundan çık
            if (e.key === 'Escape') {
                if (this._measurementTool?.isActive) {
                    this._measurementTool.deactivate();
                    this._measurementTool.clearAllDimensions();
                    if (this._elementPicker)
                        this._elementPicker.paused = false;
                    this._setMeasureButtonState(false);
                }
                document.querySelectorAll('.bv-dropdown.open').forEach((d) => {
                    d.classList.remove('open');
                    d.querySelector('.bv-dropdown-trigger')?.setAttribute('aria-expanded', 'false');
                });
                if (this._propPanelOpen)
                    this._closeProperties();
            }
            // [ → Sidebar toggle
            if (e.key === '[' && !e.ctrlKey && !e.altKey) {
                this._toggleSidebar();
            }
            // M → Ölçüm modu toggle
            if ((e.key === 'm' || e.key === 'M') && !e.ctrlKey && !e.altKey) {
                const active = e.target instanceof HTMLInputElement
                    || e.target instanceof HTMLTextAreaElement;
                if (!active)
                    this._toggleMeasurementMode();
            }
        });
    }
    // ─── Dosya Yükleme ────────────────────────────────────────────────────────
    async _handleFile(file) {
        if (!this._engine) {
            this._showToast({
                type: 'error',
                title: 'Engine Hazır Değil',
                message: 'IFC motoru henüz başlatılmamış. Lütfen bekleyin.',
            });
            return;
        }
        if (this._engine.isLoading) {
            this._showToast({
                type: 'warning',
                title: 'Yükleme Devam Ediyor',
                message: 'Lütfen mevcut yüklemenin bitmesini bekleyin.',
            });
            return;
        }
        // Mevcut model varsa önce kaldır
        if (this._engine.loadedModels.size > 0) {
            await this._unloadAllModels();
        }
        this._showLoading(file.name);
        this._currentFile = file.name;
        try {
            await this._engine.loadIFC(file);
        }
        catch {
            // Hata engine.onError callback'i üzerinden iletildi
        }
    }
    // ─── Model Yüklendi ───────────────────────────────────────────────────────
    async _onModelLoaded(modelId, model) {
        this._hideLoading();
        // Boş durumu gizle
        this._viewportEmpty.style.display = 'none';
        // Statusbar güncelle
        this._updateStatusModel(this._currentFile ?? modelId);
        // Modeli kaldır butonu etkinleştir
        const unloadBtn = document.getElementById('bv-item-unload');
        if (unloadBtn)
            unloadBtn.disabled = false;
        // ── StoreyManager: Katları çıkar ve sidebar'ı doldur ─────────────────
        try {
            // StoreyManager'ı başlat (fragments referansı gerekiyor)
            if (this._engine?.fragments) {
                this._storeyManager = new StoreyManager(this._engine.fragments);
                // Görünürlük değişikliği callback'ini bağla
                this._storeyManager.onStoreyVisibilityChange = () => {
                    this._updateStoreyListUI();
                };
                // Katları spatial structure'dan çıkar
                await this._storeyManager.extractStoreys(modelId);
                // Sidebar'ı kat bilgileriyle doldur
                this._buildStoreyUI(modelId);
                // Context menüyü oluştur (DOM'a ekle)
                this._createContextMenu();
                // ── ProgressColoring başlat ─────────────────────────────────────
                this._progressColoring = new ProgressColoring(this._engine.fragments, this._viewport);
                this._progressColoring.setModel(model);
                this._progressColoring.initLegend();
                // Mod değiştiğinde toolbar badge'ı güncelle
                this._progressColoring.onColorModeChange = (mode) => {
                    this._updateColorModeUI(mode);
                };
                // Renk dropdown butonlarını aktif et
                const applyMockBtn = document.getElementById('bv-item-apply-mock');
                const clearColorsBtn = document.getElementById('bv-item-clear-colors');
                if (applyMockBtn)
                    applyMockBtn.disabled = false;
                if (clearColorsBtn)
                    clearColorsBtn.disabled = false;
            }
            else {
                // Fragments henüz hazır değil — eski ağaç yöntemiyle devam et
                const tree = await model.getSpatialStructure();
                this._buildModelTree(modelId, tree, model);
            }
            // Element sayısını bul
            const itemsIds = await model.getItemsIdsWithGeometry();
            this._statusElements.textContent = itemsIds.length.toLocaleString('tr-TR');
        }
        catch (err) {
            console.warn('[BIMViewer] Model ağacı oluşturulamadı:', err);
            // Fallback: Eski yöntem
            try {
                const tree = await model.getSpatialStructure();
                this._buildModelTree(modelId, tree, model);
            }
            catch { /* sessiz */ }
        }
        // Durum noktasını güncelle
        this._statusDot.classList.add('bv-status-dot--ok');
        // MeasurementTool hedef nesnelerini güncelle
        if (this._measurementTool && this._ctx) {
            const sceneObjects = [];
            this._ctx.scene.traverse((obj) => {
                if (obj instanceof THREE.Mesh && !obj.userData['isHelper']) {
                    sceneObjects.push(obj);
                }
            });
            this._measurementTool.setTargetObjects(sceneObjects);
        }
        this._showToast({
            type: 'success',
            title: 'Model Yüklendi',
            message: `${this._currentFile} başarıyla yüklendi.`,
        });
        // ── MappingPanel & ilerleme renklendirmesi (compact mod + santiye bilgisi) ─
        if (this._compact && this._compactModelId !== null && this._compactSantiyeId !== null) {
            this._initMappingPanel(this._compactModelId, this._compactSantiyeId);
            this._startRealProgressColoring(this._compactModelId);
        }
    }
    /** MappingPanel'i başlatır ve toolbar'a buton ekler. */
    _initMappingPanel(modelId, santiyeId) {
        // Önceki paneli temizle
        this._mappingPanel?.destroy();
        const toolbar = document.getElementById('bv-toolbar');
        if (!toolbar)
            return;
        this._mappingPanel = new MappingPanel({
            container: document.getElementById('bv-app'),
            modelId,
            santiyeId,
            callbacks: {
                onMappingSaved: (_gid, _kid) => {
                    // Kayıt sonrası ilerleme renklerini yenile
                    if (this._compactModelId !== null) {
                        void this._refreshProgressColors(this._compactModelId);
                    }
                },
                onBulkMappingSaved: () => {
                    if (this._compactModelId !== null) {
                        void this._refreshProgressColors(this._compactModelId);
                    }
                },
                getElementsByType: async (ifcType) => {
                    if (!this._elementPicker)
                        return [];
                    const infos = await this._elementPicker.getElementInfosByType(ifcType);
                    return infos.map((info) => ({
                        globalId: info.globalId,
                        ifcType: info.ifcType,
                        name: info.name,
                        storey: info.storey ?? '—',
                    }));
                },
            },
        });
        addMappingToolbarButton(toolbar, this._mappingPanel);
    }
    /** Backend'den gerçek ilerleme verisini çekip modele uygular. */
    async _refreshProgressColors(modelId) {
        if (!this._progressColoring)
            return;
        try {
            const api = getBIMApiClient();
            const data = await api.getProgressData(modelId);
            if (data.elementMapping.length > 0) {
                await this._progressColoring.applyProgressColors(data);
                this._updateColorModeUI('progress');
            }
        }
        catch (err) {
            console.warn('[BIMViewer] İlerleme renklendirmesi yüklenemedi:', err);
        }
    }
    /** İlerleme polling'ini başlatır ve model kaldırılınca durdurur. */
    _startRealProgressColoring(modelId) {
        this._stopProgressPolling?.();
        // İlk yükleme
        void this._refreshProgressColors(modelId);
        // 60 saniyede bir otomatik güncelle
        const api = getBIMApiClient();
        this._stopProgressPolling = api.startProgressPolling(modelId, 60000, async (data) => {
            if (this._progressColoring && data.elementMapping.length > 0) {
                await this._progressColoring.applyProgressColors(data);
            }
        });
    }
    async _unloadAllModels() {
        if (!this._engine)
            return;
        await this._engine.unloadAll();
        // Progress polling durdur
        this._stopProgressPolling?.();
        this._stopProgressPolling = null;
        // MappingPanel'i kaldır
        this._mappingPanel?.destroy();
        this._mappingPanel = null;
        // StoreyManager'ı sıfırla
        this._storeyManager?.reset();
        this._storeyManager = null;
        // ProgressColoring'ı temizle
        this._progressColoring?.dispose();
        this._progressColoring = null;
        // Kesit düzlemlerini kaldır
        this._clippingMgr?.removeAllClippingPlanes();
        this._floorSectionPlaneId = null;
        // Ölçümleri temizle
        this._measurementTool?.clearAllDimensions();
        this._measurementTool?.deactivate();
        if (this._elementPicker)
            this._elementPicker.paused = false;
        this._setMeasureButtonState(false);
        this._measurementTool?.setTargetObjects([]);
        // Renk dropdown butonlarını devre dışı bırak
        const applyMockBtn = document.getElementById('bv-item-apply-mock');
        const clearColorsBtn = document.getElementById('bv-item-clear-colors');
        if (applyMockBtn)
            applyMockBtn.disabled = true;
        if (clearColorsBtn)
            clearColorsBtn.disabled = true;
        this._updateColorModeUI('original');
        // Context menüyü kaldır
        this._contextMenuEl?.remove();
        this._contextMenuEl = null;
        // UI'ı sıfırla
        this._currentFile = null;
        this._statusModel.textContent = 'Yüklenmedi';
        this._statusElements.textContent = '—';
        this._statusDot.classList.remove('bv-status-dot--ok');
        this._viewportEmpty.style.display = '';
        this._buildTreeEmpty();
        // Modeli kaldır butonunu devre dışı bırak
        const unloadBtn = document.getElementById('bv-item-unload');
        if (unloadBtn)
            unloadBtn.disabled = true;
        if (this._propPanelOpen)
            this._closeProperties();
    }
    // ─── Statusbar Güncelleme ─────────────────────────────────────────────────
    _updateStatusModel(fileName) {
        // Uzun isimleri kısalt
        const maxLen = 30;
        const displayName = fileName.length > maxLen
            ? fileName.substring(0, maxLen - 3) + '…'
            : fileName;
        this._statusModel.textContent = displayName;
    }
    // ─── Loading Overlay ──────────────────────────────────────────────────────
    _showLoading(fileName) {
        this._loadingFile.textContent = fileName;
        this._loadingMsg.textContent = 'Hazırlanıyor...';
        this._progressFill.style.width = '0%';
        this._progressPct.textContent = '0%';
        this._loadingOverlay.classList.remove('hidden');
        this._loadingOverlay.setAttribute('aria-hidden', 'false');
    }
    _hideLoading() {
        this._loadingOverlay.classList.add('hidden');
        this._loadingOverlay.setAttribute('aria-hidden', 'true');
    }
    _updateProgress(progress, message) {
        const pct = Math.round(Math.min(progress, 1) * 100);
        this._progressFill.style.width = `${pct}%`;
        this._progressPct.textContent = `${pct}%`;
        this._loadingMsg.textContent = message;
    }
    // ─── Model Ağacı ──────────────────────────────────────────────────────────
    _buildTreeEmpty() {
        this._treeContent.innerHTML = `
      <div class="bv-tree-empty" id="bv-tree-empty">
        <div class="bv-tree-empty-icon">🏗</div>
        <div class="bv-tree-empty-title">IFC dosyası yükleyin</div>
        <div class="bv-tree-empty-sub">Model yüklendikten sonra<br>kat listesi burada görünür</div>
      </div>`;
    }
    // ─── StoreyManager UI ─────────────────────────────────────────────────────
    /**
     * StoreyManager'dan gelen kat bilgileriyle sidebar UI'ını oluşturur.
     * Model yüklendikten sonra _onModelLoaded tarafından çağrılır.
     */
    _buildStoreyUI(modelId) {
        const storeys = this._storeyManager?.storeys ?? [];
        if (storeys.length === 0) {
            this._treeContent.innerHTML = `
        <div class="bv-model-section">
          <div class="bv-model-header">
            <span class="bv-model-icon">🏗</span>
            <span class="bv-model-name">${this._escapeHtml(modelId)}</span>
          </div>
          <div style="padding:16px 12px;font-size:11.5px;color:var(--bv-text-3);">
            Kat bilgisi bulunamadı.
          </div>
        </div>`;
            return;
        }
        // Tüm katlar görünür — bulk action toolbar
        const storeyItemsHtml = storeys.map((s, idx) => this._renderStoreyRow(s, idx)).join('');
        this._treeContent.innerHTML = `
      <div class="bv-model-section">
        <div class="bv-model-header">
          <span class="bv-model-icon">🏗</span>
          <span class="bv-model-name" title="${this._escapeHtml(modelId)}">${this._escapeHtml(modelId)}</span>
          <span class="bv-storey-count">${storeys.length} kat</span>
        </div>
        <div class="bv-bulk-actions">
          <button class="bv-bulk-btn" id="bv-bulk-show-all" title="Tüm katları göster">👁 Tümünü Göster</button>
          <button class="bv-bulk-btn" id="bv-bulk-hide-all" title="Tüm katları gizle">🙈 Tümünü Gizle</button>
        </div>
        <div class="bv-storey-list" id="bv-storey-list">
          ${storeyItemsHtml}
        </div>
      </div>`;
        // Event'leri bağla
        this._bindStoreyUIEvents();
    }
    /**
     * Tek bir kat satırının HTML'ini üretir.
     */
    _renderStoreyRow(s, _idx) {
        const visIcon = s.isVisible ? '👁' : '🚫';
        const hiddenClass = s.isVisible ? '' : 'bv-storey-hidden';
        const elevSign = s.elevation >= 0 ? '+' : '';
        const elevStr = `${elevSign}${s.elevation.toFixed(2)} m`;
        // Eleman tipi özeti (en çok bulunan 3 tip)
        const typeEntries = Object.entries(s.elementTypes)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3);
        const typeSummary = typeEntries
            .map(([type, count]) => `${type}: ${count}`)
            .join(', ');
        return `
      <div class="bv-storey-item ${hiddenClass}"
           data-storey-id="${this._escapeHtml(s.id)}"
           title="Kameraya odaklan: ${this._escapeHtml(s.name)}">

        <!-- Görünürlük butonu -->
        <button class="bv-storey-vis-btn"
                data-storey-id="${this._escapeHtml(s.id)}"
                title="${s.isVisible ? 'Gizle' : 'Göster'}"
                aria-label="${s.isVisible ? 'Gizle' : 'Göster'} (${this._escapeHtml(s.name)})"
                aria-pressed="${String(s.isVisible)}">
          ${visIcon}
        </button>

        <!-- Kat etiketi (kamera zoom) -->
        <div class="bv-storey-label" tabindex="0" role="treeitem"
             data-storey-id="${this._escapeHtml(s.id)}"
             aria-label="${this._escapeHtml(s.name)}, ${s.elementCount} eleman, kot: ${elevStr}">
          <span class="bv-storey-icon">${s.name.includes('(tahmini)') ? '❓' : '🏢'}</span>
          <div class="bv-storey-info">
            <span class="bv-storey-name" title="${this._escapeHtml(s.name)}">${this._escapeHtml(s.name)}</span>
            <span class="bv-storey-meta">${s.elementCount} eleman</span>
          </div>
          <span class="bv-storey-elevation" title="Kot değeri">↑ ${elevStr}</span>
        </div>

        <!-- Expand butonu -->
        <button class="bv-storey-expand-btn"
                data-storey-id="${this._escapeHtml(s.id)}"
                aria-label="Eleman listesini genişlet"
                aria-expanded="false"
                title="Eleman tiplerini göster">▶</button>

        <!-- Kat Kesiti butonu -->
        <button class="bv-storey-clip-btn"
                data-storey-id="${this._escapeHtml(s.id)}"
                data-storey-elevation="${s.elevation}"
                title="Bu katta Y ekseni kesit düzlemi uygula"
                aria-label="Kat kesiti: ${this._escapeHtml(s.name)}">✂</button>

        <!-- Expand içeriği (başlangıçta gizli) -->
        <div class="bv-storey-children" id="bv-storey-children-${this._escapeHtml(s.id)}" hidden>
          ${typeSummary
            ? typeEntries.map(([type, count]) => `<div class="bv-type-row">
                   <span class="bv-type-name">${this._escapeHtml(type)}</span>
                   <span class="bv-type-count">${count}</span>
                 </div>`).join('')
            : '<div class="bv-type-empty">Element bulunamadı</div>'}
        </div>
      </div>`;
    }
    /**
     * Storey UI'ına event listener'ları bağlar.
     */
    _bindStoreyUIEvents() {
        // Bulk actions
        document.getElementById('bv-bulk-show-all')?.addEventListener('click', () => {
            void this._storeyManager?.showAllStoreys();
        });
        document.getElementById('bv-bulk-hide-all')?.addEventListener('click', () => {
            void this._storeyAllHide();
        });
        // Her kat satırı için event'ler
        const storeyList = document.getElementById('bv-storey-list');
        if (!storeyList)
            return;
        // Görünürlük butonu
        storeyList.querySelectorAll('.bv-storey-vis-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const storeyId = e.currentTarget.dataset['storeyId'];
                if (!storeyId || !this._storeyManager)
                    return;
                const storey = this._storeyManager.storeys.find(s => s.id === storeyId);
                if (storey) {
                    void this._storeyManager.setStoreyVisibility(storeyId, !storey.isVisible);
                }
            });
        });
        // Kat etiketi — kamera zoom
        storeyList.querySelectorAll('.bv-storey-label').forEach((label) => {
            // Tıklama: kamera odakla
            label.addEventListener('click', (e) => {
                e.stopPropagation();
                const storeyId = e.currentTarget.dataset['storeyId'];
                if (storeyId)
                    this._zoomToStorey(storeyId);
            });
            // Klavye erişimi
            label.addEventListener('keydown', (e) => {
                const ke = e;
                if (ke.key === 'Enter' || ke.key === ' ') {
                    ke.preventDefault();
                    const storeyId = e.currentTarget.dataset['storeyId'];
                    if (storeyId)
                        this._zoomToStorey(storeyId);
                }
            });
        });
        // Expand butonu — eleman tiplerini aç/kapat
        storeyList.querySelectorAll('.bv-storey-expand-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const storeyId = e.currentTarget.dataset['storeyId'];
                if (!storeyId)
                    return;
                const childrenEl = document.getElementById(`bv-storey-children-${storeyId}`);
                if (!childrenEl)
                    return;
                const isExpanded = !childrenEl.hidden;
                childrenEl.hidden = isExpanded;
                btn.setAttribute('aria-expanded', String(!isExpanded));
                btn.classList.toggle('expanded', !isExpanded);
            });
        });
        // Kat Kesiti butonu — Y ekseninde düzlem uygula
        storeyList.querySelectorAll('.bv-storey-clip-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const el = e.currentTarget;
                const elevation = parseFloat(el.dataset['storeyElevation'] ?? '0');
                this._applyFloorSection(elevation);
            });
        });
        // Sağ tık: Context menü
        storeyList.querySelectorAll('.bv-storey-item').forEach((item) => {
            item.addEventListener('contextmenu', (e) => {
                e.preventDefault();
                const me = e;
                const storeyId = e.currentTarget.dataset['storeyId'];
                if (storeyId)
                    this._showContextMenu(me.clientX, me.clientY, storeyId);
            });
        });
        // Dışarıya tıklanınca context menüyü kapat
        document.addEventListener('click', () => this._hideContextMenu(), { capture: true });
    }
    /**
     * Tüm katları gizler.
     */
    async _storeyAllHide() {
        if (!this._storeyManager)
            return;
        for (const s of this._storeyManager.storeys) {
            await this._storeyManager.setStoreyVisibility(s.id, false);
        }
    }
    /**
     * Storey listesinin UI'ını günceller (görünürlük değişikliğinde).
     * Tüm DOM'u yeniden oluşturmak yerine sadece değişen satırları günceller.
     */
    _updateStoreyListUI() {
        if (!this._storeyManager)
            return;
        const storeys = this._storeyManager.storeys;
        storeys.forEach((s) => {
            const item = this._treeContent.querySelector(`.bv-storey-item[data-storey-id="${s.id}"]`);
            if (!item)
                return;
            // Gizli sınıfını güncelle
            item.classList.toggle('bv-storey-hidden', !s.isVisible);
            // Görünürlük butonunu güncelle
            const visBtn = item.querySelector('.bv-storey-vis-btn');
            if (visBtn) {
                visBtn.textContent = s.isVisible ? '👁' : '🚫';
                visBtn.title = s.isVisible ? 'Gizle' : 'Göster';
                visBtn.setAttribute('aria-pressed', String(s.isVisible));
            }
        });
    }
    /**
     * Kamerayı seçilen katin elevation'ına zoom eder.
     * Elevation değerini kullanarak orbit kontrolünü günceller.
     */
    _zoomToStorey(storeyId) {
        if (!this._ctx || !this._storeyManager)
            return;
        const storey = this._storeyManager.storeys.find(s => s.id === storeyId);
        if (!storey)
            return;
        const { camera, controls } = this._ctx;
        // Mevcut model bounding box merkezini al
        const currentTarget = controls.target.clone();
        // Hedef Y koordinatı = elevation + 1.5m (kat göz hizası)
        const targetY = storey.elevation + 1.5;
        const newTarget = new THREE.Vector3(currentTarget.x, targetY, currentTarget.z);
        // Kamerayı kat seviyesinde tutarak açısal bir konuma getir
        const camDist = camera.position.distanceTo(controls.target);
        const dist = Math.max(camDist, 15);
        camera.position.set(newTarget.x + dist * 0.6, newTarget.y + dist * 0.3, newTarget.z + dist * 0.6);
        controls.target.copy(newTarget);
        controls.update();
        this._showToast({
            type: 'info',
            title: `📍 ${storey.name}`,
            message: `Kot: ${storey.elevation >= 0 ? '+' : ''}${storey.elevation.toFixed(2)} m`,
            duration: 2500,
        });
    }
    /**
     * Context menü oluşturur ve DOM'a ekler.
     */
    _createContextMenu() {
        // Varsa önceki menüyü kaldır
        this._contextMenuEl?.remove();
        const menu = document.createElement('div');
        menu.className = 'bv-context-menu';
        menu.id = 'bv-storey-context-menu';
        menu.setAttribute('role', 'menu');
        menu.setAttribute('aria-label', 'Kat seçenekleri');
        menu.hidden = true;
        menu.innerHTML = `
      <button class="bv-ctx-item" id="bv-ctx-isolate" role="menuitem">
        <span class="bv-ctx-icon">🎯</span> Sadece bu katı göster
      </button>
      <button class="bv-ctx-item" id="bv-ctx-hide" role="menuitem">
        <span class="bv-ctx-icon">🚫</span> Bu katı gizle
      </button>
      <div class="bv-ctx-divider"></div>
      <button class="bv-ctx-item" id="bv-ctx-show-all" role="menuitem">
        <span class="bv-ctx-icon">👁</span> Tümünü göster
      </button>
      <button class="bv-ctx-item" id="bv-ctx-zoom" role="menuitem">
        <span class="bv-ctx-icon">📍</span> Bu kata odaklan
      </button>`;
        document.body.appendChild(menu);
        this._contextMenuEl = menu;
        // Context menü buton event'leri
        document.getElementById('bv-ctx-isolate')?.addEventListener('click', () => {
            if (this._contextMenuStoreyId) {
                void this._storeyManager?.isolateStorey(this._contextMenuStoreyId);
            }
            this._hideContextMenu();
        });
        document.getElementById('bv-ctx-hide')?.addEventListener('click', () => {
            if (this._contextMenuStoreyId) {
                void this._storeyManager?.setStoreyVisibility(this._contextMenuStoreyId, false);
            }
            this._hideContextMenu();
        });
        document.getElementById('bv-ctx-show-all')?.addEventListener('click', () => {
            void this._storeyManager?.showAllStoreys();
            this._hideContextMenu();
        });
        document.getElementById('bv-ctx-zoom')?.addEventListener('click', () => {
            if (this._contextMenuStoreyId) {
                this._zoomToStorey(this._contextMenuStoreyId);
            }
            this._hideContextMenu();
        });
    }
    /** Context menüyü belirli koordinatlarda gösterir. */
    _showContextMenu(x, y, storeyId) {
        if (!this._contextMenuEl)
            return;
        this._contextMenuStoreyId = storeyId;
        // Ekran sınırlarını aş maması için pozisyon düzelt
        const menuW = 200;
        const menuH = 140;
        const safeX = Math.min(x, window.innerWidth - menuW - 8);
        const safeY = Math.min(y, window.innerHeight - menuH - 8);
        this._contextMenuEl.style.left = `${safeX}px`;
        this._contextMenuEl.style.top = `${safeY}px`;
        this._contextMenuEl.hidden = false;
    }
    /** Context menüyü gizler. */
    _hideContextMenu() {
        if (this._contextMenuEl)
            this._contextMenuEl.hidden = true;
        this._contextMenuStoreyId = null;
    }
    // ─── Eski Yedek Metodlar (StoreyManager kullanılamadığında) ───────────────
    _buildModelTree(modelId, tree, model) {
        const storeys = this._collectStoreys(tree);
        if (storeys.length === 0) {
            this._treeContent.innerHTML = `
        <div class="bv-model-section">
          <div class="bv-model-header">
            <span class="bv-model-icon">🏗</span>
            <span class="bv-model-name">${this._escapeHtml(modelId)}</span>
          </div>
          <div style="padding:12px;font-size:11.5px;color:var(--bv-text-3);">
            Kat bilgisi bulunamadı.
          </div>
        </div>`;
            return;
        }
        const storeyItemsHtml = storeys.map((s) => {
            const name = s.category ?? `Kat ${s.localId ?? '?'}`;
            const localId = s.localId ?? -1;
            return `
        <div class="bv-storey-item" data-local-id="${localId}">
          <button class="bv-storey-expand" aria-label="Genişlet" aria-expanded="false">▶</button>
          <div class="bv-storey-label" tabindex="0" role="treeitem">
            <span class="bv-storey-icon">🏢</span>
            <span class="bv-storey-name" title="${this._escapeHtml(name)}">${this._escapeHtml(name)}</span>
          </div>
          <div class="bv-storey-actions">
            <button class="bv-storey-action-btn bv-visibility-btn"
                    data-local-id="${localId}"
                    title="Katı göster/gizle" aria-label="Görünürlük">👁</button>
          </div>
        </div>`;
        }).join('');
        this._treeContent.innerHTML = `
      <div class="bv-model-section">
        <div class="bv-model-header">
          <span class="bv-model-icon">🏗</span>
          <span class="bv-model-name" title="${this._escapeHtml(modelId)}">${this._escapeHtml(modelId)}</span>
        </div>
        ${storeyItemsHtml}
      </div>`;
        // Visibility toggle'ları bağla
        this._treeContent.querySelectorAll('.bv-visibility-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const localId = parseInt(e.currentTarget.dataset['localId'] ?? '-1');
                void this._toggleStoreyVisibility(localId, model, btn);
            });
        });
        // Expand butonlarını bağla
        this._treeContent.querySelectorAll('.bv-storey-expand').forEach((btn) => {
            btn.addEventListener('click', () => {
                btn.classList.toggle('expanded');
                const expanded = btn.classList.contains('expanded');
                btn.setAttribute('aria-expanded', String(expanded));
            });
        });
    }
    /** Spatial tree'den IfcBuildingStorey düğümlerini toplar (BFS) */
    _collectStoreys(root) {
        const storeys = [];
        const queue = [root];
        while (queue.length > 0) {
            const node = queue.shift();
            if (node.category?.toUpperCase().includes('STOREY') ||
                node.category?.toUpperCase().includes('KAT')) {
                storeys.push(node);
            }
            if (node.children)
                queue.push(...node.children);
        }
        return storeys;
    }
    async _toggleStoreyVisibility(localId, model, btn) {
        if (localId === -1)
            return;
        const currentlyVisible = this._storeyVisibility.get(localId) ?? true;
        const newVisible = !currentlyVisible;
        this._storeyVisibility.set(localId, newVisible);
        try {
            await model.setVisible([localId], newVisible);
            await this._engine.fragments.update(true);
            btn.textContent = newVisible ? '👁' : '🙈';
            btn.closest('.bv-storey-item')?.classList.toggle('bv-storey-hidden', !newVisible);
        }
        catch (err) {
            console.warn('[BIMViewer] Görünürlük değiştirilemedi:', err);
        }
    }
    // ─── Properties Panel ─────────────────────────────────────────────────────
    _openProperties(data) {
        this._propPanelOpen = true;
        this._propPanel.classList.remove('closed');
        this._propPanel.setAttribute('aria-hidden', 'false');
        // İçeriği oluştur
        const sections = this._buildPropertiesHTML(data);
        this._propContent.innerHTML = sections;
    }
    _closeProperties() {
        this._propPanelOpen = false;
        this._propPanel.classList.add('closed');
        this._propPanel.setAttribute('aria-hidden', 'true');
        this._propContent.innerHTML = '';
    }
    _buildPropertiesHTML(data) {
        const rows = Object.entries(data).map(([key, val]) => {
            const displayVal = val === null || val === undefined ? '—' : String(val);
            const isAccent = key === 'GlobalId' || key === 'type' || key === 'Name';
            return `
        <div class="bv-prop-row">
          <span class="bv-prop-key">${this._escapeHtml(key)}</span>
          <span class="bv-prop-val ${isAccent ? 'bv-prop-val--accent' : ''}">
            ${this._escapeHtml(displayVal)}
          </span>
        </div>`;
        }).join('');
        return `
      <div class="bv-prop-group">
        <div class="bv-prop-group-title">Eleman Bilgisi</div>
        ${rows}
      </div>`;
    }
    // ─── Sidebar Toggle ───────────────────────────────────────────────────────
    _toggleSidebar() {
        this._sidebarCollapsed = !this._sidebarCollapsed;
        this._sidebarEl.classList.toggle('collapsed', this._sidebarCollapsed);
        const toggleBtn = document.getElementById('bv-sidebar-toggle');
        if (toggleBtn) {
            toggleBtn.textContent = this._sidebarCollapsed ? '›' : '‹';
            toggleBtn.title = this._sidebarCollapsed ? 'Paneli genişlet' : 'Paneli daralt';
            toggleBtn.setAttribute('aria-label', this._sidebarCollapsed ? 'Sidebar aç' : 'Sidebar kapat');
        }
        // Three.js resize'ı ResizeObserver zaten yakalar — elle tetiklemeye gerek yok
    }
    // ─── Grid Toggle ─────────────────────────────────────────────────────────
    // ─── ProgressColoring Yardımcıları ───────────────────────────────────────
    /**
     * Toolbar renk modu dropdown'undaki aktif butonu işaretler.
     */
    _updateColorModeUI(mode) {
        const modeLabels = {
            progress: '📊 İlerleme',
            type: '🏗 IFC Tipi',
            storey: '🏢 Kat',
            original: '🎨 Orijinal',
        };
        // Tüm renk modu butonlarından active sınıfını kaldır
        document.querySelectorAll('.bv-item--color').forEach((btn) => {
            const btnMode = btn.dataset['colorMode'];
            btn.classList.toggle('bv-dropdown-item--active', btnMode === mode);
            // Badge'i güncelle
            const badge = btn.querySelector('.bv-item-badge');
            if (badge) {
                badge.textContent = btnMode === mode ? 'Aktif' : '';
            }
        });
        // Toolbar Renk butonu etiketini güncelle
        const colorBtn = document.getElementById('bv-btn-color');
        if (colorBtn) {
            colorBtn.innerHTML = `<span>🎨</span> ${modeLabels[mode]} <span class="bv-chevron">▾</span>`;
        }
    }
    /**
     * Mock ilerleme verisi üretir ve modele uygular.
     * Gerçek API entegrasyonu Aşama 4'te yapılacak.
     */
    async _applyMockProgressData() {
        if (!this._progressColoring)
            return;
        this._showToast({
            type: 'info',
            title: 'Mock Veri Uygulanıyor',
            message: 'Sahte ilerleme verisi hesaplanıyor...',
            duration: 2000,
        });
        try {
            const mockData = await this._progressColoring.getMockProgressData();
            await this._progressColoring.applyProgressColors(mockData);
            this._updateColorModeUI('progress');
            const summary = this._progressColoring.getProgressSummary();
            this._showToast({
                type: 'success',
                title: '📊 İlerleme Renklendirmesi',
                message: `${summary.eslesen} element eşlendi · %${summary.tamamlanmaYuzdesi} tamamlandı`,
                duration: 4000,
            });
        }
        catch (err) {
            this._showToast({
                type: 'error',
                title: 'Renklendirme Hatası',
                message: err instanceof Error ? err.message : 'Bilinmeyen hata',
            });
        }
    }
    // ─── Clipping Plane UI ───────────────────────────────────────────────────
    /**
     * Kesit düzlemi panelini günceller.
     * ClippingPlaneManager.onPlanesChanged callback'i tarafından çağrılır.
     * Viewport içindeki bv-clipping-panel elementini doldurur (eğer varsa).
     */
    _updateClippingPanelUI(planes) {
        const panel = document.getElementById('bv-clipping-panel');
        if (!panel)
            return;
        // Sayacı güncelle
        const countEl = document.getElementById('bv-clip-count');
        if (countEl)
            countEl.textContent = String(planes.length);
        // Panel varsa otomatik aç (ilk düzlem eklendiğinde)
        if (planes.length > 0 && panel.hidden) {
            panel.hidden = false;
            document.getElementById('bv-clipping-panel-toggle')?.setAttribute('aria-expanded', 'true');
            document.getElementById('bv-clipping-panel-toggle')?.classList.add('open');
        }
        if (planes.length === 0) {
            panel.innerHTML = `
        <div class="bv-clip-empty">
          <span class="bv-clip-empty-icon">✂️</span>
          <span>Aktif kesit düzlemi yok</span>
        </div>`;
            return;
        }
        const axisLabel = { x: 'X', y: 'Y', z: 'Z' };
        const axisIcon = { x: '↔️', y: '↕️', z: '🔄' };
        panel.innerHTML = planes.map((p) => {
            const posVal = p.position.toFixed(2);
            const posMin = -50;
            const posMax = 50;
            const flipLabel = p.flipped ? '↩' : '↪';
            const visIcon = p.helperVisible ? '👁' : '🙈';
            return `
        <div class="bv-clip-item" data-plane-id="${this._escapeHtml(p.id)}">
          <div class="bv-clip-row bv-clip-header-row">
            <span class="bv-clip-axis-badge bv-clip-axis-${p.axis}">
              ${axisIcon[p.axis]} ${axisLabel[p.axis]}
            </span>
            <span class="bv-clip-pos-label">${posVal} m</span>
            <div class="bv-clip-actions">
              <button class="bv-clip-btn bv-clip-vis-btn"
                      data-plane-id="${this._escapeHtml(p.id)}"
                      title="${p.helperVisible ? 'Yardımcıyı gizle' : 'Yardımcıyı göster'}"
                      aria-label="Görünürlük">${visIcon}</button>
              <button class="bv-clip-btn bv-clip-flip-btn"
                      data-plane-id="${this._escapeHtml(p.id)}"
                      title="Tersine çevir"
                      aria-label="Flip">${flipLabel}</button>
              <button class="bv-clip-btn bv-clip-del-btn"
                      data-plane-id="${this._escapeHtml(p.id)}"
                      title="Kaldır"
                      aria-label="Kaldır">✕</button>
            </div>
          </div>
          <div class="bv-clip-row">
            <input type="range"
                   class="bv-clip-slider"
                   data-plane-id="${this._escapeHtml(p.id)}"
                   min="${posMin}" max="${posMax}" step="0.1"
                   value="${posVal}"
                   aria-label="${axisLabel[p.axis]} ekseni pozisyon"
            />
          </div>
        </div>`;
        }).join('');
        // Event'leri bağla
        this._bindClippingPanelEvents(panel);
    }
    /**
     * Kesit düzlemi panelindeki buton ve slider event'lerini bağlar.
     */
    _bindClippingPanelEvents(panel) {
        const controls = this._ctx?.controls;
        // Slider — pozisyon değiştir
        // pointerdown: OrbitControls'ü devre dışı bırak (sürükleme çakışmasını önle)
        // pointerup (window): sürükleme bitince controls'ü yeniden etkinleştir
        panel.querySelectorAll('.bv-clip-slider').forEach((el) => {
            const slider = el;
            slider.addEventListener('pointerdown', () => {
                if (controls)
                    controls.enabled = false;
            });
            slider.addEventListener('input', (e) => {
                const input = e.currentTarget;
                const planeId = input.dataset['planeId'];
                if (!planeId || !this._clippingMgr)
                    return;
                const pos = parseFloat(input.value);
                this._clippingMgr.setPlanePosition(planeId, pos);
            });
        });
        // Global pointerup: slider dışına taşınsa bile controls geri açılsın
        // _sliderPointerUpBound, initialize() sırasında bir kez oluşturulur;
        // burada yalnızca kullanılır, yeni listener eklenmez.
        if (controls && !this._sliderPointerUpBound) {
            this._sliderPointerUpBound = () => { controls.enabled = true; };
            window.addEventListener('pointerup', this._sliderPointerUpBound);
        }
        // Görünürlük toggle
        panel.querySelectorAll('.bv-clip-vis-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const planeId = e.currentTarget.dataset['planeId'];
                if (planeId)
                    this._clippingMgr?.toggleHelperVisibility(planeId);
            });
        });
        // Flip butonu
        panel.querySelectorAll('.bv-clip-flip-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const planeId = e.currentTarget.dataset['planeId'];
                if (planeId)
                    this._clippingMgr?.flipPlane(planeId);
            });
        });
        // Sil butonu
        panel.querySelectorAll('.bv-clip-del-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const planeId = e.currentTarget.dataset['planeId'];
                if (!planeId || !this._clippingMgr)
                    return;
                if (planeId === this._floorSectionPlaneId) {
                    this._floorSectionPlaneId = null;
                }
                this._clippingMgr.removeClippingPlane(planeId);
            });
        });
    }
    // ─── Ölçüm Paneli UI ──────────────────────────────────────────────────────
    /**
     * Ölçüm panelini aktif AutoDimension listesiyle günceller.
     * onDimensionAdded ve onDimensionRemoved callback'leri tarafından çağrılır.
     */
    _updateMeasurementPanelUI() {
        const panel = document.getElementById('bv-measure-panel');
        const countEl = document.getElementById('bv-measure-count');
        if (!panel || !this._measurementTool)
            return;
        const dims = this._measurementTool.dimensions;
        if (countEl)
            countEl.textContent = String(dims.length);
        // Paneli otomatik aç (ilk boyut eklendiğinde)
        if (dims.length > 0 && panel.hidden) {
            panel.hidden = false;
            document.getElementById('bv-measure-panel-toggle')?.setAttribute('aria-expanded', 'true');
            document.getElementById('bv-measure-panel-toggle')?.classList.add('open');
        }
        if (dims.length === 0) {
            panel.innerHTML = `
        <div class="bv-clip-empty" id="bv-measure-empty">
          <span class="bv-clip-empty-icon">📐</span>
          <span>Henüz ölçüm yok</span>
        </div>`;
            return;
        }
        const itemsHtml = dims.map((d) => {
            const parts = [];
            if (d.sizeX >= 0.01)
                parts.push(`${d.sizeX.toFixed(2)}m`);
            if (d.sizeY >= 0.01)
                parts.push(`${d.sizeY.toFixed(2)}m`);
            if (d.sizeZ >= 0.01)
                parts.push(`${d.sizeZ.toFixed(2)}m`);
            const dimStr = parts.join(' × ') || `${d.sizeX.toFixed(2)}m`;
            return `
        <div class="bv-measure-item" data-measure-id="${this._escapeHtml(d.id)}">
          <span class="bv-measure-icon">📐</span>
          <span class="bv-measure-dist" title="${this._escapeHtml(d.elementName)}">${this._escapeHtml(d.elementName)}: ${dimStr}</span>
          <button class="bv-clip-btn bv-measure-del-btn"
                  data-measure-id="${this._escapeHtml(d.id)}"
                  title="Bu boyutu sil"
                  aria-label="Sil">✕</button>
        </div>`;
        }).join('');
        panel.innerHTML = `
      ${itemsHtml}
      <div class="bv-measure-footer">
        <button class="bv-measure-clear-all" id="bv-measure-clear-all">🗑 Tümünü Temizle</button>
      </div>`;
        panel.querySelectorAll('.bv-measure-del-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const dimId = e.currentTarget.dataset['measureId'];
                if (dimId)
                    this._measurementTool?.clearDimension(dimId);
            });
        });
        document.getElementById('bv-measure-clear-all')?.addEventListener('click', () => {
            this._measurementTool?.clearAllDimensions();
        });
    }
    /** Ölçüm modunu açar/kapatır. Toolbar butonu ve 'M' kısayolu tarafından çağrılır. */
    _toggleMeasurementMode() {
        if (!this._measurementTool)
            return;
        if (this._measurementTool.isActive) {
            this._measurementTool.deactivate();
            if (this._elementPicker)
                this._elementPicker.paused = false;
            void this._elementPicker?.clearSelection();
            this._setMeasureButtonState(false);
            this._showToast({
                type: 'info',
                title: 'Ölçüm Durduruldu',
                message: 'Ölçüm aracı kapatıldı.',
                duration: 2000,
            });
        }
        else {
            void this._elementPicker?.clearSelection();
            if (this._elementPicker)
                this._elementPicker.paused = true;
            this._measurementTool.activate();
            this._setMeasureButtonState(true);
            this._showToast({
                type: 'info',
                title: '📏 Ölçüm Modu',
                message: 'Elemente tıklayın → otomatik boyutlar. Shift+tık: iki element arası mesafe. ESC: çık.',
                duration: 5000,
            });
        }
    }
    /**
     * Araçlar menüsündeki Ölçüm butonunun görünümünü günceller.
     *
     * @param active - Araç aktif mi?
     */
    _setMeasureButtonState(active) {
        const btn = document.getElementById('bv-item-measure');
        const badge = document.getElementById('bv-measure-badge');
        if (btn) {
            btn.setAttribute('aria-checked', String(active));
            btn.classList.toggle('bv-dropdown-item--active', active);
        }
        if (badge)
            badge.textContent = active ? 'Aktif' : '';
    }
    /**
     * Kat kesiti modu: Seçilen katın elevation'ına göre Y ekseninde düzlem oluşturur
     * ya da mevcut düzlemi günceller.
     *
     * @param elevation - Kat kot değeri (metre)
     */
    _applyFloorSection(elevation) {
        if (!this._clippingMgr)
            return;
        // Y ekseninin üstünden hafif bir offset ekle (kat döşemesini göster)
        const cutHeight = elevation + 1.2;
        this._floorSectionPlaneId = this._clippingMgr.setFloorSection(cutHeight, this._floorSectionPlaneId ?? undefined);
        this._showToast({
            type: 'info',
            title: '✂️ Kat Kesiti',
            message: `Y = ${cutHeight.toFixed(2)} m'de kesit uygulandı.`,
            duration: 2500,
        });
    }
    // ─── Grid Toggle ─────────────────────────────────────────────────────────
    _toggleGrid() {
        if (!this._ctx)
            return;
        let gridVisible = true;
        this._ctx.scene.traverse((obj) => {
            if (obj instanceof THREE.GridHelper || obj instanceof THREE.AxesHelper) {
                obj.visible = !obj.visible;
                gridVisible = obj.visible;
            }
        });
        const badge = document.getElementById('bv-grid-badge');
        const item = document.getElementById('bv-item-grid');
        if (badge)
            badge.textContent = gridVisible ? 'Açık' : 'Kapalı';
        item?.setAttribute('aria-checked', String(gridVisible));
    }
    // ─── Kamera Preset'leri ───────────────────────────────────────────────────
    _setCameraPreset(preset) {
        if (!this._ctx)
            return;
        const { camera, controls } = this._ctx;
        // Mevcut modelin merkezini al (veya origin)
        const target = controls.target.clone();
        const dist = camera.position.distanceTo(target);
        const d = Math.max(dist, 20);
        const presets = {
            perspective: new THREE.Vector3(d * 0.7, d * 0.5, d * 0.7),
            top: new THREE.Vector3(0, d, 0.001), // 0.001: lookAt singularity önleme
            front: new THREE.Vector3(0, d * 0.2, d),
            right: new THREE.Vector3(d, d * 0.2, 0),
            isometric: new THREE.Vector3(d * 0.7, d * 0.7, d * 0.7),
        };
        const offset = presets[preset];
        camera.position.copy(target).add(offset);
        controls.update();
        // Aktif preset'i işaretle
        document.querySelectorAll('.bv-item--camera').forEach((btn) => {
            const btnPreset = btn.dataset['preset'];
            btn.classList.toggle('bv-dropdown-item--active', btnPreset === preset);
        });
    }
    // ─── Fullscreen ───────────────────────────────────────────────────────────
    async _toggleFullscreen() {
        // bv-app yerine bv-viewport'u tam ekran yapıyoruz.
        // bv-app + iframe kombinasyonunda flex layout boyutu geç raporluyordu;
        // viewport direkt ekranı doldurduğunda ResizeObserver doğru çalışır.
        const el = this._viewport ?? document.getElementById('bv-app') ?? document.documentElement;
        try {
            if (!document.fullscreenElement) {
                await el.requestFullscreen();
            }
            else {
                await document.exitFullscreen();
            }
        }
        catch {
            // Safari gibi tarayıcılarda fullscreen desteklenmeyebilir
        }
    }
    /**
     * Viewport'un güncel CSS boyutunu renderer, kamera ve fragments LOD'a uygular.
     * Tam ekran geçişinden sonra çağrılır.
     */
    _forceRendererResize() {
        if (!this._ctx || !this._viewport)
            return;
        const w = this._viewport.clientWidth;
        const h = this._viewport.clientHeight;
        if (w === 0 || h === 0)
            return;
        this._ctx.renderer.setSize(w, h);
        this._ctx.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this._ctx.camera.aspect = w / h;
        this._ctx.camera.updateProjectionMatrix();
        // Fragments LOD sistemini yeni viewport boyutuna göre güncelle —
        // bu olmadan fragment tile'ları yeni frustum'da görünmeyebilir
        void this._engine?.fragments?.update(true);
        // Hemen bir kare render et; animation loop bir sonraki frame'e kadar bekler
        this._ctx.renderer.render(this._ctx.scene, this._ctx.camera);
    }
    // ─── FPS Sayacı ───────────────────────────────────────────────────────────
    _startFPSCounter() {
        const loop = (now) => {
            if (this._isDisposed)
                return;
            this._fpsFrameCount++;
            const delta = now - this._fpsLastTime;
            if (delta >= 1000) {
                const fps = Math.round((this._fpsFrameCount * 1000) / delta);
                this._statusFps.textContent = String(fps);
                this._fpsFrameCount = 0;
                this._fpsLastTime = now;
            }
            this._fpsRafId = requestAnimationFrame(loop);
        };
        this._fpsRafId = requestAnimationFrame(loop);
    }
    // ─── Toast Bildirimleri ───────────────────────────────────────────────────
    _showToast(opts) {
        const { title, message = '', type = 'info', duration = 4500, } = opts;
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️',
        };
        const toast = document.createElement('div');
        toast.className = `bv-toast bv-toast--${type}`;
        toast.innerHTML = `
      <span class="bv-toast-icon">${icons[type]}</span>
      <div class="bv-toast-body">
        <div class="bv-toast-title">${this._escapeHtml(title)}</div>
        ${message ? `<div class="bv-toast-msg">${this._escapeHtml(message)}</div>` : ''}
      </div>`;
        this._toastContainer.appendChild(toast);
        // Otomatik kaldır
        setTimeout(() => {
            toast.classList.add('fadeout');
            toast.addEventListener('animationend', () => toast.remove(), { once: true });
        }, duration);
    }
    // ─── Yardımcılar ──────────────────────────────────────────────────────────
    /** HTML injection saldırılarını önlemek için escape eder */
    _escapeHtml(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
    // ─── Public Getter'lar ────────────────────────────────────────────────────
    /** Three.js sahne bağlamı (ileri düzey kullanım) */
    get context() { return this._ctx; }
    /** IFC motor referansı (ileri düzey kullanım) */
    get engine() { return this._engine; }
    /** Viewer başlatıldı mı? */
    get isInitialized() { return this._initialized; }
}
//# sourceMappingURL=BIMViewer.js.map