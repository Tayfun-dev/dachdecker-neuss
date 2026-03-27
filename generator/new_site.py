#!/usr/bin/env python3
"""Interactive helper to create a new niche landing page entry."""

from __future__ import annotations

from build_pages import ROOT, load_sites, main as build_pages_main
from site_factory import create_site_entry, save_sites


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def main() -> None:
    print("Neue Landingpage-Demo anlegen")
    branch = prompt("Branche", "Entruempelung")
    city = prompt("Stadt", "Düsseldorf")
    phone_display = prompt("Telefon", "0211 00000000")
    main_offer = prompt("Hauptangebot", "Schnelle Hilfe")
    category = prompt("Kategorie (optional)")
    subtitle = prompt("Untertitel (optional)")
    primary_cta = prompt("Primärer CTA (optional)")
    secondary_cta = prompt("Sekundärer CTA (optional)")

    sites = load_sites()
    new_entry = create_site_entry(
        branch,
        city,
        phone_display,
        main_offer,
        overrides={
            "category": category,
            "subtitle": subtitle,
            "primary_cta": primary_cta,
            "secondary_cta": secondary_cta,
        },
    )

    if any(site["slug"] == new_entry["slug"] for site in sites):
        print(f"Abgebrochen: Der Slug '{new_entry['slug']}' existiert bereits.")
        return

    sites.append(new_entry)
    save_sites(sites)
    build_pages_main()

    print("")
    print("Fertig.")
    print(f"Slug: {new_entry['slug']}")
    print(f"Ordner: {ROOT / new_entry['slug']}")
    print(f"GitHub Pages URL: https://tayfun-dev.github.io/dachdecker-neuss/{new_entry['slug']}/")
    print("Wenn du live gehen willst:")
    print("git add . && git commit -m \"Add new niche demo\" && git push")


if __name__ == "__main__":
    main()
