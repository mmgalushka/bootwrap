# Copyright (c) 2019 AUROMIND Ltd. All rights reserved.

"""
A web-page.
"""

from .components import (
    Link,
    Javascript,
    attr,
    inject
)

__all__ = [ 'Page' ]


class Page:
    """A web-page presenting content.

    Args:
        favicon (str): The favorite icon URL (default=None)
        resources (list): The list of Link and Javascript components which
            representing the page resources (default=None).
        title (str): The page title (default=None).
        menu (Menu): The page top level menu (default=None).
        content (WebComponent):  The page content (default=None).
    """
    def __init__(
            self,
            favicon=None,
            resources=None,
            title=None,
            menu=None,
            content=None
    ):
        super().__init__()
        self.__favicon = favicon
        self.__resources = resources
        self.__title = title
        self.__menu = menu
        self.__content = content

    def __html__(self):
        """Renders an HTML page."""
        return str(self)


    def __str__(self):
        """Renders an HTML page."""

        links = [
            Link('https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'),
            Link('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.min.css'),
            Link('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/styles/default.min.css')
        ]

        if self.__favicon:
            links.append(Link(self.__favicon, 'icon', 'image/x-icon'))

        scripts = [
            Javascript('https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js'),
            Javascript('https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'),
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/highlight.min.js'),
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/languages/python.min.js')
        ]

        if self.__resources:
            for resource in self.__resources:
                if isinstance(resource, Link):
                    links.append(resource)
                elif isinstance(resource, Javascript):
                    scripts.append(resource)
                else:
                    raise TypeError(
                        'Page resource must be either <Link> or <Javascript>,'
                        f' but got: {type(resource)};',
                    )

        title = None
        if self.__title:
            if isinstance(self.__title, str):
                title = f'''<title>{self.__title}</title>'''
            else:
                raise TypeError(
                    f'Page title must be <str>, but got: {type(resource)};',
                )

        return f'''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    {inject(*links)}
                    {inject(*scripts)}
                    {inject(title)}
                </head>
                <body>
                    {inject(self.__menu)}
                    <div class="container" style="margin-top: 90px;">
                        {inject(self.__content)}
                    </div>
                </body>
                <script>hljs.initHighlightingOnLoad();</script>
            </html>
        '''