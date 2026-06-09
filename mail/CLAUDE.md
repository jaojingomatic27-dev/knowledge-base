# CLAUDE.md — mail 项目

本文件补充 `C:\AI\cc\CLAUDE.md` 全局规则，提供 mail 项目专用知识。

## Gmail IMAP 连接

- **邮箱**: `jaojingomatic27@googlemail.com`
- **密码**: 从 `C:\AI\cc\account.txt` 读取（应用专用密码，非邮箱登录密码）
- **IMAP**: `imap.gmail.com:993`, SSL
- **必需**: Gmail 须开启两步验证 + 生成「邮件」应用专用密码。普通密码已失效。

## Gmail IMAP 关键坑

### 1. 文件夹名 UTF-7 编码
Gmail 用 Modified UTF-7 编码非 ASCII 文件夹名。解码：`&` 开头 `-` 结尾的片断是 base64（`,` 替换为 `/`），解码后是 UTF-16-BE。

常用文件夹：
| 原始名 | 解码 |
|--------|------|
| `[Gmail]/&V4NXPpCuTvY-` | 垃圾邮件 (Spam) |
| `[Gmail]/&XfJSIJZkkK5O9g-` | 已删除邮件 (Trash) |
| `[Gmail]/&YkBnCZCuTvY-` | 所有邮件 (All Mail) |
| `[Gmail]/&XfJT0ZCuTvY-` | 已发邮件 (Sent) |
| `[Gmail]/&kc2JgQ-` | 重要 (Important) |

### 2. X-GM-RAW 搜索
- `mail.search(None, "X-GM-RAW", "category:promotions")` **有效**（普通 SEARCH）
- `mail.uid("SEARCH", None, "X-GM-RAW", "...")` **无效**（UID SEARCH 不支持 X-GM-RAW）
- 用法：先用普通 SEARCH 获取序列号，再用 FETCH 获取 UID

### 3. UID 操作
- **优先用 UID 而非序列号** — 序列号在 SELECT/EXPUNGE 后会变动
- 批量 UID FETCH 返回格式：`[(header_tuple, body), b')', (header_tuple, body), b')', ...]`
  - 偶数索引 `data[0], data[2]...` 是 tuple（`resp[0]`=header 文本含 UID, `resp[1]`=邮件体）
  - 奇数索引 `data[1], data[3]...` 是 `b')'` 分隔符，须跳过
- 批量大小：每次最多 200-300 个，避免超时

### 4. 删除与垃圾邮件
- `STORE +FLAGS \Deleted` + `expunge` 在 INBOX 上可正常删除
- 在 All Mail 上同样操作**可能无效**（无标签孤立状态）
- 孤立邮件用 **`MOVE` 命令**移入 Spam 解决：`mail.uid("MOVE", uids_str, SPAM_FOLDER)`
- 移入 Spam 是一次性操作，不会创建过滤器影响新邮件

### 5. Trash 永久删除行为
Gmail IMAP 的 `\Deleted` + `expunge` 可能自动永久删除而不经过 Trash（取决于账户的 IMAP 设置「标记为已删除时」是否设为「立即永久删除」）。

## 已有脚本模式

所有脚本位于 `code/`，遵循以下模式：

### 扫描类（只读）
- `scan_ads.py` — 扫描最近 600 封，关键词匹配分类
- `scan_all.py` — 扫描所有文件夹全量，UTF-7 解码文件夹名，去重

### 删除类（扫描+删除）
- `delete_ads.py` — 删除最近 600 封中的广告
- `delete_all_ads.py` — 跨文件夹全量删除广告
- `delete_temu.py` — 关键词（域名/发件人含 temu）匹配删除
- `delete_old_ebay.py` — 按发件人+日期筛选删除
- `promotions_scan.py` — X-GM-RAW 搜索 category:promotions 删除
- `category_cleanup.py` — 遍历所有 Gmail 动态分类，按日期筛选删除

### 工具类
- `diagnose_imap.py` — 测试不同邮箱/密码组合连接
- `debug_fetch.py` — 打印 IMAP 响应格式
- `verify_temu.py` — 验证特定关键词残留
- `spam_temu.py` — MOVE 孤立邮件到 Spam

### 通用脚本结构
```python
# 连接
mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(EMAIL, PASSWORD)
mail.select("INBOX")

# 获取 UID 列表
status, data = mail.uid("SEARCH", None, "ALL")
all_uids = data[0].split()

# 批量取邮件头
for start in range(0, len(all_uids), 200):
    chunk = all_uids[start:start+200]
    uids_str = ",".join(uid.decode() for uid in chunk)
    status, data = mail.uid("FETCH", uids_str, "(RFC822.HEADER)")
    for i in range(0, len(data), 2):  # 跳过分隔符
        resp = data[i]
        if not isinstance(resp, tuple): continue
        resp_text = resp[0].decode(errors="replace")
        m = re.search(r'UID\s+(\d+)', resp_text)
        uid = m.group(1)
        msg = email.message_from_bytes(resp[1])

# 删除（批量 STORE + expunge）
for start in range(0, len(to_delete), 100):
    batch = to_delete[start:start+100]
    uids_str = ",".join(uid for uid in batch)
    mail.uid("STORE", uids_str, "+FLAGS", "\\Deleted")
mail.expunge()

# 无法删除时 MOVE 到 Spam
SPAM = "[Gmail]/&V4NXPpCuTvY-"
mail.uid("MOVE", uids_str, SPAM)
```
