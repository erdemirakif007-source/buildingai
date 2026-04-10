"""
BuildingAI — VideoAnaliz tablosu migrasyonu
Çalıştır: python migrate_yolo.py
"""

import sys
import database
import models

def migrate():
    print("[migrate_yolo] video_analizler tablosu kontrol ediliyor...")
    try:
        models.Base.metadata.create_all(
            bind=database.engine,
            tables=[models.VideoAnaliz.__table__],
            checkfirst=True,
        )
        print("[migrate_yolo] ✓ video_analizler tablosu hazır.")
    except Exception as exc:
        print(f"[migrate_yolo] ✗ Hata: {exc}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    migrate()
