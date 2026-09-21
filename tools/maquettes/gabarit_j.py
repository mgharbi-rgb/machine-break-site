# Gabarit de la page J (exécuté depuis generer.py, après gabarits_ghi.py).
# J · Enseigne : le mix. Affiche bordeaux et lettres pochoir (E), machine annotée et onglets de section (I),
# vitrine à codes (G), têtes de section numérotées (H), mini-machine qui se vide au défilement, bloc prix.
# Principes appliqués (voir le rapport) : première impression en 50 ms et faible complexité visuelle, un seul appel
# à l'action isolé par la couleur, groupes de quatre au plus, libellés à forte « odeur d'information », progression
# visible (gradient de but), curiosité entretenue par la jauge, prix expliqués en face de chaque machine.

VEND_CSS = G_CSS[G_CSS.index('/* la vitrine'):G_CSS.index('\n.machs')]

PINS_J = [
  ('1', '35%', '20%', 'Les rayons', 'Snacks, boissons fraîches, café en grains.', '/boissons-chaudes-snacks'),
  ('2', '85.5%', '25.5%', "L'écran", 'Six machines, leurs caractéristiques, leurs formules.', '#machines'),
  ('3', '35%', '61%', 'Le niveau', 'La machine nous prévient, nous passons avant la rupture.', '#fonctionnement'),
  ('4', '42%', '81.5%', 'La trappe', "Dépôt, location ou achat : trois façons de s'équiper.", '#formules'),
  ('5', '85.5%', '69%', 'Le boîtier connecté', 'Cinq engagements écrits au contrat, tout est tracé.', '#engagements'),
]
J_TABS = [('01', 'Tout ce qu\'on fait', '#offre'), ('02', 'Fonctionnement', '#fonctionnement'), ('03', 'Machines et prix', '#machines'), ('04', 'Formules', '#formules'), ('05', 'Engagements', '#engagements'), ('06', 'Secteurs', '#secteurs'), ('07', 'Zones', '#zones'), ('08', 'Questions', '#faq')]

J_CSS = '''
@font-face { font-family: "Big Shoulders Stencil"; src: url("/assets/fonts/Big Shoulders Stencil Display/BigShouldersStencilDisplay-latin.woff2") format("woff2"); font-weight: 800 900; font-display: swap; }
:root { --sh: 8px 8px 0 var(--ink); }
h1, h2, .st { font-family: "Big Shoulders Stencil", Impact, "HK Grotesk", sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: .005em; line-height: .88; }
.btn { box-shadow: 5px 5px 0 var(--ink); transition: transform .15s, box-shadow .15s, background .15s, color .15s; } .btn:hover { transform: translate(3px, 3px); box-shadow: 2px 2px 0 var(--ink); }

/* en-tête bordeaux, comme une enseigne */
.top { background: var(--mb); color: var(--cream); } .top .quick a, .top .tel { color: var(--cream); } .quick a:hover { border-bottom-color: var(--cream); }
.top .btn { background: var(--cream); border-color: var(--ink); color: var(--ink); box-shadow: 4px 4px 0 var(--ink); } .top .btn:hover { background: #fff; color: var(--ink); }
.tabs { position: sticky; top: var(--top-h); z-index: 50; background: var(--cream); border-bottom: 2px solid var(--ink); overflow-x: auto; scrollbar-width: none; } .tabs::-webkit-scrollbar { display: none; }
.tabs ul { display: flex; width: max-content; min-width: 100%; border-left: 1px solid var(--ink); }
.tabs a { display: flex; align-items: center; gap: .5rem; min-height: 48px; padding: 0 1.1rem; border-right: 1px solid var(--ink); text-decoration: none; font-weight: 600; font-size: .92rem; color: var(--ink); white-space: nowrap; }
.tabs a b { font-family: var(--mono); font-weight: 400; font-size: .72rem; color: var(--mb); }
.tabs a:hover, .tabs a.seen { background: var(--sand); } .tabs a.seen b::before { content: "✓ "; content: "✓ " / ""; }
.tabs a[aria-current] { background: var(--ink); color: #fff; } .tabs a[aria-current] b { color: #fff; }

/* ouverture : aplat bordeaux, lettres pochoir, machine annotée */
.hero { position: relative; overflow: hidden; background: var(--mb); color: var(--cream); padding: clamp(2rem, 4vw, 3.5rem) 0 0; }
.hero .main { display: grid; grid-template-columns: 1.7fr 1fr; align-items: end; gap: 1rem; }
.hero h1 { color: var(--cream); font-size: clamp(3.2rem, 8.4vw, 8.6rem); white-space: nowrap; padding-bottom: 1.6rem; }
.hero .lead { position: relative; z-index: 2; padding-bottom: 2.4rem; } .hero .lead .intro { margin: 0 0 1.5rem; color: rgba(250, 245, 241, .92); max-width: 36rem; }
.hero .lead .acts { align-items: center; gap: 1rem 1.6rem; }
.hero h1 .k { color: rgba(250, 245, 241, .85); white-space: normal; font-weight: 400; letter-spacing: .08em; }
.hero h1 .o { color: transparent; -webkit-text-stroke: 2px var(--cream); }
.hero h1 .b { display: inline-block; margin-top: .08em; padding: .05em .12em 0; background: var(--cream); color: var(--mb); box-shadow: var(--sh); }
.hero-side { position: relative; align-self: stretch; min-height: 600px; }
.disc { position: absolute; width: 118%; aspect-ratio: 1; left: -4%; bottom: -30%; border-radius: 50%; background: var(--sand); }
.mfig { position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); height: 104%; aspect-ratio: 536 / 940; filter: drop-shadow(18px 22px 0 rgba(31, 21, 23, .35)); } .mfig img { width: 100%; height: 100%; }
.pin { position: absolute; z-index: 2; left: var(--x); top: var(--y); width: 32px; height: 32px; margin: -16px 0 0 -16px; display: grid; place-items: center; background: var(--cream); color: var(--ink); border: 2px solid var(--ink); font-family: var(--mono); font-size: .82rem; text-decoration: none; transition: transform .15s, background .15s, color .15s; }
.pin.on, .pin:hover { background: var(--ink); color: #fff; transform: scale(1.2); }
.stamp { position: absolute; z-index: 3; left: -34px; top: 7%; padding: .7rem .9rem .5rem; background: var(--cream); color: var(--ink); border: 2px solid var(--ink); box-shadow: 6px 6px 0 var(--ink); rotate: -8deg; font-size: 1.5rem; text-align: center; }
.hero-foot { position: relative; z-index: 2; max-width: 60%; padding-bottom: 2.6rem; }
.hero .proofs { margin-top: 0; border-top-color: rgba(250, 245, 241, .45); } .hero .proofs dt { color: rgba(250, 245, 241, .7); } .hero .proofs dd { color: var(--cream); }
.hero .btn { background: var(--cream); border-color: var(--ink); color: var(--ink); } .hero .btn:hover { background: #fff; color: var(--ink); }
.cue { font-family: var(--mono); font-size: .76rem; letter-spacing: .04em; color: rgba(250, 245, 241, .8); max-width: 22rem; }
@media (max-width: 900px) { .hero .main { grid-template-columns: 1fr; } .hero h1 { font-size: 15.5vw; padding-bottom: 1.2rem; } .hero-side { min-height: 430px; margin: 0 -20px; overflow: hidden; border-bottom: 2px solid var(--ink); } .mfig { height: 100%; } .disc { width: 90%; left: 5%; } .stamp { left: 6%; font-size: 1.2rem; } .hero-foot { max-width: none; padding: 1.6rem 0 2.6rem; } .hero .lead { padding-bottom: .4rem; } }

/* légende des repères : cinq portes d'entrée, juste sous l'ouverture */
.callouts { display: grid; grid-template-columns: repeat(5, 1fr); background: var(--cream); border-bottom: 2px solid var(--ink); }
.callouts a { display: grid; grid-template-columns: 32px 1fr; gap: .8rem; height: 100%; padding: 1.1rem 1rem 1.2rem; border-right: 1px solid var(--ink); text-decoration: none; color: var(--ink); } .callouts li:first-child a { border-left: 1px solid var(--ink); }
.callouts b { display: grid; place-items: center; width: 32px; height: 32px; background: var(--ink); color: #fff; font-family: var(--mono); font-size: .82rem; font-weight: 400; }
.callouts strong { display: block; font-weight: 600; } .callouts span span { font-size: .9rem; color: var(--text); }
.callouts a:hover, .callouts a.on, .callouts a:focus-visible { background: var(--ink); color: #fff; } .callouts a:hover span span, .callouts a.on span span, .callouts a:focus-visible span span { color: rgba(255, 255, 255, .8); } .callouts a:hover b, .callouts a.on b { background: var(--cream); color: var(--ink); }
@media (max-width: 1000px) { .callouts { grid-template-columns: 1fr 1fr; } .callouts a { border-bottom: 1px solid var(--ink); border-left: 1px solid var(--ink); } } @media (max-width: 560px) { .callouts { grid-template-columns: 1fr; } }

/* bandeau incliné */
.marquee { overflow: hidden; white-space: nowrap; } .marquee > div { display: inline-flex; gap: 3rem; padding-right: 3rem; animation: marquee 34s linear infinite; } .marquee:hover > div { animation-play-state: paused; }
.marquee span::after { content: "■"; margin-left: 3rem; opacity: .5; font-size: .45em; vertical-align: middle; } @keyframes marquee { to { transform: translateX(-50%); } }
.strip { position: relative; z-index: 4; background: var(--ink); color: var(--cream); padding: .8rem 0; font-size: clamp(1.5rem, 3vw, 2.4rem); rotate: -1.4deg; margin: 1.6rem -2% 0; width: 104%; }

/* têtes de section, vitrine et blocs à ombre franche */
.sh h2 { font-size: clamp(2.9rem, 7vw, 6.6rem); }
.vend { max-width: 1040px; box-shadow: 12px 12px 0 var(--mb); }
.brief, .steps, .forms, .sect, .zone-card, .cmp table, .mach { box-shadow: var(--sh); } .cmp { padding: 0 10px 10px 0; }
.steps li::before { font-family: "Big Shoulders Stencil", Impact, sans-serif; font-weight: 900; font-size: 4.2rem; }
.machs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; align-items: start; }
.mach .pic { border-bottom: 2px solid var(--ink); } .mach .pic img { max-height: 250px; } .mach h3 { font-size: 1.45rem; } .mach .hi { border-top: 1px solid var(--line); background: var(--cream); }
.mach .key { display: block; margin: .7rem 0 .8rem; padding: 0; background: none; font-family: "Big Shoulders Stencil", Impact, sans-serif; font-weight: 900; font-size: 1.75rem; line-height: .95; text-transform: uppercase; color: var(--mb); }
@media (max-width: 1100px) { .machs { grid-template-columns: 1fr 1fr; } } @media (max-width: 680px) { .machs { grid-template-columns: 1fr; } }
#engagements { margin-top: clamp(4rem, 8vw, 7rem); padding-bottom: clamp(4rem, 8vw, 7rem); background: var(--ink); color: rgba(250, 245, 241, .8); }
#engagements .sh { border-top-color: var(--cream); } #engagements h2 { color: var(--cream); } #engagements .k { color: rgba(250, 245, 241, .7); }
#engagements .eng li { border-top-color: rgba(250, 245, 241, .3); color: var(--cream); font-family: "Big Shoulders Stencil", Impact, sans-serif; font-weight: 800; text-transform: uppercase; font-size: clamp(1.5rem, 2.6vw, 2.3rem); line-height: 1; letter-spacing: .01em; }
#engagements .eng li::before { color: var(--cream); font-family: var(--mono); font-weight: 400; } #engagements .eng li small { font-family: "HK Grotesk", sans-serif; text-transform: none; color: rgba(250, 245, 241, .75); margin-top: .5rem; }
.final h2 { font-size: clamp(3rem, 8vw, 7.4rem); } .final .btn { box-shadow: 6px 6px 0 var(--ink); }

/* la mini-machine : elle se vide quand on défile, atteint son seuil, déclenche le passage, se re-remplit */
.jauge { position: fixed; z-index: 98; left: 14px; bottom: 14px; width: 252px; display: grid; grid-template-columns: auto 1fr; gap: .8rem; align-items: center; padding: .7rem; background: var(--ink); color: var(--cream); border: 2px solid var(--cream); box-shadow: 5px 5px 0 var(--mb); font-size: .8rem; line-height: 1.25; }
.mini { width: 58px; padding: 4px; background: #0f0a0b; border: 2px solid var(--cream); display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px; }
.mini i { aspect-ratio: 1 / 1.3; background: var(--c, var(--cream)); transition: opacity .25s; } .mini i.off { opacity: .07; }
.mini u { grid-column: 1 / -1; height: 7px; margin-top: 2px; background: #3a2d30; }
.jauge .etat { display: block; } .jauge .k { display: block; color: rgba(250, 245, 241, .7); font-size: .6rem; } .jauge b { display: inline-block; font-family: "Big Shoulders Stencil", Impact, sans-serif; font-weight: 900; font-size: 1.8rem; line-height: 1; padding: 0 .15em; margin: .1rem 0; }
.jauge.seuil b { background: var(--cream); color: var(--ink); }
@media (max-width: 1180px) { .jauge { width: auto; bottom: 76px; left: 8px; padding: .4rem; gap: .5rem; } .jauge .k, .jauge .etat { display: none; } .mini { width: 40px; } .jauge b { font-size: 1.3rem; } }
'''

j_tabs = '<nav class="tabs" aria-label="Sections de la page"><div class="wrap"><ul>' + ''.join('<li><a data-spy href="%s"><b>%s</b>%s</a></li>' % (h, n, e(l)) for n, l, h in J_TABS) + '</ul></div></nav>\n'
j_fig = ('<div class="hero-side"><span class="disc"></span><div class="mfig">' + img('/assets/img/machines/siline-combi-m.webp', 'Distributeur combiné snacks et boissons fraîches Sielaff SiLine installé par Machine Break', lazy=False)
         + ''.join('<a class="pin" href="%s" style="--x:%s;--y:%s" data-n="%s" aria-hidden="true" tabindex="-1">%s</a>' % (h, x, y, n, n) for n, x, y, t, d, h in PINS_J)
         + '</div><span class="stamp st">Diagnostic<br>gratuit<br>1 min</span></div>')
j_hero = ('<main id="contenu">\n<section class="hero" aria-labelledby="h1">\n  <div class="wrap main">\n    <div class="lead"><h1 id="h1"><span class="k">' + e(KICKER) + '</span>La pause<br><span class="o">qui se gère</span><br><span class="b">toute seule.</span></h1>\n'
          '      <p class="intro">' + e(LEAD) + '</p><div class="acts"><a class="btn" href="/contact#contact-form">Mon diagnostic pause en 1 minute</a><p class="cue">↓ Faites défiler : la machine en bas de l\'écran se vide. Regardez ce qui se passe au seuil.</p></div></div>\n    ' + j_fig + '\n  </div>\n'
          '  <div class="wrap"><div class="hero-foot"><dl class="proofs">' + ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in PROOFS) + '</dl></div></div>\n</section>\n'
          '<ol class="callouts" aria-label="Cinq repères sur la machine, cinq entrées dans le site">' + ''.join('<li><a href="%s" data-n="%s"><b aria-hidden="true">%s</b><span><strong>%s</strong><span>%s</span></span></a></li>' % (h, n, n, e(t), e(d)) for n, x, y, t, d, h in PINS_J) + '</ol>\n'
          '<div class="marquee strip st" aria-hidden="true"><div>' + ''.join('<span>%s</span>' % w for w in ['Café en grains', 'Boissons fraîches', 'Snacks', 'Sans contact', 'Télémétrie', 'Espace client'] * 2) + '</div></div>\n')
j_offre = ('<section id="offre" aria-labelledby="offre-t"><div class="wrap">\n  ' + sh('01', "Tout ce qu'on fait", 'Servez-vous.', "Douze cases, trois rangées : ce qu'on sert, ce qu'on installe, ce qu'on gère. Touchez une case, ou tapez son code.", 'offre-t') + '\n  ' + g_vend() + '\n</div></section>\n')

cells = ''.join('<i style="--c:%s"></i>' % c for c in (['var(--cream)', '#b9956f', 'var(--sand)', '#8f4f5a'] * 5))
j_jauge = '<div class="jauge" id="jauge" aria-hidden="true"><div class="mini">' + cells + '<u></u></div><div><span class="k">Télémétrie · la machine</span><b id="jauge-n">100 %</b><span class="etat" id="jauge-e">Machine remplie, rien à faire</span></div></div>\n'

J_JS = '''<script>
(function () {
  // mini-machine liée au défilement : trois cycles « se vide, seuil, passage déclenché, se re-remplit » sur la hauteur de la page
  var j = document.getElementById('jauge'), cells = [].slice.call(j.querySelectorAll('.mini i')), num = document.getElementById('jauge-n'), etat = document.getElementById('jauge-e'), tick = false;
  function upd() {
    tick = false;
    var h = document.documentElement.scrollHeight - innerHeight, p = h > 0 ? Math.min(1, scrollY / h) : 0, c = p * 3, t = c - Math.floor(c), lvl, st;
    if (p === 0 || p >= .995) { lvl = 100; t = 0; st = 'Machine remplie, rien à faire'; }
    else if (t < .78) { lvl = 100 - 75 * (t / .78); st = lvl > 50 ? 'Machine remplie, rien à faire' : 'Le niveau baisse, la machine nous le dit'; }
    else { lvl = 25 + 75 * ((t - .78) / .22); st = t < .85 ? 'Seuil atteint : passage déclenché' : 'Réassort en cours, tout est tracé'; }
    var vides = Math.round(cells.length * (1 - lvl / 100));
    cells.forEach(function (x, i) { x.classList.toggle('off', i < vides); });
    num.textContent = Math.round(lvl) + ' %'; etat.textContent = st; j.classList.toggle('seuil', t >= .78 && t < .85);
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true }); addEventListener('resize', upd); upd();

  // progression visible : un onglet déjà parcouru reste coché
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (!x.isIntersecting) return; var a = document.querySelector('.tabs a[href="#' + x.target.id + '"]'); if (a) a.classList.add('seen'); }); }, { rootMargin: '0px 0px -50% 0px' });
    [].forEach.call(document.querySelectorAll('.tabs a'), function (a) { var s = document.getElementById(a.getAttribute('href').slice(1)); if (s) io.observe(s); });
  }
})();
</script>
'''

s_j = (head('J', 'Enseigne', HERO_CSS + VEND_CSS + J_CSS, '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/Big Shoulders Stencil Display/BigShouldersStencilDisplay-latin.woff2" crossorigin>\n<link rel="preload" as="image" href="/assets/img/machines/siline-combi-m.webp" fetchpriority="high">\n')
       + '<body>\n' + header('/assets/img/logoblanc.webp') + j_tabs + j_hero + j_offre + brief() + fonctionnement('02') + machines('03', prix=True) + formules('04') + engagements('05') + secteurs('06') + zones('07') + faq('08')
       + final_footer('J', 'Enseigne') + j_jauge + G_JS + I_JS + J_JS + '<script src="/maquettes/m.js"></script>\n</body>\n</html>\n')
s_j = s_j.replace('<p class="k">03 — Les machines</p><h2 id="mach-t" class="rv">Six machines, trois familles.</h2>', '<p class="k">03 — Les machines et leurs prix</p><h2 id="mach-t" class="rv">Six machines, trois familles.</h2>')
(OUT / 'j-enseigne.html').write_text(s_j, encoding='utf-8'); print('j-enseigne.html', len(s_j) // 1024, 'Ko')
