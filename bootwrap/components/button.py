"""
A button.
"""

from .base import (
    WebComponent,
    ClassMixin,
    ActionMixin,
    AppearanceMixin,
    OutlineMixin,
    AvailabilityMixin,
    Action
)
from .utils import attr, inject

__all__ = [ 'Button' ]


class Button(WebComponent, ClassMixin, ActionMixin, AppearanceMixin, OutlineMixin, AvailabilityMixin):
    """A web-component for a button.

    Args:
        name (str): The button name.
    """
    def __init__(self, name):
        super().__init__()
        self.__name = name

    def __str__(self):
        classes = 'btn'

        if self._category:
            if self._border:
                classes += f' btn-outline-{self._category}'
            else:
                classes += f' btn-{self._category}'

        if self.classes:
            classes += f' {self.classes}'

        if self._action == Action.LINK:
            if self._disabled:
                classes += ' disabled'
            
            if isinstance(self._target, WebComponent):
                href = f'#{self._target.identifier}'
            else: # type(target) == str
                href = self._target
                
            return f'''
                <a {attr('id', self.identifier)}
                    {attr('class', classes)}
                    {attr('href', href)}
                    role="button">
                    {self.__name}
                </a>
            '''
        elif self._action == Action.TOGGLE:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    type="button"
                    data-toggle="modal"
                    data-target="#{self._target.identifier}"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        elif self._action == Action.COLLAPSE:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    type="button"
                    data-toggle="collapse"
                    data-target="#{self._target.identifier}"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        elif  self._action == Action.DISMISS:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    type="button"
                    data-dismiss="modal"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        elif self._action == Action.SUBMIT:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    type="submit"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        else:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', classes)}
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''

