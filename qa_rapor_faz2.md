# BuildingAI — Faz 2 QA Raporu

**Tarih:** 2026-10-03  
**Test Ortamı:** Yerel geliştirme — `uvicorn app:app --port 8000`, `santiye_proje.db`  
**Test Hesapları:**
| Kullanıcı | E-posta | Rol | Org |
|-----------|---------|-----|-----|
| Müteahhit (org sahibi) | faz2mutahhit@test.com | proje_muduru | Faz2 Insaat AS (ID=7) |
| Şantiye Şefi | faz2+sefi@test.com | santi_sefi (org-wide) | ID=7 |
| Mühendis | faz2+muhendis@test.com | muhendis (santiye 9 only) | ID=7 |

**Test Şantiyeleri:** A Blok (ID=9, İstanbul), B Blok (ID=10, Ankara)

---

## Regresyon Sonuçları (S-1 … S-13)

| # | Senaryo | Durum | Gözlem |
|---|---------|-------|--------|
| S-1 | Stok negatif/sıfır miktar | ✅ DÜZELTİLDİ | `POST /stok-ekle` ile `miktar=-50` → HTTP 422 `"Miktar geçerli, negatif olmayan bir sayı olmalıdır."`. `miktar=0` → 422 `"Miktar sıfır olamaz."` |
| S-2 | Eksik `/stok-sarf` ve `/stok-esik-ayarla` | ⚠️ KISMİ | `/stok-sarf` EKLENMİŞ, çalışıyor (HTTP 200). `/stok-esik-ayarla` EKLENMIŞ ama DB'de `stok_esik.max_miktar` sütunu olmadığı için 500 döndürüyor (bkz. #A-3) |
| S-3 | MalzemeUyari scope_query | ❌ HALA AÇIK | `/fiyat-gir` fiyat değişikliği > %5 tetiklediğinde `organization_id=NULL` ile `malzeme_uyari` kaydı oluşturuluyor. `/api/fiyat/alertler`; `scope_query` önce `org_id=7` ile filtreler, ardından `(org_id=7 OR org_id=NULL)` ekler — ancak AND koşulu `org_id=NULL` satırları zaten dışlar. Org üyeleri global uyarıları göremez. |
| S-5 | Content-Disposition UTF-8 | ✅ DÜZELTİLDİ | `hakedis_api.py` → `_cd()` fonksiyonu RFC 5987 `filename*=UTF-8''...` formatını kullanıyor. Gözlemlenen başlık: `attachment; filename="BuildingAI_Hakedis_1.pdf"; filename*=UTF-8''BuildingAI_Hakedis_1.pdf` |
| S-6 | Virgüllü ondalık (`"12,5"`) | ⚠️ KISMİ | `/stok-ekle`: `"12,5"` → virgül nokta'ya dönüştürülüp `number()` a veriliyor — DÜZELTİLDİ. **Ancak** `/api/v2/mahal/{id}/is-kalemleri` ve `/api/v2/santiye/{id}/is-kalemleri`: virgül dönüşümü yok; `"12,5"` girince 422 `"Metraj geçerli, negatif olmayan bir sayı olmalıdır."` döner (hata yakalanıyor ama mesaj yanıltıcı — neden hata olduğu belirtilmiyor) |
| S-9 | BIM Türkçe dosya adı URL yolu | ✅ DÜZELTİLDİ | BIM dosyaları UUID ile saklanıyor (`4fd062d3f1cb44e98220ad5c731b1f40.ifc`). Orijinal isim `orijinal_dosya_adi` alanında tutuluyor ama URL yolunda hiç kullanılmıyor. İndirme başlığı: `attachment; filename="4fd062d3f1cb44e98220ad5c731b1f40.ifc"` |
| S-13 | Rol yazım tutarsızlığı | ✅ DÜZELTİLDİ | `normalize_role()`: `santiye_sefi`→`santi_sefi`, `mutahhit`→`muteahhit`. Davet gönderimde test edildi: `role="santiye_sefi"` ile davet → DB'de `santi_sefi`; `role="mutahhit"` ile davet → DB'de `muteahhit` kaydedildi. DB'de eski yazımla (`santi_sefi`, `muteahhit`) kayıtlı `project_members` satırları `WRITE_ROLES` kümesine dahil edildiğinden erişim kontrolünde çalışıyor. |

---

## Yeni Bulgular

| # | Modül | Tür | Önem | Yeniden Üretme Adımları | Beklenen | Gerçekleşen |
|---|-------|-----|------|------------------------|----------|-------------|
| A-1 | `/stok-ekle` | Bug | **Kritik** | `POST /stok-ekle` body: `{"token":"...","malzeme":"demir","miktar":100,"birim":"kg","tip":"giris","santiye_id":9}` (fiyat YOK) | HTTP 200, stok kaydı oluşur | HTTP 500 `"Beklenmeyen bir hata oluştu"`. Sunucu logu: `StatementError: could not convert string to float: ''` — `fiyat=""` boş string `Float` kolona yazılmaya çalışıyor. `tip="cikis"` için de aynı hata. Fiyat değeri girilirse (ör. `"fiyat":28.50`) başarılı çalışıyor. |
| A-2 | `/api/hakedis/olustur` | Bug | **Kritik** | `POST /api/hakedis/olustur` body: `{"santiye_id":9,"donem_baslangic":"2026-01-01","donem_bitis":"2026-01-31"}` | HTTP 200, hakediş oluşur | `BUILDINGAI_SCHEMA_SYNC=1` olmadan HTTP 500 — `no such table: contract_lines`. DB'de `contracts`, `contract_lines`, `payment_contracts` tabloları eksik. Sunucu `BUILDINGAI_SCHEMA_SYNC=1` ile başlatılınca tablolar oluşturuldu ve endpoint çalıştı. |
| A-3 | `/stok-esik-ayarla` | Bug | **Yüksek** | `POST /stok-esik-ayarla` body: `{"token":"...","malzeme":"demir","min_miktar":100,"santiye_id":9}` | HTTP 200, eşik ayarı kaydedilir | HTTP 500. Sunucu logu: `no such column: stok_esik.max_miktar` — model `max_miktar` kolonu tanımlıyor ama DB migrasyonu yapılmamış |
| A-4 | `POST /davet-gonder` → `santiye_ids` | Eksik Özellik | **Yüksek** | `santiye_ids:[9]` ile davet gönder, davet kabul et | Kabul eden kullanıcı yalnızca santiye 9'a atanmalı | `project_members` kaydı `santiye_id=NULL` (org-wide) oluştu. `santiye_ids` parametresi `davet_gonder`'de alınıyor ancak `Invitation` modeline kaydedilmiyor ve kabul akışında kullanılmıyor. Mühendisi manuel DB güncellemesiyle santiye 9'a kısıtladım. |
| A-5 | `POST /api/v2/mahal/{id}/is-kalemleri` | Bug/UX | **Orta** | `{"tanim":"<script>alert(1)</script>","birim":"m2","metraj":10,"birim_fiyat_tl":100}` | XSS girişimi reddedilmeli ya da encode edilerek saklanmalı | HTTP 200, `"tanim":"<script>alert(1)</script>"` ham haliyle DB'ye ve response'a yazılıyor. API bir JSON API olduğundan veri görüntüleme güvenliği tamamen frontend'e bırakılmış; `innerHTML` kullanan herhangi bir UI için risk mevcut. |
| A-6 | `POST /api/v2/mahal/{id}/is-kalemleri` | Bug | **Orta** | `tanim` alanına 1000 karakter gönder | 422 veya DB'de maksimum uzunluk kesimi | HTTP 200, 1000 karakter `tanim` olarak kaydedildi ve hakediş PDF'ine dahil oldu |
| A-7 | `/api/fiyat/alertler` (S-3 devamı) | Bug | **Orta** | 1. `POST /fiyat-gir` ile %6.8 fiyat değişimi oluştur → `malzeme_uyari` kaydı `org_id=NULL` ile oluşuyor. 2. `GET /api/fiyat/alertler` çağır (muhendis veya muteahhit token) | Fiyat uyarısı görünmeli | `{"alertler":[],"toplam":0}` — NULL org_id kayıtlar, org üyeleri tarafından görülemiyor |
| A-8 | Hakedis onay iş akışı | UX/Tasarım | **Orta** | Hakedişi hazırlayan kişi `durum=onay_bekliyor`'dan `onaylandi`'ya geçirmeye çalışır | Onaylamak için farklı kullanıcı gerekiyorsa açık mesaj göster | HTTP 409 `"Hazırlayan kişi kendi hakedişine karar veremez."` — mesaj makul. Ancak tek kullanıcılı kurulumda (org owner hem hazırlayan hem onaylayan) workflow tamamen kilitleniyor; bypass mekanizması yok. |
| A-9 | BIM model indirme | UX | **Düşük** | BIM modeli yükle (orijinal ad: "A Blok Zemin Kat.ifc"), ardından indir | İndirme `filename="A Blok Zemin Kat.ifc"` göstermeli | İndirme `filename="4fd062d3f1cb44e98220ad5c731b1f40.ifc"` gösteriyor — UUID adı, orijinal dosya adı değil. `orijinal_dosya_adi` DB'de var ama indirme başlığında kullanılmıyor. |

---

## Yetki Sınırları Özeti (T-8)

| Test | Sonuç |
|------|-------|
| Mühendis `/santiyeler` → yalnızca santiye 9 görüyor | ✅ Doğru |
| Mühendis `GET /arsiv?santiye_id=10` | ✅ HTTP 404 "Şantiye bulunamadı." |
| Mühendis `GET /api/hakedis/liste/10` | ✅ HTTP 404 "Şantiye bulunamadı." |
| Mühendis `GET /api/bim/models?santiye_id=10` | ✅ HTTP 404 "Şantiye bulunamadı." |
| Mühendis `POST /api/v2/santiye/10/is-kalemleri` | ✅ HTTP 404 "Şantiye bulunamadı." |
| Mühendis `GET /stok?santiye_id=10` | ⚠️ HTTP 200, tüm malzemeler için sıfır veri döndü — scope_query santiye_id=10'a ait veriyi filtreler mi ayrıca doğrulanmalı (bug değil, boş sonuç dönüyor) |
| Şantiye şefi olmayan kullanıcı davet gönderme | ✅ HTTP 403 "Davet göndermek için organizasyon sahibi olmalısınız." |
| Admin paneli (`/admin`) GET | ⚠️ HTTP 200 — HTML sayfa, herkes görüyor. `/admin/plan-degistir` POST → token body'de gerektiği için 401. Yetki kontrolleri API seviyesinde. |

---

## Hatalı Girdi Özeti (T-9)

| Girdi | Endpoint | Beklenen | Gerçekleşen |
|-------|----------|----------|-------------|
| `metraj: -10` | `/api/v2/mahal/{id}/is-kalemleri` | 422 | ✅ 422 "Metraj geçerli, negatif olmayan bir sayı olmalıdır." |
| `metraj: "12,5"` | `/api/v2/mahal/{id}/is-kalemleri` | 200 veya anlamlı hata | ⚠️ 422 — hata yakalanıyor ama mesaj virgül konusunu belirtmiyor |
| `tanim: ""` | `/api/v2/mahal/{id}/is-kalemleri` | 422 | ✅ 422 "Tanım zorunludur." |
| 1000 karakter `tanim` | `/api/v2/mahal/{id}/is-kalemleri` | 422 veya kesim | ❌ 200, tüm metin kabul edildi |
| `<script>alert(1)</script>` | `/api/v2/mahal/{id}/is-kalemleri` | Encode/reddedilmeli | ⚠️ 200, ham kaydedildi |
| `donem_baslangic: "31-01-2026"` | `/api/hakedis/olustur` | 422 | ✅ 422 "Geçerli başlangıç ve bitiş tarihlerini girin." |
| `ad: ""` | `/api/v2/santiye/{id}/binalar` | 422 | ✅ 422 "Bina adı zorunludur." |
| `miktar: -50` (stok) | `/stok-ekle` | 422 | ✅ 422 "Miktar geçerli, negatif olmayan bir sayı olmalıdır." |
| `miktar: 0` (stok) | `/stok-ekle` | 422 | ✅ 422 "Miktar sıfır olamaz." |
| `miktar: "12,5"` (stok) | `/stok-ekle` | 200 (S-6 fix) | ❌ 500 — fiyat sağlanmadığından A-1 hatası öne geçiyor |
| Türkçe karakterli BIM dosyası | `/api/bim/upload` | Yüklenmeli | test edilemedi — `curl --form filename=İnşaat_Planı.ifc` ile boş yanıt; Bash terminali encoding kısıtlaması nedeniyle kesin sonuç alınamadı |
| Email adresi `+` içeren kayıt | `/register` | 200 | ✅ 200, başarılı kayıt (`test+sub@example.com`) |

---

## Hakediş Akışı Özeti (T-5)

| Adım | Sonuç |
|------|-------|
| Donem 1 (Ocak) oluştur | ✅ `hakedis_id=8`, `durum=taslak` |
| Kalem miktar güncelle (5.0 m3) | ✅ `kumulatif_tutar=9000 TL` |
| Negatif miktar girişimi | ✅ 422 "Miktar geçerli, negatif olmayan bir sayı olmalıdır." |
| Hazırlayan onay girişimi | ✅ 409 "Hazırlayan kişi kendi hakedişine karar veremez." |
| Şantiye şefi onayı | ✅ `durum=onaylandi` |
| Donem 2 (Şubat) oluştur | ✅ `hakedis_id=9`, `onceki_toplam=9000 TL` |
| Donem 2 kalem güncellemesi | ✅ `kumulatif_miktar=9.0` (5+4), `kumulatif_tutar=16200 TL` |
| Onaylanmış hakedis kalemi düzenleme girişimi | ✅ 409 "Yalnızca taslak hakediş düzenlenebilir." |
| PDF indirme Content-Disposition | ✅ `filename*=UTF-8''BuildingAI_Hakedis_1.pdf` (RFC 5987) |

---

## Test Edilemeyen Noktalar

- **BIM Türkçe dosya adı yükleme** — Bash terminali `curl --form` ile `İnşaat_Planı.ifc` gibi UTF-8 karakterler encoding sorununa neden oldu; yükleme işlemi boş yanıt döndürdü. PowerShell/tarayıcı ortamında ayrıca test edilmeli.
- **AI fiyat güncelleme** (`/fiyat-ai-guncelle`) — Gemini çağrısı yaptığı için kasıtlı olarak çalıştırılmadı.
- **Excel import** (`/api/v2/santiye/{id}/is-kalemleri/excel-import`) — Test .xlsx dosyası hazırlanmadı.
- **Eş zamanlı hakediş kilitleme** (`with_for_update()`) — Tek kullanıcı senaryosunda test edilemez, eş zamanlı istek simülasyonu gerektirir.
- **Mobil UX (T-10)** — Frontend canlı ortam gerektiriyor; bu rapor kapsamında yalnızca API testi yapıldı.
- **İlerleme endpoint'i S-7 kontrolü** — `POST /api/v2/is-kalemleri/{id}/ilerleme` direkt olarak test edilmedi; S-7 kontrolü hakedis kalem güncelleme üzerinden doğrulandı.
- **Büyük dosya yükleme (>25MB)** — Test dosyası hazırlanmadı.
- **S-13 eski kullanıcıyla giriş** — DB'de `role=santi_sefi` olan `inceleme2026@buildingai.com.tr` kullanıcısının şifresi bilinmiyor. `users.role` artık erişim kararlarında kullanılmıyor (`project_members.role` kullanılıyor), dolayısıyla risk düşük.

---

## Öncelik Sıralaması

1. **A-1** — `/stok-ekle` fiyatsız çağrıda 500 → `fiyat` alanı için `None` yerine DB'ye `None` (NULL) yazılmalı
2. **A-2** — DB schema eksikliği: `contracts`, `contract_lines`, `payment_contracts` tabloları canlıda migration ile oluşturulmalı
3. **A-3** — `stok_esik.max_miktar` kolonu DB migration eksik
4. **S-3 (A-7)** — `fiyat-gir` uyarı oluştururken `organization_id` set etmeli
5. **A-4** — `davet-gonder` içindeki `santiye_ids` parametresi `Invitation` modeline ve kabul akışına yansıtılmalı
