# -*- coding: utf-8 -*-
"""切 5 页王道样本给 markitdown 实测。"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = pymupdf.open(os.path.join(base, '2027计算机网络_高清带书签版.pdf'))
nd = pymupdf.open()
for i in [12, 13, 14, 15, 16]:
    nd.insert_pdf(d, from_page=i, to_page=i)
outp = r'C:\Users\王奕博\AppData\Local\Temp\wd_sample5.pdf'
nd.save(outp)
print('sample saved', nd.page_count, os.path.getsize(outp), 'bytes')
