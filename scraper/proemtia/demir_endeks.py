"""
Proemtia demir endeks scraper.

Normal scrape ana endeks sayfasindan guncel 7 merkez x 3 cap fiyatini ceker.
Backfill ise il/merkez sayfalarini tek tek gezerek tarihsel tabloyu ceker.
"""
import logging
import re
from typing import Any

from bs4 import BeautifulSoup

from scraper.base_scraper import BaseScraper
from scraper.utils import bugun_iso, parse_fiyat, parse_tarih_tr

logger = logging.getLogger("buildingai.scraper.demir_endeks")

_BASE_URL = "https://www.proemtia.com/endeks/demir-fiyatlari"

_SLUG_TO_KOD: dict[str, str] = {
    "ankara": "ankara",
    "biga": "biga",
    "gebze": "gebze",
    "iskenderun-payas": "iskenderun_payas",
    "istanbul": "istanbul",
    "izmir": "izmir",
    "karabuk": "karabuk",
}

_KOD_TO_AD: dict[str, str] = {
    "ankara": "Ankara",
    "biga": "Biga",
    "gebze": "Gebze",
    "iskenderun_payas": "İskenderun Payas",
    "istanbul": "İstanbul",
    "izmir": "İzmir",
    "karabuk": "Karabük",
}

_MALZEME_ADLARI = [
    "Nervürlü Demir Ø8",
    "Nervürlü Demir Ø10",
    "Nervürlü Demir Ø12",
]

_ICON_TO_DEGISIM: dict[str, str] = {
    "icon-up": "yukari",
    "icon-down": "asagi",
    "icon-pause": "sabit",
}


class DemirEndeksScraper(BaseScraper):
    """Proemtia demir fiyat endeksini ceker ve parse eder."""

    base_url = _BASE_URL
    kaynak = "proemtia_endeks"

    async def scrape(self) -> list[dict[str, Any]]:
        logger.info("Proemtia demir endeks scrape basliyor: %s", self.base_url)
        html = await self.fetch_html(self.base_url)
        await self._delay()

        sonuclar = self._parse_table(html)
        logger.info("Scrape tamamlandi: %d fiyat kaydi", len(sonuclar))
        return sonuclar

    async def scrape_backfill(self) -> list[dict[str, Any]]:
        logger.info("Proemtia demir backfill scrape basliyor")
        sonuclar: list[dict[str, Any]] = []

        for slug, merkez_kod in _SLUG_TO_KOD.items():
            url = f"{self.base_url}/{slug}"
            html = await self.fetch_html(url)
            await self._delay()
            merkez_sonuclari = self._parse_history_table(
                html=html,
                merkez_kod=merkez_kod,
                merkez_ad=_KOD_TO_AD.get(merkez_kod, slug.replace("-", " ").title()),
                kaynak_url=url,
            )
            logger.info(
                "Demir backfill merkez=%s url=%s kayit=%d",
                merkez_kod,
                url,
                len(merkez_sonuclari),
            )
            sonuclar.extend(merkez_sonuclari)

        logger.info("Demir backfill tamamlandi: %d fiyat kaydi", len(sonuclar))
        return sonuclar

    def _parse_table(self, html: str) -> list[dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        tarih = self._extract_tarih(soup)

        tablo = soup.find("table", class_="price-list")
        if not tablo:
            raise ValueError("Fiyat tablosu HTML'de bulunamadi (class='price-list')")

        sonuclar: list[dict[str, Any]] = []

        for satir in tablo.select("tbody tr"):
            hucreler = satir.find_all("td")
            if len(hucreler) < 4:
                continue

            link = hucreler[0].find("a")
            if not link:
                continue

            merkez_ad = link.get_text(strip=True)
            href = link.get("href", "")
            slug = href.rstrip("/").split("/")[-1]
            merkez_kod = _SLUG_TO_KOD.get(slug)
            if not merkez_kod:
                logger.warning("Bilinmeyen merkez slug: %s", slug)
                continue

            for idx, malzeme_ad in enumerate(_MALZEME_ADLARI, start=1):
                parsed = self._parse_price_cell(hucreler[idx])
                if not parsed:
                    continue
                fiyat, degisim = parsed
                sonuclar.append({
                    "merkez_kod": merkez_kod,
                    "merkez_ad": merkez_ad,
                    "malzeme_ad": malzeme_ad,
                    "fiyat": fiyat,
                    "kdv_dahil": True,
                    "degisim": degisim,
                    "tarih": tarih,
                    "kaynak": self.kaynak,
                    "kaynak_url": self.base_url,
                })

        return sonuclar

    def _parse_history_table(
        self,
        html: str,
        merkez_kod: str,
        merkez_ad: str,
        kaynak_url: str,
    ) -> list[dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        sonuclar: list[dict[str, Any]] = []
        text_sonuclar = self._parse_history_text(
            soup=soup,
            merkez_kod=merkez_kod,
            merkez_ad=merkez_ad,
            kaynak_url=kaynak_url,
        )

        for tablo in soup.find_all("table"):
            rows = tablo.select("tbody tr") or tablo.find_all("tr")
            for satir in rows:
                hucreler = satir.find_all("td")
                if len(hucreler) < 4:
                    continue

                tarih = self._extract_row_date(satir, hucreler[0])
                if not tarih:
                    continue

                for idx, malzeme_ad in enumerate(_MALZEME_ADLARI, start=1):
                    parsed = self._parse_price_cell(hucreler[idx])
                    if not parsed:
                        continue
                    fiyat, degisim = parsed
                    sonuclar.append({
                        "merkez_kod": merkez_kod,
                        "merkez_ad": merkez_ad,
                        "malzeme_ad": malzeme_ad,
                        "fiyat": fiyat,
                        "kdv_dahil": True,
                        "degisim": degisim,
                        "tarih": tarih,
                        "kaynak": self.kaynak,
                        "kaynak_url": kaynak_url,
                    })

            if sonuclar:
                break

        if len(text_sonuclar) > len(sonuclar):
            return text_sonuclar

        if not sonuclar:
            logger.warning("Demir gecmis tablosu bulunamadi: %s", kaynak_url)

        sonuclar.sort(key=lambda r: (r["tarih"], r["merkez_kod"], r["malzeme_ad"]), reverse=True)
        return sonuclar

    def _parse_history_text(
        self,
        soup: BeautifulSoup,
        merkez_kod: str,
        merkez_ad: str,
        kaynak_url: str,
    ) -> list[dict[str, Any]]:
        text = soup.get_text(" ", strip=True)
        pattern = re.compile(
            r"(\d{1,2}[./]\d{1,2}[./]\d{4})\s+"
            r"([\d.,]+)\s*TL\s+"
            r"([\d.,]+)\s*TL\s+"
            r"([\d.,]+)\s*TL"
        )
        sonuclar: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()

        for match in pattern.finditer(text):
            tarih = parse_tarih_tr(match.group(1))
            if not tarih:
                continue

            for idx, malzeme_ad in enumerate(_MALZEME_ADLARI, start=2):
                fiyat = parse_fiyat(match.group(idx))
                if fiyat is None:
                    continue

                key = (tarih, malzeme_ad)
                if key in seen:
                    continue
                seen.add(key)

                sonuclar.append({
                    "merkez_kod": merkez_kod,
                    "merkez_ad": merkez_ad,
                    "malzeme_ad": malzeme_ad,
                    "fiyat": fiyat,
                    "kdv_dahil": True,
                    "degisim": "sabit",
                    "tarih": tarih,
                    "kaynak": self.kaynak,
                    "kaynak_url": kaynak_url,
                })

        sonuclar.sort(key=lambda r: (r["tarih"], r["merkez_kod"], r["malzeme_ad"]), reverse=True)
        return sonuclar

    def _parse_price_cell(self, hucre) -> tuple[float, str] | None:
        fiyat_div = hucre.find("div", class_="last-price") or hucre
        degisim_icon = ""
        em = fiyat_div.find("em")
        if em:
            for cls in em.get("class", []):
                if cls in _ICON_TO_DEGISIM:
                    degisim_icon = cls
                    break
            em.decompose()

        fiyat_raw = fiyat_div.get_text(" ", strip=True)
        fiyat = parse_fiyat(fiyat_raw)
        if fiyat is None:
            return None
        return fiyat, _ICON_TO_DEGISIM.get(degisim_icon, "sabit")

    def _extract_row_date(self, satir, tarih_hucre) -> str | None:
        data_date = (satir.get("data-date") or "").strip()
        if re.match(r"\d{4}-\d{2}-\d{2}$", data_date):
            return data_date

        tarih_text = tarih_hucre.get_text(" ", strip=True)
        parsed = parse_tarih_tr(tarih_text)
        if parsed:
            return parsed

        m = re.search(r"(\d{2}[./]\d{2}[./]\d{4})", tarih_text)
        if m:
            return parse_tarih_tr(m.group(1))
        return None

    def _extract_tarih(self, soup: BeautifulSoup) -> str:
        text = soup.get_text(separator=" ")
        m = re.search(r"Son\s+G[üu]ncelleme\s+Tarihi[:\s]+(\d{2}[./]\d{2}[./]\d{4})", text, re.IGNORECASE)
        if m:
            parsed = parse_tarih_tr(m.group(1))
            if parsed:
                return parsed
        return bugun_iso()
