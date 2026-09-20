# -*- coding: utf-8 -*-
"""资源审计 v2：解析构建产物引用的本地资源，按页面目录解析后逐个验证存在性。"""
import sys, os, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pages = ['index.html', 'ch1/recall.html', 'ch4/quiz.html', 'ch1/1.2.html', 'ch6/6.5.html']
refs = {}
for pg in pages:
    pdir = os.path.dirname(pg)
    t = open(os.path.join(base, pg), encoding='utf-8').read()
    for m in re.finditer(r'(?:src|href)="([^"]+)"', t):
        u = m.group(1).split('#')[0].split('?')[0]
        if not u or u.startswith(('http', 'mailto')):
            continue
        if u.endswith('.html'):
            continue  # 链接由 linkcheck 负责
        refs.setdefault(os.path.normpath(os.path.join(pdir, u)), []).append(pg)

bad = []
for r, used in sorted(refs.items()):
    if not os.path.exists(os.path.join(base, *r.split('/'))):
        bad.append((r, used[:2]))
print(f'asset refs from {len(pages)} pages: {len(refs)}')
if bad:
    print('MISSING:')
    for r, u in bad:
        print(' ', r, '<-', u)
else:
    print('RESOURCE_AUDIT_PASS')
