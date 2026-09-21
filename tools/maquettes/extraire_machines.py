"""Relit les six fiches machines/*.html du site et en tire machines.json (caractéristiques, sites visés, formules).

À relancer quand une fiche machine change, puis relancer generer.py.  Usage :  python3 tools/maquettes/extraire_machines.py
"""
import re, html, json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent

def clean(t):
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return re.sub(r'\s+', ' ', t).replace(' ,', ',').replace(' .', '.').strip()

out = []
for f in sorted((ROOT / 'machines').glob('*.html')):
    s = f.read_text(encoding='utf-8')
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    m = {'slug': f.stem, 'url': '/machines/' + f.stem}
    m['title'] = clean(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    m['description'] = clean(re.search(r'name="description" content="([^"]+)"', s).group(1))
    m['h1'] = clean(re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S).group(1))
    m['specs'] = [[clean(a), clean(b)] for a, b in re.findall(r'<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>', body, re.S)]
    # paragraphe d'introduction et section « Pour quels sites »
    intro = re.search(r'</h1>(.*?)<h2', body, re.S)
    m['intro'] = [clean(p) for p in re.findall(r'<p[^>]*>(.*?)</p>', intro.group(1), re.S)][:2] if intro else []
    sites = re.search(r'<h2[^>]*>\s*Pour quels sites\s*</h2>(.*?)<h2', body, re.S)
    m['sites'] = [clean(p) for p in re.findall(r'<(?:p|li)[^>]*>(.*?)</(?:p|li)>', sites.group(1), re.S)][:4] if sites else []
    forms = re.search(r'<h2[^>]*>[^<]*(?:façons|installer)[^<]*</h2>(.*?)<h2', body, re.S)
    m['formules'] = [clean(h) for h in re.findall(r'<h3[^>]*>(.*?)</h3>', forms.group(1), re.S)] if forms else []
    m['images'] = sorted(set(re.findall(r'/assets/img/machines/[^"\')\s]+', s)))
    m['jsonld_types'] = re.findall(r'"@type":\s*"([A-Za-z]+)"', s)
    out.append(m)

dst = HERE / 'machines.json'
dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
for m in out:
    print('\n##', m['slug'], '|', m['h1'])
    print('  intro:', (m['intro'] or ['-'])[0][:200])
    for a, b in m['specs']: print('   -', a, ':', b[:110])
    print('  sites:', ' / '.join(x[:90] for x in m['sites'][:2]) or '-')
    print('  formules:', len(m['formules']), '| images:', [i.split('/')[-1] for i in m['images']], '| json-ld:', sorted(set(m['jsonld_types'])))
