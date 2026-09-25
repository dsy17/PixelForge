"""Standalone reference: image -> ASCII text -> PNG.

Self-contained so it can be read and run in isolation. Nothing here imports
from main/ or effects/. Run it directly:

    python3 sandbox/ascii_art.py resources/image.png out.png
"""

import argparse
from math import ceil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

# Dark -> light. Index 0 is the densest glyph, so it maps to the darkest pixel.
RAMPS = {
    "classic": "@%#*+=-:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
}

# First one that exists wins. All three are true fixed-width fonts on macOS.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Supplemental/Courier New.ttf",
    "/System/Library/Fonts/Supplemental/Andale Mono.ttf",
]


def load_font(size):
    """Return a monospace font. A proportional font would misalign every column."""
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def cell_size(font):
    """Pixel size of one character cell: (advance width, line height).

    Every glyph in a monospace font shares an advance width, so measuring "M"
    measures all of them. Height comes from the font's own vertical metrics.
    """
    ascent, descent = font.getmetrics()
    return font.getlength("M"), ascent + descent


def image_to_ascii(img, cols, ramp, cell_aspect):
    """Downsample to a `cols`-wide grid and map each pixel to one character.

    cell_aspect is cell_width / line_height (~0.5). Without it the output is
    stretched vertically, because character cells are about twice as tall as
    they are wide. This is the same problem the "append a space after every
    character" trick solves for plain text -- do one or the other, never both.
    """
    width, height = img.size
    rows = max(1, round(height / width * cols * cell_aspect))

    small = ImageOps.grayscale(img.resize((cols, rows)))
    pixels = list(small.getdata())  # flat, row-major

    top = len(ramp) - 1
    lines = []
    for y in range(rows):
        row = pixels[y * cols:(y + 1) * cols]
        # Scale by ramp length rather than a fixed divisor, so the whole ramp
        # is reachable and swapping ramps can't run off the end.
        lines.append("".join(ramp[value * top // 255] for value in row))
    return "\n".join(lines)


def render_ascii_to_png(text, font, fg="black", bg="white", source_rgb=None):
    """Draw ASCII text onto a new image sized exactly to the glyph grid.

    Pass source_rgb (an RGB image already resized to the character grid) to
    colour each glyph from the original pixel instead of using a flat fg.
    """
    lines = text.splitlines()
    cell_w, line_h = cell_size(font)

    cols = max(len(line) for line in lines)
    canvas = Image.new("RGB", (ceil(cell_w * cols), line_h * len(lines)), bg)
    draw = ImageDraw.Draw(canvas)

    for y, line in enumerate(lines):
        if source_rgb is None:
            # One call per row is much faster than one per character.
            draw.text((0, y * line_h), line, font=font, fill=fg)
        else:
            for x, char in enumerate(line):
                draw.text((x * cell_w, y * line_h), char, font=font,
                          fill=source_rgb.getpixel((x, y)))
    return canvas


def main():
    parser = argparse.ArgumentParser(description="Render an image as ASCII art PNG")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--cols", type=int, default=100)
    parser.add_argument("--font-size", type=int, default=14)
    parser.add_argument("--ramp", choices=RAMPS, default="classic")
    parser.add_argument("--color", action="store_true", help="colour glyphs from the source")
    parser.add_argument("--txt", help="also write the plain-text version here")
    args = parser.parse_args()

    img = Image.open(args.input).convert("RGB")
    font = load_font(args.font_size)
    cell_w, line_h = cell_size(font)

    text = image_to_ascii(img, args.cols, RAMPS[args.ramp], cell_w / line_h)

    source_rgb = None
    if args.color:
        rows = len(text.splitlines())
        source_rgb = img.resize((args.cols, rows))

    render_ascii_to_png(text, font, source_rgb=source_rgb).save(args.output)

    if args.txt:
        Path(args.txt).write_text(text)


if __name__ == "__main__":
    main()
