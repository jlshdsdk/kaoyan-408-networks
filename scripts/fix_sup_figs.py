# -*- coding: utf-8 -*-
"""补充插图第二轮微调（按首轮裁剪结果反推）。"""
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobs = [
    ('ch4-sup.json', 'sup-4-1.png', [12, 52, 90, 87.5]),
    ('ch5-sup.json', 'sup-5-1.png', [8, 53, 94, 92]),
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
