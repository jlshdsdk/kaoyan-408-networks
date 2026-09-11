# -*- coding: utf-8 -*-
"""探测做题本与答案速查的扫描/文字属性。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = r'C:\Users\王奕博\Desktop\计算机网络自学网站'
for name in ['【留空】.pdf', '27王道《计网》综合题做题本【留空】3.16.pdf', '27王道《计网》选择题【答案速查】.pdf']:
    d = pymupdf.open(os.path.join(base, name))
    print(f'=== {name} ({d.page_count}p)')
    for pn in [1, 2, min(5, d.page_count)]:
        page = d[pn-1]
        txt = page.get_text().strip()
        infos = page.get_image_info()
        dr = page.get_drawings()
        print(f'  p{pn}: textlen={len(txt)} imgs={len(infos)} vec={len(dr)} imgsizes={[(i["width"],i["height"]) for i in infos[:3]]}')
        if txt:
            print(f'    text head: {repr(txt[:80])}')
    d.close()
print('DONE')
