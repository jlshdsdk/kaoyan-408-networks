# -*- coding: utf-8 -*-
"""统计 assets 下 webp 数量与总体积。"""
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
total = 0
n = 0
for r, d, fs in os.walk(base):
    for f in fs:
        if f.endswith('.webp'):
            total += os.path.getsize(os.path.join(r, f))
            n += 1
print(f'webp count={n} total={total//1024}KB')
