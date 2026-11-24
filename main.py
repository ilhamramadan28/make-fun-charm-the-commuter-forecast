"""Write the commuter forecast to /output/entry.txt.

Reads entry.txt next to this file, validates the sealed gate
(UTF-8 text, 1-140 characters, not only whitespace) and writes it
byte-identical to /output/entry.txt with mode 0644.
Stdlib only, no network, deterministic.
"""

import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    text = (here / "entry.txt").read_text(encoding="utf-8").strip()
    if not (1 <= len(text) <= 140):
        print(f"entry must be 1-140 chars, got {len(text)}", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 and ch not in "\n\t" for ch in text):
        print("entry must not contain control characters", file=sys.stderr)
        return 1
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.txt"
    out.write_text(text, encoding="utf-8")
    os.chmod(out, 0o644)
    if out.read_text(encoding="utf-8") != text:
        print("written entry does not match source", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
