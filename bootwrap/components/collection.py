"""
A collection of items.
"""

from abc import ABC, abstractmethod
from .base import (
    WebComponent,
    ClassMixin
)
from .anchor import Anchor
from .button import Button
from .text import Text
from .utils import attr, inject

__all__ = [ 'List', 'Deck' ]


class List(WebComponent, ClassMixin):
    """A web-component for a list of items.

    Args:
        items (list<List.Item>): The items to set.
    """
    def __init__(self, *items):
        super().__init__()

        for item in items:
            if not isinstance(item, List.Item):
                raise TypeError(
                    f'A list must contain the {List.Item.__class__} only '
                    f'but got {type(item)};'
                )
        self._items = items

    class Item(Anchor):
        """A list item.
        
        Args:
            title (str|WebComponent): The item title. 
            description (str|WebComponent): The item description (default=None).
            marker (str|WebComponent): The item marker (default=None).
            figure (str|WebComponent): The item figure (default=None).
        """
        def __init__(self, title, description=None, marker=None, figure=None):
            super().__init__()
            self._title = title
            self._description = description
            self._marker = marker
            self._figure = figure
            self._selected = False
            self._pack_actions = False

        def as_selected(self):
            """Makes a list item selected.
            
            Returns:
                self
            """
            self._selected = True
            return self

        def pack_actions(self):
            """Makes item actions packed under a drop-down menu.
            
            Returns:
                self
            """
            self._pack_actions = True
            return self


        def __str__(self):
            wc_title = self._title
            if wc_title:
                if isinstance(wc_title, str):
                    wc_title = Text(wc_title).as_heading(5)

            wc_marker = self._marker
            if wc_marker:
                if isinstance(wc_marker, str):
                    wc_marker = Text(wc_marker).as_small()

            wc_actions = None
            if self._menu:
                if self._pack_actions:
                    wc_actions = Button('...').add_menu(*self._menu)
                else:
                    for action in self._menu:
                        action.add_classes('ml-1')
                    wc_actions = inject(*self._menu)
                wc_actions = f'''
                    <div class="d-flex align-items-start">
                        {inject(wc_actions)}
                    </div>
                '''

            self._inner = f'''
                <div class="d-flex w-100 justify-content-between">
                    {inject(self._figure)}
                    <div class="ml-2 mr-2 w-100">
                        <div class="d-flex w-100 justify-content-between">
                            {inject(wc_title)}
                            {inject(wc_marker)}
                        </div>
                        {inject(self._description)}
                    </div>
                    {inject(wc_actions)}
                </div>
            '''

            self.add_classes('list-group-item list-group-item-action flex-column align-items-start')
            if self._selected:
                self.add_classes('active')

            return super().__str__()

    def __str__(self):
        self.add_classes('list-group')
        return f'''
            <div {attr("id", self.identifier)}    
                {attr('class', self.classes)}>
                {inject(*self._items)}
            </div>
        '''


class Deck(WebComponent, ClassMixin):
    """A web-component for a deck of cards.

    Args:
        items (list<Deck.Card>): The cards to set.
    """
    def __init__(self, *cards):
        super().__init__()

        for card in cards:
            if not isinstance(card, Deck.Card):
                raise TypeError(
                    f'A deck must contain the {Deck.Card.__class__} only '
                    f'but got {type(card)};'
                )
        self._cards = cards

    class Card(Anchor):
        """A deck card.
        
        Args:
            title (str|WebComponent): The card title. 
            description (str|WebComponent): The card description (default=None).
            marker (str|WebComponent): The card marker (default=None).
            figure (str|WebComponent): The card figure (default=None).
        """
        def __init__(self, title, description=None, marker=None, figure=None):
            super().__init__()
            self._title = title
            self._description = description
            self._marker = marker
            self._figure = figure
            self._pack_actions = False

        def pack_actions(self):
            """Makes item actions packed under a drop-down menu.
            
            Returns:
                self
            """
            self._pack_actions = True
            return self

        def __str__(self):
            wc_title = self._title
            if isinstance(wc_title, str):
                wc_title = Text(wc_title).as_heading(5).add_classes('card-title')
            else:
                wc_title.add_classes('card-title')

            wc_marker = self._marker
            if wc_marker:
                if isinstance(wc_marker, str):
                    wc_marker = Text(wc_marker).as_small().as_muted()
                wc_marker = f'''
                    <div class="text-right mb-2"> 
                        {inject(wc_marker)}
                    </div>
                '''

            wc_actions = None
            if self._menu:
                if self._pack_actions:
                    wc_actions = f'''
                        <div class="card-footer text-right"> 
                            {inject(Button("...").add_menu(*self._menu))}
                        </div>
                    '''
                else:
                    for action in self._menu:
                        action.add_classes('ml-1')
                    wc_actions = f'''
                        <div class="card-footer text-right"> 
                            {inject(*self._menu)}
                        </div>
                    '''

            self._inner = f'''
                <div class="row justify-content-center">
                    {inject(self._figure)}
                </div>
                <div class="card-body">
                    {inject(wc_marker)}
                    {inject(wc_title)}
                    {inject(self._description)}
                </div>
                {inject(wc_actions)}
            '''

            self.add_classes('card')

            return super().__str__()

    def __str__(self):
        style = '''
            <style>
                a.card {
                    text-decoration: none;
                }

                a.card, a.card:visited, a.card:hover, a.card:active {
                    color: inherit;
                }
            </style>
        '''
        
        self.add_classes('card-deck grid-container')
        return f'''
            <div {attr("id", self.identifier)}
                {attr('class', self.classes)}>
                {inject(*self._cards)}
            </div>
            {style}
        '''
