"""
A form with input elements.
"""

from abc import ABC, abstractclassmethod

from .base import WebComponent, ClassMixin, AvailabilityMixin
from .utils import attr, inject


class Form(WebComponent, ClassMixin):
    """A web-component for a form.

    Args:
        components (tuple): The form components.
    """
    def __init__(self, *components):
        super().__init__()
        self.__components = components
        self.__href = None

    def on_submit(self, href):
        """Sets the submit URL, for the POST request.

        Args:
            href (str): The URL for submitting the form.

        Return:
            itself
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
            self
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

    Args:
        label (str): The input label.
        name (str): The input name.
        checked (bool): The check box checked (default=False)
    """
    def __init__(self, label, name, checked=False):
        super().__init__(label, name)
        self.__checked = checked

    def label_on_top(self):
        raise AssertionError(
            'This "label_on_top" function is not used in '
            '<class "CheckboxInput">'
        )

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

    Args:
        label (str): The input label
        name (str): The input name.
        value (str): The input value (default=None).
        placeholder (str): The input placeholder (default=None).
    """
    def __init__(self, label, name, value=None, placeholder=None):
        super().__init__(label, name, value, placeholder)
        self._type = 'text'

    def with_multirows(self, n):
        """Sets the number of rows.

        Args:
            n (int): The number of rows to set.

        Returns:
            itself
        """
        self._rows = n
        return self

    def for_email(self):
        """Configuring input for entering email.

        Returns:
            itself
        """
        self._type = 'email'
        return self

    def for_password(self):
        """Configuring input for entering password.

        Returns:
            itself
        """
        self._type = 'password'
        return self


class NumericInput(Freehand):
    """A numeric input.

    Args:
        label (str): The input label
        name (str): The input name.
        value (obj): The input value (default=None).
        placeholder (str): The input placeholder (default=None).
    """
    def __init__(self, label, name, value=None, placeholder=None):
        super().__init__(label, name, value, placeholder)
        self._type = 'number'


class SelectInput(Input):
    """A select input.

    Args:
        label (str): The input label
        name (str): The input name.
        value (str): The input value (default=None).
        options (tuple): The input options (default=None).
    """
    def __init__(self, label, name, value=None, options=None):
        super().__init__(label, name)
        self.__value = value
        self.__options = options
        self.__radio = False

    class Option(WebComponent):
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
        """Makes selection in a for of radio buttons.

        Returns:
            itself
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
        value (obj): The input value (default=None).
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

    Args:
        label (str): The input label
        name (str): The input name.
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
