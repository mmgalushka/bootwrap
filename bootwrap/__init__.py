"""
Wrapper for Bootstrap components.
"""

# flake8: noqa
# pylint: disable=unused-variable

from .menu import Menu
from .page import Page
from .auth import Signup as SignupPage
from .auth import Login as LoginPage

# The components __init__.py includes an exact list of importing elements,
# so we are safe to use the '*' import hear.
from .components import *
