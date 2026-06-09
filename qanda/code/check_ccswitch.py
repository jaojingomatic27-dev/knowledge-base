import sqlite3, json

db = sqlite3.connect(r'C:\Users\jaoji\.cc-switch\cc-switch.db')
tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables:', [t[0] for t in tables])

for t in tables:
    if t[0] == 'sqlite_sequence':
        continue
    cols = [c[1] for c in db.execute(f'PRAGMA table_info({t[0]})').fetchall()]
    print(f'\n=== {t[0]} ({cols}) ===')
    rows = db.execute(f'SELECT * FROM {t[0]}').fetchall()
    for r in rows[:10]:
        print(r)

db.close()
