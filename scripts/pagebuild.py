# -*- coding: utf-8 -*-
"""页面构建器：把 src/ 下的内容片段包上统一的头/导航/面包屑/尾/上页下页，输出到站点目录。
- 子代理只写内容片段（<main> 内部），消灭相对路径/导航错误
- 用法：
    python pagebuild.py              # 构建全部
    python pagebuild.py ch1/1.1     # 只构建指定页
片段路径约定：src/{chdir}/{page}.frag.html，例如 src/ch1/1.1.frag.html
特殊片段：src/index.frag.html → index.html（根）
每章：src/chN/index.frag.html（导学）、src/chN/quiz.frag.html（习题）
页面顺序（prev/next）：首页 → ch1导学 → ch1各节 → ch1 quiz → ch2导学 → …
"""
import sys, os, json

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
manifest = json.load(open(os.path.join(base, 'scripts', 'site_manifest.json'), encoding='utf-8'))

SITE_NAME = '考研408计算机网络带学'


def flat_pages():
    seq = [{'key': 'index.html', 'title': '首页'}]
    for ch in manifest['chapters']:
        n = ch['num']
        d = f'ch{n}'
        seq.append({'key': f'{d}/index.html', 'title': f'第{n}章 导学'})
        for s in ch['sections']:
            seq.append({'key': f'{d}/{s["id"]}.html', 'title': f'{s["id"]} {s["title"]}'})
        seq.append({'key': f'{d}/quiz.html', 'title': f'第{n}章 习题'})
    return seq


def nav_links(depth):
    r = '../' * depth
    out = [f'<a class="brand" href="{r}index.html">{SITE_NAME}</a>',
           f'<a class="chlink" href="{r}index.html">首页</a>']
    for ch in manifest['chapters']:
        n = ch['num']
        out.append(f'<a class="chlink" href="{r}ch{n}/index.html">第{n}章</a>')
    return '\n      '.join(out)


def page_href(target_key, cur_key):
    """计算从 cur_key 页面指向 target_key 页面的相对链接。"""
    cur_depth = 0 if cur_key == 'index.html' else 1
    prefix = '../' * cur_depth
    if target_key == 'index.html':
        return prefix + 'index.html'
    if cur_depth == 0:
        return target_key  # 根页面指向 chN/xxx.html
    # 同章目录内：chN/xxx.html → xxx.html（同章），跨章 → ../chM/xxx.html
    cur_dir = cur_key.split('/')[0]
    tgt_dir = target_key.split('/')[0]
    if tgt_dir == cur_dir:
        return target_key.split('/', 1)[1]
    return prefix + target_key


def load_body(frag_key):
    """读片段；习题页支持 quiz.part-*.frag.html 多部分按序拼接（大章习题由多个工匠分写）。"""
    import glob as _g
    frag = os.path.join(base, 'src', *frag_key.split('/')) + '.frag.html'
    if os.path.exists(frag):
        return open(frag, encoding='utf-8').read()
    parts = sorted(_g.glob(os.path.join(base, 'src', *frag_key.split('/')) + '.part-*.frag.html'))
    if parts:
        return '\n'.join(open(p, encoding='utf-8').read() for p in parts)
    return None


def build_page(frag_key, title, crumbs, prev, nxt):
    """frag_key 形如 'ch1/1.1'、'ch1/quiz' 或 'index'。"""
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
        parts = ['<div class="box">']
        for ch in manifest['chapters']:
            n = ch['num']
            parts.append(f'<h3 class="sub" style="margin:14px 0 6px">第{n}章 {ch["title"]}</h3>')
            parts.append('<div style="font-size:14.5px">')
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
</head>
<body>
<nav class="topnav"><div class="inner">
      {nav_links(depth)}
</div></nav>
<main>
<div class="crumbs">{crumb_html}</div>
{body}
{pager}
</main>
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


def main():
    only = sys.argv[1].rstrip('.html') if len(sys.argv) > 1 else None
    if only and only.endswith('.html'):
        only = only[:-5]
    seq = flat_pages()
    idx = {p['key']: i for i, p in enumerate(seq)}

    def neighbors(key):
        i = idx[key]
        prv = seq[i-1] if i > 0 else None
        nx = seq[i+1] if i+1 < len(seq) else None
        return prv, nx

    jobs = []  # (frag_key, out_key, title, crumbs)
    jobs.append(('index', 'index.html', '首页', [('首页', None)]))
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
    print(f'PAGEBUILD_DONE built={built}')


if __name__ == '__main__':
    main()
