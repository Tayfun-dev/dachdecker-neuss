#!/usr/bin/env python3
"""Generate local niche demo landing pages from a shared template."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "generator" / "sites.json"
DEMO_HUB_DIR = ROOT / "demos"


def load_sites() -> list[dict]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def visual_svg(variant: str) -> str:
    variants = {
        "key": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#1b2229" />
            <rect x="82" y="46" width="112" height="148" rx="8" fill="#d7b178" />
            <circle cx="164" cy="122" r="18" fill="#1b2229" />
            <rect x="158" y="122" width="12" height="36" rx="6" fill="#1b2229" />
            <circle cx="229" cy="92" r="28" fill="#f0c76a" />
            <rect x="194" y="87" width="70" height="10" rx="5" fill="#f0c76a" />
            <rect x="248" y="87" width="12" height="28" rx="4" fill="#f0c76a" />
          </svg>
        """,
        "lock": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#222c35" />
            <rect x="94" y="72" width="132" height="108" rx="20" fill="#edf0f2" />
            <path d="M128 72a32 32 0 1 1 64 0" fill="none" stroke="#edf0f2" stroke-width="18" />
            <circle cx="160" cy="120" r="14" fill="#222c35" />
            <rect x="154" y="120" width="12" height="28" rx="6" fill="#222c35" />
          </svg>
        """,
        "electricity": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#132028" />
            <path d="M150 30h22l-18 52h28l-46 72l10-46h-26z" fill="#ffd34f" />
            <rect x="66" y="126" width="188" height="58" rx="18" fill="#dce5ea" />
            <circle cx="122" cy="155" r="10" fill="#132028" />
            <circle cx="198" cy="155" r="10" fill="#132028" />
          </svg>
        """,
        "panel": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#202b33" />
            <rect x="88" y="36" width="144" height="148" rx="16" fill="#f4f6f7" />
            <rect x="116" y="62" width="88" height="26" rx="8" fill="#f0b100" />
            <rect x="112" y="104" width="96" height="12" rx="6" fill="#cad4da" />
            <rect x="112" y="128" width="96" height="12" rx="6" fill="#cad4da" />
            <rect x="112" y="152" width="56" height="12" rx="6" fill="#cad4da" />
          </svg>
        """,
        "paint": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#223142" />
            <rect x="46" y="52" width="228" height="118" rx="16" fill="#f5efe7" />
            <rect x="76" y="82" width="140" height="20" rx="10" fill="#db6d45" />
            <rect x="76" y="114" width="106" height="18" rx="9" fill="#8bb6d5" />
            <rect x="230" y="74" width="26" height="90" rx="8" fill="#f2c14e" />
          </svg>
        """,
        "roller": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#2b3540" />
            <rect x="102" y="36" width="116" height="148" rx="8" fill="#f6f0ea" />
            <rect x="122" y="68" width="74" height="60" rx="8" fill="#db6d45" />
            <circle cx="188" cy="144" r="8" fill="#2b3540" />
            <rect x="44" y="80" width="76" height="24" rx="12" fill="#f2c14e" />
            <rect x="72" y="104" width="18" height="52" rx="8" fill="#f2c14e" />
          </svg>
        """,
        "wall": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#212a31" />
            <rect x="44" y="40" width="232" height="140" rx="18" fill="#ece8e1" />
            <rect x="128" y="40" width="14" height="140" fill="#c46a39" />
            <rect x="142" y="102" width="82" height="12" fill="#c46a39" />
            <rect x="70" y="72" width="34" height="44" rx="4" fill="#b7c4cf" />
            <rect x="174" y="128" width="34" height="44" rx="4" fill="#b7c4cf" />
          </svg>
        """,
        "ceiling": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#263039" />
            <rect x="52" y="50" width="216" height="24" rx="8" fill="#f4efe8" />
            <rect x="66" y="74" width="10" height="92" fill="#f4efe8" />
            <rect x="244" y="74" width="10" height="92" fill="#f4efe8" />
            <rect x="86" y="92" width="148" height="58" rx="8" fill="#c5d1d9" />
            <rect x="110" y="164" width="100" height="10" rx="5" fill="#c46a39" />
          </svg>
        """,
        "drain": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#102129" />
            <rect x="44" y="66" width="232" height="28" rx="14" fill="#d9e4e8" />
            <rect x="144" y="66" width="32" height="98" rx="12" fill="#d9e4e8" />
            <path d="M160 178c24 0 44-18 44-41h-88c0 23 20 41 44 41z" fill="#1fb7a7" />
            <circle cx="160" cy="118" r="8" fill="#102129" />
          </svg>
        """,
        "pipe": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#1a2d36" />
            <rect x="60" y="58" width="200" height="96" rx="18" fill="#ecf2f5" />
            <circle cx="120" cy="106" r="22" fill="#1fb7a7" />
            <circle cx="200" cy="106" r="22" fill="#1fb7a7" />
            <path d="M94 158h132" stroke="#ecf2f5" stroke-width="16" stroke-linecap="round" />
          </svg>
        """,
        "solar": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#1c2730" />
            <circle cx="72" cy="58" r="28" fill="#f39c12" />
            <path d="M96 156H54l34-78h42l34 78H122" fill="#2e5f88" />
            <path d="M72 80l68 76" stroke="#9fd3ff" stroke-width="8" />
            <path d="M102 80l68 76" stroke="#9fd3ff" stroke-width="8" />
            <path d="M132 80l68 76" stroke="#9fd3ff" stroke-width="8" />
            <path d="M74 118h126" stroke="#9fd3ff" stroke-width="8" />
          </svg>
        """,
        "house": """
          <svg viewBox="0 0 320 220" aria-hidden="true">
            <rect width="320" height="220" fill="#24313b" />
            <path d="M58 116l102-66l102 66v68H58z" fill="#eef3f4" />
            <path d="M42 116l118-82l118 82" fill="none" stroke="#f39c12" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" />
            <rect x="108" y="136" width="38" height="48" rx="6" fill="#95b7cf" />
            <rect x="172" y="136" width="38" height="28" rx="6" fill="#95b7cf" />
            <rect x="138" y="76" width="62" height="24" rx="6" fill="#2e5f88" />
          </svg>
        """,
    }
    return variants[variant].strip()


def join_lines(items: list[str], indent: int = 0) -> str:
    prefix = " " * indent
    return "\n".join(prefix + item for item in items)


def render_services(services: list[dict]) -> str:
    blocks = []
    for index, service in enumerate(services, start=1):
        blocks.append(
            f"""<article class="service-card">
              <span class="service-index">{index:02d}</span>
              <h3>{html.escape(service["title"])}</h3>
              <p>{html.escape(service["text"])}</p>
            </article>"""
        )
    return join_lines(blocks, 12)


def render_why_items(items: list[dict]) -> str:
    blocks = []
    for item in items:
        blocks.append(
            f"""<article class="why-card">
              <h3>{html.escape(item["title"])}</h3>
              <p>{html.escape(item["text"])}</p>
            </article>"""
        )
    return join_lines(blocks, 12)


def render_reviews(reviews: list[dict]) -> str:
    blocks = []
    for review in reviews:
        blocks.append(
            f"""<article class="review-card">
              <div class="review-stars">★★★★★</div>
              <p>{html.escape(review["text"])}</p>
              <strong>{html.escape(review["author"])}</strong>
            </article>"""
        )
    return join_lines(blocks, 12)


def render_faqs(faqs: list[dict]) -> str:
    blocks = []
    for index, faq in enumerate(faqs):
        open_attr = " open" if index == 0 else ""
        blocks.append(
            f"""<details{open_attr}>
              <summary>{html.escape(faq["question"])}</summary>
              <p>{html.escape(faq["answer"])}</p>
            </details>"""
        )
    return join_lines(blocks, 12)


def render_visuals(visuals: list[dict]) -> str:
    blocks = []
    for visual in visuals:
        blocks.append(
            f"""<figure class="visual-card">
              <div class="visual-text">
                <span class="visual-kicker">{html.escape(visual["kicker"])}</span>
                <strong>{html.escape(visual["headline"])}</strong>
              </div>
              {visual_svg(visual["variant"])}
            </figure>"""
        )
    return join_lines(blocks, 14)


def render_trust_items(items: list[str]) -> str:
    return join_lines([f"<li>{html.escape(item)}</li>" for item in items], 14)


def render_site(site: dict) -> str:
    theme = site["theme"]
    return f"""<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(site["title"])}</title>
    <meta
      name="description"
      content="{html.escape(site["meta_description"])}"
    />
    <link rel="stylesheet" href="../styles.css" />
    <style>
      :root {{
        --accent: {theme["accent"]};
        --accent-deep: {theme["accent_deep"]};
        --info: {theme["info"]};
      }}
    </style>
  </head>
  <body>
    <a class="skip-link" href="#main-content">Direkt zum Inhalt</a>
    <div class="demo-banner">
      <div class="container demo-banner-inner">
        <p>{html.escape(site["demo_banner"])}</p>
        <a href="../demos/">Alle Demos</a>
      </div>
    </div>
    <header class="site-header">
      <div class="topline">
        <div class="container topline-inner">
          <p>{html.escape(site["topline"])}</p>
          <a href="tel:{html.escape(site["phone_href"])}">{html.escape(site["phone_display"])}</a>
        </div>
      </div>
      <div class="container header-row">
        <a class="brand" href="#top" aria-label="Startseite {html.escape(site["name"])}">
          <span class="brand-mark">{html.escape(site["short_name"])}</span>
          <span class="brand-copy">
            <strong>{html.escape(site["name"])}</strong>
            <small>{html.escape(site["subtitle"])}</small>
          </span>
        </a>
        <nav class="main-nav" aria-label="Hauptnavigation">
          <a href="#leistungen">Leistungen</a>
          <a href="#warum-wir">Warum wir</a>
          <a href="#faq">FAQ</a>
          <a href="#kontakt">Kontakt</a>
        </nav>
        <div class="header-actions">
          <a class="btn btn-secondary hide-mobile" href="#kontakt">{html.escape(site["secondary_cta"])}</a>
          <a class="btn btn-primary" href="#kontakt">{html.escape(site["primary_cta"])}</a>
        </div>
      </div>
    </header>
    <main id="main-content">
      <section class="hero-section" id="top">
        <div class="container hero-grid">
          <div class="hero-copy">
            <p class="eyebrow">{html.escape(site["hero_eyebrow"])}</p>
            <h1>{html.escape(site["hero_title"])}</h1>
            <p class="hero-lead">{html.escape(site["hero_lead"])}</p>
            <div class="hero-cta">
              <a class="btn btn-primary btn-large" href="#kontakt">{html.escape(site["primary_cta"])}</a>
              <a class="btn btn-secondary btn-large" href="#kontakt">{html.escape(site["secondary_cta"])}</a>
            </div>
            <ul class="trust-list" aria-label="Vertrauenselemente">
{render_trust_items(site["trust_items"])}
            </ul>
          </div>
          <aside class="hero-panel" aria-label="Leistung und Schnellkontakt">
            <div class="contact-card">
              <p class="card-label">Demo-Kontakt</p>
              <a class="phone-number" href="#kontakt">{html.escape(site["phone_display"])}</a>
              <p class="card-text">{html.escape(site["contact_card_text"])}</p>
              <div class="contact-card-actions">
                <a class="btn btn-primary" href="#kontakt">{html.escape(site["primary_cta"])}</a>
                <a class="btn btn-dark" href="#kontakt">WhatsApp Demo</a>
              </div>
            </div>
            <div class="visual-grid">
{render_visuals(site["visuals"])}
              <div class="status-card">
                <span class="status-chip">{html.escape(site["status_chip"])}</span>
                <h2>{html.escape(site["status_title"])}</h2>
                <p>{html.escape(site["status_text"])}</p>
              </div>
            </div>
          </aside>
        </div>
      </section>
      <section class="section" id="leistungen">
        <div class="container">
          <div class="section-heading">
            <p class="eyebrow">Leistungen</p>
            <h2>{html.escape(site["services_intro"])}</h2>
          </div>
          <div class="service-grid">
{render_services(site["services"])}
          </div>
        </div>
      </section>
      <section class="section section-soft" id="warum-wir">
        <div class="container why-grid">
          <div class="section-heading left-aligned">
            <p class="eyebrow">Warum wir</p>
            <h2>{html.escape(site["why_title"])}</h2>
            <p>{html.escape(site["why_text"])}</p>
          </div>
          <div class="why-cards">
{render_why_items(site["why_items"])}
          </div>
        </div>
      </section>
      <section class="section" id="vertrauen">
        <div class="container">
          <div class="demo-review-header">
            <span class="demo-badge">Demo</span>
            <p>{html.escape(site["reviews_intro"])}</p>
          </div>
          <div class="demo-reviews">
{render_reviews(site["reviews"])}
          </div>
        </div>
      </section>
      <section class="section section-soft" id="faq">
        <div class="container faq-grid">
          <div class="section-heading left-aligned">
            <p class="eyebrow">FAQ</p>
            <h2>Typische Fragen vor der Anfrage.</h2>
          </div>
          <div class="faq-list">
{render_faqs(site["faqs"])}
          </div>
        </div>
      </section>
      <section class="section contact-section" id="kontakt">
        <div class="container contact-grid">
          <div class="contact-copy">
            <p class="eyebrow">Kontakt</p>
            <h2>{html.escape(site["contact_title"])}</h2>
            <p>{html.escape(site["contact_text"])}</p>
            <div class="contact-stack">
              <a class="contact-box" href="#">
                <span class="contact-title">{html.escape(site["contact_box_1_title"])}</span>
                <strong>{html.escape(site["phone_display"])}</strong>
                <small>{html.escape(site["contact_box_1_text"])}</small>
              </a>
              <a class="contact-box" href="#">
                <span class="contact-title">{html.escape(site["contact_box_2_title"])}</span>
                <strong>Nachricht senden</strong>
                <small>{html.escape(site["contact_box_2_text"])}</small>
              </a>
            </div>
          </div>
          <form class="contact-form" id="lead-form">
            <div class="form-intro">
              <h3>Demo-Anfrage</h3>
              <p>{html.escape(site["form_intro"])}</p>
            </div>
            <label for="name">Name</label>
            <input id="name" name="name" type="text" placeholder="Ihr Name" required />
            <label for="phone">Telefon</label>
            <input id="phone" name="phone" type="tel" placeholder="Ihre Telefonnummer" required />
            <label for="message">Anliegen</label>
            <textarea id="message" name="message" rows="5" placeholder="{html.escape(site["form_placeholder"])}" required></textarea>
            <button class="btn btn-primary btn-full" type="submit">Demo-Anfrage absenden</button>
            <p class="form-status" id="form-status" role="status" aria-live="polite"></p>
          </form>
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <div class="container footer-grid">
        <div>
          <strong>{html.escape(site["name"])}</strong>
          <p>Demo-Landingpage für lokale Leads.</p>
        </div>
        <div>
          <strong>Status</strong>
          <p>Demo</p>
        </div>
        <div>
          <strong>Region</strong>
          <p>Düsseldorf</p>
        </div>
        <div>
          <strong>Mehr</strong>
          <p><a href="../demos/">Demo-Hub</a></p>
        </div>
      </div>
    </footer>
    <div class="sticky-mobile-cta">
      <a href="#kontakt">{html.escape(site["primary_cta"])}</a>
      <a href="../demos/">Alle Demos</a>
    </div>
    <script>
      document.getElementById("lead-form").addEventListener("submit", function (event) {{
        event.preventDefault();
        document.getElementById("form-status").textContent = "{html.escape(site["form_success"])}";
      }});
    </script>
  </body>
</html>
"""


def render_hub(sites: list[dict]) -> str:
    cards = []
    cards.append(
        """<article class="hub-card">
              <h3>Dachdecker Neuss</h3>
              <p>Akute Schäden, Sturmschaden, Dachreparatur und lokale Soforthilfe.</p>
              <a class="text-link" href="../">Demo öffnen</a>
            </article>"""
    )
    for site in sites:
      cards.append(
          f"""<article class="hub-card">
              <h3>{html.escape(site["name"])}</h3>
              <p>{html.escape(site["hub_excerpt"])}</p>
              <a class="text-link" href="../{html.escape(site["slug"])}/">Demo öffnen</a>
            </article>"""
      )
    return f"""<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Demo-Hub | Lokale Lead-Landingpages</title>
    <meta
      name="description"
      content="Übersicht aller Demo-Landingpages für lokale Dienstleister und High-Ticket-Nischen."
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <a class="skip-link" href="#main-content">Direkt zum Inhalt</a>
    <div class="demo-banner">
      <div class="container demo-banner-inner">
        <p>Demo-Hub für lokale Lead-Landingpages</p>
        <a href="../">Dachdecker-Demo öffnen</a>
      </div>
    </div>
    <main id="main-content">
      <section class="hero-section">
        <div class="container">
          <div class="section-heading">
            <p class="eyebrow">System statt Zufall</p>
            <h1>Ein Conversion-Framework, mehrere lokale Nischen.</h1>
            <p>
              Jede Seite ist als direkte Lead-Landingpage gedacht: klare Hilfe,
              lokale Relevanz, starke CTA-Flächen und einfache Kontaktaufnahme.
            </p>
          </div>
          <div class="hub-grid">
{join_lines(cards, 12)}
          </div>
        </div>
      </section>
    </main>
  </body>
</html>
"""


def write_generated_site(site: dict) -> None:
    target_dir = ROOT / site["slug"]
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "index.html").write_text(render_site(site), encoding="utf-8")


def main() -> None:
    sites = load_sites()
    for site in sites:
        write_generated_site(site)
    DEMO_HUB_DIR.mkdir(parents=True, exist_ok=True)
    (DEMO_HUB_DIR / "index.html").write_text(render_hub(sites), encoding="utf-8")
    print(f"Generated {len(sites)} demo pages and updated demos/index.html")


if __name__ == "__main__":
    main()
