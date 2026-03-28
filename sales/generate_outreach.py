#!/usr/bin/env python3
"""Generate repeatable outreach and follow-up copy from a CSV lead list."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "sales" / "leads_template.csv"
DEFAULT_OUTPUT = ROOT / "sales" / "outreach_output.md"
DEFAULT_BASE_URL = "https://tayfun-dev.github.io"


WEBSITE_ANGLES = {
    "none": "Sie haben online noch keinen klaren Auftritt, der Vertrauen aufbaut und Anfragen aktiv einsammelt.",
    "weak": "Ihr aktueller Auftritt wirkt eher wie eine Visitenkarte als wie eine Seite, die aktiv Anfragen auslöst.",
    "directory": "Sie sind zwar online sichtbar, aber eher über Verzeichnisse statt über eine eigene starke Landingpage.",
}


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    def normalize(value: object) -> str:
        if isinstance(value, list):
            return " | ".join((item or "").strip() for item in value)
        return (value or "").strip()

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [{key: normalize(value) for key, value in row.items()} for row in reader]


def demo_url(base_url: str, slug: str) -> str:
    clean = base_url.rstrip("/")
    if not slug:
        return clean
    return f"{clean}/{slug.strip('/')}/"


def pick_angle(row: dict[str, str]) -> str:
    if row.get("pitch_angle"):
        return row["pitch_angle"]
    return WEBSITE_ANGLES.get(row.get("website_status", "").lower(), "Ihr Auftritt kann deutlich klarer auf Kontakt und Vertrauen gebaut werden.")


def intro_line(row: dict[str, str]) -> str:
    niche = row.get("niche", "Betrieb")
    city = row.get("city", "Ihrer Stadt")
    return f"Ich habe mir Ihren {niche}-Auftritt in {city} kurz angesehen."


def initial_dm(row: dict[str, str], link: str) -> str:
    angle = pick_angle(row)
    return (
        f"Hallo,\n\n"
        f"{intro_line(row)}\n"
        f"Mir ist dabei aufgefallen: {angle}\n\n"
        f"Ich habe deshalb eine stärkere Beispielseite vorbereitet, die klarer verkauft und Besucher schneller zur Anfrage führt:\n"
        f"{link}\n\n"
        f"Wenn die Richtung für Sie interessant ist, kann ich so etwas sauber auf Ihren Betrieb anpassen."
    )


def follow_up_day_2(row: dict[str, str], link: str) -> str:
    return (
        f"Hallo, ich wollte nur kurz nachhaken.\n\n"
        f"Hier ist nochmal die Vorschau für {row.get('business_name', 'Ihren Betrieb')}:\n"
        f"{link}\n\n"
        f"Die Seite ist bewusst so gebaut, dass Besucher in wenigen Sekunden verstehen, was Sie anbieten und wie sie direkt Kontakt aufnehmen können."
    )


def follow_up_day_5(row: dict[str, str], link: str) -> str:
    niche = row.get("niche", "Betrieb")
    return (
        f"Kurze Rückfrage:\n\n"
        f"Was wäre für Sie online wichtiger: einfach eine Website zu haben oder darüber spürbar mehr {niche}-Anfragen zu bekommen?\n\n"
        f"Falls Sie es sich anschauen möchten, hier ist die Vorschau nochmal:\n"
        f"{link}"
    )


def price_message(row: dict[str, str]) -> str:
    return (
        "Für die fertige Umsetzung inkl. Aufbau, Text, mobiler Optimierung und Livegang "
        "liegen wir je nach Umfang meist bei 790 € bis 990 €.\n"
        "Dazu kommen 29 € bis 39 € monatlich für Domain, Hosting und kleine laufende Anpassungen."
    )


def call_opener(row: dict[str, str]) -> str:
    return (
        f"Hallo, mein Name ist Tayfun. Ich habe mir Ihren Auftritt kurz angesehen und "
        f"habe eine Idee, wie man für {row.get('business_name', 'Ihren Betrieb')} online deutlich klarer Anfragen einsammeln kann. "
        f"Haben Sie gerade 30 Sekunden?"
    )


def render_markdown(rows: list[dict[str, str]], base_url: str) -> str:
    lines: list[str] = [
        "# Outreach Output",
        "",
        "Diese Datei wird aus den Lead-Daten erzeugt.",
        "",
    ]

    for index, row in enumerate(rows, start=1):
        business_name = row.get("business_name", f"Lead {index}")
        status = row.get("website_status", "")
        link = demo_url(base_url, row.get("demo_slug", ""))

        lines.extend(
            [
                f"## {index}. {business_name}",
                "",
                f"- Stadt: {row.get('city', '')}",
                f"- Nische: {row.get('niche', '')}",
                f"- Website: {row.get('website', '') or 'keine'}",
                f"- Website-Status: {status or 'unbekannt'}",
                f"- Quelle: {row.get('source', '')}",
                f"- Notizen: {row.get('notes', '')}",
                f"- Demo-Link: {link}",
                "",
                "### Erstnachricht",
                "",
                "```text",
                initial_dm(row, link),
                "```",
                "",
                "### Follow-up Tag 2",
                "",
                "```text",
                follow_up_day_2(row, link),
                "```",
                "",
                "### Follow-up Tag 5",
                "",
                "```text",
                follow_up_day_5(row, link),
                "```",
                "",
                "### Preisnachricht",
                "",
                "```text",
                price_message(row),
                "```",
                "",
                "### Telefon-Opener",
                "",
                "```text",
                call_opener(row),
                "```",
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    csv_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    base_url = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_BASE_URL
    output_path = Path(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_OUTPUT

    csv_path = csv_arg if csv_arg.is_absolute() else ROOT / csv_arg
    out_path = output_path if output_path.is_absolute() else ROOT / output_path

    if not csv_path.exists():
        print(f"CSV nicht gefunden: {csv_path}")
        sys.exit(1)

    rows = [row for row in load_rows(csv_path) if any(row.values())]
    out_path.write_text(render_markdown(rows, base_url), encoding="utf-8")

    print(f"Leads verarbeitet: {len(rows)}")
    print(f"Output geschrieben nach: {out_path}")


if __name__ == "__main__":
    main()
