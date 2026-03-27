#!/usr/bin/env python3
"""Bulk import niche landing pages from a CSV file."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from build_pages import ROOT, load_sites, main as build_pages_main
from new_site import create_site_entry, save_sites


DEFAULT_CSV = ROOT / "generator" / "bulk_sites.csv"
REQUIRED_COLUMNS = ("branch", "city", "phone", "main_offer")


def read_rows(csv_path: Path) -> list[dict]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV hat keine Kopfzeile.")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV-Spalten fehlen: {', '.join(missing)}")

        rows: list[dict] = []
        for row in reader:
            normalized = {key: (value or "").strip() for key, value in row.items()}
            if not any(normalized.values()):
                continue
            rows.append(normalized)
        return rows


def import_rows(rows: list[dict]) -> tuple[int, int, list[str]]:
    sites = load_sites()
    existing_slugs = {site["slug"] for site in sites}
    added = 0
    skipped = 0
    created_slugs: list[str] = []

    for row in rows:
        entry = create_site_entry(
            branch=row["branch"],
            city=row["city"],
            phone_display=row["phone"],
            main_offer=row["main_offer"],
        )
        if entry["slug"] in existing_slugs:
            skipped += 1
            continue
        sites.append(entry)
        existing_slugs.add(entry["slug"])
        created_slugs.append(entry["slug"])
        added += 1

    if added:
        save_sites(sites)
        build_pages_main()

    return added, skipped, created_slugs


def main() -> None:
    csv_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    csv_path = csv_arg if csv_arg.is_absolute() else ROOT / csv_arg

    if not csv_path.exists():
        print(f"CSV nicht gefunden: {csv_path}")
        print("Nutze entweder einen Pfad als Argument oder erstelle generator/bulk_sites.csv")
        sys.exit(1)

    rows = read_rows(csv_path)
    if not rows:
        print(f"Keine importierbaren Zeilen in {csv_path}")
        return

    added, skipped, created_slugs = import_rows(rows)

    print(f"CSV verarbeitet: {csv_path}")
    print(f"Neu angelegt: {added}")
    print(f"Übersprungen (Duplikate): {skipped}")
    if created_slugs:
        print("Neue Slugs:")
        for slug in created_slugs:
            print(f"- {slug}")
    print("")
    print("Wenn du live gehen willst:")
    print("git add . && git commit -m \"Import bulk niche demos\" && git push")


if __name__ == "__main__":
    main()
