# 2ndhand — 项目日志

## 2026-06-09

### 项目初始化 + 首批物品分析

**操作**：
- 创建项目文件夹 `input/`, `output/`, `code/`, `data/`
- 用 `qwen3.5-omni-plus` 视觉模型分析 4 张输入照片
- 识别出 2 样物品：LG TONE Free FP9 耳机、iRobot Roomba 966 扫地机器人
- 用 `qwen3.7-max` 生成德语 eBay Kleinanzeigen 上架文案（含 Privatverkauf 声明）

**生成文件**：
- `output/items_report.md` — 完整鉴定报告（含成色、规格、定价）
- `output/ebay_listing_lg_fp9_de.md` — LG 耳机德语上架文案（€75 VB）
- `output/ebay_listing_roomba966_de.md` — Roomba 德语上架文案（€80 VB）
- `data/ebay_disclaimer_de.md` — 声明模板，后续所有上架自动附加

**定价建议**：
| 物品 | 成色 | 建议售价 |
|------|------|----------|
| LG TONE Free FP9 | 8.5-9成新 | €65-85（上架 €75 VB） |
| iRobot Roomba 966 | 6.5-7成新 | €70-90（上架 €80 VB） |

**规则建立**：所有 eBay 上架文案末尾必须附加 Privatverkauf 免责声明。

---

### 自动上架流水线脚本

**操作**：
- 调研 Kleinanzeigen.de 自动化方案：官方无公开 API
- 选型 kleinanzeigen-bot (开源 Python CLI, GitHub: Second-Hand-Friends/kleinanzeigen-bot)
- 编写 `code/auto_pipeline.py` — 完整自动化流水线

**脚本架构**：
```
input/ 照片 → bl omni (qwen3.5-omni-plus) 视觉识别
            → 解析 JSON 物品清单
            → bl text chat (qwen3.7-max) 德语上架文案（自动附加声明）
            → 生成 kleinanzeigen-bot YAML 配置
            → output/ (报告 + 文案 + YAML)
```

**关键实现**：
- YAML 格式严格遵循 kleinanzeigen-bot 配置规范
  - 分类自动映射 (Kopfhörer → "Elektronik & Nähmaschinen > Kopfhörer & Headsets")
  - 成色 → special_attributes.condition_s (like_new/ok/alright/defect)
  - 物流选项 (DHL/Hermes), VB 定价, 图片 glob
- 声明模板 (`data/ebay_disclaimer_de.md`) 自动附加到每条文案末尾
- 图片自动复制到 output/images/ 供 kleinanzeigen-bot 引用

**使用方式**：
```bash
# 1. 把照片放入 input/
# 2. 运行流水线
python code/auto_pipeline.py
# 3. 用 kleinanzeigen-bot 上架
kleinanzeigen-bot publish --ads=output/ad_*.yaml
```

**模型更正**：
- LG 耳机型号从 FP9 更正为 **HBS-FN7**
- 补充准确规格：续航 5h/7h (ANC开/关)，Qi 无线充电，IPX4，蓝牙 5.0，3 麦克风
- 价格调整为 €65 VB (FN7 比 FP9 老一代)
