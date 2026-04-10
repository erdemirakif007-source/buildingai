"""
migration_final.py — BuildingAI Tek ve Güvenilir Migration Scripti
Çalıştır: python migration_final.py

- DATABASE_URL env varsa PostgreSQL modunda çalışır
- Yoksa santiye_proje.db SQLite kullanır
- Tüm tabloları oluşturur, eksik kolonları ekler
"""
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "erdemirakif007@gmail.com")

# Railway postgres:// → postgresql:// fix
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
        placeholder = "%s"
        print(f"[DB] PostgreSQL modunda çalışıyor: {parsed.hostname}")
    except Exception as e:
        print(f"[HATA] PostgreSQL bağlantısı kurulamadı: {e}")
        sys.exit(1)
else:
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), "santiye_proje.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    placeholder = "?"
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

# ─────────────────────────────────────────────
# TABLOLAR
# ─────────────────────────────────────────────

# 1. users
tablo_olustur("""
CREATE TABLE IF NOT EXISTS users (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    email            TEXT UNIQUE NOT NULL,
    hashed_password  TEXT NOT NULL,
    full_name        TEXT DEFAULT '',
    plan             TEXT DEFAULT 'free',
    is_admin         BOOLEAN NOT NULL DEFAULT 0,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    google_id                TEXT,
    sifre_sifirla_token      TEXT,
    sifre_sifirla_expires    DATETIME,
    odeme_bildirimi_tarihi   DATETIME,
    odeme_miktari            TEXT,
    odeme_aciklama           TEXT,
    plan_bitis_tarihi        DATETIME
)
""", "users")

# users eksik kolonlar
if tablo_var_mi("users"):
    degisiklik = False
    degisiklik |= kolon_ekle("users", "plan",                   "TEXT",     "'free'")
    degisiklik |= kolon_ekle("users", "created_at",             "DATETIME", "CURRENT_TIMESTAMP")
    degisiklik |= kolon_ekle("users", "is_admin",               "BOOLEAN",  "0")
    degisiklik |= kolon_ekle("users", "google_id",              "TEXT")
    degisiklik |= kolon_ekle("users", "sifre_sifirla_token",    "TEXT")
    degisiklik |= kolon_ekle("users", "sifre_sifirla_expires",  "DATETIME")
    degisiklik |= kolon_ekle("users", "odeme_bildirimi_tarihi", "DATETIME")
    degisiklik |= kolon_ekle("users", "odeme_miktari",          "TEXT")
    degisiklik |= kolon_ekle("users", "odeme_aciklama",         "TEXT")
    degisiklik |= kolon_ekle("users", "plan_bitis_tarihi",      "DATETIME")
    if not degisiklik:
        print("✅ Tablo users: tüm kolonlar mevcut")

# Admin kullanıcıyı güncelle
if USE_POSTGRES:
    cur.execute("UPDATE users SET is_admin = TRUE WHERE email = %s", (ADMIN_EMAIL,))
else:
    cur.execute("UPDATE users SET is_admin = 1 WHERE email = ?", (ADMIN_EMAIL,))
etkilenen = cur.rowcount
if etkilenen > 0:
    print(f"  👑 Admin güncellendi: {ADMIN_EMAIL}")

# 2. reports
tablo_olustur("""
CREATE TABLE IF NOT EXISTS reports (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    tarih      TEXT,
    content    TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "reports")

# 3. kamera_analizler
tablo_olustur("""
CREATE TABLE IF NOT EXISTS kamera_analizler (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    analiz_tipi  TEXT,
    sonuc        TEXT,
    ihlaller     TEXT DEFAULT '',
    resim_base64 TEXT DEFAULT '',
    sehir        TEXT DEFAULT '',
    hava         TEXT DEFAULT '',
    dil          TEXT DEFAULT 'tr',
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "kamera_analizler")

# 4. usage
tablo_olustur("""
CREATE TABLE IF NOT EXISTS usage (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    tip        TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "usage")

# 5. malzeme_fiyat
tablo_olustur("""
CREATE TABLE IF NOT EXISTS malzeme_fiyat (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    malzeme    TEXT NOT NULL,
    fiyat      TEXT NOT NULL,
    birim      TEXT DEFAULT '',
    sehir      TEXT DEFAULT 'genel',
    kaynak     TEXT DEFAULT 'admin',
    giren_id   INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "malzeme_fiyat")

# 6. malzeme_uyari
tablo_olustur("""
CREATE TABLE IF NOT EXISTS malzeme_uyari (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    malzeme    TEXT NOT NULL,
    onceki     TEXT NOT NULL,
    yeni       TEXT NOT NULL,
    degisim    TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "malzeme_uyari")

# 7. stok
tablo_olustur("""
CREATE TABLE IF NOT EXISTS stok (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    santiye_id INTEGER REFERENCES santiyeler(id),
    malzeme    TEXT NOT NULL,
    malzeme_ad TEXT DEFAULT '',
    miktar     TEXT NOT NULL,
    birim      TEXT DEFAULT '',
    tip        TEXT NOT NULL,
    tedarikci  TEXT DEFAULT '',
    fiyat      TEXT DEFAULT '',
    notlar     TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "stok")

# stok eksik kolonlar
if tablo_var_mi("stok"):
    degisiklik = kolon_ekle("stok", "santiye_id", "INTEGER")
    if not degisiklik:
        print("✅ Tablo stok: tüm kolonlar mevcut")

# 8. santiyeler
tablo_olustur("""
CREATE TABLE IF NOT EXISTS santiyeler (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    ad          TEXT NOT NULL,
    konum       TEXT DEFAULT '',
    lat         TEXT DEFAULT '',
    lon         TEXT DEFAULT '',
    ilerleme    INTEGER DEFAULT 0,
    isci_sayisi INTEGER DEFAULT 0,
    durum       TEXT DEFAULT 'iyi',
    isg_durumu  TEXT DEFAULT 'Normal',
    notlar      TEXT DEFAULT '',
    aktif       BOOLEAN DEFAULT 1,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "santiyeler")

# santiyeler eksik kolonlar
if tablo_var_mi("santiyeler"):
    degisiklik = False
    degisiklik |= kolon_ekle("santiyeler", "kullanici_id",  "INTEGER")
    degisiklik |= kolon_ekle("santiyeler", "ad",            "TEXT",     "''")
    degisiklik |= kolon_ekle("santiyeler", "konum",         "TEXT",     "''")
    degisiklik |= kolon_ekle("santiyeler", "enlem",         "TEXT",     "''")
    degisiklik |= kolon_ekle("santiyeler", "boylam",        "TEXT",     "''")
    degisiklik |= kolon_ekle("santiyeler", "ilerleme",      "INTEGER",  "0")
    degisiklik |= kolon_ekle("santiyeler", "isci_sayisi",   "INTEGER",  "0")
    degisiklik |= kolon_ekle("santiyeler", "durum",         "TEXT",     "'iyi'")
    degisiklik |= kolon_ekle("santiyeler", "isg_not",       "TEXT",     "''")
    degisiklik |= kolon_ekle("santiyeler", "notlar",        "TEXT",     "''")
    degisiklik |= kolon_ekle("santiyeler", "created_at",    "DATETIME", "CURRENT_TIMESTAMP")
    degisiklik |= kolon_ekle("santiyeler", "updated_at",    "DATETIME", "CURRENT_TIMESTAMP")
    if not degisiklik:
        print("✅ Tablo santiyeler: tüm kolonlar mevcut")

# 9. reset_tokens
tablo_olustur("""
CREATE TABLE IF NOT EXISTS reset_tokens (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    email      TEXT NOT NULL,
    token      TEXT NOT NULL,
    expires_at DATETIME NOT NULL,
    used       BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "reset_tokens")

# 10. login_attempts
tablo_olustur("""
CREATE TABLE IF NOT EXISTS login_attempts (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT NOT NULL UNIQUE,
    attempt_count INTEGER DEFAULT 0,
    last_attempt  DATETIME DEFAULT CURRENT_TIMESTAMP,
    locked_until  DATETIME
)
""", "login_attempts")

# ─────────────────────────────────────────────
# Commit & kapat
# ─────────────────────────────────────────────
conn.commit()
cur.close()
conn.close()

print()
print("✅ migration_final.py tamamlandı.")
