"""
Test for bootwrap/components/button.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Button, WebComponent

from .helper import HelperHTMLParser


@pytest.mark.button
def test_button():
    button = Button('Somename')
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn">
            Somename
        </button>
    ''')
    assert actual == expected

    button = Button('Somename').\
        as_primary()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn btn-primary">
            Somename
        </button>
    ''')
    assert actual == expected


    button = Button('Somename').\
        as_primary().\
        as_outline()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn btn-outline-primary">
            Somename
        </button>
    ''')
    assert actual == expected


    button = Button('Somename').\
        add_classes('someclass')
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn someclass">
            Somename
        </button>
    ''')
    assert actual == expected

    button = Button('Somename').as_disabled()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn" disabled>
            Somename
        </button>
    ''')
    assert actual == expected


@pytest.mark.button
def test_link_button():
    button = Button('Somename').\
        link('someurl')
    d = pq(str(button))
    assert d == d('a')
    assert set(d.attr('class').split(' ')) == set(['btn'])
    assert d.attr('href')  == 'someurl'
    assert d.attr('role')  == 'button'
    assert d.text().strip() == 'Somename'

    button = Button('Somename').\
        link('someurl').\
        as_disabled()
    d = pq(str(button))
    assert set(d.attr('class').split(' ')) == set(['btn', 'disabled'])
    assert 'disabled' in d.attr('class')


@pytest.mark.button
def test_toggle_button():
    target = WebComponent()
    button = Button('Somename').\
        toggle(target)
    d = pq(str(button))
    assert d == d('button')
    assert set(d.attr('class').split(' ')) == set(['btn'])
    assert d.attr('type')  == 'button'
    assert d.attr('data-toggle')  == 'modal'
    assert d.attr('data-target')  == '#' + str(target.identifier)
    assert d.text().strip() == 'Somename'


@pytest.mark.button
def test_collapse_button():
    target = WebComponent()
    button = Button('Somename').\
        collapse(target)
    d = pq(str(button))
    assert d == d('button')
    assert set(d.attr('class').split(' ')) == set(['btn'])
    assert d.attr('type')  == 'button'
    assert d.attr('data-toggle')  == 'collapse'
    assert d.attr('data-target')  == '#' + str(target.identifier)
    assert d.text().strip() == 'Somename'


@pytest.mark.button
def test_dismiss_button():
    button = Button('Somename').\
        dismiss()
    d = pq(str(button))
    assert d == d('button')
    assert set(d.attr('class').split(' ')) == set(['btn'])
    assert d.attr('type')  == 'button'
    assert d.attr('data-dismiss')  == 'modal'
    assert d.text().strip() == 'Somename'


@pytest.mark.button
def test_submit_button():
    button = Button('Somename').\
        submit()
    d = pq(str(button))
    assert d == d('button')
    assert set(d.attr('class').split(' ')) == set(['btn'])
    assert d.attr('type')  == 'submit'
    assert d.text().strip() == 'Somename'
