# -*- coding: utf-8 -*-
"""页面构建器 v2：顶栏 + 侧边目录 + 内容区 布局。
- 子代理只写内容片段（<main> 内部），导航/侧栏/搜索索引由本脚本统一生成
- 用法：
    python pagebuild.py              # 构建全部
    python pagebuild.py ch1/1.1     # 只构建指定页
片段路径约定：src/{chdir}/{page}.frag.html；quiz 支持 quiz.part-*.frag.html 拼接
页面顺序（prev/next）：首页 → ch1导学 → ch1各节 → ch1 quiz → ch2导学 → …
另生成 search-index.json（站内搜索用）。
"""
import sys, os, json, glob as _glob

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifest = json.load(open(os.path.join(base, 'scripts', 'site_manifest.json'), encoding='utf-8'))

SITE_NAME = '计算机网络自学网站'
TAGLINE = '王道带学 · 考点 × 插图 × 真题 × 打卡'
BRAND_TITLE = '循序渐进'
BRAND_L1 = '计算机网络 · 408 带学手册'
BRAND_L2 = '紧扣考纲 · 学练结合'


def flat_pages():
    seq = [{'key': 'index.html', 'title': '首页', 'ch': 0}]
    for ch in manifest['chapters']:
        n = ch['num']
        d = f'ch{n}'
        seq.append({'key': f'{d}/index.html', 'title': f'第{n}章 导学', 'ch': n})
        for s in ch['sections']:
            seq.append({'key': f'{d}/{s["id"]}.html', 'title': f'{s["id"]} {s["title"]}', 'ch': n})
        seq.append({'key': f'{d}/quiz.html', 'title': f'第{n}章 习题', 'ch': n})
    return seq


def page_href(target_key, cur_key):
    """相对链接：cur 为根页或 chN 内页。"""
    cur_depth = 0 if cur_key == 'index.html' else 1
    prefix = '../' * cur_depth
    if target_key == 'index.html':
        return prefix + 'index.html'
    if cur_depth == 0:
        return target_key
    cur_dir = cur_key.split('/')[0]
    tgt_dir = target_key.split('/')[0]
    if tgt_dir == cur_dir:
        return target_key.split('/', 1)[1]
    return prefix + target_key


def topbar_html(depth, cur_key):
    r = '../' * depth
    return f'''<header class="topbar">
    <button class="burger" id="btn-burger" aria-label="目录">☰</button>
    <a class="brand" href="{r}index.html">{SITE_NAME}</a>
    <span class="tagline">{TAGLINE}</span>
    <span class="spacer"></span>
    <div class="searchbox">
      <span class="s-ico">🔎</span>
      <input id="search-input" type="text" placeholder="全网搜索知识点 / 协议 / 端口号 / 题号…" autocomplete="off">
      <div class="search-results" id="search-results"></div>
    </div>
    <button class="topbtn" id="btn-fs-dec" title="减小字号">A-</button>
    <button class="topbtn" id="btn-fs-inc" title="增大字号">A+</button>
    <button class="topbtn" id="btn-theme" title="深色模式">🌙</button>
  </header>'''


def sidebar_html(depth, cur_key):
    """cur_key 形如 'index.html' 或 'ch1/1.1.html'。"""
    r = '../' * depth
    cur_ch = 0 if cur_key == 'index.html' else int(cur_key.split('/')[0][2:])
    parts = ['<aside class="sidebar" id="sidebar">']
    parts.append(f'''<div class="side-brand">
      <div class="sb-title">{BRAND_TITLE}</div>
      <div class="sb-line">{BRAND_L1}<br>{BRAND_L2}</div>
    </div>''')
    parts.append(f'<a class="side-home" href="{r}index.html">🏠 全站首页 · 408 考纲对照</a>')
    for ch in manifest['chapters']:
        n = ch['num']
        open_cls = ' open' if n == cur_ch else ''
        cnt = 2 + len(ch['sections'])
        parts.append(f'<div class="side-group{open_cls}" data-ch="{n}">')
        parts.append(f'''<div class="side-head"><span class="chev">▶</span>
          <span>第{n}章 {ch["title"]}</span><span class="cnt">0/{cnt}</span></div>''')
        parts.append('<div class="side-items">')
        items = [(f'ch{n}/index.html', '本章导学')]
        items += [(f'ch{n}/{s["id"]}.html', f'{s["id"]} {s["title"]}') for s in ch['sections']]
        items.append((f'ch{n}/quiz.html', '章末习题 · 答案折叠'))
        for key, label in items:
            active = ' class="active"' if key == cur_key else ''
            datak = f' data-key="{key}"'
            parts.append(f'<a href="{r}{key}"{active}{datak}><span class="dot">●</span>{label}</a>')
        parts.append('</div></div>')
    parts.append('</aside>')
    return '\n'.join(parts)


def load_body(frag_key):
    frag = os.path.join(base, 'src', *frag_key.split('/')) + '.frag.html'
    if os.path.exists(frag):
        return open(frag, encoding='utf-8').read()
    parts = sorted(_glob.glob(os.path.join(base, 'src', *frag_key.split('/')) + '.part-*.frag.html'))
    if parts:
        return '\n'.join(open(p, encoding='utf-8').read() for p in parts)
    return None


def build_page(frag_key, title, crumbs, prev, nxt):
    body = load_body(frag_key)
    if body is None:
        return False
    depth = 0 if frag_key == 'index' else 1
    r = '../' * depth
    out_key = 'index.html' if frag_key == 'index' else frag_key + '.html'
    cur_key = out_key

    crumb_html = ' › '.join(
        f'<a href="{c[1]}">{c[0]}</a>' if c[1] else f'<span>{c[0]}</span>' for c in crumbs)

    # 占位符注入：全站目录（首页用）
    if '<!--FULL_TOC-->' in body:
        parts = ['<div class="tocbox">']
        for ch in manifest['chapters']:
            n = ch['num']
            parts.append(f'<h3 class="sub" style="margin:14px 0 6px">第{n}章 {ch["title"]}</h3>')
            parts.append('<div style="font-size:.9rem">')
            parts.append(f'<div class="toc-line"><a href="ch{n}/index.html">本章导学</a><span class="pg">考纲要求 · 章节地图</span></div>')
            for s in ch['sections']:
                subs = ' / '.join(x['id'] for x in s['subsections'])
                parts.append(f'<div class="toc-line"><a href="ch{n}/{s["id"]}.html">{s["id"]} {s["title"]}</a>'
                             f'<span class="pg">{subs}</span></div>')
            parts.append(f'<div class="toc-line"><a href="ch{n}/quiz.html">第{n}章 习题（选择 + 综合，答案折叠）</a><span class="pg">做题本</span></div>')
            parts.append('</div>')
        parts.append('</div>')
        body = body.replace('<!--FULL_TOC-->', '\n'.join(parts))

    def pager_a(target, cls):
        if not target:
            return f'<a class="{cls}" style="visibility:hidden"><span class="label">—</span>—</a>'
        return (f'<a class="{cls}" href="{page_href(target["key"], cur_key)}">'
                f'<span class="label">{"上一篇" if cls == "prev" else "下一篇"}</span>{target["title"]}</a>')

    pager = f'''<div class="pager">
      {pager_a(prev, "prev")}
      {pager_a(nxt, "next")}
    </div>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - {SITE_NAME}</title>
<link rel="stylesheet" href="{r}assets/css/site.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'\\\\(',right:'\\\\)',display:false}}],throwOnError:false}});"></script>
<script>window.SITE_BASE = '{r}';</script>
<script defer src="{r}assets/js/site.js"></script>
</head>
<body>
{topbar_html(depth, cur_key)}
<div class="side-mask" id="side-mask"></div>
<div class="layout">
{sidebar_html(depth, cur_key)}
<main class="content">
<div class="crumbs">{crumb_html}</div>
{body}
{pager}
</main>
</div>
<footer class="site-footer">{SITE_NAME} · 内容依据王道《2027计算机网络考研复习指导》整理，仅供个人学习备考使用<br>
习题与解析源自王道做题本，答案经答案速查交叉核对</footer>
</body>
</html>'''
    outp = os.path.join(base, *out_key.split('/'))
    os.makedirs(os.path.dirname(outp) or base, exist_ok=True)
    with open(outp, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'BUILT {out_key}')
    return True


def write_search_index():
    idx = [{'t': '首页 · 408 考纲对照', 'u': 'index.html', 's': '', 'k': '考纲 大纲 对照 使用说明 目录'}]
    for ch in manifest['chapters']:
        n = ch['num']
        idx.append({'t': f'第{n}章 {ch["title"]} · 导学', 'u': f'ch{n}/index.html',
                    's': '', 'k': '考纲要求 复习提示 考点分布 章节地图'})
        for s in ch['sections']:
            subs = ' '.join(x['title'] for x in s['subsections'])
            idx.append({'t': f'{s["id"]} {s["title"]}', 'u': f'ch{n}/{s["id"]}.html',
                        's': f'第{n}章 {ch["title"]}', 'k': subs})
        idx.append({'t': f'第{n}章 习题', 'u': f'ch{n}/quiz.html', 's': f'第{n}章',
                    'k': '选择题 综合题 答案 解析 做题本 真题'})
    outp = os.path.join(base, 'search-index.json')
    with open(outp, 'w', encoding='utf-8') as f:
        json.dump(idx, f, ensure_ascii=False, indent=0)
    print(f'SEARCH_INDEX {len(idx)} entries')


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    if only and only.endswith('.html'):
        only = only[:-5]
    seq = flat_pages()
    idx = {p['key']: i for i, p in enumerate(seq)}

    def neighbors(key):
        i = idx[key]
        return (seq[i-1] if i > 0 else None), (seq[i+1] if i+1 < len(seq) else None)

    jobs = [('index', 'index.html', '首页', [('首页', None)])]
    for ch in manifest['chapters']:
        n = ch['num']
        d = f'ch{n}'
        jobs.append((f'{d}/index', f'{d}/index.html', f'第{n}章 {ch["title"]} · 导学',
                     [('首页', page_href('index.html', f'{d}/x')), (f'第{n}章 {ch["title"]}', None)]))
        for s in ch['sections']:
            jobs.append((f'{d}/{s["id"]}', f'{d}/{s["id"]}.html', f'{s["id"]} {s["title"]}',
                         [('首页', page_href('index.html', f'{d}/x')),
                          (f'第{n}章 {ch["title"]}', 'index.html'),
                          (f'{s["id"]} {s["title"]}', None)]))
        jobs.append((f'{d}/quiz', f'{d}/quiz.html', f'第{n}章 习题',
                     [('首页', page_href('index.html', f'{d}/x')),
                      (f'第{n}章 {ch["title"]}', 'index.html'),
                      ('本章习题', None)]))

    built = 0
    for frag_key, out_key, title, crumbs in jobs:
        if only and frag_key != only:
            continue
        prv, nx = neighbors(out_key)
        if build_page(frag_key, title, crumbs, prv, nx):
            built += 1
    if not only:
        write_search_index()
    print(f'PAGEBUILD_DONE built={built}')


if __name__ == '__main__':
    main()
