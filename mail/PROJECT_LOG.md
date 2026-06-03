# PROJECT_LOG — mail

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
