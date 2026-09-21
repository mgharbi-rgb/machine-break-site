/* Maquettes G, H, I : plan complet de l'offre (« Tout ce qu'on fait »), section courante dans la navigation, filtre des machines par famille. */
(function () {
  var d = document, root = d.documentElement;

  // plan de l'offre : un ou plusieurs boutons [data-mega] pilotent le même panneau
  var mega = d.getElementById('tout'), toggles = [].slice.call(d.querySelectorAll('[data-mega]')), last = null;
  function setMega(open, focus) {
    root.classList.toggle('mega-open', open);
    toggles.forEach(function (b) { b.setAttribute('aria-expanded', open); });
    if (focus) (open ? mega.querySelector('a') : last || toggles[0]).focus();
  }
  if (mega) {
    toggles.forEach(function (b) { b.addEventListener('click', function () { last = b; setMega(!root.classList.contains('mega-open'), true); }); });
    mega.addEventListener('click', function (e) { if (e.target.closest('a')) setMega(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && root.classList.contains('mega-open')) setMega(false, true); });
    d.addEventListener('click', function (e) { if (root.classList.contains('mega-open') && !mega.contains(e.target) && !e.target.closest('[data-mega]')) setMega(false); });
  }

  // section courante : les liens [data-spy] reçoivent aria-current quand leur section est à l'écran
  var spies = [].slice.call(d.querySelectorAll('a[data-spy]'));
  if (spies.length && 'IntersectionObserver' in window) {
    var byId = {};
    spies.forEach(function (a) { var id = a.getAttribute('href').slice(1); (byId[id] = byId[id] || []).push(a); });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        spies.forEach(function (a) { a.removeAttribute('aria-current'); });
        (byId[e.target.id] || []).forEach(function (a) { a.setAttribute('aria-current', 'true'); if (a.closest('.tabs')) a.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'auto' }); });
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(byId).forEach(function (id) { var s = d.getElementById(id); if (s) io.observe(s); });
  }

  // filtre des machines
  var fb = [].slice.call(d.querySelectorAll('.filters button')), status = d.getElementById('filtre-etat');
  fb.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-filter'), n = 0;
      fb.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      [].forEach.call(d.querySelectorAll('.mach'), function (m) { var show = f === 'tout' || m.getAttribute('data-fam') === f; m.hidden = !show; if (show) { n++; m.classList.add('in'); } });
      if (status) status.textContent = n + (n > 1 ? ' machines affichées' : ' machine affichée');
    });
  });
})();
