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
from .panel import Panel
from .dialog import Dialog
from .utils import attr, inject


class Button(WebComponent, ClassMixin, ActionMixin, AppearanceMixin,
             OutlineMixin, AvailabilityMixin):
    """A web-component for a button.

    Without applying a stylized method `Button` will be appearing very
    similar to the `Anchor`.

    Args:
        name (str): The button name.

    Example:
        Button('Google Search').link('https://www.google.com/')

    Demo:
        from bootwrap import Button
        output = Button('Google Search').link('https://www.google.com/')
    """
    def __init__(self, name):
        super().__init__()
        self.__name = name

    def __str__(self):
        self.add_classes('btn')

        if self._category:
            if self._border:
                self.add_classes(f'btn-outline-{self._category}')
            else:
                self.add_classes(f'btn-{self._category}')

        if self._menu:
            for item in self._menu:
                item.add_classes('dropdown-item')

            if self.__name == '...':
                self.add_classes('fas fa-ellipsis-v')
                host = f'''
                    <i {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        style="cursor: pointer"
                        data-toggle="dropdown"
                        onclick="return false;">
                    </i>
                '''
            else:
                self.add_classes('dropdown-toggle')
                host = f'''
                    <button {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        type="button"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                        onclick="return false;">
                        {self.__name}
                    </button>
                '''
            return f'''
                <div class="btn-group">
                    {host}
                    <div class="dropdown-menu dropdown-menu-right">
                        {inject(*self._menu)}
                    </div>
                </div>
            '''
        elif self._action == Action.LINK:
            if self._disabled:
                self.add_classes('disabled')

            # At this point, we only need to check whether the specified
            # target is a web-component or a string. The ActionMixin makes
            # sure that a user can specify only these two types.
            if isinstance(self._target, WebComponent):
                href = f'#{self._target.identifier}'
            else:  # type(target) == str
                href = self._target

            return f'''
                <a {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    {attr('href', href)}
                    role="button">
                    {self.__name}
                </a>
            '''
        elif self._action == Action.TOGGLE:
            if isinstance(self._target, Panel):
                return f'''
                    <button {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        type="button"
                        data-toggle="collapse"
                        data-target="#{self._target.identifier}"
                        onclick="return false;"
                        {attr('disabled', self._disabled)}>
                        {self.__name}
                    </button>
                '''
            elif isinstance(self._target, Dialog):
                return f'''
                    <button {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        type="button"
                        data-toggle="modal"
                        data-target="#{self._target.identifier}"
                        onclick="return false;"
                        {attr('disabled', self._disabled)}>
                        {self.__name}
                    </button>
                '''
            raise TypeError(
                'The toggle operation cannot be applied to the '
                f'{type(self._target)} web-component;',
            )
        elif self._action == Action.DISMISS:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    type="button"
                    data-dismiss="modal"
                    onclick="return false;"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        elif self._action == Action.SUBMIT:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    type="submit"
                    onclick="return false;"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
        else:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    onclick="return false;"
                    {attr('disabled', self._disabled)}>
                    {self.__name}
                </button>
            '''
