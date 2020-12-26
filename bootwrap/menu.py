# Copyright (c) 2019 AUROMIND Ltd. All rights reserved.

"""
A menu bar.
"""

import uuid

from .components import (
    Anchor,
    Text,
    attr, inject
) 


__all__ = ['Menu']


class Menu:
    """A web-component for a menu bar at the page top.

    Args:
        logo (Image): The logo (default=None).
        brand (Text):  The brand (default=None).
        anchors (list): The menu anchors (default=None).
        actions (list): The menu top-level actions (default=None).
    """
    def __init__(self, logo=None, brand=None, anchors=None, actions=None):
        super().__init__()
        self.__logo = logo

        if not isinstance(brand, Text):
            raise TypeError(
                'Parameter "brand" expected <class "Text">, '
                f'but got {type(brand)}'
            )
        self.__brand = brand

        self.__anchors = anchors
        self.__actions= actions




    def __str__(self):
        anchors = ''
        if self.__anchors is not None:
            anchors = '\n'.join([
                f'''
                    <li class="nav-item">
                        {inject(anchor.add_classes('nav-link ml-2'))}
                    </li>
                '''
                for anchor in self.__anchors
            ])

        actions = ''
        if self.__actions is not None:
            actions = '\n'.join([
                f'''{inject(action.add_classes('ml-2'))}'''
                for action in self.__actions
            ])

        return f'''
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
                {inject(self.__logo, self.__brand.add_classes('ml-1 mr-2'))}
                <button class="navbar-toggler"
                    type="button" data-toggle="collapse"
                    data-target="#menu"
                    aria-controls="menu"
                    aria-expanded="false"
                    aria-label="Toggle menu">
                    <span class="navbar-toggler-icon"></span>
                </button>
                
                <div class="collapse navbar-collapse" id="menu">
                    <ul class="navbar-nav mr-auto">
                        {anchors}
                    </ul>
                    {actions}
                </div>
            </nav>
        '''
