# GitHub Pages Deployment

Diese Website ist als statische Seite fuer GitHub Pages vorbereitet.

## Dateien

- `index.html`
- `styles.css`
- `.github/workflows/pages.yml`

## So stellst du die Seite live

1. Neues leeres GitHub-Repository anlegen
2. Dieses Projekt in das Repo pushen
3. In GitHub unter `Settings -> Pages` als Quelle `GitHub Actions` auswaehlen
4. Auf den ersten erfolgreichen Workflow-Lauf warten
5. Den erzeugten GitHub-Pages-Link an den Kunden schicken

## Lokale Git-Befehle

```bash
cd /Users/tayfungomukpinar/Documents/Playground
git add .
git commit -m "Add Dachdecker Neuss landing page"
git remote add origin https://github.com/DEIN-USERNAME/DEIN-REPO.git
git push -u origin main
```

## Hinweis

Falls `origin` schon existiert, nutze stattdessen:

```bash
git remote set-url origin https://github.com/DEIN-USERNAME/DEIN-REPO.git
git push -u origin main
```
