"""
Test for bootwrap/components/menu.py
"""

import pytest

from bootwrap import Menu, Anchor, Button, Text, Image
from .helper import HelperHTMLParser


@pytest.mark.menu
def test_menu():
    logo = Image('samelogo')
    brand = Text('somebrand')
    anchor1 = Anchor('Menu1')
    anchor2 = Anchor('Menu2')
    button1 = Button('Action1').as_primary()
    button2 = Button('Action2').as_primary().as_outline()

    menu = Menu(logo, brand, [anchor1, anchor2], [button1, button2])
    actual = HelperHTMLParser.parse(str(menu))
    expected = HelperHTMLParser.parse(f'''
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
            <img id="{logo.identifier}" src="samelogo"/>
            <span id="{brand.identifier}">somebrand</span>
            <button class="navbar-toggler"
                type="button" data-toggle="collapse"
                data-target="#menu"
                aria-controls="menu"
                aria-expanded="false"
                aria-label="Toggle menu">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="menu">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a id="{anchor1.identifier}" class="nav-link ml-2">
                            Menu1
                        </a>
                    </li>
                    <li class="nav-item">
                        <a id="{anchor2.identifier}" class="nav-link ml-2">
                            Menu2
                        </a>
                    </li>
                </ul>

                <button id="{button1.identifier}"
                    class="btn btn-primary ml-2">
                    Action1
                </button>
                <button id="{button2.identifier}"
                    class="btn btn-outline-primary ml-2">
                    Action2
                </button>
            </div>
        </nav>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        str(Menu(Image('samelogo'), list()))
