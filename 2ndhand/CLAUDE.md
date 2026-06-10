# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> 本文件补充全局 `C:\AI\cc\CLAUDE.md`，不得与其冲突。

## 项目概述

二手物品拍照 → AI 识别 → 德语 Kleinanzeigen 上架文案 + YAML → kleinanzeigen-bot 一键发布。

## 核心流水线

```
input/ 照片 → python code/auto_pipeline.py
                ├─ bl omni (qwen3.5-omni-plus)  视觉识别 → JSON 物品清单
                ├─ bl text chat (qwen3.7-max)    德语 Kleinanzeigen 文案
                ├─ 生成 ad_*.yaml                kleinanzeigen-bot 配置
                └─ output/                       报告 + 文案 + YAML + images/
```

### 运行

```powershell
python code/auto_pipeline.py
```

前置条件：`bl` CLI 已登录 (`bl auth login --api-key sk-...`)。

### 输出

| 产物 | 路径 | 用途 |
|------|------|------|
| 鉴定报告 | `output/items_report.md` | 中文，含成色/规格/定价 |
| 德语文案 | `output/listing_<slug>_de.md` | 可直接复制粘贴到 Kleinanzeigen |
| Bot 配置 | `output/ad_<slug>.yaml` | kleinanzeigen-bot 直接 `publish` |
| 图片副本 | `output/images/` | 供 bot 引用 |

## 硬性规则

### eBay 声明

**每条德语上架文案末尾必须一字不改附加：**

```
Es handelt sich um einen Privatverkauf. Ich übernehme keine Garantie und Rücknahme!!! Viel Spass beim Bieten!!!
```

模板保存在 `data/ebay_disclaimer_de.md`，供参考。

### Kleinanzeigen 分类映射

`auto_pipeline.py` 内置了关键词→分类层级映射（`CATEGORY_GUESS`）。添加新品类时扩展该 dict。

### kleinanzeigen-bot YAML 关键字段

YAML 由 `auto_pipeline.py` 生成，无外部 yaml 库依赖。字段遵循 [kleinanzeigen-bot](https://github.com/Second-Hand-Friends/kleinanzeigen-bot) 规范：

- `title` — 最长 80 字符
- `description` — 多行用 `|` 块标量
- `price` / `price_type` — NEGOTIABLE / FIXED / GIVE_AWAY
- `shipping_type` — SHIPPING / PICKUP / NOT_APPLICABLE
- `special_attributes.condition_s` — like_new / ok / alright / defect（成色 9+ → like_new, 7+ → ok, 5+ → alright）
- `images` — 相对路径 glob，图片须在 `output/images/` 下

### 模型选择

- **视觉识别**：`qwen3.5-omni-plus`（`bl omni --text-only`）
- **德语文案生成**：`qwen3.7-max`（`bl text chat`）

### Kleinanzeigen.de 自动化现状

- 官方**没有**公开 API
- 推荐方案：[kleinanzeigen-bot](https://github.com/Second-Hand-Friends/kleinanzeigen-bot)（Python CLI，浏览器自动化）
- 逆向内部 API（`api.kleinanzeigen.de`）存在但违反 AGB，不推荐
