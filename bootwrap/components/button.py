"""
A button.
"""

from .base import (
    WebComponent,
    ClassMixin,
    CompositeMixin,
    AppearanceMixin,
    OutlineMixin,
    AvailabilityMixin
)
from .utils import attr, inject

__all__ = [ 'Button' ]


class Button(WebComponent, CompositeMixin, ClassMixin, AppearanceMixin, OutlineMixin, AvailabilityMixin):
    """A web-component for a button.

    Args:
        name (str): The button name.
    """
    def __init__(self, name):
        super().__init__()
        self.__name = name
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

    def collapse(self, target):
        """Collapses an other web-component.

        Args:
            target (WebComponent): The web-component to collapse.

        Returns:
            self
        """
        self.__action = f'collapse:{target.identifier}'
        return self

    def dismiss(self):
        """Performes a dismiss action.

        Returns:
            self
        """
        self.__action = 'dismiss'
        return self

    def submit(self):
        """Performes a submit action.

        Returns:
            self
        """
        self.__action = 'submit'
        return self

    def __str__(self):
        classes = 'btn'

        if self._border:
            classes += f' btn-outline-{self._category}'
        else:
            classes += f' btn-{self._category}'

        if self.classes:
            classes += f' {self.classes}'

        if self.__action.startswith('toggle:'):
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    type="button"
                    data-toggle="modal"
                    data-target="#{self.__action[7:]}"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        elif self.__action.startswith('collapse:'):
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    type="button"
                    data-toggle="collapse"
                    data-target="#{self.__action[9:]}"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        elif self.__action.startswith('dismiss'):
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    type="button"
                    data-dismiss="modal"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        elif self.__action.startswith('submit'):
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    type="submit"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        else: # It can be only self.__action starts with 'href:'.
            if self._disabled:
                classes += ' disabled'
            return f'''
                <a {attr('id', self.identifier)}
                    {attr('class', classes)}
                    {attr('href', self.__action[5:])}
                    role="button">
                    {self.__name}
                </a>
            '''

