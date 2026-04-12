"""
Asana Webhook Server — receives Asana events and triggers the Marketing Intelligence Layer.

Architecture:
  Asana → POST /asana/webhook → fetch full task → OrchestratorRunner → Asana comment

Endpoints:
  GET  /health          — liveness check
  POST /asana/webhook   — Asana webhook receiver (handshake + event processing)

Asana Webhook Protocol:
  1. Handshake: Asana sends X-Hook-Secret → mirror it back in response header + 200
  2. Events:    Asana sends events[] array → filter → fetch task → run orchestrator

Environment variables:
  ASANA_PERSONAL_ACCESS_TOKEN  — PAT for REST API calls
  ASANA_WEBHOOK_SECRET         — stored after registration (optional validation)
  WEBHOOK_PORT                 — default 8000
  DRY_RUN                      — inherited from settings
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

import httpx
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request, Response

from marketing_agent_engine.config.settings import settings
from marketing_agent_engine.runtime.orchestrator_runner import OrchestratorRunner

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title="Marketing Intelligence Layer — Asana Webhook", version="1.0.0")

# ---------------------------------------------------------------------------
# Idempotency cache (in-process, resets on restart — good enough for MVP)
# ---------------------------------------------------------------------------
_processed_events: set[str] = set()
_MAX_CACHE = 10_000


def _mark_processed(event_key: str) -> bool:
    """Returns True if event was already processed (duplicate). Marks it otherwise."""
    if event_key in _processed_events:
        return True
    if len(_processed_events) > _MAX_CACHE:
        _processed_events.clear()
    _processed_events.add(event_key)
    return False


# ---------------------------------------------------------------------------
# Asana REST helper
# ---------------------------------------------------------------------------

ASANA_API_BASE = "https://app.asana.com/api/1.0"
_TASK_FIELDS = (
    "gid,name,notes,due_on,assignee,assignee.name,projects,projects.name,"
    "tags,tags.name,custom_fields,custom_fields.name,custom_fields.display_value,"
    "followers,workspace,workspace.name,permalink_url"
)


def _asana_headers() -> dict[str, str]:
    pat = os.getenv("ASANA_PERSONAL_ACCESS_TOKEN", "")
    if not pat:
        raise RuntimeError("ASANA_PERSONAL_ACCESS_TOKEN not set")
    return {"Authorization": f"Bearer {pat}", "Accept": "application/json"}


def _fetch_task(task_gid: str) -> dict[str, Any]:
    """Fetch full task data from Asana REST API."""
    url = f"{ASANA_API_BASE}/tasks/{task_gid}"
    with httpx.Client(timeout=15) as client:
        resp = client.get(url, headers=_asana_headers(), params={"opt_fields": _TASK_FIELDS})
        resp.raise_for_status()
        return resp.json().get("data", {})


# ---------------------------------------------------------------------------
# Signature verification (HMAC-SHA256 — optional but recommended)
# ---------------------------------------------------------------------------

def _verify_signature(body: bytes, signature_header: str | None) -> bool:
    """
    Asana signs webhook payloads with HMAC-SHA256 using X-Hook-Secret as the key.
    If ASANA_WEBHOOK_SECRET is set, validate; otherwise skip (trust network).
    """
    secret = os.getenv("ASANA_WEBHOOK_SECRET", "")
    if not secret or not signature_header:
        return True
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)


# ---------------------------------------------------------------------------
# Event filtering
# ---------------------------------------------------------------------------

_RELEVANT_RESOURCE_TYPES = {"task"}
_RELEVANT_ACTIONS = {"added", "changed"}

# Only process 'added' events to avoid duplicate runs from 'changed' events
# that fire immediately after task creation (notes, html_notes, etc.).
_PRIMARY_ACTIONS = {"added"}


def _should_process(event: dict[str, Any]) -> tuple[bool, str]:
    """
    Returns (should_process, reason).
    Filters to task created events only (not changed).
    Asana sends 'added' + multiple 'changed' events on task creation.
    Processing only 'added' avoids duplicate runs.
    'changed' events are still relevant for later manual edits and can
    be enabled via ASANA_PROCESS_CHANGED=true env var.
    """
    resource = event.get("resource", {})
    resource_type = resource.get("resource_type", "")
    action = event.get("action", "")
    task_gid = resource.get("gid", "")

    if resource_type not in _RELEVANT_RESOURCE_TYPES:
        return False, f"skip resource_type={resource_type}"
    if action not in _RELEVANT_ACTIONS:
        return False, f"skip action={action}"
    if not task_gid:
        return False, "skip: no task gid"

    # Only process 'added' by default; 'changed' triggers too many dupes
    allowed_actions = _RELEVANT_ACTIONS if os.getenv("ASANA_PROCESS_CHANGED", "false").lower() == "true" else _PRIMARY_ACTIONS
    if action not in allowed_actions:
        return False, f"skip action={action} (not in allowed set)"

    return True, "ok"


# ---------------------------------------------------------------------------
# Background processor
# ---------------------------------------------------------------------------

def _process_event(task_gid: str, action: str, change: dict[str, Any]) -> None:
    """
    Fetch full task and run the orchestrator. Runs in background thread.
    """
    event_key = f"{task_gid}:{action}:{json.dumps(change, sort_keys=True)}"
    if _mark_processed(event_key):
        logger.info("Duplicate event skipped: %s", event_key)
        return

    logger.info(
        "Processing event: task_gid=%s action=%s dry_run=%s",
        task_gid, action, settings.dry_run,
    )

    try:
        task = _fetch_task(task_gid)
    except Exception as exc:
        logger.error("Failed to fetch task %s: %s", task_gid, exc)
        _log_trigger(task_gid, action, "fetch_error", str(exc))
        return

    # Skip tasks with no meaningful content (Asana may fire 'added' before
    # the user has filled in any fields)
    task_name = task.get("name", "") or ""
    task_notes = task.get("notes", "") or ""
    if len(task_name) < 3 and len(task_notes) < 10:
        logger.info(
            "Skipping empty/minimal task %s: name=%r notes=%r",
            task_gid, task_name[:50], task_notes[:50],
        )
        _log_trigger(task_gid, action, "skipped_empty", "Task has no meaningful content yet")
        return

    try:
        runner = OrchestratorRunner()
        result = runner.run(task)
        _log_trigger(task_gid, action, result.next_step, None, result.execution_mode)
        logger.info("Orchestrator result: %s", result.summary())
    except Exception as exc:
        logger.error("Orchestrator failed for task %s: %s", task_gid, exc, exc_info=True)
        _log_trigger(task_gid, action, "orchestrator_error", str(exc))


def _log_trigger(
    task_gid: str,
    action: str,
    next_step: str,
    error: str | None,
    execution_mode: str = "unknown",
) -> None:
    entry = {
        "task_id": task_gid,
        "trigger": "asana_webhook",
        "action": action,
        "next_step": next_step,
        "execution_mode": execution_mode,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    logger.info("WEBHOOK_TRIGGER %s", json.dumps(entry))


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "dry_run": str(settings.dry_run),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/asana/webhook")
async def asana_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hook_secret: str | None = Header(default=None),
    x_hook_signature: str | None = Header(default=None),
) -> Response:
    """
    Asana webhook endpoint.

    Phase 1 — Handshake:
      Asana sends X-Hook-Secret once during registration.
      We mirror it back in the response header and return 200.

    Phase 2 — Events:
      Asana sends events[] with task changes.
      We respond 200 immediately, then process in background.
    """
    body = await request.body()

    # ── Handshake ──────────────────────────────────────────────────────────
    if x_hook_secret:
        logger.info("Asana webhook handshake received. Storing secret.")
        # Persist secret for future signature verification
        os.environ["ASANA_WEBHOOK_SECRET"] = x_hook_secret
        return Response(
            status_code=200,
            headers={"X-Hook-Secret": x_hook_secret},
        )

    # ── Signature verification ──────────────────────────────────────────────
    if not _verify_signature(body, x_hook_signature):
        logger.warning("Webhook signature verification failed.")
        raise HTTPException(status_code=403, detail="Invalid signature")

    # ── Event processing ───────────────────────────────────────────────────
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        logger.error("Invalid JSON in webhook payload")
        raise HTTPException(status_code=400, detail="Invalid JSON")

    events: list[dict[str, Any]] = payload.get("events", [])
    logger.info("Received %d Asana event(s)", len(events))

    for event in events:
        should_process, reason = _should_process(event)
        if not should_process:
            logger.debug("Skipping event: %s — %s", event, reason)
            continue

        task_gid = event["resource"]["gid"]
        action = event.get("action", "")
        change = event.get("change", {})

        background_tasks.add_task(_process_event, task_gid, action, change)

    # Respond immediately — Asana requires < 10s response time
    return Response(status_code=200)


# ---------------------------------------------------------------------------
# Server entrypoint
# ---------------------------------------------------------------------------

def start() -> None:
    """Start the webhook server. Called via: uv run webhook_server"""
    import uvicorn

    # Railway sets PORT; fall back to WEBHOOK_PORT then 8000
    port = int(os.getenv("PORT") or os.getenv("WEBHOOK_PORT") or "8000")
    host = "0.0.0.0"  # always bind to all interfaces for Railway / containers
    reload = os.getenv("WEBHOOK_RELOAD", "false").lower() == "true"

    print(f"Starting Marketing Intelligence Layer webhook server on {host}:{port} (dry_run={settings.dry_run})")
    logger.info(
        "Starting webhook server on %s:%d (dry_run=%s)",
        host, port, settings.dry_run,
    )
    uvicorn.run(
        "marketing_agent_engine.webhook.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )


if __name__ == "__main__":
    start()
