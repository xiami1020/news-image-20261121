#!/usr/bin/env python3
"""make.fun news-image-20261121 entry (Python 3.13, standard library only).
Copies the bundled entry.png to /output/entry.png, deterministically:
same bytes every run, no network, no time, no randomness.
Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

src = Path(__file__).resolve().parent / "entry.png"
out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
out.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, out)
