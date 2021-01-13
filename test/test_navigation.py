"""
Test for bootwrap/components/menu.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Navigation, Text


@pytest.mark.navigation
def test_navigation():
    navigation = Navigation(
        Navigation.Item('A', Text('a-text'), True),
        Navigation.Item('B', Text('b-text'), False)
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
    assert set(d_li_0_a.attr('class').split(' ')) == set(['nav-link', 'active'])
    assert d_li_0_a.attr('data-toggle') == 'tab' 
    assert d_li_0_a.attr('role') == 'tab' 
    assert d_li_0_a.text() == 'A'

    target = d_li_0_a.attr('href')[1:]
    d_div_0 = pq(d(f'div[id="{target}"]'))
    assert set(d_div_0.attr('class').split(' ')) == set(['tab-pane', 'fade', 'active', 'show'])
    assert d_div_0.text() == 'a-text' 

    # test for item B;
    d_li_1 = pq(d_ul('li').eq(1))
    assert d_li_1.attr('class') == 'nav-item'

    d_li_1_a = pq(d_li_1('a'))
    assert set(d_li_1_a.attr('class').split(' ')) == set(['nav-link'])
    assert d_li_1_a.attr('data-toggle') == 'tab' 
    assert d_li_1_a.attr('role') == 'tab' 
    assert d_li_1_a.text() == 'B'

    target = d_li_1_a.attr('href')[1:]
    d_div_1 = pq(d(f'div[id="{target}"]'))
    assert set(d_div_1.attr('class').split(' ')) == set(['tab-pane', 'fade'])
    assert d_div_1.text() == 'b-text'


@pytest.mark.navigation
def test_navigation_vertical():
    navigation = Navigation().\
        as_vertical()
    d = pq(str(navigation))

    d_div = pq(d('div'))
    assert d_div.attr('class') == 'd-flex'


@pytest.mark.navigation
def test_navigation_tabs():
    navigation = Navigation().\
        as_tabs()

    d = pq(str(navigation))

    d_ul = pq(d('ul'))
    assert set(d_ul.attr('class').split(' ')) == set(['nav', 'nav-tabs'])


@pytest.mark.navigation
def test_navigation_pills():
    navigation = Navigation().\
        as_pills()

    d = pq(str(navigation))

    d_ul = pq(d('ul'))
    assert set(d_ul.attr('class').split(' ')) == set(['nav', 'nav-pills'])