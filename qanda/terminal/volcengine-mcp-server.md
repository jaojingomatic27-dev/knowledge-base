# 火山引擎 MCP Server 生态

> 来源：https://github.com/volcengine/mcp-server
> 日期：2026-06-07

## 概述

火山引擎大模型生态广场的 MCP Server 集合仓库，已上线 **100+ MCP Server**，MIT 开源协议。
用户通过 MCP 协议将字节跳动生态的云服务和第三方工具接入 AI 客户端（Cursor、Trae、Claude Code 等），用自然语言操控云资源。

## 核心优势

- **资源丰富** — 火山引擎官方云服务 + 第三方生态工具
- **灵活部署** — 支持本地（Local）和远程（Remote）MCP 部署模式
- **端到端生态** — 可与火山方舟（Ark）LLM 平台或 Trae、Cursor 等 MCP 兼容工具配合

## 支持类别（18+）

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

## 使用方式

1. 在 [火山 MCP 市场](https://www.volcengine.com/mcp-marketplace) 浏览 MCP Server
2. 选择目标运行平台
3. 查看 Tools 描述和参数，可测试运行
4. 登录并激活服务后，生成唯一 URL 或代码片段
5. 将 URL/JSON 粘贴到 MCP Client 配置文件中安装

## 支持的 MCP 客户端

- 火山方舟 Ark（体验中心 + 高代码应用）
- Trae
- Cursor
- Python（编程式调用）

## 与阿里百炼 Skills 对比

| 维度 | 火山 MCP | 阿里百炼 Skills |
|------|---------|----------------|
| 协议 | MCP | Claude Code Skill 体系 |
| 生态 | 字节跳动云服务 + 第三方 | 阿里云百炼模型 + 第三方 |
| 集成方式 | MCP Server URL/JSON 配置 | npm/npx 安装 + 本地代理 |
| 数量 | 100+ | 6 个核心 skill |

两者策略相似：把云服务能力打包为标准化的 AI 工具接口，让 LLM 能直接调用。
