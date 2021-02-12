"""
Web-components utilities.
"""

__all__ = [ 'attr', 'inject' ]


def attr(name, value):
    """Makes a HTML tag attribute.

    Note, if attribute value is `None` this function returns an empty string.

    >>> attr('class', 'row')
    >>> class="row"

    Args:
        name (str): The attribute name.
        value (obj): The attribute value.

    Returns:
        result (str): The constructed attribute.
    """ 
    if value is not None:
        if isinstance(value, bool):
            return name if value else ''
        else:
            if isinstance(value, str):
                if len(value.strip()) > 0:
                    return '%s="%s"' % (name, value.strip())
            elif isinstance(value, int):
                return '%s=%d' % (name, value)
            else:
                raise TypeError(
                    'Unsupported type of attribute value. '
                    'Attribute type can be either <str> or <int>, '
                    f'but got "{type(value)}".'
                )

    return ''


def inject(*components):
    """Injects web-components.

    >>> inject(
    >>>    '<snap>a</snap>',
    >>>    '<snap>b</snap>'
    >>> )
    >>> <snap>a</snap><snap>b</snap>

    Args:
        components (WebComponents): The web-components to inject.

    Returns:
        str: The string with injected web-components.
    """
    return ''. join(map(str, filter(None, components)))