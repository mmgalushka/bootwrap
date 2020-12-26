"""
Test for bootwrap/components/page.py
"""

import pytest

from pyquery import PyQuery as pq
from bootwrap import Page, Button


@pytest.mark.page
def test_page_resources():
    page = Page()
    d = pq(str(page))

    lookup = {
        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css': 0,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.min.css': 0
    }
    for link in d('link'):
        href = pq(link).attr('href')
        if href:
            lookup[href] = 1
    assert sum(lookup.values()) == 2

    lookup = {
        'https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js': 0,
        'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js': 0,
        'https://cdn.jsdelivr.net/gh/google/code-prettify@master/loader/run_prettify.js': 0

    }
    for script in d('script'):
        src = pq(script).attr('src')
        if src:
            lookup[src] = 1
    assert sum(lookup.values()) == 3


@pytest.mark.page
def test_pagefavicon():
    page = Page(favicon='somename.ico')
    d = pq(str(page))

    favicon = pq(d('link[type="image/x-icon"]'))
    assert favicon.attr('href') == 'somename.ico'


@pytest.mark.page
def test_page_title():
    page = Page(title='Some Title')
    d = pq(str(page))

    favicon = pq(d('title'))
    assert favicon.text() == 'Some Title'
