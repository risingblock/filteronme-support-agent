# References & API Notes

## Help Scout Inbox API 2.0
Docs: https://developer.helpscout.com/mailbox-api/

- Base: `https://api.helpscout.net/v2`, JSON, HTTPS-only.
- Auth: OAuth2 **client credentials** — create app under Profile → My Apps, then
  `POST /v2/oauth2/token` with `grant_type=client_credentials` → bearer token.
- Export: `GET /v2/conversations?status=all&embed=threads` per mailbox
  (`GET /v2/mailboxes` to enumerate), HAL-style pagination via `page` /
  `_embedded.conversations`. Handle 429 with backoff.
- Live customer history at runtime: conversations list supports querying/filtering
  (search by customer email) — use this instead of the export.
- Suggested replies: **Create Note** endpoint on a conversation is confirmed
  supported. Whether the reply endpoint takes a `draft` flag: unverified — test.
- Webhooks: full CRUD support exists (not needed until latency matters).
- Community export references: guenard/helpscout-exporter (deprecated but shows the
  shape), gist fpcorso/702b80f162b2984fbd87a273af1a6f85 (CSV downloader).

## Gumclaw (the reference implementation)
- How it works (its own writeup): https://gumclaw.github.io/how-i-work/index.html
- Published playbook corpus: https://github.com/antiwork/skills — "273 skills,
  78 cron loops"; the single best template for our Phase 1 playbooks.
- GitHub org: https://github.com/gumclaw (forks of openclaw, hermes-agent;
  gumroad; codex-gumclaw-controlplane).
- Loop: cron/mention → read policy+memory → verify against live sources → do work
  → report to human. Grounded-claims-only; approval for sensitive actions.
- Runs on dedicated always-on hardware (MacBook Pro M3 Max); operator @shl.

## Hermes agent (candidate runtime)
- Install docs: https://hermes-agent.nousresearch.com/docs/getting-started/installation
  — macOS/Linux/WSL2/Windows/Android; one-line install; brings own Python 3.11 +
  Node 22; only Git required. Headless VPS: unprivileged service-user install,
  `--skip-browser`.
- Providers: https://hermes-agent.nousresearch.com/docs/integrations/providers
  - Anthropic OAuth: Claude **Max + purchased extra usage credits only**; consumes
    overage credits, not base allowance. Pro unsupported. Known credential bugs:
    issues #12905, #40014, #15080, #48320, #25267 on NousResearch/hermes-agent.
  - OpenAI Codex OAuth device flow: works incl. **ChatGPT Plus $20** (weekly cap;
    rotating refresh tokens). Guide: https://openclawlaunch.com/guides/hermes-chatgpt-subscription
  - Plain API keys: `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`. Recommended for
    production/unattended.
  - Nous Portal: their unified subscription (300+ models).

## Model pricing/benchmarks consulted (July 2026)
- GPT-5.4 vs 5.4-mini: https://benchlm.ai/compare/gpt-5-4-vs-gpt-5-4-mini —
  mini ≈ 1/3 price ($0.75/$4.50 vs $2.50/$15 per M tokens), much faster, but
  largest quality gap is agentic tool-use (65.6 vs 77). Hence D9 tiering.
- Pricing table: https://www.hikari-dev.com/en/blog/2026/04/18/gpt-54-pricing-comparison/

## Other systems to wire in (Phase 3)
- Stripe: restricted API key (read-only, scoped: charges/customers/subscriptions).
- Shopify: Admin API custom app token, read-only scopes (orders, customers).
- Our app: needs a read-only lookup endpoint or read-replica access (to be designed).
