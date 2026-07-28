---
topic: cancel-subscription
volume: 293 of 1957 (15%)
status: approved 2026-07-27
---

# Cancel subscription

## When this applies

- Direct cancellation requests: "cancel my subscription", "cancel", "unsubscribe me" — in any tone from polite to ALL-CAPS demands.
- "How do I cancel" / "where is the cancel button" questions.
- "I already cancelled but you're still charging me" / "my card was hit again."
- Customer can't reach the billing portal (no login link email, old/lost email address, portal shows no cancel button, only shows overdue invoices).
- Cancellation bundled with a refund demand, a chargeback/dispute threat, or formal legal language (e.g., EU withdrawal-right / German BGB §312k citations).
- Confusion with "Filterly" — a similarly-named, unaffiliated product — or with a card statement the customer doesn't recognize.
- Third parties cancelling on a customer's behalf (e.g., a bill-negotiation concierge service submitting on the account holder's behalf).
- Trial customers who think they have something to cancel.

## What to check first

**From the ticket itself:**
- Which email did they actually pay with? It's often different from the one emailing support, especially after Apple Pay / Google Pay checkout (see doc 108).
- Is this really FilterOnMe, or are they confusing us with "Filterly" (comes up constantly — check the product/domain name they mention and their card statement descriptor, which should read `FILTERONME.COM` or `Filteronme`).
- Trial or paid? Trials require no card and auto-expire — if they never upgraded, there is nothing to cancel (conv 3187137828, doc 112).
- Have they actually tried the self-serve billing portal, and what specifically failed (no email received, no cancel button visible, wrong email)?
- Is there a refund or legal/chargeback threat attached? That changes the escalation path (see below).

**From Help Scout history (live API search by customer email):**
- Has this person already contacted us about this same subscription? Was a manual cancellation or refund already granted or promised?
- Are they emailing from a new address because they lost access to the old one (common pattern — check prior threads under other emails on file).

**From Stripe, once Phase 3 (read-only API) lands:**
- Do they even have an active subscription under the email they gave? Many "cancel me" tickets turn out to be trial users or people with no subscription at all.
- Is it already cancelled or scheduled to cancel (`cancel_at_period_end`)? A lot of "you keep trying to charge me" tickets are really dunning retries on a subscription that's already set to end at period close (conv 3307727165, 3339172710, 3389345814) — the fix is explaining the existing state, not taking new action.
- What email/customer record does the subscription actually live under? It frequently doesn't match the emailing address.

## Policy

- **Self-serve is the default answer, for essentially every ticket, including blunt "cancel now" demands with no stated portal problem.** Point to the Billing button in-app or https://filteronme.com/billing, log in with the receipt email. This is true even for angry, all-caps, or dispute-threat openers (conv 3208656014, 3216581774, 3121420422, 3187137828) — the agent does not skip straight to a manual cancellation just because the customer is upset.
- **Trial ≠ subscription.** If they never entered a card, there's nothing to cancel — we don't hold card info for trial users, and trials auto-expire (conv 3187137828, doc 112).
- **Portal access problems get the login-link workaround, not an immediate manual cancel:** try each email they might have paid with at https://filteronme.com/billing-email — note it does NOT reveal the subscription email, it sends a portal link to a correctly-guessed address (code-verified 2026-07-27; doc 108).
- **Manual, support-side cancellation is reserved for genuine lockouts** — lost access to the email/device the account is under, no way to log in at all, elderly/confused customers, or a subscription with no working self-serve path. In the current process this is *not* something Jona or the agent does directly: the front-line rep posts an internal Help Scout Note tagging `@eddy` with the account email/last-4/details, and Eddy performs the actual cancellation in Stripe, then confirms back via another internal note before the customer-facing reply goes out (conv 3236601462, 3397716209, 3258491021, 3268271602). **This is a write action and stays entirely with a human** — consistent with D7 (agent has no Stripe write access) and D11 (money-adjacent cases stay human-touched).
- **Refunds tied to a cancellation are not the agent's call.** Current standing instruction from Eddy, including under a formal EU/BGB legal threat: give the standard cancellation instructions and hold the no-refund line, do not negotiate (conv 3196455088: *"yes just tell him the usual cancel instructions, close further tickets that request refunds"*). Route refund questions to the billing/refund playbook rather than answering inline — see Escalate section.
- **Never argue with a dispute/chargeback threat.** State the facts calmly (already cancelled, or here's how to cancel) and don't over-explain or get defensive (conv 2593688556: *"Hi this is because your subscription is already cancelled"* in reply to a CAPS "CANCEL IMMEDIATELY" demand).
- **The Filterly disclaimer matters.** A large share of confused/angry tickets are actually about an unaffiliated product with a similar name. Always sanity-check the product/billing descriptor before assuming it's us.
- Historical note: in 2023–2024 Eddy personally cancelled on request for most simple "please cancel" tickets, often in one line, and sometimes paired an immediate cancel with a refund to defuse an active dispute threat (conv 2648825500: *"Your subscription has been cancelled and refunded"*). That founder-does-it-himself pattern is **not** today's process — treat the 2025–2026 self-serve-first / escalate-for-lockouts flow above as current policy (see Notes for the open question this raises).

## How to respond

Decision guide:
1. No stated blocker → send the short self-serve reply. Don't dump the full portal-troubleshooting article at someone who hasn't mentioned a portal problem.
2. Stated portal/login problem → self-serve reply + the specific workaround for what they described (alt email, or the billing-email finder).
3. "Already cancelled but still charged" → check status before replying (see What to check first); this is a billing-playbook question as much as a cancellation one — cross-reference it rather than guessing.
4. Genuinely locked out (lost email/device, no working login at all) → don't promise a cancellation yourself; escalate with an internal note.

**1. How do I cancel (standard, first contact)**

> Hi <FirstName>,
>
> You can cancel anytime at https://filteronme.com/billing — log in with the email on your receipt (not necessarily this one, especially if you paid with Apple or Google Pay).
>
> If you're only on the free trial, there's nothing to cancel — trials auto-expire and we never save a card for them.
>
> Best

**2. Blunt/angry "cancel now" demand, no portal issue mentioned**

> Hi,
>
> You can cancel anytime at https://filteronme.com/billing using the email on your receipt.
>
> Best

**3. "I already cancelled but you charged me again" (cross-reference billing playbook)**

> Hi <FirstName>,
>
> Checking now — if your subscription shows a cancellation date in the portal, that's when it stops; a charge before that date is expected, not a mistake. If it's not showing a cancellation at all, let me know and I'll take a closer look.
>
> Best

*(If Stripe lookup — once available — shows the sub is already set to cancel at period end, say that explicitly with the date, per conv 3268271602 / 3339172710 style: "I see it cancels on <date>, no further charges after that." If it shows an actual unexpected charge on an already-cancelled sub, that's a billing-playbook / needs-human case, not a copy-paste reply.)*

**4. Genuinely locked out — internal escalation note (not sent to customer)**

> @eddy — customer locked out of the email their subscription is under, can't self-serve. Details from ticket: <email(s) mentioned>, last 4 of card if given, <brief reason they can't get in>. Can we cancel on our end?

Tag `needs-human`, do not draft a customer-facing "your subscription has been cancelled" reply until it is actually true. **Eddy's ruling (2026-07-27):** once the read-only Stripe key lands (Phase 3), the agent MAY assert cancellation as fact when Stripe itself shows the subscription `canceled` or `cancel_at_period_end` — a verified read, not a promise. Until then, or when Stripe can't confirm, never assert; escalate.

## Escalate instead (tag needs-human) when

- Customer cannot access the portal at all and has no working login path — needs a human to cancel directly in Stripe.
- Any refund request, with or without a cancellation attached — always cross-reference the billing/refund playbook, never promise or deny a refund inline.
- Legal, chargeback, or dispute threats — including formal consumer-law language (EU withdrawal rights, BGB §312k, "unauthorized renewal," etc.). These carry real financial/legal exposure per D11; don't auto-decline or auto-negotiate even though there's a precedent reply.
- Customer claims they already cancelled but got charged again — verify actual Stripe status first; could be a real billing bug, not just confusion about billing-cycle timing.
- Third parties requesting cancellation on someone else's behalf (e.g., a bill-negotiation/concierge service submitting for the account holder) — verify authorization before acting.
- Requests to cancel/delete "everything associated with" a list of multiple emails — needs manual lookup across accounts.
- Anything that reads as account deletion / data-erasure request rather than plain cancellation (adjacent topic, different handling).

## Doc links to use in replies

- https://help.filteronme.com/article/84-how-to-cancel-subscription — "How to manage or cancel subscription? Billing portal access." last_updated **January 28, 2026**. Fresh; primary link for the standard case.
- https://help.filteronme.com/article/112-how-to-cancel-trial — "How to cancel free trial?" last_updated **January 20, 2026**. Fresh; use when trial-vs-paid is unclear.
- https://help.filteronme.com/article/108-unable-to-get-login-link-to-stripe-billing-portal — "Unable to get login link to Stripe billing portal." last_updated **January 20, 2026**. Fresh; use for portal-access/no-email-received cases.
- https://help.filteronme.com/article/80-what-is-your-refund-policy — "What is your refund policy?" last_updated **August 10, 2025**. Not stale, but it's the one article here that's ~11 months older than the other three and covers the topic (refunds) with the most policy drift historically (see Policy section) — worth Eddy double-checking it still reflects the current hold-the-line stance before the agent leans on it.

## Notes from history

- This is the single largest topic by volume (293/1957, 15%), but most of it is low-drama — the vast majority of both eras' replies are a single exchange ending in either a self-serve link or a one-line confirmation.
- **Process changed over time.** 2023–2024: Eddy personally handled nearly every cancel-subscription ticket himself, often in one sentence ("Your subscription has been cancelled."), and would occasionally cancel-plus-refund on the spot to defuse a dispute threat. 2025–2026: front-line replies are Jona's, self-serve-first, with manual cancellation now happening only behind the scenes for true lockouts via an `@eddy` internal-note handoff. The agent should model the *current* flow, not the old founder-does-it-personally one.
- **Biggest Eddy/Jona divergence:** Jona sends a near-identical five-paragraph block (portal button → trial note → alt-email → billing-email finder → "Stripe is a large payment provider") to almost every ticket verbatim, regardless of what the customer actually asked — including one-line messages like "Stop ✋ I don't want your service" (conv 3312641824) and "WTF" (conv 3154274782). This directly conflicts with TONE.md ("never send a wall of steps when one will do," "one idea per reply"). It also sometimes delays actually answering the question — conv 3307727165 took three rounds of near-identical boilerplate before addressing the customer's actual "stop retrying my card" ask. Recommend the agent draft only the one or two lines relevant to what was actually asked (see example replies above), not the full stock paragraph.
- Jona's tone also runs warmer/more exclamation-heavy ("Thank you for reaching out!!", typos like "Thannk you") than Eddy's flatter, clipped style — dial this back per TONE.md when drafting.
- One conversation (conv 3389345814) shows a customer telling Jona "do not be too Filipino" after repeated canned refund-policy replies — a support-quality/customer-conduct issue independent of cancellation policy, worth flagging to Eddy directly rather than folding into this playbook.
- **Open questions for Eddy:**
  1. RESOLVED (2026-07-27): the agent may state cancellation as fact only when read-only Stripe confirms it (`canceled` / `cancel_at_period_end`); otherwise never assert, escalate.
  2. RESOLVED (2026-07-27): legal/chargeback-threat tickets stay `needs-human` pending the chargeback-economics analysis — see refund-request.md Notes and DECISIONS.md D15.
  3. Once the Stripe read-only lookup (Phase 3) is live, should trial-vs-paid and "which email did you pay with" be resolved automatically from Stripe instead of asked of the customer?
  4. The Filterly-confusion disclaimer appears in nearly every reply today — worth a one-time automated check (matching ticket text / sender domain) instead of boilerplate repeated in every draft?
