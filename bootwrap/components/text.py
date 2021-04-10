"""
A text.
"""

from textwrap import dedent

from .base import (
    WebComponent,
    ClassMixin,
    AppearanceMixin
)
from .utils import attr, tag


class Text(WebComponent, ClassMixin, AppearanceMixin):
    """A web component for a text.

    Args:
        content (str): The textual content.

    Example:
        from bootwrap import Text

        Text("Normal text")

    Demo:
        from bootwrap import Text

        output = Text("Normal text")
    """
    def __init__(self, content):
        super().__init__()
        self.__content = content
        self.__level = 0
        self.__small = False
        self.__strong = False
        self.__paragraph = False
        self.__code = False

    def as_muted(self):
        """Makes the text muted.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text

            Text("Muted text").as_muted()

        Demo:
            from bootwrap import Text

            output = Text("Muted text").as_muted()
        """
        self._category = 'muted'
        return self

    def as_heading(self, level):
        """Makes the text as heading.

        Args:
            level (int): The heading level;

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text

            Text("Header text 1").as_heading(1)
            Text("Header text 2").as_heading(2)
            Text("Header text 3").as_heading(3)
            Text("Header text 4").as_heading(4)
            Text("Header text 5").as_heading(5)
            Text("Header text 6").as_heading(6)

        Demo:
            from bootwrap import Panel, Text

            output = Panel(
                Text("Header text 1").as_heading(1),
                Text("Header text 2").as_heading(2),
                Text("Header text 3").as_heading(3),
                Text("Header text 4").as_heading(4),
                Text("Header text 5").as_heading(5),
                Text("Header text 6").as_heading(6)
            )
        """
        if level < 1 or level > 6:
            raise ValueError(
                'Argument "level" expected to be between [1..6], '
                f'but got {level};'
            )
        self.__level = level
        return self

    def as_small(self):
        """Makes the text as small.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text

            Text("Small text").as_small()

        Demo:
            from bootwrap import Text

            output = Text("Small text").as_small()
        """
        self.__small = True
        return self

    def as_strong(self):
        """Makes the text as strong.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text

            Text("Strong text").as_strong()

        Demo:
            from bootwrap import Text

            output = Text("Strong text").as_strong()
        """
        self.__strong = True
        return self

    def as_paragraph(self):
        """Makes the text wrap in a paragraph.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text

            Text("Paragraph 1").as_paragraph()
            Text("Paragraph 2").as_paragraph()
            Text("Paragraph 3").as_paragraph()
        Demo:
            from bootwrap import Panel, Text

            output = Panel(
                Text("Paragraph 1").as_paragraph(),
                Text("Paragraph 2").as_paragraph(),
                Text("Paragraph 3").as_paragraph()
            )
        """
        self.__paragraph = True
        return self

    def as_code(self):
        """Makes the text wrap as a code snippet.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text

            Text("print('Hello world!')").as_code()
        Demo:
            from bootwrap import Panel, Text

            output = Text("print('Hello world!')").as_code()
        """
        self.__code = True
        return self

    def __str__(self):
        def wrap_as_small(c):
            if self.__small:
                return f'<small>{c}</small>'
            return c

        def wrap_as_strong(c):
            if self.__strong:
                return f'<strong>{c}</strong>'
            return c

        def wrap_as_main(c):
            classes = ''
            if self._category:
                classes = f'text-{self._category}'

            if self.classes:
                classes += f' {self.classes}'

            attrs = [
                attr("id", self.identifier),
                attr("class", classes)
            ]
            if self.__level:
                return tag(f'h{self.__level}', attrs, c)
            else:
                if self.__code:
                    return tag(
                        'pre',
                        attrs,
                        tag('code', attr('class', 'python'), dedent(c))
                    )
                else:
                    if self.__paragraph:
                        return tag('p', attrs, c)
                    return tag('span', attrs, c)
        return wrap_as_main(wrap_as_strong(wrap_as_small(self.__content)))
