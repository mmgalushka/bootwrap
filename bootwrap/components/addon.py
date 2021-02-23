# Copyright (c) 2019 AUROMIND Ltd. All rights reserved.

"""
Web-components providing not essential functions.
"""

from .base import WebComponent

__all__ = [ 'Separator' ]


class Separator(WebComponent):
    """A horizontal line separator."""
    def __init__(self):
        super().__init__()

    def __str__(self):
        return '<hr/>'
