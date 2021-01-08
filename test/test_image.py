"""
Test for bootwrap/components/image.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Image


@pytest.mark.image
def test_image():
    image = Image(
        'somelink',
        width=11,
        height=22,
        alt='somename'
    )
    d = pq(str(image))
    assert d == d('img')
    assert d.attr('src') == 'somelink'
    assert d.attr('width') == '11'
    assert d.attr('height') == '22'
    assert d.attr('alt') == 'somename'


    image = Image('somelink').add_classes('mr-1')
    d = pq(str(image))
    assert d.attr('class') == 'mr-1'
