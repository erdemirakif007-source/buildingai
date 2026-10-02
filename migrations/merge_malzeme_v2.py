"""
migrations/merge_malzeme_v2.py
──────────────────────────────
Birleştirme migration'ı:

1. malzemeler tablosuna poz_no / alt_kategori / aciklama kolonları ekle
2. csb_malzeme_katalog (134 kayıt) → malzemeler'e INSERT (yeni ID'ler alır)
3. csb_is_kalemi_malzeme.malzeme_katalog_id → yeni malzeme_id'ye güncelle
4. is_kalemi_malzeme tablosunu yeni şemaya (zorunlu + kaynak) dönüştür
5. is_kalemi_csb_malzeme → is_kalemi_malzeme'ye (kaynak='katalog') taşı
6. Eski kayıtları is_kalemi_malzeme'de (kaynak='manuel') koru
7. is_kalemi_csb_malzeme ve csb_malzeme_katalog tablolarını DROP et

Güvenceler:
- scrape_fiyatlar.malzeme_id referansları dokunulmaz
- kullanici_fiyatlar.malzeme_id referansları dokunulmaz
- Mevcut malzemeler ID'leri (1-25, 1658, 2415, 2416, 2835) değişmez
- Tüm işlemler tek transaction içinde — hata olursa rollback
"""

import sqlite3
import sys
import pathlib

DB_PATH = pathlib.Path(__file__).parent.parent / "santiye_proje.db"


def run(db_path: pathlib.Path = DB_PATH) -> None:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=OFF")   # FK kontrolü geçici kapalı

    try:
        with conn:   # tek transaction

            # ────────────────────────────────────────────────────────
            # 1. malzemeler tablosuna eksik kolonları ekle
            # ────────────────────────────────────────────────────────
            existing_cols = {
                row["name"]
                for row in conn.execute("PRAGMA table_info(malzemeler)")
            }
            for col, defn in [
                ("poz_no",       "TEXT"),
                ("alt_kategori", "TEXT"),
                ("aciklama",     "TEXT"),
            ]:
                if col not in existing_cols:
                    conn.execute(f"ALTER TABLE malzemeler ADD COLUMN {col} {defn}")
                    print(f"  + malzemeler.{col} eklendi")

            # ────────────────────────────────────────────────────────
            # 2. csb_malzeme_katalog → malzemeler INSERT + mapping
            # ────────────────────────────────────────────────────────
            csb_rows = conn.execute(
                "SELECT id, poz_no, kategori, alt_kategori, ad, birim, aciklama, aktif "
                "FROM csb_malzeme_katalog ORDER BY id"
            ).fetchall()

            csb_id_to_new: dict[int, int] = {}   # csb_old_id → new malzeme_id

            for row in csb_rows:
                # Aynı poz_no zaten eklenmişse atla (idempotent)
                existing = conn.execute(
                    "SELECT id FROM malzemeler WHERE poz_no=?", (row["poz_no"],)
                ).fetchone()
                if existing:
                    csb_id_to_new[row["id"]] = existing["id"]
                    continue

                cur = conn.execute(
                    """INSERT INTO malzemeler
                       (kategori, alt_kategori, ad, birim, poz_no, aciklama,
                        aktif, scrape_tipi)
                       VALUES (?,?,?,?,?,?,?,'csb_katalog')""",
                    (
                        row["kategori"],
                        row["alt_kategori"],
                        row["ad"],
                        row["birim"],
                        row["poz_no"],
                        row["aciklama"],
                        row["aktif"],
                    ),
                )
                csb_id_to_new[row["id"]] = cur.lastrowid

            print(f"  csb_malzeme_katalog: {len(csb_rows)} kayıt işlendi, "
                  f"{len(csb_id_to_new)} mapping oluşturuldu")

            # ────────────────────────────────────────────────────────
            # 3. csb_is_kalemi_malzeme.malzeme_katalog_id → yeni id
            # ────────────────────────────────────────────────────────
            ikm_rows = conn.execute(
                "SELECT id, malzeme_katalog_id FROM csb_is_kalemi_malzeme"
            ).fetchall()
            updated = 0
            for row in ikm_rows:
                new_id = csb_id_to_new.get(row["malzeme_katalog_id"])
                if new_id and new_id != row["malzeme_katalog_id"]:
                    conn.execute(
                        "UPDATE csb_is_kalemi_malzeme SET malzeme_katalog_id=? WHERE id=?",
                        (new_id, row["id"]),
                    )
                    updated += 1
            print(f"  csb_is_kalemi_malzeme: {updated}/{len(ikm_rows)} satır güncellendi")

            # ────────────────────────────────────────────────────────
            # 4. Yeni is_kalemi_malzeme şeması (geçici tablo üzerinden)
            # ────────────────────────────────────────────────────────
            # Mevcut kayıtları oku
            old_ikm = conn.execute(
                "SELECT id, is_kalemi_id, malzeme_id, miktar, birim, notlar, created_at "
                "FROM is_kalemi_malzeme"
            ).fetchall()
            print(f"  is_kalemi_malzeme mevcut kayıt: {len(old_ikm)}")

            # is_kalemi_csb_malzeme kayıtlarını oku (bunlar katalog)
            csb_proje = conn.execute(
                "SELECT id, is_kalemi_id, malzeme_katalog_id, miktar, birim, zorunlu, notlar "
                "FROM is_kalemi_csb_malzeme"
            ).fetchall()
            print(f"  is_kalemi_csb_malzeme mevcut kayıt: {len(csb_proje)}")

            # Eski tabloyu yedekle ve yeniden oluştur
            conn.execute("DROP TABLE IF EXISTS is_kalemi_malzeme_backup")
            conn.execute(
                "CREATE TABLE is_kalemi_malzeme_backup AS "
                "SELECT * FROM is_kalemi_malzeme"
            )
            conn.execute("DROP TABLE is_kalemi_malzeme")
            conn.execute("""
                CREATE TABLE is_kalemi_malzeme (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    is_kalemi_id INTEGER NOT NULL,
                    malzeme_id   INTEGER NOT NULL REFERENCES malzemeler(id),
                    miktar       REAL    NOT NULL DEFAULT 1.0,
                    birim        TEXT,
                    zorunlu      INTEGER NOT NULL DEFAULT 0,
                    notlar       TEXT,
                    kaynak       TEXT    NOT NULL DEFAULT 'manuel',
                    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(is_kalemi_id, malzeme_id)
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_ikm_kalemi "
                "ON is_kalemi_malzeme(is_kalemi_id)"
            )

            # ────────────────────────────────────────────────────────
            # 5. Eski kayıtları aktar — kaynak sütunu varsa koru
            # ────────────────────────────────────────────────────────
            backup_cols = {row["name"] for row in conn.execute("PRAGMA table_info(is_kalemi_malzeme_backup)")}
            has_kaynak = "kaynak" in backup_cols
            has_zorunlu = "zorunlu" in backup_cols

            manuel_count = 0
            for row in old_ikm:
                kaynak = row["kaynak"] if has_kaynak and row["kaynak"] else "manuel"
                zorunlu = row["zorunlu"] if has_zorunlu and row["zorunlu"] is not None else 0
                try:
                    conn.execute(
                        """INSERT INTO is_kalemi_malzeme
                           (is_kalemi_id, malzeme_id, miktar, birim,
                            zorunlu, notlar, kaynak, created_at)
                           VALUES (?,?,?,?,?,?,?,?)""",
                        (row["is_kalemi_id"], row["malzeme_id"],
                         row["miktar"] or 1.0, row["birim"],
                         zorunlu, row["notlar"], kaynak,
                         row["created_at"] if "created_at" in backup_cols else None),
                    )
                    manuel_count += 1
                except sqlite3.IntegrityError:
                    print(f"  UYARI: is_kalemi_id={row['is_kalemi_id']} "
                          f"malzeme_id={row['malzeme_id']} zaten var, atlandı")
            print(f"  Kayıtlar aktarıldı: {manuel_count}")

            # ────────────────────────────────────────────────────────
            # 6. is_kalemi_csb_malzeme → is_kalemi_malzeme (kaynak='katalog')
            # ────────────────────────────────────────────────────────
            katalog_count = 0
            skip_count = 0
            for row in csb_proje:
                new_malzeme_id = csb_id_to_new.get(row["malzeme_katalog_id"],
                                                    row["malzeme_katalog_id"])
                try:
                    conn.execute(
                        """INSERT INTO is_kalemi_malzeme
                           (is_kalemi_id, malzeme_id, miktar, birim,
                            zorunlu, notlar, kaynak)
                           VALUES (?,?,?,?,?,'katalog','katalog')""",
                        # NOT: notlar yerine kaynak='katalog' sabitlendi yukarıda
                        (row["is_kalemi_id"], new_malzeme_id,
                         row["miktar"] or 1.0, row["birim"],
                         row["zorunlu"] or 0),
                    )
                    # notlar alanını düzelt
                    conn.execute(
                        "UPDATE is_kalemi_malzeme SET notlar=? "
                        "WHERE is_kalemi_id=? AND malzeme_id=?",
                        (row["notlar"], row["is_kalemi_id"], new_malzeme_id),
                    )
                    katalog_count += 1
                except sqlite3.IntegrityError:
                    skip_count += 1
                    print(f"  UYARI: katalog çakışma is_kalemi_id={row['is_kalemi_id']} "
                          f"csb_malzeme_id={row['malzeme_katalog_id']}→{new_malzeme_id}, atlandı")
            print(f"  Katalog kayıtları aktarıldı: {katalog_count}, atlandı: {skip_count}")

            # ────────────────────────────────────────────────────────
            # 7. Eski tabloları DROP et
            # ────────────────────────────────────────────────────────
            conn.execute("DROP TABLE IF EXISTS is_kalemi_csb_malzeme")
            print("  is_kalemi_csb_malzeme DROP edildi")

            conn.execute("DROP TABLE IF EXISTS csb_malzeme_katalog")
            print("  csb_malzeme_katalog DROP edildi")

            # İndeksler
            conn.execute(
                "CREATE INDEX IF NOT EXISTS ix_malzeme_poz "
                "ON malzemeler(poz_no) WHERE poz_no IS NOT NULL"
            )

        print("\n✓ Migration başarıyla tamamlandı.")

    except Exception:
        print("\n✗ Migration BAŞARISIZ — rollback yapıldı.", file=sys.stderr)
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
