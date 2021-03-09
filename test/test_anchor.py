"""
Test for bootwrap/components/anchor.py
"""

import pytest

from bootwrap import Anchor, Panel

from .helper import HelperHTMLParser


@pytest.mark.anchor
def test_anchor():
    anchor = Anchor('somename', 'somerole').add_classes('someclass').as_primary()
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}" class="text-primary someclass"
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
    target = Panel()
    anchor = Anchor('somename').toggle(target)
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}"
            href="#{target.identifier}"
            data-toggle="tab"
            role="tab">
            somename
        </a>
    ''')
    assert actual == expected
