# -*- coding: utf-8 -*-
"""核验两份 PDF 的书签与每页图片是否实质一致。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

new = r'D:\xwechat_files\wxid_34oeti9hlmso12_ec9e\msg\file\2026-09\2027计算机网络_高清带书签版(1).pdf'
old = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '2027计算机网络_高清带书签版.pdf')

dn, do = pymupdf.open(new), pymupdf.open(old)
tn = [tuple(x) for x in dn.get_toc()]
to = [tuple(x) for x in do.get_toc()]
print('toc identical:', tn == to)

diff_pages = 0
for i in range(dn.page_count):
    inew = [(x['width'], x['height']) for x in dn[i].get_image_info()]
    iold = [(x['width'], x['height']) for x in do[i].get_image_info()]
    if inew != iold:
        diff_pages += 1
        if diff_pages <= 3:
            print(f'page {i+1} differs: {inew[:2]} vs {iold[:2]}')
print('pages with different image layout:', diff_pages, '/', dn.page_count)
