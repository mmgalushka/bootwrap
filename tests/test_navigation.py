"""
Test for bootwrap/components/menu.py
"""

import pytest

from bootwrap import Navigation, Text
from .helper import HelperHTMLParser


@pytest.mark.navigation
def test_navigation():
    textA = Text('a-text')
    itemA = Navigation.Item('A', textA, True)
    textB = Text('b-text')
    itemB = Navigation.Item('B', textB, False)

    navigation = Navigation(itemA, itemB)
    actual = HelperHTMLParser.parse(str(navigation))
    expected = HelperHTMLParser.parse(f'''
        <ul id="{navigation.identifier}" class="nav" role="tablist">
            <li class="nav-item">
                <a id="..."
                    class="nav-link active"
                    href="..."
                    data-bs-target="..."
                    data-bs-toggle="tab"
                    role="tab">
                    A
                </a>
            </li>
            <li class="nav-item">
                <a id="..."
                    class="nav-link"
                    href="..."
                    data-bs-target="..."
                    data-bs-toggle="tab"
                    role="tab">
                    B
                </a>
            </li>
        </ul>
        <div class="tab-content">
            <div id="..."
                class="show active tab-pane fade">
                <span id="{textA.identifier}">a-text</span>
            </div>
            <div id="..."
                class="tab-pane fade">
                <span id="{textB.identifier}">b-text</span>
            </div>
        </div>
    ''')
    assert len(actual) == 2
    assert len(expected) == 2
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]


@pytest.mark.navigation
def test_navigation_vertical():
    navigation = Navigation().as_vertical()

    actual = HelperHTMLParser.parse(str(navigation))
    expected = HelperHTMLParser.parse(f'''
        <div class="d-flex">
            <ul id="{navigation.identifier}"
                class="nav flex-column"
                role="tablist">
            </ul>
            <div class="tab-content"></div>
        </div>
    ''')
    assert actual == expected


@pytest.mark.navigation
def test_navigation_tabs():
    navigation = Navigation().\
        as_tabs()

    actual = HelperHTMLParser.parse(str(navigation))
    expected = HelperHTMLParser.parse(f'''
        <ul id="{navigation.identifier}"
            class="nav nav-tabs"
            role="tablist">
        </ul>
        <div class="tab-content"></div>
    ''')
    assert len(actual) == 2
    assert len(expected) == 2
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]


@pytest.mark.navigation
def test_navigation_pills():
    navigation = Navigation().as_pills()

    actual = HelperHTMLParser.parse(str(navigation))
    expected = HelperHTMLParser.parse(f'''
        <ul id="{navigation.identifier}"
            class="nav nav-pills"
            role="tablist">
        </ul>
        <div class="tab-content"></div>
    ''')
    assert len(actual) == 2
    assert len(expected) == 2
    assert actual[0] == expected[0]
    assert actual[1] == expected[1]
