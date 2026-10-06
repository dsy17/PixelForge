from PIL import Image, ImageOps, ImageDraw, ImageFont
from main.pipeline import test_img

WIDTH = 50
IMAGE = test_img
CHAR = {
    "classic": "'@!$%^&,/>=?+#|:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'. ",
}
ascii_char = CHAR["classic"]


def resize_image(img):
    new_height = int((img.size[0] / img.size[1]) * WIDTH)
    new_image = img.resize((WIDTH, new_height), Image.Resampling.NEAREST)

    return new_image


def grayscale_img(img):
    return ImageOps.grayscale(img)


def ascii_generator(img):
    resize_img = resize_image(img)
    gs_img = grayscale_img(resize_img)
    get_pixels = gs_img.get_flattened_data()

    char_string = ""
    for a in get_pixels:
        index =  int(a // (256 / len(ascii_char)))
        char_string += "".join(ascii_char[index])

    return char_string

def ascii_to_image(text, font_size=12, fg="white", bg="black"):
    lines = text.splitlines()
    font = ImageFont.truetype("consola.ttf", font_size)

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

if __name__ == "__main__":
    img_string = ascii_generator(test_img)
    final_image = "\n".join(img_string[i:(i + WIDTH)] for i in range(0, len(img_string), WIDTH))

    with open("ascii_prime.txt", "w") as f:
        f.write(final_image)

    text = open("ascii_prime.txt").read()
    ascii_to_image(text).show()
