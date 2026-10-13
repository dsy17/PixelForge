from PIL import Image
from main.paths import RESOURCES, PALETTES
from main.pipeline import Effect
import numpy as np

PALETTE_NUM = 16


def create_thumbnail(img):
    small = img.copy()
    small.thumbnail((128, 128), Image.Resampling.NEAREST)

    return list(small.get_flattened_data())


def widest_range(box):
    return max(max(c) - min(c) for c in zip(*box))


def find_nearest(box, val):
    idx = ((box - val) ** 2).sum(axis=1).argmin()
    return tuple(box[idx].tolist())


def box_split(px, n=PALETTE_NUM):
    # px is a flat list of pixels; boxes is a list of boxes, each a list of pixels
    boxes = [px]

    while len(boxes) < n:
        box = max(boxes, key=widest_range)  # pick box whose colors vary the most

        if widest_range(box) == 0:
            break

        # find this box's widest channel (0 = R, 1 = G, 2 = B)
        ranges = [max(c) - min(c) for c in zip(*box)]
        channel = ranges.index(max(ranges))

        # sort the box along that channel and cut it at the median
        box_sorted = sorted(box, key=lambda p: p[channel])
        median_index = len(box_sorted) // 2

        # replace the box with its two halves
        boxes.remove(box)
        boxes += [box_sorted[:median_index], box_sorted[median_index:]]

    return boxes

def box_average(box):
    r_px, g_px, b_px = zip(*box)
    r_px = round(sum(r_px) / len(r_px))
    g_px = round(sum(g_px) / len(g_px))
    b_px = round(sum(b_px) / len(b_px))

    return tuple((r_px, g_px, b_px))

def build_palette(boxes):
    palette = []
    for box in boxes:
        palette.append(box_average(box))

    return palette


def mapping(palette, img):
    data = img.get_flattened_data()
    rebuild = []
    palette = np.asarray(palette)
    cache = {}
    for px in data:
        if px not in cache:
            cache[px] = find_nearest(palette, px)
        rebuild.append(cache[px])

    result = Image.new("RGB", img.size)
    result.putdata(rebuild)

    return result

def load_palette(name):
    lines = (PALETTES / f"{name}.hex").read_text().splitlines()
    return [tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) for h in lines]


class Quantize(Effect):
    """ Quantize: limits an image's colour palette via a median cut algorithm. """

    def __init__(self, palette_num: int = PALETTE_NUM):
        self.palette_num = palette_num


    def apply(self, img: Image.Image) -> Image.Image:
        thumb = create_thumbnail(img)
        palette = build_palette(box_split(thumb, self.palette_num))
        result = mapping(palette, img)
        return result.convert("RGB")  # hand RGB to the next effect


if __name__ == "__main__":
    test_img = Image.open(RESOURCES / "image.png").convert("RGB")
    Quantize().apply(test_img).show()


