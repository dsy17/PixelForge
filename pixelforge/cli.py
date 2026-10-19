import argparse
from pixelforge.image_io import load_image, save_image
from pixelforge.pipeline import Pipeline
from pixelforge.effects.quantize import Quantize
from pixelforge.effects.dither import Dither
from pixelforge.effects.ascii import Ascii
from pixelforge.effects.pixelsort import PixelSort


def build_pipeline(args: argparse.Namespace) -> Pipeline:
    """Translates parsed CLI flags into a list of Effect instances."""
    effects = []
    if args.quantize:
        effects.append(Quantize(palette_num=args.colors))
    if args.dither:
        effects.append(Dither())
    if args.ascii:
        effects.append(Ascii(width=args.ascii_width))
    if args.pixelsort:
        effects.append(PixelSort())
    return Pipeline(effects)


def main() -> None:
    parser = argparse.ArgumentParser(prog="pixelforge", description="PixelForge — image effects pipeline")
    parser.add_argument("input", help="Path to the input image")
    parser.add_argument("output", help="Path to save the processed image")
    parser.add_argument("--quantize", action="store_true")
    parser.add_argument("--colors", type=int, default=16)
    parser.add_argument("--dither", action="store_true")
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--ascii-width", type=int, default=100)
    parser.add_argument("--pixelsort", action="store_true")
    parser.add_argument("--lower", type=int, default=40)
    parser.add_argument("--upper", type=int, default=235)


    args = parser.parse_args()

    image = load_image(args.input)
    pipeline = build_pipeline(args)
    result = pipeline.run(image)
    save_image(result, args.output)


if __name__ == "__main__":
    main()