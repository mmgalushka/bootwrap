
import os
import sys
import argparse
import glob
import textwrap

import yaml

from flask import Flask, Markup
from bs4 import BeautifulSoup

import bootwrap as bw
from docgen import generate_class_doc


app = Flask(__name__, static_folder='docs', static_url_path='')


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
            bw.Text(title).as_heading(6).as_strong(),
            wc_block
        )
        self.add_classes('ml-3')


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
        wc_parameters.body.transform(
            2,
            bw.TableEntity.VALUE,
            lambda x: f'<span class="text-secondary">{x}</span>'
        )
        wc_parameters.as_small()
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

    This example represents a code fragment to show in documentation,
    also a code fragment used to render `WebComponent`s to provide a
    user with the look and feel for the component(s).

    The code fragment to show and the code fragment to render must be
    separated by the `@eval` key-string.

    Args:
        code (str): The code fragment to show and render.
    """
    def __init__(self, code):
        if '@eval' in code:
            code_to_show, code_to_eval = code.split('@eval')

            loc = {}
            exec(textwrap.dedent(code_to_eval), {}, loc)
            super().__init__(
                'Example',
                bw.Panel(
                    bw.Text(code_to_show).as_code(),
                    loc['output']
                )
            )
        else:
            super().__init__(
                'Example',
                bw.Text(code).as_code()
            )


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
                add_classes('ml-1 mr-1 btn-sm').\
                collapse(wc_arguments)

        wc_returns = None
        wc_returns_btn = None
        if len(doc['returns']) > 0:
            wc_returns = ReturnsDoc(doc['returns'])
            wc_returns_btn = bw.Button('Returns').\
                as_primary().\
                as_outline().\
                add_classes('btn-sm').\
                collapse(wc_returns)

        wc_example = None
        if len(doc['example']) > 0:
            wc_example = ExampleDoc(doc['example'])

        wc_title = bw.Panel(
            bw.Text(
                'Mathod ' + str(bw.Text(doc['name']).as_primary())
            ).as_heading(4),
            bw.Panel(wc_arguments_btn, wc_returns_btn)
        ).add_classes('d-flex justify-content-between')

        wc_summary = bw.Text(doc['summary']).as_heading(6).as_muted()

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
            wc_example
        )

        self.add_classes('mt-5')


class ClassDoc(bw.Panel):
    """A component to show a class-documentation.

    Args:
        doc (dict): The documentation about a class. For more information
            about the class-documentation, see the `docgen` module.
    """
    def __init__(self, doc):
        self.__name = bw.Text(doc['name'])

        wc_arguments = None
        wc_arguments_btn = None
        if len(doc['arguments']) > 0:
            wc_arguments = ArgumentsDoc(doc['arguments'])
            wc_arguments_btn = bw.Button('Argument').\
                as_primary().\
                as_outline().\
                add_classes('ml-1 mr-1 btn-sm').\
                collapse(wc_arguments)

        wc_returns = None
        wc_returns_btn = None
        if len(doc['returns']) > 0:
            wc_returns = ReturnsDoc(doc['returns'])
            wc_returns_btn = bw.Button('Returns').\
                as_primary().\
                as_outline().\
                add_classes('btn-sm').\
                collapse(wc_returns)

        wc_example = None
        if len(doc['example']) > 0:
            wc_example = ExampleDoc(doc['example'])

        wc_title = bw.Panel(
            bw.Text(
                'Class ' + str(bw.Text(doc['name']).as_primary())
            ).as_heading(1),
            bw.Panel(wc_arguments_btn, wc_returns_btn)
        ).add_classes('d-flex justify-content-between')

        wc_summary = bw.Text(doc['summary']).as_heading(3).as_muted()

        wc_call = bw.Text(doc['name'] + doc['init']).as_code()

        description = []
        if len(doc['description']) > 0:
            description = [
                bw.Text(text).as_paragraph()
                for text in doc['description']
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
            *methods
        )
        self.add_classes('mt-3')

    @property
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
            subtitle = bw.Text(doc['subtitle']).as_heading(2).\
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
        if 'code' in doc:
            c = doc['code']
            if '@right' in c:
                c = c.replace('@right', '').strip()
                code_right = bw.Text(c).as_code()
            else:
                c = c.replace('@left', '').strip()
                code_left = bw.Text(c).as_code()

        evaluation = None
        if 'evaluation' in doc:
            loc = {}
            exec(doc['evaluation'], {}, loc)
            evaluation = loc['output']

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
        self.add_classes('mt-3')

    @property
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
                    bw.Anchor('Components').link('/components')
                ],
                actions=[
                    bw.Button('GitHub').
                    as_outline().
                    as_light().
                    link('https://github.com/mmgalushka/python-bootwrap')
                ]
            ),
            container=generate_documentation(content)
        )


@app.route('/')
def home():
    with open('config/home.yaml', 'r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content))


@app.route('/layout')
def layout():
    with open('config/layout.yaml', 'r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content))


@app.route('/components')
def components():
    with open('config/components.yaml', 'r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=['demo', 'docs'],
        help='action to run'
    )

    args = parser.parse_args(sys.argv[1:])

    if args.action == 'docs':

        for path in glob.glob('docs/*.html'):
            os.remove(path)

        def save_page(filename, page):
            page = str(page).\
                replace('href="/"', 'href="index.html"').\
                replace('href="/layout"', 'href="layout.html"').\
                replace('href="/components"', 'href="components.html"')
            with open(f'docs/{filename}', 'w') as file:
                soup = BeautifulSoup(page)
                file.write(soup.prettify())

        save_page('index.html', home())
        save_page('layout.html', layout())
        save_page('components.html', components())

    else:
        app.run(debug=True)
