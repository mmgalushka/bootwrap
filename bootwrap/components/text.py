"""
A text.
"""

from textwrap import dedent

from .base import (
    WebComponent,
    ClassMixin,
    AppearanceMixin,
    OutlineMixin
)
from .utils import attr, tag


class Text(WebComponent, ClassMixin, AppearanceMixin, OutlineMixin):
    """A web component for a text.

    Args:
        content (str): The textual content.

    Example:
        from bootwrap import Text, Panel

        txt = Text("Text")
        txt_outline = Text("Text with border").as_outline()
        txt_primary = Text("Text of primary color").as_primary()
        txt_primary_outline = Text("Text of primary color with border").as_primary().as_outline()

        output = Panel(
            txt,
            txt_outline,
            txt_primary,
            txt_primary_outline
        ).vertical()
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
            from bootwrap import Text, Panel

            txt_small = Text("Small text").as_small()
            txt_small_outline = Text("Small text with border").as_small().as_outline()
            txt_small_primary = Text("Small text of primary color").as_small().as_primary()
            txt_small_primary_outline = Text("Small text of primary color with border").as_small().as_primary().as_outline()

            output = Panel(
                txt_small,
                txt_small_outline,
                txt_small_primary,
                txt_small_primary_outline
            ).vertical()
        """
        self.__small = True
        return self

    def as_strong(self):
        """Makes the text as strong.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Text, Panel

            txt_strong = Text("Strong text").as_strong()
            txt_strong_outline = Text("Strong text with border").as_strong().as_outline()
            txt_strong_primary = Text("Strong text of primary color").as_strong().as_primary()
            txt_strong_primary_outline = Text("Strong text of primary color with border").as_strong().as_primary().as_outline()

            output = Panel(
                txt_strong,
                txt_strong_outline,
                txt_strong_primary,
                txt_strong_primary_outline
            ).vertical()
        """
        self.__strong = True
        return self

    def as_paragraph(self):
        """Makes the text wrap in a paragraph.

        Returns:
            obj (self): The instance of this class.

        Example:
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
            from bootwrap import Panel, Text

            output = Text("print('Hello world!')").as_code()
        """
        self.__code = True
        return self

    def __str__(self):
        if self._category:
            self.add_classes(f'text-{self._category}')

        if self._border:
            self.add_classes(f'border')
            if self._category:
                self.add_classes(f'border-{self._category}')

        attrs = [
            attr("id", self.identifier),
            attr("class", self.classes)
        ]

        if self.__level:
            return tag(f'h{self.__level}', attrs, dedent(self.__content))
        else:
            if self.__code:
                return tag(
                    'pre',
                    attrs,
                    tag('code', [attr('class', 'python')], dedent(self.__content))
                )
            else:
                if self.__paragraph:
                    return tag('p', attrs, dedent(self.__content))
                elif self.__strong:
                    return tag('strong', attrs, dedent(self.__content))
                elif self.__small:
                    return tag('small', attrs, dedent(self.__content))
                else:
                    return tag('span', attrs, dedent(self.__content))