# -*- coding: utf-8 -*-
"""Generate sales_vs_presales_cheatsheet.png — regenerated with correct encoding"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttf"
FONT_REG  = r"C:\Windows\Fonts\msyh.ttf"

def ff(size, bold=False):
    p = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()

W, H = 1080, 1440
img = Image.new("RGB", (W, H), "#ffffff")
d = ImageDraw.Draw(img)

# title
d.text((W//2, 100), "销售 vs 售前 vs 方案工程师", fill="#1a1a1a", font=ff(56, True), anchor="ma")
d.text((W//2, 170), "同一链条  不同角色  不能合并", fill="#999999", font=ff(32), anchor="ma")
d.line([(90, 220), (W-90, 220)], fill="#e0e0e0", width=2)

# section 1
y = 250
d.text((90, y), "一、称呼澄清", fill="#e74c3c", font=ff(36, True)); y += 50
d.text((90, y), "方案工程师 = 售前工程师 = Solution Engineer", fill="#1a1a1a", font=ff(32, True)); y += 42
d.text((90, y), "储能PCS行业最准确的叫法：Solution Engineer", fill="#333333", font=ff(28)); y += 42
d.text((90, y), "卖的不是单一设备  是PCS+变压器+并网+通信的系统级方案", fill="#666666", font=ff(28)); y += 50

# section 2
d.text((90, y), "二、8个维度的核心差异", fill="#e74c3c", font=ff(36, True)); y += 50
rows = [
    ("核心KPI", "签了多少MW/多少钱", "技术标得分/技术澄清完成数"),
    ("工作产出", "合同（签字经过谈判）", "技术标书/单线图/配置表/合规报告"),
    ("沟通对象", "采购总监/VP/财务", "电网工程师/系统集成/电气设计"),
    ("语言", "商业：ROI IRR TCO 付款 违约金", "技术：kW kVAr ms % IEC 61850 Modbus"),
    ("性格", "外向 关系驱动 抗拒绝 谈判型", "内向中向 逻辑驱动 细节强迫 分析型"),
    ("知识结构", "三成技术 七成商务 满级人脉", "七成技术 三成商务 足够沟通"),
    ("出差", "展会 客户拜访 签约仪式", "技术澄清会 FAT SAT 电网对接"),
    ("收入", "底薪+提成 高风险高回报", "底薪+项目奖金 低风险稳定"),
]
d.rectangle([80, y, 1000, y+36], fill="#f5f5f5")
d.text((120, y+18), "维度", fill="#999999", font=ff(24, True))
d.text((290, y+18), "销售 Sales", fill="#999999", font=ff(24, True))
d.text((680, y+18), "售前/方案 Pre-Sales", fill="#999999", font=ff(24, True))
y += 38
for dim, sales, presales in rows:
    d.text((120, y), dim, fill="#1a1a1a", font=ff(26, True))
    d.text((290, y), sales, fill="#333333", font=ff(26))
    d.text((680, y), presales, fill="#333333", font=ff(26))
    y += 34
y += 20

# section 3
d.text((90, y), "三、为什么不能合并成一个人？", fill="#e74c3c", font=ff(36, True)); y += 50
reasons = [
    "1  写技术标书是全职工种  —  200页德语标书需2-3周逐条回复",
    "2  能力的天然矛盾  —  人际关系vs逻辑深度  两个极端",
    "3  客户有两个接口  —  采购部门(销售)+工程部门(方案)",
    "4  签字责任不同  —  技术参数承诺 vs 商务条款承诺",
]
for r in reasons:
    d.text((90, y), r, fill="#333333", font=ff(28, True)); y += 36
y += 12

# bottom line
d.line([(90, y), (W-90, y)], fill="#e0e0e0", width=2); y += 30
d.text((W//2, y), "中国公司常见误区：招一个有技术背景的销售就行", fill="#e74c3c", font=ff(32, True), anchor="ma"); y += 44
d.text((W//2, y), "在德语区储能行业  这不成立  —  技术严谨度全球最高", fill="#1a1a1a", font=ff(30, True), anchor="ma"); y += 44
d.text((W//2, y), "RWE会要求你用MATLAB做并网仿真+附FGH独立测试报告", fill="#666666", font=ff(28), anchor="ma")

d.text((W//2, H-100), "文件: data/sales_vs_presales_vs_solution_engineer.md", fill="#cccccc", font=ff(22), anchor="ma")
d.text((W//2, H-60), "#储能出海 #售前 #销售 #方案工程师 #德国招聘", fill="#cccccc", font=ff(22), anchor="ma")

path = r"C:\AI\cc\pvinverter\output\sales_vs_presales_cheatsheet.png"
img.save(path)
print("OK: " + path)
