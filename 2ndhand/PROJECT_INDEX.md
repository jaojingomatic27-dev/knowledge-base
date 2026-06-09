# 2ndhand — 项目索引

二手物品拍照 → AI 识别 → 生成描述与上架文案，一键发 eBay Kleinanzeigen。

## 文件夹结构

| 文件夹 | 用途 |
|--------|------|
| `input/` | 待分析的二手物品照片 |
| `output/` | 分析报告、上架文案 |
| `code/` | 自动化脚本 |
| `data/` | 模板、定价参考数据 |

## 文件清单

### input/
- `微信图片_20260609204202_66_2.jpg`
- `微信图片_20260609204202_67_2.jpg`
- `微信图片_20260609204351_68_2.jpg`
- `微信图片_20260609204352_69_2.jpg`

### output/
- `items_report.md` — 物品识别 + 定价报告（中文）
- `ebay_listing_lg_fp9_de.md` — LG FP9 耳机的德语上架文案
- `ebay_listing_roomba966_de.md` — Roomba 966 的德语上架文案

### data/
- `ebay_disclaimer_de.md` — eBay 私人卖家标准免责声明模板
