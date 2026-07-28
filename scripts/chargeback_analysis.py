#!/usr/bin/env python3
"""Chargeback economics analysis (see DECISIONS.md D15).

Question: when a customer THREATENS a chargeback/dispute and we hold the
no-refund line, how often do they follow through — and what does that cost
vs. just refunding the threat cases?

Two subcommands:
    python3 scripts/chargeback_analysis.py scan     # local: find threat tickets in history/
    python3 scripts/chargeback_analysis.py analyze  # Stripe: disputes/refunds + matching

`scan` needs only the Phase 0 export. `analyze` needs STRIPE_RESTRICTED_KEY in
.env — a RESTRICTED, READ-ONLY key (Disputes/Charges/Customers read), never
the live secret key (CLAUDE.md guardrail 2).

Stdlib only.
"""

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW = REPO_ROOT / "history" / "raw" / "conversations.jsonl"
OUT_DIR = REPO_ROOT / "history" / "analysis"
THREATS_PATH = OUT_DIR / "threat_tickets.jsonl"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from export_helpscout import load_env  # noqa: E402
from render_md_views import html_to_text  # noqa: E402

# customer-authored text only; tuned to avoid matching our own boilerplate
THREAT_RE = re.compile(
    r"chargeback|charge-?back|dispute (the|this|my) (charge|payment|transaction)"
    r"|disputing (the|this|my)|contact(ed|ing)? my bank|call(ed|ing)? my bank"
    r"|report (this|you) to my (bank|card)|fraud(ulent)? (charge|transaction)"
    r"|unauthorized (charge|payment|transaction)|paypal dispute|open(ed|ing)? a dispute"
    r"|reverse (the|this) charge|my (bank|credit card company) (will|to) (reverse|dispute)",
    re.IGNORECASE,
)

STRIPE_API = "https://api.stripe.com/v1"
STRIPE_DISPUTE_FEE = 15.00  # USD, standard Stripe dispute fee
CHARGEBLAST_ALERT_COST = 29.00  # USD per alert (Eddy, 2026-07-27)


def scan():
    """Find conversations where the CUSTOMER threatened a dispute/chargeback."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    threats = []
    for line in RAW.open():
        c = json.loads(line)
        for t in (c.get("_embedded") or {}).get("threads", []):
            if t.get("type") != "customer" or not t.get("body"):
                continue
            text = html_to_text(t["body"])
            m = THREAT_RE.search(text)
            if not m:
                continue
            start = max(0, m.start() - 80)
            threats.append(
                {
                    "conv_id": c["id"],
                    "date": t.get("createdAt", c.get("createdAt", "")),
                    "email": ((c.get("primaryCustomer") or {}).get("email") or "").lower(),
                    "subject": c.get("subject") or "",
                    "match": re.sub(r"\s+", " ", text[start : m.end() + 80]).strip(),
                }
            )
            break  # one hit per conversation is enough
    with THREATS_PATH.open("w") as f:
        for t in threats:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    years = Counter(t["date"][:4] for t in threats)
    print(f"{len(threats)} threat conversations -> {THREATS_PATH.relative_to(REPO_ROOT)}")
    print("by year:", dict(sorted(years.items())))


def stripe_get(key: str, path: str, params: dict):
    url = f"{STRIPE_API}{path}?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2**attempt)
            else:
                body = e.read().decode(errors="replace")[:300]
                raise SystemExit(f"Stripe {e.code} on {path}: {body}")
    raise SystemExit("Stripe: gave up after retries")


def stripe_list_all(key: str, path: str, extra: dict | None = None):
    items, starting_after = [], None
    while True:
        params = {"limit": 100, **(extra or {})}
        if starting_after:
            params["starting_after"] = starting_after
        page = stripe_get(key, path, params)
        items.extend(page["data"])
        if not page.get("has_more"):
            return items
        starting_after = page["data"][-1]["id"]


def charge_email(key: str, charge_id: str, cache: dict) -> str:
    if charge_id in cache:
        return cache[charge_id]
    ch = stripe_get(key, f"/charges/{charge_id}", {})
    email = (
        (ch.get("billing_details") or {}).get("email")
        or ch.get("receipt_email")
        or ""
    ).lower()
    cache[charge_id] = email
    return email


def analyze():
    env = load_env(REPO_ROOT / ".env")
    key = env.get("STRIPE_RESTRICTED_KEY", "")
    if not key.startswith("rk_"):
        sys.exit(
            "STRIPE_RESTRICTED_KEY missing or not a restricted key (must start "
            "with rk_). Create one: Stripe Dashboard -> Developers -> API keys "
            "-> Create restricted key, READ permission on Disputes, Charges, "
            "Customers only."
        )
    if not THREATS_PATH.exists():
        sys.exit("Run the scan step first: python3 scripts/chargeback_analysis.py scan")

    threats = [json.loads(l) for l in THREATS_PATH.open()]
    threat_emails = {t["email"] for t in threats if t["email"]}

    print("Fetching disputes...")
    disputes = stripe_list_all(key, "/disputes")
    print(f"  {len(disputes)} disputes")
    print("Fetching refunds...")
    refunds = stripe_list_all(key, "/refunds")
    print(f"  {len(refunds)} refunds")

    cache: dict = {}
    for d in disputes:
        d["_email"] = charge_email(key, d["charge"], cache) if d.get("charge") else ""
    for r in refunds:
        r["_email"] = charge_email(key, r["charge"], cache) if r.get("charge") else ""

    # matching: same email, dispute created within 90 days after the threat
    matched, unmatched_threats = [], []
    dispute_by_email: dict = {}
    for d in disputes:
        dispute_by_email.setdefault(d["_email"], []).append(d)
    for t in threats:
        hits = [
            d
            for d in dispute_by_email.get(t["email"], [])
            if 0 <= d["created"] - iso_to_epoch(t["date"]) <= 90 * 86400
        ]
        (matched if hits else unmatched_threats).append(t)

    silent = [d for d in disputes if d["_email"] not in threat_emails]
    lost = [d for d in disputes if d["status"] == "lost"]
    won = [d for d in disputes if d["status"] == "won"]
    total_disputed = sum(d["amount"] for d in disputes) / 100
    total_refunded = sum(r["amount"] for r in refunds) / 100
    dispute_years = Counter(time.strftime("%Y", time.gmtime(d["created"])) for d in disputes)
    refund_years = Counter(time.strftime("%Y", time.gmtime(r["created"])) for r in refunds)

    n_t = len(threats)
    follow = len(matched)
    report = {
        "threat_conversations": n_t,
        "threats_with_email": len(threat_emails),
        "threats_followed_through": follow,
        "follow_through_rate": round(follow / n_t, 3) if n_t else None,
        "disputes_total": len(disputes),
        "disputes_by_year": dict(sorted(dispute_years.items())),
        "disputes_from_silent_customers": len(silent),
        "disputes_won": len(won),
        "disputes_lost": len(lost),
        "total_disputed_usd": total_disputed,
        "refunds_total": len(refunds),
        "refunds_by_year": dict(sorted(refund_years.items())),
        "total_refunded_usd": total_refunded,
        "est_cost_per_dispute_usd": STRIPE_DISPUTE_FEE + CHARGEBLAST_ALERT_COST,
        "est_total_dispute_overhead_usd": len(disputes)
        * (STRIPE_DISPUTE_FEE + CHARGEBLAST_ALERT_COST),
        "matched_examples": [
            {"conv_id": t["conv_id"], "date": t["date"]} for t in matched[:20]
        ],
    }
    out = OUT_DIR / "chargeback_report.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(f"\nSaved -> {out.relative_to(REPO_ROOT)}")


def iso_to_epoch(iso: str) -> float:
    try:
        return time.mktime(time.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return 0.0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "scan":
        scan()
    elif cmd == "analyze":
        analyze()
    else:
        sys.exit(__doc__)
