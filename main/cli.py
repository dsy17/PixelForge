import argparse
from main.image_io import load_image, save_image
from main.pipeline import Pipeline
from effects.quantise import image_quantise
from effects.dither import image_dither
from effects.ascii_art import image_ascii


def build_pipeline(args: argparse.Namespace) -> Pipeline:
    """Translates parsed CLI flags into a list of Effect instances."""
    effects = []
    if args.quantize:
        effects.append(image_quantise(colors=args.colors))
    if args.dither:
        effects.append(image_dither(method="floyd-steinberg"))
    if args.ascii:
        effects.append(image_ascii(width=args.ascii_width))
    return Pipeline(effects)


def main() -> None:
    parser = argparse.ArgumentParser(description="PixelForge — image effects pipeline")
    parser.add_argument("input", help="Path to the input image")
    parser.add_argument("output", help="Path to save the processed image")
    parser.add_argument("--quantize", action="store_true")
    parser.add_argument("--colors", type=int, default=8)
    parser.add_argument("--dither", action="store_true")
    parser.add_argument("--ascii", action="store_true")
    parser.add_argument("--ascii-width", type=int, default=100)

    args = parser.parse_args()

    image = load_image(args.input)
    pipeline = build_pipeline(args)
    result = pipeline.run(image)
    save_image(result, args.output)


if __name__ == "__main__":
    main()