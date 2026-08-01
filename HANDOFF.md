# Session handoff — state as of 2026-08-01

Read CLAUDE.md, PLAN.md, DECISIONS.md first as always. This file captures
exactly where things stand between the two repos and what's pending.

## What's LIVE in production (filteronme-one, deployed)

- /help — in-house help center (47 articles, search, task cards, categories)
- /help/contact — structured contact form → emails Help Scout (support@)
- help.filteronme.com — DNS flipped to Vercel 2026-08-01, verified: root
  308s to /help, all legacy /article/<id> URLs 301 to new slugs
- The drafting agent (separate Vercel project from THIS repo,
  filteronme-support-agent.vercel.app/api/draft) — deployed, D17-gated,
  but NOT connected to any ticket source yet (by design; awaits portal)

## Built + verified but NOT YET DEPLOYED (uncommitted in filteronme-one)

Everything after Eddy's last deploy, all `yarn build`-verified:
- Cancel branch of contact form = pure self-serve ladder, NO form, NO
  contact-support path (Eddy's hard rule)
- /cancel — cancel-by-card (instant reversible cancel_at_period_end)
- /recover — 3-step account recovery (code-verified new email → claims →
  48h/96h veto windows), single AccountRecovery process table
- /billing-email card-finder section
- Contact form: camera field + reactive tips, deep links (?topic=&issue=),
  one-mandatory-email rule, lost-email router buttons
- accountRecovery tRPC router (sendCode/verifyCode/start/cancelByCard),
  /api/recovery/block veto endpoint, /api/cron/execute-recoveries + vercel.json
  hourly cron
- past_due fixes: restore-flow message, phantom-"transferred" bug, trial-reset
  no longer masks failing renewals (see playbooks/SELF-SERVE-FLOWS.md)
- 4 updated FAQ articles synced into content/help/

### Deploy prerequisites (ORDER MATTERS)
1. `npx prisma db push` in filteronme-one (creates AccountRecovery table)
2. Add CRON_SECRET to Vercel env
3. Commit + deploy
4. Staging walkthrough: /recover end-to-end on a test sub (code email, veto
   email, block-one/mature-one), /cancel, card finder with Eddy's own last4
5. Delete junk `.next-*trash*` dirs; delete Claude's test ticket in Help
   Scout ([help/cancel] customer@example.com)

## Eddy's open decisions

- Grace period for past_due (currently: filters off immediately)
- Stripe dashboard: verify dunning retry schedule/emails + final action
- Sweep current past_due customers with a portal-link email (revenue recovery)
- Filterly website/checkout banner (data says yes; his call)

## Remaining build phases

- THE PORTAL INBOX (last piece): SupportTicket/SupportMessage tables, inbound
  email webhook (Postmark — the app's mailer), inbox UI at /admin/support,
  wire the deployed drafting agent (POST /api/draft w/ INTERNAL_WEBHOOK_SECRET),
  daily digest. Spec: PORTAL-SPEC.md. Then 2-week parallel run → cancel
  Help Scout. Until then Jona/Eddy answer (structured) tickets in Help Scout.
- Phase 4 learning loop: weekly draft-vs-sent diffs → playbook edits here.

## Known quirks / gotchas for the next session

- Brain repo git: local commits may be ahead of origin; pushing redeploys the
  agent project (harmless).
- filteronme-one builds: never run two builds concurrently or dev+build on
  the same .next (corrupts; move .next aside if weirdness). Vercel CLI is
  authed as mrechung; filteronme-one is NOT under the personal scope.
- Stripe restricted key (brain .env): has Charges/Customers/Subscriptions/
  Disputes read; NO Invoices read (403s).
- Postmark From must be noreply@filteronme.com; Reply-To carries customers.
- Eddy's rules: no time estimates; never design him in as a reviewer/
  escalation path; "Filteronme" not "FilterOnMe"; brand sweeps must never
  touch app code identifiers.
