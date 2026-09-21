"""Exporte toutes les maquettes dans un dossier autonome, ouvrable par double-clic, sans serveur.

Usage :  python3 tools/maquettes/exporter.py ["chemin/du/dossier"]   (par défaut : Bureau/Maquettes Machine Break)
Le BRIEF.md de ce dossier est copié dans l'export.
"""
import pathlib, re, shutil, sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent.parent
DST = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path.home() / 'Desktop' / 'Maquettes Machine Break'
SITE = 'https://machinebreak.com'

# on ne régénère que notre propre dossier d'export (reconnaissable à son LISEZ-MOI)
if DST.exists() and not (DST / 'LISEZ-MOI.txt').exists():
    sys.exit("Le dossier existe et n'est pas un export des maquettes : %s" % DST)
DST.mkdir(exist_ok=True)
if (DST / 'assets').is_dir(): shutil.rmtree(DST / 'assets')  # ressources régénérées à chaque export

names = sorted(p.name for p in (SRC / 'maquettes').glob('*.html') if not p.name.startswith('_')) + ['m.css', 'm.js', 'n.css', 'n.js']
assets, missing = set(), []

for name in names:
    s = (SRC / 'maquettes' / name).read_text(encoding='utf-8')
    assets.update(re.findall(r'/assets/[^"\')]+', re.sub(r'https?://[^"\')\s]+', '', s)))
    # ressources locales : chemins relatifs au dossier exporté
    s = re.sub(r'(["\'(])/maquettes/', r'\1', s)
    s = re.sub(r'(["\'(])/assets/', r'\1assets/', s)
    if name == 'm.js':
        # sélecteur de direction : fichiers voisins plutôt que les adresses du site
        assert "a.href = '/maquettes/' + p[0];" in (SRC / 'maquettes' / name).read_text(encoding='utf-8')
        s = s.replace("a.href = '' + p[0];", "a.href = p[0] + '.html';").replace("a.href = '/maquettes/' + p[0];", "a.href = p[0] + '.html';")
    elif name.endswith('.html'):
        # liens vers le reste du site : version en ligne
        s = re.sub(r'href="/(?!/)([^"]*)"', lambda m: 'href="%s/%s"' % (SITE, m.group(1)), s)
    (DST / name).write_text(s, encoding='utf-8')

for a in sorted(assets):
    src = SRC / a.lstrip('/')
    if not src.is_file():
        missing.append(a); continue
    out = DST / a.lstrip('/')
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, out)

(DST / 'LISEZ-MOI.txt').write_text(
    "Maquettes Machine Break : dix directions d'interface\n\n"
    "POUR REPRENDRE LE TRAVAIL SUR UN AUTRE ORDINATEUR : lire BRIEF.md (dans ce dossier).\n\n"
    "LA DERNIÈRE, À REGARDER EN PREMIER :\n"
    "  j-enseigne.html       le mix : affiche et lettres pochoir de la E, machine annotée,\n"
    "                        vitrine à codes, onglets, mini-machine qui se vide au défilement,\n"
    "                        prix expliqués en face de chaque machine\n\n"
    "ANGULEUSES (charte stricte, sans rose, avec les six machines) :\n"
    "  g-distributeur.html   la vitrine de distributeur, une case à code par offre\n"
    "  h-sommaire.html       éditorial, index latéral permanent, grand sommaire\n"
    "  i-planche.html        planche technique, machine annotée, onglets de section\n\n"
    "PRÉCÉDENTES : a-nuit-cafe, b-bento, c-editorial, d-connecte, e-affiche, f-immersif\n\n"
    "Double-cliquez sur un fichier .html, puis passez d'une direction à l'autre\n"
    "avec la barre en bas de page (A à J).\n\n"
    "Les maquettes G, H, I, J fonctionnent sans connexion internet. Les maquettes A à F\n"
    "chargent leurs polices de titres en ligne (Google Fonts).\n"
    "Les liens vers le reste du site ouvrent machinebreak.com.\n"
    "Source : branche maquettes-uiux du dépôt machine-break-site.\n", encoding='utf-8')

if (HERE / 'BRIEF.md').is_file(): shutil.copy2(HERE / 'BRIEF.md', DST / 'BRIEF.md')

left = []
for name in names:
    s = (DST / name).read_text(encoding='utf-8')
    left += ['%s: %s' % (name, m) for m in re.findall(r'["\'(]/(?:assets|maquettes)/[^"\')]*', s)]
size = sum(f.stat().st_size for f in DST.rglob('*') if f.is_file())
print('exportés :', len(names), 'fichiers +', len(assets) - len(missing), 'ressources |', round(size / 1e6, 1), 'Mo')
print('ressources introuvables :', missing or 'aucune')
print('chemins absolus restants :', left or 'aucun')
