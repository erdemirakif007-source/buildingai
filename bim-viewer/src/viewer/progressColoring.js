/**
 * progressColoring.ts
 *
 * BuildingAI iş kalemi ilerleme verilerini 3D model üzerinde renk olarak görselleştirir.
 *
 * ─── MİMARİ GENEL BAKIŞ ──────────────────────────────────────────────────────
 *
 *  ProgressColoring
 *  ├── applyProgressColors(data)  → GlobalId → localId → setColor()
 *  ├── clearColors()              → resetColor(undefined) — tümünü temizle
 *  ├── setColorMode(mode)         → progress / type / storey / original
 *  ├── getProgressSummary()       → Statusbar özet verisi
 *  └── legend UI                 → Viewport sağ alt köşesi floating kutusu
 *
 * ─── RENK ATAMA AKIŞI ────────────────────────────────────────────────────────
 *
 *  Backend data (ElementProgressMapping[])
 *       │
 *       ▼  getLocalIdsByGuids(guids)   [Worker thread — GUID → localId çevirisi]
 *  localId[]
 *       │
 *       ▼  model.setColor(localIds, color)   [GPU-side renk override]
 *  3D Görsel renklendirme
 *
 * ─── MOCK DATA ────────────────────────────────────────────────────────────────
 *
 *  Bu sürümde backend entegrasyonu yok. getMockProgressData() sahte veri üretir.
 *  Gerçek API entegrasyonu Aşama 4'te:
 *    - GET /api/projects/{id}/ifc-progress → ElementProgressMapping[]
 *    - İFC GlobalId ↔ BuildingAI iş kalemi eşleşmesi backend'de tutulur
 *
 * ─── GELECEKTEKİ GELİŞTİRMELER ──────────────────────────────────────────────
 *  - Gerçek BuildingAI API entegrasyonu (Aşama 4)
 *  - Zaman eksenli animasyon (Gantt → 3D geçişi)
 *  - İlerleme yüzdesi tabanlı gradient renklendirme (0% gri → 100% yeşil)
 *  - Kategori bazlı filtre (sadece IfcWall'ları renklendir vb.)
 *  - Opacity override — tamamlananları hafif şeffaf yap
 */
import * as THREE from 'three';
// ─── Sabit Renk Paleti ─────────────────────────────────────────────────────────
/**
 * İlerleme durumlarına karşılık gelen THREE.Color renk değerleri.
 * BuildingAI UI renk sistemiyle uyumludur.
 */
export const PROGRESS_COLORS = {
    /** Gri — henüz başlanmamış, takvimde var */
    planli: new THREE.Color(0x9E9E9E),
    /** Turuncu — BuildingAI accent rengi, aktif çalışma */
    devam_ediyor: new THREE.Color(0xE15A1F),
    /** Yeşil — iş tamamlandı */
    tamamlandi: new THREE.Color(0x4CAF50),
    /** Amber — bekliyor, bağımlılık veya malzeme eksik */
    beklemede: new THREE.Color(0xFF9800),
    /** Açık gri — BuildingAI verisinde bu element için eşleşme yok */
    eslesmemis: new THREE.Color(0xC8C8C8),
};
/**
 * IFC tipine göre renk paleti (type modu için).
 * Mimari standart renk kodlaması.
 */
const TYPE_COLORS = {
    IfcWall: new THREE.Color(0x4A90D9), // Mavi — duvarlar
    IfcWallStandardCase: new THREE.Color(0x4A90D9),
    IfcSlab: new THREE.Color(0x7CB342), // Yeşil — döşemeler
    IfcColumn: new THREE.Color(0xE53935), // Kırmızı — kolonlar
    IfcBeam: new THREE.Color(0xFB8C00), // Turuncu — kirişler
    IfcDoor: new THREE.Color(0x8E24AA), // Mor — kapılar
    IfcWindow: new THREE.Color(0x00ACC1), // Cyan — pencereler
    IfcRoof: new THREE.Color(0x6D4C41), // Kahverengi — çatı
    IfcStair: new THREE.Color(0xFF7043), // Derin turuncu — merdivenler
    IfcRailing: new THREE.Color(0x546E7A), // Çelik mavisi — korkuluklar
    IfcFoundation: new THREE.Color(0x37474F), // Koyu — temel
};
/** Tanımlanmamış IFC tipleri için varsayılan renk */
const DEFAULT_TYPE_COLOR = new THREE.Color(0x78909C);
// ─── Gradient Yardımcı ────────────────────────────────────────────────────────
/**
 * İlerleme yüzdesine göre lineer interpolasyonla renk döndürür.
 * "devam_ediyor" durumundaki elementlere uygulanır.
 *
 * Anchor noktaları:
 *   0%  → #F44336 (kırmızı)
 *  25%  → #FF9800 (turuncu)
 *  50%  → #FFC107 (sarı)
 *  75%  → #8BC34A (açık yeşil)
 * 100%  → #4CAF50 (yeşil)
 */
function _gradientColorForProgress(yuzde) {
    const pct = Math.max(0, Math.min(100, yuzde));
    const anchors = [
        [0, new THREE.Color(0xF44336)],
        [25, new THREE.Color(0xFF9800)],
        [50, new THREE.Color(0xFFC107)],
        [75, new THREE.Color(0x8BC34A)],
        [100, new THREE.Color(0x4CAF50)],
    ];
    for (let i = 0; i < anchors.length - 1; i++) {
        const [p0, c0] = anchors[i];
        const [p1, c1] = anchors[i + 1];
        if (pct >= p0 && pct <= p1) {
            const t = p1 === p0 ? 0 : (pct - p0) / (p1 - p0);
            return c0.clone().lerp(c1, t);
        }
    }
    return new THREE.Color(0x4CAF50);
}
/** Kat renklendirme paleti — StoreyManager ile koordineli */
const STOREY_PALETTE = [
    new THREE.Color(0x3F51B5), // İndigo
    new THREE.Color(0x0097A7), // Teal
    new THREE.Color(0x388E3C), // Yeşil
    new THREE.Color(0xF57C00), // Turuncu
    new THREE.Color(0xC62828), // Kırmızı
    new THREE.Color(0x6A1B9A), // Mor
    new THREE.Color(0x00695C), // Koyu teal
    new THREE.Color(0x558B2F), // Açık yeşil
    new THREE.Color(0xAD1457), // Pembe
    new THREE.Color(0x1565C0), // Koyu mavi
];
// ─── Ana Sınıf ─────────────────────────────────────────────────────────────────
/**
 * BuildingAI ilerleme verilerini 3D model üzerinde renk olarak görselleştirir.
 *
 * KULLANIM ÖRNEĞİ:
 * ```ts
 * const coloring = new ProgressColoring(fragments, viewportEl);
 * await coloring.applyProgressColors(progressData);
 *
 * // Özet bilgisini al
 * const summary = coloring.getProgressSummary();
 * console.log(`Tamamlanma: %${summary.tamamlanmaYuzdesi}`);
 *
 * // Modu değiştir
 * await coloring.setColorMode('type');
 *
 * // Temizle
 * await coloring.clearColors();
 * ```
 */
export class ProgressColoring {
    // ─── Constructor ──────────────────────────────────────────────────────────
    /**
     * @param fragments - FragmentsModels orkestratörü (IFCLoaderEngine.fragments)
     * @param viewport  - Legend UI'ının ekleneceği viewport DOM elementi
     */
    constructor(fragments, viewport) {
        // ── Durum ────────────────────────────────────────────────────────────────
        /** Aktif model referansı */
        this._model = null;
        /** Mevcut renk modu */
        this._colorMode = 'original';
        /** Son uygulanan progress verisi */
        this._lastProgressData = null;
        /** GlobalId → ElementProgressMapping haritası (hızlı erişim) */
        this._guidToMapping = new Map();
        /** localId → durum haritası (son hesaplama) */
        this._localIdToStatus = new Map();
        /** Toplam model element sayısı (getItemsIdsWithGeometry'den) */
        this._totalElements = 0;
        // ── Legend UI ────────────────────────────────────────────────────────────
        /** Viewport'taki floating legend kutusu elementi */
        this._legendEl = null;
        /** Legend görünürlük durumu */
        this._legendVisible = true;
        // ── Callback'ler ─────────────────────────────────────────────────────────
        /**
         * Renk modu değiştiğinde çağrılır.
         * Statusbar veya diğer UI bileşenleri için kullanılabilir.
         */
        this.onColorModeChange = null;
        this._fragments = fragments;
        this._viewport = viewport;
    }
    // ─── Public API: Renklendirme ─────────────────────────────────────────────
    /**
     * İlerleme verilerini modele uygular.
     *
     * ADIMLAR:
     * 1. Aktif modeli al
     * 2. ElementProgressMapping'deki GlobalId'leri localId'ye çevir
     * 3. Her element grubuna (durum bazlı) renk ata
     * 4. Eşleşmeyenlere eslesmemis rengi ver
     * 5. Legend UI'ını güncelle
     *
     * @param data - BuildingAI backend'inden gelen ilerleme verisi
     * @param modelId - Hangi modele uygulanacağı (varsayılan: ilk yüklü model)
     */
    async applyProgressColors(data, modelId) {
        const model = this._getModel(modelId);
        if (!model) {
            console.warn('[ProgressColoring] Aktif model yok — önce bir IFC dosyası yükleyin.');
            return;
        }
        console.log(`[ProgressColoring] İlerleme renklendirmesi uygulanıyor: ${data.elementMapping.length} element eşleme`);
        this._model = model;
        this._lastProgressData = data;
        this._colorMode = 'progress';
        // GUID → Mapping indeksi oluştur
        this._guidToMapping.clear();
        for (const mapping of data.elementMapping) {
            this._guidToMapping.set(mapping.ifcGlobalId, mapping);
        }
        try {
            // 1. Tüm model elementlerinin GUID'lerini al
            const allGuids = await model.getGuids();
            this._totalElements = allGuids.length;
            // 2. Duruma göre GUID grupları oluştur
            const byDurum = {
                planli: [],
                devam_ediyor: [],
                tamamlandi: [],
                beklemede: [],
                eslesmemis: [],
            };
            const unmatched = [];
            for (const guid of allGuids) {
                if (!guid)
                    continue;
                const mapping = this._guidToMapping.get(guid);
                if (mapping) {
                    byDurum[mapping.durum]?.push(guid);
                }
                else {
                    unmatched.push(guid);
                }
            }
            // 3. Her grup için localId'leri al ve renk ata
            this._localIdToStatus.clear();
            // planli / tamamlandi / beklemede / eslesmemis — sabit renk
            const sabitDurumlar = ['planli', 'tamamlandi', 'beklemede', 'eslesmemis'];
            for (const durum of sabitDurumlar) {
                const guids = byDurum[durum];
                if (guids.length === 0)
                    continue;
                const localIds = await model.getLocalIdsByGuids(guids);
                const validIds = localIds.filter((id) => id !== null);
                if (validIds.length === 0)
                    continue;
                await model.setColor(validIds, PROGRESS_COLORS[durum]);
                for (const id of validIds) {
                    this._localIdToStatus.set(id, durum);
                }
                console.log(`[ProgressColoring] ${durum}: ${validIds.length} element renklendi`);
            }
            // devam_ediyor — ilerleme yüzdesine göre gradient
            const devamGuids = byDurum['devam_ediyor'];
            if (devamGuids.length > 0) {
                const devamLocalIds = await model.getLocalIdsByGuids(devamGuids);
                // Renk → localId[] grupları (aynı renk bucket'ı = tek setColor çağrısı)
                const colorBuckets = new Map();
                for (let i = 0; i < devamGuids.length; i++) {
                    const localId = devamLocalIds[i];
                    if (localId === null || localId === undefined)
                        continue;
                    const guid = devamGuids[i];
                    const mapping = this._guidToMapping.get(guid);
                    const pct = mapping?.ilerlemeYuzdesi ?? 0;
                    const color = _gradientColorForProgress(pct);
                    const key = color.getHexString();
                    if (!colorBuckets.has(key))
                        colorBuckets.set(key, { color, ids: [] });
                    colorBuckets.get(key).ids.push(localId);
                    this._localIdToStatus.set(localId, 'devam_ediyor');
                }
                for (const { color, ids } of colorBuckets.values()) {
                    await model.setColor(ids, color);
                }
                console.log(`[ProgressColoring] devam_ediyor: ${devamGuids.length} element gradient renklendi (${colorBuckets.size} bucket)`);
            }
            // 4. Eşleşmeyenler — eslesmemis rengi
            if (unmatched.length > 0) {
                const unmatchedIds = await model.getLocalIdsByGuids(unmatched);
                const validUnmatched = unmatchedIds.filter((id) => id !== null);
                if (validUnmatched.length > 0) {
                    await model.setColor(validUnmatched, PROGRESS_COLORS.eslesmemis);
                    for (const localId of validUnmatched) {
                        this._localIdToStatus.set(localId, 'eslesmemis');
                    }
                }
                console.log(`[ProgressColoring] Eşleşmemiş: ${validUnmatched.length} element`);
            }
            // 5. Renderer'ı güncelle
            await this._fragments.update(true);
            // 6. Legend'ı güncelle
            this._updateLegend('progress');
            console.log(`[ProgressColoring] ✓ İlerleme renklendirmesi tamamlandı.`);
        }
        catch (err) {
            console.error('[ProgressColoring] Renklendirme hatası:', err);
        }
    }
    /**
     * Tüm renk override'larını kaldırır ve orijinal IFC materyallerine döner.
     *
     * `model.resetColor(undefined)` → tüm elementlerin rengi sıfırlanır.
     */
    async clearColors() {
        const model = this._model;
        if (!model)
            return;
        try {
            // undefined → tüm elementleri etkiler
            await model.resetColor(undefined);
            await this._fragments.update(true);
            this._colorMode = 'original';
            this._localIdToStatus.clear();
            this._updateLegend('original');
            console.log('[ProgressColoring] ✓ Tüm renk override\'ları kaldırıldı.');
        }
        catch (err) {
            console.error('[ProgressColoring] clearColors hatası:', err);
        }
    }
    /**
     * Renk modunu değiştirir.
     *
     * @param mode - Yeni renk modu:
     *   - `'progress'` : İlerleme durumuna göre (son yüklenen progress data kullanılır)
     *   - `'type'`     : IFC element tipine göre (duvar=mavi, döşeme=yeşil vb.)
     *   - `'storey'`   : Her kat farklı renk
     *   - `'original'` : IFC'deki orijinal materyaller (renk override yok)
     */
    async setColorMode(mode) {
        if (this._colorMode === mode)
            return;
        console.log(`[ProgressColoring] Renk modu değiştiriliyor: ${this._colorMode} → ${mode}`);
        // Önce mevcut renkleri temizle
        const model = this._model;
        if (model) {
            await model.resetColor(undefined);
        }
        switch (mode) {
            case 'progress':
                if (this._lastProgressData) {
                    await this.applyProgressColors(this._lastProgressData);
                }
                else {
                    // Gerçek veri yok — mock data ile göster
                    await this._applyMockProgressColors();
                }
                break;
            case 'type':
                await this._applyTypeColors();
                break;
            case 'storey':
                await this._applyStoreyColors();
                break;
            case 'original':
                // resetColor zaten yapıldı yukarıda
                await this._fragments.update(true);
                this._updateLegend('original');
                break;
        }
        this._colorMode = mode;
        this.onColorModeChange?.(mode);
    }
    /**
     * İlerleme özet istatistiklerini döndürür.
     *
     * Statusbar ve dashboard bileşenleri için kullanılır.
     * applyProgressColors() çağrılmadan önce tüm değerler 0 döner.
     */
    getProgressSummary() {
        let planli = 0;
        let devamEdiyor = 0;
        let tamamlandi = 0;
        let beklemede = 0;
        let eslesen = 0;
        for (const status of this._localIdToStatus.values()) {
            switch (status) {
                case 'planli':
                    planli++;
                    eslesen++;
                    break;
                case 'devam_ediyor':
                    devamEdiyor++;
                    eslesen++;
                    break;
                case 'tamamlandi':
                    tamamlandi++;
                    eslesen++;
                    break;
                case 'beklemede':
                    beklemede++;
                    eslesen++;
                    break;
                // 'eslesmemis' — eslesen sayısına dahil etme
            }
        }
        const tamamlanmaYuzdesi = eslesen > 0
            ? Math.round((tamamlandi / eslesen) * 100)
            : 0;
        return {
            toplamElement: this._totalElements,
            eslesen,
            planli,
            devamEdiyor,
            tamamlandi,
            beklemede,
            tamamlanmaYuzdesi,
        };
    }
    /**
     * Bir elementin renk moduna göre etiketini döndürür.
     * Tooltip veya properties panel için kullanılabilir.
     *
     * @param localId - Sorgulanacak elementin localId'si
     */
    getElementLabel(localId) {
        const status = this._localIdToStatus.get(localId);
        if (!status)
            return null;
        const labels = {
            planli: 'Planlı',
            devam_ediyor: 'Devam Ediyor',
            tamamlandi: 'Tamamlandı',
            beklemede: 'Beklemede',
            eslesmemis: 'Eşleşmemiş',
        };
        return labels[status] ?? status;
    }
    // ─── Mock Data ────────────────────────────────────────────────────────────
    /**
     * Geliştirme aşamasında kullanılacak sahte ilerleme verisi üretir.
     *
     * Gerçek model elementlerinin GUID'lerini alır ve rastgele durum atar.
     * Bu yöntemle arayüz Aşama 4'teki gerçek API entegrasyonuna hazır olur —
     * sadece veri kaynağı değişecek, renklendirme mantığı aynı kalacak.
     *
     * Dağılım: %30 tamamlandi, %20 devam_ediyor, %15 beklemede, %35 planli
     */
    async getMockProgressData(modelId) {
        const model = this._getModel(modelId);
        if (!model) {
            return { elementMapping: [] };
        }
        try {
            const guids = await model.getGuids();
            const validGuids = guids.filter((g) => g !== null && g !== undefined);
            const durumlar = [
                'tamamlandi', // %30
                'tamamlandi',
                'tamamlandi',
                'devam_ediyor', // %20
                'devam_ediyor',
                'beklemede', // %15
                'planli', // %35
                'planli',
                'planli',
                'planli',
            ];
            // Mock IFC tipleri (gerçekte model'den okunacak)
            const mockTypes = [
                'IfcWall', 'IfcSlab', 'IfcColumn', 'IfcBeam',
                'IfcDoor', 'IfcWindow', 'IfcRoof', 'IfcStair',
            ];
            const mockIsKalemleri = [
                { id: 1001, adi: 'C25/30 Hazır Beton Dökülmesi' },
                { id: 1002, adi: 'Tuğla Duvar Örülmesi' },
                { id: 1003, adi: 'Çelik Kolon Montajı' },
                { id: 1004, adi: 'Kapı Kasası Montajı' },
                { id: 1005, adi: 'Alçı Sıva Uygulaması' },
            ];
            const elementMapping = validGuids.map((guid, index) => {
                const durum = durumlar[index % durumlar.length];
                const ilerlemeYuzdesi = durum === 'tamamlandi' ? 100
                    : durum === 'devam_ediyor' ? Math.floor(25 + (index % 6) * 12)
                        : durum === 'beklemede' ? 0
                            : 0; // planli
                const kalemi = mockIsKalemleri[index % mockIsKalemleri.length];
                return {
                    ifcGlobalId: guid,
                    ifcType: mockTypes[index % mockTypes.length],
                    isKalemiId: kalemi.id,
                    isKalemiAdi: kalemi.adi,
                    durum,
                    ilerlemeYuzdesi,
                };
            });
            return { elementMapping };
        }
        catch (err) {
            console.error('[ProgressColoring] Mock data üretme hatası:', err);
            return { elementMapping: [] };
        }
    }
    // ─── Legend UI ────────────────────────────────────────────────────────────
    /**
     * Viewport'ta legend UI bileşeni oluşturur (eğer yoksa).
     * Legend, aktif renk moduna göre dinamik olarak güncellenir.
     */
    initLegend() {
        if (this._legendEl)
            return;
        const legend = document.createElement('div');
        legend.className = 'bv-color-legend';
        legend.id = 'bv-color-legend';
        legend.setAttribute('role', 'region');
        legend.setAttribute('aria-label', 'Renk modu açıklaması');
        legend.innerHTML = this._buildLegendHTML('original');
        this._viewport.appendChild(legend);
        this._legendEl = legend;
        // Toggle butonu event'i
        legend.querySelector('.bv-legend-toggle')?.addEventListener('click', () => {
            this.toggleLegend();
        });
        // Mod seçici event'leri
        legend.querySelectorAll('[data-color-mode]').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const mode = e.currentTarget.dataset['colorMode'];
                if (mode)
                    void this.setColorMode(mode);
            });
        });
    }
    /**
     * Legend görünürlüğünü açar/kapar.
     */
    toggleLegend() {
        this._legendVisible = !this._legendVisible;
        if (this._legendEl) {
            this._legendEl.classList.toggle('collapsed', !this._legendVisible);
        }
    }
    /**
     * Legend'i DOM'dan kaldırır (model kaldırıldığında).
     */
    disposeLegend() {
        this._legendEl?.remove();
        this._legendEl = null;
    }
    // ─── Mode-Specific Renklendirme ───────────────────────────────────────────
    /**
     * Mock progress data ile progress modu renklendirmesi uygular.
     * Gerçek data olmadığında demo amaçlı kullanılır.
     */
    async _applyMockProgressColors() {
        const mockData = await this.getMockProgressData();
        await this.applyProgressColors(mockData);
    }
    /**
     * IFC element tipine göre renklendirme uygular.
     *
     * `model.getItemsOfCategories([/IfcWall/i])` → { "IfcWall": [localId, ...] }
     */
    async _applyTypeColors() {
        const model = this._model;
        if (!model)
            return;
        try {
            // Her bilinen tip için regex pattern oluştur
            const categories = Object.keys(TYPE_COLORS).map((type) => new RegExp(`^${type}$`, 'i'));
            const categoryMap = await model.getItemsOfCategories(categories);
            for (const [category, localIds] of Object.entries(categoryMap)) {
                if (localIds.length === 0)
                    continue;
                // Normalize kategori adını bul
                const color = this._findTypeColor(category);
                await model.setColor(localIds, color);
            }
            // Bilinen tiplerde olmayan elementleri varsayılan renkte bırak
            await this._fragments.update(true);
            this._updateLegend('type');
        }
        catch (err) {
            console.error('[ProgressColoring] Type renklendirme hatası:', err);
        }
    }
    /**
     * Kat bazlı renklendirme uygular.
     *
     * StoreyManager ile koordineli çalışır — spatial structure üzerinden
     * her katın element listesini alır.
     */
    async _applyStoreyColors() {
        const model = this._model;
        if (!model)
            return;
        try {
            const tree = await model.getSpatialStructure();
            // BFS ile storey'leri bul
            const queue = [tree];
            const storeyNodes = [];
            while (queue.length > 0) {
                const node = queue.shift();
                const cat = (node.category ?? '').toUpperCase();
                if (cat.includes('STOREY'))
                    storeyNodes.push(node);
                if (node.children)
                    queue.push(...node.children);
            }
            // Her kat için renk ata
            for (let i = 0; i < storeyNodes.length; i++) {
                const node = storeyNodes[i];
                const color = STOREY_PALETTE[i % STOREY_PALETTE.length];
                // Storey node'u ve tüm children'ları topla
                const ids = this._collectChildIds(node);
                if (ids.length > 0) {
                    await model.setColor(ids, color);
                }
            }
            await this._fragments.update(true);
            this._updateLegend('storey');
        }
        catch (err) {
            console.error('[ProgressColoring] Storey renklendirme hatası:', err);
        }
    }
    // ─── Yardımcılar ──────────────────────────────────────────────────────────
    /**
     * Aktif modeli döndürür.
     * modelId belirtilmezse ilk yüklü model kullanılır.
     */
    _getModel(modelId) {
        if (modelId) {
            return this._fragments.models.list.get(modelId) ?? null;
        }
        // İlk mevcut modeli al
        const models = this._fragments.models.list;
        for (const [, model] of models) {
            return model;
        }
        return null;
    }
    /**
     * IFC kategori string'inden THREE.Color döndürür.
     * Büyük/küçük harf duyarsız eşleştirme yapar.
     */
    _findTypeColor(category) {
        const lower = category.toLowerCase();
        for (const [type, color] of Object.entries(TYPE_COLORS)) {
            if (lower.includes(type.toLowerCase())) {
                return color;
            }
        }
        return DEFAULT_TYPE_COLOR;
    }
    /**
     * Bir SpatialTreeItem ve tüm çocuklarından localId'leri toplar.
     */
    _collectChildIds(node) {
        const ids = [];
        const queue = [node];
        while (queue.length > 0) {
            const n = queue.shift();
            if (n.localId != null)
                ids.push(n.localId);
            if (n.children)
                queue.push(...n.children);
        }
        return ids;
    }
    /**
     * Legend içeriğini aktif moda göre yeniden oluşturur.
     */
    _updateLegend(mode) {
        if (!this._legendEl)
            return;
        this._legendEl.innerHTML = this._buildLegendHTML(mode);
        // Event'leri yeniden bağla
        this._legendEl.querySelector('.bv-legend-toggle')?.addEventListener('click', () => {
            this.toggleLegend();
        });
        this._legendEl.querySelectorAll('[data-color-mode]').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const m = e.currentTarget.dataset['colorMode'];
                if (m)
                    void this.setColorMode(m);
            });
        });
        // Aktif mod butonunu işaretle
        this._legendEl.querySelectorAll('[data-color-mode]').forEach((btn) => {
            const m = btn.dataset['colorMode'];
            btn.classList.toggle('active', m === mode);
        });
    }
    /**
     * Legend HTML içeriğini oluşturur.
     */
    _buildLegendHTML(mode) {
        const modeLabels = {
            progress: '📊 İlerleme Durumu',
            type: '🏗 IFC Tipi',
            storey: '🏢 Kat',
            original: '🎨 Orijinal',
        };
        let itemsHTML = '';
        switch (mode) {
            case 'progress':
                itemsHTML = `
          ${this._legendItem(PROGRESS_COLORS.planli, 'Planlı')}
          ${this._gradientLegendItem()}
          ${this._legendItem(PROGRESS_COLORS.tamamlandi, 'Tamamlandı')}
          ${this._legendItem(PROGRESS_COLORS.beklemede, 'Beklemede')}
          ${this._legendItem(PROGRESS_COLORS.eslesmemis, 'Eşleşmemiş')}`;
                break;
            case 'type':
                itemsHTML = `
          ${this._legendItem(TYPE_COLORS['IfcWall'], 'Duvar (IfcWall)')}
          ${this._legendItem(TYPE_COLORS['IfcSlab'], 'Döşeme (IfcSlab)')}
          ${this._legendItem(TYPE_COLORS['IfcColumn'], 'Kolon (IfcColumn)')}
          ${this._legendItem(TYPE_COLORS['IfcBeam'], 'Kiriş (IfcBeam)')}
          ${this._legendItem(TYPE_COLORS['IfcDoor'], 'Kapı (IfcDoor)')}
          ${this._legendItem(TYPE_COLORS['IfcWindow'], 'Pencere (IfcWindow)')}
          ${this._legendItem(DEFAULT_TYPE_COLOR, 'Diğer')}`;
                break;
            case 'storey':
                itemsHTML = `
          ${STOREY_PALETTE.slice(0, 5).map((c, i) => this._legendItem(c, `${i + 1}. Kat`)).join('')}
          <div class="bv-legend-note">Her kat farklı renk</div>`;
                break;
            case 'original':
                itemsHTML = `<div class="bv-legend-note">IFC'deki orijinal<br>materyaller aktif</div>`;
                break;
        }
        return `
      <div class="bv-legend-header">
        <span class="bv-legend-title">${modeLabels[mode]}</span>
        <button class="bv-legend-toggle" title="Gizle/Göster" aria-label="Legend'ı gizle/göster">—</button>
      </div>
      <div class="bv-legend-body">
        <div class="bv-legend-items">${itemsHTML}</div>
        <div class="bv-legend-modes" role="group" aria-label="Renk modu seçimi">
          ${this._modeBtn('progress', '📊', 'İlerleme', mode)}
          ${this._modeBtn('type', '🏗', 'Tip', mode)}
          ${this._modeBtn('storey', '🏢', 'Kat', mode)}
          ${this._modeBtn('original', '🎨', 'Orijinal', mode)}
        </div>
      </div>`;
    }
    /** Tek bir legend öğesi (renk kutusu + etiket) */
    _legendItem(color, label) {
        const hex = `#${color.getHexString()}`;
        return `
      <div class="bv-legend-item">
        <span class="bv-legend-swatch" style="background:${hex};" aria-hidden="true"></span>
        <span class="bv-legend-label">${label}</span>
      </div>`;
    }
    /** Devam Ediyor için gradient swatch içeren legend öğesi */
    _gradientLegendItem() {
        const gradient = 'linear-gradient(to right, #F44336, #FF9800, #FFC107, #8BC34A, #4CAF50)';
        return `
      <div class="bv-legend-item">
        <span class="bv-legend-swatch" style="background:${gradient};" aria-hidden="true"></span>
        <span class="bv-legend-label">Devam Ediyor (%0–%99)</span>
      </div>`;
    }
    /** Legend renk modu seçici butonu */
    _modeBtn(mode, icon, label, activeMode) {
        const isActive = mode === activeMode;
        return `
      <button class="bv-mode-btn ${isActive ? 'active' : ''}"
              data-color-mode="${mode}"
              title="${label}"
              aria-pressed="${String(isActive)}"
              aria-label="${label} moduna geç">
        ${icon}
      </button>`;
    }
    // ─── Public Getter'lar ────────────────────────────────────────────────────
    /** Aktif renk modu */
    get colorMode() { return this._colorMode; }
    /** Legend görünür mü? */
    get legendVisible() { return this._legendVisible; }
    /** Aktif model */
    get model() { return this._model; }
    /**
     * Modeli günceller (yeni model yüklendiğinde çağrılır).
     * Renkleri sıfırlar ve yeni model için hazır hale getirir.
     */
    setModel(model) {
        this._model = model;
        this._localIdToStatus.clear();
        this._guidToMapping.clear();
        this._lastProgressData = null;
        this._colorMode = 'original';
        this._totalElements = 0;
        this._updateLegend('original');
    }
    /**
     * ProgressColoring kaynaklarını serbest bırakır.
     */
    dispose() {
        this.disposeLegend();
        this._guidToMapping.clear();
        this._localIdToStatus.clear();
        this._model = null;
        this._lastProgressData = null;
    }
}
//# sourceMappingURL=progressColoring.js.map