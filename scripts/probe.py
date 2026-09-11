# -*- coding: utf-8 -*-
"""探测教材 PDF：文字层、每页图片数、图片尺寸分布、印刷页码偏移。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = r'C:\Users\王奕博\Desktop\计算机网络自学网站'
d = pymupdf.open(os.path.join(base, '2027计算机网络_高清带书签版.pdf'))

# 1) 文本层探测：第1章首页 p13（1-based）
for pn in [13, 14, 50]:
    page = d[pn-1]
    txt = page.get_text().strip()
    print(f'--- PDF p{pn} text len={len(txt)} first 120 chars:')
    print(repr(txt[:120]))

# 2) 图片统计：前 60 页每页内嵌图数量与尺寸
total_imgs = 0
print('--- per-page image counts (p13..p42):')
for pn in range(13, 43):
    page = d[pn-1]
    infos = page.get_image_info()
    big = [i for i in infos if i['width'] >= 300 and i['height'] >= 200]
    total_imgs += len(infos)
    if infos:
        sizes = [(i['width'], i['height']) for i in infos]
        print(f'p{pn}: {len(infos)} imgs ({len(big)} big) {sizes[:6]}')
print('total images first 30 chapter pages:', total_imgs)

# 3) 矢量绘图探测（判断是否扫描版）
for pn in [13, 30]:
    page = d[pn-1]
    dr = page.get_drawings()
    print(f'p{pn} vector drawing paths: {len(dr)}')

# 4) 印刷页码：看页脚文本是否含数字页码
for pn in [13, 14, 100]:
    page = d[pn-1]
    words = page.get_text('words')
    if words:
        h = page.rect.height
        footer = [w[4] for w in words if w[1] > h - 60]
        header = [w[4] for w in words if w[3] < 60]
        print(f'p{pn} header={header[:8]} footer={footer[:8]}')
d.close()
print('DONE')
