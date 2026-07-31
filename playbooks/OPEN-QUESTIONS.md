# Playbook decision log — round 1 resolved 2026-07-27

Eddy answered all 13 questions; facts were then verified against the codebase
(Filteronme-one web app + Mac v2.1.7 + Windows V2, per D14). All 16 playbooks
flipped to approved. This file records outcomes, discrepancies found, and
still-open items.

## Resolved (details live in the playbooks)

1. Refunds: default decline-with-policy-link; service extensions/credits are
   the standard remedy for our-side errors; cash refunds rare (D15).
2. Cancellation claims: assert only when read-only Stripe confirms the state.
3. Discounts: never for new customers; goodwill only for long-tenured
   customers wronged by us (human-executed).
4. macOS minimum: current 2.1.x = 13+ (code-verified); old version (docs 124)
   = 12.4+.
5. Trial extensions: only when the blocker was our fault; human-executed.
6. Trial mechanics (code-verified): 7 days from first controls load after
   login; auto-resets 6 weeks after last trial start; no card. Customer-facing
   phrasing stays "a couple months" (conservative, never over-promises).
7. Restore purchase: both UI labels current ("I already have premium" on the
   trial-ended modal, "Restore purchase" in the side panel); same code-to-
   subscription-email flow. Code-verified.
8. Resolution: Mac recent builds output 1080p (upscaled from 720p capture).
   Windows: see discrepancy below.
9. Change-email tool: double opt-in, rate-limited, audit-logged. Code-verified
   — no takeover vector.
10. Hide-my-email account deletion: customer-first — doc-140 payment
    verification proves ownership, then human executes.
11. Auto-collection after cancel: fixed in code since 2025-08-10 (commit
    e7212c0), with edge-case caveats noted in billing-issue.md.
13. TONE.md refund pattern: historical; refund-request.md wins. Confirmed.

## Discrepancies — all reconciled in round 2 (2026-07-27, Eddy + repo recon)

- **Windows resolution**: RECONCILED — code registers a 1080p canvas but
  captures the camera at 720p, so Eddy's "720p" is the correct quality
  answer. FilteronmeWindows-V2 confirmed as the only Windows repo. → tech-issue.md
- **Trial start**: RECONCILED — starts on first login/controls load, which
  for nearly all users IS account creation (signup = login from the app).
  Customer phrasing: "starts when you first log in." → trial.md
- **Trial reset**: Eddy's "a couple months" kept as phrasing; code truth
  (6 weeks) recorded. → trial.md
- **Version map confirmed by repo recon**: current Mac = Filteronme-mac-v2.1
  (v2.1.7, macOS 13+); the OEP-macos* folders are the legacy 2.0.x codebase
  (2.0.15 = the docs-124 old version, macOS 12.4+).
- **Intel Macs**: docs/replies say Apple Silicon required, but the Xcode
  project builds universal (arm64+x86_64). Presumably a performance-based
  policy; customer answer stays "M1+ required." Confirm if ever challenged.

## Still open

- ~~Chargeback economics analysis~~ DONE 2026-07-27: 5% threat
  follow-through, 76% of disputes are from silent never-contacted-support
  customers, declining beats granting ~5–10× on expected cost. Policy stands;
  findings baked into refund-request.md and D15. Report:
  history/analysis/chargeback_report.json.
- **Docs site updates worth making** (support-ticket reducers):
  96/121 (state both macOS minimums + old-version path), 112 (trial starts
  at first launch), 134 (our-fault extension exception), 84/others still
  fine. Plus the Windows-uninstall doc gap (install-setup.md).
- **Filterly website/checkout banner**: confusion accelerating (~26 tickets
  H1 2026; Google AI Overview once conflated the companies). Eddy to decide —
  not an agent matter.
