"""
A separator.
"""

from .base import WebComponent


class Separator(WebComponent):
    """A horizontal line separator.

    Example:
        from bootwrap import Panel, Separator, Text

        output = Panel(
            Text("Top Text"),
            Separator(),
            Text("Bottom Text")
        )
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return '<hr/>'
