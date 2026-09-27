# -*- coding: utf-8 -*-
"""PNG → WebP 批量转换 + 全站引用改写。
1. assets/chN/*.png → .webp（quality 82）
2. src/**/*.frag.html 中 assets/chN/xxx.png 引用 → .webp
3. scripts/figcrops/*.json 的 out 字段 .png → .webp
4. 转换成功后删除 assets 下的 PNG（原始整页扫描仍在 pages/ 不受影响）
"""
import sys, os, io, re, glob, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from PIL import Image

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1) 转换
converted = 0
saved_bytes = 0
for png in glob.glob(os.path.join(base, 'assets', 'ch*', '*.png')):
    webp = png[:-4] + '.webp'
    im = Image.open(png)
    if im.mode not in ('RGB', 'L'):
        im = im.convert('RGB')
    im.save(webp, 'WEBP', quality=82, method=4)
    saved_bytes += os.path.getsize(png) - os.path.getsize(webp)
    converted += 1
print(f'converted {converted} png -> webp, saved {saved_bytes//1024}KB')

# 2) 改写片段引用
frag_alter = 0
for frag in glob.glob(os.path.join(base, 'src', '**', '*.frag.html'), recursive=True):
    t = open(frag, encoding='utf-8').read()
    t2 = re.sub(r'(assets/ch\d+/[^"?\s]+)\.png', r'\1.webp', t)
    if t2 != t:
        open(frag, 'w', encoding='utf-8').write(t2)
        frag_alter += 1
print(f'fragments rewritten: {frag_alter}')

# 3) 同步裁剪清单 out 字段
for j in glob.glob(os.path.join(base, 'scripts', 'figcrops', '*.json')):
    d = json.load(open(j, encoding='utf-8'))
    items = d.get('items') if isinstance(d, dict) else d
    if not isinstance(items, list):
        continue
    n = 0
    for c in items:
        if isinstance(c, dict) and c.get('out', '').endswith('.png'):
            c['out'] = c['out'][:-4] + '.webp'
            n += 1
    if n:
        json.dump(d, open(j, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{os.path.basename(j)}: {n} out fields -> webp')

# 4) 删除已转换 PNG
removed = 0
for png in glob.glob(os.path.join(base, 'assets', 'ch*', '*.png')):
    os.remove(png)
    removed += 1
print(f'removed {removed} png files')
print('WEBP_DONE')
