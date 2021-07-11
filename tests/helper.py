"""
Helper functions for tests automation.
"""

from html.parser import HTMLParser


class AttributeNamesNotMatchError(AssertionError):
    """This error is raised when attribute names are not matched."""
    pass


class AttributeValuesNotMatchError(AssertionError):
    """This error is raised when attribute value are not matched."""
    pass


class TagNamesNotMatchError(AssertionError):
    """This error is raised when tag names are not matched."""
    pass


class TagAttributesNotMatchError(AssertionError):
    """This error is raised when tag attributes are not matched."""
    pass


class TagChildrenNotMatchError(AssertionError):
    """This error is raised when tag children are not matched."""
    pass


class TagDataNotMatchError(AssertionError):
    """This error is raised when tag data are not matched."""
    pass


class Attr:
    """A test HTML attribute.

    Args:
        name (str): The attribute name.
        value (str): The attribute value.
    """

    def __init__(self, name, value):
        self.__name = name
        self.__value = None
        if value is not None:
            self.__value = value.strip()

    def __str__(self):
        return f'{self.__name}="{self.__value}"'

    def __eq__(self, other):
        # Checks that attributes names are the same.
        if self.__name != other.__name:
            raise AttributeNamesNotMatchError(
                f'{self.__name} != {other.__name}')

        # Checks that attributes values are the same.
        if self.__value and other.__value:
            def to_set(s):
                ns = set()
                for e in s.split(' '):
                    if len(e.strip()) > 0:
                        ns.add(e.strip())
                return ns

            if self.__value != '...' and other.__value != '...':
                self_value_set = to_set(self.__value)
                other_value_set = to_set(other.__value)
                if self_value_set != other_value_set:
                    raise AttributeValuesNotMatchError(
                        f'{self_value_set} != {other_value_set}')
        else:
            if self.__value != other.__value:
                raise AttributeValuesNotMatchError(
                    f'{self.__value} != {other.__value}')

        # Attributes are the same.
        return True

    @property
    def name(self):
        """The tag name."""
        return self.__name


class Tag:
    """A test HTML tag.

    Args:
        name (str): The tag name.
    """

    def __init__(self, name):
        self.__name = name
        self.__attrs = list()
        self.__tags = list()
        self.__data = ''

    def __str__(self):
        open_tag = f"<{self.__name} {' '.join(map(str, self.__attrs))}>"
        inner = "..."
        close_tag = f"</{self.__name}>"
        return ''.join([open_tag, inner, close_tag])

    def __eq__(self, other):
        # Checks that tags names are the same.
        if self.__name != other.__name:
            raise TagNamesNotMatchError(f'{self.__name} != {other.__name}')

        # Checks that tags attributes are matched.
        self_attrs = sorted(self.__attrs, key=lambda a: a.name)
        other_attrs = sorted(other.__attrs, key=lambda a: a.name)

        if self_attrs != other_attrs:
            if isinstance(self_attrs, list):
                self_attrs_names = " ".join(map(str, self_attrs))
            else:
                self_attrs_names = str(self_attrs)

            if isinstance(other_attrs, list):
                other_attrs_names = " ".join(map(str, other_attrs))
            else:
                other_attrs_names = str(other_attrs)

            raise TagAttributesNotMatchError(
                f'{self_attrs_names} != {other_attrs_names}')

        # Checks that tags data are matched.
        self_data = self.__data.replace(" ", "")
        other_data = other.__data.replace(" ", "")
        if self_data != other_data:
            raise TagDataNotMatchError(f'{self_data} != {other_data}')

        # Checks that children tags are matched.
        if len(self.__tags) != len(other.__tags):
            raise TagChildrenNotMatchError(
                f'{len(self.__tags)} != {len(other.__tags)}')
        for child_self_tag, child_other_tag in zip(self.__tags, other.__tags):
            assert child_self_tag == child_other_tag

        # Tags are the same.
        return True

    def add_attr(self, attr):
        """Adds an attribute.

        Args:
            attr (Attr): The attribute to add.
        """
        self.__attrs.append(attr)

    def add_tag(self, tag):
        """Adds a tag.

        Args:
            tag (Tag): The tag to add.
        """
        self.__tags.append(tag)

    def set_data(self, data):
        """Sets a tag data.

        Args:
            data (str): The tag data to set.
        """
        self.__data = data.strip()

    @property
    def name(self):
        """The tag name."""
        return self.__name


class HelperHTMLParser(HTMLParser):
    """The test HTML parser"""

    def __init__(self):
        super().__init__()
        self.__document = []
        self.__stack = []

    @staticmethod
    def parse(fragment):
        parser = HelperHTMLParser()
        parser.feed(fragment.strip())
        if len(parser.__document) > 1:
            return parser.__document
        else:
            return parser.__document[0]

    def handle_starttag(self, tag, attrs):
        e = Tag(tag)
        for attr in attrs:
            e.add_attr(Attr(attr[0], attr[1]))
        self.__stack.append(e)

    def handle_endtag(self, tag):
        e = self.__stack.pop()
        assert e.name == tag,\
            f'Corrupted HTML fragment, expected <{e.name}> but got <{tag}>;'
        if len(self.__stack) == 0:
            self.__document.append(e)
        else:
            self.__stack[-1].add_tag(e)

    def handle_data(self, data):
        if len(self.__stack) > 0:
            self.__stack[-1].set_data(data)
