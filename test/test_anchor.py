"""
Test for bootwrap/components/anchor.py
"""

import pytest

from bootwrap import Anchor, WebComponent

from .helper import HelperHTMLParser


@pytest.mark.anchor
def test_anchor():
    anchor = Anchor('somename', 'somerole').add_classes('someclass').as_primary()
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}" class="text-primary someclass" href="#"
            role="somerole">
            somename
        </a>
    ''')
    assert actual == expected


@pytest.mark.anchor
def test_link_anchor():
    anchor = Anchor('somename').link('someurl')
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}" href="someurl">
            somename
        </a>
    ''')
    assert actual == expected


@pytest.mark.anchor
def test_toggle_anchor():
    target = WebComponent()
    anchor = Anchor('somename').toggle(target)
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}" href="#{target.identifier}"
            data-toggle="tab">
            somename
        </a>
    ''')
    assert actual == expected
