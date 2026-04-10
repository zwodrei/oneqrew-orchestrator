# Ticket Examples — Context & Edge Cases

Diese Datei enthält annotierte Ticket-Beispiele für das Trainings- und
Kontextverständnis der Analyse-Agenten. Die Beispiele zeigen gute, schlechte
und grenzwertige Tickets aus dem realen Marketing-Alltag.

---

## KATEGORIE A — Vollständige, gut strukturierte Tickets

---

### Beispiel A1 — SEO Landingpage (Sehr gut, Score: 1.0)

```
Name: SEO-Optimierung Landingpage Wärmepumpen Q2 2025
Notes: Die bestehende Landingpage für Wärmepumpen soll für 5 Ziel-Keywords
       überarbeitet werden. Fokus auf Onpage-Optimierung (H1, Meta, Alt-Texte).
       Ziel: Top-10-Ranking für "Wärmepumpe kaufen" und "Wärmepumpe Kosten".
       Deliverable: Überarbeiteter Seitentext + Meta-Angaben als Google Doc.
Assignee: Anna Müller
Due: 2025-04-15
Project: SHK+E Marketing Q2
Tags: seo, wärmepumpe, landingpage, onpage
Custom Fields: Kanal=SEO, Priorität=Hoch
Followers: Ben Schmidt
```

**Routing:** SHK+E → shk_heizung (Konfidenz: 0.85)
**Assignee-Plausibilität:** plausible (Anna: content_creation + seo ✓)
**Completeness:** 11/11 ✓
**Anmerkung:** Ideales Ticket. Klarer Titel, vollständige Beschreibung mit Deliverable,
richtige Zuweisung, alle Felder befüllt.

---

### Beispiel A2 — Newsletter (Gut, Score: 0.91)

```
Name: April-Newsletter Dachsanierung — Saisonstart
Notes: Newsletter für April vorbereiten. Thema: Frühjahrs-Dachcheck und
       Förderprogramme für Dachsanierung. 3 Content-Blöcke: Ratgeber,
       Produktvorstellung, CTA zur Angebotsanfrage.
Assignee: Clara Weber
Due: 2025-04-01
Project: Dach_und_Holz Newsletter
Tags: newsletter, dachsanierung, frühjahrsaktion
Custom Fields: Kanal=Email
Followers: David Klein
```

**Routing:** Dach_und_Holz → dach_ziegel / dach_abdichtung (Konfidenz: 0.78)
**Assignee-Plausibilität:** plausible (Clara: email_marketing + design ✓)
**Completeness:** 10/11 (fehlt: workspace — normalerweise auto-gesetzt)
**Anmerkung:** Sehr gutes Ticket. Einzige Lücke ist das Workspace-Feld,
das in der Praxis automatisch befüllt wird.

---

## KATEGORIE B — Unvollständige Tickets mit häufigen Problemen

---

### Beispiel B1 — Kein Assignee, kein Datum (Schlecht, Score: 0.45)

```
Name: Instagram Posts für Rohbau
Notes: Wir brauchen ein paar Posts für den Rohbau-Bereich. Bitte Grafiken erstellen.
Assignee: (leer)
Due: (leer)
Project: Baugewerbe 2025
Tags: (leer)
Custom Fields: (leer)
Followers: (leer)
```

**Routing:** Baugewerbe → bau_rohbau (Konfidenz: 0.55)
**Assignee-Plausibilität:** — (kein Assignee)
**Completeness:** 5/11 — NICHT bestanden
**Fehlende Kriterien:** assignee_set, due_date_set, tags_present, custom_fields_filled, followers_present, permalink_present
**Empfohlener Assignee:** Felix Hoffmann (social_media + design ✓)
**Anmerkung:** Typisches Ad-hoc-Ticket. Inhaltlich klar, aber operativ nicht
umsetzbar ohne Zuweisung und Zeitplan. Briefing muss nachgefordert werden.

---

### Beispiel B2 — Sehr kurzer Titel, keine Beschreibung (Schlecht, Score: 0.27)

```
Name: Content
Notes: (leer)
Assignee: (leer)
Due: (leer)
Project: (leer)
Tags: (leer)
Custom Fields: (leer)
Followers: (leer)
```

**Routing:** unbekannt (Konfidenz: 0.0)
**Assignee-Plausibilität:** — (kein Assignee)
**Completeness:** 3/11 — NICHT bestanden
**Fehlende Kriterien:** title_present (zu kurz), description_present, due_date_set,
assignee_set, project_assigned, tags_present, custom_fields_filled, followers_present
**Anmerkung:** Nicht bearbeitbar. Dieser Ticket-Typ entsteht oft beim schnellen
Anlegen aus dem Kopf. Der gesamte Kontext fehlt. Muss vollständig nachgefüllt werden.

---

### Beispiel B3 — Falscher Assignee (Grenzfall)

```
Name: Technisches SEO-Audit Flachdach-Seiten
Notes: Vollständiger SEO-Audit für alle Flachdach-Seiten inkl. Core Web Vitals,
       Crawling-Fehler und Structured Data. Google Search Console Report.
Assignee: Felix Hoffmann
Due: 2025-05-01
Project: Dach_und_Holz SEO
Tags: seo, flachdach, audit
Custom Fields: Kanal=SEO, Priorität=Mittel
Followers: David Klein
```

**Routing:** Dach_und_Holz → dach_flachdach (Konfidenz: 0.82)
**Assignee-Plausibilität:** implausible
  - Felix hat: design, social_media, content_creation
  - Benötigt: seo, analytics, technical
  - Match: 0/3 relevante Domains
**Completeness:** 10/11 ✓
**Empfohlener Assignee:** David Klein (seo + analytics + technical ✓)
**Anmerkung:** Das Ticket ist inhaltlich vollständig, aber falsch zugewiesen.
Felix ist für Design/Social zuständig — SEO-Audits liegen klar außerhalb seiner Fähigkeiten.
David Klein (Koordinator + SEO-Experte) ist der richtige Assignee.

---

## KATEGORIE C — Grenzfälle und Sonderfälle

---

### Beispiel C1 — Cross-Cluster-Ticket (Ambiguität)

```
Name: PV-Anlage auf Flachdach — Kampagne Q3
Notes: Kombiniertes Kampagnenpaket: Werbung für Photovoltaik-Anlagen speziell
       auf Flachdächern. Inhalt: SEO-Text + Social Posts + E-Mail.
Assignee: (leer)
Due: 2025-07-15
Project: SHK+E Marketing
Tags: photovoltaik, flachdach, kampagne
```

**Routing-Ambiguität:**
- SHK+E Keywords: `photovoltaik`, `pv` → Score 0.6
- Dach_und_Holz Keywords: `flachdach` → Score 0.4
- Entscheidung: SHK+E gewinnt (höherer Score)
- Hinweis: Enthält Dach_und_Holz-Bezug — ggf. Koordination mit David Klein empfehlen

**Assignee:** Kein Assignee — Empfehlungen:
1. Ben Schmidt (Koordinator SHK+E, Paid Ads) — für Paid-Kanal
2. Anna Müller (SEO + Content) — für SEO-Text
3. Clara Weber (Email) — für Newsletter-Teil

**Anmerkung:** Kampagnen mit mehreren Kanälen brauchen oft mehrere Assignees.
Das System gibt drei Empfehlungen und markiert die Kanal-Aufteilung als manuellen Schritt.

---

### Beispiel C2 — Greta Fischer als Assignee (Warnung)

```
Name: Kampagnenplanung Jahresübersicht 2025 alle Cluster
Notes: Jahresübersicht aller geplanten Kampagnen und Budget-Aufteilung
       für 2025 über SHK+E, Dach_und_Holz und Baugewerbe.
Assignee: Greta Fischer
Due: 2025-01-31
Project: Jahresplanung 2025
Tags: jahresplanung, strategie, budget
```

**Routing:** Cross-Cluster / Strategie (kein spezifischer Cluster → unbekannt)
**Assignee-Plausibilität:** plausible
  - Greta: strategy + analytics + project_management ✓
  - Benötigt: strategy, project_management ✓
**Completeness:** 9/11 (fehlt: custom_fields_filled, followers_present)
**Anmerkung:** Dies ist einer der seltenen Fälle, bei dem Greta der richtige
Assignee ist. Das Ticket ist strategischer Natur, cluster-übergreifend und
passt exakt zu Gretas Profil. Kein operativer Content-Auftrag.

---

### Beispiel C3 — Vollständiges Ticket, Cluster `unbekannt`

```
Name: Pressemitteilung zum Unternehmensjubiläum
Notes: Wir feiern 30 Jahre Unternehmensgeschichte und brauchen eine
       Pressemitteilung für regionale Medien. Zielgruppe: Lokalpresse.
Assignee: Eva Braun
Due: 2025-09-01
Project: Unternehmenskommunikation 2025
Tags: presse, jubiläum, pr
Custom Fields: Kanal=PR
Followers: Greta Fischer
```

**Routing:** unbekannt (keine Cluster-Keywords erkannt)
**Assignee-Plausibilität:** questionable
  - Eva hat: copywriting, project_management ✓
  - Benötigt: copywriting ✓ — passt teilweise
  - Aber: PR/Presse ist kein definierter Skill-Domain
**Completeness:** 10/11 ✓
**Anmerkung:** PR-Tickets fallen aktuell in keinen definierten Cluster.
Das Ticket ist vollständig, aber das Routing gibt `unbekannt` zurück.
Empfehlung: Manuelle Eskalation an Bereichsleitung oder Cluster-Erweiterung
um PR als eigene Domain einplanen.
