<p align="center" width="100%">
    <img width="96px" src="docs/logo.png"> 
</p>

# Python Bootwrap

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9dee3621de3a4a06b7cda614f52260b2)](https://app.codacy.com/gh/mmgalushka/python-bootwrap?utm_source=github.com&utm_medium=referral&utm_content=mmgalushka/python-bootwrap&utm_campaign=Badge_Grade_Settings)
[![Continuous Integration Status](https://github.com/mmgalushka/python-bootwrap/workflows/CI/badge.svg)](https://github.com/mmgalushka/python-bootwrap/actions)
[![Code Coverage Percentage](https://codecov.io/gh/mmgalushka/python-bootwrap/branch/main/graphs/badge.svg)](https://codecov.io/gh/mmgalushka/python-bootwrap)
[![Project License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mmgalushka/python-bootwrap/blob/main/LICENSE)
[![Project Documentation](https://img.shields.io/badge/docs-up--to--date-success)](https://mmgalushka.github.io/python-bootwrap/)

This is a Python library for rapid developing of web-based user interfaces (WebUI). It helps creating WebUI using Python code only and can be used in conjunction with different web-development frameworks such as [Flask](https://palletsprojects.com/p/flask/). Under the hood, this library wraps one of the most popular front-end toolkit [Bootstrap](https://getbootstrap.com/). For more information, please visit the Python Bootwrap [documentation](https://mmgalushka.github.io/python-bootwrap/).

Python Bootwrap would be useful for developers who want to build interactive web-application quickly and prefer focusing more on business logic rather than crafting HTML, CSS and Javascript.

## Hello World Example

The following code will care three pages application with the top-level menu bar for navigations.  

```Python
from flask import Flask, Markup
from bootwrap import Page, Menu, Image, Anchor, Button, Text

# Both 'logo.png' and 'favicon.ico' are stored in 'docs' folder
app = Flask(__name__, static_folder='docs', static_url_path='')

class MyMenu(Menu):
    def __init__(self):
        super().__init__(
            logo=Image('logo.png', width=32, alt='Logo'),
            brand=Text('Bootwrap').as_strong().as_light().add_classes('ml-2'),
            anchors=[
                Anchor('Home').link('/'),
                Anchor('About').link('/about')
            ], 
            actions=[
                Button('Sign In').as_outline().as_light().link('/signin')
            ]
        )

class MyPage(Page):
    def __init__(self, content):
        super().__init__(
            favicon = 'favicon.ico',
            title='Hello World Application',
            menu=MyMenu(),
            content=content
        )

@app.route('/')
def home():
    return Markup(MyPage(content=[Text('Home').as_heading(1)]))

@app.route('/about')
def about():
    return Markup(MyPage(content=[Text('About').as_heading(1)]))

@app.route('/signin')
def signin():
    return Markup(MyPage(content=[Text('Sign In').as_heading(1)]))

if __name__ == '__main__':
    app.run(debug=True)
```

This is a result:

<img width="600px" src="docs/multi-pages-app.png"> 

