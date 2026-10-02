"""
Proemtia gazbeton ürün scraper.

Kaynak: https://www.proemtia.com/urunler/gazbetonlar
Veri: SSR — product-card listesi, 16 ürün, pagination yok.

Başlık formatları:
    "G2/400 Gaz Beton Düz Blok - Adet"          (markasız)
    "G2/350 Gaz Beton Düz Blok - Adet"
    "G3 / 500 Gaz Beton Lento - Adet"
    "Ytong - G2/350 Gaz Beton Düz Blok - Palet"  (markalı)
    "Ytong - G2/400 Gaz Beton Düz Blok - Palet"

Attrs:
    Boyut  → "Genişlik x Yükseklik x Uzunluk" mm,  örn. "50.00x250.00x600.00"
    Kalite → lambda değeri,  örn. "0,10 λ"

Birim: ₺/Adet (tek blok veya palet)

Dönen dict şeması:
    urun_adi_tam      : str
    marka             : str   — "Ytong" veya ""
    sinif             : str   — "G2/400", "G2/350", "G3/500"
    tip               : str   — "Düz Blok", "Lento"
    satis_birimi      : str   — "adet" | "palet"
    boyut_mm          : str   — "50x250x600"  (genişlik x y x z)
    genislik_mm       : float | None   — birinci boyut (duvar kalınlığı)
    lambda_degeri     : str   — "0,10"
    fiyat_kdv_dahil   : float
    fiyat_kdv_haric   : float | None
    para_birimi       : "TRY"
    birim             : "adet"
    satici / satici_slug / konum / pid / urun_url / tarih / kaynak / kaynak_url
"""
import logging
import re
from typing import Any

from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.utils import bugun_iso, parse_product_card_base

logger = logging.getLogger("buildingai.scraper.gazbeton_urun")

_URL = "https://www.proemtia.com/urunler/gazbetonlar"

# "[MARKA - ]SİNİF Gaz Beton TİP - SATIS_BİRİMİ"
_BASLIK_RE = re.compile(
    r"^(?:(?P<marka>.+?)\s+-\s+)?"
    r"(?P<sinif>G\d[\s/\d]+)"
    r"\s+Gaz\s+Beton\s+"
    r"(?P<tip>.+?)"
    r"\s+-\s+(?P<satis_birimi>Adet|Palet)$",
    re.IGNORECASE,
)

# "50.00x250.00x600.00" → genişlik, yükseklik, uzunluk
_BOYUT_RE = re.compile(r"([\d.]+)x([\d.]+)x([\d.]+)", re.IGNORECASE)

# "0,10 λ" → "0,10"
_LAMBDA_RE = re.compile(r"([\d,\.]+)\s*[λΛ]")


def _parse_baslik(baslik: str) -> dict[str, str]:
    m = _BASLIK_RE.match(baslik.strip())
    if not m:
        return {"marka": "", "sinif": "", "tip": baslik, "satis_birimi": "adet"}
    sinif = re.sub(r"\s+", "", m.group("sinif"))   # "G2 /400" → "G2/400"
    return {
        "marka":        (m.group("marka") or "").strip(),
        "sinif":        sinif,
        "tip":          m.group("tip").strip(),
        "satis_birimi": m.group("satis_birimi").lower(),
    }


class GazbetonUrunScraper(BaseScraper):
    base_url = _URL
    kaynak   = "proemtia_urun"

    async def scrape(self) -> list[dict[str, Any]]:
        logger.info("Proemtia gazbeton ürün scrape başlıyor: %s", self.base_url)
        html = await self.fetch_html(self.base_url)
        await self._delay()
        sonuclar = self._parse(html)
        logger.info("Scrape tamamlandı: %d ürün", len(sonuclar))
        return sonuclar

    def _parse(self, html: str) -> list[dict[str, Any]]:
        soup  = BeautifulSoup(html, "html.parser")
        tarih = bugun_iso()

        cards = soup.find_all("a", class_="product-card")
        if not cards:
            raise ValueError("Ürün kartları bulunamadı (class='product-card')")

        total_el = soup.find(id="total-product-result")
        if total_el:
            logger.info("Sayfa toplamı: %s", total_el.get_text(strip=True))

        sonuclar = []
        for card in cards:
            h5 = card.find("h5")
            if not h5:
                continue
            baslik = h5.get_text(strip=True)

            base = parse_product_card_base(card, tarih, self.base_url)
            if base is None:
                logger.warning("Fiyat bulunamadı: %s", baslik)
                continue

            parsed      = _parse_baslik(baslik)
            boyut_raw   = base["attrs"].get("Boyut", "")
            lambda_raw  = base["attrs"].get("Kalite", "")

            # Boyut parse: "50.00x250.00x600.00" → "50x250x600", genislik=50.0
            boyut_mm     = ""
            genislik_mm: float | None = None
            bm = _BOYUT_RE.match(boyut_raw)
            if bm:
                dims = [float(bm.group(i)) for i in (1, 2, 3)]
                boyut_mm    = "x".join(str(int(d)) for d in dims)
                genislik_mm = dims[0]

            # Lambda
            lm = _LAMBDA_RE.search(lambda_raw)
            lambda_degeri = lm.group(1) if lm else lambda_raw

            sonuclar.append({
                "urun_adi_tam":   baslik,
                **parsed,
                "boyut_mm":       boyut_mm,
                "genislik_mm":    genislik_mm,
                "lambda_degeri":  lambda_degeri,
                **base,
            })

        return sonuclar
