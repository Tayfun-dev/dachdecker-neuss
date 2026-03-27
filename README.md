# GitHub Pages Deployment

Diese Website ist als statische Seite fuer GitHub Pages vorbereitet.

## Dateien

- `index.html`
- `styles.css`
- `.github/workflows/pages.yml`
- `generator/sites.json`
- `generator/build_pages.py`

## Landingpage-Generator

Neue Demo-Seiten werden ueber eine zentrale Daten-Datei erzeugt.

### Daten pflegen

Alle Branchen-Demos stehen in:

- `generator/sites.json`

Dort kannst du neue Eintraege fuer weitere Staedte, Branchen und Angebote anlegen.

### Seiten neu erzeugen

```bash
cd /Users/tayfungomukpinar/Documents/Playground
python3 -B generator/build_pages.py
```

Der Befehl aktualisiert:

- `demos/index.html`
- alle generierten Unterordner wie `schluesseldienst-duesseldorf/`
- weitere neue Branchen aus `generator/sites.json`

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
