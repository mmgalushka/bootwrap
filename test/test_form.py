"""
Test for bootwrap/components/image.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import (
    WebComponent,
    Form,
    CheckboxInput,
    RadioInput,
    EmailInput,
    PasswordInput,
    TextInput,
    NumericInput,
    SelectInput,
    HiddenInput,
    FileInput
)


@pytest.mark.form
def test_form():
    class Dummy(WebComponent):
        def __str__(self):
            return '<dummy>dummy</dummy>'

    form = Form('someaction').add_classes('someclass').append(Dummy())
    d = pq(str(form))
    assert d == d('form')
    assert 'someclass' in d.attr('class')
    assert d.attr('action') == 'someaction' 
    assert d.attr('method') == 'POST' 
    assert d.attr('enctype') == 'multipart/form-data' 

    d_dummy = pq(d('dummy'))
    assert d_dummy.text() == 'dummy'


@pytest.mark.form
def test_checkbox_input():
    checkbox = CheckboxInput('somelabel', 'somename').add_classes('someclass')
    d = pq(str(checkbox))
    d_div = pq(d('div'))
    assert 'someclass' in d_div.attr('class')
    assert 'form-check' in d_div.attr('class')
    assert 'form-check-inline' in d_div.attr('class')

    d_div_label = pq(d_div('label'))
    assert d_div_label.attr('class') == 'form-check-label'
    assert d_div_label.attr('for') == str(checkbox.identifier)
    assert d_div_label.text() == 'somelabel'

    d_div_input_hidden = pq(d_div('input[type="checkbox"]'))
    assert d_div_input_hidden.attr('id') == str(checkbox.identifier)
    assert d_div_input_hidden.attr('name') == 'somename'
    assert d_div_input_hidden.attr('class') == 'form-check-input'
    assert d_div_input_hidden.attr('autocomplete') == 'off'
    assert d_div_input_hidden.attr('checked') is None
    assert d_div_input_hidden.attr('disabled') is None

    d_div_input_hidden = pq(d_div('input[type="hidden"]'))
    assert d_div_input_hidden.attr('name') == 'somename'
    assert d_div_input_hidden.attr('value') == 'off'

    checkbox = CheckboxInput('somelabel', 'somename').check(True).as_disabled()
    d = pq(str(checkbox))
    d_div = pq(d('div'))
    d_div_input_hidden = pq(d_div('input[type="checkbox"]'))
    assert d_div_input_hidden.attr('checked') == 'checked'
    assert d_div_input_hidden.attr('disabled') == 'disabled'


@pytest.mark.form
def test_radio_input():
    radio = RadioInput('somelabel', 'somename').add_classes('someclass').value('somevalue')
    d = pq(str(radio))
    d_div = pq(d('div'))
    assert 'someclass' in d_div.attr('class')
    assert 'form-check' in d_div.attr('class')
    assert 'form-check-inline' in d_div.attr('class')

    d_div_label = pq(d_div('label'))
    assert d_div_label.attr('class') == 'form-check-label'
    assert d_div_label.attr('for') == str(radio.identifier)
    assert d_div_label.text() == 'somelabel'

    d_div_input_hidden = pq(d_div('input[type="radio"]'))
    assert d_div_input_hidden.attr('id') == str(radio.identifier)
    assert d_div_input_hidden.attr('name') == 'somename'
    assert d_div_input_hidden.attr('class') == 'form-check-input'
    assert d_div_input_hidden.attr('autocomplete') == 'off'
    assert d_div_input_hidden.attr('value') == 'somevalue'
    assert d_div_input_hidden.attr('checked') is None
    assert d_div_input_hidden.attr('disabled') is None

    d_div_input_hidden = pq(d_div('input[type="hidden"]'))
    assert d_div_input_hidden.attr('name') == 'somename'
    assert d_div_input_hidden.attr('value') == 'off'

    radio = RadioInput('somelabel', 'somename').check(True).as_disabled()
    d = pq(str(radio))
    d_div = pq(d('div'))
    d_div_input_hidden = pq(d_div('input[type="radio"]'))
    assert d_div_input_hidden.attr('checked') == 'checked'
    assert d_div_input_hidden.attr('disabled') == 'disabled'


@pytest.mark.form
def test_email_input():
    # test label & input inline
    email = EmailInput('somelabel', 'somename', placeholder='some@place.holder').\
        add_classes('someclass').\
        value('somevalue@host.com')
    d = pq(str(email))
    assert 'row' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_label = pq(d('label'))
    assert d_label.attr('class') == 'col-sm-2 col-form-label'
    assert d_label.attr('for') == str(email.identifier)
    assert d_label.text() == 'somelabel'

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') == 'col-sm-10'

    d_div_input = pq(d_div('input'))
    assert d_div_input.attr('id') == str(email.identifier)
    assert d_div_input.attr('class') == 'form-control'
    assert d_div_input.attr('name') == 'somename'
    assert d_div_input.attr('value') == 'somevalue@host.com'
    assert d_div_input.attr('type') == 'email'
    assert d_div_input.attr('placeholder') == 'some@place.holder'

    # test label & input stack (test only a  difference with inline version)
    email = EmailInput('somelabel', 'somename').\
        label_on_top()
    d = pq(str(email))
    assert d.attr('class') is None

    d_label = pq(d('label'))
    assert d_label.attr('class') is None

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') is None


@pytest.mark.form
def test_password_input():
    # test label & input inline
    password = PasswordInput('somelabel', 'somename', placeholder='some@place.holder').\
        add_classes('someclass').\
        value('somevalue@host.com')
    d = pq(str(password))
    assert 'row' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_label = pq(d('label'))
    assert d_label.attr('class') == 'col-sm-2 col-form-label'
    assert d_label.attr('for') == str(password.identifier)
    assert d_label.text() == 'somelabel'

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') == 'col-sm-10'

    d_div_input = pq(d_div('input'))
    assert d_div_input.attr('id') == str(password.identifier)
    assert d_div_input.attr('class') == 'form-control'
    assert d_div_input.attr('name') == 'somename'
    assert d_div_input.attr('value') == 'somevalue@host.com'
    assert d_div_input.attr('type') == 'password'
    assert d_div_input.attr('placeholder') == 'some@place.holder'

    # test label & input stack (test only a  difference with inline version)
    password = PasswordInput('somelabel', 'somename').\
        label_on_top()
    d = pq(str(password))
    assert d.attr('class') is None

    d_label = pq(d('label'))
    assert d_label.attr('class') is None

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') is None


@pytest.mark.form
def test_text_input():
    # test label & input inline
    text = TextInput('somelabel', 'somename', placeholder='someplaceholder').\
        add_classes('someclass').\
        value('somevalue')
    d = pq(str(text))
    assert 'row' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_label = pq(d('label'))
    assert d_label.attr('class') == 'col-sm-2 col-form-label'
    assert d_label.attr('for') == str(text.identifier)
    assert d_label.text() == 'somelabel'

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') == 'col-sm-10'

    d_div_input = pq(d_div('input'))
    assert d_div_input.attr('id') == str(text.identifier)
    assert d_div_input.attr('class') == 'form-control'
    assert d_div_input.attr('name') == 'somename'
    assert d_div_input.attr('value') == 'somevalue'
    assert d_div_input.attr('type') == 'text'
    assert d_div_input.attr('placeholder') == 'someplaceholder'

    # test label & input stack (test only a  difference with inline version)
    text = TextInput('somelabel', 'somename', placeholder='someplaceholder').\
        label_on_top()
    d = pq(str(text))
    assert d.attr('class') is None

    d_label = pq(d('label'))
    assert d_label.attr('class') is None

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') is None

    # test multi-rows input
    text = TextInput('somelabel', 'somename', rows=5).\
        add_classes('someclass').\
        value('somevalue')
    d = pq(str(text))
    
    d_textarea_input = pq(d('textarea'))
    assert d_textarea_input.attr('id') == str(text.identifier)
    assert d_textarea_input.attr('class') == 'form-control'
    assert d_textarea_input.attr('name') == 'somename'
    assert d_textarea_input.attr('rows') == '5'
    assert d_textarea_input.attr('type') == None
    assert d_textarea_input.attr('placeholder') == None
    assert d_textarea_input.text().strip() == 'somevalue'
 

@pytest.mark.form
def test_numeric_input():
    # test label & input inline
    number = NumericInput('somelabel', 'somename', placeholder='somenumber').\
        add_classes('someclass').\
        value(123)
    d = pq(str(number))
    assert 'row' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_label = pq(d('label'))
    assert d_label.attr('class') == 'col-sm-2 col-form-label'
    assert d_label.attr('for') == str(number.identifier)
    assert d_label.text() == 'somelabel'

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') == 'col-sm-10'

    d_div_input = pq(d_div('input'))
    assert d_div_input.attr('id') == str(number.identifier)
    assert d_div_input.attr('class') == 'form-control'
    assert d_div_input.attr('name') == 'somename'
    assert int(d_div_input.attr('value')) == 123
    assert d_div_input.attr('type') == 'number'
    assert d_div_input.attr('placeholder') == 'somenumber'

    # test label & input stack (test only a  difference with inline version)
    number = NumericInput('somelabel', 'somename').\
        label_on_top()
    d = pq(str(number))
    assert d.attr('class') is None

    d_label = pq(d('label'))
    assert d_label.attr('class') is None

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') is None


@pytest.mark.form
def test_select_input():
    # test label & input inline
    select = SelectInput('somelabel', 'somename').\
        add_classes('someclass').\
        value(1).\
        append(
            ('One', '1', False),
            ('Two', '2', True),
        )
    d = pq(str(select))
    assert 'row' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_label = pq(d('label'))
    assert d_label.attr('class') == 'col-sm-2 col-form-label'
    assert d_label.attr('for') == str(select.identifier)
    assert d_label.text() == 'somelabel'

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') == 'col-sm-10'

    d_div_select = pq(d_div('select'))
    assert d_div_select.attr('id') == str(select.identifier)
    assert d_div_select.attr('class') == 'form-control'
    assert d_div_select.attr('name') == 'somename'
    assert d_div_select.attr('autocomplete') == 'off'

    d_div_select_option_0 = pq(d_div_select('option')).eq(0)
    assert d_div_select_option_0.attr('value') == '1'
    assert d_div_select_option_0.attr('disabled') is None
    assert d_div_select_option_0.text().strip() == 'One'

    d_div_select_option_1 = pq(d_div_select('option')).eq(1)
    assert d_div_select_option_1.attr('value') == '2'
    assert d_div_select_option_1.attr('disabled') == 'disabled'
    assert d_div_select_option_1.text().strip() == 'Two'

    # test label & select stack (test only a difference with inline version)
    select = SelectInput('somelabel', 'somename').\
        label_on_top()
    d = pq(str(select))
    assert d.attr('class') is None

    d_label = pq(d('label'))
    assert d_label.attr('class') is None

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') is None


@pytest.mark.form
def test_hidden_input():
    hidden = HiddenInput('somename').value('somevalue')
    d = pq(str(hidden))
    assert d.attr('id') == str(hidden.identifier)
    assert d.attr('name') == 'somename'
    assert d.attr('value') == 'somevalue'
    assert d.attr('type') == 'hidden'


@pytest.mark.form
def test_file_input():
    # test label & input inline
    file = FileInput('somelabel', 'somename').\
        add_classes('someclass')
    d = pq(str(file))
    assert 'row' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_label = pq(d('label'))
    assert d_label.attr('class') == 'col-sm-2 col-form-label'
    assert d_label.attr('for') == str(file.identifier)
    assert d_label.text() == 'somelabel'

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') == 'col-sm-10'

    d_div_div = pq(d_div('div[class="input-group"]'))
    d_div_div_div = pq(d_div_div('div[class="input-group-append"]'))

    d_div_div_div_span = pq(d_div_div_div('span'))
    assert d_div_div_div_span.attr('class') == 'btn btn-secondary'
    assert d_div_div_div_span.attr('onclick') == "$(this).parent().find('input[type=file]').click();"
    assert d_div_div_div_span.text().strip() == 'Browse'

    d_div_div_div_input = pq(d_div_div_div('input'))
    assert d_div_div_div_input.attr('id') == str(file.identifier)
    assert d_div_div_div_input.attr('name') == 'somename'
    assert d_div_div_div_input.attr('onchange') == "$(this).parent().parent().find('.form-control').html($(this).val().split(/[\\|/]/).pop());"
    assert d_div_div_div_input.attr('style') == 'display: none;'
    assert d_div_div_div_input.attr('type') == 'file'
    assert d_div_div_div_input.attr('disabled') is None

    # test label & input stack (test only a difference with inline version)
    file = FileInput('somelabel', 'somename').label_on_top()
    d = pq(str(file))
    assert d.attr('class') is None

    d_label = pq(d('label'))
    assert d_label.attr('class') is None

    d_div = pq(d('div')).eq(1)
    assert d_div.attr('class') is None

    # test disabled input
    file = FileInput('somelabel', 'somename').as_disabled()
    d = pq(str(file))

    d_div = pq(d('div')).eq(1)
    d_div_div = pq(d_div('div[class="input-group"]'))
    d_div_div_div = pq(d_div_div('div[class="input-group-append"]'))

    d_div_div_div_span = pq(d_div_div_div('span'))
    assert d_div_div_div_span.attr('class') == 'btn btn-secondary disabled'

    d_div_div_div_input = pq(d_div_div_div('input'))
    assert d_div_div_div_input.attr('disabled') == 'disabled'