# CLAUDE.md — 全局规则

本文件覆盖所有子项目的默认行为。子项目 `CLAUDE.md` 可以补充，但不得与本文件冲突。

## 核心规则

### 1. 语言
- **尽量用中文回复**。代码、技术术语、路径、命令除外。

### 2. Subagent 优先
- **能用 subagent 的任务尽量用 subagent**，尤其是搜索、浏览多文件、独立研究类任务。
- 独立子任务并行启动多个 subagent。

### 3. 项目文件夹结构

每个项目（如 `stock/`、`mail/`、`roof/`）都遵循以下子文件夹约定：

| 子文件夹 | 用途 | 规则 |
|----------|------|------|
| `code/` | 所有 Python/脚本代码 | **自动创建**，不询问许可 |
| `data/` | 下载的数据文件（CSV 等） | **自动创建**，不询问许可 |
| `image/` | 生成的图片/图表（PNG 等） | **自动创建**，不询问许可 |

创建子文件夹的命令：`New-Item -ItemType Directory -Path <project>/code -Force`（同理 `data`、`image`）。

### 4. 文件索引
- 项目根目录下维护 `PROJECT_INDEX.md`，列出所有子项目和关键文件的索引。
- 每次新增/删除文件后应更新索引。
- **优先使用已有数据**：根据索引到 `data/` 中找已下载的 CSV。
- **优先复用已有代码**：根据索引到 `code/` 中找已编写的脚本。

### 5. 路径约定
- Windows 路径使用原始字符串：`r"C:\AI\cc\..."`
- 项目根目录：`C:\AI\cc`

## 已有子项目

### stock/ — 量化回测系统
- GitHub: https://github.com/jaojingomatic27-dev/stock
- 详细文档见 `stock/CLAUDE.md`
- 已下载数据：SPY, NVDA, GOOGL, GOOG, AMZN, ORCL, GLD, SHY, SMCI, MU, GSPC
- 已实现策略：MA 交叉、动量、增强 DCA（6 种规则）、杠杆 ETF、板块轮动、权证回测

## 环境

- **OS**: Windows 10 Pro
- **Shell**: PowerShell 5.1
- **Git**: `C:\Program\bin\git.exe` (v2.49)
- **GitHub CLI**: `$env:LOCALAPPDATA\Programs\GitHub CLI\bin\gh.exe` (v2.72)
- **Python**: Python 3（全局安装，非 venv）
- **GitHub 账号**: jaojingomatic27-dev

## 常用 PowerShell 提醒

- 不支持 `&&`/`||`，用 `; if ($?) { }` 替代
- 不支持 `2>&1`、`head`/`tail`、`which`、`touch`
- PATH 需手动刷新：`$env:Path = "C:\Program\bin;$env:LOCALAPPDATA\Programs\GitHub CLI\bin;$env:Path"`
