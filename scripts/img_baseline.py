# -*- coding: utf-8 -*-
"""站点图片体积基线 + WebP 转换收益预估。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from PIL import Image

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
total = 0
count = 0
biggest = []
for root, dirs, files in os.walk(os.path.join(base, 'assets')):
    dirs[:] = [d for d in dirs if d != 'katex']
    for f in files:
        if f.endswith('.png'):
            p = os.path.join(root, f)
            sz = os.path.getsize(p)
            total += sz
            count += 1
            biggest.append((sz, os.path.relpath(p, base)))
biggest.sort(reverse=True)
print(f'png count={count} total={total//1024}KB avg={total//max(1,count)//1024}KB')
print('top5:')
for sz, p in biggest[:5]:
    print(f'  {sz//1024}KB {p}')

# 抽 3 张估 WebP 收益
sample = [p for _, p in biggest[:3]]
est_png = est_webp = 0
for p in sample:
    full = os.path.join(base, p)
    im = Image.open(full).convert('RGB')
    tmp = os.path.join(base, 'scripts', '_tmp.webp')
    im.save(tmp, 'WEBP', quality=82, method=4)
    est_png += os.path.getsize(full)
    est_webp += os.path.getsize(tmp)
    os.remove(tmp)
print(f'sample3: png={est_png//1024}KB webp_est={est_webp//1024}KB ratio={est_png/max(1,est_webp):.1f}x')
