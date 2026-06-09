import sqlite3, json

db = sqlite3.connect(r'C:\Users\jaoji\.cc-switch\cc-switch.db')

# Find Bailian ID
bailian = db.execute("SELECT id, settings_config, meta FROM providers WHERE name='Bailian' AND app_type='claude'").fetchone()
deepseek_id = db.execute("SELECT id FROM providers WHERE name='DeepSeek' AND app_type='claude'").fetchone()[0]

print(f"Bailian ID: {bailian[0]}")
print(f"DeepSeek ID: {deepseek_id}")

# 1. Set Bailian as current, unset DeepSeek
db.execute("UPDATE providers SET is_current=0 WHERE app_type='claude'")
db.execute("UPDATE providers SET is_current=1 WHERE id=?", (bailian[0],))

# 2. Update settings.json pointer
db.execute("UPDATE settings SET value=? WHERE key='currentProviderClaude'", (bailian[0],))

# 3. Write Claude Code settings.json to route through proxy
claude_settings = {
    "env": {
        "ANTHROPIC_API_KEY": "PROXY_MANAGED",
        "ANTHROPIC_BASE_URL": "http://127.0.0.1:15721",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": "qwen-turbo-latest",
        "ANTHROPIC_DEFAULT_OPUS_MODEL": "qwen3-coder-plus",
        "ANTHROPIC_DEFAULT_SONNET_MODEL": "qwen3-coder-plus"
    },
    "includeCoAuthoredBy": False,
    "skipDangerousModePermissionPrompt": True,
    "theme": "auto",
    "model": "opus"
}

with open(r'C:\Users\jaoji\.claude\settings.json', 'w', encoding='utf-8') as f:
    json.dump(claude_settings, f, indent=2, ensure_ascii=False)
print("\nClaude Code settings.json updated")

db.commit()

# Verify
cur = db.execute("SELECT id, name FROM providers WHERE app_type='claude' AND is_current=1").fetchone()
print(f"\nCurrent: {cur[1]} ({cur[0][:8]}...)")

settings = db.execute("SELECT value FROM settings WHERE key='currentProviderClaude'").fetchone()
print(f"Settings currentProviderClaude: {settings[0][:8]}... matches: {settings[0] == bailian[0]}")

db.close()
print("\nDone. Restart Claude Code (close VS Code and reopen, or /restart)")
