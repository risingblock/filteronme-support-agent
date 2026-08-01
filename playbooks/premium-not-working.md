---
topic: premium-not-working
volume: 86 of 1957 (4%)
status: approved 2026-07-27 (facts code-verified against app v2.1.7 + web)
---

# Premium not working (paid but watermark/lock still shows)


**SEE playbooks/SELF-SERVE-FLOWS.md (D21): past_due is the top hidden cause — app/restore-flow messaging fixed 2026-08-01; drafts should send the billing portal link to fix the card, and Pattern C's 'cancelled on [date]' wording is for genuinely cancelled subs only.**

## When this applies

Customer says some version of: "I paid but the watermark is still there," "it
says no premium account found," "trial expired but I already paid," "premium
features (Smile/Hair/Beard/Makeup/etc.) are locked," or "restore purchase
doesn't work." This is almost always an **account-matching problem**, not a
broken feature: the email logged into the app isn't the email Stripe has
marked premium.

Not this topic: general crashes/freezing/lag with no mention of payment or
watermark (see performance/compatibility playbook instead), or "how do I
upgrade" from a trial user who hasn't paid yet (→ doc 116).

## What to check first

Before writing anything, look the customer up — this is THE topic where an
account lookup resolves most tickets instantly instead of a troubleshooting
back-and-forth:

1. **Help Scout history by email** — has this customer emailed before under a
   different address? Repeat/duplicate subscriptions are common (conv 2690454853).
2. **(Phase 3, live app DB / Stripe, read-only):** is the email they're typing
   into the app actually marked premium? If not — which email *did* they pay
   with? Cross-reference the Stripe customer record (charge email) against the
   email in their ticket; these are frequently different (conv 2350224364:
   paid with one address, logged in with a completely different one).
3. Check subscription **status**, not just existence: past-due, failed
   payment/direct debit, or auto-cancelled (5 failed payments) all present to
   the customer as "no premium account found" and look identical to a wrong-email
   issue until you check billing status (conv 2690454853, conv 2828691638,
   conv 3004305304, conv 3382073890).
4. If everything checks out on our end (correct email, active subscription)
   and it still doesn't work, that's the signal this may be a real bug, not
   user error — see Policy below.

**Until Phase 3 tooling exists, draft the diagnostic question rather than
guessing** ("What email did you use to pay? I don't see anything special on
the ticket") — do not paste the canned fix blind (see Notes on Jona below).

## Policy

Canonical fix sequence, in order, distilled from Eddy's replies:

1. **Confirm the account is actually premium**, and state the specific email:
   "I see your email is premium: `x@example.com`" (conv 2690454853, conv
   2664419134). This single check is the fastest way to tell user error from
   a real bug — if premium is set, next step is a client-side refresh; if not,
   it's a billing issue.
2. **Log in with the purchase email** — ask what email they paid with if the
   logged-in one shows no subscription; people frequently pay with one email
   (often a work/secondary address on the receipt) and open the app logged
   into another (conv 2350224364, conv 3057432187). Log out via the Settings
   tab.
3. **"I already have a premium account" button** — if they're stuck on a
   trial-expired screen, this restores/re-syncs the subscription without
   reinstalling. This is the current name of the button as of the most recent
   tickets (through July 2026) — see Notes for a naming discrepancy with the
   docs site.
4. **Reset / reboot the app**, then **restart the computer** — Mac: "Reset"
   button bottom-left. Windows: File > Reset (top-left). This clears a stale
   local cache of the subscription state (conv 2417329808, conv 2364657181,
   conv 2334180928).
5. **Reinstall / upgrade to the latest version** — the old app has sometimes
   been fully deprecated (conv 2523322913: "please upgrade to our latest
   version... the old version has been deprecated"). Link
   filteronme.com/downloads.
6. If none of that works and premium *is* correctly set on our end: offer to
   log into their account directly to reproduce (conv 2414806198), or escalate
   to Eddy for a manual backend fix — see below. Eddy's actual backend fixes
   in this bucket: manually flip the account to premium (conv 2350224364, conv
   2470128582), move a subscription from one email to another (conv 3057432187),
   fix a broken coupon code (conv 3382073890), or issue account credit for the
   inconvenience (conv 2664419134, conv 2831833443 [$20], conv 3235403912 [$10]).

**Bug vs. user error:** Treat as user error (steps 1–5) until the account is
*confirmed* premium and still failing after reset — at that point stop
guessing and either reproduce it yourself or hand to Eddy. Never argue with
the customer about whether it's a bug; either investigate or state the
account facts plainly.

## How to respond

**Pattern A — wrong/second email (the most common case):**
> Hi,
>
> I see your email is premium: customer@example.com
>
> Please reboot the app and try again.
>
> Best

**Pattern B — trial-expired screen, haven't checked account yet:**
> Hi,
>
> Make sure you're logged into the correct email account — the one you paid
> with. You can log out in the Settings tab.
>
> If you're on a trial-expired screen, click "I already have a premium
> account."
>
> Best

**Pattern B2 — the app itself broke at/after payment (preview gone, camera
stopped, features dead — not just watermark). Per Eddy's dry-run grading
(2026-07-27): pair the account check with real troubleshooting, don't send
login-advice alone:**
> Hi,
>
> Sorry about that. Two things to try:
>
> 1. Log out (Settings tab) and back in with the email you paid with — if you
> see a trial-expired screen, click "I already have a premium account."
> 2. If the preview is still blank, reboot the app (File > Reset), and if
> that doesn't fix it, reinstall the latest version from
> filteronme.com/downloads.
>
> Let me know if it's still broken after that — are you on Mac or Windows?
>
> Best

**Pattern C — confirmed billing problem (past due / failed payment):**
> Hi,
>
> Looks like your payment failed and the subscription was cancelled on
> [date]. Please head to filteronme.com/billing to update your payment
> method.
>
> Best

**Pattern D — after manual backend fix:**
> Hi,
>
> I manually set your account to premium — reboot the app and you should be
> good to go. Sorry for the inconvenience.
>
> Best

## Escalate instead (tag needs-human) when

- Account is confirmed premium (correct email, active subscription) and the
  standard reset/reinstall sequence still fails — needs a backend look or
  screen-share, not another canned reply.
- Any request to move a subscription between emails, manually flip premium
  status, apply/fix a coupon code, or issue a credit/refund — all
  write/money actions, human-only per the guardrails.
- Duplicate/concurrent subscriptions under one customer, or disputes about
  which of several payments is active.
- Customer mentions chargeback, dispute, "consumerfinance.gov," BBB, or a
  deadline/threat — de-escalate by handing to Eddy immediately, don't keep
  looping canned troubleshooting (this is exactly what went wrong in conv
  3235403912).
- Same canned reply has already been sent once and the customer says it
  didn't help — repeating it verbatim a second time is a known failure
  pattern (see Notes). Escalate rather than resend.

## Doc links to use in replies

- https://help.filteronme.com/article/83-i-already-have-premium-but-its-not-working
  — "Premium not working, how to fix?" (last updated Jul 26, 2024, but content
  still matches what agents send through July 2026 — still accurate, just old).
- https://help.filteronme.com/article/116-how-to-remove-watermark-by-upgrading
  — for trial users who haven't upgraded yet, not this topic's core case
  (updated Jan 20, 2026).
- https://help.filteronme.com/article/136-restore-purchase-or-access-existing-subscription
  — RESOLVED by codebase verification (2026-07-27, app v2.1.7 / web controls):
  **both names are current, same underlying flow.** The trial-expired modal's
  button says "I already have premium"; the side panel link says "Restore
  purchase". Either opens the restore dialog: enter the email the subscription
  is under → a 6-digit code is emailed **to the subscription's email** (not
  the requester's) → verify → "close and reopen the app". Only works for an
  *active* subscription; it's blocked if the current login already has one.
  If the sub was previously transferred away, the dialog says where it went
  (censored). Use whichever name matches where the customer is: trial-ended
  screen → "I already have premium"; otherwise → "Restore purchase".
- filteronme.com/downloads (reinstall/upgrade), filteronme.com/billing
  (payment method update).

## Notes from history

- **Jona divergence (see DECISIONS.md D12):** Jona's default move is to paste
  the doc-83 canned paragraph immediately, before checking the account —
  visible verbatim across many tickets (conv 3074219615, conv 2831833443,
  conv 3235403912, conv 3323529036, conv 3395506892). When the real problem
  is billing status (past due, cancelled) or a genuine account-side glitch,
  this wastes multiple round-trips and visibly frustrates customers (conv
  2831833443 escalated to Eddy after 5 messages of repeated canned advice;
  conv 3235403912 escalated only after the customer threatened a formal
  complaint and chargeback). Eddy's pattern is the opposite: check first,
  then answer with the specific fact ("I see your email is premium: X" /
  "your payment failed on Aug 20"). The playbook's "What to check first"
  step exists specifically to prevent repeating Jona's mistake.
- RESOLVED: "Restore purchase" / "I already have premium" naming — see Doc
  links above. Also verified in code: premium on a device = `isPremium` on the
  user row OR an unexpired `FreePremium` row (that's the mechanism behind
  goodwill extensions), with a self-healing Stripe re-check when a
  subscriptionId exists — so "reopen the app / re-login" genuinely re-syncs.
- **Open question:** several tickets in this bucket are really about *missing
  filters* (Smile/Hair/Beard/Makeup not appearing) rather than the watermark
  (conv 2952658652, conv 3323529036). Worth checking whether that's a
  separate, more specific bug pattern (e.g. a feature-flag sync issue) once
  there's DB access to look at it directly — for now it's folded into this
  playbook since the fix (log in with correct email, reset) is identical.
- Coupon/discount codes tied to a specific customer's email sometimes fail
  silently for reasons unrelated to premium status (conv 3382073890 —
  discount code with numbers failed, code without numbers worked); this is
  Stripe/promo-code config, not an account-matching bug, but shows up in the
  ticket the same way ("I paid, why don't I have premium").
