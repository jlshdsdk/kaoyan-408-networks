# -*- coding: utf-8 -*-
"""放大答案速查 p2 的 4.2 行，存为两张横条图供精读。"""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from PIL import Image

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im = Image.open(os.path.join(base, 'pages', 'answer', 'p002.png'))
W, H = im.size
print('size', W, H)
# 4.2 答案两行大约在页面高度 11%-17% 区间
top = im.crop((0, int(0.10*H), W, int(0.145*H))).resize((W*2, int(0.045*H)*2), Image.LANCZOS)
top.save(os.path.join(base, 'scripts', '_ans42_line1.png'))
bot = im.crop((0, int(0.135*H), W, int(0.175*H))).resize((W*2, int(0.04*H)*2), Image.LANCZOS)
bot.save(os.path.join(base, 'scripts', '_ans42_line2.png'))
print('SAVED')
