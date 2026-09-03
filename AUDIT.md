# AUDIT.md — machinebreak.com

**Phase 0 du brief « génération de leads B2B »** · Audit réalisé le 2026-09-03 sur le dépôt `mgharbi-rgb/machine-break-site` (branche `main`, dernier commit `e83d8c0` du 2025-10-09), croisé avec la version en ligne servie par Netlify derrière Cloudflare.

Régénérer la partie automatique : `python3 tools/audit_site.py . > /tmp/auto.md` puis remplacer la section « Relevé automatique » ci-dessous.

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

Reste hors périmètre Phase 1 : titres au format `[Besoin] + [Zone]`, canonical, redirections `*.html → /page`, JSON-LD LocalBusiness (Phase 4) ; CTA, en-tête téléphone, formulaire réduit, `/merci` (Phase 2).

## F. Registre `TODO:MB`

| Fichier | Ligne | Valeur attendue |
|---|---|---|
| `index.html` | 520 | valeur à fournir : bloc statistiques retiré (satisfaction, support 24/7 non sourcés) ; à réintroduire uniquement avec des valeurs validées par le client |
| `mentions-legales.html` | 76 | valeur à fournir : Forme juridique : … |
| `mentions-legales.html` | 77 | valeur à fournir : Capital social : … |
| `mentions-legales.html` | 79 | valeur à fournir : SIREN / SIRET : … |
| `mentions-legales.html` | 80 | valeur à fournir : RCS : … |
| `mentions-legales.html` | 81 | valeur à fournir : Numéro de TVA intracommunautaire : … |
| `mentions-legales.html` | 86 | valeur à fournir : Directeur de la publication |
| `mentions-legales.html` | 96 | hébergeur à confirmer par le client (§8 du brief) |
| `mentions-legales.html` | 115 | valeur à fournir : date de mise à jour |
| `politique-de-confidentialite.html` | 104 | valeur à fournir : durée de conservation (recommandation CNIL prospects : 3 ans après le dernier contact) |
| `politique-de-confidentialite.html` | 124 | valeur à fournir : date de mise à jour |
| `terms-of-service.html` | 125 | le corps de cette page est un texte de gabarit (Landkit) non adapté : CGU réelles à fournir ou page à rediriger vers /mentions-legales |

12 emplacements en attente (mis à jour 2026-09-03, fin de Phase 1). Les emplacements sont **masqués en commentaire HTML** : rien de vide n'est visible en production.

---

## G. Relevé automatique (`tools/audit_site.py`)

Fichiers HTML : 9 · Fichiers total (hors .git, .netlify, hts-cache, node_modules) : 116

## 1. Inventaire des pages HTML

| Fichier | `<title>` | `meta description` | Dans la nav | Liens entrants | H1 |
|---|---|---|---|---|---|
| `boissons-chaudes-snacks.html` | Distributeurs automatiques modernes et intelligents | Machine Break | Distributeurs de boissons chaudes, froides et snacks pour entreprises en Île-de-France. Machines connectées, réassort et maintenance assurés par Machine Break. | oui | contact.html, faq.html, fonctionnement.html, index.html, mentions-legales.html, politique-de-confidentialite.html, solution-par-secteur.html, terms-of-service.html | 2 ⚠ |
| `contact.html` | Contactez Machine Break | Installation de distributeurs automatiques | Contactez Machine Break à Bailly-Romainvilliers (77) pour installer un distributeur automatique dans vos locaux en Île-de-France, par téléphone ou par email. | oui | boissons-chaudes-snacks.html, faq.html, fonctionnement.html, index.html, mentions-legales.html, politique-de-confidentialite.html, solution-par-secteur.html, terms-of-service.html | 1 |
| `faq.html` | FAQ - Vos questions sur nos distributeurs automatiques | Machine Break | Vos questions sur l'installation, le coût, l'entretien et le suivi des distributeurs automatiques Machine Break en Île-de-France. Les réponses de l'équipe. | oui | boissons-chaudes-snacks.html, contact.html, fonctionnement.html, index.html, mentions-legales.html, politique-de-confidentialite.html, solution-par-secteur.html, terms-of-service.html | 1 |
| `fonctionnement.html` | Fonctionnement de nos distributeurs automatiques | Machine Break | Le service Machine Break en Île-de-France : installation, approvisionnement, maintenance et suivi télémétrique de vos distributeurs, sans charge de gestion. | oui | boissons-chaudes-snacks.html, contact.html, faq.html, index.html, mentions-legales.html, politique-de-confidentialite.html, solution-par-secteur.html, terms-of-service.html | 1 |
| `index.html` | Distributeurs automatiques connectés pour entreprises | Machine Break | Machine Break installe et gère vos distributeurs automatiques connectés (café, boissons, snacks) en Île-de-France : réassort, entretien et suivi inclus. | oui | boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, mentions-legales.html, politique-de-confidentialite.html, solution-par-secteur.html, terms-of-service.html | 3 ⚠ |
| `mentions-legales.html` | Mentions légales | Machine Break | Mentions légales du site machinebreak.com : éditeur Machine Break à Bailly-Romainvilliers (77), directeur de publication, hébergeur et propriété intellectuelle. | **non** | boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html, politique-de-confidentialite.html, solution-par-secteur.html, terms-of-service.html | 1 |
| `politique-de-confidentialite.html` | Politique de confidentialité | Machine Break | Politique de confidentialité de Machine Break : données collectées via le formulaire de contact, finalités, durée de conservation, droits RGPD et contact. | **non** | boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html, mentions-legales.html, solution-par-secteur.html, terms-of-service.html | 1 |
| `solution-par-secteur.html` | Solutions distributeurs automatiques par secteur | Machine Break | Distributeurs automatiques adaptés à votre secteur en Île-de-France : bureaux et PME, résidences et hôtels, sites industriels et logistiques. Sur mesure. | oui | boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html, mentions-legales.html, politique-de-confidentialite.html, terms-of-service.html | 1 |
| `terms-of-service.html` | Conditions générales d'utilisation du site | Machine Break | Conditions générales d'utilisation du site machinebreak.com, opérateur de distribution automatique en Île-de-France, basé à Bailly-Romainvilliers (77). | **non** | boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html, mentions-legales.html, politique-de-confidentialite.html, solution-par-secteur.html | 1 |

## 2. Pages orphelines (hors navigation principale)

- `mentions-legales.html` — atteignable via : boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html, politique-de-confidentialite.html, solution-par-secteur.html, terms-of-service.html
- `politique-de-confidentialite.html` — atteignable via : boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html, mentions-legales.html, solution-par-secteur.html, terms-of-service.html
- `terms-of-service.html` — atteignable via : boissons-chaudes-snacks.html, contact.html, faq.html, fonctionnement.html, index.html, mentions-legales.html, politique-de-confidentialite.html, solution-par-secteur.html

## 3. Coordonnées (téléphones, adresses, emails)

### Téléphones

| Valeur | Pages (occurrences) |
|---|---|
| `01 74 81 09 52` | `boissons-chaudes-snacks.html` (2), `contact.html` (4), `faq.html` (2), `fonctionnement.html` (2), `index.html` (2), `mentions-legales.html` (6), `politique-de-confidentialite.html` (4), `solution-par-secteur.html` (2), `terms-of-service.html` (4) |

### Adresses postales (voie)

| Valeur | Pages (occurrences) |
|---|---|
| `28 Avenue Christian Doppler` | `boissons-chaudes-snacks.html` (1), `contact.html` (1), `faq.html` (1), `fonctionnement.html` (1), `index.html` (1), `mentions-legales.html` (2), `politique-de-confidentialite.html` (2), `solution-par-secteur.html` (1), `terms-of-service.html` (1) |

### Codes postaux + ville

| Valeur | Pages (occurrences) |
|---|---|
| `77700 Bailly-Romainvilliers` | `boissons-chaudes-snacks.html` (1), `contact.html` (1), `faq.html` (1), `fonctionnement.html` (1), `index.html` (1), `mentions-legales.html` (2), `politique-de-confidentialite.html` (2), `solution-par-secteur.html` (1), `terms-of-service.html` (1) |

### Emails

| Valeur | Pages (occurrences) |
|---|---|
| `contact@machinebreak.com` | `boissons-chaudes-snacks.html` (2), `contact.html` (4), `faq.html` (2), `fonctionnement.html` (2), `index.html` (2), `mentions-legales.html` (6), `politique-de-confidentialite.html` (6), `solution-par-secteur.html` (2), `terms-of-service.html` (4) |

## 4. `meta description` dupliquées

Aucune duplication.

### `<title>` dupliqués

Aucun.

### Open Graph / Twitter / canonical

| Fichier | canonical | og:url | og:image | twitter:image |
|---|---|---|---|---|
| `boissons-chaudes-snacks.html` | — | https://machinebreak.com/boissons-chaudes-snacks | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `contact.html` | — | https://machinebreak.com/contact | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `faq.html` | — | https://machinebreak.com/faq | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `fonctionnement.html` | — | https://machinebreak.com/fonctionnement | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `index.html` | — | https://machinebreak.com/ | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `mentions-legales.html` | — | https://machinebreak.com/mentions-legales | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `politique-de-confidentialite.html` | — | https://machinebreak.com/politique-de-confidentialite | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `solution-par-secteur.html` | — | https://machinebreak.com/solution-par-secteur | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |
| `terms-of-service.html` | — | https://machinebreak.com/terms-of-service | https://machinebreak.com/assets/img/og-image.jpg | https://machinebreak.com/assets/img/og-image.jpg |

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
- JSON-LD : `index.html` (1)

### Autres fichiers à la racine

- `AUDIT.md`
- `CONTENU-RECUPERE.md`
- `README.md`
- `_redirects`
- `robots.txt`
- `sitemap.xml`
- `tools/audit_site.py`

