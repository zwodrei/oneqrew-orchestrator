# Marketing Agent Engine

A production-ready CrewAI-based orchestration system that analyzes Asana marketing tickets, performs routing/assignment/completeness analysis, and operates with strict **dry-run-first** safety semantics.

---

## Quick Start

```bash
cd oneqrew

# Copy and configure environment
cp .env.example .env
# Edit .env: set OPENAI_API_KEY and MODEL=openai/gpt-4.1

# Full pipeline with LLM (demo ticket)
uv run --prerelease=allow crewai run

# Smoke test without LLM (uses _analysis_override hook)
uv run --prerelease=allow python scripts/run_local_orchestrator.py

# Test suite (no LLM, no Asana required)
uv run --prerelease=allow pytest tests/ -v
```

---

## Requirements

| Requirement | Value |
|---|---|
| Python | `>=3.10, <3.14` (tested on 3.13) |
| Package manager | `uv` with `--prerelease=allow` |
| LLM | OpenAI `gpt-4.1` (Anthropic explicitly blocked) |
| Asana | Optional — dry-run works without real credentials |

---

## Architecture

```
Input (Asana ticket dict)
    │
    ▼
TaskOrchestratorFlow          ← Control layer (crewai.flow)
    │   ├── run_analysis()    ← Delegates to AnalysisCrew (4 agents)
    │   ├── make_decision()   ← Deterministic thresholds (no LLM)
    │   └── route_next()      ← Router → 5 handlers
    │
    ▼
Domain Layer                  ← Pure Python, no LLM, source of truth
    ├── routing_rules.py      ← BU + cluster keyword scoring
    ├── completeness_rules.py ← 11-criteria ticket evaluation
    ├── skill_matching.py     ← Skill domain → employee matching
    └── assignment_rules.py   ← Combined routing + skill pipeline
    │
    ▼
Presenters
    ├── asana_comment.py      ← German Markdown comment for Asana
    └── json_output.py        ← Machine-readable structured dict
    │
    ▼
OrchestratorRunner            ← Wires Flow → Presenters → MCP
    │
    ▼
GuardedMCPClient              ← DRY_RUN guard layer
    └── create_comment()      ← Only write used (Phase 1)
```

### Key architecture decisions

1. **Two-layer knowledge**: CrewAI knowledge files for agent context; deterministic Python resolvers for all business logic. Knowledge files never override domain layer.
2. **Flow orchestrates, Crew analyzes**: `TaskOrchestratorFlow` is the control layer. `AnalysisCrew` is pure analysis with no business logic.
3. **MCP only in runner**: Agents never call MCP. Presenters never call MCP. Only `OrchestratorRunner._execute_actions()` touches `GuardedMCPClient`.
4. **`_analysis_override` test hook**: Set `flow._analysis_override = lambda ticket: dict` to bypass AnalysisCrew without LLM.
5. **Phase 1 restriction**: Only `create_comment` is wired. `update_task` is intentionally omitted.

---

## Decision Logic

```
completeness_score < 0.50  → blocked
completeness_score < 0.70  → needs_information
no assignee                → needs_assignment
implausible / questionable → review            (requires_human: true)
all green                  → ready
```

All thresholds are constants in `flows/task_orchestrator_flow.py`.

---

## Knowledge Base & Skill Matrix

### Employee knowledge files (`knowledge/employees/`)

One JSON file per team member (e.g. `knowledge/employees/maren_hoyer.json`) with:

| Field | Description |
|---|---|
| `employee_id` | Internal ID (e.g. `emp_001`) |
| `name` / `role` | Display name and job title |
| `ai_readiness` | `AI-Pioneer` / `AI-Erfahren` / `AI-Bereit` / `AI-Novice` |
| `primary_tasks` | List of main task types |
| `skills` / `channels` | Tool/channel expertise |
| `skill_domains` | Machine-readable `SkillDomain` values for routing |

`knowledge/employees/employees.md` contains a prose description for each of the 14 real team members (replaces fictional placeholder personas).

### Skill matrix (`knowledge/team_skill_map.json`)

Central mapping `task_category → { primary, secondary, coordinator }` with `ai_readiness_map` per person.

| Key | Example |
|---|---|
| `WordPress/Webmaster` | `{ "primary": ["Janosch Niemeyer"], "secondary": ["Sandra Hoppe"] }` |
| `HubSpot/Marketing-Automation` | `{ "primary": ["Matteo Diehl"], ... }` |

`ai_readiness_levels` section documents levels 1–4 (Novice → Pioneer).

### AI-Readiness in agent logic

The `analyse_assignment()` function in `domain/assignment_rules.py` now:

1. Calls `categorize_task(title, notes)` → `TaskCategory`
2. Calls `determine_ai_readiness_required(title, notes, category)` → `AIReadiness`
3. Passes `min_ai_readiness` to `recommend_assignees()` — novices are filtered out for AI-intensive tasks
4. Passes `required_ai_readiness` to `evaluate_assignee_plausibility()` — sets `human_review_required=True` on mismatch

New fields on `AssignmentAnalysis`:

| Field | Description |
|---|---|
| `task_category` | Detected task category (e.g. `"HubSpot/Marketing-Automation"`) |
| `ai_readiness_required` | Minimum AI-readiness for the task |
| `assignee_readiness` | AI-readiness level of the current assignee |
| `recommended_assignee_ai_level` | AI-readiness of the top-ranked recommendation |
| `assigned_by_skill_matrix` | `true` when no assignee was set and the matrix was used to recommend |

**Routing logic:**
- Tasks requiring `AI-Erfahren` or higher are only recommended to experienced/pioneer employees
- `AI-Novice` assignees always trigger `human_review_required=True`
- If an assignee's AI-readiness is below the task requirement → `needs_reassignment=True`

---

## Brand Guides (`knowledge/brand_guides/`)

17 PDF brand guides for each business unit, loaded into the CrewAI knowledge base via `PDFKnowledgeSource`.

| File | Business Unit | Cluster |
|---|---|---|
| `AAA-EDV.pdf` | AAA-EDV | Baugewerbe |
| `ACCANTUM.pdf` | ACCANTUM | SHK+E |
| `BAUFAKTURA.pdf` | BAUFAKTURA | Baugewerbe |
| `BLUESOLUTION.pdf` | blue:solution | SHK+E |
| `CP-PRO.pdf` | CP-PRO | Dach & Holz |
| `DIGI.pdf` | DIGI | Dach & Holz |
| `EXTRAGROUP.pdf` | EXTRAGROUP | Dach & Holz |
| `MEXXSOFT.pdf` | MEXXSOFT | SHK+E |
| `MSOFT.pdf` | M-SOFT | Dach & Holz |
| `MyOneQrew.pdf` | OneQrew | cross-cluster |
| `PFISTERER.pdf` | PFISTERER | SHK+E |
| `PINNCALC.pdf` | PINNCALC | Dach & Holz |
| `PRAKOLM.pdf` | PRAKOLM | Baugewerbe |
| `QOMET.pdf` | QOMET | SHK+E |
| `SCIREUM.pdf` | SCIREUM | Baugewerbe |
| `SYKASOFT.pdf` | SYKASOFT | SHK+E |
| `TAIFUN.pdf` | TAIFUN | SHK+E |

### Integration

- **Index**: `knowledge/brand_guides/index.json` maps each PDF to its BU and cluster
- **Loading**: `AnalysisCrew._build_knowledge_sources()` loads all 17 PDFs via `PDFKnowledgeSource` alongside the employee JSON files
- **Agent access**: All four agents in the AnalysisCrew can query brand guide content through CrewAI's built-in RAG

---

## Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...
MODEL=openai/gpt-4.1

# Safety (defaults to true)
DRY_RUN=true          # false → real Asana writes

# Asana MCP (only needed for live mode)
ASANA_MCP_APP_CLIENT_ID=...
ASANA_MCP_APP_CLIENT_SECRET=...

# Never set — explicitly blocked
# ANTHROPIC_API_KEY=...  ← raises RuntimeError
```

---

## Project Structure

```
oneqrew/
├── src/marketing_agent_engine/
│   ├── config/          # Settings, LLM provider guard
│   ├── domain/          # Deterministic business logic (source of truth)
│   ├── crews/           # AnalysisCrew: 4 agents + 4 tasks
│   ├── flows/           # TaskOrchestratorFlow (control layer)
│   ├── mcp/             # Asana MCP client + GuardedMCPClient
│   ├── presenters/      # Comment + JSON output builders
│   ├── runtime/         # OrchestratorRunner (pipeline entry point)
│   └── main.py          # crewai run entry point
├── knowledge/
│   ├── employees/       # 14 real team members (JSON + employees.md overview)
│   ├── brand_guides/    # 17 PDF brand guides + index.json
│   ├── business_units/  # 12 BUs across 3 clusters
│   ├── policies/        # Routing, assignment, completeness (SOURCE OF TRUTH notices)
│   └── context/         # 6 annotated example tickets
├── tests/               # 138 tests, no LLM required
│   ├── test_domain.py
│   ├── test_flow.py
│   ├── test_dry_run.py
│   ├── test_presenters.py
│   └── test_end_to_end.py
└── scripts/
    └── run_local_orchestrator.py
```

---

## Running Tests

```bash
cd oneqrew
uv run --prerelease=allow pytest tests/ -v
```

- **138 tests** across 5 files
+- **`test_skill_matrix.py`** now includes `TestAnalyseAssignmentNewFields` covering AI-readiness routing, `assigned_by_skill_matrix`, and `recommended_assignee_ai_level`.
- No LLM calls, no Asana connection
- Covers all 5 decision branches, all MCP guard rules, all presenter fields
- Uses `_analysis_override` hook for deterministic flow tests

---

## Safety Guarantees

| Guarantee | Mechanism |
|---|---|
| No Anthropic models | `config/llm.py` raises `RuntimeError` on detection |
| DRY_RUN by default | `settings.dry_run = True` unless explicitly overridden |
| No accidental Asana writes | `GuardedMCPClient` intercepts all writes when `dry_run=True` |
| Read tools always allowed | `READ_TOOLS` frozenset bypasses guard unconditionally |
| No LLM in critical path | Decision logic in `make_decision()` is pure Python |
