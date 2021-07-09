"""
Base web components.
"""

# flake8: noqa

from .anchor import Anchor             
from .badge import Badge
from .base import (
    WebComponent,
    ClassMixin,
    ActionMixin,
    AppearanceMixin,
    OutlineMixin,
    AvailabilityMixin,
    Breakpoint,
    Action
)
from .button import Button
from .deck import Deck
from .dialog import Dialog
from .form import (
    Form,
    Input,
    CheckboxInput,
    Freehand,
    TextInput,
    NumericInput,
    SelectInput,
    HiddenInput,
    FileInput
)
from .icon import Icon, Spinner
from .image import Image
from .javascript import Javascript
from .link import Link
from .list import List
from .navigation import Navigation
from .panel import Panel
from .separator import Separator
from .table import Table, TableEntity
from .text import Text
from .utils import attr, inject
