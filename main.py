#!/usr/bin/env python3
"""One-Liner Laughs — entry program.

Writes a single funny line (at most 200 characters) to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set) and prints it to stdout.

Standard library only. Fully deterministic: the same bytes every run.
"""

import hashlib
import os
import sys

JOKE = 'I asked AI to write my wedding vows; it said, "I do \u2014 as an AI language model."'

MAX_CHARS = 200


def entry_text() -> str:
    """Return the one-line joke, validated against the gate."""
    text = JOKE
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} chars, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text:
        raise ValueError("entry must be a single line")
    return text


def write_entry(out_dir: str) -> str:
    """Write entry.txt into out_dir; return its sha256 hex digest."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    text = entry_text()
    data = text.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    return hashlib.sha256(data).hexdigest()


def main(argv) -> int:
    if "--check" in argv:
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "rb") as f:
            data = f.read()
        digest = hashlib.sha256(data).hexdigest()
        expected = hashlib.sha256(entry_text().encode("utf-8")).hexdigest()
        text = data.decode("utf-8")
        ok = (
            digest == expected
            and 1 <= len(text) <= MAX_CHARS
            and bool(text.strip())
            and "\n" not in text
        )
        print(f"entry.txt: {len(text)} chars, sha256={digest}, "
              f"expected={expected}, valid={ok}")
        return 0 if ok else 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    digest = write_entry(out_dir)
    print(entry_text())
    print(f"sha256={digest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
