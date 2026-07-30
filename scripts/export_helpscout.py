#!/usr/bin/env python3
"""Export all Help Scout conversations (with threads) to JSONL.

Phase 0 of PLAN.md: OAuth2 client-credentials auth, then page through every
mailbox's conversations with threads embedded, writing each conversation
verbatim as one JSON line. The output is the lossless source of truth —
never edit it; regenerate derived views from it (see render_md_views.py).

Usage:
    python3 scripts/export_helpscout.py                 # everything, all mailboxes
    python3 scripts/export_helpscout.py --status active # subset by status

Credentials: HELPSCOUT_APP_ID / HELPSCOUT_APP_SECRET in .env at the repo root
(create the app under Help Scout -> your profile -> My Apps).

Output: history/raw/conversations.jsonl

Stdlib only — no pip install needed.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.helpscout.net/v2"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "history" / "raw" / "conversations.jsonl"

MAX_RETRIES = 6


def load_env(path: Path) -> dict:
    """Minimal .env parser: KEY=VALUE lines, # comments, no quoting games."""
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        # allow trailing inline comments like the ones in .env.example
        if " #" in value:
            value = value.split(" #", 1)[0]
        value = value.strip()
        # strip surrounding quotes, dotenv-style
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        env[key.strip()] = value
    return env


class HelpScoutClient:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.token = None

    def authenticate(self):
        body = urllib.parse.urlencode(
            {
                "grant_type": "client_credentials",
                "client_id": self.app_id,
                "client_secret": self.app_secret,
            }
        ).encode()
        req = urllib.request.Request(
            f"{API}/oauth2/token",
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req) as resp:
            self.token = json.load(resp)["access_token"]

    def get(self, path: str, params: dict | None = None) -> dict:
        """GET with retry on 429 (Retry-After) and one re-auth on 401."""
        url = f"{API}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        for attempt in range(MAX_RETRIES):
            req = urllib.request.Request(
                url, headers={"Authorization": f"Bearer {self.token}"}
            )
            try:
                with urllib.request.urlopen(req) as resp:
                    return json.load(resp)
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    wait = int(e.headers.get("Retry-After", "10") or "10")
                    print(f"  429 rate limited, sleeping {wait}s", file=sys.stderr)
                    time.sleep(wait)
                elif e.code == 401 and attempt == 0:
                    print("  token expired, re-authenticating", file=sys.stderr)
                    self.authenticate()
                elif e.code >= 500:
                    wait = 2**attempt
                    print(f"  {e.code} from API, retrying in {wait}s", file=sys.stderr)
                    time.sleep(wait)
                else:
                    raise
        raise RuntimeError(f"gave up after {MAX_RETRIES} attempts: GET {url}")


def select_mailboxes(client: HelpScoutClient, selector: str | None) -> list[dict]:
    mailboxes = client.get("/mailboxes")["_embedded"]["mailboxes"]
    if selector is None:
        return mailboxes
    matches = [
        m
        for m in mailboxes
        if str(m["id"]) == selector or selector.lower() in m["name"].lower()
    ]
    if not matches:
        names = [f"{m['id']}: {m['name']}" for m in mailboxes]
        sys.exit(f"No mailbox matches {selector!r}. Available:\n  " + "\n  ".join(names))
    if len(matches) > 1:
        names = [f"{m['id']}: {m['name']}" for m in matches]
        sys.exit(f"{selector!r} is ambiguous:\n  " + "\n  ".join(names))
    return matches


def export(client: HelpScoutClient, status: str, mailboxes: list[dict]) -> int:
    print(f"{len(mailboxes)} mailbox(es): {[m['name'] for m in mailboxes]}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # per-process temp name: concurrent runs must never share a partial file
    tmp_path = OUT_PATH.with_suffix(f".jsonl.tmp.{os.getpid()}")

    seen_ids = set()
    with tmp_path.open("w") as out:
        for mailbox in mailboxes:
            page = 1
            total_pages = 1
            while page <= total_pages:
                data = client.get(
                    "/conversations",
                    {
                        "mailbox": mailbox["id"],
                        "status": status,
                        "embed": "threads",
                        "sortField": "createdAt",
                        "sortOrder": "asc",
                        "page": page,
                    },
                )
                total_pages = data.get("page", {}).get("totalPages", 1)
                conversations = data.get("_embedded", {}).get("conversations", [])
                for conv in conversations:
                    if conv["id"] in seen_ids:
                        continue
                    seen_ids.add(conv["id"])
                    out.write(json.dumps(conv, ensure_ascii=False) + "\n")
                print(
                    f"  {mailbox['name']}: page {page}/{total_pages} "
                    f"({len(seen_ids)} total)"
                )
                page += 1

    tmp_path.replace(OUT_PATH)
    return len(seen_ids)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--status",
        default="all",
        choices=["all", "active", "open", "closed", "pending", "spam"],
        help="conversation status filter (default: all)",
    )
    parser.add_argument(
        "--mailbox",
        help="export only this mailbox (numeric id or name substring); "
        "default: all mailboxes",
    )
    parser.add_argument(
        "--list-mailboxes",
        action="store_true",
        help="print available mailboxes and exit",
    )
    args = parser.parse_args()

    env = load_env(REPO_ROOT / ".env")
    app_id = env.get("HELPSCOUT_APP_ID", "")
    app_secret = env.get("HELPSCOUT_APP_SECRET", "")
    if not app_id or not app_secret:
        sys.exit(
            "Missing HELPSCOUT_APP_ID / HELPSCOUT_APP_SECRET in .env\n"
            "Create the app: Help Scout -> your profile photo -> My Apps -> "
            "Create My App, then copy .env.example to .env and fill them in."
        )

    client = HelpScoutClient(app_id, app_secret)
    client.authenticate()

    if args.list_mailboxes:
        for m in client.get("/mailboxes")["_embedded"]["mailboxes"]:
            print(f"{m['id']}: {m['name']} <{m.get('email', '')}>")
        return

    mailboxes = select_mailboxes(client, args.mailbox)
    count = export(client, args.status, mailboxes)
    print(f"\nDone: {count} conversations -> {OUT_PATH.relative_to(REPO_ROOT)}")
    print("Next: python3 scripts/render_md_views.py")


if __name__ == "__main__":
    main()
