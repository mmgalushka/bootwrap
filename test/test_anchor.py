"""
Test for bootwrap/components/anchor.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Anchor, WebComponent


@pytest.mark.anchor
def test_anchor():
    anchor = Anchor('somename', 'somerole').add_classes('someclass').as_primary()
    d = pq(str(anchor))
    assert d == d('a')
    assert len(d.attr('class').split(' ')) == 2
    assert 'text-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')
    assert d.attr('href')  == '#'
    assert d.attr('role')  == 'somerole'
    assert d.text().strip() == 'somename'
    
    target = WebComponent()
    anchor = Anchor('somename').toggle(target)
    d = pq(str(anchor))
    assert d.attr('href')  == '#' + str(target.identifier)
    assert d.attr('data-toggle')  == 'tab'
