# -*- coding: utf-8 -*-
"""静态检查：图片引用存在性、lazy 属性、内部链接。"""
import sys, os, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problems = []
pages = []
for root, dirs, files in os.walk(base):
    dirs[:] = [d for d in dirs if d not in ('pages', 'tools', 'scripts', 'src', '.git', 'assets')]
    for fn in files:
        if fn.endswith('.html'):
            pages.append(os.path.join(root, fn))

for p in sorted(pages):
    relp = os.path.relpath(p, base)
    t = open(p, encoding='utf-8').read()
    imgs = re.findall(r'src="([^"]+\.png)"', t)
    missing = [i for i in imgs if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), i)))]
    nolazy = len(re.findall(r'<img (?![^>]*loading="lazy")[^>]*src="[^"]+\.png"', t))
    # 内部页面链接（排除 http/https/锚点）
    hrefs = re.findall(r'href="([^"]+\.html[^"]*)"', t)
    broken = []
    for h in hrefs:
        path_part = h.split('#')[0]
        if not path_part:
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(p), path_part))):
            broken.append(h)
    status = 'OK'
    if missing:
        status = f'MISSING_IMG {missing}'
        problems.append((relp, status))
    if nolazy:
        status += f' NO_LAZY={nolazy}'
        problems.append((relp, f'img without loading=lazy: {nolazy}'))
    if broken:
        status += f' BROKEN_LINK {broken}'
        problems.append((relp, f'broken links: {broken}'))
    print(f'{relp}: imgs={len(imgs)} {status}')

print(f'TOTAL pages={len(pages)} problems={len(problems)}')
print('LINKCHECK_DONE')
