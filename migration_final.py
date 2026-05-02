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
    organization_id  INTEGER,
    telefon          TEXT DEFAULT '',
    role             TEXT DEFAULT 'santi_sefi',
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
    degisiklik |= kolon_ekle("users", "organization_id",        "INTEGER")
    degisiklik |= kolon_ekle("users", "telefon",                "TEXT",     "''")
    degisiklik |= kolon_ekle("users", "role",                   "TEXT",     "'santi_sefi'")
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
# 1b. organizations / project_members / invitations
if tablo_var_mi("users"):
    tablo_olustur("""
CREATE TABLE IF NOT EXISTS organizations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    owner_user_id INTEGER NOT NULL REFERENCES users(id),
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "organizations")

    tablo_olustur("""
CREATE TABLE IF NOT EXISTS project_members (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER NOT NULL REFERENCES organizations(id),
    user_id         INTEGER NOT NULL REFERENCES users(id),
    santiye_id      INTEGER REFERENCES santiyeler(id),
    role            TEXT NOT NULL DEFAULT 'muhendis',
    status          TEXT NOT NULL DEFAULT 'active',
    invited_by      INTEGER REFERENCES users(id),
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "project_members")

    tablo_olustur("""
CREATE TABLE IF NOT EXISTS invitations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER NOT NULL REFERENCES organizations(id),
    email           TEXT NOT NULL,
    role            TEXT NOT NULL DEFAULT 'muhendis',
    invited_by      INTEGER NOT NULL REFERENCES users(id),
    token           TEXT UNIQUE NOT NULL,
    expires_at      DATETIME NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "invitations")

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
    organization_id INTEGER,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    tarih      TEXT,
    content    TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "reports")

if tablo_var_mi("reports"):
    kolon_ekle("reports", "organization_id", "INTEGER")

# 3. kamera_analizler
tablo_olustur("""
CREATE TABLE IF NOT EXISTS kamera_analizler (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    santiye_id   INTEGER REFERENCES santiyeler(id),
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

if tablo_var_mi("kamera_analizler"):
    degisiklik = False
    degisiklik |= kolon_ekle("kamera_analizler", "organization_id", "INTEGER")
    degisiklik |= kolon_ekle("kamera_analizler", "santiye_id", "INTEGER")

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
    organization_id INTEGER,
    malzeme    TEXT NOT NULL,
    onceki     TEXT NOT NULL,
    yeni       TEXT NOT NULL,
    degisim    TEXT NOT NULL,
    status     TEXT DEFAULT 'pending',
    decided_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "malzeme_uyari")

if tablo_var_mi("malzeme_uyari"):
    kolon_ekle("malzeme_uyari", "organization_id", "INTEGER")
    kolon_ekle("malzeme_uyari", "status",     "TEXT",     "'pending'")
    kolon_ekle("malzeme_uyari", "decided_at", "DATETIME")

# 6b. review_decisions
tablo_olustur("""
CREATE TABLE IF NOT EXISTS review_decisions (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id            INTEGER NOT NULL REFERENCES users(id),
    source_type        TEXT NOT NULL,
    source_id          INTEGER NOT NULL,
    status             TEXT DEFAULT 'pending',
    decision_note      TEXT DEFAULT '',
    decided_by_user_id INTEGER,
    decided_at         DATETIME,
    created_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, source_type, source_id)
)
""", "review_decisions")

if tablo_var_mi("review_decisions"):
    degisiklik = False
    degisiklik |= kolon_ekle("review_decisions", "decision_note",      "TEXT",     "''")
    degisiklik |= kolon_ekle("review_decisions", "decided_by_user_id", "INTEGER")
    degisiklik |= kolon_ekle("review_decisions", "decided_at",         "DATETIME")
    degisiklik |= kolon_ekle("review_decisions", "created_at",         "DATETIME", "CURRENT_TIMESTAMP")
    degisiklik |= kolon_ekle("review_decisions", "updated_at",         "DATETIME", "CURRENT_TIMESTAMP")
    if not degisiklik:
        print("✅ Tablo review_decisions: tüm kolonlar mevcut")

# 7. stok
tablo_olustur("""
CREATE TABLE IF NOT EXISTS stok (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
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
    degisiklik = False
    degisiklik |= kolon_ekle("stok", "organization_id", "INTEGER")
    degisiklik |= kolon_ekle("stok", "santiye_id", "INTEGER")
    if not degisiklik:
        print("✅ Tablo stok: tüm kolonlar mevcut")

# 8. santiyeler
tablo_olustur("""
CREATE TABLE IF NOT EXISTS santiyeler (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER,
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
    degisiklik |= kolon_ekle("santiyeler", "organization_id", "INTEGER")
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


tablo_olustur("""
CREATE TABLE IF NOT EXISTS archive_records (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL REFERENCES users(id),
    santiye_id       INTEGER REFERENCES santiyeler(id),
    camera_id        INTEGER,
    source_type      TEXT DEFAULT 'manual',
    source_ref_type  TEXT DEFAULT '',
    source_ref_id    INTEGER,
    media_type       TEXT DEFAULT 'photo',
    file_url         TEXT DEFAULT '',
    thumbnail_url    TEXT DEFAULT '',
    file_name        TEXT DEFAULT '',
    mime_type        TEXT DEFAULT '',
    file_size        INTEGER DEFAULT 0,
    title            TEXT DEFAULT '',
    description      TEXT DEFAULT '',
    event_type       TEXT DEFAULT '',
    tags             TEXT DEFAULT '[]',
    zone_label       TEXT DEFAULT '',
    captured_at      DATETIME,
    duration_seconds TEXT DEFAULT '',
    gps_lat          TEXT DEFAULT '',
    gps_lon          TEXT DEFAULT '',
    exif_payload     TEXT DEFAULT '',
    ai_suggestions   TEXT DEFAULT '',
    status           TEXT DEFAULT 'active',
    verification_status TEXT DEFAULT 'DRAFT',
    workflow_status  TEXT DEFAULT 'NEW',
    deleted_at       DATETIME,
    uploaded_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "archive_records")

if tablo_var_mi("archive_records"):
    degisiklik = False
    degisiklik |= kolon_ekle("archive_records", "camera_id",          "INTEGER")
    degisiklik |= kolon_ekle("archive_records", "source_type",        "TEXT",     "'manual'")
    degisiklik |= kolon_ekle("archive_records", "source_ref_type",    "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "source_ref_id",      "INTEGER")
    degisiklik |= kolon_ekle("archive_records", "media_type",         "TEXT",     "'photo'")
    degisiklik |= kolon_ekle("archive_records", "file_url",           "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "thumbnail_url",      "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "file_name",          "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "mime_type",          "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "file_size",          "INTEGER",  "0")
    degisiklik |= kolon_ekle("archive_records", "title",              "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "description",        "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "event_type",         "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "tags",               "TEXT",     "'[]'")
    degisiklik |= kolon_ekle("archive_records", "zone_label",         "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "captured_at",        "DATETIME")
    degisiklik |= kolon_ekle("archive_records", "duration_seconds",   "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "gps_lat",            "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "gps_lon",            "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "exif_payload",       "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "ai_suggestions",     "TEXT",     "''")
    degisiklik |= kolon_ekle("archive_records", "status",             "TEXT",     "'active'")
    degisiklik |= kolon_ekle("archive_records", "verification_status","TEXT",     "'DRAFT'")
    degisiklik |= kolon_ekle("archive_records", "workflow_status",    "TEXT",     "'NEW'")
    degisiklik |= kolon_ekle("archive_records", "deleted_at",         "DATETIME")
    degisiklik |= kolon_ekle("archive_records", "uploaded_at",        "DATETIME", "CURRENT_TIMESTAMP")
    degisiklik |= kolon_ekle("archive_records", "created_at",         "DATETIME", "CURRENT_TIMESTAMP")
    degisiklik |= kolon_ekle("archive_records", "updated_at",         "DATETIME", "CURRENT_TIMESTAMP")
    if not degisiklik:
        print("✅ Tablo archive_records: tüm kolonlar mevcut")

tablo_olustur("""
CREATE TABLE IF NOT EXISTS daily_reports (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    santiye_id  INTEGER REFERENCES santiyeler(id),
    report_date TEXT NOT NULL,
    status      TEXT DEFAULT 'draft',
    verification_status TEXT DEFAULT 'DRAFT',
    workflow_status TEXT DEFAULT 'NEW',
    summary     TEXT DEFAULT '',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "daily_reports")

if tablo_var_mi("daily_reports"):
    degisiklik = False
    degisiklik |= kolon_ekle("daily_reports", "santiye_id",           "INTEGER")
    degisiklik |= kolon_ekle("daily_reports", "report_date",          "TEXT",     "''")
    degisiklik |= kolon_ekle("daily_reports", "status",               "TEXT",     "'draft'")
    degisiklik |= kolon_ekle("daily_reports", "verification_status",  "TEXT",     "'DRAFT'")
    degisiklik |= kolon_ekle("daily_reports", "workflow_status",      "TEXT",     "'NEW'")
    degisiklik |= kolon_ekle("daily_reports", "summary",              "TEXT",     "''")
    degisiklik |= kolon_ekle("daily_reports", "created_at",           "DATETIME", "CURRENT_TIMESTAMP")
    degisiklik |= kolon_ekle("daily_reports", "updated_at",           "DATETIME", "CURRENT_TIMESTAMP")
    if not degisiklik:
        print("✅ Tablo daily_reports: tüm kolonlar mevcut")

tablo_olustur("""
CREATE TABLE IF NOT EXISTS daily_report_items (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    daily_report_id  INTEGER NOT NULL REFERENCES daily_reports(id),
    archive_record_id INTEGER REFERENCES archive_records(id),
    source_type      TEXT DEFAULT 'manual',
    source_ref_id    INTEGER,
    section_key      TEXT NOT NULL,
    section_label    TEXT DEFAULT '',
    note             TEXT DEFAULT '',
    sort_order       INTEGER DEFAULT 0,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at       DATETIME DEFAULT CURRENT_TIMESTAMP
)
""", "daily_report_items")

if tablo_var_mi("daily_report_items"):
    degisiklik = False
    degisiklik |= kolon_ekle("daily_report_items", "archive_record_id",  "INTEGER")
    degisiklik |= kolon_ekle("daily_report_items", "source_type",        "TEXT",     "'manual'")
    degisiklik |= kolon_ekle("daily_report_items", "source_ref_id",      "INTEGER")
    degisiklik |= kolon_ekle("daily_report_items", "section_key",        "TEXT",     "''")
    degisiklik |= kolon_ekle("daily_report_items", "section_label",      "TEXT",     "''")
    degisiklik |= kolon_ekle("daily_report_items", "note",               "TEXT",     "''")
    degisiklik |= kolon_ekle("daily_report_items", "sort_order",         "INTEGER",  "0")
    degisiklik |= kolon_ekle("daily_report_items", "created_at",         "DATETIME", "CURRENT_TIMESTAMP")
    degisiklik |= kolon_ekle("daily_report_items", "updated_at",         "DATETIME", "CURRENT_TIMESTAMP")
    if not degisiklik:
        print("✅ Tablo daily_report_items: tüm kolonlar mevcut")

# 12. reset_tokens
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

# 13. login_attempts
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