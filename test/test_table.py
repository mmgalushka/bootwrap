"""
Test for bootwrap/components/table.py
"""

import pytest

from bootwrap import Table

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