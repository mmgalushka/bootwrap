"""
A form with input elements.
"""

from abc import ABC, abstractclassmethod

from .base import WebComponent, ClassMixin, AvailabilityMixin
from .utils import attr, inject


class Form(WebComponent, ClassMixin):
    """A web-component for a form.

    Use the `on_submit(href)` function to specify URL where entered
    information should to be sent for processing.

    Args:
        *components (list): The list of `WebComponent` representing form
            elements for input and action.

    Example:
        from bootwrap import Form

        Form(
            # here should be an enumeration  of
            # input components and actions
            ...
        ).on_submit('go/to/this/url')
    """
    def __init__(self, *components):
        super().__init__()
        self.__components = components
        self.__href = None

    def on_submit(self, href):
        """Sets the submit URL, for the POST request.

        Args:
            href (str): The URL for submitting the form.

        Returns:
            self (Form): The instance of this class.

        Example:
            from bootwrap import Form

            Form(...).on_submit('go/to/this/url')
        """
        self.__href = href
        return self

    def __str__(self):
        return f'''
            <form {attr('id', self.identifier)}
                {attr('action', self.__href)}
                {attr('class', self.classes)}
                method="POST"
                enctype="multipart/form-data">
                {inject(*self.__components)}
            </form>
        '''


class Input(ABC, WebComponent, ClassMixin, AvailabilityMixin):
    """A base input.

    Args:
        label (str): The input label.
        name (str): The input name.
    """
    def __init__(self, label, name):
        super().__init__()
        self.__label = label
        self._name = name
        self.__label_on_top = False

    def label_on_top(self):
        """Makes an input label showing on top.

        Returns:
            self (Input): The instance of this class.
        """
        self.__label_on_top = True
        return self

    @abstractclassmethod
    def _receiver(self):
        """A component for rendering a receiver."""

    def __str__(self):
        self.add_classes('form-group')

        if self.__label:
            label_classes = None
            receiver_classes = None
            if not self.__label_on_top:
                self.add_classes('row')
                label_classes = \
                    'col-sm-2 col-form-label d-flex align-items-center'
                receiver_classes = \
                    'col-sm-10 d-flex align-items-center'
            return f'''
                <div {attr('class', self.classes)}>
                    <label {attr('class', label_classes)}
                        {attr('for', self.identifier)}>
                        {self.__label}
                    </label>
                    <div {attr('class', receiver_classes)}>
                        {self._receiver()}
                    </div>
                </div>
            '''
        return f'''
            <div {attr('class', self.classes)}>
                {self._receiver()}
            </div>
        '''


class CheckboxInput(Input):
    """A checkbox input.

    Use the `as_disabled()` function to prevent the user from changing
    status of the `CheckboxInput` component.

    Args:
        label (str): The input label.
        name (str): The input name.
        checked (bool): The check box status.

    Example:
        from bootwrap import Form, CheckboxInput

        Form(
            CheckboxInput('One', 'opt1'),
            CheckboxInput('Two', 'opt2', True),
            CheckboxInput('Three', 'opt3').as_disabled()
        )

    Demo:
        from bootwrap import Form, CheckboxInput

        output = Form(
            CheckboxInput('One', 'opt1'),
            CheckboxInput('Two', 'opt2', True),
            CheckboxInput('Three', 'opt3').as_disabled()
        )
    """
    def __init__(self, label, name, checked=False):
        super().__init__(label, name)
        self.__checked = checked

    def _receiver(self):
        return f'''
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                type="checkbox"
                class="form-check-input"
                autocomplete="off"
                {attr('checked', self.__checked)}
                {attr('disabled', self._disabled)}/>
        '''


class Freehand(Input):
    """A freehand value input.

    Args:
        label (str): The input label
        name (str): The input name.
        value (str): The input value.
        placeholder (str): The input placeholder.
    """
    def __init__(self, label, name, value, placeholder):
        super().__init__(label, name)
        self.__value = value
        self.__placeholder = placeholder
        self._type = None
        self._rows = 1

    def _receiver(self):
        if self._rows > 1:
            assert self._type == 'text',\
                f'The <class "TextInput"> of type "{self._type}" ' +\
                f'can not have {self._rows} rows.'
            return f'''
                <textarea {attr('id', self.identifier)}
                    {attr('name', self._name)}
                    class="form-control"
                    {attr('rows', self._rows)}
                    {attr('disabled', self._disabled)}>
                    {self.__value or ''}
                </textarea>
            '''
        else:
            return f'''
                <input {attr('id', self.identifier)}
                    {attr('name', self._name)}
                    {attr('value', self.__value)}
                    type="{self._type}"
                    class="form-control"
                    {attr('placeholder', self.__placeholder)}
                    {attr('disabled', self._disabled)}/>
            '''


class TextInput(Freehand):
    """A text input.

    Use the `as_disabled()` function to prevent the user from entering data
    to the `TextInput` component.

    Args:
        label (str): The input label
        name (str): The input name.
        value (str): The input value.
        placeholder (str): The input placeholder.

    Example:
        from bootwrap import Form, TextInput

        Form(
            TextInput('Text1', 'text'),
            TextInput('Text2', 'text', placeholder='type here'),
            TextInput('Text3', 'text', 'Hello World!'),
            TextInput('Text4', 'text').as_disabled()
        )
    Demo:
        from bootwrap import Form, TextInput

        output = Form(
            TextInput('Text1', 'text'),
            TextInput('Text2', 'text', placeholder='type here'),
            TextInput('Text3', 'text', 'Hello World!'),
            TextInput('Text4', 'text').as_disabled()
        )
    """
    def __init__(self, label, name, value=None, placeholder=None):
        super().__init__(label, name, value, placeholder)
        self._type = 'text'

    def with_multirows(self, n):
        """Sets the number of rows.

        Args:
            n (int): The number of rows to set.

        Returns:
            self (TextInput): The instance of this class.

        Example:
            from bootwrap import Form, TextInput

            Form(
                TextInput('Text', 'text').with_multirows(3)
            )
        Demo:
            from bootwrap import Form, TextInput

            output = Form(
                TextInput('Text', 'text').with_multirows(3)
            )
        """
        self._rows = n
        return self

    def for_email(self):
        """Configuring input for entering email.

        Returns:
            self (TextInput): The instance of this class.

        Example:
            from bootwrap import Form, TextInput

            Form(
                TextInput('Email', 'email', 'my@email.com').for_email()
            )
        Demo:
            from bootwrap import Form, TextInput

            output = Form(
                TextInput('Email', 'email', 'my@email.com').for_email()
            )
        """
        self._type = 'email'
        return self

    def for_password(self):
        """Configuring input for entering password.

        Returns:
            self (TextInput): The instance of this class.

        Example:
            from bootwrap import Form, TextInput

            Form(
                TextInput('Password', 'password', '********').for_password()
            )

        Demo:
            from bootwrap import Form, TextInput

            output = Form(
                TextInput('Password', 'password', '********').for_password()
            )
        """
        self._type = 'password'
        return self


class NumericInput(Freehand):
    """A numeric input.

    Use the `as_disabled()` function to prevent the user from entering data
    to the `NumericInput` component.

    Args:
        label (str): The input label
        name (str): The input name.
        value (obj): The input value.
        placeholder (str): The input placeholder.

    Example:
        from bootwrap import Form, TextInput

        Form(
            NumericInput('Number1', 'number'),
            NumericInput('Number2', 'number', placeholder='type here'),
            NumericInput('Number3', 'number', 123),
            NumericInput('Number4', 'number').as_disabled()
        )
    Demo:
        from bootwrap import Form, NumericInput

        output = Form(
            NumericInput('Number1', 'number'),
            NumericInput('Number2', 'number', placeholder='type here'),
            NumericInput('Number3', 'number', 123),
            NumericInput('Number4', 'number').as_disabled()
        )
    """
    def __init__(self, label, name, value=None, placeholder=None):
        super().__init__(label, name, value, placeholder)
        self._type = 'number'


class SelectInput(Input):
    """A select input.

    Use the `as_disabled()` function to prevent the user from entering data
    to the `SelectInput` component.

    Args:
        label (str): The input label
        name (str): The input name.
        value (str): The input value.
        options (tuple): The input options.

    Example:
        from bootwrap import Form, SelectInput

        options = [
            SelectInput.Option('One', 1),
            SelectInput.Option('Two', 2),
            SelectInput.Option('Three', 3, disabled=True)
        ]

        Form(
            SelectInput('Selector1', 'choice', 2, options)
            SelectInput('Selector2', 'choice', 2, options).as_disabled()
        )

    Demo:
        from bootwrap import Form, SelectInput

        options = [
            SelectInput.Option('One', 1),
            SelectInput.Option('Two', 2),
            SelectInput.Option('Three', 3, disabled=True)
        ]

        output = Form(
            SelectInput('Selector1', 'choice', 2, options),
            SelectInput('Selector2', 'choice', 2, options).as_disabled()
        )
    """
    def __init__(self, label, name, value=None, options=None):
        super().__init__(label, name)
        self.__value = value
        self.__options = options
        self.__radio = False

    class Option(WebComponent):
        """An option used by `SelectInput`.

        Args:
            name (str): The option name.
            value (str): The option value value.
            disabled (bool): `True` makes the option disabled (in other words
                user will not be able to choose this option).
        """
        def __init__(self, name, value, disabled=False):
            super().__init__()
            self.__name = name
            self.__value = value
            self.__disabled = disabled

        @property
        def name(self):
            return self.__name

        @property
        def value(self):
            return self.__value

        @property
        def disabled(self):
            return self.__disabled

    def as_radio(self):
        """Makes selection in a form of radio buttons.

        Returns:
            self (SelectInput): The instance of this class.

        Example:
            from bootwrap import Form, SelectInput

            options = [
                SelectInput.Option('One', 1),
                SelectInput.Option('Two', 2),
                SelectInput.Option('Three', 3, disabled=True)
            ]

            Form(
                SelectInput('Selector', 'choice', 2, options).as_radio()
            )

        Demo:
            from bootwrap import Form, SelectInput

            options = [
                SelectInput.Option('One', 1),
                SelectInput.Option('Two', 2),
                SelectInput.Option('Three', 3, disabled=True)
            ]

            output = Form(
                SelectInput('Selector', 'choice', 2, options).as_radio()
            )
        """
        self.__radio = True
        return self

    def _receiver(self):
        if self.__radio:
            options = []
            for option in self.__options:
                options.append(f'''
                    <div class="form-check mr-3">
                        <input {attr('id', option.identifier)}
                            {attr('name', self._name)}
                            {attr('value', option.value)}
                            type="radio"
                            class="form-check-input"
                            autocomplete="off"
                            {attr('checked', option.value == self.__value)}
                            {attr('disabled', option.disabled)}/>
                        <label class="form-check-label mr-1"
                            {attr('for', option.identifier)}>
                            {option.name}
                        </label>
                    </div>
                ''')
            return inject(*options)
        else:
            options = []
            for option in self.__options:
                options.append(f'''
                    <option {attr('id', option.identifier)}
                        {attr('value', option.value)}
                        {attr('selected', option.value == self.__value)}
                        {attr('disabled', option.disabled)}>
                        {option.name}
                    </option>
                ''')

            return f'''
                <select {attr('id', self.identifier)}
                    {attr('name', self._name)}
                    class="form-control"
                    autocomplete="off"
                    {attr('disabled', self._disabled)}>
                    {inject(*options)}
                </select>
            '''


class HiddenInput(Input):
    """A hidden input.

    Args:
        name (str): The input name.
        value (obj): The input value.

    Example:
        from bootwrap import Form, SelectInput

        Form(
            HiddenInput('token', '123')
        )
    """
    def __init__(self, name, value=None):
        super().__init__(None, name)
        self.__value = value

    def _receiver(self):
        return f'''
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                {attr('value', self.__value)}
                type="hidden"/>
        '''

    def __str__(self):
        return self._receiver()


class FileInput(Input):
    """A file input.

    Use the `as_disabled()` function to prevent the user from entering data
    to the `FileInput` component.

    Args:
        label (str): The input label
        name (str): The input name.

    Example:
        from bootwrap import Form, FileInput

        output = Form(
            FileInput('File', 'file'),
            FileInput('File', 'file').as_disabled()
        )

    Demo:
        from bootwrap import Form, FileInput

        output = Form(
            FileInput('File', 'file'),
            FileInput('File', 'file').as_disabled()
        )
    """
    def __init__(self, label, name):
        super().__init__(label, name)

    def _receiver(self):
        browse_button_class = 'btn btn-secondary'
        if self._disabled:
            browse_button_class += ' disabled'

        return f'''
            <div class="input-group">
                <span class="form-control input-group-append"></span>
                <div class="input-group-append">
                    <span class="{browse_button_class}"
                        onclick="$(this).parent().find('input[type=file]').click();">
                        Browse
                    </span>
                    <input {attr('id', self.identifier)}
                        {attr('name', self._name)}
                        onchange="$(this).parent().parent().find('.form-control').html($(this).val().split(/[\\|/]/).pop());"
                        style="display: none;"
                        type="file"
                        {attr('disabled', self._disabled)}/>
                </div>
            </div>
        '''
