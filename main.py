#!/usr/bin/env python3
"""Copy the pre-rendered front page into the grader's output directory.

The image itself is drawn by gen_image.py (run during the build, with
PIL available there). The grading sandbox has only the Python standard
library, so this entrypoint does nothing but copy entry.png, which sits
next to this file, to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
