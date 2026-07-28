---
topic: billing-issue
volume: 190 of 1957 (10%)
status: approved 2026-07-27 (facts code-verified against app v2.1.7 + web)
---

# Billing issues (charges, declines, payment methods, price)

## When this applies

- **Charged after cancelling** — customer says they cancelled but a charge still
  went through (or keeps recurring).
- **Duplicate / double charge** — two charges in a period they expected one, or
  an annual renewal mistaken for a duplicate.
- **Card declined** — checkout or renewal fails ("your card doesn't support this
  type of purchase", "keeps declining").
- **Payment methods** — "do you accept PayPal / GCash / [local currency]?",
  can't find an option at checkout.
- **Dunning / failed-payment emails** — customer replies to a Stripe
  "payment unsuccessful" email, often asking us to manually re-invoice them.
- **Price questions on existing subs** — monthly vs. yearly confusion, "why is
  this more expensive than X".
- **Discount requests** — asking for a coupon, local-currency pricing, or a
  price break because a competitor is cheaper.

Not this playbook: pure "please cancel me" with no dispute over money (→
`cancel-subscription`), refund requests with no confusion about the charge
itself (→ `refund-request`), and "I don't recognize this company" cases where
the customer never had a FilterOnMe account at all (→ `filterly-confusion`,
56 convs — see below).

## What to check first

1. **Read the full thread** — many of these are multi-message and the real ask
   is buried three replies down (conv 3056656594: customer asked "how do I pay"
   and got a canned PayPal answer that had nothing to do with the question;
   Eddy had to correct it).
2. **Search Help Scout / the live account by the email in the ticket.** If
   there is no FilterOnMe account or subscription under that email (or any
   plausible variant), stop and cross-check the **filterly-confusion**
   playbook before answering — "charged after cancelling" and "I never signed
   up" are very often actually Filterly (a different, unaffiliated product)
   confusion, not us. The tell: the customer can't get a login/portal email
   because there's genuinely no Stripe customer record for them (conv
   2905250299, 3197826113, 3380800075, 3205968548, 3210971695 — all resolved
   as "you are not subscribed to us but to Filterly").
3. **(Phase 3, once Stripe read access exists) Pull the actual subscription
   state and charge history** — status (active/past-due/scheduled-to-cancel),
   last N charges with dates/amounts, and whether a dispute was ever filed on
   this customer. Until that's wired up, ask the customer for the email on
   the receipt/portal and check Help Scout's own record of past replies on
   this email first.
4. Check whether this is a **once-per-year charge mistaken for a duplicate**
   (conv 3345970567 — two charges a year apart, not two in one year) before
   assuming anything is wrong.

## Policy

- **Self-serve first, always.** The billing portal (Billing button in the app,
  or filteronme.com/billing) is the answer to nearly everything: cancel,
  change plan/billing cycle, update card, see receipts. We do not make
  billing changes by email. (conv 2663438897, 2794482489, and the large
  majority of Jona's replies all point here first.)
- **No refunds by default** — see `history/docs/80-what-is-your-refund-policy.md`
  (last updated Aug 10, 2025): no-refund policy, free trial exists precisely
  so people test compatibility before paying, refund requests via email get
  no response, all billing goes through the portal. This is Eddy's stated,
  current policy — link it rather than re-explaining it.
- **No discounts for new customers, ever. One exception (Eddy, 2026-07-27):
  goodwill discounts/credits for LONG-TENURED existing customers when we did
  something wrong (double charge, our-side error). Execution is human-only —
  draft + `needs-human`.** Historical evidence: declining since at least
  July 2024 (TONE.md dates
  this "early 2025"; evidence shows Eddy already declining discount requests
  in conv 2661336370, Jul 2024, and again in conv 2802731584, Jan 2025 — same
  wording both times: "We no longer give discounts out, the yearly membership
  is already heavily discounted compared to the monthly."). Applies to local-
  currency requests too (conv 2988306658, Brazil: "We only accept payments in
  USD"). Never haggle, never offer a one-off "just this once."
- **No PayPal, no GCash, as of the July 2026 docs snapshot.** Accepted:
  Stripe-processed cards, Apple Pay, Google Pay, Stripe Link, Amazon Pay,
  Cash App, and (added ad hoc for a blocked EU customer, conv 2816388839)
  SEPA direct debit. See `history/docs/118-do-you-accept-paypal.md` and
  `history/docs/128-how-to-pay-with-gcash.md` (both "Last updated January 20,
  2026"). GCash *cards* sometimes work as a normal card at checkout — the
  card-decline advice below applies; a raw GCash account does not work.
- **Declined cards** are Stripe's call, not ours: "Stripe blocks transactions
  for various reasons" is the honest, complete answer. Standard next step:
  try a different card, or one of the alternate payment methods above. We
  cannot manually push through or invoice a failed payment (conv 2961151551:
  Eddy explicitly refused to manually invoice after a decline — "they need to
  use the stripe portal").
- **Failed-payment auto-collection after a legitimate cancellation is a known
  bug class**, not user error — Eddy shipped a fix around Aug 10 2025 so that
  cancelling also stops auto-collection on past-due invoices (conv
  3034159507), but it only applies going forward, so older cancellations can
  still see this. When a customer insists they cancelled and is still being
  charged, and the account genuinely shows a cancel event, escalate for Eddy
  to manually stop the auto-charge/collection rather than repeating the
  portal instructions a third time.
- **Yearly vs. monthly is the same product** — yearly is simply discounted
  vs. paying monthly (conv 2776086936). Switching cycles gets a prorated
  credit for unused time (`history/docs/115-change-to-yearly-or-monthly-billing-cycle.md`,
  last updated Jan 20, 2026).
- **Chargebacks/disputes end the relationship for that charge.** Once a
  customer disputes with their bank, we do not owe them anything further on
  that dispute and will not issue a second refund on top of a lost dispute
  (conv 3094193842 — Eddy: "no further refunds for this customer, we will
  ban permanently if they dispute again"). Filing a dispute is explicitly
  flagged elsewhere as economically painful for a small business (conv
  2686116379) and used as grounds to stop servicing that email.
- **Eddy does step in personally** for genuine account-level bugs or mix-ups
  that aren't the customer's fault: crediting a free month for a billing
  mix-up (conv 3143804112), manually cancelling a subscription with no
  self-serve trail (conv 2794482489), clearing a stuck subscription so a
  customer can restart (conv 3185774130), refunding a clear double-charge
  from an internal error (conv 2726098394). These are all human, one-off
  Stripe actions — the agent's job is to surface the evidence, not perform
  them.

## How to respond

Default to the portal + payment-method template unless the thread shows
something more specific is actually being asked (read step 1 above — don't
copy-paste the generic block onto an unrelated question).

**Charged after cancelling / can't cancel:**
> Hi [Name],
>
> To manage or cancel your subscription, click the "Billing" button in the
> app, or go to filteronme.com/billing and log in with the email on your
> receipts. If you don't get a login email, try another email address you
> may have used — or use filteronme.com/billing-email to look it up.
>
> Also worth checking: your card statement should say WWW.FILTERONME.COM or
> Filteronme. A few other companies with similar names aren't affiliated
> with us.
>
> Best

**Duplicate charge, unclear which account:**
> Hi [Name],
>
> I only see one payment under [email] — the charge you're seeing might be on
> a different email address, or it could be the once-a-year renewal rather
> than a second charge. Could you send me the other email you might have
> used, and the exact dates on both charges?
>
> Best

**Card declined:**
> Hi [Name],
>
> Sorry about that — we use Stripe to process payments and they sometimes
> block cards for reasons outside our control. Could you try a different
> card, or Apple Pay / Google Pay / Stripe Link at checkout?
>
> Best

**Discount / local pricing request:**
> Hi [Name],
>
> We don't offer discounts — the yearly plan is already discounted compared
> to paying monthly, so that's the best rate we have.
>
> Best

## Escalate instead (tag needs-human) when

- Any actual Stripe action is needed: refund, credit, manually cancelling a
  subscription, clearing/resetting an account, stopping auto-collection on a
  past-due invoice. The agent never touches money or subscription state.
- The customer threatens or has already filed a chargeback/dispute — Eddy
  decides refund-vs-fight case by case and this affects future service.
- The charge origin is genuinely unclear after checking Help Scout/Stripe
  history (can't find a matching payment, amount doesn't match anything on
  file) — don't guess.
- A customer is angry/all-caps/threatening reviews or legal action — these
  get a human regardless of how simple the underlying billing question is.
- Anything requesting a payment method or price exception not covered above
  (e.g., invoicing outside Stripe, wire transfer, crypto specifics).

## Doc links to use in replies

- filteronme.com/billing — self-serve portal
- filteronme.com/billing-email — billing email finder
- https://help.filteronme.com/article/80-what-is-your-refund-policy
- https://help.filteronme.com/article/108-unable-to-get-login-link-to-stripe-billing-portal
- https://help.filteronme.com/article/115-change-to-yearly-or-monthly-billing-cycle
- https://help.filteronme.com/article/118-do-you-accept-paypal
- https://help.filteronme.com/article/128-how-to-pay-with-gcash
- https://help.filteronme.com/article/84-how-to-cancel-subscription (referenced by Jona for cancel flow)

## Notes from history

- The single most common reply, across both Eddy and Jona, is some
  combination of: portal link, free-trial-needs-no-card, "check your
  statement says WWW.FILTERONME.COM", billing-email finder. That block covers
  a large share of the 190 tickets and is safe to draft confidently.
- **Jona divergence (quality, not policy):** Jona frequently fires the
  templated "check your statement / not affiliated with Filterly" block at
  tickets that already show the charge *is* from FilterOnMe and the customer
  has already proven it (conv 3263004357 — customer replies with the exact
  statement line, gets a near-identical canned reply back; conv 3094193842 —
  a legitimate duplicate-charge dispute got five rounds of template/context
  mismatches before Eddy intervened directly). Per D12, do not copy Jona's
  reply *content* as policy — read the thread and answer the actual question,
  matching Eddy's more specific, situation-aware replies instead.
- Non-USD/GCash-card customers sometimes just need a nudge to sign out of
  Stripe Link to reveal Apple/Google Pay options (per the GCash doc) — worth
  offering before declaring a payment truly impossible for that customer.
- Eddy's replies are consistently short (1–3 sentences) even on emotionally
  loaded tickets ("fraud", "reporting this") — he doesn't mirror the
  customer's escalation in tone, just states facts plainly.

**Resolutions (2026-07-27, Eddy + codebase verification):**
- Auto-collection fix CONFIRMED in code (commit e7212c0, 2025-08-10): when a
  cancellation is requested (or a payment is disputed), all *open* invoices
  get `auto_advance: false`. Caveats verified in code: it triggers on the
  cancel/dispute transition only, does not void invoices, and there is no
  `invoice.payment_failed` handler — so pre-Aug-2025 cancellations or edge
  cases can still surface as "charged after cancel". Those go `needs-human`.
- Payment methods: checkout uses Stripe Payment Links, so the method list
  lives in the Stripe dashboard, not code. Exception verified in code: SEPA
  is offered only to customers geolocated in Austria/Germany (euro payment
  links). Don't promise any specific wallet; say "Stripe offers several
  payment methods at checkout — try another one."
- Discounts (Eddy's ruling, D15): none for new customers; goodwill
  discount/credit only for long-tenured customers wronged by us, human-only.
  Two legit coupon mechanisms DO exist in code and are not "discounts to
  hand out": per-user **referral promo codes** ($10 credit to the referrer)
  and one campaign coupon (`choctalk`). Never generate or promise codes.
