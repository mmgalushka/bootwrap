"""
Test for bootwrap/components/javascript.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Javascript, WebComponent


@pytest.mark.javascript
def test_javascript():
    javascript = Javascript('some-src')
    d = pq(str(javascript))
    assert d == d('script')
    assert 'some-src' in d.attr('src')
    assert 'application/javascript' in d.attr('type')

    target1 = WebComponent()
    target2 = 'something'
    javascript = Javascript(
        script = 'a=_target1_, b=_target2_',
        submap = {
            '_target1_': target1,
            '_target2_': target2
        }
    )
    d = pq(str(javascript))
    assert d == d('script')
    assert d.attr('src') is None
    assert d.text().strip() == f'a={target1.identifier}, b={target2}'