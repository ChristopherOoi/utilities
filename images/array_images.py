#!/usr/bin/env python3
import os
from glob import glob
import sys
import argparse
from PIL import Image


def get_images(
    path: str,
    patterns: list[str],
) -> tuple[list[Image.Image], tuple[int, int]]:
    """
    Get images from path with pattern(s)
    Confirm if Images have different sizes
    """
    images = []
    sizes = []
    impaths = [
        impath for pattern in patterns for impath in glob(os.path.join(path, pattern))
    ]
    if len(impaths) == 0:
        print(
            f"No images found... Please double check path and patterns: {path}, {patterns}"
        )
        sys.exit()
    for impath in impaths:
        im = Image.open(impath)
        images.append(im)
        sizes.append(im.size)
    # check sizes for differences
    sizeset = set(sizes)
    # get max height and max width of images
    maxwidth = max([size[0] for size in sizes])
    maxheight = max([size[1] for size in sizes])
    sizecounts = {s: sizes.count(s) for s in sizeset}
    print(
        f"Found {count} images with size {size}..."
        for size, count in sizecounts.items()
    )
    if len(sizeset) > 1:
        print("Found images with different sizes!")
        print("Continue? [Y/n]")
        while input().lower() not in ["y", "n", ""]:
            print("Invalid input. Please enter 'y' or 'n'")
            input = input()
        if input.lower() == "n":
            sys.exit()
    return images, (maxheight, maxwidth)


def array_images(
    images: list[Image.Image],
    outname: str,
    size: tuple,
    spacing: int = 0,
    rows: int = 0,
    cols: int = 0,
) -> None:
    """
    Array images in a grid
    """
    height, width = size
    # split imagelist into groups of rows*cols
    groups = [images[i : i + rows * cols] for i in range(0, len(images), rows * cols)]
    print(f"Creating {len(groups)} new images...")
    for i, group in enumerate(groups):
        # create new image
        outname = outname + f"_{i}{group[0].format}"
        outpath = os.path.join(os.getcwd(), outname)
        newimage = Image.new(
            "RGB",
            (width * cols + spacing * (cols - 1), height * rows + spacing * (rows - 1)),
        )
        # paste images in grid
        for i, im in enumerate(group):
            row = i // cols
            col = i % cols
            newimage.paste(im, (col * (width + spacing), row * (height + spacing)))
        newimage.save(outpath)
        print(f"Saved {outname} to {os.getcwd()}...")


def create_image_arrays(
    path: str = None,
    patterns: list[str] = None,
    outname: str = None,
    spacing: int = 0,
    rows: int = 0,
    cols: int = 0,
):
    if not rows and not cols:
        print("Please specify number of rows or columns")
        sys.exit()
    if not patterns:
        print("No patterns specified, defaulting to .png...")
        patterns = ["*.png"]
    if not outname:
        print("No output name specified, defaulting to 'array'...")
        outname = "array"
    if not path:
        print("No path specified, defaulting to current directory...")
        path = os.getcwd()
    images, size = get_images(path, patterns)
    print(f"Creating image arrays with {len(images)} images...")
    array_images(images, outname, size, spacing, rows, cols)
    # close images
    for im in images:
        im.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Array images in a grid")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path to images",
    )
    parser.add_argument(
        "-pat",
        "--patterns",
        type=str,
        nargs="+",
        help="Patterns to search for in path",
    )
    parser.add_argument(
        "-o",
        "--outname",
        type=str,
        help="Name of output file",
    )
    parser.add_argument(
        "-s",
        "--spacing",
        type=int,
        help="Spacing between images",
    )
    parser.add_argument(
        "-r",
        "--rows",
        type=int,
        help="Number of rows",
    )
    parser.add_argument(
        "-c",
        "--cols",
        type=int,
        help="Number of columns",
    )
    args = parser.parse_args()
    create_image_arrays(
        args.path, args.patterns, args.outname, args.spacing, args.rows, args.cols
    )
