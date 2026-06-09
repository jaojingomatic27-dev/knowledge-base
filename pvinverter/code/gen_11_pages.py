# -*- coding: utf-8 -*-
"""Generate 11 clean white-background Xiaohongshu pages with Pillow"""
from PIL import Image, ImageDraw, ImageFont
import os

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttf"
FONT_REG  = r"C:\Windows\Fonts\msyh.ttf"

def ff(size, bold=False):
    p = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()

OUT = r"C:\AI\cc\pvinverter\output\covers\notes_pillow"
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1440

def new_page():
    img = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(img)
    return img, d

def header(d, num, title, subtitle=None):
    tag = num + "/10" if num else ""
    if tag:
        d.text((90, 80), tag, fill="#e74c3c", font=ff(30, True))
    d.text((90, 130), title, fill="#1a1a1a", font=ff(64, True))
    if subtitle:
        d.text((90, 210), subtitle, fill="#999999", font=ff(32))
    d.line([(90, 270), (W-90, 270)], fill="#e0e0e0", width=2)

def footer(d):
    d.text((W//2, H-100), "先收藏，刷走了找不回来", fill="#bbbbbb", font=ff(26), anchor="ma")
    d.text((W//2, H-60), "#储能出海 #欧盟政策 #新能源 #光伏 #电池", fill="#cccccc", font=ff(24), anchor="ma")

# ═══ P00 ═══
img, d = new_page()
d.text((W//2, 300), "欧盟对中国储能动手了", fill="#1a1a1a", font=ff(72, True), anchor="ma")
d.text((W//2, 400), "比关税狠100倍", fill="#e74c3c", font=ff(88, True), anchor="ma")
d.text((W//2, 510), "2026 欧盟七重政策壁垒 全拆解", fill="#666666", font=ff(36), anchor="ma")
tags = ["NZIA","IAA","电池法规","FSR","CBAM","CRMA","PCS"]
colors = ["#4a90d9","#e05555","#8b5cf6","#e8a840","#4caf84","#38bdf8","#f472b6"]
x0 = W//2 - (7*140)//2
for i,(t,c) in enumerate(zip(tags,colors)):
    d.rectangle([x0+i*140+10, 600, x0+(i+1)*140-10, 660], fill=c)
    d.text((x0+i*140+70, 630), t, fill="white", font=ff(22, True), anchor="ma")
d.text((W//2, 750), "不在欧洲建厂 = 丢市场", fill="#1a1a1a", font=ff(44, True), anchor="ma")
d.text((W//2, 810), "在欧洲建厂 = 可能丢技术", fill="#e74c3c", font=ff(44, True), anchor="ma")
d.text((W//2, 920), "共10篇笔记 建议按顺序收藏", fill="#999999", font=ff(30), anchor="ma")
img.save(os.path.join(OUT, "00_开头.png"))
print("P00 done")

# ═══ P01 ═══
img, d = new_page()
header(d, "01", "总览：七重政策壁垒")
rows_data = [
    ("1", "净零工业法案 NZIA", "2025.7实施", "★★★★★"),
    ("2", "工业加速器法案 IAA", "2026.3提案", "★★★★★"),
    ("3", "电池法规 2023/1542", "2023-28分阶段", "★★★★"),
    ("4", "外国补贴条例 FSR", "2023.7已生效", "★★★★"),
    ("5", "碳边境调节 CBAM", "2026.1收费", "★★★★"),
    ("6", "光伏临时关税", "2025.6生效", "★★★"),
    ("7", "储能PCS限制", "2026.5生效", "★★★"),
]
colx = [90, 130, 500, 680]
y = 310
for r in rows_data:
    d.text((colx[0], y), r[0], fill="#e74c3c", font=ff(32, True))
    d.text((colx[1], y), r[1], fill="#1a1a1a", font=ff(32, True))
    d.text((colx[2], y), r[2], fill="#666666", font=ff(28))
    d.text((colx[3], y), r[3], fill="#f0c040", font=ff(28, True))
    y += 56
y += 30
d.line([(90, y), (W-90, y)], fill="#eeeeee", width=1)
y += 30
d.text((90, y), "欧盟从收点税升级成系统性封堵", fill="#1a1a1a", font=ff(34, True))
y += 48
d.text((90, y), "不在欧洲建厂 = 丢市场    在欧洲建厂 = 可能丢技术", fill="#e74c3c", font=ff(36, True))
footer(d)
img.save(os.path.join(OUT, "01_总览.png"))
print("P01 done")

# ═══ P02 NZIA ═══
img, d = new_page()
header(d, "02", "NZIA — 净零工业法案")
d.text((90, 280), "2024年4月通过", fill="#999999", font=ff(30))
d.text((90, 320), "2025年7月全面实施", fill="#999999", font=ff(30))
d.line([(90, 360), (W-90, 360)], fill="#e0e0e0", width=2)
y = 400
d.text((90, y), "核心杀招：", fill="#e74c3c", font=ff(44, True))
y += 80
nzia_items = [
    (False, "1 非价格标准拍卖规则"),
    (True,  "2025.12.30起30%拍卖不只看价格，看供应链韧性"),
    (False, "2 供应链依赖阈值"),
    (True,  "单一国供应大于50%则公共采购须50%价值来自欧盟"),
    (False, "3 中国特设条款 第7(3)条"),
    (True,  "电池储能最终产品不得在中国组装"),
    (True,  "至少4个主要组件不得来自中国"),
]
for is_sub, txt in nzia_items:
    if is_sub:
        d.text((140 if not txt.startswith("至少") else 170, y), txt, fill="#666666" if not "不得" in txt else "#e74c3c", font=ff(30, True if "不得" in txt else False))
    else:
        d.text((90, y), txt, fill="#1a1a1a", font=ff(34, True))
    y += 48
y += 20
d.line([(90, y), (W-90, y)], fill="#e0e0e0", width=2)
y += 40
d.text((90, y), "说白了：用规则把中国产品从欧盟政府项目中排出去", fill="#e74c3c", font=ff(36, True))
footer(d)
img.save(os.path.join(OUT, "02_NZIA.png"))
print("P02 done")

# ═══ P03 IAA1 ═══
img, d = new_page()
header(d, "03", "IAA 工业加速器法案 上", "原产地要求")
y = 310
d.text((90, y), "如果说 NZIA 是不让你参加游戏", fill="#333333", font=ff(36, True))
y += 50
d.text((90, y), "那 IAA 就是——想玩？先把半条命交出来", fill="#e74c3c", font=ff(36, True))
y += 60
d.rectangle([90, y, W-90, y+160], fill="#fafafa", outline="#e0e0e0")
d.text((120, y+20), "第一阶段（生效后1-3年）", fill="#1a1a1a", font=ff(34, True))
d.text((120, y+60), "BESS须为欧盟原产", fill="#333333", font=ff(30))
d.text((120, y+95), "大于1MWh系统：BMS须欧盟原产", fill="#333333", font=ff(30))
d.text((120, y+130), "第二阶段：电芯+BMS+核心部件 全部须欧盟原产", fill="#e74c3c", font=ff(34, True))
y += 190
d.text((90, y), "全球电芯产能中国占90%以上，欧盟几乎为零", fill="#e74c3c", font=ff(36, True))
y += 50
d.text((90, y), "结论：不在欧洲建电芯厂，3年后产品进不来", fill="#1a1a1a", font=ff(38, True))
footer(d)
img.save(os.path.join(OUT, "03_IAA上.png"))
print("P03 done")

# ═══ P04 IAA2 ═══
img, d = new_page()
header(d, "04", "IAA 工业加速器法案 下", "六选四强制审查")
y = 310
d.text((90, y), "触发条件：投资大于1亿欧元+战略领域+母国产能占比大于40%", fill="#e74c3c", font=ff(32, True))
y += 50
d.text((90, y), "中国光伏电池产能占全球大于90%，必触发", fill="#e74c3c", font=ff(30, True))
y += 60
iaa_items = [
    ("1", "持股/表决权 不超过 49%", False),
    ("2", "须与欧盟企业合资，欧盟方实质参与管理", False),
    ("3", "强制向欧盟实体授权核心知识产权", True),
    ("4", "年研发支出 至少 目标企业年营收的 1%", False),
    ("5", "欧盟员工占比 至少 50%（强制！所有岗位）", True),
    ("6", "至少 30% 的生产投入来自欧盟供应链", False),
]
for num, txt, is_red in iaa_items:
    d.text((90, y), num, fill="#e74c3c" if is_red else "#333333", font=ff(34, True))
    d.text((170, y), txt, fill="#e74c3c" if is_red else "#333333", font=ff(34, True))
    y += 52
y += 30
d.line([(90, y), (W-90, y)], fill="#e0e0e0", width=2)
y += 30
d.text((90, y), "核心杀招第3条：", fill="#e74c3c", font=ff(36, True))
y += 48
d.text((90, y), "你的核心技术，要白送给欧盟实体", fill="#e74c3c", font=ff(42, True))
y += 50
d.text((90, y), "不是技术合作，不是合资——是单方面强制授权", fill="#333333", font=ff(32))
footer(d)
img.save(os.path.join(OUT, "04_IAA下.png"))
print("P04 done")

# ═══ P05 Battery ═══
img, d = new_page()
header(d, "05", "欧盟电池法规", "EU 2023/1542  2023年生效，分阶段推进")
y = 310
btl = [
    ("2025.2", "电动车电池碳足迹声明强制"),
    ("2026.2", "工业电池(大于2kWh)碳足迹等级标签"),
    ("2027.2", "数字电池护照强制（64+数据字段，QR码）"),
    ("2027.8", "供应链尽职调查（钴/锂/镍/石墨溯源到矿）"),
    ("2028.2", "最大碳阈值——超标产品禁售"),
    ("2031", "最低再生含量：钴16% 锂6% 镍6% 铅85%"),
]
for dt, txt in btl:
    is_red = "禁售" in txt
    d.ellipse([90, y+8, 102, y+20], fill="#e74c3c" if is_red else "#cccccc")
    d.text((130, y), dt, fill="#e74c3c" if is_red else "#666666", font=ff(28, True))
    d.text((310, y), txt, fill="#e74c3c" if is_red else "#333333", font=ff(30, True if is_red else False))
    y += 52
y += 30
d.rectangle([90, y, W-90, y+120], fill="#fff8e1", outline="#f0c040")
d.text((120, y+20), "最大的坑：欧盟不认可中国绿证(GEC)", fill="#e8a840", font=ff(34, True))
d.text((120, y+58), "必须证明额外性+时空匹配，否则可能直接超2028禁售阈值", fill="#333333", font=ff(28))
d.text((120, y+88), "罚款：全球年营收的 4%", fill="#e74c3c", font=ff(28, True))
y += 150
d.text((90, y), "对策：按PEF方法论收集数据 重签PPA 找CAB预审", fill="#333333", font=ff(30))
footer(d)
img.save(os.path.join(OUT, "05_电池法规.png"))
print("P05 done")

# ═══ P06 FSR ═══
img, d = new_page()
header(d, "06", "FSR 外国补贴条例 + 光伏关税")
y = 310
cases = [
    ("2024.2", "保加利亚列车采购(CRRC中车) 中企退出"),
    ("2024.4", "罗马尼亚110MW光伏(隆基+上海电气) 双方退出"),
    ("2024.4", "中国风电供应商五国调查 Dawn Raids"),
    ("2024.4", "同方威视 扣押电子设备和手机"),
    ("2025.12", "Temu都柏林 黎明突袭"),
]
for dt, txt in cases:
    d.ellipse([90, y+8, 100, y+18], fill="#e74c3c")
    d.text((130, y), dt, fill="#e74c3c", font=ff(28, True))
    d.text((310, y), txt, fill="#333333", font=ff(28))
    y += 48
y += 20
facts = [
    "2024年全部深入调查 都针对中国公司",
    "CRRC所有政府合同被算成补贴 共计75亿欧元",
    "保加利亚案回复期限 只有3天",
    "中国商务部结论（2025.1）：FSR构成贸易投资壁垒",
]
for t in facts:
    d.text((90, y), "  "+t, fill="#333333", font=ff(28))
    y += 38
y += 10
d.line([(90, y), (W-90, y)], fill="#e0e0e0", width=1)
y += 20
d.text((90, y), "光伏临时关税：2025.6.23生效，对欧出口预计下降15-20%", fill="#e74c3c", font=ff(32, True))
footer(d)
img.save(os.path.join(OUT, "06_FSR和关税.png"))
print("P06 done")

# ═══ P07 CBAM+CRMA ═══
img, d = new_page()
header(d, "07", "CBAM 碳关税 + CRMA 关键原材料")
y = 310
d.text((90, y), "CBAM 碳边境调节机制", fill="#1a1a1a", font=ff(40, True))
y += 50
d.text((90, y), "2026.1.1正式收费。铝边框/钢支架/玻璃均覆盖", fill="#333333", font=ff(30))
y += 38
d.text((90, y), "每GW碳关税 600-1000万元（按80欧元/吨碳价）", fill="#e74c3c", font=ff(34, True))
y += 38
d.text((90, y), "ESMC正推动光伏成品纳入CBAM 成本将大幅跳升", fill="#333333", font=ff(30))
y += 60
d.line([(90, y), (W-90, y)], fill="#e0e0e0", width=1)
y += 30
d.text((90, y), "CRMA 关键原材料法案", fill="#1a1a1a", font=ff(40, True))
y += 50
crma = [
    "中国稀土精炼 大于90%",
    "中国锂加工 60%",
    "欧盟风电永磁体 93% 来自中国",
    "欧盟2030目标：开采10% 加工40% 回收15% 单一来源不超过65%",
    "中欧博弈：中国限制稀土出口  << 欧盟RESourceEU 30亿欧元反制",
]
for t in crma:
    is_red = any(k in t for k in ["大于","60","93","目标","博弈"])
    d.text((90, y), "  "+t, fill="#e74c3c" if is_red else "#333333", font=ff(30, True if is_red else False))
    y += 42
y += 20
d.text((90, y), "中欧供应链脱钩在加速", fill="#e74c3c", font=ff(38, True))
footer(d)
img.save(os.path.join(OUT, "07_CBAM和CRMA.png"))
print("P07 done")

# ═══ P08 PCS ═══
img, d = new_page()
header(d, "08", "PCS 公共融资排除 + 头部企业布局")
y = 310
d.text((90, y), "PCS公共资金限制（2026.5生效）", fill="#e74c3c", font=ff(36, True))
y += 48
d.text((90, y), "EIB/EIF不得为使用中国PCS的项目提供资金", fill="#333333", font=ff(32))
y += 38
d.text((90, y), "影响约 61.82 GWh 订单", fill="#e74c3c", font=ff(30, True))
y += 60
d.text((90, y), "头部企业欧洲布局", fill="#1a1a1a", font=ff(36, True))
y += 50
ents = [
    ("CATL", "匈牙利+西班牙", "100+50GWh", "一期投产二期暂停"),
    ("BYD", "匈牙利（整车）", "50万辆/年", "电池厂尚未决策"),
    ("EVE", "匈牙利", "28GWh", "目标2026/2027"),
    ("Gotion", "德国+斯洛伐克", "~20GWh", "运营中"),
    ("CALB", "葡萄牙", "15GWh", "20亿欧元2027/2028"),
]
d.text((90, y), "企业", fill="#999999", font=ff(24, True))
d.text((280, y), "基地", fill="#999999", font=ff(24, True))
d.text((550, y), "产能", fill="#999999", font=ff(24, True))
d.text((720, y), "状态", fill="#999999", font=ff(24, True))
y += 30
d.line([(90, y), (W-90, y)], fill="#eeeeee", width=1)
for e in ents:
    y += 38
    d.text((90, y), e[0], fill="#1a1a1a", font=ff(28, True))
    d.text((280, y), e[1], fill="#333333", font=ff(26))
    d.text((550, y), e[2], fill="#333333", font=ff(26))
    d.text((720, y), e[3], fill="#666666", font=ff(24))
y += 50
d.text((90, y), "CATL投了73亿欧元，可能还不够", fill="#e74c3c", font=ff(36, True))
y += 44
d.text((90, y), "IAA要求电芯也必须欧盟原产，但本土产能几乎为零", fill="#333333", font=ff(30))
footer(d)
img.save(os.path.join(OUT, "08_PCS和头部企业.png"))
print("P08 done")

# ═══ P09 Strategy ═══
img, d = new_page()
header(d, "09", "五条应对策略")
y = 310
strats = [
    ("1", "本地化建厂", "匈牙利/东欧建厂，FTA缔约国设厂视同欧盟原产"),
    ("2", "碳合规先行", "按PEF方法论、重签PPA、区块链溯源、CAB预审"),
    ("3", "技术授权+主导权", "财务投资人，协议保留上游采购和技术迭代主导权"),
    ("4", "市场多元化", "东南亚、中东、拉美、非洲、中亚"),
    ("5", "合规前置", "风险预警、法律稳定性条款、ESG合规"),
]
for num, title, desc in strats:
    d.rectangle([90, y-4, 90+44, y+44], fill="#f0f0f0")
    d.text((112, y+20), num, fill="#e74c3c", font=ff(28, True), anchor="ma")
    d.text((160, y), title, fill="#1a1a1a", font=ff(36, True))
    d.text((160, y+44), desc, fill="#666666", font=ff(28))
    y += 96
y += 20
d.line([(90, y), (W-90, y)], fill="#e0e0e0", width=2)
y += 30
d.text((90, y), "窗口期：2027年前 —— IAA预计2027-2029逐步生效", fill="#e74c3c", font=ff(36, True))
footer(d)
img.save(os.path.join(OUT, "09_应对策略.png"))
print("P09 done")

# ═══ P10 Timeline ═══
img, d = new_page()
header(d, "10", "关键时间线 + 核心结论")
y = 310
tl = [
    ("2023", "FSR生效 / 电池法规生效 / CBAM过渡期"),
    ("2024", "NZIA+CRMA通过 / 罗马尼亚光伏FSR案"),
    ("2025", "NZIA全面实施 / 光伏关税 / 中国限制稀土出口"),
    ("2026", "CBAM收费 / IAA提案 / PCS限制 / 电池等级标签"),
    ("2027", "数字电池护照 / 供应链尽职调查"),
    ("2028", "最大碳阈值超标禁售 / CBAM扩围"),
    ("2029", "IAA公共采购原产地要求生效"),
    ("2030", "NZIA 40%本土制造目标"),
    ("2031", "电池再生含量强制"),
    ("2034", "CBAM免费配额完全取消"),
]
for yr, txt in tl:
    is_key = yr in ["2027", "2029"]
    d.ellipse([90, y+6, 100, y+16], fill="#e74c3c" if is_key else "#cccccc")
    d.text((130, y), yr, fill="#e74c3c" if is_key else "#666666", font=ff(28, True))
    d.text((230, y), txt, fill="#e74c3c" if is_key else "#333333", font=ff(28, True if is_key else False))
    y += 42
y += 30
d.line([(90, y), (W-90, y)], fill="#e0e0e0", width=2)
y += 30
d.text((90, y), "核心结论", fill="#e74c3c", font=ff(44, True))
y += 60
concs = [
    "1. 欧盟不再是加点税——是用规则重塑整个产业链的地理分布",
    "2. 中国储能/光伏企业面临的核心矛盾：不入欧=失标，入欧=可能失技术",
    "3. 2027年前是战略窗口期，完成欧洲产能+碳合规才有主动权",
]
for t in concs:
    d.text((90, y), t, fill="#1a1a1a", font=ff(32, True))
    y += 50
footer(d)
img.save(os.path.join(OUT, "10_时间线.png"))
print("P10 done")

print("ALL 11 DONE -> " + OUT)
