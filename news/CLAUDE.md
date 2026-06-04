# CLAUDE.md — news 项目

本文件补充 `C:\AI\cc\CLAUDE.md` 全局规则，提供 news 项目专用知识。

## 项目用途

美股盘前新闻扫描系统：开盘前 1 小时自动搜索全网 24 小时内关于持仓公司的新闻，情感分析（利多/利空），邮件发送汇总报告。

## 覆盖标的

| 组合 | Tickers | 类型 |
|------|---------|------|
| 铁三角 | NVDA, MSFT, ORCL | Turbo 权证多单 |
| 窜天猴 | PLTR, SMCI, TSLA | Turbo 权证多单 |
| DCA 均衡型 | SPY, NVDA, AVGO | DCA 定投 |

## 核心脚本

`code/daily_news_scanner.py`

- **数据源**: yfinance `.news` + Google News RSS (`feedparser`)
- **情感分析**: 自定义金融关键词词典（50+ 利多/利空正则模式）
- **输出**: HTML 邮件 → Gmail SMTP
- **数据持久化**: `data/news_YYYYMMDD.json`

用法：
```
python code/daily_news_scanner.py              # 正式模式（发送邮件）
python code/daily_news_scanner.py --dry-run    # 仅生成报告，不发邮件
python code/daily_news_scanner.py --output     # 发送邮件 + 保存 HTML
```

## 邮件

- **邮箱**: `jaojingomatic27@googlemail.com`
- **密码**: 从 `account.txt` 读取（应用专用密码）
- **SMTP**: `smtp.gmail.com:587`, STARTTLS

## 定时任务

Windows Task Scheduler: `NewsPreMarketScanner`
- 执行: `python C:\AI\cc\news\code\daily_news_scanner.py`
- 触发: 每日 20:30 (北京时间，对应美东 08:30 EDT)
- 设置脚本: `code/setup_scheduled_task.ps1`

## 数据文件

- `financial_products.txt` — 来自 stock 项目的完整金融产品名录
- `account.txt` — 第 1 行邮箱，第 2 行应用专用密码
