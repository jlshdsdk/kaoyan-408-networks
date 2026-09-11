# -*- coding: utf-8 -*-
"""从教材真实书签生成站点清单 site_manifest.json。
规则：
- 只取 6 个 L1 章（标题以「第N章」开头）
- L2=X.Y 节 → 站点页面；L3=X.Y.Z 小节 → 页内锚点
- 排除 L3 中「本节习题精选 / 答案与解析 / 考纲内容 / 复习提示 / 本章小结及疑难点」等非正文书签
  （小结页仍保留为 L2 节，因为它是教材真实目录的一部分）
每个小节的页码区间 = [自身起始页, 同级或更高级下一书签起始页-1]
"""
import sys, os, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pymupdf

base = r'C:\Users\王奕博\Desktop\计算机网络自学网站'
d = pymupdf.open(os.path.join(base, '2027计算机网络_高清带书签版.pdf'))
toc = d.get_toc()  # [level, title, page(1-based)]
d.close()

EXCLUDE_SUB = re.compile(r'(本节)?习题精选|答案与解析|考纲内容|复习提示')
SEC_RE = re.compile(r'^(\d+)\.(\d+)\s+(.+)$')
SUB_RE = re.compile(r'^(\d+)\.(\d+)\.(\d+)\s+(.+)$')
CH_RE = re.compile(r'^第(\d+)章\s*(.+)$')

# 规范化书签标题中的空格（如 "1.1  计算机网络概述"），并去掉选学星号前缀
def norm(t):
    return re.sub(r'\s+', ' ', t).replace('\u3000', ' ').strip().lstrip('*').strip()

chapters = []
cur_ch = None
cur_sec = None
# 先展开为带层级的平坦列表
flat = []
for lvl, title, page in toc:
    flat.append({'lvl': lvl, 'title': norm(title), 'page': page})

for i, e in enumerate(flat):
    m = CH_RE.match(e['title'])
    if e['lvl'] == 1 and m:
        cur_ch = {'num': int(m.group(1)), 'title': m.group(2).strip(),
                  'page_start': e['page'], 'sections': []}
        chapters.append(cur_ch)
        cur_sec = None
        continue
    if cur_ch is None:
        continue
    if e['lvl'] == 2:
        ms = SEC_RE.match(e['title'])
        if not ms:
            continue  # 考纲内容/复习提示等 L2 杂项
        cur_sec = {'id': f"{ms.group(1)}.{ms.group(2)}", 'title': ms.group(3).strip(),
                   'page_start': e['page'], 'subsections': []}
        cur_ch['sections'].append(cur_sec)
        continue
    if e['lvl'] == 3 and cur_sec is not None:
        ms = SUB_RE.match(e['title'])
        if not ms or EXCLUDE_SUB.search(e['title']):
            continue
        cur_sec['subsections'].append({'id': f"{ms.group(1)}.{ms.group(2)}.{ms.group(3)}",
                                       'title': ms.group(4).strip(), 'page': e['page']})

# 计算区间终点：下一同级/更高级书签的起始页-1
def end_page(entries_key, items, global_next_page):
    for j, it in enumerate(items):
        nxt = items[j+1]['page_start'] if j+1 < len(items) else global_next_page
        it['page_end'] = nxt - 1

for ci, ch in enumerate(chapters):
    ch_next = chapters[ci+1]['page_start'] if ci+1 < len(chapters) else 317
    end_page('sections', ch['sections'], ch_next)
    for sec in ch['sections']:
        # 小节终点：书签平坦列表里该小节之后第一个"其他"书签
        for si, sub in enumerate(sec['subsections']):
            # 找到该小节在平坦列表中的位置之后，第一个 page > sub['page'] 的书签起点
            # 简化：用该小节书签在 toc 中的 index —— 按 (page,title) 匹配
            nxt = sec['page_end'] + 1
            found = False
            for j, e in enumerate(flat):
                if e['page'] == sub['page'] and e['title'].startswith(sub['id']):
                    # 向后找第一个起点更大的书签
                    for e2 in flat[j+1:]:
                        if e2['page'] > sub['page']:
                            nxt = e2['page']
                            found = True
                            break
                    break
            sub['page_end'] = nxt - 1
    ch['page_end'] = ch['sections'][-1]['page_end'] if ch['sections'] else ch_next - 1

manifest = {'chapters': chapters}
out = os.path.join(base, 'scripts', 'site_manifest.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)

# 打印摘要供人工核验
for ch in chapters:
    print(f"ch{ch['num']} {ch['title']} p{ch['page_start']}-{ch['page_end']} sections={len(ch['sections'])} subs={sum(len(s['subsections']) for s in ch['sections'])}")
    for s in ch['sections']:
        print(f"  {s['id']} {s['title']} p{s['page_start']}-{s['page_end']} subs={[x['id'] for x in s['subsections']]}")
print('MANIFEST_OK ->', out)
