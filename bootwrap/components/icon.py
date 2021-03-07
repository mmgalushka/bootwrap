"""
An icon.
"""

from .base import (
    WebComponent,
    ClassMixin,
    AppearanceMixin
)
from .utils import attr

__all__ = [ 'Icon' , 'Spinner']


class Icon(WebComponent, ClassMixin, AppearanceMixin):
    """An icon.

    Args:
        name (str): The icon name.
    """
    def __init__(self, name):
        super().__init__()
        self.__name = name

    def __str__(self):
        self.add_classes(self.__name)

        if self._category is not None:
            self.add_classes('text-%s' % self._category)

        return f'''<i {attr('class', self.classes)}></i>'''


class Spinner(WebComponent, ClassMixin, AppearanceMixin):
    """A spinner icon."""

    def __str__(self):
        self.add_classes('spinner')

        if self._category is not None:
            self.add_classes('text-%s' % self._category)

        return f'''<span {attr('class', self.classes)}></span>'''
