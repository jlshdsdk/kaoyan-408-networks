# -*- coding: utf-8 -*-
"""ch2-quiz.json 的 rect 是 [x,y,w,h]，转成 [x0,y0,x1,y1]。"""
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(base, 'scripts', 'figcrops', 'ch2-quiz.json')
d = json.load(open(p, encoding='utf-8'))
items = d['items'] if isinstance(d, dict) else d
for c in items:
    x0, y0, a, b = c['rect']
    c['rect'] = [x0, y0, x0 + a, y0 + b]
    print(c['out'], '->', c['rect'])
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('FIXED')
