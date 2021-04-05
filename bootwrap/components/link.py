"""
An external resource link.
"""

from .base import WebComponent
from .utils import attr


class Link(WebComponent):
    """A web-component for an external resource link.

    See https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link
    for more information.

    Args:
        href (str): This attribute specifies the URL of the linked resource.
            A URL can be absolute or relative (from MDN WebDoc).
        rel (str): This attribute names a relationship of the linked document
            to the current document (from MDN WebDoc).
        ctype (str): This attribute is used to define the type of the content
            linked to (from MDN WebDoc).

    Example:
        from bootwrap import Page, Link

        my_page = Page(
            ...
            resources = [
                Link("https://cdnjs.cloudflare.com/.../all.min.css")
            ]
            ...
        )
    """
    def __init__(self, href, rel='stylesheet', ctype='text/css'):
        super().__init__()
        self.__rel = rel
        self.__ctype = ctype
        self.__href = href

    def __str__(self):
        return f'''
            <link {attr('rel', self.__rel)}
                {attr('type', self.__ctype)}
                {attr('href', self.__href)}/>
        '''
