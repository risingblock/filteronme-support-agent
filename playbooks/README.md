# Playbooks — the agent's brain

One markdown file per ticket topic, distilled from 1,957 real conversations
(2023–2026) + the help docs site. The cron loop matches an incoming ticket to a
topic, follows that playbook, and drafts a reply as a private Note. Editing
these files is how the agent learns (see CLAUDE.md).

Precedence when sources conflict:
**playbook Policy section > help docs article > TONE.md > any historical reply.**
Eddy's historical replies are evidence for policy; Jona's/Rajan's are not (D12).

| File | Volume | Automation posture |
|---|---|---|
| tech-issue.md | 17% | draft troubleshooting, one step at a time |
| cancel-subscription.md | 15% | draft self-serve portal reply |
| refund-request.md | 12% | draft decline-with-policy-link; grants are human-only |
| spam-outreach.md | 11% | no reply — tag + close |
| billing-issue.md | 10% | draft; any Stripe action is human-only |
| presales-question.md | 5% | draft from fact table |
| premium-not-working.md | 4% | draft fix sequence; account lookups resolve most |
| how-to-use.md | 4% | draft 1–2 line answer + doc link |
| install-setup.md | 4% | draft per-error fix (OS first!) |
| login-account.md | 4% | draft; account changes are human-only |
| filterly-confusion.md | 3% | draft the not-affiliated template |
| trial.md | 2% | draft; extensions always escalate |
| feature-request.md | 2% | draft honest-roadmap reply + log for Eddy |
| subscription-change.md | 2% | draft self-serve path; transfers escalate |
| business-partnership.md | 1% | draft qualifying questions; ALWAYS needs-human |
| receipt-invoice.md | <1% | draft self-serve receipt path |

Unmatched/unclear tickets: tag `needs-human`, stop. Escalation is success (D11).

All playbooks are `status: draft-for-eddy-review` until Eddy approves them —
see OPEN-QUESTIONS.md for the policy decisions each draft is waiting on.
Conversation ids cited as (conv NNN) refer to Help Scout conversations; find
the local copy with `grep -rl "id: NNN" history/md/`.
