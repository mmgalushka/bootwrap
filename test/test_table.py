"""
Test for bootwrap/components/table.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Table


@pytest.mark.table
def test_table():
    table = Table(['A', 'B'], [[1,2], [3,4]]).add_classes('someclass')
    d = pq(str(table))
    assert d == d('table')
    assert len(d.attr('class').split(' ')) == 2
    assert 'table' in d.attr('class')
    assert 'someclass' in d.attr('class')

    d_thead = pq(d('thead'))

    d_thead_tr = pq(d_thead('tr'))
    
    d_thead_tr_th_0 = pq(d_thead_tr('th')).eq(0)
    assert d_thead_tr_th_0.attr('scope') == 'col'
    assert d_thead_tr_th_0.text().strip() == 'A'

    d_thead_tr_th_1 = pq(d_thead_tr('th')).eq(1)
    assert d_thead_tr_th_1.attr('scope') == 'col'
    assert d_thead_tr_th_1.text().strip() == 'B'

    d_tbody = pq(d('tbody'))

    d_tbody_tr_0 = pq(d_tbody('tr')).eq(0)
    
    d_tbody_tr_0_td_0 = pq(d_tbody_tr_0('td')).eq(0)
    assert d_tbody_tr_0_td_0.attr('scope') == 'row'
    assert d_tbody_tr_0_td_0.text().strip() == '1'

    d_tbody_tr_0_td_1 = pq(d_tbody_tr_0('td')).eq(1)
    assert d_tbody_tr_0_td_1.attr('scope') is None
    assert d_tbody_tr_0_td_1.text().strip() == '2'

    d_tbody_tr_1 = pq(d_tbody('tr')).eq(1)
    
    d_tbody_tr_1_td_0 = pq(d_tbody_tr_1('td')).eq(0)
    assert d_tbody_tr_1_td_0.attr('scope') == 'row'
    assert d_tbody_tr_1_td_0.text().strip() == '3'

    d_tbody_tr_1_td_1 = pq(d_tbody_tr_1('td')).eq(1)
    assert d_tbody_tr_1_td_1.attr('scope') is None
    assert d_tbody_tr_1_td_1.text().strip() == '4'
