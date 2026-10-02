from database import engine

DDL = """
CREATE TABLE IF NOT EXISTS hakedisler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organization_id INTEGER REFERENCES organizations(id),
    santiye_id INTEGER NOT NULL REFERENCES santiyeler(id) ON DELETE CASCADE,
    hakedis_no INTEGER NOT NULL,
    donem_baslangic TEXT NOT NULL,
    donem_bitis TEXT NOT NULL,
    durum TEXT DEFAULT 'taslak',
    hazirlayan_id INTEGER REFERENCES users(id),
    onaylayan_id INTEGER REFERENCES users(id),
    toplam_tutar INTEGER DEFAULT 0,
    onceki_toplam INTEGER DEFAULT 0,
    notlar TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(santiye_id, hakedis_no)
);

CREATE TABLE IF NOT EXISTS hakedis_kalemleri (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hakedis_id INTEGER NOT NULL REFERENCES hakedisler(id) ON DELETE CASCADE,
    is_kalemi_id INTEGER NOT NULL REFERENCES is_kalemleri(id) ON DELETE CASCADE,
    sozlesme_metraj REAL DEFAULT 0,
    onceki_toplam_miktar REAL DEFAULT 0,
    bu_donem_miktar REAL DEFAULT 0,
    kumulatif_miktar REAL DEFAULT 0,
    birim_fiyat INTEGER DEFAULT 0,
    bu_donem_tutar INTEGER DEFAULT 0,
    kumulatif_tutar INTEGER DEFAULT 0,
    notlar TEXT,
    UNIQUE(hakedis_id, is_kalemi_id)
);

CREATE INDEX IF NOT EXISTS idx_hakedisler_santiye ON hakedisler(santiye_id);
CREATE INDEX IF NOT EXISTS idx_hakedisler_org ON hakedisler(organization_id);
CREATE INDEX IF NOT EXISTS idx_hakedisler_durum ON hakedisler(durum);
CREATE INDEX IF NOT EXISTS idx_hakedis_kalemleri_hakedis ON hakedis_kalemleri(hakedis_id);
CREATE INDEX IF NOT EXISTS idx_hakedis_kalemleri_is_kalemi ON hakedis_kalemleri(is_kalemi_id);
"""

def run():
    with engine.begin() as conn:
        for statement in DDL.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                conn.execute(__import__("sqlalchemy").text(stmt))

    print("hakedisler tablosu: OK")
    print("hakedis_kalemleri tablosu: OK")
    print("indexler: OK")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"HATA Migration: {e}")
        raise
