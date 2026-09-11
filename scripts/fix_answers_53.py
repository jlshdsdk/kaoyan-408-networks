# -*- coding: utf-8 -*-
"""修复 answers.json 5.3：第31-55项组内错位（速查页逐字核实），61 项为 B。"""
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(base, 'scripts', 'answers.json')
d = json.load(open(p, encoding='utf-8'))
a = d['5.3']['answers']
print('before', len(a))
correct = list('CCDDC') + list('BDBCB') + list('CACDA') + ['C', 'C', 'AC', 'D', 'C'] + \
    list('BCBDC') + list('CCCCC') + list('CACBD') + list('CDABB') + list('DCACB') + \
    list('BAAAC') + list('DDCBD') + list('CCDDA') + ['B']
assert len(correct) == 61, len(correct)
d['5.3']['answers'] = correct
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('after', len(correct))
diff = [(i+1, old, new) for i, (old, new) in enumerate(zip(a, correct)) if old != new]
print('changed positions:', diff[:30])
