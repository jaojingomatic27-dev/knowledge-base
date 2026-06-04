# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

本文件补充 `C:\AI\cc\CLAUDE.md` 全局规则。

## 项目用途

美股盘前新闻扫描系统 — 每天开盘前 1 小时自动搜索 8 只持仓标的的新闻，情感分析（利多/利空），生成中英双语简报邮件。

## 架构

```
fetch_yfinance_news()  ─┐
                        ├→ fetch_all_news() → 去重 → analyze_sentiment()
fetch_google_news_rss()─┘                              ↓
                                                       │
email ← send_email() ← generate_html_report() ← generate_briefing() ← batch_translate()
                                         ↑
                          extract_themes()   highlight_companies()
```

- **数据获取**: 双源并行 (yfinance `.news` + Google News RSS)，URL 去重，24 小时时间窗口
- **情感分析**: 50+ 正则模式匹配，amplifier ×1.3 / diminisher ×0.7 修饰词加权，输出 score + label
- **翻译**: `deep-translator` (Google Translate 免费后端)，磁盘缓存 `data/translation_cache.json`，每 5 条限速 0.5s
- **简报生成**: `generate_briefing()` 按投资组合分组 → `extract_themes()` 提取主题标签 → 每组合 3 条关键标题
- **公司高亮**: `highlight_companies()` 中英文双模式，`COMPANY_HIGHLIGHT_MAP` + `CN_COMPANY_NAMES`，8 色配色方案
- **输出**: HTML 暗色主题邮件，Gmail SMTP (587 STARTTLS)

## 依赖

| 库 | 用途 |
|----|------|
| `yfinance` | 个股新闻 (每标的 10 条) |
| `feedparser` | Google News RSS 搜索 |
| `deep-translator` | 标题英→中翻译 |

安装: `pip install yfinance feedparser deep-translator`

## 命令

```powershell
python code/daily_news_scanner.py              # 正式：搜索 + 翻译 + 发邮件
python code/daily_news_scanner.py --dry-run    # 仅生成 HTML，不发邮件
```

## 定时任务

Windows Task Scheduler: `NewsPreMarketScanner`，每日 20:30 (周一至周五)，对应美东 08:30 EDT。

注册（需管理员）:
```powershell
C:\AI\cc\news\code\setup_scheduled_task.ps1
# 或自定义时间:
C:\AI\cc\news\code\setup_scheduled_task.ps1 -Time "21:30"
```

## 覆盖标的

| 组合 | Tickers | 策略 |
|------|---------|------|
| 🔺 铁三角 | NVDA, MSFT, ORCL | Turbo 权证多单 |
| 🚀 窜天猴 | PLTR, SMCI, TSLA | Turbo 权证多单 |
| ⚖️ DCA 均衡型 | SPY, NVDA, AVGO | DCA 定投 |

## 关键配置

- **邮箱**: `jaojingomatic27@googlemail.com`，密码从 `account.txt` 读取 (Gmail 应用专用密码)
- **情感词典**: `BULLISH_PATTERNS` / `BEARISH_PATTERNS` — 业绩/评级/产品/监管/宏观 5 大类
- **公司高亮色**: NVIDIA 绿 #76b900 / 博通红 #cc0000 / 特斯拉红 #e82127 / 微软蓝 #00a4ef / Oracle 红 #f80000 / Palantir 银 #c0c0c0 / 超微蓝 #1e90ff / SPY 橙 #ff9800
- **翻译缓存**: `data/translation_cache.json` — 磁盘持久化，避免重复翻译

## 注意事项

- Google Translate 免费 API 有频率限制，`batch_translate()` 已内置 5 条/0.5s 限速
- 首次运行 ~250 条翻译需约 25 秒，后续仅翻译新增标题（秒级）
- `account.txt` 已在 `.gitignore` 中排除，不提交
- 根目录 `.gitignore` 排除了 `account.txt`、`stock/`、`__pycache__/`
- 新闻数据 `data/news_YYYYMMDD.json` 不提交 (`.gitignore`)
