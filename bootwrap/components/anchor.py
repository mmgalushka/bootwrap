"""
An anchor.
"""

from .base import (
    WebComponent,
    CompositeMixin,
    ClassMixin,
    AppearanceMixin
)
from .utils import attr, inject

__all__ = [ 'Anchor' ]


class Anchor(WebComponent, CompositeMixin, ClassMixin, AppearanceMixin):
    """A web-component for an anchor.
    
    Args:
        name (str): The anchor name.
    """
    def __init__(self, name, role=None):
        super().__init__()
        self.__name = name
        self.__role = role
        self.__action = 'href:#' 

    def link(self, href):
        """Links to the web-resource.

        Args:
            href (WebComponent): The URL of the page the link goes to.
        
        Returns:
            self
        """
        self.__action = f'href:{href}'
        return self

    def toggle(self, target):
        """Toggles an other web-component.

        Args:
            target (WebComponent): The web-component to toggle.
        
        Returns:
            self
        """
        self.__action = f'toggle:{target.identifier}'
        return self

    def __str__(self):
        if self._category is None:
            classes = ''
        else:
            classes = f'text-{self._category}'

        if self.classes:
            classes += f' {self.classes}'

        if self.__action.startswith('toggle:'):
            return f'''
                <a {attr("id", self.identifier)}
                    {attr("class", classes)}
                    {attr("href", f'#{self.__action[7:]}')}
                    {attr("data-toggle", "tab")}
                    {attr("role", self.__role)}>
                    {self.__name}
                </a>
            '''
        else: # It can be only self.__action starts with 'href:'.
            return f'''
                <a {attr("id", self.identifier)}
                    {attr("class", classes)}
                    {attr("href", self.__action[5:])}
                    {attr("role", self.__role)}>
                    {self.__name}
                </a>
            '''
