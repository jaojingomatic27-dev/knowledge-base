# -*- coding: utf-8 -*-
"""Append new entry to terminal/output.md"""
import os
from datetime import datetime

path = r"C:\AI\cc\pvinverter\terminal\output.md"
now = datetime.now().strftime("%Y-%m-%d %H:%M")

entry = u"""

---

## """ + now + u""" — Intersolar Europe 2026 名片整理分析

### 数据来源

`input/Intersolar Europe 2026/名片.txt` — OCR 识别名片共 17 条记录，解析出 15 家独立公司。

### 公司分类

| 类型 | 数量 | 代表公司 |
|------|------|---------|
| 光伏组件/电池 | 5 | JMTHY, PERLIGHT, ERA, 正信光电, Haitai Solar |
| 光伏逆变器 | 2 | FORTUNES SOLAR, VDS |
| 光伏支架 | 1 | MG SOLAR (厦门，西班牙有号码) |
| 光伏材料 | 1 | Qujing Huanju |
| 便携式太阳能 | 1 | Sola-E |
| 非光伏 | 1 | SHIMGE (水泵) |
| 不详 | 4 | GOLAND CENTURY, ELECWAY, APsolway, 英发 |

### 关键发现

- **Electronic Way GmbH (ELECWAY)** — 唯一在德国杜塞尔多夫有实体办公室的公司，两位联系人 (Alex Cernov + Steven VP)，可能是本地渠道伙伴
- **FORTUNES SOLAR** — 逆变器同行，Trade Manager Bruce 可跟进了解产品定位
- **MG SOLAR** — 光伏支架厂，Managing Partner Megan 有西班牙号码 (+34)，支架+逆变器常一起采购，可探讨渠道合作
- **无大型 EPC/Utility/IPP 名片** — 这批名片以中国参展供应商为主，缺乏本地项目方
- **后续建议**: 参加 E-World (Essen) / Energy Storage Europe (Dusseldorf) 接触本地项目方
"""

with open(path, "a", encoding="utf-8") as f:
    f.write(entry)

print("Appended to " + path)
print("Entry: " + now)
