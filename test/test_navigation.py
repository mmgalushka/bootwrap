"""
Test for bootwrap/components/menu.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Navigation, Text


@pytest.mark.navigation
def test_navigation():
    navigation = Navigation().\
        append(
            ('A', Text('a-text'), True),
            ('B', Text('b-text'), False)
        )

    d = pq(str(navigation))

    d_ul = pq(d('ul'))
    assert d_ul.attr('id') == navigation.identifier
    assert d_ul.attr('class') == 'nav'
    assert d_ul.attr('role') == 'tablist'

    # test for item A;
    d_li_0 = pq(d_ul('li').eq(0))
    assert d_li_0.attr('class') == 'nav-item'

    d_li_0_a = pq(d_li_0('a'))
    assert 'nav-link' in d_li_0_a.attr('class')
    assert 'active' in d_li_0_a.attr('class') 
    assert d_li_0_a.attr('data-toggle') == 'tab' 
    assert d_li_0_a.attr('role') == 'tab' 
    assert d_li_0_a.text() == 'A'

    target = d_li_0_a.attr('href')[1:]
    d_div_0 = pq(d(f'div[id="{target}"]'))
    assert 'tab-pane' in d_div_0.attr('class')
    assert 'fade' in d_div_0.attr('class') 
    assert 'active' in d_div_0.attr('class') 
    assert 'show' in d_div_0.attr('class') 
    assert d_div_0.text() == 'a-text' 

    # test for item B;
    d_li_1 = pq(d_ul('li').eq(1))
    assert d_li_1.attr('class') == 'nav-item'

    d_li_1_a = pq(d_li_1('a'))
    assert 'nav-link' in d_li_1_a.attr('class')
    assert 'active' not in d_li_1_a.attr('class') 
    assert d_li_1_a.attr('data-toggle') == 'tab' 
    assert d_li_1_a.attr('role') == 'tab' 
    assert d_li_1_a.text() == 'B'

    target = d_li_1_a.attr('href')[1:]
    d_div_1 = pq(d(f'div[id="{target}"]'))
    assert 'tab-pane' in d_div_1.attr('class')
    assert 'fade' in d_div_1.attr('class') 
    assert 'active' not in d_div_1.attr('class') 
    assert 'show' not in d_div_1.attr('class') 
    assert d_div_1.text() == 'b-text'

    with pytest.raises(TypeError) as err:
        Navigation().append(None)
    assert '<class "tuple">' in str(err.value)

    with pytest.raises(TypeError) as err:
        Navigation().append((None, Text('a-text'), True))
    assert '"components[0][0]"' in str(err.value)
    assert '<class "str">' in str(err.value)

    with pytest.raises(TypeError) as err:
        Navigation().append(('A', None, True))
    assert '"components[0][1]"' in str(err.value)
    assert '<class "WebComponent">' in str(err.value)

    with pytest.raises(TypeError) as err:
        Navigation().append(('A', Text('a-text'), None))
    assert '"components[0][2]"' in str(err.value)
    assert '<class "bool">' in str(err.value)



@pytest.mark.navigation
def test_navigation_vertical():
    navigation = Navigation().\
        as_vertical().\
        append(
            ('A', Text('a-text'), True),
            ('B', Text('b-text'), False)
        )

    d = pq(str(navigation))

    d_div = pq(d('div'))
    assert 'd-flex' in d_div.attr('class')


@pytest.mark.navigation
def test_navigation_tabs():
    navigation = Navigation().\
        as_tabs().\
        append(
            ('A', Text('a-text'), True),
            ('B', Text('b-text'), False)
        )

    d = pq(str(navigation))

    d_ul = pq(d('ul'))
    assert 'nav-tabs' in d_ul.attr('class')


@pytest.mark.navigation
def test_navigation_pills():
    navigation = Navigation().\
        as_pills().\
        append(
            ('A', Text('a-text'), True),
            ('B', Text('b-text'), False)
        )

    d = pq(str(navigation))

    d_ul = pq(d('ul'))
    assert 'nav-pills' in d_ul.attr('class')