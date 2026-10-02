/**
 * ifcLoader.ts
 *
 * IFC (Industry Foundation Classes) dosyalarının tarayıcıda yüklenmesi,
 * 3D sahneye eklenmesi ve yönetilmesinden sorumlu modül.
 *
 * ─── MİMARİ GENEL BAKIŞ ──────────────────────────────────────────────────
 *
 *  IFC Dosyası (.ifc)
 *       │
 *       ▼  IfcImporter.process()   [Ana thread — CPU yoğun, WASM]
 *  Fragment Bytes (Uint8Array)
 *       │
 *       ▼  FragmentsModels.load()  [Worker thread — veri işleme]
 *  FragmentsModel             ────► THREE.Object3D (scene'e eklenir)
 *       │                               │
 *       ▼                               ▼
 *  .box (THREE.Box3)         Camera fit-to-box
 *
 * ─── IFC → FRAGMENT DÖNÜŞÜMÜ ─────────────────────────────────────────────
 *
 *  IFC formatı STEP/EXPRESS tabanlı metin formatıdır (insan okunabilir ama
 *  parse etmesi ağır). @thatopen/fragments bu veriyi ikili FlatBuffer
 *  formatına dönüştürür:
 *
 *  - Geometri: Triangle mesh → FlatBuffer binary (GPU-hazır)
 *  - Özellikler: IFC attribute/relation → FlatBuffer tablo
 *  - Hiyerarşi: IfcProject → IfcSite → IfcBuilding → IfcStorey → ...
 *
 *  Avantajlar:
 *  - 10× daha hızlı yükleme (.frag cache kullanıldığında)
 *  - Web Worker'da işleme (UI thread'i bloklamaz)
 *  - LOD (Level of Detail) — uzak elemanlar daha düşük çözünürlükte
 *
 * ─── WASM NOTU ────────────────────────────────────────────────────────────
 *
 *  IfcImporter, IFC geometrisini parse etmek için web-ifc'in WebAssembly
 *  modülünü kullanır. WASM dosyaları public/ klasöründe bulunmalıdır:
 *    - public/web-ifc.wasm        (single-thread)
 *    - public/web-ifc-mt.wasm     (multi-thread, SharedArrayBuffer gerektirir)
 *
 *  Multi-thread kullanmak için sunucu COOP/COEP HTTP başlıkları
 *  göndermelidir (vite.config.ts'de ayarlanmış).
 *
 * ─── GELECEKTEKİ GELİŞTİRMELER ──────────────────────────────────────────
 *  - IndexedDB .frag önbellekleme (aynı dosyayı tekrar parse etme)
 *  - IFC entity filtreleme (yalnızca IfcWall, IfcSlab yükle)
 *  - Clipping plane entegrasyonu (FragmentsModel.getClippingPlanesEvent)
 *  - Raycasting ile eleman seçimi (FragmentsModel.raycast)
 *  - Spatial structure tree (sidebar için getSpatialStructure)
 */
import * as THREE from 'three';
import { FragmentsModels, IfcImporter, } from '@thatopen/fragments';
import * as WEBIFC from 'web-ifc';
import { fitCameraToBox } from './sceneSetup';
// web-ifc-mt.wasm'ın pthread worker URL sorunu nedeniyle Init() asla resolve olmuyor.
// IfcGeometryProcessor.load() içindeki this._ifcAPI.Init() çağrısı
// forceSingleThread argümanını destekliyor — prototype'ı patch'leyerek ST modunu zorla.
// Sonuç: pthread worker oluşturulmaz, WASM direkt ana thread'de tek-iş-parçacıklı çalışır.
WEBIFC.IfcAPI.prototype._initOrig
    = WEBIFC.IfcAPI.prototype.Init;
WEBIFC.IfcAPI.prototype.Init = function (locateFile) {
    const self = this;
    return self._initOrig.call(this, locateFile, /* forceSingleThread= */ true);
};
// ─── Ana Sınıf ─────────────────────────────────────────────────────────────────
/**
 * IFC ve Fragment dosyalarını yönetmekten sorumlu ana motor sınıfı.
 *
 * KULLANIM ÖRNEĞİ:
 * ```ts
 * const engine = new IFCLoaderEngine(scene, camera, controls);
 * await engine.init();
 *
 * engine.onProgress = (p, msg) => console.log(`${Math.round(p * 100)}% - ${msg}`);
 * engine.onModelLoaded = (id) => console.log(`Model yüklendi: ${id}`);
 *
 * const file = inputEl.files[0]; // <input type="file" accept=".ifc">
 * await engine.loadIFC(file);
 * ```
 */
export class IFCLoaderEngine {
    // ─── Constructor ─────────────────────────────────────────────────────────
    /**
     * @param scene    - Three.js sahnesi (yüklenen modeller buraya eklenir)
     * @param camera   - Perspektif kamera (LOD hesabı ve camera fit için)
     * @param controls - OrbitControls (camera fit sonrası target güncelleme)
     */
    constructor(scene, camera, controls) {
        // ── @thatopen/fragments ──────────────────────────────────────────────────
        /**
         * FragmentsModels ana orkestratörü.
         * init() çağrısına kadar null; init() sonrasında dolu.
         */
        this._fragments = null;
        // ── Model Durumu ─────────────────────────────────────────────────────────
        /**
         * Yüklü modellerin haritası.
         * key: modelId (dosya adı tabanlı, benzersiz)
         * value: FragmentsModel referansı
         */
        this.loadedModels = new Map();
        /** Şu an yükleme/işlem yapılıp yapılmadığı */
        this.isLoading = false;
        // ── Callback'ler ─────────────────────────────────────────────────────────
        /**
         * Yükleme ilerlemesi callback'i.
         * Null ise ilerleme bildirimi yapılmaz.
         * UI tarafından setStatusbar vb. için kullanılır.
         */
        this.onProgress = null;
        /**
         * Model başarıyla yüklendiğinde çağrılır.
         * Null ise callback yapılmaz.
         * Sidebar model ağacını doldurmak için kullanılır.
         */
        this.onModelLoaded = null;
        /**
         * Hata oluştuğunda çağrılır.
         * Null ise hata yalnızca console'a yazılır.
         */
        this.onError = null;
        // ── Dispose Durumu ───────────────────────────────────────────────────────
        /** dispose() çağrısından sonra true olur — tekrar kullanımı önler */
        this._isDisposed = false;
        this._scene = scene;
        this._camera = camera;
        this._controls = controls;
    }
    // ─── Başlatma ─────────────────────────────────────────────────────────────
    /**
     * FragmentsModels'ı başlatır. loadIFC() çağrısından önce çağrılmalıdır.
     *
     * NEDEN AYRI BİR INIT() METODU?
     * FragmentsModels.getWorker() ağ üzerinden worker script'i indirir
     * (versiona özel, unpkg CDN'den). Bu async işlem constructor'da
     * yapılamaz — bu yüzden init() metodu gerekli.
     *
     * WORKER URL SEÇENEKLERİ:
     * 1. getWorker() (önerilen): Kütüphane versiyonuna eşleşen worker'ı CDN'den indirir.
     * 2. Yerel worker: Build pipeline'a entegrasyon gerektirir, karmaşık.
     *
     * @throws {Error} Worker yüklenemezse veya FragmentsModels başlatılamazsa
     */
    async init() {
        if (this._isDisposed) {
            throw new Error('[IFCLoaderEngine] Dispose edilmiş engine tekrar kullanılamaz.');
        }
        if (this._fragments) {
            console.warn('[IFCLoaderEngine] Engine zaten başlatılmış.');
            return;
        }
        try {
            console.log('[IFCLoaderEngine] FragmentsModels başlatılıyor...');
            this._reportProgress(0.01, 'Fragment engine başlatılıyor...');
            // Worker URL'ini CDN'den al (kütüphane versiyonu ile eşleşir)
            // Bu çağrı ağ isteği yapar — offline modda hata verebilir
            const workerUrl = await FragmentsModels.getWorker();
            // FragmentsModels instance'ı oluştur
            // Worker thread'ini başlatır (geometry ve data thread'leri)
            this._fragments = new FragmentsModels(workerUrl);
            // ── Model Yükleme Event'i ─────────────────────────────────────────
            // FragmentsModels.load() çağrısından SONRA model list'e eklenir.
            // Bu event model hazır olduğunda tetiklenir:
            //  1. Camera bağlamasını yap (LOD için zorunlu)
            //  2. Object3D'yi sahneye ekle
            //  3. Render döngüsünü başlat (fragments.update)
            this._fragments.models.list.onItemSet.add(({ value: model }) => {
                // LOD (Level of Detail) sistemi için kamerayı bağla.
                // Camera'nın bakış yönüne göre uzak objeler daha düşük
                // çözünürlükte render edilir (performans optimizasyonu).
                model.useCamera(this._camera);
                // Model'in Three.js Object3D'sini sahneye ekle
                this._scene.add(model.object);
                // İlk tile'ları render etmek için güncellemeyi tetikle
                void this._fragments.update(true);
                console.log(`[IFCLoaderEngine] Model sahneye eklendi: ${model.modelId}`);
            });
            // ── Z-Fighting Önleme ─────────────────────────────────────────────
            // BIM modellerinde binlerce yüzey aynı düzlemde çakışabilir
            // (örn. döşeme + kaplama katmanı). Bu durum "z-fighting" denilen
            // titreşen piksel artefaktlarına yol açar.
            //
            // Çözüm: Her materyal için rastgele polygonOffset değeri atar.
            // Bu, GPU'nun derinlik testi sırasında çakışan yüzeyleri
            // farklı derinlikte değerlendirmesini sağlar.
            //
            // NOT: isLodMaterial kontrolü önemli — LOD materyalleri (uzak
            // mesh'ler için özel shader) farklı davranış sergiler; bunlara
            // polygonOffset uygulamak görsel bozukluklara yol açar.
            this._fragments.models.materials.list.onItemSet.add(({ value: material }) => {
                const bimMaterial = material;
                const isLod = 'isLodMaterial' in bimMaterial && bimMaterial.isLodMaterial;
                if (!isLod) {
                    const mat = material;
                    mat.polygonOffset = true;
                    mat.polygonOffsetUnits = 1;
                    // Rastgele factor: Farklı materyaller birbiriyle çakışmaz
                    mat.polygonOffsetFactor = Math.random();
                }
            });
            console.log('[IFCLoaderEngine] ✓ FragmentsModels başarıyla başlatıldı.');
            this._reportProgress(0.05, 'Engine hazır.');
        }
        catch (err) {
            const error = this._normalizeError(err, 'FragmentsModels başlatma hatası');
            this._handleError(error);
            throw error;
        }
    }
    // ─── IFC Yükleme ──────────────────────────────────────────────────────────
    /**
     * IFC dosyasını yükler, Fragment'e dönüştürür ve sahneye ekler.
     *
     * İŞLEM ADIMLARI:
     * 1. Dosyayı ArrayBuffer olarak oku
     * 2. IfcImporter ile IFC → Uint8Array (Fragment binary) dönüşümü yap
     *    (Bu adım CPU yoğun — WASM kullanır; büyük dosyalarda 10-30 saniye sürer)
     * 3. FragmentsModels.load() ile Fragment'i Worker thread'ine yükle
     * 4. Model sahneye eklenir (onItemSet event'i tetiklenir)
     * 5. Kamerayı modele fit et
     * 6. onModelLoaded callback'i çağır
     *
     * @param file - <input type="file"> veya drag-drop'tan gelen IFC dosyası
     * @returns Yüklenen modelin bilgileri (modelId, model, boundingBox)
     * @throws {Error} WASM bulunamazsa, geçersiz IFC formatıysa veya bellek yetersizse
     */
    async loadIFC(file) {
        this._assertReady();
        const modelId = this._fileNameToModelId(file.name);
        // Aynı model zaten yüklüyse uyar
        if (this.loadedModels.has(modelId)) {
            console.warn(`[IFCLoaderEngine] Model zaten yüklü: ${modelId}. Önce unloadModel() çağırın.`);
            throw new Error(`Model zaten yüklü: ${modelId}`);
        }
        this.isLoading = true;
        console.log(`[IFCLoaderEngine] IFC yükleniyor: ${file.name} (${this._formatBytes(file.size)})`);
        try {
            // ── Adım 1: Dosyayı oku ────────────────────────────────────────────
            this._reportProgress(0.05, `Dosya okunuyor: ${file.name}...`);
            const buffer = await this._readFileAsArrayBuffer(file);
            // ── Adım 2: IFC → Fragment dönüşümü ──────────────────────────────
            // IfcImporter, web-ifc WASM ile IFC'yi parse eder ve
            // @thatopen/fragments FlatBuffer formatına dönüştürür.
            // Bu adım en yoğun adım — büyük modellerde dakikalar alabilir.
            const fragmentBytes = await this._convertIFCToFragment(buffer, file.name);
            // ── Adım 3: Fragment'i yükle ──────────────────────────────────────
            this._reportProgress(0.85, 'Model Worker\'a yükleniyor...');
            const model = await this._loadFragmentBytes(fragmentBytes, modelId);
            // ── Adım 4: Bounding box ve camera fit ────────────────────────────
            const boundingBox = await this._fitCameraToModel(model);
            // ── Adım 5: Map'e ekle ────────────────────────────────────────────
            this.loadedModels.set(modelId, model);
            this._reportProgress(1.0, `✓ ${file.name} yüklendi`);
            this.onModelLoaded?.(modelId, model);
            console.log(`[IFCLoaderEngine] ✓ IFC yüklendi: ${modelId}`);
            return { modelId, model, boundingBox };
        }
        catch (err) {
            const error = this._normalizeIFCError(err, file);
            this._handleError(error);
            throw error;
        }
        finally {
            this.isLoading = false;
        }
    }
    // ─── Fragment Yükleme (Önbellek) ──────────────────────────────────────────
    /**
     * Daha önce dönüştürülmüş .frag dosyasını yükler.
     *
     * Bu metod IFC parse adımını ATLAR — bu nedenle 10× daha hızlıdır.
     * Tipik kullanım:
     *  1. loadIFC() ile IFC yükle
     *  2. exportFragment() ile .frag dosyasını kaydet (backend'e gönder)
     *  3. Sonraki açılışta loadFragment() ile direkt yükle (parse yok!)
     *
     * @param buffer  - .frag dosyasının ArrayBuffer içeriği
     * @param modelId - Modele atanacak benzersiz kimlik
     * @returns Yüklenen modelin bilgileri
     * @throws {Error} Buffer geçersizse veya model ID çakışıyorsa
     */
    async loadFragment(buffer, modelId) {
        this._assertReady();
        if (this.loadedModels.has(modelId)) {
            throw new Error(`Model zaten yüklü: ${modelId}`);
        }
        this.isLoading = true;
        console.log(`[IFCLoaderEngine] Fragment yükleniyor: ${modelId} (${this._formatBytes(buffer.byteLength)})`);
        try {
            this._reportProgress(0.1, `Fragment yükleniyor: ${modelId}...`);
            const fragmentBytes = new Uint8Array(buffer);
            const model = await this._loadFragmentBytes(fragmentBytes, modelId);
            const boundingBox = await this._fitCameraToModel(model);
            this.loadedModels.set(modelId, model);
            this._reportProgress(1.0, `✓ ${modelId} yüklendi`);
            this.onModelLoaded?.(modelId, model);
            console.log(`[IFCLoaderEngine] ✓ Fragment yüklendi: ${modelId}`);
            return { modelId, model, boundingBox };
        }
        catch (err) {
            const error = this._normalizeError(err, `Fragment yükleme hatası: ${modelId}`);
            this._handleError(error);
            throw error;
        }
        finally {
            this.isLoading = false;
        }
    }
    // ─── Fragment Dışa Aktarma ────────────────────────────────────────────────
    /**
     * Yüklü modeli .frag formatında dışa aktarır.
     *
     * .frag formatı, IFC'nin işlenmiş ikili versiyonudur.
     * Backend'e gönderilip veritabanında saklanabilir.
     * Bir sonraki açılışta loadFragment() ile 10× daha hızlı yüklenir.
     *
     * @param modelId - Dışa aktarılacak modelin kimliği
     * @returns Sıkıştırılmış fragment verisi (backend'e POST için hazır)
     * @throws {Error} Model bulunamazsa
     */
    async exportFragment(modelId) {
        const model = this._getLoadedModel(modelId);
        try {
            console.log(`[IFCLoaderEngine] Fragment dışa aktarılıyor: ${modelId}`);
            // raw: false → LZ4 sıkıştırması (daha küçük dosya boyutu)
            // raw: true  → Sıkıştırmasız (daha hızlı okuma, büyük dosya)
            const buffer = await model.getBuffer(false);
            console.log(`[IFCLoaderEngine] ✓ Fragment dışa aktarıldı: ${this._formatBytes(buffer.byteLength)}`);
            return buffer;
        }
        catch (err) {
            const error = this._normalizeError(err, `Fragment dışa aktarma hatası: ${modelId}`);
            this._handleError(error);
            throw error;
        }
    }
    // ─── Model Kaldırma ───────────────────────────────────────────────────────
    /**
     * Belirtilen modeli sahneden kaldırır ve bellekten temizler.
     *
     * KAYNAK TEMİZLEME SIRASI:
     * 1. fragments.disposeModel() → Worker'daki veriyi temizle
     *    (Object3D otomatik olarak sahne.remove() edilir)
     * 2. loadedModels Map'inden kaldır
     *
     * @param modelId - Kaldırılacak modelin kimliği
     */
    async unloadModel(modelId) {
        if (!this.loadedModels.has(modelId)) {
            console.warn(`[IFCLoaderEngine] Kaldırılacak model bulunamadı: ${modelId}`);
            return;
        }
        try {
            console.log(`[IFCLoaderEngine] Model kaldırılıyor: ${modelId}`);
            // FragmentsModels.disposeModel():
            //  - Worker thread'indeki veriyi serbest bırakır
            //  - Three.js Object3D'yi sahne grafiğinden kaldırır
            //  - GPU belleğindeki geometri ve materyalleri temizler
            await this._fragments.disposeModel(modelId);
            this.loadedModels.delete(modelId);
            console.log(`[IFCLoaderEngine] ✓ Model kaldırıldı: ${modelId}`);
        }
        catch (err) {
            const error = this._normalizeError(err, `Model kaldırma hatası: ${modelId}`);
            this._handleError(error);
            throw error;
        }
    }
    /**
     * Tüm yüklü modelleri sahneden kaldırır ve bellekten temizler.
     * Yeni bir IFC dosyası yüklemeden önce çağrılabilir.
     */
    async unloadAll() {
        const modelIds = [...this.loadedModels.keys()];
        if (modelIds.length === 0) {
            console.log('[IFCLoaderEngine] Kaldırılacak model yok.');
            return;
        }
        console.log(`[IFCLoaderEngine] ${modelIds.length} model kaldırılıyor...`);
        // Sıralı kaldır (Promise.all yerine sıralı — worker stabilitesi için)
        for (const modelId of modelIds) {
            await this.unloadModel(modelId);
        }
        console.log('[IFCLoaderEngine] ✓ Tüm modeller kaldırıldı.');
    }
    // ─── Dispose ──────────────────────────────────────────────────────────────
    /**
     * Engine'i ve tüm kaynakları temizler.
     *
     * Bu metod çağrıldıktan sonra engine kullanılamaz.
     * BIMViewer.dispose() tarafından çağrılır.
     *
     * KAYNAK TEMİZLEME SIRASI:
     * 1. Tüm modelleri kaldır (worker veri + GPU belleği)
     * 2. FragmentsModels.dispose() (worker thread'lerini sonlandır)
     * 3. Referansları null'a al
     */
    async dispose() {
        if (this._isDisposed) {
            return;
        }
        console.log('[IFCLoaderEngine] Engine kaynakları serbest bırakılıyor...');
        this._isDisposed = true;
        try {
            if (this._fragments) {
                // Tüm modelleri ve worker'ları temizle
                await this._fragments.dispose();
                this._fragments = null;
            }
            this.loadedModels.clear();
            console.log('[IFCLoaderEngine] ✓ Engine temizlendi.');
        }
        catch (err) {
            // Dispose sırasındaki hatalar yutulur — zaten temizleniyoruz
            console.error('[IFCLoaderEngine] Dispose sırasında hata:', err);
        }
    }
    // ─── Özel Yardımcı Metodlar ───────────────────────────────────────────────
    /**
     * Engine'in kullanıma hazır olduğunu doğrular.
     * init() çağrılmamışsa veya dispose edilmişse hata fırlatır.
     */
    _assertReady() {
        if (this._isDisposed) {
            throw new Error('[IFCLoaderEngine] Engine dispose edilmiş. Yeni bir instance oluşturun.');
        }
        if (!this._fragments) {
            throw new Error('[IFCLoaderEngine] Engine henüz başlatılmamış. Önce init() çağırın.');
        }
    }
    /**
     * Dosya adından benzersiz model ID'si üretir.
     * Boşluk ve özel karakterleri temizler.
     *
     * @example
     * 'My Building.ifc' → 'my_building'
     * 'Proje v2.1.IFC'  → 'proje_v2_1'
     */
    _fileNameToModelId(fileName) {
        return fileName
            .replace(/\.(ifc|IFC)$/, '') // Uzantıyı kaldır
            .replace(/[^a-zA-Z0-9_\-\.]/g, '_') // Özel karakterleri _ ile değiştir
            .replace(/_+/g, '_') // Çoklu _ → tek _
            .replace(/^_|_$/g, '') // Baş/son _ kaldır
            .toLowerCase()
            .substring(0, 100); // Max 100 karakter
    }
    /**
     * File'ı ArrayBuffer olarak okur.
     * FileReader API'sini Promise wrapper ile kullanır.
     *
     * @throws {Error} Dosya okunamazsa (izin hatası, bozuk dosya vb.)
     */
    _readFileAsArrayBuffer(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (event) => {
                if (event.target?.result instanceof ArrayBuffer) {
                    resolve(event.target.result);
                }
                else {
                    reject(new Error('Dosya ArrayBuffer olarak okunamadı.'));
                }
            };
            reader.onerror = () => {
                reject(new Error(`Dosya okuma hatası: ${reader.error?.message ?? 'Bilinmeyen hata'}`));
            };
            reader.readAsArrayBuffer(file);
        });
    }
    /**
     * IFC verilerini @thatopen/fragments binary formatına dönüştürür.
     *
     * Bu metod CPU yoğundur — web-ifc WASM modülünü kullanarak IFC
     * entity'lerini parse eder ve Triangle mesh'lere dönüştürür.
     *
     * WASM PATH NOTU:
     * `absolute: true` ile `path: window.location.origin + '/'` kombinasyonu
     * Vite dev server'ın public/ klasörünü işaret eder.
     * Pthread worker URL sorunu vite.config.ts'deki fixWebIfcPthreadUrl plugin'i ile çözülmüştür.
     *
     * @param buffer   - IFC dosyasının ham binary verisi
     * @param fileName - İlerleme mesajlarında kullanılan dosya adı
     * @returns Fragment binary verisi (FragmentsModels.load() için hazır)
     */
    async _convertIFCToFragment(buffer, fileName) {
        this._reportProgress(0.1, `${fileName} parse ediliyor...`);
        const importer = new IfcImporter();
        // WASM dosyasının konumunu belirt.
        // absolute: true → path tam URL olarak kullanılır (relative değil)
        // import.meta.env.BASE_URL: Vite'ın base path'i (/bim-viewer/ veya / gibi)
        importer.wasm = {
            absolute: true,
            path: window.location.origin + import.meta.env.BASE_URL,
        };
        let fragmentBytes;
        try {
            fragmentBytes = await importer.process({
                bytes: new Uint8Array(buffer),
                // İlerleme callback'i — parse aşamalarını bildirir
                progressCallback: (progress, data) => {
                    // ProgressData.process: 'geometries' | 'attributes' | 'relations' | 'conversion'
                    // ProgressData.state:   'start' | 'inProgress' | 'finish'
                    // İlerleme aralığını 0.1-0.8 arasına normalize et
                    // (0.0-0.1 dosya okuma, 0.8-1.0 fragment yükleme için ayrıldı)
                    const normalizedProgress = 0.1 + progress * 0.7;
                    const phaseMessages = {
                        geometries: 'Geometriler işleniyor...',
                        attributes: 'Özellikler okunuyor...',
                        relations: 'İlişkiler çözümleniyor...',
                        conversion: 'Format dönüştürülüyor...',
                    };
                    const message = phaseMessages[data.process] ?? 'İşleniyor...';
                    const entityInfo = data.entitiesProcessed
                        ? ` (${data.entitiesProcessed.toLocaleString('tr-TR')} eleman)`
                        : '';
                    this._reportProgress(normalizedProgress, `${message}${entityInfo}`);
                },
            });
        }
        catch (error) {
            throw error;
        }
        this._reportProgress(0.82, 'Parse tamamlandı, yükleniyor...');
        return fragmentBytes;
    }
    /**
     * Fragment byte verisini FragmentsModels'a yükler.
     * Worker thread'inde işlenir — UI thread'i bloklanmaz.
     *
     * @param fragmentBytes - IfcImporter.process() veya .frag dosyasından gelen veri
     * @param modelId       - Modele atanacak benzersiz ID
     * @returns Yüklenen FragmentsModel referansı
     */
    async _loadFragmentBytes(fragmentBytes, modelId) {
        const model = await this._fragments.load(fragmentBytes, {
            modelId,
            // Camera'yı load sırasında da verebiliriz (LOD için)
            // Ancak onItemSet event'inde de bağlanıyor — bu opsiyonel
            camera: this._camera,
        });
        return model;
    }
    /**
     * Model yüklendikten sonra bounding box'ı hesaplar ve
     * kamerayı modele fit eder.
     *
     * FragmentsModel.box: Three.js Box3 — model'in world-space bounding box'ı.
     * Boş model için Box3 sonsuz değerler içerebilir — bunu kontrol et.
     *
     * @param model - Kameraın fit edileceği FragmentsModel
     * @returns Hesaplanan bounding box (later camera fit için)
     */
    async _fitCameraToModel(model) {
        // Fragment model yüklenince box otomatik hesaplanır
        // Küçük bir gecikme: tile'ların initialize olması için
        await this._fragments.update(true);
        const box = model.box;
        // Box geçerli mi kontrol et (boş veya sonsuz değerlere sahip olabilir)
        if (box.isEmpty() || !isFinite(box.min.x) || !isFinite(box.max.x)) {
            console.warn(`[IFCLoaderEngine] Model bounding box geçersiz: ${model.modelId}`);
            // Varsayılan konum kullan
            return new THREE.Box3(new THREE.Vector3(-10, 0, -10), new THREE.Vector3(10, 10, 10));
        }
        // Camera'yı modele fit et (sceneSetup.ts'deki yardımcı fonksiyon)
        fitCameraToBox(this._camera, this._controls, box);
        console.log(`[IFCLoaderEngine] Kamera modele fit edildi. ` +
            `Boyut: ${box.getSize(new THREE.Vector3()).toArray().map(v => v.toFixed(1)).join(' × ')} m`);
        return box;
    }
    /**
     * Yüklü model referansını döner.
     * Model bulunamazsa hata fırlatır.
     */
    _getLoadedModel(modelId) {
        const model = this.loadedModels.get(modelId);
        if (!model) {
            throw new Error(`[IFCLoaderEngine] Model bulunamadı: ${modelId}. Önce loadIFC() çağırın.`);
        }
        return model;
    }
    /**
     * İlerleme callback'ini güvenle çağırır.
     * Callback yoksa veya hata fırlatırsa sessizce devam eder.
     */
    _reportProgress(progress, message) {
        try {
            this.onProgress?.(progress, message);
        }
        catch {
            // Callback'teki hatalar yükleme işlemini durdurmamalı
        }
    }
    /**
     * Hata callback'ini çağırır ve console'a yazar.
     */
    _handleError(error) {
        console.error('[IFCLoaderEngine] Hata:', error);
        try {
            this.onError?.(error);
        }
        catch {
            // Callback'teki hatalar yutulur
        }
    }
    /**
     * IFC'ye özgü hata mesajları üretir.
     * WASM, bellek ve format hatalarını tanımlayarak Türkçe mesaj döner.
     *
     * @param err      - Yakalanan hata (tip belirsiz)
     * @param file     - Hata oluşan IFC dosyası
     * @returns Kullanıcı dostu hata mesajı ile Error nesnesi
     */
    _normalizeIFCError(err, file) {
        const originalMessage = err instanceof Error ? err.message : String(err);
        const lowerMsg = originalMessage.toLowerCase();
        // WASM dosyası bulunamadı
        if (lowerMsg.includes('wasm') || lowerMsg.includes('fetch') || lowerMsg.includes('network')) {
            return new Error(`web-ifc.wasm dosyası bulunamadı. Lütfen public/ dizinini kontrol edin.\n` +
                `(Orijinal hata: ${originalMessage})`);
        }
        // Geçersiz IFC formatı
        if (lowerMsg.includes('ifc') && (lowerMsg.includes('invalid') || lowerMsg.includes('parse') || lowerMsg.includes('format'))) {
            return new Error(`"${file.name}" dosyası geçerli bir IFC dosyası değil.\n` +
                `IFC2X3, IFC4 veya IFC4X3 formatları desteklenir.\n` +
                `(Orijinal hata: ${originalMessage})`);
        }
        // Bellek yetersizliği
        if (lowerMsg.includes('memory') || lowerMsg.includes('oom') || lowerMsg.includes('out of memory') || lowerMsg.includes('allocation')) {
            const fileMB = Math.round(file.size / 1024 / 1024);
            return new Error(`Model çok büyük, tarayıcı belleği yetersiz (${fileMB} MB).\n` +
                `Daha küçük bir IFC dosyası deneyin veya IFC'yi bölün.\n` +
                `(Orijinal hata: ${originalMessage})`);
        }
        // Genel hata
        return new Error(`IFC yükleme hatası: "${file.name}"\n${originalMessage}`);
    }
    /**
     * Genel hataları normalize eder (unknown → Error).
     */
    _normalizeError(err, context) {
        if (err instanceof Error) {
            return new Error(`${context}: ${err.message}`);
        }
        return new Error(`${context}: ${String(err)}`);
    }
    /**
     * Byte değerini insan okunabilir formata çevirir.
     * @example 1536000 → '1.5 MB'
     */
    _formatBytes(bytes) {
        if (bytes < 1024)
            return `${bytes} B`;
        if (bytes < 1024 * 1024)
            return `${(bytes / 1024).toFixed(1)} KB`;
        if (bytes < 1024 * 1024 * 1024)
            return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
        return `${(bytes / 1024 / 1024 / 1024).toFixed(2)} GB`;
    }
    // ─── Public Getter'lar ────────────────────────────────────────────────────
    /**
     * FragmentsModels referansı (ileri düzey kullanım için).
     * init() çağrısından önce null döner.
     */
    get fragments() {
        return this._fragments;
    }
    /** Engine'in başlatılıp başlatılmadığı */
    get isInitialized() {
        return this._fragments !== null && !this._isDisposed;
    }
    /** Engine'in dispose edilip edilmediği */
    get isDisposed() {
        return this._isDisposed;
    }
}
//# sourceMappingURL=ifcLoader.js.map