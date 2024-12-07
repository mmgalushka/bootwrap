"""
Test for bootwrap/components/panel.py
"""

import pytest

from bootwrap import Panel, Text
from .helper import HelperHTMLParser


@pytest.mark.panel
def test_panel():
    text = Text('sometext')
    panel = Panel(text).add_classes('someclass')
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}" class="someclass">
            <span id="{text.identifier}">sometext</span>
        </div>
    ''')
    assert actual == expected


@pytest.mark.panel
def test_panel_appearance():
    panel = Panel().as_primary()
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}" class="bg-primary">
        </div>
    ''')
    assert actual == expected

@pytest.mark.panel
def test_panel_outline():
    panel = Panel().as_outline()
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}" class="border">
        </div>
    ''')
    assert actual == expected

    panel = Panel().as_primary().as_outline()
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}" class="border border-primary">
        </div>
    ''')
    assert actual == expected

@pytest.mark.panel
def test_panel_justify_content():
    panel = Panel().justify_content('start')
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}" class="d-flex justify-content-start">
        </div>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        Panel().justify_content(0)

    with pytest.raises(ValueError):
        Panel().justify_content("xyz")


@pytest.mark.panel
def test_panel_align_items():
    panel = Panel().align_items('start')
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}" class="d-flex align-items-start">
        </div>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        Panel().align_items(0)

    with pytest.raises(ValueError):
        Panel().align_items("xyz")


@pytest.mark.panel
def test_iter():
    text1 = Text('sometext1')
    text2 = Text('sometext2')
    text3 = Text('sometext3')
    panel = Panel(text1, text2, text3)
    for actual, expected in zip(panel, [text1, text2, text3]):
        assert actual == expected


@pytest.mark.panel
def test_horizontal_panel():
    text1 = Text('sometext1')
    text2 = Text('sometext2')
    text3 = Text('sometext3')
    panel = Panel(text1, text2, text3).horizontal()
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}">
            <div class="row">
                <div class="col-md">
                    <span id="{text1.identifier}">sometext1</span>
                </div>
                <div class="col-md">
                    <span id="{text2.identifier}">sometext2</span>
                </div>
                <div class="col-md">
                    <span id="{text3.identifier}">sometext3</span>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected


@pytest.mark.panel
def test_vertical_panel():
    text1 = Text('sometext1')
    text2 = Text('sometext2')
    text3 = Text('sometext3')
    panel = Panel(text1, text2, text3).vertical()
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}">
            <div class="row">
                <div class="col-md">
                    <span id="{text1.identifier}">sometext1</span>
                </div>
            </div>
            <div class="row">
                <div class="col-md">
                    <span id="{text2.identifier}">sometext2</span>
                </div>
            </div>
            <div class="row">
                <div class="col-md">
                    <span id="{text3.identifier}">sometext3</span>
                </div>
            </div>
        </div>
    ''')
    assert actual == expected


@pytest.mark.panel
def test_as_collapse():
    panel = Panel().as_collapse()
    actual = HelperHTMLParser.parse(str(panel))
    expected = HelperHTMLParser.parse(f'''
        <div id="{panel.identifier}" class="collapse"></div>
    ''')
    assert actual == expected
