# https://python.astrotech.io/design-patterns/structural/adapter.html
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

# Inheritance: НАСЛЕДОВАНИЕ

class Image:
    pass


class Filter(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, image: Image) -> None:
        pass


class VividFilter(Filter):
    def apply(self, image: Image) -> None:
        print('Applying Vivid Filter')


class BlackAndWhite3rdPartyFilter:
    def init(self):
        """Required by 3rd party library"""

    def render(self, image: Image):
        print('Applying BlackAndWhite Filter')


@dataclass
class BlackAndWhiteAdapter:
    __filter: BlackAndWhite3rdPartyFilter

    def apply(self, image: Image) -> None:
        self.__filter.init()
        self.__filter.render(image)


@dataclass
class ImageView:
    __image: Image

    def apply(self, filter: Filter):
        filter.apply(self.__image)


if __name__ == '__main__':
    image_view = ImageView(Image())
    image_view.apply(BlackAndWhiteAdapter(BlackAndWhite3rdPartyFilter()))