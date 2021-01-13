"""
Test for bootwrap/components/image.py
"""

import pytest

from pyquery import PyQuery as pq
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

# This a helper function for selecting tag(s) for interest from the HTML
# fragment.
def _get_element(wc, tag):
    d = pq(str(wc))
    d_target = pq(d(tag))
    if len(d_target) > 1:
        return [d_target.eq(i) for i in range(len(d_target))]
    return d_target


@pytest.mark.form
def test_form():
    class Dummy(WebComponent):
        def __str__(self):
            return '<dummy>dummy</dummy>'

    form = Form(Dummy()).\
        on_submit('somelink').\
        add_classes('someclass')
    d_form = _get_element(form, 'form')
    assert set(d_form.attr('class').split(' ')) == set(['someclass'])
    assert d_form.attr('action') == 'somelink' 
    assert d_form.attr('method') == 'POST' 
    assert d_form.attr('enctype') == 'multipart/form-data' 

    d_dummy = _get_element(form, 'dummy')
    assert d_dummy.text() == 'dummy'


@pytest.mark.form
def test_generic_input():
    class GenericInput(Input):
        def _receiver(self):
            return f'<xyz>{self._name}</xyz>'

    # the label on the same row as input...
    generic = GenericInput('somelabel', 'somename').\
        add_classes('someclass')
    d_div_0, d_div_1 = _get_element(generic, 'div')
    assert set(d_div_0.attr('class').split(' ')) == set(['row', 'someclass'])
    assert set(d_div_1.attr('class').split(' ')) == set(['col-sm-10', 'd-flex', 'align-items-center'])

    d_label = _get_element(generic, 'label')
    assert set(d_label.attr('class').split(' ')) == set(['col-sm-2', 'col-form-label', 'd-flex', 'align-items-center'])
    assert d_label.attr('for') == str(generic.identifier)
    assert d_label.text() == 'somelabel'

    d_xyz = _get_element(generic, 'xyz')
    assert d_xyz.text().strip() == 'somename'
    
    # the label on the top, input at the bottom...
    generic = GenericInput('somelabel', 'somename').\
        add_classes('someclass').\
        label_on_top()
    d_div_0, d_div_1 = _get_element(generic, 'div')
    assert set(d_div_0.attr('class').split(' ')) == set(['someclass'])
    assert d_div_1.attr('class') is None

    d_label = _get_element(generic, 'label')
    assert d_label.attr('class') is None
    assert d_label.attr('for') == str(generic.identifier)
    assert d_label.text() == 'somelabel'

    d_xyz = _get_element(generic, 'xyz')
    assert d_xyz.text().strip() == 'somename'

    # with no label...
    generic = GenericInput(None, 'somename').\
        add_classes('someclass')
    d_div = _get_element(generic, 'div')
    assert set(d_div.attr('class').split(' ')) == set(['someclass'])\

    d_xyz = _get_element(generic, 'xyz')
    assert d_xyz.text().strip() == 'somename'


@pytest.mark.form
def test_checkbox_input():
    checkbox = CheckboxInput('somelabel', 'somename')
    d = pq(str(checkbox))
    d_div = pq(d('div'))
    d_div_div = pq(d_div('div')).eq(1)
    d_div_div_input = pq(d_div_div('input'))

    assert d_div_div_input.attr('id') == str(checkbox.identifier)
    assert d_div_div_input.attr('name') == 'somename'
    assert d_div_div_input.attr('type') == 'checkbox'
    assert d_div_div_input.attr('class') == 'form-check-input'
    assert d_div_div_input.attr('autocomplete') == 'off'
    assert d_div_div_input.attr('checked') is None
    assert d_div_div_input.attr('disabled') is None

    checkbox = CheckboxInput('somelabel', 'somename', True).\
        as_disabled()
    d = pq(str(checkbox))
    d_div = pq(d('div'))
    d_div_div = pq(d_div('div')).eq(1)
    d_div_div_input = pq(d_div_div('input'))
    assert d_div_div_input.attr('checked') == 'checked'
    assert d_div_div_input.attr('disabled') == 'disabled'


@pytest.mark.form
def test_text_input():
    # testing text-input...
    text = TextInput('somelabel', 'somename', 'somevalue', placeholder='someplaceholder')
    d_input = _get_element(text, 'input')
    assert d_input.attr('id') == str(text.identifier)
    assert d_input.attr('class') == 'form-control'
    assert d_input.attr('name') == 'somename'
    assert d_input.attr('value') == 'somevalue'
    assert d_input.attr('type') == 'text'
    assert d_input.attr('placeholder') == 'someplaceholder'
    assert d_input.attr('disabled') is None

    text = TextInput('somelabel', 'somename', 'somevalue').\
        as_disabled()
    d_input = _get_element(text, 'input')
    assert d_input.attr('disabled') == 'disabled'

    # testing email-input...
    email = TextInput('somelabel', 'somename').\
        for_email()
    d_input = _get_element(email, 'input')
    assert d_input.attr('type') == 'email'

    # testing password-input...
    password = TextInput('somelabel', 'somename').\
        for_password()
    d_input = _get_element(password, 'input')
    assert d_input.attr('type') == 'password'

    # testing textarea-input...
    textarea = TextInput('somelabel', 'somename', 'somevalue').\
        with_multirows(5)
    d_textarea = _get_element(textarea, 'textarea')
    assert d_textarea.attr('id') == str(textarea.identifier)
    assert d_textarea.attr('class') == 'form-control'
    assert d_textarea.attr('name') == 'somename'
    assert d_textarea.attr('rows') == '5'
    assert d_textarea.attr('type') == None
    assert d_textarea.attr('placeholder') == None
    assert d_textarea.text().strip() == 'somevalue'

    # testing exception...
    xyz = TextInput('somelabel', 'somename', 'somevalue').\
        with_multirows(5).for_email()
    with pytest.raises(AssertionError):
        _get_element(xyz, 'xyz')


@pytest.mark.form
def test_numeric_input():
    numeric = NumericInput('somelabel', 'somename', 'somevalue', placeholder='someplaceholder')
    d_input = _get_element(numeric, 'input')
    assert d_input.attr('id') == str(numeric.identifier)
    assert d_input.attr('class') == 'form-control'
    assert d_input.attr('name') == 'somename'
    assert d_input.attr('value') == 'somevalue'
    assert d_input.attr('type') == 'number'
    assert d_input.attr('placeholder') == 'someplaceholder'
    assert d_input.attr('disabled') is None

    numeric = NumericInput('somelabel', 'somename', 'somevalue').\
        as_disabled()
    d_input = _get_element(numeric, 'input')
    assert d_input.attr('disabled') == 'disabled'


@pytest.mark.form
def test_select_input():
    option_0 = SelectInput.Option('Zero', 0, False)
    option_1 = SelectInput.Option('One', 1, True)
    options = [option_0, option_1]

    # testing select-input...
    select = SelectInput('somelabel', 'somename', 0, options)
    d_select = _get_element(select, 'select')
    assert d_select.attr('id') == str(select.identifier)
    assert d_select.attr('class') == 'form-control'
    assert d_select.attr('name') == 'somename'
    assert d_select.attr('autocomplete') == 'off'

    d_option_0, d_option_1 = _get_element(select, 'option')

    assert d_option_0.attr('value') == '0'
    assert d_option_0.attr('disabled') is None
    assert d_option_0.text().strip() == 'Zero'
    
    assert d_option_1.attr('value') == '1'
    assert d_option_1.attr('disabled') == 'disabled'
    assert d_option_1.text().strip() == 'One'

    select = SelectInput('somelabel', 'somename', 1, options).\
        as_disabled()
    d_select = _get_element(select, 'select')
    assert d_select.attr('disabled') == 'disabled'

    # testing radio-input...
    radio = SelectInput('somelabel', 'somename', 0, options).as_radio()
    d_radio_0, d_radio_1 = _get_element(radio, 'input')
    
    assert d_radio_0.attr('id') == str(option_0.identifier)
    assert d_radio_0.attr('name') == 'somename'
    assert d_radio_0.attr('class') == 'form-check-input'
    assert d_radio_0.attr('autocomplete') == 'off'
    assert d_radio_0.attr('value') == '0'
    assert d_radio_0.attr('checked') is not None
    assert d_radio_0.attr('disabled') is None

    assert d_radio_1.attr('id') == str(option_1.identifier)
    assert d_radio_1.attr('name') == 'somename'
    assert d_radio_1.attr('class') == 'form-check-input'
    assert d_radio_1.attr('autocomplete') == 'off'
    assert d_radio_1.attr('value') == '1'
    assert d_radio_1.attr('checked') is None
    assert d_radio_1.attr('disabled') is not None


@pytest.mark.form
def test_hidden_input():
    hidden = HiddenInput('somename', 'somevalue')
    d = pq(str(hidden))
    assert d.attr('id') == str(hidden.identifier)
    assert d.attr('name') == 'somename'
    assert d.attr('value') == 'somevalue'
    assert d.attr('type') == 'hidden'


@pytest.mark.form
def test_file_input():
    file = FileInput('somelabel', 'somename').\
        add_classes('someclass')

    d_span_0, d_span_1 = _get_element(file, 'span')
    assert set(d_span_0.attr('class').split(' ')) == set(['form-control', 'input-group-append'])
    assert d_span_0.text().strip() == ''
    assert set(d_span_1.attr('class').split(' ')) == set(['btn', 'btn-secondary'])
    assert d_span_1.attr('onclick') == "$(this).parent().find('input[type=file]').click();"
    assert d_span_1.text().strip() == 'Browse'

    d_file = _get_element(file, 'input')
    assert d_file.attr('id') == str(file.identifier)
    assert d_file.attr('name') == 'somename'
    assert d_file.attr('onchange') == "$(this).parent().parent().find('.form-control').html($(this).val().split(/[\\|/]/).pop());"
    assert d_file.attr('style') == 'display: none;'
    assert d_file.attr('type') == 'file'
    assert d_file.attr('disabled') is None

    file = FileInput('somelabel', 'somename').\
        as_disabled()
    
    _, d_span = _get_element(file, 'span')
    assert set(d_span.attr('class').split(' ')) == set(['btn', 'btn-secondary', 'disabled'])

    d_file = _get_element(file, 'input')
    assert d_file.attr('disabled') == 'disabled'
