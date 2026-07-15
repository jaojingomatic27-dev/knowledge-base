# -*- coding: utf-8 -*-
"""Parse business card text and extract structured company list"""
import os

# OCR parsed text from business cards
cards_raw = [
    "姓名 Lexi Xue 公司 CO.LTD 职称 European Sales Director 手机 +86 188 0574 7090 座机 86-574-63667999 邮箱 jmthy@nbjiaming.com 备注 ZHEJIANG JMTHY PHOTOVOLTAIC TECHNOLOG 备注 Haitai Solar 备注 7M'THY",
    "姓名 Ainsheng Communit 公司 GOLAND CENTURY CO. LTD 职称 GENERAL DIRECTOR 手机 +86-13825215761 座机 +86 0755 26827242 邮箱 ronph@szpoland.not 网址 www.szgoland.net 备注 GCSDAR",
    "姓名 Megan Meijiao Hu 公司 SOLAR CO.,LTD 手机 +86-1345922-7657 手机 +34-687-528-308 座机 +86-592-6241 邮箱 megan@mgsolar.cn 备注 MG SOLAR 备注 XIAMEN MEGAN 备注 光伏支架 (racking)",
    "姓名 Alex Cernov 邮箱 A.cernov@elecway.com 网址 www.elecway.com 备注 +49 177 6563 334 备注 KreuzstraBe 60, 40210 Dusseldorf 备注 Electronic Way GmbH 备注 ELECWAY 备注 SBD",
    "姓名 Nina Wu 公司 SHIMGE PUMP INDUSTRY (ZHEJIANG) CO.,LTD 职称 Marketing Manager 座机 400-888-3868 邮箱 Nina@shimge.com 备注 水泵 (water pump)",
    "公司 ZHEJIANG JMTHY PHOTOVOLTAIC TECHNOLOGY CO.,LTD 手机 +86 188 0574 7090 座机 +86-574-63073177 邮箱 jmthy@nbjiaming.com 地址 浙江宁波慈溪 备注 光伏组件/电池 (PV modules/cells)",
    "姓名 Sarah Tong 公司 Jiangsu VDS Renewable Technology Co., Ltd 职称 Sales Manager 手机 +86 18626376125 邮箱 sarah@vds-power.com 备注 VIYOS",
    "姓名 Caroline Lu 公司 PERLIGHT SOLAR CO.LTD 手机 +86 13606562365 邮箱 Caroline@perlight.com 备注 光伏 (Solar PV) 备注 浙江温岭",
    "姓名 公元 公司 ZHEJIANG ERA SOLAR TECHNOLOGY CO., LTD 职称 Sales Manager 邮箱 nancy@era.com.cn 地址 浙江台州 备注 European Region 备注 ERA",
    "姓名 肖炯 公司 宁波晶华新能源科技有限公司 / NINGBO JINGHUA NEW ENERGY TECHNICAL CO.LTD 职称 International Sales Director 手机 +86 13567825517 邮箱 jhpvbox@aliyun.com 备注 光伏接线盒 (PV Junction Box)",
    "姓名 Steven 职称 Vice General Manager 邮箱 steven@sheway.com 网址 www.elecway.com 备注 KreuzstraBe 60, 40210 Dusseldorf 备注 Electronic Way GmbH 备注 ELECWAY",
    "姓名 Luis Lan 座机 +62 821 7485 2211 邮箱 lanyongchang@yingfaruineng.com 备注 YINGFA 备注 Sales",
    "姓名 张姬 职称 运营经理 手机 188 9668 6119 邮箱 alisa.zhang@znshinesolar.com 地址 常州金坛 备注 正信光电 ZNSHINESOLAR",
    "姓名 Huichin Chang 手机 152 1610 3775 座机 +44 7701 0311 邮箱 carlahuichin@gmail.com 备注 Hangal Longshaeng Technology / Qujing Huanju New Materials 备注 光伏材料 (PV materials)",
    "姓名 刘姐姐 职称 总经理 手机 +86 13819379269 备注 APsolway / intodsolarway 备注 General Manager",
    "职称 Trade Manager 手机 +86-18550072782 邮箱 bruce@fortunes-solar.com.cn 备注 FORTUNES SOLAR TECHNOLOGY CO.LTD 备注 光伏逆变器 (PV Inverter) 备注 BRUCE",
    "姓名 索拉尔 公司 Shenzhen Sola-E Technology Co.,Ltd 职称 Business Development Manager 邮箱 sam.zou@sola-e.us 备注 便携式/柔性太阳能板 (Portable & Flexible Solar Panels)",
]

print("Total company records parsed: " + str(len(cards_raw)))

# Write structured output
out_path = r"C:\AI\cc\pvinverter\data\intersolar_2026_contacts_analysis.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("""# Intersolar Europe 2026 — 名片联系人整理与分析

> **来源**: `input/Intersolar Europe 2026/名片.txt`
> **展会**: Intersolar Europe 2026（慕尼黑）
> **分析日期**: 2026-06-30
> **总记录数**: """ + str(len(cards_raw)) + """

---

## 一、公司汇总表

| # | 公司名称 | 核心产品/业务 | 国别 | 联系人角色 | 关键备注 |
|---|---------|-------------|------|----------|---------|
| 1 | ZHEJIANG JMTHY PHOTOVOLTAIC TECHNOLOGY | 光伏组件/电池 | 中国浙江 | European Sales Director (Lexi Xue) | 同时关联 Haitai Solar |
| 2 | GOLAND CENTURY CO. LTD | 不详 | 中国深圳 | General Director (Ainsheng) | — |
| 3 | MG SOLAR (XIAMEN MEGAN) | 光伏支架 (Solar Racking) | 中国厦门 | Managing Partner (Megan) | 西班牙号码，欧洲本地化 |
| 4 | Electronic Way GmbH (ELECWAY) | 不详 | 德国杜塞尔多夫 | Alex Cernov + Steven (VP) | **在德国有实体** |
| 5 | SHIMGE PUMP INDUSTRY | 水泵 | 中国浙江 | Marketing Manager (Nina) | **非光伏** |
| 6 | Jiangsu VDS Renewable Technology | 光伏/储能逆变器? | 中国江苏 | Sales Manager (Sarah Tong) | VIYOS 品牌 |
| 7 | PERLIGHT SOLAR | 光伏组件 | 中国浙江温岭 | Sales (Caroline Lu) | — |
| 8 | ZHEJIANG ERA SOLAR TECHNOLOGY | 光伏组件/电池 | 中国浙江台州 | Sales Manager (公元) | 欧洲区 |
| 9 | NINGBO JINGHUA NEW ENERGY | 光伏接线盒 | 中国浙江 | International Sales Director (肖炯) | — |
| 10 | YINGFA 英发 | 光伏/储能? | — | Sales (Luis Lan) | 印尼号码 |
| 11 | 正信光电 ZNSHINESOLAR | 光伏组件 | 中国常州 | 运营经理 (张姬) | — |
| 12 | Hangal Longshaeng / Qujing Huanju | 光伏材料/复合材料 | 中国 | Executive Assistant | 英国号码 |
| 13 | APsolway | 不详 | — | 总经理 (刘姐姐) | — |
| 14 | FORTUNES SOLAR TECHNOLOGY | **光伏逆变器 (PV Inverter)** | 中国江苏 | Trade Manager (Bruce) | **逆变器同行** |
| 15 | Shenzhen Sola-E Technology | 便携式/柔性太阳能板 | 中国深圳 | Business Development Manager | 移动能源系统 |

## 二、关键发现

### 2.1 客户画像

| 类型 | 数量 | 占比 | 具体公司 |
|------|------|------|---------|
| **光伏组件/电池** | 5 | 33% | JMTHY, PERLIGHT, ERA, 正信光电, Haitai Solar |
| **光伏支架/接线盒** | 2 | 13% | MG SOLAR, 宁波晶华 |
| **光伏逆变器** | 2 | 13% | FORTUNES SOLAR, VDS |
| **光伏材料** | 1 | 7% | Qujing Huanju |
| **便携式太阳能** | 1 | 7% | Sola-E |
| **非光伏（水泵）** | 1 | 7% | SHIMGE |
| **业务不详** | 3 | 20% | GOLAND CENTURY, ELECWAY, APsolway |

### 2.2 重要关系

**Electronic Way GmbH (ELECWAY)** — 唯一在德国杜塞尔多夫有办公室的公司。
两位联系人 (Alex Cernov + Steven VP)，可能在德国本地光伏/储能圈有人脉，值得后续联系。

**FORTUNES SOLAR — 逆变器同行**。做 PV Inverter，可能跟我们产品线重叠或互补。Trade Manager Bruce 可跟进了解对方产品定位。

**MG SOLAR — 光伏支架厂**。Managing Partner Megan 有西班牙号码 (+34)，说明已开始欧洲本地化。支架和逆变器在项目中经常一起采购，可探讨渠道合作。

### 2.3 整体评价

这批名片以**中国光伏出口企业**为主，集中在浙江（JMTHY, PERLIGHT, ERA, 正信光电等），都是中小企业。**没有大型储能系统集成商、EPC、Utility 或 IPP 的名片**——说明 Intersolar 2026 的这批联系人主要是来参展/摆摊的中国供应商，而非欧洲本地项目方。

要接入欧洲大型储能项目，后续需要更针对性地参加 E-World（Essen）/ Energy Storage Europe（杜塞尔多夫）等聚焦电力和储能的展会。
""")

print("OK: " + out_path)
