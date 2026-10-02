"""
Faz 1 fiyat takip scraper runner.

Tüm aktif scraper'ları sırayla çalıştırır ve sonuçları scrape_fiyatlar
tablosuna yazar.

Kullanım:
    python scraper/runner.py           # standart çalıştırma
    python scraper/runner.py --dry-run # DB'ye yazmadan test
    python scraper/runner.py --usd-kur 45.42  # manuel kur geçersiz kıl

Railway cron: "0 3 * * 1"  (Her Pazartesi 03:00 UTC)
"""
import asyncio
import io
import logging
import sys
import os
import argparse
import datetime
import sqlite3

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
if isinstance(sys.stderr, io.TextIOWrapper):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("buildingai.scraper.runner")

from scraper.proemtia.demir_endeks    import DemirEndeksScraper
from scraper.proemtia.hasir_endeks    import HasirEndeksScraper
from scraper.proemtia.filmasin_endeks import FilmasinEndeksScraper
from scraper.proemtia.cimento_urun    import CimentoUrunScraper
from scraper.proemtia.kum_urun        import KumUrunScraper
from scraper.proemtia.gazbeton_urun   import GazbetonUrunScraper
from scraper.db_writer import (
    get_connection,
    load_malzeme_map,
    load_merkez_map,
    kaydet_endeks,
    kaydet_urun_cimento,
    kaydet_urun_kum,
    kaydet_urun_gazbeton,
    usd_to_try,
    USD_KUR_VARSAYILAN,
)
from scraper.tcmb_kur import usd_try_kur

# Scraper'lar arası ek bekleme (saniye) — Proemtia rate limit
_SCRAPER_DELAY = 3.0


# ── Scraper görevleri ────────────────────────────────────────────────────────

async def _calistir_scraper(ad: str, scraper_cls) -> list[dict] | None:
    """Scraper'ı çalıştırır; hata olursa None döndürür ve loglar."""
    try:
        logger.info("Başlıyor: %s", ad)
        sonuc = await scraper_cls().scrape()
        logger.info("Tamamlandı: %s — %d kayıt", ad, len(sonuc))
        return sonuc
    except Exception as exc:
        logger.error("HATA: %s — %s: %s", ad, type(exc).__name__, exc, exc_info=True)
        return None


async def _calistir_backfill(ad: str, scraper_cls) -> list[dict] | None:
    """Scraper'in tarihsel backfill modunu calistirir; hata olursa loglar."""
    try:
        logger.info("Backfill basliyor: %s", ad)
        sonuc = await scraper_cls().scrape_backfill()
        logger.info("Backfill tamamlandi: %s - %d kayit", ad, len(sonuc))
        return sonuc
    except Exception as exc:
        logger.error("BACKFILL HATA: %s - %s: %s", ad, type(exc).__name__, exc, exc_info=True)
        return None


def _ozet_kaydet(ozet: dict[str, dict], ad: str, e: int, a: int) -> None:
    """Özet sözlüğüne eklendi/atlandi sayılarını yazar."""
    ozet[ad]["eklendi"] = e
    ozet[ad]["atlandi"] = a


# ── Ana runner ───────────────────────────────────────────────────────────────

async def run_all(
    dry_run: bool = False,
    usd_kur: float | None = None,
) -> dict:
    """
    Tüm scraper'ları sırayla çalıştırır ve DB'ye yazar.

    usd_kur=None ise TCMB'den anlık kur çekilir; TCMB erişilemezse
    USD_KUR_VARSAYILAN sabit kuru kullanılır.
    dry_run=True ise scrape yapar ama DB'ye yazmaz.

    Döner: {scraper_adi: {"hata": bool, "eklendi": int, "atlandi": int}}
    """
    baslangic = datetime.datetime.now()
    ozet: dict[str, dict] = {}

    # ── USD/TRY kuru ─────────────────────────────────────────────────────────
    if usd_kur is None:
        usd_kur = await usd_try_kur(fallback=USD_KUR_VARSAYILAN)
    logger.info("USD/TRY kuru: %.4f%s", usd_kur,
                "" if usd_kur != USD_KUR_VARSAYILAN else " (sabit varsayılan)")

    # ── DB bağlantısı ─────────────────────────────────────────────────────────
    conn: sqlite3.Connection | None = None
    malzeme_map: dict[str, int] = {}
    merkez_map:  dict[str, int] = {}

    if not dry_run:
        conn = get_connection()
        malzeme_map = load_malzeme_map(conn)
        merkez_map  = load_merkez_map(conn)
        logger.info(
            "DB bağlantısı hazır — %d malzeme, %d merkez yüklendi",
            len(malzeme_map), len(merkez_map),
        )

    # ── 1. Demir endeks ──────────────────────────────────────────────────────
    demir = await _calistir_scraper("DemirEndeks", DemirEndeksScraper)
    ozet["DemirEndeks"] = {"hata": demir is None}
    if demir is not None and conn is not None:
        e, a = kaydet_endeks(conn, demir, malzeme_map, merkez_map)
        _ozet_kaydet(ozet, "DemirEndeks", e, a)
        logger.info("DemirEndeks DB: +%d, atlandı=%d", e, a)
    await asyncio.sleep(_SCRAPER_DELAY)

    # ── 2. Çelik hasır endeks ────────────────────────────────────────────────
    hasir = await _calistir_scraper("HasirEndeks", HasirEndeksScraper)
    ozet["HasirEndeks"] = {"hata": hasir is None}
    if hasir is not None and conn is not None:
        e, a = kaydet_endeks(conn, hasir, malzeme_map, merkez_map)
        _ozet_kaydet(ozet, "HasirEndeks", e, a)
        logger.info("HasirEndeks DB: +%d, atlandı=%d", e, a)
    await asyncio.sleep(_SCRAPER_DELAY)

    # ── 3. Filmaşin endeks (USD → TRY) ──────────────────────────────────────
    filmasin = await _calistir_scraper("FilmasinEndeks", FilmasinEndeksScraper)
    ozet["FilmasinEndeks"] = {"hata": filmasin is None}
    if filmasin is not None:
        for k in filmasin:
            if k.get("para_birimi") == "USD":
                usd_fiyat = k["fiyat"]
                k["fiyat"] = usd_to_try(usd_fiyat, usd_kur)
                logger.info(
                    "Filmaşin USD→TRY: %.2f USD × %.4f = %.2f TRY",
                    usd_fiyat, usd_kur, k["fiyat"],
                )
        if conn is not None:
            e, a = kaydet_endeks(conn, filmasin, malzeme_map, merkez_map)
            _ozet_kaydet(ozet, "FilmasinEndeks", e, a)
            logger.info("FilmasinEndeks DB: +%d, atlandı=%d", e, a)
    await asyncio.sleep(_SCRAPER_DELAY)

    # ── 4. Çimento ürünleri ──────────────────────────────────────────────────
    cimento = await _calistir_scraper("CimentoUrun", CimentoUrunScraper)
    ozet["CimentoUrun"] = {"hata": cimento is None}
    if cimento is not None and conn is not None:
        e, a = kaydet_urun_cimento(conn, cimento, malzeme_map)
        _ozet_kaydet(ozet, "CimentoUrun", e, a)
        logger.info("CimentoUrun DB: +%d, atlandı=%d", e, a)
    await asyncio.sleep(_SCRAPER_DELAY)

    # ── 5. Kum ürünleri ──────────────────────────────────────────────────────
    kum = await _calistir_scraper("KumUrun", KumUrunScraper)
    ozet["KumUrun"] = {"hata": kum is None}
    if kum is not None and conn is not None:
        e, a = kaydet_urun_kum(conn, kum, malzeme_map)
        _ozet_kaydet(ozet, "KumUrun", e, a)
        logger.info("KumUrun DB: +%d, atlandı=%d", e, a)
    await asyncio.sleep(_SCRAPER_DELAY)

    # ── 6. Gazbeton ürünleri ─────────────────────────────────────────────────
    gazbeton = await _calistir_scraper("GazbetonUrun", GazbetonUrunScraper)
    ozet["GazbetonUrun"] = {"hata": gazbeton is None}
    if gazbeton is not None and conn is not None:
        e, a = kaydet_urun_gazbeton(conn, gazbeton, malzeme_map)
        _ozet_kaydet(ozet, "GazbetonUrun", e, a)
        logger.info("GazbetonUrun DB: +%d, atlandı=%d", e, a)

    if conn is not None:
        conn.close()

    # ── Özet ─────────────────────────────────────────────────────────────────
    sure = (datetime.datetime.now() - baslangic).total_seconds()
    basarili  = sum(1 for v in ozet.values() if not v["hata"])
    hatali    = sum(1 for v in ozet.values() if v["hata"])
    toplam_ek = sum(v.get("eklendi", 0) for v in ozet.values())

    logger.info(
        "Runner tamamlandı %.1fs — scraper: %d/%d başarılı, DB: +%d kayıt%s",
        sure, basarili, len(ozet), toplam_ek,
        " [DRY-RUN]" if dry_run else "",
    )
    if hatali:
        hatali_adlar = [k for k, v in ozet.items() if v["hata"]]
        logger.warning("Hatalı scraper'lar: %s", ", ".join(hatali_adlar))

    return ozet


# ── CLI entrypoint ───────────────────────────────────────────────────────────

async def run_backfill(
    dry_run: bool = False,
    usd_kur: float | None = None,
) -> dict:
    """
    Tek seferlik tarihsel endeks backfill calistirir.

    Haftalik normal scrape akisi bundan etkilenmez; sadece endeks
    scraper'larindaki archive/city history satirlari DB'ye UPSERT edilir.
    """
    baslangic = datetime.datetime.now()
    ozet: dict[str, dict] = {}

    if usd_kur is None:
        usd_kur = await usd_try_kur(fallback=USD_KUR_VARSAYILAN)
    logger.info("Backfill USD/TRY kuru: %.4f%s", usd_kur,
                "" if usd_kur != USD_KUR_VARSAYILAN else " (sabit varsayilan)")

    conn: sqlite3.Connection | None = None
    malzeme_map: dict[str, int] = {}
    merkez_map: dict[str, int] = {}

    if not dry_run:
        conn = get_connection()
        malzeme_map = load_malzeme_map(conn)
        merkez_map = load_merkez_map(conn)
        logger.info(
            "Backfill DB hazir - %d malzeme, %d merkez yuklendi",
            len(malzeme_map), len(merkez_map),
        )

    backfill_scrapers = [
        ("DemirEndeksBackfill", DemirEndeksScraper),
        ("HasirEndeksBackfill", HasirEndeksScraper),
        ("FilmasinEndeksBackfill", FilmasinEndeksScraper),
    ]

    for ad, scraper_cls in backfill_scrapers:
        kayitlar = await _calistir_backfill(ad, scraper_cls)
        ozet[ad] = {"hata": kayitlar is None}

        if kayitlar is not None:
            if ad == "FilmasinEndeksBackfill":
                donusen = 0
                for k in kayitlar:
                    if k.get("para_birimi") == "USD":
                        usd_fiyat = k["fiyat"]
                        k["fiyat"] = usd_to_try(usd_fiyat, usd_kur)
                        donusen += 1
                logger.info("Filmasin backfill USD->TRY donusumu: %d kayit, kur=%.4f", donusen, usd_kur)

            if conn is not None:
                e, a = kaydet_endeks(conn, kayitlar, malzeme_map, merkez_map)
                _ozet_kaydet(ozet, ad, e, a)
                logger.info("%s DB: +%d, atlandi=%d", ad, e, a)

        await asyncio.sleep(_SCRAPER_DELAY)

    if conn is not None:
        conn.close()

    sure = (datetime.datetime.now() - baslangic).total_seconds()
    basarili = sum(1 for v in ozet.values() if not v["hata"])
    toplam_ek = sum(v.get("eklendi", 0) for v in ozet.values())
    logger.info(
        "Backfill tamamlandi %.1fs - scraper: %d/%d basarili, DB: +%d kayit%s",
        sure, basarili, len(ozet), toplam_ek,
        " [DRY-RUN]" if dry_run else "",
    )

    return ozet


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="BuildingAI fiyat takip runner")
    p.add_argument("--dry-run", action="store_true",
                   help="Scrape yap ama DB'ye yazma")
    p.add_argument("--usd-kur", type=float, default=None,
                   help="USD/TRY kuru (belirtilmezse TCMB'den çekilir)")
    p.add_argument("--backfill", action="store_true",
                   help="Tek seferlik tarihsel endeks backfill calistir")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    if args.backfill:
        ozet = asyncio.run(run_backfill(dry_run=args.dry_run, usd_kur=args.usd_kur))
    else:
        ozet = asyncio.run(run_all(dry_run=args.dry_run, usd_kur=args.usd_kur))

    print()
    print(f"{'Scraper':<20}  {'Durum':<8}  {'Eklendi':>8}  {'Atlandı':>8}")
    print("-" * 52)
    for ad, v in ozet.items():
        durum   = "HATA" if v["hata"] else "OK"
        eklendi = str(v.get("eklendi", "-")) if not v["hata"] else "-"
        atlandi = str(v.get("atlandi", "-")) if not v["hata"] else "-"
        print(f"  {ad:<18}  {durum:<8}  {eklendi:>8}  {atlandi:>8}")
    print()
