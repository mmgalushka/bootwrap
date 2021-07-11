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


class Anchor(WebComponent, ClassMixin, ActionMixin, AppearanceMixin):
    """A web component for an anchor.

    The `Anchor` component is used for creating a hyperlink to pages, files,
    email addresses, locations on the same page, or other web-resources
    defined by a URL address. The <i>Bootwrap</i> also uses the `Anchor` in
    conjunction with other components, for example, in creating a navigation
    menu.

    Args:
        inner (str|WebComponent): The object wrapped by the anchor.

    Example:
        Anchor('Google Search').link('https://www.google.com/')

    Demo:
        from bootwrap import Anchor
        output = Anchor('Google Search').link('https://www.google.com/')
    """

    def __init__(self, inner=None):
        super().__init__()
        self._inner = inner

    def __str__(self):
        name = None
        if isinstance(self._inner, WebComponent):
            name = self._inner.identifier

        if self._category is not None:
            self.add_classes(f'text-{self._category}')

        if self._action == Action.LINK:
            if isinstance(self._target, WebComponent):
                href = f'#{self._target.identifier}'
            else:  # type(target) == str
                href = self._target

            return f'''
                <a {attr("id", self.identifier)}
                    {attr("class", self.classes)}
                    {attr("href", href)}>
                    {inject(self._inner)}
                </a>
            '''
        elif self._action == Action.TOGGLE:
            if isinstance(self._target, Panel):
                data_toggle = 'tab'
                role = 'tab'
                if self._target.classes is not None:
                    if 'collapse' in self._target.classes:
                        data_toggle = 'collapse'
                        role = 'collapse'

                return f'''
                    <a {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        {attr("href", f'#{self._target.identifier}')}
                        {attr("data-toggle", data_toggle)}
                        {attr("role", role)}
                        data-target="#{self._target.identifier}">
                        {inject(self._inner)}
                    </a>
                '''
            elif isinstance(self._target, Dialog):
                return f'''
                    <a {attr("id", self.identifier)}
                        {attr("class",self.classes)}
                        {attr("href", f'#{self._target.identifier}')}
                        {attr("data-toggle", "modal")}
                        {attr("role", 'modal')}>
                        {inject(self._inner)}
                    </a>
                '''
            raise TypeError(
                'The toggle operation cannot be applied to the '
                f'{type(self._target)} web component;',
            )
        elif self._action == Action.DISMISS:
            return f'''
                <a {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    {attr("href", f'#')}
                    data-dismiss="modal">
                    {inject(self._inner)}
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
                    {inject(self._inner)}
                </button>
            '''
        else:
            return f'''
                <a {attr("id", self.identifier)}
                    {attr("name", name)}
                    {attr("class", self.classes)}>
                    {inject(self._inner)}
                </a>
            '''
