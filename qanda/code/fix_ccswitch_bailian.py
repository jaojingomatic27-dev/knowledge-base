import sqlite3, json

db = sqlite3.connect(r'C:\Users\jaoji\.cc-switch\cc-switch.db')

# 1. Enable Claude proxy
db.execute("UPDATE proxy_config SET proxy_enabled=1, enabled=1 WHERE app_type='claude'")
print("1. Claude local proxy enabled")

# 2. Fix Bailian provider: mark as openai-compatible so CC Switch routes through proxy
meta = json.loads(db.execute("SELECT meta FROM providers WHERE id='200d6fd7-8817-4db1-bc90-32a57275674c'").fetchone()[0])
print(f"   Current meta: {meta}")
meta['apiFormat'] = 'openai-compatible'  # Tell CC Switch this needs translation
db.execute("UPDATE providers SET meta=? WHERE id='200d6fd7-8817-4db1-bc90-32a57275674c'", (json.dumps(meta),))
print(f"   Updated meta: {meta}")

# 3. Update the endpoint URL to use the correct workspace endpoint from CSV
# (current endpoint in DB is the workspace URL which is correct)
endpoints = db.execute("SELECT * FROM provider_endpoints WHERE provider_id='200d6fd7-8817-4db1-bc90-32a57275674c'").fetchall()
print(f"   Endpoints: {endpoints}")

# 4. Update provider BASE_URL to match the workspace endpoint
settings_config = json.loads(db.execute("SELECT settings_config FROM providers WHERE id='200d6fd7-8817-4db1-bc90-32a57275674c'").fetchone()[0])
print(f"   Current ANTHROPIC_BASE_URL: {settings_config['env']['ANTHROPIC_BASE_URL']}")
# Update to workspace endpoint
settings_config['env']['ANTHROPIC_BASE_URL'] = 'https://ws-v4cbycsu1jig5w31.eu-central-1.maas.aliyuncs.com/compatible-mode/v1'
db.execute("UPDATE providers SET settings_config=? WHERE id='200d6fd7-8817-4db1-bc90-32a57275674c'", (json.dumps(settings_config),))
print(f"   Updated ANTHROPIC_BASE_URL")

db.commit()
db.close()
print("\nDone. Restart CC Switch for changes to take effect.")
