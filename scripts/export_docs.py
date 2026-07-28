#!/usr/bin/env python3
"""Export the public help docs site (help.filteronme.com) to markdown.

Fetches sitemap.xml, pulls every /article/ page, and writes one markdown file
per article with frontmatter (url, title, last_updated). Derived data —
regenerate anytime; the site is the source of truth.

Note: articles may be stale (check last_updated). Playbooks should link to
articles but state policy themselves.

Usage:
    python3 scripts/export_docs.py

Output: history/docs/<slug>.md

Stdlib only.
"""

import json
import re
import sys
import time
import urllib.request
from html import unescape
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "history" / "docs"
SITE = "https://help.filteronme.com"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from render_md_views import html_to_text  # noqa: E402


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "filteronme-docs-export"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", errors="replace")


def article_urls() -> list[str]:
    xml = fetch(f"{SITE}/sitemap.xml")
    return sorted(set(re.findall(rf"{SITE}/article/[^<]+", xml)))


def extract(html: str) -> tuple[str, str, str]:
    """Return (title, last_updated, body_text) from an article page."""
    title = ""
    m = re.search(r"<title>([^<]*)</title>", html)
    if m:
        title = unescape(m.group(1)).replace(" - Filteronme Support Center", "").strip()

    updated = ""
    m = re.search(r"Last updated on ([^<]+)", html)
    if m:
        updated = m.group(1).strip()

    # article body lives in the #fullArticle container; fall back to whole page
    m = re.search(
        r'<div[^>]+id="fullArticle"[^>]*>(.*?)<div[^>]+class="articleRatings',
        html,
        re.DOTALL,
    )
    body_html = m.group(1) if m else html
    return title, updated, html_to_text(body_html)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    urls = article_urls()
    print(f"{len(urls)} articles in sitemap")
    for url in urls:
        slug = url.rsplit("/", 1)[-1]
        title, updated, body = extract(fetch(url))
        content = "\n".join(
            [
                "---",
                f"url: {url}",
                f"title: {json.dumps(title, ensure_ascii=False)}",
                f"last_updated: {json.dumps(updated)}",
                "---",
                "",
                f"# {title}",
                "",
                body,
                "",
            ]
        )
        (OUT_DIR / f"{slug}.md").write_text(content)
        print(f"  {slug} (updated {updated or '?'})")
        time.sleep(0.3)  # be polite to the docs host
    print(f"Done -> {OUT_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
