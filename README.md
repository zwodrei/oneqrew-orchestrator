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
│   ├── employees/       # 7 employees with skill matrix
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
