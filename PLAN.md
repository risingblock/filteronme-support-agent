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

## Phase 2 — Support portal + email ingestion in filteronme-one (REPLANNED
## 2026-07-27, see D19; supersedes the Help Scout cron loop)

Build into the filteronme-one Next.js app on Vercel (spec: PORTAL-SPEC.md in
this repo):

1. **Email in**: inbound webhook (Postmark/Resend inbound or Cloudflare Email
   Routing) for support@filteronme.com → SupportTicket/SupportMessage rows in
   the existing Postgres. Threading via In-Reply-To/References.
2. **Agent drafting**: on new inbound message, run the agent (eve framework,
   fallback: plain Agent SDK background function; model: Sonnet 5) with the
   playbooks from this repo + the D20 read-only tool whitelist → store draft,
   topic, needs_human, rationale.
3. **Eddy's inbox UI**: ticket list + customer message + draft + edit box +
   [Send] / [Close as spam] / [Escalated]. Outbound via Resend/Postmark
   (SPF/DKIM on filteronme.com). Every send records draft-vs-sent diff.
4. **Cutover**: switch support@ forwarding when live; Help Scout goes
   read-only, then cancelled. History is already archived here.

## Phase 3 — Tools + guardrails hardening (with Phase 2)

- Stripe restricted read-only key (exists in .env here; add Subscriptions/
  Invoices read) behind deterministic wrapper tools (D20).
- App DB lookups via scoped Prisma wrappers (same D20 rules).
- ~~Chargeback economics analysis~~ DONE 2026-07-27 — hold the line (D15).
- Later, with explicit guardrail-2 amendment: single-purpose cancel tool with
  code-enforced ownership verification (D18).

## Phase 4 — Learning loop + graduated autonomy (ongoing)

1. Daily digest (Vercel cron): tickets seen / drafted / escalated /
   heavily-edited drafts, emailed to Eddy.
2. Weekly: export draft-vs-sent diffs → review in Claude Code here →
   playbook edits → redeploy. (This replaces RL — the playbooks are the
   weights; D17 dry-run harness re-runs after major playbook changes.)
3. Graduate autonomy one intent at a time via eve's approval gates: a
   playbook whose drafts go ~2 weeks without meaningful edits can flip to
   auto-send (spam-close and filterly-template first — likely candidates).
   Refunds, angry customers, anything money-touching stay drafts-only
   indefinitely.

## Effort summary

| Phase | What | Effort |
|---|---|---|
| 0 | Export script + run | DONE |
| 1 | Playbooks + review + dry-run gate | DONE |
| 2 | Portal MVP (email in, drafts, inbox UI) | 2–3 days in filteronme-one |
| 3 | Tool layer + guardrails | with Phase 2 |
| 4 | Digest + learning loop + graduated auto-send | ongoing |

Running cost: Vercel (existing) + model usage (~$5–15/mo at this volume) +
email provider. No VPS, no Help Scout subscription after cutover.
