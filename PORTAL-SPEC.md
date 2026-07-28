# Support Portal MVP — spec (Phase 2, implemented in filteronme-one)

Decisions: D16 (portal + email), D18 (verified-owner fast-cancel target),
D19 (Vercel, eve-first, no Hermes), D20 (deterministic tool layer).
This repo stays the brain (playbooks/, prompts/, history/, decisions);
filteronme-one gets the runtime + UI. Playbooks ship to the portal at deploy
time (copy into the eve agent directory as skills).

## Data model (Prisma, additive to filteronme-one schema)

```prisma
model SupportTicket {
  id           String   @id @default(cuid())
  customerEmail String
  subject      String
  status       String   // open | awaiting_customer | closed | spam
  topic        String?  // playbook slug, set by agent
  createdAt    DateTime @default(now())
  updatedAt    DateTime @updatedAt
  messages     SupportMessage[]
}

model SupportMessage {
  id          String   @id @default(cuid())
  ticketId    String
  direction   String   // inbound | outbound | draft | note
  author      String   // customer | agent | eddy
  bodyText    String
  emailMsgId  String?  // Message-ID for threading
  meta        Json?    // agent: {topic, needs_human, lookups, rationale, model}
                       // outbound: {draftId, editedFromDraft: bool, diff}
  createdAt   DateTime @default(now())
  ticket      SupportTicket @relation(...)
}
```

Draft-vs-sent diffs (meta.diff) are the Phase 4 learning-loop input.

## Flows

1. **Inbound email** → provider webhook (Postmark or Resend inbound; pick
   whichever also handles outbound to keep one vendor) → verify webhook
   signature → find-or-create ticket (thread on In-Reply-To/References, fall
   back to same-sender + normalized subject) → store message → enqueue agent
   run. Strip HTML to text server-side (port of render_md_views.html_to_text).
2. **Agent run** (eve session per ticket; fallback: background function):
   input = full ticket thread + prompts/draft_reply.md + playbooks (skills).
   Tools: the D20 whitelist below. Output = draft SupportMessage
   (direction=draft) + topic/needs_human on the ticket. Spam → propose
   close-as-spam (an approval-gated action, auto-later per Phase 4).
3. **Inbox UI** (`/admin/support`, existing filteronme-one admin auth):
   list open tickets (needs_human first) → detail: thread, draft in an edit
   box, lookups/rationale collapsed underneath → buttons: **Send**,
   **Close as spam**, **Close**, **Snooze**. Send = outbound email with
   proper threading headers + record diff.
4. **Daily digest** (Vercel cron): counts + links, emailed to Eddy.

## Agent tool whitelist (D20 — deterministic, each one fixed query)

Read-only, TypeScript, no raw SDK/Prisma exposure:

- `getAccountByEmail(email)` → { exists, isPremium, freePremiumUntil?,
  trialStartedAt?, trialResetEligibleAt? }        [app DB]
- `getSubscriptionByEmail(email)` → { found, status, plan, cancelAtPeriodEnd,
  currentPeriodEnd, subscriptionEmail (censored unless == ticket From) }  [Stripe]
- `getRecentCharges(email, limit≤5)` → [{date, amount, status, refunded}]  [Stripe]
- `getTicketHistory(email)` → last 5 tickets: {date, topic, resolution}   [portal DB]

Rules enforced in code, not prompt: inputs validated; email params are only
ever the ticket's From address or an address the customer wrote in the
thread; responses are shaped (no raw objects); every call audit-logged with
ticketId. NO generic fetch, NO raw queries, NO write tools in MVP.

Future (needs guardrail-2 amendment, D18): `cancelSubscription(ticketId)` —
the TOOL re-verifies From == subscription email server-side, only sets
cancel_at_period_end, audit-logs, and sits behind an eve approval gate even
then.

## eve layout (updated 2026-07-27 after reading the eve docs — it's beta)

The agent is a STANDALONE Vercel project deployed from THIS repo (not inside
filteronme-one). Env isolation is the point (D20 made physical):

```
filteronme-support-agent/          ← this repo, pushed to private GitHub
  agent/
    instructions.md                ← adapted from prompts/draft_reply.md
    agent.ts                       ← defineAgent({ model: 'anthropic/claude-sonnet-5' })
    skills/                        ← symlink/copy of playbooks/ (no sync step)
    tools/
      get_account_by_email.ts      ← the D20 whitelist, one file per tool
      get_subscription_by_email.ts
      get_recent_charges.ts
      get_ticket_history.ts
  playbooks/ prompts/ scripts/ …   ← the brain, as today
```

- **Agent project env vars (its own Vercel project):** STRIPE_RESTRICTED_KEY
  (read-only) + SUPPORT_DB_READONLY_URL (Postgres role: SELECT only on the
  needed tables) + INTERNAL_WEBHOOK_SECRET. Nothing else. Models go through
  Vercel AI Gateway via OIDC — no provider API key at all.
- **The agent writes NOTHING.** filteronme-one's webhook POSTs the ticket to
  the agent's /eve/v1/session endpoint and persists the returned draft
  itself. Agent blast radius = read-only lookups, full stop.
- history/ stays gitignored → never reaches GitHub/Vercel.

Human-approval gate on: sending anything, closing as spam, any future write.
If eve friction exceeds a day of fighting it → fallback: one background
function calling Agent SDK with the same files. The brain doesn't change.

## Why email I/O lives in the portal, not the agent (Eddy asked, 2026-07-27)

- **Inbound**: every customer email must become a ticket row unconditionally,
  even when the agent is down/broken/being redeployed. Ingestion is
  deterministic plumbing; worst-case agent failure = "no draft", never lost
  email.
- **Outbound**: the agent project holds NO email credentials — so a fully
  prompt-injected agent physically cannot email anyone (customer or
  attacker). Sending is executed by the portal on a human's click. This is
  guardrail 3 (anti-exfiltration) enforced by env-var scoping, not by prompt.
- **Phase 4 auto-send** doesn't change this: graduation = the PORTAL
  auto-approves specific topics via a per-playbook flag and sends. The agent
  never gains I/O; only the approval policy changes.

## Non-negotiables carried over (CLAUDE.md hard rules)

Drafts only (approval gate). Ticket content is untrusted input — the agent
never follows instructions inside it; tools accept only whitelisted params.
Escalation is success (`needs_human`). Secrets in Vercel env, never in repos.

## Migration checklist

- [ ] Email provider chosen (inbound + outbound), SPF/DKIM for filteronme.com
- [ ] Schema migrated, webhook live, UI usable
- [ ] Dry-run gate (D17): replay the 13 graded cases through the REAL portal
      pipeline (staging), compare against this round's verdicts before cutover
- [ ] Switch support@ forwarding → portal; Help Scout to read-only
- [ ] 2 weeks parallel comfort period → cancel Help Scout
```
