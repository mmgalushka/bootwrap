"""
Test for bootwrap/components/badge.py
"""

import pytest

from bootwrap import Badge
from .helper import HelperHTMLParser


@pytest.mark.badge
def test_badge():
    badge = Badge('sometext').add_classes('someclass').as_primary()
    actual = HelperHTMLParser.parse(str(badge))
    expected = HelperHTMLParser.parse(f'''
        <span id="{badge.identifier}"
            class="badge badge-primary someclass">
            sometext
        </span>
    ''')
    assert actual == expected
