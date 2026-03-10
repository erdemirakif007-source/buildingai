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

conn.commit()
conn.close()
print("Tamamlandı!")
