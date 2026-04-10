import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "erdemirakif007@gmail.com")

conn = sqlite3.connect('santiye_proje.db')

try:
    conn.execute('ALTER TABLE users ADD COLUMN plan TEXT DEFAULT "free"')
    print("plan kolonu eklendi")
except Exception as e:
    print(f"plan: {e}")

try:
    conn.execute('ALTER TABLE users ADD COLUMN created_at TEXT')
    print("created_at kolonu eklendi")
except Exception as e:
    print(f"created_at: {e}")

# is_admin migration
try:
    conn.execute('ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0')
    print("is_admin kolonu eklendi")
except Exception as e:
    print(f"is_admin: {e}")

# Şantiye foto kolonu
try:
    conn.execute('ALTER TABLE santiyeler ADD COLUMN foto TEXT DEFAULT NULL')
    print("foto kolonu eklendi")
except Exception as e:
    print(f"foto: {e}")

# Admin kullanıcıyı güncelle
conn.execute(f"UPDATE users SET is_admin = 1 WHERE email = '{ADMIN_EMAIL}'")
print(f"Admin güncellendi: {conn.total_changes} satır etkilendi")

conn.commit()
conn.close()
print("Tamamlandı!")
