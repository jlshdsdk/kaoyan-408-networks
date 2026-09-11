/* 考研408计算机网络带学 - 交互脚本（无依赖） */
(function () {
  'use strict';
  var BASE = window.SITE_BASE || './';

  /* ---------- 深色模式 ---------- */
  var themeBtn = document.getElementById('btn-theme');
  function applyTheme(t) {
    if (t === 'dark') { document.documentElement.setAttribute('data-theme', 'dark'); }
    else { document.documentElement.removeAttribute('data-theme'); }
    if (themeBtn) themeBtn.textContent = t === 'dark' ? '☀️' : '🌙';
  }
  var savedTheme = null;
  try { savedTheme = localStorage.getItem('cn404_theme'); } catch (e) {}
  applyTheme(savedTheme === 'dark' ? 'dark' : 'light');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    var next = cur === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('cn404_theme', next); } catch (e) {}
    applyTheme(next);
  });

  /* ---------- 字号 A- / A+ ---------- */
  var MIN_FS = 14, MAX_FS = 19;
  function applyFs(px) {
    document.documentElement.style.fontSize = px + 'px';
  }
  var savedFs = null;
  try { savedFs = parseInt(localStorage.getItem('cn404_font'), 10); } catch (e) {}
  if (!savedFs || savedFs < MIN_FS || savedFs > MAX_FS) savedFs = 16;
  applyFs(savedFs);
  function bindFs(id, delta) {
    var b = document.getElementById(id);
    if (!b) return;
    b.addEventListener('click', function () {
      var cur = parseInt(document.documentElement.style.fontSize, 10) || 16;
      var next = Math.min(MAX_FS, Math.max(MIN_FS, cur + delta));
      applyFs(next);
      try { localStorage.setItem('cn404_font', String(next)); } catch (e) {}
    });
  }
  bindFs('btn-fs-dec', -1);
  bindFs('btn-fs-inc', +1);

  /* ---------- 移动端侧栏 ---------- */
  var burger = document.getElementById('btn-burger');
  if (burger) burger.addEventListener('click', function () {
    document.body.classList.toggle('side-open');
  });
  var mask = document.getElementById('side-mask');
  if (mask) mask.addEventListener('click', function () {
    document.body.classList.remove('side-open');
  });

  /* ---------- 侧栏分组折叠 ---------- */
  var groups = document.querySelectorAll('.side-group');
  Array.prototype.forEach.call(groups, function (g) {
    var head = g.querySelector('.side-head');
    if (!head) return;
    head.addEventListener('click', function () { g.classList.toggle('open'); });
  });

  /* ---------- 学习进度（访问过的页面标记 + 每章计数） ---------- */
  var VIS_KEY = 'cn404_visited';
  function loadVis() {
    try { return JSON.parse(localStorage.getItem(VIS_KEY) || '{}'); } catch (e) { return {}; }
  }
  function saveVis(v) {
    try { localStorage.setItem(VIS_KEY, JSON.stringify(v)); } catch (e) {}
  }
  var vis = loadVis();
  var here = location.pathname.replace(/\\/g, '/');
  here = here.substring(here.lastIndexOf('/') + 1) || 'index.html';
  var hereDir = location.pathname.replace(/\/[^/]*$/, '').split('/').pop();
  var hereKey = (hereDir && /^ch\d$/.test(hereDir) ? hereDir + '/' : '') + here;
  vis[hereKey] = Date.now();
  saveVis(vis);

  // 标记侧栏已访问小圆点 + 每章计数
  var items = document.querySelectorAll('.side-items a[data-key]');
  Array.prototype.forEach.call(items, function (a) {
    if (vis[a.getAttribute('data-key')]) a.classList.add('visited');
  });
  Array.prototype.forEach.call(document.querySelectorAll('.side-group[data-ch]'), function (g) {
    var total = g.querySelectorAll('.side-items a[data-key]').length;
    var done = g.querySelectorAll('.side-items a.visited').length;
    var cnt = g.querySelector('.side-head .cnt');
    if (cnt) {
      cnt.textContent = done + '/' + total;
      if (done >= total) cnt.classList.add('done');
    }
  });

  /* ---------- 搜索 ---------- */
  var sInput = document.getElementById('search-input');
  var sBox = document.getElementById('search-results');
  if (sInput && sBox) {
    var INDEX = null;
    function ensureIndex(cb) {
      if (INDEX) return cb(INDEX);
      fetch(BASE + 'search-index.json').then(function (r) { return r.json(); }).then(function (d) {
        INDEX = d; cb(d);
      }).catch(function () { INDEX = []; cb(INDEX); });
    }
    function render(list) {
      if (!list.length) {
        sBox.innerHTML = '<div class="sr-none">没有匹配的页面，试试「子网」「TCP」「端口」</div>';
      } else {
        sBox.innerHTML = list.map(function (it) {
          return '<a href="' + BASE + it.u + '">' + it.t +
            (it.s ? '<span class="sr-sub">' + it.s + '</span>' : '') + '</a>';
        }).join('');
      }
      sBox.classList.add('open');
    }
    sInput.addEventListener('input', function () {
      var q = sInput.value.trim();
      if (!q) { sBox.classList.remove('open'); return; }
      ensureIndex(function (idx) {
        var ql = q.toLowerCase();
        var hits = idx.filter(function (it) {
          return (it.t + ' ' + (it.s || '') + ' ' + (it.k || '')).toLowerCase().indexOf(ql) >= 0;
        }).slice(0, 9);
        render(hits);
      });
    });
    sInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        var first = sBox.querySelector('a');
        if (first) location.href = first.getAttribute('href');
      }
      if (e.key === 'Escape') sBox.classList.remove('open');
    });
    document.addEventListener('click', function (e) {
      if (!sBox.contains(e.target) && e.target !== sInput) sBox.classList.remove('open');
    });
  }

  /* ---------- 打卡（仅首页元素存在时启用） ---------- */
  var ciBtn = document.getElementById('btn-checkin');
  if (ciBtn) {
    var CK_KEY = 'cn404_checkins';
    function todayStr(d) {
      d = d || new Date();
      return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
    }
    function loadCk() {
      try { return JSON.parse(localStorage.getItem(CK_KEY) || '[]'); } catch (e) { return []; }
    }
    function streak(days) {
      if (!days.length) return 0;
      var set = {}; days.forEach(function (d) { set[d] = 1; });
      var n = 0, d = new Date();
      if (!set[todayStr(d)]) d.setDate(d.getDate() - 1); // 今天还没打卡则从昨天起算
      while (set[todayStr(d)]) { n++; d.setDate(d.getDate() - 1); }
      return n;
    }
    var ck = loadCk();
    var t0 = todayStr();
    var elStreak = document.getElementById('ci-streak');
    var elTotal = document.getElementById('ci-total');
    var elBar = document.getElementById('ci-bar');
    var elProg = document.getElementById('ci-progress');
    function refresh() {
      ck = loadCk();
      var has = ck.indexOf(t0) >= 0;
      ciBtn.disabled = has;
      ciBtn.textContent = has ? '✅ 今日已打卡' : '✅ 今日打卡';
      if (elStreak) elStreak.textContent = streak(ck);
      if (elTotal) elTotal.textContent = ck.length;
    }
    refresh();
    ciBtn.addEventListener('click', function () {
      var c = loadCk();
      if (c.indexOf(t0) < 0) { c.push(t0); c.sort(); try { localStorage.setItem(CK_KEY, JSON.stringify(c)); } catch (e) {} }
      refresh();
    });
    // 全站学习进度条（按侧栏总页数）
    var allItems = document.querySelectorAll('.side-items a[data-key]');
    if (elBar && elProg && allItems.length) {
      var doneN = 0;
      Array.prototype.forEach.call(allItems, function (a) {
        if (vis[a.getAttribute('data-key')]) doneN++;
      });
      elBar.style.width = Math.round(doneN / allItems.length * 100) + '%';
      elProg.textContent = doneN + '/' + allItems.length + ' 页';
    }
  }
})();
