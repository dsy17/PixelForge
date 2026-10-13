from abc import ABC, abstractmethod
from PIL import Image


class Effect(ABC):
    """Base class for every effect: takes an image, returns a new image.

    Settings go in __init__, the work goes in apply():

        class Dither(Effect):
            def __init__(self, method: str = "bayer"):
                self.method = method

            def apply(self, image: Image.Image) -> Image.Image:
                ...
                return result
    """

    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image:
        """Returns the processed image (does not modify input)."""

    def __repr__(self) -> str:
        settings = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({settings})"


class Pipeline:
    """Runs a list of effects in order and feeds each one's output into the next."""

    def __init__(self, effects: list[Effect] | None = None):
        self.effects = list(effects or [])

    def add(self, effect: Effect) -> "Pipeline":
        self.effects.append(effect)
        return self  # allows Pipeline().add(a).add(b)

    def run(self, image: Image.Image) -> Image.Image:
        for effect in self.effects:
            image = effect.apply(image)
        return image
