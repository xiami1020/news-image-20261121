"""Entry point: build the 21 November 2026 news front page.

Run:  python3 main.py

Writes the same PNG bytes to /output/entry.png, to output/entry.png
and to entry.png next to this file. Fully offline and deterministic:
no clock, no network, no randomness, so every run produces the
identical file.
"""

import hashlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate import render

HERE = Path(__file__).resolve().parent


def main() -> None:
    image = render()
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    blob = buffer.getvalue()
    targets = [
        Path("/output/entry.png"),
        HERE / "output" / "entry.png",
        HERE / "entry.png",
    ]
    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
    digest = hashlib.sha256(blob).hexdigest()
    print(f"wrote {len(blob)} bytes, sha256={digest}")
    for target in targets:
        print(f"  {target}")


if __name__ == "__main__":
    main()
