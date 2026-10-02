"""
Proemtia kum ürün scraper.

Kaynak: https://www.proemtia.com/urunler/kumlar
Veri: SSR — product-card listesi, 8 ürün, pagination yok.

Başlık formatı (marka yoktur):
    "0,5 Şap Kumu"
    "Kaba Sıva Kumu"

Attrs:
    Boyut  → ambalaj ağırlığı (ton)   örn. "0.05", "1.00"
    Kalite → "Standart"

Birim: ₺/Ton

Dönen dict şeması:
    urun_adi_tam     : str
    urun_adi         : str   — başlığın normalize hali
    kum_turu         : str   — "sap" | "kaba" | "diger"
    ambalaj_ton      : float | None
    fiyat_kdv_dahil  : float
    fiyat_kdv_haric  : float | None
    para_birimi      : "TRY"
    birim            : "ton"
    satici / satici_slug / konum / pid / urun_url / tarih / kaynak / kaynak_url
"""
import logging
import re
from typing import Any

from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.utils import bugun_iso, parse_fiyat, parse_product_card_base

logger = logging.getLogger("buildingai.scraper.kum_urun")

_URL = "https://www.proemtia.com/urunler/kumlar"

# Başlık → kum türü eşleştirmesi
_KUM_TURU: list[tuple[re.Pattern, str]] = [
    (re.compile(r"şap\s+kumu",  re.I), "sap"),
    (re.compile(r"kaba",        re.I), "kaba"),
]


def _kum_turu(baslik: str) -> str:
    for pat, tur in _KUM_TURU:
        if pat.search(baslik):
            return tur
    return "diger"


class KumUrunScraper(BaseScraper):
    base_url = _URL
    kaynak   = "proemtia_urun"

    async def scrape(self) -> list[dict[str, Any]]:
        logger.info("Proemtia kum ürün scrape başlıyor: %s", self.base_url)
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

            ambalaj_ton: float | None = None
            boyut_raw = base["attrs"].get("Boyut", "")
            if boyut_raw:
                try:
                    ambalaj_ton = float(boyut_raw.replace(",", "."))
                except ValueError:
                    pass

            sonuclar.append({
                "urun_adi_tam":    baslik,
                "urun_adi":        baslik,
                "kum_turu":        _kum_turu(baslik),
                "ambalaj_ton":     ambalaj_ton,
                **base,
            })

        return sonuclar
