# Assignment Policy

## SOURCE OF TRUTH
The deterministic logic in `/domain` ALWAYS overrides this document.
This file provides context only and must never contradict system logic.

---

## Zweck

Dieses Dokument beschreibt, wie Ticket-Zuweisungen bewertet und
empfohlen werden. Es spiegelt die Logik in `domain/skill_matching.py`
und `domain/assignment_rules.py` wider. Es ersetzt NICHT die deterministische Logik.

---

## Grundprinzip

Jede Ticket-Zuweisung wird in drei Stufen bewertet:

```
1. Skill-Domain-Matching — Passen die Fähigkeiten des Mitarbeiters zur Aufgabe?
2. Cluster-Kontext — Ist der Mitarbeiter dem richtigen Cluster zugeordnet?
3. Plausibilitätsverdikt — Ist die Zuweisung vertretbar?
```

---

## Skill-Domain-Matching

Aus Titel und Beschreibung werden die benötigten Skill-Domains ermittelt.
Jede Domain hat einen definierten Keyword-Satz:

| Domain | Typische Inhalte |
|--------|-----------------|
| content_creation | Artikel, Blog, Landingpage, Story |
| seo | Keywords, Meta, Rankings, Backlinks |
| social_media | Instagram, TikTok, Facebook, Reels |
| email_marketing | Newsletter, Mailing, Kampagne |
| paid_ads | Google Ads, Meta Ads, CPC, Performance |
| analytics | Tracking, Reporting, KPIs, Daten |
| design | Grafik, Canva, Banner, Infografik |
| copywriting | Text, Copy, Headline, Produkttext |
| project_management | Planung, Briefing, Koordination |
| strategy | Strategie, Jahresplan, Konzept |
| technical | CMS, WordPress, HTML, Integration |

---

## Plausibilitätsverdikt

| Verdikt | Bedeutung | Maßnahme |
|---------|-----------|----------|
| `plausible` | ≥ 60% der benötigten Domains vorhanden | Keine Aktion nötig |
| `questionable` | 30–59% der Domains vorhanden | Zur Überprüfung empfehlen |
| `implausible` | < 30% der Domains vorhanden | Neuzuweisung empfehlen |
| `unknown` | Mitarbeiter nicht gefunden / Domains unklar | Manuelle Prüfung |

---

## Empfehlungslogik

Bei Neuzuweisungsempfehlungen gilt:
1. Cluster-Filter: Bevorzuge Mitarbeiter aus dem ermittelten Cluster
2. Domain-Score: Sortiere nach prozentualem Trefferquoten-Anteil
3. Top-3: Gib maximal 3 Empfehlungen zurück
4. Cross-Cluster-Fallback: Wenn keine Cluster-Treffer, erweitere auf alle aktiven Mitarbeiter

---

## Koordinatoren-Rolle

Koordinatoren erhalten KEINE automatische Zuweisung von operativen Tickets.
Sie werden nur als Eskalations- und Überprüfungspunkt benannt:

- Ben Schmidt (SHK+E) — bei unklaren Zuweisungen im SHK+E-Cluster
- David Klein (Dach_und_Holz) — bei Routing-Problemen im Dach-Cluster
- Eva Braun (Baugewerbe) — bei fehlender Zuweisung im Baugewerbe-Cluster

---

## Spezialfälle

### Ticket ohne Assignee
- Pflicht: Empfehlungen generieren (Top-3)
- `needs_reassignment = True`
- Grund: "No assignee set."

### Assignee nicht im Mitarbeiterregister
- Verdikt: `unknown`
- Empfehlungen trotzdem generieren
- Hinweis in Analyse: "Assignee not in registry — manual verification required."

### Greta Fischer als Assignee
- Greta ist Cross-Cluster-Strategin, kein operativer Assignee
- Bei operativen Tickets (Content, Design, SEO) → Verdikt `questionable`
- Empfehlung: An zuständigen Cluster-Spezialisten weitergeben

### Mehrdeutige Skill-Anforderung
- Wenn keine klaren Skill-Domains erkannt werden → Domain `unknown`
- Verdikt wird `unknown`
- Agenten-Kommentar: "Skill-Analyse nicht möglich — Beschreibung zu kurz oder unklar."

---

## Was dieses Dokument NICHT tut

- Es ändert keine Skill-Scores oder Plausibilitäts-Schwellwerte
- Es fügt keine neuen Mitarbeiter hinzu
- Es überschreibt keine Entscheidungen aus `skill_matching.py`
