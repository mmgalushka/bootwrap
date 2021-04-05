"""
Test for bootwrap/components/image.py
"""

import pytest

from bootwrap import Icon, Spinner
from .helper import HelperHTMLParser


@pytest.mark.icon
def test_icon():
    icon = Icon('fab fa-google').as_primary()
    actual = HelperHTMLParser.parse(str(icon))
    expected = HelperHTMLParser.parse(f'''
        <i id={icon.identifier} class="fab fa-google text-primary"></i>
    ''')
    assert actual == expected


@pytest.mark.icon
def test_spinner():
    spinner = Spinner().as_primary()
    actual = HelperHTMLParser.parse(str(spinner))
    expected = HelperHTMLParser.parse(f'''
        <span id="{spinner.identifier}"
            class="spinner text-primary">
        </span>
    ''' + '''
        <style>
            @keyframes spinner-border {
                to { transform: rotate(360deg); }
            }

            .spinner{
                display: inline-block;
                vertical-align: text-bottom;
                height: 16px;
                width: 16px;
                border: .15em solid currentColor;
                border-right-color: transparent;
                border-radius: 50%;
                -webkit-animation: spinner-border .75s linear infinite;
                animation: spinner-border .75s linear infinite;
            }
        </style>
    ''')
    assert actual == expected
