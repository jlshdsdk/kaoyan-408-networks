# PLAN.md — 考研408计算机网络带学网站

> 断点文件：任何模型接手都能据此续作。配合 PROGRESS.md 查看当前进度。

## 目标
用工作区的 4 个王道 PDF（均为**扫描版**，无文本层）搭建「考研408计算机网络带学网站」，
部署到 GitHub Pages（仓库 kaoyan-408-networks，账号 jlshdsdk）。

## 关键事实（已验证）
- 教材 `2027计算机网络_高清带书签版.pdf`：316 页，419 书签，**每页=一张 1443×2011 整页扫描图，无文本**
- 选择题做题本 = `【留空】.pdf`：145 页（扫描）→ pages/choice/
- 综合题做题本 = `27王道《计网》综合题做题本【留空】3.16.pdf`：56 页（扫描）→ pages/comp/
- 答案速查 = `27王道《计网》选择题【答案速查】.pdf`：2 页（扫描）→ pages/answer/
- 教材真实 TOC 已提取：`scripts/toc_textbook.txt`（PyMuPDF get_toc，PDF 页码 1-based）
- 教材目录结构：6 章；L2=X.Y 节；L3=X.Y.Z 小节；每节末有「本节习题精选/答案与解析」（网站不用它，
  网站习题取自独立做题本）
- 章节页码区间（PDF 页）：ch1 p13-41，ch2 p42-61，ch3 p62-138，ch4 p139-235，ch5 p236-278，ch6 p279-316
- 做题本书签：`scripts/toc_choice_quizbook.txt`、`scripts/toc_comprehensive_quizbook.txt`
- 环境：Python 3.14.4 + PyMuPDF 1.28.2（用 `import pymupdf`）；git/gh 在 `tools/git/`、`tools/bin/gh.exe`
- gh 已登录 jlshdsdk（keyring，repo 权限）。winget 被墙，github.com 直连 OK。

## 架构决策（主模型已定，不要重议）
1. **MPA 静态站，无构建**：`index.html` + `chN/`（每章 index.html 导学 + 每 L2 节一个 html + quiz.html）
2. 全站相对路径；`assets/css/site.css` 公共样式；`assets/chN/` 放本章插图
3. 图片策略（扫描版唯一可行解）：从 pages/textbook/pXXX.png **按区域裁剪**。
   作者子代理输出裁剪清单 JSON（页码 + 相对坐标 0-100 + 文件名 + 图号），脚本批量裁剪 → assets/chN/
4. 内容生产：Flash 档视觉子代理直接读教材页面 PNG 撰写 HTML（教材无文本层，纯视觉转录+改写）
5. 习题：quiz.html 内选择题+综合题，取自做题本页面（视觉转录），答案与 pages/answer 交叉核对；
   答案用 <details> 折叠
6. 公式：KaTeX CDN（deferred），公式同时保留可读文本
7. 课外拓展内容统一 `.ext` 类标注「课外拓展」徽标，与考点分离

## 站点结构
```
index.html            首页：章节导航 + 408考纲对照 + 使用说明
ch1/index.html        第1章导学（考纲要求/考点分布/章节地图）
ch1/1.1.html ...      每节一页（含 X.Y.Z 锚点）
ch1/quiz.html         本章习题（选择+综合，答案折叠）
assets/css/site.css   公共样式
assets/chN/*.png      插图
408大纲.md?           不需要——考纲对照并入首页
```

## 裁剪清单 schema（scripts/figcrops/chN.json）
```json
[{"page":15, "rect":[8,20,92,55], "out":"fig-1-3.png", "caption":"图1-3 分组交换示意"}]
```
rect 为相对页面百分比 [x0,y0,x1,y1]（0-100，原点左上）。裁剪脚本：`scripts/crop_figs.py`。

## 子代理分工
- **作者代理**（Flash 档视觉）：每章 1 个正文任务 + 1 个习题任务；prompt 写死模板/素材路径/输出路径/验收标准
- **审查代理**（Flash 档视觉）：每章 1 个，对照页面 PNG 抽查事实/公式/答案、图片配对、相对路径断链，
  输出问题清单（不修）
- **主模型**：按清单修复 + 抽查复验

## 执行顺序
1. ✅ 侦察（PDF/环境/TOC/扫描版判定）
2. ✅ gh 就绪；git 解压中
3. ⏳ 整页图导出 pages/（后台）
4. 答案速查转录 → scripts/answers.json（视觉，2 页）
5. 站点骨架：site.css / index.html / 模板 / crop_figs.py
6. ch1 样板全流程 → 主模型自查（浏览器/静态检查）
7. ch2-ch6 批量（可并行的子代理任务，ch4 拆分为 2-3 个任务）
8. 每章审查+修复循环
9. 部署 + curl 验证（首页+3 子页+图片）
10. 收尾报告

## 禁区/纪律
- 不要把 pages/ 提交进 git（体积大）；.gitignore 排除 pages/ tools/ scripts/中间产物
- 不要凭记忆写章节结构——一律以 scripts/toc_textbook.txt 为准
- 答案必须与 pages/answer 交叉核对，不得由作者代理凭印象写答案
- 相对路径：ch1/index.html 引用首页用 `../index.html`，引用图片 `../assets/ch1/x.png`
