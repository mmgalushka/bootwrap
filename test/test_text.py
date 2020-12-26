"""
Test for bootwrap/components/text.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Text


@pytest.mark.text
def test_text():
    text = Text('sometext').add_classes('someclass').as_primary()
    d = pq(str(text))
    assert len(d.attr('class').split(' ')) == 2
    assert 'text-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')
    assert d.text().strip() == 'sometext'


@pytest.mark.text
def test_text_paragraph():
    text = Text('sometext').add_classes('someclass').as_primary().as_paragraph()
    d = pq(str(text))
    assert d == d('p')
    assert len(d.attr('class').split(' ')) == 2
    assert 'text-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')
    assert d.text().strip() == 'sometext'


@pytest.mark.text
def test_text_strong():
    text = Text('sometext').add_classes('someclass').as_primary().as_strong()
    d = pq(str(text))
    assert d == d('span')
    assert len(d.attr('class').split(' ')) == 2
    assert 'text-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_strong = pq(d('strong'))
    assert d_strong.text().strip() == 'sometext'


@pytest.mark.text
def test_text_small():
    text = Text('sometext').add_classes('someclass').as_primary().as_small()
    d = pq(str(text))
    assert d == d('span')
    assert len(d.attr('class').split(' ')) == 2
    assert 'text-primary' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_small = pq(d('small'))
    assert d_small.text().strip() == 'sometext'