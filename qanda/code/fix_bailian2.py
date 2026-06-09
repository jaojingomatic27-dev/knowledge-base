import sqlite3, json

db = sqlite3.connect(r'C:\Users\jaoji\.cc-switch\cc-switch.db')

provider_id = 'ed98d912-71c0-4b7e-a9d3-252125c146c2'
api_key = 'sk-ws-djI.Tw66uUd98NeXNIvIRTwito-yxMj8dz3DszW3R7d8t4bbUVfutasL4HDw8kpiS6BXow1umi8Jk3FeDWLQj0GxHqPV62qfCwioa3VcB6UOYDQfnfS8xM8IG4dzeHP5Lgy2.MEQCIAKCyb_apTSbh34qV0MrhpLeC_coqILKqFX8zLNVhBszAiA_0IWXahIumljH2B1-A9O3ti2QJlmBzyjhEYKDm7tCFw'
# CSV row: apiHost = ws-v4cbycsu1jig5w31.eu-central-1.maas.aliyuncs.com
# CSV row: openAiCompatible = https://ws-v4cbycsu1jig5w31.eu-central-1.maas.aliyuncs.com/compatible-mode/v1
workspace_host = 'ws-v4cbycsu1jig5w31.eu-central-1.maas.aliyuncs.com'
workspace_url = f'https://{workspace_host}/compatible-mode/v1'

# Fix settings_config: ANTHROPIC_API_KEY not AUTH_TOKEN, + model
new_settings = {
    "env": {
        "ANTHROPIC_API_KEY": api_key,
        "ANTHROPIC_BASE_URL": workspace_url,
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen-turbo-latest",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3-coder-plus",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3-coder-plus",
        "ANTHROPIC_MODEL": "qwen3-coder-plus"
    },
    "skipDangerousModePermissionPrompt": True
}

db.execute("UPDATE providers SET settings_config=? WHERE id=?",
    (json.dumps(new_settings), provider_id))

# Fix meta: openai-compatible + needsLocalRouting
new_meta = {
    "commonConfigEnabled": True,
    "endpointAutoSelect": True,
    "apiFormat": "openai-compatible",
    "needsLocalRouting": True,
    "apiKeyField": "ANTHROPIC_API_KEY"
}
db.execute("UPDATE providers SET meta=? WHERE id=?",
    (json.dumps(new_meta), provider_id))

# Fix endpoint URL
db.execute("UPDATE provider_endpoints SET url=? WHERE provider_id=?",
    (workspace_url, provider_id))

# Ensure proxy is enabled
db.execute("UPDATE proxy_config SET proxy_enabled=1, enabled=1 WHERE app_type='claude'")

db.commit()

# Verify
p = db.execute("SELECT id, name, meta, settings_config FROM providers WHERE id=?", (provider_id,)).fetchone()
print("=== 修复验证 ===")
print("id:", p[0])
print("name:", p[1])
print("meta:", p[2])
s = json.loads(p[3])
print("env:")
for k, v in s['env'].items():
    if 'KEY' in k:
        print(f"  {k}: {v[:30]}...")
    else:
        print(f"  {k}: {v}")

ep = db.execute("SELECT url FROM provider_endpoints WHERE provider_id=?", (provider_id,)).fetchone()
print(f"endpoint: {ep[0]}")

db.close()

print("\n=== 下一步 ===")
print("1. 完全退出 CC Switch (系统托盘右键→Quit)")
print("2. 重新启动 CC Switch")
print("3. 切换到 Bailian")
print("4. 运行 Stream Check")
