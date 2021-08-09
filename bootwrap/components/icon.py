"""
An icon.
"""

from .base import (
    WebComponent,
    ClassMixin,
    AppearanceMixin
)
from .utils import attr


class Icon(WebComponent, ClassMixin, AppearanceMixin):
    """An icon.

    Args:
        name (str): The icon name.

    Example:
        from bootwrap import Icon, Panel

        output = Panel(
            Icon("fas fa-folder"),
            Icon("fas fa-folder").as_primary(),
            Icon("fas fa-folder").as_secondary(),
            Icon("fas fa-folder").as_success(),
            Icon("fas fa-folder").as_warning(),
            Icon("fas fa-folder").as_danger(),
            Icon("fas fa-folder").as_info(),
            Icon("fas fa-folder").as_light(),
            Icon("fas fa-folder").as_dark()
        )
    """

    def __init__(self, name):
        super().__init__()
        self.__name = name

    def __str__(self):
        self.add_classes(self.__name)

        if self._category is not None:
            self.add_classes('text-%s' % self._category)

        return f'''
            <i {attr('id', self.identifier)}
                {attr('class', self.classes)}>
            </i>
        '''


class Spinner(WebComponent, ClassMixin, AppearanceMixin):
    """A spinner icon.

    Example:
        from bootwrap import Spinner, Panel

        output = Panel(
            Spinner(),
            Spinner().as_primary(),
            Spinner().as_secondary(),
            Spinner().as_success(),
            Spinner().as_warning(),
            Spinner().as_danger(),
            Spinner().as_info(),
            Spinner().as_light(),
            Spinner().as_dark()
        )
    """

    def __str__(self):
        self.add_classes('spinner')

        if self._category is not None:
            self.add_classes('text-%s' % self._category)

        return f'''
            <span {attr('id', self.identifier)}
                {attr('class', self.classes)}>
            </span>
        ''' + '''
            <style>
                @keyframes spinner-border {
                    to { transform: rotate(360deg); }
                }

                .spinner{
                    display: inline-block;
                    vertical-align: text-bottom;
                    height: 16px;
                    width: 16px;
                    border: .15em solid currentColor;
                    border-right-color: transparent;
                    border-radius: 50%;
                    -webkit-animation: spinner-border .75s linear infinite;
                    animation: spinner-border .75s linear infinite;
                }
            </style>
        '''
