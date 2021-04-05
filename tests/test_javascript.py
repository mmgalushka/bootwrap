"""
Test for bootwrap/components/javascript.py
"""

import pytest

from bootwrap import Javascript, WebComponent
from .helper import HelperHTMLParser


@pytest.mark.javascript
def test_javascript():
    javascript = Javascript('someurl')
    actual = HelperHTMLParser.parse(str(javascript))
    expected = HelperHTMLParser.parse('''
        <script src="someurl" type="application/javascript"></script>
    ''')
    assert actual == expected

    target1 = WebComponent()
    target2 = 'something'
    javascript = Javascript(
        script='a=_target1_, b=_target2_',
        submap={
            '_target1_': target1,
            '_target2_': target2
        }
    )
    actual = HelperHTMLParser.parse(str(javascript))
    expected = HelperHTMLParser.parse(f'''
        <script type="application/javascript">
            a={target1.identifier}, b={target2}
        </script>
    ''')
    assert actual == expected
