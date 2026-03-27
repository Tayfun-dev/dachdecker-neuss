# Tayfun-dev.github.io Root Export

Das ist die saubere Basis für alle zukünftigen GitHub-Pages-Seiten.

Warum das besser ist:

- keine URL mehr mit `dachdecker-neuss` in jeder Seite
- alle Seiten laufen sauber unter `https://tayfun-dev.github.io/<slug>/`
- neue Kundenseiten können einfach als neuer Unterordner ergänzt werden

Beispiele:

- `https://tayfun-dev.github.io/dachdecker-koblenz/`
- `https://tayfun-dev.github.io/shk-herne/`
- `https://tayfun-dev.github.io/schluesseldienst-duesseldorf/`

Was in ein neues GitHub-Repo `Tayfun-dev.github.io` gehört:

- `index.html`
- `styles.css`
- `.github/workflows/pages.yml`
- alle Unterordner mit den einzelnen Seiten

Empfohlener Ablauf:

1. Neues öffentliches Repo `Tayfun-dev.github.io` anlegen
2. Den kompletten Inhalt dieses Ordners dort hochladen
3. In GitHub unter `Settings -> Pages` `GitHub Actions` auswählen
4. Kurz warten

Dann ist die Root-Domain sauber aufgesetzt.
