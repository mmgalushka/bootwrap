"""
Test for bootwrap/components/collection.py
"""

import pytest

from bootwrap import List, Button, Icon, Text
from .helper import HelperHTMLParser


@pytest.mark.list
def test_list_item():
    # Tests a default list item.
    item = List.Item(
        'sometitle',
        description='somedescr',
        figure=Icon('someicon'),
        marker="somemarker",
    ).as_selected()
    actual = HelperHTMLParser.parse(str(item))
    expected = HelperHTMLParser.parse(f'''
        <a id="{item.identifier}"
            class="list-group-item list-group-item-action flex-column
                   align-items-start active">
            <div class="d-flex w-100 justify-content-between">
                <i id="..." class="someicon"> </i>
                <div class="ml-2 mr-2 w-100">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 id="...">sometitle</h5>
                        <span id="..."><small>somemarker</small></span>
                     </div>
                    somedescr
                </div>
            </div>
        </a>
    ''')
    assert actual == expected

    # Tests a custom list item.
    item = List.Item(
        Text('sometitle'),
        description=Text('somedescr'),
        figure=Icon('someicon'),
        marker=Text("somemarker")
    ).as_selected()
    actual = HelperHTMLParser.parse(str(item))
    expected = HelperHTMLParser.parse(f'''
        <a id="{item.identifier}"
            class="list-group-item list-group-item-action flex-column
                   align-items-start active">
            <div class="d-flex w-100 justify-content-between">
                <i id="..." class="someicon"> </i>
                <div class="ml-2 mr-2 w-100">
                    <div class="d-flex w-100 justify-content-between">
                        <span id="...">sometitle</span>
                        <span id="...">somemarker</span>
                     </div>
                    <span id="...">somedescr</span>
                </div>
            </div>
        </a>
    ''')
    assert actual == expected

    # Tests an unpacked list item actions.
    actions = [Button('A'), Button('B')]
    item = List.Item('sometitle').add_menu(*actions)
    actual = HelperHTMLParser.parse(str(item))
    expected = HelperHTMLParser.parse(f'''
        <a id="{item.identifier}"
            class="list-group-item list-group-item-action flex-column
                   align-items-start">
            <div class="d-flex w-100 justify-content-between">
                <div class="ml-2 mr-2 w-100">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 id="...">sometitle</h5>
                     </div>
                </div>
                <div class="d-flex align-items-start">
                    <button id="..."
                        class="ml-1 btn"
                        onclick="return false;">
                        A
                    </button>
                    <button id="..."
                        class="ml-1 btn"
                        onclick="return false;">
                        B
                    </button>
                </div>
            </div>
        </a>
    ''')
    assert actual == expected

    # Tests a packed list item actions.
    actions = [Button('A'), Button('B')]
    item = List.Item('sometitle').add_menu(*actions).pack_actions()
    actual = HelperHTMLParser.parse(str(item))
    expected = HelperHTMLParser.parse(f'''
        <a id="{item.identifier}"
            class="list-group-item list-group-item-action flex-column
                   align-items-start">
            <div class="d-flex w-100 justify-content-between">
                <div class="ml-2 mr-2 w-100">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 id="...">sometitle</h5>
                     </div>
                </div>
                <div class="d-flex align-items-start">
                    <div class="btn-group">
                        <i id="..."
                            class="btn fas fa-ellipsis-v"
                            style="cursor: pointer"
                            data-toggle="dropdown"
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
        </a>
    ''')
    assert actual == expected


@pytest.mark.list
def test_list():
    ls = List(
        List.Item('sometitle1').as_selected(),
        List.Item('sometitle2'),
        List.Item('sometitle3')
    )
    actual = HelperHTMLParser.parse(str(ls))
    expected = HelperHTMLParser.parse(f'''
        <div id="{ls.identifier}" class="list-group">
            <a id="..."
                class="list-group-item list-group-item-action flex-column
                       align-items-start active">
                <div class="d-flex w-100 justify-content-between">
                    <div class="ml-2 mr-2 w-100">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 id="...">sometitle1</h5>
                        </div>
                    </div>
                </div>
            </a>
            <a id="..."
                class="list-group-item list-group-item-action flex-column
                       align-items-start">
                <div class="d-flex w-100 justify-content-between">
                    <div class="ml-2 mr-2 w-100">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 id="...">sometitle2</h5>
                        </div>
                    </div>
                </div>
            </a>
            <a id="..."
                class="list-group-item list-group-item-action flex-column
                       align-items-start">
                <div class="d-flex w-100 justify-content-between">
                    <div class="ml-2 mr-2 w-100">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 id="...">sometitle3</h5>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        List("someitem")
