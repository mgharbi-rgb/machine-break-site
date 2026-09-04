# Contenu récupéré des pages orphelines (ancienne génération du site)

Extrait le 2026-09-03 depuis la version en ligne de machinebreak.com, avant redirection 301.
Ces deux pages appartiennent à l'ancienne génération du site (adresse La Garenne-Colombes, tél. 01 70 82 31 32, logo `.jpg`).
**Décision client (2026-09-03) :** pages supprimées volontairement, contenu périmé (anciennes machines). Rien n'est à remettre en ligne tel quel ; seuls les éléments ci-dessous sont conservés comme matière première.

## 1. Engagement de service (réutilisé en Phase 2, bloc « Nos engagements »)

Source : `/location-distributeurs-automatiques-boissons`, section « Nos solutions ».

- **Installation** — « Nos équipes se chargent de la livraison et de la mise en service des appareils. L'installation nécessite un emplacement dédié, une arrivée d'eau et d'électricité. »
- **Maintenance** — « La maintenance des machines s'effectue à l'aide des données télémétriques que nous envoient nos appareils. **Lorsqu'une panne est signalée un technicien est envoyé dans la demi-journée.** Le **nettoyage des machines se fait de manière hebdomadaire**, suivant des normes d'hygiène très strictes. »
- **Approvisionnement** — « L'approvisionnement des machines se fait de façon régulière selon vos habitudes de consommation. Ce renouvellement est planifié grâce à notre système de télémétrie installé sur les machines qui permet aux techniciens de suivre l'état des machines en temps réel. »

> Valeurs à confirmer par le client avant publication : délai d'intervention (« demi-journée »), fréquence de nettoyage (« hebdomadaire »). Voir `TODO:MB` dans les pages.

## 2. Catalogue d'équipements Necta (périmé selon le client — archivé, ne pas republier)

Source : `/location-distributeurs-automatiques-boissons`, section « Nos équipements ».

| Modèle | Description d'origine |
|---|---|
| Krea Touch | Solution idéale pour les hôtels, la restauration et les sites libre-service. Complète le portefeuille de solutions de petit-déjeuner Necta. |
| Melodia | Dimensions réduites et grande capacité : solution idéale aux emplacements limités. |
| Kalea | Café de qualité : expressos italiens, cappuccinos, latte macchiato. |
| Tango | Modèle Impulse, allure personnalisable. |
| Orchestra | Famille de machines à 8 spires pour les sites les plus exigeants. |
| Opera | Milieu de gamme haute technologie, large gamme de produits, excellente qualité de boissons. |

Si une page `/solutions/equipements` est créée (Phase 3), le catalogue devra être refait avec le parc actuel fourni par le client.

## 3. `title` et `meta description` d'origine (géolocalisés)

| Page | `<title>` | `meta description` |
|---|---|---|
| `/location-distributeurs-automatiques-boissons` | Location distributeurs boissons chaudes Paris | Besoin d'une machine à café pour vos clients ? Faites appel à Machine Break pour des solutions sur mesures à Paris en distribution automatique de boissons. |
| `/entreprise-location-distributeur-automatique-boisson` | Entreprise location distributeurs boissons automatiques Paris | Besoin de solutions pour proposer à vos clients, collaborateurs un distributeur de boissons : cafés, thés, snacks. Faites appel à Machine Break. |

Ces formulations (« location distributeurs boissons », « Paris ») sont des requêtes de recherche à réutiliser dans les titres des pages actuelles, en remplaçant « Paris » par « Île-de-France » selon le format `[Besoin] + [Zone] | Machine Break`.

## 4. Redirections retenues

| Ancienne URL | Destination 301 | Motif |
|---|---|---|
| `/location-distributeurs-automatiques-boissons` | `/fonctionnement` | Contenu = équipements + installation/maintenance/approvisionnement |
| `/entreprise-location-distributeur-automatique-boisson` | `/boissons-chaudes-snacks` | Contenu = partenaires produits |
| `/index.html` | `/` | Doublon |
| `/careers`, `/career-single` | `/contact` | Pages supprimées (décision client 2026-09-03 : le recrutement ne passe pas par le site) |
| `/avantages` | `/fonctionnement` | Brouillon inachevé, jamais lié |
| `/admin/*` | `/` | Interface Netlify CMS retirée (décision client 2026-09-03) |

Les règles sont dans le fichier `_redirects` (syntaxe Netlify), avec les variantes `.html`.

## 5. Autre contenu de la page `/entreprise-location-distributeur-automatique-boisson`

Une seule section textuelle : « Nous travaillons avec les meilleurs. Dans l'optique d'améliorer la qualité de nos prestations, nous sélectionnons les meilleurs partenaires pour des produits de qualité supérieure. » suivie de logos partenaires (SVG inline). Pas de contenu à conserver.
