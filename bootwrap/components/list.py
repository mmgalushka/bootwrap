"""
An external resource link.
"""

from .base import (
    WebComponent,
    ClassMixin
)
from .anchor import Anchor
from .text import Text
from .utils import attr, inject

__all__ = [ 'List' ]


class List(WebComponent, ClassMixin):
    """A web-component for list of items.

    Args:
        items (list): The list of `ListItem` to display.
    """
    def __init__(self, *items):
        super().__init__()
        self.__items = items

    class Item(Anchor):
        """A list item.
        
        Args:
            title (obj): The first-level line to define an item name. 
            description (obj): The second-level line to show additional
                information about an item (default=None).
            marker (obj): The object levelled with the item title and justified
                to the right element to present such information as a timestamp
                or badge (default=None).
            icon (obj): The object justified to the left to present an item
                icon (default=None).
            custom (obj): The object justified the right to present actions
                that can be applied to an item(default=None).
        """
        def __init__(self, title, description=None, marker=None, icon=None, custom=None):
            wc_title = title
            if wc_title:
                if isinstance(wc_title, str):
                    wc_title = Text(wc_title).as_heading(5)

            wc_description = description
            if wc_description:
                if isinstance(wc_description, str):
                    wc_description = Text(wc_description).as_small()

            wc_marker = marker
            if wc_marker:
                if isinstance(wc_marker, str):
                    wc_marker = Text(wc_marker).as_small().as_secondary()

            super().__init__(f'''
                <div class="d-flex w-100 justify-content-between">
                        {inject(icon)}
                        <div class="ml-2 mr-2 w-100">
                            <div class="d-flex w-100 justify-content-between">
                                {inject(wc_title)}
                                {inject(wc_marker)}
                            </div>
                            {inject(wc_description)}
                        </div>
                        {inject(custom)}
                </div>
            ''')
            self.add_classes('list-group-item list-group-item-action flex-column align-items-start')

        def as_active(self):
            """Makes a list item active.

            Returns:
                self
            """
            self.add_classes('active')
            return self


    def __str__(self):
        return f'''
            <div class="list-group">
                {inject(*self.__items)}
            </div>
        '''
