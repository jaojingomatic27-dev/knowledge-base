import sqlite3, json

db = sqlite3.connect(r'C:\Users\jaoji\.cc-switch\cc-switch.db')

provider_id = 'ed98d912-71c0-4b7e-a9d3-252125c146c2'

p = db.execute("SELECT id, name, meta, settings_config, provider_type FROM providers WHERE id=?", (provider_id,)).fetchone()
print('=== Bailian Provider ===')
print('id:', p[0])
print('meta:', p[2])
print('provider_type:', p[4])

settings = json.loads(p[3])
print('settings_config:')
for k, v in settings.items():
    if 'KEY' in k:
        print(f'  {k}: {str(v)[:30]}...')
    else:
        print(f'  {k}: {v}')

# Endpoint
eps = db.execute("SELECT * FROM provider_endpoints WHERE provider_id=?", (provider_id,)).fetchall()
print('endpoints:', eps)

# Check if there's a new entry or was recreated
print('\nAll provider ids in stream_check:')
ids = db.execute("SELECT DISTINCT provider_id FROM stream_check_logs").fetchall()
for i in ids:
    print(' ', i[0])

db.close()
