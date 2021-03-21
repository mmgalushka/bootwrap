
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
            lambda x: f'<code>{x}</code>'
        )
        table.body.transform(
            2,
            bw.TableEntity.VALUE,
            lambda x: f'<span class="text-secondary">{x}</span>'
        )
        super().__init__(table)


class DocSection(bw.Panel):

    def __init__(self, content):

        class Title(bw.Anchor):
            def __init__(self, text):
                super().__init__(bw.Text(text).as_heading(1))
                self.__text = text

            @property
            def text(self):
                return self.__text

        self.__title = None
        if 'title' in content:
            self.__title = Title(content['title'])

        subtitle = None
        if 'subtitle' in content:
            subtitle = bw.Text(content['subtitle']).as_heading(2).\
                add_classes('text-muted')

        image = None
        if 'image' in content:
            image = bw.Image(content['image'], width=500)

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
                bw.Panel(code_right, image, evaluation)
            ).horizontal(),
            bw.Anchor(bw.Text('Back on Top').as_small()).link('#')
        )
        self.add_classes('mt-5')

    @property
    def title(self):
        """The section title"""
        return self.__title


class GenericPage(bw.Page):
    """Generic web-pages for demoing web-components.

    Args:
        content (WebComponent): The web-page content to show
    """
    def __init__(self, content):

        class NavLink(bw.Anchor):
            def __init__(self, section):
                super().__init__(bw.Text(section.title.text).as_small())
                self.link(section.title)

        def docgen(content):
            if isinstance(content, dict):
                items = []
                for name, tab in content.items():
                    sections = list(map(DocSection, tab))

                    toc = None
                    if len(sections) > 2:
                        navlinks = list(map(NavLink, sections))
                        toc = bw.Panel(
                            bw.Text('Navigate To').as_heading(6),
                            *navlinks
                        ).add_classes('mt-2 p-2 border bg-light').horizontal()

                    items.append(
                        bw.Navigation.Item(
                            name,
                            bw.Panel(toc, *sections),
                            len(items) == 0
                        )
                    )
                return [bw.Navigation(*items).as_tabs()]
            else:
                return list(map(DocSection, content))

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
                    bw.Anchor('Introduction').link('/introduction'),
                    bw.Anchor('Components').link('/components')
                ],
                actions=[
                    bw.Button('GitHub').
                    as_outline().
                    as_light().
                    link('https://github.com/mmgalushka/python-bootwrap')
                ]
            ),
            content=docgen(content)
        )


@app.route('/')
def home():
    with open('main.yaml', 'r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content['home']))


@app.route('/introduction')
def introduction():
    with open('main.yaml', 'r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
    return Markup(GenericPage(content['introduction']))


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
                replace('href="/introduction"', 'href="introduction.html"').\
                replace('href="/components"', 'href="components.html"')
            with open(f'docs/{filename}', 'w') as file:
                soup = BeautifulSoup(page)
                file.write(soup.prettify())

        save_page('index.html', home())
        save_page('introduction.html', introduction())
        save_page('components.html', components())

    else:
        app.run(debug=True)
