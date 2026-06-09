# qanda — terminal/output.md

记录超过 20 行的总结/列表/表格，自动追加。

---

## 百炼 CLI + qwen 模型接入 Claude Code 全流程 — 2026-06-07 13:15 (CEST)

### 一、目标

在 Claude Code 中通过 `bl` CLI 直接调用阿里云百炼平台上的 qwen 系列模型（文本、视觉、生图、生视频等），结果直接在对话中反馈。

### 二、整体思路

```
Claude Code → Bash 工具 → bl 命令 → 百炼 API → qwen 模型 → 结果返回对话
```

核心链路：安装 bailian-cli → 安装 skills（知识库） → 配置 API Key → 验证调用。

### 三、操作步骤

#### 3.1 前置环境检查

| 要求 | 实际 | 结论 |
|------|------|------|
| Node.js ≥ 22.12.0 | v24.16.0 | ✅ |
| npm 可用 | 11.13.0 | ✅ |

#### 3.2 安装 CLI

```bash
npm install -g bailian-cli
# 验证
bl --version  # → bl 1.2.0
```

#### 3.3 安装 Skills（遇到问题并解决）

```bash
npx skills add modelstudioai/skills --all -g
```

**❌ 问题：Windows 260 字符路径限制**

仓库文件路径极深（部分文件路径 > 260 字符），克隆到 `%TEMP%` 时 Git checkout 失败，报 `Filename too long`。

**✅ 解决：三步走**

1. `git config --global core.longpaths true`（解除 Git 层限制）
2. 手动克隆到极短路径 `C:\b\s`
3. 用本地路径安装：`npx skills add C:\b\s --all -g`

最终成功安装 6 个 skill（安装到了 71 个 agent）：
- `bailian-cli` — `bl` 命令用法手册
- `bailian-docs-llm-wiki` — 百炼平台文档知识库（models/wiki/raw 三层）
- `bailian-model-recommend` — 模型选型推荐
- `financial-expert` — 金融分析
- `happyhorse-prompt-studio` — 提示词工坊
- `spark-video-episode` — 视频制作

#### 3.4 鉴权配置（遇到问题并解决）

**第一把 Key（欧盟区工作空间专属）**

- 来源：`C:\AI\qwen\默认业务空间-apiKey-14095.csv`
- 格式：`sk-ws-djI...`（带 `-ws-` 前缀）
- ❌ 默认端点 `dashscope.aliyuncs.com` 返回 401
- ✅ 指定 `--base-url "https://ws-v4cbycsu1jig5w31.eu-central-1.maas.aliyuncs.com"` 后成功

**第二把 Key（标准 DashScope Key）**

- 格式：`sk-44b0...`（无 `-ws-` 前缀）
- ❌ 初次调用报 `Arrearage`（账户欠费）
- ✅ 用户充值后，直接 curl 测试 200 OK
- ❌ `bl auth login --api-key` 验证流程有 bug，始终报 invalid key，即使 key 实际有效
- ✅ 绕过：`bl config set --key api_key --value sk-...` 直写配置，恢复默认 base_url

**最终配置：**

```json
{
  "api_key": "sk-4...bebc",
  "base_url": "https://dashscope.aliyuncs.com",
  "region": "cn"
}
```

#### 3.5 功能验证

| 能力 | 命令 | 模型 | 结果 |
|------|------|------|------|
| 文本对话 | `bl text chat --message "ping"` | qwen3.7-max | ✅ Pong! |
| 视觉理解 | `bl vision describe --image xxx.jpg` | qwen3-vl-plus | ✅ 详细中英文描述 |
| 图片生成 | `bl image generate --prompt "一只太空猫"` | qwen-image-2.0 | ✅ 成功生成 |

### 四、关键经验

1. **Windows 路径限制是常见坑点**：安装 skills 时路径太深，需 `core.longpaths=true` + 短路径手动克隆
2. **`bl auth login` 验证不靠谱**：key 明明有效但验证失败，`bl config set` 直写配置可绕过
3. **工作空间 Key vs 标准 Key**：`sk-ws-` 前缀的是工作空间专属，需指定对应 region 的 base_url；不带前缀的是通用 DashScope Key
4. **`--base-url` 不要带路径**：`bl` 会自动拼接 `/compatible-mode/v1/chat/completions`，只需指定 host
5. **超时问题**：第一次调用可能超时，`--timeout 60` 加长即可，通常是网络波动

### 五、可用能力一览

| 命令 | 功能 | 默认模型 |
|------|------|---------|
| `bl text chat` | 文本/代码/翻译 | qwen3.7-max |
| `bl vision describe` | 图片/视频理解 | qwen3-vl-plus |
| `bl image generate` | 文生图 | qwen-image-2.0 |
| `bl image edit` | 图片编辑 | qwen-image-2.0 |
| `bl video generate` | 文/图生视频 | happyhorse-1.0-t2v |
| `bl video edit` | 视频风格转换 | happyhorse-1.0-video-edit |
| `bl omni` | 多模态输入+语音输出 | qwen3.5-omni-plus |
| `bl speech synthesize` | 语音合成 TTS | cosyvoice-v3-flash |
| `bl speech recognize` | 语音识别 ASR | fun-asr |
| `bl search web` | 网页搜索 | DashScope MCP |
| `bl app call` | 调用百炼应用 | 需 app-id |
| `bl memory *` | 记忆管理 | — |
| `bl knowledge retrieve` | 知识库 RAG | — |

---

## 火山引擎 MCP Server 生态 — 2026-06-07 13:13 (CEST)

来源：https://github.com/volcengine/mcp-server

### 概述

火山引擎大模型生态广场的 MCP Server 集合仓库，已上线 **100+ MCP Server**，MIT 开源协议。用户通过 MCP 协议将字节跳动生态的云服务和第三方工具接入 AI 客户端（Cursor、Trae、Claude Code 等），用自然语言操控云资源。

### 核心优势

| 优势 | 说明 |
|------|------|
| 资源丰富 | 火山引擎官方云服务 + 第三方生态工具 |
| 灵活部署 | 本地 Local + 远程 Remote 两种 MCP 部署模式 |
| 端到端生态 | 与火山方舟 Ark LLM 平台、Trae、Cursor 配合 |

### 支持类别（18+）

| 类别 | 示例 Server |
|------|------------|
| 计算 | ECS、云助手 |
| 存储 | TOS 对象存储、TLS 日志分析、EBS |
| 数据库 | RDS MySQL、veDB MySQL、Redis、MongoDB、CloudSearch |
| 容器/中间件 | VKE (K8s)、veFaaS 函数计算、Prometheus、APMPlus |
| CDN/边缘 | CDN、边缘计算、ALB |
| 大数据 | LAS、ByteHouse |
| 视频云 | 直播、点播、veImageX、Mobile Use（云手机自动化） |
| 安全 | AI 驱动 SOC 安全运营 |
| 管理/治理 | 计费、IAM、STS、ResourceShare、Project、CloudTrail |
| 开发工具 | Browser-Use、Code-Sandbox、Computer-Use、云浏览器 |
| 搜索 | Brave Search、Tavily、FireCrawl、Elasticsearch |
| 地图 | 高德地图、百度地图、Google Maps、FlightRadar24 |
| 内容生成 | 咔片 PPT、Figma、EverArt、SearchInfinity |
| 源码管理 | GitHub、GitLab、Git、Sentry |
| 数据查询 | PostgreSQL、SQLite、MySQL、MongoDB、Redis、Neo4j、Chroma |
| 文件管理 | Excel、XMind、Filesystem、Google Drive、Pandoc |
| 协作 | Notion、Slack、Google Calendar、Google Tasks |
| 金融 | CoinMarketCap |
| 其他 | Time、Spotify、Home Assistant、Playwright |

### 使用方式

1. 在[火山 MCP 市场](https://www.volcengine.com/mcp-marketplace)浏览 MCP Server
2. 选择目标运行平台
3. 查看 Tools 描述和参数，可测试运行
4. 登录并激活服务后，生成唯一 URL 或代码片段
5. 将 URL/JSON 粘贴到 MCP Client 配置文件中安装

### 支持的 MCP 客户端

- 火山方舟 Ark（体验中心 + 高代码应用）
- Trae
- Cursor
- Python（编程式调用）

### 与阿里百炼 Skills 对比

| 维度 | 火山 MCP | 阿里百炼 Skills |
|------|---------|----------------|
| 协议 | MCP | Claude Code Skill 体系 |
| 生态 | 字节跳动云服务 + 第三方 | 阿里云百炼模型 + 第三方 |
| 集成方式 | MCP Server URL/JSON 配置 | npm/npx 安装 + 本地代理 |
| 数量 | 100+ | 6 个核心 skill |

两者策略相似：把云服务能力打包为标准化的 AI 工具接口，让 LLM 能直接调用。
