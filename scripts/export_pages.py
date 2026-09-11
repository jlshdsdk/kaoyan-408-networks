# -*- coding: utf-8 -*-
"""把三个 PDF 的每一页导出为 PNG（直接抽取内嵌整页图，无损且快）。
输出：
  pages/textbook/p001.png ... p316.png
  pages/choice/p001.png ... p145.png     (选择题做题本【留空】.pdf)
  pages/comp/p001.png ... p056.png       (综合题做题本)
  pages/answer/p001.png ... p002.png     (答案速查)
"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = r'C:\Users\王奕博\Desktop\计算机网络自学网站'
jobs = [
    ('2027计算机网络_高清带书签版.pdf', 'textbook'),
    ('【留空】.pdf', 'choice'),
    ('27王道《计网》综合题做题本【留空】3.16.pdf', 'comp'),
    ('27王道《计网》选择题【答案速查】.pdf', 'answer'),
]

for pdf, outdir in jobs:
    out = os.path.join(base, 'pages', outdir)
    os.makedirs(out, exist_ok=True)
    d = pymupdf.open(os.path.join(base, pdf))
    n_ok = 0
    for i in range(d.page_count):
        outp = os.path.join(out, f'p{i+1:03d}.png')
        if os.path.exists(outp):
            n_ok += 1
            continue
        page = d[i]
        infos = page.get_image_info()
        saved = False
        if infos:
            # 取最大内嵌图直接抽取（扫描版=整页图）
            best = max(infos, key=lambda x: x['width'] * x['height'])
            xref = best['xref'] if 'xref' in best else 0
            try:
                pix = pymupdf.Pixmap(d, xref)
                if pix.n - pix.alpha > 3:
                    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
                pix.save(outp)
                saved = True
            except Exception:
                saved = False
        if not saved:
            # 兜底：按页面渲染（2x）
            pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
            pix.save(outp)
        n_ok += 1
    print(f'{outdir}: {n_ok} pages exported')
    d.close()
print('ALL_DONE')
