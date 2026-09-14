# -*- coding: utf-8 -*-
"""补充插图第三轮微调。"""
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jobs = [
    ('ch4-sup.json', 'sup-4-1.png', [12, 54.5, 90, 82.5]),
    ('ch2-sup.json', 'sup-2-1.png', [5, 42.5, 96, 57]),
    ('ch6-sup.json', 'sup-6-1.png', [4, 49.5, 96, 92]),
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
