from PIL import Image, ImageOps, ImageDraw, ImageFont
from main.paths import RESOURCES
from main.pipeline import Effect

WIDTH = 100
CHAR = {
    "classic": "'@!$%^&,/>=?+#|:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'. ",
}
ascii_char = CHAR["classic"]

# Monospace fonts to try, one per OS: Windows, macOS, Linux
FONTS = ["consola.ttf", "Menlo.ttc", "DejaVuSansMono.ttf"]


def load_font(size):
    """ Returns the first monospace font found on this system, or Pillow's built-in font."""
    for name in FONTS:
        try:
            return ImageFont.truetype(name, size)
        except OSError:  # font isn't installed here, try the next one
            continue

    return ImageFont.load_default(size)


def resize_image(img, width):
    new_height = int((img.size[1] / img.size[0]) * width)
    new_image = img.resize((width, new_height), Image.Resampling.NEAREST)

    return new_image


def grayscale_img(img):
    return ImageOps.grayscale(img)


def text_to_str(img_str, width):
    ascii_str = "\n".join(img_str[i:(i + width)] for i in range(0, len(img_str), width))
    return ascii_str


def ascii_generator(img, width):
    resize_img = resize_image(img, width)
    gs_img = grayscale_img(resize_img)
    get_pixels = gs_img.get_flattened_data()

    char_string = ""
    for a in get_pixels:
        index =  int(a // (256 / len(ascii_char)))
        char_string += "".join(ascii_char[index])

    return char_string

def ascii_to_image(tx, width, font_size=12, fg="white", bg="black"):
    text = text_to_str(tx, width)
    lines = text.splitlines()
    font = load_font(font_size)

    # size of one character cell
    left, top, right, bottom = font.getbbox("@")
    cell_w = bottom - top

    cols = max(len(line) for line in lines)
    img = Image.new("RGB", (cols * cell_w, len(lines) * cell_w), bg)
    draw = ImageDraw.Draw(img)

    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            draw.text((col * cell_w, row * cell_w - top), ch, font=font, fill=fg)

    return img

class Ascii(Effect):

    def __init__(self, width: int = WIDTH):
        self.width = width

    def apply(self, image: Image.Image) -> Image.Image:
        result = ascii_to_image(ascii_generator(image, self.width), self.width)
        return result.convert("RGB")



if __name__ == "__main__":
    test_img = Image.open(RESOURCES / "image.png").convert("RGB")
    Ascii().apply(test_img).show()
