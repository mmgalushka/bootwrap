"""
Test for bootwrap/components/link.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Link


@pytest.mark.link
def test_link():
    link = Link('somelink')
    d = pq(str(link))
    assert d == d('link')
    assert 'somelink' in d.attr('href')
    assert 'stylesheet' in d.attr('rel')
    assert 'text/css' in d.attr('type')

    link = Link('somelink', 'somerel', 'sometype')
    d = pq(str(link))
    assert d == d('link')
    assert 'somelink' in d.attr('href')
    assert 'somerel' in d.attr('rel')
    assert 'sometype' in d.attr('type')
