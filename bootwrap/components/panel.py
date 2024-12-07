"""
A panel.
"""

from .base import WebComponent, ClassMixin, AppearanceMixin, OutlineMixin
from .utils import attr, inject


class Panel(WebComponent, ClassMixin, AppearanceMixin, OutlineMixin):
    """A web component for a panel.

    Args:
        *components (list): The list of `WebComponent`.

    Example:
        from bootwrap import Text, Panel

        comp1 = Text("Component 1").as_outline().ms(1)
        comp2 = Text("Component 2").as_outline().ms(1)
        comp3 = Text("Component 3").as_outline().ms(1)

        output = Panel(comp1, comp2, comp3)
    """

    def __init__(self, *components):
        super().__init__()
        self.__components = components
        self.__arrangement = None

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

            comp1 = Text("Component 1").as_outline()
            comp2 = Text("Component 2").as_outline()
            comp3 = Text("Component 3").as_outline()

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

            comp1 = Text("Component 1").as_outline()
            comp2 = Text("Component 2").as_outline()
            comp3 = Text("Component 3").as_outline()

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

            comp1 = Text("Component 1").as_light().as_outline().p(2).m(2)
            comp2 = Text("Component 2").as_light().as_outline().p(2).m(2)
            comp3 = Text("Component 3").as_light().as_outline().p(2).m(2)

            pnl_start = Panel(comp1, comp2, comp3).as_dark().justify_content("start").mt(1)
            pnl_end = Panel(comp1, comp2, comp3).as_dark().justify_content("end").mt(1)
            pnl_center = Panel(comp1, comp2, comp3).as_dark().justify_content("center").mt(1)
            pnl_between = Panel(comp1, comp2, comp3).as_dark().justify_content("between").mt(1)
            pnl_around = Panel(comp1, comp2, comp3).as_dark().justify_content("around").mt(1)
            pnl_evenly = Panel(comp1, comp2, comp3).as_dark().justify_content("evenly").mt(1)

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
                "Invalid justify panel content style type, expected "
                f"{type(style)}, but got {type(style)}."
            )
        if style not in [
            "start","end","center","between","around","evenly"
        ]:
            raise ValueError(
                f"Invalid justify panel content style: {style}."
            )

        self.add_classes(f"d-flex justify-content-{style}")
        return self
    
    def align_items(self, style):
        """Align panel items.

        Args:
            style (str): 
                The style for aligning items can be one of "start",
                "end", "center", "baseline", "stretch".

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text, Panel, Image

            image  = Image("logo.png", height="200px")
            comp1 = Text("Component 1").as_light().as_outline().p(2).m(2)
            comp2 = Text("Component 2").as_light().as_outline().p(2).m(2)
            comp3 = Text("Component 3").as_light().as_outline().p(2).m(2)

            pnl_start = Panel(image, comp1, comp2, comp3).as_dark().align_items("start").mt(1)
            pnl_end = Panel(image, comp1, comp2, comp3).as_dark().align_items("end").mt(1)
            pnl_center = Panel(image, comp1, comp2, comp3).as_dark().align_items("center").mt(1)
            pnl_baseline = Panel(image, comp1, comp2, comp3).as_dark().align_items("baseline").mt(1)
            pnl_stretch = Panel(image, comp1, comp2, comp3).as_dark().align_items("stretch").mt(1)

            output = Panel(
                pnl_start,
                pnl_end,
                pnl_center,
                pnl_baseline,
                pnl_stretch,
            ).vertical()
        """
        self.__arrangement = None
        if not isinstance(style, str):
            raise TypeError(
                "Invalid align panel items style type, expected "
                f"{type(style)}, but got {type(style)}."
            )
        if style not in [
            "start", "end", "center", "baseline", "stretch"
        ]:
            raise ValueError(
                f"Invalid align panel items style: {style}."
            )

        self.add_classes(f"d-flex align-items-{style}")
        return self

    def __str__(self):
        if self._border:
            self.add_classes(f'border')
            if self._category:
                self.add_classes(f'border-{self._category}')
        else:
            if self._category:
                self.add_classes(f'bg-{self._category}')

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
