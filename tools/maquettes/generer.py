"""Génère les maquettes G, H, I, J, K (HTML statique) à partir des données des fiches machines du dépôt.

Usage, depuis n'importe où :  python3 tools/maquettes/generer.py
Les gabarits sont dans gabarits_ghi.py, gabarit_j.py et gabarit_k.py, les données machines dans machines.json (voir extraire_machines.py).
"""
import json, html, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
OUT = ROOT / 'maquettes'
MACH = json.load(open(HERE / 'machines.json', encoding='utf-8'))
SITE = 'https://machinebreak.com'
e = lambda s: html.escape(s, quote=True)

def _taille(path):
    """Largeur et hauteur d'un fichier WebP ou PNG, lues dans son en-tête (sans dépendance, identique sur macOS, Windows, Linux)."""
    b = path.read_bytes()[:40]
    if b[:8] == b'\x89PNG\r\n\x1a\n':
        return str(int.from_bytes(b[16:20], 'big')), str(int.from_bytes(b[20:24], 'big'))
    assert b[:4] == b'RIFF' and b[8:12] == b'WEBP', 'format non géré : %s' % path
    if b[12:16] == b'VP8X':
        return str(1 + int.from_bytes(b[24:27], 'little')), str(1 + int.from_bytes(b[27:30], 'little'))
    if b[12:16] == b'VP8L':
        bits = int.from_bytes(b[21:25], 'little')
        return str((bits & 0x3FFF) + 1), str(((bits >> 14) & 0x3FFF) + 1)
    return str(int.from_bytes(b[26:28], 'little') & 0x3FFF), str(int.from_bytes(b[28:30], 'little') & 0x3FFF)

_dims = {}
def img(src, alt, cls='', lazy=True, extra=''):
    if src not in _dims:
        _dims[src] = _taille(ROOT / src.lstrip('/'))
    w, h = _dims[src]
    return '<img src="%s" alt="%s"%s width="%s" height="%s"%s%s>' % (src, e(alt), ' class="%s"' % cls if cls else '', w, h, ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"', extra)

# ---------- données éditoriales (reprises du site et des maquettes validées, aucun chiffre inventé) ----------
KICKER = 'Distributeurs automatiques et machines à café pour entreprises · Paris et Île-de-France'
LEAD = "Café en grains, boissons et snacks pour vos équipes. La machine remonte son remplissage, déclenche elle-même le passage, et vous voyez tout dans votre espace client."
TITLE = 'Distributeur automatique et machine à café en entreprise | Machine Break'
DESC = "Machines à café en grains et distributeurs automatiques pour entreprises à Paris et en Île-de-France. Dépôt, location ou achat, réassort déclenché par télémétrie."
PROOFS = [('Zone', "Toute l'Île-de-France, depuis la Seine-et-Marne"), ('Réponse', 'Sous 24 h'), ('Formules', 'Dépôt, location ou achat')]

FAM = {
  'animo-optibean-x': ('cafe', 'Machine à café en grains', 'Animo', 'Animo OptiBean X', "jusqu'à 250 boissons par jour", ['Production journalière recommandée', 'Boissons', 'Bacs à grains', 'Écran', 'Dimensions (L × P × H)']),
  'animo-optime-x': ('cafe', 'Machine à café en grains compacte', 'Animo', 'Animo OptiMe X', "jusqu'à 125 boissons par jour, 38 cm de large", ['Production journalière recommandée', 'Capacité horaire', 'Bacs à grains', 'Moulin', 'Dimensions (L × P × H)']),
  'bianchi-agily': ('chaud', 'Distributeur de boissons chaudes', 'Bianchi Vending', 'Bianchi Agily', "écran 21 pouces, jusqu'à 1 100 gobelets", ['Interface', 'Café en grains', 'Gobelets', 'Bacs de produits solubles', 'Dimensions (H × L × P)']),
  'bianchi-intuity': ('chaud', 'Distributeur de boissons chaudes grande capacité', 'Bianchi Vending', 'Bianchi Intuity', "écran 32 pouces, jusqu'à 1 560 gobelets", ['Modèles', 'Chaudière', 'Gobelets', 'Toppings', 'Dimensions (H × L × P)']),
  'sielaff-robimat': ('frais', 'Distributeur de boissons fraîches', 'Sielaff', 'Sielaff Robimat X', "jusqu'à 770 bouteilles de 50 cl", ['Capacité', 'Distribution', 'Produits', 'Plateaux', 'Dimensions (H × L × P)']),
  'sielaff-siline': ('frais', 'Distributeur de snacks et boissons fraîches', 'Sielaff', 'Sielaff SiLine Snack et Combi', 'deux zones de température, ascenseur', ['Gamme', 'Distribution', 'Températures', 'Écran', 'Dimensions (H × L × P)']),
}
ORDER = ['animo-optibean-x', 'animo-optime-x', 'bianchi-agily', 'bianchi-intuity', 'sielaff-robimat', 'sielaff-siline']
BY = {m['slug']: m for m in MACH}

MEGA = [
  ('Pour qui', [('Bureaux et PME', '/solutions/bureaux-pme', 'Accueils, salles de pause, open spaces'), ('Résidences et hôtels', '/solutions/residences-hotels', 'Un service à toute heure, sans personnel dédié'), ('Industrie et logistique', '/solutions/industrie-logistique', "Grande capacité, équipes en rotation"), ('Grands comptes multi-sites', '/grands-comptes', 'Un interlocuteur nommé pour tous vos sites'), ('Tous les secteurs', '/solution-par-secteur', '')]),
  ('Les machines', [('Machines à café en grains', '#machines', 'Animo OptiBean X, OptiMe X'), ('Distributeurs de boissons chaudes', '#machines', 'Bianchi Agily, Intuity'), ('Boissons fraîches et snacks', '#machines', 'Sielaff Robimat X, SiLine'), ('Tous nos distributeurs', '/solutions/equipements', '')]),
  ('Produits et formules', [('Boissons et snacks', '/boissons-chaudes-snacks', 'Café en grains, boissons fraîches, snacks'), ('Dépôt, location, achat', '/solutions/location-machine-a-cafe-distributeur', "Trois façons de s'équiper"), ('Maintenance et réassort', '/fonctionnement', 'Déclenchés par la télémétrie')]),
  ('Le service', [('Fonctionnement', '/fonctionnement', ''), ("Zones d'intervention", '/zones/ile-de-france', "Paris et toute l'Île-de-France"), ('F.A.Q.', '/faq', ''), ('Conseils', '/blog', ''), ('Contact', '/contact', '')]),
]
STEPS = [('La machine nous prévient', 'Ventes, remplissage, alertes techniques : tout remonte en temps réel.'), ('Nous passons avant la rupture', 'Le réassort est déclenché par la télémétrie, selon les habitudes de consommation de votre site.'), ('Vous suivez tout', 'Chaque intervention est tracée et horodatée dans votre espace client.')]
FORMS = [
  ('Formule 1 · En dépôt', 'Machine mise à disposition, vous ne payez que les consommations', "Nous installons, approvisionnons et entretenons. Installation offerte à partir de 100 collaborateurs.", ['Installation, réassort et entretien par nos équipes', 'Machine connectée, réassort déclenché par la télémétrie', "Interventions tracées dans l'espace client"], 'Choisir le dépôt'),
  ('Formule 2 · En location', 'Un loyer mensuel fixe, entretien et dépannage compris', "Les consommations sont réglées par vos collaborateurs à la machine, ou prises en charge par l'entreprise.", ['Loyer mensuel fixe', 'Entretien et dépannage compris', "Interventions tracées dans l'espace client"], 'Choisir la location'),
  ("Formule 3 · À l'achat", "La machine vous appartient, nous l'entretenons", 'Installée et mise en service par nos équipes, avec un contrat de maintenance.', ['Installation et mise en service comprises', 'Contrat de maintenance', 'Consommables livrés sur votre site'], "Choisir l'achat"),
]
CMP = [
  ('La machine', ['Mise à disposition par Machine Break', 'Louée, loyer mensuel fixe', 'Elle vous appartient']),
  ('Ce que vous payez', ['Uniquement les consommations', "Le loyer ; les consommations sont réglées à la machine ou prises en charge par l'entreprise", 'La machine et un contrat de maintenance']),
  ('Installation', ['Par nos équipes, offerte à partir de 100 collaborateurs', 'Par nos équipes', 'Installation et mise en service par nos équipes']),
  ('Entretien et dépannage', ['Par nos équipes', 'Compris dans le loyer', 'Contrat de maintenance']),
  ('Télémétrie et traçabilité', ['Machine connectée, interventions tracées'] * 3),
]
ENG = [('Réassort déclenché par la télémétrie', 'Le passage suit la consommation réelle, pas un calendrier.'), ('Alerte analysée à distance', 'Avant tout déplacement, pour partir avec la bonne pièce.'), ("Un délai d'intervention écrit au contrat", 'Défini pour chaque site.'), ('Chaque intervention tracée', 'Horodatée, consultable dans votre espace client.'), ('Un interlocuteur nommé, joignable directement', 'Pas de plateforme téléphonique : une personne qui connaît votre site.')]
SECT = [('Bureaux et PME', '/solutions/bureaux-pme', '/assets/img/maquette/duo.webp', 'Machines à café dans un espace de pause de bureaux', 'Accueils, salles de pause, open spaces.'), ('Résidences et hôtels', '/solutions/residences-hotels', '/assets/img/shooting/distributeur-salon-residence-640.webp', "Distributeur automatique dans le salon d'une résidence", 'Un service disponible à toute heure, sans personnel dédié.'), ('Industrie et logistique', '/solutions/industrie-logistique', '/assets/img/shooting/allee-usine-640.webp', "Allée d'un site industriel équipé de distributeurs", "Grande capacité, réassort calé sur les rotations d'équipe."), ('Grands comptes multi-sites', '/grands-comptes', '/assets/img/maquette/salle.webp', "Salle de restauration d'entreprise équipée de distributeurs", 'Plusieurs sites, un interlocuteur nommé.')]
ZONES = [('Paris', '/zones/paris'), ('Seine-et-Marne', '/zones/seine-et-marne'), ('Marne-la-Vallée', '/zones/marne-la-vallee'), ('Est parisien', '/zones/est-parisien'), ("Toute l'Île-de-France", '/zones/ile-de-france')]
FAQ = [
  ("Qui peut bénéficier d'un distributeur Machine Break ?", "Toutes les entreprises, collectivités, établissements de santé ou écoles souhaitant améliorer leur espace de pause peuvent bénéficier de notre solution."),
  ("Est-ce que l'installation est gratuite ?", "À partir de 100 collaborateurs sur le site, l'installation, la mise en service, la maintenance et le réapprovisionnement sont offerts : le service est clé en main. En dessous de ce seuil, nous étudions chaque demande au cas par cas lors du diagnostic."),
  ('Quels types de produits proposez-vous ?', 'Nous proposons des cafés de qualité, des snacks sains et gourmands, ainsi que des boissons fraîches. Tous nos produits sont rigoureusement sélectionnés.'),
  ('À quelle fréquence les machines sont-elles réapprovisionnées ?', 'Grâce à notre système de télémétrie, nous suivons les consommations en temps réel pour planifier les réapprovisionnements de façon optimale.'),
  ('Que faire en cas de panne ?', "Nos équipes sont alertées automatiquement en cas d'anomalie et interviennent dans les plus brefs délais, souvent avant que vous ne constatiez le problème."),
  ("Peut-on personnaliser l'habillage des distributeurs ?", 'Oui, nous proposons un service de personnalisation visuelle pour intégrer les distributeurs dans votre environnement ou aux couleurs de votre entreprise.'),
  ('Proposez-vous des produits bio ou sans allergènes ?', 'Oui, notre offre inclut des références bio, sans gluten et à faible teneur en sucre. Nous nous adaptons aux besoins spécifiques de vos collaborateurs.'),
  ('Quel est le délai pour installer une machine ?', "Une fois le besoin validé, l'installation peut être effectuée sous quelques jours selon votre région et les équipements choisis."),
]

# ---------- données structurées (SEO et moteurs génératifs) ----------
def jsonld():
    org = {'@type': 'LocalBusiness', '@id': SITE + '/#entreprise', 'name': 'Machine Break', 'url': SITE + '/', 'telephone': '+33174810952', 'image': SITE + '/assets/img/logo.webp', 'description': DESC,
           'address': {'@type': 'PostalAddress', 'streetAddress': '28 avenue Christian Doppler', 'postalCode': '77700', 'addressLocality': 'Bailly-Romainvilliers', 'addressRegion': 'Île-de-France', 'addressCountry': 'FR'},
           'areaServed': [{'@type': 'AdministrativeArea', 'name': n} for n in ['Île-de-France', 'Paris', 'Seine-et-Marne', 'Marne-la-Vallée', 'Est parisien']]}
    service = {'@type': 'Service', '@id': SITE + '/#service', 'name': 'Installation et gestion de distributeurs automatiques et de machines à café en entreprise', 'serviceType': 'Distribution automatique en entreprise', 'provider': {'@id': SITE + '/#entreprise'}, 'areaServed': {'@type': 'AdministrativeArea', 'name': 'Île-de-France'},
               'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Formules', 'itemListElement': [{'@type': 'Offer', 'name': k.split(' · ')[1], 'description': t + '. ' + p} for k, t, p, _, _ in FORMS]}}
    products = []
    for i, slug in enumerate(ORDER):
        m, (fam, typ, brand, name, key, _) = BY[slug], FAM[slug]
        products.append({'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'Product', 'name': name, 'category': typ, 'brand': {'@type': 'Brand', 'name': brand}, 'description': m['intro'][0] if m['intro'] else m['description'], 'url': SITE + m['url'], 'image': SITE + '/assets/img/machines/%s.webp' % slug,
                         'additionalProperty': [{'@type': 'PropertyValue', 'name': a, 'value': b} for a, b in m['specs']]}})
    faq = {'@type': 'FAQPage', '@id': SITE + '/#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    graph = {'@context': 'https://schema.org', '@graph': [org, {'@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': 'Machine Break', 'inLanguage': 'fr-FR', 'publisher': {'@id': SITE + '/#entreprise'}}, service, {'@type': 'ItemList', '@id': SITE + '/#machines', 'name': 'Machines installées par Machine Break', 'itemListElement': products}, faq]}
    return json.dumps(graph, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

# ---------- blocs communs ----------
def head(letter, name, css, preload=''):
    return '''<!doctype html>
<html lang="fr" class="no-js">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Maquette de démonstration : non indexée. À la mise en ligne : retirer cette ligne et ajouter <link rel="canonical" href="%s/">. -->
<meta name="robots" content="noindex, nofollow">
<title>%s</title>
<meta name="description" content="%s">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR"><meta property="og:site_name" content="Machine Break">
<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:image" content="%s/assets/img/maquette/people.webp">
<meta name="theme-color" content="#753F48">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/HK Grotesk Pro/HKGroteskPro-Medium.woff2" crossorigin>
%s<link rel="stylesheet" href="/maquettes/n.css">
<style>
/* Direction %s « %s » */
%s
</style>
<script type="application/ld+json">%s</script>
</head>
''' % (SITE, e(TITLE), e(DESC), e(TITLE), e(DESC), SITE, preload, letter, name, css.strip(), jsonld())

def mega_cols(footer=False):
    out = []
    for title, links in MEGA:
        lis = ''.join('<li><a href="%s">%s%s</a></li>' % (h, e(l), ('<small>%s</small>' % e(s)) if s and not footer else '') for l, h, s in links)
        out.append('<div%s><%s class="k">%s</%s><ul>%s</ul></div>' % ('' if footer else ' class="col"', 'p' if not footer else 'h3', e(title), 'p' if not footer else 'h3', lis))
    return ''.join(out)

def header(logo='/assets/img/logo.webp'):
    return '''<a class="skip" href="#contenu">Aller au contenu</a>
<header class="top"><div class="wrap">
  <a class="logo" href="/" aria-label="Machine Break, accueil">%s</a>
  <button class="all" type="button" data-mega aria-expanded="false" aria-controls="tout"><svg class="m" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg><svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg><span class="long">Tout ce qu'on fait</span><span class="short">Menu</span></button>
  <nav class="quick" aria-label="Accès rapides"><ul><li><a href="/fonctionnement">Fonctionnement</a></li><li><a href="/faq">F.A.Q.</a></li><li><a href="/blog">Conseils</a></li><li><a href="/contact">Contact</a></li></ul></nav>
  <a class="tel" href="tel:+33174810952">01 74 81 09 52</a>
  <a class="btn btn-mb" href="/contact#contact-form">Mon diagnostic</a>
</div></header>
<nav class="mega" id="tout" aria-label="Tout ce que fait Machine Break"><div class="wrap">
  <div class="cols">%s</div>
  <div class="foot"><span>Ailleurs dans le groupe :</span><a href="https://tazza.fr" rel="noopener">Cafés et restaurants : Tazza</a><a href="https://lac.ltd" rel="noopener">Côte d'Azur, Monaco, Genève : L.A Concept</a><a href="tel:+33174810952">01 74 81 09 52</a></div>
</div></nav>
''' % (img(logo, 'Machine Break', lazy=False), mega_cols())

def sh(num, label, h2, p, hid):
    return '<div class="sh"><p class="k">%s — %s</p><h2 id="%s" class="rv">%s</h2><p class="rv">%s</p></div>' % (num, e(label), hid, h2, p)

def brief():
    facts = [('Activité', 'Distributeurs automatiques et machines à café en entreprise'), ('Zone', "Paris et toute l'Île-de-France"), ('Siège', 'Bailly-Romainvilliers, Seine-et-Marne (77)'), ('Machines', '6 modèles : Animo, Bianchi Vending, Sielaff'), ('Formules', 'Dépôt, location, achat'), ('Réponse', 'Sous 24 h'), ('Téléphone', '<a href="tel:+33174810952">01 74 81 09 52</a>')]
    return '''<section id="bref" aria-labelledby="bref-t"><div class="wrap"><div class="brief rv">
  <div><p class="k">En bref</p><h2 id="bref-t">Machine Break, en trois phrases</h2>
    <p>Machine Break installe et gère des machines à café en grains et des distributeurs automatiques de boissons et de snacks pour les entreprises, à Paris et dans toute l'Île-de-France, depuis Bailly-Romainvilliers en Seine-et-Marne.</p>
    <p>Chaque machine est connectée : elle remonte ses ventes, son niveau de remplissage et ses alertes techniques. Le réassort et les interventions sont déclenchés par cette télémétrie, puis tracés et horodatés dans l'espace client.</p>
    <p>Trois formules existent pour chaque machine : le dépôt, la location et l'achat. À partir de 100 collaborateurs sur le site, l'installation, la mise en service, la maintenance et le réapprovisionnement sont offerts.</p></div>
  <div><dl class="facts">%s</dl></div>
</div></div></section>
''' % ''.join('<dt>%s</dt><dd>%s</dd>' % (a, b) for a, b in facts)

def fonctionnement(num, extra=''):
    return '''<section id="fonctionnement" aria-labelledby="fonc-t"><div class="wrap">
  %s
  <ol class="steps">%s</ol>%s
</div></section>
''' % (sh(num, 'Fonctionnement', 'Vous ne gérez rien. Vous voyez tout.', "Pas de tournée à date fixe : chaque machine est connectée et c'est elle qui déclenche nos passages.", 'fonc-t'),
       ''.join('<li class="rv"><h3>%s</h3><p>%s</p></li>' % (e(t), e(p)) for t, p in STEPS), extra)

def spec_table(rows, caption):
    return '<table class="spec"><caption>%s</caption><tbody>%s</tbody></table>' % (e(caption), ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (e(a), e(b)) for a, b in rows))

PRIX = '''<div class="prix"><p class="k">Combien ça coûte</p><dl><div><dt>Dépôt</dt><dd>Vous ne payez que les consommations</dd></div><div><dt>Location</dt><dd>Un loyer mensuel fixe <span class="todo">montant à renseigner</span></dd></div><div><dt>Achat</dt><dd>Sur devis <span class="todo">prix à renseigner</span></dd></div></dl></div>'''

def machines(num, prix=False):
    arts = []
    for slug in ORDER:
        m, (fam, typ, brand, name, key, keys) = BY[slug], FAM[slug]
        specs = dict(m['specs']); hi = [(k, specs[k]) for k in keys if k in specs]
        sites = ' ; '.join(s[0].lower() + s[1:] for s in m['sites'][:3])
        arts.append(('''<article class="mach rv" data-fam="%s" id="m-%s">
      <div class="pic">%s</div>
      <div class="body"><span class="k fam">%s · %s</span><h3><a href="%s">%s</a></h3><p class="key">%s</p><p>%s</p><p class="for"><strong>Pour quels sites :</strong> %s.</p>
        <ul class="tags" aria-label="Formules disponibles pour cette machine"><li>Dépôt</li><li>Location</li><li>Achat</li></ul></div>
      <div class="hi">%s{{PRIX}}</div>
      <details><summary>Toutes les caractéristiques : %s</summary><div>%s<a class="more" href="%s">Voir la fiche complète : %s</a></div></details>
    </article>''' % (fam, slug, img('/assets/img/machines/%s-640.webp' % slug, '%s %s' % (typ, name)), e(typ), e(brand), m['url'], e(name), e(key), e(m['intro'][0]), e(sites),
                     spec_table(hi, 'Points clés'), e(name), spec_table(m['specs'], 'Caractéristiques : ' + name), m['url'], e(name))).replace('{{PRIX}}', PRIX if prix else ''))
    return '''<section id="machines" aria-labelledby="mach-t"><div class="wrap">
  %s
  <div class="filters" role="group" aria-label="Filtrer les machines par famille"><button type="button" data-filter="tout" aria-pressed="true">Toutes (6)</button><button type="button" data-filter="cafe" aria-pressed="false">Café en grains (2)</button><button type="button" data-filter="chaud" aria-pressed="false">Boissons chaudes (2)</button><button type="button" data-filter="frais" aria-pressed="false">Boissons fraîches et snacks (2)</button></div>
  <p class="sr" id="filtre-etat" role="status"></p>
  <div class="machs">
    %s
  </div>
</div></section>
''' % (sh(num, 'Les machines', 'Six machines, trois familles.', "Du plateau de bureaux au site industriel. Chaque machine est proposée en dépôt, en location ou à l'achat, connectée et entretenue par nos équipes.", 'mach-t'), '\n    '.join(arts))

def formules(num):
    cards = ''.join('<div class="form%s rv"><span class="k">%s</span><h3>%s</h3><p>%s</p><ul>%s</ul><a class="btn %s" href="/contact#contact-form">%s</a></div>' % (' main' if i == 0 else '', e(k), e(t), e(p), ''.join('<li>%s</li>' % e(x) for x in li), 'btn-cream' if i == 0 else '', e(cta)) for i, (k, t, p, li, cta) in enumerate(FORMS))
    rows = ''.join('<tr><th scope="row">%s</th>%s</tr>' % (e(a), ''.join('<td>%s</td>' % e(c) for c in cells)) for a, cells in CMP)
    return '''<section id="formules" aria-labelledby="form-t"><div class="wrap">
  %s
  <div class="forms">%s</div>
  <div class="cmp rv" tabindex="0" role="region" aria-label="Comparatif des trois formules"><table><caption class="k">Comparatif des trois formules</caption><thead><tr><td></td><th scope="col">Dépôt</th><th scope="col">Location</th><th scope="col">Achat</th></tr></thead><tbody>%s</tbody></table></div>
</div></section>
''' % (sh(num, 'Les formules', "Trois façons de s'équiper.", 'Dans les trois cas, la machine est connectée, entretenue par nos équipes, et chaque intervention est tracée.', 'form-t'), cards, rows)

def engagements(num):
    return '''<section id="engagements" aria-labelledby="eng-t"><div class="wrap">
  %s
  <ol class="eng">%s</ol>
</div></section>
''' % (sh(num, 'Nos engagements', 'Cinq engagements, écrits au contrat.', "Des promesses que nous tenons parce qu'elles reposent sur notre façon de travailler.", 'eng-t'), ''.join('<li class="rv"><span>%s<small>%s</small></span></li>' % (e(a), e(b)) for a, b in ENG))

def secteurs(num):
    return '''<section id="secteurs" aria-labelledby="sect-t"><div class="wrap">
  %s
  <div class="sect rv">%s</div>
</div></section>
''' % (sh(num, 'Votre secteur', 'Pensé pour votre site.', "Nous visitons, puis nous définissons avec vous la machine qui convient à l'espace.", 'sect-t'), ''.join('<a href="%s">%s<div><h3>%s</h3><p>%s</p></div></a>' % (h, img(src, alt), e(t), e(p)) for t, h, src, alt, p in SECT))

def zones(num):
    return '''<section id="zones" aria-labelledby="zone-t"><div class="wrap">
  %s
  <div class="zones"><div class="rv"><p>Nos équipes interviennent à Paris et dans toute l'Île-de-France, au départ de Bailly-Romainvilliers, en Seine-et-Marne.</p>
    <ul>%s</ul></div>
    <div class="zone-card rv"><p class="k">Les huit départements d'Île-de-France</p><p class="deps" aria-label="Départements 75, 77, 78, 91, 92, 93, 94 et 95">75 · 77 · 78 · 91<br>92 · 93 · 94 · 95</p><address><strong>Machine Break</strong><br>28 avenue Christian Doppler, 77700 Bailly-Romainvilliers<br><a href="tel:+33174810952">01 74 81 09 52</a></address></div></div>
</div></section>
''' % (sh(num, "Zones d'intervention", "Paris et toute l'Île-de-France.", 'Un passage déclenché par la machine, où que soit votre site dans la région.', 'zone-t'), ''.join('<li><a href="%s">%s</a></li>' % (h, e(n)) for n, h in ZONES))

def faq(num):
    return '''<section id="faq" aria-labelledby="faq-t"><div class="wrap">
  %s
  <div class="faq">%s</div>
  <p style="margin-top:1.6rem"><a class="btn" href="/faq">Toutes les questions</a></p>
</div></section>
''' % (sh(num, 'Questions fréquentes', 'Les réponses, sans détour.', 'Les questions que les entreprises nous posent avant de s\'équiper.', 'faq-t'), ''.join('<details class="rv"><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in FAQ))

def final_footer(letter, name):
    return '''</main>
<section class="final" aria-labelledby="fin-t" style="padding-top:clamp(3.5rem,8vw,6.5rem)"><div class="wrap">
  <h2 id="fin-t">Et vos pauses, elles ressemblent à quoi ?</h2>
  <div><p>Un diagnostic en une minute, une réponse sous 24 h.</p><div class="acts"><a class="btn btn-cream" href="/contact#contact-form">Mon diagnostic pause en 1 minute</a><a class="tel" href="tel:+33174810952">01 74 81 09 52</a></div></div>
</div></section>
<footer class="site"><div class="wrap">
  <div class="cols"><div>%s<address>28 avenue Christian Doppler<br>77700 Bailly-Romainvilliers<br><a href="tel:+33174810952">01 74 81 09 52</a></address></div>%s</div>
  <p class="note">Maquette de démonstration · Direction %s « %s »</p>
</div></footer>
<script src="/maquettes/n.js"></script>
''' % (img('/assets/img/logoblanc.webp', 'Machine Break'), mega_cols(footer=True), letter, name)

def hero_text(h1_html, cta2=True):
    return '''<h1 id="h1"><span class="k">%s</span>%s</h1>
    <p class="intro">%s</p>
    <div class="acts"><a class="btn btn-mb" href="/contact#contact-form">Mon diagnostic pause en 1 minute</a>%s</div>
    <dl class="proofs">%s</dl>''' % (e(KICKER), h1_html, e(LEAD), '<a class="btn" href="#fonctionnement">Comment ça marche</a>' if cta2 else '', ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (e(a), e(b)) for a, b in PROOFS))

HERO_CSS = '''
h1 .k { display: block; margin-bottom: 1.4rem; line-height: 1.6; max-width: 36rem; }
.intro { font-size: 1.15rem; max-width: 34rem; margin: 1.6rem 0 1.8rem; }
.acts { display: flex; flex-wrap: wrap; gap: .7rem; }
.proofs { display: grid; grid-template-columns: repeat(3, auto); justify-content: start; gap: 0 2.2rem; margin-top: 2.2rem; padding-top: 1.1rem; border-top: 2px solid var(--ink); }
.proofs dt { font-family: var(--mono); font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); } .proofs dd { color: var(--ink); font-weight: 600; font-size: .95rem; }
@media (max-width: 640px) { .proofs { grid-template-columns: 1fr; gap: .7rem; } }
.mach .body, .mach .hi { padding: 1.4rem; } .mach .for { margin-top: .7rem; font-size: .95rem; }
'''

exec(open(HERE / 'gabarits_ghi.py', encoding='utf-8').read())
exec(open(HERE / 'gabarit_j.py', encoding='utf-8').read())
exec(open(HERE / 'gabarit_k.py', encoding='utf-8').read())
