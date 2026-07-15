# -*- coding: utf-8 -*-
"""Append Intersolar V2 entry to terminal/output.md"""
import os
from datetime import datetime

path = r"C:\AI\cc\pvinverter\terminal\output.md"
now = datetime.now().strftime("%Y-%m-%d %H:%M")

entry = u"""

---

## """ + now + u""" — Intersolar 2026 名片分析 V2

### 回答：光伏板保护电路公司

**找到了：宁波晶华新能源 (NINGBO JINGHUA NEW ENERGY)**
- 网址: jhbox.com
- 产品: 光伏接线盒 (PV Junction Box) — 即光伏板保护电路（旁路二极管、电气连接、防雷防水 IP67/IP68）
- 联系人: 肖炯 (International Sales Director), 邮箱 jhpvbox@aliyun.com, 手机 +86 13567825517

### 新发现的其他公司

| 公司 | 之前标记 | 查明后 |
|------|---------|--------|
| GOLAND CENTURY (光澜世纪) | 不详 | MPPT控制器+纯正弦波逆变器+太阳能水泵(离网户用) |
| ELECWAY (Electronic Way GmbH) | 不详 | 电动汽车直流充电桩(EV DC Charger)，杜塞尔多夫实体 |

### 更新后逆变器相关联系

| 公司 | 类型 | 优先级 |
|------|------|--------|
| FORTUNES SOLAR | 逆变器同行 | 中 |
| GOLAND CENTURY | 离网户用逆变器 | 低 |
| VDS Renewable (VIYOS) | 光伏/储能逆变器 | 中 |
| ELECWAY | 杜塞本地充电桩公司 | 高(本地人脉渠道) |
| MG SOLAR | 光伏支架(西班牙号) | 中(配套采购) |

### 建议

ELECWAY 是这批名片中唯一在德国(杜塞尔多夫)有实体办公室的非中国企业，两位联系人 (Alex Cernov + Steven VP)。充电桩与储能在德国地面电站场景下经常配套，值得主动联系——即使不直接合作，也可能通过他们接触到德国本地 EPC/项目方人脉。
"""

with open(path, "a", encoding="utf-8") as f:
    f.write(entry)

print("Appended to " + path)
