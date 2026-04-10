#!/usr/bin/env python
"""
Register an Asana webhook for a project.

Usage:
    uv run --prerelease=allow python scripts/register_asana_webhook.py \
        --project-gid 1234567890 \
        --target-url https://abc123.ngrok-free.app/asana/webhook

Environment variables required:
    ASANA_PERSONAL_ACCESS_TOKEN

The script:
  1. Creates the webhook via Asana REST API
  2. Prints the webhook_id and gid (save these!)
  3. The handshake is handled automatically by the running server

Asana docs: https://developers.asana.com/docs/webhooks-guide
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv()

ASANA_API_BASE = "https://app.asana.com/api/1.0"


def register_webhook(project_gid: str, target_url: str) -> dict:
    pat = os.getenv("ASANA_PERSONAL_ACCESS_TOKEN", "")
    if not pat:
        sys.exit("ERROR: ASANA_PERSONAL_ACCESS_TOKEN not set in environment / .env")

    headers = {
        "Authorization": f"Bearer {pat}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "data": {
            "resource": project_gid,
            "target": target_url,
            "filters": [
                {"resource_type": "task", "action": "added"},
                {"resource_type": "task", "action": "changed"},
            ],
        }
    }

    print(f"Registering webhook for project {project_gid} → {target_url}")

    with httpx.Client(timeout=30) as client:
        resp = client.post(
            f"{ASANA_API_BASE}/webhooks",
            headers=headers,
            content=json.dumps(payload),
        )

    if resp.status_code not in (200, 201):
        print(f"ERROR {resp.status_code}: {resp.text}")
        sys.exit(1)

    data = resp.json().get("data", {})
    print("\n✅ Webhook registered successfully!")
    print(f"   webhook gid : {data.get('gid')}")
    print(f"   resource    : {data.get('resource', {}).get('gid')}")
    print(f"   target      : {data.get('target')}")
    print(f"   active      : {data.get('active')}")
    print("\nSave the webhook gid — you'll need it to delete/inspect the webhook.")
    return data


def list_webhooks(workspace_gid: str) -> None:
    pat = os.getenv("ASANA_PERSONAL_ACCESS_TOKEN", "")
    if not pat:
        sys.exit("ERROR: ASANA_PERSONAL_ACCESS_TOKEN not set")

    headers = {"Authorization": f"Bearer {pat}", "Accept": "application/json"}

    with httpx.Client(timeout=30) as client:
        resp = client.get(
            f"{ASANA_API_BASE}/webhooks",
            headers=headers,
            params={"workspace": workspace_gid},
        )
    resp.raise_for_status()
    hooks = resp.json().get("data", [])
    print(f"\nActive webhooks in workspace {workspace_gid}:")
    for h in hooks:
        print(f"  {h.get('gid')} → {h.get('target')} (active={h.get('active')})")


def delete_webhook(webhook_gid: str) -> None:
    pat = os.getenv("ASANA_PERSONAL_ACCESS_TOKEN", "")
    if not pat:
        sys.exit("ERROR: ASANA_PERSONAL_ACCESS_TOKEN not set")

    headers = {"Authorization": f"Bearer {pat}"}

    with httpx.Client(timeout=30) as client:
        resp = client.delete(
            f"{ASANA_API_BASE}/webhooks/{webhook_gid}",
            headers=headers,
        )
    if resp.status_code == 200:
        print(f"✅ Webhook {webhook_gid} deleted.")
    else:
        print(f"ERROR {resp.status_code}: {resp.text}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Asana Webhook Manager")
    sub = parser.add_subparsers(dest="command")

    reg = sub.add_parser("register", help="Register a new webhook")
    reg.add_argument("--project-gid", required=True, help="Asana project GID")
    reg.add_argument("--target-url", required=True, help="Public HTTPS URL (e.g. ngrok)")

    lst = sub.add_parser("list", help="List active webhooks")
    lst.add_argument("--workspace-gid", required=True, help="Asana workspace GID")

    rm = sub.add_parser("delete", help="Delete a webhook")
    rm.add_argument("--webhook-gid", required=True, help="Webhook GID to delete")

    args = parser.parse_args()

    if args.command == "register":
        register_webhook(args.project_gid, args.target_url)
    elif args.command == "list":
        list_webhooks(args.workspace_gid)
    elif args.command == "delete":
        delete_webhook(args.webhook_gid)
    else:
        parser.print_help()
