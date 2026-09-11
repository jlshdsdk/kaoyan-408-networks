# -*- coding: utf-8 -*-
"""ch2 审查后的 rect 修正（审查官逐图目检给出的精确建议值）。"""
import io, sys, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXDIR = os.path.join(base, 'scripts', 'figcrops')

# 文件名 -> 新 rect（审查报告建议）
ch2 = {
    'fig-2-1.png': [15, 18.5, 85, 29.2],
    'fig-2-3.png': [18, 45.5, 85, 77],
    'fig-2-4.png': [18, 38.7, 85, 60],
    'fig-2-5.png': [20, 53.5, 80, 65.3],
    'fig-2-6.png': [20, 78, 80, 88],
    'fig-2-7.png': [15, 18.5, 85, 30],
    'fig-2-8.png': [15, 35.3, 88, 45.2],
    'fig-2-9.png': [15, 52.4, 88, 60.8],
    'fig-2-10.png': [18, 19, 82, 31],
    'fig-2-2.png': [18, 29.5, 82, 61.5],
}
ch2quiz = {
    'quiz-2.1-q20.png': [30, 29.3, 75, 36.5],
    'quiz-2.1-q23.png': [38, 13.2, 68, 20],
    'quiz-comp-1.png': [38, 17.5, 68, 20],
    'quiz-2.1-q8.png': [30, 57.5, 75, 66.5],
    'quiz-2.1-q22.png': [30, 63.8, 75, 76.2],
}

def apply(fn, mapping):
    p = os.path.join(FIXDIR, fn)
    d = json.load(open(p, encoding='utf-8'))
    items = d['items'] if isinstance(d, dict) else d
    n = 0
    for c in items:
        if c['out'] in mapping:
            c['rect'] = mapping[c['out']]
            n += 1
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(fn, 'updated', n)

apply('ch2.json', ch2)
apply('ch2-quiz.json', ch2quiz)
print('RECTS_FIXED')
