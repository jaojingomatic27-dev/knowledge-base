# -*- coding: utf-8 -*-
"""Generate 5 Xiaohongshu cover images"""

from PIL import Image, ImageDraw, ImageFont
import os

OUT = r"C:\AI\cc\pvinverter\output\covers"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1440

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttf"
FONT_REG  = r"C:\Windows\Fonts\msyh.ttf"

def ff(size, bold=False):
    p = FONT_BOLD if bold else FONT_REG
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()

TITLE = "欧盟对中国储能动手了\n比关税狠100倍"
SUBTITLE = "2026 七重政策壁垒 · 全拆解"
TAG = "#储能出海 #欧盟政策 #新能源"

# ===== Style 1: Real battle (laofanshu) =====
def s1():
    img = Image.new("RGB", (W, H), "#1a1a2e")
    d = ImageDraw.Draw(img)
    for i in range(0, H, 2):
        a = 255 - int((i/H)*60)
        d.line([(0,i),(W,i)], fill=(a,a+10,a+25))
    for x in [20,28]:
        d.rectangle([x,0,x+3,H], fill="#e74c3c")
    d.rectangle([60,80,260,150], fill="#e74c3c")
    d.text((160,115), "一线实录", fill="white", font=ff(36,True), anchor="mm")
    y = 240
    for ln in TITLE.split("\n"):
        d.text((W//2+4,y+4), ln, fill="#e74c3c", font=ff(80,True), anchor="ma")
        d.text((W//2,y), ln, fill="white", font=ff(80,True), anchor="ma")
        y += 110
    d.line([(W//2-200,y+30),(W//2+200,y+30)], fill="#e74c3c", width=4)
    pts = ["不是加点税那么简单","是七重政策壁垒一起上","不在欧洲建厂 = 丢标","在欧洲建厂 = 可能丢技术"]
    y += 80
    for p in pts:
        d.text((150,y), p, fill="#cccccc", font=ff(32))
        y += 58
    d.text((W//2,H-100), "来源：欧盟官方公报 + 行业一线调研", fill="#888", font=ff(26), anchor="ma")
    d.text((W//2,H-60), TAG, fill="#666", font=ff(22), anchor="ma")
    img.save(os.path.join(OUT, "1_一线实战_海外储能老番薯风.png"))
    print("1 done")

# ===== Style 2: Emotion hook (xiaozhitiao) =====
def s2():
    img = Image.new("RGB", (W, H), "#0a0a0a")
    d = ImageDraw.Draw(img)
    for i in range(H//3):
        r = 180 - int((i/(H//3))*100)
        d.rectangle([0,i,W,i+1], fill=(r,20,20))
    y = 200
    for ln in TITLE.split("\n"):
        for dx,dy in [(4,4),(-2,-2),(2,-2)]:
            d.text((W//2+dx,y+dy), ln, fill="#ff4444", font=ff(88,True), anchor="ma")
        d.text((W//2,y), ln, fill="white", font=ff(88,True), anchor="ma")
        y += 120
    d.rectangle([0,y+30,W,y+100], fill="#ffcc00")
    d.text((W//2,y+65), "2027年之前必须知道", fill="black", font=ff(40,True), anchor="ma")
    y += 180
    d.text((W//2-130,y), "7", fill="#ff4444", font=ff(110,True), anchor="ma")
    d.text((W//2+130,y), "重", fill="white", font=ff(65,True), anchor="ma")
    d.text((W//2,y+80), "NZIA IAA CBAM FSR 电池法规 CRMA PCS限制", fill="#aaa", font=ff(28), anchor="ma")
    y += 170
    d.rectangle([W//2-200,y-35,W//2+200,y+45], fill="#1a1a1a", outline="#ff4444", width=2)
    d.text((W//2,y+5), "90%的储能出海企业还没意识到", fill="#ff6666", font=ff(32,True), anchor="ma")
    d.text((W//2,H-100), "先收藏 刷走了找不回来", fill="#888", font=ff(26), anchor="ma")
    d.text((W//2,H-60), TAG, fill="#555", font=ff(22), anchor="ma")
    img.save(os.path.join(OUT, "2_情绪钩子_商业小纸条风.png"))
    print("2 done")

# ===== Style 3: Structured knowledge (Freddy) =====
def s3():
    img = Image.new("RGB", (W, H), "#0d1117")
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,120], fill="#161b22")
    d.line([(0,120),(W,120)], fill="#30363d", width=2)
    d.text((W//2,60), "一张图看懂 欧盟对中国储能七重壁垒", fill="#58a6ff", font=ff(30,True), anchor="ma")
    d.text((W//2,190), "欧盟对中国储能动手了", fill="white", font=ff(58,True), anchor="ma")
    d.text((W//2,265), "比关税狠100倍", fill="#ff7b72", font=ff(64,True), anchor="ma")
    tags = [("NZIA","#58a6ff"),("IAA","#ff7b72"),("BATT","#8b5cf6"),("FSR","#e8a840"),("CBAM","#4caf84"),("CRMA","#38bdf8"),("PCS","#a78bfa")]
    for i,(nm,cl) in enumerate(tags):
        x = 70 + i*138
        d.rectangle([x,350,x+128,400], fill=cl)
        d.text((x+64,375), nm, fill="white", font=ff(24,True), anchor="ma")
    rows = [
        ("NZIA 净零工业法案","2025.7","5","公共采购排除中国产品"),
        ("IAA 工业加速器法案","2026.3","5","欧洲制造原产地+强制技术转让"),
        ("电池法规 2023/1542","2023-28","4","碳足迹/数字护照/超标禁售"),
        ("FSR 外国补贴条例","2023.7","4","调查中企不公平补贴"),
        ("CBAM 碳边境调节","2026.1","4","碳成本内部化"),
        ("CRMA 关键原材料","2024.4","4","去中国化供应链"),
        ("PCS 公共资金限制","2026.5","3","排除中国PCS融资"),
    ]
    col_x = [70, 340, 490, 590]
    col_w = [260, 140, 90, 440]
    yt = 460
    d.rectangle([70,yt,1010,yt+54], fill="#21262d")
    for j,hdr in enumerate(["法案","生效","影响","核心"]):
        d.text((col_x[j]+col_w[j]//2,yt+27), hdr, fill="#8b949e", font=ff(24,True), anchor="ma")
    d.line([(70,yt+54),(1010,yt+54)], fill="#30363d", width=1)
    for i,(nm,dt,st,co) in enumerate(rows):
        ry = yt+54+i*80
        if i%2==1:
            d.rectangle([70,ry,1010,ry+80], fill="#161b22")
        d.line([(70,ry+80),(1010,ry+80)], fill="#21262d", width=1)
        d.text((col_x[0]+14,ry+40), nm, fill="#e6edf3", font=ff(24), anchor="lm")
        d.text((col_x[1]+col_w[1]//2,ry+40), dt, fill="#8b949e", font=ff(24), anchor="ma")
        stars = "".join(["★"]*int(st))
        d.text((col_x[2]+col_w[2]//2,ry+40), stars, fill="#f0c040", font=ff(20), anchor="ma")
        d.text((col_x[3]+14,ry+40), co, fill="#c9d1d9", font=ff(24), anchor="lm")
    yc = yt+54+7*80+50
    d.rectangle([70,yc,1010,yc+90], fill="#1a1a2e", outline="#ff7b72", width=2)
    d.text((W//2,yc+28), "战略窗口期：2027年前完成欧洲产能+碳合规布局", fill="#ff7b72", font=ff(30,True), anchor="ma")
    d.text((W//2,yc+60), "不入欧 失标  |  入欧 可能失技术", fill="#ffcccc", font=ff(26), anchor="ma")
    d.text((W//2,H-50), TAG, fill="#555", font=ff(24), anchor="ma")
    img.save(os.path.join(OUT, "3_结构化知识_Freddy商业笔记风.png"))
    print("3 done")

# ===== Style 4: Checklist (laochuanzhang) =====
def s4():
    img = Image.new("RGB", (W, H), "#0f1a2e")
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,100], fill="#1a2d47")
    d.text((W//2,50), "出海老船长 · 避坑清单", fill="#7eb8da", font=ff(32,True), anchor="ma")
    y = 170
    d.text((W//2,y), "欧盟对中国储能动手了", fill="white", font=ff(58,True), anchor="ma")
    y += 75
    d.text((W//2,y), "比关税狠100倍  2026出海必看", fill="#f4a261", font=ff(44,True), anchor="ma")
    y += 50
    d.line([(100,y),(W-100,y)], fill="#264653", width=3)
    y += 60
    cl = [
        ("坑1","还在打价格战？","NZIA要求30%拍卖看非价格标准"),
        ("坑2","以为欧洲认证就够了？","IAA要求电芯+BMS欧盟原产"),
        ("坑3","在匈牙利建了组装厂？","IAA第3年电芯也必须本土造"),
        ("坑4","拿了中国补贴没申报？","FSR调查-全部中企被针对"),
        ("坑5","碳足迹数据用国内标准？","欧盟不认中国绿证！可能被禁售"),
        ("坑6","储能PCS还在用国产？","EIB公共融资直接排除中国PCS"),
        ("坑7","核心技术还在国内？","IAA要求强制向欧盟实体授权IP"),
    ]
    for i,(tg,tl,ds) in enumerate(cl):
        cx = 110
        d.ellipse([cx-26,y+18,cx+26,y+70], fill="#e76f51")
        d.text((cx,y+44), str(i+1), fill="white", font=ff(22,True), anchor="ma")
        d.text((160,y), tl, fill="#e9c46a", font=ff(38,True))
        d.text((160,y+42), ds, fill="#aaaaaa", font=ff(26))
        y += 105
    y += 30
    d.rectangle([80,y,W-80,y+60], fill="#264653")
    d.text((W//2,y+30), "你踩过哪个坑？评论区接龙！", fill="#e9c46a", font=ff(32,True), anchor="ma")
    d.text((W//2,H-60), TAG, fill="#555", font=ff(24), anchor="ma")
    img.save(os.path.join(OUT, "4_避坑清单_出海老船长风.png"))
    print("4 done")

# ===== Style 5: News flash (36kr) =====
def s5():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0,0,W,80], fill="#c41230")
    d.text((W//2,40), "BREAKING  快报", fill="white", font=ff(36,True), anchor="ma")
    d.text((W//2,140), "2026.06.06  布鲁塞尔", fill="#999", font=ff(24), anchor="ma")
    d.line([(W//2-160,165),(W//2+160,165)], fill="#ddd", width=1)
    y = 210
    for ln in TITLE.split("\n"):
        d.text((W//2,y), ln, fill="#1a1a1a", font=ff(62,True), anchor="ma")
        y += 85
    d.text((W//2,y+30), "欧盟七重政策壁垒全面拆解", fill="#666", font=ff(30), anchor="ma")
    y += 110
    d.rectangle([80,y,W-80,y+340], fill="#f8f8f8", outline="#e0e0e0", width=1)
    ss = [
        "NZIA: 2025.12 非价格标准生效，中国储能组件受限",
        "IAA: 六选四审查 + 强制技术转让",
        "电池法规: 2027电池护照，2028碳超标禁售",
        "CBAM: 2026.1 正式收费，碳关税 600-1000万元/GW",
        "FSR: 三起深入调查全部针对中国企业",
        "CRMA: 2030 本土加工40%，单一来源<=65%",
        "PCS: 2026.5 中国储能变流器不得获EIB融资",
    ]
    sy = y+30
    for s in ss:
        d.text((120,sy), s, fill="#333", font=ff(28))
        sy += 42
    y += 380
    d.text((W//2,y), "来源：欧盟委员会公报 中国商务部 行业调研", fill="#aaa", font=ff(24), anchor="ma")
    d.text((W//2,y+35), "全文分析  关注获取", fill="#c41230", font=ff(28,True), anchor="ma")
    d.rectangle([0,H-70,W,H], fill="#f0f0f0")
    d.text((W//2,H-35), TAG, fill="#999", font=ff(24), anchor="ma")
    img.save(os.path.join(OUT, "5_资讯快报_36氪风.png"))
    print("5 done")

s1(); s2(); s3(); s4(); s5()
print("DONE -> " + OUT)