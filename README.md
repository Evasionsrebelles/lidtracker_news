# Pokelids — Bulletin d'infos

Ce dépôt contient uniquement le "bulletin d'infos" affiché dans Pokelids
(popup / entrée de menu) et consultable directement en ligne.

## Fichiers

- **`news.json`** — la seule donnée source de vérité. L'app ET la page web
  lisent ce fichier. Format :

  ```json
  {
    "timestamp": "2026-08-27T10:00:00Z",
    "fr": ["Ligne 1", "Ligne 2"],
    "en": ["Line 1", "Line 2"],
    "jp": ["行1", "行2"]
  }
  ```

  - `timestamp` : date ISO 8601 (UTC) de la dernière mise à jour. C'est CE
    champ que l'app compare à la valeur mémorisée en local pour savoir s'il
    y a du nouveau.
  - `fr` / `en` / `jp` : les lignes du bulletin, une entrée par ligne,
    **dans le même ordre** dans les trois langues (l'app affichera la ligne
    `fr[i]` / `en[i]` / `jp[i]` selon la langue choisie).

- **`index.html`** — page web simple qui affiche ce même contenu
  (logo, titre, date, lignes), avec un petit sélecteur FR/EN/JP. Ne
  contient aucune donnée en dur : elle va chercher `news.json` au chargement.

- **`logo.png`** — **à ajouter toi-même** à la racine du dépôt, à côté de
  `index.html` (même dossier). N'importe quelle image carrée (ex.
  512×512) fonctionne, elle sera affichée centrée en haut de la page,
  redimensionnée automatiquement en 96×96 px à l'écran.

## Mise en place (une seule fois)

1. Crée un nouveau dépôt GitHub (public), par exemple `pokelids-news`.
2. Mets-y ces 3 fichiers (`news.json`, `index.html`, `README.md`) + ton
   `logo.png` à la racine.
3. Active **GitHub Pages** : Settings → Pages → Source = branche `main`,
   dossier `/ (root)` → Save.
4. Après quelques minutes, la page sera visible à :
   `https://<ton-user>.github.io/<nom-du-repo>/`

## URL à donner à l'app

L'app doit lire directement le JSON brut (pas la page HTML), à cette URL :

```
https://raw.githubusercontent.com/<ton-user>/<nom-du-repo>/main/news.json
```

(remplace `<ton-user>` et `<nom-du-repo>` par les tiens — remplace aussi
`main` par le nom de ta branche si elle s'appelle autrement, ex. `master`)

## Publier une nouvelle info

1. Édite `news.json` :
   - Ajoute ta/tes nouvelle(s) ligne(s) dans les 3 tableaux (`fr`, `en`,
     `jp`), à la position que tu veux (généralement en premier, ou en
     dernier — à toi de choisir l'ordre d'affichage).
   - Mets à jour le champ `timestamp` avec la date/heure actuelle en UTC
     (ex. `2026-09-01T14:30:00Z`) — **c'est ce qui déclenche le popup**
     côté app, même si tu ne changes que le texte.
2. Commit + push sur GitHub (directement depuis l'interface web GitHub si
   tu veux, pas besoin de Git en ligne de commande).
3. C'est tout : la page web se met à jour immédiatement, et l'app détectera
   la nouvelle info à son prochain lancement.

⚠️ Si tu ne changes QUE le texte sans changer `timestamp`, l'app ne
détectera pas de nouveauté (elle ne compare que l'horodatage).
