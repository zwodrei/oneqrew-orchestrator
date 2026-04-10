# Completeness Policy

## SOURCE OF TRUTH
The deterministic logic in `/domain` ALWAYS overrides this document.
This file provides context only and must never contradict system logic.

---

## Zweck

Dieses Dokument beschreibt die 11 Vollständigkeitskriterien für Asana-Tickets
in menschenlesbarer Form. Es spiegelt die Logik in `domain/completeness_rules.py`
wider. Es ersetzt NICHT die deterministische Prüfung.

---

## Vollständigkeits-Score

```
Score = Anzahl bestandener Kriterien / 11
Bestanden (passed) = Score ≥ 0.8  →  mindestens 9 von 11 Kriterien erfüllt
```

---

## Die 11 Kriterien

### 1. `title_present` — Titel vorhanden und aussagekräftig
- Mindestlänge: 10 Zeichen
- Der Titel soll das Thema klar benennen
- ❌ Schlecht: „Content", „Aufgabe", „TODO"
- ✅ Gut: „SEO-Optimierung Wärmepumpen-Landingpage Q2"

### 2. `description_present` — Beschreibung vorhanden
- Mindestlänge: 30 Zeichen
- Beschreibt das Ziel, den Kontext oder die Anforderungen
- ❌ Schlecht: Kein Text / nur ein Satz ohne Substanz
- ✅ Gut: „Überarbeitung der Landingpage für Wärmepumpen. Ziel: Mehr Anfragen über organische Suche."

### 3. `due_date_set` — Fälligkeitsdatum gesetzt
- Feld `due_on` oder `due_at` muss befüllt sein
- ❌ Schlecht: Kein Datum → unklar, wann Aufgabe erledigt sein soll
- ✅ Gut: `2025-04-15`

### 4. `assignee_set` — Mitarbeiter zugewiesen
- Feld `assignee.gid` oder `assignee.name` muss vorhanden sein
- ❌ Schlecht: Kein Assignee → Aufgabe bleibt liegen
- ✅ Gut: Assignee mit GID oder Name verknüpft

### 5. `project_assigned` — Dem Projekt zugeordnet
- Mindestens ein Eintrag in `projects[]`
- ❌ Schlecht: Loose Task ohne Projekt-Kontext
- ✅ Gut: Ticket ist Teil eines definierten Marketingprojekts

### 6. `tags_present` — Tags gesetzt
- Mindestens ein Tag muss vorhanden sein
- Tags helfen bei Filterung, Reporting und Routing
- ❌ Schlecht: Keine Tags → schwer zu kategorisieren
- ✅ Gut: Tags wie `seo`, `wärmepumpe`, `q2-2025`, `landingpage`

### 7. `custom_fields_filled` — Custom Fields befüllt
- Mindestens ein Custom Field mit einem Wert ≠ null/leer
- Typische Custom Fields: Kampagnentyp, Priorität, Budget, Kanal
- ❌ Schlecht: Alle Custom Fields leer → keine Strukturdaten
- ✅ Gut: Mindestens Kampagnentyp oder Kanal befüllt

### 8. `followers_present` — Follower vorhanden
- Mindestens ein Follower muss eingetragen sein
- Follower = Stakeholder, der über Änderungen informiert werden soll
- ❌ Schlecht: Keine Follower → keine Transparenz über Fortschritt
- ✅ Gut: Team-Lead oder zuständiger Koordinator als Follower

### 9. `not_orphaned` — Kein verwaistes Ticket
- Ticket muss entweder ein Eltern-Ticket (`parent`) ODER ein Projekt haben
- ❌ Schlecht: Ticket ohne Projekt und ohne Parent → verliert sich
- ✅ Gut: Eingebettet in Projekt oder als Subtask eines Haupttickets

### 10. `workspace_set` — Workspace vorhanden
- Feld `workspace` muss gesetzt sein
- Normalerweise automatisch durch Asana gesetzt
- ❌ Schlecht: Fehlendes Workspace-Feld → Integrationsproblem
- ✅ Gut: Workspace-GID vorhanden

### 11. `permalink_present` — Permalink vorhanden
- Feld `permalink_url` muss mit `https://` beginnen
- ❌ Schlecht: Kein Link → kein Direktzugriff auf Ticket
- ✅ Gut: `https://app.asana.com/0/...`

---

## Typische Muster unvollständiger Tickets

### Schnell erstellte Tickets
- Titel kurz, keine Beschreibung, kein Datum, kein Assignee
- Score: ~0.27 (3/11)
- Empfehlung: Briefing nachfordern

### Planung ohne Ausführung
- Guter Titel, Beschreibung, Datum — aber kein Assignee, keine Tags
- Score: ~0.55 (6/11)
- Empfehlung: Assignee und Tags ergänzen

### Fast vollständig
- Alles befüllt bis auf Custom Fields und Follower
- Score: ~0.82 (9/11)
- Gilt als bestanden — aber Hinweise ausgeben

---

## Was dieses Dokument NICHT tut

- Es ändert keine Schwellwerte in `completeness_rules.py`
- Es fügt keine neuen Kriterien hinzu
- Es überschreibt keine berechneten Scores
