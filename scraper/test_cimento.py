"""
Proemtia çimento ürün scraper test scripti.
Çalıştır: python scraper/test_cimento.py

Gerçek siteye istek ATMAZ — test_data/proemtia_cimento.html fixture'ını kullanır.
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

from scraper.proemtia.cimento_urun import CimentoUrunScraper

_FIXTURE = pathlib.Path(__file__).parent / "test_data" / "proemtia_cimento.html"


async def main() -> None:
    html = _FIXTURE.read_text(encoding="utf-8")

    scraper = CimentoUrunScraper()

    async def _stub(*_a, **_kw):
        return html

    scraper.fetch_html = _stub
    sonuclar = await scraper.scrape()

    if not sonuclar:
        print("HATA: Hiç ürün bulunamadı!")
        sys.exit(1)

    # ── Tablo çıktısı ─────────────────────────────────────────────
    print(f"\n{'='*90}")
    print(f"  Proemtia Çimento Ürünleri  —  {sonuclar[0]['tarih']}  ({len(sonuclar)} ürün)")
    print(f"{'='*90}")
    print(f"  {'Marka':<18} {'Ürün':<30} {'kg':>4}  {'KDV Dahil':>10}  {'KDV Hariç':>10}  Satıcı")
    print(f"  {'-'*18} {'-'*30} {'-'*4}  {'-'*10}  {'-'*10}  {'-'*20}")

    for k in sonuclar:
        kg     = f"{k['torba_kg']:.0f}" if k["torba_kg"] else "?"
        kdvli  = f"{k['fiyat_kdv_dahil']:,.2f} ₺" if k["fiyat_kdv_dahil"] else "-"
        kdvsiz = f"{k['fiyat_kdv_haric']:,.2f} ₺" if k["fiyat_kdv_haric"] else "-"
        print(f"  {k['marka']:<18} {k['urun_adi']:<30} {kg:>4}  {kdvli:>10}  {kdvsiz:>10}  {k['satici']}")

    print()

    # ── Doğrulama ─────────────────────────────────────────────────
    hatalar = []

    # Her kayıtta zorunlu alanlar dolu olmalı
    zorunlu = ["marka", "urun_adi", "fiyat_kdv_dahil", "tarih", "pid", "urun_url"]
    for i, k in enumerate(sonuclar):
        for alan in zorunlu:
            if not k.get(alan):
                hatalar.append(f"Kayıt {i}: '{alan}' boş — {k['urun_adi_tam']}")

    if not hatalar:
        print(f"[OK] Tüm {len(sonuclar)} kayıtta zorunlu alanlar dolu")

    # torba_kg parse edilmiş olmalı
    eksik_kg = [k for k in sonuclar if k["torba_kg"] is None]
    if eksik_kg:
        hatalar.append(f"torba_kg parse edilemedi: {[k['urun_adi_tam'] for k in eksik_kg]}")
    else:
        print(f"[OK] torba_kg tüm kayıtlarda parse edildi")

    # KDV hariç fiyat en az bir kayıtta olmalı
    kdv_haric_var = [k for k in sonuclar if k["fiyat_kdv_haric"] is not None]
    if not kdv_haric_var:
        hatalar.append("Hiçbir kayıtta KDV hariç fiyat yok")
    else:
        print(f"[OK] KDV hariç fiyat: {len(kdv_haric_var)}/{len(sonuclar)} kayıtta mevcut")

    # KDV dahil > KDV hariç olmalı
    for k in sonuclar:
        if k["fiyat_kdv_haric"] and k["fiyat_kdv_dahil"] <= k["fiyat_kdv_haric"]:
            hatalar.append(
                f"KDV mantığı hatalı: {k['urun_adi_tam']} — "
                f"dahil={k['fiyat_kdv_dahil']}, hariç={k['fiyat_kdv_haric']}"
            )
    if not hatalar:
        print("[OK] KDV dahil > KDV hariç (tüm kayıtlar)")

    # pid sayısal olmalı
    pid_hatali = [k for k in sonuclar if not k["pid"].isdigit()]
    if pid_hatali:
        hatalar.append(f"pid sayısal değil: {[k['pid'] for k in pid_hatali]}")
    else:
        print("[OK] pid alanı tüm kayıtlarda sayısal")

    # Marka çeşitliliği
    markalar = {k["marka"] for k in sonuclar}
    print(f"[OK] Markalar ({len(markalar)}): {', '.join(sorted(markalar))}")

    # Torba boyutları
    boyutlar = sorted({k["torba_kg"] for k in sonuclar if k["torba_kg"]})
    print(f"[OK] Torba boyutları: {[f'{b:.0f} kg' for b in boyutlar]}")

    print()
    if hatalar:
        for h in hatalar:
            print(f"HATA: {h}")
        sys.exit(1)
    else:
        print(f"[OK] Tüm doğrulamalar geçti — {len(sonuclar)} ürün")


if __name__ == "__main__":
    asyncio.run(main())
