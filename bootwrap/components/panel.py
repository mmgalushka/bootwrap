"""
A panel.
"""

from .base import (
    WebComponent,
    CompositeMixin,
    ClassMixin
)
from .utils import attr, inject

__all__ = [ 'Panel' ]


class Panel(WebComponent, CompositeMixin, ClassMixin):
    """A web-component for a panel."""
    def __init__(self, role=None):
        super().__init__()
        self.__role = role
        self.__arrangement = None

    def with_vertical_arrangement(self):
        """Makes the panel with the vertical arrangement of encapsulating
        elements

        Returns:
            self
        """
        self.__arrangement = 'vertical'
        return self

    def with_horizontal_arrangement(self):
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
                        {attr("class", self.classes)}
                        {attr("role", self.__role)}>
                        {inject(*map(row, filter(None, self._components)))}
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
                        {attr("class", self.classes)}
                        {attr("role", self.__role)}>
                        <div class="row">
                            {inject(*map(col, filter(None, self._components)))}
                        </div>
                    </div>
                '''

        return f'''
            <div {attr("id", self.identifier)}
                {attr("class", self.classes)}
                {attr("role", self.__role)}>
                {inject(*self._components)}
            </div>
        '''