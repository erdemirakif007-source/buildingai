"""
Proemtia çimento ürün scraper.

Kaynak: https://www.proemtia.com/urunler/cimentolar
Veri: SSR — product-card listesi, tek sayfa (12 ürün), pagination yok.

HTML yapısı:
    <a class="product-card card" href="/urunler/SLUG?pid=ID&satici=SATICI_SLUG">
      <h5>MARKA - URUN Torba Çimento - BOYUT kg</h5>
      ...
      <span class="success mr-3">SATICI ADI</span>
      <span class="location">ŞEHİR - İLÇE</span>
      <p class="price">70,80 ₺/Adet</p>
      <span class="vat">KDV Hariç: 59,00 ₺/Adet</span>

Dönen dict şeması:
    urun_adi_tam     : str   — "Akçansa - CEM I 42,5 Torba Çimento - 50 kg"
    marka            : str   — "Akçansa"
    urun_adi         : str   — "CEM I 42,5"
    torba_kg         : float — 50.0
    fiyat_kdv_dahil  : float — TRY / torba  (₺/Adet fiyatı)
    fiyat_kdv_haric  : float | None
    para_birimi      : str   — "TRY"
    satici           : str   — "Nokta Çimento"
    satici_slug      : str   — "nokta-cimento"  (URL'den)
    konum            : str   — "İSTANBUL - KADIKÖY"
    pid              : str   — ürün ID
    urun_url         : str
    tarih            : str   — "2026-05-13" (ISO)
    kaynak           : str   — "proemtia_urun"
    kaynak_url       : str
"""
import logging
import re
from typing import Any
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.utils import bugun_iso, parse_fiyat

logger = logging.getLogger("buildingai.scraper.cimento_urun")

_URL      = "https://www.proemtia.com/urunler/cimentolar"
_BASE_URL = "https://www.proemtia.com"

# "MARKA - URUN Torba Çimento - BOYUTkg"  veya  "MARKA - URUN Torba Çimento - BOYUT kg"
_BASLIK_RE = re.compile(
    r"^(?P<marka>.+?)\s+-\s+(?P<urun>.+?)\s+Torba\s+[Çç]imento\s+-\s+(?P<boyut>[\d,\.]+)\s*kg",
    re.IGNORECASE,
)


def _parse_baslik(baslik: str) -> tuple[str, str, float | None]:
    """
    Başlıktan (marka, urun_adi, torba_kg) döndürür.
    Parse edilemezse ham başlığı marka'ya yazar, urun_adi boş, torba_kg None.
    """
    m = _BASLIK_RE.match(baslik.strip())
    if m:
        marka   = m.group("marka").strip()
        urun    = m.group("urun").strip()
        kg_raw  = m.group("boyut").replace(",", ".")
        try:
            kg = float(kg_raw)
        except ValueError:
            kg = None
        return marka, urun, kg
    return baslik.strip(), "", None


def _parse_card(card: Any, tarih: str) -> dict[str, Any] | None:
    href = card.get("href", "")
    full_url = _BASE_URL + href if href.startswith("/") else href

    parsed  = urlparse(href)
    qs      = parse_qs(parsed.query)
    pid     = qs.get("pid",  [""])[0]
    satici_slug = qs.get("satici", [""])[0]

    # Başlık
    h5 = card.find("h5")
    if not h5:
        return None
    baslik = h5.get_text(strip=True)
    marka, urun_adi, torba_kg = _parse_baslik(baslik)

    # Satıcı adı ve konum
    satici_span = card.find("span", class_="success")
    satici = satici_span.get_text(strip=True) if satici_span else ""

    konum_span = card.find("span", class_="location")
    konum = konum_span.get_text(strip=True) if konum_span else ""

    # Fiyat: KDV dahil
    price_p = card.find("p", class_="price")
    if not price_p:
        logger.warning("Fiyat bulunamadı: %s", baslik)
        return None
    fiyat_kdv_dahil = parse_fiyat(price_p.get_text(strip=True))
    if fiyat_kdv_dahil is None:
        logger.warning("Fiyat parse edilemedi: %r  (%s)", price_p.get_text(strip=True), baslik)
        return None

    # Fiyat: KDV hariç (opsiyonel)
    vat_span = card.find("span", class_="vat")
    fiyat_kdv_haric: float | None = None
    if vat_span:
        fiyat_kdv_haric = parse_fiyat(vat_span.get_text(strip=True))

    return {
        "urun_adi_tam":    baslik,
        "marka":           marka,
        "urun_adi":        urun_adi,
        "torba_kg":        torba_kg,
        "fiyat_kdv_dahil": fiyat_kdv_dahil,
        "fiyat_kdv_haric": fiyat_kdv_haric,
        "para_birimi":     "TRY",
        "satici":          satici,
        "satici_slug":     satici_slug,
        "konum":           konum,
        "pid":             pid,
        "urun_url":        full_url,
        "tarih":           tarih,
        "kaynak":          "proemtia_urun",
        "kaynak_url":      _URL,
    }


class CimentoUrunScraper(BaseScraper):
    """Proemtia çimento ürün listesini çeker ve parse eder."""

    base_url = _URL
    kaynak   = "proemtia_urun"

    async def scrape(self) -> list[dict[str, Any]]:
        logger.info("Proemtia çimento ürün scrape başlıyor: %s", self.base_url)
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
            raise ValueError("Ürün kartları HTML'de bulunamadı (class='product-card')")

        # Toplam ürün sayısını logla
        total_el = soup.find(id="total-product-result")
        if total_el:
            logger.info("Sayfa toplamı: %s", total_el.get_text(strip=True))

        sonuclar = []
        for card in cards:
            kayit = _parse_card(card, tarih)
            if kayit:
                sonuclar.append(kayit)

        return sonuclar
