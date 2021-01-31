"""
Test for bootwrap/components/link.py
"""

import pytest

from bootwrap import Link

from .helper import HelperHTMLParser


@pytest.mark.link
def test_link():
    link = Link('somelink')
    actual = HelperHTMLParser.parse(str(link))
    expected = HelperHTMLParser.parse(f'''
        <link rel="stylesheet" type="text/css" href="somelink"/>
    ''')
    assert actual == expected

    link = Link('somelink', 'somerel', 'sometype')
    actual = HelperHTMLParser.parse(str(link))
    expected = HelperHTMLParser.parse(f'''
        <link rel="somerel" type="sometype" href="somelink"/>
    ''')
    assert actual == expected
