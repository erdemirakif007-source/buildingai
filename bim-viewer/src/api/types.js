/**
 * types.ts — BuildingAI BIM API istek/yanıt tip tanımları
 * =========================================================
 *
 * Tüm BIM Viewer ↔ Backend veri sözleşmesi bu dosyada tanımlanır.
 * bimApi.ts, progressColoring.ts ve diğer modüller buradan import eder.
 *
 * Backend karşılıkları: bim_api.py (Python/FastAPI)
 */
/**
 * BIMApiClient tarafından fırlatılan yapılandırılmış hata.
 */
export class BIMAPIError extends Error {
    constructor(message, statusCode, detail) {
        super(message);
        this.statusCode = statusCode;
        this.detail = detail;
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
//# sourceMappingURL=types.js.map