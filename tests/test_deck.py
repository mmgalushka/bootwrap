"""
Test for bootwrap/components/collection.py
"""

import pytest

from bootwrap import Deck, Button, Icon, Text
from .helper import HelperHTMLParser


@pytest.mark.deck
def test_deck_card():
    # Tests a default deck card.
    card = Deck.Card(
        'sometitle',
        description='somedescr',
        figure=Icon('someicon'),
        marker="somemarker",
    )
    actual = HelperHTMLParser.parse(str(card))
    expected = HelperHTMLParser.parse(f'''
        <div id="{card.identifier}" class="card">
            <a>
                <i id="..." class="card-img-top someicon"></i>
            </a>
            <div class="card-body">
                <div class="text-right mb-2">
                    <small id="..." class="text-muted">somemarker</small>
                </div>
                <h5 id="..."
                    class="card-title">
                    sometitle
                </h5>
                somedescr
            </div>
        </div>
    ''')
    assert actual == expected

    # Tests a custom deck card.
    card = Deck.Card(
        Text('sometitle'),
        description=Text('somedescr'),
        figure=Icon('someicon'),
        marker=Text("somemarker")
    )
    actual = HelperHTMLParser.parse(str(card))
    expected = HelperHTMLParser.parse(f'''
        <div id="{card.identifier}" class="card">
            <a>
                <i id="..." class="card-img-top someicon"></i>
            </a>
            <div class="card-body">
                <div class="text-right mb-2">
                    <span id="...">somemarker</span>
                </div>
                <span id="..." class="card-title">sometitle</span>
                <span id="..." >somedescr</span>
            </div>
        </div>
    ''')
    assert actual == expected

    # Tests an unpacked deck card actions.
    actions = [Button('A'), Button('B')]
    card = Deck.Card('sometitle').add_menu(*actions)
    actual = HelperHTMLParser.parse(str(card))
    expected = HelperHTMLParser.parse(f'''
        <div id="{card.identifier}" class="card">
            <a></a>
            <div class="card-body">
                <h5 id="..." class="card-title">
                    sometitle
                </h5>
            </div>
            <div class="card-footer text-right">
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
        </div>
    ''')
    assert actual == expected

    # Tests a packed deck card actions.
    actions = [Button('A'), Button('B')]
    card = Deck.Card('sometitle').add_menu(*actions).pack_actions()
    actual = HelperHTMLParser.parse(str(card))
    expected = HelperHTMLParser.parse(f'''
        <div id="{card.identifier}" class="card">
            <a></a>
            <div class="card-body">
                <h5 id="..." class="card-title">
                    sometitle
                </h5>
            </div>
            <div class="card-footer text-right">
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
            </div>
        </div>
    ''')
    assert actual == expected

    # Tests a linked deck card.
    card = Deck.Card(
        'sometitle',
        description='somedescr',
        figure=Icon('someicon'),
        marker="somemarker",
    ).link('somewhere')
    actual = HelperHTMLParser.parse(str(card))
    expected = HelperHTMLParser.parse(f'''
        <div id="{card.identifier}" class="card">
            <a onclick="location.href='somewhere';">
                <i id="..." class="someicon card-img-top"></i>
            </a>
            <div class="card-body"  onclick="location.href='somewhere';">
                <div class="text-right mb-2">
                    <small id="..." class="text-muted">somemarker</small>
                </div>
                <h5 id="..."
                    class="card-title">
                    sometitle
                </h5>
                somedescr
            </div>
        </div>
    ''')
    assert actual == expected


@pytest.mark.deck
def test_deck():
    dk = Deck(
        Deck.Card('sometitle1'),
        Deck.Card('sometitle2'),
        Deck.Card('sometitle3')
    )
    actual = HelperHTMLParser.parse(str(dk))
    expected = HelperHTMLParser.parse(f'''
        <div id="{dk.identifier}" class="card-deck grid-container">
            <div id="..." class="card">
                <a></a>
                <div class="card-body">
                    <h5 id="..." class="card-title">sometitle1</h5>
                </div>
            </div>
            <div id="..." class="card">
                <a></a>
                <div class="card-body">
                    <h5 id="..." class="card-title">sometitle2</h5>
                </div>
            </div>
            <div id="..." class="card">
                <a></a>
                <div class="card-body">
                    <h5 id="..." class="card-title">sometitle3</h5>
                </div>
            </div>
        </div>
    ''' + '''
        <style>
            div.card {
                cursor:pointer
            }
        </style>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        Deck("somecard")
