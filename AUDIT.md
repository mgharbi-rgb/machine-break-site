# AUDIT.md — machinebreak.com

**Phase 0 du brief « génération de leads B2B »** · Audit réalisé le 2026-09-03 sur le dépôt `mgharbi-rgb/machine-break-site` (branche `main`, dernier commit `e83d8c0` du 2025-10-09), croisé avec la version en ligne servie par Netlify derrière Cloudflare.

Régénérer la partie automatique : `python3 tools/audit_site.py . > /tmp/auto.md` puis remplacer la section « Relevé automatique » ci-dessous.

---

## A. Synthèse — ce qu'il faut retenir

1. **Deux générations du site coexistent**, confirmé. L'ancienne génération représente **5 fichiers**, pas 2 : les deux orphelines connues, mais aussi `careers.html`, `career-single.html` et `terms-of-service.html`, qui portent encore l'adresse de La Garenne-Colombes, le 01 70 82 31 32 et le logo `.jpg`. `terms-of-service.html` contient en plus un **troisième numéro** (01 85 65 81 51).
2. **Trois pages supplémentaires hors brief** ont été découvertes : `avantages.html` (brouillon inachevé, sans H1 ni meta, lien cassé vers `pourquoi-nous.html`, encore lié depuis la nav de 4 pages), `career-single.html` (gabarit Landkit brut : « UX Design Lead », `hello@domain.com`) et `admin/` (interface Netlify CMS chargée depuis unpkg.com, publiquement accessible en ligne, backend git-gateway pointant sur `main`).
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
| `terms-of-service.html` | **ancienne** (3 numéros différents dans la page) | réécrire coordonnées ; devient la base des CGU, à côté de `/mentions-legales` |
| `location-distributeurs-automatiques-boissons.html` | **ancienne**, orpheline | 301 → `/fonctionnement` (contenu extrait dans `CONTENU-RECUPERE.md`) |
| `entreprise-location-distributeur-automatique-boisson.html` | **ancienne**, orpheline | 301 → `/boissons-chaudes-snacks` |
| `avantages.html` | brouillon (hors brief) | supprimer + 301 → `/fonctionnement`, retirer le lien de nav sur 4 pages |
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

## F. Registre `TODO:MB`

Aucun marqueur `TODO:MB` dans le dépôt à ce stade. Cette section sera mise à jour à chaque phase et listera tous les emplacements en attente de valeur client (critère d'acceptation n° 12).

---

## G. Relevé automatique (`tools/audit_site.py`)

Fichiers HTML : 13 · Fichiers total (hors .git, .netlify, hts-cache, node_modules) : 121

## 1. Inventaire des pages HTML

| Fichier | `<title>` | `meta description` | Dans la nav | Liens entrants | H1 |
|---|---|---|---|---|---|
| `admin/index.html` | Admin | *(absente)* | **non** | **aucun** | 0 ⚠ |
| `avantages.html` | Pourquoi nous ? – Machine Break | *(absente)* | **non** | **aucun** | 0 ⚠ |
| `boissons-chaudes-snacks.html` | Distributeurs automatiques modernes et intelligents | Machine Break | Découvrez les distributeurs Machine Break : boissons chaudes, snacks et suivi intelligent par télémétrie. Sans coût ni contrainte pour votre entreprise. | oui | avantages.html, career-single.html, careers.html, contact.html, entreprise-location-distributeur-automatique-boisson.html, faq.html, fonctionnement.html, index.html, location-distributeurs-automatiques-boissons.html, solution-par-secteur.html, terms-of-service.html | 2 ⚠ |
| `career-single.html` | Landkit | @@pageDescription | **non** | careers.html | 1 |
| `careers.html` | Landkit | @@pageDescription | **non** | boissons-chaudes-snacks.html, career-single.html, contact.html, entreprise-location-distributeur-automatique-boisson.html, faq.html, fonctionnement.html, index.html, location-distributeurs-automatiques-boissons.html, solution-par-secteur.html, terms-of-service.html | 1 |
| `contact.html` | Contactez Machine Break | Installation de distributeurs automatiques | Besoins d'informations sur nos offres commerciales ? Faites appel à notre entreprise Machine Break pour des solutions sur mesures. | oui | avantages.html, boissons-chaudes-snacks.html, career-single.html, careers.html, entreprise-location-distributeur-automatique-boisson.html, faq.html, fonctionnement.html, index.html, location-distributeurs-automatiques-boissons.html, solution-par-secteur.html, terms-of-service.html | 1 |
| `entreprise-location-distributeur-automatique-boisson.html` | Entreprise location distributeurs boissons automatiques Paris | Besoin de solutions pour proposer à vos clients, collaborateurs un distributeur de boissons : cafés, thés, snacks. Faites appel à Machine Break. | oui | career-single.html, careers.html, contact.html, location-distributeurs-automatiques-boissons.html, terms-of-service.html | 0 ⚠ |
| `faq.html` | FAQ - Vos questions sur nos distributeurs automatiques | Machine Break | Trouvez les réponses à vos questions sur l'installation, la maintenance et l’utilisation de nos distributeurs automatiques. | oui | avantages.html, boissons-chaudes-snacks.html, contact.html, fonctionnement.html, index.html, solution-par-secteur.html | 1 |
| `fonctionnement.html` | Fonctionnement de nos distributeurs automatiques | Machine Break | Machine Break prend en charge l'installation, l’approvisionnement et la maintenance de vos distributeurs automatiques connectés. | oui | avantages.html, boissons-chaudes-snacks.html, contact.html, faq.html, index.html, solution-par-secteur.html | 1 |
| `index.html` | Distributeurs automatiques connectés pour entreprises | Machine Break | Machine Break propose des distributeurs automatiques connectés avec un suivi intelligent et sans contrainte pour les entreprises. | oui | avantages.html, boissons-chaudes-snacks.html, career-single.html, careers.html, contact.html, entreprise-location-distributeur-automatique-boisson.html, faq.html, fonctionnement.html, location-distributeurs-automatiques-boissons.html, solution-par-secteur.html, terms-of-service.html | 3 ⚠ |
| `location-distributeurs-automatiques-boissons.html` | Location distributeurs boissons chaudes Paris | Besoin d'une machine à café pour vos clients ? Faites appel à Machine Break pour des solutions sur mesures à Paris en distribution automatique de boissons. | oui | career-single.html, careers.html, entreprise-location-distributeur-automatique-boisson.html, terms-of-service.html | 1 |
| `solution-par-secteur.html` | Solutions distributeurs automatiques par secteur | Machine Break | Une solution de distributeur pour chaque secteur : écoles, bureaux, hôpitaux ou espaces publics. Installez un service café moderne avec Machine Break. | oui | boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html | 1 |
| `terms-of-service.html` | MACHINE BREAK - Café - Boissons - Friandises | @@pageDescription | **non** | boissons-chaudes-snacks.html, career-single.html, careers.html, contact.html, entreprise-location-distributeur-automatique-boisson.html, faq.html, fonctionnement.html, index.html, location-distributeurs-automatiques-boissons.html, solution-par-secteur.html | 1 |

## 2. Pages orphelines (hors navigation principale)

- `admin/index.html` — **aucun lien entrant**
- `avantages.html` — **aucun lien entrant**
- `career-single.html` — atteignable via : careers.html
- `careers.html` — atteignable via : boissons-chaudes-snacks.html, career-single.html, contact.html, entreprise-location-distributeur-automatique-boisson.html, faq.html, fonctionnement.html, index.html, location-distributeurs-automatiques-boissons.html, solution-par-secteur.html, terms-of-service.html
- `terms-of-service.html` — atteignable via : boissons-chaudes-snacks.html, career-single.html, careers.html, contact.html, entreprise-location-distributeur-automatique-boisson.html, faq.html, fonctionnement.html, index.html, location-distributeurs-automatiques-boissons.html, solution-par-secteur.html

### Liens internes cassés

- `avantages.html` → `pourquoi-nous.html`

## 3. Coordonnées (téléphones, adresses, emails)

### Téléphones

> ⚠ **Divergence : 5 valeurs distinctes.**

| Valeur | Pages (occurrences) |
|---|---|
| `0174810952` | `boissons-chaudes-snacks.html` (1), `contact.html` (2), `faq.html` (1), `fonctionnement.html` (1), `index.html` (1), `solution-par-secteur.html` (1) |
| `01 74 81 09 52` | `boissons-chaudes-snacks.html` (1), `contact.html` (2), `faq.html` (1), `fonctionnement.html` (1), `index.html` (1), `solution-par-secteur.html` (1) |
| `0170823132` | `career-single.html` (1), `careers.html` (1), `entreprise-location-distributeur-automatique-boisson.html` (1), `location-distributeurs-automatiques-boissons.html` (1), `terms-of-service.html` (1) |
| `01 70 82 31 32` | `career-single.html` (1), `careers.html` (1), `entreprise-location-distributeur-automatique-boisson.html` (1), `location-distributeurs-automatiques-boissons.html` (1), `terms-of-service.html` (1) |
| `01 85 65 81 51` | `terms-of-service.html` (2) |

### Adresses postales (voie)

> ⚠ **Divergence : 2 valeurs distinctes.**

| Valeur | Pages (occurrences) |
|---|---|
| `28 Avenue Christian Doppler` | `boissons-chaudes-snacks.html` (1), `contact.html` (1), `faq.html` (1), `fonctionnement.html` (1), `index.html` (1), `solution-par-secteur.html` (1) |
| `71 Boulevard National` | `career-single.html` (1), `careers.html` (1), `entreprise-location-distributeur-automatique-boisson.html` (1), `location-distributeurs-automatiques-boissons.html` (1), `terms-of-service.html` (1) |

### Codes postaux + ville

> ⚠ **Divergence : 2 valeurs distinctes.**

| Valeur | Pages (occurrences) |
|---|---|
| `77700 Bailly Romainvilliers` | `boissons-chaudes-snacks.html` (1), `contact.html` (1), `faq.html` (1), `fonctionnement.html` (1), `index.html` (1), `solution-par-secteur.html` (1) |
| `92250 La Garenne Colombes` | `career-single.html` (1), `careers.html` (1), `entreprise-location-distributeur-automatique-boisson.html` (1), `location-distributeurs-automatiques-boissons.html` (1), `terms-of-service.html` (1) |

### Emails

| Valeur | Pages (occurrences) |
|---|---|
| `contact@machinebreak.com` | `boissons-chaudes-snacks.html` (2), `career-single.html` (2), `careers.html` (2), `contact.html` (4), `entreprise-location-distributeur-automatique-boisson.html` (2), `faq.html` (2), `fonctionnement.html` (2), `index.html` (2), `location-distributeurs-automatiques-boissons.html` (2), `solution-par-secteur.html` (2), `terms-of-service.html` (4) |
| `hello@domain.com` | `career-single.html` (1) |

## 4. `meta description` dupliquées

- « @@pageDescription » (17 car.) — `career-single.html`, `careers.html`, `terms-of-service.html`

Sans meta description : `admin/index.html`, `avantages.html`

### `<title>` dupliqués

- « Landkit » — `career-single.html`, `careers.html`

### Open Graph / Twitter / canonical

| Fichier | canonical | og:url | og:image | twitter:image |
|---|---|---|---|---|
| `admin/index.html` | — | — | — | — |
| `avantages.html` | — | — | — | — |
| `boissons-chaudes-snacks.html` | — | index.html | https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg | — |
| `career-single.html` | — | index.html | https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg | — |
| `careers.html` | — | index.html | https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg | — |
| `contact.html` | — | index.html | https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg | — |
| `entreprise-location-distributeur-automatique-boisson.html` | — | index.html | https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg | — |
| `faq.html` | — | — | — | — |
| `fonctionnement.html` | — | — | — | — |
| `index.html` | — | index.html | https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg | — |
| `location-distributeurs-automatiques-boissons.html` | — | index.html | https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg | — |
| `solution-par-secteur.html` | — | — | — | — |
| `terms-of-service.html` | — | index.html | https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg | — |

## 5. Images

### Images sans attribut `alt`

Aucune.

Images avec `alt=""` (vide, décoratif) : 0

### Images pointant vers un domaine externe

Aucune balise `<img>` externe.

Meta images externes (og/twitter) :
- `boissons-chaudes-snacks.html` `og:image` → `https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg`
- `career-single.html` `og:image` → `https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg`
- `careers.html` `og:image` → `https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg`
- `contact.html` `og:image` → `https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg`
- `entreprise-location-distributeur-automatique-boisson.html` `og:image` → `https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg`
- `index.html` `og:image` → `https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg`
- `location-distributeurs-automatiques-boissons.html` `og:image` → `https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg`
- `terms-of-service.html` `og:image` → `https://socialbrew.dk/wp-content/uploads/2020/06/171026-better-coffee-boost-se-329p_67dfb6820f7d3898b5486975903c2e51.fit-760w-1.jpg`

### Images référencées mais absentes du dépôt

Aucune.

## 6. Fichiers techniques

- `sitemap.xml` : présent
- `robots.txt` : présent
- `_redirects` : **absent**
- `_headers` : **absent**
- `netlify.toml` : **absent**
- `.htaccess` : **absent**
- `404.html` : **absent**
- JSON-LD : `index.html` (1)

### Autres fichiers à la racine

- `README.md`
- `admin/config.yml`
- `backblue.gif`
- `fade.gif`
- `robots.txt`
- `sitemap.xml`
- `tools/audit_site.py`
