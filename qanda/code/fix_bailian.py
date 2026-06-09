import sqlite3, json

db = sqlite3.connect(r'C:\Users\jaoji\.cc-switch\cc-switch.db')

provider_id = 'ed98d912-71c0-4b7e-a9d3-252125c146c2'
api_key = 'sk-ws-djI.Tw66uUd98NeXNIvIRTwito-yxMj8dz3DszW3R7d8t4bbUVfutasL4HDw8kpiS6BXow1umi8Jk3FeDWLQj0GxHqPV62qfCwioa3VcB6UOYDQfnfS8xM8IG4dzeHP5Lgy2.MEQCIAKCyb_apTSbh34qV0MrhpLeC_coqILKqFX8zLNVhBszAiA_0IWXahIumljH2B1-A9O3ti2QJlmBzyjhEYKDm7tCFw'
workspace_url = 'https://ws-v4cbycsu1jig5w31.eu-central-1.maas.aliyuncs.com/compatible-mode/v1'

# Fix settings_config: use ANTHROPIC_API_KEY (not AUTH_TOKEN), workspace URL
new_settings = {
    "env": {
        "ANTHROPIC_API_KEY": api_key,
        "ANTHROPIC_BASE_URL": workspace_url,
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen-turbo",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3-coder-plus",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3-coder-plus",
        "ANTHROPIC_MODEL": "qwen3-coder-plus"
    },
    "skipDangerousModePermissionPrompt": True
}

db.execute("UPDATE providers SET settings_config=? WHERE id=?", (json.dumps(new_settings), provider_id))

# Fix meta: this is openai-compatible, needs local routing
db.execute("UPDATE providers SET meta=? WHERE id=?",
    (json.dumps({"commonConfigEnabled": True, "endpointAutoSelect": True, "apiFormat": "openai-compatible", "needsLocalRouting": True}), provider_id))

# Delete old 200d6fd7 entry if it exists
db.execute("DELETE FROM providers WHERE id='200d6fd7-8817-4db1-bc90-32a57275674c'")
db.execute("DELETE FROM stream_check_logs WHERE provider_id='200d6fd7-8817-4db1-bc90-32a57275674c'")

# Ensure proxy is on
db.execute("UPDATE proxy_config SET proxy_enabled=1, enabled=1 WHERE app_type='claude'")

db.commit()

# Verify
p = db.execute("SELECT id, name, meta, settings_config FROM providers WHERE id=?", (provider_id,)).fetchone()
print('=== Fixed ===')
print('meta:', p[2])
s = json.loads(p[3])
print('env:')
for k, v in s['env'].items():
    if 'KEY' in k: print(f'  {k}: {v[:25]}...')
    else: print(f'  {k}: {v}')
print('\nDone. Now:')
print('1. Restart CC Switch')
print('2. Select Bailian as current provider')
print('3. Run Stream Check')

db.close()
