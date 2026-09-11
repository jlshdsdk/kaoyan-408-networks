# -*- coding: utf-8 -*-
"""主代理亲核两图精确 rect：fig-3-13(p78)、fig-4-6(p151)。"""
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobs = [
    ('ch3-2.json', 'fig-3-13.png', [13, 47.9, 88, 60.3]),
    ('ch4-2.json', 'fig-4-6.png', [12, 46.0, 80, 64.6]),
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
