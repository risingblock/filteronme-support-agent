# Build Plan: Help Scout Support Agent

Goal: an agent that drafts every support reply, grounded in our Help Scout history
and live data from Stripe / Shopify / our app. Human clicks send. Autonomy expands
per-intent only after drafts prove trustworthy. Run locally on the Mac until it's
boring, then promote to a small Hetzner VPS.

## Phase 0 — Export Help Scout history (an afternoon)

1. Help Scout: Profile → My Apps → Create App → OAuth2 client credentials
   (client-credentials flow, no user interaction).
2. `scripts/export_helpscout.py`: page through
   `GET /v2/conversations?status=all&embed=threads` across all mailboxes,
   handle pagination and 429s with backoff. Low volume ⇒ full history exports
   in an hour or two.
3. Output: `history/raw/conversations.jsonl` (lossless source of truth), then a
   second pass generates `history/md/YYYY/conv-<id>-<slug>.md` views with YAML
   frontmatter (id, date, customer_email, tags, topic, status) for grep + reading.
   Doubles as a permanent backup of support history.

## Phase 1 — Distill history into playbooks (2–3 sessions; highest-leverage step)

1. Cluster exported conversations by topic (refunds, shipping/order status,
   subscription changes, how-tos, bug reports, angry-customer, spam). A cheap/fast
   model is fine for this bulk pass.
2. Per cluster, write one playbook: when it applies → what to check first (e.g.
   "look up the charge in Stripe") → the policy → 2–3 real anonymized example
   replies in our tone → when to escalate instead.
3. `playbooks/TONE.md`: sign-off, formality, what we never say, how discounts and
   exceptions are handled.
4. Expect 10–20 playbooks to cover 90%+ of volume. Eddy reviews; his corrections
   ARE the training. (Reference: github.com/antiwork/skills is exactly this,
   published, for Gumroad.)

## Phase 2 — Drafts-only loop, on the Mac (a day)

Cron every 15 minutes (webhooks unnecessary at this volume):

> Fetch active/unanswered Help Scout conversations → match playbook → gather facts
> (Phase 3 tools) → post suggested reply as a **private Note** on the conversation
> (guaranteed API support; test whether the reply endpoint's draft flag also works)
> → tag `ai-drafted`.

Workflow: open Help Scout, read note, edit if needed, send. A weekly cron diffs
sent replies vs drafts and proposes playbook updates.

Mac-sleep caveat: closed lid ⇒ missed polls; agent catches up on wake. Fine for
drafts-only. `caffeinate` if it bugs us. Auto-send is the trigger to move to a server.

## Phase 3 — Read-only fact tools (half a day + app endpoint)

- Stripe: **restricted read-only key** scoped to charges/customers/subscriptions.
- Shopify: read-only Admin API token scoped to orders/customers.
- Our app: tiny read-only internal endpoint (or read-replica SQL) for account
  lookups. Browser automation only if truly no API path — last resort, not foundation.
- v1 rule: agent reads everywhere, writes nowhere except Help Scout notes.
- ~~Chargeback economics analysis~~ DONE 2026-07-27 (ahead of schedule —
  Eddy created the restricted key early). Verdict: hold the line; see D15.
  The Stripe restricted key already exists in .env; extend its permissions
  (Subscriptions/Invoices read) when building the Phase 3 fact tools.

## Phase 4 — Hetzner + graduated autonomy (half a day, then ongoing)

1. Small VPS (~€5–8/mo), Ubuntu, agent as unprivileged service user, headless
   (no browser). Brain folder synced via private git repo ⇒ move is clone + install.
2. Secrets via env files, tight permissions, never in the repo.
3. Daily digest cron: tickets seen / drafted / escalated / heavily-edited drafts.
4. Graduate autonomy one intent at a time: a playbook whose drafts go ~2 weeks
   without meaningful edits can flip to auto-send. Order status and how-tos first.
   Refunds, angry customers, anything money-touching stay drafts-only indefinitely.

## Effort summary

| Phase | What | Effort |
|---|---|---|
| 0 | Export script + run | an afternoon |
| 1 | Cluster + 10–20 playbooks + review | 2–3 sessions |
| 2 | Local drafts-only cron loop | a day |
| 3 | Stripe/Shopify keys + app lookup | half a day |
| 4 | VPS move + digest + graduated auto-send | half a day, then tuning |

Running cost target: VPS ~€5–8/mo + model usage (~$10–30/mo at this volume).
