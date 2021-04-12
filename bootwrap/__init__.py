"""
Wrapper for Bootstrap components.
"""

__version__ = '1.0.0-alpha4'

from .menu import Menu                 # NOQA
from .page import Page                 # NOQA

# The components __init__.py includes an exact list of importing elements,
# so we are safe to use the '*' import hear.
from .components import *              # NOQA
