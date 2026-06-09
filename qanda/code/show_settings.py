import sqlite3, json

db = sqlite3.connect(r'C:\Users\jaoji\.cc-switch\cc-switch.db')

# All providers
ps = db.execute("SELECT id, name, app_type, is_current, meta, settings_config FROM providers").fetchall()
print("=" * 60)
print("ALL PROVIDERS")
print("=" * 60)
for p in ps:
    mark = " *** CURRENT ***" if p[3] else ""
    s = json.loads(p[5]) if p[5] else {}
    env = s.get('env', {})
    base_url = env.get('ANTHROPIC_BASE_URL', 'N/A')
    model = env.get('ANTHROPIC_MODEL', 'N/A')
    print(f"\n{p[1]} ({p[2]}){mark}")
    print(f"  id: {p[0]}")
    print(f"  apiFormat: {json.loads(p[4]).get('apiFormat', 'N/A') if p[4] else 'N/A'}")
    print(f"  BASE_URL: {base_url}")
    print(f"  MODEL: {model}")

# Proxy
print("\n" + "=" * 60)
print("PROXY CONFIG")
print("=" * 60)
pxs = db.execute("SELECT app_type, proxy_enabled, enabled, listen_address, listen_port FROM proxy_config").fetchall()
for px in pxs:
    print(f"  {px[0]}: proxy={px[1]} enabled={px[2]} {px[3]}:{px[4]}")

# Stream checks
print("\n" + "=" * 60)
print("RECENT STREAM CHECKS")
print("=" * 60)
scs = db.execute("SELECT provider_name, status, success, message, http_status, tested_at FROM stream_check_logs ORDER BY tested_at DESC LIMIT 10").fetchall()
for sc in scs:
    print(f"  {sc[0]}: {sc[1]} (success={sc[2]}, http={sc[4]}) {sc[3]}")

# Claude settings
print("\n" + "=" * 60)
print("CC SWITCH settings.json")
print("=" * 60)
with open(r'C:\Users\jaoji\.cc-switch\settings.json') as f:
    s = json.load(f)
    for k, v in s.items():
        if isinstance(v, dict):
            print(f"  {k}: {json.dumps(v)[:100]}")
        else:
            print(f"  {k}: {v}")

db.close()
