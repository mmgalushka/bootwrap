"""
Test for bootwrap/page.py
"""

import pytest

from bootwrap import Page, Link, Javascript, Menu, Text
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
        container=Text('sometext')
    ).background(
        color='somevalue',
        image='somevalue',
        position='somevalue',
        size='somevalue',
        repeat='somevalue',
        origin='somevalue',
        clip='somevalue',
        attachment='somevalue'
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
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"/>
                <link rel="stylesheet"
                    type="text/css"
                    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"/>
                <link rel="stylesheet"
                    type="text/css"
                    href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css"/>
                <link rel="icon" type="image/x-icon" href="somename.ico"/>
                <link rel="stylesheet" type="text/css" href="https//someresource.com/some.css"/>

                <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"
                    type="application/javascript">
                </script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js"
                    type="application/javascript">
                </script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
                    type="application/javascript">
                </script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"
                    type="application/javascript">
                </script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js"
                    type="application/javascript">
                </script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/json.min.js"
                    type="application/javascript">
                </script>                  
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/yaml.min.js"
                    type="application/javascript">
                </script>   
                <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js"
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
                        type="button" data-bs-toggle="collapse"
                        data-bs-target="#menu"
                        aria-controls="menu"
                        aria-expanded="false"
                        aria-label="Toggle menu">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    
                    <div class="collapse navbar-collapse" id="menu">
                        <ul class="navbar-nav me-auto"></ul>
                    </div>
                </nav>
                <div class="container-fluid">
                    <span id="...">
                        sometext
                    </span>
                </div>
            </body>
            <script>...</script>
            <style>...</style>
        </html>
    ''')  # NOQA
    assert actual == expected

    with pytest.raises(TypeError):
        Page(resources=[Text('Some Title')]).__html__()

    with pytest.raises(TypeError):
        Page(title=Text('Some Title')).__html__()
