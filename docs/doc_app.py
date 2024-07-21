"""
The web-application for showing the project documentation.
"""

import os
import re
import textwrap
import pathlib
import glob

import yaml

from flask import Flask
from markupsafe import Markup
from bs4 import BeautifulSoup

import bootwrap as bw
from .doc_generator import generate_class_doc


doc_app = Flask(__name__, static_folder='.', static_url_path='')


class BlockDoc(bw.Panel):
    """The documentation block.

    It represents a piece of documentation that can be isolated into an
    independent block. For example method or class arguments, return values
    can be viewed as a block.

    Args:
        title (str): The block title.
        wc_content (WebComponent): The block content.
    """

    def __init__(self, title, wc_block):
        super().__init__(
            bw.Text(title).as_heading(6).as_strong() if title else None,
            wc_block
        )
        self.ms(3)


class ParamsDoc(BlockDoc):
    """A component for visualizing class or method parameters.

    In this context by class or method parameters understood description
    of receiving arguments and returning values

    Args:
        title (str): The block title.
        params (list): The information about visualising parameters.
            This information is represented as a list of lists
            `[[name, type, description], ...]`.
    """

    def __init__(self, title, params):
        wc_parameters = bw.Table(
            head=['Name', 'Type', 'Description'],
            body=params
        )
        wc_parameters.body.transform(
            0,
            bw.TableEntity.VALUE,
            lambda x: f'<i style="white-space: nowrap">{x}</i>'
        )
        wc_parameters.body.transform(
            1,
            bw.TableEntity.VALUE,
            lambda x: f'<code style="white-space: nowrap">{x}</code>'
        )

        wc_parameters.as_small().add_classes('bg-light')
        super().__init__(title, wc_parameters)
        self.as_collapse()


class ArgumentsDoc(ParamsDoc):
    """A component for visualizing class or method arguments."""

    def __init__(self, params):
        super().__init__('Arguments', params)


class ReturnsDoc(ParamsDoc):
    """A component for visualizing class or method return values."""

    def __init__(self, params):
        super().__init__('Returns', params)


class ExampleDoc(BlockDoc):
    """A component for visualizing class or method example.

    The example block represents a code fragment to show how a particular
    web component can be used.

    Args:
        code (str): The code fragment to show.
    """

    def __init__(self, code):
        super().__init__(
            'Example',
            bw.Text(
                re.sub(r'(^\n\s)*output\s*=\s*', '', code)
            ).as_code()
        )


class DemoDoc(BlockDoc):
    """A component to render an example.

    Renders an example code to provide a user with the look and feel for
    the component(s).

    The code fragment to show and the code fragment to render must be
    separated by the `@eval` key-string.

    Args:
        code (str): The code fragment to render.
    """

    def __init__(self, code):
        loc = {}
        exec(textwrap.dedent(code), {}, loc)
        super().__init__(None, loc['output'])


class PropertyDoc(bw.Panel):
    """A component to show a property-documentation.

    Args:
        doc (dict): The documentation about a property. For more information
            about the property-documentation, see the `docgen` module.
    """

    def __init__(self, doc):
        wc_example = None
        wc_demo = None
        if len(doc['example']) > 0:
            wc_example = ExampleDoc(doc['example'])
            if re.search(r'(^\s)*output\s*=\s*', doc['example']):
                wc_demo = DemoDoc(doc['example'])

        wc_title = bw.Text(
            'Property ' + str(bw.Text(doc['name']).as_primary())
        ).as_heading(4)

        wc_summary = bw.Text(doc['summary']).as_muted()

        description = [
            bw.Text(text).as_paragraph()
            for text in doc['description']
        ]

        super().__init__(
            wc_title,
            wc_summary,
            *description,
            wc_example,
            wc_demo
        )

        self.mt(5)


class MethodDoc(bw.Panel):
    """A component to show a method-documentation.

    Args:
        doc (dict): The documentation about a method. For more information
            about the method-documentation, see the `docgen` module.
    """

    def __init__(self, doc):
        wc_arguments = None
        wc_arguments_btn = None
        if len(doc['arguments']) > 0:
            wc_arguments = ArgumentsDoc(doc['arguments'])
            wc_arguments_btn = bw.Button('Argument').\
                as_primary().\
                as_outline().\
                ms(1).\
                me(1).\
                add_classes('btn-sm').\
                toggle(wc_arguments)

        wc_returns = None
        wc_returns_btn = None
        if len(doc['returns']) > 0:
            wc_returns = ReturnsDoc(doc['returns'])
            wc_returns_btn = bw.Button('Returns').\
                as_primary().\
                as_outline().\
                add_classes('btn-sm').\
                toggle(wc_returns)

        wc_example = None
        wc_demo = None
        if len(doc['example']) > 0:
            wc_example = ExampleDoc(doc['example'])
            if re.search(r'(^\s)*output\s*=\s*', doc['example']):
                wc_demo = DemoDoc(doc['example'])

        wc_title = bw.Panel(
            bw.Text(
                'Method ' + str(bw.Text(doc['name']).as_primary())
            ).as_heading(4),
            bw.Panel(wc_arguments_btn, wc_returns_btn)
        ).add_classes('d-flex justify-content-between')

        wc_summary = bw.Text(doc['summary']).as_muted()

        wc_call = bw.Text(doc['name'] + doc['init']).as_code()

        description = [
            bw.Text(text).as_paragraph()
            for text in doc['description']
        ]

        super().__init__(
            wc_title,
            wc_summary,
            wc_call,
            wc_arguments,
            wc_returns,
            *description,
            wc_example,
            wc_demo
        )

        self.mt(5)


class ClassDoc(bw.Panel):
    """A component to show a class-documentation.

    Args:
        doc (dict): The documentation about a class. For more information
            about the class-documentation, see the `docgen` module.
    """

    def __init__(self, doc):
        self.__name = doc['name']

        wc_arguments = None
        wc_arguments_btn = None
        if len(doc['arguments']) > 0:
            wc_arguments = ArgumentsDoc(doc['arguments'])
            wc_arguments_btn = bw.Button('Argument').\
                as_primary().\
                as_outline().\
                ms(1).\
                me(1).\
                add_classes('btn-sm').\
                toggle(wc_arguments)

        wc_returns = None
        wc_returns_btn = None
        if len(doc['returns']) > 0:
            wc_returns = ReturnsDoc(doc['returns'])
            wc_returns_btn = bw.Button('Returns').\
                as_primary().\
                as_outline().\
                add_classes('btn-sm').\
                toggle(wc_returns)

        wc_example = None
        wc_demo = None
        if len(doc['example']) > 0:
            wc_example = ExampleDoc(doc['example'])
            if re.search(r'(^\s)*output\s*=\s*', doc['example']):
                wc_demo = DemoDoc(doc['example'])

        wc_title = bw.Panel(
            bw.Text(
                'Class ' + str(bw.Text(self.__name).as_primary())
            ).as_heading(1),
            bw.Panel(wc_arguments_btn, wc_returns_btn)
        ).add_classes('d-flex justify-content-between')

        wc_summary = bw.Text(doc['summary']).as_muted()

        # Shows constructor call only for classes None for Enum.
        # for Class the doc['attributes'] should be empty.
        wc_call = None
        if len(doc['attributes']) == 0:
            wc_call = bw.Text(doc['name'] + doc['init']).as_code()

        description = []
        if len(doc['description']) > 0:
            description = [
                bw.Text(text).as_paragraph()
                for text in doc['description']
            ]

        wc_attributes = None
        if len(doc['attributes']) > 0:
            wc_attributes = bw.Panel(
                *[
                    bw.Panel(
                        '%s.<strong class="text-primary">%s</strong>' % (
                            doc['name'], attribute_doc['name']
                        )
                    ).p(1).m(1).add_classes('border text-center')
                    for attribute_doc in doc['attributes']
                ]
            ).horizontal()

        properties = []
        if len(doc['properties']) > 0:
            properties = [
                PropertyDoc(property_doc)
                for property_doc in doc['properties']
            ]

        methods = []
        if len(doc['methods']) > 0:
            methods = [
                MethodDoc(method_doc)
                for method_doc in doc['methods']
            ]

        super().__init__(
            wc_title,
            wc_summary,
            wc_call,
            wc_arguments,
            wc_returns,
            *description,
            wc_example,
            wc_demo,
            wc_attributes,
            *properties,
            *methods
        )
        self.mt(5)

    @ property
    def name(self):
        """The section name"""
        return self.__name


class CustomDoc(bw.Panel):
    """A component to show a custom documentation.

    Args:
        doc (dict): The custom-documentation.
    """

    def __init__(self, doc):
        self.__name = doc.get('title')

        title = None
        if 'title' in doc:
            title = bw.Text(doc['title']).as_heading(1)

        subtitle = None
        if 'subtitle' in doc:
            subtitle = bw.Text(doc['subtitle']).\
                as_heading(2).\
                add_classes('text-muted')

        image = None
        if 'image' in doc:
            image = bw.Panel(
                bw.Image(
                    doc['image']['file'],
                    width=doc['image'].get('width'),
                    height=doc['image'].get('height')
                )
            ).add_classes('text-center')

        code_left = None
        code_right = None
        evaluation = None
        if 'code' in doc:
            c = doc['code']

            is_right = '@right' in c

            c = c.replace('@right', '').replace('@left', '').strip()

            if re.search(r'(^\s)*output\s*=\s*', c):
                loc = {}
                exec(c, {}, loc)
                evaluation = loc['output']

            c = re.sub(r'(^\n\s)*output\s*=\s*', '', c)

            if is_right:
                code_right = bw.Text(c).as_code()
            else:
                code_left = bw.Text(c).as_code()

        description = []
        if 'description' in doc:
            for paragraph in doc['description']:
                description.append(bw.Text(paragraph).as_paragraph())

        super().__init__(
            bw.Panel(
                bw.Panel(title, subtitle),
                bw.Panel()
            ).horizontal(),
            bw.Panel(
                bw.Panel(*description,  code_left),
                bw.Panel(image, code_right, evaluation)
            ).horizontal()
        )
        self.mt(3)

    @ property
    def name(self):
        """The section name"""
        return self.__name


def generate_documentation(config):
    """Generates a documentation content using the configuration.

    All Bootstrap documentation is generated using the configuration.
    This configuration defines by a  YAML file (one configuration file
    per documentation page).

    If the top level of the configuration is a list, then the documentation
    page will look like a list of section.

    If the top level of the configuration is a dictionary, then the
    documentation page will be split into partitions, each represented
    by a list of sections. Partitions names will be used for creating a
    navigation menu.

    To learn more about configuration files for creating documentation, read
    developer notes on GitHub Page.

    Args:
        config (dict): The configuration for generating a documentation
            contant.

    Returns:
        wc (Panel|Navigation): The `Panel` constructed if the top-level
            configuration is a list and `Navigation` if the top-level is a
            dictionary.
    """
    if isinstance(config, dict):
        # Constructs a Navigation control consisting of top-level partitions
        # split into a list of sections.
        items = []
        for name, partition in config.items():
            # name - the partition name (used for top-level navigation);
            # partition - the partition contant (a list of sections);

            # The following code block renders a documentation for each
            # section. ClassDoc renders Python-class documentation. CustomDoc
            # renders a supplemental documentation such as examples.
            sections = [
                ClassDoc(generate_class_doc(eval('bw.' + doc['class'])))
                if 'class' in doc else CustomDoc(doc)
                for doc in partition
            ]

            if len(sections) > 1:
                # Creates an item with multiple sections.
                item = bw.Navigation.Item(
                    name,
                    bw.Panel(
                        bw.Separator(),
                        bw.Navigation(*[
                            bw.Navigation.Item(
                                bw.Text(section.name).as_secondary(),
                                section,
                                active=(idx == 0)
                            )
                            for idx, section in enumerate(sections)
                        ])
                    ),
                    len(items) == 0
                )
            else:
                # Creates an item with just one section.
                item = bw.Navigation.Item(
                    name,
                    sections[0],
                    len(items) == 0
                )
            items.append(item)
        return bw.Navigation(*items).as_pills()
    else:
        return bw.Panel(
            *[
                ClassDoc(generate_class_doc(eval('bw.' + doc['class'])))
                if 'class' in doc else CustomDoc(doc)
                for doc in config
            ]
        )


class GenericPage(bw.Page):
    """A documentation web-pages.

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
            container=generate_documentation(content)
        )


@ doc_app.route('/')
def home():
    path = pathlib.Path(__file__).parent / 'config/home.yaml'
    with path.open('r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content))


@ doc_app.route('/layout')
def layout():
    path = pathlib.Path(__file__).parent / 'config/layout.yaml'
    with path.open('r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content))


@ doc_app.route('/base')
def base():
    path = pathlib.Path(__file__).parent / 'config/base.yaml'
    with path.open('r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content))


@ doc_app.route('/components')
def components():
    path = pathlib.Path(__file__).parent / 'config/components.yaml'
    with path.open('r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content))


def doc_to_html():
    current_dir = pathlib.Path(__file__).parent
    for path in glob.glob(str(current_dir / '*.html')):
        os.remove(path)

    def save_page(filename, page):
        page = str(page).\
            replace('href="/"', 'href="index.html"').\
            replace('href="/layout"', 'href="layout.html"').\
            replace('href="/base"', 'href="base.html"').\
            replace('href="/components"', 'href="components.html"')
        with (current_dir / filename).open('w') as file:
            soup = BeautifulSoup(page, features='html.parser')
            file.write(soup.prettify())

    save_page('index.html', home())
    save_page('layout.html', layout())
    save_page('base.html', base())
    save_page('components.html', components())
