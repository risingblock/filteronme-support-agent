---
topic: login-account
volume: 84 of 1957 (4%)
status: approved 2026-07-27 (facts code-verified against app v2.1.7 + web)
---

# Login & Account Access


**SEE playbooks/SELF-SERVE-FLOWS.md (D21): lost/unknown-email cases now have full self-serve flows (/billing-email card finder, /recover, /change-email) with deep links — link those first.**

## When this applies

Verification code never arrives or errors out, can't get the Stripe billing-portal
login link, how to sign out, changing/transferring the account email, lost access
to the old email on file, "do I need an account", and account/data deletion
requests.

## What to check first

- **Is the email they're writing from the email they paid with?** The single
  biggest cause of "can't log in" / "no link" tickets is the customer using a
  different email than the one Stripe has on file — especially after Apple Pay
  or Google Pay checkout, which can silently use a different address than
  expected. (Phase 3: once we have read-only Stripe/app-DB lookups, check this
  directly instead of asking.)
- Have they checked spam/junk?
- For verification-code errors specifically: did they request more than one
  code and enter an old one? Requesting a new code invalidates the previous
  one, and codes can arrive out of order — always enter the most recent code,
  and wait ~10 minutes between requests.
- Ask Mac vs Windows only if it changes the troubleshooting step (it usually
  doesn't for login issues).

## Policy

### Verification code never arrives / "Error with verification code, try again"
(conv 2808870379, 2805987740, 2686050540, 2749817240, 3167991440, 3124884874; doc 113)

- Standard fix: wait ~10 minutes, then request one new code. Only request one
  code per 10-minute window — requesting another invalidates the code already
  in flight, which is what produces "Error with verification code, try again."
- If they insist they've waited and retried and checked spam with zero codes
  ever arriving, that can mean their email is bouncing / has been disabled on
  our side (conv 2749817240 — Eddy reactivated a hard-bounced address). Agent
  can't check or fix this itself — escalate with the exact email used.
- Don't claim "we just shipped a fix" unless a current playbook note says a
  real fix shipped recently — Eddy has said this before (conv 2808870379) but
  only when true.

### Billing portal link ("manage subscription" email) not arriving
(conv 3236800785, 3201927098, 3286426672, 2591879768; doc 108)

- Most common cause: wrong email. Ask them to try any other email they own
  at **filteronme.com/billing-email**. IMPORTANT (code-verified 2026-07-27):
  that page does NOT reveal which email a subscription is under — it emails
  a portal login link IF the entered address has a subscription. Never tell
  a customer it will "look up" or "show" their email; say "try each email
  you might have used there — the one with the subscription will receive a
  login link." (If they've lost access to the right email entirely → the
  transfer flow / doc 140 instead.)
- Ask them to check their bank/card statement or receipt — real charges say
  **FILTERONME.COM** or **Filteronme**. A similarly-named company **Filterly**
  is a different business we're not affiliated with; if that's what they mean,
  redirect them to Filterly's own support.
- Free trial only (no payment yet) = no Stripe record = no login email will
  ever be sent. This is expected behavior, not a bug — say so plainly.
- If they've genuinely tried every email they have and still get nothing,
  escalate — Eddy can look the customer up in Stripe directly.

### Sign out / log out
(conv 3266707829, 3201927098; doc 109, 90)

- Simple: Settings tab → Sign out button. No escalation needed, just link/quote
  the doc.
- Watch for this dressed up as a trial-reset request ("I can't sign out to
  start a new trial") — we don't offer repeat trials, one 7-day trial per
  person, no exceptions (Eddy, conv 3266707829, 2026-03-23). State the policy
  once, don't argue further; escalate only if they push back with a dispute
  threat.

### Change email / transfer subscription (customer still has old-email access)
(conv 3399074605, 3383009920, 3314040890, 3335046178 first turn; doc 132)

- Self-serve: send them to **filteronme.com/change-email**. This works as long
  as they can still receive mail at the old address.
- Even if the customer pastes everything doc 140 asks for (old email, new
  email, last 4 of card, billing address, etc.) unprompted, still point them
  to the self-serve link first if there's no indication the old email is dead
  — don't do the change manually just because the info was volunteered. Agent
  has no write access to make this change regardless.
- Only escalate this sub-case if they come back saying the self-serve flow
  itself failed.

### Lost access to the old email (self-serve change/transfer is not possible)
(conv 3335046178 full thread, 3212508542, 3232573634, 2787212096, 3055378830; doc 140)

- This is always a manual account-record change with identity verification —
  **tag needs-human immediately**, don't attempt to send the self-serve link
  once they've said the old email bounces/is gone.
- If they haven't already supplied it, ask for as much of this as possible
  (per doc 140): old account email, new email, most recent charge date and
  amount, last 4 digits + brand of the card, name and billing address on the
  card, any receipt/invoice number, and whether they might have more than one
  Filteronme account. If they already gave this in their first message, don't
  re-ask — just escalate.
- Set expectations honestly: manual review, can take 5–10 business days or
  longer, no guaranteed date.
- Note for Eddy, not for the customer: when a clean Stripe transfer isn't
  possible and the account has to be recreated under the new email, you've
  sometimes issued a single-use 100%-off coupon so the customer isn't double
  charged (conv 3314040890 / 3335046178, code `lisajjamovesubscription`
  pattern). That's your judgment call each time — the agent should never
  offer or predict a coupon, just escalate and let you decide.

### Do I need an account?
(doc 91)

- No separate signup: entering an email auto-creates an account, and a code is
  emailed to log in. The same email always logs back into the same account.
  This rarely needs more than the doc quoted back.

### Delete account / delete my data
(conv 3253343839, 3286426672, 3302823366, 3305368004, 3360244901, 3361523655,
3394565793, 2462204607)

- Reasoning note for the agent (not a line to send the customer): because
  accounts are created automatically on login, deleting one that still has an
  active subscription doesn't accomplish what the customer wants — it can
  effectively get recreated. Always establish subscription status first.
- **Active paid subscription still running:** tell them to cancel first via
  the billing portal (the "Billing" button in-app, or filteronme.com/billing).
  Deletion of the account/personal data follows after cancellation.
- **Free account, or subscription already cancelled:** this is a genuine
  deletion request. The agent has no delete capability — **always tag
  needs-human**. Eddy has been handling these directly (conv 3394565793: "no
  subscription found, deleted his free account").
- Don't reflexively send the "check your receipt, might be Filterly" deflection
  that shows up on several 2026 deletion tickets — most of these customers
  clearly mean Filteronme and that reply just stalls a simple request. Confirm
  subscription status and escalate instead.
- Escalate (don't improvise) on: account owner deceased (conv 3305368004 —
  Eddy cancelled the sub as a compassionate gesture), and "hide my email"
  relay addresses where the requester can't be emailed back directly at the
  account address (conv 3360244901 — Jona flagged it as a possible privacy
  wrinkle and it was never resolved in the thread). Both need Eddy's judgment.

## How to respond

**Verification code error:**
> Hi Paul,
>
> Please wait ~10 minutes and try again. Only request one login code every ~10
> minutes or so — requesting a new one invalidates the previous code.
>
> Best

**Billing portal link not arriving:**
> Hi,
>
> Try each email you might have used to pay at filteronme.com/billing-email —
> the one your subscription is under will receive a login link (it usually
> takes a couple tries). Also worth checking your card statement:
> charges from us say FILTERONME.COM. If your subscription is still on a free
> trial, no billing email will go out — that's expected, not a bug.
>
> Best

**Lost access to old email:**
> Hi,
>
> Sorry about that — since you no longer have access to that inbox, I'll need
> to verify you own the subscription before I can move it. Could you send: your
> old account email, the new one you'd like to use, your most recent charge
> date and amount, and the last 4 digits + brand of the card on file?
>
> This kind of change is handled manually so it can take a little while — I'll
> follow up once I have it sorted.
>
> Best

**Account deletion, subscription still active:**
> Hi,
>
> To cancel first, click "Billing" in the app (or go to filteronme.com/billing)
> — that'll take you straight to our billing portal. Once it's cancelled, let
> me know and I'll take care of deleting the account.
>
> Best

## Escalate instead (tag needs-human) when

- Verification codes never arrive despite spam check + wait-and-retry — possible
  email bounce/block on our side that needs backend confirmation.
- Billing portal link never arrives after trying all known emails.
- Any email change/transfer where the customer has lost access to the old
  email (doc 140 path) — always, no exceptions, this is a real account-record
  change.
- Self-serve change-email tool reported as broken/failing by the customer.
- Any account/data deletion request once subscription status is confirmed —
  the agent cannot delete anything.
- Deceased account holder, relay/hide-my-email addresses, or anything else
  where verifying the requester's identity or right to the account isn't
  straightforward.
- Suspected systemic login bug (2+ independent reports in a short window)
  rather than an individual account issue.

## Doc links to use in replies

- Verification code errors: help.filteronme.com/article/113
- Billing portal link: help.filteronme.com/article/108
- Sign out: help.filteronme.com/article/109
- Change email / transfer subscription: help.filteronme.com/article/132
- Lost access to email: help.filteronme.com/article/140
- Do I need an account: help.filteronme.com/article/91
- Billing portal link sender (NOT a lookup — sends a login link if the
  entered email has a subscription): filteronme.com/billing-email
- Self-serve change email: filteronme.com/change-email
- Billing portal: filteronme.com/billing

## Notes from history

- Jona divergence: the "check your receipt/card statement, might be Filterly"
  reply is overused as a generic first response to deletion and lost-access
  tickets where it doesn't fit — a poor pattern per DECISIONS.md D12, don't
  copy it as policy.
- RESOLVED (Eddy, 2026-07-27): for accounts behind "hide my email" relay
  addresses, be customer-first — if they can prove ownership (doc 140's
  payment-verification checklist: last charge date/amount, card last-4 +
  brand, name on card), deletion/cancellation proceeds. Execution is
  human-only; the agent drafts the verification-request reply and tags
  `needs-human` (conv 3360244901).
- The one-time 100%-off coupon workaround for failed email transfers (conv
  3314040890/3335046178) is ad hoc, Eddy-issued case by case, and not standing
  policy — the agent should never generate or promise a coupon code itself.
- Docs 132 and 140 were both updated May 7, 2026 and read as the current,
  coherent policy pair (self-serve if you have the old email; manual/verified
  if you don't). Docs 90 and 91 are stale (July 2024) but their content still
  matches current behavior in the tickets read.
