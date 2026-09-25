from PIL import Image, ImageOps
from main.paths import RESOURCES

new_width = 50

ascii_char = set(line.strip() for line in open(RESOURCES / 'ascii_char.txt'))
print(ascii_char)


ascii_char_alt = ["@", "!", "$", "%", "^", "&", "*", "~", ",", "`", "\"", "=", ">", "{", "}", "[", "]", "?", "±", "§",
                  "+", "#", "|", ":", ".", " "]


def process_image(image):
    image_width, image_height = image.size
    ratio = image_height / image_width
    new_height = int(ratio * new_width)
    new_image = image.resize((new_width, new_height))

    new_image = ImageOps.grayscale(new_image)

    return new_image


def ascii_generator():
    new_image = process_image(pre_image)
    new_image.save("newimage.png")
    get_pixels = new_image.getdata()

    char_string = ""
    for a in get_pixels:
        char_string += "".join(ascii_char[a//18])
        char_string += " "

    return char_string


img_string = ascii_generator()
final_image = "\n".join(img_string[i:(i + (new_width * 2))] for i in range(0, len(img_string), new_width * 2))

with open("ascii_prime.txt", "w") as f:
    f.write(final_image)


def image_ascii():
    return None