"""
A collection of items.
"""

from .base import ActionMixin, WebComponent, ClassMixin
from .button import Button
from .text import Text
from .utils import attr, inject


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
                figure=Image("google-logo.png", width=128).mt(3),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.google.com"),
            Deck.Card(
                "LinkedIn (NASDAQ: LNKD)",
                description= "Price for a single LinkedIn share",
                figure=Image("linkedin-logo.png", width=128).mt(3),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.linkedin.com"),
            Deck.Card(
                "Amazon (NASDAQ: AMZN)",
                description= "Price for a single Amazon share",
                figure=Image("amazon-logo.png", width=128).mt(3),
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
                figure=Image("google-logo.png", width=128).mt(3),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.google.com"),
            Deck.Card(
                "LinkedIn (NASDAQ: LNKD)",
                description= "Price for a single LinkedIn share",
                figure=Image("linkedin-logo.png", width=128).mt(3),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.linkedin.com"),
            Deck.Card(
                "Amazon (NASDAQ: AMZN)",
                description= "Price for a single Amazon share",
                figure=Image("amazon-logo.png", width=128).mt(3),
                marker="12:04:58 12/01/2021"
            ).add_menu(*actions).pack_actions().link(
                "https://www.amazon.com")
        )
    """

    def __init__(self, *cards):
        super().__init__()

        for card in cards:
            if not isinstance(card, Deck.Card):
                print(Deck.Card.__name__)
                raise TypeError(
                    f'A deck must contain the <class \'Deck.Card\'> only '
                    f'but got {type(card)};'
                )
        self._cards = cards

    class Card(WebComponent, ActionMixin):
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
                figure=Image("google-logo.png", width=128).mt(3),
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
                figure=Image("google-logo.png", width=128).mt(3),
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
                figure=Image("google-logo.png", width=128).mt(3),
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
                figure=Image("google-logo.png", width=128).mt(3),
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
                    # for action in self._menu:
                    #     action.ml(1)
                    wc_actions = f'''
                        <div class="card-footer text-right">
                            {inject(*self._menu)}
                        </div>
                    '''

            onclick = None
            if self._target:
                onclick = f"location.href='{self._target}';"

            return f'''
                <div class="card">
                    <div class="row justify-content-center" {attr('onclick', onclick)}>
                        {inject(self._figure)}
                    </div>
                    <div class="card-body" {attr('onclick', onclick)}>
                        {inject(wc_marker)}
                        {inject(wc_title)}
                        {inject(self._description)}
                    </div>
                    {inject(wc_actions)}
                </div>
            '''

    def __str__(self):
        style = '''
            <style>
                div.card {
                    cursor:pointer
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
