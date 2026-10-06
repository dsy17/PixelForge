from main.paths import RESOURCES
from main.pipeline import test_img
from PIL import Image

test_img = test_img.convert("L").resize(size=(200,200))

BAYER_4 = [
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
]

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


def dither_pixel(value, x, y):
    return 255 if value > thresholds[y % n][x % n] else 0


def dither_image(img: Image.Image) -> Image.Image:
    src = img.load()
    result = Image.new("L", img.size)  # new blank image, same size
    out = result.load()
    W, H = img.size
    for y in range(H):
        for x in range(W):
            out[x, y] = dither_pixel(src[x, y], x, y)

    return result


img = dither_image(test_img)
img.show()
