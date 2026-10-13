from main.paths import RESOURCES
from main.pipeline import Effect
from PIL import Image

BAYER_4 = [
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
]

# Unused alternative matrix for PS1 style rendering
PS1_DITHER = [
    [-4, 0, -3, 1],
    [2, -2, 3, -1],
    [-3, 1, -4, 0],
    [3, -1, 2, -2],
]



n = len(BAYER_4)  # 4
levels = n * n  # 16 cells, so 16 thresholds
step = 256 // levels  # 16 brightness values per threshold
thresholds = [[cell * step + step // 2 for cell in row] for row in BAYER_4]


def dither_pixel(value, x, y) -> int:
    return 255 if value > thresholds[y % n][x % n] else 0


def dither_image(img: Image.Image, color: bool = False) -> Image.Image:
    if color:
        raise NotImplementedError("Colour dithering not implemented yet")

    src = img.load()
    result = Image.new("L", img.size)  # new blank image, same size
    out = result.load()
    W, H = img.size
    for y in range(H):
        for x in range(W):
            out[x, y] = dither_pixel(src[x, y], x, y)

    return result


class Dither(Effect):
    """Ordered (Bayer) dithering: reduces the image to pure black and white."""

    def __init__(self, color: bool = False):
        self.color = color  # keep colour instead of reducing to black and white

    def apply(self, image: Image.Image) -> Image.Image:
        result = dither_image(image.convert("L"), self.color)
        return result.convert("RGB")  # hand RGB to the next effect


if __name__ == "__main__":
    test_img = Image.open(RESOURCES / "image.png").resize(size=(200, 200))
    Dither().apply(test_img).show()
