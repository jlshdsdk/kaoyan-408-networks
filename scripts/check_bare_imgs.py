# -*- coding: utf-8 -*-
"""检查片段中 img 是否被 figure 包裹（往前最近的 figure 标签是开还是闭）。"""
import sys, os, io, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

for p in glob.glob('src/**/*.frag.html', recursive=True):
    t = open(p, encoding='utf-8').read()
    for m in re.finditer(r'<img[^>]*>', t):
        before = t[:m.start()]
        last_open = before.rfind('<figure')
        last_close = before.rfind('</figure>')
        # 最近的是开标签且没有紧随的闭标签 → 在 figure 内
        inside = last_open > last_close
        if not inside:
            src = re.search(r'src="([^"]+)"', m.group(0))
            # 找它前面最近的包裹标签
            ctx = re.findall(r'<(\w+)[^>]{0,80}>', before[-200:])
            print(f'{p}: BARE img {src.group(1) if src else "?"} ctx_tags={ctx[-4:]}')
print('SCAN_DONE')
