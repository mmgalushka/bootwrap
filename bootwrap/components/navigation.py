"""
A tabs style navigation.
"""

from collections import namedtuple

from .base import (
    WebComponent,
    ClassMixin
)
from .anchor import Anchor
from .panel import Panel
from .utils import attr, inject


NavigationItem = namedtuple('NavigationItem', 'anchor panel')


class Navigation(WebComponent, ClassMixin):
    """A web component for navigation.

    Args:
        *items (list): The list of `Navigation.Item`.

    Example:
        from bootwrap import Navigation

        Navigation(
            Navigation.Item('Chapter 1', 'Text 1', True),
            Navigation.Item('Chapter 2', 'Text 2'),
            Navigation.Item('Chapter 3', 'Text 3')
        )

    Demo:
        from bootwrap import Navigation

        output = Navigation(
            Navigation.Item('Chapter 1', 'Text 1', True),
            Navigation.Item('Chapter 2', 'Text 2'),
            Navigation.Item('Chapter 3', 'Text 3')
        )
    """

    def __init__(self, *items):
        super().__init__()
        self.__items = items
        self.__vertical = False

    class Item(WebComponent):
        def __init__(self, name, content, active=False):
            super().__init__()
            self.__name = name
            self.__content = content
            self.__active = active

        @property
        def name(self):
            return self.__name

        @property
        def content(self):
            return self.__content

        @property
        def active(self):
            return self.__active

    def as_vertical(self):
        """Makes the navigation vertical.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Navigation

            Navigation(
                Navigation.Item('Chapter 1', 'Text 1', True),
                Navigation.Item('Chapter 2', 'Text 2'),
                Navigation.Item('Chapter 3', 'Text 3')
            ).as_vertical()

        Demo:
            from bootwrap import Navigation

            output = Navigation(
                Navigation.Item('Chapter 1', 'Text 1', True),
                Navigation.Item('Chapter 2', 'Text 2'),
                Navigation.Item('Chapter 3', 'Text 3')
            ).as_vertical()
        """
        self.__vertical = True
        return self

    def as_tabs(self):
        """Makes the navigation controls looks like buttons.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Navigation

            Navigation(
                Navigation.Item('Chapter 1', 'Text 1', True),
                Navigation.Item('Chapter 2', 'Text 2'),
                Navigation.Item('Chapter 3', 'Text 3')
            ).as_tabs()

        Demo:
            from bootwrap import Navigation

            output = Navigation(
                Navigation.Item('Chapter 1', 'Text 1', True),
                Navigation.Item('Chapter 2', 'Text 2'),
                Navigation.Item('Chapter 3', 'Text 3')
            ).as_tabs()
        """
        return self.add_classes('nav-tabs')

    def as_pills(self):
        """Makes the navigation controls looks like buttons.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Navigation

            Navigation(
                Navigation.Item('Chapter 1', 'Text 1', True),
                Navigation.Item('Chapter 2', 'Text 2'),
                Navigation.Item('Chapter 3', 'Text 3')
            ).as_pills()

        Demo:
            from bootwrap import Navigation

            output = Navigation(
                Navigation.Item('Chapter 1', 'Text 1', True),
                Navigation.Item('Chapter 2', 'Text 2'),
                Navigation.Item('Chapter 3', 'Text 3')
            ).as_pills()
        """
        return self.add_classes('nav-pills')

    def __str__(self):
        menus, panels = [], []
        for item in self.__items:

            panel_classes = "tab-pane fade"
            if item.active:
                panel_classes += " active show"
            panel = Panel(item.content).add_classes(panel_classes)
            panels.append(panel)

            anchor_classes = "nav-link"
            if item.active:
                anchor_classes += " active"
            anchor = Anchor(item.name).add_classes(anchor_classes).\
                toggle(panel)
            menus.append(
                f'''
                    <li class="nav-item">
                        {inject(anchor)}
                    </li>
                '''
            )

        classes = 'nav'
        if self.__vertical:
            classes += ' flex-column'
        if self.classes:
            classes += f' {self.classes}'

        output = f'''
            <ul {attr("id", self.identifier)}
                {attr('class', classes)}
                role="tablist">
                {''.join(menus)}
            </ul>
            <div class="tab-content">
                {inject(*panels)}
            </div>
        '''

        if self.__vertical:
            output = f'''
                <div class="d-flex">{output}</div>
            '''

        return output
