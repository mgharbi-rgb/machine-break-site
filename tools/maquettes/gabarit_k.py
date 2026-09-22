# Gabarit de la page K (exécuté depuis generer.py, après gabarit_j.py).
# K · Épure : l'esprit de J (affiche bordeaux, pochoir, ombres franches, mini-machine qui se vide) avec le strict
# nécessaire. Une idée par bloc, une phrase par idée. Les détails vivent sur les pages intérieures, jamais ici.

K_CSS = '''
@font-face { font-family: "Big Shoulders Stencil"; src: url("/assets/fonts/Big Shoulders Stencil Display/BigShouldersStencilDisplay-latin.woff2") format("woff2"); font-weight: 800 900; font-display: swap; }
:root { --sh: 8px 8px 0 var(--ink); }
h1, h2, .st { font-family: "Big Shoulders Stencil", Impact, "HK Grotesk", sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: .005em; line-height: .88; }
.btn { box-shadow: 5px 5px 0 var(--ink); transition: transform .15s, box-shadow .15s, background .15s, color .15s; } .btn:hover { transform: translate(3px, 3px); box-shadow: 2px 2px 0 var(--ink); }
section { padding: clamp(4rem, 9vw, 8rem) 0 0; }
h2 { font-size: clamp(2.8rem, 6.4vw, 5.6rem); margin-bottom: 1.6rem; } .sub { max-width: 34rem; margin: -.6rem 0 2.2rem; font-size: 1.1rem; }

/* en-tête bordeaux, quatre choses : le logo, le plan, le téléphone, l'action */
.top { background: var(--mb); color: var(--cream); } .top .tel { color: var(--cream); margin-left: auto; }
.top .btn { background: var(--cream); border-color: var(--ink); color: var(--ink); box-shadow: 4px 4px 0 var(--ink); } .top .btn:hover { background: #fff; color: var(--ink); }
@media (max-width: 1100px) { .all { margin-left: 0; order: 0; } }

/* ouverture */
.hero { position: relative; overflow: hidden; background: var(--mb); color: var(--cream); padding: clamp(2rem, 4vw, 3.5rem) 0 0; }
.hero .main { display: grid; grid-template-columns: 1.6fr 1fr; align-items: end; gap: 1rem; }
.hero .lead { position: relative; z-index: 2; padding-bottom: 3rem; }
.hero h1 { color: var(--cream); font-size: clamp(3.2rem, 8.6vw, 8.8rem); white-space: nowrap; padding-bottom: 1.6rem; }
.hero h1 .k { color: rgba(250, 245, 241, .85); white-space: normal; font-weight: 400; letter-spacing: .08em; display: block; margin-bottom: 1.4rem; line-height: 1.6; max-width: 34rem; }
.hero h1 .o { color: transparent; -webkit-text-stroke: 2px var(--cream); }
.hero h1 .b { display: inline-block; margin-top: .08em; padding: .05em .12em 0; background: var(--cream); color: var(--mb); box-shadow: var(--sh); }
.hero .intro { font-size: 1.18rem; max-width: 32rem; margin: 0 0 1.6rem; color: rgba(250, 245, 241, .92); }
.hero .acts { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem 1.8rem; }
.hero .btn { background: var(--cream); border-color: var(--ink); color: var(--ink); } .hero .btn:hover { background: #fff; color: var(--ink); }
.hero .tel { font-family: var(--mono); font-size: .92rem; color: var(--cream); } .hero .tel a { color: #fff; text-decoration: none; font-weight: 600; }
.cue { margin-top: 1.4rem; font-family: var(--mono); font-size: .76rem; letter-spacing: .04em; color: rgba(250, 245, 241, .75); }
.hero-side { position: relative; align-self: stretch; min-height: 540px; }
.disc { position: absolute; width: 118%; aspect-ratio: 1; left: -4%; bottom: -30%; border-radius: 50%; background: var(--sand); }
.mfig { position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); height: 104%; aspect-ratio: 536 / 940; filter: drop-shadow(18px 22px 0 rgba(31, 21, 23, .35)); } .mfig img { width: 100%; height: 100%; }
@media (max-width: 900px) { .hero .main { grid-template-columns: 1fr; } .hero h1 { font-size: 15.5vw; } .hero .lead { padding-bottom: 1rem; } .hero-side { min-height: 400px; margin: 0 -20px; overflow: hidden; border-bottom: 2px solid var(--ink); } .mfig { height: 100%; } .disc { width: 90%; left: 5%; } }

/* ce qu'on fait : quatre cases, comme dans une vitrine */
.four { display: grid; grid-template-columns: repeat(4, 1fr); border: 2px solid var(--ink); background: #fff; box-shadow: var(--sh); }
.four a { display: block; text-decoration: none; color: var(--ink); } .four a + a { border-left: 2px solid var(--ink); }
.four img { width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-bottom: 2px solid var(--ink); } .four .contain img { object-fit: contain; padding: .8rem; background: #fff; }
.four div { padding: 1.1rem 1.2rem 1.4rem; } .four h3 { font-size: 1.3rem; margin-bottom: .3rem; } .four p { font-size: .95rem; }
.four a:hover, .four a:focus-visible { background: var(--ink); color: rgba(255, 255, 255, .8); } .four a:hover h3, .four a:focus-visible h3 { color: #fff; }
@media (max-width: 900px) { .four { grid-template-columns: 1fr 1fr; } .four a:nth-child(3) { border-left: 0; } .four a:nth-child(n+3) { border-top: 2px solid var(--ink); } }
@media (max-width: 520px) { .four { grid-template-columns: 1fr; } .four a + a { border-left: 0; border-top: 2px solid var(--ink); } }

/* comment ça marche : trois pas, une ligne de contrat */
.steps { box-shadow: var(--sh); } .steps li::before { font-family: "Big Shoulders Stencil", Impact, sans-serif; font-weight: 900; font-size: 4rem; margin-bottom: 1.4rem; }
.steps h3 { font-size: 1.4rem; } .steps p { font-size: .98rem; }
.contract { margin-top: 1.6rem; padding-left: 1.2rem; border-left: 6px solid var(--mb); font-size: 1.05rem; max-width: 46rem; } .contract b { color: var(--ink); }

/* les familles de machines : deux modèles en exemple, une ligne, un lien */
.mk { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; }
.mk article { background: #fff; border: 2px solid var(--ink); box-shadow: var(--sh); color: var(--text); }
.mk .pic { display: grid; grid-template-columns: 1fr 1fr; place-items: end center; gap: .6rem; padding: 1.2rem; border-bottom: 2px solid var(--ink); background: #fff; } .mk .pic img { max-height: 190px; width: auto; }
.mk .pic + div { padding: 1.1rem 1.2rem 1.3rem; } .mk .k { display: block; margin-bottom: .3rem; } .mk h3 { font-size: 1.45rem; margin-bottom: .3rem; }
.mk .ex { margin-top: .8rem; padding-top: .6rem; border-top: 1px solid var(--line); font-size: .93rem; } .mk .ex li { padding: .3rem 0; } .mk .ex a { color: var(--ink); font-weight: 600; text-underline-offset: 4px; } .mk .ex span { color: var(--muted); }
.mk .key { font-family: "Big Shoulders Stencil", Impact, sans-serif; font-weight: 900; text-transform: uppercase; font-size: 1.5rem; line-height: .95; color: var(--mb); margin-bottom: .5rem; }
.mk-act { margin-top: 1.8rem; display: flex; flex-wrap: wrap; align-items: center; gap: 1rem 1.6rem; }
@media (max-width: 960px) { .mk { grid-template-columns: 1fr 1fr; } } @media (max-width: 560px) { .mk { grid-template-columns: 1fr; } }

/* trois formules, un bouton */
.forms { box-shadow: var(--sh); } .form { gap: .6rem; } .form h3 { font-size: 1.45rem; } .form p { font-size: 1rem; }
.form.main { background: var(--mb); } .form .price { font-family: var(--mono); font-size: .86rem; color: var(--mb); padding-top: .6rem; border-top: 1px solid var(--line); margin-top: .4rem; } .form.main .price { color: var(--cream); border-color: rgba(250, 245, 241, .4); }
.forms-act { margin-top: 1.8rem; display: flex; flex-wrap: wrap; align-items: center; gap: 1rem 1.6rem; }

/* pour qui */
.sect { box-shadow: var(--sh); } .sect img { filter: none; }

/* appel final et pied de page court */
.final { margin-top: clamp(4rem, 9vw, 8rem); } .final h2 { font-size: clamp(3rem, 8vw, 7.4rem); } .final .btn { box-shadow: 6px 6px 0 var(--ink); }
.site .cols { grid-template-columns: 1.3fr repeat(3, 1fr); } .site .k { display: block; margin-bottom: .8rem; }
@media (max-width: 960px) { .site .cols { grid-template-columns: 1fr 1fr; } } @media (max-width: 520px) { .site .cols { grid-template-columns: 1fr; } }

/* la mini-machine : elle se vide quand on défile, atteint son seuil, déclenche le passage, se re-remplit */
.jauge { position: fixed; z-index: 98; left: 14px; bottom: 14px; width: 236px; display: grid; grid-template-columns: auto 1fr; gap: .8rem; align-items: center; padding: .7rem; background: var(--ink); color: var(--cream); border: 2px solid var(--cream); box-shadow: 5px 5px 0 var(--mb); font-size: .8rem; line-height: 1.25; }
.mini { width: 58px; padding: 4px; background: #0f0a0b; border: 2px solid var(--cream); display: grid; grid-template-columns: repeat(4, 1fr); gap: 2px; }
.mini i { aspect-ratio: 1 / 1.3; background: var(--c, var(--cream)); transition: opacity .25s; } .mini i.off { opacity: .07; }
.mini u { grid-column: 1 / -1; height: 7px; margin-top: 2px; background: #3a2d30; }
.jauge .etat { display: block; } .jauge b { display: inline-block; font-family: "Big Shoulders Stencil", Impact, sans-serif; font-weight: 900; font-size: 1.8rem; line-height: 1; padding: 0 .15em; margin: .1rem 0; }
.jauge.seuil b { background: var(--cream); color: var(--ink); }
@media (max-width: 1180px) { .jauge { width: auto; bottom: 76px; left: 8px; padding: .4rem; gap: .5rem; } .jauge .etat { display: none; } .mini { width: 40px; } .jauge b { font-size: 1.3rem; } }
'''

K_FOUR = [
  ('Café en grains et boissons chaudes', '/boissons-chaudes-snacks', '/assets/img/maquette/grains.webp', 'Grains de café', 'Moulu à la demande, espresso ou café filtre.', ''),
  ('Boissons fraîches et snacks', '/boissons-chaudes-snacks', '/assets/img/shooting/canettes-distributeur-640.webp', 'Canettes dans un distributeur', 'Canettes, bouteilles, snacks, références bio.', ''),
  ('Des machines connectées', '#machines', '/assets/img/machines/animo-optibean-x-640.webp', 'Machine à café en grains installée par Machine Break', 'Café, boissons chaudes, fraîches et snacks : trois familles.', 'contain'),
  ('Dépôt, location ou achat', '#formules', '/assets/img/shooting/ecran-accueil-distributeur-640.webp', "Écran d'accueil d'un distributeur", 'Trois formules, entretien compris.', ''),
]
K_FORMS = [
  ('En dépôt', 'La machine est mise à disposition.', 'Vous ne payez que les consommations. Installation offerte à partir de 100 collaborateurs.'),
  ('En location', 'Un loyer mensuel fixe.', 'Entretien et dépannage compris. Montant selon la machine : demandez-le-nous.'),
  ("À l'achat", 'La machine vous appartient.', 'Installée par nos équipes, avec un contrat de maintenance. Sur devis.'),
]
K_FOOT = [
  ('Pour qui', [('Bureaux et PME', '/solutions/bureaux-pme'), ('Résidences et hôtels', '/solutions/residences-hotels'), ('Industrie et logistique', '/solutions/industrie-logistique'), ('Grands comptes', '/grands-comptes')]),
  ('Machines et formules', [('Nos distributeurs', '/solutions/equipements'), ('Boissons et snacks', '/boissons-chaudes-snacks'), ('Dépôt, location, achat', '/solutions/location-machine-a-cafe-distributeur')]),
  ('Le service', [('Fonctionnement', '/fonctionnement'), ("Zones d'intervention", '/zones/ile-de-france'), ('F.A.Q.', '/faq'), ('Conseils', '/blog'), ('Contact', '/contact')]),
]

def k_head():
    h = head('K', 'Épure', HERO_CSS + K_CSS, '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/Big Shoulders Stencil Display/BigShouldersStencilDisplay-latin.woff2" crossorigin>\n<link rel="preload" as="image" href="/assets/img/machines/siline-combi-m.webp" fetchpriority="high">\n')
    # la F.A.Q. n'est pas affichée sur cette page : on retire FAQPage des données structurées (le balisage doit refléter le visible)
    g = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1).replace('<\\/', '</'))
    g['@graph'] = [x for x in g['@graph'] if x['@type'] not in ('FAQPage', 'ItemList')]
    ld = json.dumps(g, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + ld + '</script>', h, flags=re.S)

def k_header():
    return '''<a class="skip" href="#contenu">Aller au contenu</a>
<header class="top"><div class="wrap">
  <a class="logo" href="/" aria-label="Machine Break, accueil">%s</a>
  <button class="all" type="button" data-mega aria-expanded="false" aria-controls="tout"><svg class="m" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg><svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg><span class="long">Tout ce qu'on fait</span><span class="short">Menu</span></button>
  <a class="tel" href="tel:+33174810952">01 74 81 09 52</a>
  <a class="btn btn-mb" href="/contact#contact-form">Mon diagnostic</a>
</div></header>
<nav class="mega" id="tout" aria-label="Tout ce que fait Machine Break"><div class="wrap">
  <div class="cols">%s</div>
  <div class="foot"><span>Ailleurs dans le groupe :</span><a href="https://tazza.fr" rel="noopener">Cafés et restaurants : Tazza</a><a href="https://lac.ltd" rel="noopener">Côte d'Azur, Monaco, Genève : L.A Concept</a></div>
</div></nav>
''' % (img('/assets/img/logoblanc.webp', 'Machine Break', lazy=False), mega_cols())

k_hero = ('<main id="contenu">\n<section class="hero" aria-labelledby="h1"><div class="wrap main">\n'
          '  <div class="lead"><h1 id="h1"><span class="k">' + e(KICKER) + '</span>La pause<br><span class="o">qui se gère</span><br><span class="b">toute seule.</span></h1>\n'
          '    <p class="intro">Café en grains, boissons et snacks pour vos équipes. La machine est connectée : elle nous prévient, nous passons avant la rupture.</p>\n'
          '    <div class="acts"><a class="btn" href="/contact#contact-form">Mon diagnostic pause en 1 minute</a><span class="tel"><a href="tel:+33174810952">01 74 81 09 52</a> · réponse sous 24 h</span></div>\n'
          '    <p class="cue">↓ En descendant, regardez la petite machine se vider.</p></div>\n'
          '  <div class="hero-side"><span class="disc"></span><div class="mfig">' + img('/assets/img/machines/siline-combi-m.webp', 'Distributeur de snacks et de boissons fraîches installé par Machine Break', lazy=False) + '</div></div>\n'
          '</div></section>\n')

k_four = ('<section id="offre" aria-labelledby="offre-t"><div class="wrap">\n  <h2 id="offre-t" class="rv">Ce qu\'on fait.</h2>\n  <div class="four rv">'
          + ''.join('<a href="%s" class="%s">%s<div><h3>%s</h3><p>%s</p></div></a>' % (h, cls, img(src, alt), e(t), e(p)) for t, h, src, alt, p, cls in K_FOUR) + '</div>\n</div></section>\n')

k_steps = ('<section id="fonctionnement" aria-labelledby="fonc-t"><div class="wrap">\n  <h2 id="fonc-t" class="rv">Vous ne gérez rien.</h2>\n  <ol class="steps rv">'
           + ''.join('<li><h3>%s</h3><p>%s</p></li>' % (e(t), e(p)) for t, p in STEPS) + '</ol>\n'
           '  <p class="contract rv"><b>Écrit au contrat :</b> un délai d\'intervention, chaque passage tracé dans votre espace client, un interlocuteur nommé et joignable directement.</p>\n</div></section>\n')

# Les machines sont décrites par ce qu'elles font, jamais par leur fabricant (chiffres repris des fiches du site).
K_FAM = [
  ('Café en grains', 'Espresso et café filtre, moulus à la demande.', 'Bureaux, accueils, salles de pause.',
   [('animo-optime-x', 'La compacte', "38 cm de large, jusqu'à 125 boissons par jour"), ('animo-optibean-x', 'La grande', "jusqu'à 250 boissons par jour")]),
  ('Boissons chaudes', 'Grand écran, recettes gourmandes, réserve de gobelets.', 'Halls, sites industriels, grands sites.',
   [('bianchi-agily', "Grand écran", "21 pouces, jusqu'à 1 100 gobelets"), ('bianchi-intuity', 'Très grande capacité', "32 pouces, double chaudière, jusqu'à 1 560 gobelets")]),
  ('Boissons fraîches et snacks', 'Canettes, bouteilles et snacks, livrés par ascenseur.', 'Logistique, industrie, résidences.',
   [('sielaff-robimat', 'Boissons fraîches', "vitrine panoramique, jusqu'à 770 bouteilles"), ('sielaff-siline', 'Snacks et frais', 'deux zones de température, écran tactile')]),
]

def k_machines():
    cards = []
    for i, (fam, key, pour, models) in enumerate(K_FAM):
        pics = ''.join(img('/assets/img/machines/%s-640.webp' % slug, '%s : %s, %s' % (fam, n.lower(), d)) for slug, n, d in models)
        ex = ''.join('<li><a href="%s">%s</a> <span>%s</span></li>' % (BY[slug]['url'], e(n), e(d)) for slug, n, d in models)
        cards.append('<article><div class="pic">%s</div><div><span class="k">Famille %d</span><h3>%s</h3><p class="key">%s</p><p>%s</p><ul class="ex">%s</ul></div></article>' % (pics, i + 1, e(fam), e(key), e(pour), ex))
    return ('<section id="machines" aria-labelledby="mach-t"><div class="wrap">\n  <h2 id="mach-t" class="rv">Trois familles de machines.</h2>\n  <p class="sub rv">Selon votre site et votre consommation. Chaque machine est connectée, entretenue par nos équipes, et proposée en dépôt, en location ou à l\'achat.</p>\n  <div class="mk rv">'
            + ''.join(cards) + '</div>\n  <div class="mk-act rv"><a class="btn" href="/solutions/equipements">Voir les machines</a><span>Vous cherchez autre chose ? Demandez-nous.</span></div>\n</div></section>\n')

k_forms = ('<section id="formules" aria-labelledby="form-t"><div class="wrap">\n  <h2 id="form-t" class="rv">Trois façons de s\'équiper.</h2>\n  <div class="forms rv">'
           + ''.join('<div class="form%s"><span class="k">%s</span><h3>%s</h3><p>%s</p></div>' % (' main' if i == 0 else '', e(k), e(t), e(p)) for i, (k, t, p) in enumerate(K_FORMS))
           + '</div>\n  <div class="forms-act rv"><a class="btn btn-mb" href="/contact#contact-form">Trouver ma formule en 1 minute</a><span>Nous visitons votre site, puis nous choisissons la machine et la formule avec vous.</span></div>\n</div></section>\n')

k_sect = ('<section id="secteurs" aria-labelledby="sect-t"><div class="wrap">\n  <h2 id="sect-t" class="rv">Pour qui.</h2>\n  <div class="sect rv">'
          + ''.join('<a href="%s">%s<div><h3>%s</h3><p>%s</p></div></a>' % (h, img(src, alt), e(t), e(p)) for t, h, src, alt, p in SECT) + '</div>\n</div></section>\n')

k_end = ('</main>\n<section class="final" aria-labelledby="fin-t" style="padding-top:clamp(3.5rem,8vw,6.5rem)"><div class="wrap">\n'
         '  <h2 id="fin-t">Et vos pauses, elles ressemblent à quoi ?</h2>\n'
         '  <div><p>Un diagnostic en une minute, une réponse sous 24 h, partout en Île-de-France.</p><div class="acts"><a class="btn btn-cream" href="/contact#contact-form">Mon diagnostic pause en 1 minute</a><a class="tel" href="tel:+33174810952">01 74 81 09 52</a></div></div>\n</div></section>\n'
         '<footer class="site"><div class="wrap">\n  <div class="cols"><div>' + img('/assets/img/logoblanc.webp', 'Machine Break') + '<address>28 avenue Christian Doppler<br>77700 Bailly-Romainvilliers<br><a href="tel:+33174810952">01 74 81 09 52</a></address></div>'
         + ''.join('<div><span class="k">%s</span><ul>%s</ul></div>' % (e(t), ''.join('<li><a href="%s">%s</a></li>' % (h, e(l)) for l, h in ls)) for t, ls in K_FOOT)
         + '</div>\n  <p class="note">Maquette de démonstration · Direction K « Épure »</p>\n</div></footer>\n')

k_jauge = '<div class="jauge" id="jauge" aria-hidden="true"><div class="mini">' + ''.join('<i style="--c:%s"></i>' % c for c in (['var(--cream)', '#b9956f', 'var(--sand)', '#8f4f5a'] * 5)) + '<u></u></div><div><b id="jauge-n">100 %</b><span class="etat" id="jauge-e">Machine remplie, rien à faire</span></div></div>\n'

K_JS = '''<script>
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
})();
</script>
'''

s_k = k_head() + '<body>\n' + k_header() + k_hero + k_four + k_steps + k_machines() + k_forms + k_sect + k_end + k_jauge + K_JS + '<script src="/maquettes/n.js"></script>\n<script src="/maquettes/m.js"></script>\n</body>\n</html>\n'
(OUT / 'k-epure.html').write_text(s_k, encoding='utf-8'); print('k-epure.html', len(s_k) // 1024, 'Ko')
