"""
Faz 14 Migration — 3 Kademeli Plan Sistemi
Çalıştır: python migrate_faz14.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "buildingai.db")

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # users.plan sütunu zaten var; 'admin' değerine izin vermek için
    # SQLite'ta CHECK kısıtı yoksa ek bir şey gerekmez.
    # Ancak mevcut NULL plan değerlerini 'free' yap.
    cur.execute("UPDATE users SET plan = 'free' WHERE plan IS NULL OR plan = ''")
    updated = cur.rowcount
    print(f"  ✅ {updated} kullanıcının plan değeri 'free' olarak güncellendi.")

    # Kontrol: geçersiz plan değeri var mı?
    cur.execute("SELECT id, email, plan FROM users WHERE plan NOT IN ('free','pro','max','admin')")
    invalid = cur.fetchall()
    if invalid:
        print(f"  ⚠️  Geçersiz plan değeri olan kullanıcılar:")
        for row in invalid:
            print(f"     id={row[0]}  email={row[1]}  plan={row[2]}")
        print("     Bunları 'free' olarak sıfırlıyorum...")
        cur.execute("UPDATE users SET plan = 'free' WHERE plan NOT IN ('free','pro','max','admin')")

    conn.commit()
    conn.close()
    print("  ✅ Faz 14 migrasyonu tamamlandı.")

if __name__ == "__main__":
    print(f"Veritabanı: {DB_PATH}")
    migrate()
