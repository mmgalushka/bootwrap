"""
Test for bootwrap/components/button.py
"""

import pytest

from bootwrap import (
    WebComponent,
    ButtonGroup,
    Button,
    Panel,
    Dialog,
    Text,
    Icon
)
from .helper import HelperHTMLParser


@pytest.mark.button
def test_button():
    button = Button('Somename')
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn"
            onclick="return false;">
            Somename
        </button>
    ''')
    assert actual == expected

    button = Button('Somename').as_primary()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn btn-primary"
            onclick="return false;">
            Somename
        </button>
    ''')
    assert actual == expected

    button = Button('Somename').as_primary().as_outline()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn btn-outline-primary"
            onclick="return false;">
            Somename
        </button>
    ''')
    assert actual == expected

    button = Button('Somename').add_classes('someclass')
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn someclass"
            onclick="return false;">
            Somename
        </button>
    ''')
    assert actual == expected

    button = Button('Somename').as_disabled()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn"
            onclick="return false;"
            disabled>
            Somename
        </button>
    ''')
    assert actual == expected


@pytest.mark.button
def test_button_with_icon():
    left_button = Button('Left').with_icon(
        Icon("fa-solid fa-arrow-left")
    )
    actual = HelperHTMLParser.parse(str(left_button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{left_button.identifier}"
            class="btn"
            onclick="return false;">
            <i id="..." class="fa-solid fa-arrow-left"></i>
            Left
        </button>
    ''')
    assert actual == expected

    right_button = Button('Left').with_icon(
        Icon("fa-solid fa-arrow-left"), True
    )
    actual = HelperHTMLParser.parse(str(right_button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{right_button.identifier}"
            class="btn"
            onclick="return false;">
            Right
            <i id="..." class="fa-solid fa-arrow-left"></i>
        </button>
    ''')
    assert actual == expected



@pytest.mark.button
def test_link_button():
    button = Button('Somename').link('someurl')
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <a id="{button.identifier}"
            class="btn"
            href="someurl"
            role="button">
            Somename
        </a>
    ''')
    assert actual == expected

    target = WebComponent()
    button = Button('Somename').link(target)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <a id="{button.identifier}"
            class="btn" href="#{target.identifier}"
            role="button">
            Somename
        </a>
    ''')
    assert actual == expected

    button = Button('Somename').link('someurl').as_disabled()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <a id="{button.identifier}"
            class="btn disabled"
            href="someurl"
            role="button">
            Somename
        </a>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        str(Button('somename').toggle(Text('sometext')))


@pytest.mark.button
def test_toggle_button():
    target = Dialog('Somatitle', 'Someinfo')
    button = Button('Somename').toggle(target)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn"
            type="button"
            data-bs-toggle="modal"
            data-bs-target="#{target.identifier}"
            onclick="return false;">
            Somename
        </button>
    ''')
    assert actual == expected

    target = Panel()
    button = Button('Somename').toggle(target)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn"
            type="button"
            data-bs-toggle="tab"
            data-bs-target="#{target.identifier}"
            onclick="return false;">
            Somename
        </button>
    ''')
    assert actual == expected

    target = Panel().as_collapse()
    button = Button('Somename').toggle(target)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#{target.identifier}"
            onclick="return false;">
            Somename
        </button>
    ''')
    assert actual == expected


@pytest.mark.button
def test_dismiss_button():
    button = Button('Somename').dismiss()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn"
            type="button"
            data-bs-dismiss="modal"
            onclick="return false;">
            Somename
        </button>
    ''')
    assert actual == expected


@pytest.mark.button
def test_submit_button():
    button = Button('Somename').submit()
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse(f'''
        <button id="{button.identifier}"
            class="btn"
            type="submit">
            Somename
        </button>
    ''')
    assert actual == expected


@pytest.mark.button
def test_menu_button():
    actions = [Button('A'), Button('B')]
    button = Button('Somename').add_menu(*actions)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse('''
        <div class="btn-group">
            <button id="..."
                class="btn dropdown-toggle"
                type="button"
                data-bs-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                onclick="return false;">
                Somename
            </button>
            <div class="dropdown-menu dropdown-menu-right">
                <button id="..."
                    class="dropdown-item btn"
                    onclick="return false;">
                    A
                </button>
                <button id="..."
                    class="dropdown-item btn"
                    onclick="return false;">
                    B
                </button>
            </div>
        </div>
    ''')
    assert actual == expected

    actions = [Button('A'), Button('B')]
    button = Button('...').add_menu(*actions)
    actual = HelperHTMLParser.parse(str(button))
    expected = HelperHTMLParser.parse('''
        <div class="btn-group">
            <i id="..."
                class="btn fas fa-ellipsis-v"
                style="cursor: pointer"
                data-bs-toggle="dropdown"
                onclick="return false;">
            </i>
            <div class="dropdown-menu dropdown-menu-right">
                <button id="..."
                    class="dropdown-item btn"
                    onclick="return false;">
                    A
                </button>
                <button id="..."
                    class="dropdown-item btn"
                    onclick="return false;">
                    B
                </button>
            </div>
        </div>
    ''')
    assert actual == expected



@pytest.mark.button
def test_button_group():
    btn_a = Button('A')
    btn_b = Button('B')
    button_group = ButtonGroup( btn_a, btn_b)
    actual = HelperHTMLParser.parse(str(button_group))
    expected = HelperHTMLParser.parse('''
        <div id="..."
            class="btn-group"
            role="group">
            <button id="..."
                class="btn"
                onclick="return false;">
                A
            </button>
            <button id="..."
                class="btn"
                onclick="return false;">
                B
            </button>
        </div>
    ''')
    assert actual == expected