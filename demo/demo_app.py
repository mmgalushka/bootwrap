"""
The web-application for showing the project documentation.
"""

from flask import Flask, Markup

import bootwrap as bw

demo_app = Flask(__name__, static_folder='.', static_url_path='')


class DemoPage(bw.Page):
    """A demo web-pages.

    Args:
        config (dict): The configuration for generating a documentation
            contant.
    """

    def __init__(self, content):
        super().__init__(
            favicon='favicon.ico',
            menu=bw.Menu(
                logo=bw.Image(
                    'logo.png',
                    width=32,
                    alt='Bootwrap Logo'
                ),
                brand=bw.Text('Bootwrap').as_strong().as_light(),
                anchors=[
                    bw.Anchor('Home').link('/'),
                    bw.Anchor('Layout').link('/layout'),
                    bw.Anchor('Base').link('/base'),
                    bw.Anchor('Components').link('/components')
                ],
                actions=[
                    bw.Button('GitHub').
                    as_outline().
                    as_light().
                    link('https://github.com/mmgalushka/bootwrap')
                ]
            ),
            container=content
        )


@ demo_app.route('/')
def home():
    return Markup(DemoPage([]))


@ demo_app.route('/layout')
def layout():
    return Markup(DemoPage([]))


@ demo_app.route('/base')
def base():
    return Markup(DemoPage([]))


@ demo_app.route('/components')
def components():
    return Markup(DemoPage([]))
