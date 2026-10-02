"""
Proemtia filmasin endeks scraper.

Kaynak: https://www.proemtia.com/endeks/celik-hasir-ve-filmasin/filmasin-fiyatlari
Veri: SSR archive-table. Normal scrape yalnizca guncel satiri, backfill tum
gecmis fiyat serisini dondurur.

Not: Filmasin fiyati USD/ton cinsinden yayimlanir. DB yazim katmani runner
icinde TRY'ye cevirir.
"""
import logging
from typing import Any

from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.utils import parse_archive_table

logger = logging.getLogger("buildingai.scraper.filmasin_endeks")

_URL = (
    "https://www.proemtia.com/endeks/celik-hasir-ve-filmasin"
    "/filmasin-fiyatlari"
)


class FilmasinEndeksScraper(BaseScraper):
    """Proemtia filmasin fiyat endeksini ceker ve parse eder."""

    base_url = _URL
    kaynak = "proemtia_endeks"

    async def scrape(self) -> list[dict[str, Any]]:
        logger.info("Proemtia filmasin endeks scrape basliyor: %s", self.base_url)
        html = await self.fetch_html(self.base_url)
        await self._delay()

        sonuclar = self._parse(html, full_history=False)
        logger.info("Scrape tamamlandi: %d fiyat kaydi", len(sonuclar))
        return sonuclar

    async def scrape_backfill(self) -> list[dict[str, Any]]:
        logger.info("Proemtia filmasin backfill scrape basliyor: %s", self.base_url)
        html = await self.fetch_html(self.base_url)
        await self._delay()

        sonuclar = self._parse(html, full_history=True)
        logger.info("Backfill scrape tamamlandi: %d fiyat kaydi", len(sonuclar))
        return sonuclar

    def _parse(self, html: str, full_history: bool = False) -> list[dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        satirlar = parse_archive_table(soup)

        if not satirlar:
            raise ValueError("Filmasin fiyat tablosu HTML'de bulunamadi")

        sonuclar = []
        for satir in (satirlar if full_history else satirlar[:1]):
            sonuclar.append({
                "malzeme_ad": "Filmaşin",
                "referans_merkez_kod": None,
                "fiyat": satir["fiyat"],
                "para_birimi": satir["para_birimi"],
                "kdv_dahil": False,
                "tarih": satir["tarih"],
                "kaynak": self.kaynak,
                "kaynak_url": self.base_url,
            })
        return sonuclar
