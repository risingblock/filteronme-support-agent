---
topic: filterly-confusion
volume: 56 of 1957 (3%)
status: draft-for-eddy-review
---

# "Filterly" isn't us

## When this applies

The customer is angry about a charge or subscription for **"Filterly"** (also
seen misspelled: Fiterly, Filtery, Fliterly, Filtertly, Filtermi) — a
different company, not affiliated with FilterOnMe. Tells:

- They name "Filterly" explicitly, or the charge descriptor on their
  statement doesn't match ours (ours reads `WWW.FILTERONME.COM` or
  `Filteronme`; theirs reads `FILTERLY` or similar).
- Charge amounts that don't match our pricing (common Filterly amounts seen:
  $19.99, €19.99, £16.70-£34, CHF19.06, 8052 HUF — recurring weekly or
  biweekly in several complaints, which is not how our billing cycles work).
- No FilterOnMe account findable under their email; they often can't even
  say what app they supposedly used.
- Occasionally the "conversation" isn't a customer email to us at all — it's
  Filterly's own outbound support correspondence (a Gleap-powered helpdesk,
  sender address like `ticket+id...@filterly-*.gleap-mail.com`, or the
  "customer" name literally shows as "Filterly") that ended up in our inbox,
  likely via a customer CC'ing/forwarding both companies. No real question is
  being asked of us in these.

## What to check first

Confirm they have **no** FilterOnMe account or charge before sending the
not-us reply:

- (Phase 3) Stripe/app lookup by email — not built yet.
- Until then: search Help Scout history for the email, and take the
  customer's own description at face value — if they can't produce anything
  that matches our product (app name, statement descriptor, price point),
  that's sufficient. Do not spend time investigating further than that.
- If the complaint is ambiguous (they don't name "Filterly" and just say
  "your charge" or "your app"), ask them to check the statement descriptor
  before assuming — see the verification variant below.
- In the 20+ conversations reviewed for this playbook, none turned out to
  actually be a FilterOnMe customer. Treat that as the base rate, but don't
  skip the check — if a lookup ever does surface a real FilterOnMe charge,
  handle that separately (see Escalate section) rather than sending the
  not-us template.

## Policy

- **Never argue, never investigate further than the check above.** This is
  the single most template-able topic we have — one short reply resolves it
  in one round nearly every time, even against fraud/chargeback/PayPal-dispute
  language.
- The reply states the fact and stops: we are not affiliated with Filterly,
  contact Filterly's support directly. We do not offer to "look into it," we
  do not ask for transaction IDs or card numbers (that's Filterly's job, not
  ours — see the ambiguous-case example in history where a customer without a
  findable Filterly account got stuck in a multi-week back-and-forth with
  *Filterly's own* support asking for exact amounts/dates; that's their
  process to run, not something to replicate here).
- If they come back angry a second time (repeat contact, legal/chargeback
  threats), send the same template again, unchanged. Do not escalate tone,
  do not apologize more, do not add detail. In every reviewed case where the
  customer pushed back once, the same flat template closed it — several
  replied back with a thank-you or apology once they understood.
- If a Filterly-internal email lands in our inbox (see tells above), it's
  safe to send the same template anyway (harmless, and matches Eddy's actual
  practice) — no need to build a special no-reply path for this at current
  volume.

## How to respond

Standard case (the vast majority):

> Hi [name],
>
> Filteronme.com is not affiliated with Filterly. If you're trying to cancel
> Filterly, please contact their support directly.
>
> Best

Verification variant — customer didn't name Filterly, or the complaint is
vague ("your organisation," "your app," no product name):

> Hi [name],
>
> Please check your receipt or card statement — our charges show as
> WWW.FILTERONME.COM or Filteronme. There are other companies with similar
> names that aren't affiliated with us, including Filterly. If the charge
> says Filterly, you'll need to contact their support directly to cancel.
>
> Best

If a lookup ever confirms they DO also have a real FilterOnMe
subscription/charge:

> Hi [name],
>
> I can see the Filterly charge isn't from us — we're not affiliated with
> them, so you'll need to contact their support directly for that one.
>
> I also see you have a FilterOnMe subscription with us. [answer/handle that
> part on its own merits — don't conflate the two in one paragraph]
>
> Best

## Escalate instead (tag needs-human) when

- A lookup shows they actually do have a FilterOnMe charge or account —
  handle the FilterOnMe side as its own ticket/topic; don't let the Filterly
  confusion template paper over a real charge of ours.
- Legal/regulatory language aimed specifically **at us** (not "I'll report
  Filterly," but "I'm reporting FilterOnMe" / naming us in a chargeback or to
  a regulator) — rare, but worth a human look since it implies they believe
  the charge is ours.
- Anything that doesn't fit the pattern at all after the check (e.g., they
  genuinely describe our product/features, not Filterly's).

## Doc links to use in replies

- https://help.filteronme.com/article/122-filterly (last updated 2026-05-07;
  the reply template above already mirrors its wording — consider adding the
  direct link plus the "manage your Filteronme subscription via the Billing
  Portal" line from the doc, since neither is currently included in replies
  and TONE.md favors linking over explaining)

## Notes from history

- Volume has clearly accelerated: ~30 of these in all of 2025 (first one
  seen May 2025 — Filterly seems to be a newer/growing source of confusion)
  vs. ~26 already by late July 2026 — roughly double the pace.
- The reply wording drifted through mid-2025 ("we are FILTERONME not
  FILTERLY" / "Sadly, we're FilterOnMe not Filterly" / a longer version
  explaining the statement-descriptor mismatch) before settling by September
  2025 into the fixed two-sentence template that now matches docs 122
  verbatim. Treat that settled wording as the template; don't reintroduce the
  earlier variants.
- One case (conv history, Jul 2025) needed an Eddy correction because
  Google's AI Overview was telling a customer FilterOnMe and Filterly were
  the same company — worth keeping an eye on whether that recurs, and maybe
  worth Eddy flagging to Google/considering a homepage banner if it keeps
  happening.
- Replies are always sent in English regardless of the customer's language
  (French, Spanish, Hungarian, Dutch all seen in the sample) — consistent
  with current practice, not something this playbook changes.
- Open question for Eddy: is it worth a small banner on filteronme.com and/or
  the docs homepage ("Looking for Filterly? We are not the same company.")
  given the volume trend, rather than relying on every customer finding
  article 122 or writing in first?
