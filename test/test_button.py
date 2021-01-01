"""
Test for bootwrap/components/button.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Button, WebComponent


@pytest.mark.button
def test_button():
    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        link('someurl')
    d = pq(str(button))
    assert d == d('a')
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn' in d.attr('class')
    assert 'btn-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')
    assert d.attr('role')  == 'button'
    assert d.text().strip() == 'Somename'

    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        as_outline().\
        link('someurl')
    d = pq(str(button))
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn-outline-primary' in d.attr('class')

    button = Button('Somename').as_disabled()
    d = pq(str(button))
    assert 'disabled' in d.attr('class')


@pytest.mark.button
def test_toggle_button():
    target = WebComponent()
    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        toggle(target)
    d = pq(str(button))
    assert d == d('button')
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn' in d.attr('class')
    assert 'btn-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')
    assert d.attr('type')  == 'button'
    assert d.attr('data-toggle')  == 'modal'
    assert d.attr('data-target')  == '#' + str(target.identifier)
    assert d.text().strip() == 'Somename'

    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        as_outline().\
        toggle(target)
    d = pq(str(button))
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn-outline-primary' in d.attr('class')

    button = Button('Somename').toggle(target).as_disabled()
    d = pq(str(button))
    assert d.attr('disabled') == 'disabled'



@pytest.mark.button
def test_collapse_button():
    target = WebComponent()
    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        collapse(target)
    d = pq(str(button))
    assert d == d('button')
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn' in d.attr('class')
    assert 'btn-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')
    assert d.attr('type')  == 'button'
    assert d.attr('data-toggle')  == 'collapse'
    assert d.attr('data-target')  == '#' + str(target.identifier)
    assert d.text().strip() == 'Somename'

    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        as_outline().\
        collapse(target)
    d = pq(str(button))
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn-outline-primary' in d.attr('class')

    button = Button('Somename').collapse(target).as_disabled()
    d = pq(str(button))
    assert d.attr('disabled') == 'disabled'



@pytest.mark.button
def test_dismiss_button():
    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        dismiss()
    d = pq(str(button))
    assert d == d('button')
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn' in d.attr('class')
    assert 'btn-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')
    assert d.attr('type')  == 'button'
    assert d.attr('data-dismiss')  == 'modal'
    assert d.text().strip() == 'Somename'

    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        as_outline().\
        dismiss()
    d = pq(str(button))
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn-outline-primary' in d.attr('class')

    button = Button('Somename').as_disabled().dismiss()
    d = pq(str(button))
    assert d.attr('disabled') == 'disabled'


@pytest.mark.button
def test_submit_button():
    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        submit()
    d = pq(str(button))
    assert d == d('button')
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn' in d.attr('class')
    assert 'btn-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')
    assert d.attr('type')  == 'submit'
    assert d.text().strip() == 'Somename'

    button = Button('Somename').\
        add_classes('someclass').\
        as_primary().\
        as_outline().\
        submit()
    d = pq(str(button))
    assert len(d.attr('class').split(' ')) == 3
    assert 'btn-outline-primary' in d.attr('class')

    button = Button('Somename').as_disabled().submit()
    d = pq(str(button))
    assert d.attr('disabled') == 'disabled'
