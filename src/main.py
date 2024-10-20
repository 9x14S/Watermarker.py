"""
Watermarker CLI program. 

It does basically that: receives a number of image files, and a logo
    or watermark SVG, then applies that watermark to all images.
"""

__author__  = "9x14S"
__version__ = 0.1

import argparse

from pathlib import Path
from sys import exit, stderr

from PIL import Image


def printerr(err_msg: str, exit_code: int) -> None:
    print(err_msg, file=stderr)
    if exit_code > 0:
        exit(exit_code)


def main(
    watermark: str,
    files: list,
    position: str,
    alpha: float,
) -> int:

    if not watermark.lower().endswith(".svg"):
        printerr(f"File {watermark} not an SVG file.", 1)
    
    usable = []
    for file in files:
        extension = file.lower().split('.')[-1]
        if extension not in ["jpeg", "jpg", "png"]:
            printerr(f"Skipping {file} due to unknown extension {extension}.", 0)
        else:
            path = Path(file)
            if not path.exists():
                printerr(f"Nonexistent file {path.name}. Skipping", 0)
            else:
                usable.append(path)

    print(usable)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Watermarker.py",
        description="Watermarks images with provided watermark",
        epilog=f"Made as a test by {__author__}",
    )

    parser.add_argument("watermark", help="watermark file")
    parser.add_argument("files", nargs='+', help="files to be watermarked")
    parser.add_argument(
        "-p", "--position",
        type=str,
        default="bottomright",
        choices=["topleft", "topright", "bottomleft", "bottomright", "center"],
        help="position"
    )
    parser.add_argument("-a", "--alpha", default=100.0, type=float, help="transparency value")
    args = parser.parse_args()

    exit(main(args.watermark, args.files, args.position, args.alpha))
