"""
A panel.
"""

from .base import WebComponent, ClassMixin
from .utils import attr, inject


class Panel(WebComponent, ClassMixin, ):
    """A web component for a panel.

    Args:
        *components (list): The list of `WebComponent`.

    Example:
        from bootwrap import Text, Panel

        comp1 = Text("Component 1")
        comp2 = Text("Component 2")
        comp3 = Text("Component 3")

        Panel(comp1, comp2, comp3)

    Demo:
        from bootwrap import Text, Panel

        comp1 = Text("Component 1").add_classes("border").ml(1)
        comp2 = Text("Component 2").add_classes("border").ml(1)
        comp3 = Text("Component 3").add_classes("border").ml(1)

        output = Panel(comp1, comp2, comp3)
    """

    def __init__(self, *components):
        super().__init__()
        self.__components = components
        self.__arrangement = None
        self.__background = None

    def __iter__(self):
        return iter(self.__components)

    def as_collapse(self):
        """Makes the panel collapsed.

        Returns:
            obj (self): The instance of this class.
        """
        self.add_classes('collapse')
        return self

    def vertical(self):
        """Makes the panel with the vertical arrangement of encapsulating
        elements

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text, Panel

            comp1 = Text("Component 1")
            comp2 = Text("Component 2")
            comp3 = Text("Component 3")

            Panel(comp1, comp2, comp3).vertical()

        Demo:
            from bootwrap import Text, Panel

            comp1 = Text("Component 1").add_classes("border")
            comp2 = Text("Component 2").add_classes("border")
            comp3 = Text("Component 3").add_classes("border")

            output = Panel(comp1, comp2, comp3).vertical()
        """
        self.__arrangement = 'vertical'
        return self

    def horizontal(self):
        """Makes the panel with the horizontal arrangement of encapsulating
        elements

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text, Panel

            comp1 = Text("Component 1")
            comp2 = Text("Component 2")
            comp3 = Text("Component 3")

            Panel(comp1, comp2, comp3).horizontal()

        Demo:
            from bootwrap import Text, Panel

            comp1 = Text("Component 1").add_classes("border")
            comp2 = Text("Component 2").add_classes("border")
            comp3 = Text("Component 3").add_classes("border")

            output = Panel(comp1, comp2, comp3).horizontal()
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
            else:  # self.__arrangement == 'horizontal'

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
                            {inject(
                                *map(col, filter(None, self.__components))
                            )}
                        </div>
                    </div>
                '''

        return f'''
            <div {attr("id", self.identifier)}
                {attr("class", self.classes)}>
                {inject(*self.__components)}
            </div>
        '''
