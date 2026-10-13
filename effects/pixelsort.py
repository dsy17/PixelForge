from main.paths import RESOURCES
from main.pipeline import Effect
from PIL import Image

# Unused settings for future features implementing masks
MASK = []
SORT = []
ROW = True  # If false, filter by columns instead

# Settings
LOWER = 40
UPPER = 235
REVERSE = False


def pixel_sort(img, lower: int = LOWER, upper: int = UPPER, reverse: bool = REVERSE):
    w, h = img.size
    pixels = list(img.get_flattened_data())
    rows = [pixels[y * w:(y + 1) * w] for y in range(h)]

    for row in rows:
        for start, end in find_intervals(row, lower, upper):
            row[start:end] = sorted(row[start:end], key=luma, reverse=REVERSE)

    result = Image.new("RGB", img.size)
    result.putdata([p for row in rows for p in row])
    return result


def luma(px):
    r, g, b = px
    return 0.299 * r + 0.587 * g + 0.114 * b


def find_intervals(row: list, lower, upper) -> list:
    intervals = []
    start = None

    for i, pixel in enumerate(row):
        val = luma(pixel)
        sortable = lower <= val <= upper

        if sortable and start is None:
            start = i

        elif not sortable and start is not None:
            intervals.append((start, i))
            start = None

    if start is not None:
        intervals.append((start, len(row)))

    return intervals


class PixelSort(Effect):
    """Pixel sorting: sorts runs of pixels in each row by bright
    ness, leaving the darkest and brightest untouched."""

    def __init__(self, lower: int = LOWER, upper: int = UPPER, reverse: bool = False):
        self.lower = lower
        self.upper = upper
        self.reverse = reverse

    def apply(self, image: Image.Image) -> Image.Image:
        result = pixel_sort(image.convert("RGB"), self.lower, self.upper, self.reverse)
        return result  # hand RGB to the next effect

if __name__ == "__main__":

    img = Image.open(RESOURCES / "image.png").convert("RGB")
    PixelSort().apply(img).show()
