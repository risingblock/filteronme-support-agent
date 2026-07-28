---
topic: receipt-invoice
volume: 9 of 1957 (<1%)
status: approved 2026-07-27
---

# Receipts, invoices, and custom quotes

## When this applies

Customer wants a copy of a receipt/invoice, wants their company name/VAT/tax ID
added to one, can't find or access the billing portal, or (rarer) a company
wants an official quotation/pro forma invoice before paying for procurement.

## What to check first

(Phase 3) Stripe: look up the charge/customer by email to confirm they have a
paid subscription and see the receipt/invoice Stripe already generated. Useful
when the customer says the portal shows nothing for them (conv 3034329525 —
account created after paying, wrong email) or a login link expired/never
arrived (conv 3349431340, docs 108).

## Policy

- **Self-serve by default.** Every paid customer's receipts and invoices live
  in the Stripe-hosted billing portal (filteronme.com/billing, or the
  "Billing" button in the app). Portal login is email-based — no password
  (docs 84, docs 108).
- **We don't customize invoices for customers.** No VAT numbers, no company
  letterhead, no reverse-charge notes — not even for EU VAT/reverse-charge
  requests (conv 3163097359) or accountant requests (conv 2938469982). We are
  a US company and have no VAT number to add (conv 2938469982, conv
  3266386366). The fix is always: download the PDF from the portal and edit
  it yourself (Preview, Acrobat, Smallpdf) — docs 120.
- **No custom quotes/pro forma invoices for procurement**, even for annual
  corporate purchases (conv 3005810681). Same answer: pay normally, then edit
  the resulting invoice PDF yourself.
- **No auto-email-on-renewal feature.** A customer asked to be emailed a
  receipt at the moment of every renewal charge (conv 3237702217) — not
  supported today. Point them to the portal's upcoming-billing-date view and
  let them set their own reminder; forward the request as feedback, don't
  promise it'll be built.
- Access-only requests (can't find the portal, no idea where invoices live)
  are just docs 84/108 — no escalation needed.

## How to respond

Access / can't find invoice:

> Hi [name],
>
> You can find all your receipts and invoices in the billing portal:
> filteronme.com/billing — log in with the email your Stripe receipt was sent
> to.
>
> Best

VAT / company details / custom invoice request:

> Hi [name],
>
> We don't have a VAT number to add — we're a US company. You can download
> the invoice from the billing portal and add your own company name or VAT
> number to the PDF with any PDF editor (Preview, Acrobat, Smallpdf all work).
>
> Best

## Escalate instead (tag needs-human) when

- Customer wants a fully custom invoice/quote/pro forma filled in with their
  company details *by us*, especially for corporate procurement (conv
  3005810681) — Eddy's standing answer is no, but confirm before replying if
  the ask is unusual (large order, government/institutional buyer).
- Feature requests around billing (e.g. auto-email on every renewal charge,
  conv 3237702217) — forward as feedback, don't commit to a timeline.
- Portal genuinely inaccessible after trying alternate emails and the billing
  email finder (docs 108) — may need a manual Stripe lookup.

## Doc links to use in replies

- https://help.filteronme.com/article/120-custom-invoices-or-quotes
- https://help.filteronme.com/article/84-how-to-cancel-subscription (billing
  portal access)
- https://help.filteronme.com/article/108-unable-to-get-login-link-to-stripe-billing-portal
- filteronme.com/billing, filteronme.com/billing-email

## Notes from history

- Lowest-volume topic (9 of 1957 conversations, <1%) — keep this playbook
  short, it rarely needs updates.
- Every VAT/custom-invoice reply in the sample used near-identical wording
  from Jona, confirmed by Eddy each time — this is a stable, low-ambiguity
  policy, safe for the agent to draft directly rather than escalate by
  default.
- docs 120 last updated 2026-01-20; docs 84 last updated 2026-01-28 — both
  current as of this writing.
