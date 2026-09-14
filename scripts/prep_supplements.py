# -*- coding: utf-8 -*-
"""补充资料素材准备：
1) biji/gaojun 整页渲染 PNG → pages/biji/、pages/gaojun/（供视觉工匠与裁剪）
2) biji 文字按章切分 → scripts/biji_txt/chN.txt（带页码标记）
"""
import sys, os, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1) 页面渲染（灰度 1.6x 足够阅读+裁剪，控制体积）
for name in ['biji', 'gaojun']:
    outdir = os.path.join(base, 'pages', name)
    os.makedirs(outdir, exist_ok=True)
    d = pymupdf.open(os.path.join(base, 'pages_src', f'{name}.pdf'))
    n = 0
    for i in range(d.page_count):
        outp = os.path.join(outdir, f'p{i+1:03d}.png')
        if os.path.exists(outp):
            n += 1
            continue
        pix = d[i].get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), colorspace=pymupdf.csGRAY)
        pix.save(outp)
        n += 1
    print(f'{name}: {n} pages rendered')
    d.close()

# 2) biji 文字按章切分
d = pymupdf.open(os.path.join(base, 'pages_src', 'biji.pdf'))
ch_re = re.compile(r'第\s*([1-7一二三四五六七])\s*章')
num_map = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
           '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7}
bounds = []  # (chapter_num, page1based, title_line)
for i in range(d.page_count):
    t = d[i].get_text()
    for line in t.split('\n'):
        line = line.strip()
        m = ch_re.search(line)
        if m and len(line) <= 30:
            bounds.append((num_map[m.group(1)], i + 1, line))
            break
print('chapter markers found:', bounds)
d.close()
