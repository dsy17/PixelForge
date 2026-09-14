from PIL import Image

def load_image(image_path):
    image = Image.open(image_path)
    return image.convert("RGB")

def save_image(image, path):
    image.save(path)