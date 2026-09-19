import re,json,os,glob
from PIL import Image
D=os.path.expanduser("~/Downloads/")
M=[
 dict(slug="animo-optibean-x",img="OptiBean-X-front-zwart.png",fab="Animo",nom="OptiBean X",type="Machine à café en grains, pose libre sur meuble",
  h1="Animo OptiBean X : la machine à café en grains pour les espaces à fort passage",
  lead="Espresso et café filtre fraîchement moulus dans la même machine, écran tactile 7 pouces, jusqu'à 250 boissons par jour selon le constructeur.",
  desc="Animo OptiBean X en entreprise à Paris et en Île-de-France : machine à café en grains jusqu'à 250 boissons par jour, en dépôt, location ou achat.",
  chiffres=[("250","boissons par jour recommandées"),("7\"","écran tactile"),("A+","classe énergétique"),("± 150 000","tasses pour le moulin céramique")],
  specs=[("Production journalière recommandée","jusqu'à 250 boissons"),("Groupe café","X-press, 6 à 20 g, pression de tassage réglable sur 7 niveaux, fabriqué en Suisse"),("Boissons","espresso et café filtre frais, deux tasses en un cycle, sortie d'eau chaude séparée"),("Bacs à grains","1 × 2,2 kg (environ 295 tasses) ou 2 × 1 kg (environ 270 tasses), verrouillables"),("Bacs de produits solubles","1 à 3 (lait, cacao, sucre)"),("Moulin","céramique Ditting, environ 150 000 tasses"),("Écran","tactile 7 pouces, personnalisable (logo, image, vidéo)"),("Paiement et télémétrie","compatible MDB et EVA DTS"),("Dimensions (L × P × H)","409 × 567 × 780 mm"),("Classe énergétique","A+")],
  pour=["Bureaux, accueils et salles de pause très fréquentés","Sites qui veulent à la fois l'espresso et le café filtre","Espaces où la machine est visible : finitions noir ou bois, éclairage LED réglable"],source="Animo, tarif France 2026"),
 dict(slug="animo-optime-x",img="OptiMe_11_Kleuroptie-front-white-510x800.png",fab="Animo",nom="OptiMe X",type="Machine à café en grains compacte",
  h1="Animo OptiMe X : la machine à café en grains compacte pour les bureaux",
  lead="Le même groupe espresso que sa grande sœur dans 38 cm de large, pour les espaces de pause où chaque centimètre compte. Jusqu'à 125 boissons par jour selon le constructeur.",
  desc="Animo OptiMe X pour bureaux à Paris et en Île-de-France : machine à café en grains compacte, jusqu'à 125 boissons par jour. Dépôt, location ou achat.",
  chiffres=[("125","boissons par jour recommandées"),("38 cm","de large"),("25-30 s","pour un café de 120 ml"),("A+","classe énergétique")],
  specs=[("Production journalière recommandée","jusqu'à 125 boissons"),("Groupe café","X-press, 6 à 20 g, double sortie"),("Bacs à grains","1 × 1,2 kg (environ 160 tasses) ou 2 × 600 g"),("Bacs de produits solubles","1 ou 2 (lait, cacao)"),("Capacité horaire","60 tasses en infusion simple, 120 en infusion double"),("Moulin","céramique Ditting, environ 150 000 tasses, moins de 70 dB"),("Écran","tactile 7 pouces, personnalisable"),("Paiement et télémétrie","compatible MDB et EVA DTS"),("Dimensions (L × P × H)","380 × 515 × 600 mm"),("Raccordements","eau 3/4\", 220-240 V, 1 950 W"),("Classe énergétique","A+")],
  pour=["PME et plateaux de bureaux parisiens à l'espace compté","Étages, salles de réunion, espaces de coworking","Sites où le café est offert par l'entreprise"],source="Animo, tarif France 2026"),
 dict(slug="bianchi-agily",img="agily_L-2.jpg",fab="Bianchi Vending",nom="Agily",type="Distributeur automatique de boissons chaudes",
  h1="Bianchi Agily : le distributeur de boissons chaudes à grand écran",
  lead="Café en grains, recettes gourmandes et toppings sur un écran tactile 21 pouces, avec une réserve de plus de 1 000 gobelets pour les sites qui tournent toute la journée.",
  desc="Bianchi Agily en entreprise en Île-de-France : distributeur de boissons chaudes à écran 21 pouces, café en grains, 1 100 gobelets. Dépôt, location, achat.",
  chiffres=[("21\"","écran tactile"),("1 100","gobelets au maximum (Agily L)"),("2","trémies de café en grains"),("10","bacs de produits solubles")],
  specs=[("Modèles","Agily L (H 1 830 mm) et Agily M (H 1 700 mm)"),("Interface","écran tactile 21 pouces, ou interface Smart à 25 boutons avec écran 7 pouces"),("Groupe café","espresso traditionnel, ou chambre variable de 8 à 13 g"),("Café en grains","jusqu'à 2 trémies, dont une sous vide pour la conservation des arômes"),("Bacs de produits solubles","jusqu'à 10, plus bac à sucre"),("Toppings","2 bacs en option (chocolat, céréales)"),("Gobelets","jusqu'à 1 100 (L) ou 910 (M), diamètre variable ; mugs acceptés"),("Paiement","protocoles Executive et MDB"),("Dimensions (H × L × P)","1 830 × 685 × 870 mm (L) · 1 700 × 685 × 870 mm (M)"),("Puissance","1,7 kW, mode économie d'énergie")],
  pour=["Sites industriels et logistiques, équipes en 3×8","Halls, établissements d'enseignement, lieux de passage","Entreprises qui veulent une carte large : cafés, chocolats, thés, potages"],source="Bianchi Industry, fiche technique Agily 2023"),
 dict(slug="bianchi-intuity",img="32_Intuity32_PAZ_0091_ic02.jpg",fab="Bianchi Vending",nom="Intuity",type="Distributeur automatique de boissons chaudes haut de gamme",
  h1="Bianchi Intuity : le distributeur de boissons chaudes à écran 32 pouces",
  lead="Le modèle le plus complet de la gamme : écran tactile 32 ou 21 pouces, double chaudière, deux cafés en grains, toppings, et jusqu'à 1 560 gobelets.",
  desc="Bianchi Intuity pour grands sites en Île-de-France : distributeur de boissons chaudes à écran 32 pouces, double chaudière, 1 560 gobelets. Dépôt ou location.",
  chiffres=[("32\"","écran tactile (Intuity +)"),("1 560","gobelets au maximum"),("2","cafés en grains"),("4","bacs de toppings")],
  specs=[("Modèles","Intuity + (écran 32 pouces) et Intuity (écran 21 pouces)"),("Café en grains","1 ou 2 trémies, dont une sous vide en option"),("Chaudière","double"),("Bacs de produits solubles","4 bacs de 3 l et 3 bacs de 6,5 l, plus sucre 7 kg"),("Toppings","4 bacs (Intuity +), 2 en option (Intuity)"),("Gobelets","deux distributeurs : 650 (Ø 70-74) et 440 (Ø 80), détection de gobelet de série"),("Façade","porte vitrée rétro-éclairée, visuel personnalisable, parcours lumineux"),("Dimensions (H × L × P)","1 830 × 685 × 990 mm"),("Poids","245 kg")],
  pour=["Grands sites tertiaires, sièges et campus","Sites industriels à très forte fréquentation","Lieux où la machine porte aussi l'image : façade personnalisable aux couleurs de l'entreprise"],source="Bianchi, tarif Phygital Solutions 2025"),
 dict(slug="sielaff-siline",img="Produkt_Varianten_Bilder_SiLine_Combi_M-2.png",fab="Sielaff",nom="SiLine Snack et Combi",type="Distributeur automatique de snacks et de boissons fraîches",
  h1="Sielaff SiLine : le distributeur de snacks et boissons fraîches à ascenseur",
  lead="Snacks, canettes, bouteilles et produits frais dans une seule machine, deux zones de température, un ascenseur qui dépose le produit sans le faire tomber. Fabriqué en Allemagne.",
  desc="Sielaff SiLine en Île-de-France : distributeur de snacks et boissons fraîches à ascenseur, deux zones de température, écran tactile. Dépôt, location, achat.",
  chiffres=[("2","zones de température"),("5","produits par achat groupé"),("780 / 990","mm de large, au choix"),("R-290","réfrigérant naturel")],
  specs=[("Gamme","SiLine Snack (spirales) et SiLine Combi (spirales et boissons)"),("Distribution","ascenseur, adapté aux produits fragiles, ronds ou carrés"),("Températures","deux zones distinctes, logiciel de sécurité alimentaire"),("Écran","tactile : ingrédients et allergènes affichés, fonction panier jusqu'à 5 produits, offres menu"),("Configuration","6 à 7 plateaux, spirales et poussoirs pour bouteilles et canettes"),("Dimensions (H × L × P)","1 830 × 990 × 895 mm (modèle M) · largeur 780 mm (modèle S)"),("Poids","environ 340 kg à vide (modèle M)"),("Alimentation","220-230 V, 400 W selon la réfrigération"),("Finitions","noir, aluminium ou blanc")],
  pour=["Salles de pause d'entreprise : un seul meuble pour le snack et le frais","Sites industriels et logistiques sans commerce à proximité","Résidences, hôtels et lieux ouverts en continu"],source="Sielaff, brochure SiLine Snack et Combi 2023"),
 dict(slug="sielaff-robimat",img="Produkt_Varianten_Bilder_Robimat_X-Serie_Robimat_XL.png",fab="Sielaff",nom="Robimat X",type="Distributeur automatique de boissons fraîches",
  h1="Sielaff Robimat X : le distributeur de boissons fraîches grande capacité",
  lead="Une grande vitrine éclairée, un ascenseur qui délivre la boisson en moins de dix secondes sans la secouer, et jusqu'à 770 bouteilles de 50 cl selon la configuration.",
  desc="Sielaff Robimat X en Île-de-France : distributeur de boissons fraîches à ascenseur, jusqu'à 770 bouteilles, vitrine panoramique. Dépôt, location ou achat.",
  chiffres=[("770","bouteilles 50 cl au maximum (XL)"),("< 10 s","par distribution"),("7","plateaux"),("99,7 %","de matériaux recyclables")],
  specs=[("Modèles","Robimat XS (790 mm), XM (990 mm) et XL"),("Distribution","ascenseur, presque sans secousse ; premier entré, premier sorti"),("Capacité","de 405 à 770 boissons selon la configuration (XL)"),("Produits","canettes, bouteilles PET jusqu'à 0,6 l, bouteilles en verre, briques"),("Plateaux","jusqu'à 7, jusqu'à 70 sélections"),("Vitrine","panoramique, éclairage LED"),("Dimensions (H × L × P)","1 830 × 790 × 880 mm (XS) · 1 830 × 990 × 880 mm (XM)"),("Alimentation","220-230 V, 500 W"),("Réfrigérant","R-290, classe énergétique C"),("Finitions","façade peinte (RB) ou inox (EB)")],
  pour=["Sites à forte consommation de boissons fraîches : logistique, industrie, campus","Salles de sport, résidences, lieux de passage","En complément d'une machine à café ou d'un distributeur de snacks"],source="Sielaff, brochure Robimat série X"),
]
os.makedirs("machines",exist_ok=True)
for m in M:
    im=Image.open(D+m["img"]).convert("RGBA"); bg=Image.new("RGBA",im.size,(255,255,255,255)); bg.alpha_composite(im); im=bg.convert("RGB")
    if im.height>1400: im.thumbnail((1400,1400),Image.LANCZOS)
    im.save(f"assets/img/machines/{m['slug']}.webp","WEBP",quality=86,method=6)
    s=im.copy(); s.thumbnail((640,640),Image.LANCZOS); s.save(f"assets/img/machines/{m['slug']}-640.webp","WEBP",quality=82,method=6); m["w"],m["h"]=im.size
src=open('solutions/location-machine-a-cafe-distributeur.html',encoding='utf-8').read()
a=src.index('<!-- HERO -->'); b=src.index('<!-- CTA DIAGNOSTIC'); HEAD,TAIL=src[:a],src[b:]
HEAD=re.sub(r'\s*<script type="application/ld\+json">.*?</script>','',HEAD,flags=re.S)
LOC="/solutions/location-machine-a-cafe-distributeur"
def page(m):
    url=f"https://machinebreak.com/machines/{m['slug']}"; T=f"{m['fab']} {m['nom']} en entreprise : dépôt, location ou achat en Île-de-France | Machine Break"
    assert 140<=len(m["desc"])<=165,(m["slug"],len(m["desc"]))
    h=re.sub(r'<title>.*?</title>',f'<title>{T}</title>',HEAD,flags=re.S)
    for pat,val in [(r'(<meta name="description" content=")[^"]*',m["desc"]),(r'(<meta (?:property|name)="(?:og|twitter):description" content=")[^"]*',m["desc"]),(r'(<meta (?:property|name)="(?:og|twitter):title" content=")[^"]*',T)]:
        h=re.sub(pat,lambda mm,v=val:mm.group(1)+v,h)
    h=h.replace("https://machinebreak.com"+LOC,url)
    h=re.sub(r'(<meta property="og:image" content=")[^"]*',lambda mm:mm.group(1)+f"https://machinebreak.com/assets/img/machines/{m['slug']}.webp",h)
    ld={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Accueil","item":"https://machinebreak.com/"},{"@type":"ListItem","position":2,"name":"Nos machines","item":"https://machinebreak.com/solutions/equipements"},{"@type":"ListItem","position":3,"name":f"{m['fab']} {m['nom']}","item":url}]}
    h=h.replace('</head>','  <script type="application/ld+json">\n'+json.dumps(ld,ensure_ascii=False,indent=2)+'\n  </script>\n</head>',1)
    chif=''.join(f'<div class="col-6 col-md-3 text-center mb-5 mb-md-0"><p class="display-4 text-primary mb-1" style="font-size:2.2rem">{v}</p><p class="text-muted font-size-sm mb-0">{l}</p></div>' for v,l in m["chiffres"])
    rows=''.join(f'<tr><th scope="row" class="font-weight-normal text-muted" style="width:38%">{k}</th><td>{v}</td></tr>' for k,v in m["specs"])
    pour=''.join(f'<div class="d-flex mb-3"><div class="badge badge-rounded-circle badge-success-soft mt-1 mr-4 flex-shrink-0"><i class="fe fe-check"></i></div><p class="mb-0">{x}</p></div>' for x in m["pour"])
    autres=''.join(f'<a class="btn btn-sm btn-outline-primary mr-2 mb-2" href="/machines/{o["slug"]}">{o["fab"]} {o["nom"]}</a>' for o in M if o is not m)
    body=f'''<!-- HERO -->
  <section class="pt-8 pt-md-10 pb-8 bg-light">
    <div class="container"><div class="row align-items-center">
      <div class="col-12 col-lg-7 mb-6 mb-lg-0">
        <p class="font-size-sm text-muted mb-3"><a href="/solutions/equipements" class="text-muted">Nos machines</a> · {m["fab"]}</p>
        <p class="text-uppercase text-success font-weight-bold mb-3">{m["type"]}</p>
        <h1 class="display-4 mb-4">{m["h1"]}</h1>
        <p class="lead text-muted mb-6">{m["lead"]}</p>
        <a class="btn btn-success lift cta-diagnostic" href="/contact#contact-form">Mon diagnostic pause en 1 minute <i class="fe fe-arrow-right ml-2"></i></a>
      </div>
      <div class="col-12 col-lg-5 text-center">
        <div class="bg-white rounded shadow-lg p-5 d-inline-block"><img src="/assets/img/machines/{m["slug"]}.webp" srcset="/assets/img/machines/{m["slug"]}-640.webp 640w, /assets/img/machines/{m["slug"]}.webp {m["w"]}w" sizes="(max-width: 991px) 80vw, 35vw" width="{m["w"]}" height="{m["h"]}" alt="{m["fab"]} {m["nom"]}, {m["type"].lower()}" style="max-height:460px;width:auto;max-width:100%;height:auto"></div>
      </div>
    </div></div>
  </section>

<!-- EN BREF -->
  <section class="py-7 border-bottom"><div class="container"><div class="row">{chif}</div></div></section>

<!-- CARACTÉRISTIQUES -->
  <section class="py-8 py-md-10">
    <div class="container"><div class="row">
      <div class="col-12 col-lg-7 mb-7 mb-lg-0">
        <h2 class="mb-5">Caractéristiques</h2>
        <div class="table-responsive"><table class="table table-sm font-size-sm mb-3"><tbody>{rows}</tbody></table></div>
        <p class="font-size-sm text-muted mb-0">Données constructeur ({m["source"]}), indicatives et variables selon la configuration retenue.</p>
      </div>
      <div class="col-12 col-lg-5">
        <h2 class="h3 mb-4">Pour quels sites</h2>{pour}
        <div class="card shadow-light-lg mt-6"><div class="card-body">
          <h3 class="h4 mb-3">En dépôt, en location ou à l'achat</h3>
          <p class="text-muted font-size-sm mb-3">Dans les trois cas, la machine est connectée, entretenue par nos équipes, et vous suivez chaque intervention dans votre espace client. Nous venons voir votre site avant de recommander un modèle.</p>
          <a href="{LOC}" class="font-weight-bold font-size-sm">Comparer les trois formules <i class="fe fe-arrow-right"></i></a>
        </div></div>
      </div>
    </div></div>
  </section>

<!-- AUTRES MACHINES -->
  <section class="py-7 bg-light"><div class="container text-center"><h2 class="h4 mb-4">Les autres machines que nous installons</h2>{autres}</div></section>

'''
    open(f"machines/{m['slug']}.html","w",encoding="utf-8").write(h+body+TAIL)
for m in M: page(m)
# page équipements : cartes machines
f='solutions/equipements.html'; s=open(f,encoding='utf-8').read()
cards=''.join(f'''
        <div class="col-6 col-md-4 col-lg-2 d-flex mb-5"><a class="card shadow-light-lg lift w-100 text-center" href="/machines/{m["slug"]}"><div class="bg-white p-3"><img src="/assets/img/machines/{m["slug"]}-640.webp" alt="{m["fab"]} {m["nom"]}" loading="lazy" style="height:150px;width:auto;max-width:100%;object-fit:contain"></div><div class="card-body p-3"><p class="font-size-sm text-muted mb-0">{m["fab"]}</p><p class="font-weight-bold mb-0">{m["nom"]}</p></div></a></div>''' for m in M)
block=f'''<!-- FICHES MACHINES -->
  <section class="py-8 py-md-10" id="machines">
    <div class="container">
      <div class="row justify-content-center"><div class="col-12 col-md-10 col-lg-8 text-center"><h2>Les machines que nous installons le plus</h2><p class="font-size-lg text-muted mb-7">Six modèles éprouvés sur nos sites. La recommandation se fait toujours après une visite.</p></div></div>
      <div class="row justify-content-center">{cards}
      </div>
    </div>
  </section>

'''
if 'id="machines"' not in s: s=s.replace('<!-- CTA DIAGNOSTIC',block+'<!-- CTA DIAGNOSTIC',1); open(f,'w',encoding='utf-8').write(s)
d=json.load(open('_data/site.json'))
for m in M:
    u=f"/machines/{m['slug']}"
    if u not in d['staticPages']: d['staticPages'].append(u)
json.dump(d,open('_data/site.json','w'),ensure_ascii=False,indent=2)
r=open('_redirects').read()
for m in M:
    u=f"/machines/{m['slug']}"
    if u+".html" not in r: r+=f"{u+'.html':<62}{u:<27}301!\n"
open('_redirects','w').write(r)
e=open('eleventy.config.js').read()
if '"machines"' not in e: e=e.replace('"solutions", "zones",','"solutions", "zones", "machines",'); open('eleventy.config.js','w').write(e)
print("6 fiches créées")
