# AUDIT.md — machinebreak.com

**Phase 0 du brief « génération de leads B2B »** · Audit réalisé le 2026-09-03 sur le dépôt `mgharbi-rgb/machine-break-site` (branche `main`, dernier commit `e83d8c0` du 2025-10-09), croisé avec la version en ligne servie par Netlify derrière Cloudflare.

Régénérer la partie automatique : `npm run build && python3 tools/audit_site.py _site > /tmp/auto.md` puis remplacer la section « Relevé automatique » ci-dessous.

---

## A. Synthèse — ce qu'il faut retenir

1. **Deux générations du site coexistent**, confirmé. L'ancienne génération représente **5 fichiers**, pas 2 : les deux orphelines connues, mais aussi `careers.html`, `career-single.html` et `terms-of-service.html`, qui portent encore l'adresse de La Garenne-Colombes, le 01 70 82 31 32 et le logo `.jpg`. `terms-of-service.html` contient en plus un **troisième numéro** (01 85 65 81 51).
2. **Trois pages supplémentaires hors brief** ont été découvertes : `avantages.html` (brouillon inachevé, sans H1 ni meta, lien cassé vers `pourquoi-nous.html`, lien de nav présent mais commenté sur 4 pages), `career-single.html` (gabarit Landkit brut : « UX Design Lead », `hello@domain.com`) et `admin/` (interface Netlify CMS chargée depuis unpkg.com, publiquement accessible en ligne, backend git-gateway pointant sur `main`).
3. **Aucun mécanisme de redirection** n'existe (`_redirects`, `netlify.toml` absents). Toutes les URL, orphelines comprises, répondent 200 en production, et chaque page est servie **en double** (`/contact` et `/contact.html`) sans canonical.
4. **Le bloc statistiques** de l'accueil n'est pas un bug d'affichage mais un bug de fond : les valeurs `100 %` satisfaction et `24/7` support sont codées en dur via countup.js, sans source. À supprimer ou à remplacer par des valeurs client (§ 7 du brief).
5. **La bibliothèque fancybox est cassée sur toutes les pages** : le chemin est écrit `assets/libs/%40fancyapps/…` (l'« @ » encodé) alors que le dossier s'appelle `@fancyapps`. 404 silencieux en production.
6. **Poids des images** : 8 images dépassent 3 Mo (record 12 Mo pour `secteurs/sante.webp`), pour 66 Mo d'assets. Le score mobile en souffre nécessairement.
7. **Mesure** : seul un tag Google Ads (`AW-10786145165`) est posé, sur 3 pages seulement. Pas de GA4, pas de Search Console, pas de consentement cookies.
8. Le formulaire de contact est un formulaire Netlify Forms fonctionnel (7 champs, 4 obligatoires), mais **le sélecteur d'effectif a des `value` décalées par rapport aux libellés** (« Moins de 49 » envoie « Moins de 19 », etc.). Pas de page de remerciement, pas de consentement RGPD.

## B. Inventaire commenté des pages

| Fichier | Génération | Verdict Phase 1 |
|---|---|---|
| `index.html` | actuelle | conserver, corriger (3 H1, stats, faute, og) |
| `boissons-chaudes-snacks.html` | actuelle | conserver, corriger (2 H1, og) |
| `solution-par-secteur.html` | actuelle | conserver ; sera éclatée en 3 pages sectorielles (Phase 3) |
| `fonctionnement.html` | actuelle | conserver, réviser |
| `faq.html` | actuelle | conserver, ajouter JSON-LD FAQPage |
| `contact.html` | actuelle | conserver, refondre le formulaire (Phase 2) |
| `careers.html` | **ancienne** (adresse 92, tél. 01 70, logo .jpg, title « Landkit ») | mettre à jour coordonnées + title/meta, ou supprimer si le recrutement ne passe pas par le site |
| `career-single.html` | **ancienne**, gabarit brut non personnalisé | supprimer + 301 vers `/careers` |
| `terms-of-service.html` | **ancienne** (3 numéros différents dans la page, nav de l'ancienne génération) | réécrire coordonnées et nav ; **le corps est un texte de gabarit Landkit** (« Licensing Terms », « vendeur sur notre plateforme ») : CGU réelles à fournir ou redirection vers `/mentions-legales` |
| `location-distributeurs-automatiques-boissons.html` | **ancienne**, orpheline | 301 → `/fonctionnement` (contenu extrait dans `CONTENU-RECUPERE.md`) |
| `entreprise-location-distributeur-automatique-boisson.html` | **ancienne**, orpheline | 301 → `/boissons-chaudes-snacks` |
| `avantages.html` | brouillon (hors brief) | supprimer + 301 → `/fonctionnement`, retirer le lien de nav commenté sur 4 pages |
| `admin/index.html` + `admin/config.yml` | Netlify CMS (hors brief) | **décision client requise** : le brief interdit le CMS ; recommandation = supprimer le dossier (dépendance externe unpkg, surface d'attaque, backend sur `main`) |

Fichiers parasites à la racine : `backblue.gif`, `fade.gif` (résidus HTTrack), `assets/img/partenaires/test`, `assets/img/secteurs/test` (fichiers vides).

## C. Coordonnées — état des divergences

| Donnée | Version actuelle (6 pages) | Ancienne génération (5 pages) | Autre |
|---|---|---|---|
| Adresse | 28 avenue Christian Doppler, 77700 Bailly-Romainvilliers | 71 boulevard National, 92250 La Garenne-Colombes | — |
| Téléphone | 01 74 81 09 52 (`tel:0174810952`) | 01 70 82 31 32 | 01 85 65 81 51 (×2 dans `terms-of-service.html`) |
| Email | contact@machinebreak.com | contact@machinebreak.com | hello@domain.com (`career-single.html`) |
| Logo | `assets/img/logo.webp` | `assets/img/logo.jpg` | `logoweb.png`, `logoblanc.webp` |
| JSON-LD | `Organization` sur l'accueil uniquement, tél. `+33-1-7481-0952` | — | — |

Adresse et numéro retenus comme uniques : **ceux de la version actuelle** (Bailly-Romainvilliers, 01 74 81 09 52), sauf contre-ordre client (§ 8 du brief).

## D. SEO technique — état initial

- `<title>` : uniques sur les 6 pages actuelles, mais aucun ne suit le format `[Besoin] + [Zone] | Machine Break` ; aucun ne mentionne l'Île-de-France. « Landkit » sur 2 pages.
- `meta description` : uniques sur les 6 pages actuelles (contrairement à ce qu'annonce le brief, corrigé depuis). `@@pageDescription` non remplacé sur 3 pages, absente sur 2.
- `og:url` = `index.html` sur 8 pages ; `og:image` = image tierce `socialbrew.dk` sur 8 pages ; absents sur `faq`, `fonctionnement`, `solution-par-secteur`.
- **Aucune balise `canonical`** sur aucune page, alors que chaque page existe sous deux URL.
- H1 : 3 sur l'accueil, 2 sur `boissons-chaudes-snacks`, 0 sur `avantages` et `entreprise-location-…`.
- `alt` : présent sur toutes les `<img>` (qualité descriptive non évaluée ici).
- `sitemap.xml` : généré à la main (xml-sitemaps.com, lastmod 2025-07-08), **liste les pages orphelines et `career-single`**, pas `avantages`.
- `robots.txt` : minimal dans le repo ; Cloudflare y injecte en production un bloc « Content-Signal » qui bloque GPTBot, ClaudeBot, CCBot… (réglage Cloudflare, pas repo).
- Liens internes : tous en `page.html` ; Netlify sert aussi `/page`. Le sitemap référence les URL sans extension. Cible : canonical + liens internes sans extension + 301 `*.html → /page`.
- Fichiers `.webp` majoritaires ; restent `logo.jpg`, `logoweb.png`, `angle-right.png` (280 Ko).

## E. Décisions à prendre par le client avant Phase 1

- [ ] Suppression du dossier `admin/` (Netlify CMS) — recommandé.
- [ ] Sort de `careers.html` : mise à jour ou suppression.
- [ ] Sort du tag Google Ads `AW-10786145165` : à conserver et généraliser (avec consentement) ou à retirer.
- [ ] Confirmation de l'adresse et du numéro uniques (Bailly-Romainvilliers / 01 74 81 09 52).
- [ ] Valeurs juridiques (§ 8 du brief) pour `/mentions-legales`.

## E-bis. État d'avancement

### Phase 1 — corrections critiques (2026-09-03) ✅

Décisions client du 2026-09-03 : suppression d'`admin/`, suppression de `careers.html` et `career-single.html`, tag Google Ads conservé (généralisation avec consentement en Phase 3.1), coordonnées uniques confirmées.

- **Supprimé** : 2 pages orphelines, `careers.html`, `career-single.html`, `avantages.html`, dossier `admin/`, résidus HTTrack (`backblue.gif`, `fade.gif`, commentaires « Mirrored from »), fichiers vides `test`.
- **`_redirects`** créé : 301 pour `/index.html`, les 5 pages supprimées (avec et sans `.html`) et `/admin/*`. Liens internes `index.html` → `/` pour ne pas déclencher la redirection.
- **`CONTENU-RECUPERE.md`** : engagement de service, catalogue Necta (archivé, périmé), title/meta d'origine, table des redirections.
- **Coordonnées** : une seule adresse (28 Avenue Christian Doppler, 77700 Bailly-Romainvilliers), un seul numéro (01 74 81 09 52), un seul email. Nav et pied de page des CGU alignés sur la version actuelle.
- **Bugs visibles** : bloc statistiques retiré (remplacé par un `TODO:MB`), `og:image`/`twitter:image` → `assets/img/og-image.jpg` (1200×630, 100 Ko, généré depuis la photo du hero), `og:url`/`twitter:url` absolus par page, blocs OG ajoutés sur les 3 pages qui n'en avaient pas, « séléctionnés » corrigé, chemin fancybox `%40fancyapps` → `@fancyapps`.
- **Meta descriptions** : réécrites sur les 9 pages, uniques, 150–160 caractères, zone géographique incluse.
- **Légal** : `/mentions-legales` et `/politique-de-confidentialite` créés (gabarit FAQ, valeurs juridiques en `TODO:MB`), liés depuis le pied de page de toutes les pages ; « Carrière » retiré de la rubrique Légal ; case de consentement obligatoire ajoutée au formulaire. Bandeau cookies reporté à la Phase 3.1 (avec GA4), conformément au brief.
- **`sitemap.xml`** régénéré : 9 URL, sans extension.
- Fins de ligne normalisées en LF sur `index.html`, `contact.html`, `terms-of-service.html` (étaient en CRLF).

### Phase 2 — conversion (2026-09-03) ✅

- **En-tête unique sur toutes les pages** : bandeau sombre avec le téléphone en `tel:` cliquable (horaires en `TODO:MB`), emplacement « Espace client » commenté avec `TODO:MB` (aucun lien mort), CTA principal en bouton contrasté. Les 6 variantes de nav qui coexistaient sont remplacées par un seul bloc.
- **CTA unique « Mon diagnostic pause en 1 minute »** (classe `cta-diagnostic`, cible `/contact#contact-form` en attendant l'URL Typeform/Tally) : en-tête, fin de chaque section de l'accueil, bas de chaque page intérieure. Les 12 libellés précédents (« Et si on s'occupait de vos pauses ? », « Et maintenant, on installe ? », « Parlons café… », etc.) ont disparu.
- **Formulaire de contact** : 3 champs visibles (email, téléphone, effectif), seconde étape repliable (nom, prénom, entreprise, commune, message), consentement RGPD, `action="/merci"`. Les `value` du sélecteur d'effectif sont alignées sur les libellés (bug corrigé). Délai de réponse en `TODO:MB`.
- **`/merci`** créée (`noindex`, exclue du robots.txt), base du suivi de conversion GA4 en Phase 3.1. Elle n'a volontairement aucun lien entrant.
- **Bloc « Nos engagements »** sur l'accueil et la page secteurs : 5 lignes qualitatives (fréquence de passage, délai d'intervention, remplissage, pannes résolues au passage, interlocuteur unique) ; les valeurs chiffrées sont en `TODO:MB`, y compris la « demi-journée » de l'ancienne page, non validée.
- **Section « Plateforme client »** sur l'accueil, au même niveau que l'offre : liste de ce que le client voit (ventes par machine et par site, historique horodaté, délais constatés, alertes et suites, réassorts, consolidation multi-sites), emplacement de captures d'écran en `TODO:MB`.
- **Reformulations** appliquées (accueil, offre, fonctionnement, secteurs) : « vous suivez vos machines en temps réel », « sans aucune zone d'ombre », « chaque intervention tracée, horodatée, consultable » ; plus de « nous supervisons », « sans aucune intervention de votre part », « maintenance proactive ».

### Phase 3.1 — mesure (2026-09-03) ✅ (identifiant GA4 en attente)

- **`assets/js/mb-consent.js`** (sans dépendance) : bandeau cookies Accepter / Refuser, choix conservé 6 mois en `localStorage`, lien « Gérer les cookies » en pied de page pour rouvrir. **Rien n'est chargé avant le consentement.**
- **GA4** : configuré dans le script, identifiant en `TODO:MB` (`CONFIG.ga4Id`). **Google Ads** (`AW-10786145165`) conservé et généralisé aux 10 pages, chargé uniquement après accord (avant : 3 pages, sans consentement).
- **Événements de conversion** : `generate_lead` + conversion Ads « Form rempli » sur `/merci` (auparavant la conversion Ads se déclenchait à chaque affichage de `/contact`, donc fausse), `tel_click` sur tout lien `tel:`, `cta_diagnostic_click` sur `.cta-diagnostic`.
- **Search Console** : emplacement de la balise `google-site-verification` en `TODO:MB` dans le `<head>` de l'accueil (alternative : vérification DNS via Cloudflare).
- Les trois snippets Google inline (dont un helper `gtagSendEvent` jamais appelé) ont été retirés.

### Phase 4 — SEO technique et performance (2026-09-03) ✅

- **`<title>`** au format `[Besoin] + [Zone] | Machine Break` sur les 6 pages métier (Île-de-France dans chacun) ; pages légales et `/merci` gardent un titre fonctionnel.
- **`canonical`** sur les 10 pages (URL sans extension) ; **liens internes** tous convertis vers les URL sans extension ; **`_redirects`** : chaque `/page.html` renvoie un 301 vers `/page`. Fin du contenu servi en double.
- **Un seul `<h1>` par page** : sur l'accueil, le H1 devient « Distributeurs automatiques connectés pour entreprises en Île-de-France » (le nom de marque passe en paragraphe stylé, « Bienvenue chez Machine Break » en H2) ; « Notre offre » passe en H2 sur la page offre.
- **JSON-LD** : `LocalBusiness` sur l'accueil (adresse unique, téléphone, `areaServed` Île-de-France + 8 départements, réseaux sociaux ; horaires en `TODO:MB`) remplace l'ancien `Organization` ; `FAQPage` généré depuis les 8 questions de `/faq`.
- **`alt` descriptifs** rédigés après visualisation des images pour les 20 `alt="..."` et 4 alt approximatifs.
- **Images** : 13 fichiers lourds recompressés (côté max 1920 px, WebP qualité 80) — ex. `secteurs/sante.webp` 12,5 Mo → 111 Ko, slider d'accueil 3 × 6 Mo → 53 à 110 Ko. `loading="lazy"` sur les images sous la ligne de flottaison. Dossier `assets` : **66 Mo → 9,1 Mo**.
- **Dépendances retirées** (aucune n'était utilisée, le thème teste leur présence) : highlight.js (730 Ko), Quill, Dropzone, Isotope, Choices, CountUp, Fancybox, jarallax-video/element, et les services externes Mapbox, Cloudimage (token `aympdnreno`), Font Awesome CDN, AOS via jsDelivr. Scripts en double de `fonctionnement.html` dédoublonnés. 23 fichiers sans référence supprimés (dont `Intro.MP4`, 4 Mo).
- **Score PageSpeed mobile** : à mesurer sur l'aperçu Netlify (non mesurable hors ligne). Point à vérifier sur mobile réel : le bouton hamburger n'apparaît pas dans les captures headless à 390 px, y compris sur la version en production actuelle (probable artefact du rendu headless).

### Phase 3 — architecture et nouvelles pages (2026-09-03) ✅ (contenus client en attente)

Arborescence cible du brief posée, en fichiers `.html` dans des sous-dossiers servis sans extension par Netlify (`/solutions/bureaux-pme` → `solutions/bureaux-pme.html`). À vérifier sur l'aperçu Netlify : si l'option « Pretty URLs » ajoute un slash final, ajuster canonical et sitemap.

- **3 pages sectorielles** au contenu distinct, trame du brief respectée (titre = requête du prospect, problème concret, configuration type, engagements, emplacement cas client en commentaire `TODO:MB`, FAQ sectorielle 4-5 questions avec JSON-LD `FAQPage`, CTA) : `/solutions/bureaux-pme` (QVT, produit, zéro gestion), `/solutions/residences-hotels` (24/7 sans personnel, sans contact, discrétion), `/solutions/industrie-logistique` (3×8, environnement, capacité, réassort sur rotations).
- **`/solutions/equipements`** : quatre familles de machines et critères de choix ; le catalogue détaillé (marques, modèles) est en `TODO:MB` car le parc Necta archivé est périmé selon le client.
- **`/grands-comptes`** : argument central, dispositif de suivi, engagements contractualisables, pièces administratives sur demande, double CTA. Chiffres de capacité en `TODO:MB`. **Mécanisme « dossier contre email »** : formulaire Netlify `dossier-capacite` (email + organisation + consentement) → `/merci-dossier` (noindex). **Tant que le PDF n'est pas fourni, la page annonce un envoi par email : l'équipe doit l'assurer manuellement à chaque soumission** (notification Netlify Forms à activer). Dès le PDF déposé, remplacer par un téléchargement direct (commentaire `TODO:MB` dans la page).
- **Page pilier `/zones/ile-de-france`** + 3 pages de zone (`seine-et-marne`, `marne-la-vallee`, `est-parisien`) : communes et pôles d'activité nommés, typologies de sites, texte propre à chaque zone (aucune substitution de nom de ville). Délai d'intervention réel et références locales en `TODO:MB`. Roissy / Ouest / Sud annoncés « prochainement », non créés (consigne du brief).
- **Navigation** : menu Solutions réorganisé (3 secteurs, tous les secteurs, distributeurs, boissons & snacks, grands comptes, zones) ; pied de page enrichi (Grands comptes, Île-de-France) sur les 20 pages ; la page hub `/solution-par-secteur` renvoie vers les pages dédiées.
- **Sitemap** : 18 URL (les deux pages de remerciement exclues, `noindex` + robots).

### Compléments du 2026-09-04 (retours client) ✅

- **Engagements réécrits** selon le fonctionnement réel : « Réassort piloté par la télémétrie » (pas de passage à date fixe, c'est le remplissage et les habitudes de consommation qui déclenchent la visite) remplace « Fréquence de passage garantie » ; « Diagnostic à distance avant déplacement » (pièce embarquée si le défaut est identifié, sinon commande et information) remplace « Pannes résolues pendant le passage ». Appliqué sur les 12 pages qui portent le bloc et dans le guide du blog. **Le client souhaite revoir la liste complète : formulations et valeurs restent à valider** (`TODO:MB` en tête de chaque bloc).
- **Visuels et mise en page alternée** sur les pages secteurs, équipements, grands comptes et zones : photo dans le hero (texte à gauche, image à droite), section problème en deux colonnes avec image alternée, cartes de configuration illustrées. Photos d'ambiance Machine Break existantes, chacune avec un `alt` descriptif ; `TODO:MB` pour des photos réelles par type de site et par zone.
- **Blog** `/blog` (« Conseils », dans la nav et le pied de page) avec deux guides sans chiffre ni promesse, balisés `BlogPosting` : les huit points à vérifier avant de signer, organiser la pause sur un site en 3×8. Format prêt pour d'autres articles : un fichier HTML par article dans `blog/`.
- **Couverture Île-de-France** : la page pilier affirme désormais explicitement la prise en charge des Hauts-de-Seine, Yvelines, Essonne, Val-d'Oise, Seine-Saint-Denis et Paris (communes et pôles nommés), avec les mêmes engagements ; la mention « pages à venir » qui pouvait décourager un prospect de l'ouest a été retirée. La concentration plus forte à l'est est assumée sans être excluante.
- **Formulaire de contact** : cinq champs obligatoires (email, téléphone, entreprise ou entité, code postal du site, effectif) pour identifier l'entité d'un groupe et préparer le rappel ; nom, prénom et message restent en seconde étape facultative. Formulaire dossier de capacité : entreprise obligatoire. Politique de confidentialité alignée.
- **Correctif** : le menu déroulant « Solutions » avait été cassé par la régénération (balise fermante en trop) ; réparé et vérifié sur les 23 pages, générateur corrigé. CTA de la nav raccourci sous 1200 px pour éviter le débordement.

**Sur la longueur des textes (question client)** : ni Google ni les moteurs de réponse par IA ne récompensent le volume. Ce qui compte : des affirmations précises et vérifiables, une structure lisible (titres, FAQ balisées, listes), des entités nommées (communes, types de sites, engagements) et des contenus distincts d'une page à l'autre. Des pages longues et semblables entre elles nuisent plutôt. Les pages ont donc été différenciées par les visuels et la mise en page, pas rallongées.

### Éditeur pour l'équipe communication + réseaux sociaux + Tazza (2026-09-04) ✅ (activation Netlify à faire)

**Décision client** : l'équipe com doit publier seule. Cela impose un éditeur et donc une étape de construction du site, contraire à la contrainte initiale du brief ; la contrainte est levée par le client, et l'étape de build est limitée au strict nécessaire.

- **Eleventy** (`eleventy.config.js`, `package.json`, `netlify.toml` : `npm run build` → `_site/`). Il ne traite que les fichiers `.md` (articles) et `.njk` (index du blog, sitemap) ; **toutes les pages HTML existantes sont copiées telles quelles**, jamais interprétées. Gabarits dans `_includes/` (en-tête et pied de page extraits des pages actuelles).
- **Blog** : un article = un fichier Markdown dans `blog/` (titre, résumé 150-160, date, rubrique, image, description d'image, corps). Adresse `/blog/<slug>`, carte sur `/blog`, entrée dans `sitemap.xml` et JSON-LD `BlogPosting` générés automatiquement. Les deux guides existants ont été convertis.
- **Decap CMS** dans `/admin/` (éditeur open source, interface en français, connexion par email via Netlify Identity, écriture directe dans `main` via Git Gateway). Collections : *Articles du blog* et *Sur les réseaux*. Le résumé est contrôlé (150-160 caractères). Seule page du site à charger un script externe (CDN officiel de Decap et widget Identity) ; réservée à l'équipe, `noindex`. Le formulaire Decap n'a rien à voir avec l'ancien `admin/` supprimé en Phase 1 : celui-ci est configuré, documenté et utilisé.
- **Section « Sur les réseaux »** (accueil et page Conseils) : trois cartes (LinkedIn ou Instagram, visuel, texte, lien vers le post) lues depuis `social.json`, éditable dans `/admin/`, plus les boutons Suivre. Aucun script LinkedIn ni Instagram (pas de flux intégrable côté LinkedIn, cookies côté Instagram) : la section est masquée tant que la liste est vide, donc rien de vide n'est visible. Choix orienté clients B2B : LinkedIn en premier, Instagram pour l'ambiance.
- **Tazza** : carte « Cafés, hôtels, restaurants, boulangeries » sur la page secteurs et note sur la page résidences-hôtels, renvoyant vers tazza.fr (enseigne CHR de Machine Break). Renvoi visible plutôt que redirection automatique, pour ne pas perdre le référencement des pages.
- **`GUIDE-EQUIPE-COM.md`** : mode d'emploi en trois étapes pour l'équipe (publier, corriger, mettre à jour les réseaux) et règles de rédaction (pas de chiffre non validé, vocabulaire « vous suivez vos machines », réassort piloté par la télémétrie).

**À faire une seule fois dans Netlify par le client** (impossible depuis le dépôt) :
1. Site settings → Identity → *Enable Identity* ; Registration → *Invite only* ; Services → *Enable Git Gateway*.
2. Identity → *Invite users* : inviter les emails de l'équipe com. Chaque personne accepte l'invitation (le lien la conduit sur l'accueil puis vers `/admin/`) et choisit un mot de passe.
3. Vérifier après fusion que le déploiement de `main` utilise bien `npm run build` et publie `_site` (lu depuis `netlify.toml`).

### Médiathèque client intégrée (2026-09-04) ✅

Le client a mis à disposition ses deux shootings (agence VZ, 220 photos JPG, 2,3 Go sur le Mac du client, dossier « 10 - Mediatheque/Shootings »). 22 photos ont été choisies, converties en WebP (largeur 1920 px, qualité 80, 2,7 Mo au total dans `assets/img/shooting/`) et placées sur les pages secteurs, équipements et zones avec des descriptions fidèles : atelier industriel et allée d'usine (industrie-logistique), salon de résidence (résidences-hôtels), espace de pause et comptoir de bureau (bureaux-PME), machines, rayons de boissons, snacks et écrans (équipements), salle de pause et hall (zones). Les `TODO:MB` « photo réelle à fournir » des pages secteurs sont levés. Reste possible : renouveler le slider de l'accueil et l'image Open Graph avec cette série.

Toutes les phases du brief sont livrées. Reste : les données client (registre `TODO:MB`, section G.7), la validation sur l'aperçu Netlify, puis la fusion dans `main`.

## F. Registre `TODO:MB`

Voir la section **G.7**, régénérée automatiquement par `tools/audit_site.py` (critère d'acceptation n° 12).

---

## G. Relevé automatique (`tools/audit_site.py`, exécuté sur le site construit `_site/`)

Fichiers HTML : 24 · Fichiers total (hors .git, .netlify, hts-cache, node_modules) : 104

## 1. Inventaire des pages HTML

| Fichier | `<title>` | `meta description` | Dans la nav | Liens entrants | H1 |
|---|---|---|---|---|---|
| `admin/index.html` | Administration du site | Machine Break | *(absente)* | **non** | **aucun** | 0 ⚠ |
| `blog.html` | Conseils distribution automatique et pause en entreprise | Machine Break | Guides Machine Break : choisir un prestataire de distribution automatique, organiser la pause sur un site en 3×8, comprendre le service. Île-de-France. | oui | blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html` | Distributeur automatique en entreprise : les huit points à vérifier avant de signer | Machine Break | Réassort, délai d'intervention, propriété des machines, reporting, hygiène : les huit points à vérifier chez un prestataire de distribution automatique. | **non** | blog.html | 1 |
| `blog/organiser-la-pause-sur-un-site-en-3x8.html` | Postes en 3×8 : organiser la pause sur un site industriel ou logistique | Machine Break | Équipes de nuit, pics d'activité, pas de commerce à proximité : comment dimensionner et organiser la distribution automatique sur un site qui tourne en continu. | **non** | blog.html | 1 |
| `boissons-chaudes-snacks.html` | Distributeurs de boissons chaudes, fraîches et snacks en Île-de-France | Machine Break | Distributeurs de boissons chaudes, froides et snacks pour entreprises en Île-de-France. Machines connectées, réassort et maintenance assurés par Machine Break. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `contact.html` | Diagnostic pause et contact distributeur automatique en Île-de-France | Machine Break | Contactez Machine Break à Bailly-Romainvilliers (77) pour installer un distributeur automatique dans vos locaux en Île-de-France, par téléphone ou par email. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `faq.html` | Questions fréquentes sur les distributeurs automatiques en Île-de-France | Machine Break | Vos questions sur l'installation, le coût, l'entretien et le suivi des distributeurs automatiques Machine Break en Île-de-France. Les réponses de l'équipe. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `fonctionnement.html` | Installation, réassort et entretien de distributeurs en Île-de-France | Machine Break | Le service Machine Break en Île-de-France : installation, approvisionnement, maintenance et suivi télémétrique de vos distributeurs, sans charge de gestion. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `grands-comptes.html` | Distribution automatique multi-sites pour grands comptes en Île-de-France | Machine Break | Grands comptes en Île-de-France : distributeurs déployés sur plusieurs sites, interlocuteur nommé, engagements contractualisés, un reporting consolidé. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `index.html` | Distributeurs automatiques connectés pour entreprises en Île-de-France | Machine Break | Machine Break installe et gère vos distributeurs automatiques connectés (café, boissons, snacks) en Île-de-France : réassort, entretien et suivi inclus. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `mentions-legales.html` | Mentions légales | Machine Break | Mentions légales du site machinebreak.com : éditeur Machine Break à Bailly-Romainvilliers (77), directeur de publication, hébergeur et propriété intellectuelle. | **non** | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `merci-dossier.html` | Merci, votre demande de dossier est bien reçue | Machine Break | Votre demande de dossier de capacité Machine Break a bien été transmise. Notre équipe vous l'adresse par email et reste disponible pour un rendez-vous. | **non** | **aucun** | 1 |
| `merci.html` | Merci, votre demande est bien reçue | Machine Break | Votre demande de diagnostic pause a bien été transmise à l'équipe Machine Break (Île-de-France). Nous vous rappelons pour cadrer votre besoin. | **non** | **aucun** | 1 |
| `politique-de-confidentialite.html` | Politique de confidentialité | Machine Break | Politique de confidentialité de Machine Break : données collectées via le formulaire de contact, finalités, durée de conservation, droits RGPD et contact. | **non** | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `solution-par-secteur.html` | Distributeurs automatiques par secteur d'activité en Île-de-France | Machine Break | Distributeurs automatiques adaptés à votre secteur en Île-de-France : bureaux et PME, résidences et hôtels, sites industriels et logistiques. Sur mesure. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `solutions/bureaux-pme.html` | Machine à café et distributeur automatique pour bureaux et PME en Île-de-France | Machine Break | Machine à café et distributeur de snacks pour bureaux et PME en Île-de-France : produits de qualité, zéro gestion pour l'office manager, suivi en temps réel. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `solutions/equipements.html` | Distributeurs automatiques et machines à café professionnelles en Île-de-France | Machine Break | Machines à café en grains, distributeurs de boissons fraîches, snacks et combinés installés par Machine Break en Île-de-France : connectés et entretenus. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `solutions/industrie-logistique.html` | Distributeur automatique pour sites industriels et logistiques en Île-de-France | Machine Break | Distributeurs automatiques pour usines et entrepôts en Île-de-France : grande capacité, équipes en 3×8, réassort calé sur les rotations, machines robustes. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `solutions/residences-hotels.html` | Distributeur automatique pour résidences et hôtels en Île-de-France | Machine Break | Distributeur automatique pour hôtels et résidences en Île-de-France : service en libre accès à toute heure, paiement sans contact, intégration discrète. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `terms-of-service.html` | Conditions générales d'utilisation du site | Machine Break | Conditions générales d'utilisation du site machinebreak.com, opérateur de distribution automatique en Île-de-France, basé à Bailly-Romainvilliers (77). | **non** | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `zones/est-parisien.html` | Distributeur automatique dans l'Est parisien : Val de Fontenay, Montreuil, Créteil | Machine Break | Distributeurs automatiques et machines à café dans l'Est parisien : Val de Fontenay, Montreuil, Noisy-le-Grand, Créteil, Paris Est. Service Machine Break. | **non** | zones/ile-de-france.html | 1 |
| `zones/ile-de-france.html` | Distributeur automatique en Île-de-France : installation et service régional | Machine Break | Machine Break installe et entretient des distributeurs automatiques dans toute l'Île-de-France depuis la Seine-et-Marne : huit départements, un seul numéro. | oui | blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/marne-la-vallee.html, zones/seine-et-marne.html | 1 |
| `zones/marne-la-vallee.html` | Distributeur automatique à Marne-la-Vallée : Val d'Europe, Bussy, Torcy, Noisy | Machine Break | Distributeurs automatiques et machines à café à Marne-la-Vallée : Val d'Europe, Val de Bussy, Val Maubuée, Noisy-le-Grand. Machine Break est installé sur place. | **non** | zones/ile-de-france.html | 1 |
| `zones/seine-et-marne.html` | Distributeur automatique en Seine-et-Marne (77) : installation et entretien | Machine Break | Distributeurs automatiques et machines à café en Seine-et-Marne : Machine Break, basé à Bailly-Romainvilliers, intervient de Meaux à Melun et à Sénart. | **non** | zones/ile-de-france.html | 1 |

## 2. Pages orphelines (hors navigation principale)

- `admin/index.html` — **aucun lien entrant**
- `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html` — atteignable via : blog.html
- `blog/organiser-la-pause-sur-un-site-en-3x8.html` — atteignable via : blog.html
- `mentions-legales.html` — atteignable via : blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html
- `merci-dossier.html` — **aucun lien entrant**
- `merci.html` — **aucun lien entrant**
- `politique-de-confidentialite.html` — atteignable via : blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, terms-of-service.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html
- `terms-of-service.html` — atteignable via : blog.html, blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html, blog/organiser-la-pause-sur-un-site-en-3x8.html, boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, grands-comptes.html, index.html, mentions-legales.html, merci-dossier.html, merci.html, politique-de-confidentialite.html, solution-par-secteur.html, solutions/bureaux-pme.html, solutions/equipements.html, solutions/industrie-logistique.html, solutions/residences-hotels.html, zones/est-parisien.html, zones/ile-de-france.html, zones/marne-la-vallee.html, zones/seine-et-marne.html
- `zones/est-parisien.html` — atteignable via : zones/ile-de-france.html
- `zones/marne-la-vallee.html` — atteignable via : zones/ile-de-france.html
- `zones/seine-et-marne.html` — atteignable via : zones/ile-de-france.html

## 3. Coordonnées (téléphones, adresses, emails)

### Téléphones

| Valeur | Pages (occurrences) |
|---|---|
| `01 74 81 09 52` | `blog.html` (6), `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html` (6), `blog/organiser-la-pause-sur-un-site-en-3x8.html` (6), `boissons-chaudes-snacks.html` (6), `contact.html` (8), `faq.html` (6), `fonctionnement.html` (6), `grands-comptes.html` (8), `index.html` (7), `mentions-legales.html` (10), `merci-dossier.html` (8), `merci.html` (8), `politique-de-confidentialite.html` (8), `solution-par-secteur.html` (6), `solutions/bureaux-pme.html` (6), `solutions/equipements.html` (6), `solutions/industrie-logistique.html` (6), `solutions/residences-hotels.html` (6), `terms-of-service.html` (8), `zones/est-parisien.html` (6), `zones/ile-de-france.html` (8), `zones/marne-la-vallee.html` (6), `zones/seine-et-marne.html` (6) |

### Adresses postales (voie)

| Valeur | Pages (occurrences) |
|---|---|
| `28 Avenue Christian Doppler` | `blog.html` (1), `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html` (1), `blog/organiser-la-pause-sur-un-site-en-3x8.html` (1), `boissons-chaudes-snacks.html` (1), `contact.html` (1), `faq.html` (1), `fonctionnement.html` (1), `grands-comptes.html` (1), `index.html` (1), `mentions-legales.html` (2), `merci-dossier.html` (1), `merci.html` (1), `politique-de-confidentialite.html` (2), `solution-par-secteur.html` (1), `solutions/bureaux-pme.html` (1), `solutions/equipements.html` (1), `solutions/industrie-logistique.html` (1), `solutions/residences-hotels.html` (1), `terms-of-service.html` (1), `zones/est-parisien.html` (1), `zones/ile-de-france.html` (1), `zones/marne-la-vallee.html` (1), `zones/seine-et-marne.html` (2) |

### Codes postaux + ville

| Valeur | Pages (occurrences) |
|---|---|
| `77700 Bailly-Romainvilliers` | `blog.html` (1), `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html` (1), `blog/organiser-la-pause-sur-un-site-en-3x8.html` (1), `boissons-chaudes-snacks.html` (1), `contact.html` (1), `faq.html` (1), `fonctionnement.html` (1), `grands-comptes.html` (1), `index.html` (1), `mentions-legales.html` (2), `merci-dossier.html` (1), `merci.html` (1), `politique-de-confidentialite.html` (2), `solution-par-secteur.html` (1), `solutions/bureaux-pme.html` (1), `solutions/equipements.html` (1), `solutions/industrie-logistique.html` (1), `solutions/residences-hotels.html` (1), `terms-of-service.html` (1), `zones/est-parisien.html` (1), `zones/ile-de-france.html` (1), `zones/marne-la-vallee.html` (1), `zones/seine-et-marne.html` (2) |

### Emails

| Valeur | Pages (occurrences) |
|---|---|
| `contact@machinebreak.com` | `blog.html` (2), `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html` (2), `blog/organiser-la-pause-sur-un-site-en-3x8.html` (2), `boissons-chaudes-snacks.html` (2), `contact.html` (4), `faq.html` (2), `fonctionnement.html` (2), `grands-comptes.html` (2), `index.html` (3), `mentions-legales.html` (6), `merci-dossier.html` (2), `merci.html` (2), `politique-de-confidentialite.html` (6), `solution-par-secteur.html` (2), `solutions/bureaux-pme.html` (2), `solutions/equipements.html` (2), `solutions/industrie-logistique.html` (2), `solutions/residences-hotels.html` (2), `terms-of-service.html` (4), `zones/est-parisien.html` (2), `zones/ile-de-france.html` (2), `zones/marne-la-vallee.html` (2), `zones/seine-et-marne.html` (2) |
| `prenom@entreprise.fr` | `contact.html` (1), `grands-comptes.html` (1) |

## 4. `meta description` dupliquées

Aucune duplication.

Sans meta description : `admin/index.html`

### `<title>` dupliqués

Aucun.

### Open Graph / Twitter / canonical

| Fichier | canonical | og:url | og:image | twitter:image |
|---|---|---|---|---|
| `admin/index.html` | — | — | — | — |
| `blog.html` | https://machinebreak.com/blog | https://machinebreak.com/blog | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html` | https://machinebreak.com/blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer | https://machinebreak.com/blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer | https://machinebreak.com/assets/img/covers/machine_cafe.webp | https://machinebreak.com/assets/img/covers/machine_cafe.webp |
| `blog/organiser-la-pause-sur-un-site-en-3x8.html` | https://machinebreak.com/blog/organiser-la-pause-sur-un-site-en-3x8 | https://machinebreak.com/blog/organiser-la-pause-sur-un-site-en-3x8 | https://machinebreak.com/assets/img/secteurs/public.webp | https://machinebreak.com/assets/img/secteurs/public.webp |
| `boissons-chaudes-snacks.html` | https://machinebreak.com/boissons-chaudes-snacks | https://machinebreak.com/boissons-chaudes-snacks | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `contact.html` | https://machinebreak.com/contact | https://machinebreak.com/contact | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `faq.html` | https://machinebreak.com/faq | https://machinebreak.com/faq | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `fonctionnement.html` | https://machinebreak.com/fonctionnement | https://machinebreak.com/fonctionnement | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `grands-comptes.html` | https://machinebreak.com/grands-comptes | https://machinebreak.com/grands-comptes | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `index.html` | https://machinebreak.com/ | https://machinebreak.com/ | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `mentions-legales.html` | https://machinebreak.com/mentions-legales | https://machinebreak.com/mentions-legales | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `merci-dossier.html` | https://machinebreak.com/merci-dossier | https://machinebreak.com/merci-dossier | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `merci.html` | https://machinebreak.com/merci | https://machinebreak.com/merci | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `politique-de-confidentialite.html` | https://machinebreak.com/politique-de-confidentialite | https://machinebreak.com/politique-de-confidentialite | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `solution-par-secteur.html` | https://machinebreak.com/solution-par-secteur | https://machinebreak.com/solution-par-secteur | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `solutions/bureaux-pme.html` | https://machinebreak.com/solutions/bureaux-pme | https://machinebreak.com/solutions/bureaux-pme | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `solutions/equipements.html` | https://machinebreak.com/solutions/equipements | https://machinebreak.com/solutions/equipements | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `solutions/industrie-logistique.html` | https://machinebreak.com/solutions/industrie-logistique | https://machinebreak.com/solutions/industrie-logistique | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `solutions/residences-hotels.html` | https://machinebreak.com/solutions/residences-hotels | https://machinebreak.com/solutions/residences-hotels | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `terms-of-service.html` | https://machinebreak.com/terms-of-service | https://machinebreak.com/terms-of-service | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `zones/est-parisien.html` | https://machinebreak.com/zones/est-parisien | https://machinebreak.com/zones/est-parisien | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `zones/ile-de-france.html` | https://machinebreak.com/zones/ile-de-france | https://machinebreak.com/zones/ile-de-france | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `zones/marne-la-vallee.html` | https://machinebreak.com/zones/marne-la-vallee | https://machinebreak.com/zones/marne-la-vallee | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `zones/seine-et-marne.html` | https://machinebreak.com/zones/seine-et-marne | https://machinebreak.com/zones/seine-et-marne | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |

## 5. Images

### Images sans attribut `alt`

Aucune.

Images avec `alt=""` (vide, décoratif) : 0

### Images pointant vers un domaine externe

Aucune balise `<img>` externe.

### Images référencées mais absentes du dépôt

Aucune.

## 6. Fichiers techniques

- `sitemap.xml` : présent
- `robots.txt` : présent
- `_redirects` : présent
- `_headers` : **absent**
- `netlify.toml` : **absent**
- `.htaccess` : **absent**
- `404.html` : **absent**
- JSON-LD : `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html` (1), `blog/organiser-la-pause-sur-un-site-en-3x8.html` (1), `faq.html` (1), `index.html` (1), `solutions/bureaux-pme.html` (1), `solutions/industrie-logistique.html` (1), `solutions/residences-hotels.html` (1)

## 7. Registre `TODO:MB` (valeurs à fournir par le client)

| Valeur attendue | Emplacements |
|---|---|
| valeur à fournir : horaires d'ouverture à afficher à côté du numéro (ex. « du lundi au vendredi, 8h–18h »). | `blog.html`:32, `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html`:32, `blog/organiser-la-pause-sur-un-site-en-3x8.html`:32, `boissons-chaudes-snacks.html`:53, `contact.html`:69, `faq.html`:111, `fonctionnement.html`:38, `grands-comptes.html`:37, `index.html`:122, `mentions-legales.html`:38, `merci-dossier.html`:38, `merci.html`:39, `politique-de-confidentialite.html`:38, `solution-par-secteur.html`:37, `solutions/bureaux-pme.html`:78, `solutions/equipements.html`:37, `solutions/industrie-logistique.html`:86, `solutions/residences-hotels.html`:78, `terms-of-service.html`:49, `zones/est-parisien.html`:37, `zones/ile-de-france.html`:37, `zones/marne-la-vallee.html`:37, `zones/seine-et-marne.html`:37 |
| valeur à fournir : URL de l'espace client (plateforme de suivi). | `blog.html`:37, `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html`:37, `blog/organiser-la-pause-sur-un-site-en-3x8.html`:37, `boissons-chaudes-snacks.html`:58, `contact.html`:74, `faq.html`:116, `fonctionnement.html`:43, `grands-comptes.html`:42, `index.html`:127, `mentions-legales.html`:43, `merci-dossier.html`:43, `merci.html`:44, `politique-de-confidentialite.html`:43, `solution-par-secteur.html`:42, `solutions/bureaux-pme.html`:83, `solutions/equipements.html`:42, `solutions/industrie-logistique.html`:91, `solutions/residences-hotels.html`:83, `terms-of-service.html`:54, `zones/est-parisien.html`:42, `zones/ile-de-france.html`:42, `zones/marne-la-vallee.html`:42, `zones/seine-et-marne.html`:42 |
| URL du formulaire de diagnostic (Typeform ou Tally) à fournir : remplacer /contact#contact-form dans tous les liens .cta-diagnostic | `blog.html`:43, `blog/distributeur-automatique-entreprise-ce-qu-il-faut-verifier-avant-de-signer.html`:43, `blog/organiser-la-pause-sur-un-site-en-3x8.html`:43, `boissons-chaudes-snacks.html`:64, `contact.html`:80, `faq.html`:122, `fonctionnement.html`:49, `grands-comptes.html`:48, `index.html`:133, `mentions-legales.html`:49, `merci-dossier.html`:49, `merci.html`:50, `politique-de-confidentialite.html`:49, `solution-par-secteur.html`:48, `solutions/bureaux-pme.html`:89, `solutions/equipements.html`:48, `solutions/industrie-logistique.html`:97, `solutions/residences-hotels.html`:89, `terms-of-service.html`:60, `zones/est-parisien.html`:48, `zones/ile-de-france.html`:48, `zones/marne-la-vallee.html`:48, `zones/seine-et-marne.html`:48 |
| valeur à fournir : délai de réponse annoncé (ex. « sous 24 h ouvrées »). | `contact.html`:359 |
| photo réelle de ce type de site / de cette zone à fournir (les visuels actuels sont des photos d'ambiance Machine Break) | `grands-comptes.html`:129, `solutions/bureaux-pme.html`:170, `solutions/equipements.html`:129, `solutions/industrie-logistique.html`:178, `solutions/residences-hotels.html`:170, `zones/est-parisien.html`:129, `zones/ile-de-france.html`:129, `zones/marne-la-vallee.html`:129, `zones/seine-et-marne.html`:129 |
| valeur à fournir : chiffres de capacité à afficher ici une fois validés — nombre de sites équipés, nombre de machines en parc, délai moyen d | `grands-comptes.html`:170 |
| valeur à fournir : délai d'intervention garanti. | `grands-comptes.html`:207, `solutions/bureaux-pme.html`:272, `solutions/industrie-logistique.html`:278, `solutions/residences-hotels.html`:270 |
| valeur à fournir : taux de remplissage constaté à chaque passage (en %). | `grands-comptes.html`:222, `index.html`:624, `solution-par-secteur.html`:282, `solutions/bureaux-pme.html`:287, `solutions/industrie-logistique.html`:293, `solutions/residences-hotels.html`:285 |
| valeur à fournir : dossier de capacité au format PDF. Tant qu'il n'est pas déposé dans /assets/docs/, l'envoi est assuré manuellement par l' | `grands-comptes.html`:245 |
| Google Search Console : balise de vérification à fournir. | `index.html`:21 |
| horaires d'ouverture à fournir pour ajouter "openingHoursSpecification" ; forme juridique / SIREN pour "legalName" et "taxID" | `index.html`:42 |
| valeur à fournir : captures d'écran anonymisées de la plateforme client. | `index.html`:569 |
| liste à revoir avec le client (2026-09-04), formulations et valeurs à valider | `index.html`:589, `solution-par-secteur.html`:247 |
| valeur à fournir : délai d'intervention garanti (base ancienne page : technicien envoyé dans la demi-journée — à confirmer). | `index.html`:616, `solution-par-secteur.html`:274 |
| valeur à fournir : bloc statistiques retiré (satisfaction, support 24/7 non sourcés) ; à réintroduire uniquement avec des valeurs validées p | `index.html`:680 |
| valeur à fournir : Forme juridique : … | `mentions-legales.html`:134 |
| valeur à fournir : Capital social : … | `mentions-legales.html`:135 |
| valeur à fournir : SIREN / SIRET : … | `mentions-legales.html`:137 |
| valeur à fournir : RCS : … | `mentions-legales.html`:138 |
| valeur à fournir : Numéro de TVA intracommunautaire : … | `mentions-legales.html`:139 |
| valeur à fournir : Directeur de la publication | `mentions-legales.html`:144 |
| hébergeur à confirmer par le client (§8 du brief) | `mentions-legales.html`:154 |
| valeur à fournir : date de mise à jour | `mentions-legales.html`:173, `politique-de-confidentialite.html`:182 |
| valeur à fournir : une fois le PDF déposé, remplacer ce paragraphe par un bouton de téléchargement direct : <a class="btn btn-primary lift"  | `merci-dossier.html`:128 |
| valeur à fournir : délai de réponse annoncé (ex. « sous 24 h ouvrées ») | `merci.html`:129 |
| valeur à fournir : durée de conservation (recommandation CNIL prospects : 3 ans après le dernier contact) | `politique-de-confidentialite.html`:162 |
| valeur à fournir : référence client bureaux / PME (nommée ou anonymisée) validée par le client. | `solutions/bureaux-pme.html`:301 |
| valeur à fournir : seuil d'effectif à partir duquel l'installation est offerte, par zone | `solutions/bureaux-pme.html`:338 |
| valeur à fournir : parc actuel (marques, modèles, capacités, photos). L'ancien catalogue Necta (Krea Touch, Melodia, Kalea, Tango, Orchestra | `solutions/equipements.html`:214 |
| valeur à fournir : référence client industrie / logistique (nommée ou anonymisée) validée par le client. | `solutions/industrie-logistique.html`:307 |
| valeur à fournir : référence client résidence / hôtel (nommée ou anonymisée) validée par le client. | `solutions/residences-hotels.html`:299 |
| le corps de cette page est un texte de gabarit (Landkit) non adapté : CGU réelles à fournir ou page à rediriger vers /mentions-legales | `terms-of-service.html`:142 |
| valeur à fournir : délai d'intervention réel constaté sur cette zone (moyenne 12 mois) et délai garanti au contrat. | `zones/est-parisien.html`:173, `zones/marne-la-vallee.html`:173, `zones/seine-et-marne.html`:173 |
| valeur à fournir : références clients sur cette zone (nommées ou anonymisées), validées par le client. | `zones/est-parisien.html`:202, `zones/marne-la-vallee.html`:202, `zones/seine-et-marne.html`:202 |

34 valeurs distinctes attendues, 123 emplacements au total. Tous sont masqués dans un commentaire HTML : rien de vide n'est visible en production.

### Autres fichiers à la racine

- `_redirects`
- `admin/config.yml`
- `robots.txt`
- `sitemap.xml`
- `social.json`

