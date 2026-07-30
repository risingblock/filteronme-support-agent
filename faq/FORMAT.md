# FAQ article format (source of truth for the /help build)

One markdown file per article in this directory, named `<slug>.md`.
Screenshots live in history/docs/images/ during authoring and get copied to
filteronme-one/public/help/images/ at build time — reference them as
`images/<original-article-slug>/<n>.<ext>` exactly as the exported articles do.

## Frontmatter

```yaml
---
id: 84                # legacy Help Scout article id; null for new articles
slug: how-to-cancel-subscription   # KEEP the legacy slug for old articles (301s depend on it)
legacy_url: https://help.filteronme.com/article/84-how-to-cancel-subscription  # null for new
title: How to cancel your subscription
category: billing-account | account-login | install-setup | troubleshooting | using-with-apps | presales
verdict: rewrite | fix | keep | merged | new
related: [slug-a, slug-b]          # 2-3 related article slugs
---
```

## Body rules

- Eddy's voice per playbooks/TONE.md: short sentences, zero filler, link over
  lecture, honest about limitations. Sentence-case headings.
- Lead with the answer or the first action — never background.
- Facts MUST match the approved playbooks (they outrank the old article text
  when they conflict — the playbooks were code-verified). Cite nothing; just
  be right.
- Keep every still-relevant screenshot marker from the old article. Drop
  markers only if the step is gone; note dropped/starving-for-screenshot spots
  with `<!-- TODO screenshot: <what to capture> -->` so Eddy can shoot them.
- Self-serve actions get direct links: https://filteronme.com/billing,
  filteronme.com/billing-email (describe it truthfully: it SENDS a login link
  to the address you enter if that address has a subscription),
  filteronme.com/downloads.
- End every article that could dead-end with: "Still stuck? Email
  support@filteronme.com" (one line, no header).
- Merged articles: the surviving file absorbs the content; note the absorbed
  legacy id in frontmatter as `absorbs: [90]` so redirects get generated.
