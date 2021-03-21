"""
An image.
"""

from .base import (
    WebComponent,
    ClassMixin
)
from .utils import attr


class Image(WebComponent, ClassMixin):
    """A web-component for an image.

    Args:
        src (obj): The image source to show.
        width (int): The image width.
        height (int): The image height.
        alt (str): The alt text.
    """
    def __init__(self, src, width=None, height=None, alt=None):
        super().__init__()
        self.__src = src
        self.__width = width
        self.__height = height
        self.__alt = alt

    def __str__(self):
        return f'''
            <img {attr("id", self.identifier)}
                {attr('class', self.classes)}
                {attr('src', self.__src)}
                {attr('width', self.__width)}
                {attr('height', self.__height)}
                {attr('alt', self.__alt)}/>
        '''
