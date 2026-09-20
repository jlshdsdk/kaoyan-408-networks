# -*- coding: utf-8 -*-
"""线上内容终验（显式 UTF-8）。"""
import io, sys, urllib.request, ssl
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = 'https://jlshdsdk.github.io/kaoyan-408-networks/'
proxy = 'http://127.0.0.1:7892'
ctx = ssl.create_default_context()

def get(u):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}))
    return opener.open(u, timeout=30).read().decode('utf-8', 'ignore')

h = get(BASE + 'ch1/recall.html')
checks = {
    'has_title': '第1章 速记手册' in h,
    'has_points': '核心考点速记' in h,
    'has_traps': '易错清单' in h,
    'has_numbers': '必背' in h,
    'has_quiz5': '一分钟自测' in h,
    'map_nodes': h.count('map-node'),
}
for k, v in checks.items():
    print(k, v)

q = get(BASE + 'ch4/quiz.html')
print('quiz_selftest_flag', 'SELFTEST = 1' in q)
css = get(BASE + 'assets/css/site.css')
print('live_css_has_stbar', '.st-bar' in css)
print('live_css_has_mapflow', '.map-node' in css)
print('DONE')
