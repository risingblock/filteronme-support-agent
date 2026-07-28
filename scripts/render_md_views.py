#!/usr/bin/env python3
"""Render history/raw/conversations.jsonl into per-conversation markdown views.

Derived, disposable output (Phase 0 of PLAN.md) — regenerate anytime from the
JSONL, never edit these by hand. One file per conversation with YAML
frontmatter (id, date, customer_email, tags, topic, status) for ripgrep and
human reading.

Usage:
    python3 scripts/render_md_views.py

Input:  history/raw/conversations.jsonl
Output: history/md/YYYY/conv-<id>-<slug>.md

Stdlib only.
"""

import json
import re
import shutil
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
IN_PATH = REPO_ROOT / "history" / "raw" / "conversations.jsonl"
OUT_DIR = REPO_ROOT / "history" / "md"
TOPICS_PATH = REPO_ROOT / "history" / "topics.json"  # {"<conv id>": "<topic>"}

# thread types worth reading; lineitems are status-change noise
THREAD_TYPES = {"customer", "message", "note", "chat", "phone", "forwardparent"}

BLOCK_TAGS = {"p", "div", "br", "li", "tr", "blockquote", "h1", "h2", "h3", "h4"}


class HTMLToText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip_depth += 1
        elif tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip_depth:
            self._skip_depth -= 1
        elif tag in BLOCK_TAGS and tag != "br":
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip_depth:
            self.parts.append(data)


def html_to_text(html: str) -> str:
    parser = HTMLToText()
    parser.feed(unescape(html))
    text = "".join(parser.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def slugify(text: str, max_len: int = 50) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:max_len].rstrip("-") or "no-subject"


def yaml_str(value) -> str:
    """JSON-encode scalars/lists: valid YAML, safe against quotes/colons."""
    return json.dumps(value, ensure_ascii=False)


def author_of(thread: dict) -> str:
    who = thread.get("createdBy") or {}
    name = " ".join(filter(None, [who.get("first"), who.get("last")])).strip()
    email = who.get("email") or ""
    label = name or email or "unknown"
    return f"{label} ({who.get('type', '?')})"


def render(conv: dict, topics: dict) -> tuple[Path, str]:
    conv_id = conv["id"]
    created = conv.get("createdAt", "")
    year = created[:4] or "unknown"
    subject = conv.get("subject") or "(no subject)"
    customer = (conv.get("primaryCustomer") or {}).get("email", "")
    tags = [t.get("tag", "") for t in conv.get("tags", [])]
    status = conv.get("status", "")

    lines = [
        "---",
        f"id: {conv_id}",
        f"date: {yaml_str(created)}",
        f"customer_email: {yaml_str(customer)}",
        f"tags: {yaml_str(tags)}",
        f"topic: {topics.get(str(conv_id), '')}",
        f"status: {yaml_str(status)}",
        "---",
        "",
        f"# {subject}",
        "",
    ]

    threads = (conv.get("_embedded") or {}).get("threads") or []
    threads = [t for t in threads if t.get("type") in THREAD_TYPES]
    threads.sort(key=lambda t: t.get("createdAt", ""))

    for thread in threads:
        kind = thread.get("type", "?")
        heading = {"customer": "Customer", "message": "Reply", "note": "Note"}.get(
            kind, kind.capitalize()
        )
        lines.append(f"## {heading} — {author_of(thread)} — {thread.get('createdAt', '')}")
        lines.append("")
        body = thread.get("body") or ""
        lines.append(html_to_text(body) if body else "(empty)")
        lines.append("")

    rel = Path(year) / f"conv-{conv_id}-{slugify(subject)}.md"
    return rel, "\n".join(lines)


def main():
    if not IN_PATH.exists():
        sys.exit(f"{IN_PATH} not found — run scripts/export_helpscout.py first.")

    # derived output: rebuild from scratch so deleted conversations don't linger
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)

    topics = {}
    if TOPICS_PATH.exists():
        topics = json.loads(TOPICS_PATH.read_text())
        print(f"Loaded {len(topics)} topic assignments")

    count = 0
    for line in IN_PATH.open():
        line = line.strip()
        if not line:
            continue
        rel, content = render(json.loads(line), topics)
        out_path = OUT_DIR / rel
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)
        count += 1

    print(f"Rendered {count} conversations -> {OUT_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
