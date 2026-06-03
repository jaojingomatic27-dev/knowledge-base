# PROJECT_LOG — mail

## [2026-06-04 01:30] 深度全量扫描，删除 857 封广告邮件

- **输入命令**: "扫描更早的邮件，还有 6600+ 封没查尤其是推广文件夹里" → "删除全部 737 封"
- **PROJECT_INDEX 变更**: 新增 scan_all.py、delete_all_ads.py
- **关键发现**:
  1. 全量扫描 INBOX 7,195 封 + 已发邮件 1,657 封 + 其他文件夹，共 9,500+ 封
  2. 发现 857 封广告邮件（含跨文件夹重复），去重后 737 封，来自 43 个域名
  3. Groupon 是最大垃圾来源：497 封（占 58%），有 30+ 种不同邮件类型
  4. 其他大户：ASICS 66封、adidas 56封、Mister Spex 43封、REWE 29封
  5. Gmail 文件夹 UTF-7 编码解码：存档=[&W1hoYw-]，垃圾邮件=[Gmail]/&V4NXPpCuTvY-
  6. 用户无 Gmail 分类标签（Promotions/Social），所有广告混在收件箱
- **生成/修改的文件**:
  | 文件 | 说明 |
  |------|------|
  | `code/scan_all.py` | 全量扫描脚本（所有文件夹，UTF-7 解码） |
  | `code/delete_all_ads.py` | 批量删除脚本（跨文件夹 UID 删除） |
  | `PROJECT_LOG.md` | 本文件 |

## [2026-06-04 01:00] 清理 Gmail 邮箱广告邮件

- **输入命令**: 清理 Gmail 邮箱，扫描并删除广告邮件
- **PROJECT_INDEX 变更**: 新增 mail 项目文件索引
- **关键发现**:
  1. Gmail IMAP 需要应用专用密码（App Password），普通密码无法登录
  2. 邮箱 `jaojingomatic27@googlemail.com` 共 7,248 封邮件，扫描最近 600 封
  3. 发现 53 封广告邮件，来自 10 个域名，已全部删除
  4. 主要垃圾来源：REWE（15封）、Stepstone（8封）、PAYBACK（8封）、eBay（6封）
  5. Gmail 未启用 Promotions 分类标签，所有广告混在收件箱中
- **生成/修改的文件**:
  | 文件 | 说明 |
  |------|------|
  | `code/scan_ads.py` | 广告邮件扫描脚本（只读，分类展示） |
  | `code/delete_ads.py` | 广告邮件删除脚本（扫描+删除） |
  | `code/diagnose_imap.py` | IMAP 连接诊断脚本 |
  | `code/debug_fetch.py` | IMAP 响应格式调试脚本 |
