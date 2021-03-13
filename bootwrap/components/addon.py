# Copyright (c) 2019 AUROMIND Ltd. All rights reserved.

"""
Web-components providing additional functions.
"""

from .base import (
    WebComponent,
    ClassMixin,
    AppearanceMixin
)
from .utils import inject, attr

__all__ = [
    'Icon',
    'Separator' ,
    'Spinner'
]


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

        return f'''
            <i {attr('id', self.identifier)}
                {attr('class', self.classes)}>
            </i>
        '''


class Separator(WebComponent):
    """A horizontal line separator."""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return '<hr/>'


class Spinner(WebComponent, ClassMixin, AppearanceMixin):
    """A spinner icon."""

    def __str__(self):
        self.add_classes('spinner')

        if self._category is not None:
            self.add_classes('text-%s' % self._category)

        return f'''
            <span {attr('id', self.identifier)}
                {attr('class', self.classes)}>
            </span>'''