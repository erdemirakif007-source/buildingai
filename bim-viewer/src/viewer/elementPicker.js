/**
 * elementPicker.ts
 *
 * 3D sahnede IFC element seçimi ve highlight yönetiminden sorumlu modül.
 *
 * ─── MİMARİ GENEL BAKIŞ ──────────────────────────────────────────────────
 *
 *  Mouse olayı
 *       │
 *       ▼  _onMouseMove() / _onClick()
 *  Normalize fare koordinatları (NDC: -1…+1)
 *       │
 *       ▼  model.raycast({ camera, mouse, dom })  ← Fragments built-in
 *  RaycastResult { localId, fragments (model), point, ... }
 *       │
 *       ├──► Hover  → model.highlight([localId], HOVER_MATERIAL)
 *       └──► Click  → model.highlight([localId], SELECT_MATERIAL)
 *
 *  Element bilgisi:
 *       model.getItemsData([localId], { attributesDefault: true,
 *         relations: { IsDefinedBy: { attributes: true, relations: true } } })
 *       → { Name, Description, GlobalId, ObjectType, Tag, ... PropertySets }
 *
 * ─── NEDEN FRAGMENTS RAYCASTING? ────────────────────────────────────────
 *
 *  @thatopen/fragments, geometriyi tile'lar halinde worker thread'inde tutar.
 *  Three.js Raycaster, sahne grafiğindeki Mesh nesnelerine erişir; ancak
 *  Fragments'ın LOD tile mesh'leri standart Three.js Mesh değildir. Bu yüzden
 *  kütüphanenin kendi model.raycast() metodu kullanılmalıdır — hem doğru çalışır
 *  hem de LOD-aware olduğu için daha performanslıdır.
 *
 * ─── THROTTLE NOTU ───────────────────────────────────────────────────────
 *
 *  mousemove olayı saniyede 200-300 kez tetiklenebilir. Raycasting CPU/GPU
 *  yoğun bir işlemdir. 16 ms throttle (~60 fps) ile gereksiz işlem engellenir.
 *  Throttle, son çağrıdan itibaren minimum 16 ms bekler (leading edge).
 */
import * as THREE from 'three';
// ─── Sabitler ─────────────────────────────────────────────────────────────────
/** Hover highlight rengi: mavi (#4A90D9) */
const HOVER_COLOR = new THREE.Color(0x4a90d9);
/** Seçim highlight rengi: turuncu (#E15A1F) */
const SELECT_COLOR = new THREE.Color(0xe15a1f);
/** Hover opacity */
const HOVER_OPACITY = 0.3;
/** Seçim opacity */
const SELECT_OPACITY = 0.5;
/** Mouse throttle aralığı (ms) — ~60 fps */
const MOUSE_THROTTLE_MS = 16;
/** Hover için MaterialDefinition */
const HOVER_MATERIAL = {
    color: HOVER_COLOR,
    opacity: HOVER_OPACITY,
    transparent: true,
    renderedFaces: 2, // RenderedFaces.TwoSides
};
/** Seçim için MaterialDefinition */
const SELECT_MATERIAL = {
    color: SELECT_COLOR,
    opacity: SELECT_OPACITY,
    transparent: true,
    renderedFaces: 2,
};
// ─── Ana Sınıf ────────────────────────────────────────────────────────────────
/**
 * 3D sahne element seçici.
 *
 * Mouse hareketlerini izler, @thatopen/fragments built-in raycasting ile
 * IFC elementlerini tespit eder, hover/select highlight uygular ve
 * element bilgilerini callback'ler aracılığıyla iletir.
 *
 * KULLANIM:
 * ```ts
 * const picker = new ElementPicker(scene, camera, renderer, fragments);
 *
 * picker.onElementHover = (info) => {
 *   if (info) statusBar.setText(info.name);
 * };
 *
 * picker.onElementSelect = (info) => {
 *   if (info) propertiesPanel.show(info);
 *   else propertiesPanel.hide();
 * };
 *
 * // İşiniz bittiğinde:
 * picker.dispose();
 * ```
 */
export class ElementPicker {
    // ─── Constructor ──────────────────────────────────────────────────────────
    /**
     * @param _scene       - Three.js sahnesi (gelecekte kullanılmak üzere alınır)
     * @param camera       - Perspektif kamera
     * @param renderer     - WebGL renderer
     * @param loadedModels - IFCLoaderEngine.loadedModels ile aynı Map referansı
     */
    constructor(_scene, camera, renderer, loadedModels) {
        // ── Durum ────────────────────────────────────────────────────────────────
        /**
         * true ise tüm mouse event'leri yoksayılır.
         * AutoDimensionTool aktifken BIMViewer tarafından true yapılır.
         */
        this.paused = false;
        /**
         * Şu an hover (fareyle üstünde) durumundaki element.
         * null ise hiçbir element hover'da değil.
         */
        this.highlightedElement = null;
        /**
         * Şu an seçili (tıklanmış) element.
         * null ise hiçbir element seçili değil.
         */
        this.selectedElement = null;
        // ── Callback'ler ─────────────────────────────────────────────────────────
        /**
         * Bir element hover edildiğinde veya hover bırakıldığında çağrılır.
         * element null ise fare boş alana geldi demektir.
         */
        this.onElementHover = () => { };
        /**
         * Bir element seçildiğinde veya seçim temizlendiğinde çağrılır.
         * element null ise seçim temizlendi demektir.
         */
        this.onElementSelect = () => { };
        // ── Throttle ─────────────────────────────────────────────────────────────
        /** Son mousemove işlem zamanı (ms) — throttle için */
        this._lastMoveTime = 0;
        this._camera = camera;
        this._renderer = renderer;
        this._loadedModels = loadedModels;
        this.raycaster = new THREE.Raycaster();
        this.mouse = new THREE.Vector2();
        // Bound referansları oluştur (dispose'da aynı referans gerekli)
        this._onMouseMoveBound = this._onMouseMove.bind(this);
        this._onClickBound = this._onClick.bind(this);
        this._onDblClickBound = this._onDblClick.bind(this);
        this._onKeyDownBound = this._onKeyDown.bind(this);
        // Event listener'ları bağla
        this._attachEvents();
        console.log('[ElementPicker] ✓ Başlatıldı.');
    }
    // ─── Public API ───────────────────────────────────────────────────────────
    /**
     * Belirli bir kattaki tüm element expressId'lerini döndürür.
     *
     * Spatial structure'da IfcBuildingStorey araması yaparak ilgili katı bulur,
     * ardından o katın children element'lerini listeler.
     *
     * @param storeyName - Aranacak kat adı (tam veya kısmi eşleşme)
     * @returns expressId (localId) listesi
     */
    async getElementsByStorey(storeyName) {
        const results = [];
        for (const [, model] of this._loadedModels) {
            try {
                // Spatial structure'dan katları bul
                const spatialTree = await model.getSpatialStructure();
                const storeyNodes = this._findStoreyNodes(spatialTree, storeyName);
                for (const storeyNode of storeyNodes) {
                    if (storeyNode.localId != null) {
                        // Katın children element'lerini al
                        const children = await model.getItemsChildren([storeyNode.localId]);
                        results.push(...children);
                    }
                }
            }
            catch (err) {
                console.warn(`[ElementPicker] getElementsByStorey hatası (${storeyName}):`, err);
            }
        }
        return results;
    }
    /**
     * Belirli tipte tüm elementleri döndürür.
     *
     * @param ifcType - IFC entity tipi: "IfcWall", "IfcColumn", "IfcSlab" vb.
     *                  Büyük/küçük harf duyarsız eşleşme yapılır.
     * @returns expressId (localId) listesi
     */
    async getElementsByType(ifcType) {
        const results = [];
        const pattern = new RegExp(`^${ifcType}$`, 'i');
        for (const [, model] of this._loadedModels) {
            try {
                const byCategory = await model.getItemsOfCategories([pattern]);
                for (const ids of Object.values(byCategory)) {
                    results.push(...ids);
                }
            }
            catch (err) {
                console.warn(`[ElementPicker] getElementsByType hatası (${ifcType}):`, err);
            }
        }
        return results;
    }
    /**
     * Belirli tipte elementlerin bilgilerini toplu olarak getirir.
     * BIMViewer'ın getElementsByType callback'i tarafından kullanılır.
     *
     * @param ifcType - IFC entity tipi (örn. "IfcWall")
     * @returns ElementInfo listesi (bilgisi alınamayan elementler atlanır)
     */
    async getElementInfosByType(ifcType) {
        const localIds = await this.getElementsByType(ifcType);
        const results = [];
        for (const [, model] of this._loadedModels) {
            for (const localId of localIds) {
                const info = await this._fetchElementInfo(model, localId);
                if (info)
                    results.push(info);
            }
        }
        return results;
    }
    /**
     * Seçimi programatik olarak temizler.
     * Hem seçim hem hover highlight'larını sıfırlar.
     */
    async clearSelection() {
        await this._clearHover();
        await this._clearSelect();
        this.onElementSelect(null);
    }
    /**
     * ElementPicker'ı temizler: event listener'ları kaldırır,
     * mevcut highlight'ları sıfırlar.
     */
    async dispose() {
        this._detachEvents();
        // Aktif highlight'ları temizle
        await this._clearHover();
        await this._clearSelect();
        console.log('[ElementPicker] Kaynaklar temizlendi.');
    }
    // ─── Event Yönetimi ───────────────────────────────────────────────────────
    _attachEvents() {
        const canvas = this._renderer.domElement;
        canvas.addEventListener('mousemove', this._onMouseMoveBound);
        canvas.addEventListener('click', this._onClickBound);
        canvas.addEventListener('dblclick', this._onDblClickBound);
        document.addEventListener('keydown', this._onKeyDownBound);
    }
    _detachEvents() {
        const canvas = this._renderer.domElement;
        canvas.removeEventListener('mousemove', this._onMouseMoveBound);
        canvas.removeEventListener('click', this._onClickBound);
        canvas.removeEventListener('dblclick', this._onDblClickBound);
        document.removeEventListener('keydown', this._onKeyDownBound);
    }
    // ─── Mouse Event Handler'ları ─────────────────────────────────────────────
    /**
     * Fare hareketi: throttle uygulanmış hover raycasting.
     * 16 ms (~60 fps) altındaki olayları atlar.
     */
    _onMouseMove(event) {
        if (this.paused)
            return;
        const now = performance.now();
        if (now - this._lastMoveTime < MOUSE_THROTTLE_MS)
            return;
        this._lastMoveTime = now;
        this._updateMouseCoords(event);
        void this._handleHover();
    }
    /**
     * Sol tık: element seçimi.
     * Fare sol tuşu (button 0) ile gerçekleşen tıklamaları işler.
     */
    _onClick(event) {
        if (this.paused)
            return;
        console.log('[ElementPicker] click event fired', {
            button: event.button,
            clientX: event.clientX,
            clientY: event.clientY,
            modelsLoaded: this._loadedModels.size,
        });
        // Yalnızca sol tık
        if (event.button !== 0)
            return;
        this._updateMouseCoords(event);
        void this._handleSelect();
    }
    /**
     * Çift tık: seçili elementin bounding box'ına zoom.
     */
    _onDblClick(event) {
        if (event.button !== 0)
            return;
        void this._handleZoomToSelected();
    }
    /**
     * Escape tuşu: seçimi temizle.
     */
    _onKeyDown(event) {
        if (event.key === 'Escape') {
            void this.clearSelection();
        }
    }
    // ─── Koordinat Güncelleme ─────────────────────────────────────────────────
    /**
     * Fare konumunu canvas'a göre normalize edilmiş koordinatlara (-1…+1) çevirir.
     * Three.js / Fragments raycasting için NDC (Normalized Device Coordinates) gerekir.
     */
    _updateMouseCoords(event) {
        const canvas = this._renderer.domElement;
        const rect = canvas.getBoundingClientRect();
        // Canvas içindeki piksel konumu
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        // NDC: sol=-1, sağ=+1, üst=+1, alt=-1
        this.mouse.x = (x / rect.width) * 2 - 1;
        this.mouse.y = -(y / rect.height) * 2 + 1;
    }
    // ─── Raycasting ───────────────────────────────────────────────────────────
    /**
     * AutoDimensionTool gibi dış araçların doğrudan raycasting yapmasına izin verir.
     * `mouse` verilirse bu koordinatları kullanır; yoksa mevcut `this.mouse`'u kullanır.
     */
    async performRaycast(mouse) {
        if (mouse)
            this.mouse.copy(mouse);
        return this._raycastModels();
    }
    /**
     * Yüklü tüm modeller üzerinde raycasting yaparak en yakın elementi döndürür.
     *
     * @thatopen/fragments, model.raycast({ camera, mouse, dom }) çağrısı ile
     * kendi iç tile yapısı üzerinde raycast yapar — Three.js Raycaster'dan
     * çok daha doğru ve performanslı.
     *
     * @returns { model, localId } veya null (hiçbir element isabet etmedi)
     */
    async _raycastModels() {
        const canvas = this._renderer.domElement;
        // Yüklü model yoksa atla
        if (this._loadedModels.size === 0)
            return null;
        let closestDistance = Infinity;
        let closestResult = null;
        for (const [modelId, model] of this._loadedModels) {
            try {
                const result = await model.raycast({
                    camera: this._camera,
                    mouse: this.mouse,
                    dom: canvas,
                });
                console.debug('[ElementPicker] raycast sonucu', {
                    modelId,
                    result: result ? { localId: result.localId, distance: result.distance } : null,
                });
                if (result === null)
                    continue;
                // En yakın sonucu seç (birden fazla model varsa)
                if (result.distance < closestDistance) {
                    closestDistance = result.distance;
                    closestResult = { model, localId: result.localId };
                }
            }
            catch (err) {
                // Model henüz hazır değilse (tile yükleniyor) sessizce atla
                console.debug('[ElementPicker] Raycast atlandı:', err);
            }
        }
        if (!closestResult) {
            console.debug('[ElementPicker] Hiçbir modelde kesişim bulunamadı. mouse NDC:', this.mouse);
        }
        return closestResult;
    }
    // ─── Hover ────────────────────────────────────────────────────────────────
    /**
     * Hover işlemi: raycast yap, sonuca göre highlight uygula.
     */
    async _handleHover() {
        const hit = await this._raycastModels();
        if (!hit) {
            // Boş alana gelinid — hover temizle
            if (this.highlightedElement !== null) {
                await this._clearHover();
                this.onElementHover(null);
            }
            return;
        }
        const { model, localId } = hit;
        // Zaten aynı element hover'da ise gereksiz işlem yapma
        if (this.highlightedElement?.modelId === model.modelId &&
            this.highlightedElement?.expressId === localId) {
            return;
        }
        // Önceki hover'ı temizle
        await this._clearHover();
        // Seçili element ile aynıysa hover rengi değiştirme (seçim öncelikli)
        if (this.selectedElement?.modelId === model.modelId &&
            this.selectedElement?.expressId === localId) {
            return;
        }
        // Hover highlight uygula
        try {
            await model.highlight([localId], HOVER_MATERIAL);
            this.highlightedElement = { modelId: model.modelId, expressId: localId };
            // Element bilgisini asenkron getir ve callback'i çağır
            const info = await this._fetchElementInfo(model, localId);
            this.onElementHover(info);
        }
        catch (err) {
            console.warn('[ElementPicker] Hover highlight hatası:', err);
        }
    }
    /**
     * Mevcut hover highlight'ı temizler.
     */
    async _clearHover() {
        if (!this.highlightedElement)
            return;
        const { modelId, expressId } = this.highlightedElement;
        const model = this._loadedModels.get(modelId);
        if (model) {
            try {
                await model.resetHighlight([expressId]);
            }
            catch {
                // Model kaldırılmış olabilir — sessizce atla
            }
        }
        this.highlightedElement = null;
    }
    // ─── Seçim ────────────────────────────────────────────────────────────────
    /**
     * Seçim işlemi: raycast yap, seçili elementi highlight et.
     */
    async _handleSelect() {
        const hit = await this._raycastModels();
        if (!hit) {
            // Boş alana tıklandı — seçimi temizle
            await this._clearSelect();
            this.onElementSelect(null);
            return;
        }
        const { model, localId } = hit;
        // Aynı element tekrar tıklandıysa seçimi toggle et
        if (this.selectedElement?.modelId === model.modelId &&
            this.selectedElement?.expressId === localId) {
            await this._clearSelect();
            this.onElementSelect(null);
            return;
        }
        // Önceki seçimi temizle
        await this._clearSelect();
        // Seçim highlight uygula
        try {
            await model.highlight([localId], SELECT_MATERIAL);
            this.selectedElement = { modelId: model.modelId, expressId: localId };
            // Element bilgisini getir ve callback'i çağır
            const info = await this._fetchElementInfo(model, localId);
            this.onElementSelect(info);
        }
        catch (err) {
            console.warn('[ElementPicker] Seçim highlight hatası:', err);
        }
    }
    /**
     * Mevcut seçim highlight'ı temizler.
     */
    async _clearSelect() {
        if (!this.selectedElement)
            return;
        const { modelId, expressId } = this.selectedElement;
        const model = this._loadedModels.get(modelId);
        if (model) {
            try {
                await model.resetHighlight([expressId]);
            }
            catch {
                // Model kaldırılmış olabilir
            }
        }
        this.selectedElement = null;
    }
    // ─── Zoom to Element ──────────────────────────────────────────────────────
    /**
     * Seçili elementin bounding box'ına kamerayı fit eder (zoom).
     * Double click ile tetiklenir.
     */
    async _handleZoomToSelected() {
        // Önce tıklanan elementi bul (double click'te de raycast yap)
        const hit = await this._raycastModels();
        const target = hit ?? (this.selectedElement ? {
            model: this._loadedModels.get(this.selectedElement.modelId),
            localId: this.selectedElement.expressId,
        } : null);
        if (!target || !target.model)
            return;
        try {
            const box = await target.model.getMergedBox([target.localId]);
            if (box.isEmpty() || !isFinite(box.min.x)) {
                console.warn('[ElementPicker] Element bounding box geçersiz.');
                return;
            }
            // Kamerayı bounding box'a fit et
            this._fitCameraToBox(box);
        }
        catch (err) {
            console.warn('[ElementPicker] Zoom to element hatası:', err);
        }
    }
    /**
     * Three.js Box3'e kamerayı fit eder.
     * fitCameraToBox (sceneSetup.ts) bağımlılığı olmadan kendi implementasyonu.
     *
     * @param box - Odaklanılacak bounding box
     */
    _fitCameraToBox(box) {
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const fovRad = THREE.MathUtils.degToRad(this._camera.fov);
        const dist = (maxDim / 2) / Math.tan(fovRad / 2) * 1.8;
        // Near/far dinamik ayarı — küçük elemanlara yakın zoom'da klipleme önlenir
        const dynNear = Math.max(0.001, maxDim * 0.0005);
        this._camera.near = dynNear;
        this._camera.updateProjectionMatrix();
        const dir = new THREE.Vector3(1, 0.8, 1).normalize();
        this._camera.position.copy(center).addScaledVector(dir, dist);
        this._camera.lookAt(center);
        // OrbitControls target güncelleme için custom event yayınla
        // BIMViewer veya harici bir listener bunu dinleyebilir
        this._renderer.domElement.dispatchEvent(new CustomEvent('ep:zoom', { detail: { center, distance: dist }, bubbles: true }));
    }
    // ─── Element Bilgisi ──────────────────────────────────────────────────────
    /**
     * Belirtilen localId için IFC özelliklerini getirir ve ElementInfo'ya dönüştürür.
     *
     * getItemsData() çağrısı:
     *  - attributesDefault: true → Name, GlobalId, ObjectType, Tag, Description
     *  - IsDefinedBy: attributes + relations → PropertySet ve Quantity içerikleri
     *
     * @param model   - Hedef FragmentsModel
     * @param localId - Element'in localId (expressId)
     * @returns ElementInfo veya null (veri alınamadıysa)
     */
    async _fetchElementInfo(model, localId) {
        try {
            const [itemData] = await model.getItemsData([localId], {
                attributesDefault: true,
                relations: {
                    IsDefinedBy: { attributes: true, relations: true },
                    ContainedInStructure: { attributes: true, relations: false },
                    Decomposes: { attributes: true, relations: false },
                },
            });
            if (!itemData)
                return null;
            return this._parseItemData(model.modelId, localId, itemData);
        }
        catch (err) {
            console.warn(`[ElementPicker] Element bilgisi alınamadı (localId: ${localId}):`, err);
            return null;
        }
    }
    /**
     * getItemsData() çıktısını ElementInfo formatına dönüştürür.
     *
     * ItemData yapısı: { [attributeName]: { value, type } | ItemData[] }
     * İlişkiler de ItemData[] biçiminde gelir.
     *
     * @param modelId  - Model kimliği
     * @param localId  - Element'in localId
     * @param itemData - getItemsData() ham çıktısı
     */
    _parseItemData(modelId, localId, itemData) {
        // ── Temel attribute'lar ───────────────────────────────────────────────
        const getAttr = (key) => {
            const entry = itemData[key];
            if (entry && entry.value !== undefined && entry.value !== null) {
                return String(entry.value);
            }
            return '';
        };
        const name = getAttr('Name') || getAttr('LongName') || `Element ${localId}`;
        const globalId = getAttr('GlobalId');
        const ifcType = getAttr('type') || getAttr('ifcType') || 'IfcBuildingElement';
        // ── PropertySet özellikleri ───────────────────────────────────────────
        const properties = {};
        // Temel attribute'ları ekle
        const baseAttrs = ['Description', 'ObjectType', 'Tag', 'PredefinedType'];
        for (const key of baseAttrs) {
            const val = getAttr(key);
            if (val)
                properties[key] = val;
        }
        // IsDefinedBy: PropertySet ve Quantity içeriklerini düzleştir
        const isDefinedBy = itemData['IsDefinedBy'];
        if (Array.isArray(isDefinedBy)) {
            for (const pset of isDefinedBy) {
                this._extractPropertySet(pset, properties);
            }
        }
        // ── Kat bilgisi ───────────────────────────────────────────────────────
        let storey = '';
        const containedIn = itemData['ContainedInStructure'];
        if (Array.isArray(containedIn) && containedIn.length > 0) {
            const storeyData = containedIn[0];
            const storeyName = storeyData['Name']?.value;
            if (storeyName)
                storey = String(storeyName);
        }
        // Decomposes üzerinden de kat arama
        if (!storey) {
            const decomposes = itemData['Decomposes'];
            if (Array.isArray(decomposes) && decomposes.length > 0) {
                const parent = decomposes[0];
                const parentName = parent['Name']?.value;
                if (parentName)
                    storey = String(parentName);
            }
        }
        return {
            modelId,
            expressId: localId,
            ifcType,
            name,
            globalId,
            properties,
            storey,
        };
    }
    /**
     * PropertySet (IfcPropertySet / IfcElementQuantity) içeriğini properties'e ekler.
     *
     * İlgili IFC ilişki yapısı:
     *   IfcRelDefinesByProperties.RelatingPropertyDefinition
     *     → IfcPropertySet.HasProperties[*]
     *         → IfcPropertySingleValue { Name, NominalValue }
     *
     * @param psetRelation - IsDefinedBy altındaki bir ilişki nesnesi
     * @param target       - Özelliklerin yazılacağı hedef map
     */
    _extractPropertySet(psetRelation, target) {
        // RelatingPropertyDefinition → PropertySet
        const relDef = psetRelation['RelatingPropertyDefinition'];
        if (!relDef || typeof relDef !== 'object')
            return;
        const psetData = relDef;
        const psetName = psetData['Name']?.value ?? '';
        // HasProperties: IfcPropertySingleValue listesi
        const hasProps = psetData['HasProperties'];
        if (Array.isArray(hasProps)) {
            for (const prop of hasProps) {
                const propData = prop;
                const propName = propData['Name']?.value;
                const nomVal = propData['NominalValue'];
                const nomValData = nomVal;
                const propValue = nomValData?.['value'];
                if (propName && propValue !== undefined && propValue !== null) {
                    const key = psetName ? `${psetName}.${propName}` : String(propName);
                    target[key] = String(propValue);
                }
            }
        }
        // Quantities (IfcElementQuantity): HasQuantities
        const hasQuantities = psetData['Quantities'];
        if (Array.isArray(hasQuantities)) {
            for (const qty of hasQuantities) {
                const qtyData = qty;
                const qtyName = qtyData['Name']?.value;
                // IfcQuantityArea, IfcQuantityVolume, IfcQuantityLength vb.
                const qtyValue = qtyData['AreaValue']?.value ??
                    qtyData['VolumeValue']?.value ??
                    qtyData['LengthValue']?.value ??
                    qtyData['WeightValue']?.value ??
                    qtyData['CountValue']?.value;
                if (qtyName && qtyValue !== undefined && qtyValue !== null) {
                    const key = psetName ? `${psetName}.${qtyName}` : String(qtyName);
                    target[key] = String(qtyValue);
                }
            }
        }
    }
    // ─── Yardımcı Metodlar ────────────────────────────────────────────────────
    /**
     * Spatial tree'de belirli bir kat adıyla eşleşen düğümleri bulur (BFS).
     *
     * @param root        - Ağacın kökü (IfcProject veya IfcSite vb.)
     * @param storeyName  - Aranan kat adı (kısmi eşleşme)
     * @returns Eşleşen IfcBuildingStorey düğümleri
     */
    _findStoreyNodes(root, storeyName) {
        const results = [];
        const queue = [root];
        const lowerSearch = storeyName.toLowerCase();
        while (queue.length > 0) {
            const node = queue.shift();
            const nodeName = node.category?.toLowerCase() ?? '';
            if (nodeName.includes(lowerSearch)) {
                results.push(node);
            }
            if (Array.isArray(node.children)) {
                for (const child of node.children) {
                    queue.push(child);
                }
            }
        }
        return results;
    }
}
//# sourceMappingURL=elementPicker.js.map