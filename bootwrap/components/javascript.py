"""
A javascript.
"""

from .base import WebComponent
from .utils import attr


class Javascript(WebComponent):
    """A web-component for a javascript.

    Args:
        src (str): The URL to load javascript. A URL can be absolute or
            relative.
        script (str): The javascript code.
        submap (dict): The map with substitutions, binding the javascript
            with Python objects.

    Example:
        from bootwrap import Page, Javascript

        my_page = Page(
            ...
            resources = [
                Javascript("https://ajax...0/jquery.min.js")
            ]
            ...
        )
    """
    def __init__(self, src=None, script=None, submap=None):
        super().__init__()
        self.__src = src
        self.__script = script
        self.__submap = submap

    def __str__(self):
        if self.__src:
            output = f'''
                <script {attr('src', self.__src)}
                    type="application/javascript">
                </script>
            '''
        else:
            script = self.__script
            for name, wc in self.__submap.items():
                if isinstance(wc, WebComponent):
                    substitution = str(wc.identifier)
                else:
                    substitution = str(wc)
                script = script.replace(name, substitution)

            output = f'''
                <script type="application/javascript">
                    {script}
                </script>
            '''
        return output
