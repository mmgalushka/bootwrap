"""
Base web-component and mixins.
"""

import uuid

__all__ = [
    'WebComponent',
    'CompositeMixin',
    'ClassMixin',
    'AppearanceMixin',
    'BorderMixin'
]


class WebComponent:
    """A web-component base class."""
    def __init__(self):
        super(WebComponent, self).__init__()
        self.__identifier = str(uuid.uuid4())

    @property
    def identifier(self):
        """A unique web-component identifier."""
        return self.__identifier


class CompositeMixin:
    """Mixin for a web-component that can encapsulate other components."""
    def __init__(self):
        super(CompositeMixin, self).__init__()
        self._components = []

    def append(self, *components):
        """Adds other components.

        Args:
            components (obj): The component(s) to append. The appending 
                components must be either <class "WebComponent"> or
                <class "tuple"> depending on the context provided by
                the inherited class.

        Returns:
            self
        """
        for i, c in enumerate(list(components)):
            if isinstance(c, WebComponent) or isinstance(c, tuple):
                self._components.append(c)
            else:
                raise TypeError(
                    f'''Parameter "components[{i}]" expected to be either
                    <class "WebComponent"> or <class "tuple">, but got {type(c)};
                    '''
                )
        return self


class ClassMixin(object):
    """Mixin for a web-component which class can be amended."""
    def __init__(self):
        super(ClassMixin, self).__init__()
        self.__classes = set()

    def add_classes(self, classes):
        """Adds other classes.

        Args:
            classes (str): The classes to add.

        Returns:
            self
        """
        for c in classes.split(' '):
            if len(c)>0:
                self.__classes.add(c)
        return self

    @property
    def classes(self):
        """The web-component classes."""
        if len(self.__classes) > 0:
            return ' '.join(self.__classes)
        return None


class AppearanceMixin:
    """Mixin for a web-component which appearance can be associated
    with predefined categories."""
    def __init__(self):
        super(AppearanceMixin, self).__init__()
        self._category = None

    def as_primary(self):
        """Makes the 'primary' look to a web-components.

        Returns:
            self
        """
        self._category = 'primary'
        return self

    def as_secondary(self):
        """Makes the 'secondary' look to a web-components.

        Returns:
            self
        """
        self._category = 'secondary'
        return self


    def as_success(self):
        """Makes the 'success' look to a web-components.

        Returns:
            self
        """
        self._category = 'success'
        return self

    def as_danger(self):
        """Makes the 'danger' look to a web-components.

        Returns:
            self
        """
        self._category = 'danger'
        return self

    def as_warning(self):
        """Makes the 'warning' look to a web-components.

        Returns:
            self
        """
        self._category = 'warning'
        return self

    def as_info(self):
        """Makes the 'info' look to a web-components.

        Returns:
            self
        """
        self._category = 'info'
        return self

    def as_light(self):
        """Makes the 'light' look to a web-components.

        Returns:
            self
        """
        self._category = 'light'
        return self

    def as_dark(self):
        """Makes the 'dark' look to a web-components.

        Returns:
            self
        """
        self._category = 'dark'
        return self


class BorderMixin:
    """Mixin for a web component that can be surrounded by a border."""
    def __init__(self):
        super(BorderMixin, self).__init__()
        self._border = False

    def with_border(self):
        """Makes the web-component surrounded by a border.

        Returns:
            self
        """
        self._border = True
        return self


class AvailabilityMixin:
    """Mixin for a web-component which can be enabled or disabled."""
    def __init__(self):
        super(AvailabilityMixin, self).__init__()
        self._disabled = False

    def as_disabled(self):
        """Disables a web-component.

        Returns:
            self
        """
        self._disabled = True
        return self