"""
migrate_hierarchy.py — Bina/Kat/Mahal/İş Kalemi Hiyerarşi Migration Scripti
Çalıştır: python migrate_hierarchy.py

Yeni tablolar: binalar, katlar, mahaller, is_kalemleri, ilerleme_kayitlari
Mevcut tablolara eklenen sütunlar: satin_alma.is_kalemi_id, archive_records.is_kalemi_id

Mevcut tabloları ve çalışan sistemi KIRMAZ — sadece ekler.
"""
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

USE_POSTGRES = DATABASE_URL.startswith("postgresql://")

if USE_POSTGRES:
    try:
        import psycopg2
        from urllib.parse import urlparse
        parsed = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            dbname=parsed.path.lstrip("/"),
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port or 5432
        )
        conn.autocommit = False
        cur = conn.cursor()
        print(f"[DB] PostgreSQL modunda çalışıyor: {parsed.hostname}")
    except Exception as e:
        print(f"[HATA] PostgreSQL bağlantısı kurulamadı: {e}")
        sys.exit(1)
else:
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), "santiye_proje.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    print(f"[DB] SQLite modunda çalışıyor: {db_path}")

print()


# ─────────────────────────────────────────────
# Yardımcı fonksiyonlar
# ─────────────────────────────────────────────

def tablo_var_mi(tablo_adi):
    if USE_POSTGRES:
        cur.execute(
            "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name=%s)",
            (tablo_adi,)
        )
        return cur.fetchone()[0]
    else:
        cur.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?",
            (tablo_adi,)
        )
        return cur.fetchone()[0] > 0


def kolon_var_mi(tablo_adi, kolon_adi):
    if USE_POSTGRES:
        cur.execute(
            "SELECT EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name=%s AND column_name=%s)",
            (tablo_adi, kolon_adi)
        )
        return cur.fetchone()[0]
    else:
        cur.execute(f"PRAGMA table_info({tablo_adi})")
        kolonlar = [row[1] for row in cur.fetchall()]
        return kolon_adi in kolonlar


def kolon_ekle(tablo, kolon, tip, default=None):
    if kolon_var_mi(tablo, kolon):
        print(f"  ✅ {tablo}.{kolon}: mevcut")
        return False
    if default is not None:
        sql = f"ALTER TABLE {tablo} ADD COLUMN {kolon} {tip} DEFAULT {default}"
    else:
        sql = f"ALTER TABLE {tablo} ADD COLUMN {kolon} {tip}"
    cur.execute(sql)
    print(f"  ➕ {tablo}.{kolon}: eklendi")
    return True


def tablo_olustur(sql, tablo_adi):
    if tablo_var_mi(tablo_adi):
        print(f"✅ Tablo {tablo_adi}: mevcut")
        return False
    cur.execute(sql)
    print(f"🆕 Tablo {tablo_adi}: oluşturuldu")
    return True


def index_olustur(sql, index_adi):
    # CREATE INDEX IF NOT EXISTS her zaman güvenli
    cur.execute(sql)


# ─────────────────────────────────────────────
# Mevcut tablolar — çakışma kontrolü
# ─────────────────────────────────────────────

print("=== Mevcut tablolar kontrol ediliyor ===")
yeni_tablolar = ["binalar", "katlar", "mahaller", "is_kalemleri", "ilerleme_kayitlari"]
for t in yeni_tablolar:
    durum = "VAR (atlanacak)" if tablo_var_mi(t) else "YOK (oluşturulacak)"
    print(f"  {t}: {durum}")
print()

# ─────────────────────────────────────────────
# TABLOLAR (FK bağımlılık sırasıyla)
# ─────────────────────────────────────────────

try:
    print("=== Tablolar oluşturuluyor ===")

    # 1. binalar
    tablo_olustur("""
        CREATE TABLE IF NOT EXISTS binalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            santiye_id INTEGER NOT NULL REFERENCES santiyeler(id) ON DELETE CASCADE,
            ad TEXT NOT NULL,
            bina_tipi TEXT DEFAULT 'konut',
            toplam_kat INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """, "binalar")

    # 2. katlar
    tablo_olustur("""
        CREATE TABLE IF NOT EXISTS katlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bina_id INTEGER NOT NULL REFERENCES binalar(id) ON DELETE CASCADE,
            kat_no INTEGER NOT NULL,
            etiket TEXT,
            brut_alan_m2 REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """, "katlar")

    # 3. mahaller
    tablo_olustur("""
        CREATE TABLE IF NOT EXISTS mahaller (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kat_id INTEGER NOT NULL REFERENCES katlar(id) ON DELETE CASCADE,
            ad TEXT NOT NULL,
            mahal_tipi TEXT,
            alan_m2 REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """, "mahaller")

    # 4. is_kalemleri
    # birim_fiyat ve toplam_fiyat INTEGER — kuruş cinsinden (1 TL = 100 kuruş)
    # durum: planli | devam_eden | tamamlandi | iptal
    tablo_olustur("""
        CREATE TABLE IF NOT EXISTS is_kalemleri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mahal_id INTEGER REFERENCES mahaller(id) ON DELETE SET NULL,
            santiye_id INTEGER NOT NULL REFERENCES santiyeler(id) ON DELETE CASCADE,
            poz_no TEXT,
            tanim TEXT NOT NULL,
            birim TEXT NOT NULL,
            metraj REAL NOT NULL DEFAULT 0,
            birim_fiyat INTEGER NOT NULL DEFAULT 0,
            toplam_fiyat INTEGER NOT NULL DEFAULT 0,
            durum TEXT DEFAULT 'planli',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """, "is_kalemleri")

    # 5. ilerleme_kayitlari
    # yuzde: 0-100 arası
    tablo_olustur("""
        CREATE TABLE IF NOT EXISTS ilerleme_kayitlari (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            is_kalemi_id INTEGER NOT NULL REFERENCES is_kalemleri(id) ON DELETE CASCADE,
            raporlayan_id INTEGER REFERENCES users(id),
            yuzde REAL NOT NULL DEFAULT 0,
            tarih DATE NOT NULL,
            notlar TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """, "ilerleme_kayitlari")

    print()
    print("=== Mevcut tablolara sütun ekleniyor ===")

    # satin_alma.is_kalemi_id
    kolon_ekle("satin_alma", "is_kalemi_id", "INTEGER")

    # archive_records.is_kalemi_id
    kolon_ekle("archive_records", "is_kalemi_id", "INTEGER")

    print()
    print("=== İndeksler oluşturuluyor ===")

    index_olustur(
        "CREATE INDEX IF NOT EXISTS idx_binalar_santiye_id ON binalar(santiye_id)",
        "idx_binalar_santiye_id"
    )
    index_olustur(
        "CREATE INDEX IF NOT EXISTS idx_katlar_bina_id ON katlar(bina_id)",
        "idx_katlar_bina_id"
    )
    index_olustur(
        "CREATE INDEX IF NOT EXISTS idx_mahaller_kat_id ON mahaller(kat_id)",
        "idx_mahaller_kat_id"
    )
    index_olustur(
        "CREATE INDEX IF NOT EXISTS idx_is_kalemleri_mahal_id ON is_kalemleri(mahal_id)",
        "idx_is_kalemleri_mahal_id"
    )
    index_olustur(
        "CREATE INDEX IF NOT EXISTS idx_is_kalemleri_santiye_id ON is_kalemleri(santiye_id)",
        "idx_is_kalemleri_santiye_id"
    )
    index_olustur(
        "CREATE INDEX IF NOT EXISTS idx_ilerleme_is_kalemi_id ON ilerleme_kayitlari(is_kalemi_id)",
        "idx_ilerleme_is_kalemi_id"
    )
    index_olustur(
        "CREATE INDEX IF NOT EXISTS idx_satin_alma_is_kalemi_id ON satin_alma(is_kalemi_id)",
        "idx_satin_alma_is_kalemi_id"
    )
    index_olustur(
        "CREATE INDEX IF NOT EXISTS idx_archive_is_kalemi_id ON archive_records(is_kalemi_id)",
        "idx_archive_is_kalemi_id"
    )
    print("  ✅ Tüm indeksler oluşturuldu")

    conn.commit()
    print()
    print("✅ Migration tamamlandı.")

except Exception as e:
    conn.rollback()
    print(f"\n[HATA] Migration başarısız: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    conn.close()
