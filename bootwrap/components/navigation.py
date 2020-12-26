"""
A tabs style navigation.
"""

from collections import namedtuple

from .base import (
    WebComponent,
    ClassMixin, 
    CompositeMixin
)
from .anchor import Anchor
from .panel import Panel
from .utils import attr, inject

__all__ = [ 'Navigation' ]


NavigationItem = namedtuple('NavigationItem', 'anchor panel')


class Navigation(WebComponent, ClassMixin, CompositeMixin):
    """A web-component for a tabs style navigation."""
    def __init__(self):
        super().__init__()
        self.__vertical = False

    def as_vertical(self):
        """Makes the navigation vertical.

        Returns:
            self
        """
        self.__vertical = True
        return self

    def as_tabs(self):
        """Makes the navigation controls looks like buttons.

        Returns:
            self
        """
        return self.add_classes('nav-tabs')


    def as_pills(self):
        """Makes the navigation controls looks like buttons.

        Returns:
            self
        """
        return self.add_classes('nav-pills')


    def append(self, *components):
        """Appends an item to the navigation control.
        
        The appending item should be <class "tuple"> with the following
        structure (name, content, active):
        
        name    - the component name, should be <class "str">;
        content - the component content, should be <class "WebComponent">;
        active  - the flag for (in)active component, should be <class "bool">;

        Return:
            self
        """
        explanation = '''
            The appending item should be <class "tuple"> with the following
            structure (name, content, active):
            
            name    - the component name, should be <class "str">;
            content - the component content, should be <class "WebComponent">;
            active  - the flag for (in)active component, should be <class "bool">;
        '''
        for i, c in enumerate(list(components)):
            if not isinstance(c, tuple):
                raise TypeError(
                    f'''Parameter "components[{i}]" expected to be 
                    <class "tuple">, but got {type(c)};
                    
                    {explanation}
                    '''
                )
            
            if not isinstance(c[0], str):
                raise TypeError(
                    f'''Parameter "components[{i}][0]" expected to be 
                    <class "str">, but got {type(c)};
                    
                    {explanation}
                    '''
                )
            name = c[0]

            if not isinstance(c[1], WebComponent):
                raise TypeError(
                    f'''Parameter "components[{i}][1]" expected to be 
                    <class "WebComponent">, but got {type(c)};
                    
                    {explanation}
                    '''
                )
            content = c[1]

            if not isinstance(c[2], bool):
                raise TypeError(
                    f'''Parameter "components[{i}][2]" expected to be <class "bool">,
                    but got {type(c)};
                    
                    {explanation}
                    '''
                )
            active = c[2]

            panel_classes = "tab-pane fade"
            if active:
                panel_classes += " show active"
            panel = Panel('tabpanel').\
                add_classes(panel_classes).\
                append(content)
            
            anchor_classes = "nav-link"
            if active:
                anchor_classes += " active"
            anchor = Anchor(name, "tab").\
                toggle(panel).\
                add_classes(anchor_classes)

            super().append(NavigationItem(anchor, panel))

        return self

    def __str__(self):
        navs, panels = [], []
        for component in self._components:
            navs.append(f'''<li class="nav-item">{inject(component.anchor)}</li>''')
            panels.append(component.panel)

        classes = 'nav'
        if self.__vertical:
            classes += ' flex-column'
        if self.classes:
            classes += f' {self.classes}'

        output = f'''
            <ul {attr("id", self.identifier)}
                {attr('class', classes)}
                role="tablist">
                {''.join(navs)}
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

