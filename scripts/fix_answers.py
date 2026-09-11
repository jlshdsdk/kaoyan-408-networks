# -*- coding: utf-8 -*-
"""修正 answers.json 两处转录错误（主代理已对照答案速查扫描图逐字核实）：
1. "4.2"：应为 72 项（转录版丢 2 项导致假错位）
2. "6.3"："AAAC" 实为 4 道连续单选（无括号），拆为 A/A/A/C
"""
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(base, 'scripts', 'answers.json')
d = json.load(open(p, encoding='utf-8'))

old42 = d['4.2']['answers']
print('old 4.2 count:', len(old42))

new42 = list("CBCBD") + list("DADDB") + list("CBAAA") + list("DBCCA") + list("CACAD") + \
    ["B", "DA", "B", "C", "D"] + list("BCDBA") + list("CABDC") + list("AABCB") + \
    list("CDACB") + list("CCDDA") + list("BCCDC") + list("ACDBB") + list("BBDAB") + ["D", "C"]
assert len(new42) == 72, len(new42)
d['4.2']['answers'] = new42

old63 = d['6.3']['answers']
print('old 6.3:', old63)
new63 = []
for item in old63:
    if item == 'AAAC':
        new63 += ['A', 'A', 'A', 'C']
    else:
        new63.append(item)
print('new 6.3 count:', len(new63))
d['6.3']['answers'] = new63

d['_meta']['fix_note'] = '4.2 已按答案速查扫描图逐字重核（72 项）；6.3 的 AAAC 拆为 4 道单选。主代理核定。'
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('FIXED answers.json')
for k, v in d.items():
    if k == '_meta':
        continue
    print(k, len(v['answers']))
