# CLAUDE.md — 全局规则

本文件覆盖所有子项目。子项目 `CLAUDE.md` 可补充，不得冲突。

## 核心规则

1. **语言**：尽量用中文回复。代码、路径、命令除外。
2. **Subagent 优先**：搜索、浏览多文件、独立研究类任务用 subagent，可并行。
3. **文件夹约定**：每个项目下 `code/`、`data/`、`image/` 自动创建，不询问许可。
4. **文件索引**：项目根目录维护 `PROJECT_INDEX.md`，每次新增/删除文件后更新。优先复用已有数据（`data/`）和代码（`code/`）。
5. **路径**：Windows 原始字符串 `r"C:\AI\cc\..."`，根目录 `C:\AI\cc`。
6. **项目日志**：每个项目维护 `PROJECT_LOG.md`，格式统一（以 `stock/PROJECT_LOG.md` 为模板）。上下文超 80% 或重要操作完成后更新。生成/改写文件不需要批准。
7. **自动提交**：更新 `PROJECT_LOG.md` 后自动 push。版本号 `YYYYMMDD-HH`，写入 commit message。

## 环境

- Windows 10 Pro / PowerShell 5.1
- Git: `C:\Program\bin\git.exe` / GitHub CLI: `$env:LOCALAPPDATA\Programs\GitHub CLI\bin\gh.exe`
- Python 3 全局安装 / GitHub: jaojingomatic27-dev

## 已有子项目

| 项目 | 说明 |
|------|------|
| `stock/` | 量化回测系统，GitHub: https://github.com/jaojingomatic27-dev/stock |
| `news/` | 每日盘前新闻扫描 + 情感分析 + 邮件简报，GitHub: https://github.com/jaojingomatic27-dev/news |
| `mail/` | Gmail 清理/管理脚本 |

## PowerShell 速记

- 无 `&&`/`||` → `; if ($?) { }`
- 无 `2>&1`、`head`/`tail`、`which`、`touch`
- PATH: `$env:Path = "C:\Program\bin;$env:LOCALAPPDATA\Programs\GitHub CLI\bin;$env:Path"`
