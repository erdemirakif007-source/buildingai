"""
Proemtia demir endeks scraper test scripti.
Calistir: python -m scraper.test_demir
veya    : python scraper/test_demir.py

Gercek siteye istek ATMAZ — scraper/test_data/proemtia_demir.html dosyasini kullanir.
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

# Proje kokunu path'e ekle
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

from scraper.proemtia.demir_endeks import DemirEndeksScraper

_FIXTURE = pathlib.Path(__file__).parent / "test_data" / "proemtia_demir.html"


async def main() -> None:
    html = _FIXTURE.read_text(encoding="utf-8")

    scraper = DemirEndeksScraper()
    # fetch_html'i gercek HTTP istegi atmadan fixture ile override et
    async def _fixture_html(*_args, **_kwargs):
        return html

    scraper.fetch_html = _fixture_html

    sonuclar = await scraper.scrape()

    if not sonuclar:
        print("HATA: Hic fiyat kaydi bulunamadi!")
        sys.exit(1)

    # Baslik
    print(f"\n{'='*70}")
    print(f"  Proemtia Demir Endeks  --  {sonuclar[0]['tarih']}")
    print(f"  Toplam kayit: {len(sonuclar)}  (beklenen: 21)")
    print(f"{'='*70}")
    print(f"  {'Merkez':<22} {'Malzeme':<24} {'Fiyat (TL/ton)':>14}  Degisim")
    print(f"  {'-'*22} {'-'*24} {'-'*14}  {'-'*8}")

    # Merkeze gore grupla
    merkezler: dict[str, list] = {}
    for r in sonuclar:
        merkezler.setdefault(r["merkez_ad"], []).append(r)

    for merkez_ad, kayitlar in sorted(merkezler.items()):
        for k in kayitlar:
            ok = "^" if k["degisim"] == "yukari" else ("v" if k["degisim"] == "asagi" else "-")
            malzeme_kisa = k["malzeme_ad"].replace("Ø", "O")  # O8/O10/O12
            print(f"  {k['merkez_ad']:<22} {malzeme_kisa:<24} {k['fiyat']:>14,.2f}  {ok}")
        print()

    # Dogrulama
    beklenen_merkezler = {"ankara", "biga", "gebze", "iskenderun_payas", "istanbul", "izmir", "karabuk"}
    bulunan_merkezler  = {r["merkez_kod"] for r in sonuclar}
    eksik = beklenen_merkezler - bulunan_merkezler
    if eksik:
        print(f"UYARI: Eksik merkezler: {eksik}")
        sys.exit(1)
    else:
        print("[OK] Tum 7 merkez bulundu")

    if len(sonuclar) == 21:
        print("[OK] 21 fiyat kaydi dogrulandi (7 merkez x 3 cap)")
    else:
        print(f"UYARI: {len(sonuclar)} kayit bulundu, 21 bekleniyor")
        sys.exit(1)

    kdv_bilgi = "KDV %20 dahil (fabrika teslim)" if sonuclar[0]["kdv_dahil"] else "KDV haric"
    print(f"[OK] Fiyat turu: {kdv_bilgi}")
    print(f"[OK] Kaynak: {sonuclar[0]['kaynak_url']}\n")


if __name__ == "__main__":
    asyncio.run(main())
