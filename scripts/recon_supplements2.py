# -*- coding: utf-8 -*-
"""深入分析两本补充资料：高军书签全量 + 笔记版文字/图片分布。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = r'C:\Users\王奕博\Desktop\计算机网络自学网站'

# 1) 高军书签全量
d = pymupdf.open(os.path.join(base, 'pages_src', 'gaojun.pdf'))
lines = [f'{"  "*(lvl-1)}[L{lvl}] p{page}  {title}' for lvl, title, page in d.get_toc()]
with open(os.path.join(base, 'scripts', 'toc_gaojun.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'gaojun toc: {len(lines)} lines -> scripts/toc_gaojun.txt')
d.close()

# 2) 笔记版：每页文字量 + 内嵌图片尺寸分布
d = pymupdf.open(os.path.join(base, 'pages_src', 'biji.pdf'))
total_chars = 0
textful = 0
imgful = 0
for i in range(d.page_count):
    t = d[i].get_text().strip()
    total_chars += len(t)
    if len(t) >= 100:
        textful += 1
    infos = d[i].get_image_info()
    if any(x['width'] >= 500 and x['height'] >= 400 for x in infos):
        imgful += 1
print(f'biji: pages={d.page_count} total_chars={total_chars} textful_pages(>=100chars)={textful} imageful_pages={imgful}')
d.close()
print('DONE')
