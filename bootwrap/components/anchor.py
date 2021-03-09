"""
An anchor.
"""

import warnings

from .base import (
    WebComponent,
    ClassMixin,
    AppearanceMixin,
    Action
)
from .panel import Panel
from .utils import attr, inject

__all__ = [ 'Anchor' ]


class Anchor(WebComponent, ClassMixin, AppearanceMixin):
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
        self.__action = None
        self.__target = None

    def link(self, href):
        """Links to the web-resource.

        Args:
            href (WebComponent): The URL of the page the link goes to.
        
        Returns:
            self
        """
        self.__action = Action.LINK
        self.__target = href
        # if isinstance(href, str):
        #     self.__target = href
        # else:
        #     raise TypeError(
        #         f'Anchor hyper-link must be <class "str">, but got: {type(href)};',
        #     )
        return self

    def toggle(self, target):
        """Toggles an other web-component.

        Args:
            target (WebComponent): The web-component to toggle.
        
        Returns:
            self
        """
        self.__action = Action.TOGGLE
        if isinstance(target, WebComponent):
            self.__target = target
        else:
            raise TypeError(
                f'Anchor hyper-link must be <class "WebComponent">, but got: {type(target)};',
            )
        return self

    def __str__(self):
        name = None
        if isinstance(self.__inner, WebComponent):
            name = self.__inner.identifier

        if self._category is not None:
            self.add_classes(f'text-{self._category}')

        if self.__action == Action.LINK:
            if isinstance(self.__target, WebComponent):
                href = f'#{self.__target.identifier}'
            else:
                href = self.__target
            return f'''
                <a {attr("id", self.identifier)}
                    {attr("class", self.classes)}
                    {attr("href", href)}
                    {attr("role", self.__role)}>
                    {inject(self.__inner)}
                </a>
            '''
        elif self.__action == Action.TOGGLE:
            if self.__role:
                warnings.warn(
                    'When you call the "Anchor" toggle-function it is advisable '
                    'not to set the role-parameter prior to it. Your role setting '
                    'will overwrite the internally defined role. This may affect '
                    'anchor behaviour. ', category=RuntimeWarning
                )

            if isinstance(self.__target, Panel):
                return f'''
                    <a {attr("id", self.identifier)}
                        {attr("class",self.classes)}
                        {attr("href", f'#{self.__target.identifier}')}
                        {attr("data-toggle", "tab")}
                        {attr("role", self.__role or 'tab')}>
                        {inject(self.__inner)}
                    </a>
                '''
            else:
                raise TypeError(
                    f'The toggle operation cannot be applied to the {type(self.__target)} object;',
                )
        else:
            return f'''
                <a {attr("id", self.identifier)}
                    {attr("name", name)}
                    {attr("class", self.classes)}
                    {attr("role", self.__role)}>
                    {inject(self.__inner)}
                </a>
            '''
