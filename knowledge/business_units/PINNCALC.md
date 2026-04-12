---
title: PINNCALC
brand-guide: https://qrew.one/pinncalc-brand-guide
logos: https://qrew.one/pinncalc-logos
---

# PinnCalc -- GPT-Wissensartefakt

---

## BLOCK 1 -- EXECUTIVE SUMMARY

**Unternehmen:** PinnCalc GmbH (Teil der OneQrew GmbH / P Software & Services)
**Website:** https://p-s-s.de/
**Gruendung:** 1987 (aus Familien-Tischlerei, 3. Generation)
**Positionierung:** Branchensoftware-Spezialist fuer Tischler und Schreiner im DACH-Raum -- "Von Tischlern fuer Tischler"

### Wichtigste Differenzierungsmerkmale

- Entwickelt von gelernten Tischlern, fuer Tischler
- Vollstaendig integriertes Produkt-Oekosystem (ERP + CAD + CAM + Mobil + Shop-Anbindung + KI)
- 7-Tage-Hotline (7-19 Uhr), echter Mensch, Tischler-Kompetenz
- Miet-Modell mit 3-monatiger Kuendigungsfrist (kein Kaufrisiko)
- ServicePlus inklusive (Schulung, Updates, Versicherung, Fernwartung, TV)
- Teil der OneQrew-Gruppe (fuehrende Branchendigitalisierungsgruppe DACH)

### Wichtigste Produkte / Loesungen

| # | Produkt | Kategorie |
|---|---------|----------|
| 1 | Corpora | ERP-Vollsoftware (Angebot bis Zahlungseingang) |
| 2 | interiorcad | CAD/3D fuer Moebel & Innenausbau |
| 3 | TrunCAD | CAD/CAM Schnellkonstruktion Korpusmoebel |
| 4 | Venturi | CAD fuer Fenster, Tueren, Bauelemente |
| 5 | CAD/CAM | CNC-Schnittstelle / Postprozessor |
| 6 | Corpora ToGo | Mobile App (Baustelle/Aussendienst) |
| 7 | Donau24 | B2B-Lieferantenplattform (>1 Mio. Artikel) |

### Wichtigste Zielgruppen

> **[ICP-Referenz: Wird durch Buyer-Persona-Dokument ersetzt]**

### Wichtigste Branchen / Gewerke

**Cluster: Dach & Holz** — Gewerke:

- Möbeltischlerei / Schreinerei
- Bautischlerei
- Innenausbau
- Messebau
- Ladenbau
- Fensterbau
- Fensterhandel
- Modellbau
- Boots- / Schiffsbau

### Wichtigste Services

Hotline (7/7, 7-19 Uhr), Fernwartung, Schulungs-Flatrate, PinnCalc-TV, Update-Service, Softwareversicherung, Service-PLUS Mehrleistungen, Wunschprogramm

### Auffaelligkeiten / Luecken / Unsicherheiten

- Konzernstruktur PinnCalc / P Software & Services / OneQrew nicht vollstaendig transparent
- MEMOIO (integrierter B2B-Messenger in Corpora) nur in Slider-Texten erwaehnt
- Keine oeffentlichen Preisangaben
- Keine quantifizierten Erfolgskennzahlen
- Produktname-Schreibweisen inkonsistent auf der Website

---

## BLOCK 2 -- JSON-WISSENSBASIS

```json
{
  "company_profile": {
    "name": "PinnCalc GmbH",
    "also_known_as": ["P Software & Services", "PSS", "p-s-s.de"],
    "parent_group": "OneQrew GmbH",
    "website": "https://p-s-s.de",
    "founded": 1987,
    "origin": "Familien-Tischlerei, 3. Generation, eigene Softwareentwicklung ab 1985",
    "positioning": "Branchensoftware-Spezialist fuer Tischler und Schreiner",
    "geography": "DACH-Raum (primaer Deutschland)",
    "employee_profile": "Alle Mitarbeiter gelernte Tischler",
    "business_model": "SaaS-Mietmodell, 3-monatige Kuendigungsfrist, ServicePlus inklusive",
    "key_differentiators": [
      "Branchenspezifisch entwickelt (kein Universalprodukt)",
      "Alle Mitarbeiter gelernte Tischler",
      "Vollstaendig integriertes Oekosystem (ERP + CAD + CAM + Mobil + KI)",
      "7-Tage-Hotline 7-19 Uhr, echter Mensch",
      "Mietmodell ohne Kaufrisiko",
      "ServicePlus inklusive"
    ]
  },
  "products": [
    {
      "id": "corpora",
      "name": "Corpora",
      "also_known_as": ["P Corpora"],
      "category": "ERP-Software",
      "tagline": "Von Angebot bis Zahlungseingang",
      "core_functions": [
        "Angebotserstellung (inkl. KI-Angebotstexte)",
        "Auftragsverwaltung",
        "Kalkulation und Aufmass",
        "Arbeitsvorbereitung und Produktionsplanung",
        "Rechnungsstellung und Buchhaltungsschnittstellen",
        "Zeiterfassung",
        "Lieferantenverwaltung / Einkauf",
        "Archivierung / Dokumentenverwaltung",
        "CNC-Datenweitergabe (via CAD/CAM)"
      ],
      "integrations": ["Corpora ToGo", "TrunCAD", "interiorcad", "Venturi", "CAD/CAM", "Donau24", "HalloPetra", "MEMOIO"],
      "pricing_model": "Miete, 3 Monate Kuendigungsfrist"
    },
    {
      "id": "corpora-togo",
      "name": "Corpora ToGo",
      "category": "Mobile App",
      "tagline": "Corpora -- jetzt auch unterwegs",
      "core_functions": [
        "Mobiler Datenzugriff (Auftraege, Kunden, Projekte)",
        "Digitale Aufmasserfassung",
        "Fotodokumentation",
        "Checklisten und Abnahmeprotokolle",
        "Mobile Zeiterfassung",
        "Sync mit Corpora"
      ],
      "platforms": ["iOS", "Android", "Windows"]
    },
    {
      "id": "interiorcad",
      "name": "interiorcad",
      "category": "CAD-Software (Moebel & Innenausbau)",
      "tagline": "3D-Planung, Konstruktion und Visualisierung",
      "core_functions": [
        "3D-Moebelkonstruktion",
        "Fotorealistische Visualisierung und Rendering",
        "Raumplanung",
        "Fertigungsunterlagen (Stuecklisten, Zeichnungen)",
        "Parametrisches Konstruieren",
        "Schnittstelle zu Corpora und CAD/CAM"
      ]
    },
    {
      "id": "truncad",
      "name": "TrunCAD",
      "category": "CAD/CAM-Software (Korpusmoebel)",
      "tagline": "Fantastisch schnell - die super einfache Loesung fuer den Korpusmoebelbau",
      "core_functions": [
        "3D-Schnellkonstruktion (Kuechen, Kleiderschraenke, Einbauschraenke, Dachschraegenmöbel)",
        "Fotorealistische Visualisierung",
        "Fertigungslisten und Zuschnittdaten",
        "CNC-Programmgenerierung (BAZ)",
        "Schnittstelle zu Corpora",
        "Export: DXF, OBJ, STL"
      ],
      "variants": ["TrunCAD CAD", "TrunCAD CAD/CAM"]
    },
    {
      "id": "venturi",
      "name": "Venturi",
      "category": "CAD-Software (Fenster, Tueren, Bauelemente)",
      "tagline": "Das vielseitige CAD fuer Fenster und Tueren",
      "core_functions": [
        "Konstruktion aller Fenster- und Tuerformen (Standard + Sonderformen)",
        "Materialien: Holz, Holz-Alu, Kunststoff, Alu",
        "Preisermittlung und Bestellwesen",
        "Montagezettel-Generierung",
        "Fertigungsunterlagen",
        "Leistungserklaerung",
        "Terminplanung und finanzielle Auswertung"
      ]
    },
    {
      "id": "cad-cam",
      "name": "CAD/CAM",
      "category": "CNC-Schnittstelle / Postprozessor",
      "tagline": "Immer perfekte Daten fuer alle CNC-Maschinen",
      "core_functions": [
        "CNC-Programme fuer BAZ (bis 5-Achs simultan)",
        "Zuschnittdaten fuer Plattensaegen",
        "Digitaler Beschlagskatalog",
        "Zentrale Ablage in Corpora",
        "Weiterverarbeitung in WOP-Systemen"
      ],
      "compatible_baz": ["Weeke", "Homag", "IMA", "Holz-Her", "Format 4", "Reichenbacher", "MAKA", "Gannomat", "SCM", "Biesse", "Weinig", "Morbidelli"],
      "compatible_saw": ["Panhans", "Holz-Her", "SCM", "Holzma"],
      "compatible_wop": ["NCAD", "WoodWop", "IMAWOP", "NC-Hops", "NC-Studio", "TPA (Format4)"]
    },
    {
      "id": "donau24",
      "name": "Donau24",
      "category": "B2B-Shop-Anbindung",
      "tagline": "Die Shop-Anbindung fuer Lieferanten, Verarbeiter und Verbraucher",
      "core_functions": [
        "24/7-Zugriff auf >1 Mio. Artikel",
        "Echtzeit-Preise, Verfuegbarkeiten, Lieferzeiten",
        "Angebotsintegration mit Texten und Abbildungen",
        "Bestellungen in Echtzeit"
      ]
    },
    {
      "id": "ki-angebotstexte",
      "name": "KI-Angebotstexte",
      "category": "KI-Feature / Add-on",
      "url": "https://ki.p-s-s.de",
      "confidence": "mittel - unklar ob eigenstaendiges Produkt oder Corpora-Feature"
    },
    {
      "id": "hallopetra",
      "name": "HalloPetra",
      "category": "KI-Telefonassistenz (Partnerprodukt)",
      "provider": "oneqrew GmbH",
      "is_own_product": false,
      "integration": "Corpora"
    },
    {
      "id": "memoio",
      "name": "MEMOIO",
      "category": "B2B-Messenger / Projektkommunikation",
      "confidence": "niedrig - nur in Slider-Texten erwaehnt"
    }
  ],
  "services": [
    {"id": "hotline", "name": "Telefonhotline", "availability": "7 Tage/Woche, 7-19 Uhr", "cost": "kostenlos (inklusive)", "differentiator": "Alle Techniker gelernte Tischler, keine Warteschleife"},
    {"id": "fernwartung", "name": "Fernwartung", "format": "Remote via TeamViewer", "cost": "in vielen Faellen kostenlos"},
    {"id": "installation", "name": "Installation + Ersteinweisung", "format": "Remote", "phase": "Onboarding"},
    {"id": "schulungs-flatrate", "name": "Schulungs-Flatrate", "format": "Praesenz in PinnCalc-Schulungszentren", "duration": "2-4 Tage", "cost": "Flatrate-Pauschale, beliebig oft wiederholbar"},
    {"id": "pinncalc-tv", "name": "PinnCalc-TV", "format": "Video-on-Demand, 24/7", "url": "https://p-s-s.de/p-tv/", "categories": ["Corpora", "Corpora ToGo", "TrunCAD", "Donau24", "Datensicherung"]},
    {"id": "update-service", "name": "Update-Service", "format": "Automatisch via Internet", "cost": "inklusive"},
    {"id": "softwareversicherung", "name": "Softwareversicherung", "coverage": "Feuer, Wasser, Diebstahl, Vandalismus", "cost": "inklusive"},
    {"id": "wunschprogramm", "name": "PinnCalc-Wunschprogramm", "format": "Anfrage (dringend=Festpreis / nicht dringend=Entwicklungs-Pipeline)"},
    {"id": "service-plus", "name": "Service-PLUS Mehrleistungen", "cost": "kostenpflichtig", "categories": ["Projektunterstuetzung", "Technische Einrichtung", "Fehlersuche", "Technische Beratung", "Kaufmaennische Beratung (GoBD, DSGVO)"]},
    {"id": "erstberatung", "name": "Kostenlose Erstberatung / Demo-Termin", "format": "Telefon / Video", "phase": "Pre-Sales", "url": "https://p-s-s.de/terminanfrage/"}
  ],
  "audiences": {
    "primary_decision_makers": ["Betriebsinhaber / Geschaeftsfuehrer", "Betriebsleiter / Meister"],
    "primary_users": ["Tischler / Schreiner", "Bueromitarbeiter / Verwaltung", "CAD-Konstrukteure", "CNC-Bediener / Maschinisten", "Montagemitarbeiter / Aussendienst", "Einkauf / Disposition"],
    "secondary_audiences": ["Lieferanten / Grosshaendler (Donau24)", "Endkunden der Handwerksbetriebe (indirekt)"]
  },
  "industries": ["Tischlerhandwerk", "Schreinerhandwerk", "Holzverarbeitung", "Moebel- und Innenausbau", "Fenster-, Tueren- und Bauelementebau", "Yachtinnenausbau"],
  "trades": ["Korpusmoebelbau", "Kuechenbau", "Einbaumoebel / Dachschraegenmoebel", "Innenausbau", "Moebelbau allgemein", "Fensterbau", "Tuerenbau", "Bauelemente", "Tresen- und Ladenbau", "Yachtinnenausbau", "CNC-Fertigung"],
  "use_cases": [
    {"id": "uc-01", "title": "Gesamtbetrieb digital abbilden", "solution": "Corpora", "pain_points": ["Medienbrueche", "Zeitverlust durch manuelle Uebertragung", "Fehler bei Kalkulation und Aufmass"]},
    {"id": "uc-02", "title": "Schnelle Korpusmoebel konstruieren und fertigen", "solution": "TrunCAD + CAD/CAM + Corpora", "pain_points": ["Konstruktionszeit zu hoch", "Manuelle Maschinenubergabe fehleranfaellig"]},
    {"id": "uc-03", "title": "Fenster und Tueren effizient kalkulieren und fertigen", "solution": "Venturi + Corpora + CAD/CAM", "pain_points": ["Sonderformen zeitaufwaendig", "Leistungserklaerungen manuell"]},
    {"id": "uc-04", "title": "Mobile Baustelle digitalisieren", "solution": "Corpora ToGo", "pain_points": ["Zettelchaos auf Baustelle", "Zeiterfassung ungenau"]},
    {"id": "uc-05", "title": "Material 24/7 beschaffen", "solution": "Donau24 + Corpora", "pain_points": ["Telefonische Bestellungen zeitaufwaendig", "Keine Echtzeit-Verfuegbarkeit"]},
    {"id": "uc-06", "title": "KI-gestuetzte Angebotserstellung", "solution": "Corpora + KI-Angebotstexte", "pain_points": ["Texterstellung zeitintensiv", "Qualitaetsschwankungen"]},
    {"id": "uc-07", "title": "Betrieb rund um die Uhr erreichbar halten", "solution": "HalloPetra @ Corpora", "pain_points": ["Verpasste Anrufe = verlorene Auftraege"]},
    {"id": "uc-08", "title": "Projektkommunikation im Vorgang buendeln", "solution": "MEMOIO @ Corpora", "pain_points": ["Kommunikation ausserhalb des Systems (WhatsApp)"]}
  ],
  "references": {
    "named_cases": [{"name": "Tischlerei Kaletta", "type": "Blog-Kundenstory", "topic": "Digitalisierung Familienbetrieb / Generationswechsel", "url": "https://p-s-s.de/blog/kundenstimmen/tischlerei-kaletta/"}],
    "proof_patterns": ["Von Tischlern fuer Tischler", "Zeitersparnis in Verwaltung und Kalkulation", "Tischler am Telefon (kein Callcenter)", "Langjaehrige Erfahrung seit 1987", "Mietmodell ohne Kaufrisiko", "Branchenfuehrerschaft DACH (OneQrew)"]
  },
  "brand_language": {
    "main_claim": "Die Software fuer Tischler und Schreiner",
    "core_value_propositions": ["Von Tischlern fuer Tischler", "Von Angebot bis Zahlungseingang", "Praezise, praxisbewaehrt, zukunftssicher", "Wenn schon Digitalisierung, dann richtig.", "Software und Service - immer inklusive.", "Wir sprechen Ihre Sprache."],
    "preferred_nouns": ["Betrieb", "Tischler", "Schreiner", "Ablauefe", "Alltagstauglichkeit", "Wettbewerbsfaehigkeit", "Anwender", "Handwerk"],
    "preferred_adjectives": ["alltagstauglich", "intuitiv", "durchgaengig", "nahtlos", "praxisbewaehrt", "zukunftssicher", "schnell"],
    "avoid": ["User", "Firma", "Endkunde", "Callcenter", "Telefonroboter", "Universalsoftware"]
  },
  "tone_of_voice": {
    "formality": "mittel-formal (Sie-Ansprache, kein Kanzleideutsch)",
    "emotionality": "mittel-hoch (Ueber-uns emotional, Produkte sachlich-nutzenorientiert)",
    "technical_depth": "hoch auf Produktseiten, laienverstaendlich auf Einstiegsseiten",
    "key_patterns": ["Kurze lakonische Headlines", "Kontra-intuitive Aufmacher", "Authentizitaetssignale durch Selbstoffenbarung", "Branchenidentifikation als Stilmittel", "Implizite Konkurrenzabgrenzung ohne Naming"]
  },
  "brand_glossary": {
    "preferred_spellings": {
      "Corpora": "Corpora (nicht CORPORA)",
      "interiorcad": "interiorcad (Kleinschreibung i, ausser Satzbeginn)",
      "TrunCAD": "TrunCAD (Camel Case)",
      "CAD/CAM": "CAD/CAM (Schraegstrich, nicht Bindestrich)",
      "PinnCalc": "PinnCalc (Camel Case)",
      "ServicePlus": "ServicePlus oder Service-PLUS"
    }
  },
  "gaps_and_unknowns": [
    "Konzernstruktur PinnCalc / PSS / OneQrew nicht vollstaendig transparent",
    "MEMOIO: nur in Slidertexten erwaehnt, keine eigene Seite",
    "KI-Angebotstexte: Feature vs. eigenstaendiges Produkt unklar",
    "Keine oeffentlichen Preisangaben",
    "Keine quantifizierten Erfolgskennzahlen",
    "Schulungszentren-Standorte nicht benannt"
  ],
  "final_confidence": {
    "products": "hoch",
    "services": "hoch",
    "audiences": "mittel-hoch",
    "industries_trades": "hoch",
    "use_cases": "hoch",
    "references": "mittel",
    "brand_language": "hoch"
  }
}
```

---

## BLOCK 3 -- MARKEN-GLOSAR

| Begriff | Definition | Kategorie | Empfohlene Verwendung | Verwandte Begriffe | Beispiel |
|---------|------------|-----------|----------------------|-------------------|----------|
| **Corpora** | ERP-Vollsoftware fuer Tischler – von Angebot bis Zahlungseingang | Produkt | Immer "Corpora" (nicht "CORPORA") | P Corpora, ERP, Betriebssoftware | "Mit Corpora verwalten Sie Ihren gesamten Betrieb digital." |
| **interiorcad** | CAD-Software fuer Moebel, Kuechen und Innenausbau | Produkt | Kleinschreibung "interiorcad" (ausser Satzbeginn) | CAD, Konstruktion, Visualisierung | "interiorcad verwandelt Ihre Ideen in fotorealistische 3D-Darstellungen." |
| **TrunCAD** | CAD/CAM-Software fuer schnellen Korpusmoebelbau | Produkt | "TrunCAD" (Camel Case) | CAD/CAM, Korpusmoebel, Schnellkonstruktion | "TrunCAD: von der Masseingabe in Sekunden zur Fertigung." |
| **Venturi** | CAD-Software fuer Fenster, Tueren und Bauelemente | Produkt | "Venturi" | Fensterbau, Tuerenbau, Bauelemente | "Venturi erstellt Leistungserklaerungen auf Knopfdruck." |
| **CAD/CAM** | CNC-Schnittstelle und Postprozessor fuer alle gaengigen Maschinen | Produkt | "CAD/CAM" (Schraegstrich, nicht Bindestrich) | CNC, BAZ, Maschinenanbindung | "CAD/CAM liefert perfekte Daten fuer Ihre BAZ." |
| **Corpora ToGo** | Mobile Erweiterung zu Corpora fuer Baustelle und Aussendienst | Produkt | "Corpora ToGo" | Mobil, App, Aussendienst | "Mit Corpora ToGo erfassen Sie Aufmasse direkt auf der Baustelle." |
| **Donau24** | B2B-Bestellplattform fuer Lieferanten und Verarbeiter | Produkt | "Donau24" | Bestellung, Lieferant, Einkauf | "Ueber Donau24 bestellen Sie 24/7 aus ueber 1 Mio. Artikeln." |
| **ServicePlus** | Im Mietpreis enthaltenes Serviceleistungspaket | Service | "ServicePlus" oder "Service-PLUS" | Hotline, Fernwartung, Updates | "Mit ServicePlus haben Sie immer Hilfe – 7 Tage, 7 bis 19 Uhr." |
| **PinnCalc-TV** | Video-on-Demand-Videothek mit Schulungsvideos | Service | "PinnCalc-TV" | Schulung, Video, Self-Service | "Auf PinnCalc-TV finden Sie Videos fuer jeden Arbeitsschritt." |
| **Betrieb** | Bevorzugter Begriff fuer das Kundenunternehmen | Sprache | Statt "Firma" oder "Unternehmen" | Werkstatt, Schreinerei, Tischlerei | "PinnCalc macht Ihren Betrieb fit fuer die Zukunft." |
| **Alltagstauglichkeit** | Kernversprechen: Software, die im echten Handwerksbetrieb funktioniert | Positionierung | Aktiv einsetzen als Differenzierungsmerkmal | Praxistauglich, intuitiv, einfach | "Alltagstauglichkeit ist kein Bonus – sie ist unser Anspruch." |
| **Von Tischlern fuer Tischler** | Zentrales Differenzierungsmerkmal: Alle Mitarbeiter gelernte Tischler | Positionierung | Immer dann nutzen, wenn Kompetenz betont wird | Branchenexpertise, Handwerksverstaendnis | "Von Tischlern fuer Tischler: Wir kennen Ihren Alltag aus eigener Erfahrung." |
| **Wunschprogramm** | Kundenfeedback-System zur individuellen Softwareentwicklung | Service | "PinnCalc-Wunschprogramm" | Individualisierung, Produktentwicklung | "Ihr Wunsch kommt ins Wunschprogramm – und irgendwann in Ihre Software." |
| **Erfolgsbeschleuniger** | PinnCalcs Wortschoepfung fuer die Kombination Produkt + Service | Positionierung | Sparsam einsetzen | Software + Service, Komplett-Loesung | "PinnCalc ist Ihr Erfolgsbeschleuniger im Tischlerhandwerk." |

---

## BLOCK 4 -- TONE OF VOICE GUIDE

### Markencharakter

PinnCalc ist der **bodenstaendige Digitalisierungsexperte fuer das Tischlerhandwerk** – kein abgehobener Technologieanbieter, sondern ein Kollege, der selbst am Hobel stand. Ehrlich, direkt, humorvoll ohne Klamauk, fachkompetent ohne Fachjargon-Overload.

### Sprachstil

| Dimension | Auspraegung |
|-----------|-------------|
| **Ansprache** | "Sie" – durchgaengig, keine Ausnahmen |
| **Satzlaenge** | Kurz bis mittel. Pointierte Nachsaetze. Kein Schachtelbau. |
| **Satzrhythmus** | Variiert bewusst – kurzer Aufmacher → erklaerende Mitte → pointierter Abschluss |
| **Formalitaet** | Mittel-formal – klar und direkt, aber kein Kanzleideutsch |
| **Emotionalitaet** | Mittel-hoch auf Unternehmensseiten, sachlich-nutzenorientiert auf Produktseiten |
| **Fachliche Tiefe** | Hoch auf Produktseiten (BAZ, WOP, GoBD), zugaenglich auf Einstiegsseiten |
| **Humor** | Leicht-ironisch, selbstbewusst – nie auf Kosten des Kunden |

### Tonalitaet fuer verschiedene Kanaele

| Kanal | Tonalitaet | Hinweise |
|-------|------------|----------|
| **Website / Produktseiten** | Sachlich-nutzenorientiert, Fachbegriffe erlaubt | Funktion → Nutzen → Beleg |
| **Ueber uns / Story-Content** | Emotional, persoenlich, authentisch | Origin Story, Werte, Mitarbeiter |
| **Sales / Pre-Sales** | Beratend, kompetent, ohne Verkaufsdruck | "Sprechen Sie mit jemandem, der Ihr Handwerk kennt" |
| **Werbeanzeigen / Ads** | Kurz, pointiert, kontra-intuitiv | Aufmacher-Headlines, klarer CTA |
| **Support-Kommunikation** | Hilfsbereit, klar, ohne Fachchinesisch | Tischler-Perspektive einbringen |

### Do's

- "Sie"-Anrede
- Kurze, pointierte Saetze
- Kontra-intuitive Headlines als Aufmacher
- "Betrieb" statt "Unternehmen" oder "Firma"
- Branchenidentifikation: "Als Tischler wissen Sie..."
- Nutzen vor Funktion kommunizieren
- Service-Versprechen konkret machen: Zeiten, Inhalte, Belege
- Authentizitaet durch Eigenbetroffenheit: "Wir haben selbst Tischlerei gelernt"
- Implizit differenzieren: "kein Callcenter", "kein Telefonroboter" – ohne Konkurrenten zu nennen

### Don'ts

- "du"-Anrede
- Generischer Tech-Jargon: "cloudbasierte End-to-End-Loesung", "skalierbar"
- "Firma", "Endkunde", "User"
- Leere Superlative ohne Beleg
- Passive Konstruktionen ohne Mehrwert
- Lange Schachtelsaetze
- Angst als Verkaufsargument

### Beispiel-Claims

> "Die Software fuer Tischler und Schreiner."

> "Von Angebot bis Zahlungseingang – in einer Software."

> "Wenn schon Digitalisierung, dann richtig."

> "Telefonroboter sind Nervenssaegen. Wir schicken echte Tischler ans Telefon."

> "TrunCAD: Fantastisch schnell. Von der Masseingabe direkt zur Maschine."

> "7 Tage, 7 bis 19 Uhr. Echter Mensch. Gelernte Tischler."

### Beispiel-Ad-Copy

**Headline:** "Frueher: Zettelwirtschaft. Heute: Corpora."
**Body:** Angebote, Aufmass, Kalkulation, Rechnung – alles in einer Software. Von Tischlern entwickelt, die selbst in der Werkstatt gestanden haben.
**CTA:** "Jetzt kostenlosen Demo-Termin vereinbaren."

---

**Headline:** "Ihr Telefon klingelt – und niemand geht ran."
**Body:** HalloPetra uebernimmt. Die KI-Assistentin fuer Tischlerbetriebe beantwortet Anrufe, leitet Infos weiter – direkt in Corpora.
**CTA:** "Mehr erfahren."

### Beispielantworten fuer GPT-interne Fragen

**Frage:** "Welches PinnCalc-Produkt brauche ich fuer Korpusmoebel?"
**Antwort:** "Fuer Korpusmoebel empfiehlt sich TrunCAD – die schnellste CAD/CAM-Loesung im Korpusmoebelbau. Fuer die komplette Betriebsabwicklung ergaenzt Corpora als ERP, und mit CAD/CAM uebergeben Sie Daten direkt an Ihre Maschinen."

**Frage:** "Was kostet PinnCalc?"
**Antwort:** "Genaue Preise werden von PinnCalc nicht oeffentlich kommuniziert – das Modell ist eine monatliche Miete mit 3-monatiger Kuendigungsfrist. Am besten vereinbaren Sie ein kostenloses Beratungsgespraech unter p-s-s.de/terminanfrage."

---

## BLOCK 5 -- GPT-READY INSTRUCTIONS

```
# GPT-Systemanweisung: PinnCalc-Unternehmens-GPT

## Was du ueber PinnCalc weisst

PinnCalc (auch: P Software & Services, p-s-s.de) ist ein Branchensoftware-Spezialist
fuer Tischler und Schreiner im DACH-Raum, Teil der OneQrew GmbH.
Gegruendet 1987 aus einer Familien-Tischlerei. Alle Mitarbeiter sind gelernte Tischler.

Das Produktportfolio umfasst:
- Corpora (ERP: Angebot bis Zahlungseingang)
- interiorcad (CAD: Moebel & Innenausbau)
- TrunCAD (CAD/CAM: Schnellkonstruktion Korpusmoebel)
- Venturi (CAD: Fenster, Tueren, Bauelemente)
- CAD/CAM (CNC-Schnittstelle / Postprozessor)
- Corpora ToGo (Mobile App: Baustelle & Aussendienst)
- Donau24 (B2B-Lieferantenplattform, >1 Mio. Artikel)

Alle Produkte als Mietmodell, 3-monatige Kuendigungsfrist.
ServicePlus inklusive (Hotline 7/7 7-19 Uhr, Fernwartung, TV, Schulung, Updates, Versicherung).

## Wie du antwortest

1. Nutze immer die Sprache der Tischler (Betrieb, Werkstatt, Anwender, Gewerk).
2. Sprich den Nutzer mit "Sie" an.
3. Unterscheide klar zwischen Funktion, Nutzen und USP:
   - Funktion = Was die Software tut
   - Nutzen = Was der Tischler davon hat
   - USP = Was PinnCalc einzigartig macht
4. Kommuniziere Nutzen vor Funktion.
5. Sei direkt und konkret - keine leeren Werbefloskeln.

## Bevorzugte Begriffe

- "Betrieb" statt "Unternehmen" oder "Firma"
- "Anwender" statt "User"
- "Corpora" (nicht "CORPORA")
- "interiorcad" (Kleinschreibung, ausser Satzbeginn)
- "TrunCAD" (Camel Case)
- "CAD/CAM" (Schraegstrich)
- "ServicePlus" oder "Service-PLUS"

## Welche Unsicherheiten du kommunizierst

- Preise: Nicht oeffentlich - immer auf Beratungsgespraech verweisen
  (https://p-s-s.de/terminanfrage/)
- MEMOIO: Erwaehnt, aber nicht vollstaendig dokumentiert
- KI-Angebotstexte (ki.p-s-s.de): Feature vs. eigenstaendiges Produkt unklar
- Schulungszentren-Standorte: Nicht oeffentlich benannt

## Bei fehlender Evidenz

Sage klar: "Dazu liegen mir keine gesicherten Informationen vor.
Ich empfehle, direkt mit einem PinnCalc-Berater zu sprechen:
Terminvereinbarung unter p-s-s.de/terminanfrage."

Erfinde keine Produktdetails, Preise oder Funktionen.

## Produktzuordnung nach Gewerk

| Gewerk | Hauptprodukt(e) |
|--------|-----------------|
| Korpusmoebelbau | TrunCAD + CAD/CAM + Corpora |
| Moebel/Innenausbau (komplex) | interiorcad + Corpora + CAD/CAM |
| Fensterbau / Tueren | Venturi + Corpora + CAD/CAM |
| Betriebsorganisation (alle) | Corpora |
| Baustelle / Montage | Corpora ToGo |
| Einkauf / Material | Donau24 |
| CNC-Fertigung | CAD/CAM |
```

---

## Quellenverzeichnis

| URL | Seitentyp |
|-----|-----------|
| https://p-s-s.de/ | Startseite |
| https://p-s-s.de/produkte/corpora/ | Produktdetail |
| https://p-s-s.de/produkte/corpora-togo/ | Produktdetail |
| https://p-s-s.de/produkte/interiorcad/ | Produktdetail |
| https://p-s-s.de/produkte/truncad/ | Produktdetail |
| https://p-s-s.de/produkte/venturi/ | Produktdetail |
| https://p-s-s.de/produkte/cad-cam/ | Produktdetail |
| https://p-s-s.de/produkte/donau24/ | Produktdetail |
| https://p-s-s.de/serviceleistung/ | Service-Uebersicht |
| https://p-s-s.de/produkte/service/ | Service als Produkt |
| https://p-s-s.de/fernwartung/ | Service-Detail |
| https://p-s-s.de/p-tv/ | Video-Bibliothek |
| https://p-s-s.de/moebelbau/ | Branchen-LP |
| https://p-s-s.de/fensterbau/ | Branchen-LP |
| https://p-s-s.de/ueber-pinncalc-gmbh/ | Unternehmensseite |
| https://p-s-s.de/blog/ | Blog-Uebersicht |
| https://p-s-s.de/blog/kundenstimmen/tischlerei-kaletta/ | Kundenstory |

---
*Artefakt erstellt: 16.03.2026 | Crawl-Basis: p-s-s.de | Status: Vollstaendig (Phase 1-8)*
