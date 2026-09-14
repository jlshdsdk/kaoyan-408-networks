# -*- coding: utf-8 -*-
"""侦察用户新提供的两本补充资料 PDF。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

files = [
    r'D:\xwechat_files\wxid_34oeti9hlmso12_ec9e\msg\file\2026-09\深入浅出计算机网络（笔记）.pdf',
    r'D:\xwechat_files\wxid_34oeti9hlmso12_ec9e\msg\file\2026-09\深入浅出计算机网络（高军）.pdf',
]
for p in files:
    print('=' * 60)
    print(os.path.basename(p))
    if not os.path.exists(p):
        print('  !! NOT FOUND')
        continue
    print(f'  size: {os.path.getsize(p)//1024//1024}MB')
    d = pymupdf.open(p)
    print(f'  pages: {d.page_count}, toc entries: {len(d.get_toc())}')
    # 文本层探测
    for pn in [1, min(10, d.page_count), min(50, d.page_count)]:
        t = d[pn-1].get_text().strip()
        print(f'  p{pn}: textlen={len(t)} head={repr(t[:60])}')
    d.close()
print('DONE')
