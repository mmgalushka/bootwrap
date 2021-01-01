"""
Test for bootwrap/components/menu.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Menu, Anchor, Button, Text, Image


@pytest.mark.menu
def test_menu():
    menu = Menu(
        Image('samelogo'),
        Text('somebrand'),
        [
            Anchor('Menu1'),
            Anchor('Menu2')
        ],
        [
            Button('Action1').as_primary().as_outline(),
            Button('Action2').as_primary().as_outline()
        ]
    )
    d = pq(str(menu))
    assert d == d('nav')
    assert 'navbar' in d.attr('class')
    assert 'navbar-expand-lg' in d.attr('class')
    assert 'navbar-dark' in d.attr('class')
    assert 'bg-dark' in d.attr('class')
    assert 'fixed-top' in d.attr('class')

    # test menu logo image;
    d_img = pq(d('img'))
    assert d_img.attr('src') == 'samelogo'
    
    # test menu brand label;
    assert 'somebrand' in d.text()

    # test menu anchors...
    d_div = pq(d('div[class="collapse navbar-collapse"]'))
    identifier = d_div.attr('id')

    d_div_ul = pq(d_div('ul'))
    assert 'navbar-nav' in d_div_ul.attr('class')
    assert 'mr-auto' in d_div_ul.attr('class')

    d_div_ul_li_0 = pq(d_div_ul('li')).eq(0)
    assert 'nav-item' in d_div_ul_li_0.attr('class')

    d_div_ul_li_0_a = pq(d_div_ul_li_0('a'))
    assert d_div_ul_li_0_a.text() == 'Menu1'

    d_div_ul_li_1 = pq(d_div_ul('li')).eq(1)
    assert 'nav-item' in d_div_ul_li_1.attr('class')

    d_div_ul_li_1_a = pq(d_div_ul_li_1('a'))
    assert d_div_ul_li_1_a.text() == 'Menu2'

    # Tests collapsing block -> main menu...
    collapse_actions = d_div('a[class="btn btn-outline-primary ml-2"]')
    assert len(collapse_actions) == 2

    # test menu action buttons...
    d_a_0 = pq(d('a[role="button"]')).eq(0)
    assert d_a_0.text() == 'Action1'

    d_a_1 = pq(d('a[role="button"]')).eq(1)
    assert d_a_1.text() == 'Action2'

    # test toggle button
    d_toggle = pq(d('button[class="navbar-toggler"]'))
    assert d_toggle.attr('type') == 'button'
    assert d_toggle.attr('data-toggle') == 'collapse'
    assert d_toggle.attr('data-target') == f'#{identifier}'
    assert d_toggle.attr('aria-controls') == f'{identifier}'
    assert d_toggle.attr('aria-expanded') == 'false'
    assert d_toggle.attr('aria-label') == 'Toggle menu'
    
    d_toggle_icon = pq(d_toggle('span'))
    assert d_toggle_icon.attr('class') == 'navbar-toggler-icon'