(function(){
  var d = document.querySelector('img[src*="q11"]');
  if (!d) return 'not found';
  d.scrollIntoView({block:'center'});
  return 'scrolled, w=' + Math.round(d.getBoundingClientRect().width);
})()
