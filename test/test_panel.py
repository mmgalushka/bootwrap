"""
Test for bootwrap/components/panel.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Panel, Text


@pytest.mark.panel
def test_panel():
    panel = Panel()
    d = pq(str(panel))
    assert d == d('div')
    assert d.attr('class') is None

    panel = Panel(Text('sometext'))
    d = pq(str(panel))
    assert d.text() == 'sometext'

    panel = Panel().add_classes('mr-1')
    d = pq(str(panel))
    assert  d.attr('class') == 'mr-1'
