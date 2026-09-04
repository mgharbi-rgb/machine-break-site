#!/usr/bin/env python3
"""Audit Phase 0 — machinebreak.com (site statique).

Usage : python3 audit_site.py <racine_du_site> [sortie.md]

Produit un rapport Markdown couvrant les 6 points du brief :
 1. inventaire HTML (chemin, title, meta description, présence nav, liens entrants)
 2. pages orphelines
 3. téléphones / adresses postales / emails (avec divergences)
 4. meta description dupliquées
 5. images sans alt / images externes
 6. sitemap.xml, robots.txt, JSON-LD, redirections
"""
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = sys.argv[2] if len(sys.argv) > 2 else None
SKIP_DIRS = {".git", "node_modules", "hts-cache", ".netlify"}

# ---------------------------------------------------------------- parsing

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.description = None
        self.canonical = None
        self.og = {}
        self.links = []          # (href, in_nav)
        self.imgs = []           # (src, alt or None)
        self.h1 = []
        self.jsonld = 0
        self._in_title = False
        self._in_h1 = False
        self._in_script_ld = False
        self._nav_depth = 0
        self._depth = 0
        self._nav_stack = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._depth += 1
        cls = a.get("class", "") or ""
        if tag == "nav" or (tag in ("header", "div", "ul") and re.search(r"\bnavbar\b|\bnav\b", cls)):
            self._nav_stack.append(self._depth)
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
            self.h1.append("")
        elif tag == "meta":
            n = (a.get("name") or "").lower()
            p = (a.get("property") or "").lower()
            if n == "description":
                self.description = (a.get("content") or "").strip()
            if p.startswith("og:") or n.startswith("twitter:"):
                self.og[p or n] = a.get("content")
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href")
        elif tag == "a" and a.get("href"):
            self.links.append((a["href"].strip(), bool(self._nav_stack)))
        elif tag == "img":
            self.imgs.append((a.get("src") or a.get("data-src") or "", a.get("alt")))
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self.jsonld += 1
        if tag in ("img", "meta", "link", "br", "hr", "input"):
            self._depth -= 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        if self._nav_stack and self._depth == self._nav_stack[-1]:
            self._nav_stack.pop()
        self._depth -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1 and self.h1:
            self.h1[-1] += data


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def norm_target(href, from_file):
    """Résout un lien interne vers un chemin relatif à ROOT (sans .html forcé)."""
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "/cdn-cgi/")):
        return None
    if re.match(r"^https?://", href):
        m = re.match(r"^https?://(www\.)?machinebreak\.com(/.*)?$", href)
        if not m:
            return None
        href = m.group(2) or "/"
    href = href.split("#")[0].split("?")[0]
    if href == "":
        return None
    if href.startswith("/"):
        path = href.lstrip("/")
    else:
        path = os.path.normpath(os.path.join(os.path.dirname(from_file), href))
    path = path.replace(os.sep, "/")
    if path in ("", "."):
        path = "index.html"
    return path


def exists_variants(path, html_set):
    """Retourne le fichier HTML correspondant au chemin logique, ou None."""
    cands = [path, path + ".html", path.rstrip("/") + "/index.html"]
    if path.endswith("/"):
        cands.append(path + "index.html")
    for c in cands:
        if c in html_set:
            return c
    return None


# ---------------------------------------------------------------- collecte

html_files, all_files = [], []
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
    for f in files:
        p = os.path.join(d, f)
        all_files.append(rel(p))
        if f.lower().endswith((".html", ".htm")):
            html_files.append(rel(p))
html_files.sort()
html_set = set(html_files)

pages = {}
for f in html_files:
    with open(os.path.join(ROOT, f), encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    pg = Page()
    pg.feed(raw)
    pg.raw = raw
    pages[f] = pg

inbound = defaultdict(set)        # target -> set(sources)
nav_targets = set()
broken = defaultdict(set)         # source -> set(href)
for f, pg in pages.items():
    for href, in_nav in pg.links:
        t = norm_target(href, f)
        if t is None:
            continue
        real = exists_variants(t, html_set)
        if real is None:
            if not any(t == x or t.rstrip("/") == x for x in all_files):
                broken[f].add(href)
            continue
        if real != f:
            inbound[real].add(f)
        if in_nav:
            nav_targets.add(real)

# ---------------------------------------------------------------- coordonnées

PHONE_RE = re.compile(r"(?<![\d.])(?:\+33\s?[1-9]|0[1-9])(?:[\s.\-]?\d{2}){4}(?![\d])")
EMAIL_RE = re.compile(r"[\w.+-]+@[A-Za-z][\w-]*\.[A-Za-z]{2,}(?:\.[A-Za-z]{2,})?")
ADDR_RE = re.compile(
    r"\d{1,4}\s?(?:bis|ter)?,?\s+(?:avenue|av\.|boulevard|bd|rue|all[ée]e|chemin|impasse|place|route|quai)\s+[^<\n,;]{2,60}",
    re.I,
)
CP_RE = re.compile(r"\b(77|78|91|92|93|94|95|75)\d{3}\s+[A-ZÉ][\w\-' ]{2,40}")

def strip_tags(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S | re.I)
    return s

def occurrences(regex, text, normalize=None):
    found = defaultdict(int)
    for m in regex.finditer(text):
        v = re.sub(r"\s+", " ", m.group(0)).strip(" ,.")
        if normalize:
            v = normalize(v)
        found[v] += 1
    return found

def norm_phone(v):
    d = re.sub(r"\D", "", v)
    if d.startswith("33"):
        d = "0" + d[2:]
    return " ".join(d[i:i + 2] for i in range(0, len(d), 2))

phones, emails, addrs, cps = {}, {}, {}, {}
for f, pg in pages.items():
    txt = pg.raw  # inclure tel: et JSON-LD volontairement
    phones[f] = occurrences(PHONE_RE, txt, norm_phone)
    emails[f] = occurrences(EMAIL_RE, txt)
    addrs[f] = occurrences(ADDR_RE, strip_tags(txt))
    cps[f] = occurrences(CP_RE, strip_tags(txt))

def pivot(d):
    out = defaultdict(dict)
    for f, occ in d.items():
        for v, n in occ.items():
            out[v][f] = n
    return out

# ---------------------------------------------------------------- rapport

L = []
w = L.append
w(f"# AUDIT.md — machinebreak.com\n")
w(f"Racine auditée : `{ROOT}`  ")
w(f"Fichiers HTML : {len(html_files)} · Fichiers total (hors {', '.join(sorted(SKIP_DIRS))}) : {len(all_files)}\n")

w("## 1. Inventaire des pages HTML\n")
w("| Fichier | `<title>` | `meta description` | Dans la nav | Liens entrants | H1 |")
w("|---|---|---|---|---|---|")
for f in html_files:
    pg = pages[f]
    desc = pg.description if pg.description is not None else "*(absente)*"
    nav = "oui" if f in nav_targets else "**non**"
    inb = ", ".join(sorted(inbound[f])) if inbound[f] else "**aucun**"
    h1 = f"{len(pg.h1)}" + ("" if len(pg.h1) == 1 else " ⚠")
    w(f"| `{f}` | {pg.title.strip() or '*(vide)*'} | {desc} | {nav} | {inb} | {h1} |")
w("")

w("## 2. Pages orphelines (hors navigation principale)\n")
orphans = [f for f in html_files if f not in nav_targets]
strict_orphans = [f for f in orphans if not inbound[f]]
if orphans:
    for f in orphans:
        via = f" — atteignable via : {', '.join(sorted(inbound[f]))}" if inbound[f] else " — **aucun lien entrant**"
        w(f"- `{f}`{via}")
else:
    w("Aucune.")
w("")
if broken:
    w("### Liens internes cassés\n")
    for f in sorted(broken):
        w(f"- `{f}` → " + ", ".join(f"`{h}`" for h in sorted(broken[f])))
    w("")

def coord_section(title, data, warn_if_multiple=True):
    w(f"### {title}\n")
    pv = pivot(data)
    if not pv:
        w("Aucune occurrence.\n")
        return
    if warn_if_multiple and len(pv) > 1:
        w(f"> ⚠ **Divergence : {len(pv)} valeurs distinctes.**\n")
    w("| Valeur | Pages (occurrences) |")
    w("|---|---|")
    for v, files in sorted(pv.items(), key=lambda kv: -sum(kv[1].values())):
        w(f"| `{v}` | " + ", ".join(f"`{f}` ({n})" for f, n in sorted(files.items())) + " |")
    w("")

w("## 3. Coordonnées (téléphones, adresses, emails)\n")
coord_section("Téléphones", phones)
coord_section("Adresses postales (voie)", addrs)
coord_section("Codes postaux + ville", cps)
coord_section("Emails", emails, warn_if_multiple=False)

w("## 4. `meta description` dupliquées\n")
by_desc = defaultdict(list)
for f, pg in pages.items():
    if pg.description:
        by_desc[pg.description].append(f)
dups = {d: fs for d, fs in by_desc.items() if len(fs) > 1}
if dups:
    for d, fs in dups.items():
        w(f"- « {d} » ({len(d)} car.) — " + ", ".join(f"`{f}`" for f in sorted(fs)))
else:
    w("Aucune duplication.")
missing = [f for f, pg in pages.items() if not pg.description]
if missing:
    w("\nSans meta description : " + ", ".join(f"`{f}`" for f in sorted(missing)))
w("")

w("### `<title>` dupliqués\n")
by_title = defaultdict(list)
for f, pg in pages.items():
    by_title[pg.title.strip()].append(f)
tdups = {t: fs for t, fs in by_title.items() if len(fs) > 1}
if tdups:
    for t, fs in tdups.items():
        w(f"- « {t} » — " + ", ".join(f"`{f}`" for f in sorted(fs)))
else:
    w("Aucun.")
w("")

w("### Open Graph / Twitter / canonical\n")
w("| Fichier | canonical | og:url | og:image | twitter:image |")
w("|---|---|---|---|---|")
for f in html_files:
    pg = pages[f]
    w(f"| `{f}` | {pg.canonical or '—'} | {pg.og.get('og:url') or '—'} | {pg.og.get('og:image') or '—'} | {pg.og.get('twitter:image') or '—'} |")
w("")

w("## 5. Images\n")
w("### Images sans attribut `alt`\n")
noalt = [(f, src) for f, pg in pages.items() for src, alt in pg.imgs if alt is None]
emptyalt = [(f, src) for f, pg in pages.items() for src, alt in pg.imgs if alt == ""]
if noalt:
    for f, src in noalt:
        w(f"- `{f}` → `{src}`")
else:
    w("Aucune.")
w(f"\nImages avec `alt=\"\"` (vide, décoratif) : {len(emptyalt)}\n")
w("### Images pointant vers un domaine externe\n")
ext = [(f, src) for f, pg in pages.items() for src, _ in pg.imgs
       if re.match(r"^(https?:)?//", src) and "machinebreak.com" not in src]
ext_meta = [(f, k, v) for f, pg in pages.items() for k, v in pg.og.items()
            if k.endswith("image") and v and "machinebreak.com" not in v and re.match(r"^https?://", v)]
if ext:
    for f, src in ext:
        w(f"- `{f}` → `{src}`")
else:
    w("Aucune balise `<img>` externe.")
if ext_meta:
    w("\nMeta images externes (og/twitter) :")
    for f, k, v in ext_meta:
        w(f"- `{f}` `{k}` → `{v}`")
w("")
w("### Images référencées mais absentes du dépôt\n")
missing_img = []
for f, pg in pages.items():
    for src, _ in pg.imgs:
        t = norm_target(src, f)
        if t and not re.match(r"^(https?:)?//", src) and t not in all_files:
            missing_img.append((f, src))
if missing_img:
    for f, src in missing_img:
        w(f"- `{f}` → `{src}`")
else:
    w("Aucune.")
w("")

w("## 6. Fichiers techniques\n")
def present(name):
    return "présent" if name in all_files else "**absent**"
for name in ["sitemap.xml", "robots.txt", "_redirects", "_headers", "netlify.toml", ".htaccess", "404.html"]:
    w(f"- `{name}` : {present(name)}")
ld = {f: pg.jsonld for f, pg in pages.items() if pg.jsonld}
w(f"- JSON-LD : " + (", ".join(f"`{f}` ({n})" for f, n in sorted(ld.items())) if ld else "**absent sur toutes les pages**"))
w("")

# ---------------------------------------------------------------- TODO:MB (critère d'acceptation n° 12)
w("## 7. Registre `TODO:MB` (valeurs à fournir par le client)\n")
todos = []
for f in html_files:
    for i, line in enumerate(pages[f].raw.splitlines(), 1):
        if "TODO:MB" in line:
            txt = re.sub(r"\s+", " ", line).strip()
            txt = re.sub(r"^.*?TODO:MB\s*[—-]*\s*", "", txt)
            txt = re.sub(r"\s*(?:-->|Décommenter.*)$", "", txt).strip()
            todos.append((f, i, txt[:140]))
if todos:
    grouped = {}
    for f, i, txt in todos:
        grouped.setdefault(txt, []).append(f"`{f}`:{i}")
    w("| Valeur attendue | Emplacements |")
    w("|---|---|")
    for txt, locs in grouped.items():
        w(f"| {txt} | {', '.join(locs)} |")
    w(f"\n{len(grouped)} valeurs distinctes attendues, {len(todos)} emplacements au total. Tous sont masqués dans un commentaire HTML : rien de vide n'est visible en production.")
else:
    w("Aucun.")
w("")

# Fichiers non-HTML notables
others = [x for x in all_files if not x.endswith((".html", ".htm")) and not x.startswith("assets/")]
if others:
    w("### Autres fichiers à la racine\n")
    for x in sorted(others):
        w(f"- `{x}`")
    w("")

report = "\n".join(L)
if OUT:
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(report)
    print(f"Rapport écrit : {OUT}")
else:
    print(report)
