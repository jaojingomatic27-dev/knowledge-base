# -*- coding: utf-8 -*-
"""Minimal test: is Pillow Chinese rendering broken or was it the inline encoding?"""
from PIL import Image, ImageDraw, ImageFont

f = r"C:\Windows\Fonts\msyhbd.ttc"
font = ImageFont.truetype(f, 60)

img = Image.new("RGB", (800, 200), "white")
d = ImageDraw.Draw(img)
d.text((50, 50), "测试中文 ABC 123", fill="black", font=font)
img.save(r"C:\AI\cc\pvinverter\output\_zh_test.png")
print("OK - open the file to verify")
