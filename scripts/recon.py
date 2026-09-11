# -*- coding: utf-8 -*-
"""侦察：确认 PDF 文件名/页数/书签数。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = r'C:\Users\王奕博\Desktop\计算机网络自学网站'
for f in sorted(os.listdir(base)):
    if f.lower().endswith('.pdf'):
        p = os.path.join(base, f)
        d = pymupdf.open(p)
        print(f'FILE: {f} | pages={d.page_count} | toc_entries={len(d.get_toc())} | size={os.path.getsize(p)//1024//1024}MB')
        d.close()
print('DONE')
