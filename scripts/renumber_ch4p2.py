# -*- coding: utf-8 -*-
"""ch4 quiz.part-2 选择题全局编号 +1（因 part-1 将补做题本 4.2 第72题=全局第93题）。
规则：正文/alt/caption 中 "第 N 题"/"第N题"（92≤N≤153）→ N+1；h2 区间 "第 A～B 题" 双双 +1。
综合题编号不动。
"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(base, 'src', 'ch4', 'quiz.part-2.frag.html')
t = open(p, encoding='utf-8').read()

def bump(m):
    n = int(m.group(1))
    return f'第 {n+1} 题' if 92 <= n <= 153 else m.group(0)

t2 = re.sub(r'第 (\d+) 题', bump, t)

def bump2(m):
    a, b = int(m.group(1)), int(m.group(2))
    if 92 <= a <= 153 and 92 <= b <= 154:
        return f'第 {a+1}～{b+1} 题'
    return m.group(0)

t2 = re.sub(r'第 (\d+)～(\d+) 题', bump2, t2)

def bump3(m):
    n = int(m.group(1))
    return f'第{n+1}题' if 92 <= n <= 153 else m.group(0)

t2 = re.sub(r'第(\d+)题', bump3, t2)

# B1：综合题标题 28～28 → 19～28
t2 = t2.replace('综合题 28～28', '综合题 19～28')

open(p, 'w', encoding='utf-8').write(t2)

# 统计改动
old_nums = re.findall(r'第 (\d+) 题', t)
print('total 第 N 题 occurrences before:', len(old_nums))
changed = [n for n in old_nums if 92 <= int(n) <= 153]
print('renumbered:', len(changed))
print('sample h2 lines:')
for line in t2.split('\n'):
    if '<h2' in line:
        print(' ', line.strip()[:100])
