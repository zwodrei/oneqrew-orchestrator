# Architecture — Marketing Agent Engine

## Overview

The Marketing Agent Engine is a multi-layer orchestration system. Each layer has a single, bounded responsibility. No layer may call below or above its designated neighbor.

```
                    ┌─────────────────────────────────┐
                    │        External Input            │
                    │  (Asana ticket dict / mock)      │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │     TaskOrchestratorFlow         │
                    │  crewai.flow — Control Layer     │
                    │  - state machine (5 handlers)    │
                    │  - deterministic decision logic  │
                    │  - NO business logic             │
                    └──────────────┬──────────────────┘
                      delegates    │    reads result
                    ┌──────────────▼──────────────────┐
                    │        AnalysisCrew              │
                    │  4 agents: routing, assignment,  │
                    │  completeness, synthesis         │
                    │  - pure analysis only            │
                    │  - no MCP calls                  │
                    │  - uses domain tools             │
                    └──────────────┬──────────────────┘
                      calls        │
                    ┌──────────────▼──────────────────┐
                    │         Domain Layer             │
                    │  routing_rules.py                │
                    │  completeness_rules.py           │
                    │  skill_matching.py               │
                    │  assignment_rules.py             │
                    │  - pure Python, no LLM           │
                    │  - source of truth               │
                    └──────────────┬──────────────────┘
                                   │ state passed to
                    ┌──────────────▼──────────────────┐
                    │         Presenters               │
                    │  asana_comment.py → str          │
                    │  json_output.py   → dict         │
                    │  - formatting ONLY               │
                    │  - no decisions, no side effects │
                    └──────────────┬──────────────────┘
                                   │ outputs passed to
                    ┌──────────────▼──────────────────┐
                    │      OrchestratorRunner          │
                    │  - wires all layers together     │
                    │  - ONLY place that calls MCP     │
                    │  - structured logging (Phase C)  │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │      GuardedMCPClient            │
                    │  - DRY_RUN guard (all writes)    │
                    │  - READ tools always pass-thru   │
                    │  - Phase 1: create_comment only  │
                    └─────────────────────────────────┘
```

---

## Component Reference

### `config/settings.py`
- Reads `DRY_RUN`, `MODEL`, `CREWAI_API_KEY` from `.env`
- `settings.dry_run` defaults to `True`

### `config/llm.py`
- `get_default_llm()` — raises `RuntimeError` if Anthropic model or key is detected
- Enforced hard constraint: no Anthropic models ever

### `domain/schemas.py`
- `ClusterSlug`, `SkillDomain`, `PlausibilityVerdict` enums
- `RoutingResult`, `CompletenessResult` (with `@computed_field passed`), `AssigneePlausibilityResult`, `AssignmentAnalysis`, `BusinessUnitMatch`

### `domain/routing_rules.py`
- `route_ticket(title, description, gid)` → `RoutingResult`
- Keyword scoring → BU → cluster → coordinator
- GID shortcut: if `asana_project_gid` matches a BU exactly, confidence = 1.0

### `domain/completeness_rules.py`
- `check_completeness(ticket)` → `CompletenessResult`
- 11 criteria: title, description, due_date, assignee, project, tags, custom_fields, followers, not_orphaned, workspace, permalink
- Score = passed / 11

### `domain/skill_matching.py`
- `resolve_skill_domain(title, description)` → `list[SkillDomain]`
- `recommend_assignees(title, description, cluster_slug, top_n)` → `list[AssigneeRecommendation]`
- `evaluate_assignee_plausibility(employee_id, title, description)` → `AssigneePlausibilityResult`

### `domain/employees.py`
- 7 employees with skill domains, cluster membership, coordinator flags
- O(1) lookups: `get_employee_by_id()`, `get_employee_by_email()`, `get_employee_by_asana_gid()`

### `domain/business_units.py`
- 12 BUs across 3 clusters with slugs, aliases, key_terms

### `domain/clusters.py`
- 4 clusters: `SHK+E`, `Dach_und_Holz`, `Baugewerbe`, `unbekannt`
- Each cluster has coordinator_employee_id and key_terms

### `crews/analysis_crew/crew.py`
- `AnalysisCrew` — `@CrewBase` decorated class
- 4 agents: `routing_analyst`, `assignment_analyst`, `completeness_analyst`, `decision_synthesizer`
- `.analyse(ticket)` → parsed dict with routing, assignment, completeness blocks
- JSON extraction with markdown fence stripping

### `flows/task_orchestrator_flow.py`
- `TaskOrchestratorFlow(Flow[TaskState])`
- 5-step chain: `start_flow` → `run_analysis` → `make_decision` → `route_next` → handler
- `_analysis_override` hook: set to `lambda ticket: dict` to bypass crew
- `_finalize()` adds `requires_human: True` for review branch (Phase E)

### `mcp/guarded_client.py`
- `GuardedMCPClient(dry_run, mcp_client)`
- `create_comment()`, `update_task()` — blocked in dry-run → `SimulatedWriteResponse`
- `get_task_by_id()`, `get_comments()` — always pass through
- `make_guarded_client()` factory reads `settings.dry_run`

### `presenters/asana_comment.py`
- `build_asana_comment(state)` → German Markdown string
- Fields: workflow state, cluster/BU, assignee verdict, skill match, completeness score, missing fields, action plan, decision trace, next-step description
- DRY RUN footer when `execution_mode == "dry_run"`

### `presenters/json_output.py`
- `build_json_output(state)` → dict (schema_version 1.0)
- Fields: routing, assignment, completeness, decision (with confidence_summary), actions (with severity), decision_trace, simulated flag

### `runtime/orchestrator_runner.py`
- `OrchestratorRunner` — full pipeline entry point
- `RunResult` dataclass with `simulated` property and `summary()` method
- `_log_structured()` — emits one JSON log line per run (Phase C)
- Phase 1 restriction: only `create_comment` called

---

## Decision Priority Order

```python
COMPLETENESS_BLOCK_THRESHOLD = 0.50
COMPLETENESS_WARN_THRESHOLD  = 0.70

if score < 0.50:              → "blocked"
elif score < 0.70:            → "needs_information"
elif not assignee_present:    → "needs_assignment"
elif verdict in (IMPLAUSIBLE, QUESTIONABLE): → "review"  # requires_human: true
else:                         → "ready"
```

---

## Data Flow (single ticket)

```
raw ticket dict
  → flow.state.raw_input = ticket
  → flow.kickoff()
    → start_flow()         sets task_id, execution_mode, timestamp
    → run_analysis()       calls AnalysisCrew (or _analysis_override)
                           populates state.routing / .assignment / .completeness
    → make_decision()      deterministic threshold logic
                           sets state.next_step, state.decision_trace
    → route_next()         returns state.next_step string
    → handle_*()           builds state.action_plan
    → _finalize()          writes final_decision dict (+ requires_human)
  → build_asana_comment(state) → str
  → build_json_output(state)   → dict
  → GuardedMCPClient.create_comment(task_id, comment)
    → DRY_RUN? SimulatedWriteResponse : real MCP call
  → RunResult(task_id, next_step, execution_mode, comment, json_output, mcp_responses)
```

---

## Extension Guide

### Adding a new decision branch
1. Add threshold constant to `task_orchestrator_flow.py`
2. Add handler method with `@listen("new_branch")`
3. Update `_NEXT_STEP_DESCRIPTIONS` in `asana_comment.py`
4. Update `_NEXT_STEP_ACTION_TYPES` and `_NEXT_STEP_OVERALL_STATUS` in `json_output.py`
5. Add test in `tests/test_flow.py`

### Adding a new MCP write tool (Phase 2+)
1. Add request model to `mcp/tools.py`, add to `WRITE_TOOLS`
2. Add method to `GuardedMCPClient` following existing pattern
3. Wire in `OrchestratorRunner._execute_actions()` under correct next_step

### Adding a new employee
1. Add `Employee(...)` to `EMPLOYEES` list in `domain/employees.py`
2. Update knowledge file `knowledge/employees/employees.md`
3. Tests will automatically exercise the new employee via `recommend_assignees()`

### Adding a new business unit
1. Add `BusinessUnit(...)` to `BUSINESS_UNITS` in `domain/business_units.py`
2. Add to appropriate cluster's `business_unit_slugs` in `domain/clusters.py`
3. Add knowledge file in `knowledge/business_units/`

---

## Hardening Summary (Phases A–F)

| Phase | Status | Implementation |
|---|---|---|
| A — Test Suite | ✅ 138 tests passing | `tests/` — 5 files, all branches covered |
| B — Error Handling | ✅ | Flow catches analysis errors → `blocked`; MCP client never crashes |
| C — Structured Logging | ✅ | `_log_structured()` in runner → JSON log per run |
| D — Performance Safety | ✅ | `_analysis_override` prevents LLM in tests; crew runs once per kickoff |
| E — Human-in-the-Loop | ✅ | `requires_human: True` in `final_decision` for `review` branch |
| F — Final Validation | ✅ | Flow controls all decisions; MCP fully guarded; dry-run global |
