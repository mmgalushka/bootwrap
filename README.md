<p align="center" width="100%">
    <img height="96px" src="docs/bootwrap-equation.png"> 
</p>

# Python Bootwrap

[![Continuous Integration Status](https://github.com/mmgalushka/python-bootwrap/workflows/CI/badge.svg)](https://github.com/mmgalushka/python-bootwrap/actions)
[![Code Coverage Percentage](https://codecov.io/gh/mmgalushka/python-bootwrap/branch/main/graphs/badge.svg)](https://codecov.io/gh/mmgalushka/python-bootwrap)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/763657a471ff424c85a5b894ddb750d0)](https://www.codacy.com/gh/mmgalushka/python-bootwrap/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mmgalushka/python-bootwrap&amp;utm_campaign=Badge_Grade)
[![Project License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/mmgalushka/python-bootwrap/blob/main/LICENSE)
[![Project Documentation](https://img.shields.io/badge/docs-up--to--date-success)](https://mmgalushka.github.io/python-bootwrap/)

**Bootwrap** is a Python library for rapid developing of web-based user interfaces (WebUI). It helps creating WebUI using Python code only and can be used in conjunction with different web-development frameworks such as [Flask](https://palletsprojects.com/p/flask/). Under the hood, this library wraps one of the most popular front-end toolkit [Bootstrap](https://getbootstrap.com/).

This library would be useful for developers and data scientists who wish to build interactive web-application without crafting HTML, CSS and Javascript.

As a showcase of what this library is capable of please check the documentation. The entire [documentation](https://mmgalushka.github.io/python-bootwrap/) web interface is created using the **Bootwrap** library.


## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
~$ pip install -i https://test.pypi.org/simple/ bootwrap
```

<p style="color: orange"><strong>Note:</strong> The Bootwrap is currently deployed using TestPyPI – which is a separate instance of the Python Package Index. This allows us to test distribution before moving this package to the real index.</p>


## A Simple Example

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

Use the following command to launch the application.

```bash
$ flask run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The result should look like.

<img width="600px" src="docs/multi-pages-app.png"> 

