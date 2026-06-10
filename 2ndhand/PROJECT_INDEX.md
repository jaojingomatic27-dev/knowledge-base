# 2ndhand — 项目索引

二手物品拍照 → AI 识别 → 生成描述与上架文案 → YAML → kleinanzeigen-bot 一键上架

## 工作流

```
input/ 照片 → code/auto_pipeline.py → bl omni 视觉识别
                                      → bl text chat 德语文案
                                      → YAML 配置
                                      → output/ 全部输出
```

## 文件夹结构

| 文件夹 | 用途 |
|--------|------|
| `input/` | 待分析的二手物品照片 |
| `output/` | 分析报告、上架文案、YAML 配置文件 |
| `code/` | 自动化脚本（auto_pipeline.py） |
| `data/` | 模板、定价参考数据 |
| `terminal/` | 长输出归档（`output.md`） |

## 文件清单

- `CLAUDE.md` — 项目级 Claude Code 指引

### code/
- `auto_pipeline.py` — **主脚本**：扫描 input/ → bl 识别 → 生成报告 + 德语文案 + YAML

### input/
- `微信图片_20260609204202_66_2.jpg`
- `微信图片_20260609204202_67_2.jpg`
- `微信图片_20260609204351_68_2.jpg`
- `微信图片_20260609204352_69_2.jpg`

### output/
- `items_report.md` — 物品识别 + 定价报告（中文）
- `ebay_listing_lg_fp9_de.md` — LG HBS-FN7 耳机德语上架文案（已更正型号）
- `ebay_listing_roomba966_de.md` — Roomba 966 德语上架文案

### data/
- `ebay_disclaimer_de.md` — eBay 私人卖家标准免责声明模板
