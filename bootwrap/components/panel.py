"""
A panel.
"""

from .base import (
    WebComponent,
    CompositeMixin,
    ClassMixin
)
from .utils import attr, inject

__all__ = [ 'Panel' ]


class Panel(WebComponent, CompositeMixin, ClassMixin):
    """A web-component for a panel."""
    def __init__(self, role=None):
        super().__init__()
        self.__role = role

    def __str__(self):
        return f'''
            <div {attr("id", self.identifier)}
                {attr("class", self.classes)}
                {attr("role", self.__role)}>
                {inject(*self._components)}
            </div>
        '''