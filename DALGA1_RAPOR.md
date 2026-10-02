# BuildingAI — Claude Code Talimatları

## Proje
Müteahhitler ve şantiye mühendisleri için Türkçe şantiye yönetimi SaaS'ı. FastAPI + SQLAlchemy + SQLite (PostgreSQL'e geçiş planlı), Gemini, Railway. İki geliştirici.

## Yapı
- `app.py`: Ana uygulama. Bölümler yorum başlıklarıyla ayrılmış (sırasıyla):
  - review/karar yardımcıları
  - şema senkronu (`BUILDINGAI_SCHEMA_SYNC=1`)
  - auth (login, register, Google OAuth, şifre)
  - AI uçları (`/sor`, `/api/chat`, `/kamera-analiz`, `/sesli-rapor`)
  - arşiv, manual-evidence, daily-reports
  - fiyat, stok, ödeme, admin
  - şantiye CRUD
  - deprem, YOLO
  - hiyerarşi CRUD (`/api/v2/...`)
  - hakediş, ekip, dashboard
  - motor fonksiyonları (`_save_progress`, `update_hakedis_from_ilerleme`)
  - satın alma
- Ayrı router'lar: `bim_api.py`, `hakedis_api.py`, `wave2_api.py`.
- Yetki: `access_control.py`. Para: `financial_values.py`. Diğer: `models.py`, `schemas.py`, `auth.py`, `database.py`, `santiye_beyni.py`, `kamera_analiz.py`, `pdf_rapor.py`, `scraper/`.
- Frontend:
  - `/app`: `interface.py` + `scripts.py`
  - `/workspace`: `react-dashboard/dist`
  - `/bim-viewer`: `bim-viewer/dist`

## Yetki deseni (her endpoint'te zorunlu)
- Kullanıcı: `kullanici_dogrula(_request_token(request), db)`
- Şantiye: `require_site(user, santiye_id, db, "write")`
- Kayıt: `require_record(user, row, db, "read" | "write" | "review")`
- Bina, kat, mahal, iş kalemi: `require_hierarchy(user, obj, db, "read" | "write")`
- Liste sorguları: `scope_query(db, user, Model)`
- Yeni kodda `User.role` ile yetki kararı verilmez. Mevcut `role` kullanımlarına görev istemedikçe dokunulmaz.

## Para
- Tutarlar DB'de kuruş (int) olarak tutulur. TL'ye çevirme yalnızca response'ta `/100` ile yapılır.
- Hesaplarda `number()`, `kurus()`, `amount()` kullanılır. Yeni float para aritmetiği eklenmez.

## Kurallar
- Cerrahi değişiklik yap: Yalnızca görevin istediği endpoint veya fonksiyon değişir. Geniş refaktör, yeniden adlandırma ve format düzeltmesi ancak istenirse yapılır.
- Kapsam dışındaki dosyalara dokunma.
- Response şekillerini değiştirme. `success_response` / `error_response` gibi sarmalayıcı ekleme. Hatalar `HTTPException(status, detail)` ile döner.
- Şema veya veri değiştiren işten önce DB yedeği alınır.
- VERIFIED kayıt ve kesinleşmiş hakediş korumaları (409) gevşetilmez.
- Yeni paket veya bağımlılık eklemeden önce sor.
- Gizli değerleri (`.env`, API anahtarları) koda, loga veya commit'e yazma.
- İş bitince şunları kısaca bildir: değişen dosyalar, değişen endpoint'ler, test edilemeyen noktalar.

## Model yönlendirme
Ana oturum işi planlar, kodlama işini büyüklüğüne ve riskine göre `.claude/agents/` altındaki alt ajanlardan birine devreder:
- **`buyuk-is`:** Mimari, migration, app.py bölme, kapsamlı güvenlik denetimi, çok modüllü işler.
- **`orta-ust-is`:** Birden çok endpoint'e dokunan işler. Yetki, para, hakediş veya ilerleme mantığına dokunan her iş, boyutu ne olursa olsun buraya gider.
- **`orta-alt-is`:** Tek endpoint veya fonksiyonla sınırlı ve riskli alanlara dokunmayan işler.
- Birkaç satırlık değişiklikler devredilmez, ana oturumda yapılır.
- Kararsız kalırsan bir üst seviyeyi seç. Alt ajan "kapsam büyük" diye dönerse işi bir üst seviyeye devret.

## Komutlar
<!-- Doğrulanmadı: doldurun. Claude Code burada olmayan komut uydurmaz. -->
- Çalıştırma:
- Alembic migration:
- DB yedeği:
- Test:

## Ortam değişkenleri
`GEMINI_API_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GMAIL_ADRES`, `GMAIL_UYGULAMA_SIFRESI`, `BUILDINGAI_SCHEMA_SYNC`, `BUILDINGAI_SCHEDULER`, `BUILDINGAI_LOG_PATH`

## İletişim
Türkçe, kısa ve direkt.
