import sqlite3

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

# Admin kullanıcıyı güncelle
conn.execute("UPDATE users SET is_admin = 1 WHERE email = 'erdemirakif007@gmail.com'")
print(f"Admin güncellendi: {conn.total_changes} satır etkilendi")

conn.commit()
conn.close()
print("Tamamlandı!")
