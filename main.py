"""One Sentence Absurd Invention Pitch — the sighing kettle (Sparta entry).

The pitch is a single sentence in spec/log format: a kettle with a daily
boil limit that sighs, logs its own burnout risk, and goes on strike when
overworked. The humour comes from the fields — a SKU, a decibel reading,
a burnout percentage, and a closed status — not from prose.

Gate: entry.txt must be exactly one sentence, 1-220 characters, not only
whitespace. One terminal period only — the "status: on strike" closing is
part of the same sentence, joined by a comma, so the log line stays a
single sentence while still ending on a closed machine status.
"""

import os
import sys

TEXT = "SKU-KE-731: kettle rated 6 boils/day sighs at 42 dB on boil #7, logs burnout risk 87%, and refuses to boil again until tomorrow, status: on strike."


def main() -> int:
    text = TEXT
    encoded = text.encode("utf-8")
    if not (1 <= len(text) <= 220):
        print(f"gate failed: entry is {len(text)} characters, must be 1-220", file=sys.stderr)
        return 1
    if not text.strip():
        print("gate failed: entry is only whitespace", file=sys.stderr)
        return 1
    if text.count(".") != 1 or not text.endswith("."):
        # Exactly one terminal period: the status clause is comma-joined,
        # so the whole log line is a single sentence by construction.
        print("gate failed: entry must be exactly one sentence", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(encoded)

    # Read back and verify byte-for-byte.
    with open(path, "rb") as fh:
        if fh.read() != encoded:
            print("verification failed: entry.txt does not match TEXT", file=sys.stderr)
            return 1
    print(f"wrote entry.txt ({len(text)} characters, 1 sentence)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
