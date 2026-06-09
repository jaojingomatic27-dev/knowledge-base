import sqlite3, json

db = sqlite3.connect(r'C:\Users\jaoji\.cc-switch\cc-switch.db')

# Show all providers
prods = db.execute("SELECT id, name, app_type, is_current FROM providers").fetchall()
print('=== All Providers ===')
for p in prods:
    print(p)

# Show current claude provider from settings.json
setting = db.execute("SELECT value FROM settings WHERE key LIKE '%claude%'").fetchall()
print('\n=== Claude Settings ===')
for s in setting:
    print(s)

# Proxy
proxy = db.execute("SELECT * FROM proxy_config WHERE app_type='claude'").fetchall()
print('\n=== Claude Proxy ===')
for p in proxy:
    print('proxy_enabled:', p[1], 'enabled:', p[5])

# Last stream checks
checks = db.execute("SELECT id, provider_name, status, success, message, http_status FROM stream_check_logs ORDER BY id DESC LIMIT 5").fetchall()
print('\n=== Last Stream Checks ===')
for c in checks:
    print(c)

db.close()
