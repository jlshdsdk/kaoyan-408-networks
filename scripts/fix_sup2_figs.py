# -*- coding: utf-8 -*-
"""补图二轮微调：fig-1-1（p014 图题被切半）、sup-6-2（p306 顶部混入正文）。"""
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobs = [
    ('ch1-sup2.json', 'fig-1-1.webp', [26, 32.8, 74, 50.8]),
    ('ch6-sup2.json', 'sup-6-2.webp', [15, 78.6, 85, 88.2]),
]
for fn, out, rect in jobs:
    p = os.path.join(base, 'scripts', 'figcrops', fn)
    d = json.load(open(p, encoding='utf-8'))
    items = d.get('items') if isinstance(d, dict) else d
    for c in items:
        if c['out'] == out:
            print(fn, out, c['rect'], '->', rect)
            c['rect'] = rect
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK')
