"""
A separator.
"""

from .base import WebComponent


class Separator(WebComponent):
    """A horizontal line separator."""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return '<hr/>'
