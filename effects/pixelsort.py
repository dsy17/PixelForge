from main.paths import RESOURCES
from PIL import Image

img = Image.open(RESOURCES / "mountain.png").convert("RGB")

MASK = []
SORT = []
ROW = True  # If false, filter by columns instead
REVERSE = False
LOWER = 40
UPPER = 235


def pixel_sort(img):
    w, h = img.size
    pixels = list(img.get_flattened_data())
    rows = [pixels[y * w:(y + 1) * w] for y in range(h)]

    for row in rows:
        for start, end in find_intervals(row):
            row[start:end] = sorted(row[start:end], key=luma, reverse=REVERSE)

    result = Image.new("RGB", img.size)
    result.putdata([p for row in rows for p in row])
    return result


def luma(px):
    r, g, b = px
    return 0.299 * r + 0.587 * g + 0.114 * b


def find_intervals(row: list) -> list:
    intervals = []
    start = None
    sortable = False

    for i, pixel in enumerate(row):
        val = luma(pixel)
        sortable = LOWER <= val <= UPPER

        if sortable and start is None:
            start = i

        elif not sortable and start is not None:
            intervals.append((start, i))
            start = None

    if start is not None:
        intervals.append((start, len(row)))

    return intervals


pixel_sort(img).show()
