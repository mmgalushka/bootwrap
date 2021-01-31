"""
Test for bootwrap/components/text.py
"""

import pytest

from bootwrap import Text

from .helper import HelperHTMLParser


@pytest.mark.text
def test_text():
    text = Text('sometext').add_classes('someclass').as_primary()
    actual = HelperHTMLParser.parse(str(text))
    expected = HelperHTMLParser.parse(f'''
        <span id="{text.identifier}" class="text-primary someclass">
            sometext
        </span>
    ''')
    assert actual == expected

@pytest.mark.text
def test_text_paragraph():
    text = Text('sometext').add_classes('someclass').as_primary().as_paragraph()
    actual = HelperHTMLParser.parse(str(text))
    expected = HelperHTMLParser.parse(f'''
        <p id="{text.identifier}" class="text-primary someclass">
            sometext
        </p>
    ''')
    assert actual == expected


@pytest.mark.text
def test_text_strong():
    text = Text('sometext').add_classes('someclass').as_primary().as_strong()
    actual = HelperHTMLParser.parse(str(text))
    expected = HelperHTMLParser.parse(f'''
        <span id="{text.identifier}" class="text-primary someclass">
            <strong>sometext</strong>
        </span>
    ''')
    assert actual == expected


@pytest.mark.text
def test_text_small():
    text = Text('sometext').add_classes('someclass').as_primary().as_small()
    actual = HelperHTMLParser.parse(str(text))
    expected = HelperHTMLParser.parse(f'''
        <span id="{text.identifier}" class="text-primary someclass">
            <small>sometext</small>
        </span>
    ''')
    assert actual == expected
