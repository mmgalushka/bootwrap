# Copyright (c) 2019 AUROMIND Ltd. All rights reserved.

"""
An image.
"""

from .base import (
    WebComponent,
    ClassMixin
)
from .utils import attr

__all__ = [ 'Image' ]


class Image(WebComponent, ClassMixin):
    """A web-component for an image.

    Args:
        src (obj): The image source to show.
        width (int): The image width.
        height (int): The image height.
        alternative (list): The alternative missage.
    """
    def __init__(self, src, width=None, height=None, alternative=None):
        super().__init__()
        self.__src = src
        self.__width = width
        self.__height = height
        self.__alternative = alternative

    def __str__(self):
        return f'''
            <img {attr('class', self.classes)} 
                {attr('src', self.__src)}
                {attr('width', self.__width)}
                {attr('height', self.__height)}
                {attr('alt', self.__alternative)}/>
        '''
