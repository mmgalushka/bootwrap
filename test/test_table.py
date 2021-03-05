"""
Test for bootwrap/components/table.py
"""

import pytest

from bootwrap import Table, TableEntity

from .helper import HelperHTMLParser


@pytest.mark.table
def test_table():
    table = Table(['A', 'B'], [[1,2], [3,4]]).add_classes('someclass')
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table someclass">
            <thead>
                <tr>
                    <th scope="col">A</th>
                    <th scope="col">B</th>
                </tr>
            </thead>
            <tbody>
                <tr><td scope="row">1</td><td>2</td></tr><tr><td scope="row">3</td><td>4</td></tr>
            </tbody>
        </table>
    ''')
    assert actual == expected


@pytest.mark.table
def test_table_head():
    table = Table(['A', 'B'], None)

    table.head.as_light()
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table">
            <thead class="thead-light">
                <tr>
                    <th scope="col">A</th>
                    <th scope="col">B</th>
                </tr>
            </thead>
        </table>
    ''')
    assert actual == expected

    table.head.as_dark()
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table">
            <thead class="thead-dark">
                <tr>
                    <th scope="col">A</th>
                    <th scope="col">B</th>
                </tr>
            </thead>
        </table>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        str(Table('somename', None))


@pytest.mark.table
def test_table_body():
    table = Table(None,  [[1,2], [3,4]])
    table.body.transform(0, TableEntity.VALUE, lambda v: 0 if v==1 else v)
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table">
            <tbody>
                <tr>
                    <td scope="row">0</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td scope="row">3</td>
                    <td>4</td>
                </tr>
            </tbody>
        </table>
    ''')
    assert actual == expected

    table = Table(None,  [[1,2], [3,4]])
    table.body.transform(0, TableEntity.CELL, lambda v: 'someclass' if v==1 else '')
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table">
            <tbody>
                <tr>
                    <td scope="row" class="someclass">1</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td scope="row">3</td>
                    <td>4</td>
                </tr>
            </tbody>
        </table>
    ''')
    assert actual == expected

    table = Table(None,  [[1,2], [3,4]])
    table.body.transform(0, TableEntity.ROW, lambda v: 'someclass' if v==1 else '')
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table">
            <tbody>
                <tr class="someclass"> 
                    <td scope="row">1</td>
                    <td>2</td>
                </tr>
                <tr>
                    <td scope="row">3</td>
                    <td>4</td>
                </tr>
            </tbody>
        </table>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        str(Table(None, 'somename'))

    with pytest.raises(ValueError):
        table = Table(None,  [[1,2], [3,4]])
        table.body.transform(0, TableEntity.VALUE, lambda v: v)
        table.body.transform(0, TableEntity.VALUE, lambda v: v)


@pytest.mark.table
def test_table_as_striped():
    table = Table(None, None).as_striped()
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table table-striped">
        </table>
    ''')
    assert actual == expected


@pytest.mark.table
def test_table_as_bordered():
    table = Table(None, None).as_bordered()
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table table-bordered">
        </table>
    ''')
    assert actual == expected


@pytest.mark.table
def test_table_as_small():
    table = Table(None, None).as_small()
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table table-sm">
        </table>
    ''')
    assert actual == expected


@pytest.mark.table
def test_table_as_dark():
    table = Table(None, None).as_dark()
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table table-dark">
        </table>
    ''')
    assert actual == expected


@pytest.mark.table
def test_table_as_responsive():
    table = Table(None, None).as_responsive()
    actual = HelperHTMLParser.parse(str(table))
    expected = HelperHTMLParser.parse(f'''
        <table id="{table.identifier}" class="table table-responsive-sm">
        </table>
    ''')
    assert actual == expected