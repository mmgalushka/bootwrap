"""
Test for bootwrap/components/button.py
"""

import pytest

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

    button = Button('Somename').as_primary()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn btn-primary">
            Somename
        </button>
    ''')
    assert actual == expected


    button = Button('Somename').as_primary().as_outline()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn btn-outline-primary">
            Somename
        </button>
    ''')
    assert actual == expected


    button = Button('Somename').add_classes('someclass')
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
    button = Button('Somename').link('someurl')
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <a id="{button.identifier}" class="btn" href="someurl" role="button">
            Somename
        </a>
    ''')
    assert actual == expected

    target = WebComponent()
    button = Button('Somename').link(target)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <a id="{button.identifier}" class="btn" href="#{target.identifier}" role="button">
            Somename
        </a>
    ''')
    assert actual == expected

    button = Button('Somename').link('someurl').as_disabled()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <a id="{button.identifier}" class="btn disabled" href="someurl"
            role="button">
            Somename
        </a>
    ''')
    assert actual == expected


@pytest.mark.button
def test_toggle_button():
    target = WebComponent()
    button = Button('Somename').toggle(target)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn" type="button"
            data-toggle="modal" data-target="#{target.identifier}">
            Somename
        </button>
    ''')
    assert actual == expected


@pytest.mark.button
def test_collapse_button():
    target = WebComponent()
    button = Button('Somename').collapse(target)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn" type="button"
            data-toggle="collapse" data-target="#{target.identifier}">
            Somename
        </button>
    ''')
    assert actual == expected


@pytest.mark.button
def test_dismiss_button():
    button = Button('Somename').dismiss()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn" type="button"
            data-dismiss="modal">
            Somename
        </button>
    ''')
    assert actual == expected


@pytest.mark.button
def test_submit_button():
    button = Button('Somename').submit()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}" class="btn" type="submit">
            Somename
        </button>
    ''')
    assert actual == expected
