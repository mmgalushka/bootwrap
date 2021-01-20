"""
Helper functions for tests automation.
"""

from html.parser import HTMLParser

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

    def __eq__(self, other):
        assert self.__name == other.__name, f'{self.__name} != {other.__name}'
        assert self.__value == other.__value, f'{self.__value} != {other.__value}'
        return True

class Tag:
    """A test HTML tag.
    
    Args:
        name (str): The tag name.
    """
    def __init__(self, name):
        self.__name = name
        self.__attrs = list()
        self.__tags = list()
        self.__data = None

    def __eq__(self, other):
        assert self.__name == other.__name, f'{self.__name} != {other.__name}'
        assert self.__attrs == other.__attrs, f'{self.__attrs} != {other.__attrs}'
        assert self.__tags == other.__tags, f'{self.__tags} != {other.__tags}'
        assert self.__data == other.__data, f'{self.__data} != {other.__data}'
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
        self.__document = None
        self.__stack = []

    @staticmethod
    def parse(fragment):
        parser = HelperHTMLParser()
        parser.feed(fragment.strip())
        return parser.__document

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
            assert self.__document == None,\
                'Corrupted HTML fragment, it should have only one root element;'
            self.__document = e
        else:
            self.__stack[-1].add_tag(e)

    def handle_data(self, data):
        assert len(self.__stack) > 0,\
            'Corrupted HTML fragment, missing element to set data;'
        self.__stack[-1].set_data(data)