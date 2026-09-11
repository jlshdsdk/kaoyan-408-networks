# -*- coding: utf-8 -*-
"""按裁剪清单从整页扫描图裁出插图 → assets/chN/
清单：scripts/figcrops/chN*.json（如 ch1.json、ch1-quiz.json）
  [{"page":15, "rect":[8,20,92,55], "out":"fig-1-2.png", "caption":"图1.2 电路交换示意图",
    "src":"教材P3", "book":"textbook"}]
rect 为相对页面百分比 [x0,y0,x1,y1]（原点左上，0-100）。
book 可选：textbook（默认）| choice | comp —— 决定从哪本 PDF 的页面图裁剪。
输出文件额外写一份 manifest：assets/chN/_figs.json（含 caption，页面可选用）。
"""
import sys, os, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from PIL import Image

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGEDIRS = {'textbook': 'textbook', 'choice': 'choice', 'comp': 'comp'}

figdir = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].startswith('--ch') else None

total = 0
for fn in sorted(os.listdir(os.path.join(base, 'scripts', 'figcrops'))):
    if not fn.endswith('.json'):
        continue
    chname = fn.split('.')[0].split('-')[0]  # ch1-quiz.json -> ch1
    if figdir and chname != figdir[2:]:
        continue
    crops = json.load(open(os.path.join(base, 'scripts', 'figcrops', fn), encoding='utf-8'))
    if isinstance(crops, dict):
        crops = crops.get('items') or crops.get('crops') or []
    if not isinstance(crops, list):
        print(f'{fn}: UNEXPECTED STRUCTURE, skipped')
        continue
    outdir = os.path.join(base, 'assets', chname)
    os.makedirs(outdir, exist_ok=True)
    saved = []
    for c in crops:
        book = PAGEDIRS.get(c.get('book', 'textbook'), 'textbook')
        page_png = os.path.join(base, 'pages', book, f"p{c['page']:03d}.png")
        if not os.path.exists(page_png):
            print(f"  SKIP {c.get('out')}: page image missing {page_png}")
            continue
        im = Image.open(page_png)
        W, H = im.size
        x0, y0, x1, y1 = c['rect']
        if not (0 <= x0 < x1 <= 100 and 0 <= y0 < y1 <= 100):
            print(f"  SKIP {c.get('out')}: bad rect {c['rect']} (page {c['page']}, {fn})")
            continue
        box = (max(0, int(x0/100*W)), max(0, int(y0/100*H)),
               min(W, int(x1/100*W)), min(H, int(y1/100*H)))
        crop = im.crop(box)
        # 自动去白边：灰度化找非白内容 bbox，四周留 6px
        g = crop.convert('L')
        mask = g.point(lambda v: 255 if v < 242 else 0)
        bbox = mask.getbbox()
        if bbox:
            pad = 6
            x0b = max(0, bbox[0] - pad); y0b = max(0, bbox[1] - pad)
            x1b = min(crop.size[0], bbox[2] + pad); y1b = min(crop.size[1], bbox[3] + pad)
            # 防止意外裁成空图：面积过小则放弃 trim
            if (x1b - x0b) > 60 and (y1b - y0b) > 40:
                crop = crop.crop((x0b, y0b, x1b, y1b))
        outp = os.path.join(outdir, c['out'])
        crop.save(outp)
        saved.append({'file': c['out'], 'caption': c.get('caption', ''),
                      'page': c['page'], 'w': crop.size[0], 'h': crop.size[1]})
        total += 1
    with open(os.path.join(outdir, '_figs-' + fn), 'w', encoding='utf-8') as f:
        json.dump(saved, f, ensure_ascii=False, indent=1)
    print(f'{chname}: {len(saved)} figs')
print(f'CROP_DONE total={total}')
