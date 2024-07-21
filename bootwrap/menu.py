"""
A menu bar.
"""

from .components import Text, inject


class Menu:
    """A web component for a menu bar at the page top.

    Args:
        logo (Image): The <code>Image</code> representing a company or
            organization logo (default=None).
        brand (Text):  The the <code>Text</code> representing a company,
            organization, or a project (default=None).
        anchors (list): The list of <code>Anchor</code> allowing to navigate
            to the different pages from the top-level menu (default=None).
        actions (list): The list of <code>Button</code> allowing to perform
            specific actions such as login, logout, etc. (default=None).
    """

    def __init__(self, logo=None, brand=None, anchors=None, actions=None):
        super().__init__()
        self.__logo = logo

        if brand is not None:
            if not isinstance(brand, Text):
                raise TypeError(
                    'Parameter "brand" expected <class "Text">, '
                    f'but got {type(brand)}'
                )
        self.__brand = brand

        self.__anchors = anchors
        self.__actions = actions

    def __str__(self):
        anchors = ''
        if self.__anchors is not None:
            anchors = '\n'.join([
                f'''
                    <li class="nav-item">
                        {inject(anchor.ms(2).add_classes('nav-link'))}
                    </li>
                '''
                for anchor in self.__anchors
            ])

        actions = ''
        if self.__actions is not None:
            actions = '\n'.join([
                f'''{inject(action.ms(2))}'''
                for action in self.__actions
            ])

        return f'''
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
                {inject(self.__logo, self.__brand)}
                <button class="navbar-toggler"
                    type="button" data-bs-toggle="collapse"
                    data-bs-target="#menu"
                    aria-controls="menu"
                    aria-expanded="false"
                    aria-label="Toggle menu">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="menu">
                    <ul class="navbar-nav me-auto">
                        {anchors}
                    </ul>
                    {actions}
                </div>
            </nav>
        '''
