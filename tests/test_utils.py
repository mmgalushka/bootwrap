"""
Test for bootwrap/components/link.py
"""

import pytest

from bootwrap import attr, inject, Text

from .helper import HelperHTMLParser


@pytest.mark.utils
def test_attr():
    output = attr('name', True)
    assert output == 'name'

    output = attr('name', 1)
    assert output == 'name=1'

    output = attr('name', '1')
    assert output == 'name="1"'

    output = attr('name', None)
    assert output == ''

    output = attr('name', None)
    assert output == ''

    with pytest.raises(TypeError):
        attr('name', list())


@pytest.mark.utils
def test_inject():
    output = inject(Text('A'), Text('B'), Text('C'))
    actual = HelperHTMLParser.parse(output)
    expected = HelperHTMLParser.parse('''
        <span id="...">A</span>
        <span id="...">B</span>
        <span id="...">C</span>
    ''')
    assert actual == expected

    output = inject(Text('A'), None, Text('C'))
    actual = HelperHTMLParser.parse(output)
    expected = HelperHTMLParser.parse('''
        <span id="...">A</span>
        <span id="...">C</span>
    ''')
    assert actual == expected
