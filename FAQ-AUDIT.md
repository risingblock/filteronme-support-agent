# FAQ content audit — help.filteronme.com → in-house (2026-07-29)

Data: citations = times the article was linked in 4 years of sent replies
(813 total); pb = references from approved playbooks (the agent's reading
list). Full table generated from history/; verdicts below are for Eddy's
approval. URL RULE for migration: every existing /article/<id>-<slug> URL
gets a 301 to its new home — 813 links live in old emails, playbooks, Google.

## Priority 1 — REWRITE (the workhorses; correct facts, Eddy's voice)

| id | article | cites | why rewrite |
|---|---|---|---|
| 80 | refund policy | 384 | carries half of all citations; align with D15 wording; add service-extension/goodwill language |
| 123 | full reinstall (Mac) | 60 | keep step-per-line, add 2.1.x specifics |
| 99 | install Mac | 55 | macOS 13+ requirement + old-version path (docs 124) |
| 84 | cancel subscription | 50 | lead with in-app Billing button (auto-login); portal second |
| 81 | OBS/Streamlabs | 45 | current admin-mode fix, Mac-can-close-app note |
| 105 | fix most problems | 36 | mirror the playbook fix ladder, cheapest step first |
| 106 | Windows installer problem | 31 | oldest workhorse (Nov 2024); reorder per Eddy's actual sequence |
| 98 | install Windows | 31 | current + link the 3 required libraries |

## Priority 2 — FIX KNOWN ERRORS (from the codebase-verification pass)

| id | fix |
|---|---|
| 96 + 121 | resolve macOS contradiction: current = 13+, old version (124) = 12.4+; state the split in both |
| 112 | add: trial starts at first login; no card; auto-expires |
| 134 | align with ruling: extensions only for our-fault blockers |
| 108 | rewrite: the page SENDS a login link to a correctly-guessed email (it does not reveal the email); add try-each-email guidance |
| 122 | Filterly: add statement-descriptor line (charges show WWW.FILTERONME.COM) |
| 94 | 4K/resolution: add Mac-1080p-on-recent-builds / Windows-720p truth |

## MERGE

- 90 (logout) → 109 (sign out): duplicates. 301 90 → 109.
- 83 (premium not working, 2024) → 136 (restore purchase, May 2026): same
  subject, 136 is current; port 83's fix-sequence content in. 301 83 → 136.
- 93 (uninstall Mac) → new combined **Uninstall (Mac & Windows)** article
  (Windows uninstall is a known doc gap). 301 93 → new.

## KILL

- 104 (contact us) → becomes site chrome (footer/contact block on every
  /help page), not an article. 301 → /help.
- 125 (upgrading to 2.1.5) — already dead in sitemap but cited 16× in old
  emails: 301 → 124 (old versions).

## ADD (ticket-data-driven, in priority order)

1. **"What is this FILTERONME.COM charge on my statement?"** — aimed at the
   78 silent disputers + Filterly confusion; covers descriptor, how to check
   which email you used, cancel/billing links. Highest expected ROI.
2. **Uninstall FilterOnMe (Mac & Windows)** — real gap, replaces 93.
3. **Using FilterOnMe on multiple devices** — the most copy-pasted policy
   answer in history (one login at a time; simultaneous needs two subs).
4. **Which apps does it work with?** — compatibility list + "test with the
   free trial" guidance (top presales question).

## KEEP (current, accurate, or too new to judge)

82, 85, 88, 89, 91, 95, 97, 107, 110, 111, 113, 115, 116, 118, 120, 124,
126, 127, 128, 130, 132, 135, 137, 139, 140, 141 — light copy pass only,
show last-updated, add related-links + feedback vote like everything else.

## Every article gets

- 301 from the old URL; last-updated stamp; related articles; "Did this
  solve it?" vote (PostHog) with a no → prefilled email-support handoff.
- Category + task-card placement per the /help UX (see PORTAL-SPEC).
