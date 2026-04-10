"""
Şantiye Beyin Merkezi — Real Data + PDF RAG Engine
────────────────────────────────────────────────────────
Adım 1: read_documents()    → data/ klasöründeki PDF'leri pdfplumber ile okur
Adım 2: check_live_status() → gercek_veri.json'dan stok/ekip/hava okur
Adım 3: generate_response() → RAG + gerçek veri + hafıza → Gemini sentezi
"""
import json
import datetime
import logging
from pathlib import Path
from typing import List

try:
    import pdfplumber  # type: ignore
    _PDF_OK = True
except ImportError:
    _PDF_OK = False

logger = logging.getLogger("buildingai")

# Şantiye verisi dosyası — proje kökünde
GERCEK_VERI_PATH = Path("gercek_veri.json")

# Boş veri şablonu (dosya yoksa veya bozuksa bu döner)
_BOŞ_VERİ: dict = {
    "stok":  {},
    "hava":  {"durum": "Veri girilmedi", "sicaklik": None, "ruzgar": "—", "nem": "—"},
    "ekip":  {},
    "notlar": "",
}

# PDF metin önbelleği: {dosya_adı: (mtime, metin)}
_pdf_cache: dict = {}

# PDF başına maksimum karakter (Gemini context limitini aşmamak için)
_PDF_MAX_CHARS = 4000


class ŞantiyeAgent:
    """
    Şantiye Karar Destek Sistemi AI Ajanı.
    ai_client: google.genai.Client (app.py'den enjekte edilir)
    """

    def __init__(self, ai_client=None):
        self.ai_client = ai_client
        self.data_dir = Path("Yönetmelikler")

    # ─────────────────────────────────────────────────────────────────────
    # 1. GERÇEK PDF OKUMA — RAG Motoru
    # ─────────────────────────────────────────────────────────────────────
    def _pdf_klasoru_oku(self, klasor: Path, result: dict) -> None:
        """Bir klasördeki PDF'leri okuyup result'a ekler (in-place)."""
        if not klasor.exists() or not _PDF_OK:
            return
        for f in sorted(klasor.iterdir()):
            if f.suffix.lower() != ".pdf":
                continue
            cache_key = str(f)
            result["pdf"].append(f.name)
            current_mtime = f.stat().st_mtime
            cached_mtime, cached_text = _pdf_cache.get(cache_key, (None, ""))
            if cached_mtime == current_mtime and cached_text:
                result["icerikler"][f.name] = cached_text
                continue
            try:
                parcalar: list[str] = []
                with pdfplumber.open(f) as pdf:
                    for sayfa in pdf.pages:
                        metin = sayfa.extract_text() or ""
                        parcalar.append(metin.strip())
                        if sum(len(p) for p in parcalar) >= _PDF_MAX_CHARS:
                            break
                tam_metin = "\n".join(parcalar)
                kisaltilmis = tam_metin[:_PDF_MAX_CHARS]  # type: ignore[misc]
                if len(tam_metin) > _PDF_MAX_CHARS:
                    kisaltilmis += "\n[... belge devam ediyor ...]"
                _pdf_cache[cache_key] = (current_mtime, kisaltilmis)
                icerikler: dict = result["icerikler"]  # type: ignore[assignment]
                icerikler[f.name] = kisaltilmis
                result["icerikler"] = icerikler
                logger.info(f"[RAG] {f.name} okundu — {len(kisaltilmis)} karakter")
            except Exception as exc:
                logger.error(f"[RAG] {f.name} okunamadı: {exc}")
                result["icerikler"][f.name] = f"[Okuma hatası: {exc}]"

    def read_documents(self, santiye_id: int = None) -> dict:  # type: ignore[assignment]
        """
        PDF RAG motoru. İki katmanlı okuma:
          1. self.data_dir (Yönetmelikler/) — her zaman okunur
          2. data/{santiye_id}/ — şantiyeye özel; yoksa data/ ortak klasörü
        """
        result: dict = {
            "pdf": [],
            "loaded": False,
            "ozet": "",
            "icerikler": {},
        }

        if not _PDF_OK:
            logger.warning("[RAG] pdfplumber yüklü değil — pip install pdfplumber")
            return result

        # Katman 1: Genel yönetmelikler (Yönetmelikler/)
        self._pdf_klasoru_oku(self.data_dir, result)

        # Katman 2: Şantiyeye özel belgeler
        if santiye_id is not None:
            ozel_dir = Path(f"data/{santiye_id}")
            ortak_dir = Path("data")
            if ozel_dir.exists():
                self._pdf_klasoru_oku(ozel_dir, result)
                logger.info(f"[RAG] Şantiye #{santiye_id} özel klasörü okundu.")
            elif ortak_dir.exists():
                self._pdf_klasoru_oku(ortak_dir, result)
                logger.info("[RAG] Ortak data/ klasörü okundu (şantiyeye özel yoktu).")

        toplam_pdf = len(result["pdf"])
        result["loaded"] = toplam_pdf > 0
        if toplam_pdf:
            result["ozet"] = (
                f"{toplam_pdf} PDF — "
                + ", ".join(result["pdf"])
                + " — içerikler RAG belleğine alındı."
            )

        return result

    # ─────────────────────────────────────────────────────────────────────
    # 2. GERÇEK VERİ — gercek_veri.json
    # ─────────────────────────────────────────────────────────────────────
    def check_live_status(self) -> dict:
        """
        gercek_veri.json dosyasını okur.
        Dosya yoksa veya bozuksa boş veri şablonu döner.
        Güncelleme zamanı dosyadaki 'tarih_guncelleme' alanından alınır.
        """
        if not GERCEK_VERI_PATH.exists():
            logger.info("[LIVE] gercek_veri.json bulunamadı — boş şablon kullanılıyor.")
            return self._bos_durum("gercek_veri.json henüz oluşturulmamış.")

        try:
            raw = GERCEK_VERI_PATH.read_text(encoding="utf-8").strip()
            if not raw:
                return self._bos_durum("gercek_veri.json boş — lütfen veri girin.")

            veri: dict = json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.error(f"[LIVE] gercek_veri.json JSON hatası: {exc}")
            return self._bos_durum(f"JSON format hatası: {exc}")

        stok  = veri.get("stok",  {})
        hava  = veri.get("hava",  _BOŞ_VERİ["hava"])
        ekip  = veri.get("ekip",  {})
        notlar = veri.get("notlar", "")

        # Güncelleme tarih/saati
        guncelleme = veri.get(
            "tarih_guncelleme",
            datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        )

        # Güvenli kritik kontrol (boş stok/hava'ya karşı)
        kritik = self._kritik_kontrol(stok, hava)

        durum = {
            "tarih":         guncelleme,
            "stok":          stok,
            "hava":          hava,
            "ekip":          ekip,
            "notlar":        notlar,
            "kritik_uyari":  kritik,
            "kaynak":        "gercek_veri.json",
        }
        logger.info(f"[LIVE] Veri okundu — güncelleme: {guncelleme}")
        return durum

    def _bos_durum(self, mesaj: str) -> dict:
        return {
            "tarih":        datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
            "stok":         {},
            "hava":         {"durum": "Veri girilmedi", "sicaklik": None, "ruzgar": "—", "nem": "—"},
            "ekip":         {},
            "notlar":       mesaj,
            "kritik_uyari": [f"ℹ️ {mesaj}"],
            "kaynak":       "—",
        }

    def _kritik_kontrol(self, stok: dict, hava: dict) -> List[str]:
        uyarilar: List[str] = []

        # Stok kontrolleri (alan adları gercek_veri.json'dakiyle eşleşmeli)
        cimento = stok.get("Çimento (ton)")
        if isinstance(cimento, (int, float)) and cimento < 15:
            uyarilar.append("⚠️ Çimento stoğu kritik — acil sipariş gerekiyor.")

        demir = stok.get("Demir (kg)")
        if isinstance(demir, (int, float)) and demir < 1000:
            uyarilar.append("⚠️ Demir stoğu düşük — sipariş verilmeli.")

        # Hava kontrolleri
        hava_durum = hava.get("durum", "")
        if any(k in hava_durum for k in ("Yağmurlu", "Karlı", "Fırtına")):
            uyarilar.append("🌧️ Yağış/Kar — açık beton dökümü uygun değil.")

        ruzgar_str = str(hava.get("ruzgar", "0 km/s"))
        try:
            ruzgar_kmh = int(ruzgar_str.split()[0])
            if ruzgar_kmh > 32:
                uyarilar.append("💨 Şiddetli rüzgar — vinç operasyonunu durdur.")
        except (ValueError, IndexError):
            pass

        sicaklik = hava.get("sicaklik")
        if isinstance(sicaklik, (int, float)):
            if sicaklik > 32:
                uyarilar.append("🔥 Aşırı sıcak — beton kür sürelerini artır.")
            if sicaklik < 5:
                uyarilar.append("❄️ Donma riski — beton/şap için ısıtma ve örtme tedbirleri al.")

        return uyarilar

    # ─────────────────────────────────────────────────────────────────────
    # 3. ANA YANIT MOTORU
    # ─────────────────────────────────────────────────────────────────────
    async def generate_response(
        self,
        soru: str,
        gecmis: list,
        ai_client=None,
        santiye_id: int = None,  # type: ignore[assignment]
    ) -> dict:
        """
        Agentic workflow:
          Adım 1 → PDF RAG (gerçek içerik)
          Adım 2 → Gerçek şantiye durumu (gercek_veri.json)
          Adım 3 → Konuşma hafızası (son 4 mesaj)
          Adım 4 → Gemini 2.5 Flash sentezi
        """
        client = ai_client or self.ai_client

        # Adım 1 — Gerçek PDF RAG
        docs = self.read_documents(santiye_id=santiye_id)
        if docs["loaded"] and docs["icerikler"]:
            pdf_metinleri = "\n\n---\n\n".join(
                f"📄 {ad}:\n{metin}"
                for ad, metin in docs["icerikler"].items()
            )
            doc_blok = f"📂 Şantiye Dokümanları (RAG):\n{pdf_metinleri}"
        else:
            doc_blok = "📂 data/ klasöründe henüz PDF yok — genel inşaat mühendisliği bilginle yanıt ver."

        # Adım 2 — Gerçek veri
        canli = self.check_live_status()
        uyari_str = " | ".join(canli["kritik_uyari"]) if canli["kritik_uyari"] else "✅ Kritik uyarı yok."

        stok_str = (
            ", ".join(f"{k}: {v}" for k, v in canli["stok"].items())
            if canli["stok"] else "Stok verisi girilmedi"
        )
        ekip_str = (
            ", ".join(f"{k}: {v}" for k, v in canli["ekip"].items())
            if canli["ekip"] else "Ekip verisi girilmedi"
        )

        hava = canli["hava"]
        hava_str = (
            f"{hava.get('durum','—')} {hava.get('sicaklik','?')}°C  "
            f"Rüzgar: {hava.get('ruzgar','—')}  Nem: {hava.get('nem','—')}"
        )

        canli_blok = (
            f"📡 Anlık Şantiye ({canli['tarih']}) [Kaynak: {canli['kaynak']}]\n"
            f"  Hava : {hava_str}\n"
            f"  Stok : {stok_str}\n"
            f"  Ekip : {ekip_str}\n"
            f"  Notlar: {canli.get('notlar','—')}\n"
            f"  Uyarılar: {uyari_str}"
        )

        # Adım 3 — Hafıza bağlamı
        hafiza_blok = ""
        if gecmis:
            son = list(gecmis)[-4:]  # type: ignore[arg-type]
            hafiza_blok = "🧠 Önceki konuşma:\n" + "\n".join(
                f"  {'Kullanıcı' if m['rol'] == 'user' else 'AI'}: {m['icerik']}"
                for m in son
            )

        # Adım 4 — Prompt
        sistem_prompt = f"""Sen BuildingAI'ın Şantiye Karar Destek Sistemi'nin AI ajanısın.
Deneyimli bir inşaat mühendisi gibi — kısa, net, aksiyona odaklı yanıtlar ver.
Türkçe yanıt ver. Markdown kullan (## başlık kullanma, sadece **kalın** ve - madde).

{doc_blok}

{canli_blok}

{hafiza_blok}

Kullanıcı: {soru}

Yanıt (max 3 madde + 1 net aksiyon önerisi, toplam 120 kelimeyi geçme):"""

        if client:
            try:
                resp = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=sistem_prompt,
                )
                cevap = resp.text
            except Exception as exc:
                cevap = f"⚠️ AI bağlantı hatası: {exc}"
        else:
            cevap = self._mock_cevap(soru, canli)

        return {
            "cevap":       cevap,
            "canli_durum": canli,
            "kaynak":      "RAG+Gerçek" if docs["loaded"] else "Gerçek Veri",
        }

    def _mock_cevap(self, soru: str, canli: dict) -> str:
        uyari_str = (
            " | ".join(canli["kritik_uyari"])
            if canli["kritik_uyari"]
            else "✅ Kritik uyarı yok."
        )
        stok_ilk = next(iter(canli["stok"].items()), ("—", "—")) if canli["stok"] else ("—", "—")
        return (
            f"**Şantiye AI — Offline Mod**\n\n"
            f"Sorunuz: _{soru}_\n\n"
            f"- Hava: {canli['hava'].get('durum','?')}, {canli['hava'].get('sicaklik','?')}°C\n"
            f"- {stok_ilk[0]}: {stok_ilk[1]}\n"
            f"- Notlar: {canli.get('notlar','—')}\n\n"
            f"**Uyarılar:** {uyari_str}\n\n"
            f"_Gemini API bağlantısı pasif. GEMINI_API_KEY değerini kontrol edin._"
        )
