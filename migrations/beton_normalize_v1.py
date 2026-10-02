"""
migrations/beton_normalize_v1.py
─────────────────────────────────
1. poz_no IS NULL beton kayıtlarını CSB formatına yeniden adlandırır.
2. id=2835'teki kullanici_fiyatlar FK'sını id=10'a taşır, kaydı siler.
3. Seed kaynaklı duplikatları siler.
4. Tek transaction — hata → rollback.
"""

import sqlite3
import pathlib
import sys

DB_PATH = pathlib.Path(__file__).parent.parent / "santiye_proje.db"

# (eski_id, yeni_ad, yeni_kategori, yeni_alt_kategori)
YENIDEN_ADLANDIR = [
    (3263, "C16/20 Hazır Beton", "beton", "Beton"),
    (9,    "C20/25 Hazır Beton", "beton", "Beton"),
    (10,   "C25/30 Hazır Beton", "beton", "Beton"),
    (11,   "C30/37 Hazır Beton", "beton", "Beton"),
    (12,   "C35/45 Hazır Beton", "beton", "Beton"),
    (3269, "C40/50 Hazır Beton", "beton", "Beton"),
    (3270, "C45/55 Hazır Beton", "beton", "Beton"),
    (3271, "C50/60 Hazır Beton", "beton", "Beton"),
]

# id=2835 FK'sı bu id'ye taşınır
FK_HEDEF = 10   # C25/30 Hazır Beton

# Silinecek duplikat id'ler (FK yok)
SILINECEKLER = [2835, 3264, 3265, 3266, 3267, 3268]


def run(db_path: pathlib.Path = DB_PATH) -> None:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=OFF")

    try:
        with conn:
            # ── 1. Yeniden adlandır ──────────────────────────────────────────
            for mid, yeni_ad, yeni_kat, yeni_alt in YENIDEN_ADLANDIR:
                row = conn.execute("SELECT ad FROM malzemeler WHERE id=?", (mid,)).fetchone()
                if not row:
                    print(f"  ATLA: id={mid} bulunamadı")
                    continue
                conn.execute(
                    "UPDATE malzemeler SET ad=?, kategori=?, alt_kategori=?, birim='m3' WHERE id=?",
                    (yeni_ad, yeni_kat, yeni_alt, mid),
                )
                print(f"  RENAME id={mid}: '{row['ad']}' -> '{yeni_ad}'")

            # ── 2. id=2835 FK'sını FK_HEDEF'e taşı ─────────────────────────
            kf = conn.execute(
                "SELECT COUNT(*) as c FROM kullanici_fiyatlar WHERE malzeme_id=?",
                (2835,)
            ).fetchone()["c"]
            if kf:
                conn.execute(
                    "UPDATE kullanici_fiyatlar SET malzeme_id=? WHERE malzeme_id=?",
                    (FK_HEDEF, 2835)
                )
                print(f"  FK TASINDI: kullanici_fiyatlar malzeme_id=2835 -> {FK_HEDEF} ({kf} kayit)")

            # ── 3. Duplikatları sil ─────────────────────────────────────────
            for mid in SILINECEKLER:
                row = conn.execute("SELECT ad FROM malzemeler WHERE id=?", (mid,)).fetchone()
                if not row:
                    print(f"  ATLA (zaten yok): id={mid}")
                    continue
                conn.execute("DELETE FROM malzemeler WHERE id=?", (mid,))
                print(f"  SILINDI id={mid}: '{row['ad']}'")

        # ── Dogrulama ────────────────────────────────────────────────────────
        print("\n=== SON DURUM (poz_no IS NULL beton) ===")
        rows = conn.execute(
            "SELECT id, ad, birim, kategori FROM malzemeler "
            "WHERE (LOWER(ad) LIKE '%beton%' OR LOWER(kategori) LIKE '%beton%') "
            "AND poz_no IS NULL ORDER BY ad"
        ).fetchall()
        for r in rows:
            print(f"  {r['id']:5d}  {r['kategori']:<15} {r['birim']:<4} {r['ad']}")
        print(f"\nToplam: {len(rows)}")
        print("\nMigration tamamlandi.")

    except Exception as e:
        print(f"\nHATA: {e}", file=sys.stderr)
        raise
    finally:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(DB_PATH))
    args = parser.parse_args()
    run(pathlib.Path(args.db))
