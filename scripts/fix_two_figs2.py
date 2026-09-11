# -*- coding: utf-8 -*-
"""第二轮微调：fig-3-13 / fig-4-6（按首轮裁剪结果反推）。"""
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobs = [
    ('ch3-2.json', 'fig-3-13.png', [13, 49.65, 88, 61.0]),
    ('ch4-2.json', 'fig-4-6.png', [12, 47.4, 82, 65.6]),
]
for fn, out, rect in jobs:
    p = os.path.join(base, 'scripts', 'figcrops', fn)
    d = json.load(open(p, encoding='utf-8'))
    items = d['items'] if isinstance(d, dict) else d
    for c in items:
        if c['out'] == out:
            print(fn, out, c['rect'], '->', rect)
            c['rect'] = rect
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK')
