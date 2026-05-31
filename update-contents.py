#!/usr/bin/env python3
"""Update the `contents` front matter field for blog posts.

The value is generated from Markdown headings in the post body. Headings inside
fenced code blocks are ignored. By default all files in `_posts/*.md` are
updated in place.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

POSTS = Path("_posts")
HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
CONTENTS_RE = re.compile(r"(?m)^contents:\s*.*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def split_front_matter(text: str) -> tuple[str, str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing front matter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("unterminated front matter")
    # Include the first delimiter in `start` and the second delimiter in `end`.
    start = text[:4]
    front = text[4:end]
    body = text[end:]
    return start, front, body


def clean_heading(text: str) -> str:
    text = re.sub(r"\s+#+\s*$", "", text).strip()
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*]+", "", text)
    return text.strip()


def extract_contents(body: str) -> list[str]:
    contents: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            heading = clean_heading(match.group(2))
            if heading:
                contents.append(heading)
    return contents


def update_post(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    start, front, body = split_front_matter(original)
    contents = extract_contents(body)
    contents_line = "contents: " + json.dumps(contents, ensure_ascii=False)
    if CONTENTS_RE.search(front):
        front = CONTENTS_RE.sub(contents_line, front, count=1)
    else:
        front = front.rstrip("\n") + "\n" + contents_line + "\n"
    updated = start + front + body
    if updated != original:
        path.write_text(updated, encoding="utf-8", newline="")
        return True
    return False


def iter_posts(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(p) for p in paths]
    return sorted(POSTS.glob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Update contents arrays from Markdown headings.")
    parser.add_argument("paths", nargs="*", help="posts to update; defaults to _posts/*.md")
    parser.add_argument("--check", action="store_true", help="fail if any post would change")
    args = parser.parse_args()

    changed: list[Path] = []
    for path in iter_posts(args.paths):
        before = path.read_text(encoding="utf-8")
        try:
            did_change = update_post(path)
        except ValueError as exc:
            print(f"{path}: {exc}", file=sys.stderr)
            return 1
        if did_change:
            changed.append(path)
            if args.check:
                path.write_text(before, encoding="utf-8", newline="")

    for path in changed:
        print(path)

    if args.check and changed:
        print(f"{len(changed)} post(s) need contents updates", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
