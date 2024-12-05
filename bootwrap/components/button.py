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
from .icon import Icon
from .utils import attr, inject


class Button(WebComponent, ClassMixin, ActionMixin, AppearanceMixin,
             OutlineMixin, AvailabilityMixin):
    """A web component for a button.

    Without applying a stylized method `Button` will be appearing very
    similar to the `Anchor`.

    Args:
        name (str): The button name.

    Example:
        from bootwrap import Button
        output = Button('Google Search').link('https://www.google.com/')
    """

    def __init__(self, name):
        super().__init__()
        self.__name = name
        self.__icon = None
        self.__right_side = None

    def with_icon(self, icon, right_side = False):
        """Makes button with icon.

        Args:
            icon (Icon):
                The icon to add on button.
            right_side (bool):
                If `True` the icon is placed on the right side of the button
                name and `False` on the right side accordingly. 

        Returns:
            self
        
        Example:
            from bootwrap import Button, Icon, Panel
            ico_left = Icon("fa-solid fa-arrow-left")
            btn_left = Button("Left").with_icon(ico_left).as_primary()
            ico_right = Icon("fa-solid fa-arrow-right")
            btn_right = Button("Right").with_icon(ico_right, True).as_primary()
            output = Panel(btn_left, btn_right)
        """
        self.__icon = icon
        self.__right_side = right_side
        return self


    def __str__(self):
        self.add_classes('btn')

        if self._category:
            if self._border:
                self.add_classes(f'btn-outline-{self._category}')
            else:
                self.add_classes(f'btn-{self._category}')

        button_name = self.__name
        if self.__icon:
            if self.__right_side:
                button_name = f"{self.__name}{inject(self.__icon)}"
            else:
                button_name = f"{inject(self.__icon)}{self.__name}"   
        

        if self._menu:
            for item in self._menu:
                item.add_classes('dropdown-item')

            if self.__name == '...':
                self.add_classes('fas fa-ellipsis-v')
                host = f'''
                    <i {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        style="cursor: pointer"
                        data-bs-toggle="dropdown"
                        onclick="return false;">
                    </i>
                '''
            else:
                self.add_classes('dropdown-toggle')
                host = f'''
                    <button {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        type="button"
                        data-bs-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                        onclick="return false;">
                        {button_name}
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
            # target is a web component or a string. The ActionMixin makes
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
                    {button_name}
                </a>
            '''
        elif self._action == Action.TOGGLE:
            if isinstance(self._target, Panel):
                data_toggle = 'tab'
                if self._target.classes is not None:
                    if 'collapse' in self._target.classes:
                        data_toggle = 'collapse'

                return f'''
                    <button {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        type="button"
                        data-bs-toggle="{data_toggle}"
                        data-bs-target="#{self._target.identifier}"
                        onclick="return false;"
                        {attr('disabled', self._disabled)}>
                        {button_name}
                    </button>
                '''
            elif isinstance(self._target, Dialog):
                return f'''
                    <button {attr('id', self.identifier)}
                        {attr('class', self.classes)}
                        type="button"
                        data-bs-toggle="modal"
                        data-bs-target="#{self._target.identifier}"
                        onclick="return false;"
                        {attr('disabled', self._disabled)}>
                        {button_name}
                    </button>
                '''
            raise TypeError(
                'The toggle operation cannot be applied to the '
                f'{type(self._target)} web component;',
            )
        elif self._action == Action.DISMISS:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    type="button"
                    data-bs-dismiss="modal"
                    onclick="return false;"
                    {attr('disabled', self._disabled)}>
                    {button_name}
                </button>
            '''
        elif self._action == Action.SUBMIT:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    type="submit"
                    {attr('disabled', self._disabled)}>
                    {button_name}
                </button>
            '''
        else:
            return f'''
                <button {attr('id', self.identifier)}
                    {attr('class', self.classes)}
                    onclick="return false;"
                    {attr('disabled', self._disabled)}>
                    {button_name}
                </button>
            '''

class ButtonGroup(WebComponent, ClassMixin):
    """A web component for a button group.

    Group a series of buttons together on a single line or stack them in
    a vertical column.

    Args:
        *buttons (list): The list of `WebComponent`.

    Example:
        from bootwrap import Button, ButtonGroup

        button1 = Button('One').as_success()
        button2 = Button('Two').as_warning()
        button3 = Button('Three').as_danger()

        output = ButtonGroup(button1, button2, button3)
    """
    def __init__(self, *buttons):
        super().__init__()
        self.__buttons = buttons

    def __str__(self):
        self.add_classes("btn-group")
        return f'''
            <div {attr("id", self.identifier)}
                {attr("class", self.classes)}
                role="group">
                {inject(*self.__buttons)}
            </div>
        '''