/**
 * types.ts — BuildingAI BIM API istek/yanıt tip tanımları
 * =========================================================
 *
 * Tüm BIM Viewer ↔ Backend veri sözleşmesi bu dosyada tanımlanır.
 * bimApi.ts, progressColoring.ts ve diğer modüller buradan import eder.
 *
 * Backend karşılıkları: bim_api.py (Python/FastAPI)
 */

// ─── Model Yükleme / Listeleme ───────────────────────────────────────────────

/**
 * POST /api/bim/upload response
 * GET  /api/bim/models response — her bir model öğesi
 */
export interface BIMModelResponse {
  /** Veritabanındaki benzersiz model ID'si */
  model_id: number;
  /** Sunucudaki benzersiz dosya adı (UUID tabanlı) */
  dosya_adi: string;
  /** Kullanıcının yüklediği orijinal dosya adı */
  orijinal_dosya_adi: string;
  /** Dosya boyutu (byte) */
  dosya_boyutu: number;

  // --- Aşağıdaki alanlar yalnızca GET /models yanıtında gelir ---

  /** Şantiye ID'si */
  santiye_id?: number;
  /** Blok/bina ID'si (opsiyonel) */
  blok_id?: number | null;
  /** Yükleme tarihi (ISO 8601) */
  yukleme_tarihi?: string;
  /** Yükleyen kullanıcı ID'si */
  yukleyen_kullanici_id?: number;
  /** Model durumu: 'aktif' | 'arsivlendi' | 'silindi' */
  durum?: 'aktif' | 'arsivlendi' | 'silindi';
  /** IFC'den çekilen metadata (proje adı, yazar vb.) */
  metadata?: Record<string, unknown>;
  /** .frag dosyası mevcut mu? */
  fragment_hazir?: boolean;
}

/**
 * GET /api/bim/models response zarfı
 */
export interface BIMModelsListResponse {
  modeller: BIMModelResponse[];
  toplam: number;
}

// ─── Fragment Yükleme ────────────────────────────────────────────────────────

/**
 * POST /api/bim/model/{id}/fragment response
 */
export interface FragmentUploadResponse {
  model_id: number;
  fragment_dosya_yolu: string;
  dosya_boyutu: number;
}

// ─── Soft Delete ─────────────────────────────────────────────────────────────

/**
 * DELETE /api/bim/model/{id} response
 */
export interface DeleteModelResponse {
  status: 'ok';
  model_id: number;
  durum: 'silindi';
}

/**
 * DELETE /api/bim/model/{id}/mapping/{eslestirme_id} response
 */
export interface DeleteMappingResponse {
  status: 'ok';
  eslestirme_id: number;
}

// ─── İlerleme / Renklendirme ─────────────────────────────────────────────────

/**
 * Bir IFC elementinin BuildingAI iş kalemi ile ilerleme eşleşmesi.
 *
 * Backend: bim_element_eslestirme tablosu + ilerleme_kayitlari JOIN.
 * progressColoring.ts bu interface'i kullanır.
 */
export interface ElementProgressMapping {
  /** bim_element_eslestirme.id */
  eslestirme_id: number;
  /** IFC GlobalId (örn. "2O2Fr$t4X7Zf8NOew3FNr2") */
  ifc_global_id: string;
  /** IFC element tipi (IfcWall, IfcSlab vb.) */
  ifc_tip: string | null;
  /** IFC katı (BuildingStorey adı) */
  ifc_kat: string | null;
  /** BuildingAI iş kalemi ID'si */
  is_kalemi_id: number | null;
  /** İş kalemi tanımı */
  is_kalemi_tanim: string | null;
  /** İş kalemi birimi (m², m³ vb.) */
  is_kalemi_birim: string | null;
  /** İş kalemi durumu: planli | devam_eden | tamamlandi | iptal */
  is_kalemi_durum: 'planli' | 'devam_eden' | 'tamamlandi' | 'iptal' | null;
  /** Metraj */
  is_kalemi_metraj: number | null;
  /** Son ilerleme kaydından hesaplanan tamamlanma yüzdesi (0–100) */
  tamamlanma_yuzdesi: number | null;
  /** Backend tarafından hesaplanan renk hex kodu */
  renk_kodu: string;
}

/**
 * GET /api/bim/model/{id}/progress response zarfı.
 *
 * progressColoring.ts içindeki ProgressData interface'i ile uyumludur —
 * elementMapping alanı oraya dönüştürülerek beslenir.
 */
export interface ProgressDataResponse {
  model_id: number;
  /** Tüm element eşleştirmeleri + ilerleme verileri */
  eslestirmeler: ElementProgressMapping[];
  toplam: number;
}

/**
 * progressColoring.ts'in beklediği ProgressData formatına dönüştürülmüş veri.
 * BIMApiClient.getProgressData() bu formatta döner.
 */
export interface ProgressData {
  elementMapping: ElementProgressMappingLegacy[];
}

/**
 * progressColoring.ts içindeki mevcut ElementProgressMapping interface'i
 * (camelCase). BIMApiClient backend yanıtını bu formata dönüştürür.
 */
export interface ElementProgressMappingLegacy {
  ifcGlobalId: string;
  ifcType: string;
  isKalemiId: number;
  isKalemiAdi: string;
  durum: 'planli' | 'devam_ediyor' | 'tamamlandi' | 'beklemede' | 'eslesmemis';
  ilerlemeYuzdesi: number;
}

// ─── Eşleştirme (Mapping) ────────────────────────────────────────────────────

/**
 * POST /api/bim/model/{id}/mapping request body
 */
export interface SingleMappingRequest {
  ifc_global_id: string;
  is_kalemi_id: number;
}

/**
 * POST /api/bim/model/{id}/mapping response
 */
export interface SingleMappingResponse {
  status: 'ok';
  model_id: number;
  ifc_global_id: string;
  is_kalemi_id: number;
}

/**
 * POST /api/bim/model/{id}/mapping/bulk — tek bir eşleştirme öğesi
 */
export interface MappingInput {
  ifc_global_id: string;
  is_kalemi_id: number;
  ifc_tip?: string;
  ifc_kat?: string;
  metraj?: number;
  metraj_birimi?: string;
  metraj_kaynagi?: string;
}

/**
 * POST /api/bim/model/{id}/mapping/bulk request body
 */
export interface BulkMappingRequest {
  mappings: MappingInput[];
}

/**
 * POST /api/bim/model/{id}/mapping/bulk response
 */
export interface BulkMappingResponse {
  status: 'ok' | 'partial';
  model_id: number;
  basarili: number;
  hata_sayisi: number;
  hatalar: Array<{ ifc_global_id: string; hata: string }>;
}

// ─── Upload İlerleme ─────────────────────────────────────────────────────────

/**
 * uploadIFC() progress callback için parametre.
 */
export interface UploadProgress {
  /** Yüklenen byte miktarı */
  loaded: number;
  /** Toplam dosya boyutu (byte) */
  total: number;
  /** Yüzde (0–100) */
  percent: number;
}

// ─── AI Öneri ────────────────────────────────────────────────────────────────

/**
 * POST /api/bim/ai/eslestirme-oner — malzeme reçetesi öğesi
 */
export interface AISuggestionMalzeme {
  malzeme: string;
  miktar_birim_basina: number;
  birim: string;
  zorunlu: boolean;
}

/**
 * POST /api/bim/ai/eslestirme-oner — tek bir öneri
 */
export interface AISuggestion {
  katalog_id: number;
  poz_no: string;
  ad: string;
  birim: string;
  guven_skoru: number;
  gerekce: string;
  metraj: number | null;
  metraj_birimi: string | null;
  metraj_kaynagi: string | null;
  malzeme_recetesi: AISuggestionMalzeme[];
}

/**
 * POST /api/bim/ai/eslestirme-oner response
 */
export interface AISuggestionResponse {
  status: string;
  oneriler: AISuggestion[];
}

/**
 * POST /api/bim/model/{id}/mapping request body (single mapping)
 */
export interface SingleMappingBody {
  ifc_global_id: string;
  is_kalemi_id: number;
  ifc_tip?: string;
  ifc_kat?: string;
  metraj?: number;
  metraj_birimi?: string;
  metraj_kaynagi?: string;
}

// ─── Hata Tipleri ────────────────────────────────────────────────────────────

/**
 * BIM API hata yanıtı (FastAPI HTTPException formatı).
 */
export interface APIError {
  detail: string;
}

/**
 * BIMApiClient tarafından fırlatılan yapılandırılmış hata.
 */
export class BIMAPIError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number,
    public readonly detail: string,
  ) {
    super(message);
    this.name = 'BIMAPIError';
  }
}

/**
 * Ağ bağlantısı olmadığında fırlatılan hata.
 */
export class BIMNetworkError extends Error {
  constructor(message = 'Sunucuya bağlanılamıyor. İnternet bağlantınızı kontrol edin.') {
    super(message);
    this.name = 'BIMNetworkError';
  }
}
