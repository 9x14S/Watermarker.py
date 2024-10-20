"""
Watermarker CLI program. 

It does basically that: receives a number of image files, and a logo
    or watermark SVG, then applies that watermark to all images.
"""

__author__  = "9x14S"
__version__ = 0.1

import argparse

from pathlib import Path
from shutil import copy
from sys import exit, stderr
from io import BytesIO

from cairosvg import svg2png
from PIL import Image


def printerr(err_msg: str, exit_code: int) -> None:
    """Prints and error message and (optionally) exits with error code."""
    print(err_msg, file=stderr)
    if exit_code > 0:
        exit(exit_code)
    return


def backup(files: list[Path]) -> None:
    """Backs up all files in `files` and names them `<file>.bak`.
    :param files: list of files to back up.
    :type files: list[Path]

    :return: None
    """

    for file in files:
        try:
            copy(file, str(file)+".bak")
        except PermissionError as e:
            printerr(str(e), 0)
            printerr(f"File {file} could not be backed. Exiting.", 3)
    return


def main(
    watermark: str,
    files: list[str],
    position: str,
    alpha: float,
) -> int:
    """Checks and loads all the files and the watermark. Then adds the watermark to 
    them based on the options provided.

    :param watermark: the watermark SVG filepath.
    :type watermark: str

    :param files: a list of length >= 1 of all the png/jpg files.
    :type files: list[str]

    :param position: the position where the watermark will be placed.
    :type position: str

    :param alpha: the desired transparency for the watermark.
    :type alpha: float

    :return: exit code
    :rtype: int
    """

    # Check SVG
    if not watermark.lower().endswith(".svg"):
        printerr(f"File {watermark} not an SVG file.", 1)

    watermark_path = Path(watermark)
    if not watermark_path.exists():
        printerr(f"Nonexistent file {watermark_path.name}. Exiting.", 2)

    # Load SVG
    svg2png_buffer = BytesIO()
    svg2png(url=str(watermark_path), write_to=svg2png_buffer)
    png_watermark = Image.open(fp=svg2png_buffer)
    
    # Check for valid files
    usable: list[Path] = []
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

    backup(usable)

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

    printerr("Finalized execution", main(args.watermark, args.files, args.position, args.alpha))
