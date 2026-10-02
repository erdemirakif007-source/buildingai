"""
TCMB (Türkiye Cumhuriyet Merkez Bankası) döviz kuru çekici.

Kaynak: https://www.tcmb.gov.tr/kurlar/today.xml
- Ücretsiz, API key gerektirmez.
- Hafta içi ~09:30'da güncellenir; hafta sonu önceki iş gününün kuru döner.
- Hata / erişim sorunu durumunda sabit varsayılan kur kullanılır.

Kullanım:
    from scraper.tcmb_kur import usd_try_kur
    kur = await usd_try_kur()          # örn. 45.42
"""
import asyncio
import datetime
import logging
import xml.etree.ElementTree as ET

import httpx

logger = logging.getLogger("buildingai.scraper.tcmb_kur")

_TCMB_URL      = "https://www.tcmb.gov.tr/kurlar/today.xml"
_KUR_VARSAYILAN = 38.50          # runner.py'deki sabit ile aynı — fallback
_TTL_SANIYE    = 3600            # 1 saat önbellek

# Basit bellek önbelleği: (kur_degeri, zaman_damgasi)
_cache: tuple[float, datetime.datetime] | None = None
_cache_lock = asyncio.Lock()


async def usd_try_kur(fallback: float = _KUR_VARSAYILAN) -> float:
    """
    Güncel USD/TRY ForexSelling kurunu döndürür.
    TCMB'ye erişilemezse `fallback` değerini döner.
    Sonuç 1 saat önbelleğe alınır.
    """
    global _cache

    async with _cache_lock:
        now = datetime.datetime.now()
        if _cache is not None:
            kur, zaman = _cache
            if (now - zaman).total_seconds() < _TTL_SANIYE:
                logger.debug("TCMB kur önbellekten: %.4f", kur)
                return kur

        kur = await _fetch_kur(fallback)
        _cache = (kur, now)
        return kur


async def _fetch_kur(fallback: float) -> float:
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            resp = await client.get(
                _TCMB_URL,
                headers={"User-Agent": "BuildingAI/1.0 (fiyat-takip; +https://buildingai.com.tr)"},
            )
            resp.raise_for_status()
            kur = _parse_usd_xml(resp.text)
            logger.info("TCMB USD/TRY kuru alındı: %.4f", kur)
            return kur
    except Exception as exc:
        logger.warning("TCMB kur alınamadı (%s: %s), varsayılan kullanılıyor: %.2f",
                       type(exc).__name__, exc, fallback)
        return fallback


def _parse_usd_xml(xml_text: str) -> float:
    """TCMB XML'inden USD ForexSelling kurunu çeker."""
    root = ET.fromstring(xml_text)
    for currency in root.findall("Currency"):
        code = currency.get("CurrencyCode") or currency.get("Kod", "")
        if code.upper() != "USD":
            continue
        # ForexSelling tercih edilir; yoksa ForexBuying
        for tag in ("ForexSelling", "ForexBuying"):
            el = currency.find(tag)
            if el is not None and el.text and el.text.strip():
                return float(el.text.strip())
    raise ValueError("USD kuru XML'de bulunamadı")
