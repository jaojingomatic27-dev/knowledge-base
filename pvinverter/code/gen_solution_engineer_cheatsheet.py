# -*- coding: utf-8 -*-
"""Generate solution_engineer_cheatsheet.png — regenerated with correct encoding"""
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

y = 100
d.text((W//2, y), "PCS 技术方案/售前工程师", fill="#1a1a1a", font=ff(56, True), anchor="ma")
y += 80
d.text((W//2, y), "核心职责 · 所需能力 · 为什么必须在德国", fill="#999999", font=ff(32), anchor="ma")
y += 60
d.line([(90, y), (W-90, y)], fill="#e0e0e0", width=2)

y += 40
sections = [
    ("核心职责 (70%)", [
        "投标技术方案 — 读德语招标书 → PCS配置/单线图",
        "并网兼容性分析 — VDE 4105/4110/4120/EN 50549",
        "系统方案设计 — PCS+变压器+BESS+EMS/SCADA",
        "FAT/SAT技术支持 — 工厂+现场验收技术代表",
    ]),
    ("延伸职责 (30%)", [
        "竞品技术对标 → 向中国研发反馈市场技术需求",
        "新品本地化验证 → 德国电网仿真/现场试点",
        "培训销售团队 → 储能PCS 101技术培训",
    ]),
    ("硬技能（必须）", [
        "电力电子拓扑 / 单线图 / 变压器选型",
        "VDE 4105/4110/4120 + EN 50549 并网标准",
        "BESS系统集成：电池 ↔ PCS ↔ EMS链路",
        "Modbus / IEC 61850 / CANbus 通信协议",
        "德语技术文档读写 C1+ 英语商务 B2+",
    ]),
    ("软技能（同样必须）", [
        "跨文化沟通 — 中国研发 ↔ 德国客户",
        "客户服务 — 快速响应 + 技术有据",
        "压力承受 — 投标截止前48小时的冷静",
        "结构化表达 — 逻辑 + 数据 + 图示",
    ]),
    ("为什么必须在德国 (5个理由)", [
        "1. 时差 — 30分钟响应 vs 6小时延迟",
        "2. 法域 — § StromNEV/EEG 不是语言,是Jurisdiction",
        "3. 现场 — 并网评估/技术答辩/FAT不可能是Zoom",
        "4. 跨文化中介 — 两国技术逻辑的唯一翻译器",
        "5. 信任 — 电网是国安级,必须见过人握过手",
    ]),
]

for title, items in sections:
    d.text((90, y), title, fill="#e74c3c" if "???" in title else "#1a1a1a", font=ff(36, True))
    y += 48
    for item in items:
        d.text((110, y), "  " + item, fill="#333333", font=ff(28))
        y += 38
    y += 12

d.text((W//2, H-100), "底线：与客户直接沟通的技术角色，必须在德国本地", fill="#e74c3c", font=ff(32, True), anchor="ma")
d.text((W//2, H-55), "#储能出海 #技术方案 #售前工程师 #德国招聘", fill="#cccccc", font=ff(24), anchor="ma")

path = r"C:\AI\cc\pvinverter\output\solution_engineer_cheatsheet.png"
img.save(path)
print("OK: " + path)
