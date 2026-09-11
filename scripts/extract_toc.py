# -*- coding: utf-8 -*-
"""提取教材与做题本的书签 TOC，保存为文件。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = r'C:\Users\王奕博\Desktop\计算机网络自学网站'
out = os.path.join(base, 'scripts')

jobs = [
    ('2027计算机网络_高清带书签版.pdf', 'toc_textbook.txt'),
    ('【留空】.pdf', 'toc_choice_quizbook.txt'),
    ('27王道《计网》综合题做题本【留空】3.16.pdf', 'toc_comprehensive_quizbook.txt'),
]
for pdf, txt in jobs:
    d = pymupdf.open(os.path.join(base, pdf))
    lines = []
    for lvl, title, page in d.get_toc():
        lines.append(f'{"  "*(lvl-1)}[L{lvl}] p{page}  {title}')
    with open(os.path.join(out, txt), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'{txt}: {len(lines)} lines')
    d.close()
print('DONE')
