---
topic: subscription-change
volume: 32 of 1957 (2%)
status: approved 2026-07-27 (facts code-verified against app v2.1.7 + web)
---

# Switching plans, changing email, restoring access

## When this applies

Customer wants to: switch monthly ↔ yearly billing, upgrade to remove the
watermark, change/transfer the account to a different email address, restore
an existing purchase on a new device/reinstall, or is confused about which
email their active subscription lives under. Also covers "I signed up for the
wrong plan by accident" and "can I get a discount."

## What to check first

Before drafting anything, look up the customer in Stripe (read-only, Phase 3):

- Which email has the **active** subscription — it is frequently *not* the
  email the customer is writing from or thinks they used (conv 2746208264,
  2929713312, 2574992624, 3311230847, 3349317521). Half of this topic's
  volume is really "customer is confused about which email to log in with,"
  not an actual change request.
- Current plan (monthly/yearly), status (active/past due/expired/trialing),
  and most recent charge date/amount.
- If the "old" account they want to move from is already expired/past due,
  say so — starting a fresh subscription on the new email is often simpler
  than a transfer (conv 2845954011).

## Policy

**Monthly → Yearly (upgrade): self-serve, no escalation needed.**
Billing portal ("Billing" button in app, or filteronme.com/billing) →
"Update Subscription" → select yearly. Stripe automatically prorates: unused
time on the current monthly plan becomes a credit applied to the annual
charge (docs 115; conv 2835305559, 2969517627, 3207923843 — all Eddy-confirmed).
Draft the doc link, no ticket action needed beyond that.

**Yearly → Monthly (downgrade): self-serve, but NOT prorated.**
Same billing-portal flow, but the change takes effect **at the end of the
current yearly term**, not immediately, and there is no partial refund for
the unused year (Eddy, conv 3382425778: "no proration, it would change after
the year, and then move to monthly"). Doc 115 only describes the
monthly→yearly direction — say the downgrade part explicitly so the customer
isn't surprised.

**Accidental purchase (picked yearly by mistake, wants a swap + refund of the
difference): escalate, don't promise.** Standard line is that the plan
change itself is self-serve (per above) but a refund or immediate proration
is a manual Stripe action only Eddy can approve case-by-case (conv 3382425778,
2919806489). One old exception exists (conv 2512150530, 2024: partial refund
+ switch to monthly) — that was Eddy's discretion, not standing policy; do
not offer it as an option, just escalate.

**Discount requests (long-time customer, "can I get 20% off yearly," etc.):
no.** "We no longer give discounts out, the yearly membership is already
heavily discounted compared to the monthly" (TONE.md; conv 3155879524). Two
2024 conversations show Eddy handing out ad hoc coupon codes — that practice
stopped; do not offer or invent a code.

**Change email / transfer subscription to another email: self-serve if they
still have the old email.** Direct to https://www.filteronme.com/change-email
(doc 132, current as of May 2026 — this replaced the old "email Eddy and
he'll do it manually" flow seen in most of the 2024/2025 history below).

**Lost access to the old email entirely: escalate, needs-human.** This is a
manual Stripe-side transfer and is the #1 account-takeover risk in this
topic — never promise or perform it from a ticket alone. Per doc 140 and
Eddy's own bar (conv 2845954011), ask the customer for as much as they can
provide before escalating:
- old account email + new email wanted
- most recent charge date and amount
- last 4 digits and brand of the card used
- name and billing address on the payment method
- any receipt/invoice/order number
- whether they might have more than one FilterOnMe account

Tag `needs-human` and hand this to Eddy with whatever verification info the
customer already gave — do not tell them it's done, and set expectations
that account recovery can take 5–10 business days (doc 140).

**Restore purchase on a new machine / after reinstall: self-serve.** "Restore
purchase" button, bottom-right corner of the app; verify ownership of the
billing email when prompted (doc 136). Covers: shows Free Trial despite
having paid, reinstalled and lost access, switched computers, logged in with
the wrong email by mistake.

**Watermark still showing after upgrading: almost always a login/email
mismatch, not a billing problem.** Check Stripe for which email actually has
the active premium sub, then have them log out (Settings → Reset App) and
log back in with *that* email (conv 2500950141, 2574992624). Only point to
the upgrade button (doc 116, bottom-left in app) if Stripe shows no active
subscription at all.

**One subscription = one device at a time.** Two simultaneous devices need
two subscriptions (conv 2977450094, 3020051763). Not a change request, but
comes up in this topic often enough to note.

**Duplicate signups:** if a customer signed up twice by accident, Eddy can
cancel the extra one — this is a write action, escalate rather than
confirming it yourself (conv 2298724708).

## How to respond

**Monthly → yearly, straightforward:**
> Hi,
>
> You can do this yourself in the billing portal — click "Billing" in the
> app, then "Update Subscription" and pick the yearly plan. It'll
> automatically credit you for the unused time on your current month.
>
> Best

**Yearly → monthly:**
> Hi,
>
> You can switch this in the billing portal (Billing → Update Subscription →
> Monthly). Just a heads up: since you're on yearly, the switch won't take
> effect until your current year ends — there's no partial refund for the
> remaining time.
>
> Best

**Confused which email to use (checked Stripe, found the real one):**
> Hi,
>
> I checked and your active subscription is actually under
> <other-email> — try logging in with that one. You can also use
> filteronme.com/change-email if you'd like to move it to a different
> address.
>
> Best

**Lost access to old email (escalate — draft as a note for Eddy, or as a
customer-facing ask for more info if key details are missing):**
> Hi,
>
> To move your subscription to a new email we need to verify you own the
> account first. Could you send: the old email, your most recent charge
> date/amount, the last 4 digits and brand of the card used, and the name on
> the card? I'll get this moved over once I can confirm it's you.
>
> Best

## Escalate instead (tag needs-human) when

- Customer lost access to the old email and needs a manual transfer —
  always, regardless of how much verification info they've provided. Collect
  the doc-140 checklist in the ticket, then escalate; never confirm the
  transfer happened.
- Any refund or proration outside the standard self-serve billing-portal
  flow (accidental purchase, "swap my plan and refund the difference").
- Duplicate-account cancellation requests.
- Customer disputes the Stripe record (e.g., insists they're on a different
  plan/price than what Stripe shows) — needs manual investigation.
- Anything asking for a discount/coupon beyond linking to the yearly plan.

## Doc links to use in replies

- https://help.filteronme.com/article/115-change-to-yearly-or-monthly-billing-cycle
- https://help.filteronme.com/article/116-how-to-remove-watermark-by-upgrading
- https://www.filteronme.com/change-email (doc 132)
- https://help.filteronme.com/article/136-restore-purchase-or-access-existing-subscription
- https://help.filteronme.com/article/140-lost-access-to-email
- filteronme.com/billing (portal login by receipt email) and
  filteronme.com/billing-email (portal access link) as fallbacks when the
  Billing button isn't available (free trial has none)

## Notes from history

- Jona's replies are template-heavy and correct on the mechanics (billing
  portal steps, boilerplate about free trials having no Billing button) but
  routinely fail to actually check Stripe before replying — several threads
  show Jona pinging Eddy mid-conversation to do the lookup that should
  happen first (conv 3382425778, 2929713312, 3155879524). The agent should
  do the Stripe lookup *before* drafting, not after the customer pushes back.
- The self-serve change-email tool (doc 132) and the verification checklist
  for lost-access transfers (doc 140) are both dated May 7, 2026 — clearly a
  recent process change from the older "email Eddy, he'll do it by hand"
  pattern that dominates the 2024–early-2025 conversations. Treat the
  self-serve tool + doc-140 checklist as current policy; the older manual
  "just tell me old/new email" replies (conv 2821050717, 2845995716,
  2594738110-era) are superseded.
- RESOLVED by codebase verification (2026-07-27): the change-email tool is
  **double opt-in** — a 6-digit code to the OLD email (proves ownership),
  then a second code to the NEW email (proves control), only then does Stripe
  update. Active subscriptions only; rate-limited (5/15min per IP, 3/60min
  per email); every transfer audit-logged to `SubscriptionTransferLog`; and
  it refuses if the new email already has an active subscription. Safe to
  point customers at confidently.
- 2024 had at least two ad hoc discount coupons (50MAY2024, and a per-customer
  20% code). TONE.md and conv 3155879524 make clear this stopped; flagged so
  Eddy can confirm no exceptions remain live.
