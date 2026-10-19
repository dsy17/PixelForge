from pathlib import Path

PACKAGE = Path(__file__).parent  # the pixelforge/ folder
PALETTES = PACKAGE / "palettes"  # installed with the package
RESOURCES = PACKAGE.parent / "resources"  # local test images, only in a cloned repo
