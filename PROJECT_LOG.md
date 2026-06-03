# 项目日志 — knowledge-base（全局）

## [2026-06-04 01:00] 清理 Gmail 邮箱广告邮件

- **输入命令**: "清理我的电子邮箱...找出所有广告邮件，分类，告诉我 我同意后批量删除"
- **PROJECT_INDEX 变更**: 新增 mail 项目索引（4 个脚本 + 项目日志）
- **关键发现**:
  1. Gmail IMAP 需要应用专用密码（App Password），普通密码已不可用
  2. 邮箱 `jaojingomatic27@googlemail.com` 共 7,248 封，扫描最近 600 封发现 53 封广告
  3. 主要垃圾源：REWE（15封）、Stepstone（8封）、PAYBACK（8封）、eBay（6封）
  4. Gmail 未启用 Promotions 分类，所有广告混在收件箱
- **生成/修改的文件**:
  | 文件 | 说明 |
  |------|------|
  | `mail/code/scan_ads.py` | 广告扫描脚本（只读分类） |
  | `mail/code/delete_ads.py` | 广告删除脚本 |
  | `mail/code/diagnose_imap.py` | IMAP 连接诊断 |
  | `mail/code/debug_fetch.py` | IMAP 响应格式调试 |
  | `mail/PROJECT_LOG.md` | mail 项目日志 |
  | `PROJECT_INDEX.md` | 新增 mail 项目索引 |
  | `PROJECT_LOG.md` | 本文件 |

## [2026-06-04 00:00] 细化日志格式，更新 stock 项目日志

- **输入命令**: "再微调规则，比如项目C:\AI\cc\stock的如下内容也要加到项目日志里"
- **PROJECT_INDEX 变更**: 新增 `chart_6pairs_annual.py`、`threshold_scan_4pairs.py`、`chart_6pairs_annual.png`、`threshold_scan_4pairs.png`
- **关键发现**:
  1. 日志格式细化：关键发现须列编号条目，生成文件用表格（路径 + 说明）
  2. 以 `stock/PROJECT_LOG.md` 为所有项目日志的格式模板
- **生成/修改的文件**:
  | 文件 | 说明 |
  |------|------|
  | `CLAUDE.md` | 细化规则 6 日志格式 |
  | `stock/PROJECT_LOG.md` | 新增轮动+杠杆回测日志条目 |
  | `PROJECT_INDEX.md` | 新增 4 个文件索引 |
  | `PROJECT_LOG.md` | 本文件，新增条目 |

## [2026-06-03 22:56] 添加项目日志和自动提交规则

- **输入命令**: "把下面规则加到全局claude.md"
- **PROJECT_INDEX 变更**: 无
- **关键发现**:
  1. 新增规则 6（项目日志）和规则 7（自动提交与版本号），建立完整的项目追踪体系
- **生成/修改的文件**:
  | 文件 | 说明 |
  |------|------|
  | `CLAUDE.md` | 新增第 6、7 条规则 |
  | `PROJECT_LOG.md` | 本文件，新建 |
