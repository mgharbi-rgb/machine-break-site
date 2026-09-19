/* Maquettes : apparitions au défilement, halo qui suit le curseur (A), inclinaison des tuiles (B), image de survol (A/C). */
(function () {
  var d = document, reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  d.documentElement.classList.remove('no-js');
  var els = [].slice.call(d.querySelectorAll('.rv'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }
  if (reduce || !window.matchMedia('(hover: hover)').matches) return;

  var glow = d.querySelector('[data-glow]');
  if (glow) glow.addEventListener('pointermove', function (e) { var r = glow.getBoundingClientRect(); glow.style.setProperty('--gx', (e.clientX - r.left) + 'px'); glow.style.setProperty('--gy', (e.clientY - r.top) + 'px'); });

  [].forEach.call(d.querySelectorAll('[data-tilt]'), function (t) {
    t.addEventListener('pointermove', function (e) { var r = t.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; t.style.transform = 'perspective(900px) rotateX(' + (-y * 5) + 'deg) rotateY(' + (x * 6) + 'deg) translateY(-4px)'; });
    t.addEventListener('pointerleave', function () { t.style.transform = ''; });
  });

  var list = d.querySelector('[data-hoverlist]'), pic = d.querySelector('[data-hoverpic]');
  if (list && pic) {
    [].forEach.call(list.querySelectorAll('a[data-img]'), function (a) {
      a.addEventListener('pointerenter', function () { pic.style.backgroundImage = 'url(' + a.getAttribute('data-img') + ')'; pic.classList.add('on'); });
      a.addEventListener('pointerleave', function () { pic.classList.remove('on'); });
    });
    list.addEventListener('pointermove', function (e) { pic.style.transform = 'translate(' + (e.clientX + 24) + 'px,' + (e.clientY - 120) + 'px)'; });
  }
})();
