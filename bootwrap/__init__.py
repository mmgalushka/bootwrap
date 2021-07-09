"""
Wrapper for Bootstrap components.
"""

# flake8: noqa
# pylint: disable=unused-variable

__version__ = '1.0.0-alpha4'

from .menu import Menu
from .page import Page

# The components __init__.py includes an exact list of importing elements,
# so we are safe to use the '*' import hear.
from .components import *
