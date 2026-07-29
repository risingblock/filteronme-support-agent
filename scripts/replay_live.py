#!/usr/bin/env python3
"""D17 replay against the DEPLOYED agent endpoint.

Takes replay cases (JSON list with conv_id/subject/customer_message), resolves
each conversation's real customer email from the local export, POSTs to the
live /api/draft, and writes a side-by-side report.

Usage:
    python3 scripts/replay_live.py <cases.json> [--url https://...]

Requires INTERNAL_WEBHOOK_SECRET in .env. Read-only effects only: the agent
does read-only lookups; nothing is sent to any customer.
"""

import json
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from export_helpscout import load_env  # noqa: E402

DEFAULT_URL = "https://filteronme-support-agent.vercel.app/api/draft"


def customer_emails_by_conv() -> dict:
    emails = {}
    raw = REPO_ROOT / "history" / "raw" / "conversations.jsonl"
    for line in raw.open():
        c = json.loads(line)
        emails[c["id"]] = ((c.get("primaryCustomer") or {}).get("email") or "").lower()
    return emails


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    url = DEFAULT_URL
    if "--url" in sys.argv:
        url = sys.argv[sys.argv.index("--url") + 1]

    secret = load_env(REPO_ROOT / ".env").get("INTERNAL_WEBHOOK_SECRET", "")
    if not secret:
        sys.exit("INTERNAL_WEBHOOK_SECRET missing from .env (use the same value as the Vercel project)")

    cases = json.load(open(args[0]))
    emails = customer_emails_by_conv()
    out_dir = REPO_ROOT / "history" / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for i, case in enumerate(cases):
        payload = {
            "ticketRef": f"replay-{case['conv_id']}",
            "subject": case.get("subject", ""),
            "customerEmail": emails.get(case["conv_id"]) or "unknown@example.com",
            "messages": [
                {
                    "direction": "inbound",
                    "author": "customer",
                    "bodyText": case["customer_message"],
                    "createdAt": case.get("date", ""),
                }
            ],
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"content-type": "application/json", "x-internal-secret": secret},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                result = json.load(resp)
        except Exception as e:  # keep going; report the failure
            result = {"error": str(e)}
        results.append({"case": i, "conv_id": case["conv_id"],
                        "topic_true": case.get("topic_true"), "result": result})
        status = result.get("action", result.get("error", "?"))
        print(f"[{i}] conv {case['conv_id']} ({case.get('topic_true','?')}): {status}")

    out = out_dir / "replay_live_results.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nSaved -> {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
