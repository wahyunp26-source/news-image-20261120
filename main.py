"""News in One Image: Friday 20 November 2026.

A single-day newspaper front page — 38 verified stories from Friday
20 November 2026 across 6 continents plus space — as one 1024x1024 image.

The page is pre-composed at build time (build.py, Pillow) and stored beside
this file as entry.png (JPEG bytes). This program only copies that file to
the grader's output directory, using paths anchored to __file__ so it works
no matter what the working directory is. Deterministic: same bytes every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    # Guard against a truncated copy: the output must be byte-identical.
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        return 1
    print("wrote", target, os.path.getsize(target), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
