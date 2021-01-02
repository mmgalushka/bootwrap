"""
A form with input elements.
"""

from abc import ABC, abstractclassmethod

from .base import (
    WebComponent,
    ClassMixin,
    CompositeMixin,
    AvailabilityMixin
)
from .utils import attr, inject

__all__ = [ 
    'Form',
    'CheckboxInput',
    'RadioInput',
    'EmailInput',
    'PasswordInput',
    'TextInput',
    'NumericInput',
    'SelectInput', 
    'HiddenInput',
    'FileInput'
]


class Form(WebComponent, CompositeMixin, ClassMixin):
    """A web-component for a form.
    
    Args:
        action (str): The form action.
    """
    def __init__(self, action):
        super().__init__()
        self.__action = action

    def __str__(self):
        return f'''
            <form {attr('id', self.identifier)}
                {attr('action', self.__action)}
                {attr('class', self.classes)}
                method="POST"
                enctype="multipart/form-data">
                {inject(*self._components)}
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
        self._label = label
        self._name = name


class Switch(Input):
    """A switch-base input."""
    def __init__(self, label, name):
        super().__init__(label, name)
        self._checked = False

    def as_checked(self, status=True):
        """Makes a web-component checked.

        Returns:
            self
        """
        self._checked = True
        return self


class Value(Input):
    """A value-base input."""
    def __init__(self, label, name):
        super().__init__(label, name)
        self._value = None

    def with_value(self, value):
        """Sets a web-component value.

        Args:
            value (obj): The value to set.

        Returns:
            self
        """
        self._value = value
        return self


class CheckboxInput(Switch):
    """A checkbox input."""
    def __str__(self):
        label = ''
        if self._label:
            label = f'''
                <label class="form-check-label"
                    {attr('for', self.identifier)}>
                    {self._label}
                </label>
            '''

        component = f'''
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                type="checkbox" 
                class="form-check-input" 
                autocomplete="off"
                {attr('checked', self._checked)}
                {attr('disabled', self._disabled)}>
            <input {attr('name', self._name)}
                type="hidden" 
                value="off">
        '''

        self.add_classes('form-check form-check-inline')
        return f'''
            <div {attr('class', self.classes)}>
                {inject(component, label)}
            </div>
        '''


class RadioInput(Switch, Value):
    """A radio button input."""

    def __str__(self):
        label = ''
        if self._label:
            label = f'''
                <label class="form-check-label"
                    {attr('for', self.identifier)}>
                    {self._label}
                </label>
            '''

        component = f'''
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                {attr('value', self._value)}
                type="radio" 
                class="form-check-input" 
                autocomplete="off"
                {attr('checked', self._checked)}
                {attr('disabled', self._disabled)}>
            <input {attr('name', self._name)}
                type="hidden" 
                value="off">
        '''

        self.add_classes('form-check form-check-inline')
        return f'''
            <div {attr('class', self.classes)}>
                {inject(component, label)}
            </div>
        '''

class Freehand(Value):
    """A freehand value input."""
    def __init__(self, label, name):
        super().__init__(label, name)
        self._label_on_top = False

    def label_on_top(self):
        """Makes an input label showing on top.

        Returns:
            self
        """
        self._label_on_top = True
        return self

    @abstractclassmethod
    def _receiver(self):
        """A component for rendering a receiver for freehand value."""
        raise NotImplementedError()

    def __str__(self):
        if self._label:
            label_classes = None
            receiver_classes = None
            if not self._label_on_top:
                self.add_classes('row')
                label_classes = 'col-sm-2 col-form-label'
                receiver_classes = 'col-sm-10'
            return f'''
                <div {attr('class', self.classes)}>
                    <label {attr('class', label_classes)}
                        {attr('for', self.identifier)}>
                        {self._label}
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

class EmailInput(Freehand):
    """A email input.

    Args:
        label (str): The input label
        name (str): The input name.
        placeholder (str): The input placeholder (default=None).
    """
    def __init__(self, label, name, placeholder=None):
        super().__init__(label, name)
        self.__placeholder = placeholder

    def _receiver(self):
        return f'''
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                {attr('value', self._value)}
                type="email" 
                class="form-control"
                {attr('placeholder', self.__placeholder)}
                {attr('disabled', self._disabled)}>
        '''


class PasswordInput(Freehand):
    """A password input.

    Args:
        label (str): The input label
        name (str): The input name.
        placeholder (str): The input placeholder (default=None).
    """
    def __init__(self, label, name, placeholder=None):
        super().__init__(label, name)
        self.__placeholder = placeholder

    def _receiver(self):
        return f'''
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                {attr('value', self._value)}
                type="password" 
                class="form-control"
                {attr('placeholder', self.__placeholder)}
                {attr('disabled', self._disabled)}>
        '''

class TextInput(Freehand):
    """A text input.

    Args:
        label (str): The input label
        name (str): The input name.
        rows (int): The number of input (default=None).
        placeholder (str): The input placeholder (default=None).
    """
    def __init__(self, label, name,  rows=None, placeholder=None):
        super().__init__(label, name)
        self.__rows = rows
        self.__placeholder = placeholder

    def _receiver(self):
        if self.__rows:
            value = '' if self._value is None else self._value
            return f'''
                <textarea {attr('id', self.identifier)}"
                    {attr('name', self._name)} 
                    class="form-control"
                    {attr('rows', self.__rows)}
                    {attr('disabled', self._disabled)}>
                    {value}
                </textarea>
            '''
        else:
            return f'''
                <input {attr('id', self.identifier)}"
                    {attr('name', self._name)}
                    {attr('value', self._value)}
                    type="text"
                    class="form-control"
                    {attr('placeholder', self.__placeholder)}
                    {attr('disabled', self._disabled)}>
            '''

class NumericInput(Freehand):
    """A numeric input.

    Args:
        label (str): The input label
        name (str): The input name.
        placeholder (str): The input placeholder (default=None).
    """
    def __init__(self, label, name, placeholder=None):
        super().__init__(label, name)
        self.__placeholder = placeholder

    def _receiver(self):
        return f'''
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                {attr('value', self._value)}
                type="number"
                step="any"
                class="form-control"
                {attr('placeholder', self.__placeholder)}
                {attr('disabled', self._disabled)}>
        '''


class SelectInput(Value):
    """A select input.

    Args:
        label (str): The input label
        name (str): The input name.
        options (tuple): The input options.
    """
    def __init__(self, label, name, options):
        super().__init__(label, name)
        self.__options = options
        self.__label_on_top = False

    class Option():
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

    def __str__(self):
        options = []
        for option in self.__options:
            options.append(f'''
                <option {attr('value', option.value)}
                    {attr('selected', option.value == self._value)}
                    {attr('disabled', option.disabled)}>{option.name}</option>
            ''')

        component = f'''
            <select {attr('id', self.identifier)}
                {attr('name', self._name)}
                class="form-control"
                autocomplete="off"
                {attr('disabled', self._disabled)}>
                {inject(*options)}
            </select>
        '''
        if self._label:
            label_classes = None
            receiver_classes = None
            if not self.__label_on_top:
                self.add_classes('row')
                label_classes = 'col-sm-2 col-form-label'
                receiver_classes = 'col-sm-10'
            return f'''
                <div {attr('class', self.classes)}>
                    <label {attr('class', label_classes)}
                        {attr('for', self.identifier)}>
                        {self._label}
                    </label>
                    <div {attr('class', receiver_classes)}>
                        {inject(component)}
                    </div>
                </div>
            '''
        return f'''
            <div {attr('class', self.classes)}>
                {inject(component)}
            </div>
        '''


class HiddenInput(Value):
    """A hidden input.

    Args:
        name (str): The input name.
    """
    def __init__(self, name):
        super().__init__(None, name)

    def __str__(self):
        return f'''
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                {attr('value', self._value)}
                type="hidden">
        '''


class FileInput(Input):
    """A file input.

    Args:
        label (str): The input label
        name (str): The input name.
    """
    def __init__(self, label, name):
        super().__init__(label, name)
        self.__label_on_top = False

    def label_on_top(self):
        """Makes an input label showing on top.

        Returns:
            self
        """
        self.__label_on_top = True
        return self


    def __str__(self):
        browse_button_class = 'btn btn-secondary'
        if self._disabled:
            browse_button_class += ' disabled'

        component = f'''
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
                        {attr('disabled', self._disabled)}>
                </div>
            </div>
        '''

        if self._label:
            label_classes = None
            receiver_classes = None
            if not self.__label_on_top:
                self.add_classes('row')
                label_classes = 'col-sm-2 col-form-label'
                receiver_classes = 'col-sm-10'
            return f'''
                <div {attr('class', self.classes)}>
                    <label {attr('class', label_classes)}
                        {attr('for', self.identifier)}>
                        {self._label}
                    </label>
                    <div {attr('class', receiver_classes)}>
                        {component}
                    </div>
                </div>
            '''
        return f'''
            <div {attr('class', self.classes)}>
                {component}
            </div>
        '''