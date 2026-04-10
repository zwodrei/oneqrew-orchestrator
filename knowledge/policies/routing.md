# Routing Policy

## SOURCE OF TRUTH
The deterministic logic in `/domain` ALWAYS overrides this document.
This file provides context only and must never contradict system logic.

---

## Zweck

Dieses Dokument erklärt die Routing-Regeln in menschenlesbarer Form.
Es spiegelt die Logik in `domain/routing_rules.py` wider und dient Agenten
als Kontext-Referenz. Es ersetzt NICHT die deterministische Logik.

---

## Grundprinzip

Jedes Ticket gehört genau einem **Cluster**. Ein Cluster besteht aus
mehreren **Business Units (BUs)**. Die Zuordnung erfolgt in dieser Reihenfolge:

```
1. Asana Project GID → direkte BU-Zuordnung (höchste Priorität)
2. Keyword-Scoring → beste BU aus Titel + Beschreibung
3. Cluster-Keyword-Scoring → Fallback auf Cluster-Ebene
4. unbekannt → wenn keine Zuordnung möglich
```

---

## Cluster-Übersicht

| Cluster | Kern-Keywords | Koordinator |
|---------|--------------|-------------|
| SHK+E | shk, sanitär, heizung, wärmepumpe, elektro, pv, wallbox | Ben Schmidt |
| Dach_und_Holz | dach, dachdeckung, ziegel, flachdach, holzbau, zimmerei | David Klein |
| Baugewerbe | rohbau, ausbau, tiefbau, maler, mauerwerk, trockenbau | Eva Braun |
| unbekannt | — | — |

---

## Routing-Entscheidungsbaum

### Schritt 1: Asana Project GID vorhanden?
- Ja → BU direkt aus GID → Cluster aus BU → fertig (Konfidenz 1.0)
- Nein → weiter zu Schritt 2

### Schritt 2: BU-Keyword-Scoring
- Kombiniere Titel + Beschreibung
- Normalisiere (Kleinbuchstaben, keine Sonderzeichen)
- Zähle Treffer gegen BU-Key-Terms und Aliases
- Beste BU mit Score > Mindestschwelle → Route zu dieser BU
- Kein Treffer über Schwelle → weiter zu Schritt 3

### Schritt 3: Cluster-Fallback-Scoring
- Wende dasselbe Scoring auf Cluster-Key-Terms an
- Beste Übereinstimmung → Route zu diesem Cluster ohne BU
- Immer noch kein Treffer → Cluster `unbekannt`

### Schritt 4: Koordinator-Zuordnung
- Ermittle Koordinator des Ziel-Clusters
- Koordinator wird als Eskalationspunkt notiert (kein automatisches Assignment)

---

## Konfidenz-Interpretation

| Konfidenz | Bedeutung |
|-----------|-----------|
| 1.0 | GID-basierte Zuordnung — sicher |
| 0.7–0.9 | Starke Keyword-Übereinstimmung — sehr wahrscheinlich korrekt |
| 0.4–0.69 | Moderate Übereinstimmung — zur Überprüfung markieren |
| 0.1–0.39 | Schwache Übereinstimmung — manuell prüfen |
| 0.0 | Keine Zuordnung — Cluster `unbekannt` |

---

## Spezialfälle

### Ticket mit mehreren Cluster-Bezügen
Wenn Titel und Beschreibung Begriffe aus mehreren Clustern enthalten
(z.B. „PV-Anlage auf Flachdach"), gilt:
- Primärer Cluster wird durch die **Hauptaufgabe** bestimmt
- Sekundäre Keywords erhöhen nur den Konfidenz-Score nicht
- Im Zweifel: Cluster mit mehr Keyword-Hits gewinnt

### Ticket ohne Beschreibung
- Nur Titel wird für Scoring verwendet
- Konfidenz wird maximal auf 0.5 begrenzt (kein Volltext vorhanden)
- Hinweis auf fehlende Beschreibung im Completeness-Check

### Ticket mit unbekanntem Cluster
- Cluster `unbekannt` wird gesetzt
- Kein Koordinator zugewiesen
- Flag wird im Completeness-Ergebnis vermerkt
- Empfehlung: Ticket an zuständigen Bereichsleiter eskalieren

---

## Was dieses Dokument NICHT tut

- Es ändert keine Routing-Entscheidungen zur Laufzeit
- Es überschreibt nicht die Scoring-Logik in `routing_rules.py`
- Es fügt keine neuen Business Units oder Cluster hinzu
