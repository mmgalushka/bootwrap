"""
Test for bootwrap/components/image.py
"""

import pytest

from bootwrap import Image

from .helper import HelperHTMLParser


@pytest.mark.image
def test_image():
    image = Image('somelink', width=11, height=22, alt='somename').\
        add_classes('someclass')
    actual = HelperHTMLParser.parse(str(image))
    expected = HelperHTMLParser.parse(f'''
        <img id="{image.identifier}" class="someclass" src="somelink"
            width=11 height=22 alt="somename"/>
    ''')
    assert actual == expected
