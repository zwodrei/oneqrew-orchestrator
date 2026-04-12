---
title: INFLEET
brand-guide: https://qrew.one/infleet-brand-guide
logos: https://qrew.one/infleet-logos
---

# INFLEET -- GPT-Wissensartefakt

---

## BLOCK 1 -- EXECUTIVE SUMMARY

| Feld | Inhalt |
|---|---|
| **Unternehmen** | Infleet GmbH |
| **Adresse** | Im Fliegerhorst 7, D-38642 Goslar |
| **Kontakt** | +49 5321 5182-517 / kontakt@infleet.de |
| **Muttergesellschaft** | Bornemann AG |
| **Vertriebspartner (Ratgeber)** | OneQrew (Dr. Benno Quade, Co-CEO; München, März 2026) |
| **Website** | www.infleet.de / OneQrew.com/Infleet |
| **Positionierung** | GPS-Ortungssysteme und Sicherheitslösungen für Fuhrparks, Fahrzeuge, Geräte und Maschinen – speziell für Handwerksbetriebe, Bau und KMU. Made and Hosted in Germany. |
| **Kernbotschaft Handwerk** | Sichtbarkeit auf der Baustelle – Echtzeit-Standortdaten senken Kosten, eliminieren Suchzeiten und machen Disponieren zur Routine. |
| **Wichtigste Produkte** | GPS Fahrzeugortung, GPS Containerortung, Elektronisches Fahrtenbuch, Tachograph auslesen, Fuhrparkmanagement (SaaS) |
| **Wichtigste Zielgruppen** | Handwerksbetriebe (SHK, Elektro, GaLaBau, Bau), Fuhrparkverantwortliche KMU, Disponenten, Geschaeftsfuehrer kleiner Betriebe |
| **Wichtigste Gewerke** | GaLaBau, Bauhauptgewerbe, SHK, Elektro/Gebaeudetechnik, Entsorgung |
| **Wichtigste Services** | 30-Tage-Test, BALM-Foerderberatung, Demo, DGUV-Fahrerunterweisung, Fuehrerscheinkontrolle, RDL-Tacho-Archiv |
| **Wichtigste USPs** | Made in Germany, ISO 9001 + 27001, DSGVO-konform, modular, BALM-foerderfaehig, ERP-integrierbar |
| **Auffaelligkeiten** | Tonalitaet Du/Sie inkonsistent; keine dedizierte Referenzseite; Bewertungsquelle (4,8/5) nicht verlinkt; Ratgeber ist OneQrew-Partnerdokument |

---

## BLOCK 2 -- JSON-WISSENSBASIS

```json
{
  "company_profile": {
    "name": "Infleet GmbH",
    "address": "Im Fliegerhorst 7, D-38642 Goslar",
    "phone": "+49 5321 5182-517",
    "email": "kontakt@infleet.de",
    "website": "https://www.infleet.de",
    "partner_portal": "https://OneQrew.com/Infleet",
    "parent_company": "Bornemann AG",
    "distribution_partner": "OneQrew (Dr. Benno Quade, Co-CEO, Muenchen)",
    "positioning": "GPS-Ortungs- und Sicherheitsloesungen fuer Fuhrparks, Fahrzeuge, Geraete und Maschinen - modular, DSGVO-konform, hosted in Germany",
    "tagline": "GPS-Systeme, die fuer dich arbeiten.",
    "certifications": ["ISO 9001:2015", "ISO 27001:2022", "DSGVO-konform", "BALM-foerderfaehig", "DGUV-zertifiziert (Fahrerunterweisung)"],
    "target_market": "B2B - KMU, Handwerksbetriebe, Fuhrparkmanager, Logistik, Spedition, Entsorgung",
    "customer_count": "28.000+ Firmenkunden (Bornemann Group gesamt)",
    "avg_rating": "4,8 / 5 aus 223 Bewertungen"
  },

  "products": [
    {
      "id": "P01",
      "name": "GPS Fahrzeugortung",
      "category": "Kernprodukt / SaaS + Hardware",
      "url": "/gps-fahrzeugortung/",
      "description": "Echtzeit-GPS-Ortung fuer Fahrzeugflotten (PKW, Transporter, LKW, Baumaschinen). Cloud-basiert, plattformunabhaengig, skalierbar von 5 bis 500+ Fahrzeugen.",
      "primary_functions": [
        "Live-Ortung auf Karte (Google Maps, HERE, OSM)",
        "Positionsarchiv / Tourhistorie",
        "Tourenplanung und Umkreissuche",
        "Geozonen und Regeln (Ein-/Austritt-Events)",
        "Benachrichtigungen (E-Mail, SMS, WhatsApp, Voice, API/Webhook)",
        "Berichte (PDF, CSV, XLSX, plan- und abonnierbar)",
        "Fahrzeugverwaltung (Gruppen, Rollen, Rechte)"
      ],
      "optional_modules": [
        "Elektronisches Fahrtenbuch",
        "Fuehrerscheinkontrolle (manuell / AutoIdent / VideoIdent)",
        "Fahrerunterweisung (DGUV-zertifiziert)",
        "UVV-Check",
        "Tachograph auslesen (Remote)",
        "Auftragsverwaltung",
        "Container- / Trailer- / Maschinenortung",
        "Anlasserunterbrechung (Remote Immobilizer)",
        "Privatschalter (DSGVO-Privatmodus)"
      ],
      "hardware_options": [
        {"type": "OBD-Schnellstecker", "use_case": "Plug and Play, PKW/Transporter/Poolfahrzeuge"},
        {"type": "Festeinbau-Ortungsbox", "use_case": "LKW, Nutzfahrzeuge, Baumaschinen (verdeckt, dauerhaft)"},
        {"type": "Sonderloesungen", "use_case": "Solar, Akku (bis 10 Jahre), RFID-ready; Container, Trailer, Maschinen"}
      ],
      "accuracy": "<2,5 m (OBD/Festeinbau), <1 m (Sonderloesung)",
      "key_metrics": {
        "auftragskapazitaet": "+10%",
        "kraftstoffkosten": "-15%",
        "gefahrene_km": "-11%",
        "kommunikationsaufwand": "-40%",
        "fahrzeugkosten": "-18%"
      },
      "usps": [
        "Made and Hosted in Germany",
        "ISO 9001 + ISO 27001",
        "BALM-foerderfaehig",
        "Modular erweiterbar",
        "30 Tage kostenlos testen",
        "Sparrechner auf der Website"
      ],
      "target_audiences": ["Handwerksbetriebe", "Logistik", "Entsorgung", "Bau", "Aussendienst"]
    },
    {
      "id": "P02",
      "name": "GPS Containerortung",
      "category": "Asset-Tracking / IoT-Sensorik",
      "url": "/gps-containerortung/",
      "description": "GPS/GNSS-, BLE-, LoRa-WAN- und RFID-basierte Ortung von Containern aller Art inkl. Sensor-Integration.",
      "technologies": ["GPS/GNSS", "Bluetooth BLE", "LoRa-WAN", "RFID"],
      "sensor_types": ["Fuellstand", "Temperatur", "Licht", "Magnet", "CO2", "Feinstaub", "Geraeusch", "Deckelstatus", "Parken"],
      "hardware_specs": {"battery_life": "bis zu 5-10 Jahre", "protection_class": "IP68", "power_options": ["Solar", "Akku", "Netz"]},
      "container_types": ["Baucontainer", "Absatzcontainer", "Abrollcontainer", "Presscontainer", "Frachtcontainer", "Recycling-Container", "Muldencontainer"],
      "usps": ["Multi-Technologie (GPS+BLE+LoRa-WAN+RFID)", "Weltweite Abdeckung", "IP68-zertifiziert", "Jahre-lange Akkulaufzeit"],
      "target_audiences": ["Ver-/Entsorger", "Containerdienste", "Bauunternehmen", "Handel"]
    },
    {
      "id": "P03",
      "name": "Trailer- und Anhaengerortung",
      "category": "Asset-Tracking",
      "url": "/trailerortung-und-anhaengerortung-angebot-erhalten-sea/",
      "description": "GPS-Echtzeitortung fuer Trailer, Wechselbruecken und Anhaenger ohne eigene Stromversorgung.",
      "key_features": ["Echtzeit-Standort", "Geozonen und Alarme", "E-Lock (Seilalarm)", "Krone-Trailer-Integration", "Plug and Play"],
      "cost_savings": "bis zu 20%",
      "target_audiences": ["Transportunternehmen", "Logistikfirmen"]
    },
    {
      "id": "P04",
      "name": "Elektronisches Fahrtenbuch (Logbook)",
      "category": "Compliance / SaaS + Hardware",
      "url": "/elektronisches-fahrtenbuch/",
      "description": "GPS-gestuetztes digitales Fahrtenbuch - automatisch, manipulationssicher, finanzamtkonform.",
      "key_features": [
        "Automatische Erfassung (Datum, Uhrzeit, Start/Ziel, km, Route)",
        "Kategorisierung (dienstlich/privat/Arbeitsweg)",
        "Privatmodus (nur Distanz gespeichert)",
        "Export PDF/CSV",
        "Sparrechner 1%-Regel vs. Fahrtenbuchmethode",
        "E-Auto (0,25%) und Plug-in-Hybrid (0,5%) unterstuetzt"
      ],
      "contracts": ["12 Monate flexibel", "24 Monate mit Preisvorteil", "30+ Fahrzeuge: massgeschneidert"],
      "usps": ["Finanzamtanerkannt", "DSGVO-konform", "Hosting Deutschland", "Hardware inklusive"]
    },
    {
      "id": "P05",
      "name": "Tachograph auslesen (Infleet Tacho)",
      "category": "Compliance / Remote-Service / SaaS",
      "url": "/tachograph-auslesen/",
      "description": "Remote Download (RDL) von Fahrerkarten- und Fahrzeug-Massenspeicherdaten.",
      "modules": [
        "Remote Download (RDL)",
        "RDL-Server (optional, vollautomatisiert)",
        "Lenk- und Ruhezeiten Live",
        "BASIC Analysen und Auswertungen",
        "Gesetzeskonforme Archivierung (24 Monate, ISO 27001 DE)",
        "API fuer Drittanwendungen"
      ],
      "legal_context": "Tachographpflicht ab 2006; ab 1. Juli 2026 auch fuer Fahrzeuge ab 2,5t grenzueberschreitend",
      "target_audiences": ["LKW-Fuhrparks", "Speditionen", "Transportunternehmen"]
    },
    {
      "id": "P06",
      "name": "Fuhrparkmanagement (SaaS-Plattform)",
      "category": "SaaS / Flottenmanagement-Software",
      "url": "/fuhrparkmanagement",
      "description": "Cloud-basierte Fuhrparkverwaltungs-Software ohne Hardware.",
      "packages": [
        {"name": "S", "price_month_net": "25 EUR", "vehicles": 10, "drivers": 50, "users": 3},
        {"name": "M", "price_month_net": "80 EUR", "vehicles": 50, "drivers": 150, "users": 6},
        {"name": "L", "price_month_net": "115 EUR", "vehicles": 75, "drivers": 300, "users": 20},
        {"name": "XL", "price_month_net": "300 EUR", "vehicles": 200, "drivers": 1500, "users": "unbegrenzt"}
      ],
      "add_ons": {
        "fuehrerscheinkontrolle_auto": "5,19-6,49 EUR je Kontrolle",
        "fahrerunterweisung_uvv": "8,99-11,88 EUR je Unterweisung (DGUV-zertifiziert)"
      },
      "usps": ["Keine Hardware", "Keine Setup-Gebuehr", "30 Tage kostenlos", "SAP-Export", "Cloud Made in Germany (erneuerbare Energie)"]
    },
    {
      "id": "P07",
      "name": "GPS Diebstahlschutz",
      "category": "Sicherheitsloesung (Use-Case-Produkt)",
      "url": "/gps-diebstahlschutz/",
      "description": "GPS-basierter Diebstahlschutz via Geofencing, RFID Mutter/Tochtermodul und Lichtsensorik.",
      "key_features": ["Geofencing + Echtzeitalarm", "RFID Mutter/Tochter-System", "Lichtsensor (Oeffnungserkennung)", "Langzeitortung (Akku)", "Anlasserunterbrechung"]
    },
    {
      "id": "P08",
      "name": "GPS Mitarbeiterortung",
      "category": "Personenortung",
      "url": "/gps-mitarbeiterortung/",
      "description": "GPS-Ortung von Aussendienstmitarbeitern und mobilen Einsatzkraeften inkl. Notfallalarm.",
      "key_features": ["Echtzeit-Ortung", "Bewegungszonen", "Alarmknopf (Notfall)", "Reports"],
      "accuracy": "bis zu 7 m",
      "battery": "bis zu 72 Stunden",
      "target_audiences": ["Aussendienst", "Monteure", "Pflegedienste"]
    }
  ],

  "services": [
    {"id": "S01", "name": "Telefonische Beratung", "format": "Telefonisch, kostenlos", "phase": "Pre-Sales"},
    {"id": "S02", "name": "Demo / virtuelle Vorfuehrung", "format": "Online, ca. 20 Min, kostenlos", "phase": "Evaluation"},
    {"id": "S03", "name": "30 Tage kostenloser Test", "format": "SaaS-Testzugang + Hardware-Versand", "phase": "Onboarding"},
    {"id": "S04", "name": "BALM-Foerderberatung", "format": "Beratung, Unterstuetzung bei Antrag", "phase": "Pre-Sales", "note": "bis 80% Erstattung, max. 2.000 EUR/Fzg, max. 17 Fzg / 33.000 EUR; Zielgruppe: Fzg >= 7,5t GKV"},
    {"id": "S05", "name": "Onboarding / Hardware-Zusendung", "format": "Versand + Portal-Aktivierung", "phase": "Kauf / Start"},
    {"id": "S06", "name": "Helpdesk / Support", "format": "Online-Ticketsystem (hilfe.bornemann.net), Telefon 0800", "phase": "Aftersales"},
    {"id": "S07", "name": "Sparrechner (Self-Service Tools)", "format": "Online-Rechner auf Website", "phase": "Kaufentscheidung"},
    {"id": "S08", "name": "DGUV-zertifizierte Fahrerunterweisung (UVV)", "format": "Online, dezentral", "phase": "Laufender Betrieb"},
    {"id": "S09", "name": "Fuehrerscheinkontrolle", "format": "Manuell / AutoIdent / VideoIdent", "phase": "Laufender Betrieb"},
    {"id": "S10", "name": "Gesetzeskonforme Tacho-Archivierung", "format": "Cloud (ISO 27001 DE, 24 Monate)", "phase": "Laufender Betrieb"},
    {"id": "S11", "name": "Datenschutz-Partnervermittlung (via OneQrew)", "format": "Externer DSB-Zugang ueber Infleet-Partnerkreis", "phase": "Einfuehrung", "source": "Ratgeber PDF"}
  ],

  "audiences": [
    {
      "persona": "Fuhrparkleiter / Fleet Manager",
      "pain_points": ["Terminpflichten", "Compliance (Fuehrerschein, UVV)", "Kosten-Controlling"],
      "products": ["P06", "P01", "P05"]
    },
    {
      "persona": "Geschaeftsfuehrer / Inhaber KMU",
      "pain_points": ["Zeitaufwand", "fehlende Transparenz", "Betriebskosten"],
      "products": ["P01", "P04", "P06"]
    },
    {
      "persona": "Disponent / Disponentin",
      "pain_points": ["Echtzeitstatus", "Tourenoptimierung", "Kommunikationsaufwand"],
      "products": ["P01"]
    },
    {
      "persona": "Logistikleiter (Spedition)",
      "pain_points": ["Tachograph-Compliance", "Ruhezeiten", "Remote-Download"],
      "products": ["P05", "P01", "P03"]
    },
    {
      "persona": "Handwerker-Unternehmer",
      "pain_points": ["Suchzeiten Geraete/Maschinen", "Leerfahrten", "Kundennachweise", "Kostenlawine Kleinkram"],
      "products": ["P01", "P07", "P02"],
      "source": "Ratgeber PDF"
    },
    {
      "persona": "HR-Abteilung",
      "pain_points": ["Fuehrerscheinkontrolle", "Haftungsschutz", "Verwaltungsaufwand"],
      "products": ["P06"]
    }
  ],

  "industries": [
    "Transport und Logistik",
    "Speditionen / LKW-Transport",
    "Handwerk (allgemein)",
    "Garten- und Landschaftsbau (GaLaBau)",
    "Bau / Bauhauptgewerbe",
    "Entsorgung / Containerdienste",
    "Aussendienst / Serviceflotten",
    "Gesundheit / Pflege",
    "Fuhrparkbetreiber KMU und Konzern",
    "Automobilindustrie / Engineering",
    "Poolfahrzeug-Verwaltung"
  ],

  "trades": [
    "Handwerk (allgemein)",
    "SHK (Sanitaer, Heizung, Klima) - abgeleitet",
    "Elektro / Gebaeudetechnik - abgeleitet",
    "Garten- und Landschaftsbau (GaLaBau)",
    "Bauhauptgewerbe / Tiefbau",
    "Entsorgung / Recycling",
    "Spedition / Gueterkraftverkehr",
    "Pflegedienste / Sozialwesen",
    "Aussendienstunternehmen"
  ],

  "use_cases": [
    {
      "id": "UC01",
      "name": "Tourenoptimierung und Disposition",
      "industries": ["Logistik", "Handwerk", "GaLaBau", "Spedition"],
      "pain": "Ungeplante Fahrwege, hohe Kraftstoffkosten, keine Echtzeittransparenz",
      "solution": "GPS Live-Ortung, Tourenplanung, Umkreissuche",
      "outcomes": ["-15% Kraftstoff", "-11% km", "+10% Auftragskapazitaet", "-40% Kommunikation"]
    },
    {
      "id": "UC02",
      "name": "Suchzeiten-Eliminierung im Handwerk",
      "industries": ["Handwerk", "Bau", "GaLaBau"],
      "pain": "Geraete/Maschinen nicht auffindbar; Rueckfahrten zum Betrieb wegen vergessener Werkzeuge",
      "solution": "Maschinenortung + BLE-Tagging + Geozonen",
      "outcomes": ["40 Min Wartezeit verhindert (Fall 1 Ratgeber)", "Leerfahrten -75% (GaLaBau-Case)"],
      "roi_example": "4 Fzg / 2 Personen / 3x/Monat vergessen: 7.200 EUR Verlust/Jahr (bei 50 EUR/Std.)",
      "source": "Ratgeber PDF + GaLaBau-Case"
    },
    {
      "id": "UC03",
      "name": "Compliance und Tachographenpflicht",
      "industries": ["Speditionen", "Transport"],
      "pain": "Manuelle Auslesepflicht, Bussgeldrisiko, komplexe Auswertung",
      "solution": "Remote Download, automatische Archivierung, Lenk-/Ruhezeitenmonitor",
      "outcomes": ["Kein Fahrt zum Betrieb", "Bussgeld-Vermeidung", "24-Monats-Archivierung"]
    },
    {
      "id": "UC04",
      "name": "Steueroptimierung mit Fahrtenbuch",
      "industries": ["Alle Branchen mit Dienstwagen"],
      "pain": "1%-Regel-Ueberbesteuerung, Papierchaos",
      "solution": "Automatisches GPS-Fahrtenbuch, Privatmodus, Sparrechner",
      "outcomes": ["Steuerersparnis", "Verwaltungsvereinfachung"]
    },
    {
      "id": "UC05",
      "name": "Diebstahlpraevention und Asset-Schutz",
      "industries": ["Bau", "Logistik", "Entsorgung"],
      "pain": "Fahrzeug-/Maschinen-/Containerschwund",
      "solution": "Geofencing, RFID Mutter/Tochter, Lichtsensoren, Langzeitortung",
      "outcomes": ["Schnelle Polizeimeldung", "Asset-Rueckholung"]
    },
    {
      "id": "UC06",
      "name": "Anwesenheitsnachweis und Kundenbelege",
      "industries": ["Handwerk", "Bau"],
      "pain": "Streitfaelle mit Bauherren; fehlende Belege fuer Anwesenheitszeiten",
      "solution": "Geozonen-Zeitstempel, automatische Ein-/Ausfahr-Logs",
      "outcomes": ["Belastbare Protokolle", "Weniger Reklamationen (-80%)", "Schnellere Abschlaege"],
      "source": "Ratgeber PDF + GaLaBau-Case"
    },
    {
      "id": "UC07",
      "name": "ERP-Integration im Handwerk",
      "industries": ["Handwerk"],
      "pain": "GPS-Daten isoliert; kein Austausch mit Dispositions- oder ERP-System",
      "solution": "Integration Infleet-GPS in ERP via API (TAIFUN+, smarthandwerk pro, Sykasoft+, PASST+, Corpora, ANNEXUS, OneQrew ERP, VenDoc)",
      "outcomes": ["Vollstaendigkeitspruefung Werkzeuge vor Tour", "Automatisiertes Disponieren"],
      "source": "Ratgeber PDF"
    },
    {
      "id": "UC08",
      "name": "BALM-Foerderung fuer Transportunternehmen",
      "industries": ["Gueterkraftverkehr >= 7,5t"],
      "pain": "Investitionskosten als Kaufhuerde",
      "solution": "BALM-Foerderung bis 80%, max. 2.000 EUR/Fzg, max. 17 Fzg",
      "outcomes": ["Drastische Kostensenkung", "ROI deutlich schneller"]
    }
  ],

  "references": [
    {
      "id": "R01",
      "name": "GaLaBau-Betrieb Niedersachsen (anonym)",
      "industry": "Garten- und Landschaftsbau",
      "size": "25 MA, 8 Transporter, 3 Radlader, 6 Anhaenger",
      "results": {"-15% Kraftstoff": true, "-50% Dispoaufwand": true, "-75% Leerfahrten": true, "-80% Reklamationen": true, "ROI 5 Monate": true, "Einsparung Jahr 1 > 15.000 EUR": true},
      "products": ["P01"]
    },
    {
      "id": "R02",
      "name": "Fuhrparkleitung (anonym, 37 Fahrzeuge, seit 2011)",
      "industry": "Unbekannt",
      "results": {"Individuelle Alarmfunktion auf Kundenwunsch entwickelt": true, "Langjaehrige Bindung (15 Jahre)": true},
      "products": ["P01"]
    },
    {"id": "R03", "name": "Zeltverleih Dietrich", "industry": "Verleih / Events", "products": ["P01"]},
    {"id": "R04", "name": "FENESTRA Huefnagels GmbH", "industry": "Bau / Fensterbau", "products": ["P01"]},
    {"id": "R05", "name": "Klinik Nordseekueste KG", "industry": "Gesundheit / Pflege", "products": ["P08"]},
    {"id": "R06", "name": "ISVB Automotive", "industry": "Automotive / Engineering", "products": ["P01"]}
  ],

  "brand_language": {
    "core_claims": [
      "GPS-Systeme, die fuer dich arbeiten.",
      "Technologie, die fuer dich arbeitet.",
      "Made and Hosted in Germany - sicher, zertifiziert und nachhaltig.",
      "Einfach, sicher, fair.",
      "Wir entwickeln Loesungen, die wirklich helfen - transparent, nachhaltig und zukunftssicher."
    ],
    "key_verbs": ["orten", "sparen", "schuetzen", "planen", "nachweisen", "optimieren", "verwalten", "vereinfachen", "arbeiten", "reagieren"],
    "key_nouns": ["Flotte", "Fuhrpark", "Transparenz", "Ueberblick", "Echtzeit", "Sicherheit", "Datenschutz", "Kostenersparnis", "Foerderung", "Effizienz", "Compliance", "Nachweis"],
    "key_adjectives": ["smart", "intelligent", "einfach", "modular", "skalierbar", "DSGVO-konform", "finanzamtkonform", "lueckenlos", "revisionssicher", "transparent", "zukunftssicher"],
    "cta_patterns": [
      "Jetzt Angebot erhalten",
      "Kostenlos testen",
      "30 Tage kostenlos testen",
      "Demo anfragen",
      "Vorfuehrung anfordern",
      "Termin vereinbaren",
      "Jetzt informieren"
    ],
    "argumentation_patterns": [
      "Problem -> Loesung -> messbare Kennzahl",
      "Risikoabbau: 30 Tage kostenlos, unverbindlich, keine versteckten Kosten",
      "Trust-Signale: ISO, Made in Germany, DSGVO",
      "Vergleich: 1%-Regel vs. Fahrtenbuch (Sparrechner)",
      "Skalierbarkeit: von 5 bis 500+ Fahrzeugen"
    ]
  },

  "tone_of_voice": {
    "primary_tone": "partnerschaftlich, loesungsorientiert, bodenstaendig",
    "formality": "niedrig bis mittel; Du-Ansprache dominiert",
    "emotionality": "gering bis mittel; sachlich-nutzenfokussiert",
    "technical_depth": "mittel bis hoch; Specs auf Produktseiten, didaktisch im Blog",
    "character": "erfahrener, zugaenglicher Berater; spricht Praktikern auf Augenhoehe"
  },

  "brand_glossary": {
    "GPS Fahrzeugortung": "Echtzeit-Standorterfassung von Fahrzeugen via GPS; Kernprodukt Infleet",
    "Infleet Cloud": "DSGVO-konforme, ISO 27001-zertifizierte Cloud-Plattform hosted in Germany",
    "Geozone": "Virtuelle geografische Zone mit automatischer Alarmierung bei Ein-/Austritt",
    "Logbook": "Elektronisches Fahrtenbuch von Infleet; finanzamtkonform, GPS-gestuetzt",
    "RDL": "Remote Download - Fernauslesen des digitalen Tachographen",
    "BALM-Foerderung": "Bundesfoerderung fuer GPS-Telematik im GKV; bis 80%, max. 2.000 EUR/Fzg",
    "Privatschalter": "DSGVO-konforme Funktion zur Deaktivierung der Ortung bei Privatfahrten",
    "OBD-Schnellstecker": "Plug-and-Play-Hardware fuer GPS-Ortung ohne Werkstattmontage",
    "Maschinenortung": "GPS/BLE-Tracking von Baumaschinen, Geraeten und Werkzeugen",
    "ETA": "Expected Arrival Time; Echtzeit-Ankunftsprognose fuer Endkunden",
    "UVV-Check": "Digitale Fahrzeuguntersuchung nach Unfallverhuetungsvorschriften",
    "Made in Germany": "Infleet-Software und -Infrastruktur wird in Deutschland entwickelt und betrieben"
  },

  "sales_marketing_qa": [
    {
      "q": "Warum GPS im Handwerk? Die Mitarbeiter koennten sich ueberwacht fuehlen.",
      "a": "GPS ist kein Misstrauen, sondern Betriebsorganisation. Es geht darum, Werkzeuge zu finden, Leerfahrten zu vermeiden und bei Kundenstreit belastbare Nachweise zu haben. Wichtig: Mitarbeitende transparent und fruehzeitig einbinden.",
      "source": "Ratgeber PDF"
    },
    {
      "q": "Ist GPS-Tracking DSGVO-konform?",
      "a": "Ja, wenn die DSGVO eingehalten wird: klare Zweckbindung, transparente Information der Mitarbeitenden, Datenschutz-Folgeabschaetzung nach Art. 35 DSGVO, Auftragsdatenverarbeitung mit Infleet (ISO 27001, Server Deutschland).",
      "source": "Ratgeber PDF"
    },
    {
      "q": "Was kostet Infleet?",
      "a": "Fuhrparkmanagement ab 25 EUR/Monat (Paket S, 10 Fahrzeuge). GPS Fahrzeugortung: individuelles Angebot (Hardware + Lizenz). 30 Tage kostenlos testen. BALM-Foerderung moeglich."
    },
    {
      "q": "Was kann ich im Handwerk alles tracken?",
      "a": "Fahrzeuge (Montagefahrzeuge, Transporter, Kleinbagger, Anhaenger), Maschinen (Bohrhammer, Saegen, Bautrockner, Ruettelplatte), Leitern, Gerueste und Container. Kombination aus GPS-Tracker (mit SIM) fuer Fahrzeuge und BLE-Tags fuer Kleingeraete empfohlen.",
      "source": "Ratgeber PDF"
    },
    {
      "q": "Wie schnell ist der ROI?",
      "a": "GaLaBau-Case: Amortisation nach 5 Monaten, >15.000 EUR Einsparung im ersten Jahr. Ratgeber-Rechnung: 4 Fahrzeuge / 2 Personen, 3 vergessene Rueckfahrten/Monat = 7.200 EUR Verlust/Jahr."
    }
  ],

  "source_index": [
    {"id": "W01", "title": "GPS Fahrzeugortung", "url": "https://infleet.de/gps-fahrzeugortung/"},
    {"id": "W02", "title": "GPS Containerortung", "url": "https://infleet.de/gps-containerortung/"},
    {"id": "W03", "title": "Trailer- und Anhaengerortung", "url": "https://infleet.de/trailerortung-und-anhaengerortung-angebot-erhalten-sea/"},
    {"id": "W04", "title": "Elektronisches Fahrtenbuch", "url": "https://infleet.de/elektronisches-fahrtenbuch/"},
    {"id": "W05", "title": "Tachograph auslesen", "url": "https://infleet.de/tachograph-auslesen/"},
    {"id": "W06", "title": "Fuhrparkmanagement", "url": "https://infleet.de/fuhrparkmanagement"},
    {"id": "W07", "title": "GPS Diebstahlschutz", "url": "https://infleet.de/gps-diebstahlschutz/"},
    {"id": "W08", "title": "GPS Mitarbeiterortung", "url": "https://infleet.de/gps-mitarbeiterortung/"},
    {"id": "W09", "title": "GPS Loesungen Uebersicht", "url": "https://infleet.de/gps-loesungen/"},
    {"id": "W10", "title": "BALM-Foerderung", "url": "https://infleet.de/foerderung-umweltschutz-und-sicherheit-de-minimis/"},
    {"id": "W11", "title": "Unternehmen", "url": "https://infleet.de/unternehmen/"},
    {"id": "W12", "title": "GaLaBau Praxisbeispiel", "url": "https://infleet.de/praxisbeispiel-gps-system-galabau-betrieb-spart-15-sprit-10-std-dispo-zeit-pro-woche/"},
    {"id": "PDF01", "title": "Infleet Ratgeber: GPS-Tracking fuer Fahrzeuge, Geraete und Maschinen im Handwerk", "publisher": "Infleet GmbH / OneQrew", "author": "Dr. Benno Quade, Co-CEO OneQrew", "date": "2026-03-05"}
  ],

  "gaps_and_unknowns": [
    "Tonalitaet Du/Sie inkonsistent; keine normative Entscheidung erkennbar",
    "28.000 Firmenkunden: unklar ob Infleet oder Bornemann Group gesamt",
    "Bewertungsquelle (4,8/5 aus 223 Bewertungen): Plattform nicht verlinkt",
    "Akkulaufzeit GPS Diebstahlschutz: 15 Jahre (alt) vs. 5 Jahre (aktuell)",
    "Seconity und Work: eigenstaendige Produktlinien, nicht gecrawlt",
    "GPS Yachtortung, Personenortung, Sensorik-Seite: nicht gecrawlt",
    "Keine dedizierte Referenz-/Case-Study-Seite vorhanden",
    "GaLaBau-Case-Zahlen: nicht explizit als reale Kundenmessung ausgewiesen",
    "Ratgeber-PDF ist OneQrew-Partnerdokument, nicht offiziell auf infleet.de",
    "ERP-Integrationen (TAIFUN+ etc.) sind OneQrew-spezifisch"
  ],

  "final_confidence": {
    "products": "hoch",
    "services": "mittel-hoch",
    "audiences": "hoch",
    "industries_trades": "mittel-hoch",
    "references": "mittel",
    "brand_language": "hoch",
    "pdf_content": "hoch"
  }
}
```

---

## BLOCK 3 -- MARKEN-GLOSAR

| Begriff | Definition | Kategorie | Empfohlene Verwendung | Verwandte Begriffe | Beispiel (markenkonforme Sprache) |
|---|---|---|---|---|---|
| **GPS Fahrzeugortung** | Echtzeit-Standorterfassung von Fahrzeugen via GPS-Technologie inkl. Cloud-Auswertung | Kernprodukt | Immer als Hauptbegriff fuer das Tracking-Kernprodukt | Live-Ortung, Flottenmanagement, Tracking | Mit GPS Fahrzeugortung weisst du jederzeit, wo deine Transporter stehen. |
| **Infleet Cloud** | DSGVO-konforme, ISO 27001-zertifizierte Softwareplattform; Hosting in Deutschland | Plattform | Bei Datenschutz- und Hosting-Argumenten | Made in Germany, Hosted in Germany, ISO 27001 | Alle Daten laufen sicher in der Infleet Cloud - hosted in Germany. |
| **Geozone / Geofencing** | Virtuelle geografische Zone; loest automatisch Ereignisse aus bei Ein- oder Austritt | Produktfunktion | Zur Erklaerung von Alarmfunktionen, Nachweisen, Diebstahlschutz | Alarm, Benachrichtigung, Anwesenheitsnachweis | Mit Geozonen erhaeltst du sofort eine Meldung, wenn ein Fahrzeug die Baustelle verlaesst. |
| **Logbook** | Elektronisches Fahrtenbuch von Infleet; automatisch, GPS-gestuetzt, finanzamtkonform | Produktname | Als Produktname fuer das Fahrtenbuch-Modul | Elektronisches Fahrtenbuch, 1%-Regel, Privatmodus | Logbook erfasst jede Fahrt automatisch - finanzamtkonform und ohne Papierchaos. |
| **Remote Download (RDL)** | Fernauslesen des digitalen Tachographen ohne physischen Zugang zum Fahrzeug | Fachbegriff | Im Kontext Tachograph; Zielgruppe Spedition/LKW | Tachograph, Lenk-/Ruhezeiten, Archivierung | Mit RDL werden Tachographendaten automatisch uebertragen - kein Fahrt zum Betrieb noetig. |
| **BALM-Foerderung** | Bundesfoerderung fuer Telematik im gewerblichen Gueterkraftverkehr; bis 80% Erstattung | Kaufargument | Als Preisargument fuer GKV >= 7,5t | De-minimis (veraltet), Foerderprogramm | Als Transportunternehmen mit LKW >= 7,5t kannst du bis zu 80% der Kosten ueber die BALM-Foerderung erstatten lassen. |
| **Privatschalter** | Funktion zum Deaktivieren der Ortung waehrend privater Fahrten; DSGVO-konform | Produktfunktion / Datenschutz | Bei Datenschutz-Einwaenden; immer zusammen mit DSGVO kommunizieren | DSGVO, Privatmodus, Datenschutz | Mit dem Privatschalter schalten Fahrer die Ortung bei Privatfahrten einfach aus. |
| **OBD-Schnellstecker** | Plug-and-Play-Hardware; steckt in die OBD-Buchse; keine Werkstatt noetig | Hardware | Als Einstiegsloesung fuer schnelle Implementierung | Festeinbau-Ortungsbox, Hardware, Tracker | Der OBD-Schnellstecker ist in Sekunden montiert - ohne Werkstatttermin. |
| **Maschinenortung** | GPS/BLE-Tracking von Baumaschinen, Geraeten und Kleinwerkzeugen | Produktkategorie (Handwerk) | Speziell im Handwerk/Bau-Kontext | Geraete-Tracking, BLE-Tag, Asset-Tracking | Mit Maschinenortung weisst du, wo deine Ruettelplatte gerade steht - ohne drei Telefonate. |
| **ETA** | Expected Arrival Time; Echtzeit-Ankunftsprognose fuer Endkunden | Fachbegriff / USP | Im Kontext Kundenkommunikation und Servicequalitaet | Tourenplanung, Disposition, Transparenz | Schick deinen Kunden eine ETA per SMS - wie beim Paketdienst. |
| **Made in Germany / Hosted in Germany** | Infleet-Software und -Infrastruktur wird in Deutschland entwickelt und betrieben | Trust-Signal / USP | Als Datenschutz- und Qualitaetsargument | ISO 27001, DSGVO-konform, Sicherheit | Infleet ist Made and Hosted in Germany - deine Daten verlassen nie den deutschen Rechtsraum. |
| **UVV-Check** | Digitale Fahrzeuguntersuchung nach Unfallverhuetungsvorschriften | Compliance-Begriff | Im Kontext Fuhrparkmanagement und Arbeitgeberpflichten | Fahrerunterweisung, DGUV, Compliance | Der UVV-Check laeuft digital im System - kein Papierchaos, volle Nachweisbarkeit. |

---

## BLOCK 4 -- TONE OF VOICE GUIDE

### Markencharakter
Infleet ist ein verlasslicher, praxisnaher Partner fuer Unternehmer und Fuhrparkverantwortliche. Die Marke spricht wie ein erfahrener Kollege aus der Branche - nicht wie ein anonymer Software-Konzern. Kompetenz wird durch Fakten, Zertifikate und messbare Ergebnisse bewiesen, nicht durch Superlative.

### Sprachstil
- Aktive Verben, kurze Saetze, direkte Ansprache
- Kein Marketing-Bingo; lieber konkrete Zahlen als leere Adjektive
- Technische Details nur, wenn sie den Nutzen unterstreichen
- Einwaende (Datenschutz, Mitarbeiterkontrolle) proaktiv und ehrlich adressieren

### Satzlaenge / Satzrhythmus
- **Headlines:** maximal 6 Woerter, Dreier-Rhythmus bevorzugt
- **Fliesstext:** 15-25 Woerter pro Satz; wechselnde Laengen fuer Rhythmus
- **Bullets:** 1 Vorteil pro Punkt; kein Staccato-Stil ohne Kontext

### Fachliche Tiefe
- **Produktseiten:** mittel bis hoch (Specs, Genauigkeiten, Normen)
- **Blog / Ratgeber:** didaktisch, Schritt-fuer-Schritt, Einwaende antizipieren
- **CTAs und Landingpages:** minimal; Nutzen first, Technik second
- **Sales-Gespraech / GPT-Antworten:** Fachtiefe anpassen an Persona

### Ansprache
- **Standard: Du / Dein / Dir** (partnerschaftlich, direkt)
- **Ausnahme:** Containerortung, Fuhrparkmanagement, Terminseite nutzen Sie - fuer neue Inhalte bitte Du normieren

### Tonalitaet je Kanal

| Kanal | Ton | Beispiel |
|---|---|---|
| Website-Produktseiten | Klar, benefit-orientiert, partnerschaftlich | Mit GPS Fahrzeugortung sparst du bis zu 15% Kraftstoff. |
| Blog / Ratgeber | Edukativ, empathisch, Problemloeser | Drei Telefonate, vier Screenshots, zwanzig Minuten Stillstand - nur um die Ruettelplatte zu finden. |
| CTA-Buttons | Direkt, handlungsaktivierend, risikoreduzierend | Jetzt 30 Tage kostenlos testen - unverbindlich. |
| Ads / Social | Kurz, Zahlen-getrieben, neugierig machend | -15% Sprit. -75% Leerfahrten. 5 Monate ROI. Infleet fuer deinen Fuhrpark. |
| Sales / GPT-Antwort | Beratend, loesungsorientiert, konkret | Fuer einen Betrieb mit 5 Transportern empfehle ich den OBD-Schnellstecker plus 30-Tage-Test. |
| Datenschutz-Kommunikation | Sachlich, beruhigend, transparent | GPS ist kein Misstrauen - es ist Betriebsorganisation. |

### Dos
- Messbare Ergebnisse nennen: -15% Sprit, 5 Monate ROI
- Einwaende proaktiv adressieren (Datenschutz, Mitarbeiterkontrolle)
- Dreier-Rhythmen in Headlines: weniger km, weniger Kosten, mehr Ueberblick
- Trust-Signale einbauen: ISO 9001/27001, Made in Germany, DSGVO
- Risikoabbau kommunizieren: kostenlos testen, unverbindlich, keine versteckten Kosten
- Branchenkonkretes Beispiel vor abstraktem Nutzen
- ERP-Integration als Hebelargument im Handwerk (OneQrew-Kontext)

### Donts
- Keine Ueberwachungsrhetorik: nie Mitarbeiter ueberwachen
- Keine leeren Superlative ohne Beleg
- Nicht mit Sie anreden auf Seiten, die Du als Standard haben
- Keine Akkulaufzeit-Angaben ohne Kontext (immer Geraetetyp nennen)
- Nicht De-minimis sagen - korrekt ist BALM-Foerderung
- Keine Angabe, dass Infleet die BALM-Antraege selbst abwickelt

### Beispiel-Claims
- Weisst du gerade, wo dein zweiter Transporter steht?
- GPS auf der Baustelle: Du suchst nicht mehr. Du entscheidest.
- 30 Tage testen. Nichts riskieren. Alles gewinnen.
- Weniger Suchen. Mehr Bauen. Infleet fuer Handwerksbetriebe.
- Deine Daten. Dein Land. Hosted in Germany.

### Beispiel-Ad-Copy (Handwerk)

> **Headline:** 3 Suchsituationen a 15 Min taeglich kosten dich 7.200 EUR im Jahr.
>
> **Body:** GPS-Ortung fuer Fahrzeuge, Maschinen und Werkzeuge - damit du weisst, was wo steht. Ohne Sucherei. Ohne Leerfahrten. Mit lueckenlosen Nachweisen fuer deine Bauherren.
>
> **CTA:** Jetzt 30 Tage kostenlos testen

### Beispielantworten fuer interne GPT-Fragen

**Frage:** Welches Produkt empfiehlst du einem Elektrobetrieb mit 8 Fahrzeugen?

**GPT-Antwort:** Fuer einen Elektrobetrieb mit 8 Fahrzeugen empfehle ich die GPS Fahrzeugortung mit OBD-Schnellsteckern - Plug and Play, keine Werkstatt noetig. Das Elektronische Fahrtenbuch laesst sich als Modul direkt integrieren, wenn Dienstwagenfahrer steuerlich abrechnen wollen. Einstieg am besten ueber den kostenlosen 30-Tage-Test.

**Frage:** Darf ich Mitarbeiter per GPS tracken?

**GPT-Antwort:** Ja - aber mit klaren DSGVO-Regeln: Mitarbeitende muessen transparent informiert werden, die Zwecke muessen dokumentiert sein, und eine Datenschutz-Folgeabschaetzung nach Art. 35 DSGVO ist erforderlich. Infleet verarbeitet alle Daten ausschliesslich auf deutschen Servern (ISO 27001). Ueber den Infleet-Partnerkreis kannst du externe Datenschutzbeauftragte fuer die Umsetzung hinzuziehen.

---

## BLOCK 5 -- GPT-READY INSTRUCTIONS

```
## Was dieses GPT ueber Infleet wissen soll

Du bist ein spezialisierter Wissensassistent fuer die Infleet GmbH.
Infleet ist ein Anbieter von GPS-Ortungssystemen und Sicherheitsloesungen fuer Fuhrparks,
Fahrzeuge, Maschinen und Geraete - spezialisiert auf Handwerksbetriebe, Bau, GaLaBau,
Logistik und KMU. Muttergesellschaft: Bornemann AG. Vertriebspartner u. a. OneQrew.

Deine Kernaufgaben:
1. Produkt-, Service- und Nutzenfragen zu Infleet kompetent beantworten
2. Branchenspezifische Empfehlungen geben (Handwerk, Bau, Logistik etc.)
3. Datenschutz- und Mitarbeiter-Einwaende sachlich und beruhigend adressieren
4. Zwischen Funktion, Nutzen und USP sauber unterscheiden
5. Passende CTAs und naechste Schritte kommunizieren

---

## Wie dieses GPT antworten soll

Tonalitaet:
- Partnerschaftlich, direkt, bodenstaendig
- Du-Ansprache (ausser wenn User explizit Sie bevorzugt)
- Konkrete Zahlen vor abstrakten Adjektiven
- Einwaende proaktiv aufgreifen, nicht ignorieren
- Keine Floskeln; kein Marketing-Bingo

Antwortstruktur:
- Kurze, direkte Erstantwort (1-2 Saetze)
- Dann: strukturierte Detailasfuehrung mit Bullets wenn sinnvoll
- Bei Produktfragen: immer Funktion -> Nutzen -> USP trennen
- Bei fehlender Evidenz: transparent kommunizieren (s. u.)

---

## Bevorzugte Begriffe

| Bevorzugt | Statt |
|---|---|
| GPS Fahrzeugortung | Tracking, Ueberwachung |
| Infleet Cloud | Software, System |
| Geozone | virtueller Zaun, Bereich |
| BALM-Foerderung | De-minimis-Foerderung |
| Maschinenortung | Geraete-Tracking (kontextabhaengig) |
| Privatschalter | Datenschutzfunktion |
| Made and Hosted in Germany | deutsches Produkt |
| Mitarbeitende | Mitarbeiter (genderinklusiv) |

---

## Unterscheidung: Funktion vs. Nutzen vs. USP

- Funktion = Was das Produkt technisch tut:
  Geozonen erzeugen automatisch Ein-/Ausfahr-Logs.

- Nutzen = Was der Kunde davon hat:
  Du hast lueckenlose Nachweise fuer Bauherren - ohne Aufwand.

- USP = Warum Infleet das besser/anders macht:
  Hosted in Germany, ISO 27001-zertifiziert, DSGVO-konform.

Antworte immer in dieser Reihenfolge, wenn nach Produktvorteilen gefragt wird.

---

## Wie bei fehlender Evidenz reagiert werden soll

Wenn zu einer Frage keine gesicherte Information vorliegt:
1. Das offen kommunizieren: Dazu habe ich keine gesicherte Information.
2. Plausible Ableitungen klar als solche kennzeichnen: Ich vermute, dass...
3. An Infleet direkt verweisen: Das beantwortet dir das Infleet-Team am besten: +49 5321 5182-517 oder kontakt@infleet.de
4. Niemals erfinden oder spekulieren ohne Hinweis.

---

## Wichtige Unsicherheiten, die kommuniziert werden sollen

- Akkulaufzeit: Immer Geraetetyp nennen; nicht pauschal bis zu 15 Jahre sagen
- 28.000 Firmenkunden: Bornemann-Konzernzahl; Infleet-spezifische Zahl unbekannt
- GaLaBau-Case-Zahlen: Plausible Orientierungswerte, keine zertifizierten Messungen
- ERP-Integrationen (TAIFUN+ etc.): Gelten fuer OneQrew-Kontext; fuer allgemeine Infleet-Nutzung bitte beim Vertrieb anfragen
- Tonalitaet: Auf bestehenden Seiten teils Sie - fuer neue Inhalte gilt Du als Standard

---

## Handwerk-Spezifika (aus Ratgeber PDF, Maerz 2026)

Zielgruppen Handwerk:
- Inhaber/Geschaeftsfuehrer kleiner Betriebe (5-50 Fahrzeuge)
- Disponenten in Ausbaugewerken
- Gewerke: SHK, Elektro, GaLaBau, Bau, Entsorgung

Typische Pain Points:
- Wo steht die Ruettelplatte? -> Maschinenortung
- Rueckfahrten zum Betrieb wegen vergessener Werkzeuge -> ROI-Rechner
- Streitfaelle mit Bauherren ueber Anwesenheitszeiten -> Geozonen-Logs
- Datenschutz-Einwaende bei Mitarbeitenden -> Kommunikationsleitfaden

Empfohlene Einfuehrungs-Checkliste (aus Ratgeber):
1. Kontaktaufnahme Infleet
2. Zwecke GPS-Tracking festlegen
3. Datenschutzbeauftragten einbinden
4. Datenschutz-Folgeabschaetzung durchfuehren
5. Mitarbeitende transparent informieren
6. Vertraege und Dokumentation abschliessen
7. GPS-Tracking einfuehren
8. Regelmaessig ueberpruefen und anpassen

ERP-Integration (OneQrew-Kontext):
Infleet-GPS kann mit TAIFUN+, smarthandwerk pro, Sykasoft+, PASST+, Corpora,
ANNEXUS, OneQrew ERP und VenDoc integriert werden.
Vollstaendigkeitspruefung von Werkzeugen und Geraeten vor Tagestouren wird damit moeglich.
```

---

*Erstellt: 16. Maerz 2026 | Quelle: infleet.de + Infleet Ratgeber (OneQrew, Maerz 2026)*
