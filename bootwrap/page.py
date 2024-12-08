"""
A web-page.
"""

import re
import pkg_resources

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
        self.__vars = {}

    def __html__(self):
        """Renders an HTML page."""
        return str(self)

    def background(self, color=None, image=None, position=None, size=None,
                   repeat=None, origin=None, clip=None, attachment=None):
        """Configures the page background.

        See <a href="https://www.w3schools.com/cssref/css3_pr_background.asp">
        form more information.

        Args:
            color (str): The background color to used.
            image(str): The background images to used.
            position(str): The position of the background images.
            size(str): The size of the background images.
            repeat(str): The parameter to define of how to repeat the
                background images.
            origin(str): The positioning area of the background images.
            clip(str): The painting area of the background images.
            attachment (str): The parameter to define whether the background
                images are fixed or scrolls with the rest of the page.

        Returns:
            obj (self): The instance of this class.
        """
        if color:
            self.__vars['--body-background-color'] = color
        if image:
            self.__vars['--body-background-image'] = image
        if position:
            self.__vars['--body-background-position'] = position
        if size:
            self.__vars['background-size'] = size
        if repeat:
            self.__vars['--body-background-repeat'] = repeat
        if origin:
            self.__vars['--body-background-origin'] = origin
        if clip:
            self.__vars['--body-background-clip'] = clip
        if attachment:
            self.__vars['--body-background-attachment'] = attachment
        return self

    def __str__(self):
        """Renders an HTML page."""
        # Collects CSS supporting Bootstrap stypes.
        links = [
            Link('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css'),                 # NOQA
            Link('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css'),               # NOQA
            Link('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css')        # NOQA
        ]

        # Collects FABICON showing in tab.
        if self.__favicon:
            links.append(Link(self.__favicon, 'icon', 'image/x-icon'))

        # Collects JS scriptis supporting JQuery and code highlights.
        scripts = [
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js'),                  # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js'),          # NOQA
            Javascript('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js'),       # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js'),        # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/python.min.js'), # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/json.min.js'),   # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/yaml.min.js'),   # NOQA
            Javascript('https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/languages/bash.min.js')    # NOQA
        ]

        # Adds customer defined resources which could be CSS or JS files.
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

        # Sets the page title.
        title = None
        if self.__title:
            if isinstance(self.__title, str):
                title = f'''<title>{self.__title}</title>'''
            else:
                raise TypeError(
                    f'Page title must be <str>, but got: {type(title)};',
                )

        # Creates inner style which will be embedded in the page.
        root_vars = ''
        if len(self.__vars) > 0:
            for name, value in self.__vars.items():
                root_vars += '%s: %s;' % (name, value)
        root_vars += '--container-margin-top: %s' % (
            '90px' if self.__menu else '10px'
        )
        root_vars = ':root{' + root_vars + '}'


        inner_style = pkg_resources.resource_string(__name__, 'generic.css').\
            decode('utf-8')
        inner_style = root_vars + inner_style
        inner_style = re.sub('\\n|\\s\\s+', ' ', inner_style)

        # Creates inner script which will be embedded in the page.
        inner_script = pkg_resources.resource_string(__name__, 'generic.js').\
            decode('utf-8')
        inner_script = re.sub('\\n|\\s\\s+', ' ', inner_script)

        return f'''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8"/>
                    <meta name="viewport"
                        content="width=device-width, initial-scale=1,
                        shrink-to-fit=no"/>
                    {inject(*links)}
                    {inject(*scripts)}
                    {inject(title)}
                </head>
                <body>
                    {inject(self.__menu)}
                    <div class="container-fluid">
                        {inject(self.__container)}
                    </div>
                </body>
                <script>{inner_script}</script>
                <style>{inner_style}</style>
            </html>
        '''
