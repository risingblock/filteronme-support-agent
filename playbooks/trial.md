---
topic: trial
volume: 48 of 1957 (2%)
status: draft-for-eddy-review
---

# Free trial: cancelling, "will I be charged?", expired, extend, and free-version confusion

## When this applies

Customer asks how to cancel a trial, worries they'll be (or already were)
charged during a trial, says their trial expired before they could use it,
asks for a reset/extension, or is confused about the difference between the
watermarked free version and the 7-day premium trial.

## What to check first

- (Phase 3) Look the customer up in Stripe/the app by email. Most "will I be
  charged" and "I got charged during my trial" tickets resolve immediately
  once you see whether they actually have a paid subscription. A real trial
  cannot charge anyone — if a charge exists, they upgraded (knowingly or not)
  and this is really a billing/cancel ticket, not a trial ticket (conv
  3271193503 — customer thought she was on trial, was actually "subscribed
  already billed yearly"; conv 3221197989 — customer says trial "charged
  instantly," never confirmed either way before replying, which is a gap, not
  a model to copy).
- If they're asking about a reset/extension, check whether this is a repeat
  request from the same email/device — Eddy has said no to near-identical
  asks from other customers (see Policy).

## Policy

- **No card required, ever, for the trial itself.** Signing up for the trial
  does not collect payment info. It auto-cancels on its own — there is
  nothing to cancel and nothing that will charge them (docs 112; conv
  2893864676, conv 3135356291, conv 2942075487, conv 2874075623-adjacent
  wording). This is the single most-repeated fact in the whole topic and is
  safe to state with confidence.
- **The trial is 7 days and starts on account creation**, per Eddy (conv
  2646025175: "the trial starts when you create an account"). In practice
  several customers report it starting the moment they launch the app,
  before they felt "ready" (conv 2874955077) — flag this as a real product
  behavior gap, not customer error, but don't promise a fix.
- **There are two different free things — don't conflate them:**
  - *Free version*: permanent, has a watermark, no time limit, no account
    needed (conv 2328316599 — Eddy: "No time limit is enforced at the
    moment, just the watermark"; conv 2454589821).
  - *Free trial*: 7 days of full premium (no watermark), requires creating
    an account, auto-expires.
  Several tickets are really "I didn't realize the watermark-free trial was
  time-limited" (conv 2632623812-style, conv 2454589821) — clarify which one
  they're on.
- **We do not extend or reset trials as standing policy** (docs 134 — "We
  are unable to extend any free trials... Please consider subscribing").
  The current default reply (Jona, 2025–2026) is a polite no plus "the trial
  resets automatically after some time" — do not commit to a specific
  duration; Eddy has given inconsistent numbers across tickets ("a couple of
  months," docs 134's "every few months," "a month or so" in conv
  3347988527). Say "after some time" / "after a while," not a number.
- **In practice, Eddy personally overrides this often** — this is the
  central tension in the topic and the reason it needs a human in the loop:
  - 2023–2024 (Eddy directly answering): routinely granted manual free-
    premium extensions for sympathetic cases — sick customer who missed her
    trial (conv 2819326611, "free premium until Feb 1st"), never-used trial
    reporting as expired (conv 2692047248, conv 2676498635), a bug-report
    follow-up (conv 2785658951).
  - 2025–2026 (Jona fields the ticket, escalates to Eddy via internal note
    when the ask seems reasonable): Eddy approved extensions for a
    camera-setup delay (conv 3206106434, "extended it for a few days") and a
    secondhand-Mac hardware lock where the buyer had never used the app
    (conv 3214902202, "extended free trial for a week... go to settings >
    logout and sign in with their email to get the trial again").
  - Eddy declined near-identical-sounding asks: a customer who wanted the
    trial reset because they hadn't used it during the original window (conv
    3174467811 — "No, they can pay for the subscription or wait for the
    trial to reset"), a customer without new equipment yet (conv 3347988527),
    and general "I want to try it again before I buy" requests without a
    concrete blocker (conv 3376584624, conv 3379022156, conv 2874955077).
  - The pattern isn't purely random: approvals cluster around a specific,
    verifiable blocker outside the customer's control (illness, gear not
    arriving yet, secondhand device with someone else's trial already
    burned) and the customer never having actually used the trial. Pure "I
    want another shot" or "I wasn't ready" asks get the standard no. This
    playbook should not try to auto-approve extensions — always escalate
    (see below) rather than guess which side of the line a request falls on.
- Cancelling a **paid** subscription (not a trial) is out of scope here — see
  the billing/cancel-subscription playbook; the standard line is the
  "Billing" button in app controls or filteronme.com/billing.

## How to respond

Trial hasn't converted to anything, no charge is possible:

> Hi [name],
>
> Our free trial doesn't require a credit card and cancels automatically —
> there's nothing you need to do. If you never upgraded to premium, we don't
> have any payment info on file to charge.
>
> Best

Trial expired before they got to use it (no clear extenuating blocker —
default no, but flag internally for you rather than silently refuse if the
story is sympathetic):

> Hi [name],
>
> Sorry about that! The free trial is 7 days and resets automatically after
> some time, but we're not able to extend or reset it manually. You're
> welcome to subscribe now, or try again once it resets.
>
> Best

Confused about watermark/free version vs. the timed trial:

> Hi [name],
>
> Just to clarify — the free version (with the watermark) has no time limit.
> The 7-day free trial is what removes the watermark, and that's the part
> that expires.
>
> Best

## Escalate instead (tag needs-human) when

- Any extension/reset request with a concrete, verifiable blocker the
  customer didn't cause (equipment delay, illness, secondhand/inherited
  device that already burned someone else's trial, trial auto-started on
  launch before they touched it). Eddy has approved these before case by
  case — don't send the standard refusal without asking him first, and don't
  grant it yourself either.
- Customer insists they were charged during a trial — verify in Stripe
  before replying at all; if a charge is real, this becomes a billing ticket,
  not a trial ticket.
- Angry/legal-threat tone (e.g. conv 2794630459) — still just state the
  facts calmly (no premium = no billing tab = nothing to cancel), but tag for
  visibility rather than letting the agent be the only reply on a heated
  thread.
- Anything asking to change how the trial itself works (e.g. "warn users
  before their trial auto-starts on launch," conv 2874955077's feedback) —
  route as product feedback, don't promise a change.

## Doc links to use in replies

- https://help.filteronme.com/article/112-how-to-cancel-trial (last updated
  2026-01-20)
- https://help.filteronme.com/article/134-how-to-extend-free-trial (last
  updated 2026-01-22)
- filteronme.com/billing, filteronme.com/billing-email (only relevant once
  someone has an actual premium subscription)

## Notes from history

- Jona's canned reply for "will I be charged / how do I cancel" (docs
  112's exact wording, reused verbatim across conv 2893864676, conv
  3135356291, conv 2942075487) is accurate and safe to reuse as-is.
- Jona's canned reply for "please extend/reset my trial" always escalates to
  Eddy via an internal note first in 2025–2026 tickets — the agent should
  copy that behavior (escalate, don't auto-decide) rather than copying only
  the final customer-facing text.
- One Jona reply (conv 2874075623) is confusing/possibly wrong — it tells a
  trial user "our free trial comes with watermark" and pushes premium
  pricing without clarifying the free-version-vs-trial distinction. Don't
  treat this one as a model reply; flagging for Eddy to confirm which
  product tier that customer was actually on.
- Open question for Eddy: how long does a trial actually take to "reset"?
  Docs say "every few months," you've told customers "a couple of months"
  and "a month or so" in different tickets. Worth picking one true number (or
  confirming there isn't one) so the agent doesn't have to hedge.
- Open question for Eddy: does the trial start at account creation or at
  first app launch? Your 2024 answer (conv 2646025175) says account
  creation; a 2025 customer's account was activated the instant the app
  launched, before any real usage (conv 2874955077). If launch-triggered
  activation is expected behavior, it's worth a one-line mention in docs 112
  so this stops generating "it started without me doing anything" tickets.
