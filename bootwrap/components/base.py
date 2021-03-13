"""
Base web-component and mixins.
"""

import uuid
import enum

__all__ = [
    'WebComponent',
    'ClassMixin',
    'ActionMixin',
    'AppearanceMixin',
    'OutlineMixin',
    'AvailabilityMixin',
    'Breakpoint',
    'Action'
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


class ClassMixin:
    """Mixin for a web-component which class can be amended."""
    def __init__(self):
        super(ClassMixin, self).__init__()
        self.__classes = []

    def add_classes(self, classes):
        """Adds other classes.

        Args:
            classes (str): The classes to add.

        Returns:
            self
        """
        for c in classes.split(' '):
            if len(c)>0:
                if c not in self.__classes:
                    self.__classes.append(c)
        return self

    @property
    def classes(self):
        """The web-component classes."""
        if len(self.__classes) > 0:
            return ' '.join(self.__classes)
        return None


class ActionMixin:
    """Mixin for a web-component which able to perform an action."""
    def __init__(self):
        super(ActionMixin, self).__init__()
        self._action = None
        self._target = None

    def link(self, target):
        """Links to the web-resource.

        Args:
            target (str|WebComponent): The URL to the linking web-page or 
                linking web-component. In the case of the web-component,
                the hyperlink will have the following format `#identifier`,
                where the identifier is a unique ID of the specified target.
        
        Returns:
            self
        """
        self._action = Action.LINK
        if isinstance(target, str) or isinstance(target, WebComponent):
            self._target = target
            return self
        raise TypeError(
            'The target must be not empty string <class "str"> or <class '
            f'"WebComponent">, instead got: {type(target)};'
        )


    def toggle(self, target):
        """Toggles an other web-component.

        Args:
            target (WebComponent): The web-component to toggle.
        
        Returns:
            self
        """
        self._action = Action.TOGGLE
        if isinstance(target, WebComponent):
            self._target = target
            return self
        raise TypeError(
            'The target must be not empty string <class "WebComponent">, '
            f'instead got: {type(target)};'
        )

    def collapse(self, target):
        """Collapses an other web-component.

        Args:
            target (WebComponent): The web-component to collapse.

        Returns:
            self
        """
        self._action = Action.COLLAPSE
        if isinstance(target, WebComponent):
            self._target = target
            return self
        raise TypeError(
            'The target must be not empty string <class "WebComponent">, '
            f'instead got: {type(target)};'
        )

    def dismiss(self):
        """Performes a dismiss action.

        Returns:
            self
        """
        self._action = Action.DISMISS
        return self

    def submit(self):
        """Performes a submit action.

        Returns:
            self
        """
        self._action = Action.SUBMIT
        return self


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


class OutlineMixin:
    """Mixin for a web component that can be surrounded by a border."""
    def __init__(self):
        super(OutlineMixin, self).__init__()
        self._border = False

    def as_outline(self):
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


class Breakpoint(str, enum.Enum):
    """Breakpoints are defined by Bootstrap and mostly based on minimum
    viewport widths and allow us to scale up elements as the viewport
    changes.
    
    https://getbootstrap.com/docs/4.0/layout/overview/#responsive-breakpoints
    """
    XS = 'xs'
    SM = 'sm'
    MD = 'md'
    LG = 'lg'
    XL = 'xl'


class Action(str, enum.Enum):
    """The most common actions."""
    LINK = 'link'
    TOGGLE = 'toggle'
    COLLAPSE = 'collapse'
    DISMISS = 'dismiss'
    SUBMIT = 'submit'