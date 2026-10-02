/**
 * bimApi.ts — BuildingAI BIM Viewer API İstemcisi
 * =================================================
 *
 * BIM Viewer frontend'ini BuildingAI backend'ine bağlar.
 *
 * ─── MİMARİ GENEL BAKIŞ ──────────────────────────────────────────────────────
 *
 *  BIMApiClient
 *  ├── uploadIFC()          → POST /api/bim/upload          (XHR + progress)
 *  ├── getModels()          → GET  /api/bim/models
 *  ├── downloadModel()      → GET  /api/bim/model/{id}/download
 *  ├── uploadFragment()     → POST /api/bim/model/{id}/fragment
 *  ├── getProgressData()    → GET  /api/bim/model/{id}/progress
 *  ├── saveMapping()        → POST /api/bim/model/{id}/mapping
 *  ├── saveBulkMapping()    → POST /api/bim/model/{id}/mapping/bulk
 *  ├── suggestMapping()     → POST /api/bim/ai/eslestirme-oner
 *  └── deleteModel()        → DELETE /api/bim/model/{id}
 *
 * ─── MODEL YÜKLEME AKIŞI ─────────────────────────────────────────────────────
 *
 *  1. Kullanıcı IFC dosyasını seçer
 *  2. uploadIFC()          → Backend'e IFC yükle → model_id al
 *  3. IFC → Fragment dönüşümü (web-ifc WASM, frontend'de)
 *  4. uploadFragment()     → .frag'ı backend'e kaydet
 *  5. 3D sahneye fragment'ı ekle
 *  Sonraki açılışta: downloadModel() → direkt .frag (10× hızlı)
 *
 * ─── İLERLEME RENKLENDİRME AKIŞI ────────────────────────────────────────────
 *
 *  1. Model yüklendikten sonra getProgressData() çağır
 *  2. ProgressColoring.applyProgressColors() ile renkleri uygula
 *  3. Her 30 saniyede polling ile güncelle (opsiyonel)
 *
 * ─── HATA YÖNETİMİ ───────────────────────────────────────────────────────────
 *
 *  401 → Token expired: login sayfasına yönlendir
 *  413 → Dosya çok büyük: kullanıcıya bilgi ver
 *  5xx → Retry logic: maks 3 deneme, exponential backoff
 *  Ağ hatası → Offline mesajı göster
 */
import { BIMAPIError, BIMNetworkError, } from './types';
// ─── Sabitler ────────────────────────────────────────────────────────────────
/** localStorage'daki token anahtarı */
const TOKEN_KEY = 'bai_token';
/** Maksimum retry sayısı (5xx ve ağ hataları için) */
const MAX_RETRIES = 3;
/** İlk retry bekleme süresi (ms) — exponential backoff */
const RETRY_BASE_DELAY_MS = 500;
// ─── Ana Sınıf ───────────────────────────────────────────────────────────────
/**
 * BuildingAI BIM API istemcisi.
 *
 * KULLANIM ÖRNEĞİ:
 * ```ts
 * const api = new BIMApiClient('http://localhost:8010');
 *
 * // IFC yükle (ilerleme takipli)
 * const model = await api.uploadIFC(file, santiyeId, (p) => {
 *   console.log(`Yükleniyor: ${p.percent}%`);
 * });
 *
 * // İlerleme verisini al ve 3D sahneye uygula
 * const progressData = await api.getProgressData(model.model_id);
 * await progressColoring.applyProgressColors(progressData);
 * ```
 */
export class BIMApiClient {
    // ── Constructor ──────────────────────────────────────────────────────────
    /**
     * @param baseUrl - BuildingAI backend API URL'si.
     *   Sondaki slash'ı otomatik siler.
     */
    constructor(baseUrl) {
        this._baseUrl = baseUrl.replace(/\/$/, '');
    }
    // ─── Token Yönetimi ───────────────────────────────────────────────────────
    /**
     * localStorage'dan JWT token'ı okur.
     *
     * Token yoksa boş string döner (401 hatası backend'den gelir).
     */
    getToken() {
        return localStorage.getItem(TOKEN_KEY) ?? '';
    }
    /**
     * Token'ı localStorage'a kaydeder.
     * Auth callback'lerinden çağrılabilir.
     */
    setToken(token) {
        localStorage.setItem(TOKEN_KEY, token);
    }
    /**
     * Token'ı localStorage'dan siler (logout).
     */
    clearToken() {
        localStorage.removeItem(TOKEN_KEY);
    }
    // ─── Dosya Yükleme: IFC ──────────────────────────────────────────────────
    /**
     * IFC dosyasını backend'e yükler.
     *
     * `XMLHttpRequest` kullanılır — `fetch` API ilerleme olaylarını desteklemez.
     * Başarılı yüklemede backend'den `model_id` alınır.
     *
     * @param file       - Yüklenecek IFC dosyası
     * @param santiyeId  - Hangi şantiyeye ait olduğu
     * @param onProgress - Yükleme ilerlemesi callback (opsiyonel)
     * @returns BIMModelResponse — model_id içerir
     *
     * @throws BIMAPIError  — HTTP hata yanıtı
     * @throws BIMNetworkError — Ağ bağlantısı yok
     */
    uploadIFC(file, santiyeId, onProgress, blokId) {
        return new Promise((resolve, reject) => {
            const url = `${this._baseUrl}/api/bim/upload`;
            const formData = new FormData();
            formData.append('file', file);
            formData.append('santiye_id', String(santiyeId));
            if (blokId !== undefined)
                formData.append('blok_id', String(blokId));
            const xhr = new XMLHttpRequest();
            // ── Progress tracking ─────────────────────────────────────────────
            if (onProgress) {
                xhr.upload.addEventListener('progress', (event) => {
                    if (event.lengthComputable) {
                        onProgress({
                            loaded: event.loaded,
                            total: event.total,
                            percent: Math.round((event.loaded / event.total) * 100),
                        });
                    }
                });
            }
            // ── Tamamlandı ────────────────────────────────────────────────────
            xhr.addEventListener('load', () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        const data = JSON.parse(xhr.responseText);
                        resolve(data);
                    }
                    catch {
                        reject(new BIMAPIError('Sunucu yanıtı ayrıştırılamadı.', xhr.status, xhr.responseText));
                    }
                    return;
                }
                // HTTP hata
                this._handleXHRError(xhr, reject);
            });
            // ── Ağ hatası ────────────────────────────────────────────────────
            xhr.addEventListener('error', () => {
                reject(new BIMNetworkError());
            });
            xhr.addEventListener('timeout', () => {
                reject(new BIMNetworkError('Bağlantı zaman aşımına uğradı.'));
            });
            // ── İstek gönder ─────────────────────────────────────────────────
            xhr.open('POST', url);
            xhr.setRequestHeader('Authorization', `Bearer ${this.getToken()}`);
            xhr.timeout = 5 * 60 * 1000; // 5 dakika (büyük IFC dosyaları için)
            xhr.send(formData);
        });
    }
    // ─── Model Listesi ────────────────────────────────────────────────────────
    /**
     * Bir şantiyeye ait aktif BIM modellerini listeler.
     *
     * @param santiyeId - Şantiye ID'si
     * @returns BIMModelResponse dizisi
     */
    async getModels(santiyeId) {
        const response = await this._fetchWithRetry(`${this._baseUrl}/api/bim/models?santiye_id=${santiyeId}`);
        const data = await response.json();
        return data.modeller;
    }
    // ─── Model İndirme ────────────────────────────────────────────────────────
    /**
     * Model dosyasını ArrayBuffer olarak indirir.
     *
     * Backend .frag varsa onu, yoksa .ifc dosyasını gönderir.
     * Dönen ArrayBuffer doğrudan `FragmentsModels.load()` veya
     * `IFCLoader.loadFromBuffer()` metodlarına beslenebilir.
     *
     * @param modelId - BIM model ID'si
     * @returns Dosya içeriği (ArrayBuffer)
     */
    async downloadModel(modelId) {
        const response = await this._fetchWithRetry(`${this._baseUrl}/api/bim/model/${modelId}/download`);
        return response.arrayBuffer();
    }
    // ─── Fragment Yükleme ─────────────────────────────────────────────────────
    /**
     * Frontend'de IFC → .frag dönüşümü yapıldıktan sonra çağrılır.
     *
     * .frag dosyası backend'e kaydedilir. Sonraki açılışlarda
     * `downloadModel()` .frag döndürür → yaklaşık 10× daha hızlı yükleme.
     *
     * @param modelId      - BIM model ID'si
     * @param fragmentData - Dönüştürülmüş .frag içeriği (ArrayBuffer)
     */
    async uploadFragment(modelId, fragmentData) {
        const blob = new Blob([fragmentData], { type: 'application/octet-stream' });
        const formData = new FormData();
        formData.append('file', blob, `model_${modelId}.frag`);
        const response = await this._fetchWithRetry(`${this._baseUrl}/api/bim/model/${modelId}/fragment`, {
            method: 'POST',
            body: formData,
            // FormData için Content-Type'ı tarayıcıya bırak (boundary dahil edilmesi için)
        }, { skipContentType: true });
        await response.json();
        // Hata yoksa void döner
    }
    // ─── İlerleme Verisi ──────────────────────────────────────────────────────
    /**
     * Bir BIM modeline atanmış element–iş kalemi eşleştirmelerini ve
     * ilerleme verilerini getirir.
     *
     * Dönen veri `progressColoring.ts`'deki `applyProgressColors()` metoduna
     * doğrudan beslenebilir:
     * ```ts
     * const data = await api.getProgressData(modelId);
     * await progressColoring.applyProgressColors(data);
     * ```
     *
     * @param modelId - BIM model ID'si
     * @returns ProgressData — elementMapping dizisi içerir
     */
    async getProgressData(modelId) {
        const response = await this._fetchWithRetry(`${this._baseUrl}/api/bim/model/${modelId}/progress`);
        const raw = await response.json();
        // Backend snake_case → frontend camelCase dönüşümü.
        // is_kalemi_id === null olanlar "eslesmemis" renk grubuna girer — filtreden çıkarılmaz.
        const elementMapping = raw.eslestirmeler
            .map((e) => this._mapProgressElement(e));
        return { elementMapping };
    }
    // ─── Tekli Eşleştirme ────────────────────────────────────────────────────
    /**
     * Bir IFC elementini bir BuildingAI iş kalemine eşler (veya günceller).
     *
     * Backend UPSERT yapar: aynı (model, globalId) çifti varsa günceller,
     * yoksa ekler. İsteğe bağlı metraj ve IFC metadata alanları da kaydedilir.
     *
     * @param modelId      - BIM model ID'si
     * @param body         - Eşleştirme verisi (ifc_global_id, is_kalemi_id, + opsiyonel alanlar)
     */
    async saveMapping(modelId, body) {
        await this._fetchWithRetry(`${this._baseUrl}/api/bim/model/${modelId}/mapping`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
    }
    /**
     * IFC elementi için Gemini destekli iş kalemi önerisi alır.
     *
     * @param santiyeId   - Şantiye ID'si (filtreleme için)
     * @param elementInfo - Seçili IFC elementinin bilgileri
     * @returns AISuggestionResponse — öneriler dizisi
     */
    async suggestMapping(santiyeId, elementInfo) {
        const response = await this._fetchWithRetry(`${this._baseUrl}/api/bim/ai/eslestirme-oner`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                santiye_id: santiyeId,
                element: {
                    ifc_type: elementInfo.ifcType,
                    name: elementInfo.name,
                    storey: elementInfo.storey,
                    properties: elementInfo.properties,
                },
            }),
        });
        return response.json();
    }
    // ─── Toplu Eşleştirme ────────────────────────────────────────────────────
    /**
     * Birden fazla IFC elementini iş kalemlerine toplu eşler.
     *
     * Büyük IFC modellerinde tüm elementleri tek tek eşleştirmek yerine
     * tek seferde gönderilmesini sağlar.
     *
     * @param modelId  - BIM model ID'si
     * @param mappings - Eşleştirme listesi [{ ifc_global_id, is_kalemi_id }]
     * @returns BulkMappingResponse — basarili/hata_sayisi içerir
     */
    async saveBulkMapping(modelId, mappings) {
        const body = { mappings };
        const response = await this._fetchWithRetry(`${this._baseUrl}/api/bim/model/${modelId}/mapping/bulk`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        return response.json();
    }
    // ─── Eşleştirme Silme ────────────────────────────────────────────────────
    /**
     * Tek bir element–iş kalemi eşleştirmesini siler.
     *
     * @param modelId       - BIM model ID'si
     * @param eslestirmeId  - Silinecek eşleştirme ID'si
     */
    async deleteMapping(modelId, eslestirmeId) {
        const response = await this._fetchWithRetry(`${this._baseUrl}/api/bim/model/${modelId}/mapping/${eslestirmeId}`, { method: 'DELETE' });
        return response.json();
    }
    // ─── Model Silme (Soft Delete) ────────────────────────────────────────────
    /**
     * BIM modelini soft-delete yapar (durum → 'silindi').
     *
     * Fiziksel dosya silinmez. Endpoint 410 döner sonraki GET isteklerinde.
     *
     * @param modelId - Silinecek BIM model ID'si
     */
    async deleteModel(modelId) {
        await this._fetchWithRetry(`${this._baseUrl}/api/bim/model/${modelId}`, { method: 'DELETE' });
    }
    // ─── İlerleme Polling ─────────────────────────────────────────────────────
    /**
     * İlerleme verilerini her `intervalMs` milisaniyede bir günceller.
     *
     * KULLANIM:
     * ```ts
     * const stop = api.startProgressPolling(modelId, 30_000, async (data) => {
     *   await progressColoring.applyProgressColors(data);
     * });
     *
     * // Polling'i durdur
     * stop();
     * ```
     *
     * @param modelId    - BIM model ID'si
     * @param intervalMs - Polling aralığı (ms). Varsayılan: 30.000 (30 saniye)
     * @param onUpdate   - Veri güncellendiğinde çağrılan callback
     * @returns Polling'i durduran fonksiyon
     */
    startProgressPolling(modelId, intervalMs = 30000, onUpdate) {
        let active = true;
        const poll = async () => {
            if (!active)
                return;
            try {
                const data = await this.getProgressData(modelId);
                if (active)
                    onUpdate(data);
            }
            catch (err) {
                // Polling sırasındaki hatalar sessizce loglanır — kullanıcıyı rahatsız etme
                console.warn('[BIMApiClient] Progress polling hatası:', err);
            }
        };
        const timerId = window.setInterval(() => { void poll(); }, intervalMs);
        // İlk çağrıyı hemen yap
        void poll();
        return () => {
            active = false;
            window.clearInterval(timerId);
        };
    }
    // ─── Özel: HTTP İstekleri ─────────────────────────────────────────────────
    /**
     * Retry logic'li fetch wrapper.
     *
     * - 5xx hataları ve ağ hatalarında `MAX_RETRIES` kez dener
     * - Her denemede bekleme süresi katlanır (exponential backoff)
     * - 401 → login'e yönlendir
     * - 413 → `BIMAPIError` fırlat (retry yok)
     *
     * @param url     - İstek URL'si
     * @param init    - fetch RequestInit (method, headers, body)
     * @param options - Ek seçenekler (skipContentType vb.)
     */
    async _fetchWithRetry(url, init = {}, options = {}) {
        // Authorization header'ı her isteğe ekle
        const headers = new Headers(init.headers);
        if (!options.skipContentType && !headers.has('Content-Type') && !init.body) {
            // GET isteklerinde Content-Type ekleme
        }
        headers.set('Authorization', `Bearer ${this.getToken()}`);
        const mergedInit = { ...init, headers };
        let lastError = null;
        for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
            try {
                const response = await fetch(url, mergedInit);
                // ── Başarı ───────────────────────────────────────────────────
                if (response.ok) {
                    return response;
                }
                // ── 401: Token süresi dolmuş ─────────────────────────────────
                if (response.status === 401) {
                    this._handleUnauthorized();
                    throw new BIMAPIError('Oturum süresi dolmuştur. Lütfen tekrar giriş yapın.', 401, 'unauthorized');
                }
                // ── 413: Dosya çok büyük ─────────────────────────────────────
                if (response.status === 413) {
                    throw new BIMAPIError('Dosya çok büyük. Maksimum izin verilen boyut 500 MB.', 413, 'file_too_large');
                }
                // ── 4xx: İstemci hatası — retry yok ─────────────────────────
                if (response.status >= 400 && response.status < 500) {
                    let detail = response.statusText;
                    try {
                        const errBody = await response.json();
                        detail = errBody.detail ?? detail;
                    }
                    catch { /* JSON parse hatası — statusText kullan */ }
                    throw new BIMAPIError(`İstek hatası: ${detail}`, response.status, detail);
                }
                // ── 5xx: Sunucu hatası — retry ───────────────────────────────
                let detail = response.statusText;
                try {
                    const errBody = await response.json();
                    detail = errBody.detail ?? detail;
                }
                catch { /* ignore */ }
                lastError = new BIMAPIError(`Sunucu hatası (${response.status}): ${detail}`, response.status, detail);
            }
            catch (err) {
                if (err instanceof BIMAPIError)
                    throw err; // Retry yapma
                // Ağ hatası
                lastError = err instanceof Error ? err : new BIMNetworkError();
                if (!(err instanceof BIMNetworkError) && !(err instanceof TypeError)) {
                    throw lastError;
                }
            }
            // Son deneme değilse bekle
            if (attempt < MAX_RETRIES - 1) {
                const delay = RETRY_BASE_DELAY_MS * Math.pow(2, attempt);
                console.warn(`[BIMApiClient] Retry ${attempt + 1}/${MAX_RETRIES - 1} — ${delay}ms bekleniyor...`);
                await this._sleep(delay);
            }
        }
        // Tüm denemeler başarısız
        if (lastError instanceof BIMAPIError)
            throw lastError;
        throw new BIMNetworkError(lastError?.message ?? 'Sunucuya bağlanılamıyor. İnternet bağlantınızı kontrol edin.');
    }
    // ─── Özel: Yardımcılar ────────────────────────────────────────────────────
    /**
     * XMLHttpRequest hata yanıtını `BIMAPIError`'a dönüştürür.
     */
    _handleXHRError(xhr, reject) {
        if (xhr.status === 401) {
            this._handleUnauthorized();
            reject(new BIMAPIError('Oturum süresi dolmuştur.', 401, 'unauthorized'));
            return;
        }
        if (xhr.status === 413) {
            reject(new BIMAPIError('Dosya çok büyük (maks 500 MB).', 413, 'file_too_large'));
            return;
        }
        let detail = xhr.statusText;
        try {
            const body = JSON.parse(xhr.responseText);
            detail = body.detail ?? detail;
        }
        catch { /* ignore */ }
        reject(new BIMAPIError(`HTTP ${xhr.status}: ${detail}`, xhr.status, detail));
    }
    /**
     * 401 yanıtı alındığında token'ı temizler ve login sayfasına yönlendirir.
     */
    _handleUnauthorized() {
        console.warn('[BIMApiClient] 401 — Token geçersiz. Login sayfasına yönlendiriliyor.');
        this.clearToken();
        // BuildingAI login sayfası
        window.location.href = '/';
    }
    /**
     * Backend snake_case progress elementini frontend camelCase formatına çevirir.
     * progressColoring.ts'deki `ElementProgressMapping` interface'ini doldurur.
     */
    _mapProgressElement(raw) {
        // is_kalemi_id null ise element iş kalemine eşleştirilmemiş — özel durum rengi
        if (raw.is_kalemi_id === null) {
            return {
                ifcGlobalId: raw.ifc_global_id,
                ifcType: raw.ifc_tip ?? 'IfcBuildingElement',
                isKalemiId: 0,
                isKalemiAdi: '',
                durum: 'eslesmemis',
                ilerlemeYuzdesi: 0,
            };
        }
        // Backend durum → progressColoring durum eşleştirmesi
        const durumMap = {
            planli: 'planli',
            devam_eden: 'devam_ediyor',
            tamamlandi: 'tamamlandi',
            iptal: 'planli',
        };
        return {
            ifcGlobalId: raw.ifc_global_id,
            ifcType: raw.ifc_tip ?? 'IfcBuildingElement',
            isKalemiId: raw.is_kalemi_id,
            isKalemiAdi: raw.is_kalemi_tanim ?? '',
            durum: durumMap[raw.is_kalemi_durum ?? 'planli'] ?? 'planli',
            ilerlemeYuzdesi: raw.tamamlanma_yuzdesi ?? 0,
        };
    }
    /**
     * Belirtilen süre kadar bekler (retry için).
     */
    _sleep(ms) {
        return new Promise((resolve) => window.setTimeout(resolve, ms));
    }
}
// ─── Singleton Factory ────────────────────────────────────────────────────────
/**
 * Uygulama genelinde tek bir `BIMApiClient` örneği döndürür.
 *
 * KULLANIM:
 * ```ts
 * import { getBIMApiClient } from './api/bimApi';
 *
 * const api = getBIMApiClient();
 * const models = await api.getModels(santiyeId);
 * ```
 *
 * `BASE_URL` ortam değişkeninden veya mevcut sayfanın origin'inden alınır.
 */
let _instance = null;
export function getBIMApiClient(baseUrl) {
    if (!_instance) {
        // Vite env var veya mevcut origin (aynı domain'den serve ediliyorsa)
        const envUrl = (typeof import.meta !== 'undefined'
            ? import.meta.env?.VITE_API_URL
            : undefined) ?? '';
        const url = baseUrl ?? (envUrl !== '' ? envUrl : window.location.origin);
        _instance = new BIMApiClient(url);
    }
    return _instance;
}
/**
 * Singleton'ı sıfırlar (test veya logout için).
 */
export function resetBIMApiClient() {
    _instance = null;
}
//# sourceMappingURL=bimApi.js.map