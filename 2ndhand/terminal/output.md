# terminal/output.md — 2ndhand 长输出归档

## 2026-06-09 20:42 — 首次照片分析结果

### 识别物品清单（共2样）

| # | 物品 | 成色 | 建议售价 |
|---|------|------|----------|
| 🎧 | LG TONE Free HBS-FN7 真无线降噪耳机 | 8.5-9成新 | €55-70 |
| 🤖 | iRobot Roomba 966 扫地机器人 | 6.5-7成新 | €70-90 |

### 物品1：LG TONE Free HBS-FN7

- UVnano UV-C 杀菌（99.9%细菌去除）
- Meridian HSP 空间音效 + 4 EQ 模式
- ANC 主动降噪 + Ambient 通透
- 续航：5h(ANC开)/7h(关) + 充电盒 15h/21h
- Qi 无线充电 + USB-C + 快充（5分钟→1小时）
- IPX4 防溅 + BT 5.0 + Google Fast Pair
- 3 麦克风/耳 + 触控 + 佩戴检测
- 🆕 全新硅胶耳塞已更换

### 物品2：iRobot Roomba 966

- vSLAM 视觉导航（摄像头建图，非随机碰撞）
- AeroForce 清洁系统
- Wi-Fi + App 控制
- ⚠️ 主刷磨损严重，需更换（约€15-20）
- ⚠️ 顶盖塑料泛黄

---

## 2026-06-09 21:00 — 型号更正 & 德语文案生成

### LG 型号更正
- 原识别：FP9 / HBS-FP9
- 实际型号：**HBS-FN7**
- 价格调整：€75 → **€65 VB**（FN7 比 FP9 老一代）

### 生成文件
- `output/ebay_listing_lg_fp9_de.md` — LG HBS-FN7 德语文案（€65 VB）
- `output/ebay_listing_roomba966_de.md` — Roomba 966 德语文案（€80 VB）
- 均包含 Privatverkauf 声明

### 德语声明模板
> Es handelt sich um einen Privatverkauf. Ich übernehme keine Garantie und Rücknahme!!! Viel Spass beim Bieten!!!

---

## 2026-06-09 21:30 — 自动上架流水线脚本

### 工作流
```
input/ 照片 → bl omni (qwen3.5-omni-plus) 视觉识别
            → 解析 JSON 物品清单
            → bl text chat (qwen3.7-max) 德语上架文案（自动附加声明）
            → 生成 kleinanzeigen-bot YAML 配置
            → output/ (报告 + 文案 + YAML + images/)
```

### 使用方式
```bash
# 1. 把照片放入 input/
# 2. 运行流水线
python code/auto_pipeline.py
# 3. 用 kleinanzeigen-bot 上架
kleinanzeigen-bot publish --ads=output/ad_*.yaml
```

### Kleinanzeigen.de 上架方案调研
- ❌ 官方无公开 API
- ✅ kleinanzeigen-bot（开源 Python CLI，浏览器自动化）— 推荐
- ⚠️ 逆向内部 API — 违反 AGB，不推荐

### YAML 关键字段
- title ≤80 字符, price/price_type (NEGOTIABLE/FIXED)
- shipping_type (SHIPPING/PICKUP), shipping_costs
- special_attributes.condition_s (like_new/ok/alright/defect)
- images — 相对路径 glob，图片在 output/images/
- 分类关键词自动映射 (Kopfhörer → Elektronik & Nähmaschinen > Kopfhörer & Headsets)

---

## 2026-06-10 — 项目 CLAUDE.md + 长输出补录
- 创建 `2ndhand/CLAUDE.md`（本地项目级，补充全局规则）
- 补录前几轮未落盘的长输出内容到本文件
- 全局 CLAUDE.md 第9条：回复中总结/列表/表格超过 20 行必须写入 `terminal/output.md`
