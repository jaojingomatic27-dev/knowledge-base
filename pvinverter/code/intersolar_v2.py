# -*- coding: utf-8 -*-
"""Consolidated Intersolar contacts research — V2"""

out = r"C:\AI\cc\pvinverter\data\intersolar_2026_contacts_analysis.md"

lines = []

# Read raw card data
with open(r"C:\AI\cc\pvinverter\input\Intersolar Europe 2026\名片.txt", "r", encoding="utf-8") as f:
    raw = f.read()

lines.append("""# Intersolar Europe 2026 — 名片联系人整理与分析 V2

> **来源**: `input/Intersolar Europe 2026/名片.txt`
> **展会**: Intersolar Europe 2026（慕尼黑）
> **分析日期**: 2026-07-15
> **总记录数**: 17 条名片记录，解析 15 家独立公司

---

## 一、公司汇总表

| # | 公司名称 | 核心产品/业务 | 国别 | 关键联系人 | 备注 |
|---|---------|-------------|------|----------|------|
| 1 | ZHEJIANG JMTHY PHOTOVOLTAIC TECHNOLOGY | 光伏组件/电池 | 中国浙江宁波 | Lexi Xue (European Sales Director) | 同时关联 Haitai Solar / Terry.Ma |
| 2 | 深圳市光澜世纪科技 GOLAND CENTURY CO. LTD | MPPT控制器/太阳能逆变器/水泵系统/路灯 | 中国深圳 | Ainsheng (General Director) | szgoland.net；含纯正弦波逆变器 |
| 3 | MG SOLAR / XIAMEN MEGAN | 光伏支架 (Solar Racking) | 中国厦门 | Megan Hu (Managing Partner) | 西班牙号码 +34，已开始欧洲本地化 |
| 4 | Electronic Way GmbH (ELECWAY) | 电动汽车充电桩 (EV DC Charger) | 德国杜塞尔多夫 | Alex Cernov + Steven (VP) | **在德国有实体**，杜塞地址 |
| 5 | SHIMGE PUMP 新界泵业 | 水泵 | 中国浙江温岭 | Nina Wu (Marketing Manager) | **非光伏** |
| 6 | Jiangsu VDS Renewable Technology | 光伏逆变器/储能系统 | 中国江苏 | Sarah Tong (Sales Manager) | VIYOS 品牌，vds-power.com |
| 7 | PERLIGHT SOLAR | 光伏组件 | 中国浙江温岭 | Caroline Lu (Sales) | perlight.com |
| 8 | ZHEJIANG ERA SOLAR TECHNOLOGY | 光伏组件/电池 | 中国浙江台州 | 公元 (Sales Manager) | European Region 标签 |
| 9 | 宁波晶华新能源 NINGBO JINGHUA NEW ENERGY | **光伏接线盒 (PV Junction Box)** / 光伏板保护电路 | 中国浙江 | 肖炯 (International Sales Director) | **jhbox.com，做光伏板电气保护** |
| 10 | YINGFA 英发 | 光伏/储能 | 中国 | Luis Lan (Sales) | 印尼号码 +62 |
| 11 | 正信光电 ZNSHINESOLAR | 光伏组件 | 中国常州金坛 | 张姬 (运营经理) | znshinesolar.com |
| 12 | Qujing Huanju / Hangal Longshaeng | 光伏材料/复合材料 | 中国 | Huichin Chang (Exec Asst) | 英国号码 +44 |
| 13 | APsolway | 不详 | — | 刘姐姐 (总经理) | 信息极少 |
| 14 | FORTUNES SOLAR TECHNOLOGY | **光伏逆变器 (PV Inverter)** | 中国江苏张家港 | Bruce (Trade Manager) | **逆变器同行** |
| 15 | Shenzhen Sola-E Technology | 便携式/柔性太阳能板 | 中国深圳 | 索拉尔 (BD Manager) | sola-e.us，移动能源系统 |

---

## 二、关于"光伏板保护电路"的公司

### ✅ 找到了：宁波晶华新能源 (NINGBO JINGHUA NEW ENERGY)

名片 OCR 提取的关键信息：
- **公司**: 宁波晶华新能源科技有限公司 / NINGBO JINGHUA NEW ENERGY TECHNICAL CO.,LTD
- **联系人**: 肖炯 — International Sales Director
- **手机**: +86 13567825517
- **邮箱**: jhpvbox@aliyun.com
- **网址**: www.jhbox.com
- **产品**: 光伏接线盒 (PV Junction Box)，即你所说的"光伏板保护电路"

### 光伏接线盒是什么？

它就是装在光伏板背面的那个小盒子——核心作用是：
1. **旁路二极管保护** — 当某片电池被阴影遮挡时，电流绕过它，防止热斑烧毁光伏板
2. **电气连接** — 把光伏板的直流电接出来
3. **防反/防雷/防水** — IP67/IP68 防护等级

所以你说的"光伏板的保护电路"，就是对这家公司的准确描述。联系人肖炯是 International Sales Director，邮箱 jhpvbox@aliyun.com。

---

## 三、新发现：之前遗漏的两家公司

### 2. 深圳市光澜世纪科技 (GOLAND CENTURY)

之前标记为"业务不详"。现在查到了：这家公司做太阳能控制器、MPPT 控制器、纯正弦波逆变器(Pure Sine Wave Inverter)、太阳能水泵系统、太阳能路灯等。**也是一家逆变器厂商**（主要做离网/户用逆变器）。

### 4. Electronic Way GmbH (ELECWAY)

之前也标记为"不详"。现在查到：做**电动汽车直流充电桩 (EV DC Charger)**，在杜塞尔多夫有实体办公室 (Kreuzstrasse 60, 40210 Dusseldorf)。虽然不是光伏/储能，但充电桩和储能在地面电站场景下常配套。

---

## 四、更新后的客户画像

| 类型 | 数量 | 公司 |
|------|------|------|
| 光伏组件/电池 | 5 | JMTHY, PERLIGHT, ERA, 正信光电, Haitai Solar |
| 光伏逆变器 | 3 | **FORTUNES SOLAR**, **GOLAND CENTURY (光澜世纪)**, VDS |
| 光伏支架 | 1 | MG SOLAR |
| 光伏接线盒/保护 | 1 | **宁波晶华 (JHBOX)** |
| 光伏材料/复材 | 1 | Qujing Huanju |
| 便携式太阳能 | 1 | Sola-E |
| 充电桩 | 1 | ELECWAY (德国杜塞尔多夫实体) |
| 水泵(非光伏) | 1 | SHIMGE |
| 不详 | 1 | APsolway |

---

## 五、与逆变器/PCS业务相关的重要关系

| 公司 | 关系类型 | 优先级 | 建议动作 |
|------|---------|--------|---------|
| **FORTUNES SOLAR** | 逆变器同行 | 中 | 了解对方产品定位(组串式/集中式?功率段?)，判断是竞争还是互补 |
| **GOLAND CENTURY (光澜世纪)** | 逆变器同行（离网/户用） | 低 | 主要是离网小功率，跟大储PCS重叠不大 |
| **VDS Renewable** | 逆变器/储能系统 | 中 | 品牌 VIYOS，查一下功率和认证情况 |
| **ELECWAY** | 杜塞本地充电桩公司 | 高 | **德国本地公司**，充电桩+储能有交叉场景，可探讨渠道合作/本地人脉介绍 |
| **宁波晶华 (JHBOX)** | 光伏板保护电路 | 高(你的问题) | 接线盒厂家，肖炯 International Sales Director |
| **MG SOLAR** | 光伏支架 | 中 | 支架+逆变器在项目中常一起采购，Megan 在西班牙有布局 |
""")

with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("V2 written: " + out)
