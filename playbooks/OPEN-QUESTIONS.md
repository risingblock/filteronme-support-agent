# Open questions for Eddy — answer these to finalize the playbooks

Compiled from all 16 drafts (2026-07-27). Each playbook's "Notes from history"
has the full context. Answer inline, then we update the playbooks and flip
their status from draft to approved.

## Money (highest priority — these gate the biggest topics)

1. **Refunds** (refund-request.md): current practice is effectively zero cash
   refunds. Confirm the agent should default to decline-with-policy-link, and:
   - Is the non-cash "service extension" goodwill fix (conv 3227032537) a
     standard alternative for support-caused errors, or a one-off?
   - Chargeback/legal-demand tickets: draft-and-close automatically (your
     "close this" shorthand), or always human-first-look?
   - Fraud/unauthorized-charge claims: still "verify, cancel, no refund"?
2. **Cancellations** (cancel-subscription.md): may the agent's draft ever say
   "your subscription has been cancelled," or only after a human confirms in
   Stripe? (Recommended: never assert until confirmed.)
3. **Discounts**: zero exceptions, ever? (Playbooks currently say never.)

## Policy contradictions found in your docs

4. Minimum macOS: article 96 says macOS 12.4+, article 121 says macOS 13+.
   Which is right? (tech-issue.md, presales-question.md)
5. Trial extensions: article 134 says never, but you've granted them for
   verifiable blockers. Drafts route all extension requests to needs-human —
   OK, or is there a rule the agent can apply? (trial.md)
6. Trial reset window: "every few months" vs "a couple months" vs "a month or
   so" — pick one. And does the trial start at account creation or first app
   launch? (trial.md)
7. "Restore purchase" button (article 136, May 2026) vs the "I already have
   Premium" flow every reply still uses — which is current UI? (premium-not-working.md)
8. Is 1080p supported on Windows too, or only recent Mac builds? (tech-issue.md,
   presales-question.md)

## Process decisions

9. The self-serve change-email tool: does it verify old-email ownership? If
   not, that's an account-takeover vector worth knowing about. (subscription-change.md)
10. Deleting accounts behind hide-my-email relay addresses when the requester
    can't be reached at the real address — what's the rule? (login-account.md)
11. Post-Aug-2025 fix that stops auto-collection after cancel: universal now,
    or do old accounts still hit the "charged after cancel" bug? (billing-issue.md)
12. Filterly confusion is accelerating (~26 tickets in H1 2026; Google's AI
    Overview once conflated the two companies). Worth a website/checkout
    banner? Not an agent question, but the data says yes. (filterly-confusion.md)

## Tone

13. TONE.md's old "offer a refund when troubleshooting fails" pattern has been
    marked historical and refund-request.md now wins. Confirm.
