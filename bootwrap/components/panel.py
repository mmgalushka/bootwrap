"""
A panel.
"""

from .base import (
    WebComponent,
    ClassMixin
)
from .utils import attr, inject

__all__ = [ 'Panel' ]


class Panel(WebComponent, ClassMixin):
    """A web-component for a panel."""
    def __init__(self, *components):
        super().__init__()
        self.__components = components
        self.__arrangement = None

    def __iter__(self):
        return iter(self.__components)

    def vertical(self):
        """Makes the panel with the vertical arrangement of encapsulating
        elements

        Returns:
            self
        """
        self.__arrangement = 'vertical'
        return self

    def horizontal(self):
        """Makes the panel with the horizontal arrangement of encapsulating
        elements

        Returns:
            self
        """
        self.__arrangement = 'horizontal'
        return self

    def __str__(self):
        if self.__arrangement:
            if self.__arrangement == 'vertical':

                def row(element):
                    return f'''
                        <div class="row">
                            <div class="col-md">
                                {element}
                            </div>
                        </div>
                    '''
                return f'''
                    <div {attr("id", self.identifier)}
                        {attr("class", self.classes)}>
                        {inject(*map(row, filter(None, self.__components)))}
                    </div>
                '''
            else: # self.__arrangement == 'horizontal'

                def col(element):
                    return f'''
                        <div class="col-md">
                            {element}
                        </div>
                    '''
                return f'''
                    <div {attr("id", self.identifier)}
                        {attr("class", self.classes)}>
                        <div class="row">
                            {inject(*map(col, filter(None, self.__components)))}
                        </div>
                    </div>
                '''

        return f'''
            <div {attr("id", self.identifier)}
                {attr("class", self.classes)}>
                {inject(*self.__components)}
            </div>
        '''