# Sales System

Dieser Ordner ist fuer wiederholbare Akquise gedacht.

## Inhalt

- `leads_template.csv`
- `dachdecker_duesseldorf_leads.csv`
- `generate_outreach.py`

## Lead-Felder

- `business_name`
- `city`
- `niche`
- `contact_name`
- `website`
- `website_status`
- `source`
- `instagram`
- `phone`
- `pitch_angle`
- `demo_slug`
- `notes`
- `status`
- `next_follow_up`

`website_status` sollte idealerweise einer von diesen Werten sein:

- `none`
- `weak`
- `directory`

## Outreach automatisch erzeugen

```bash
cd /Users/tayfungomukpinar/Documents/Playground
python3 -B sales/generate_outreach.py sales/dachdecker_duesseldorf_leads.csv https://tayfun-dev.github.io sales/outreach_output.md
```

Danach liegt eine fertige Datei mit:

- Erstnachricht
- Follow-up Tag 2
- Follow-up Tag 5
- Preisnachricht
- Telefon-Opener

in:

- `sales/outreach_output.md`

## Sales-Regel

Nicht "Website" verkaufen.
Immer diese 3 Dinge verkaufen:

1. mehr Vertrauen
2. klarerer erster Eindruck
3. mehr Anrufe und Nachrichten
