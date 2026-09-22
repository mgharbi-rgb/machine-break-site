# Brief de reprise · Maquettes du site Machine Break

Rédigé le 21 septembre 2026. Ce document permet de reprendre le travail sur un autre ordinateur, avec ou sans Claude Code, sans rien perdre de ce qui a été décidé. Il vit à deux endroits : dans le dossier exporté « Maquettes Machine Break » et dans le dépôt, sous `tools/maquettes/BRIEF.md`.

---

## 1. Où on en est, en cinq lignes

- Onze maquettes de page d'accueil existent, de A à K. **La référence est K « Épure »** : l'esprit de J (le mix E + G/H/I), allégé après le retour « beaucoup trop d'informations, on s'y perd » : 664 mots au lieu de 3 342, aucun tableau, six blocs.
- Tout est poussé sur GitHub, branche **`maquettes-uiux`**. Rien n'est fusionné, aucune PR n'est ouverte, le site en production n'a pas changé.
- Les maquettes sont des pages de démonstration **non indexées** (`noindex`). Elles ne remplacent pas encore l'accueil.
- Les six machines, leurs caractéristiques, les trois formules, le balisage SEO/GEO et la navigation « Tout ce qu'on fait » sont en place dans G, H, I, J.
- **Ce qui manque pour avancer** : vos montants de prix, vos éléments de preuve sociale, et votre choix final de direction (voir la section 9).

## 2. Récupérer le projet sur l'autre PC

Il faut Git, Node 20 ou plus récent (Netlify construit le site avec Node 20) et Python 3 (seulement pour régénérer ou exporter les maquettes).

```bash
git clone https://github.com/mgharbi-rgb/machine-break-site.git
cd machine-break-site
git checkout maquettes-uiux
npm install
npm run dev
```

Puis ouvrir http://localhost:8080/maquettes/k-epure et changer de maquette avec la barre du bas (A à J). Sous Windows, remplacer `python3` par `python` dans toutes les commandes de ce document.

Sans rien installer : le dossier exporté « Maquettes Machine Break » s'ouvre par double-clic sur un fichier `.html`. C'est une copie de consultation, on ne travaille pas dedans.

Particularité du premier ordinateur (le Mac) : la branche `maquettes-uiux` y est ouverte dans un dossier de travail isolé, `.claude/worktrees/maquettes-uiux`. Sur ce Mac, `git checkout maquettes-uiux` dans le dossier principal échoue donc ; utiliser `git checkout --detach maquettes-uiux` pour seulement regarder. Ce problème n'existe pas sur un clone neuf.

## 3. Carte des fichiers

| Emplacement | Rôle |
|---|---|
| `maquettes/a-nuit-cafe.html` … `f-immersif.html` | Les six premières directions. Socle commun `m.css` et `m.js`. |
| `maquettes/g-distributeur.html`, `h-sommaire.html`, `i-planche.html`, `j-enseigne.html`, `k-epure.html` | Les directions anguleuses. Socle commun `n.css` et `n.js`. **Pages générées**, voir la section 8. |
| `maquettes/m.js` | Sert aux dix pages : barre de changement de maquette, bouton de pause des animations, apparitions au défilement. Pour ajouter une maquette, l'ajouter à la liste `pages` en haut du fichier. |
| `tools/maquettes/` | Générateur, extraction des données machines, export, contrôles, et ce brief. Le dossier `tools` est exclu du site par `.eleventyignore`. |
| `machines/*.html` | Les six fiches machines du site : **seule source** des caractéristiques affichées dans les maquettes. |
| `assets/fonts/Big Shoulders Stencil Display/` | Police pochoir de J, hébergée en local, licence libre OFL. |
| `assets/css/mb-ui.css` | La charte réelle du site (variables de couleur). |

Branches : `main` (production), `maquette-ui` (maquettes A à F d'origine, commit `39a3005`), `maquettes-uiux` (tout le travail décrit ici, construite sur `maquette-ui`).

Commits de `maquettes-uiux`, du plus ancien au plus récent :
1. `fbd8838` passe d'accessibilité et d'ergonomie sur A à F (menu mobile, focus clavier, contrastes, pause des animations, onglets et carrousel au clavier).
2. `f3aaf7e` directions G, H, I avec les six machines et le balisage SEO/GEO.
3. `6822a9d` direction J, jauge liée au défilement, bloc prix, camionnette retirée.
4. `18aa03b` outils portables dans `tools/maquettes/` et ce brief.
5. Le commit suivant ajoute K « Épure ».

Règle apprise avec K : **une idée par bloc, une phrase par idée**. La page d'accueil oriente ; les caractéristiques, la F.A.Q., les zones et le comparatif des formules vivent sur leurs pages.

## 4. La charte et vos préférences (à respecter sans exception)

- **Couleurs** : bordeaux `#753F48`, bordeaux foncé `#4e2930`, encre `#1f1517`, texte `#3a2f31`, gris `#6b5d60`, crème `#faf5f1`, sable `#f1e8e2`, filet `#eadfd8`.
- **Aucune écriture rose.** Le rose `#f2a7b1` des maquettes A à F ne fait pas partie de la charte, il avait été ajouté par-dessus.
- **Police** : HK Grotesk partout. Seule exception, à valider par vous : la police pochoir Big Shoulders Stencil Display pour les titres de J, reprise de la E que vous aimez.
- **Pas de style « trop rond, IA vibe codé »** : pas de boutons en pilule, pas de grands rayons, pas de verre dépoli, pas de dégradés ni de halos. Angles droits, filets visibles, ombres franches décalées.
- **Un « petit truc en plus »** lié au métier : la vitrine à codes, la machine annotée, la mini-machine qui se vide.
- **Navigation très simple** : le prospect doit retrouver tout ce que fait Machine Break. D'où le bouton « Tout ce qu'on fait » (plan complet en quatre colonnes), repris dans le pied de page.
- **Les machines sont présentées par familles** (café en grains, boissons chaudes, boissons fraîches et snacks), **sans nommer les fabricants ni les modèles** sur la page d'accueil : on les décrit par ce qu'elles font (« la compacte », « grand écran »), avec leurs chiffres réels. Dire « six machines » est réducteur. L'utilisateur envisage des noms maison : à décider par lui, jamais inventés par nous.
- **SEO et GEO soignés** (section 7).
- **Pas de détourage de la camionnette.**
- **But affiché** : attirer le visiteur et lui donner envie de parcourir le site, en s'appuyant sur des études (section 6).
- **Règle absolue sur le contenu : ne rien inventer.** Aucun chiffre, aucun prix, aucun client, aucun avis qui ne vienne pas du site ou de vous.

## 5. Les dix maquettes

| | Nom | En une ligne | Statut |
|---|---|---|---|
| A | Nuit café | Sombre, photo plein écran, halo | Écartée (ronde, rose) |
| B | Bento | Tuiles arrondies | Écartée |
| C | Éditorial | Serif, cartes empilées | Écartée |
| D | Connecté | Style SaaS, onglets | Écartée |
| E | Affiche | Aplat bordeaux, lettres pochoir, ombres franches | **Style aimé**, mais texte rose |
| F | Immersif | Panneaux photo plein écran | Écartée |
| G | Distributeur | L'accueil est une vitrine de distributeur : douze cases à code, de A1 à C4, écran et clavier | Style aimé |
| H | Sommaire | Éditorial suisse, index latéral permanent, grand sommaire numéroté | Style aimé |
| I | Planche | Planche technique, machine annotée à cinq repères, onglets de section | Style aimé |
| J | Enseigne | Le mix : affiche et pochoir de la E, machine annotée et onglets de I, vitrine de G, têtes numérotées de H | Aimée dans l'esprit, jugée trop chargée |
| **K** | **Épure** | **J allégée : héros, quatre cases « Ce qu'on fait », trois pas, trois familles de machines sans marque, trois formules, quatre secteurs, appel final. Les détails restent sur les pages intérieures.** | **Référence** |

Ce que J ajoute : une mini-machine fixe à l'écran qui se vide case par case quand on défile, atteint son seuil, déclenche le passage puis se re-remplit, trois fois sur la hauteur de la page ; des onglets de section qui restent cochés une fois parcourus ; un bloc « Combien ça coûte » en face de chaque machine.

## 6. Les choix de conception et les études derrière

| Choix dans J | Étude ou principe |
|---|---|
| Héros simple : un message, une machine, un seul bouton d'action, en-tête classique | La première impression se forme en 50 ms (Lindgaard et al., 2006) ; elle est meilleure quand la page est visuellement simple et conforme aux habitudes (Tuch et al., 2012) |
| Bouton d'action et invitation à défiler placés en haut ; la légende des repères dépasse en bas d'écran | 57 % du temps de lecture se passe au-dessus de la ligne de flottaison, 74 % dans les deux premiers écrans (NN/g, « Scrolling and Attention ») |
| Prix expliqués en face de chaque machine | Le prix est l'information n° 1 attendue sur un site B2B, les visiteurs quittent les sites qui le cachent ; à défaut de tarif exact, donner des prix pour des cas types (NN/g) |
| « Faites défiler : la machine se vide. Regardez ce qui se passe au seuil » | Écart de curiosité (Loewenstein, 1994) |
| Onglets qui restent cochés, jauge qui progresse | Gradient de but et progression amorcée (Kivetz et al., 2006 ; Nunes et Drèze, 2006) |
| Vitrine en trois rangées de quatre cases | Loi de Hick ; mémoire de travail d'environ quatre éléments (Cowan, 2001) |
| Liens à libellé explicite avec un sous-texte | Recherche d'information, « odeur » des liens (Pirolli et Card, 1999) |

Vérifiés à la source pendant le travail : les trois chiffres NN/g, Lindgaard 2006, Tuch 2012. Les autres références sont classiques mais n'ont pas été revérifiées. Liens : nngroup.com/articles/show-price, nngroup.com/articles/show-prices-for-common-scenarios, nngroup.com/articles/scrolling-and-attention.

Accessibilité, sur les dix pages : lien « Aller au contenu », focus clavier à double anneau, cibles de 44 px, menu mobile, bouton de pause des animations, respect de `prefers-reduced-motion`, contrastes calculés (`tools/maquettes/contraste.py`).

## 7. SEO et GEO : ce qui est fait, ce qui reste à la mise en ligne

Fait dans G, H, I, J : un seul `h1` qui contient les mots-clés, hiérarchie de titres sans saut, bloc « En bref » en trois phrases citables plus une liste de faits, huit vraies questions de la F.A.Q., section zones avec liens vers les cinq pages de zone et l'adresse, textes alternatifs descriptifs, dimensions d'image déclarées, image principale préchargée, polices locales, aucun script ni police externe. Données structurées JSON-LD : `LocalBusiness` (adresse, téléphone, zones desservies), `WebSite`, `Service` avec ses trois offres, `ItemList` de six `Product` avec toutes leurs caractéristiques, `FAQPage`.

À faire quand une maquette devient la vraie page d'accueil :
1. Retirer `<meta name="robots" content="noindex, nofollow">` et ajouter `<link rel="canonical" href="https://machinebreak.com/">` (un commentaire dans le code le rappelle).
2. Vérifier que le JSON-LD ne fait pas doublon avec celui des gabarits du site (`_includes/layout-base.njk`).
3. Ajouter des prix aux `Product` si vous décidez de les publier : sans prix, pas d'affichage enrichi Google, mais les fiches restent lisibles par les moteurs et les IA.
4. Tester avec l'outil de test des résultats enrichis de Google et avec Lighthouse.

## 8. Régénérer, contrôler, exporter

Les pages G, H, I, J sont produites par un générateur : **ne pas les modifier à la main, la prochaine génération écraserait vos changements.** Modifier les gabarits, puis régénérer.

```bash
python3 tools/maquettes/extraire_machines.py   # seulement si une fiche machines/*.html a changé
python3 tools/maquettes/generer.py             # réécrit maquettes/g…, h…, i…, j….html
python3 tools/maquettes/verifier_seo.py        # balises, ancres, titres, JSON-LD, images, absence de rose
python3 tools/maquettes/exporter.py            # dossier autonome sur le Bureau (ou : exporter.py "autre/chemin")
```

- `generer.py` : textes, données, JSON-LD et sections communes (en bref, fonctionnement, machines, formules, engagements, secteurs, zones, questions, pied de page).
- `gabarits_ghi.py` : héros, navigation et habillage de G, H, I. `gabarit_j.py` : ceux de J, plus la jauge. `gabarit_k.py` : K, page complète et courte.
- `maquettes/n.css` et `n.js` : socle commun, modifiables directement.
- Les pages A à F sont écrites à la main et se modifient directement.
- Ces scripts n'utilisent que la bibliothèque standard de Python et fonctionnent sur macOS, Windows et Linux. La régénération a été vérifiée : elle redonne exactement les pages committées.

## 9. Ce qui reste à faire et les questions ouvertes

Ce qui dépend de vous :
1. **Les prix.** Le site n'en publie aucun. Dans J, les emplacements « montant à renseigner » et « prix à renseigner » attendent vos chiffres : un « à partir de X € par mois » par machine en location, ou deux ou trois cas types (par exemple « 30 personnes, OptiMe X en location »). Recommandation : les afficher.
2. **La preuve sociale.** Logos de clients, avis Google, nombre de machines installées, ancienneté. Rien n'a été inventé, donc rien n'est affiché. C'est le levier de conviction suivant.
3. **La police pochoir** de J : la valider, ou revenir à HK Grotesk pour les titres.
4. **Le choix final** : K telle quelle, ou K avec un élément repris de J (repères sur la machine, vitrine à codes, onglets de section).

Ce qui suit une fois le choix fait :
5. Intégrer la direction retenue dans les vrais gabarits Eleventy (`_includes/header.html`, `footer.html`, `layout-base.njk`) pour que tout le site partage l'en-tête « Tout ce qu'on fait » et le pied de page, puis décliner les pages intérieures (fiches machines, secteurs, formules, zones, F.A.Q., contact).
6. Tester sur de vrais téléphones et avec un lecteur d'écran : les contrôles ont été faits dans Chrome sans interface, à 1440 px et à 375 px seulement.
7. Décider du sort de la mini-machine sur mobile, où elle occupe un coin de l'écran.
8. Fusionner : `git checkout maquette-ui && git merge maquettes-uiux`, ou ouvrir une PR vers `main`.

## 10. Le skill de design « ui-ux-pro-max » sur l'autre PC

Ce skill Claude Code (github.com/nextlevelbuilder/ui-ux-pro-max-skill) a servi de base de règles : priorités d'accessibilité, styles, structure de page. Il a été **audité avant installation** : le cœur du skill est entièrement local (lecture de fichiers CSV, aucun réseau, aucun sous-processus), sans instruction malveillante ni caractère invisible. Il est installé sur le Mac dans `~/.claude/skills/ui-ux-pro-max`, épinglé au commit audité **`dcc40ff5133ef78276117db0cc34e7b83cc8aeba`** (version 2.13.0).

Pour l'autre PC, mêmes règles :
- Installer **par copie du dossier** `.claude/skills/ui-ux-pro-max` du dépôt, **à ce commit précis**, vers le dossier `skills` de Claude (`~/.claude/skills/` ou `%USERPROFILE%\.claude\skills\`). Retirer `scripts/tests`. Dans `SKILL.md`, remplacer `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/` par le chemin réel d'installation, et `python` par la commande Python de la machine.
- **Ne pas utiliser** `npx ui-ux-pro-max-cli`, ni le marketplace de plugins, ni `stack/scripts/setup.sh` : ils téléchargent du code non audité, et le dossier `stack/` active des réglages trop permissifs. Pour mettre à jour, relire d'abord le diff depuis `dcc40ff`.
- Le skill penche vers React et Tailwind, et sa palette par défaut (bleu marine) ne convient pas : on n'en garde que les règles d'ergonomie et de structure, jamais les couleurs ni les polices.
- Il est utile mais pas indispensable : tout ce qu'il a apporté est déjà consigné dans ce brief.

## 11. Message de reprise à coller dans Claude Code sur l'autre PC

Claude n'aura ni la mémoire ni l'historique du Mac. Ouvrir Claude Code dans le dossier du dépôt et coller :

> Lis `tools/maquettes/BRIEF.md` en entier avant toute chose : il contient l'état du projet, la charte, mes préférences et les règles à respecter. Enregistre en mémoire les sections 4 et 10. Nous travaillons sur la branche `maquettes-uiux`. La maquette de référence est K (`maquettes/k-epure.html`), produite par `tools/maquettes/generer.py` : on modifie les gabarits, jamais le HTML généré. N'invente aucun chiffre, prix, client ni avis. Pas d'écriture rose, pas de formes rondes. Vérifie ton travail par un rendu réel à 1440 px et à 375 px, relance `verifier_seo.py`, puis régénère le dossier du Bureau avec `exporter.py`. Commence par me résumer le brief en dix lignes et par me demander ce que je veux faire parmi les points de la section 9.

## 12. Coordonnées utilisées dans les maquettes

Machine Break · 28 avenue Christian Doppler, 77700 Bailly-Romainvilliers · 01 74 81 09 52 · machinebreak.com. Marques sœurs citées dans le menu : Tazza (cafés et restaurants, tazza.fr) et L.A Concept (Côte d'Azur, Monaco, Genève, lac.ltd).
