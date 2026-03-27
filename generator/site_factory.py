#!/usr/bin/env python3
"""Shared helpers for creating niche landing-page entries."""

from __future__ import annotations

import json
import re
import unicodedata

from build_pages import DATA_FILE


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
        "mode": "emergency",
        "category": "Notdienst",
        "subtitle": "Schnelle Hilfe & direkter Kontakt",
        "hub": "Aussperrung, Türöffnung und direkte Hilfe mit starker Notfall-Ansprache.",
    },
    {
        "keywords": ["elektriker", "elektro", "strom"],
        "visuals": ["electricity", "panel"],
        "mode": "emergency",
        "category": "Notdienst",
        "subtitle": "Notdienst & Elektrohilfe",
        "hub": "Stromausfall, Sicherung, Elektro-Notdienst und klare Soforthilfe.",
    },
    {
        "keywords": ["maler", "lackierer", "anstrich"],
        "visuals": ["paint", "roller"],
        "mode": "service",
        "category": "Renovierung",
        "subtitle": "Anstrich, Renovierung & saubere Ausführung",
        "hub": "Saubere Renovierungs-Leads für Anstrich, Lackierung und Wohnungsübergaben.",
    },
    {
        "keywords": ["trockenbau", "innenausbau"],
        "visuals": ["wall", "ceiling"],
        "mode": "service",
        "category": "Innenausbau",
        "subtitle": "Raumlösungen & Innenausbau",
        "hub": "Wände, Decken, Raumaufteilung und saubere Ausbau-Projekte mit klarer Struktur.",
    },
    {
        "keywords": ["rohr", "abfluss", "kanal"],
        "visuals": ["drain", "pipe"],
        "mode": "emergency",
        "category": "Notdienst",
        "subtitle": "Soforthilfe & Notdienst",
        "hub": "Rohrreinigung und Abflusshilfe mit hoher Dringlichkeit und starken Call-Leads.",
    },
    {
        "keywords": ["photovoltaik", "solar", "solaranlage"],
        "visuals": ["solar", "house"],
        "mode": "premium",
        "category": "High Ticket",
        "subtitle": "Beratung, Planung & Montage",
        "hub": "High-ticket Eigentümer-Leads für Solaranlage, Beratung und Montage.",
    },
]


MODE_DEFAULTS = {
    "emergency": {
        "primary_cta": "Jetzt Hilfe anfragen",
        "secondary_cta": "Problem schildern",
        "status_chip": "Sofortkontakt",
        "status_title": "Tempo, Vertrauen und Klarheit auf einen Blick.",
        "status_text": "Gerade bei akuten Problemen entscheiden oft die ersten Sekunden auf dem Handy.",
        "reviews_intro": "Beispielhafte Demo-Bewertungen für spätere Trust-Elemente im Notdienst-Kontext.",
        "form_intro": "Formular zeigt den schnellen Einstieg für akute Anfragen.",
    },
    "service": {
        "primary_cta": "Jetzt Anfrage starten",
        "secondary_cta": "Leistungen ansehen",
        "status_chip": "Lokale Anfrage",
        "status_title": "Sauber präsentiert. Direkt verständlich. Leicht anfragbar.",
        "status_text": "Bei planbaren Dienstleistungen zählt vor allem eine ruhige, klare und vertrauenswürdige Darstellung.",
        "reviews_intro": "Beispielhafte Demo-Bewertungen für eine serviceorientierte Vertrauensdarstellung.",
        "form_intro": "Formular zeigt den einfachen Einstieg für neue Anfragen.",
    },
    "premium": {
        "primary_cta": "Beratung anfragen",
        "secondary_cta": "Projekt ansehen",
        "status_chip": "Beratung & Abschluss",
        "status_title": "Mehr Wertigkeit für erklärungsbedürftige Angebote.",
        "status_text": "Bei High-Ticket-Themen hilft eine ruhigere, hochwertigere Lead-Story mit klarer Beratungsausrichtung.",
        "reviews_intro": "Beispielhafte Demo-Bewertungen für beratungsstarke High-Ticket-Angebote.",
        "form_intro": "Formular zeigt den Einstieg für qualifizierte Beratungsanfragen.",
    },
}


def slugify(value: str) -> str:
    replacements = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
    lowered = value.lower()
    for source, target in replacements.items():
        lowered = lowered.replace(source, target)
    normalized = unicodedata.normalize("NFKD", lowered)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-")


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
        "mode": "service",
        "category": "Lokal",
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


def save_sites(sites: list[dict]) -> None:
    DATA_FILE.write_text(
        json.dumps(sites, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def create_site_entry(
    branch: str,
    city: str,
    phone_display: str,
    main_offer: str,
    overrides: dict | None = None,
) -> dict:
    overrides = {key: value for key, value in (overrides or {}).items() if value not in ("", None)}
    full_name = f"{branch} {city}"
    slug = slugify(full_name)
    profile = choose_profile(branch)
    palette = choose_palette(slug)
    phone_href = normalize_phone_href(phone_display)
    visual_1, visual_2 = profile["visuals"]
    defaults = MODE_DEFAULTS.get(profile.get("mode", "service"), MODE_DEFAULTS["service"])

    subtitle = overrides.get("subtitle", profile["subtitle"])
    primary_cta = overrides.get("primary_cta", defaults["primary_cta"])
    secondary_cta = overrides.get("secondary_cta", defaults["secondary_cta"])
    hub_excerpt = overrides.get("hub_excerpt", profile["hub"])

    entry = {
        "slug": slug,
        "city": city,
        "category": overrides.get("category", profile.get("category", "Lokal")),
        "name": full_name,
        "subtitle": subtitle,
        "short_name": initials(branch),
        "title": overrides.get("title", f"{full_name} | Demo-Landingpage"),
        "meta_description": overrides.get(
            "meta_description",
            f"Demo-Landingpage für {branch} in {city}: {main_offer}, lokale Lead-Ansprache und direkte Kontaktaufnahme.",
        ),
        "theme": palette,
        "phone_display": phone_display,
        "phone_href": phone_href,
        "topline": overrides.get("topline", f"{full_name} | {main_offer} | Demo-Website"),
        "demo_banner": overrides.get(
            "demo_banner",
            f"Demo-Konzept {branch} | Kontakt, Bewertungen und Referenzen sind Platzhalter",
        ),
        "hero_eyebrow": overrides.get("hero_eyebrow", full_name),
        "hero_title": overrides.get(
            "hero_title",
            f"Mehr Anfragen für {branch} in {city}, ohne dass Besucher lange überlegen müssen.",
        ),
        "hero_lead": overrides.get(
            "hero_lead",
            f"Diese Demo-Landingpage ist auf direkte Leads ausgelegt: {main_offer}, klare Positionierung, lokale Relevanz und eine einfache Anfrage per Telefon, WhatsApp oder Formular.",
        ),
        "primary_cta": primary_cta,
        "secondary_cta": secondary_cta,
        "trust_items": [
            "direkte Kontaktflächen",
            "starke mobile Struktur",
            "lokale Relevanz",
            f"{city} und Umgebung",
            "Platz für echte Bewertungen",
        ],
        "contact_card_text": overrides.get(
            "contact_card_text",
            "Die Demo ist so gebaut, dass Vertrauen, Nutzen und nächster Schritt schnell verständlich werden.",
        ),
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
        "status_chip": overrides.get("status_chip", defaults["status_chip"]),
        "status_title": overrides.get("status_title", defaults["status_title"]),
        "status_text": overrides.get(
            "status_text",
            defaults["status_text"],
        ),
        "services_intro": overrides.get("services_intro", "Die wichtigsten Einstiege für schnelle Anfragen."),
        "services": make_services(main_offer),
        "why_title": overrides.get("why_title", "Warum diese Struktur für lokale Anfragen funktioniert."),
        "why_text": overrides.get(
            "why_text",
            "Die Seite reduziert Unsicherheit, macht den Nutzen verständlich und führt Besucher sichtbar zum nächsten Schritt.",
        ),
        "why_items": make_why_items(branch, city),
        "reviews_intro": overrides.get(
            "reviews_intro",
            defaults["reviews_intro"],
        ),
        "reviews": make_reviews(branch, city),
        "faqs": make_faqs(branch, city, main_offer),
        "contact_title": overrides.get("contact_title", f"Demo-Kontaktbereich für {branch}-Leads in {city}."),
        "contact_text": overrides.get(
            "contact_text",
            "Später lassen sich hier echte Telefonnummer, WhatsApp-Link, Bilder und qualifizierende Felder ergänzen.",
        ),
        "contact_box_1_title": "Demo-Nummer",
        "contact_box_1_text": "Platzhalter für direkten Erstkontakt",
        "contact_box_2_title": "Demo-WhatsApp",
        "contact_box_2_text": "Platzhalter für Bilder und Kurzbeschreibung",
        "form_intro": overrides.get("form_intro", defaults["form_intro"]),
        "form_placeholder": overrides.get("form_placeholder", f"Worum geht es bei {main_offer} genau?"),
        "form_success": overrides.get(
            "form_success",
            "Demo-Formular aktiv: Für Live-Nutzung nur echte Kontaktdaten und Angebotslogik einsetzen.",
        ),
        "hub_excerpt": hub_excerpt,
    }

    trust_override = [
        overrides.get("trust_1"),
        overrides.get("trust_2"),
        overrides.get("trust_3"),
        overrides.get("trust_4"),
        overrides.get("trust_5"),
    ]
    filtered_trust = [item for item in trust_override if item]
    if filtered_trust:
        entry["trust_items"] = filtered_trust

    return entry
