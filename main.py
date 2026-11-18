#!/usr/bin/env python3
"""Entry program for the make.fun competition news-image-20261117.

The repository ships a finished front-page image, entry.png, which sums up
the world news of Tuesday 17 November 2026 in fifty stories. This program
copies that image to the output location the grader expects:

    $MAKEFUN_OUTPUT_DIR/entry.png   when the variable is set
    /output/entry.png               otherwise

It uses only the Python standard library, touches no network, and writes
exactly the same bytes on every run.
"""

import os
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
FALLBACK_OUTPUT_DIR = "/output"
COPY_CHUNK = 65536


def output_directory():
    """Return the directory the grader wants the image written to."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return chosen or FALLBACK_OUTPUT_DIR


def copy_bytes(source, target):
    """Copy a file chunk by chunk and return how many bytes were written."""
    written = 0
    with open(source, "rb") as src, open(target, "wb") as dst:
        while True:
            chunk = src.read(COPY_CHUNK)
            if not chunk:
                break
            dst.write(chunk)
            written += len(chunk)
    return written


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        raise SystemExit("source image not found beside main.py: " + source)
    target_dir = output_directory()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, OUTPUT_NAME)
    written = copy_bytes(source, target)
    expected = os.path.getsize(source)
    if written != expected:
        raise IOError(
            "copied %d bytes but the source image holds %d" % (written, expected)
        )
    print("wrote %s (%d bytes)" % (target, written), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
