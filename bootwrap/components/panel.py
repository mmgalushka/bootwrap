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

        comp1 = Text("Component 1").add_classes("border").ms(1)
        comp2 = Text("Component 2").add_classes("border").ms(1)
        comp3 = Text("Component 3").add_classes("border").ms(1)

        output = Panel(comp1, comp2, comp3)
    """

    def __init__(self, *components):
        super().__init__()
        self.__components = components
        self.__arrangement = None

    def __iter__(self):
        return iter(self.__components)

    def background(self, color):
        """Sets the panel background color.

        Args:
            color (str):
                The background color to set can be one of "primary",
                "secondary", "success", "danger", "warning", "info",
                "light", "dark", "body", "white","transparent"

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Panel, Text

            output = Panel(
                Panel(Text("primary").as_light()).background("primary").mb(1),
                Panel(Text("secondary").as_light()).background("secondary").mb(1),
                Panel(Text("success").as_light()).background("success").mb(1),
                Panel(Text("danger").as_light()).background("danger").mb(1),
                Panel(Text("warning")).background("warning").mb(1),
                Panel(Text("info")).background("info").mb(1),
                Panel(Text("light")).background("light").mb(1),
                Panel(Text("dark").as_light()).background("dark").mb(1),
                Panel(Text("body")).background("body").mb(1),
                Panel(Text("white")).background("white").mb(1),
                Panel(Text("transparent")).background("transparent").mb(1),
            )
        """
        if not isinstance(color, str):
            raise TypeError(
                f"Invalid background color type, expected {type(str)}, "
                f"but got {type(color)}."
            )
        if color not in [
            "primary", "secondary", "success", "danger", "warning", 
            "info", "light", "dark", "body", "white", "transparent"
        ]:
            raise ValueError(
                f"Invalid panel background color: '{color}'."
            )
        self.add_classes(f"bg-{color}")
        return self

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

            comp1 = Text("Component 1").add_classes("border")
            comp2 = Text("Component 2").add_classes("border")
            comp3 = Text("Component 3").add_classes("border")

            output = Panel(comp1, comp2, comp3).horizontal()
        """
        self.__arrangement = 'horizontal'
        return self

    def justify_content(self, style):
        """Justifies panel content.

        Args:
            style (str): 
                The style for justifying content can be one of "start",
                "end", "center", "between", "around", "evenly".

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text, Panel

            comp1 = Text("Component 1").as_light().add_classes("border").p(2).m(2)
            comp2 = Text("Component 2").as_light().add_classes("border").p(2).m(2)
            comp3 = Text("Component 3").as_light().add_classes("border").p(2).m(2)

            pnl_start = Panel(comp1, comp2, comp3).background("dark").justify_content("start").mt(1)
            pnl_end = Panel(comp1, comp2, comp3).background("dark").justify_content("end").mt(1)
            pnl_center = Panel(comp1, comp2, comp3).background("dark").justify_content("center").mt(1)
            pnl_between = Panel(comp1, comp2, comp3).background("dark").justify_content("between").mt(1)
            pnl_around = Panel(comp1, comp2, comp3).background("dark").justify_content("around").mt(1)
            pnl_evenly = Panel(comp1, comp2, comp3).background("dark").justify_content("evenly").mt(1)

            output = Panel(
                pnl_start,
                pnl_end,
                pnl_center,
                pnl_between,
                pnl_around,
                pnl_evenly
            ).vertical()
        """
        self.__arrangement = None
        if not isinstance(style, str):
            raise TypeError(
                "Invalid panel justify content style type, expected "
                f"{type(style)}, but got {type(style)}."
            )
        if style not in [
            "start","end","center","between","around","evenly"
        ]:
            raise ValueError(
                f"Invalid panel justify content style: {style}."
            )

        self.add_classes(f"d-flex justify-content-{style}")
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
