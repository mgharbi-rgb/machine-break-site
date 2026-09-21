import pathlib, re
from html.parser import HTMLParser

VOID = {'meta', 'link', 'img', 'br', 'source', 'input', 'hr', 'path', 'circle'}

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.errors = []; self.ids = []; self.counts = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        self.counts[tag] = self.counts.get(tag, 0) + 1
        if tag == 'img' and 'alt' not in a: self.errors.append('img sans alt: ' + a.get('src', '?'))
        if tag == 'a' and a.get('href') == '#': self.errors.append('lien href="#" restant')
        if tag == 'button' and 'type' not in a: self.errors.append('button sans type')
        if tag not in VOID: self.stack.append(tag)
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in VOID: return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append('fermeture inattendue </%s> (pile: %s) ligne %d' % (tag, self.stack[-3:], self.getpos()[0]))
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag: pass
        else:
            self.stack.pop()

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent if '__file__' in dir() else pathlib.Path('.')
for f in sorted((ROOT / 'maquettes').glob('*.html')):
    s = f.read_text(encoding='utf-8'); p = P(); p.feed(s)
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    ctrl = re.findall(r'aria-(?:controls|labelledby)="([^"]+)"', s)
    missing = [c for c in ctrl if c not in p.ids]
    print(f.name, '| main:', p.counts.get('main', 0), '| nav:', p.counts.get('nav', 0), '| h1:', p.counts.get('h1', 0),
          '| skip:', 'class="skip"' in s, '| pile restante:', p.stack, '| ids dupliqués:', dup or '-', '| aria orphelins:', missing or '-')
    for e in p.errors: print('   !!', e)
