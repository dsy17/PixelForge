import argparse
import sys
from pathlib import Path
from pixelforge.image_io import ImageIOError, load_image, save_image
from pixelforge.pipeline import Effect, Pipeline
from pixelforge.effects.quantize import Quantize, available_palettes
from pixelforge.effects.dither import Dither
from pixelforge.effects.ascii import Ascii
from pixelforge.effects.pixelsort import PixelSort, LOWER, UPPER


class PaletteAction(argparse.Action):
    """Handles --palette NAME: stores the palette name and adds a quantize step at this point in the order."""

    def __call__(self, parser, namespace, values, option_string=None):
        namespace.palette = values
        namespace.effects = (namespace.effects or []) + ["quantize"]


def make_effect(name: str, args: argparse.Namespace) -> Effect:
    """Creates one effect from its name, using the settings from the CLI flags."""
    if name == "quantize":
        return Quantize(palette_num=args.colors, palette=args.palette)
    if name == "dither":
        return Dither()
    if name == "ascii":
        return Ascii(width=args.ascii_width)
    if name == "pixelsort":
        return PixelSort(lower=args.lower, upper=args.upper, reverse=args.reverse)
    raise ValueError(f"Unknown effect: {name}")


def build_pipeline(args: argparse.Namespace) -> Pipeline:
    """Turns the effect flags into a Pipeline, in the order they were typed."""
    return Pipeline([make_effect(name, args) for name in args.effects])


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pixelforge",
        description="PixelForge — image effects pipeline. Effects run in the order you type them.",
    )
    parser.add_argument("input", help="Path to the input image")
    parser.add_argument("output", help="Path to save the processed image")

    # Each effect flag adds its name to args.effects, so the list keeps the typed order
    effects = parser.add_argument_group("effects")
    effects.add_argument("--quantize", dest="effects", action="append_const", const="quantize",
                         help="reduce the number of colours using a palette generated from the image")
    effects.add_argument("--palette", choices=available_palettes(), action=PaletteAction,
                         help="quantize to a fixed palette instead of generating one")
    effects.add_argument("--dither", dest="effects", action="append_const", const="dither",
                         help="ordered (Bayer) dithering to black and white")
    effects.add_argument("--ascii", dest="effects", action="append_const", const="ascii",
                         help="redraw the image as ASCII characters")
    effects.add_argument("--pixelsort", dest="effects", action="append_const", const="pixelsort",
                         help="sort runs of pixels in each row by brightness")

    parser.add_argument("--colors", type=int, default=16)
    parser.add_argument("--ascii-width", type=int, default=100)
    parser.add_argument("--lower", type=int, default=LOWER)
    parser.add_argument("--upper", type=int, default=UPPER)
    parser.add_argument("--reverse", action="store_true")
    parser.add_argument("--overwrite", action="store_true",
                        help="replace the output file if it already exists")


    args = parser.parse_args()
    if not args.effects:
        parser.error("choose at least one effect, e.g. --dither")
    if Path(args.output).exists() and not args.overwrite:
        sys.exit(f"pixelforge: error: {args.output} already exists (use --overwrite to replace it)")

    try:
        image = load_image(args.input)
        pipeline = build_pipeline(args)
        result = pipeline.run(image)
        save_image(result, args.output)
    except ImageIOError as error:
        sys.exit(f"pixelforge: error: {error}")  # prints to stderr and exits with code 1


if __name__ == "__main__":
    main()
