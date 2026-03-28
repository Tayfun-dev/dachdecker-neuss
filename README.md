# GitHub Pages Deployment

Diese Website ist als statische Seite fuer GitHub Pages vorbereitet.

## Dateien

- `index.html`
- `styles.css`
- `.github/workflows/pages.yml`
- `generator/sites.json`
- `generator/build_pages.py`
- `generator/new_site.py`
- `generator/import_sites_csv.py`
- `generator/bulk_sites_template.csv`
- `sales/leads_template.csv`
- `sales/generate_outreach.py`

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

### Neue Seite per Fragen-Tool anlegen

Wenn du nicht direkt JSON bearbeiten willst:

```bash
cd /Users/tayfungomukpinar/Documents/Playground
python3 -B generator/new_site.py
```

Dann fragt das Tool nacheinander:

- Branche
- Stadt
- Telefon
- Hauptangebot

Danach passiert automatisch:

- neuer Eintrag in `generator/sites.json`
- Generierung der neuen Unterseite
- Aktualisierung von `demos/index.html`

Zum Live-Stellen danach nur noch:

```bash
git add .
git commit -m "Add new niche demo"
git push
```

### Mehrere Seiten per CSV anlegen

Wenn du viele Seiten auf einmal bauen willst:

1. Oeffne `generator/bulk_sites_template.csv`
2. Fuelle Zeilen mit:
   - `branch`
   - `city`
   - `phone`
   - `main_offer`
3. Speichere die Datei als `generator/bulk_sites.csv`
4. Fuehre aus:

```bash
cd /Users/tayfungomukpinar/Documents/Playground
python3 -B generator/import_sites_csv.py
```

Oder mit eigener Datei:

```bash
cd /Users/tayfungomukpinar/Documents/Playground
python3 -B generator/import_sites_csv.py generator/bulk_sites_example.csv
```

Danach passiert automatisch:

- neue Eintraege in `generator/sites.json`
- Generierung aller neuen Unterseiten
- Aktualisierung von `demos/index.html`

Das ist auch der einfachste Weg fuer Google Sheets:

1. Spalten genauso in Google Sheets anlegen
2. Als CSV herunterladen
3. Die CSV mit `python3 -B generator/import_sites_csv.py PFAD_ZUR_DATEI.csv` importieren

## Sales-System

Fuer Akquise, Follow-ups und CRM gibt es einen extra Bereich:

- `sales/leads_template.csv`
- `sales/dachdecker_duesseldorf_leads.csv`
- `sales/generate_outreach.py`
- `sales/README.md`

Outreach aus einer Lead-Liste erzeugen:

```bash
cd /Users/tayfungomukpinar/Documents/Playground
python3 -B sales/generate_outreach.py sales/dachdecker_duesseldorf_leads.csv https://tayfun-dev.github.io sales/outreach_output.md
```

Danach entsteht eine Markdown-Datei mit:

- Erstnachrichten
- Follow-up Texten
- Preisnachrichten
- Telefon-Openern

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
