import sqlite3
conn = sqlite3.connect('santiye_proje.db')
conn.execute("INSERT INTO reports (user_id, tarih, content, created_at) VALUES (1, '2026-03-09', 'test', '2026-03-09')")
conn.commit()
print('Tamam!')
conn.close()