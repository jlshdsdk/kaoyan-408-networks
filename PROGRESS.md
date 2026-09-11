# PROGRESS.md — 进度断点

> 每完成一个里程碑更新。接手者先读 PLAN.md。

## 当前状态（内容生产全部完成，进入审查+修复期）

- [x] 侦察：4 PDF 全扫描版；教材 TOC 提取（scripts/toc_textbook.txt → site_manifest.json）
- [x] git（tools/git）+ gh（tools/bin/gh.exe，登录 jlshdsdk，keyring token）
- [x] 全部 519 页整页图导出 pages/{textbook,choice,comp,answer}/
- [x] 站点骨架：assets/css/site.css、scripts/pagebuild.py（片段→整页，含 quiz.part-* 拼接）、
      crop_figs.py（支持 book 字段+白边 trim）、linkcheck.py、首页（408考纲对照+全站目录注入）
- [x] answers.json 转录（28 节）+ **主代理放大扫描图复核修正 3 处**：
      4.2=72项（转录丢2项）、6.3 AAAC=4道单选、5.3 末尾补 B
- [x] 6 章正文片段全产出（src/chN/*.frag.html + figcrops/*.json），43 页构建通过
- [x] 6 套习题片段全产出（ch3/ch4 各 2 个 part 拼接）
- [ ] 进行中：4 个定向修复
  1. ch4-A：part-1 第88-92题答案改 B,D,A,B,D + 查做题本 4.2 Q72 是否存在（answers.json 已修为 72 项）
  2. ch4-B：part-2 综合题 10-19 → 19-28（A 已编到 18）
  3. ch3-A：补综合题 7（comp p011 顶部 2017 GBN 真题）
  4. ch3-B：补 3.5 补充题 Q20/21（教材 p099 核答案）+ 复核第 127 题 PPP 答案（教材 p128）
- [ ] 全部习题插图裁剪（新 json：ch3-quiz/ch3-quiz2/ch4-quiz/ch4-quiz2/ch5-quiz/ch6-quiz）+ 重建 + linkcheck
- [ ] 每章对抗性审查（视觉子代理×6）→ 修复循环
- [ ] 部署 + 验证
- [ ] 收尾报告

## 关键数字（截至当前）
- 页面：43 个 html 已构建（首页 + 6 导学 + 27 节页 + 6 quiz + 更多待重建）
- 插图：121 张已裁（新增习题图裁剪待跑）
- 题目：ch1 55+3综、ch2 49+2综、ch3 150~152+12综、ch4 91~93+19综+10综、ch5 88+19综、ch6 65+13综
  （ch3/ch4 修复中，最终数待定）
- 408 章节映射：site_manifest.json（与教材书签一一对应，34 节 93 小节）

## 已裁决事项（主代理）
1. 教材为扫描版 → 内容由视觉工匠读页面图生产；插图按页面区域裁剪
2. ch4 导学节名错误（按考纲臆排）已由主代理重写为教材真实目录
3. answers.json 三处转录错误已修（主代理亲眼核对扫描图）
4. ch3 3.5 的 Q20/Q21（速查无对应项）→ 补充题方案（标注来源教材解析）
5. ch4 综合题编号冲突 → part-2 顺延为 19-28
6. 6.3 的 "AAAC" 不是多空题，是速查压缩排版（拆为 4 项）

## 已知待办风险
- 图裁剪 rect 全靠目测，正文行混入问题需审查代理逐图目检（已知 ch2 fig-2-2 上下缘、
  ch1 quiz q16 下缘有文字残留，待审查环节统一修）
- ch4 做题本 4.2 题数（71 vs 速查 72）待 ch4-A 回报
- ch3 3.9 小节标题已对齐"本章小结及疑难点"

## 部署预案（未执行）
- 仓库 jlshdsdk/kaoyan-408-networks（公开）；.gitignore 排除 pages/ tools/ scripts/_*.png 等
- tools/git/cmd/git.exe init → gh repo create → push → gh api pages → curl 验证
