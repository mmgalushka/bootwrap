"""
An anchor.
"""

import warnings

from .base import (
    WebComponent,
    ClassMixin,
    ActionMixin,
    AppearanceMixin,
    Action
)
from .panel import Panel
from .dialog import Dialog 
from .utils import attr, inject

__all__ = [ 'Anchor' ]


class Anchor(WebComponent, ClassMixin, ActionMixin, AppearanceMixin):
    """A web-component for an anchor.
    
    Args:
        inner (obj): The object wrapped by an anchor (default=None).
        role (obj): The anchor role. This parameter is not used in a typical
            scenario. It usually set by other web-components, which is using
            the anchor to introduce a specific action (default=None).
    """
    def __init__(self, inner=None, role=None):
        super().__init__()
        self.__inner = inner
        self.__role = role

    def __str__(self):
        name = None
        if isinstance(self.__inner, WebComponent):
            name = self.__inner.identifier

        if self._category is not None:
            self.add_classes(f'text-{self._category}')

        if self._action == Action.LINK:
            if isinstance(self._target, WebComponent):
                href = f'#{self._target.identifier}'
            else: # type(target) == str
                href = self._target

            return f'''
                <a {attr("id", self.identifier)}
                    {attr("class", self.classes)}
                    {attr("href", href)}
                    {attr("role", self.__role)}>
                    {inject(self.__inner)}
                </a>
            '''
        elif self._action == Action.TOGGLE:
            if self.__role:
                warnings.warn(
                    'When you use the anchor toggle-function it is advisable '
                    'to avoid of setting the role-parameter. Your role setting '
                    'will overwrite the internally defined role. is may cause '
                    'faulty anchor behaviour.', category=RuntimeWarning
                )

            if isinstance(self._target, Panel):
                return f'''
                    <a {attr("id", self.identifier)}
                        {attr("class",self.classes)}
                        {attr("href", f'#{self._target.identifier}')}
                        {attr("data-toggle", "tab")}
                        {attr("role", self.__role or 'tab')}>
                        {inject(self.__inner)}
                    </a>
                '''
            elif isinstance(self._target, Dialog):
                return f'''
                    <a {attr("id", self.identifier)}
                        {attr("class",self.classes)}
                        {attr("href", f'#{self._target.identifier}')}
                        {attr("data-toggle", "modal")}
                        {attr("role", self.__role or 'modal')}>
                        {inject(self.__inner)}
                    </a>
                '''
            else:
                raise TypeError(
                    'The toggle operation cannot be applied to the '
                    f'{type(self._target)} web-component;',
                )
        elif self._action == Action.COLLAPSE:
            return f'''
                <a {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    {attr("href", f'#{self._target.identifier}')}
                    data-toggle="collapse"
                    data-target="#{self._target.identifier}">
                    {inject(self.__inner)}
                </a>
            '''
        elif  self._action == Action.DISMISS:
            return f'''
                <a {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    {attr("href", f'#')}
                    data-dismiss="modal">
                    {inject(self.__inner)}
                </a>
            '''
        elif self._action == Action.SUBMIT:
            warnings.warn(
                'Avoid using an anchor for performing submit action and use '
                'a button instead. If you still decided to use anchor, the '
                'rendering script will forcefully replace it with a button.',
                category=RuntimeWarning
            )

            self.add_classes('btn')
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    type="submit">
                    {inject(self.__inner)}
                </button>
            '''
        else:
            return f'''
                <a {attr("id", self.identifier)}
                    {attr("name", name)}
                    {attr("class", self.classes)}
                    {attr("role", self.__role)}>
                    {inject(self.__inner)}
                </a>
            '''
