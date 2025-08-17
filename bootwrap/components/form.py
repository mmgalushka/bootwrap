"""
A form with input elements.
"""

from abc import ABC, abstractmethod
from textwrap import dedent
from html import escape
from json import dumps

from .base import (
    WebComponent,
    ClassMixin,
    AvailabilityMixin,
    AppearanceMixin,
    OutlineMixin,
)
from .utils import attr, tag, inject
from .text import Text  #


class Form(WebComponent, ClassMixin):
    """A web component for a form.

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
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form

            Form(...).on_submit('go/to/this/url')
        """
        self.__href = href
        return self

    def __str__(self):
        return f"""
            <form {attr('id', self.identifier)}
                {attr('action', self.__href)}
                {attr('class', self.classes)}
                method="POST"
                enctype="multipart/form-data">
                {inject(*self.__components)}
            </form>
        """


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
        self._tip = None
        self.__label_on_top = False

    def with_tip(self, tip):
        self._tip = tip
        return self

    def label_on_top(self):
        """Makes an input label showing on top.

        Returns:
            obj (self): The instance of this class.
        """
        self.__label_on_top = True
        return self

    @abstractmethod
    def _receiver(self):
        """A component for rendering a receiver."""

    def __str__(self):
        self.add_classes("form-group")

        tips_html = ""
        if hasattr(self, "_tip") and self._tip:
            tips_html = f"""
                <small class="form-text text-secondary" style="font-size: 0.75em;">
                    {self._tip}
                </small>
            """

        if self._label:
            label_classes = None
            receiver_classes = None
            if not self.__label_on_top:
                self.add_classes("row")
                label_classes = "col-sm-4 col-form-label"
                receiver_classes = "col-sm-8"

            return f"""
                <div {attr('class', self.classes)}>
                    <label {attr('class', label_classes)} {attr('for', self.identifier)}>
                        {self._label}
                    </label>
                    <div {attr('class', receiver_classes)}>
                        {self._receiver()}
                        {tips_html}
                    </div>
                </div>
            """

        # This part handles the case where there is no label.
        return f"""
            {self._receiver()}
            {tips_html}
        """


class CheckboxInput(Input, AppearanceMixin, OutlineMixin):
    """A checkbox input.

    Use the `as_disabled()` function to prevent the user from changing
    status of the `CheckboxInput` component.

    Args:
        label (str): The input label.
        name (str): The input name.
        checked (bool): The check box status.

    Example:
        from bootwrap import Form, CheckboxInput

        output = Form(
            CheckboxInput('One', 'opt1'),
            CheckboxInput('Two', 'opt2', True),
            CheckboxInput('Three', 'opt3').as_disabled(),
            CheckboxInput('Four', 'opt4', True).as_disabled(),
        )
    """

    def __init__(self, label, name, checked=False):
        super().__init__(label, name)
        self.__checked = checked
        self.__value = None
        self.__switch = False
        self.__button = False
        self.__inline = False
        self.__label_on_left = False

    def label_on_left(self):
        """Makes an input label showing on left.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form, CheckboxInput

            output = Form(
                CheckboxInput('One', 'opt1').label_on_left(),
                CheckboxInput('Two', 'opt2', True).label_on_left().as_switch(),
                CheckboxInput('Three', 'opt3').label_on_left().as_disabled(),
                CheckboxInput('Four', 'opt4', True).label_on_left().as_disabled()
            )
        """
        self.__label_on_left = True
        return self

    def as_radio(self, value):
        """Makes a chack box as radio button.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form, CheckboxInput

            output = Form(
                CheckboxInput('One', 'opt').as_radio(1),
                CheckboxInput('Two', 'opt', True).as_radio(2),
                CheckboxInput('Three', 'opt').as_radio(3).as_disabled(),
                CheckboxInput('Four', 'opt', True).as_radio(4).as_disabled()
            )
        """
        self.__value = value
        return self

    def as_switch(self):
        """Sets the "switch"-style to the check box.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form, CheckboxInput

            output = Form(
                CheckboxInput('One', 'opt1').as_switch(),
                CheckboxInput('Two', 'opt2', True).as_switch(),
                CheckboxInput('Three', 'opt3').as_switch().as_disabled(),
                CheckboxInput('Four', 'opt4', True).as_switch().as_disabled()
            )
        """
        self.__switch = True
        self.__button = False
        return self

    def as_button(self):
        """Sets the "button"-style to the check box.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form, CheckboxInput

            output = Form(
                CheckboxInput('One', 'opt1').as_button().as_primary().as_outline(),
                CheckboxInput('Two', 'opt2', True).as_button(),
                CheckboxInput('Three', 'opt3').as_button().as_disabled(),
                CheckboxInput('Four', 'opt4', True).as_button().as_disabled()
            )
        """
        self.__button = True
        self.__switch = False
        return self

    def inline(self):
        """Sets the check box in line.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form, CheckboxInput

            output = Form(
                CheckboxInput('One', 'opt1').inline(),
                CheckboxInput('Two', 'opt2', True).inline(),
                CheckboxInput('Three', 'opt3').inline().as_disabled(),
                CheckboxInput('Four', 'opt4', True).inline().as_disabled()
            )
        """
        self.__inline = True
        return self

    def _receiver(self):
        return ""

    def __str__(self):
        if self.__label_on_left:
            label_classes = "col-sm-4 col-form-label d-flex align-items-center"
            receiver_classes = "col-sm-8 d-flex align-items-center"
            return f"""
                <div {attr('class', 'form-group row')}>
                    <label {attr('class', label_classes)}
                        {attr('for', self.identifier)}>
                        {self._label}
                    </label>
                    <div {attr('class', receiver_classes)}>
                        <input {attr('id', self.identifier)}
                            {attr('name', self._name)}
                            {attr('class', 'form-check-input')}
                            {attr('value', "true" if self.__value is None else self.__value)}
                            type="checkbox"
                            autocomplete="off"
                            {attr('checked', self.__checked)}
                            {attr('disabled', self._disabled)}>
                        </input>    
                        <input type="hidden" name="{self._name}" value="false">
                        </input> 
                    </div>
                </div>
            """
        else:
            self.add_classes("form-check")
            type = "checkbox" if self.__value is None else "radio"
            if self.__inline:
                self.add_classes("form-check-inline")
            if self.__switch:
                self.add_classes("form-switch")

            # Sets input class (for the button look)
            input_classes = "form-check-input"
            label_classes = "form-check-label"
            if self.__button:
                input_classes = "btn-check"
                label_classes = "btn"
                if self._category:
                    if self._border:
                        label_classes += f" btn-outline-{self._category}"
                    else:
                        label_classes += f" btn-{self._category}"

            wc_input_n_label = f"""
                <input {attr('id', self.identifier)}
                    {attr('name', self._name)}
                    {attr('value', "true" if self.__value is None else self.__value)}
                    {attr('class', input_classes)}
                    type="{type}"
                    autocomplete="off"
                    {attr('checked', self.__checked)}
                    {attr('disabled', self._disabled)}>
                </input>    
                <label {attr('class', label_classes)} 
                    {attr('for', self.identifier)}>
                    {self._label or ''}
                    <input type="hidden" name="{self._name}" value="false">
                    </input> 
                </label>
            """

            if self.__button:
                return wc_input_n_label
            else:
                return f"""
                    <div {attr('class', self.classes)}>
                        {wc_input_n_label}
                    </div>
                """


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
        self._readonly = False

    def as_readonly(self):
        """Sets the freehand input components as read only.

        Returns:
            obj (self): The instance of this class.
        """
        self._readonly = True
        return self

    def _receiver(self):
        if self._rows > 1:
            assert self._type == "text", (
                f'The <class "TextInput"> of type "{self._type}" '
                + f"can not have {self._rows} rows."
            )
            return f"""
                <textarea {attr('id', self.identifier)}
                    {attr('name', self._name)}
                    class="form-control"
                    {attr('rows', self._rows)}
                    {attr('readonly', self._readonly)}
                    {attr('disabled', self._disabled)}>
                    {self.__value or ''}
                </textarea>
            """
        else:
            return f"""
                <input {attr('id', self.identifier)}
                    {attr('name', self._name)}
                    {attr('value', self.__value)}
                    type="{self._type}"
                    class="form-control"
                    {attr('placeholder', self.__placeholder)}
                    {attr('readonly', self._readonly)}
                    {attr('disabled', self._disabled)}/>
            """


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

        output = Form(
            TextInput('Text1', 'text'),
            TextInput('Text2', 'text').with_tip('Here is some tip').mt(2),
            TextInput('Text3', 'text', placeholder='type here').mt(2),
            TextInput('Text4', 'text', 'Hello World!').mt(2),
            TextInput('Text5', 'text', 'Hello World!').as_readonly().mt(2),
            TextInput('Text6', 'text').as_disabled().mt(2)
        )
    """

    def __init__(self, label, name, value=None, placeholder=None):
        super().__init__(label, name, value, placeholder)
        self._type = "text"

    def with_multirows(self, n):
        """Sets the number of rows.

        Args:
            n (int): The number of rows to set.

        Returns:
            obj (self): The instance of this class.

        Example:
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
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form, TextInput

            output = Form(
                TextInput('Email', 'email', 'my@email.com').for_email()
            )
        """
        self._type = "email"
        return self

    def for_password(self):
        """Configuring input for entering password.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form, TextInput

            output = Form(
                TextInput('Password', 'password', '********').for_password()
            )
        """
        self._type = "password"
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
        from bootwrap import Form, NumericInput

        output = Form(
            NumericInput('Number1', 'number'),
            NumericInput('Number2', 'number').with_tip('Here is some tip').mt(2),
            NumericInput('Number3', 'number', placeholder='type here').mt(2),
            NumericInput('Number4', 'number', 123).mt(2),
            NumericInput('Number5', 'number', 123).as_readonly().mt(2),
            NumericInput('Number6', 'number').as_disabled().mt(2)
        )
    """

    def __init__(self, label, name, value=None, placeholder=None):
        super().__init__(label, name, value, placeholder)
        self._type = "number"


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

        output = Form(
            SelectInput('Selector1', 'choice', 2, options),
            SelectInput('Selector2', 'choice', 2, options).with_tip('Here is some tip').mt(2),
            SelectInput('Selector3', 'choice', 2, options).as_disabled().mt(2)
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
            obj (self): The instance of this class.

        Example:
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
                options.append(
                    f"""
                    <div class="form-check me-3">
                        <input {attr('id', option.identifier)}
                            {attr('name', self._name)}
                            {attr('value', option.value)}
                            type="radio"
                            class="form-check-input"
                            autocomplete="off"
                            {attr('checked', option.value == self.__value)}
                            {attr('disabled', option.disabled)}/>
                        <label class="form-check-label me-1"
                            {attr('for', option.identifier)}>
                            {option.name}
                        </label>
                    </div>
                """
                )
            return inject(*options)
        else:
            options = []
            for option in self.__options:
                options.append(
                    f"""
                    <option {attr('id', option.identifier)}
                        {attr('value', option.value)}
                        {attr('selected', option.value == self.__value)}
                        {attr('disabled', option.disabled)}>
                        {option.name}
                    </option>
                """
                )

            return f"""
                <select {attr('id', self.identifier)}
                    {attr('name', self._name)}
                    class="form-control"
                    autocomplete="off"
                    {attr('disabled', self._disabled)}>
                    {inject(*options)}
                </select>
            """


class JsonInput(Input):
    """A JSON input.

    Args:
        label (str): The input label
        name (str): The input name.
        value (str): The input value.

        Example:
            from bootwrap import Form, JsonInput

            output = Form(
                JsonInput('JSON Config', 'code', '{"hello": "world enable"}'),
                JsonInput('JSON Config', 'code', '{"hello": "world enable"}').with_tip('Here is some tip').mt(2),
                JsonInput('JSON Config', 'code', '{"hello": "world disable"}').as_disabled().mt(2)
            )

    """

    def __init__(self, label, name, value=None):
        super().__init__(label, name)
        self.__value = value

    def _receiver(self):
        input_attr = [
            attr("id", self.identifier),
            attr("name", self._name),
            attr(
                "value",
                escape(
                    dumps(self.__value, ensure_ascii=False, indent=4).strip()
                ),
            ),
            attr("type", "hidden"),
        ]
        input_tag = tag("input", input_attr, "")

        json_attr = [
            attr("class", "language-json"),
        ]
        json_tag = tag(
            "code",
            json_attr,
            escape(
                dumps(self.__value, ensure_ascii=False, indent=4).strip(),
                quote=False,
            ),
        )

        onkeyup = "javascript:$('#" + self.identifier + "').val($(this).text())"
        pre_attr = [
            attr("contenteditable", "false" if self._disabled else "true"),
            attr("class", "w-100"),
            attr("onkeyup", onkeyup),
        ]
        pre_tag = tag("pre", pre_attr, json_tag)

        return pre_tag + input_tag


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
        return f"""
            <input {attr('id', self.identifier)}
                {attr('name', self._name)}
                {attr('value', self.__value)}
                type="hidden"/>
        """

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
            FileInput('File', 'file').with_tip('Here is some tip').mt(2),
            FileInput('File', 'file').as_disabled().mt(2)
        )
    """

    def __init__(self, label, name):
        super().__init__(label, name)

    def _receiver(self):
        browse_button_class = "btn btn-secondary"
        if self._disabled:
            browse_button_class += " disabled"

        return f"""
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
        """


class InputGroup(WebComponent, ClassMixin):
    """A web component for an input group.
    Groups together a series of input components
    Args:
        *components (list): The list of `WebComponent`.
    Example:
        from bootwrap import Text, TextInput, NumericInput, InputGroup, Form
        at = Text("@")
        username = TextInput(None, 'username', placeholder='type username')
        ig1 = InputGroup(at, username)
        ig2 = InputGroup(at, username).with_tip('Here is some tip').mt(2)
        recipient = TextInput(None, 'recipient', placeholder='Recipient username')
        domain = Text("@example.com")
        ig3 = InputGroup(recipient, domain).mt(2)
        recipient = TextInput(None, 'recipient', placeholder='Recipient username')
        domain = Text("@example.com")
        ig4 = InputGroup(recipient, domain).mt(2)
        money = Text("$")
        amount = NumericInput(None, 'amount', placeholder='Amount (to the nearest dollar)')
        cents = Text(".00")
        ig5 = InputGroup(money, amount, cents).mt(2)
        login = TextInput(None, 'login', placeholder='Login')
        at = Text("@")
        password = TextInput(None, 'password', placeholder='Password').for_password()
        ig6 = InputGroup(login, at, password).mt(2)
        output=Form(ig1,ig2,ig3,ig4,ig5,ig6)
    """

    def __init__(self, *inputs):
        super().__init__()
        self.__inputs = inputs
        self._tip = None

    def with_tip(self, tip):
        """Add a tip text to be displayed below the input group.
        Args:
            tip (str): The tip text to display.
        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text, TextInput, InputGroup, Form
            at = Text("@")
            username = TextInput(None, 'username', placeholder='type username')
            ig = InputGroup(at, username).with_tip('Here is some tip').mt(2)
            output=Form(ig)
        """
        self._tip = tip
        return self

    def __str__(self):
        self.add_classes("input-group")
        for input in self.__inputs:
            if isinstance(input, Text):
                input.add_classes("input-group-text")

        tips_html = ""
        if hasattr(self, "_tip") and self._tip:
            tips_html = f"""
                <small class="form-text text-secondary" style="font-size: 0.75em;">
                    {self._tip}
                </small>
            """

        return f"""
            <div {attr("id", self.identifier)}
                {attr("class", self.classes)}
                role="group">
                {inject(*self.__inputs)}
            </div>
            {tips_html}
        """
