"""
Test for bootwrap/components/image.py
"""

import pytest

from bootwrap import Separator

from .helper import HelperHTMLParser


@pytest.mark.addon
def test_separator():
    separator = Separator()
    actual = HelperHTMLParser.parse(str(separator))
    expected = HelperHTMLParser.parse('<hr/>')
    assert actual == expected
