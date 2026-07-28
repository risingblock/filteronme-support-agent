---
topic: presales-question
volume: 102 of 1957 (5%)
status: approved 2026-07-27 (facts code-verified against app v2.1.7 + web)
---

# Pre-sales questions: compatibility, requirements, pricing, trial

## When this applies

Anyone who hasn't bought yet (or is still on free/trial) asking whether
FilterOnMe will work for their setup, what it costs, what free vs. premium
gets them, or how the trial/account/payment mechanics work. Typical shapes:
"does it work with [app]?", "what are the system requirements?", "is there a
mobile app?", "do you need a credit card for the trial?", "is there a
lifetime/one-time option?", "can I get a discount?".

Not this playbook: existing paying customers troubleshooting a broken
install (→ troubleshooting playbooks), refund/cancel requests (→
billing/cancellation playbook), bulk seat / reseller / enterprise pricing
asks (→ business-partnership playbook, see Escalate below).

## What to check first

Mostly nothing external — this is answered from the fact table below, not a
live lookup. The two things that DO depend on their setup:

- **OS** — Mac vs. Windows changes which requirements/version links apply.
- **The specific third-party app/camera they're asking about** — if it's not
  on the known-compatible or known-exception list below, don't guess: per
  Eddy (conv 2985236562, conv 3035340878, both from July/Aug 2025 onward),
  the standing answer for an unlisted app is "try the free trial and see" —
  not a yes/no guess.

## Policy

**Platforms**
- Desktop only: **Mac and Windows**. No mobile app (iOS/Android), no
  ChromeOS, no Linux (conv 2324657266, conv 2689208824, conv 3268254770,
  docs 85). This has been stable across the entire history sample, 2023–2026.
- Mac: current version requires **macOS 13+**; an older downloadable version
  supports macOS 12.4+ (docs 124) — Eddy, 2026-07-27, resolving the docs
  96 vs 121 conflict. Requires Apple Silicon (M1+) — Intel Macs are not
  supported and there's no Rosetta workaround (conv 2782543924, docs 96).
- Windows: min **8GB RAM**, **~3.8GHz i3 or better**; tested working on a
  budget machine (Acer Aspire 3 A314-36P-35UU) (docs 96, last updated
  2025-07-23).
- New macOS versions: Eddy has confirmed compatibility case-by-case as they
  ship (e.g., macOS Tahoe confirmed working, conv 3285870299, Apr 2026) —
  point to the full-reinstall guide (docs 123) rather than promising in the
  abstract.

**App/hardware compatibility**
- Confirmed working: Zoom, Google Meet, Teams, OBS/Streamlabs, Discord,
  WhatsApp, Livestorm, Jitsi (conv 2503773482, conv 2828042237, docs 81,
  docs 88). For OBS on Mac (latest version), FilterOnMe can be closed after
  setup to save resources; on Windows keep it open (docs 81).
- **The filter is invisible to other participants** — they only see your
  camera feed, not the FilterOnMe app window (conv 2828042237).
- Known exception / needs a workaround: **DroidCam** (phone-as-webcam) —
  open FilterOnMe *before* DroidCam, or it's treated as incompatible (conv
  2941005538). This is the one specific workaround Eddy has given for a
  virtual-camera-type source; it's not guaranteed to generalize.
- Unverified / open question: whether FilterOnMe reliably picks up *other*
  virtual-camera sources as input (e.g., DSLR-as-webcam software) — one
  customer's ticket (conv 2875366915) went unanswered in our history.
  Default to "try opening FilterOnMe first" per the DroidCam pattern, but
  don't promise it'll work.
- Anything else not listed (Ecamm Live, iMLive, Logitech Capture, Clipchamp,
  photo booth software, capture cards, etc.) → **tell them to test with the
  free trial**, per Eddy's standing guidance from mid-2025 on (conv
  2985236562, conv 3035340878, conv 3123037191). Older tickets (2024 and
  earlier) show Eddy/Jona giving direct yes/no guesses for unlisted apps
  (e.g., "yes it should work with Livestorm") — treat that as superseded;
  current policy is "test the trial," not guess.

**Resolution**
- Max output is capped; **no user-facing setting to change it** (conv
  2963417881).
- **4K is not supported** — auto-downscaled, deliberately, because it's too
  resource-intensive and most call apps (Zoom etc.) recompress video anyway
  so the visible quality gain is minimal (conv 2916335464, docs 94, last
  updated 2025-06-01).
- **1080p**: this changed. Through 2024 (conv 2792967404, Dec 2024) Mac was
  capped at 720p due to performance/lag from the filter pipeline. A newer
  Mac version released in 2026 **fully supports 1080p** (conv 3244632632,
  Mar 2026 — "This new version fully supports 1080p," pointing to the
  full-reinstall guide, docs 123). Treat 1080p-on-Mac as current truth;
  the 720p-cap replies are stale. Doc 94 (4K doc) doesn't call out the
  1080p fix explicitly, so lean on the conv 3244632632 answer over the doc
  wording alone.

**Free vs. premium**
- The **only** difference is the **watermark** — premium removes it (conv
  2840643115, docs 116). Video quality/color processing is identical on
  both (conv 2816509974 — a customer thought paid would look better; Eddy:
  "colors will be the same on both the trial and paid version").

**Trial / account**
- **7-day free trial, no credit card required**, auto-cancels/expires on
  its own — nothing to cancel if you never upgraded (docs 112, docs 80).
- **No separate account creation**: enter an email, a login code is sent,
  account is created automatically (or logs you into an existing one with
  that email) (docs 91).

**Pricing / billing model**
- **Monthly or yearly subscription only** — no lifetime/one-time-purchase
  option, repeatedly declined (conv 2373279059, conv 2863699835, conv
  2996001161).
- **No discounts** — not for students, low-income, "too expensive," or
  bulk/negotiated asks; this has been consistent since at least early 2025
  and matches TONE.md's "never haggle" rule (conv 2842890717, conv 3116101265,
  conv 3137065882, conv 3245034528, conv 3370979805). Always point to
  filteronme.com/pricing instead of engaging on price.
- **Multi-device**: one active login at a time. You can switch between
  devices freely (not simultaneously) on one subscription; using two devices
  *at the same time* requires two subscriptions (conv 2676353286, conv
  2903948785, conv 2921577752, conv 3216602724, conv 3390413588 — this
  answer is unusually consistent, near-verbatim, across 5+ tickets spanning
  2024–2026).
- **Payment methods**: no PayPal; accepts major cards and wallets (Apple
  Pay, Google Pay, Amazon Pay, Stripe Link) via Stripe (conv 3118611313,
  docs 118). SEPA direct debit shows on the upgrade page only for users
  geolocated in **Austria or Germany** (VPN off) — code-verified 2026-07-27
  (conv 3170098392). Note: the exact wallet list is configured in the Stripe
  dashboard, not code — "Stripe offers several payment methods at checkout"
  is the safe phrasing.
- **Privacy**: FilterOnMe cannot see/access the camera feed itself, per Eddy
  (conv 3365635761) — point privacy-conscious askers to
  filteronme.com/privacy rather than drafting a custom assurance letter.

### Open questions (can't verify from history — ask Eddy / escalate)
- RESOLVED (Eddy, 2026-07-27): the 1080p fix is Mac-only; **Windows is 720p**.
- Whether virtual-camera sources in general (beyond DroidCam) are
  supported — conv 2875366915 has no reply on record.

## How to respond

Platform question:
> Hi,
>
> We are only on Mac + Windows at the moment!
>
> Best

Unlisted app/compatibility question:
> Hi [name],
>
> Best way to know for sure is to try our free trial with that setup — no
> card required. Let me know if it doesn't work and we'll take a look.
>
> Best

Discount ask:
> Hi [name],
>
> Sorry — we don't offer discounts, the yearly plan is already discounted
> vs. monthly. Pricing's here: filteronme.com/pricing. Happy to have you try
> the free trial first if you haven't.
>
> Best

## Escalate instead (tag needs-human) when

- Bulk/team/enterprise seat pricing, reseller asks, or anything that isn't
  a single consumer subscription → business-partnership playbook.
- A compatibility question about an app/OS version genuinely not covered
  by the fact table above and not something "try the trial" resolves (e.g.,
  they've already tried the trial and it doesn't work) → normal
  troubleshooting escalation, not this playbook.
- Payment-method dead ends beyond the documented options (no card, no
  PayPal, non-Germany SEPA-style requests) — check docs 118/128 first, but
  if none apply, escalate rather than improvise a workaround.
- Anything asking us to promise a roadmap feature (mobile app, 4K, lifetime
  plan) as "coming soon" — never commit to a timeline per TONE.md; if
  pressed, escalate rather than speculate.

## Doc links to use in replies

- https://help.filteronme.com/article/85-do-you-have-a-mobile-app
- https://help.filteronme.com/article/91-do-i-need-to-create-an-account
- https://help.filteronme.com/article/94-do-you-offer-4k-or-higher-quality-resolution
- https://help.filteronme.com/article/96-minimum-computer-requirements-to-run-filteronme
- https://help.filteronme.com/article/112-how-to-cancel-trial
- https://help.filteronme.com/article/116-how-to-remove-watermark-by-upgrading
- https://help.filteronme.com/article/118-do-you-accept-paypal
- https://help.filteronme.com/article/123-how-to-do-a-full-reinstall-of-filteronme-for-mac
- https://help.filteronme.com/article/81-how-to-use-with-obs-or-streamlabs
- https://help.filteronme.com/article/88-how-to-use-with-discord
- https://help.filteronme.com/article/80-what-is-your-refund-policy
- filteronme.com/pricing, filteronme.com/privacy

## Notes from history

- **Policy shift mid-2025**: before ~July 2025, Eddy/Jona answered
  unlisted-app compatibility questions with direct guesses ("yes it should
  work with Livestorm"). From conv 2985236562 (Jul 2025) on, Eddy explicitly
  told Jona to stop guessing and default to "test with the free trial" —
  this is a real policy change, not just Jona inconsistency. The agent
  should follow the newer rule.
- **Resolution cap changed over time**: 720p-on-Mac (2024) → 1080p-on-Mac
  supported after a 2026 Mac release (conv 3244632632). If new
  presales-question tickets about resolution keep citing 720p, that's stale
  — verify against the app's current changelog before answering.
- **Jona divergence worth flagging**: conv 3216602724 (Feb 2026) — a
  customer asked about using the app on "iPhone and my laptop." Jona
  answered with the standard multi-device/simultaneous-use script without
  ever correcting that there is no iPhone/iOS app at all. The customer's
  own follow-up suggests they meant two non-iPhone devices, so this may not
  have caused real harm, but the agent should always lead with "desktop
  only, no mobile app" when a mobile OS is named, before addressing
  multi-device mechanics.
- Multi-device answer is the single most copy-paste-consistent policy in
  the whole sample (near-identical wording across 2024–2026 tickets) — safe
  for the agent to draft directly.
- Discount refusal is fully stable and matches TONE.md's "never haggle"
  rule; several 2025–2026 tickets show customers pushing back after the
  refusal — the correct move is a brief second "no," not re-engaging on
  price.
- doc 94 (4K) last updated 2025-06-01, doc 96 (requirements) last updated
  2025-07-23, doc 85 (mobile) and doc 91 (account) last updated 2024-07-26
  (older but content still matches every 2026 reply sampled — no
  contradiction found).
