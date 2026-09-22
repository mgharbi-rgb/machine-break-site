/* Machine Break · script du site : plan complet de l'offre, page courante dans le menu, apparitions au défilement, mini-machine de l'accueil. Sans dépendance. */
(function () {
  var d = document, root = d.documentElement, reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.remove('no-js');

  // plan de l'offre : un ou plusieurs boutons [data-mega] pilotent le même panneau
  var mega = d.getElementById('tout'), toggles = [].slice.call(d.querySelectorAll('[data-mega]')), last = null;
  function setMega(open, focus) {
    root.classList.toggle('mega-open', open);
    toggles.forEach(function (b) { b.setAttribute('aria-expanded', open); });
    if (focus) (open ? mega.querySelector('a') : last || toggles[0]).focus();
  }
  if (mega && toggles.length) {
    toggles.forEach(function (b) { b.addEventListener('click', function () { last = b; setMega(!root.classList.contains('mega-open'), true); }); });
    mega.addEventListener('click', function (e) { if (e.target.closest('a')) setMega(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && root.classList.contains('mega-open')) setMega(false, true); });
    d.addEventListener('click', function (e) { if (root.classList.contains('mega-open') && !mega.contains(e.target) && !e.target.closest('[data-mega]')) setMega(false); });
    // page courante signalée dans le plan
    var here = location.pathname.replace(/\.html$/, '').replace(/\/$/, '') || '/';
    [].forEach.call(mega.querySelectorAll('a[href]'), function (a) { var h = a.getAttribute('href').replace(/\.html$/, '').replace(/\/$/, '') || '/'; if (h === here) a.setAttribute('aria-current', 'page'); });
  }

  // formulaire : « Ce qui vous intéresse » présélectionné depuis le lien d'arrivée (?interet=cafe|chaud|frais)
  var sel = d.getElementById('interet'), val = new URLSearchParams(location.search).get('interet');
  if (sel && val && sel.querySelector('option[value="' + val + '"]')) { sel.value = val; var t = d.getElementById('form-t'); if (t) t.textContent = 'Trouver ma machine en 1 minute'; }
  var cfg = new URLSearchParams(location.search).get('config'), msg = d.getElementById('message'), det = d.getElementById('contactDetails');
  if (cfg && msg) { msg.value = cfg; if (det) det.open = true; }

  // apparitions au défilement
  var els = [].slice.call(d.querySelectorAll('.rv'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  // mini-machine liée au défilement (accueil) : trois cycles « se vide, seuil, passage déclenché, se re-remplit »
  var j = d.getElementById('jauge');
  if (j && !reduce) {
    var cells = [].slice.call(j.querySelectorAll('.mini i')), num = d.getElementById('jauge-n'), etat = d.getElementById('jauge-e'), tick = false;
    var upd = function () {
      tick = false;
      var h = root.scrollHeight - innerHeight, p = h > 0 ? Math.min(1, scrollY / h) : 0, c = p * 3, t = c - Math.floor(c), lvl, st;
      if (p === 0 || p >= .995) { lvl = 100; t = 0; st = 'Machine remplie, rien à faire'; }
      else if (t < .78) { lvl = 100 - 75 * (t / .78); st = lvl > 50 ? 'Machine remplie, rien à faire' : 'Le niveau baisse, la machine nous le dit'; }
      else { lvl = 25 + 75 * ((t - .78) / .22); st = t < .85 ? 'Seuil atteint : passage déclenché' : 'Réassort en cours, tout est tracé'; }
      var vides = Math.round(cells.length * (1 - lvl / 100));
      cells.forEach(function (x, i) { x.classList.toggle('off', i < vides); });
      num.textContent = Math.round(lvl) + ' %'; etat.textContent = st; j.classList.toggle('seuil', t >= .78 && t < .85);
    };
    addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true }); addEventListener('resize', upd); upd();
  } else if (j) { j.hidden = true; }
})();
