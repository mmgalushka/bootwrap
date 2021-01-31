"""
Test for bootwrap/components/image.py
"""

import pytest

from bootwrap import (
    WebComponent,
    Form,
    Input,
    CheckboxInput,
    Freehand,
    TextInput,
    NumericInput,
    SelectInput,
    HiddenInput,
    FileInput
)

from .helper import HelperHTMLParser


@pytest.mark.form
def test_form():
    class Dummy(WebComponent):
        def __str__(self):
            return '<dummy>dummy</dummy>'

    form = Form(Dummy()).\
        on_submit('somelink').\
        add_classes('someclass')
    actual = HelperHTMLParser.parse(str(form))
    expected = HelperHTMLParser.parse(f'''
        <form id="{form.identifier}"
            action="somelink"
            class="someclass"
            method="POST"
            enctype="multipart/form-data">
            <dummy>dummy</dummy>
        </form>
    ''')
    assert actual == expected


@pytest.mark.form
def test_generic_input():
    class GenericInput(Input):
        def _receiver(self):
            return f'<xyz id="{self.identifier}">{self._name}</xyz>'

    # the label on the same row as input...
    generic = GenericInput('somelabel', 'somename').\
        add_classes('someclass')
    actual = HelperHTMLParser.parse(str(generic))
    expected = HelperHTMLParser.parse(f'''
        <div class="someclass row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{generic.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <xyz id="{generic.identifier}">somename</xyz>
            </div>
        </div>
    ''')
    assert actual == expected
    
    # the label on the top, input at the bottom...
    generic = GenericInput('somelabel', 'somename').\
        add_classes('someclass').\
        label_on_top()
    actual = HelperHTMLParser.parse(str(generic))
    expected = HelperHTMLParser.parse(f'''
        <div class="someclass">
            <label 
                for="{generic.identifier}">
                somelabel
            </label>
            <div >
                <xyz id="{generic.identifier}">somename</xyz>
            </div>
        </div>
    ''')
    assert actual == expected

    # with no label...
    generic = GenericInput(None, 'somename').\
        add_classes('someclass')
    actual = HelperHTMLParser.parse(str(generic))
    expected = HelperHTMLParser.parse(f'''
        <div class="someclass">
            <xyz id="{generic.identifier}">somename</xyz>
        </div>
    ''')
    assert actual == expected


@pytest.mark.form
def test_checkbox_input():
    checkbox = CheckboxInput('somelabel', 'somename')
    actual = HelperHTMLParser.parse(str(checkbox))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{checkbox.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <input id="{checkbox.identifier}"
                    name="somename"
                    type="checkbox" 
                    class="form-check-input" 
                    autocomplete="off"/>
            </div>
        </div>
    ''')
    assert actual == expected

    checkbox = CheckboxInput('somelabel', 'somename', True).\
        as_disabled()
    actual = HelperHTMLParser.parse(str(checkbox))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{checkbox.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
            <input id="{checkbox.identifier}"
                name="somename"
                type="checkbox" 
                class="form-check-input" 
                autocomplete="off" checked disabled/>
            </div>
        </div>
    ''')
    assert actual == expected

    # testing exception...
    with pytest.raises(AssertionError):
        str(CheckboxInput('somelabel', 'somename', True).label_on_top())

@pytest.mark.form
def test_text_input():
    # testing text-input...
    text = TextInput('somelabel', 'somename', 'somevalue', placeholder='someplaceholder')
    actual = HelperHTMLParser.parse(str(text))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{text.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <input id="{text.identifier}"
                    name="somename"
                    value="somevalue"
                    type="text"
                    class="form-control"
                    placeholder="someplaceholder"/>
            </div>
        </div>
    ''')
    assert actual == expected

    # testing email-input...
    email = TextInput('somelabel', 'somename').for_email()
    actual = HelperHTMLParser.parse(str(email))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{email.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <input id="{email.identifier}"
                    name="somename"
                    type="email"
                    class="form-control"/>
            </div>
        </div>
    ''')
    assert actual == expected

    # testing password-input...
    password = TextInput('somelabel', 'somename').for_password()
    actual = HelperHTMLParser.parse(str(password))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{password.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <input id="{password.identifier}"
                    name="somename"
                    type="password"
                    class="form-control"/>
            </div>
        </div>
    ''')
    assert actual == expected    

    # testing exception...
    with pytest.raises(AssertionError):
        str(
            TextInput('somelabel', 'somename', 'somevalue').\
            with_multirows(5).for_email()
        )
    with pytest.raises(AssertionError):
        str(
            TextInput('somelabel', 'somename', 'somevalue').\
            with_multirows(5).for_password()
        )


@pytest.mark.form
def test_text_area():
    def get_expected(element, disabled=False):
        return f'''
            <div class="row">
                <label class="col-sm-2 col-form-label d-flex align-items-center"
                    for="{element.identifier}">
                    somelabel
                </label>
                <div class="col-sm-10 d-flex align-items-center">
                    <textarea id="{element.identifier}"
                        name="somename" 
                        class="form-control"
                        rows=5
                        {'disabled' if disabled else ''}
                        >somevalue</textarea>
                </div>
            </div>
        '''

    textarea = TextInput('somelabel', 'somename', 'somevalue', placeholder='someplaceholder').\
        with_multirows(5)
    actual = HelperHTMLParser.parse(str(textarea))
    expected = HelperHTMLParser.parse(get_expected(textarea))
    assert actual == expected

    textarea = TextInput('somelabel', 'somename', 'somevalue', placeholder='someplaceholder').\
        with_multirows(5).as_disabled()
    actual = HelperHTMLParser.parse(str(textarea))
    expected = HelperHTMLParser.parse(get_expected(textarea, disabled=True))
    assert actual == expected


@pytest.mark.form
def test_numeric_input():
    numeric = NumericInput('somelabel', 'somename', 'somevalue', placeholder='someplaceholder')
    actual = HelperHTMLParser.parse(str(numeric))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{numeric.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <input id="{numeric.identifier}"
                    name="somename"
                    value="somevalue"
                    type="number"
                    class="form-control"
                    placeholder="someplaceholder"/>
    
            </div>
        </div>
    ''')
    assert actual == expected 

@pytest.mark.form
def test_select_input():
    option_0 = SelectInput.Option('Zero', 0, False)
    option_1 = SelectInput.Option('One', 1, True)
    options = [option_0, option_1]

    # testing select-input...
    select = SelectInput('somelabel', 'somename', 0, options)
    actual = HelperHTMLParser.parse(str(select))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{select.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <select id="{select.identifier}"
                    name="somename"
                    class="form-control"
                    autocomplete="off">
                    <option id="{option_0.identifier}"
                        value=0
                        selected
                        >Zero</option>
                    <option id="{option_1.identifier}"
                        value=1
                        disabled>One</option>
                </select>
            </div>
        </div>
    ''')
    assert actual == expected 

    select = SelectInput('somelabel', 'somename', 0, options).as_disabled()
    actual = HelperHTMLParser.parse(str(select))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{select.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <select id="{select.identifier}"
                    name="somename"
                    class="form-control"
                    autocomplete="off"
                    disabled>
                    <option id="{option_0.identifier}"
                        value=0
                        selected
                        >Zero</option>
                    <option id="{option_1.identifier}"
                        value=1
                        disabled>One</option>
                </select>
            </div>
        </div>
    ''')
    assert actual == expected 


@pytest.mark.form
def test_radio_input():
    option_0 = SelectInput.Option('Zero', 0, False)
    option_1 = SelectInput.Option('One', 1, True)
    options = [option_0, option_1]

    # testing select-input...
    radio = SelectInput('somelabel', 'somename', 0, options).as_radio()
    actual = HelperHTMLParser.parse(str(radio))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{radio.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <div class="form-check mr-3">
                    <input id="{option_0.identifier}"
                        name="somename"
                        value=0
                        type="radio" 
                        class="form-check-input" 
                        autocomplete="off"
                        checked/>
                    <label class="form-check-label mr-1" 
                        for="{option_0.identifier}">
                        Zero
                    </label>
                </div>
                <div class="form-check mr-3">
                    <input id="{option_1.identifier}"
                        name="somename"
                        value=1
                        type="radio" 
                        class="form-check-input" 
                        autocomplete="off"
                        disabled/>
                    <label class="form-check-label mr-1" 
                        for="{option_1.identifier}">
                        One
                    </label>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected 


@pytest.mark.form
def test_hidden_input():
    hidden = HiddenInput('somename', 'somevalue')
    actual = HelperHTMLParser.parse(str(hidden))
    expected = HelperHTMLParser.parse(f'''
        <input id="{hidden.identifier}"
            name="somename"
            value="somevalue"
            type="hidden"/>
    ''')
    assert actual == expected 

@pytest.mark.form
def test_file_input():
    regexp = r'/[\|/]/'
    file = FileInput('somelabel', 'somename').add_classes('someclass')
    actual = HelperHTMLParser.parse(str(file))
    expected = HelperHTMLParser.parse(f'''
        <div class="someclass row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{file.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <div class="input-group">
                    <span class="form-control input-group-append"></span>
                    <div class="input-group-append">
                        <span class="btn btn-secondary"
                            onclick="$(this).parent().find('input[type=file]').click();">
                            Browse
                        </span>
                        <input id="{file.identifier}"
                            name="somename"
                            onchange="$(this).parent().parent().find('.form-control').html($(this).val().split({regexp}).pop());"
                            style="display: none;"
                            type="file"/>
                    </div>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected 

    file = FileInput('somelabel', 'somename').as_disabled()
    actual = HelperHTMLParser.parse(str(file))
    expected = HelperHTMLParser.parse(f'''
        <div class="row">
            <label class="col-sm-2 col-form-label d-flex align-items-center"
                for="{file.identifier}">
                somelabel
            </label>
            <div class="col-sm-10 d-flex align-items-center">
                <div class="input-group">
                    <span class="form-control input-group-append"></span>
                    <div class="input-group-append">
                        <span class="btn btn-secondary disabled"
                            onclick="$(this).parent().find('input[type=file]').click();">
                            Browse
                        </span>
                        <input id="{file.identifier}"
                            name="somename"
                            onchange="$(this).parent().parent().find('.form-control').html($(this).val().split({regexp}).pop());"
                            style="display: none;"
                            type="file"
                            disabled/>
                    </div>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected 
