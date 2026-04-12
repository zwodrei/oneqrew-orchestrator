---
title: EXTRAGROUP
brand-guide: https://qrew.one/extragroup-brand-guide
logos: https://qrew.one/extragroup-logos
---

# extragroup GmbH -- GPT-Wissensartefakt

---

## BLOCK 1 -- EXECUTIVE SUMMARY

**Unternehmen:** extragroup GmbH
**Website:** https://www.extragroup.de
**Teil von:** OneQrew-Gruppe
**Standort:** Münster, NRW (D-48149)

### Kurzbeschreibung
extragroup GmbH ist ein spezialisierter Anbieter von CAD- und ERP-Branchensoftware für das Holz- und Innenausbauhandwerk. Das Kernprodukt interiorcad powered by Vectorworks adressiert Tischler, Schreiner, Laden- und Messebauer. Ergänzt wird es durch die Integration in das ERP-System P Corpora von PinnCalc sowie durch den autorisierten Vertrieb von Vectorworks-Branchenversionen (Architektur, Landschaft, Spotlight) im nördlichen NRW / südwestlichen Niedersachsen.

### Positionierung
„CAD und ERP aus einer Hand“ – Vollständige digitale Prozesskette von der Konstruktion über die Arbeitsvorbereitung bis zur CNC-Fertigung, spezialisiert auf die Losgröße-Eins-Fertigung im Handwerk.

### Wichtigste Differenzierungsmerkmale
- Tiefste Branchenspezialisierung auf Tischler / Schreiner (kein Generalisten-CAD)
- CAD + ERP aus einer Hand (interiorcad + corpora (PinnCalc))
- Integrierte Beschläge von 20+ führenden Herstellern
- Direkter NC-Export in alle gängigen CNC-Systeme
- Abo-Modell mit jährlichen Updates und Planungssicherheit
- Eigene Lernplattform + Seminare + E-Learning-Kurse
- Vectorworks-Plattform als technologische Basis
- Verankerung im Ausbildungsbereich (Schulversionen, Berufsschulen)

### Wichtigste Produkte / Lösungen
1. **interiorcad Starter** – Einstiegspaket CAD
2. **interiorcad Worker** – Vollpaket CAD (Kern)
3. **interiorcad Expert** – Erweiterung für Messebauer (neu 2026)
4. **Vectorworks Architektur / Landschaft / Spotlight** (Reseller)

### Wichtigste Zielgruppen

> **[ICP-Referenz: Wird durch Buyer-Persona-Dokument ersetzt]**

### Wichtigste Branchen / Gewerke

**Cluster: Dach & Holz** — Gewerke:

- Dachdeckerei
- Möbeltischlerei / Schreinerei
- Bautischlerei
- Zimmerei
- Fensterbau
- Fensterhandel
- Innenausbau
- Messebau
- Ladenbau
- Modellbau
- Boots- / Schiffsbau

### Wichtigste Services
Einsteiger- & Aufbauseminare (Präsenz + Online), E-Learning-Videokurs, Webinare (kostenlos), Individuelle Schulungen, Support-Ticketsystem, Demo, Online-Präsentation

---


## BLOCK 2 -- JSON-WISSENSBASIS

```json
{
  "company_profile": {
    "name": "extragroup GmbH",
    "website": "https://www.extragroup.de",
    "english_site": "https://extragroup.com",
    "group": "OneQrew",
    "location": "Münster, NRW, Deutschland",
    "positioning": "CAD und ERP aus einer Hand für Tischler, Schreiner, Laden- und Messebauer",
    "core_claim": "CAD und ERP. Für Tischler, Schreiner, Laden- und Messebauer.",
    "sub_claim": "Mit Tischlersoftware die du liebst",
    "vectorworks_partner": "Autorisierter Fachhändler ComputerWorks GmbH, Gebiet: nördliches NRW / südwestliches Niedersachsen",
    "confidence": "hoch"
  },
  "products": [
    {
      "id": "interiorcad_starter",
      "name": "interiorcad Starter",
      "category": "CAD-Branchensoftware",
      "tier": 1,
      "description": "Einstiegspaket für interiorcad powered by Vectorworks mit eingeschränktem Funktionsumfang",
      "target_audience": ["Einsteiger", "kleinere Betriebe"],
      "license_model": "Abo",
      "confidence": "explizit belegt"
    },
    {
      "id": "interiorcad_worker",
      "name": "interiorcad Worker",
      "category": "CAD-Branchensoftware",
      "tier": 2,
      "description": "Vollständiges CAD-Kernpaket für Tischler und Schreiner. Konstruktion von Korpusmöbeln, Massivholz, NC-Export, ERP-Integration.",
      "key_functions": [
        "Korpusmöbel 3D",
        "Bauteil 3D",
        "Sockel 3D",
        "Integrierte Beschläge (Blum, Häfele, Hettich, Grass, Lamello, Simonswerk, FESTOOL)",
        "NC-Export (Maestro, woodWOP, Xilog Plus, bSolid, F4Integrate, NC-Hops, Wood Flash, Vectric VCarve)",
        "Stücklisten-Export (productionManager, AK-Soft, Swiss-Soft, Triviso ERP)",
        "Vectorworks Package Manager",
        "Renderworks",
        "Massivholz-Unterstützung",
        "interiorcad Viewer"
      ],
      "target_audience": ["Tischler", "Schreiner", "Ladenbauer"],
      "license_model": "Abo",
      "confidence": "explizit belegt"
    },
    {
      "id": "interiorcad_expert",
      "name": "interiorcad Expert",
      "category": "CAD-Branchensoftware (Erweiterung)",
      "tier": 3,
      "description": "Neues Paket ab interiorcad 2026 F2. Kombiniert interiorcad mit Vectorworks Spotlight-Funktionen für Messebauer.",
      "target_audience": ["Messebauer"],
      "license_model": "Abo",
      "since": "interiorcad 2026 F2",
      "confidence": "explizit belegt"
    },
    {
      "id": "vectorworks_architektur",
      "name": "Vectorworks Architektur",
      "category": "CAD-Branchensoftware (Reseller)",
      "description": "BIM-/Architektur-CAD von ComputerWorks. extragroup ist autorisierter Fachhändler.",
      "target_audience": ["Architekten"],
      "confidence": "explizit belegt"
    },
    {
      "id": "vectorworks_landschaft",
      "name": "Vectorworks Landschaft",
      "category": "CAD-Branchensoftware (Reseller)",
      "description": "Landschafts- und Freiraumplanung.",
      "target_audience": ["Landschaftsplaner"],
      "confidence": "explizit belegt"
    },
    {
      "id": "vectorworks_spotlight",
      "name": "Vectorworks Spotlight",
      "category": "CAD-Branchensoftware (Reseller)",
      "description": "Veranstaltungs- und Bühnentechnik.",
      "target_audience": ["Veranstaltungstechniker"],
      "confidence": "explizit belegt"
    }
  ],
  "services": [
    {
      "id": "seminar_einstieg_praesenz",
      "name": "interiorcad Einsteigerseminar (Präsenz)",
      "category": "Schulung",
      "format": "Präsenz, Münster",
      "price": "799 EUR zzgl. MwSt.",
      "phase": "Onboarding",
      "target_audience": ["Neueinsteiger"],
      "related_products": ["interiorcad_starter", "interiorcad_worker"]
    },
    {
      "id": "seminar_einstieg_online",
      "name": "interiorcad Online-Einsteigerseminar",
      "category": "Schulung",
      "format": "Online (Live)",
      "price": "799 EUR zzgl. MwSt.",
      "phase": "Onboarding",
      "target_audience": ["Neueinsteiger"],
      "related_products": ["interiorcad_starter", "interiorcad_worker"]
    },
    {
      "id": "seminar_aufbau",
      "name": "interiorcad Aufbauseminar (Präsenz / Online)",
      "category": "Schulung",
      "format": "Präsenz Münster oder Online",
      "price": "799 EUR zzgl. MwSt.",
      "phase": "Mid-Use",
      "target_audience": ["Bestehende Anwender mit Grundkenntnissen"],
      "related_products": ["interiorcad_worker", "interiorcad_expert"]
    },
    {
      "id": "individuelle_schulung",
      "name": "Individuelle Schulung",
      "category": "Schulung / Consulting",
      "format": "Präsenz oder Online, maßgeschneidert",
      "price": "auf Anfrage",
      "phase": "Onboarding oder laufender Betrieb",
      "target_audience": ["Betriebe mit individuellem Bedarf"]
    },
    {
      "id": "elearning_einsteiger",
      "name": "E-Learning Einsteigerkurs interiorcad",
      "category": "E-Learning",
      "format": "Self-paced Video-Kurs, 76 Lektionen, 14:24h",
      "price": "199,99 EUR inkl. MwSt.",
      "access_duration": "1 Jahr",
      "platform": "lernen.extragroup.de",
      "phase": "Onboarding / Pre-Purchase",
      "target_audience": ["Auszubildende", "Dozenten", "Selbstlerner"],
      "related_products": ["interiorcad_starter", "interiorcad_worker"]
    },
    {
      "id": "webinare",
      "name": "Webinare (kostenlos)",
      "category": "Webinar / Pre-Sales",
      "format": "Online, Live, kostenlos",
      "price": "0 EUR",
      "phase": "Awareness / Pre-Purchase / Retention",
      "target_audience": ["Interessenten", "Bestandskunden"]
    },
    {
      "id": "support_ticket",
      "name": "Support-Ticket",
      "category": "After-Sales Support",
      "format": "Online-Ticketsystem",
      "platform": "support.extragroup.de",
      "phase": "Post-Purchase",
      "target_audience": ["Bestandskunden interiorcad"]
    },
    {
      "id": "demo_bestellung",
      "name": "Demo bestellen",
      "category": "Pre-Sales",
      "format": "Online-Bestellung",
      "phase": "Consideration",
      "target_audience": ["Interessenten"]
    },
    {
      "id": "online_praesentation",
      "name": "Online-Präsentation vereinbaren",
      "category": "Sales-Beratung",
      "format": "Terminbuchung / Online-Meeting",
      "phase": "Decision",
      "target_audience": ["Interessenten"]
    },
    {
      "id": "vw_seminare",
      "name": "Vectorworks Seminare (Architektur / Landschaft)",
      "category": "Schulung (Reseller)",
      "format": "Präsenz Münster oder Online",
      "price": "435 EUR zzgl. MwSt. (Schüler: 59 EUR)",
      "phase": "Onboarding / Weiterbildung",
      "target_audience": ["Architekten", "Landschaftsplaner", "Studierende"]
    }
  ],
  "audiences": [
    {
      "id": "tischler_schreiner_betrieb",
      "name": "Tischler-/Schreinerbetrieb (Inhaber/Meister)",
      "role": "Buyer + Nutzer",
      "pain_points": ["Mehrere Softwaretools", "Probemontagen kosten Zeit", "Individuelle Fertigung schwer planbar"],
      "desired_outcomes": ["CAD+ERP aus einer Hand", "Probemontagen entfallen", "Fertigungspräzision"],
      "primary_products": ["interiorcad_worker"]
    },
    {
      "id": "ladenbauer",
      "name": "Ladenbauer / Shop-Fitter",
      "role": "Buyer + Nutzer",
      "pain_points": ["Individuelle Projektvielfalt", "Kundenpräsentation ohne Rendering schwierig"],
      "desired_outcomes": ["Visualisierung als Vertriebstool", "Schnelle Konstruktionsanpassung"],
      "primary_products": ["interiorcad_worker"]
    },
    {
      "id": "messebauer",
      "name": "Messebauer",
      "role": "Buyer + Nutzer",
      "pain_points": ["Temporäre Sonderkonstruktionen", "Spotlight-Funktionen benötigt"],
      "primary_products": ["interiorcad_expert"]
    },
    {
      "id": "auszubildende",
      "name": "Auszubildende / Schüler",
      "role": "Nutzer (Schulversion)",
      "primary_products": ["interiorcad_starter"],
      "primary_services": ["elearning_einsteiger"]
    },
    {
      "id": "dozenten",
      "name": "Dozenten / Berufsschullehrer",
      "role": "Multiplikator + Nutzer",
      "primary_products": ["interiorcad_starter"],
      "primary_services": ["elearning_einsteiger"]
    },
    {
      "id": "berufsschulen",
      "name": "Berufsschulen / Bildungseinrichtungen",
      "role": "Institutioneller Buyer",
      "primary_products": ["interiorcad_starter"]
    },
    {
      "id": "gruender",
      "name": "Existenzgründer im Holzhandwerk",
      "role": "Buyer",
      "note": "Gründer-Stipendium: interiorcad + Corpora kostenlos für 24 Monate",
      "primary_products": ["interiorcad_worker"]
    }
  ],
  "industries": [
    "Tischler- / Schreinerhandwerk",
    "Ladenbau / Shop-Fitting",
    "Messebau",
    "Innenausbau",
    "Aus- und Weiterbildung (Holztechnik)",
    "Architektur (Reseller)",
    "Landschaftsarchitektur (Reseller)",
    "Veranstaltungstechnik (Reseller)"
  ],
  "trades": [
    "Tischler",
    "Schreiner",
    "Ladenbauer",
    "Messebauer",
    "Innenausbauer",
    "Holztechnik-Dozent / Ausbilder",
    "Architekt (Reseller-Segment)",
    "Landschaftsplaner (Reseller-Segment)",
    "Veranstaltungstechniker (Reseller-Segment)"
  ],
  "use_cases": [
    "Küchenmöbel- und Korpusmöbelplanung",
    "Massivholz-Möbelkonstruktion",
    "Ladeneinrichtungsplanung (Theken, Regale, Shopdesign)",
    "Messebau-Konstruktion (Expert-Paket)",
    "CNC-Fertigung vorbereiten (NC-Export)",
    "Arbeitsvorbereitung (AV) und Stücklisten",
    "Photorealistisches Rendering für Kundenpräsentation",
    "Dachschrägen-Einbaumöbel",
    "Gesellen- und Meisterstückzeichnung (Ausbildung)",
    "3D-Laseraufmaß-Integration",
    "BIM-Raumplanung (Wände, Fenster, Türen, Treppen)"
  ],
  "references": [
    {
      "name": "Till Hubl",
      "industry": "Tischler/Schreiner (DE)",
      "format": "Video-Testimonial",
      "key_quote": "Möbel, die ich baue, bau ich eigentlich schon vorher am Computer",
      "outcome": "Probemontagen entfallen weitestgehend",
      "products": ["interiorcad_worker"]
    },
    {
      "name": "Daniel Zangger",
      "industry": "Ladenbau / Messebau (CH)",
      "format": "Video-Testimonial",
      "key_quote": "Kunden Emotionen überbringen",
      "outcome": "Nahtlose 3D-Laseraufmaß-Integration; Visualisierung als Vertriebstool",
      "products": ["interiorcad_worker", "interiorcad_expert"]
    },
    {
      "name": "P.M., Aachen / A.G., Warendorf / A.S., Dortmund",
      "industry": "Tischlerausbildung",
      "format": "Text-Testimonials",
      "outcome": "Positives selbstständiges Lernen mit E-Learning-Kurs",
      "services": ["elearning_einsteiger"]
    }
  ],
  "brand_language": {
    "main_claim": "CAD und ERP. Für Tischler, Schreiner, Laden- und Messebauer.",
    "sub_claim": "Mit Tischlersoftware die du liebst",
    "abo_claim": "Immer zuverlässig, jederzeit planbar, stets aktuell",
    "product_endorsement": "interiorcad powered by Vectorworks",
    "key_nouns": ["Tischler", "Schreiner", "Möbel", "Konstruktion", "Fertigung", "Rendering", "Workflow", "Losgröße Eins", "Abo", "Update"],
    "key_verbs": ["planen", "konstruieren", "exportieren", "ableiten", "bauen", "lernen", "überbringen", "abonnieren"],
    "key_adjectives": ["zuverlässig", "planbar", "aktuell", "einfach", "individuell", "professionell"],
    "cta_patterns": ["Jetzt einfach Abo!", "Demo bestellen", "Online-Präsentation vereinbaren", "Jetzt anmelden", "Ticket anlegen"]
  },
  "tone_of_voice": {
    "address_form": "Du (informell, direkt)",
    "formality": "niedrig-mittel",
    "emotionality": "moderat, punktuell",
    "technical_depth": "hoch (setzt Fachvorwissen voraus)",
    "pace": "kompakt, keine langen Erklär-Texte",
    "character": "bodenständig, handwerklich-kollegial, verlässlich"
  },
  "brand_glossary": {
    "interiorcad": "Primäres CAD-Produkt; immer mit Zusatz powered by Vectorworks bei Vollnennung",
    "Losgröße Eins": "Schlüsselbegriff für individuelle Serienfertigung im Handwerk",
    "Arbeitsvorbereitung (AV)": "Fachbegriff für fertigungsvorbereitende Prozesse",
    "NC-Export": "Export an CNC-Maschinen; nicht CNC-Schnittstelle",
    "Renderworks": "Rendering-Modul innerhalb interiorcad (Vectorworks-Terminologie)",
    "Vectorworks Package Manager": "Bibliotheksverwaltung; bei Beschlagsbibliotheken verwenden"
  },
  "sales_marketing_qa": [
    {
      "q": "Was ist der Unterschied zwischen interiorcad Worker und Expert?",
      "a": "interiorcad Expert enthält zusätzlich Vectorworks Spotlight-Funktionen für Messebauer. Es ist seit interiorcad 2026 F2 verfügbar. Worker ist das Standard-Vollpaket für Tischler, Schreiner und Ladenbauer.",
      "confidence": "explizit belegt"
    },
    {
      "q": "Gibt es interiorcad auch als Kauf-Lizenz?",
      "a": "Die Website bewirbt primär das Abo-Modell. Ob Kauf-Lizenzen noch erhältlich sind, ist auf der Website nicht explizit angegeben.",
      "confidence": "unklar"
    },
    {
      "q": "Welche CNC-Systeme werden unterstützt?",
      "a": "Maestro, woodWOP, Xilog Plus, bSolid, F4Integrate, NC-Hops, Wood Flash, Vectric VCarve. Hersteller: HOMAG, Weeke, Biesse, HOLZ-HER, SCM, Felder, IMA, Ganner.",
      "confidence": "explizit belegt"
    },
    {
      "q": "Was kostet das interiorcad Einsteigerseminar?",
      "a": "799 EUR zzgl. MwSt., sowohl als Präsenz- als auch als Online-Variante.",
      "confidence": "explizit belegt"
    },
    {
      "q": "Gibt es kostenlose Einstiegsmöglichkeiten?",
      "a": "Ja: kostenlose Webinare, kostenlose Schülerversion, kostenlose Dozentenversion, Demo-Bestellung. Gründer-Stipendium: interiorcad + Corpora kostenlos für 24 Monate.",
      "confidence": "explizit belegt"
    }
  ],
  "source_index": [
    {"id": "S1", "url": "https://www.extragroup.de/", "title": "Startseite"},
    {"id": "S2", "url": "https://www.extragroup.de/interiorcad/interiorcad-highlights", "title": "interiorcad Highlights"},
    {"id": "S3", "url": "https://www.extragroup.de/vectorworks/branchenversionen/", "title": "Vectorworks Branchenversionen"},
    {"id": "S4", "url": "https://www.extragroup.de/interiorcad/hilfesupport/seminare-und-schulungen/", "title": "Seminare und Schulungen"},
    {"id": "S5", "url": "https://www.extragroup.de/interiorcad/hilfesupport/webinare/", "title": "Webinare"},
    {"id": "S6", "url": "https://www.extragroup.de/xg/team/", "title": "Team"},
    {"id": "S7", "url": "https://www.extragroup.de/interiorcad/updates/historie/", "title": "Updates / Historie"},
    {"id": "S8", "url": "https://www.extragroup.de/interiorcad/hilfesupport/systemvoraussetzungen/", "title": "Systemvoraussetzungen"},
    {"id": "S9", "url": "https://www.extragroup.de/vectorworks/updates/vectorworks-service-select/", "title": "Vectorworks Service Select"},
    {"id": "S10", "url": "https://www.extragroup.de/interiorcad/schulen/", "title": "Schulen / Schülerversion"},
    {"id": "S11", "url": "https://lernen.extragroup.de/lp/einsteiger-kurs-interiorcad-schulen/", "title": "E-Learning Einsteigerkurs"},
    {"id": "S12", "url": "https://www.extragroup.de/vectorworks/seminare-und-schulungen/", "title": "Vectorworks Seminare"}
  ],
  "gaps_and_unknowns": [
    "Lizenzpreise interiorcad: nicht öffentlich auf Website",
    "Updateseminar: existiert laut Abo-Text, aber keine eigene Seminarseite",
    "Vectorworks Spotlight-Schulungen: kein Schulungsangebot trotz Vertrieb",
    "Support-Konditionen für Kauf-Lizenzen: unklar",
    "Internationale Reichweite interiorcad: unklar (Testimonial CH vorhanden)",
    "Brand Guide: nicht vorhanden",
    "Gründer-Stipendium: Konditionen nur teilweise bekannt"
  ],
  "final_confidence": {
    "products": "hoch (interiorcad)",
    "services": "hoch",
    "audiences": "hoch",
    "brand_language": "hoch",
    "references": "mittel (keine strukturierten Cases mit Kennzahlen)",
    "overall": "mittel-hoch"
  }
}
```

---

## BLOCK 3 -- MARKEN-GLOSAR

| Begriff | Definition | Kategorie | Empfohlene Verwendung | Verwandte Begriffe | Beispiel |
|---|---|---|---|---|---|
| **interiorcad** | Primäres CAD-Branchenprodukt von extragroup auf Vectorworks-Basis | Produktname | Vollform: „interiorcad powered by Vectorworks“; Kurzform: „interiorcad“ | Vectorworks, CAD | „Mit interiorcad planst du Möbel in 3D.“ |
| **powered by Vectorworks** | Produktzusatz / Endorsement | Branding-Element | Bei erster Nennung immer ausschreiben | Vectorworks | „interiorcad powered by Vectorworks“ |
| **Losgröße Eins** | Individuelle Einzelfertigung; jedes Möbel ist ein Unikat | Fachbegriff / USP | Als Differenzierungsmerkmal einsetzen | Einzelfertigung | „Für die Losgröße Eins entwickelt.“ |
| **Arbeitsvorbereitung (AV)** | Fertigungsvorbereitende Prozesse: Stücklisten, Bauteilableitung, CNC-Export | Fachbegriff | In technischer Kommunikation und bei ERP-Kontext | Stückliste, NC-Export | „Von der Konstruktion direkt in die AV.“ |
| **NC-Export** | Datenausgabe für CNC-Maschinen | Fachbegriff | Nicht „CNC-Schnittstelle“ verwenden | CNC, woodWOP | „NC-Export für deine HOMAG-Maschine.“ |
| **Renderworks** | Photorealistisches Rendering-Modul | Produktfeature | Bei Visualisierungskontext einsetzen | Rendering, 3D | „Renderworks liefert fotorealistische Ansichten.“ |
| **Abo** | Lizenzmodell für interiorcad; jährlich, inkl. Updates und Support | Geschäftsmodell | Positiv: Einfachheit und Planbarkeit betonen | Update, Lizenz | „Immer aktuell mit dem interiorcad Abo.“ |
| **Probemontage** | Physischer Testaufbau vor Montage; durch interiorcad reduzierbar | Branchenbegriff / Pain-Point | Als negativen Referenzpunkt nutzen | Testaufbau, Fehlerkosten | „Probemontagen gehören der Vergangenheit an.“ |

---

## BLOCK 4 -- TONE OF VOICE GUIDE

### Markencharakter
extragroup spricht wie ein erfahrener Handwerkskollege, der zufällig auch ein Software-Profi ist. Bodenständig, verlässlich, direkt – kein Startup-Buzzword-Sprech, kein Corporate-Geschwurbel.

### Sprachstil
- **Du-Ansprache** durchgehend (nie „Sie“)
- Kurze, aktive Sätze
- Fachbegriffe werden verwendet, nicht erklärt
- Substantivierungen vermeiden; lieber Verben
- Keine Übertreibungen oder Superlative ohne Beleg

### Satzlänge / Satzrhythmus
- Headlines: max. 5–7 Wörter, oft ohne Verb
- Fließtext: 1–3 Sätze pro Absatz
- Bewusste Verknappung als Stilmittel: „CAD und ERP.“ (Punkt als Betonung)

### Fachliche Tiefe
- **Marketing-Layer:** mittel – nutzenorientiert
- **Produkt-Layer:** hoch – exakte Funktionsnamen
- **Support/Doku-Layer:** sehr hoch – Release Notes, Specs

### Tonalität nach Kanal
| Kanal | Tonalität |
|---|---|
| Website / Marketing | Du, direkt, aktiv |
| Seminare / Schulungen | Du, einladend, strukturiert |
| Support | Du, sachlich, lösungsorientiert |
| Testimonials | Authentische Handwerkerstimmen, unpoliert |

### Do's
- Du-Form konsequent
- Fachbegriffe aus dem Handwerk (Korpus, NC, AV, Stückliste)
- Kurze, präzise Nutzenaussagen
- Konkrete Produktnamen nennen
- Verben statt Substantivierungen
- Testimonials als sozialen Beweis einsetzen

### Don'ts
- „Sie“-Ansprache
- Marketing-Floskeln: „innovativ“, „ganzheitlich“, „zukunftsorientiert“
- Englische Buzzwords ohne Notwendigkeit
- Lange erklärende Texte ohne Struktur
- Übertriebene Emotionalität („revolutionär“, „game-changing“)
- Produktnamen falsch schreiben: immer „interiorcad“ (klein)

### Beispiel-Claims
- „CAD und ERP. Für Tischler, Schreiner, Laden- und Messebauer.“
- „Mit Tischlersoftware die du liebst.“
- „Immer zuverlässig, jederzeit planbar, stets aktuell.“
- „Jetzt einfach Abo!“

### Beispiel-Ad-Copy
> **interiorcad. Dein Möbel. Dein CNC. Dein Abo.**
> Plane, konstruiere und exportiere – alles in einer Software. interiorcad powered by Vectorworks ist die CAD-Lösung für Tischler, die keine Kompromisse machen. Jetzt Demo bestellen.

### Beispielantwort GPT (markenkonform)
> **Frage:** „Was macht interiorcad besonders?“
> **Antwort:** „interiorcad powered by Vectorworks ist die einzige CAD-Software, die speziell für Tischler, Schreiner und Ladenbauer entwickelt wurde. Du konstruierst Möbel in 3D, leitest Bauteile und Stücklisten automatisch ab und exportierst direkt an deine CNC-Maschine. Beschläge von Blum, Häfele, Hettich und Co. sind bereits integriert.“

---

## BLOCK 5 -- GPT-READY INSTRUCTIONS

```
# SYSTEM INSTRUCTIONS – extragroup GPT

## Über das Unternehmen
Du bist ein spezialisierter Assistent für die extragroup GmbH (https://www.extragroup.de),
Anbieter von CAD- und ERP-Branchensoftware für Tischler, Schreiner, Laden- und Messebauer.
Das Kernprodukt ist interiorcad powered by Vectorworks.
Ergänzendes ERP-Produkt: P Corpora (PinnCalc).
extragroup ist Teil der OneQrew-Gruppe, Standort Münster.

## Wie du antworten sollst
- Antworte auf Deutsch, in Du-Form, direkt und fachlich präzise.
- Setze Fachkenntnis der Zielgruppe voraus (Tischler, Schreiner, Ladenbauer).
- Nutze kurze Sätze und aktive Verben.
- Keine Marketing-Floskeln, keine Anglizismen ohne Notwendigkeit.
- Trenne klar: Was ist eine Funktion? Was ist ein Nutzen? Was ist ein USP?

## Bevorzugte Begriffe
- "interiorcad powered by Vectorworks" (Vollform) oder "interiorcad" (Kurzform)
- "NC-Export" (nicht "CNC-Schnittstelle")
- "Arbeitsvorbereitung (AV)" (nicht "Produktionsvorbereitung")
- "Abo" (nicht "Abonnement" oder "Subscription")
- "Losgröße Eins" (als USP-Begriff)

## Zu vermeidende Begriffe
- "Sie"-Ansprache
- "innovativ", "ganzheitlich", "zukunftsorientiert", "revolutionär"
- "game-changing", "cutting-edge"
- "InteriorCAD", "Interiorcad" (immer "interiorcad")

## Umgang mit Unsicherheiten
- Wenn du eine Information nicht sicher belegen kannst:
  "Das ist mir nicht sicher bekannt – bitte direkt bei extragroup nachfragen."
- Plausible Ableitungen kennzeichnen:
  "Das lässt sich ableiten, ist aber nicht explizit bestätigt."
- Erfinde keine Preise, Produktfeatures oder Kundennamen.

## Unterscheidung Funktion / Nutzen / USP
- Funktion: Was das Produkt technisch tut. (z.B. "NC-Export in woodWOP")
- Nutzen: Was der Anwender gewinnt. (z.B. "Du sparst dir den manuellen Datenexport.")
- USP: Was kein anderes Produkt so bietet. (z.B. "Tiefste Branchenspezialisierung")

## Bei fehlender Evidenz
- Antworte nicht mit Vermutungen.
- Verweise auf: Demo bestellen (https://www.extragroup.de/demo-bestellen/)
  oder Online-Präsentation (https://www.extragroup.de/online-praesentation/)
```
