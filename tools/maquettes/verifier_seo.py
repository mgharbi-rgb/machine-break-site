"""Contrôle les maquettes G à J : balises, ancres, hiérarchie de titres, JSON-LD, images, absence de rose.  Usage :  python3 tools/maquettes/verifier_seo.py"""
import json, re, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
exec(open(HERE / 'verifier_html.py', encoding='utf-8').read().split("ROOT = pathlib")[0])

for name in ['g-distributeur.html', 'h-sommaire.html', 'i-planche.html', 'j-enseigne.html']:
    s = (ROOT / 'maquettes' / name).read_text(encoding='utf-8')
    p = P(); p.feed(s)
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1).replace('<\\/', '</'))
    types = [g['@type'] for g in ld['@graph']]
    prods = [g for g in ld['@graph'] if g['@type'] == 'ItemList'][0]['itemListElement']
    faq = [g for g in ld['@graph'] if g['@type'] == 'FAQPage'][0]['mainEntity']
    title = re.search(r'<title>(.*?)</title>', s).group(1); desc = re.search(r'name="description" content="([^"]+)"', s).group(1)
    h = re.findall(r'<(h[1-4])\b', s); order_ok = all(int(b[1]) - int(a[1]) <= 1 for a, b in zip(h, h[1:]))
    imgs = re.findall(r'<img [^>]+>', s); nodim = [i for i in imgs if 'width=' not in i]; noalt = [i for i in imgs if 'alt=""' in i or 'alt=' not in i]
    faq_visible = all(q['name'].replace("'", '&#x27;') in s for q in faq)
    pink = re.findall(r'(?i)#f2a7b1|#f4b8c0|--rose|--pink|pink|rose\b', s)
    ids = p.ids; dup = {i for i in ids if ids.count(i) > 1}
    anchors = set(re.findall(r'href="#([^"]+)"', s)); dead = [a for a in anchors if a not in ids]
    print('\n##', name)
    print('  balises non fermées:', p.stack or 'aucune', '| erreurs:', p.errors or 'aucune', '| ids dupliqués:', dup or 'aucun', '| ancres mortes:', dead or 'aucune')
    print('  h1:', p.counts.get('h1'), '| hiérarchie de titres sans saut:', order_ok, '| main:', p.counts.get('main'), '| tables:', p.counts.get('table'), '| articles machines:', s.count('class="mach '))
    print('  title (%d car.):' % len(title), title); print('  description (%d car.)' % len(desc))
    print('  JSON-LD:', types, '| produits:', len(prods), '| propriétés produit 1:', len(prods[0]['item']['additionalProperty']), '| questions:', len(faq), '| questions visibles dans la page:', faq_visible)
    print('  images:', len(imgs), '| sans dimensions:', len(nodim), '| sans alt descriptif:', len(noalt), '| traces de rose:', pink or 'aucune')
    print('  polices externes:', 'fonts.googleapis' in s, '| scripts externes:', len(re.findall(r'<script[^>]+src="https?://', s)))
