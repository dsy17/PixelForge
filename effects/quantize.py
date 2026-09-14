from PIL import Image
from main.pipeline import Effect

class Quantize(Effect):
    """Reduces number of colors in an image to a limited palette"""

    def apply(self):