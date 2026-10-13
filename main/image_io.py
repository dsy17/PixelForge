from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError


class ImageIOError(Exception):
    """Raised when an image can't be loaded or saved."""


def load_image(path: str | Path) -> Image.Image:
    """Opens an image file and returns it as RGB."""
    path = Path(path)

    if not path.exists():
        raise ImageIOError(f"Input file not found: {path}")
    if not path.is_file():
        raise ImageIOError(f"Input is not a file: {path}")

    try:
        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image)  # apply rotation stored by cameras/phones
            return image.convert("RGB")
    except UnidentifiedImageError:
        raise ImageIOError(f"Not a supported image file: {path}") from None
    except OSError as error:
        raise ImageIOError(f"Could not read {path}: {error}") from None


def save_image(image: Image.Image, path: str | Path) -> None:
    """Saves an image, creating the output folder if needed. The file extension picks the format."""
    path = Path(path)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
    except (ValueError, KeyError):
        raise ImageIOError(f"Unsupported output format '{path.suffix}': {path}") from None
    except OSError as error:
        raise ImageIOError(f"Could not save {path}: {error}") from None
