"""
Test for bootwrap/components/link.py
"""

import pytest

from bootwrap import List, Icon, Text

from .helper import HelperHTMLParser


@pytest.mark.list
def test_default_list_item():
    item = List.Item(
        'sometitle',
        description= 'somedescr',
        icon=Icon('someicon'),
        marker="somemarker",
        custom=Text('sometext')
    ).as_active()
    actual = HelperHTMLParser.parse(str(item))
    expected = HelperHTMLParser.parse(f'''
        <a id="{item.identifier}"
            class="list-group-item list-group-item-action flex-column align-items-start active">
            <div class="d-flex w-100 justify-content-between">    
                <i id="..." class="someicon"></i>
                <div class="ml-2 mr-2 w-100">
                    <div class="d-flex w-100 justify-content-between">   
                        <h6 id="...">
                            sometitle
                        </h6>  
                        <span id="..." class="text-secondary">
                            <small>somemarker</small>
                        </span>
                    </div>
                    <span id="...">
                        <small>somedescr</small>
                    </span>    
                </div>
                <span id="...">
                    sometext
                </span>        
            </div>    
        </a>
    ''')
    assert actual == expected

@pytest.mark.list
def test_default_custom_item():
    item = List.Item(
        Text('sometitle'),
        description= Text('somedescr'),
        icon=Icon('someicon'),
        marker=Text("somemarker"),
        custom=Text('sometext')
    ).as_active()
    actual = HelperHTMLParser.parse(str(item))
    expected = HelperHTMLParser.parse(f'''
        <a id="{item.identifier}"
            class="list-group-item list-group-item-action flex-column align-items-start active">
            <div class="d-flex w-100 justify-content-between">     
                <i id="..." class="someicon"></i>
                <div class="ml-2 mr-2 w-100">
                    <div class="d-flex w-100 justify-content-between">      
                        <span id="...">sometitle</span>    
                        <span id="...">somemarker</span>
                    </div>
                    <span id="...">somedescr</span>
                </div>
                <span id="...">sometext</span>
            </div>
        </a>
    ''')
    assert actual == expected


@pytest.mark.list
def test_list():
    ls = List(
        List.Item('sometitle1').as_active(),
        List.Item('sometitle2'),
        List.Item('sometitle3')
    )
    actual = HelperHTMLParser.parse(str(ls))
    expected = HelperHTMLParser.parse(f'''
        <div class="list-group">
            <a id="..." class="list-group-item list-group-item-action flex-column align-items-start active">
                <div class="d-flex w-100 justify-content-between">
                    <div class="ml-2 mr-2 w-100">
                        <div class="d-flex w-100 justify-content-between">            
                            <h6 id="...">sometitle1</h6>
                        </div>
                    </div>   
                </div>
            </a>
            <a id="..." class="list-group-item list-group-item-action flex-column align-items-start">
                <div class="d-flex w-100 justify-content-between">
                    <div class="ml-2 mr-2 w-100">
                        <div class="d-flex w-100 justify-content-between">            
                            <h6 id="...">sometitle2</h6>
                        </div>
                    </div>   
                </div>
            </a>
            <a id="..." class="list-group-item list-group-item-action flex-column align-items-start">
                <div class="d-flex w-100 justify-content-between">
                    <div class="ml-2 mr-2 w-100">
                        <div class="d-flex w-100 justify-content-between">            
                            <h6 id="...">sometitle3</h6>
                        </div>
                    </div>   
                </div>
            </a>
        </div>
    ''')
    assert actual == expected