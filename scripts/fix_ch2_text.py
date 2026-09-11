# -*- coding: utf-8 -*-
"""ch2 审查后的文字小修。"""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fixes = [
    (r'src\ch2\index.frag.html', '码元比转数', '码元比特数'),
    (r'src\ch2\2.1.frag.html', '码元比转数', '码元比特数'),
    (r'src\ch2\2.1.frag.html', 'P30–P37', 'P30–P35'),
    (r'src\ch2\2.2.frag.html', '衰减的小', '衰减小'),
    (r'src\ch2\quiz.frag.html', '≈260Mb/s', '≈266Mb/s'),
]
for rel, old, new in fixes:
    p = os.path.join(base, rel)
    t = open(p, encoding='utf-8').read()
    n = t.count(old)
    t = t.replace(old, new)
    open(p, 'w', encoding='utf-8').write(t)
    print(rel, repr(old), '->', n, 'replaced')
