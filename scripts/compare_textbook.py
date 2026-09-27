# -*- coding: utf-8 -*-
"""对比用户新发 PDF 与工作区教材：哈希/页数/书签差异。"""
import sys, os, io, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

new = r'D:\xwechat_files\wxid_34oeti9hlmso12_ec9e\msg\file\2026-09\2027计算机网络_高清带书签版(1).pdf'
old = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '2027计算机网络_高清带书签版.pdf')

for p in [new, old]:
    if not os.path.exists(p):
        print('MISSING:', p)
        continue
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    d = pymupdf.open(p)
    print(os.path.basename(p))
    print('  size:', os.path.getsize(p) // 1024 // 1024, 'MB | md5:', h.hexdigest()[:12],
          '| pages:', d.page_count, '| toc:', len(d.get_toc()))
    d.close()
