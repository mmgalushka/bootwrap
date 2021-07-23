"""
A web-page.
"""

from .components import Link, Javascript, inject


class Page:
    """A web-page presenting container.

    Args:
        favicon (str): The file name for the favorite icon displayed in a
            browser tab(default=None)
        title (str): The page title, displayed in a browser tab (default=None).
        resources (list): The list of `Link` and `Javascript` components which
            representing the page resources (default=None).
        menu (Menu): The page top level menu (default=None).
        container (WebComponent): The page container (default=None).
    """

    def __init__(
            self,
            favicon=None,
            resources=None,
            title=None,
            menu=None,
            container=None
    ):
        super().__init__()
        self.__favicon = favicon
        self.__resources = resources
        self.__title = title
        self.__menu = menu
        self.__container = container

    def __html__(self):
        """Renders an HTML page."""
        return str(self)

    def __str__(self):
        """Renders an HTML page."""

        links = [
            Link('https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'),                   # NOQA
            Link('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.min.css'),               # NOQA
            Link('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/styles/default.min.css')        # NOQA
        ]

        if self.__favicon:
            links.append(Link(self.__favicon, 'icon', 'image/x-icon'))

        scripts = [
            Javascript('https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js'),                  # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js'),         # NOQA
            Javascript('https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'),               # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/highlight.min.js'),       # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.5.0/languages/python.min.js')  # NOQA
        ]

        if self.__resources:
            for resource in self.__resources:
                if isinstance(resource, Link):
                    links.append(resource)
                elif isinstance(resource, Javascript):
                    scripts.append(resource)
                else:
                    raise TypeError(
                        'Page resource must be either <class "Link"> or '
                        f'<class "Javascript">, but got: {type(resource)};',
                    )

        title = None
        if self.__title:
            if isinstance(self.__title, str):
                title = f'''<title>{self.__title}</title>'''
            else:
                raise TypeError(
                    f'Page title must be <str>, but got: {type(title)};',
                )

        return f'''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <meta name="viewport"
                        container="width=device-width, initial-scale=1,
                        shrink-to-fit=no"/>
                    {inject(*links)}
                    {inject(*scripts)}
                    {inject(title)}
                </head>
                <body>
                    {inject(self.__menu)}
                    <div class="container" style="margin-top: 90px;">
                        {inject(self.__container)}
                    </div>
                </body>
                <script>hljs.initHighlightingOnLoad();</script>
            </html>
        '''
