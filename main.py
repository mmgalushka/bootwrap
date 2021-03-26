
import os
import sys
import argparse
import glob

import yaml

from flask import Flask, Markup
from bs4 import BeautifulSoup

import bootwrap as bw

app = Flask(__name__, static_folder='docs', static_url_path='')

with open('main.yaml', 'r') as file:
    demo = yaml.load(file)


class DocArguments(bw.Panel):
    def __init__(self, content):
        table = bw.Table(
            head=['Name', 'Type', 'Description'],
            body=content
        ).as_small().as_bordered()
        table.body.transform(
            0,
            bw.TableEntity.VALUE,
            lambda x: f'<i style="white-space: nowrap">{x}</i>'
        )
        table.body.transform(
            1,
            bw.TableEntity.VALUE,
            lambda x: f'<code style="white-space: nowrap">{x}</code>'
        )
        table.body.transform(
            2,
            bw.TableEntity.VALUE,
            lambda x: f'<span class="text-secondary">{x}</span>'
        )
        super().__init__(table)


class DocSection(bw.Panel):

    def __init__(self, content):
        self.__name = content.get('title')

        self.__title = None
        if 'title' in content:
            self.__title = bw.Text(content['title']).as_heading(1)

        subtitle = None
        if 'subtitle' in content:
            subtitle = bw.Text(content['subtitle']).as_heading(2).\
                add_classes('text-muted')

        image = None
        if 'image' in content:
            image = bw.Panel(
                bw.Image(
                    content['image']['file'],
                    width=content['image'].get('width'),
                    height=content['image'].get('height')
                )
            ).add_classes('text-center')

        code_left = None
        code_right = None
        if 'code' in content:
            c = content['code']
            if '@right' in c:
                c = c.replace('@right', '').strip()
                code_right = bw.Text(c).as_code()
            else:
                c = c.replace('@left', '').strip()
                code_left = bw.Text(c).as_code()

        constructor = None
        if 'constructor' in content:
            constructor = f'''
                <p><strong>Constructor:</strong>
                    <code>{content['constructor']}</code>
                </p>
            '''

        arguments = None
        if 'arguments' in content:
            arguments = DocArguments(content['arguments'])

        evaluation = None
        if 'evaluation' in content:
            loc = {}
            exec(content['evaluation'], {}, loc)
            evaluation = loc['output']

        description = []
        if 'description' in content:
            for fragment in content['description']:
                if isinstance(fragment, str):
                    description.append(bw.Text(fragment).as_paragraph())
                elif isinstance(fragment, dict):
                    try:
                        description.append(
                            bw.Table(
                                head=fragment['head'],
                                body=fragment['body']
                            )
                        )
                    except KeyError as err:
                        raise AssertionError(
                            'Invalid fragment format for a table;'
                        ) from err
                else:
                    raise AssertionError(
                        f'Unsupported fragment type {type(fragment)};'
                    )

        if not isinstance(description, list):
            description = [description]

        super().__init__(
            bw.Panel(
                bw.Panel(self.__title, subtitle, constructor),
                bw.Panel()
            ).horizontal(),
            bw.Panel(
                bw.Panel(arguments, *description,  code_left),
                bw.Panel(image, code_right, evaluation)
            ).horizontal()
        )
        self.add_classes('mt-3')

    @property
    def name(self):
        """The section name"""
        return self.__name


class GenericPage(bw.Page):
    """Generic web-pages for demoing web-components.

    Args:
        content (WebComponent): The web-page content to show
    """
    def __init__(self, content):
        def docgen(content):
            if isinstance(content, dict):
                items = []
                for name, tab in content.items():
                    sections = list(map(DocSection, tab))

                    if len(sections) > 1:
                        view = bw.Panel(
                            bw.Separator(),
                            bw.Navigation(*[
                                bw.Navigation.Item(
                                    bw.Text(section.name).as_secondary(),
                                    section,
                                    active=(idx == 0)
                                )
                                for idx, section in enumerate(sections)
                            ])
                        )
                    else:
                        view = sections[0]

                    items.append(
                        bw.Navigation.Item(name, view, len(items) == 0)
                    )
                return bw.Navigation(*items).as_pills()
            else:
                return bw.Panel(*list(map(DocSection, content)))

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
            container=docgen(content)
        )


@app.route('/')
def home():
    with open('main.yaml', 'r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content['home']))


@app.route('/layout')
def layout():
    with open('main.yaml', 'r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content['layout']))


@app.route('/components')
def components():
    with open('main.yaml', 'r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content['components']))


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
