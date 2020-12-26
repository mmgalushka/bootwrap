
import sys
import argparse

from textwrap import dedent
from flask import Flask, Markup, redirect, url_for
from bs4 import BeautifulSoup

import bootwrap as bw

app = Flask(__name__, static_folder='docs', static_url_path='')


QUOTES_AUTHORS = [
    'N.Mandela',
    'W.Disney',
    'S.Jobs',
]

QUOTES_TEXT = [
    '"The greatest glory in living lies not in never falling, but in rising every time we fall."',
    '"The way to get started is to quit talking and begin doing."',
    '"Your time is limited, so don\'t waste it living someone else\'s life. Don\'t be trapped by dogma – which is living with the results of other people\'s thinking."'
]


class Demo(bw.Page):
    def __init__(self, content):
        super().__init__(
            favicon = url_for('docs', filename='favicon.ico'),
            menu=bw.Menu(
                logo = bw.Image(
                    url_for('docs', filename='python-bootwrap-logo.png'),
                    width=32,
                    alternative='Bootwrap Logo'
                ),
                brand=bw.Text('Bootwrap').as_strong().as_light(),
                anchors=[
                    bw.Anchor('Components').link('/components'),
                    bw.Anchor('Assemblies').link('/assemblies'),
                    bw.Anchor('Page').link('/page'),
                ], 
                actions=[
                    bw.Button('For Contributors').with_border().as_light()
                ]
            ),
            content=content
        )

class ButtonDemo(bw.Panel):
    def __init__(self):
        super().__init__()
        self.append(
            # Button
            bw.Text('Buttons').as_heading(1).add_classes('mt-3'),
            bw.Button('Primary').as_primary(),
            bw.Button('Secondary').as_secondary(),
            bw.Button('Success').as_success(),
            bw.Button('Warning').as_warning(),
            bw.Button('Danger').as_danger(),
            bw.Button('Info').as_info(),
            bw.Button('Light').as_light(),
            bw.Button('Dark').as_dark(),
            bw.Text(
                dedent('''
                    Button('Primary').as_primary()
                    Button('Secondary').as_secondary()
                    Button('Success').as_success()
                    Button('Warning').as_warning()
                    Button('Danger').as_danger()
                    Button('Info').as_info()
                    Button('Light').as_light()
                    Button('Dark').as_dark()
                ''')
            ).as_code().add_classes('mt-3'),
            
            # Outline Button
            bw.Text('Outline Buttons').as_heading(1).add_classes('mt-3'),
            bw.Button('Primary').with_border().as_primary(),
            bw.Button('Secondary').with_border().as_secondary(),
            bw.Button('Success').with_border().as_success(),
            bw.Button('Warning').with_border().as_warning(),
            bw.Button('Danger').with_border().as_danger(),
            bw.Button('Info').with_border().as_info(),
            bw.Button('Light').with_border().as_light(),
            bw.Button('Dark').with_border().as_dark(),
            bw.Text(
                dedent('''
                    Button('Primary', outline=True).as_primary()
                    Button('Secondary', outline=True).as_secondary()
                    Button('Success', outline=True).as_success()
                    Button('Warning', outline=True).as_warning()
                    Button('Danger', outline=True).as_danger()
                    Button('Info', outline=True).as_info()
                    Button('Light', outline=True).as_light()
                    Button('Dark', outline=True).as_dark()
                ''')
            ).as_code().add_classes('mt-3'),

            # Enable/Disable Button
            bw.Text('Enable/Disable Button').as_heading(1).add_classes('mt-3'),
            bw.Button('Enable Button').as_primary(),
            bw.Button('Disable Button').as_disabled().as_primary(),
            bw.Text(
                dedent('''
                    Button('Enable Button').as_primary()
                    Button('Disable Button', disabled=True).as_primary()
                ''')
            ).as_code().add_classes('mt-3'),
        ).add_classes('mt-3')


class AnchorDemo(bw.Panel):
    def __init__(self):
        super().__init__()
        self.append(
            # Anchor
            bw.Text('Anchors').as_heading(1).add_classes('mt-3'),
            bw.Anchor('No Style').add_classes('mr-3'),
            bw.Anchor('Primary').as_primary().add_classes('mr-3'),
            bw.Anchor('Secondary').as_secondary().add_classes('mr-3'),
            bw.Anchor('Success').as_success().add_classes('mr-3'),
            bw.Anchor('Warning').as_warning().add_classes('mr-3'),
            bw.Anchor('Danger').as_danger().add_classes('mr-3'),
            bw.Anchor('Info').as_info().add_classes('mr-3'),
            bw.Anchor('Light').as_light().add_classes('mr-3'),
            bw.Anchor('Dark').as_dark().add_classes('mr-3'),
            bw.Text(
                dedent('''
                    Anchor('No Style'),
                    Anchor('Primary').as_primary(),
                    Anchor('Secondary').as_secondary(),
                    Anchor('Success').as_success(),
                    Anchor('Warning').as_warning(),
                    Anchor('Danger').as_danger(),
                    Anchor('Info').as_info(),
                    Anchor('Light').as_light(),
                    Anchor('Dark').as_dark(),
                ''')
            ).as_code().add_classes('mt-3')
        )


class FormDemo(bw.Panel):
    def __init__(self):
        super().__init__()
        self.append(
            # Checkbox Input
            bw.Text('Checkbox Input').as_heading(1).add_classes('mt-3'),
            bw.CheckboxInput('Example 1', 'example-enable1'),
            bw.CheckboxInput('Example 2', 'example-enable2').check(True),
            bw.Text('If check-boxes are disabled').as_paragraph().add_classes('mt-3'),
            bw.CheckboxInput('Example 1', 'example-disable1').as_disabled(),
            bw.CheckboxInput('Example 2', 'example-disable2').check(True).as_disabled(),

            # Radio Input
            bw.Text('Radio Input').as_heading(1).add_classes('mt-3'),
            bw.RadioInput('Example 1', 'example-enable').value('example1'),
            bw.RadioInput('Example 2', 'example-enable').value('example2').check(True),
            bw.Text('If radio buttons are disabled').as_paragraph().add_classes('mt-3'),
            bw.RadioInput('Example 1', 'example-disable').value('example1').as_disabled(),
            bw.RadioInput('Example 2', 'example-disable').value('example2').check(True).as_disabled(),
        
            # Email Input
            bw.Text('Email Input').as_heading(1).add_classes('mt-3'),
            bw.Text('Email input with label inline:').as_paragraph().add_classes('mt-3'),
            bw.EmailInput('Some Email', 'some-email', placeholder='example@host.com'),
            bw.Text('Email input disabled:').as_paragraph().add_classes('mt-3'),
            bw.EmailInput('Some Email', 'some-email', placeholder='example@host.com').as_disabled(),
            bw.Text('Email input with label on top:').as_paragraph().add_classes('mt-3'),
            bw.EmailInput('Some Email', 'some-email', placeholder='example@host.com').label_on_top(),
        
            # Password Input
            bw.Text('Password Input').as_heading(1).add_classes('mt-3'),
            bw.Text('Password input with label inline:').as_paragraph().add_classes('mt-3'),
            bw.PasswordInput('Some Password', 'some-password', placeholder='********'),
            bw.Text('Password input disabled:').as_paragraph().add_classes('mt-3'),
            bw.PasswordInput('Some Password', 'some-password', placeholder='********').as_disabled(),
            bw.Text('Password input with label on top:').as_paragraph().add_classes('mt-3'),
            bw.PasswordInput('Some Password', 'some-password', placeholder='********').label_on_top(),
        
            # Text Input
            bw.Text('Text Input').as_heading(1).add_classes('mt-3'),
            bw.Text('Text input with label inline:').as_paragraph().add_classes('mt-3'),
            bw.TextInput('Some Text', 'some-text', placeholder='place holder'),
            bw.Text('Text input with label on top:').as_paragraph().add_classes('mt-3'),
            bw.TextInput('Some Text', 'some-text', rows=5, placeholder='place holder'),

            # Numeric Input
            bw.Text('Numeric Input').as_heading(1).add_classes('mt-3'),
            bw.NumericInput('Some Numeric', 'some-number', placeholder='some number'),

            # Select Input
            bw.Text('Select Input').as_heading(1).add_classes('mt-3'),
            bw.SelectInput('Some Selector', 'some-selector').\
                append(
                    ('One', '1', False),
                    ('Two', '2', False),
                    ('Three', '3', True)
                ),


            # File Input
            bw.Text('File Input').as_heading(1).add_classes('mt-3'),
            bw.FileInput('File Selector', 'file-selector')
        )

class ImageDemo(bw.Panel):
    def __init__(self):
        super().__init__()
        self.append(
            bw.Text('Image').as_heading(1).add_classes('mt-3'),
            bw.Image(
                url_for('docs', filename='python-bootwrap-logo.png'),
                width=32,
                alternative='Bootwrap Logo'
            ).add_classes('mt-3'),
            bw.Text(
                dedent('''
                    Image(
                        'python-bootwrap-logo.png',
                        width=32,
                        alternative='Bootwrap Logo'
                    )
                ''')
            ).as_code().add_classes('mt-3')
        )



class LinkAndJavascriptDemo(bw.Panel):
    def __init__(self):
        super().__init__()
        self.append(
            # Link
            bw.Text('Link').as_heading(1).add_classes('mt-3'),
            bw.Text(
                dedent('''
                    Link('https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css')
                ''')
            ).as_code().add_classes('mt-3'),

            # Javascript
            bw.Text('Javascript').as_heading(1).add_classes('mt-3'),
            bw.Text('Import').as_heading(4).add_classes('mt-3'),
            bw.Text(
                dedent('''
                    Javascript('https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js')
                ''')
            ).as_code().add_classes('mt-3'),
            bw.Text('Embedding').as_heading(4).add_classes('mt-3'),
            bw.Text(
                dedent('''
                    Javascript(
                        script = 'console.log("Hello someone!")',
                        submap = {
                            'someone': 'World'
                        }
                    )
                ''')
            ).as_code().add_classes('mt-3')
        )


class MenuDemo(bw.Panel):
    def __init__(self):
        super().__init__()
        self.append(
            bw.Text('Menu').as_heading(1).add_classes('mt-3'),
            bw.Text(
                dedent('''
                ''')
            ).as_code().add_classes('mt-3')
        )


class NavigationDemo(bw.Panel):
    def __init__(self):
        super().__init__()
        
        quotes = [
            (
                'N.Mandela',
                bw.Text('"The greatest glory in living lies not in never falling, but in rising every time we fall." - Nelson Mandela'),
                True
            ),
            (
                'W.Disney',
                bw.Text('"The way to get started is to quit talking and begin doing." - Walt Disney'),
                False
            ),
            (
                'S.Jobs',
                bw.Text('"Your time is limited, so don\'t waste it living someone else\'s life. Don\'t be trapped by dogma – which is living with the results of other people\'s thinking." - Steve Jobs'),
                False
            )

        ]
        
        self.append(
            # Basic
            bw.Text('Basic').as_heading(1).add_classes('mt-3'),
            bw.Text('Horizontal').as_heading(4).add_classes('mt-3'),
            bw.Navigation().append(*quotes),
            bw.Text('Vertical').as_heading(4).add_classes('mt-3'),
            bw.Navigation().append(*quotes).as_vertical(),

            # Tabs
            bw.Text('Tabs').as_heading(1).add_classes('mt-3'),
            bw.Navigation().append(*quotes).as_tabs(),

            #  Pills
            bw.Text('Horizontal').as_heading(4).add_classes('mt-3'),
            bw.Navigation().append(*quotes).as_pills(),
            bw.Text('Vertical').as_heading(4).add_classes('mt-3'),
            bw.Navigation().append(*quotes).as_pills().as_vertical()
        )


class TableDemo(bw.Panel):
    def __init__(self):
        super().__init__()

        head = ['Authors', 'Text']
        body = list(zip(QUOTES_AUTHORS, QUOTES_TEXT))

        self.append(
            bw.Text('Table').as_heading(1).add_classes('mt-3'),
            bw.Table(head, body).add_classes('mt-3')
        )


class Components(Demo):
    def __init__(self):
        super().__init__(
            content=bw.Navigation().as_tabs().\
                append(
                    ('Button', ButtonDemo(), False),
                    ('Anchor', AnchorDemo(), False),
                    ('Form', FormDemo(), False),
                    ('Image', ImageDemo(), False),
                    ('Link&Javascript', LinkAndJavascriptDemo(), False),
                    ('Menu', MenuDemo(), False),
                    ('Navigation', NavigationDemo(), False),
                    ('Table', TableDemo(), True)
                )
            )


class GenericPage(bw.Page):
    """Generic web-pages for demoing web-components.
    
    Args:
        content (WebComponent): The web-page content to show
    """
    def __init__(self, content):
        super().__init__(
            favicon = 'favicon.ico',
            menu=bw.Menu(
                logo = bw.Image(
                    'logo.png',
                    width=32,
                    alternative='BLogo'
                ),
                brand=bw.Text('Bootwrap').as_strong().as_light(),
                anchors=[
                    bw.Anchor('Home').link('/'),
                    bw.Anchor('Basics').link('/basics'),
                    bw.Anchor('Components').link('/components')
                ], 
                actions=[
                    bw.Button('For Contributors').\
                        with_border().\
                        as_light().\
                        link('/contributors')
                ]
            ),
            content=content
        )


class HomePage(GenericPage):
    """A home-page"""
    def __init__(self):
        super().__init__(
            content=bw.Text('home')
        )   


class BasicsPage(GenericPage):
    def __init__(self):
        super().__init__(
            content=bw.Text('basics')
        ) 


class ComponentsPage(GenericPage):
    def __init__(self):
        super().__init__(
            content=bw.Text('components')
        )


class ContributorsPage(GenericPage):
    def __init__(self):
        super().__init__(
            content=bw.Text('contributors')
        )


@app.route('/')
def home():
    return Markup(HomePage())


@app.route('/basics')
def basics():
    return Markup(BasicsPage())


@app.route('/components')
def components():
    return Markup(ComponentsPage())


@app.route('/contributors')
def contributors():
    return Markup(ContributorsPage())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action', 
        choices=['demo', 'docs'],
        help='action to run'
    )

    args = parser.parse_args(sys.argv[1:])

    if args.action == 'docs':

        def save_page(filename, page):
            page = page.replace('href="/"', 'href="index.html"').\
                replace('href="/basics"', 'href="basics.html"').\
                replace('href="/components"', 'href="components.html"').\
                replace('href="/contributors"', 'href="contributors.html"')
            with open(f'docs/{filename}', 'w') as file:
                soup = BeautifulSoup(page)
                file.write(soup.prettify())

        save_page('index.html', str(HomePage()))
        save_page('basics.html', str(BasicsPage()))
        save_page('components.html', str(ComponentsPage()))
        save_page('contributors.html', str(ContributorsPage()))
    else:
        app.run(debug=True)
