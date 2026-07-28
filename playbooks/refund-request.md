---
topic: refund-request
volume: 236 of 1957 (12%)
status: approved 2026-07-27 (chargeback-economics analysis pending — see Notes)
---

# Refund requests

## When this applies

Customer asks for money back — full refund, partial refund, "make an exception,"
a chargeback/dispute threat, a "formal legal demand," or a confused "did you
refund me yet?" follow-up. Includes accidental-renewal, unauthorized-charge/fraud
claims, and currency/price-confusion complaints, since in practice all of these
resolve through the same policy, not a fraud-investigation or legal process.

## What to check first

- **Stripe (Phase 3):** when was the charge, how many charges total, monthly or
  yearly plan, has this customer been refunded before. A same-day or
  within-hours charge (accidental renewal, mis-click) is a materially different
  case from "I've been on this plan for 6 months."
- **Did they already cancel?** If yes, via the self-service portal or did
  support cancel it on the backend? Cancelling on Filteronme's end takes effect
  *immediately* and cuts off access the customer already paid for — the
  self-service portal cancels at end of billing period instead. Getting this
  backwards is what caused the one goodwill exception on record (conv 3227032537).
- **Did they actually use the app?** Check for prior troubleshooting history in
  this thread/HelpScout — has a fix already been offered?
- **Is there a suspicious "as discussed" claim?** Filteronme has no phone
  support. A customer claiming a prior phone call, verbal promise, or "as
  agreed" refund is a red flag, not something to act on (see conv 3042853509 below).
- **Repeat refunder / multiple accounts?** Check email variants (Apple Pay/Google
  Pay can attach a different email than the one used to write in).

## Policy

**Stated policy** (doc 80, last updated Aug 10, 2025): Filteronme does not
offer refunds, period. The free trial is the offered alternative to "try before
you buy." Billing/cancellation is self-service via Stripe only; support cannot
process refunds via email.

**Observed practice has hardened over time and now matches the stated policy
almost exactly.** This is the most important finding for this playbook:

- **2023 (early/beta era):** Eddy personally granted refunds readily and fast —
  for bugs (conv 2352867567, 2409344138), for "purchased by mistake" with no
  technical complaint at all (conv 2327110219), often within hours, one
  sentence, no argument.
- **2024 (transition):** Eddy starts citing "our policy" as an opening move
  (conv 2499494944) even while still granting refunds elsewhere (conv 2614392627,
  double-charge after a cancellation attempt). He also draws a boundary that
  still matters: refund the *current/most recent* charge, but refuse retroactive
  multi-month requests as "unreasonable" — "If you were unhappy with the
  service you should have cancelled earlier" (conv 2472890695, refunded 1 of 3
  months billed, refused the other 2).
- **2025–2026 (current era, ~193 of 236 conversations in this topic, Jona
  De Guzman is the primary responder):** Refunds are essentially never granted,
  full stop, regardless of how sympathetic the case:
  - Documented technical bugs with logs/screenshots (conv 3111141794, 3360099591)
  - Chargeback/dispute threats (conv 2930806784, 2948083784, 3053540563)
  - "Formal legal demand" letters citing consumer law (conv 3226137703 — Eddy's
    internal instruction: *"close this and any other 'legal demands' for
    refunds that come in"*)
  - Financial hardship pleas (conv 2977519960)
  - Unauthorized-charge / fraud claims (conv 2996425149, 3024456111, 3332629059
    — practice is to verify identity, cancel the subscription, and still decline
    the refund)
  - Accidental auto-renewal caught within hours (conv 3288518668, 3368643222,
    3346471492)
  - Currency/pricing confusion (conv 3351742141 — "we're based in the US, all
    payments are charged in USD")
  - "Make an exception" pleas of any kind (conv 2847252438: Eddy explicitly
    told Jona "We don't refund in this case," even for a same-day mistaken
    purchase)

  The stock move is: point to the billing portal for cancellation, point to
  doc 80 for the refund answer, and if pushed further, close the conversation.
  Eddy's own shorthand notes to Jona: *"yes close this"* (conv 3195037757),
  *"close this, it is a refund request"* (conv 3219400744).

- **Non-cash service extensions / credits are the STANDARD remedy for
  support-caused or our-side errors** (Eddy, 2026-07-27): when our mistake cost
  a customer paid access (e.g. immediate backend cancellation, conv 3227032537),
  draft a service-extension/credit offer, not a cash refund. Execution is still
  human-only; tag `needs-human`.
- **The one documented correction of over-granting:** Jona once refunded a
  customer based solely on their claim of "as discussed on our phone call"
  (there is no phone support). Eddy's internal note afterward: *"this should
  not have been refunded... Please do not refund for filteronme in the
  future"* (conv 3042853509). Treat unverifiable claims of prior verbal
  agreements as a reason to escalate, never as grounds to grant.

**IMPORTANT: the agent never executes a refund.** Even in a grant scenario, the
agent drafts language like "I've issued a refund" or "I can look into an
exception" only as a **suggested Note for human review** — a person (Eddy)
issues the actual refund in Stripe and confirms before anything is said as fact
to the customer.

## How to respond

Given current practice, the default path for a fresh, low-context ticket is
**decline-with-policy-link**, not troubleshoot-first and not grant. Only draft
a grant-path reply if there's a **very recent, well-documented, uncontested
operational error on Filteronme's side** (e.g., support cancelled the wrong
way and cut off paid access) — and even then, tag `needs-human` rather than
asserting it's done.

**Decline path (default — matches current practice):**

> Hi [Name],
>
> Thanks for reaching out. To manage or cancel your subscription, use the
> Billing button in the app or visit filteronme.com/billing.
>
> We're not able to offer a refund — here's our policy:
> help.filteronme.com/article/80-what-is-your-refund-policy
>
> Best

**Troubleshoot-first path (when no fix has been offered yet and the complaint
is "it doesn't work," not "give me my money back"):**

> Hi [Name],
>
> Sorry it's not working. A few quick things to try: make sure Filteronme is
> open before your call app, and that you can see yourself in the Filteronme
> preview before selecting it as your camera. If it's already open, try
> File > Reset, then log back in.
>
> Let me know if that fixes it.
>
> Best

**Escalate-for-goodwill path (rare — recent operational error, not a
dissatisfaction complaint):**

> Hi [Name],
>
> Sorry about that — it looks like your access was cut off before your paid
> period ended. I'm flagging this for a manual fix so you get service back
> through your paid term.
>
> Best

(Then tag `needs-human`; do not tell the customer a refund/credit is
confirmed until a person acts on it.)

**Repeat-pushback path (customer already got the policy link and is pushing
again):**

> Hi [Name],
>
> I understand the frustration, but this is outside what we're able to do —
> our refund policy is here: help.filteronme.com/article/80-what-is-your-refund-policy
>
> Best

## Escalate instead (tag needs-human) when

- Chargeback, dispute, or "formal legal demand" language appears — draft the
  standard decline, but tag `needs-human` so a person decides whether to
  respond further or just close (Eddy's own SOP has been to close these, but
  that's a judgment call each time, not something the agent should assume).
- Customer claims a prior phone call, verbal agreement, or "as discussed"
  refund promise — there is no phone support; this pattern has caused an
  incorrect refund before (conv 3042853509).
- Fraud / unauthorized-charge / "someone else used my card" claims — needs a
  human to verify the account rather than a templated decline.
- Any request for a refund covering more than the most recent charge/period
  (backdated multi-month requests) — the "how far back" line has shifted over
  time and should be Eddy's call, not the agent's.
- Support-side error is the actual cause (wrong cancellation timing, double
  charge from a system glitch, etc.) — these are the only cases with a real
  precedent for a non-cash goodwill fix.
- Repeat refunders (same customer/account across multiple past refund tickets).
- Large amounts (annual plans, business/CEO-signature emails) combined with
  any pushback.
- Anything where the agent is not confident the situation matches a pattern in
  this playbook.

## Doc links to use in replies

- Refund policy: help.filteronme.com/article/80-what-is-your-refund-policy
- Cancel subscription: help.filteronme.com/article/84-how-to-cancel-subscription
- Billing portal: filteronme.com/billing
- Billing email finder (can't find login email): filteronme.com/billing-email
- General troubleshooting: help.filteronme.com/article/105-how-to-fix-most-problems
- Full reinstall (Mac): help.filteronme.com/article/123-how-to-do-a-full-reinstall-of-filteronme-for-mac

## Notes from history

- **Refund grant rate is very low and concentrated in the past.** Across the
  236-conversation sample, explicit "refund issued/processed" language
  appears in only ~4 conversations — 2 from 2023 (Eddy, early/generous era)
  and 1 from 2025 that was subsequently reversed/reprimanded internally. In
  the 2025–2026 window, which is ~82% of this topic's volume, the observed
  grant rate for an actual cash refund is effectively **zero**, with one
  documented non-cash (service extension) exception.
- **Eddy/Jona divergence — the opposite of what you might expect.** Jona is
  not softer or harder than Eddy; she consistently escalates ambiguous cases
  to him via internal notes before answering ("Do we allow refund in cases
  like this?"), and he consistently says no. The single deviation on record
  is Jona granting a refund she shouldn't have (based on an unverifiable
  "phone call" claim), which Eddy corrected — not a case of her wrongly
  refusing something he'd have granted. No example was found of Jona refusing
  a refund Eddy would have granted under current policy.
- **Stated-vs-practice gap is really a stated-vs-*past*-practice gap.** Doc 80
  (last updated Aug 10, 2025) accurately describes current behavior. The gap
  is that Eddy personally was much more generous in 2023–2024, and TONE.md's
  "Recurring healthy pattern: proactive refund as the honest exit when
  troubleshooting fails" reflects that older era, not 2025–2026 practice —
  this is worth flagging to Eddy as a possible TONE.md update.

**Eddy's rulings (2026-07-27, see DECISIONS.md D15):**

1. Default decline-with-policy-link CONFIRMED. TONE.md's old proactive-refund
   pattern is historical; this playbook wins.
2. Service extensions/credits: STANDARD remedy for our-side errors (folded into
   Policy above).
3. Chargeback/legal-demand tickets: keep `needs-human` for now. PENDING
   ANALYSIS: once the Stripe read-only key lands (Phase 3), measure how often a
   chargeback *threat* becomes an actual dispute, and what disputes actually
   cost (fee + ~$29/alert Chargeblast). Eddy is open to selectively granting
   refunds to high-follow-through-risk cases if the math favors it — until that
   analysis exists, the agent never grants, only escalates.
4. "Most recent charge only" rule: moot while default is decline; revisit only
   if the chargeback analysis loosens policy.
5. Fraud/unauthorized-charge claims: verify, cancel, decline — but always
   `needs-human` (real card fraud carries dispute risk).
