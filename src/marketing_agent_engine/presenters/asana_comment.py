"""
Asana comment builder.

Transforms a completed TaskState into a structured, human-readable
comment string ready to be posted to Asana.

Rules:
  - NO business logic
  - NO decisions
  - ONLY formatting from state data
  - No JSON inside the comment
  - No hallucination — every line sourced from state fields
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from marketing_agent_engine.flows.task_orchestrator_flow import TaskState

# ---------------------------------------------------------------------------
# Next-step descriptions (presentation only)
# ---------------------------------------------------------------------------

_NEXT_STEP_DESCRIPTIONS: dict[str, str] = {
    "blocked": (
        "Dieses Ticket ist unvollständig und kann nicht bearbeitet werden. "
        "Bitte alle fehlenden Pflichtfelder ergänzen, bevor das Ticket wieder "
        "in die Analyse-Queue eingestellt wird."
    ),
    "needs_information": (
        "Einige Informationen fehlen noch. Bitte die unten aufgeführten "
        "Felder ergänzen, damit die Analyse abgeschlossen werden kann."
    ),
    "needs_assignment": (
        "Das Ticket hat noch keinen Bearbeiter. Der Cluster-Koordinator "
        "sollte einen Mitarbeiter aus den Empfehlungen unten auswählen."
    ),
    "review": (
        "Die aktuelle Zuweisung ist möglicherweise nicht optimal. "
        "Der Cluster-Koordinator sollte die Zuweisung prüfen und ggf. anpassen."
    ),
    "ready": (
        "Das Ticket ist vollständig und korrekt zugewiesen. "
        "Es kann unmittelbar in die Bearbeitung übergehen."
    ),
    "": "Status unbekannt — bitte manuelle Überprüfung.",
}

_WORKFLOW_STATE_LABELS: dict[str, str] = {
    "blocked": "🚫 Blockiert",
    "needs_information": "⚠️ Informationen fehlen",
    "needs_assignment": "👤 Zuweisung fehlt",
    "review": "🔍 Überprüfung erforderlich",
    "ready": "✅ Bereit",
    "": "❓ Unbekannt",
}

_OWNER_LABELS: dict[str, str] = {
    "requester": "Ersteller des Tickets",
    "coordinator": "Cluster-Koordinator",
    "system": "System (automatisch)",
}


# ---------------------------------------------------------------------------
# Public builder
# ---------------------------------------------------------------------------

def build_asana_comment(state: "TaskState") -> str:
    """
    Build a formatted Asana comment from a completed TaskState.
    Returns a plain-text string with emoji formatting (Asana renders these).
    """
    lines: list[str] = []

    # Header
    lines += [
        "🔍 **Marketing-Analyse**",
        f"_(Ausführungsmodus: {state.execution_mode})_",
        "",
    ]

    # Workflow state
    workflow_label = _WORKFLOW_STATE_LABELS.get(state.next_step, "❓ Unbekannt")
    lines.append(f"📊 **Workflow-Zustand**: {workflow_label}")

    # Cluster / BU
    routing = state.routing
    if routing:
        cluster_val = routing.cluster.value if routing.cluster else "Unbekannt"
        bu_val = routing.business_unit.display_name if routing.business_unit else "—"
        conf_pct = f"{routing.confidence:.0%}"
        coordinator = routing.cluster_coordinator_id or "—"
        lines.append(f"🏢 **Business Unit / Cluster**: {cluster_val} › {bu_val} (Konfidenz: {conf_pct})")
        lines.append(f"   📍 Koordinator: {coordinator}")
    else:
        lines.append("🏢 **Business Unit / Cluster**: Nicht ermittelbar")

    # Assignee status
    assignment = state.assignment
    if assignment and assignment.current_assignee_verdict:
        av = assignment.current_assignee_verdict
        name = av.display_name or "Unbekannt"
        verdict = av.verdict.value
        verdict_icons = {
            "plausible": "✅",
            "questionable": "⚠️",
            "implausible": "❌",
            "unknown": "❓",
        }
        icon = verdict_icons.get(verdict, "❓")
        lines.append(f"👤 **Verantwortlichkeit**: {name} — {icon} {verdict.capitalize()}")
        if av.explanation:
            lines.append(f"   _{av.explanation}_")
    elif assignment and assignment.needs_reassignment:
        lines.append("👤 **Verantwortlichkeit**: Kein Bearbeiter zugewiesen")
    else:
        lines.append("👤 **Verantwortlichkeit**: —")

    # Skill match / recommendations
    if assignment and assignment.recommendations:
        top = assignment.recommendations[0]
        skills = ", ".join(top.matched_skills) if top.matched_skills else "—"
        lines.append(
            f"🧠 **Skill-Match**: {top.display_name} "
            f"(Konfidenz: {top.confidence:.0%}, Skills: {skills})"
        )
        if len(assignment.recommendations) > 1:
            others = ", ".join(r.display_name for r in assignment.recommendations[1:])
            lines.append(f"   Weitere Kandidaten: {others}")
    else:
        lines.append("🧠 **Skill-Match**: Keine Empfehlung verfügbar")

    # Completeness
    completeness = state.completeness
    if completeness:
        score_pct = f"{completeness.score:.0%}"
        passed_icon = "✅" if completeness.passed else "❌"
        passed_count = sum(1 for f in completeness.flags if f.passed)
        total = len(completeness.flags)
        lines.append(
            f"📦 **Vollständigkeit**: {passed_icon} {score_pct} "
            f"({passed_count}/{total} Kriterien erfüllt)"
        )
    else:
        lines.append("📦 **Vollständigkeit**: Nicht bewertet")

    # Missing information
    missing = completeness.missing if completeness else []
    if missing:
        lines.append("")
        lines.append("❗ **Fehlende Informationen**:")
        for m in missing:
            lines.append(f"  - `{m}`")

    # Who should supply missing info
    if state.action_plan:
        owner_actions: dict[str, list[str]] = {}
        for item in state.action_plan:
            owner_key = item.owner
            label = _OWNER_LABELS.get(owner_key, owner_key)
            owner_actions.setdefault(label, []).append(item.action)

        lines.append("")
        lines.append("🧾 **Wer liefern sollte**:")
        for owner_label, actions in owner_actions.items():
            for act in actions:
                lines.append(f"  - **{owner_label}**: {act}")

    # Decision trace
    trace = state.decision_trace
    if any(trace.values()):
        lines.append("")
        lines.append("🔎 **Entscheidungsbegründung**:")
        if trace.get("routing"):
            lines.append(f"  - _Routing_: {trace['routing']}")
        if trace.get("assignment"):
            lines.append(f"  - _Zuweisung_: {trace['assignment']}")
        if trace.get("completeness"):
            lines.append(f"  - _Vollständigkeit_: {trace['completeness']}")

    # Next step
    next_desc = _NEXT_STEP_DESCRIPTIONS.get(state.next_step, _NEXT_STEP_DESCRIPTIONS[""])
    lines += [
        "",
        "📋 **Nächster Schritt**:",
        f"  {next_desc}",
    ]

    # Dry-run notice
    if state.execution_mode == "dry_run":
        lines += [
            "",
            "---",
            "_⚠️ DRY RUN — Diese Analyse wurde nicht an Asana übermittelt._",
        ]

    return "\n".join(lines)
