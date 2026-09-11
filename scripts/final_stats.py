# -*- coding: utf-8 -*-
"""终版统计：每章页面数/图数/题目数。"""
import io, sys, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

total_q = 0
total_comp = 0
total_figs = 0
for n in range(1, 7):
    d = f'ch{n}'
    qdir = os.path.join(base, 'src', d)
    frags = [f for f in os.listdir(qdir) if f.endswith('.frag.html')]
    content_pages = [f for f in frags if re.match(r'\d+\.\d+\.frag', f)]
    quiz_parts = [f for f in frags if 'quiz' in f]
    # 题目数
    qn = 0
    comp = 0
    for pf in quiz_parts:
        t = open(os.path.join(qdir, pf), encoding='utf-8').read()
        nums = re.findall(r'第 (\d+) 题', t)
        if nums:
            qn = max(qn, max(int(x) for x in nums))
        comp += len(re.findall(r'>综合题 \d+', t))
    # 图数
    figs = len([f for f in os.listdir(os.path.join(base, 'assets', d)) if f.endswith('.png')])
    total_q += qn
    total_comp += comp
    total_figs += figs
    print(f'{d}: 正文页 {len(content_pages)} 节, 插图 {figs} 张, 选择题 {qn} 题, 综合题 {comp} 题')
print(f'合计: 选择题 {total_q}, 综合题 {total_comp}, 插图 {total_figs}')
htmls = sum(len([f for f in files if f.endswith('.html')]) for _, dirs, files in os.walk(base)
            if not any(x in _ for x in ('pages', 'tools', 'scripts', 'assets', '.git', 'src')))
print('html pages:', htmls)
