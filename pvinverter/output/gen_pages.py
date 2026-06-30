#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 10 小红书 note cards with 楷体 handwriting font, 3:4, left-aligned, polite wording."""

import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"C:\AI\cc\pvinverter\output"
W, H = 1080, 1440  # 3:4
PADDING_L = 60
PADDING_R = 60
PADDING = PADDING_L  # all left-aligned

BG_COLOR   = (255, 255, 255)
ACCENT     = (200, 40, 40)
SOFT_RED   = (220, 80, 80)
DARK       = (50, 50, 50)
GRAY       = (130, 130, 130)
LIGHT_GRAY = (248, 248, 248)
MID_GRAY   = (225, 225, 225)
PILL_BG    = (255, 242, 242)
STRIPE_GRAY = (235, 235, 235)

FONT_BODY  = r"C:/Windows/Fonts/simkai.ttf"    # 楷体 — handwrite style
FONT_TITLE = r"C:/Windows/Fonts/simhei.ttf"    # 黑体 — bold contrast for headings

def gf(size, style="title"):
    path = FONT_TITLE if style == "title" else FONT_BODY
    return ImageFont.truetype(path, size)

# Pre-measure
def tw(font, text): return font.getbbox(text)[2] - font.getbbox(text)[0]
def th(font, text): return font.getbbox(text)[3] - font.getbbox(text)[1]

def wrap_lines(text, font, max_w):
    out, cur = [], ""
    for ch in text:
        t = cur + ch
        if tw(font, t) > max_w and cur:
            out.append(cur); cur = ch
        else: cur = t
    if cur: out.append(cur)
    return out or [text]

# ── drawing helpers ──

def make_base():
    img = Image.new("RGB", (W, H), BG_COLOR)
    d = ImageDraw.Draw(img)
    # soft top accent bar
    d.rectangle([0, 0, W, 8], fill=SOFT_RED)
    return img, d

def page_num(draw, n):
    f = gf(28)
    txt = f"· {n}/10 ·"
    w = tw(f, txt)
    draw.text((PADDING, 16), txt, fill=SOFT_RED, font=f)

def footer(draw):
    f = gf(26)
    txt = " 收藏  慢慢消化        #欧盟储能政策全拆解"
    draw.rectangle([0, H - 72, W, H], fill=(250, 250, 250))
    w = tw(f, txt)
    draw.text(((W - w)//2, H - 58), txt, fill=GRAY, font=f)

def section_pill(draw, y, text):
    """Red-text section heading, left aligned, with a light pill behind it."""
    f = gf(52, "title")
    line_h = th(f, text)
    w = tw(f, text)
    # subtle pill bg
    draw.rectangle([PADDING - 4, y - 2, PADDING + w + 12, y + line_h + 8], fill=PILL_BG)
    draw.text((PADDING + 4, y + 2), text, fill=SOFT_RED, font=f)
    return y + line_h + 28

def rule_line(draw, y):
    draw.line([PADDING, y, W - PADDING_R, y], fill=MID_GRAY, width=1)
    return y + 18

def body_line(draw, y, text, font=None):
    """Draw one line of body text, left-aligned. Returns new y."""
    if font is None: font = gf(48, "body")
    lh = th(font, text)
    draw.text((PADDING, y), text, fill=DARK, font=font)
    return y + lh + 12

def body_block(draw, y, text, font=None):
    """Word-wrapped body block."""
    if font is None: font = gf(48, "body")
    max_w = W - PADDING_L - PADDING_R
    for line in wrap_lines(text, font, max_w):
        y = body_line(draw, y, line, font)
    return y

def note_line(draw, y, text):
    """Smaller note line, gray."""
    f = gf(36, "body")
    lh = th(f, text)
    draw.text((PADDING + 8, y), text, fill=GRAY, font=f)
    return y + lh + 8

def bullet_line(draw, y, text, font=None):
    if font is None: font = gf(44, "body")
    lh = th(font, text)
    draw.text((PADDING + 16, y), text, fill=DARK, font=font)
    return y + lh + 10

def star_list(draw, y, items):
    """Items prefixed with   ."""
    f = gf(46, "body")
    max_w = W - PADDING_L - PADDING_R - 48
    for item in items:
        prefix = "  "
        lines = wrap_lines(item, f, max_w)
        for li, line in enumerate(lines):
            if li == 0:
                t = prefix + line
            else:
                t = "   " + line
            lh = th(f, t)
            draw.text((PADDING + 8, y), t, fill=DARK, font=f)
            y += lh + 12
    return y

def gap(draw, y, px=14):
    return y + px


# ═══════════════════════════════════════
# PAGE 1 — 封面·总览
# ═══════════════════════════════════════
def pg1():
    img, d = make_base()
    page_num(d, 1)
    y = 80

    y = body_line(d, y, "EU 与 CN 储能", gf(72, "title"))
    y = body_line(d, y, "比关税更深远的变化", gf(56, "title"))
    y = rule_line(d, y)
    y = gap(d, y, 12)
    y = body_line(d, y, "2026 七项政策梳理   一文读懂", gf(44, "body"))
    y = gap(d, y, 28)

    barriers = [
        ("NZIA", "净零工业法案", "2025.7 生效"),
        ("IAA", "工业加速器法案", "2026 提出"),
        ("电池法规", "2023/1542", "2023-2028"),
        ("CBAM", "碳边境调节", "2026.1 执行"),
        ("FSR", "外国补贴条例", "2023 生效"),
        ("光伏保障", "临时保障措施", "2025.6"),
        ("储能限制", "PCS 融资规则", "2026.5"),
    ]
    box_w = (W - PADDING_L - PADDING_R - 24) // 4
    box_h = 96
    for i, (abbr, name, date) in enumerate(barriers):
        col = i % 4
        row = i // 4
        bx = PADDING + col * (box_w + 8)
        by = y + row * (box_h + 8)
        d.rectangle([bx, by, bx + box_w, by + box_h], fill=LIGHT_GRAY, outline=MID_GRAY)
        af = gf(34, "title")
        nf = gf(22, "body")
        df = gf(20, "body")
        d.text((bx + 10, by + 10), abbr, fill=SOFT_RED, font=af)
        d.text((bx + 10, by + 48), name, fill=DARK, font=nf)
        d.text((bx + 10, by + 72), date, fill=GRAY, font=df)

    y += 2 * (box_h + 8) + 36
    y = section_pill(d, y, "一句话")
    y = gap(d, y, 6)
    y = body_line(d, y, "不在欧洲深耕   可能失去市场", gf(48, "body"))
    y = body_line(d, y, "深度融入欧洲   则需审慎布局", gf(48, "body"))
    y = gap(d, y, 10)
    y = note_line(d, y, "欧盟正用规则引导产业链重新分布，这或许是个重新思考的机会。")
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_01_封面总览.png"))
    print("OK pg1")

# ═══════════════════════════════════════
# PAGE 2 — NZIA
# ═══════════════════════════════════════
def pg2():
    img, d = make_base()
    page_num(d, 2)
    y = 80
    y = body_line(d, y, "NZIA 净零工业法案", gf(60, "title"))
    y = note_line(d, y, "2024.4 通过   2025.7 全面实施")
    y = rule_line(d, y)
    y = gap(d, y, 8)
    y = section_pill(d, y, "值得关注的三个方向")
    y = gap(d, y, 8)

    y = body_line(d, y, "  拍卖评价体系多元化", gf(50, "title"))
    y = body_block(d, y, "2025.12.30 起，至少 30%（或 6 GW）的可再生能源拍卖，除价格外也将综合评估供应链韧性、网络安全与可持续表现。")
    y = gap(d, y, 16)

    y = body_line(d, y, "  供应链集中度考量", gf(50, "title"))
    y = body_block(d, y, "若某一第三国供应占比超过 50%，欧盟公共采购将被要求确保至少 50% 的附加值来自欧盟内部，否则可能面临合同额 10% 的罚则。")
    y = gap(d, y, 16)

    y = body_line(d, y, "  特定领域的补充条款（第 7(3) 条）", gf(50, "title"))
    y = body_block(d, y, "即使未触发上述集中度阈值，部分领域（如陆上/海上风电、电解槽）也需控制对特定来源的依赖。电池储能方面，最终组装与至少 4 个主要组件建议逐步实现多元化布局。")
    y = gap(d, y, 16)

    y = rule_line(d, y)
    y = note_line(d, y, "某种程度上，这是在用规则鼓励供应链的多样化。")
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_02_NZIA净零工业法案.png"))
    print("OK pg2")

# ═══════════════════════════════════════
# PAGE 3 — IAA 上（原产地）
# ═══════════════════════════════════════
def pg3():
    img, d = make_base()
    page_num(d, 3)
    y = 80
    y = body_line(d, y, "IAA 工业加速器法案（上）", gf(56, "title"))
    y = note_line(d, y, "2026.3.4 提出   尚在讨论中")
    y = rule_line(d, y)
    y = gap(d, y, 8)
    y = section_pill(d, y, "大方向")
    y = body_block(d, y, "目标是将制造业在 GDP 中的占比从约 14.3% 逐步提升至 20%（2035 年远景）。为达成这一目标，提案对部分战略性产品提出了更明确的原产地期望。")
    y = gap(d, y, 16)
    y = section_pill(d, y, "储能产品相关条款（草案）")
    y = gap(d, y, 8)
    y = body_line(d, y, "过渡期（生效后第 1-3 年）", gf(50, "title"))
    y = star_list(d, y, ["电池储能系统希望逐步达到「欧盟原产」标准", "1 MWh 以上系统：BMS 建议由欧盟本土供应"])
    y = gap(d, y, 16)
    y = body_line(d, y, "全面实施期（生效后第 3 年起）", gf(50, "title"))
    y = star_list(d, y, ["电池储能系统需为欧盟原产", "电芯、BMS 及至少一项核心部件均建议在欧盟生产"])
    y = gap(d, y, 16)
    y = rule_line(d, y)
    y = note_line(d, y, "目前全球电芯产能高度集中在东亚。对于希望深耕欧洲市场的企业来说，")
    y = note_line(d, y, "这或许提示着本地化的时间表正在提前。")
    y = gap(d, y, 4)
    y = note_line(d, y, "  下篇：IAA 中关于外商投资审查的讨论")
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_03_IAA原产地.png"))
    print("OK pg3")

# ═══════════════════════════════════════
# PAGE 4 — IAA 下（六选四）
# ═══════════════════════════════════════
def pg4():
    img, d = make_base()
    page_num(d, 4)
    y = 80
    y = body_line(d, y, "IAA 外商投资审查框架", gf(54, "title"))
    y = note_line(d, y, "关于「六选四」机制的梳理")
    y = rule_line(d, y)
    y = gap(d, y, 8)
    y = section_pill(d, y, "什么情况下可能触发？")
    y = body_block(d, y, "提案建议，当单笔投资超过 1 亿   、属于新兴战略制造领域、且母国在该领域的全球产能占比较高时，可能被纳入审查范围。")
    y = gap(d, y, 16)
    y = section_pill(d, y, "需要满足的条件（满足  4 项）")
    y = gap(d, y, 6)

    conds = [
        "外资持股与表决权建议不超过 49%",
        "建议与欧盟企业建立合资关系，欧方实质性参与管理",
        "可能被要求向欧盟实体授权部分核心知识产权",
        "建议年度在欧研发投入不低于目标企业年营收的 1%",
        "  欧盟员工占比建议不低于 50%（此项为强制性要求）",
        "至少 30% 的生产投入来自欧盟供应链",
    ]
    for ci, c in enumerate(conds):
        marker = "  " if "  " in c else "  "
        y = body_line(d, y, f"  {marker} {c.replace(chr(0x20)*3, '').strip()}", gf(43, "body"))

    y = gap(d, y, 20)
    y = rule_line(d, y)
    y = body_block(d, y, "需要说明的是，部分条款（尤其是知识产权相关安排）仍处于讨论阶段，最终文本可能与提案有较大出入。建议保持关注。", gf(40, "body"))
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_04_IAA六选四.png"))
    print("OK pg4")

# ═══════════════════════════════════════
# PAGE 5 — 电池法规
# ═══════════════════════════════════════
def pg5():
    img, d = make_base()
    page_num(d, 5)
    y = 80
    y = body_line(d, y, "电池法规 2023/1542", gf(60, "title"))
    y = note_line(d, y, "碳足迹   数字护照   再生含量")
    y = rule_line(d, y)
    y = gap(d, y, 12)
    y = section_pill(d, y, "关键时间节点")
    y = gap(d, y, 8)

    tl = [
        ("2025.2", "电动车电池碳足迹声明开始执行"),
        ("2026.2", "工业电池（>2 kWh）碳足迹等级标签"),
        ("2027.2", "数字电池护照上线（64+ 字段，QR 码）"),
        ("2027.8", "供应链尽职调查（钴/锂/镍/石墨溯源）"),
        ("2028.2", "最大碳足迹阈值生效   超标产品将受限"),
        ("2031", "最低再生含量要求（钴 16% 等）"),
    ]
    for i, (yr, desc) in enumerate(tl):
        yf = gf(40, "title")
        df = gf(38, "body")
        row_h = 48
        stripe = LIGHT_GRAY if i % 2 == 0 else BG_COLOR
        d.rectangle([PADDING, y, W - PADDING_R, y + row_h], fill=stripe)
        d.text((PADDING + 12, y + 4), yr, fill=SOFT_RED, font=yf)
        d.text((PADDING + 150, y + 4), desc, fill=DARK, font=df)
        y += row_h + 4

    y = gap(d, y, 20)
    y = section_pill(d, y, "值得注意的挑战")
    y = body_block(d, y, "欧盟目前对中国的绿证（GEC）认可度有限。电力碳足迹的计算涉及额外性论证与时空匹配（建议小时级、同电网区域），建议企业尽早参照欧盟 PEF 方法论进行数据准备。")
    y = gap(d, y, 12)
    y = rule_line(d, y)
    y = note_line(d, y, "违规罚则可能达到全球年营收的 4%。提早规划，从容应对。")
    y = gap(d, y, 6)
    y = note_line(d, y, "  建议：按欧盟 PEF 方法论收集数据、重签 PPA、联系 CAB 机构预审。")
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_05_电池法规碳足迹.png"))
    print("OK pg5")

# ═══════════════════════════════════════
# PAGE 6 — FSR + 光伏保障
# ═══════════════════════════════════════
def pg6():
    img, d = make_base()
    page_num(d, 6)
    y = 80
    y = body_line(d, y, "FSR 与光伏保障措施", gf(56, "title"))
    y = note_line(d, y, "贸易工具的双线运作")
    y = rule_line(d, y)
    y = gap(d, y, 12)
    y = section_pill(d, y, "FSR（外国补贴条例）")
    y = body_block(d, y, "2023 年 7 月生效。当公共采购合同金额较大（如超过 2.5 亿  ）且企业在过去三年内获得了一定规模的财务资助时，可能需要主动申报。")
    y = gap(d, y, 16)
    y = section_pill(d, y, "近期的实际案例")
    y = gap(d, y, 6)

    cases = [
        "2024.2  保加利亚列车项目（中车参与）  企业主动退出竞标",
        "2024.4  罗马尼亚 110 MW 光伏项目（隆基、上海电气参与）  两家退出",
        "2024.4  中国风电供应商在五国遭遇 Dawn Raids 突袭检查",
        "2024.12 Temu 都柏林办公室  设备被扣押",
    ]
    for c in cases:
        y = bullet_line(d, y, c, gf(36, "body"))

    y = gap(d, y, 16)
    y = section_pill(d, y, "光伏保障措施")
    y = body_block(d, y, "2025 年 6 月 23 日起，欧盟对中国光伏组件实施临时保障措施。欧盟市场约占中国组件出口的 23%（约 65 GW），市场预计短期内可能有一定波动。")

    y = gap(d, y, 14)
    y = rule_line(d, y)
    y = body_block(d, y, "中国商务部于 2025 年 1 月评估认为，FSR 在实践中构成了一定程度的贸易投资壁垒。建议企业密切关注后续发展。", gf(40, "body"))
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_06_FSR光伏关税.png"))
    print("OK pg6")

# ═══════════════════════════════════════
# PAGE 7 — CBAM + CRMA
# ═══════════════════════════════════════
def pg7():
    img, d = make_base()
    page_num(d, 7)
    y = 80
    y = body_line(d, y, "CBAM 与 CRMA", gf(60, "title"))
    y = note_line(d, y, "碳成本与原材料  需要关注的趋势")
    y = rule_line(d, y)
    y = gap(d, y, 12)
    y = section_pill(d, y, "CBAM（碳边境调节机制）")
    y = body_block(d, y, "2026 年 1 月 1 日起正式进入收费阶段。光伏组件本身暂时未被直接纳入，但铝边框、钢支架、玻璃等上游材料已在覆盖范围内。以碳价约   80/吨估算，每 GW 组件可能涉及数百万元的碳成本。")
    y = gap(d, y, 6)
    y = note_line(d, y, "此外，欧洲太阳能制造委员会（ESMC）正在推动将光伏成品纳入 CBAM 范围，值得持续关注。")
    y = gap(d, y, 18)

    y = section_pill(d, y, "CRMA（关键原材料法案）")
    y = body_block(d, y, "受全球供应链结构影响，欧盟在部分关键原材料上对单一来源有较高依赖。例如稀土精炼、锂加工、风电永磁体等领域。CRMA 设定了 2030 年的本土化目标：开采 10%、加工 40%、回收 15%、单一来源不超过 65%。")
    y = gap(d, y, 12)
    y = body_block(d, y, "2025 年底欧盟推出了 RESourceEU（  30 亿资金池）用于关键矿产储备。与此同时，中国在 2025 年也调整了部分稀土及锂电池材料的出口管理。")
    y = gap(d, y, 14)
    y = rule_line(d, y)
    y = body_line(d, y, "供应链的多元化布局正在成为各方的共同选择。", gf(44, "body"))
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_07_CBAM_CRMA.png"))
    print("OK pg7")

# ═══════════════════════════════════════
# PAGE 8 — PCS + 企业布局
# ═══════════════════════════════════════
def pg8():
    img, d = make_base()
    page_num(d, 8)
    y = 80
    y = body_line(d, y, "PCS 融资规则与企业布局", gf(52, "title"))
    y = note_line(d, y, "2026.5 生效   涉及约 62 GWh 订单")
    y = rule_line(d, y)
    y = gap(d, y, 12)
    y = section_pill(d, y, "关于 PCS 的新规")
    y = body_block(d, y, "2026 年 5 月起，EIB（欧洲投资银行）与 EIF（欧洲投资基金）等公共融资渠道，对使用特定来源 PCS（储能变流器）的项目提出了新的限制要求。")
    y = gap(d, y, 18)
    y = section_pill(d, y, "同行们的欧洲步伐")
    y = gap(d, y, 8)

    ents = [
        ("CATL", "匈牙利 + 西班牙", "100 + 50 GWh", "一期 2025 底"),
        ("BYD", "匈牙利（整车）", "50 万辆/年", "电池项目待定"),
        ("EVE", "匈牙利", "28 GWh", "2026 / 2027"),
        ("Gotion", "德国 + 斯洛伐克", "约 20 GWh", "已投产"),
        ("CALB", "葡萄牙", "15 GWh", "2027 / 2028"),
    ]
    for i, (name, loc, cap, status) in enumerate(ents):
        row_h = 46
        stripe = LIGHT_GRAY if i % 2 == 0 else BG_COLOR
        d.rectangle([PADDING, y, W - PADDING_R, y + row_h], fill=stripe)
        nf = gf(36, "title")
        df = gf(32, "body")
        d.text((PADDING + 10, y + 4), name, fill=SOFT_RED, font=nf)
        d.text((PADDING + 150, y + 4), loc, fill=DARK, font=df)
        d.text((PADDING + 390, y + 4), cap, fill=DARK, font=df)
        d.text((PADDING + 600, y + 4), status, fill=GRAY, font=df)
        y += row_h + 4

    y = gap(d, y, 20)
    y = section_pill(d, y, "一些思考")
    y = body_block(d, y, "CATL 已累计投入约 73 亿欧元，但 IAA 框架下未来电芯或也需满足原产地要求，而目前欧盟本土电芯产能仍在起步阶段。欧洲电池企业 Northvolt 于 2025 年 3 月进入破产程序，也给行业格局增添了变数。")
    y = gap(d, y, 10)
    y = note_line(d, y, "机遇与挑战并存，这是一场需要耐心的长跑。")
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_08_PCS限制企业布局.png"))
    print("OK pg8")

# ═══════════════════════════════════════
# PAGE 9 — 五条思路
# ═══════════════════════════════════════
def pg9():
    img, d = make_base()
    page_num(d, 9)
    y = 80
    y = body_line(d, y, "五条可以探索的思路", gf(56, "title"))
    y = note_line(d, y, "策略窗口期：2027 年之前")
    y = rule_line(d, y)
    y = gap(d, y, 18)

    strategies = [
        (" 本地化布局", SOFT_RED, [
            "在匈牙利 / 东欧等区域探索产能布局机会",
            "本地化率可从 30-50% 起步，逐步提升",
            "研究 FTA 缔约国设厂的可能性（视同欧盟原产）",
            "关注豁免条款：成本差异 >25% 可申请",
        ]),
        (" 碳合规先行", (40, 160, 80), [
            "尽早按欧盟 PEF 方法论开展数据收集",
            "重新评估电力采购协议（PPA）的额外性与匹配度",
            "引入区块链溯源系统（如 Catena-X 兼容方案）",
            "主动联系欧盟 CAB 机构进行预审沟通",
        ]),
        (" 知识产权与运营主导权", (60, 100, 190), [
            "探索以财务投资人身份参与，保留关键运营主导权",
            "合资架构下通过协议安排保护核心权益",
            "建立核心技术分级管理机制",
        ]),
        (" 市场多元化", (180, 120, 40), [
            "积极拓展东南亚 / 中东 / 拉美 / 非洲 / 中亚市场",
            "善用一带一路框架下的产能合作机制",
        ]),
        (" 合规前置", (120, 40, 160), [
            "建立全维度风险监测（地缘 / 价格 / 产能 / 交付）",
            "合同中完善法律稳定性、不可抗力与退出条款",
            "供应商协议中加入 ESG 合规附件",
        ]),
    ]

    for title, color, lines in strategies:
        # card with colored left stripe
        card_h = 50 + len(lines) * 44 + 14
        d.rectangle([PADDING, y, W - PADDING_R, y + card_h], fill=LIGHT_GRAY)
        d.rectangle([PADDING, y + 8, PADDING + 6, y + card_h - 8], fill=color)
        tf = gf(44, "title")
        bf = gf(37, "body")
        d.text((PADDING + 20, y + 12), title, fill=color, font=tf)
        ly = y + 56
        for line in lines:
            d.text((PADDING + 20, ly), f"· {line}", fill=DARK, font=bf)
            ly += 44
        y += card_h + 14

    y = gap(d, y, 10)
    y = body_line(d, y, "窗口期可能不会太长。IAA 预计在 2027-2029 年间逐步落地，", gf(40, "body"))
    y = body_line(d, y, "建议在此之前完成关键布局。", gf(40, "body"))
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_09_五条应对策略.png"))
    print("OK pg9")

# ═══════════════════════════════════════
# PAGE 10 — 时间线 + 结语
# ═══════════════════════════════════════
def pg10():
    img, d = make_base()
    page_num(d, 10)
    y = 80
    y = body_line(d, y, "2023-2034 关键时间线", gf(56, "title"))
    y = note_line(d, y, "一图纵览   建议保存")
    y = rule_line(d, y)
    y = gap(d, y, 12)

    tl = [
        ("2023", "FSR 生效 / 电池法规生效 / CBAM 过渡期开始"),
        ("2024", "NZIA + CRMA 通过 / 罗马尼亚光伏项目 FSR 事件"),
        ("2025", "NZIA 实施 / 光伏保障措施 / 中国调整稀土出口管理"),
        ("2026", "CBAM 收费 / IAA 提出 / PCS 新规 / 电池等级标签"),
        ("2027", "数字电池护照上线 / 供应链尽职调查    "),
        ("2028", "最大碳足迹阈值执行 / CBAM 可能扩围"),
        ("2029", "IAA 公共采购原产地要求预计生效    "),
        ("2030", "NZIA 40% 本土制造目标节点"),
        ("2031", "电池再生含量要求生效"),
        ("2034", "CBAM 免费配额预计完全退出"),
    ]

    yf = gf(38, "title")
    df = gf(36, "body")
    for year, desc in tl:
        row_h = 44
        yw = tw(yf, year)
        # year pill
        is_key = "" in desc
        pill_c = SOFT_RED if is_key else LIGHT_GRAY
        txt_c = (255, 255, 255) if is_key else DARK
        d.rectangle([PADDING, y + 2, PADDING + yw + 22, y + row_h - 2], fill=pill_c)
        d.text((PADDING + 10, y + 4), year, fill=txt_c, font=yf)
        d.text((PADDING + yw + 40, y + 4), desc, fill=DARK, font=df)
        y += row_h + 4

    y = gap(d, y, 28)
    d.line([PADDING, y, W - PADDING_R, y], fill=MID_GRAY, width=2)
    y = gap(d, y, 24)

    y = section_pill(d, y, "三点思考")
    y = gap(d, y, 10)
    y = body_line(d, y, "  变化中也有机遇", gf(46, "title"))
    y = body_block(d, y, "与其看作是壁垒，不妨将它理解为一种推动产业链升级与多元化的力量。")
    y = gap(d, y, 14)
    y = body_line(d, y, "  核心在于平衡", gf(46, "title"))
    y = body_block(d, y, "深入欧洲市场需要投入，但关键在于找到「融入」与「守住核心能力」之间的均衡点。")
    y = gap(d, y, 14)
    y = body_line(d, y, "  窗口期值得珍惜", gf(46, "title"))
    y = body_block(d, y, "2027 年前或许是相对从容的布局期，在 IAA 全面落地之前把关键的产能、合规体系搭好，主动权就会在自己手里。")
    y = gap(d, y, 20)
    y = rule_line(d, y)
    y = note_line(d, y, "  感谢阅读。如有具体问题欢迎交流。")
    y = note_line(d, y, "  #欧盟储能政策梳理  #出海思考  #2027窗口期")
    footer(d)
    img.save(os.path.join(OUT_DIR, "page_10_时间线核心结论.png"))
    print("OK pg10")


if __name__ == "__main__":
    pg1(); pg2(); pg3(); pg4(); pg5()
    pg6(); pg7(); pg8(); pg9(); pg10()
    print("Done!", OUT_DIR)