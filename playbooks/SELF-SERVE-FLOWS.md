# Self-serve flows — the agent's first-choice links (built 2026-07-31/08-01)

RULE (Eddy): never route customers to "contact support" for anything these
flows cover. Link the flow. All are deterministic app code — no human, no
agent involvement. All give identical responses whether or not data matched
(no enumeration oracles), are rate-limited, honeypotted, and audit-logged.

## The flows

| Situation | Link | What happens |
|---|---|---|
| Cancel (can log in) | Billing button in app, or filteronme.com/billing | instant portal cancel |
| Don't know which email | filteronme.com/billing-email (card section) | card last-4 → portal login link emailed to address on file |
| Cancel, locked out of everything | filteronme.com/cancel | statement details → instant reversible cancel_at_period_end; email-on-file gets undo link |
| Lost email access, wants account back | filteronme.com/recover | verify NEW email w/ code → statement details → transfer after veto window |
| Has old email, wants to switch | filteronme.com/change-email | double opt-in code verification, instant |
| Which email has my sub (portal link) | filteronme.com/billing-email (email section) | sends portal link if entered email has a sub |

## Contact-form deep links (for support replies and agent drafts)

- filteronme.com/help/contact?topic=cancel — cancel self-serve ladder (no form!)
- ?topic=login&issue=lost-email — recovery path preselected
- ?topic=login&issue=dont-know-email — card finder path
- ?topic=login&issue=change-email — change-email path
- ?topic=billing&issue=unrecognized-charge — statement-charge explainer
- topics: not-working | installing | billing | cancel | login | presales | other

## Recovery/cancel matching mechanics (for reasoning about edge cases)

- Strong match: card last-4 → exactly ONE Stripe customer + ≥1 corroboration
  (brand/name/amount; contradicting brand disqualifies). Recovery: 48h veto
  window. Cancel-by-card: instant (reversible, notified, undo link).
- Weak match (Apple Pay device numbers): name + exact amount, unique →
  recovery 96h window; cancel-by-card instant-weak.
- Veto click (old email) → transfer blocked + recovery locked for that sub.
- Apple Pay: card.last4 in Stripe is the DEVICE account number — customers
  find it in Wallet → card → ⓘ. Physical-card digits won't match.
- Currency: match compares in the charge's own currency; bank-converted
  amounts won't match — tell customers to leave amount blank if converted.
- All attempts (incl. failures) are rows in filteronme-one's AccountRecovery
  table: status email_pending/email_verified/scheduled/no_match/executed/
  locked, method claims_veto/weak_claims_veto/cancel_by_card_strong|weak.

## past_due handling (fixed 2026-08-01 — the "Laura" bug class)

- App now shows the payment-failed modal immediately (trial-reset no longer
  masks failing renewals with a silent free week).
- Restore-premium flow now says "renewal payment didn't go through — update
  your card at filteronme.com/billing" instead of the FALSE "subscription was
  transferred to <other email>" message (that fallback now fires only when no
  subscription exists at all).
- Agent guidance: past_due + "no subscription found" complaints = send the
  billing portal link to update the card; the sub is intact.
- Decline "your card does not support this type of purchase" = issuer blocks
  recurring charges; advise different card or call bank.
