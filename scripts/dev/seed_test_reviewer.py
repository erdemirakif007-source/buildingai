"""
Yerel geliştirme veritabanına test onaylayıcı kullanıcı ekler.

Sadece SQLite veritabanında ve BUILDINGAI_ENV=production OLMAYAN ortamda çalışır.

Kullanım:
    python scripts/dev/seed_test_reviewer.py [--password SIFRE] [--org ORG_ID] [--site SITE_ID]
"""

import sys
import os
import argparse
import secrets
import string

# Uygulama kök dizinini sys.path'e ekle (modeller buradan import edilir)
_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(_ROOT))

# --- Güvenlik kontrolleri (modüller import edilmeden önce) ---
_DB_URL = os.getenv("DATABASE_URL", "sqlite:///./santiye_proje.db")
_ENV = os.getenv("BUILDINGAI_ENV", "")

if "sqlite" not in _DB_URL:
    print("HATA: Bu script sadece yerel geliştirme veritabanında çalışır.")
    print(f"  DATABASE_URL: {_DB_URL[:40]}...")
    sys.exit(1)

if _ENV.lower() == "production":
    print("HATA: Bu script sadece yerel geliştirme veritabanında çalışır.")
    print("  BUILDINGAI_ENV=production ortamında çalıştırılamaz.")
    sys.exit(1)

# --- Uygulama modülleri ---
from database import SessionLocal
import models
from auth import get_password_hash
from access_control import REVIEW_ROLES

# REVIEW_ROLES içindeki kanonik roller (alias'lar hariç)
_CANONICAL_REVIEW_ROLES = {"santi_sefi", "muteahhit", "yonetici", "proje_muduru"}

# require_site(..., "review") kontrolünü geçecek minimum rol.
# REVIEW_ROLES = WRITE_ROLES - {"muhendis"} = {santi_sefi, muteahhit, yonetici, proje_muduru}
# Test için en az ayrıcalıklı kanonik rol olan santi_sefi seçildi.
REVIEWER_ROLE = "santi_sefi"

TEST_EMAIL = "test.onayci@buildingai.local"
TEST_FULL_NAME = "Test Onaycı"


def _random_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def main():
    parser = argparse.ArgumentParser(description="Test onaylayıcı kullanıcı oluştur")
    parser.add_argument("--password", default=None, help="Kullanıcı şifresi (verilmezse rastgele üretilir)")
    parser.add_argument("--org", type=int, default=5, help="Organization ID (varsayılan: 5)")
    parser.add_argument("--site", type=int, default=5, help="Şantiye ID (varsayılan: 5)")
    args = parser.parse_args()

    generated = False
    password = args.password
    if not password:
        password = _random_password()
        generated = True

    print("\n=== BuildingAI — Test Onaycı Seed Script ===")
    print(f"  Veritabanı  : {_DB_URL}")
    print(f"  Organization: {args.org}")
    print(f"  Şantiye     : {args.site}")
    print(f"  Rol seçimi  : '{REVIEWER_ROLE}' — REVIEW_ROLES {sorted(_CANONICAL_REVIEW_ROLES)} içinde")
    print(f"                muhendis kasıtlı dışarıda (require_site action='review' onu reddeder)\n")

    db = SessionLocal()
    try:
        # 1. Kullanıcı
        user = db.query(models.User).filter_by(email=TEST_EMAIL).first()
        if user:
            print(f"[MEVCUT] Kullanıcı zaten var → id={user.id}, email={user.email}")
        else:
            user = models.User(
                email=TEST_EMAIL,
                full_name=TEST_FULL_NAME,
                hashed_password=get_password_hash(password),
                auth_provider="local",
                email_verified=True,
                organization_id=args.org,
            )
            db.add(user)
            db.flush()  # id'yi al, henüz commit etme
            print(f"[OLUŞTURULDU] Kullanıcı → id={user.id}, email={user.email}")

        # 2. Şantiye üyeliği
        existing_member = db.query(models.ProjectMember).filter_by(
            user_id=user.id,
            organization_id=args.org,
            santiye_id=args.site,
        ).first()

        if existing_member:
            print(
                f"[MEVCUT] Üyelik zaten var → user_id={user.id}, "
                f"org={args.org}, santiye={args.site}, rol='{existing_member.role}', "
                f"status='{existing_member.status}'"
            )
        else:
            member = models.ProjectMember(
                organization_id=args.org,
                user_id=user.id,
                santiye_id=args.site,
                role=REVIEWER_ROLE,
                status="active",
            )
            db.add(member)
            print(
                f"[OLUŞTURULDU] Üyelik → user_id={user.id}, "
                f"org={args.org}, santiye={args.site}, rol='{REVIEWER_ROLE}', status='active'"
            )

        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    print("\n--- Giriş Bilgileri ---")
    print(f"  E-posta     : {TEST_EMAIL}")
    if generated:
        print(f"  Şifre       : {password}  ← rastgele üretildi, kaydet!")
    else:
        print(f"  Şifre       : (argüman olarak verildi)")
    print(f"  Organization: {args.org}")
    print(f"  Şantiye     : {args.site}")
    print(f"  Rol         : {REVIEWER_ROLE}")
    print()


if __name__ == "__main__":
    main()
