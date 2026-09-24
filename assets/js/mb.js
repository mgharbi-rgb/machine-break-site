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

  // autocomplétion d'adresse : Base Adresse Nationale (api-adresse.data.gouv.fr), gratuite, sans clé ni cookie.
  // Un champ [data-adresse] ; data-cp et data-ville désignent les champs à remplir (code postal, ville).
  [].forEach.call(d.querySelectorAll('input[data-adresse]'), function (inp) {
    var list = d.createElement('ul'), cp = d.getElementById(inp.getAttribute('data-cp')), ville = d.getElementById(inp.getAttribute('data-ville')), timer, items = [], active = -1, last = '';
    list.className = 'sugg'; list.id = inp.id + '-sugg'; list.setAttribute('role', 'listbox'); list.hidden = true; inp.insertAdjacentElement('afterend', list);
    inp.setAttribute('role', 'combobox'); inp.setAttribute('aria-autocomplete', 'list'); inp.setAttribute('aria-expanded', 'false'); inp.setAttribute('aria-controls', list.id); inp.setAttribute('autocomplete', 'off');
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function close() { list.hidden = true; list.innerHTML = ''; items = []; active = -1; inp.setAttribute('aria-expanded', 'false'); }
    function pick(i) { var f = items[i]; if (!f) return; inp.value = f.properties.label; if (cp) cp.value = f.properties.postcode || ''; if (ville) ville.value = f.properties.city || ''; close(); }
    function render() { list.innerHTML = items.map(function (f, i) { return '<li role="option" id="' + list.id + '-' + i + '" aria-selected="' + (i === active) + '">' + esc(f.properties.label) + '</li>'; }).join(''); list.hidden = !items.length; inp.setAttribute('aria-expanded', items.length ? 'true' : 'false'); }
    function search(q) { if (!window.fetch) return; fetch('https://api-adresse.data.gouv.fr/search/?q=' + encodeURIComponent(q) + '&limit=5&autocomplete=1&lat=48.85&lon=2.5').then(function (r) { return r.ok ? r.json() : null; }).then(function (x) { if (!x || inp.value.trim() !== q) return; items = x.features || []; active = -1; render(); }).catch(close); }
    inp.addEventListener('input', function () { var q = inp.value.trim(); clearTimeout(timer); if (q.length < 3) { close(); return; } if (q === last) return; last = q; timer = setTimeout(function () { search(q); }, 250); });
    inp.addEventListener('keydown', function (e) { if (list.hidden) return; if (e.key === 'ArrowDown') { e.preventDefault(); active = (active + 1) % items.length; render(); } else if (e.key === 'ArrowUp') { e.preventDefault(); active = (active - 1 + items.length) % items.length; render(); } else if (e.key === 'Enter' && active > -1) { e.preventDefault(); pick(active); } else if (e.key === 'Escape') close(); });
    list.addEventListener('mousedown', function (e) { var li = e.target.closest('li'); if (li) { e.preventDefault(); pick(+li.id.split('-').pop()); } });
    inp.addEventListener('blur', function () { setTimeout(close, 120); });
  });

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
