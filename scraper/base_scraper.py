"""Ortak scraping altyapısı: HTTP istek, retry, rate-limit, logging."""
import asyncio
import logging
import random
from typing import Any

import httpx

logger = logging.getLogger("buildingai.scraper")

# Gerçek Chrome 124 tarayıcı başlıkları
CHROME_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
        "application/signed-exchange;v=b3;q=0.7"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",   # br (Brotli) yok — httpx paketi desteklemiyor
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

# İstekler arası bekleme (saniye) — bot tespitini önler
REQUEST_DELAY_MIN = 2.0
REQUEST_DELAY_MAX = 3.5

# Retry ayarları
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 5.0   # ilk retry bekleme süresi (saniye)


class BaseScraper:
    """
    Ortak HTTP altyapısı.
    Alt sınıflar `scrape()` metodunu uygular.
    """

    base_url: str = ""
    kaynak: str = ""

    def __init__(self, delay_min: float = REQUEST_DELAY_MIN,
                 delay_max: float = REQUEST_DELAY_MAX) -> None:
        self._delay_min = delay_min
        self._delay_max = delay_max

    # ── HTTP ────────────────────────────────────────────────────

    async def fetch_html(self, url: str, extra_headers: dict[str, str] | None = None) -> str:
        """
        Verilen URL'yi çek, HTML string döndür.
        Geçici hatalar için MAX_RETRIES kez yeniden dener.
        """
        headers = {**CHROME_HEADERS, **(extra_headers or {})}

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                async with httpx.AsyncClient(
                    headers=headers,
                    follow_redirects=True,
                    timeout=30,
                ) as client:
                    resp = await client.get(url)

                if resp.status_code == 200:
                    logger.debug("Fetch OK  %s  (%d bytes)", url, len(resp.content))
                    return resp.text
                elif resp.status_code in (429, 503):
                    wait = RETRY_BACKOFF_BASE * (2 ** (attempt - 1))
                    logger.warning("HTTP %d — %s  (deneme %d/%d, %ds bekleniyor)",
                                   resp.status_code, url, attempt, MAX_RETRIES, int(wait))
                    await asyncio.sleep(wait)
                else:
                    logger.error("HTTP %d — %s", resp.status_code, url)
                    resp.raise_for_status()

            except httpx.TransportError as exc:
                wait = RETRY_BACKOFF_BASE * (2 ** (attempt - 1))
                logger.warning("TransportError %s  (deneme %d/%d, %ds bekleniyor): %s",
                               url, attempt, MAX_RETRIES, int(wait), exc)
                if attempt == MAX_RETRIES:
                    raise
                await asyncio.sleep(wait)

        raise RuntimeError(f"Tüm denemeler başarısız: {url}")

    async def _delay(self) -> None:
        """İstekler arasında rastgele bekleme."""
        wait = random.uniform(self._delay_min, self._delay_max)
        logger.debug("Rate-limit delay: %.1fs", wait)
        await asyncio.sleep(wait)

    # ── Ana arayüz ──────────────────────────────────────────────

    async def scrape(self) -> list[dict[str, Any]]:
        raise NotImplementedError
