"""
Proemtia kum + gazbeton ürün scraper test scripti.
Çalıştır: python scraper/test_urunler.py

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

from scraper.proemtia.kum_urun      import KumUrunScraper
from scraper.proemtia.gazbeton_urun import GazbetonUrunScraper

_DATA = pathlib.Path(__file__).parent / "test_data"


def _fixture(fname: str):
    html = (_DATA / fname).read_text(encoding="utf-8")
    async def _stub(*_a, **_kw):
        return html
    return _stub


async def _test_kum() -> list[dict]:
    s = KumUrunScraper()
    s.fetch_html = _fixture("proemtia_kum.html")
    return await s.scrape()


async def _test_gazbeton() -> list[dict]:
    s = GazbetonUrunScraper()
    s.fetch_html = _fixture("proemtia_gazbeton.html")
    return await s.scrape()


def _print_table(baslik: str, satirlar: list[dict], kolonlar: list[tuple[str, int]]) -> None:
    print(f"\n{'='*80}")
    print(f"  {baslik}  ({len(satirlar)} ürün)")
    print(f"{'='*80}")
    fmt = "  " + "  ".join(f"{{:<{w}}}" for _, w in kolonlar)
    print(fmt.format(*[k for k, _ in kolonlar]))
    print("  " + "  ".join("-" * w for _, w in kolonlar))
    for r in satirlar:
        vals = []
        for key, w in kolonlar:
            v = r.get(key)
            if isinstance(v, float):
                vals.append(f"{v:,.2f}")
            else:
                vals.append(str(v) if v is not None else "-")
        print(fmt.format(*vals))


async def main() -> None:
    kum_sonuc      = await _test_kum()
    gazbeton_sonuc = await _test_gazbeton()
    hatalar: list[str] = []

    # ── KUM tablosu ───────────────────────────────────────────────
    _print_table(
        "Proemtia Kum Ürünleri",
        kum_sonuc,
        [("urun_adi", 22), ("kum_turu", 6), ("ambalaj_ton", 11),
         ("fiyat_kdv_dahil", 13), ("fiyat_kdv_haric", 13), ("satici", 28)],
    )

    # ── GAZBETON tablosu ──────────────────────────────────────────
    _print_table(
        "Proemtia Gazbeton Ürünleri",
        gazbeton_sonuc,
        [("marka", 8), ("sinif", 8), ("tip", 12), ("satis_birimi", 12),
         ("boyut_mm", 14), ("fiyat_kdv_dahil", 13), ("satici", 24)],
    )

    print()

    # ── Kum doğrulamaları ─────────────────────────────────────────
    if len(kum_sonuc) != 8:
        hatalar.append(f"Kum: {len(kum_sonuc)} ürün, 8 bekleniyor")
    else:
        print("[OK] Kum: 8 ürün")

    kum_turleri = {k["kum_turu"] for k in kum_sonuc}
    beklenen_kum = {"sap", "kaba"}
    if not beklenen_kum.issubset(kum_turleri):
        hatalar.append(f"Kum türleri eksik: bulunan={kum_turleri}, beklenen={beklenen_kum}")
    else:
        print(f"[OK] Kum türleri: {sorted(kum_turleri)}")

    kum_birim_hatali = [k for k in kum_sonuc if k["birim"].lower() not in ("ton","adet")]
    if kum_birim_hatali:
        hatalar.append(f"Kum birim hatalı: {[k['birim'] for k in kum_birim_hatali]}")
    else:
        print(f"[OK] Kum birimi: {kum_sonuc[0]['birim'] if kum_sonuc else '-'}")

    kum_ambalaj_eksik = [k for k in kum_sonuc if k["ambalaj_ton"] is None]
    if kum_ambalaj_eksik:
        hatalar.append(f"Kum ambalaj_ton parse edilemedi: {[k['urun_adi'] for k in kum_ambalaj_eksik]}")
    else:
        print("[OK] Kum ambalaj_ton tüm kayıtlarda parse edildi")

    # ── Gazbeton doğrulamaları ────────────────────────────────────
    if len(gazbeton_sonuc) != 16:
        hatalar.append(f"Gazbeton: {len(gazbeton_sonuc)} ürün, 16 bekleniyor")
    else:
        print("[OK] Gazbeton: 16 ürün")

    markali = [g for g in gazbeton_sonuc if g["marka"]]
    markasiz = [g for g in gazbeton_sonuc if not g["marka"]]
    print(f"[OK] Gazbeton markalı: {len(markali)}, markasız: {len(markasiz)}")

    siniflar = {g["sinif"] for g in gazbeton_sonuc if g["sinif"]}
    print(f"[OK] Gazbeton sınıfları: {sorted(siniflar)}")

    satis_birimleri = {g["satis_birimi"] for g in gazbeton_sonuc}
    if not {"adet", "palet"}.issubset(satis_birimleri):
        hatalar.append(f"Gazbeton satış birimleri eksik: {satis_birimleri}")
    else:
        print(f"[OK] Gazbeton satış birimleri: {sorted(satis_birimleri)}")

    gaz_boyut_eksik = [g for g in gazbeton_sonuc if not g["boyut_mm"]]
    if gaz_boyut_eksik:
        hatalar.append(f"Gazbeton boyut_mm eksik: {[g['urun_adi_tam'] for g in gaz_boyut_eksik]}")
    else:
        genislikler = sorted({g["genislik_mm"] for g in gazbeton_sonuc if g["genislik_mm"]})
        print(f"[OK] Gazbeton genişlikler (mm): {[int(g) for g in genislikler]}")

    # ── Ortak zorunlu alanlar ─────────────────────────────────────
    for liste, ad in [(kum_sonuc, "kum"), (gazbeton_sonuc, "gazbeton")]:
        for i, k in enumerate(liste):
            for alan in ("fiyat_kdv_dahil", "pid", "urun_url", "tarih"):
                if not k.get(alan):
                    hatalar.append(f"{ad}[{i}] '{alan}' boş — {k.get('urun_adi_tam')}")

    if not hatalar:
        print(f"[OK] Zorunlu alanlar tüm kayıtlarda dolu")

    # KDV mantığı
    for liste in (kum_sonuc, gazbeton_sonuc):
        for k in liste:
            if k["fiyat_kdv_haric"] and k["fiyat_kdv_dahil"] <= k["fiyat_kdv_haric"]:
                hatalar.append(
                    f"KDV mantığı hatalı: {k.get('urun_adi_tam')} "
                    f"dahil={k['fiyat_kdv_dahil']}, hariç={k['fiyat_kdv_haric']}"
                )
    if not hatalar:
        print("[OK] KDV dahil > KDV hariç (tüm kayıtlar)")

    print()
    if hatalar:
        for h in hatalar:
            print(f"HATA: {h}")
        sys.exit(1)
    else:
        toplam = len(kum_sonuc) + len(gazbeton_sonuc)
        print(f"[OK] Tüm doğrulamalar geçti — toplam {toplam} ürün (kum={len(kum_sonuc)}, gazbeton={len(gazbeton_sonuc)})")


if __name__ == "__main__":
    asyncio.run(main())
