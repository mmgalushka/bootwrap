"""
A collection of items.
"""

from .base import WebComponent, ClassMixin
from .anchor import Anchor
from .button import Button
from .text import Text
from .utils import attr, inject


class List(WebComponent, ClassMixin):
    """A web component for a list of items.

    Args:
        *items (list): The `list` of `List.Item` elements.

    Example:
        from bootwrap import Button, List, Image

        actions = [
            Button("Buy"),
            Button("Sell"),
            Button("Transfer")
        ]

        List(
            List.Item(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=32, height=32),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().as_selected().link(
                "https://www.google.com"),
            List.Item(
                "LinkedIn (NASDAQ: LNKD)",
                description= "Price for a single LinkedIn share",
                figure=Image("linkedin-logo.png", width=32, height=32),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.linkedin.com"),
            List.Item(
                "Amazon (NASDAQ: AMZN)",
                description= "Price for a single Amazon share",
                figure=Image("amazon-logo.png", width=32, height=32),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.amazon.com")
        )

    Demo:
        from bootwrap import Button, List, Image
        actions = [
            Button("Buy").as_success(),
            Button("Sell"),
            Button("Transfer")
        ]
        output = List(
            List.Item(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=32, height=32),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().as_selected().link(
                "https://www.google.com"),
            List.Item(
                "LinkedIn (NASDAQ: LNKD)",
                description= "Price for a single LinkedIn share",
                figure=Image("linkedin-logo.png", width=32, height=32),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.linkedin.com"),
            List.Item(
                "Amazon (NASDAQ: AMZN)",
                description= "Price for a single Amazon share",
                figure=Image("amazon-logo.png", width=32, height=32),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.amazon.com")
        )
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
            description (str|WebComponent): The item description.
            marker (str|WebComponent): The item marker.
            figure (str|WebComponent): The item figure.

        Example:
            from bootwrap import Button, List, Image

            actions = [
                Button("Buy"),
                Button("Sell"),
                Button("Transfer")
            ]

            List.Item(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=32, height=32),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).link(
                "https://www.google.com")

        Demo:
            from bootwrap import Button, List, Image

            actions = [
                Button("Buy"),
                Button("Sell"),
                Button("Transfer")
            ]

            output = List.Item(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=32, height=32),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).link(
                "https://www.google.com")
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

            Example:
                from bootwrap import Button, List, Image

                actions = [
                    Button("Buy"),
                    Button("Sell"),
                    Button("Transfer")
                ]

                List.Item(
                    "Google (NASDAQ: GOOGL)",
                    description= "Price for a single Google share",
                    figure=Image("google-logo.png", width=32, height=32),
                    marker="12:04:58 12/01/2021"
                ).add_menu(*actions).as_selected().link(
                    "https://www.google.com")

            Demo:
                from bootwrap import Button, List, Image

                actions = [
                    Button("Buy"),
                    Button("Sell"),
                    Button("Transfer")
                ]

                output = List.Item(
                    "Google (NASDAQ: GOOGL)",
                    description= "Price for a single Google share",
                    figure=Image("google-logo.png", width=32, height=32),
                    marker="12:04:58 12/01/2021"
                ).add_menu(*actions).as_selected().link(
                    "https://www.google.com")
            """
            self._selected = True
            return self

        def pack_actions(self):
            """Makes item actions packed under a drop-down menu.

            Returns:
                self

            Example:
                from bootwrap import Button, List, Image

                actions = [
                    Button("Buy"),
                    Button("Sell"),
                    Button("Transfer")
                ]

                List.Item(
                    "Google (NASDAQ: GOOGL)",
                    description= "Price for a single Google share",
                    figure=Image("google-logo.png", width=32, height=32),
                    marker="12:04:58 12/01/2021"
                ).add_menu(*actions).pack_actions().link(
                    "https://www.google.com")

            Demo:
                from bootwrap import Button, List, Image

                actions = [
                    Button("Buy"),
                    Button("Sell"),
                    Button("Transfer")
                ]

                output = List.Item(
                    "Google (NASDAQ: GOOGL)",
                    description= "Price for a single Google share",
                    figure=Image("google-logo.png", width=32, height=32),
                    marker="12:04:58 12/01/2021"
                ).add_menu(*actions).pack_actions().link(
                    "https://www.google.com")
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

            self.add_classes(
                'list-group-item list-group-item-action flex-column '
                'align-items-start'
            )
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
    """A web component for a deck of cards.

    Args:
        *cards (list): The `list` of `Deck.Card` elements.

    Example:
        from bootwrap import Button, Deck, Image

        actions = [
            Button("Buy"),
            Button("Sell"),
            Button("Transfer")
        ]

        Deck(
            Deck.Card(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=128).add_classes(
                    "mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.google.com"),
            Deck.Card(
                "LinkedIn (NASDAQ: LNKD)",
                description= "Price for a single LinkedIn share",
                figure=Image("linkedin-logo.png", width=128).add_classes(
                    "mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.linkedin.com"),
            Deck.Card(
                "Amazon (NASDAQ: AMZN)",
                description= "Price for a single Amazon share",
                figure=Image("amazon-logo.png", width=128).add_classes(
                    "mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.amazon.com")
        )

    Demo:
        from bootwrap import Button, Deck, Image
        actions = [
            Button("Buy"),
            Button("Sell"),
            Button("Transfer")
        ]
        output = Deck(
            Deck.Card(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=128).add_classes(
                    "mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.google.com"),
            Deck.Card(
                "LinkedIn (NASDAQ: LNKD)",
                description= "Price for a single LinkedIn share",
                figure=Image("linkedin-logo.png", width=128).add_classes(
                    "mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.linkedin.com"),
            Deck.Card(
                "Amazon (NASDAQ: AMZN)",
                description= "Price for a single Amazon share",
                figure=Image("amazon-logo.png", width=128).add_classes(
                    "mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.amazon.com")
        )
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
            description (str|WebComponent): The card description.
            marker (str|WebComponent): The card marker.
            figure (str|WebComponent): The card figure.

        Example:
            from bootwrap import Button, Deck, Image

            actions = [
                Button("Buy"),
                Button("Sell"),
                Button("Transfer")
            ]

            Deck.Card(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=128).add_classes("mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).link(
                "https://www.google.com")

        Demo:
            from bootwrap import Button, Deck, Image

            actions = [
                Button("Buy"),
                Button("Sell"),
                Button("Transfer")
            ]

            output = Deck.Card(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=128).add_classes("mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).link(
                "https://www.google.com")
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

        Example:
            from bootwrap import Button, Deck, Image

            actions = [
                Button("Buy"),
                Button("Sell"),
                Button("Transfer")
            ]

            Deck.Card(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=128).add_classes("mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.google.com")

        Demo:
            from bootwrap import Button, Deck, Image

            actions = [
                Button("Buy"),
                Button("Sell"),
                Button("Transfer")
            ]

            output = Deck.Card(
                "Google (NASDAQ: GOOGL)",
                description= "Price for a single Google share",
                figure=Image("google-logo.png", width=128).add_classes("mt-3"),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.google.com")
            """
            self._pack_actions = True
            return self

        def __str__(self):
            wc_title = self._title
            if isinstance(wc_title, str):
                wc_title = Text(wc_title).as_heading(5).\
                    add_classes('card-title')
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
