# Decision Log

Decisions made in the planning chat (July 2026), with rationale. Don't reopen
without new information.

## D1. Drafts-only to start
Agent posts suggested replies as private Help Scout notes; human sends. Chosen
over auto-send both to build trust AND as the primary prompt-injection defense
(a human sees every output before a customer does).

## D2. Model the architecture on gumclaw, scaled down
Gumclaw = stock agent framework + ~273 markdown skill playbooks + read access to
live systems + ~78 cron loops, on always-on hardware. No fine-tuning; it learns by
editing files. At <10 tickets/day we need ~10–20 playbooks and 2–3 crons. Same
architecture, tiny scale.

## D3. Raw export is JSONL, not markdown
Eddy challenged "export to .md files" — correctly. JSONL verbatim from the API is
the lossless source of truth (keeps tags, timestamps, emails, status). Markdown
views with YAML frontmatter are *generated* from it for grep and human reading.
Re-render anytime without re-exporting.

## D4. No vector DB; playbooks + grep; SQLite FTS5 as upgrade path
At a few thousand conversations, agentic search (ripgrep over md views + frontmatter
topic tags) is effective and zero-infrastructure. The agent shouldn't be searching
raw history at runtime much anyway: "how do we answer this?" → playbooks (if it's
searching often, a playbook is missing — fix the playbook); "have we talked to this
customer?" → live Help Scout API search by email, never the stale export. If search
ever feels weak: load JSONL into SQLite FTS5 (single file, no server). Embeddings
only justified at 10k+ conversations — not our scale.

## D5. Local Mac first, Hetzner VPS later
Early weeks are all iteration (editing playbooks daily) — faster on the machine in
front of you. Promote to server once boring. Enablers from day one: brain folder as
a private git repo (move = clone), secrets in .env outside the repo. Mac sleep gap
is acceptable for drafts-only; auto-send or annoyance triggers the move.

## D6. Browser/computer-use is a last resort
Help Scout, Stripe, Shopify all have full APIs. Only our own app might lack one —
prefer building a tiny read-only endpoint over screen-driving. This also means the
agent runs headless on cheap Linux.

## D7. Read-only everywhere, write only Help Scout notes/tags
Stripe restricted read-only key; Shopify read-only Admin token; no refund/cancel/
account-change capability. Humans execute money actions even after replies go
autonomous. Also part of the injection blast-radius containment.

## D8. Model auth/billing strategy
- Hermes + Claude subscription OAuth: only works on Claude **Max with extra usage
  credits purchased**, and burns overage credits (≈API pricing anyway). Pro doesn't
  work. Trail of credential bugs in the Hermes issue tracker. Not attractive.
- Hermes + **ChatGPT Plus ($20) via Codex OAuth: works** — good for the free-ish
  local phase. Caveats: weekly usage cap (errors until reset ⇒ silent stalls),
  rotating refresh tokens occasionally need interactive re-auth — fine on the Mac,
  bad unattended.
- **Server phase: plain API key.** Unattended cron wants metered, predictable auth
  that never needs a human login. Even pro-subscription guides say API keys for
  production. ~$10–30/mo at our volume.

## D9. Model tiering
Frontier model for the judgment loop (anything a customer might read, anything
deciding an escalation) — the mini-tier models degrade most on exactly agentic
tool-use, and savings at our volume (~$15/mo) don't cover the review-time cost of
dumber drafts. Mini-tier (e.g. GPT-5.4 mini) IS right for bulk mechanical passes:
Phase 1 clustering (the single biggest token spend), ticket topic-tagging, daily
digest, spam detection.

## D10. Polling over webhooks
15-minute cron poll is plenty at <10/day. Webhooks exist in the Help Scout API if
latency ever matters (i.e., after auto-send).

## D11. Escalation is a success state
Playbooks explicitly define when NOT to answer. `needs-human` tag is rewarded
behavior. Refunds/angry/money cases stay human-touched indefinitely.

## D12. Historical reply quality is tiered by author (added 2026-07-27)
Reply authors in the export: Jona De Guzman (1,489 replies — outgoing support
agent, performance was poor), Eddy Chung (933 — founder, canonical), Rajan Patel
(16 — assumed non-canonical). Playbook distillation treats **Eddy's replies as
the gold standard**; Jona's/Rajan's replies are raw material only, cross-checked
against Eddy's patterns and the docs site, never copied as policy on their own.

## D13. Help docs site is a knowledge source, with staleness dates (added 2026-07-27)
https://help.filteronme.com (Help Scout Docs, 47 articles) is exported to
history/docs/ via scripts/export_docs.py (public scrape, no API key needed).
Eddy says not all articles are current — each export carries `last_updated`
frontmatter; playbooks state policy themselves and link articles rather than
deferring to them blindly.

## D14. Codebase is consulted at authoring time only, never at runtime (added 2026-07-27)
When drafting or revising playbooks, Claude may do read-only consultation of the
app codebases (~/work/Filteronme-one web app, ~/work/Filteronme-mac-v2.1,
~/work/FilterOnMeWindows-V2) to verify facts (UI strings, trial logic, billing
behavior). Verified facts are snapshotted INTO playbooks with the app version
noted. The runtime support agent never reads source code — keeps guardrail #3's
attack surface minimal (Eddy's call, confirmed in OPEN-QUESTIONS round 1).
Re-consult manually after major releases.

## D15. Refund/credit policy per Eddy (2026-07-27, OPEN-QUESTIONS round 1)
Default: decline-with-policy-link. Cash refunds rare. Non-cash service
extensions/credits are the STANDARD remedy for support-caused or our-side
errors. Goodwill discounts only for long-tenured existing customers wronged by
us — never new customers.
**Chargeback analysis (ran 2026-07-27, scripts/chargeback_analysis.py):**
threat→dispute follow-through is 5% (2/40); 76% of disputes come from
customers who never contacted support; declining a refund request costs an
expected ~$4–6 in dispute risk vs. a certain $20–43 to grant. Decision:
policy STANDS on data — no loosening; the dispute cost center is silent
customers (product-side fixes: statement descriptor, Filterly banner,
cancel discoverability), not support policy.

## D16. Help Scout is the current channel, not the destination (added 2026-07-27)
Eddy intends to eventually replace Help Scout with a custom support portal +
email ingestion (email stays mandatory — many customers will only ever email).
Implications now: (a) the cron loop isolates all Help Scout calls behind a
small adapter module so the channel can be swapped without touching playbooks
or prompts; (b) we keep owning the data (raw JSONL export is already the
source of truth); (c) no deep Help Scout-specific investment (workflows,
custom fields) beyond notes + tags. Portal build itself is out of scope for
this repo until Eddy green-lights it.

## D17. Dry-run gate before any live loop (added 2026-07-27)
Phase 2 ships only after a replay dry-run: recent closed tickets are re-drafted
by the agent (seeing only what a new ticket would show) and compared against
the historical human replies. Eddy grades the side-by-side. The drafting prompt
used in the dry run (prompts/draft_reply.md) IS the production prompt — no
separate test-only prompt that could diverge.

## D18. Verified-owner fast-cancel is the target workflow (Eddy, 2026-07-27)
From the dry-run grading: when the ticket's From address matches the
subscription's email of record (app-DB login email or Stripe customer email),
Eddy wants cancellation executed on request — no bouncing the customer to the
portal. Rollout is phased to respect guardrail 2:
- **Now (Phase 2, drafts-only):** agent verifies ownership via read-only
  lookups, then escalates with an explicit recommendation note ("verified
  owner — cancel now") + a drafted confirmation reply. Human cancels in
  Stripe, sends the reply.
- **Later (requires amending guardrail 2, explicit approval at that time):** a
  Stripe restricted key with write scoped to Subscriptions only could let the
  agent cancel directly (cancel_at_period_end — reversible, no refund
  capability). Not enabled yet.
- If ownership can't be verified: portal link as before. Also always mention
  the in-app **Billing button** (auto-logs into the portal) alongside the
  billing URL.

## D19. Runtime pivot: custom portal on Vercel, no Hermes, no Hetzner, no
## Help Scout loop (Eddy, 2026-07-27)
Phase 2 is now a support portal + email ingestion built INTO filteronme-one
(same repo/DB/auth/Stripe code), hosted on Vercel. The "agent runtime"
collapses to per-ticket LLM calls (Claude API, Sonnet 5) from the portal
backend — no always-on machine. Vercel's **eve** framework (June 2026,
agents-as-directories: markdown skills + TS tools + built-in human-approval
gates) is the primary runtime candidate; plain Agent SDK background functions
are the fallback if eve proves too immature. Brain (playbooks/prompts) stays
in THIS repo and ships to the portal at deploy time. Hermes is dropped
entirely (D8's auth concerns + no need for a harness at this workload).
Help Scout: kept read-only until cutover, then cancelled; the JSONL export is
the permanent archive. Model: Sonnet 5 (GLM 5.2 benchmarks within noise;
harness-native wins at this scale — re-evaluate only if volume 100×es).

## D20. Agent tools are deterministic scoped wrappers, never raw APIs
## (Eddy, 2026-07-27)
The LLM never gets the app's Stripe SDK, Prisma client, or arbitrary HTTP.
It gets a whitelist of narrow, read-only TypeScript functions (e.g.
getSubscriptionByEmail, getTicketHistory), each doing one fixed query.
Any future write action (D18 fast-cancel) is its own single-purpose tool
whose SAFETY CHECK LIVES IN CODE: the tool itself re-verifies ticket-From ==
subscription email server-side before acting, regardless of what the model
claims, only ever cancel_at_period_end, and writes an audit log. Prompt
guardrails are the soft layer; deterministic code is the enforcement layer.

## Open questions (not yet decided)

- Does Help Scout's reply endpoint support a `draft: true` flag for real API drafts,
  or do we standardize on private Notes? → test with a real account in Phase 2.
- Final runtime: chat leaned Hermes agent (macOS + Linux headless, `--skip-browser`),
  but Eddy is now working in Claude Code — Claude Code headless (`claude -p`) on cron
  is a viable alternative runtime that uses his existing Claude subscription natively.
  Decide in Phase 2; the playbooks/scripts/data design is runtime-agnostic either way.
- Which ChatGPT/Claude subscriptions Eddy actually holds (affects local-phase billing
  choice only).
