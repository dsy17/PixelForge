from PIL import Image, ImageOps
from main.pipeline import test_img

WIDTH = 50
IMAGE = test_img
CHAR = {
    "classic": "'@!$%^&*~,/>={}[]?+#|:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
}
ascii_char = CHAR["classic"]


def resize_image(img):
    new_height = int((img.size[0] / img.size[1]) * WIDTH)
    new_image = img.resize((WIDTH, new_height))

    return new_image


def grayscale_img(img):
    return ImageOps.grayscale(img)


def ascii_generator(img):
    resize_img = resize_image(img)
    gs_img = grayscale_img(resize_img)
    get_pixels = gs_img.get_flattened_data()

    char_string = ""
    for a in get_pixels:
        char_string += "".join(ascii_char[a // 18])
        char_string += " "

    return char_string


img_string = ascii_generator(test_img)
final_image = "\n".join(img_string[i:(i + (WIDTH * 2))] for i in range(0, len(img_string), WIDTH * 2))

with open("ascii_prime.txt", "w") as f:
    f.write(final_image)


def image_ascii():
    return None
