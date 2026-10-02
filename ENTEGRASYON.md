# Hiyerarşi Sayfası — Entegrasyon Talimatları

Bu dosya, yeni hiyerarşi sayfasını mevcut sisteme bağlamak için
`interface.py` ve `scripts.py`'ye yapılması gereken **minimal eklemeleri** açıklar.
Dosyalar dışında `static/hiyerarsi.css`, `static/hiyerarsi.js` zaten oluşturulmuştur.

---

## 1. interface.py — `<head>` Bölümüne CSS + JS Ekle

**Nereye:** `interface.py` satır 24'ten sonra (`Chart.js` script tag'ının hemen altına).

```html
    <link rel="stylesheet" href="/static/hiyerarsi.css">
    <script src="/static/hiyerarsi.js" defer></script>
```

**Tam bağlam (24. satır civarı):**
```html
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
    <!-- ↓ EKLE -->
    <link rel="stylesheet" href="/static/hiyerarsi.css">
    <script src="/static/hiyerarsi.js" defer></script>
    <!-- ↑ EKLE -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
```

---

## 2. interface.py — Sayfa Container Div Ekle

**Nereye:** `id="arsivPage"` div'inin kapanış tag'ından (`</div>`) hemen sonra.

arsivPage satır 1665 civarında başlar. En son kapanış `</div>`'ini bulup hemen ardına ekle:

```html
          <!-- ══════ HİYERARŞİ SAYFASI ══════ -->
          <div id="hiyerarsiPage" style="display:none;flex:1;flex-direction:column;overflow:hidden;background:#F1F5F9;"></div>
```

---

## 3. interface.py — Navigasyon'a Menü Öğesi Ekle

**Nereye:** `id="nav-santiye"` div'inin hemen altına (satır 474-476 civarı).

```html
            <!-- Yapı Hiyerarşisi -->
            <div class="nav-item" id="nav-hiyerarsi" onclick="navGit('hiyerarsi')" style="margin:4px 10px;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink:0;"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="9"/><rect x="14" y="14" width="7" height="4"/></svg>
              Yapı Hiyerarşisi
            </div>
```

---

## 4. interface.py — Şantiye Kartlarına Buton Ekle

Şantiyeler listesinde her kart için "Yapı Hiyerarşisi" butonu:

Şantiye kartı render edilirken (santiyePageAc ya da santiyeRender içinde) her kartın buton grubuna şunu ekle:

```html
<button onclick="localStorage.setItem('bai_aktif_santiye', '${s.id}'); localStorage.setItem('bai_aktif_santiye_ad', '${s.ad}'); navGit('hiyerarsi');"
        style="...mevcut buton stili...">
  🏗️ Yapı Hiyerarşisi
</button>
```

> **Not:** `${s.id}` ve `${s.ad}` şantiye objesinin alanlarıdır — şantiye kartı template'ine göre uyarla.

---

## 5. scripts.py — PAGE_TITLES Objesine Ekle

**Nereye:** `scripts.py` satır 2746 civarı, `sesli: '...'` satırından sonra.

```javascript
    hiyerarsi: '🏗️ Yapı Hiyerarşisi',
```

**Tam bağlam:**
```javascript
const PAGE_TITLES = {
    home: '🏠 Ana Sayfa',
    kamera: '📷 Kamera Analizi',
    'saha-kayitlari': 'Saha Kayıtları',
    hesaplama: '🧮 Hesaplama',
    arsiv: '📁 Arşiv',
    gunluk: '📝 Günlük Rapor',
    sesli: '🎤 Sesli Rapor',
    hiyerarsi: '🏗️ Yapı Hiyerarşisi',   // ← EKLE
};
```

---

## 6. scripts.py — navGit() Fonksiyonuna Case Ekle

**Nereye:** `scripts.py` satır 2770 civarı, `santiyePageAc()` satırından hemen önce.

```javascript
    else if (page === 'hiyerarsi') hiyerarsiPageAc();
```

**Tam bağlam:**
```javascript
    else if (page === 'stok') stokPageAc();
    else if (page === 'deprem') depremModalAc();
    else if (page === 'hiyerarsi') hiyerarsiPageAc();   // ← EKLE
    else if (page === 'santiye') santiyePageAc();
```

---

## 7. scripts.py — navGit() home Case'ine Kapat Ekle

`navGit` içindeki `else` (home) bloğuna `hiyerarsiPageKapat()` çağrısı ekle:

**Tam bağlam:**
```javascript
    else {
        santiyePageKapat();
        fiyatPageKapat();
        stokPageKapat();
        sahaKayitlariPageKapat();
        kameraPageKapat();
        arsivKapat();
        hiyerarsiPageKapat();   // ← EKLE
    }
```

---

## Özet Kontrol Listesi

| # | Dosya | Eylem | Bitti mi? |
|---|---|---|---|
| 1 | interface.py | `<head>`'e CSS + JS link ekle | ☐ |
| 2 | interface.py | `<div id="hiyerarsiPage">` ekle | ☐ |
| 3 | interface.py | Navigasyona menü öğesi ekle | ☐ |
| 4 | interface.py | Şantiye kartlarına hiyerarşi butonu ekle | ☐ |
| 5 | scripts.py | `PAGE_TITLES`'a `hiyerarsi` ekle | ☐ |
| 6 | scripts.py | `navGit()`'e `hiyerarsiPageAc()` case'i ekle | ☐ |
| 7 | scripts.py | `navGit()` home bloğuna `hiyerarsiPageKapat()` ekle | ☐ |

---

## Test Adımları

1. Sunucuyu başlat: `uvicorn app:app --reload`
2. Migration çalıştır (daha önce çalıştırılmadıysa): `python migrate_hierarchy.py`
3. Tarayıcıda `/app`'e gir, sol menüde **Yapı Hiyerarşisi** görünmeli
4. Şantiye seç → Yapı Hiyerarşisi butonuna tıkla
5. **Bina Ekle** → bina oluştur → sol ağaçta görünmeli
6. Binaya tıkla → **Kat Ekle** → kat oluştur
7. Kata tıkla → **Mahal Ekle** → mahal oluştur
8. Mahale tıkla → sağda **İş Kalemi Ekle** → form doldur → kaydet
9. İlerleme yüzdesine tıkla → ilerleme kaydı ekle
10. **Excel'den Yükle** → test .xlsx yükle → başarı/hata raporu gör
