"""
A badge.
"""

from .base import WebComponent, ClassMixin, AppearanceMixin
from .utils import attr


class Badge(WebComponent, ClassMixin, AppearanceMixin):
    """A web-component for a badge.

    Args:
        label (str): The badge label.
    """
    def __init__(self, label):
        super().__init__()
        self.__label = label

    def __str__(self):
        classes = 'badge'
        if self._category:
            classes += f' badge-{self._category}'

        if self.classes:
            classes += f' {self.classes}'

        return f'''
            <span {attr("id", self.identifier)}
                {attr('class', classes)}>
                {self.__label}
            </span>
        '''
