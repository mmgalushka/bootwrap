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
                        action.ml(1)
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
