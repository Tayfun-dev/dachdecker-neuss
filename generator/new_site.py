#!/usr/bin/env python3
"""Interactive helper to create a new niche landing page entry."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from build_pages import DATA_FILE, ROOT, load_sites, main as build_pages_main


PALETTES = [
    {"accent": "#d76735", "accent_deep": "#953b17", "info": "#2b6c8f"},
    {"accent": "#128c7e", "accent_deep": "#0d6158", "info": "#1f7a8c"},
    {"accent": "#d58f18", "accent_deep": "#9f6500", "info": "#556b2f"},
    {"accent": "#c46a39", "accent_deep": "#87401f", "info": "#5a6e7b"},
    {"accent": "#f39c12", "accent_deep": "#b66a06", "info": "#1c7c54"},
]


PROFILES = [
    {
        "keywords": ["schluessel", "schlüssel"],
        "visuals": ["key", "lock"],
        "subtitle": "Schnelle Hilfe & direkter Kontakt",
        "hub": "Aussperrung, Türöffnung und direkte Hilfe mit starker Notfall-Ansprache.",
    },
    {
        "keywords": ["elektriker", "elektro", "strom"],
        "visuals": ["electricity", "panel"],
        "subtitle": "Notdienst & Elektrohilfe",
        "hub": "Stromausfall, Sicherung, Elektro-Notdienst und klare Soforthilfe.",
    },
    {
        "keywords": ["maler", "lackierer", "anstrich"],
        "visuals": ["paint", "roller"],
        "subtitle": "Anstrich, Renovierung & saubere Ausführung",
        "hub": "Saubere Renovierungs-Leads für Anstrich, Lackierung und Wohnungsübergaben.",
    },
    {
        "keywords": ["trockenbau", "innenausbau"],
        "visuals": ["wall", "ceiling"],
        "subtitle": "Raumlösungen & Innenausbau",
        "hub": "Wände, Decken, Raumaufteilung und saubere Ausbau-Projekte mit klarer Struktur.",
    },
    {
        "keywords": ["rohr", "abfluss", "kanal"],
        "visuals": ["drain", "pipe"],
        "subtitle": "Soforthilfe & Notdienst",
        "hub": "Rohrreinigung und Abflusshilfe mit hoher Dringlichkeit und starken Call-Leads.",
    },
    {
        "keywords": ["photovoltaik", "solar", "solaranlage"],
        "visuals": ["solar", "house"],
        "subtitle": "Beratung, Planung & Montage",
        "hub": "High-ticket Eigentümer-Leads für Solaranlage, Beratung und Montage.",
    },
]


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def slugify(value: str) -> str:
    replacements = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
    lowered = value.lower()
    for source, target in replacements.items():
        lowered = lowered.replace(source, target)
    normalized = unicodedata.normalize("NFKD", lowered)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")
    return slug


def initials(value: str) -> str:
    words = [word for word in re.split(r"[^A-Za-zÄÖÜäöüß0-9]+", value) if word]
    if not words:
        return "LP"
    if len(words) == 1:
        return words[0][:2].upper()
    return "".join(word[0] for word in words[:2]).upper()


def normalize_phone_href(phone_display: str) -> str:
    digits = re.sub(r"\D+", "", phone_display)
    if not digits:
        return "+"
    if digits.startswith("00"):
        return "+" + digits[2:]
    if digits.startswith("0"):
        return "+49" + digits[1:]
    return "+" + digits


def choose_profile(branch: str) -> dict:
    lowered = branch.lower()
    for profile in PROFILES:
        if any(keyword in lowered for keyword in profile["keywords"]):
            return profile
    return {
        "visuals": ["house", "solar"],
        "subtitle": "Lokale Hilfe & klare Anfrage",
        "hub": "Lokale Lead-Landingpage mit direkter Kontaktaufnahme und klarer Positionierung.",
    }


def choose_palette(slug: str) -> dict:
    checksum = sum(ord(char) for char in slug)
    return PALETTES[checksum % len(PALETTES)]


def make_services(main_offer: str) -> list[dict]:
    return [
        {
            "title": main_offer,
            "text": "Das Hauptangebot steht sofort sichtbar im Fokus und beantwortet direkt den ersten Suchimpuls.",
        },
        {
            "title": "Schnelle Einschätzung",
            "text": "Besucher können ihr Problem oder Vorhaben kurz schildern und sehen sofort einen einfachen nächsten Schritt.",
        },
        {
            "title": "Vor-Ort-Termin",
            "text": "Die Seite ist darauf ausgelegt, kurzfristige Rückmeldung und klare Terminabstimmung zu verkaufen.",
        },
        {
            "title": "Direkte Anfrage",
            "text": "Anruf, WhatsApp oder Formular werden bewusst niedrigschwellig und conversionstark platziert.",
        },
    ]


def make_why_items(branch: str, city: str) -> list[dict]:
    return [
        {
            "title": "Klare Positionierung",
            "text": f"Die Seite macht in wenigen Sekunden verständlich, warum genau dieser {branch} in {city} relevant ist.",
        },
        {
            "title": "Starke mobile Nutzung",
            "text": "Große Buttons, klare Scrolltiefe und direkte Kontaktflächen erhöhen die Lead-Chance auf dem Handy.",
        },
        {
            "title": "Lokale Relevanz",
            "text": f"{city} steht nicht nur in der Überschrift, sondern zieht sich sauber durch die komplette Lead-Story.",
        },
        {
            "title": "Schneller Austausch",
            "text": "Texte, Telefonnummer und Angebote lassen sich später in Minuten auf echte Kundendaten umstellen.",
        },
    ]


def make_reviews(branch: str, city: str) -> list[dict]:
    return [
        {
            "text": f"„Sehr gute Demo dafür, wie man einen {branch} in {city} direkt, verständlich und kontaktstark präsentiert.“",
            "author": f"Demo-Bewertung · {city}",
        },
        {
            "text": "„Die Seite führt schnell zum Kontakt und wirkt dabei klar, lokal und vertrauenswürdig.“",
            "author": "Demo-Bewertung · Lead-Konzept",
        },
        {
            "text": "„Saubere Struktur für Anzeigen, Google Business und direkte Suchanfragen.“",
            "author": "Demo-Bewertung · Wachstum",
        },
    ]


def make_faqs(branch: str, city: str, main_offer: str) -> list[dict]:
    return [
        {
            "question": f"Ist diese Demo auf {main_offer} ausgerichtet?",
            "answer": f"Ja. Die Struktur ist so aufgebaut, dass {main_offer} als klarer Haupteinstieg für {branch}-Leads in {city} funktioniert.",
        },
        {
            "question": "Sind Kontaktdaten und Bewertungen echt?",
            "answer": "Nein. Diese Demo arbeitet bewusst mit Platzhaltern, damit das Konzept schnell gezeigt und später sauber ersetzt werden kann.",
        },
        {
            "question": "Kann man die Seite später einfach anpassen?",
            "answer": "Ja. Genau dafür gibt es den Generator: Daten ändern, Seiten neu bauen, pushen, fertig.",
        },
    ]


def create_site_entry(branch: str, city: str, phone_display: str, main_offer: str) -> dict:
    full_name = f"{branch} {city}"
    slug = slugify(full_name)
    profile = choose_profile(branch)
    palette = choose_palette(slug)
    phone_href = normalize_phone_href(phone_display)
    visual_1, visual_2 = profile["visuals"]
    return {
        "slug": slug,
        "city": city,
        "name": full_name,
        "subtitle": profile["subtitle"],
        "short_name": initials(branch),
        "title": f"{full_name} | Demo-Landingpage",
        "meta_description": f"Demo-Landingpage für {branch} in {city}: {main_offer}, lokale Lead-Ansprache und direkte Kontaktaufnahme.",
        "theme": palette,
        "phone_display": phone_display,
        "phone_href": phone_href,
        "topline": f"{full_name} | {main_offer} | Demo-Website",
        "demo_banner": f"Demo-Konzept {branch} | Kontakt, Bewertungen und Referenzen sind Platzhalter",
        "hero_eyebrow": full_name,
        "hero_title": f"Mehr Anfragen für {branch} in {city}, ohne dass Besucher lange überlegen müssen.",
        "hero_lead": f"Diese Demo-Landingpage ist auf direkte Leads ausgelegt: {main_offer}, klare Positionierung, lokale Relevanz und eine einfache Anfrage per Telefon, WhatsApp oder Formular.",
        "primary_cta": "Jetzt Anfrage starten",
        "secondary_cta": "Leistung ansehen",
        "trust_items": [
            "direkte Kontaktflächen",
            "starke mobile Struktur",
            "lokale Relevanz",
            f"{city} und Umgebung",
            "Platz für echte Bewertungen",
        ],
        "contact_card_text": "Die Demo ist so gebaut, dass Vertrauen, Nutzen und nächster Schritt schnell verständlich werden.",
        "visuals": [
            {
                "variant": visual_1,
                "kicker": "Sofort verständlich",
                "headline": f"{main_offer} muss in wenigen Sekunden greifbar und relevant wirken.",
            },
            {
                "variant": visual_2,
                "kicker": "Lokale Lead-Ansprache",
                "headline": f"Die Seite soll {branch}-Interessenten aus {city} schnell zum Kontakt führen.",
            },
        ],
        "status_chip": "Demo-Positionierung",
        "status_title": "Klarer Nutzen. Klare Anfrage. Klare Richtung.",
        "status_text": f"Genau so lässt sich {branch} in {city} als lokale Lead-Landingpage effizient präsentieren.",
        "services_intro": "Die wichtigsten Einstiege für schnelle Anfragen.",
        "services": make_services(main_offer),
        "why_title": "Warum diese Struktur für lokale Anfragen funktioniert.",
        "why_text": "Die Seite reduziert Unsicherheit, macht den Nutzen verständlich und führt Besucher sichtbar zum nächsten Schritt.",
        "why_items": make_why_items(branch, city),
        "reviews_intro": "Beispielhafte Demo-Bewertungen für die spätere Trust-Darstellung.",
        "reviews": make_reviews(branch, city),
        "faqs": make_faqs(branch, city, main_offer),
        "contact_title": f"Demo-Kontaktbereich für {branch}-Leads in {city}.",
        "contact_text": "Später lassen sich hier echte Telefonnummer, WhatsApp-Link, Bilder und qualifizierende Felder ergänzen.",
        "contact_box_1_title": "Demo-Nummer",
        "contact_box_1_text": "Platzhalter für direkten Erstkontakt",
        "contact_box_2_title": "Demo-WhatsApp",
        "contact_box_2_text": "Platzhalter für Bilder und Kurzbeschreibung",
        "form_intro": "Formular zeigt den schnellen Einstieg für neue Leads.",
        "form_placeholder": f"Worum geht es bei {main_offer} genau?",
        "form_success": "Demo-Formular aktiv: Für Live-Nutzung nur echte Kontaktdaten und Angebotslogik einsetzen.",
        "hub_excerpt": profile["hub"],
    }


def save_sites(sites: list[dict]) -> None:
    DATA_FILE.write_text(
        json.dumps(sites, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    print("Neue Landingpage-Demo anlegen")
    branch = prompt("Branche", "Entruempelung")
    city = prompt("Stadt", "Düsseldorf")
    phone_display = prompt("Telefon", "0211 00000000")
    main_offer = prompt("Hauptangebot", "Schnelle Hilfe")

    sites = load_sites()
    new_entry = create_site_entry(branch, city, phone_display, main_offer)

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
