# -*- coding: utf-8 -*-
"""biji 文字按章切分（带页码标记）→ scripts/biji_txt/chN.txt"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bounds = [(1, 5, 25), (2, 26, 40), (3, 41, 126), (4, 127, 254), (5, 255, 299), (6, 300, 331)]
d = pymupdf.open(os.path.join(base, 'pages_src', 'biji.pdf'))
outdir = os.path.join(base, 'scripts', 'biji_txt')
os.makedirs(outdir, exist_ok=True)
for ch, p0, p1 in bounds:
    parts = []
    for i in range(p0, p1 + 1):
        t = d[i-1].get_text().strip()
        if t:
            parts.append(f'--- p{i} ---\n{t}')
    outp = os.path.join(outdir, f'ch{ch}.txt')
    with open(outp, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(parts))
    print(f'ch{ch}.txt: pages {p0}-{p1}, {sum(len(p) for p in parts)} chars')
d.close()
print('DONE')
