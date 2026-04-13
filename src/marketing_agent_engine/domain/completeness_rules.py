"""
Completeness rules: evaluate an Asana ticket dict against 11 defined criteria.

Each criterion maps to a named flag in CompletenessResult. A ticket scores
1 point per passed criterion; total score = passed / 11.
"""

from __future__ import annotations

from typing import Any, Optional

from .schemas import CompletenessFlag, CompletenessResult

# Minimum character counts for text fields
_MIN_TITLE_LEN = 10
_MIN_DESCRIPTION_LEN = 30
_MIN_NOTES_LEN = 20


def _flag(criterion: str, passed: bool, value: Any = None, note: str = "") -> CompletenessFlag:
    return CompletenessFlag(criterion=criterion, passed=passed, value=value, note=note)


def check_completeness(ticket: dict[str, Any]) -> CompletenessResult:
    """
    Evaluate a raw Asana ticket dict against 11 completeness criteria.

    Expected keys (all optional at input level):
        name, notes, due_on, assignee, projects, tags,
        custom_fields, followers, parent, workspace, permalink_url
    """
    flags: list[CompletenessFlag] = []

    # 1. Title present and meaningful
    name: str = ticket.get("name", "") or ""
    title_is_valid = len(name.strip()) >= _MIN_TITLE_LEN
    flags.append(_flag(
        "title_present",
        title_is_valid,
        value=name.strip() or None,
        note="Title must be at least 10 characters." if not title_is_valid else "",
    ))

    # 2. Description / notes present. If html_notes is present, check that instead.
    notes: str = ticket.get("notes", "") or ""
    html_notes: str = ticket.get("html_notes", "") or ""
    desc_content = html_notes if html_notes else notes
    desc_is_valid = len(desc_content.strip()) >= _MIN_DESCRIPTION_LEN
    flags.append(_flag(
        "description_present",
        desc_is_valid,
        value=bool(desc_content.strip()),
        note="Notes/Description field should have at least 30 characters." if not desc_is_valid else "",
    ))

    # 3. Due date set
    due_on: Optional[str] = ticket.get("due_on") or ticket.get("due_at")
    flags.append(_flag(
        "due_date_set",
        bool(due_on),
        value=due_on,
        note="No due date found." if not due_on else "",
    ))

    # 4. Assignee set
    assignee = ticket.get("assignee")
    assignee_set = bool(assignee and (assignee.get("gid") or assignee.get("name")))
    flags.append(_flag(
        "assignee_set",
        assignee_set,
        value=assignee,
        note="No assignee." if not assignee_set else "",
    ))

    # 5. Project membership
    projects = ticket.get("projects") or []
    flags.append(_flag(
        "project_assigned",
        len(projects) > 0,
        value=[p.get("name") for p in projects if isinstance(p, dict)],
        note="Task not linked to any project." if not projects else "",
    ))

    # 6. At least one tag
    tags = ticket.get("tags") or []
    flags.append(_flag(
        "tags_present",
        len(tags) > 0,
        value=[t.get("name") for t in tags if isinstance(t, dict)],
        note="No tags set." if not tags else "",
    ))

    # 7. Custom fields populated (at least one non-null value)
    custom_fields: list[dict] = ticket.get("custom_fields") or []
    filled_cf = [
        cf for cf in custom_fields
        if isinstance(cf, dict) and cf.get("display_value") not in (None, "", "—")
    ]
    flags.append(_flag(
        "custom_fields_filled",
        len(filled_cf) > 0,
        value=len(filled_cf),
        note="No custom fields have values." if not filled_cf else "",
    ))

    # 8. Has at least one follower
    followers = ticket.get("followers") or []
    flags.append(_flag(
        "followers_present",
        len(followers) > 0,
        value=len(followers),
        note="No followers on ticket." if not followers else "",
    ))

    # 9. Has a parent task or is part of a project (not a loose orphan)
    parent = ticket.get("parent")
    has_parent_or_project = bool(parent) or len(projects) > 0
    flags.append(_flag(
        "not_orphaned",
        has_parent_or_project,
        value={"parent": bool(parent), "in_project": len(projects) > 0},
        note="Task has no parent and no project." if not has_parent_or_project else "",
    ))

    # 10. Workspace is set
    workspace = ticket.get("workspace")
    flags.append(_flag(
        "workspace_set",
        bool(workspace),
        value=workspace,
        note="No workspace found." if not workspace else "",
    ))

    # 11. Permalink / URL accessible (structural presence only)
    permalink = ticket.get("permalink_url") or ""
    flags.append(_flag(
        "permalink_present",
        permalink.startswith("https://"),
        value=permalink or None,
        note="No valid permalink." if not permalink.startswith("https://") else "",
    ))

    passed_count = sum(1 for f in flags if f.passed)
    score = round(passed_count / len(flags), 3)
    missing = [f.criterion for f in flags if not f.passed]
    warnings = [f.note for f in flags if not f.passed and f.note]

    return CompletenessResult(
        score=score,
        flags=flags,
        missing=missing,
        warnings=warnings,
    )
