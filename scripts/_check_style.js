(function(){
  var imgs = document.querySelectorAll('.quiz-item img');
  var out = [];
  for (var i = 0; i < imgs.length; i++) {
    var el = imgs[i];
    var w = Math.round(el.getBoundingClientRect().width);
    if (w > 1200) {
      var cs = getComputedStyle(el);
      out.push('w=' + w + ' maxWidth=' + cs.maxWidth + ' src=' + el.getAttribute('src').slice(-24));
    }
  }
  var sheet = 0, hit = false;
  for (var j = 0; j < document.styleSheets.length; j++) {
    var href = document.styleSheets[j].href || '';
    if (href.indexOf('site.css') >= 0) { sheet = 1; try { hit = document.styleSheets[j].cssText.indexOf('quiz-item img') >= 0; } catch(e){} }
  }
  return 'site.css loaded=' + sheet + ' rule_present=' + hit + ' | ' + (out.join(' | ') || 'no img over 1200px');
})()
