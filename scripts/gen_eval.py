# -*- coding: utf-8 -*-
"""生成 agent-browser eval 用的 base64 脚本（避免 cmd 引号地狱）。
用法：python gen_eval.py <脚本文件.js>  → 写 scripts/_b64.txt（单行 base64）
然后：set /p B64=<scripts\_b64.txt && agent-browser eval -b %B64%
"""
import sys, os, io, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1]
s = open(src, encoding='utf-8').read()
b64 = base64.b64encode(s.encode('utf-8')).decode()
with open(os.path.join(root, 'scripts', '_b64.txt'), 'w') as f:
    f.write(b64)
print('B64_WRITTEN len=' + str(len(b64)))
