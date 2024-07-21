"""
Test for bootwrap/components/anchor.py
"""

import warnings
import pytest

from bootwrap import (
    Anchor,
    Panel,
    Dialog,
    Text
)
from .helper import HelperHTMLParser


@pytest.mark.anchor
def test_anchor():
    anchor = Anchor('somename').add_classes('someclass').\
        as_primary()
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}" class="text-primary someclass">
            somename
        </a>
    ''')
    assert actual == expected

    header = Text('someheader').as_heading(1)
    anchor = Anchor(header)
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}" name="{header.identifier}">
            <h1 id="{header.identifier}">someheader</h1>
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

    target = Text('someheader').as_heading(1)
    anchor = Anchor('somename').link(target)
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}" href="#{target.identifier}">
            somename
        </a>
    ''')
    assert actual == expected


@pytest.mark.anchor
def test_toggle_anchor():
    target = Dialog('sometitle', 'somecontent')
    anchor = Anchor('somename').toggle(target)
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}"
            href="#{target.identifier}"
            data-bs-toggle="modal"
            role="modal">
            somename
        </a>
    ''')
    assert actual == expected

    target = Panel()
    anchor = Anchor('somename').toggle(target)
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}"
            href="#{target.identifier}"
            data-bs-target="#{target.identifier}"
            data-bs-toggle="tab"
            role="tab">
            somename
        </a>
    ''')
    assert actual == expected

    target = Panel().as_collapse()
    anchor = Anchor('somename').toggle(target)
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}"
            href="#{target.identifier}"
            data-bs-target="#{target.identifier}"
            data-bs-toggle="collapse"
            role="collapse">
            somename
        </a>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        str(Anchor('somename').toggle(Text('sometext')))


@pytest.mark.anchor
def test_dismiss_anchor():
    anchor = Anchor('somename').dismiss()
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <a id="{anchor.identifier}"
            href="#"
            data-bs-dismiss="modal">
            somename
        </a>
    ''')
    assert actual == expected


@pytest.mark.anchor
def test_toggle_submit():
    with warnings.catch_warnings(record=True) as out:
        str(Anchor('somename').submit())
        assert len(out) > 0
        assert out[-1].category == RuntimeWarning

    anchor = Anchor('somename').submit()
    actual = HelperHTMLParser.parse(str(anchor))
    expected = HelperHTMLParser.parse(f'''
        <button id="{anchor.identifier}"
            class="btn"
            type="submit">
            somename
        </button>
    ''')
    assert actual == expected
