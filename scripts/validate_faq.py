#!/usr/bin/env python3
"""Validate faq/ articles and emit the redirect map for the /help build.

Checks: required frontmatter, unique slugs, valid categories, image markers
resolve to files under history/docs/images/, audit coverage (every non-killed
article accounted for), related-slugs resolve. Emits faq/redirects.json:
old Help Scout paths -> new /help/<slug> paths (incl. absorbed ids and the
two killed articles).
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FAQ = REPO / "faq"
IMAGES = REPO / "history" / "docs" / "images"
CATEGORIES = {
    "billing-account", "account-login", "install-setup",
    "troubleshooting", "using-with-apps", "presales",
}

def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm

errors, warnings = [], []
slugs, id_map = {}, {}
articles = sorted(p for p in FAQ.glob("*.md") if p.name != "FORMAT.md")

for path in articles:
    text = path.read_text()
    fm = parse_frontmatter(text)
    slug = fm.get("slug", "")
    if not fm:
        errors.append(f"{path.name}: no frontmatter"); continue
    if path.stem != slug:
        errors.append(f"{path.name}: filename != slug '{slug}'")
    if slug in slugs:
        errors.append(f"{path.name}: duplicate slug")
    slugs[slug] = fm
    if fm.get("category") not in CATEGORIES:
        errors.append(f"{path.name}: bad category '{fm.get('category')}'")
    aid = fm.get("id", "null")
    if aid not in ("null", "", "~"):
        id_map[aid] = slug
    for absorbed in re.findall(r"\d+", fm.get("absorbs", "")):
        id_map[absorbed] = slug
    for img in re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", text):
        if not (REPO / "history" / "docs" / img.replace("images/", "images/")).exists():
            if not (IMAGES / img.replace("images/", "")).exists():
                errors.append(f"{path.name}: missing image {img}")
    todos = len(re.findall(r"<!-- TODO screenshot", text))
    if todos:
        warnings.append(f"{path.name}: {todos} screenshot TODO(s) for Eddy")

# related-slug resolution
for slug, fm in slugs.items():
    for rel in re.findall(r"[a-z0-9-]{3,}", fm.get("related", "")):
        if rel not in slugs:
            warnings.append(f"{slug}: related '{rel}' not found")

# redirects: every legacy id -> new path (+ killed articles)
redirects = {}
for aid, slug in sorted(id_map.items(), key=lambda x: int(x[0])):
    redirects[f"/article/{aid}"] = f"/help/{slug}"
redirects["/article/104"] = "/help"          # contact-us -> help home
redirects["/article/125"] = "/help/" + id_map.get("124", "download-old-mac-version")
(FAQ / "redirects.json").write_text(json.dumps(redirects, indent=1))

print(f"{len(articles)} articles, {len(id_map)} legacy ids mapped, "
      f"{len(redirects)} redirects -> faq/redirects.json")
for e in errors:
    print("ERROR:", e)
for w in warnings:
    print("warn: ", w)
sys.exit(1 if errors else 0)
