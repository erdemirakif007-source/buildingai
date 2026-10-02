"""
Proemtia çelik hasır ve filmaşin endeks scraper test scripti.
Çalıştır: python scraper/test_hasir.py

Gerçek siteye istek ATMAZ — test_data/ fixture dosyalarını kullanır.
"""
import asyncio
import io
import logging
import pathlib
import sys
import os

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")
if isinstance(sys.stderr, io.TextIOWrapper):
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

from scraper.proemtia.hasir_endeks import HasirEndeksScraper
from scraper.proemtia.filmasin_endeks import FilmasinEndeksScraper

_DATA = pathlib.Path(__file__).parent / "test_data"


def _fixture(fname: str):
    html = (_DATA / fname).read_text(encoding="utf-8")
    async def _stub(*_a, **_kw):
        return html
    return _stub


async def main() -> None:
    # ── Çelik Hasır ──────────────────────────────────────────────
    hasir = HasirEndeksScraper()
    hasir.fetch_html = _fixture("proemtia_hasir.html")
    hasir_sonuc = await hasir.scrape()
    hasir_backfill = await hasir.scrape_backfill()

    # ── Filmaşin ─────────────────────────────────────────────────
    filmasin = FilmasinEndeksScraper()
    filmasin.fetch_html = _fixture("proemtia_filmasin.html")
    filmasin_sonuc = await filmasin.scrape()
    filmasin_backfill = await filmasin.scrape_backfill()

    tum_sonuclar = hasir_sonuc + filmasin_sonuc

    # ── Çıktı ────────────────────────────────────────────────────
    print(f"\n{'='*68}")
    print(f"  Proemtia Çelik Hasır & Filmaşin Endeks")
    print(f"{'='*68}")
    print(f"  {'Malzeme':<28} {'Fiyat':>12}  {'Birim':<5}  {'Tarih'}")
    print(f"  {'-'*28} {'-'*12}  {'-'*5}  {'-'*10}")

    for k in tum_sonuclar:
        birim = k["para_birimi"]
        print(f"  {k['malzeme_ad']:<28} {k['fiyat']:>12,.2f}  {birim:<5}  {k['tarih']}")

    print()

    # ── Doğrulama ────────────────────────────────────────────────
    hatalar = []

    if len(hasir_sonuc) != 2:
        hatalar.append(f"Hasır: {len(hasir_sonuc)} kayıt beklendi 2, bulundu")
    else:
        print("[OK] Çelik Hasır: 2 kayıt (Q131 + Q188)")

    beklenen_hasir_malzemeler = {"Çelik Hasır Q131", "Çelik Hasır Q188"}
    bulunan = {r["malzeme_ad"] for r in hasir_sonuc}
    if bulunan != beklenen_hasir_malzemeler:
        hatalar.append(f"Hasır malzeme adları yanlış: {bulunan}")
    else:
        print("[OK] Çelik Hasır malzeme adları doğru")

    if hasir_sonuc[0]["para_birimi"] != "TRY":
        hatalar.append(f"Hasır para birimi TRY beklendi, geldi: {hasir_sonuc[0]['para_birimi']}")
    else:
        print("[OK] Çelik Hasır para birimi: TRY")

    if len(filmasin_sonuc) != 1:
        hatalar.append(f"Filmaşin: {len(filmasin_sonuc)} kayıt, 1 bekleniyor")
    else:
        print("[OK] Filmaşin: 1 kayıt")

    if filmasin_sonuc[0]["para_birimi"] != "USD":
        hatalar.append(f"Filmaşin para birimi USD beklendi, geldi: {filmasin_sonuc[0]['para_birimi']}")
    else:
        print("[OK] Filmaşin para birimi: USD (not: DB katmanı TL'ye çevirir)")

    if len(hasir_backfill) != 500:
        hatalar.append(f"Hasir backfill: {len(hasir_backfill)} kayit, 500 bekleniyor")
    else:
        print("[OK] Celik Hasir backfill: 500 kayit (250 tarih x Q131/Q188)")

    if len(filmasin_backfill) != 249:
        hatalar.append(f"Filmasin backfill: {len(filmasin_backfill)} kayit, 249 bekleniyor")
    else:
        print("[OK] Filmasin backfill: 249 kayit")

    for r in tum_sonuclar:
        if r["referans_merkez_kod"] is not None:
            hatalar.append(f"{r['malzeme_ad']}: referans_merkez_kod None olmalı (ulusal endeks)")
        if r["kdv_dahil"] is not False:
            hatalar.append(f"{r['malzeme_ad']}: kdv_dahil False olmalı (endeks fiyatı)")
    if not hatalar:
        print("[OK] referans_merkez_kod=None, kdv_dahil=False (tüm kayıtlar)")

    print()
    if hatalar:
        for h in hatalar:
            print(f"HATA: {h}")
        sys.exit(1)
    else:
        print(f"[OK] Tüm doğrulamalar geçti — {len(tum_sonuclar)} kayıt")


if __name__ == "__main__":
    asyncio.run(main())
