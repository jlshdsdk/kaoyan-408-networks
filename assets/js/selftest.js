/* 自测模式（仅习题页加载）：选项点击判分 + 计分条。
 * 规则：
 * - 仅 ans-key 为单个字母（A-D）的选择题参与判分；多空/多选题标注后跳过
 * - 点击选项即判分：选中项标紫，判对标绿，判错标红并高亮正确项，自动展开解析
 * - 底部浮动计分条：已答/总数、正确数、正确率、历史最佳（localStorage）
 */
(function () {
  'use strict';
  if (!window.SELFTEST) return;

  var main = document.querySelector('main.content');
  if (!main) return;
  var items = Array.prototype.slice.call(main.querySelectorAll('.quiz-item'));
  if (!items.length) return;

  var KEY = 'cn404_selftest';
  var chKey = (location.pathname.match(/ch\d/) || ['quiz'])[0];
  var on = false;
  var answered = 0, right = 0, total = 0;

  function loadBest() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }
  function saveBest(pct) {
    var d = loadBest();
    var rec = d[chKey] || {};
    rec.last = pct;
    if (pct > (rec.best || 0)) rec.best = pct;
    d[chKey] = rec;
    try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {}
  }

  /* ---- 工具条 ---- */
  var bar = document.createElement('div');
  bar.className = 'st-bar';
  bar.style.display = 'none';
  document.body.appendChild(bar);

  var launch = document.createElement('div');
  launch.className = 'st-launch';
  var best = loadBest()[chKey] || {};
  launch.innerHTML = '<button class="btn-checkin st-go">🎯 自测模式</button>' +
    '<span class="st-best">历史最佳' + (best.best != null ? best.best + '%' : '—') + '</span>';
  main.insertBefore(launch, main.querySelector('.quiz-item'));

  function fmt() {
    var pct = answered ? Math.round(right / answered * 100) : 0;
    return '已答 ' + answered + '/' + total + ' · 对 ' + right + ' · 正确率 ' + pct + '%' +
      (answered ? '' : '（点击选项即可作答）');
  }
  function refreshBar() {
    var pct = answered ? Math.round(right / answered * 100) : 0;
    bar.textContent = fmt() + ' · 最佳 ' + (loadBest()[chKey] ? loadBest()[chKey].best + '%' : '—') + ' ';
    var exit = document.createElement('button');
    exit.className = 'st-exit'; exit.textContent = '退出自测';
    exit.addEventListener('click', toggle);
    bar.appendChild(exit);
  }

  function parseLetter(item) {
    var key = item.querySelector('.ans-key');
    if (!key) return null;
    var m = (key.textContent || '').replace(/\s/g, '').match(/^答案：([A-D])$/);
    return m ? m[1] : null;
  }

  function grade(item, picked) {
    var correct = item.dataset.answer;
    item.dataset.done = '1';
    answered++;
    if (picked === correct) right++;
    Array.prototype.forEach.call(item.querySelectorAll('.choices li'), function (li) {
      var L = (li.textContent || '').trim().charAt(0);
      if (L === correct) li.classList.add('st-right');
      else if (L === picked) li.classList.add('st-wrong');
    });
    var det = item.querySelector('details.ans');
    if (det) det.open = true;
    var pct = Math.round(right / answered * 100);
    saveBest(pct);
    refreshBar();
  }

  function activate() {
    total = 0; answered = 0; right = 0;
    items.forEach(function (item) {
      var letter = parseLetter(item);
      if (!letter) {
        var chip = document.createElement('div');
        chip.className = 'st-skip';
        chip.textContent = '多空 / 多选题 · 不参与自测判分，请展开答案自行对照';
        var q = item.querySelector('.choices');
        if (q) q.parentNode.insertBefore(chip, q); else item.appendChild(chip);
        return;
      }
      item.dataset.answer = letter;
      item.classList.add('st-live');
      total++;
      var ul = item.querySelector('.choices');
      if (!ul) return;
      Array.prototype.forEach.call(ul.querySelectorAll('li'), function (li) {
        var L = (li.textContent || '').trim().charAt(0);
        if (!/^[A-D]$/.test(L)) return;
        li.classList.add('st-opt');
        li.addEventListener('click', function () {
          if (item.dataset.done) return;
          Array.prototype.forEach.call(ul.querySelectorAll('li'), function (o) { o.classList.remove('st-pick'); });
          li.classList.add('st-pick');
          grade(item, L);
        });
      });
    });
    refreshBar();
    bar.style.display = 'block';
    launch.querySelector('.st-go').textContent = '⏹ 退出自测';
  }

  function deactivate() {
    bar.style.display = 'none';
    launch.querySelector('.st-go').textContent = '🎯 自测模式';
    Array.prototype.forEach.call(main.querySelectorAll('.st-opt, .st-pick, .st-right, .st-wrong'), function (el) {
      el.classList.remove('st-opt', 'st-pick', 'st-right', 'st-wrong');
    });
    Array.prototype.forEach.call(main.querySelectorAll('.st-live'), function (el) {
      el.classList.remove('st-live'); delete el.dataset.done; delete el.dataset.answer;
    });
    Array.prototype.forEach.call(main.querySelectorAll('.st-skip'), function (el) { el.remove(); });
  }

  function toggle() {
    on = !on;
    if (on) activate(); else deactivate();
  }
  launch.querySelector('.st-go').addEventListener('click', toggle);
})();
