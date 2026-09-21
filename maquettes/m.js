/* Maquettes : sélecteur de direction, menu mobile, pause des animations, apparitions au défilement, halo qui suit le curseur (A), inclinaison des tuiles (B), image de survol (A/C). */
(function () {
  var d = document, root = d.documentElement, reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.remove('no-js');

  // sélecteur de direction, commun à toutes les maquettes
  var pages = [['a-nuit-cafe', 'A', 'Nuit café'], ['b-bento', 'B', 'Bento'], ['c-editorial', 'C', 'Éditorial'], ['d-connecte', 'D', 'Connecté'], ['e-affiche', 'E', 'Affiche'], ['f-immersif', 'F', 'Immersif'], ['g-distributeur', 'G', 'Distributeur'], ['h-sommaire', 'H', 'Sommaire'], ['i-planche', 'I', 'Planche']];
  var sw = d.createElement('nav'); sw.className = 'switch'; sw.setAttribute('aria-label', 'Directions de maquette');
  pages.forEach(function (p) {
    var a = d.createElement('a'), on = location.pathname.indexOf(p[0]) > -1;
    a.href = '/maquettes/' + p[0]; a.textContent = p[1]; a.title = p[2]; a.setAttribute('aria-label', 'Direction ' + p[1] + ' : ' + p[2]);
    if (on) { a.className = 'on'; a.setAttribute('aria-current', 'page'); var s = d.createElement('span'); s.textContent = ' · ' + p[2]; a.appendChild(s); }
    sw.appendChild(a);
  });
  d.body.appendChild(sw);

  // menu mobile : bouton ajouté ici, pour que les liens restent visibles sans JavaScript
  var header = d.querySelector('header.nav'), menu = header && header.querySelector('nav');
  if (menu) {
    var tg = d.createElement('button'); tg.type = 'button'; tg.className = 'nav-toggle';
    tg.setAttribute('aria-controls', menu.id); tg.setAttribute('aria-expanded', 'false'); tg.setAttribute('aria-label', 'Ouvrir le menu');
    tg.innerHTML = '<svg class="ic m" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg><svg class="ic x" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
    header.querySelector('.wrap').appendChild(tg);
    var setMenu = function (open, focus) {
      header.classList.toggle('open', open); tg.setAttribute('aria-expanded', open); tg.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
      if (focus) (open ? menu.querySelector('a') : tg).focus();
    };
    tg.addEventListener('click', function () { setMenu(!header.classList.contains('open'), true); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && header.classList.contains('open')) setMenu(false, true); });
    d.addEventListener('click', function (e) { if (header.classList.contains('open') && !header.contains(e.target)) setMenu(false); });
  }

  // pause des animations en boucle (inutile si le visiteur a déjà demandé moins de mouvement)
  if (!reduce) {
    var mt = d.createElement('button'), store = function (v) { try { if (v === undefined) return sessionStorage.getItem('mb-paused') === '1'; sessionStorage.setItem('mb-paused', v ? '1' : '0'); } catch (e) { return false; } };
    mt.type = 'button'; mt.className = 'motion-toggle';
    mt.innerHTML = '<svg class="pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z"/></svg><svg class="play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5l11 7-11 7z"/></svg>';
    var setPaused = function (p) { root.classList.toggle('paused', p); mt.setAttribute('aria-pressed', p); mt.setAttribute('aria-label', p ? 'Relancer les animations' : 'Mettre les animations en pause'); mt.title = mt.getAttribute('aria-label'); };
    setPaused(!!store());
    mt.addEventListener('click', function () { var p = !root.classList.contains('paused'); setPaused(p); store(p); });
    d.body.appendChild(mt);
  }

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
