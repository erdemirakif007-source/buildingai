/**
 * mappingPanel.ts
 *
 * BIM Viewer — Element Eşleştirme Paneli
 * ========================================
 *
 * IFC modelindeki elementleri BuildingAI iş kalemleriyle eşleştirir.
 * Eşleştirme yapıldığında progressColoring modülü renklendirmeyi çalıştırır.
 *
 * ─── PANEL YAPisi ─────────────────────────────────────────────────────────────
 *
 *  MappingPanel
 *  ├── Başlık çubuğu (başlık + kapat butonu)
 *  ├── Seçilen Element Kartı
 *  │   ├── IFC Tipi, Ad, Kat, GlobalId
 *  │   └── Mevcut eşleştirme durumu
 *  ├── İş Kalemi Seçici
 *  │   ├── Arama kutusu (yazarken filtrele)
 *  │   ├── İş kalemi listesi (scrollable)
 *  │   └── "Eşleştir" butonu
 *  ├── Toplu Eşleştirme Bölümü
 *  │   └── "Tipe Göre Toplu Eşleştir" butonu + onay dialog'u
 *  ├── Eşleştirme Listesi Tablosu
 *  │   ├── Filtreler (kata/tipe göre)
 *  │   └── Mevcut eşleştirmeler (IFC Tipi | Element | İş Kalemi | Sil)
 *  └── Otomatik Öneri Butonu (placeholder — disabled)
 *
 * ─── API ENTEGRASYONu ─────────────────────────────────────────────────────────
 *
 *  GET  /api/is-kalemleri?santiye_id=…   → İş kalemlerini çek
 *  POST /api/bim/model/{id}/mapping      → Tekli eşleştirme kaydet
 *  POST /api/bim/model/{id}/mapping/bulk → Toplu eşleştirme kaydet
 *
 * GELECEKTEKİ GELİŞTİRMELER:
 *  - Otomatik eşleştirme önerisi (IFC tipi → iş kalemi AI eşleşmesi)
 *  - Eşleştirme geçmişi / undo stack
 *  - CSV dışa aktarma
 */

import { getBIMApiClient } from '../api/bimApi';
import type { AISuggestion } from '../api/types';

// ─── Tip Tanımları ─────────────────────────────────────────────────────────────

/**
 * Seçilen IFC elementi hakkındaki bilgiler.
 * BIMViewer'dan setSelectedElement() ile beslenir.
 */
export interface SelectedElementInfo {
  /** IFC GlobalId (benzersiz tanımlayıcı) */
  globalId: string;
  /** IFC sınıf tipi (örn. "IfcWall") */
  ifcType: string;
  /** Element adı (örn. "Duvar-123") */
  name: string;
  /** Ait olduğu kat (örn. "Zemin Kat") */
  storey: string;
  /** IFC PropertySet + QuantitySet değerleri ("PsetAdı.PropAdı" format) */
  properties?: Record<string, string>;
  /** Mevcut eşleştirme (varsa) */
  currentMapping?: {
    isKalemiId: number;
    isKalemiTanim: string;
    pozNo: string;
  };
}

/**
 * BuildingAI'dan gelen iş kalemi verisi.
 * GET /api/is-kalemleri?santiye_id=… yanıt öğesi.
 */
export interface IsKalemi {
  /** Veritabanı birincil anahtarı */
  id: number;
  /** Poz numarası (örn. "15.140.1003") */
  poz_no: string;
  /** İş tanımı (örn. "C25/30 Hazır Beton Dökülmesi") */
  tanim: string;
  /** Ölçü birimi (örn. "m³") */
  birim: string;
  /** Bağlı iş paketi adı (opsiyonel) */
  is_paketi_adi?: string;
}

/**
 * Mevcut eşleştirme kayıtları için UI satır verisi.
 */
export interface MappingRecord {
  id: string; // Geçici front-end ID (globalId + isKalemiId)
  /** Backend veritabanı eşleştirme ID'si — DELETE için gerekli */
  eslestirmeId?: number;
  ifcType: string;
  elementName: string;
  globalId: string;
  storey: string;
  isKalemiId: number;
  isKalemiTanim: string;
  pozNo: string;
}

/**
 * MappingPanel callback'leri — dışarıdan bağlanır.
 */
export interface MappingPanelCallbacks {
  /**
   * Eşleştirme kaydedilince çağrılır.
   * progressColoring güncellemesi için kullanılır.
   */
  onMappingSaved?: (globalId: string, isKalemiId: number) => void;
  /**
   * Toplu eşleştirme tamamlanınca çağrılır.
   */
  onBulkMappingSaved?: (count: number) => void;
  /**
   * Eşleştirme silinince çağrılır.
   */
  onMappingDeleted?: (globalId: string) => void;
  /**
   * Panel kapatma isteği — toolbar butonunu pasif yapar.
   */
  onClose?: () => void;
  /**
   * Belirli IFC tipindeki tüm elementleri döner (toplu eşleştirme için).
   * BIMViewer tarafından sağlanır; yoksa yalnızca seçili element kullanılır.
   */
  getElementsByType?: (ifcType: string) => Promise<SelectedElementInfo[]>;
}

// ─── Sabitler ──────────────────────────────────────────────────────────────────

/** İş kalemi listesi maksimum kayıt sayısı (performans için) */
const MAX_IS_KALEMLERI = 500;

// ─── Ana Sınıf ─────────────────────────────────────────────────────────────────

/**
 * Element Eşleştirme Paneli
 *
 * KULLANIM ÖRNEĞİ:
 * ```ts
 * const panel = new MappingPanel({
 *   container: document.querySelector('#right-panel')!,
 *   modelId: 42,
 *   santiyeId: 7,
 *   callbacks: {
 *     onMappingSaved: (gid, kid) => progressColoring.refresh(),
 *   },
 * });
 *
 * // Toolbar butonuyla aç/kapat
 * panel.toggle();
 *
 * // Eleman seçilince güncelle
 * panel.setSelectedElement(elementInfo);
 * ```
 */
export class MappingPanel {

  // ── DOM Referansları ───────────────────────────────────────────────────────

  /** Panel kökleri */
  private _panel: HTMLElement;
  private _container: HTMLElement;

  // Seçilen eleman kartı
  private _elType!: HTMLElement;
  private _elName!: HTMLElement;
  private _elStorey!: HTMLElement;
  private _elGlobalId!: HTMLElement;
  private _elCurrentMapping!: HTMLElement;

  // İş kalemi seçici
  private _searchInput!: HTMLInputElement;
  private _itemList!: HTMLElement;
  private _btnEslestir!: HTMLButtonElement;
  private _loadingIndicator!: HTMLElement;

  // Toplu eşleştirme
  private _btnBulkMap!: HTMLButtonElement;

  // Eşleştirme listesi
  private _filterStorey!: HTMLSelectElement;
  private _filterType!: HTMLSelectElement;
  private _mappingTableBody!: HTMLElement;
  private _emptyMappingMsg!: HTMLElement;

  // ── State ─────────────────────────────────────────────────────────────────

  private _isOpen: boolean = false;
  private _modelId: number;
  private _santiyeId: number;
  private _callbacks: MappingPanelCallbacks;

  /** Tüm iş kalemleri listesi (API'den çekilir) */
  private _allIsKalemleri: IsKalemi[] = [];
  /** Filtrelenmiş liste */
  private _filteredIsKalemleri: IsKalemi[] = [];
  /** Seçilen iş kalemi */
  private _selectedIsKalemi: IsKalemi | null = null;
  /** Seçilen IFC elementi */
  private _selectedElement: SelectedElementInfo | null = null;
  /** Mevcut eşleştirmeler (in-memory cache) */
  private _mappings: MappingRecord[] = [];
  /** API yükleniyor mu */
  private _loading: boolean = false;

  // ── Constructor ───────────────────────────────────────────────────────────

  constructor(options: {
    container: HTMLElement;
    modelId: number;
    santiyeId: number;
    callbacks?: MappingPanelCallbacks;
  }) {
    this._container  = options.container;
    this._modelId    = options.modelId;
    this._santiyeId  = options.santiyeId;
    this._callbacks  = options.callbacks ?? {};

    this._panel = this._buildDOM();
    this._container.appendChild(this._panel);
    this._bindEvents();

    console.log('[MappingPanel] Panel oluşturuldu. Model ID:', this._modelId);
  }

  // ── Genel API ─────────────────────────────────────────────────────────────

  /**
   * Paneli açar (kapalıysa) veya kapatır (açıksa).
   */
  toggle(): void {
    this._isOpen ? this.close() : this.open();
  }

  /**
   * Paneli açar ve iş kalemlerini yükler.
   */
  async open(): Promise<void> {
    if (this._isOpen) return;
    this._isOpen = true;
    this._panel.classList.remove('mp-panel--closed');
    this._panel.classList.add('mp-panel--open');

    console.log('[MappingPanel] Panel açıldı.');

    // İş kalemlerini API'den çek (ilk açılışta veya boşsa)
    if (this._allIsKalemleri.length === 0) {
      await this._fetchIsKalemleri();
    }
  }

  /**
   * Paneli kapatır.
   */
  close(): void {
    if (!this._isOpen) return;
    this._isOpen = false;
    this._panel.classList.remove('mp-panel--open');
    this._panel.classList.add('mp-panel--closed');

    console.log('[MappingPanel] Panel kapatıldı.');
    this._callbacks.onClose?.();
  }

  /**
   * Panelin açık olup olmadığını döner.
   */
  get isOpen(): boolean {
    return this._isOpen;
  }

  /**
   * Seçilen IFC elementini günceller.
   * BIMViewer'daki tıklama event'inden çağrılır.
   *
   * @param element - Seçilen element bilgisi (null ise seçim kaldırılır)
   */
  setSelectedElement(element: SelectedElementInfo | null): void {
    this._selectedElement = element;
    this._selectedIsKalemi = null;
    this._updateSelectedElementCard();
    this._updateEslestirButton();

    if (element) {
      console.log('[MappingPanel] Seçilen element:', element.globalId, element.ifcType);
    }
  }

  /**
   * Model ve şantiye bilgilerini günceller (model değişince).
   */
  updateContext(modelId: number, santiyeId: number): void {
    this._modelId   = modelId;
    this._santiyeId = santiyeId;
    // İş kalemlerini yeniden çek
    this._allIsKalemleri = [];
    if (this._isOpen) {
      void this._fetchIsKalemleri();
    }
  }

  /**
   * Mevcut eşleştirmeleri dışarıdan besler (model yüklendikten sonra).
   */
  loadMappings(mappings: MappingRecord[]): void {
    this._mappings = [...mappings];
    this._renderMappingTable();
    this._updateFilterOptions();
  }

  /**
   * Paneli ve tüm alt DOM'ları temizler.
   */
  destroy(): void {
    this._panel.remove();
    console.log('[MappingPanel] Panel yok edildi.');
  }

  // ── DOM Oluşturma ─────────────────────────────────────────────────────────

  /**
   * Panel DOM yapısını oluşturur.
   */
  private _buildDOM(): HTMLElement {
    const panel = document.createElement('aside');
    panel.id = 'mp-panel';
    panel.className = 'mp-panel mp-panel--closed';
    panel.setAttribute('role', 'complementary');
    panel.setAttribute('aria-label', 'Element Eşleştirme Paneli');

    panel.innerHTML = `
      <!-- ── Başlık Çubuğu ──────────────────────────────────────────────── -->
      <div class="mp-header">
        <div class="mp-header-left">
          <span class="mp-header-icon">🔗</span>
          <h2 class="mp-header-title">Element Eşleştirme</h2>
        </div>
        <button class="mp-close-btn" id="mp-close-btn" title="Paneli kapat" aria-label="Paneli kapat">
          ✕
        </button>
      </div>

      <!-- ── Panel İçeriği (scrollable) ────────────────────────────────── -->
      <div class="mp-body" id="mp-body">

        <!-- ── Seçilen Element Kartı ─────────────────────────────────── -->
        <section class="mp-section" id="mp-element-section">
          <div class="mp-section-title">
            <span class="mp-section-icon">📌</span>
            Seçilen Element
          </div>

          <div class="mp-element-card" id="mp-element-card">
            <!-- Boş durum -->
            <div class="mp-element-empty" id="mp-element-empty">
              <span class="mp-element-empty-icon">🖱️</span>
              <span>3D görünümden bir element seçin</span>
            </div>

            <!-- Dolu durum -->
            <div class="mp-element-info" id="mp-element-info" hidden>
              <div class="mp-info-row">
                <span class="mp-info-key">IFC Tipi</span>
                <span class="mp-info-val mp-ifc-type-badge" id="mp-el-type">—</span>
              </div>
              <div class="mp-info-row">
                <span class="mp-info-key">Adı</span>
                <span class="mp-info-val" id="mp-el-name">—</span>
              </div>
              <div class="mp-info-row">
                <span class="mp-info-key">Kat</span>
                <span class="mp-info-val" id="mp-el-storey">—</span>
              </div>
              <div class="mp-info-row">
                <span class="mp-info-key">GlobalId</span>
                <span class="mp-info-val mp-mono" id="mp-el-global-id">—</span>
              </div>
              <div class="mp-info-row mp-current-mapping-row">
                <span class="mp-info-key">Eşleştirme</span>
                <span class="mp-info-val" id="mp-el-current-mapping">
                  <span class="mp-badge mp-badge--none">Eşleştirilmemiş</span>
                </span>
              </div>
            </div>
          </div>
        </section>

        <!-- ── İş Kalemi Seçici ──────────────────────────────────────── -->
        <section class="mp-section" id="mp-selector-section">
          <div class="mp-section-title">
            <span class="mp-section-icon">🔍</span>
            İş Kalemi Seç
          </div>

          <!-- Arama -->
          <div class="mp-search-wrap">
            <span class="mp-search-icon">⌕</span>
            <input
              type="search"
              class="mp-search-input"
              id="mp-search-input"
              placeholder="Poz no veya tanım ara..."
              aria-label="İş kalemi ara"
              autocomplete="off"
            />
            <div class="mp-loading-dot" id="mp-loading-dot" hidden></div>
          </div>

          <!-- İş Kalemi Listesi -->
          <div class="mp-item-list" id="mp-item-list" role="listbox" aria-label="İş kalemleri">
            <div class="mp-item-empty" id="mp-item-loading">
              <span class="mp-spinner-sm"></span>
              <span>İş kalemleri yükleniyor...</span>
            </div>
          </div>

          <!-- Eşleştir Butonu -->
          <button
            class="mp-action-btn mp-action-btn--primary"
            id="mp-btn-eslestir"
            disabled
            aria-label="Seçilen iş kalemiyle eşleştir"
          >
            <span>🔗</span>
            <span>Eşleştir</span>
          </button>
        </section>

        <!-- ── Toplu Eşleştirme ──────────────────────────────────────── -->
        <section class="mp-section" id="mp-bulk-section">
          <div class="mp-section-title">
            <span class="mp-section-icon">⚡</span>
            Toplu İşlemler
          </div>

          <button
            class="mp-action-btn mp-action-btn--secondary"
            id="mp-btn-bulk"
            disabled
            title="Önce bir element ve iş kalemi seçin"
            aria-label="Tipe göre toplu eşleştir"
          >
            <span>🏗️</span>
            <span>Tipe Göre Toplu Eşleştir</span>
          </button>

          <p class="mp-hint-text">
            Seçilen IFC tipindeki <strong>tüm elementleri</strong> aynı iş kalemine eşleştirir.
          </p>
        </section>

        <!-- ── Otomatik Eşleştirme Öner ──────────────────────────────── -->
        <section class="mp-section" id="mp-auto-section">
          <div class="mp-section-title">
            <span class="mp-section-icon">🤖</span>
            Otomatik Eşleştirme
          </div>

          <button
            class="mp-action-btn mp-action-btn--ghost"
            id="mp-btn-auto"
            title="Gemini AI ile seçili element için iş kalemi öner"
            aria-label="Otomatik eşleştirme öner"
          >
            <span>✨</span>
            <span>Otomatik Eşleştirme Öner</span>
          </button>

          <div class="mp-auto-preview" id="mp-auto-preview" hidden>
            <!-- AI öneri kartları buraya render edilir -->
          </div>
        </section>

        <!-- ── Eşleştirme Listesi ─────────────────────────────────────── -->
        <section class="mp-section mp-section--table" id="mp-list-section">
          <div class="mp-section-title">
            <span class="mp-section-icon">📋</span>
            Eşleştirme Listesi
            <span class="mp-list-count" id="mp-list-count">0</span>
          </div>

          <!-- Filtreler -->
          <div class="mp-filters" id="mp-filters">
            <select class="mp-filter-select" id="mp-filter-storey" aria-label="Kata göre filtrele">
              <option value="">Tüm Katlar</option>
            </select>
            <select class="mp-filter-select" id="mp-filter-type" aria-label="Tipe göre filtrele">
              <option value="">Tüm Tipler</option>
            </select>
          </div>

          <!-- Tablo -->
          <div class="mp-table-wrap">
            <table class="mp-table" aria-label="Eşleştirme kayıtları">
              <thead>
                <tr>
                  <th>IFC Tipi</th>
                  <th>Element</th>
                  <th>İş Kalemi</th>
                  <th></th>
                </tr>
              </thead>
              <tbody id="mp-table-body">
                <!-- Dinamik satırlar -->
              </tbody>
            </table>
            <div class="mp-table-empty" id="mp-table-empty">
              <span class="mp-table-empty-icon">🗂️</span>
              <span>Henüz eşleştirme yapılmadı</span>
            </div>
          </div>
        </section>

      </div><!-- /mp-body -->
    `;

    // DOM referanslarını kaydet
    this._elType           = panel.querySelector('#mp-el-type')!;
    this._elName           = panel.querySelector('#mp-el-name')!;
    this._elStorey         = panel.querySelector('#mp-el-storey')!;
    this._elGlobalId       = panel.querySelector('#mp-el-global-id')!;
    this._elCurrentMapping = panel.querySelector('#mp-el-current-mapping')!;
    this._searchInput      = panel.querySelector<HTMLInputElement>('#mp-search-input')!;
    this._itemList         = panel.querySelector('#mp-item-list')!;
    this._btnEslestir      = panel.querySelector<HTMLButtonElement>('#mp-btn-eslestir')!;
    this._loadingIndicator = panel.querySelector('#mp-loading-dot')!;
    this._btnBulkMap       = panel.querySelector<HTMLButtonElement>('#mp-btn-bulk')!;
    this._filterStorey     = panel.querySelector<HTMLSelectElement>('#mp-filter-storey')!;
    this._filterType       = panel.querySelector<HTMLSelectElement>('#mp-filter-type')!;
    this._mappingTableBody = panel.querySelector('#mp-table-body')!;
    this._emptyMappingMsg  = panel.querySelector('#mp-table-empty')!;

    return panel;
  }

  // ── Event Bağlama ─────────────────────────────────────────────────────────

  /**
   * Tüm event listener'ları bağlar.
   */
  private _bindEvents(): void {
    // Kapat butonu
    this._panel.querySelector('#mp-close-btn')
      ?.addEventListener('click', () => this.close());

    // Arama inputu
    this._searchInput.addEventListener('input', () => {
      this._filterIsKalemleri(this._searchInput.value);
    });

    // Eşleştir butonu
    this._btnEslestir.addEventListener('click', () => {
      void this._saveMapping();
    });

    // Toplu eşleştirme
    this._btnBulkMap.addEventListener('click', () => {
      void this._showBulkConfirmDialog();
    });

    // Otomatik eşleştirme
    this._panel.querySelector('#mp-btn-auto')
      ?.addEventListener('click', () => {
        void this._runAutoSuggest();
      });

    // Filtreler
    this._filterStorey.addEventListener('change', () => this._renderMappingTable());
    this._filterType.addEventListener('change', () => this._renderMappingTable());
  }

  // ── API İşlemleri ─────────────────────────────────────────────────────────

  /**
   * GET /api/is-kalemleri?santiye_id=… endpoint'inden iş kalemlerini çeker.
   *
   * Mock data ile başlar, gerçek API hazır olunca yorum kaldırılır.
   */
  private async _fetchIsKalemleri(): Promise<void> {
    if (this._loading) return;
    this._loading = true;
    this._loadingIndicator.hidden = false;

    // Loading durumunu göster
    this._itemList.innerHTML = `
      <div class="mp-item-empty">
        <span class="mp-spinner-sm"></span>
        <span>İş kalemleri yükleniyor...</span>
      </div>
    `;

    try {
      const api = getBIMApiClient();
      const token = api.getToken();

      const baseUrl = (
        (typeof import.meta !== 'undefined'
          ? (import.meta as { env?: { VITE_API_URL?: string } }).env?.VITE_API_URL
          : undefined) ?? ''
      ) || window.location.origin;

      const response = await fetch(
        `${baseUrl}/api/is-kalemleri?santiye_id=${this._santiyeId}&limit=${MAX_IS_KALEMLERI}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        },
      );

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json() as {
        is_kalemleri?: IsKalemi[];
        items?: IsKalemi[];
      };

      // Farklı API yanıt formatlarını destekle
      this._allIsKalemleri = data.is_kalemleri ?? data.items ?? [];
      console.log(`[MappingPanel] ${this._allIsKalemleri.length} iş kalemi yüklendi.`);

    } catch (err) {
      console.warn('[MappingPanel] İş kalemleri yüklenemedi, mock data kullanılıyor:', err);
      // Geliştirme aşamasında mock data
      this._allIsKalemleri = _getMockIsKalemleri();
    } finally {
      this._loading = false;
      this._loadingIndicator.hidden = true;
    }

    // Listeyi render et
    this._filteredIsKalemleri = [...this._allIsKalemleri];
    this._renderIsKalemiList();
  }

  /**
   * Tekli eşleştirmeyi API'ye kaydeder.
   */
  private async _saveMapping(): Promise<void> {
    if (!this._selectedElement || !this._selectedIsKalemi) return;

    const { globalId, ifcType, name, storey, properties } = this._selectedElement;
    const isKalemi = this._selectedIsKalemi;

    this._btnEslestir.disabled = true;
    this._btnEslestir.innerHTML = '<span class="mp-spinner-sm"></span><span>Kaydediliyor...</span>';

    try {
      const api = getBIMApiClient();
      const metrajBilgi = this._extractMetraj(ifcType, properties);
      await api.saveMapping(this._modelId, {
        ifc_global_id:  globalId,
        is_kalemi_id:   isKalemi.id,
        ifc_tip:        ifcType,
        ifc_kat:        storey,
        metraj:         metrajBilgi?.deger,
        metraj_birimi:  metrajBilgi?.birim,
        metraj_kaynagi: metrajBilgi?.kaynak,
      });

      // Yerel eşleştirme listesini güncelle
      this._upsertMapping({
        id: `${globalId}::${isKalemi.id}`,
        ifcType,
        elementName: name,
        globalId,
        storey,
        isKalemiId:    isKalemi.id,
        isKalemiTanim: isKalemi.tanim,
        pozNo:         isKalemi.poz_no,
      });

      // Element kartını güncelle
      if (this._selectedElement) {
        this._selectedElement.currentMapping = {
          isKalemiId: isKalemi.id,
          isKalemiTanim: isKalemi.tanim,
          pozNo: isKalemi.poz_no,
        };
        this._updateSelectedElementCard();
      }

      this._showToast('success', 'Eşleştirme Kaydedildi', `"${name}" → "${isKalemi.tanim}"`);
      this._callbacks.onMappingSaved?.(globalId, isKalemi.id);

      console.log('[MappingPanel] Eşleştirme kaydedildi:', globalId, '→', isKalemi.id);

    } catch (err) {
      console.error('[MappingPanel] Eşleştirme kayıt hatası:', err);
      this._showToast('error', 'Kayıt Hatası', 'Eşleştirme kaydedilemedi. Tekrar deneyin.');
    } finally {
      this._btnEslestir.disabled = false;
      this._btnEslestir.innerHTML = '<span>🔗</span><span>Eşleştir</span>';
    }
  }

  /**
   * Toplu eşleştirme onay dialog'unu gösterir ve onaylanırsa API'ye gönderir.
   */
  private async _showBulkConfirmDialog(): Promise<void> {
    if (!this._selectedElement || !this._selectedIsKalemi) return;

    const { ifcType, storey } = this._selectedElement;
    const isKalemi = this._selectedIsKalemi;

    // Aynı kat ve tipteki elementleri bul
    const sameTypeElements = await this._getElementsOfSameType(ifcType, storey);
    const count = sameTypeElements.length || '?';

    // Onay dialog'u oluştur
    const dialog = document.createElement('div');
    dialog.className = 'mp-dialog-overlay';
    dialog.setAttribute('role', 'dialog');
    dialog.setAttribute('aria-modal', 'true');
    dialog.setAttribute('aria-labelledby', 'mp-dialog-title');

    dialog.innerHTML = `
      <div class="mp-dialog">
        <div class="mp-dialog-header">
          <span class="mp-dialog-icon">⚡</span>
          <h3 class="mp-dialog-title" id="mp-dialog-title">Toplu Eşleştirme Onayı</h3>
        </div>
        <div class="mp-dialog-body">
          <p class="mp-dialog-message">
            <strong>${storey}</strong> katındaki
            <strong>${count} adet ${ifcType}</strong> elementi
            <br/>
            <span class="mp-dialog-target">"${isKalemi.tanim}"</span>
            <br/>
            iş kalemine eşleştirilecek.
          </p>
          <p class="mp-dialog-warn">
            ⚠️ Bu işlem mevcut eşleştirmelerin üzerine yazacak.
          </p>
        </div>
        <div class="mp-dialog-actions">
          <button class="mp-action-btn mp-action-btn--ghost" id="mp-dialog-cancel">
            İptal
          </button>
          <button class="mp-action-btn mp-action-btn--primary" id="mp-dialog-confirm">
            <span>⚡</span>
            <span>Onaylıyorum</span>
          </button>
        </div>
      </div>
    `;

    document.body.appendChild(dialog);

    // Animasyon için küçük gecikme
    requestAnimationFrame(() => dialog.classList.add('mp-dialog-overlay--visible'));

    await new Promise<void>((resolve) => {
      dialog.querySelector('#mp-dialog-cancel')?.addEventListener('click', () => {
        this._closeDialog(dialog);
        resolve();
      });

      dialog.querySelector('#mp-dialog-confirm')?.addEventListener('click', async () => {
        this._closeDialog(dialog);
        await this._executeBulkMapping(sameTypeElements, isKalemi);
        resolve();
      });

      // Overlay'e tıklanınca kapat
      dialog.addEventListener('click', (e) => {
        if (e.target === dialog) {
          this._closeDialog(dialog);
          resolve();
        }
      });
    });
  }

  /**
   * Toplu eşleştirmeyi API'ye gönderir.
   */
  private async _executeBulkMapping(
    elements: SelectedElementInfo[],
    isKalemi: IsKalemi,
  ): Promise<void> {
    if (elements.length === 0) return;

    this._btnBulkMap.disabled = true;
    this._btnBulkMap.innerHTML = '<span class="mp-spinner-sm"></span><span>Eşleştiriliyor...</span>';

    try {
      const api = getBIMApiClient();
      const mappings = elements.map((el) => ({
        ifc_global_id: el.globalId,
        is_kalemi_id:  isKalemi.id,
      }));

      const result = await api.saveBulkMapping(this._modelId, mappings);

      // Yerel listeyi güncelle
      elements.forEach((el) => {
        this._upsertMapping({
          id: `${el.globalId}::${isKalemi.id}`,
          ifcType:       el.ifcType,
          elementName:   el.name,
          globalId:      el.globalId,
          storey:        el.storey,
          isKalemiId:    isKalemi.id,
          isKalemiTanim: isKalemi.tanim,
          pozNo:         isKalemi.poz_no,
        });
      });

      const basarili = result.basarili ?? elements.length;
      this._showToast(
        'success',
        'Toplu Eşleştirme Tamamlandı',
        `${basarili} element başarıyla eşleştirildi.`,
      );

      this._callbacks.onBulkMappingSaved?.(basarili);
      console.log('[MappingPanel] Toplu eşleştirme:', basarili, 'başarılı');

    } catch (err) {
      console.error('[MappingPanel] Toplu eşleştirme hatası:', err);
      this._showToast('error', 'Toplu Eşleştirme Hatası', 'İşlem tamamlanamadı. Tekrar deneyin.');
    } finally {
      this._btnBulkMap.disabled = false;
      this._btnBulkMap.innerHTML = '<span>🏗️</span><span>Tipe Göre Toplu Eşleştir</span>';
    }
  }

  /**
   * Bir eşleştirmeyi backend'den ve yerel listeden siler.
   */
  private _deleteMapping(mappingId: string): void {
    const mapping = this._mappings.find((m) => m.id === mappingId);
    if (!mapping) return;

    // Yerel listeden hemen çıkar (optimistic update)
    this._mappings = this._mappings.filter((m) => m.id !== mappingId);
    this._renderMappingTable();

    // Eğer seçili element buysa kartı güncelle
    if (this._selectedElement?.globalId === mapping.globalId) {
      this._selectedElement.currentMapping = undefined;
      this._updateSelectedElementCard();
    }

    this._callbacks.onMappingDeleted?.(mapping.globalId);

    // Backend API çağrısı (eslestirmeId varsa)
    if (mapping.eslestirmeId !== undefined) {
      const api = getBIMApiClient();
      api.deleteMapping(this._modelId, mapping.eslestirmeId).catch((err) => {
        console.error('[MappingPanel] Eşleştirme backend silme hatası:', err);
        // Hata olursa geri al
        this._mappings.push(mapping);
        this._renderMappingTable();
        this._showToast('error', 'Silme Hatası', 'Eşleştirme silinemedi. Tekrar deneyin.');
      });
    }
  }

  // ── Filtreleme ─────────────────────────────────────────────────────────────

  /**
   * İş kalemi listesini arama terimine göre filtreler.
   */
  private _filterIsKalemleri(query: string): void {
    const q = query.trim().toLowerCase();

    if (!q) {
      this._filteredIsKalemleri = [...this._allIsKalemleri];
    } else {
      this._filteredIsKalemleri = this._allIsKalemleri.filter(
        (k) =>
          k.poz_no.toLowerCase().includes(q) ||
          k.tanim.toLowerCase().includes(q) ||
          (k.birim?.toLowerCase().includes(q) ?? false),
      );
    }

    this._renderIsKalemiList();
  }

  // ── Render Fonksiyonları ───────────────────────────────────────────────────

  /**
   * Seçilen element kartını günceller.
   */
  private _updateSelectedElementCard(): void {
    const el       = this._selectedElement;
    const emptyDiv = this._panel.querySelector<HTMLElement>('#mp-element-empty');
    const infoDiv  = this._panel.querySelector<HTMLElement>('#mp-element-info');

    if (!el) {
      emptyDiv!.hidden = false;
      infoDiv!.hidden  = true;
      return;
    }

    emptyDiv!.hidden = true;
    infoDiv!.hidden  = false;

    this._elType.textContent    = el.ifcType;
    this._elType.dataset['type'] = el.ifcType;
    this._elName.textContent    = el.name;
    this._elStorey.textContent  = el.storey;
    this._elGlobalId.textContent = el.globalId;

    // Mevcut eşleştirme
    if (el.currentMapping) {
      this._elCurrentMapping.innerHTML = `
        <span class="mp-badge mp-badge--mapped" title="${el.currentMapping.isKalemiTanim}">
          ${el.currentMapping.pozNo} — ${el.currentMapping.isKalemiTanim}
        </span>
      `;
    } else {
      this._elCurrentMapping.innerHTML = `
        <span class="mp-badge mp-badge--none">Eşleştirilmemiş</span>
      `;
    }

    // Toplu eşleştirme butonunu güncelle
    this._updateBulkButton();
    // AI öneri panelini sıfırla
    const previewEl = this._panel.querySelector<HTMLElement>('#mp-auto-preview');
    if (previewEl) previewEl.hidden = true;
  }

  /**
   * İş kalemi listesini render eder.
   */
  private _renderIsKalemiList(): void {
    const list = this._filteredIsKalemleri;

    if (list.length === 0) {
      const q = this._searchInput.value.trim();
      this._itemList.innerHTML = `
        <div class="mp-item-empty">
          ${q
            ? `<span>🔍</span><span>"${q}" için sonuç bulunamadı</span>`
            : '<span>📭</span><span>İş kalemi bulunamadı</span>'
          }
        </div>
      `;
      return;
    }

    const fragment = document.createDocumentFragment();

    list.forEach((kalemi) => {
      const item = document.createElement('div');
      item.className = 'mp-list-item';
      item.setAttribute('role', 'option');
      item.dataset['id'] = String(kalemi.id);
      item.setAttribute('tabindex', '0');
      item.setAttribute('aria-selected', 'false');

      item.innerHTML = `
        <div class="mp-list-item-main">
          <span class="mp-list-item-poz">${_escapeHtml(kalemi.poz_no)}</span>
          <span class="mp-list-item-tanim">${_escapeHtml(kalemi.tanim)}</span>
        </div>
        <span class="mp-list-item-birim">${_escapeHtml(kalemi.birim)}</span>
      `;

      item.addEventListener('click', () => this._selectIsKalemi(kalemi, item));
      item.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          this._selectIsKalemi(kalemi, item);
        }
      });

      fragment.appendChild(item);
    });

    this._itemList.innerHTML = '';
    this._itemList.appendChild(fragment);
  }

  /**
   * Eşleştirme tablosunu render eder (filtrelerle).
   */
  private _renderMappingTable(): void {
    const storeyFilter = this._filterStorey.value;
    const typeFilter   = this._filterType.value;

    let records = this._mappings;

    if (storeyFilter) {
      records = records.filter((r) => r.storey === storeyFilter);
    }
    if (typeFilter) {
      records = records.filter((r) => r.ifcType === typeFilter);
    }

    // Sayacı güncelle
    const countEl = this._panel.querySelector('#mp-list-count');
    if (countEl) countEl.textContent = String(this._mappings.length);

    if (records.length === 0) {
      this._mappingTableBody.innerHTML = '';
      this._emptyMappingMsg.hidden = false;
      return;
    }

    this._emptyMappingMsg.hidden = true;

    const fragment = document.createDocumentFragment();

    records.forEach((record) => {
      const tr = document.createElement('tr');
      tr.className = 'mp-table-row';
      tr.dataset['id'] = record.id;

      tr.innerHTML = `
        <td>
          <span class="mp-ifc-type-badge mp-ifc-type-badge--sm" data-type="${_escapeHtml(record.ifcType)}">
            ${_escapeHtml(record.ifcType)}
          </span>
        </td>
        <td class="mp-table-element-cell" title="${_escapeHtml(record.globalId)}">
          <span class="mp-table-el-name">${_escapeHtml(record.elementName)}</span>
          <span class="mp-table-el-storey">${_escapeHtml(record.storey)}</span>
        </td>
        <td class="mp-table-isk-cell" title="${_escapeHtml(record.pozNo)}">
          <span class="mp-table-isk-tanim">${_escapeHtml(record.isKalemiTanim)}</span>
          <span class="mp-table-isk-poz">${_escapeHtml(record.pozNo)}</span>
        </td>
        <td class="mp-table-action-cell">
          <button
            class="mp-delete-btn"
            title="Eşleştirmeyi sil"
            aria-label="${_escapeHtml(record.elementName)} eşleştirmesini sil"
          >
            🗑
          </button>
        </td>
      `;

      tr.querySelector('.mp-delete-btn')?.addEventListener('click', () => {
        this._deleteMapping(record.id);
      });

      fragment.appendChild(tr);
    });

    this._mappingTableBody.innerHTML = '';
    this._mappingTableBody.appendChild(fragment);
  }

  // ── Yardımcı Güncelleme Fonksiyonları ─────────────────────────────────────

  /**
   * "Eşleştir" butonunun aktif/pasif durumunu günceller.
   */
  private _updateEslestirButton(): void {
    const canEslestir = !!this._selectedElement && !!this._selectedIsKalemi;
    this._btnEslestir.disabled = !canEslestir;
  }

  /**
   * Toplu eşleştirme butonunu günceller.
   */
  private _updateBulkButton(): void {
    const canBulk = !!this._selectedElement && !!this._selectedIsKalemi;
    this._btnBulkMap.disabled = !canBulk;

    if (canBulk && this._selectedElement) {
      this._btnBulkMap.title = `"${this._selectedElement.ifcType}" tipindeki tüm elementleri eşleştir`;
    } else {
      this._btnBulkMap.title = 'Önce bir element ve iş kalemi seçin';
    }
  }

  /**
   * Gemini AI'dan eşleştirme önerisi alır ve kartları render eder.
   */
  private async _runAutoSuggest(): Promise<void> {
    if (!this._selectedElement) {
      this._showToast('info', 'Element Seçilmedi', 'Önce 3D görünümden bir element seçin.');
      return;
    }

    const btn = this._panel.querySelector<HTMLButtonElement>('#mp-btn-auto')!;
    const previewEl = this._panel.querySelector<HTMLElement>('#mp-auto-preview')!;

    btn.disabled = true;
    btn.innerHTML = '<span class="mp-spinner-sm"></span><span>AI düşünüyor...</span>';
    previewEl.hidden = false;
    previewEl.innerHTML = `
      <div class="mp-ai-loading">
        <span class="mp-spinner-sm"></span>
        <span>ÇŞB kataloğu analiz ediliyor...</span>
      </div>
    `;

    try {
      const api = getBIMApiClient();
      const el = this._selectedElement;
      const result = await api.suggestMapping(this._santiyeId, {
        modelId:    '',
        expressId:  0,
        ifcType:    el.ifcType,
        name:       el.name,
        globalId:   el.globalId,
        storey:     el.storey,
        properties: el.properties ?? {},
      });

      if (result.status !== 'ok' || result.oneriler.length === 0) {
        previewEl.innerHTML = `
          <div class="mp-ai-empty">
            <span>🤷</span>
            <span>Bu element için uygun öneri bulunamadı.</span>
          </div>
        `;
        return;
      }

      this._renderAISuggestionCards(previewEl, result.oneriler);

    } catch (err) {
      console.error('[MappingPanel] AI öneri hatası:', err);
      const msg = err instanceof Error ? err.message : 'Bilinmeyen hata';
      previewEl.innerHTML = `
        <div class="mp-ai-error">
          <span>⚠️</span>
          <span>AI servisi yanıt vermedi: ${_escapeHtml(msg)}</span>
        </div>
      `;
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<span>✨</span><span>Otomatik Eşleştirme Öner</span>';
    }
  }

  /**
   * AI öneri kartlarını render eder.
   */
  private _renderAISuggestionCards(container: HTMLElement, oneriler: AISuggestion[]): void {
    const html = oneriler.map((o, i) => {
      const skorClass = o.guven_skoru >= 80 ? 'high' : o.guven_skoru >= 50 ? 'mid' : 'low';
      const metrajHtml = o.metraj != null
        ? `<div class="mp-ai-metraj">
             <span class="mp-ai-label">Metraj:</span>
             <strong>${o.metraj} ${_escapeHtml(o.metraj_birimi ?? '')}</strong>
           </div>`
        : '';
      const malzemeHtml = o.malzeme_recetesi.length > 0
        ? `<details class="mp-ai-recipe">
             <summary>Malzeme Reçetesi (${o.malzeme_recetesi.length} kalem)</summary>
             <ul>
               ${o.malzeme_recetesi.map((m) =>
                 `<li>${_escapeHtml(m.malzeme)} — ${m.miktar_birim_basina} ${_escapeHtml(m.birim)}${m.zorunlu ? ' <em>*</em>' : ''}</li>`
               ).join('')}
             </ul>
           </details>`
        : '';

      return `
        <div class="mp-ai-card" data-index="${i}">
          <div class="mp-ai-card-header">
            <div class="mp-ai-card-title">
              <span class="mp-ai-poz">${_escapeHtml(o.poz_no)}</span>
              <span class="mp-ai-ad">${_escapeHtml(o.ad)}</span>
            </div>
            <div class="mp-ai-skor mp-ai-skor--${skorClass}" title="Eşleşme güveni">
              %${o.guven_skoru}
            </div>
          </div>
          <div class="mp-ai-birim">Birim: <strong>${_escapeHtml(o.birim)}</strong></div>
          <div class="mp-ai-gerekce">${_escapeHtml(o.gerekce)}</div>
          ${metrajHtml}
          ${malzemeHtml}
          <button class="mp-action-btn mp-action-btn--primary mp-ai-uygula" data-index="${i}">
            <span>✅</span><span>Uygula</span>
          </button>
        </div>
      `;
    }).join('');

    container.innerHTML = `<div class="mp-ai-cards">${html}</div>`;

    // "Uygula" butonlarına event bağla
    container.querySelectorAll<HTMLButtonElement>('.mp-ai-uygula').forEach((btn) => {
      btn.addEventListener('click', () => {
        const idx = Number(btn.dataset['index'] ?? 0);
        void this._applyAISuggestion(oneriler[idx]);
      });
    });
  }

  /**
   * Seçilen AI önerisini eşleştirme olarak kaydeder.
   */
  private async _applyAISuggestion(oneri: AISuggestion): Promise<void> {
    if (!this._selectedElement) return;

    const { globalId, ifcType, name, storey } = this._selectedElement;

    // Mevcut iş kalemleri arasında poz_no ile eşleşen var mı?
    let isKalemi = this._allIsKalemleri.find((k) => k.poz_no === oneri.poz_no);

    if (!isKalemi) {
      // Yeni iş kalemi oluştur
      try {
        const api = getBIMApiClient();
        const token = api.getToken();
        const baseUrl = (
          (typeof import.meta !== 'undefined'
            ? (import.meta as { env?: { VITE_API_URL?: string } }).env?.VITE_API_URL
            : undefined) ?? ''
        ) || window.location.origin;

        const res = await fetch(`${baseUrl}/api/v2/santiye/${this._santiyeId}/is-kalemleri`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            katalog_id: oneri.katalog_id,
            poz_no:     oneri.poz_no,
            tanim:      oneri.ad,
            birim:      oneri.birim,
            metraj:     oneri.metraj ?? 0,
            durum:      'planli',
          }),
        });

        if (!res.ok) {
          const err = await res.json().catch(() => ({ detail: res.statusText })) as { detail?: string };
          throw new Error(err.detail ?? `HTTP ${res.status}`);
        }

        isKalemi = await res.json() as IsKalemi;
        this._allIsKalemleri.push(isKalemi);

      } catch (err) {
        const msg = err instanceof Error ? err.message : 'Bilinmeyen hata';
        this._showToast('error', 'İş Kalemi Oluşturulamadı', msg);
        return;
      }
    }

    // Eşleştirmeyi kaydet
    try {
      const api = getBIMApiClient();
      await api.saveMapping(this._modelId, {
        ifc_global_id:  globalId,
        is_kalemi_id:   isKalemi.id,
        ifc_tip:        ifcType,
        ifc_kat:        storey,
        metraj:         oneri.metraj ?? undefined,
        metraj_birimi:  oneri.metraj_birimi ?? undefined,
        metraj_kaynagi: oneri.metraj_kaynagi ?? undefined,
      });

      this._upsertMapping({
        id:            `${globalId}::${isKalemi.id}`,
        ifcType,
        elementName:   name,
        globalId,
        storey,
        isKalemiId:    isKalemi.id,
        isKalemiTanim: isKalemi.tanim,
        pozNo:         isKalemi.poz_no,
      });

      if (this._selectedElement) {
        this._selectedElement.currentMapping = {
          isKalemiId:    isKalemi.id,
          isKalemiTanim: isKalemi.tanim,
          pozNo:         isKalemi.poz_no,
        };
        this._updateSelectedElementCard();
      }

      // Öneri panelini gizle
      const previewEl = this._panel.querySelector<HTMLElement>('#mp-auto-preview');
      if (previewEl) previewEl.hidden = true;

      this._showToast(
        'success',
        'AI Önerisi Uygulandı',
        `"${_escapeHtml(name)}" → "${_escapeHtml(isKalemi.tanim)}"`,
      );
      this._callbacks.onMappingSaved?.(globalId, isKalemi.id);

    } catch (err) {
      console.error('[MappingPanel] AI öneri uygulama hatası:', err);
      this._showToast('error', 'Eşleştirme Hatası', 'Eşleştirme kaydedilemedi. Tekrar deneyin.');
    }
  }

  /**
   * Element properties'inden metraj değerini çıkarır.
   * QtoSetAdı.MiktarAdı formatındaki QuantitySet verilerini tarar.
   */
  private _extractMetraj(
    ifcType: string,
    properties?: Record<string, string>,
  ): { deger: number; birim: string; kaynak: string } | null {
    if (!properties) return null;

    // IFC tipine göre öncelikli QuantitySet anahtarları
    const candidates: Array<{ key: string; birim: string }> = [
      { key: `Qto_${ifcType.replace('Ifc', '')}BaseQuantities.GrossVolume`, birim: 'm³' },
      { key: `Qto_${ifcType.replace('Ifc', '')}BaseQuantities.NetVolume`,   birim: 'm³' },
      { key: `Qto_${ifcType.replace('Ifc', '')}BaseQuantities.GrossArea`,   birim: 'm²' },
      { key: `Qto_${ifcType.replace('Ifc', '')}BaseQuantities.NetArea`,     birim: 'm²' },
      { key: `Qto_${ifcType.replace('Ifc', '')}BaseQuantities.Length`,      birim: 'm' },
    ];

    for (const { key, birim } of candidates) {
      const val = properties[key];
      if (val !== undefined && val !== null && val !== '') {
        const deger = parseFloat(val);
        if (!isNaN(deger) && deger > 0) {
          return { deger, birim, kaynak: key };
        }
      }
    }
    return null;
  }

  /**
   * Filtre dropdown'larını mevcut eşleştirmelere göre günceller.
   */
  private _updateFilterOptions(): void {
    const storeys = [...new Set(this._mappings.map((m) => m.storey))].sort();
    const types   = [...new Set(this._mappings.map((m) => m.ifcType))].sort();

    const currentStorey = this._filterStorey.value;
    const currentType   = this._filterType.value;

    this._filterStorey.innerHTML = '<option value="">Tüm Katlar</option>' +
      storeys.map((s) => `<option value="${_escapeHtml(s)}">${_escapeHtml(s)}</option>`).join('');

    this._filterType.innerHTML = '<option value="">Tüm Tipler</option>' +
      types.map((t) => `<option value="${_escapeHtml(t)}">${_escapeHtml(t)}</option>`).join('');

    // Önceki seçimi koru
    this._filterStorey.value = currentStorey;
    this._filterType.value   = currentType;
  }

  // ── Seçim İşlemleri ───────────────────────────────────────────────────────

  /**
   * Bir iş kalemini seçer.
   */
  private _selectIsKalemi(kalemi: IsKalemi, itemEl: HTMLElement): void {
    // Önceki seçimi temizle
    this._itemList.querySelectorAll('.mp-list-item--selected').forEach((el) => {
      el.classList.remove('mp-list-item--selected');
      el.setAttribute('aria-selected', 'false');
    });

    // Yeni seçim
    itemEl.classList.add('mp-list-item--selected');
    itemEl.setAttribute('aria-selected', 'true');

    this._selectedIsKalemi = kalemi;
    this._updateEslestirButton();
    this._updateBulkButton();

    console.log('[MappingPanel] İş kalemi seçildi:', kalemi.poz_no, kalemi.tanim);
  }

  // ── Yardımcı Araçlar ──────────────────────────────────────────────────────

  /**
   * Eşleştirmeyi yerel listeye ekler veya günceller (upsert).
   */
  private _upsertMapping(record: MappingRecord): void {
    const idx = this._mappings.findIndex((m) => m.globalId === record.globalId);
    if (idx >= 0) {
      this._mappings[idx] = record;
    } else {
      this._mappings.push(record);
    }
    this._renderMappingTable();
    this._updateFilterOptions();
  }

  /**
   * Belirli IFC tipindeki tüm elementleri döner.
   * BIMViewer tarafından `callbacks.getElementsByType` sağlanmışsa onu kullanır;
   * yoksa yalnızca seçili elementi döner.
   */
  private async _getElementsOfSameType(ifcType: string, _storey: string): Promise<SelectedElementInfo[]> {
    if (!this._selectedElement) return [];

    if (this._callbacks.getElementsByType) {
      const all = await this._callbacks.getElementsByType(ifcType);
      return all.length > 0 ? all : [this._selectedElement];
    }

    return [this._selectedElement];
  }

  /**
   * Dialog'u animasyonlu kapatır.
   */
  private _closeDialog(dialog: HTMLElement): void {
    dialog.classList.remove('mp-dialog-overlay--visible');
    setTimeout(() => dialog.remove(), 200);
  }

  /**
   * Panel içinde toast benzeri bildirim gösterir.
   */
  private _showToast(type: 'success' | 'error' | 'info', title: string, message: string): void {
    // Global toast container'ı kullan (main.css'de .bv-toast-container)
    let container = document.querySelector<HTMLElement>('.bv-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'bv-toast-container';
      document.body.appendChild(container);
    }

    const icons: Record<string, string> = { success: '✅', error: '❌', info: 'ℹ️' };

    const toast = document.createElement('div');
    toast.className = `bv-toast bv-toast--${type}`;
    toast.innerHTML = `
      <span class="bv-toast-icon">${icons[type] ?? 'ℹ️'}</span>
      <div class="bv-toast-body">
        <div class="bv-toast-title">${_escapeHtml(title)}</div>
        <div class="bv-toast-msg">${_escapeHtml(message)}</div>
      </div>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('fadeout');
      setTimeout(() => toast.remove(), 250);
    }, 3500);
  }
}

// ─── Toolbar Entegrasyonu ──────────────────────────────────────────────────────

/**
 * Toolbar'a "Eşleştirme Modu" butonunu ekler.
 *
 * KULLANIM:
 * ```ts
 * const panel = new MappingPanel({ ... });
 * addMappingToolbarButton(toolbar, panel);
 * ```
 *
 * @param toolbar      - Toolbar DOM elementi (.bv-toolbar)
 * @param mappingPanel - MappingPanel örneği
 */
export function addMappingToolbarButton(
  toolbar: HTMLElement,
  mappingPanel: MappingPanel,
): HTMLButtonElement {

  // Separator
  const sep = document.createElement('div');
  sep.className = 'bv-separator';
  toolbar.appendChild(sep);

  // Buton
  const btn = document.createElement('button');
  btn.id = 'btn-mapping-mode';
  btn.className = 'bv-btn';
  btn.setAttribute('title', 'Element Eşleştirme Modu (M)');
  btn.setAttribute('aria-label', 'Eşleştirme modunu aç/kapat');
  btn.setAttribute('aria-pressed', 'false');
  btn.innerHTML = `<span>🔗</span><span>Eşleştirme</span>`;

  btn.addEventListener('click', () => {
    mappingPanel.toggle();
    const isOpen = mappingPanel.isOpen;
    btn.classList.toggle('bv-btn--active', isOpen);
    btn.setAttribute('aria-pressed', String(isOpen));
  });

  // Panel kapanınca buton pasif duruma geç
  const originalOnClose = mappingPanel['_callbacks'].onClose;
  mappingPanel['_callbacks'].onClose = () => {
    btn.classList.remove('bv-btn--active');
    btn.setAttribute('aria-pressed', 'false');
    originalOnClose?.();
  };

  // Klavye kısayolu: M tuşu
  document.addEventListener('keydown', (e) => {
    if (
      e.key === 'm' &&
      !e.ctrlKey &&
      !e.altKey &&
      !e.shiftKey &&
      !(e.target instanceof HTMLInputElement) &&
      !(e.target instanceof HTMLTextAreaElement)
    ) {
      btn.click();
    }
  });

  toolbar.appendChild(btn);
  console.log('[MappingPanel] Toolbar butonu eklendi (kısayol: M).');

  return btn;
}

// ─── Mock Data (Geliştirme Aşaması) ───────────────────────────────────────────

/**
 * API hazır olmadan geliştirme aşamasında kullanılacak örnek iş kalemleri.
 * Gerçek API entegrasyonunda bu fonksiyon kullanılmaz.
 */
function _getMockIsKalemleri(): IsKalemi[] {
  return [
    { id: 1,  poz_no: '03.502.1001', tanim: 'Briket Duvar (19cm)',             birim: 'm²' },
    { id: 2,  poz_no: '03.502.1002', tanim: 'Tuğla Duvar (13.5cm)',            birim: 'm²' },
    { id: 3,  poz_no: '03.502.1003', tanim: 'Gaz Beton Duvar (20cm)',          birim: 'm²' },
    { id: 4,  poz_no: '15.140.1001', tanim: 'C20/25 Hazır Beton Dökülmesi',   birim: 'm³' },
    { id: 5,  poz_no: '15.140.1002', tanim: 'C25/30 Hazır Beton Dökülmesi',   birim: 'm³' },
    { id: 6,  poz_no: '15.140.1003', tanim: 'C30/37 Hazır Beton Dökülmesi',   birim: 'm³' },
    { id: 7,  poz_no: '15.140.1010', tanim: 'C25/30 Kalıp Çelik Donatısı',    birim: 'ton' },
    { id: 8,  poz_no: '15.210.1001', tanim: 'Betonarme Kolon Kalıbı',          birim: 'm²' },
    { id: 9,  poz_no: '15.210.1002', tanim: 'Betonarme Kiriş Kalıbı',          birim: 'm²' },
    { id: 10, poz_no: '15.210.1003', tanim: 'Betonarme Döşeme Kalıbı',         birim: 'm²' },
    { id: 11, poz_no: '21.010.1001', tanim: 'PVC Doğrama (Tek Cam)',           birim: 'm²' },
    { id: 12, poz_no: '21.010.1002', tanim: 'PVC Doğrama (Çift Cam)',          birim: 'm²' },
    { id: 13, poz_no: '21.011.1001', tanim: 'Ahşap İç Kapı (PB Kanatlı)',      birim: 'adet' },
    { id: 14, poz_no: '21.011.1002', tanim: 'Çelik Yangın Kapısı (EI90)',      birim: 'adet' },
    { id: 15, poz_no: '25.010.1001', tanim: 'İç Sıva (Alçı)',                  birim: 'm²' },
    { id: 16, poz_no: '25.020.1001', tanim: 'Dış Cephe Sıvası (Cem. Esaslı)', birim: 'm²' },
    { id: 17, poz_no: '27.010.1001', tanim: 'Seramik Yer Kaplaması (30x30)',   birim: 'm²' },
    { id: 18, poz_no: '27.010.1002', tanim: 'Granit Yer Kaplaması (60x60)',    birim: 'm²' },
    { id: 19, poz_no: '28.030.1001', tanim: 'Çatı Terası Su Yalıtımı',         birim: 'm²' },
    { id: 20, poz_no: '28.030.1002', tanim: 'Bitümlü Örtü (4mm)',              birim: 'm²' },
  ];
}

// ─── Yardımcı Fonksiyonlar ─────────────────────────────────────────────────────

/**
 * HTML özel karakterlerini kaçış karakterine çevirir (XSS koruması).
 */
function _escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
