"""
Test for bootwrap/components/page.py
"""

import pytest

from bootwrap import Page, Button, Link, Javascript, Menu, Text

from .helper import HelperHTMLParser


@pytest.mark.page
def test_page_resources():
    page = Page(
        favicon='somename.ico',
        resources=[
            Link('https//someresource.com/some.css'),
            Javascript('https//someresource.com/some.js')
        ],
        title='Some Title',
        menu=Menu(logo='somelogo.jpg'),
        content=[Text('sometext')]
    )
    actual = HelperHTMLParser.parse(page.__html__())
    expected = HelperHTMLParser.parse(f'''
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
                
                <link rel="stylesheet"
                    type="text/css"
                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"/>
                <link rel="stylesheet"
                    type="text/css"
                    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.min.css"/>
                <link rel="stylesheet"
                    type="text/css"
                    href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/styles/default.min.css"/>
                <link rel="icon" type="image/x-icon" href="somename.ico"/>
                <link rel="stylesheet" type="text/css" href="https//someresource.com/some.css"/>

                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"
                    type="application/javascript">
                </script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
                    type="application/javascript">
                </script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/highlight.min.js"
                    type="application/javascript">
                </script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/languages/python.min.js"
                    type="application/javascript">
                </script>
                <script src="https//someresource.com/some.js"
                    type="application/javascript">
                </script>

                <title>Some Title</title>
            </head>
            <body>
                <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
                    somelogo.jpg
                    <button class="navbar-toggler"
                        type="button" data-toggle="collapse"
                        data-target="#menu"
                        aria-controls="menu"
                        aria-expanded="false"
                        aria-label="Toggle menu">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    
                    <div class="collapse navbar-collapse" id="menu">
                        <ul class="navbar-nav mr-auto"></ul>
                    </div>
                </nav>
                <div class="container" style="margin-top: 90px;">
                    <span id="...">
                        sometext
                    </span>
                </div>
            </body>
            <script>hljs.initHighlightingOnLoad();</script>
        </html>
    ''')
    assert actual == expected

    with pytest.raises(TypeError):
        Page(resources=[Text('Some Title')]).__html__()

    with pytest.raises(TypeError):
        Page(title=Text('Some Title')).__html__()



