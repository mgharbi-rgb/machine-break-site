# Gabarits des pages G, H, I (exécuté depuis generer.py, qui fournit les blocs communs).

def page(fname, letter, name, css, body_open, hero, sections, extra_js='', preload=''):
    s = head(letter, name, HERO_CSS + css, preload) + body_open + header() + hero + sections + final_footer(letter, name) + extra_js + '<script src="/maquettes/m.js"></script>\n</body>\n</html>\n'
    (OUT / fname).write_text(s, encoding='utf-8')
    print(fname, len(s) // 1024, 'Ko')

# =====================================================================================================
# G · Distributeur : la page d'accueil est une vitrine de distributeur, chaque case est une offre
# =====================================================================================================
SLOTS = [
  ("A — Ce qu'on sert", [
    ('A1', 'Café en grains', '/boissons-chaudes-snacks', '/assets/img/maquette/grains.webp', 'Grains de café', 'Moulu à la demande, dans toutes nos machines à café.', ''),
    ('A2', 'Boissons chaudes', '/boissons-chaudes-snacks', '/assets/img/shooting/espresso-tasse-verre-640.webp', 'Espresso servi en tasse de verre', 'Espresso, café filtre, recettes gourmandes.', ''),
    ('A3', 'Boissons fraîches', '/boissons-chaudes-snacks', '/assets/img/shooting/canettes-distributeur-640.webp', 'Canettes dans un distributeur', 'Canettes, bouteilles, briques.', ''),
    ('A4', 'Snacks', '/boissons-chaudes-snacks', '/assets/img/shooting/hall-distributeurs-640.webp', 'Distributeurs de snacks dans un hall', 'Snacks, avec des références bio et sans gluten.', '')]),
  ("B — Ce qu'on installe", [
    ('B1', 'Machines à café en grains', '#machines', '/assets/img/machines/animo-optibean-x-640.webp', 'Machine à café en grains Animo OptiBean X', 'Animo OptiBean X et OptiMe X.', 'contain'),
    ('B2', 'Distributeurs de boissons chaudes', '#machines', '/assets/img/machines/bianchi-agily-640.webp', 'Distributeur de boissons chaudes Bianchi Agily', 'Bianchi Agily et Intuity, à grand écran.', 'contain'),
    ('B3', 'Distributeurs frais et snacks', '#machines', '/assets/img/machines/sielaff-robimat-640.webp', 'Distributeur de boissons fraîches Sielaff Robimat X', 'Sielaff Robimat X et SiLine, à ascenseur.', 'contain'),
    ('B4', 'Dépôt, location, achat', '#formules', '/assets/img/shooting/ecran-accueil-distributeur-640.webp', "Écran d'accueil d'un distributeur", 'Trois formules, pour chaque machine.', '')]),
  ("C — Ce qu'on gère", [
    ('C1', 'Télémétrie et espace client', '#fonctionnement', '/assets/img/plateforme/espace-client-apercu.webp', "Aperçu de l'espace client Machine Break", 'La machine nous prévient, vous voyez tout.', ''),
    ('C2', 'Votre secteur', '#secteurs', '/assets/img/shooting/espace-pause-bureau-640.webp', 'Espace de pause dans des bureaux', 'Bureaux, résidences, industrie, multi-sites.', ''),
    ('C3', 'Grands comptes', '/grands-comptes', '/assets/img/maquette/salle.webp', "Salle de restauration d'entreprise", 'Plusieurs sites, un interlocuteur nommé.', ''),
    ('C4', "Zones d'intervention", '#zones', None, '', "Paris et toute l'Île-de-France.", 'txt')]),
]

G_CSS = '''
.hero { padding: clamp(2rem, 4vw, 3.5rem) 0 0; }
.hero .wrap { display: grid; grid-template-columns: 5fr 7fr; gap: clamp(2rem, 4vw, 4rem); align-items: start; }
h1 { font-size: clamp(2.7rem, 5.2vw, 5rem); }
h1 .u { background: linear-gradient(var(--mb), var(--mb)) 0 94% / 100% .11em no-repeat; }
@media (max-width: 1000px) { .hero .wrap { grid-template-columns: 1fr; } }

/* la vitrine : tout ce qu'on fait, rangé comme dans un distributeur */
.vend { background: var(--ink); border: 3px solid var(--ink); color: #fff; }
.vend-head { display: flex; justify-content: space-between; gap: 1rem; padding: .7rem .9rem; font-family: var(--mono); font-size: .74rem; letter-spacing: .08em; text-transform: uppercase; }
.led::before { content: ""; display: inline-block; width: 8px; height: 8px; background: #5fd39a; margin-right: .5rem; animation: blink 2.4s steps(2, jump-none) infinite; }
@keyframes blink { 50% { opacity: .25; } }
.slots { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3px; padding: 0 3px; }
.rowt { grid-column: 1 / -1; margin: 0; padding: .4rem .7rem; font-family: var(--mono); font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; color: rgba(255, 255, 255, .78); background: #33262a; }
.slot { display: flex; flex-direction: column; background: var(--cream); color: var(--ink); text-decoration: none; transition: opacity .15s; }
.slot img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; } .slot.contain img { object-fit: contain; background: #fff; padding: .5rem; }
.slot-txt { display: grid; place-items: center; aspect-ratio: 4 / 3; background: var(--sand); color: var(--ink); font-family: var(--mono); font-size: clamp(.8rem, 1.25vw, 1.05rem); line-height: 1.7; text-align: center; letter-spacing: .04em; }
.slot .lab { flex: 1; display: grid; grid-template-columns: auto 1fr; border-top: 2px solid var(--ink); min-height: 3.5rem; }
.slot .lab b { display: grid; place-items: center; padding: 0 .55rem; background: var(--mb); color: #fff; font-family: var(--mono); font-size: .8rem; font-weight: 400; }
.slot .lab span { display: flex; align-items: center; padding: .45rem .6rem; font-weight: 600; font-size: .9rem; line-height: 1.2; }
.slot:hover .lab, .slot:focus-visible .lab, .slot.sel .lab { background: var(--ink); color: #fff; }
.slot.sel { outline: 4px solid var(--mb); outline-offset: -4px; }
.vend[data-row] .slot { opacity: .35; } .vend[data-row="A"] .slot[data-code^="A"], .vend[data-row="B"] .slot[data-code^="B"], .vend[data-row="C"] .slot[data-code^="C"] { opacity: 1; }
.console { display: grid; grid-template-columns: 1fr auto; gap: 3px; padding: 3px; }
.screen { margin: 0; background: #0f0a0b; color: #f3e9e2; font-family: var(--mono); font-size: .86rem; line-height: 1.45; padding: .85rem 1rem; min-height: 5.6rem; } .screen b { color: #fff; font-weight: 400; background: var(--mb); padding: 0 .35rem; margin-right: .3rem; }
.pad { display: grid; grid-template-columns: repeat(4, 44px); grid-auto-rows: 44px; gap: 3px; }
.pad button { border: 0; background: #3a2d30; color: #fff; font-family: var(--mono); cursor: pointer; } .pad button:hover { background: var(--mb); } .pad .ok { background: var(--mb); } .pad .ok:hover { background: #fff; color: var(--ink); }
@media (max-width: 700px) { .slots { grid-template-columns: 1fr 1fr; } .pad { display: none; } .console { grid-template-columns: 1fr; } .screen { min-height: 0; } }

.machs { display: grid; gap: 16px; }
.mach { display: grid; grid-template-columns: 220px 1.15fr 1fr; } .mach .pic { border-right: 2px solid var(--ink); } .mach .hi { border-left: 1px solid var(--line); background: var(--cream); } .mach details { grid-column: 1 / -1; }
@media (max-width: 1000px) { .mach { grid-template-columns: 160px 1fr; } .mach .hi { grid-column: 1 / -1; border-left: 0; border-top: 1px solid var(--line); } }
@media (max-width: 600px) { .mach { grid-template-columns: 1fr; } .mach .pic { border-right: 0; border-bottom: 2px solid var(--ink); } }
'''

def g_vend():
    rows = []
    for title, slots in SLOTS:
        rows.append('<p class="rowt">%s</p>' % e(title))
        for code, label, href, src, alt, desc, cls in slots:
            pic = img(src, alt, lazy=code not in ('A1', 'A2', 'A3', 'A4')) if src else '<span class="slot-txt" aria-hidden="true">75 · 77 · 78<br>91 · 92 · 93<br>94 · 95</span>'
            rows.append('<a class="slot %s" href="%s" data-code="%s" data-desc="%s">%s<span class="lab"><b>%s</b><span>%s</span></span></a>' % (cls, href, code, e(desc), pic, code, e(label)))
    return '''<div class="vend" id="vitrine" role="group" aria-labelledby="vend-t">
    <div class="vend-head"><span id="vend-t">Tout ce qu'on fait, en vitrine</span><span class="led">En service</span></div>
    <div class="slots">%s</div>
    <div class="console"><p class="screen" id="ecran" aria-live="polite">Choisissez une case. Au clavier, une fois dans la vitrine : une lettre puis un chiffre, par exemple B2.</p>
      <div class="pad" role="group" aria-label="Clavier du distributeur"><button type="button" data-k="A">A</button><button type="button" data-k="B">B</button><button type="button" data-k="C">C</button><button type="button" class="ok" data-k="OK">OK</button><button type="button" data-k="1">1</button><button type="button" data-k="2">2</button><button type="button" data-k="3">3</button><button type="button" data-k="4">4</button></div></div>
  </div>''' % ''.join(rows)

G_JS = '''<script>
(function () {
  // la vitrine : survol ou focus décrit la case ; lettre puis chiffre la sélectionne ; OK ou Entrée ouvre. Les touches ne sont écoutées que dans la vitrine.
  var v = document.getElementById('vitrine'), ecran = document.getElementById('ecran'), slots = [].slice.call(v.querySelectorAll('.slot')), row = '', sel = null, base = ecran.textContent;
  function show(s) { ecran.innerHTML = '<b>' + s.getAttribute('data-code') + '</b>' + s.querySelector('.lab span').textContent + '. ' + s.getAttribute('data-desc'); }
  function pick(s) { slots.forEach(function (x) { x.classList.remove('sel'); }); sel = s; s.classList.add('sel'); v.removeAttribute('data-row'); row = ''; show(s); ecran.innerHTML += ' Entrée ou OK pour ouvrir.'; s.focus(); }
  function key(k) {
    k = k.toUpperCase();
    if (/^[ABC]$/.test(k)) { row = k; v.setAttribute('data-row', k); ecran.innerHTML = '<b>' + k + '_</b>Rangée ' + k + ' : tapez un chiffre de 1 à 4.'; return true; }
    if (/^[1-4]$/.test(k) && row) { pick(v.querySelector('[data-code="' + row + k + '"]')); return true; }
    if (k === 'OK' && sel) { location.href = sel.href; return true; }
    if (k === 'ESCAPE') { row = ''; v.removeAttribute('data-row'); ecran.textContent = base; return true; }
    return false;
  }
  v.addEventListener('keydown', function (e) { if (e.metaKey || e.ctrlKey || e.altKey) return; if (key(e.key)) e.preventDefault(); });
  [].forEach.call(v.querySelectorAll('.pad button'), function (b) { b.addEventListener('click', function () { key(b.getAttribute('data-k')); }); });
  slots.forEach(function (s) { s.addEventListener('pointerenter', function () { show(s); }); s.addEventListener('focus', function () { if (s !== sel) show(s); }); });
})();
</script>
'''

page('g-distributeur.html', 'G', 'Distributeur', G_CSS, '<body>\n',
     '<main id="contenu">\n<section class="hero" aria-labelledby="h1"><div class="wrap">\n  <div>' + hero_text('La pause qui se gère <span class="u">toute seule.</span>') + '</div>\n  ' + g_vend() + '\n</div></section>\n',
     brief() + fonctionnement('01') + machines('02') + formules('03') + engagements('04') + secteurs('05') + zones('06') + faq('07'), G_JS)

# =====================================================================================================
# H · Sommaire : éditorial suisse, index latéral permanent et grand sommaire numéroté
# =====================================================================================================
H_NAV = [('01', 'Fonctionnement', '#fonctionnement'), ('02', 'Les machines', '#machines'), ('03', 'Les formules', '#formules'), ('04', 'Nos engagements', '#engagements'), ('05', 'Votre secteur', '#secteurs'), ('06', "Zones d'intervention", '#zones'), ('07', 'Questions fréquentes', '#faq')]
H_INDEX = [('Fonctionnement', '#fonctionnement', 'La machine nous prévient, nous passons avant la rupture.'), ('Les machines', '#machines', 'Six modèles, leurs caractéristiques, pour quels sites.'), ('Les formules', '#formules', 'Dépôt, location ou achat, comparés ligne à ligne.'), ('Boissons et snacks', '/boissons-chaudes-snacks', 'Café en grains, boissons fraîches, snacks, références bio.'), ('Votre secteur', '#secteurs', 'Bureaux, résidences, industrie, grands comptes.'), ("Zones d'intervention", '#zones', "Paris et toute l'Île-de-France."), ('Questions fréquentes', '#faq', 'Installation, réassort, panne, délais.'), ('Mon diagnostic en 1 minute', '/contact#contact-form', 'Une réponse sous 24 h.')]

H_CSS = '''
:root { --side: 288px; }
.side { display: none; }
@media (min-width: 1101px) {
  :root { --top-h: 0px; }
  .top { display: none; }
  .side { display: flex; flex-direction: column; position: fixed; inset: 0 auto 0 0; width: var(--side); z-index: 61; background: var(--cream); border-right: 2px solid var(--ink); padding: 1.6rem 1.4rem; overflow-y: auto; }
  main, .final, .site { margin-left: var(--side); } .wrap { width: min(1180px, 100% - 96px); }
  .mega { left: var(--side); top: 0; max-height: 100dvh; } .mega .wrap { width: calc(100% - 64px); }
  .switch { left: calc(50% + var(--side) / 2); }
  [id] { scroll-margin-top: 32px; }
}
.side .logo img { height: 56px; width: auto; }
.side nav { margin: 2rem 0 1.4rem; } .side nav .k { display: block; margin-bottom: .7rem; }
.side ol a { display: grid; grid-template-columns: 2.2rem 1fr; align-items: baseline; padding: .5rem .6rem; margin-left: -.6rem; border-left: 3px solid transparent; text-decoration: none; font-weight: 600; color: var(--ink); }
.side ol a b { font-family: var(--mono); font-weight: 400; font-size: .74rem; color: var(--muted); }
.side ol a:hover { background: var(--sand); } .side ol a[aria-current] { border-left-color: var(--mb); background: var(--sand); color: var(--mb); }
.side .all { width: 100%; justify-content: center; }
.side-foot { margin-top: auto; padding-top: 1.4rem; display: grid; gap: .6rem; } .side-foot .tel { font-family: var(--mono); color: var(--ink); text-decoration: none; padding: .5rem 0; } .side-foot .btn { justify-content: space-between; }

.hero { padding: clamp(2.5rem, 5vw, 4.5rem) 0 0; }
h1 { font-size: clamp(3rem, 7vw, 7.4rem); line-height: .94; letter-spacing: -.045em; } h1 .u { color: var(--mb); }
.hero-grid { display: grid; grid-template-columns: 5fr 7fr; gap: 3rem; margin-top: 2.4rem; padding-top: 1.4rem; border-top: 2px solid var(--ink); align-items: start; }
.hero-grid .intro { margin-top: 0; } .hero figure img { width: 100%; aspect-ratio: 16 / 10; object-fit: cover; object-position: 70% 40%; }
figcaption.cap { font-family: var(--mono); font-size: .74rem; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-top: .6rem; }
@media (max-width: 900px) { .hero-grid { grid-template-columns: 1fr; gap: 2rem; } }

/* le sommaire : toute l'offre, numérotée, une ligne par sujet */
.index { border-top: 2px solid var(--ink); counter-reset: i; }
.index li { border-bottom: 1px solid var(--ink); counter-increment: i; }
.index a { display: grid; grid-template-columns: 4rem 1.1fr 1fr 2rem; gap: 1.5rem; align-items: baseline; padding: 1.25rem .8rem; text-decoration: none; color: var(--ink); transition: background .15s, color .15s, padding-left .2s; }
.index a::before { content: "0" counter(i); font-family: var(--mono); font-size: .85rem; color: var(--mb); }
.index strong { font-weight: 500; font-size: clamp(1.5rem, 2.9vw, 2.6rem); letter-spacing: -.03em; line-height: 1.05; }
.index span { color: var(--text); } .index i { font-style: normal; text-align: right; }
.index a:hover, .index a:focus-visible { background: var(--mb); color: #fff; padding-left: 1.4rem; } .index a:hover::before, .index a:hover span, .index a:focus-visible::before, .index a:focus-visible span { color: #fff; }
@media (max-width: 800px) { .index a { grid-template-columns: 2.6rem 1fr; gap: .2rem 1rem; } .index span { grid-column: 2; } .index i { display: none; } }

.pull { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center; margin-top: 3rem; }
.pull p { font-size: clamp(1.7rem, 3.2vw, 2.9rem); line-height: 1.08; letter-spacing: -.03em; color: var(--ink); font-weight: 500; padding-left: 1.4rem; border-left: 6px solid var(--mb); }
.pull img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; }
@media (max-width: 800px) { .pull { grid-template-columns: 1fr; gap: 1.6rem; } }

.machs { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start; }
.mach { display: grid; grid-template-columns: 150px 1fr; } .mach .pic { border-right: 2px solid var(--ink); } .mach .pic img { max-height: 230px; } .mach .hi { grid-column: 1 / -1; border-top: 1px solid var(--line); background: var(--cream); } .mach details { grid-column: 1 / -1; } .mach h3 { font-size: 1.45rem; }
@media (max-width: 1350px) { .machs { grid-template-columns: 1fr; } } @media (max-width: 560px) { .mach { grid-template-columns: 1fr; } .mach .pic { border-right: 0; border-bottom: 2px solid var(--ink); } }
'''

h_side = '<aside class="side" aria-label="Sommaire">\n  <a class="logo" href="/" aria-label="Machine Break, accueil">' + img('/assets/img/logo.webp', 'Machine Break', lazy=False) + '</a>\n  <nav aria-label="Sections de la page"><span class="k">Sur cette page</span><ol>' + ''.join('<li><a data-spy href="%s"><b>%s</b>%s</a></li>' % (h, n, e(l)) for n, l, h in H_NAV) + '</ol></nav>\n  <button class="all" type="button" data-mega aria-expanded="false" aria-controls="tout"><svg class="m" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg><svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>Tout ce qu\'on fait</button>\n  <div class="side-foot"><a class="tel" href="tel:+33174810952">01 74 81 09 52</a><a class="btn btn-mb" href="/contact#contact-form">Mon diagnostic</a></div>\n</aside>\n'
h_hero = ('<main id="contenu">\n<section class="hero" aria-labelledby="h1"><div class="wrap">\n  <h1 id="h1"><span class="k">' + e(KICKER) + '</span>La pause qui se gère <span class="u">toute seule.</span></h1>\n  <div class="hero-grid"><div><p class="intro">' + e(LEAD) + '</p><div class="acts"><a class="btn btn-mb" href="/contact#contact-form">Mon diagnostic pause en 1 minute</a></div><dl class="proofs">' + ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in PROOFS) + '</dl></div>\n    <figure>' + img('/assets/img/maquette/pour-wide.webp', 'Café en grains qui coule dans un gobelet, sur une machine installée par Machine Break', lazy=False) + '<figcaption class="cap">Fig. 1 — Café en grains, moulu à la demande</figcaption></figure></div>\n</div></section>\n'
          '<section id="sommaire" aria-labelledby="som-t"><div class="wrap">\n  <div class="sh"><p class="k">Sommaire</p><h2 id="som-t" class="rv">Tout ce qu\'on fait, en huit lignes.</h2><p class="rv">Chaque ligne mène au sujet. Rien n\'est caché dans un sous-menu.</p></div>\n  <ol class="index">' + ''.join('<li class="rv"><a href="%s"><strong>%s</strong><span>%s</span><i aria-hidden="true">→</i></a></li>' % (h, e(t), e(d)) for t, h, d in H_INDEX) + '</ol>\n</div></section>\n')
h_pull = '\n  <div class="pull rv"><p>Pas de tournée à date fixe. C\'est la machine qui déclenche nos passages.</p>' + img('/assets/img/maquette/refill.webp', "Un technicien Machine Break remplit le bac à grains d'une machine à café") + '</div>'

s_h =head('H', 'Sommaire', HERO_CSS + H_CSS, '<link rel="preload" as="image" href="/assets/img/maquette/pour-wide.webp" fetchpriority="high">\n') + '<body>\n' + header() + h_side + h_hero + brief() + fonctionnement('01', h_pull) + machines('02') + formules('03') + engagements('04') + secteurs('05') + zones('06') + faq('07') + final_footer('H', 'Sommaire') + '<script src="/maquettes/m.js"></script>\n</body>\n</html>\n'
(OUT / 'h-sommaire.html').write_text(s_h, encoding='utf-8'); print('h-sommaire.html', len(s_h) // 1024, 'Ko')

# =====================================================================================================
# I · Planche : planche technique, machine annotée dont chaque repère mène à une partie de l'offre
# =====================================================================================================
I_TABS = [('01', 'Fonctionnement', '#fonctionnement'), ('02', 'Machines', '#machines'), ('03', 'Formules', '#formules'), ('04', 'Engagements', '#engagements'), ('05', 'Secteurs', '#secteurs'), ('06', 'Zones', '#zones'), ('07', 'Questions', '#faq')]
PINS = [
  ('1', '50%', '4.5%', 'Le bac à grains', 'Réassort déclenché par la télémétrie, avant la rupture.', '#fonctionnement'),
  ('2', '50%', '33%', "L'écran", 'Six machines, du plateau de bureaux au site industriel.', '#machines'),
  ('3', '83%', '50%', 'Le boîtier connecté', 'Ventes, remplissage, alertes : tout remonte, tout est tracé.', '#engagements'),
  ('4', '50%', '69%', 'Les becs', 'Café en grains, boissons fraîches et snacks.', '/boissons-chaudes-snacks'),
  ('5', '50%', '92%', 'Le socle', "Dépôt, location ou achat : l'entretien est assuré par nos équipes.", '#formules'),
]

I_CSS = '''
body { background-image: linear-gradient(rgba(117, 63, 72, .07) 1px, transparent 1px), linear-gradient(90deg, rgba(117, 63, 72, .07) 1px, transparent 1px); background-size: 32px 32px; }
.tabs { position: sticky; top: var(--top-h); z-index: 50; background: var(--cream); border-bottom: 2px solid var(--ink); overflow-x: auto; scrollbar-width: none; } .tabs::-webkit-scrollbar { display: none; }
.tabs ul { display: flex; width: max-content; min-width: 100%; border-left: 1px solid var(--ink); }
.tabs a { display: flex; align-items: center; gap: .5rem; min-height: 48px; padding: 0 1.1rem; border-right: 1px solid var(--ink); text-decoration: none; font-weight: 600; font-size: .92rem; color: var(--ink); white-space: nowrap; }
.tabs a b { font-family: var(--mono); font-weight: 400; font-size: .72rem; color: var(--mb); }
.tabs a:hover { background: var(--sand); } .tabs a[aria-current] { background: var(--ink); color: #fff; } .tabs a[aria-current] b { color: #fff; }

.hero { padding: clamp(2rem, 4vw, 3.5rem) 0 0; }
.hero .wrap { display: grid; grid-template-columns: 1.2fr .78fr 1fr; gap: clamp(1.5rem, 3vw, 3rem); align-items: center; }
h1 { font-size: clamp(2.6rem, 4.4vw, 4.4rem); } h1 .u { color: var(--mb); }
.plate { position: relative; background: #fff; border: 2px solid var(--ink); padding: 1.2rem 1.2rem 0; }
.plate .fig { position: relative; aspect-ratio: 483 / 900; } .plate .fig img { width: 100%; height: 100%; object-fit: contain; }
.plate .ln { position: absolute; left: var(--x); right: -1.2rem; top: var(--y); border-top: 1px dashed var(--mb); }
.pin { position: absolute; z-index: 2; left: var(--x); top: var(--y); width: 30px; height: 30px; margin: -15px 0 0 -15px; display: grid; place-items: center; background: var(--mb); color: #fff; border: 2px solid #fff; font-family: var(--mono); font-size: .8rem; text-decoration: none; transition: transform .15s, background .15s; }
.pin.on, .pin:hover { background: var(--ink); transform: scale(1.2); }
.cart { margin: 1rem -1.2rem 0; border-top: 2px solid var(--ink); display: grid; grid-template-columns: 1fr auto; font-family: var(--mono); font-size: .7rem; letter-spacing: .06em; text-transform: uppercase; color: var(--ink); }
.cart span { padding: .55rem .8rem; } .cart span + span { border-left: 2px solid var(--ink); }
.callouts li a { display: grid; grid-template-columns: 30px 1fr; gap: .9rem; padding: .85rem .6rem; border-top: 1px solid var(--ink); text-decoration: none; color: var(--ink); }
.callouts li:last-child a { border-bottom: 1px solid var(--ink); }
.callouts b { display: grid; place-items: center; width: 30px; height: 30px; background: var(--mb); color: #fff; font-family: var(--mono); font-size: .8rem; font-weight: 400; }
.callouts strong { display: block; font-weight: 600; } .callouts span { font-size: .93rem; color: var(--text); }
.callouts a:hover, .callouts a.on, .callouts a:focus-visible { background: var(--ink); color: #fff; } .callouts a:hover span, .callouts a.on span, .callouts a:focus-visible span { color: rgba(255, 255, 255, .8); }
@media (max-width: 1100px) { .hero .wrap { grid-template-columns: 1fr 1fr; } .hero .wrap > div:first-child { grid-column: 1 / -1; } }
@media (max-width: 640px) { .hero .wrap { grid-template-columns: 1fr; } .plate { max-width: 300px; margin-inline: auto; } }

/* têtes de section en cartouche de plan */
.sh { background: #fff; border: 2px solid var(--ink); padding: 0; gap: 0; grid-template-columns: 1.2fr 1fr; align-items: stretch; }
.sh .k { padding: .55rem 1.2rem; background: var(--ink); color: #fff; max-width: none; } .sh h2 { padding: 1.4rem 1.2rem; font-size: clamp(1.9rem, 3.6vw, 3.1rem); align-self: center; }
.sh p:last-child { padding: 1.4rem 1.2rem; border-left: 2px solid var(--ink); display: flex; align-items: center; max-width: none; }
@media (max-width: 800px) { .sh p:last-child { border-left: 0; border-top: 2px solid var(--ink); } }

.machs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; align-items: start; }
.mach .pic { border-bottom: 2px solid var(--ink); background-image: linear-gradient(rgba(117, 63, 72, .07) 1px, transparent 1px), linear-gradient(90deg, rgba(117, 63, 72, .07) 1px, transparent 1px); background-size: 16px 16px; } .mach .pic img { max-height: 260px; mix-blend-mode: multiply; }
.mach h3 { font-size: 1.45rem; } .mach .hi { border-top: 1px solid var(--line); background: var(--cream); }
@media (max-width: 1100px) { .machs { grid-template-columns: 1fr 1fr; } } @media (max-width: 680px) { .machs { grid-template-columns: 1fr; } }
'''

i_tabs = '<nav class="tabs" aria-label="Sections de la page"><div class="wrap"><ul>' + ''.join('<li><a data-spy href="%s"><b>%s</b>%s</a></li>' % (h, n, e(l)) for n, l, h in I_TABS) + '</ul></div></nav>\n'
i_plate = ('<div class="plate"><div class="fig">' + img('/assets/img/machines/optibean-x.webp', 'Machine à café en grains Animo OptiBean X, vue de face', lazy=False)
           + ''.join('<span class="ln" style="--x:%s;--y:%s"></span><a class="pin" href="%s" style="--x:%s;--y:%s" data-n="%s" aria-hidden="true" tabindex="-1">%s</a>' % (x, y, h, x, y, n, n) for n, x, y, t, d, h in PINS)
           + '</div><div class="cart"><span>Planche 00 · Animo OptiBean X</span><span>5 repères</span></div></div>')
i_call = '<ol class="callouts" aria-label="Repères de la machine">' + ''.join('<li><a href="%s" data-n="%s"><b aria-hidden="true">%s</b><span><strong>%s</strong><span>%s</span></span></a></li>' % (h, n, n, e(t), e(d)) for n, x, y, t, d, h in PINS) + '</ol>'
i_hero = '<main id="contenu">\n<section class="hero" aria-labelledby="h1"><div class="wrap">\n  <div>' + hero_text('La pause qui se gère <span class="u">toute seule.</span>', cta2=False) + '</div>\n  ' + i_plate + '\n  ' + i_call + '\n</div></section>\n'
I_JS = '''<script>
(function () {
  // repères et légende s'allument ensemble
  var els = [].slice.call(document.querySelectorAll('.pin, .callouts a'));
  function on(n, v) { els.forEach(function (x) { if (x.getAttribute('data-n') === n) x.classList.toggle('on', v); }); }
  els.forEach(function (x) { var n = x.getAttribute('data-n'); ['pointerenter', 'focus'].forEach(function (t) { x.addEventListener(t, function () { on(n, true); }); }); ['pointerleave', 'blur'].forEach(function (t) { x.addEventListener(t, function () { on(n, false); }); }); });
})();
</script>
'''
s_i = head('I', 'Planche', HERO_CSS + I_CSS, '<link rel="preload" as="image" href="/assets/img/machines/optibean-x.webp" fetchpriority="high">\n') + '<body>\n' + header() + i_tabs + i_hero + brief() + fonctionnement('Planche 01') + machines('Planche 02') + formules('Planche 03') + engagements('Planche 04') + secteurs('Planche 05') + zones('Planche 06') + faq('Planche 07') + final_footer('I', 'Planche') + I_JS + '<script src="/maquettes/m.js"></script>\n</body>\n</html>\n'
(OUT / 'i-planche.html').write_text(s_i, encoding='utf-8'); print('i-planche.html', len(s_i) // 1024, 'Ko')
