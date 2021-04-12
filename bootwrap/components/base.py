"""
Base web component and mixins.
"""

import uuid
import enum


class WebComponent:
    """A web component base class.

    This class must be inherited by all web components. 

    In many operations where one web component encapsulates another one has
    implemented a type check. If the received element is not `WebComponent`
    will be generated a `TypeError`. To ensure correct handling of your
    custom component, do not forget to inherit the `WebComponent` class. 

    Example:
        from bootwrap import WebComponent

        class CustomHeader(WebComponent):
            def __init__(self, title):
                self.__title = title

            sef __str__(self):
                return f'''
                    &lt;h1 id="{self.identifier}"&gt
                        {self.__title}
                    &lt;/h1&gt
                '''
    """
    def __init__(self):
        super(WebComponent, self).__init__()
        self.__identifier = str(uuid.uuid4())

    @property
    def identifier(self):
        """A unique web component identifier.

        Every `WebComponent` has a unique identifier (ex. cfe040e6-df5f-4a3a-
        b96e-b0cefc31bbd9). This identifier is used for referencing between
        components inside a page. This property returns this identifier as
        `str`.

        When you create a custom  `WebComponent` it is advisable to set its
        tag attribute `id` equals to `identifier`.

        Example:
            header = CustomHeader('Hello World")
            print(header.classes)

            # Result: cfe040e6-df5f-4a3a-b96e-b0cefc31bbd9
        """
        return self.__identifier


class ClassMixin:
    """Mixin for a web component which class can be amended.

    The vast majority of web components in Bootwrap inherit this class.
    It allows a user to adjust web components look and feel. 
    """
    def __init__(self):
        super(ClassMixin, self).__init__()
        self.__classes = []

    def add_classes(self, classes):
        """Adds other classes.

        Note, the order of specified classes will be preserved during the 
        component rendering. 

        Args:
            classes (str): The classes to add. The specified classes must be
                separated by white space.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").add_classes("ml-1 mr-1")
        """
        for c in classes.split(' '):
            if len(c) > 0:
                if c not in self.__classes:
                    self.__classes.append(c)
        return self

    @property
    def classes(self):
        """The web component classes.
        
        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").add_classes("ml-1 mr-1")
            print(button.classes)

            # Result: ml-1 mr-1
        """
        if len(self.__classes) > 0:
            return ' '.join(self.__classes)
        return None

    def m(self, size):
        """Sets margin for all four sides to the specified size.

        Args:
            size (int): Size of the margin to set.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").m(3)
        """
        return self.add_classes(f"m-{size}")

    def mt(self, size):
        """Sets margin for the top side to the specified size.

        Args:
            size (int): Size of the margin to set.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").mt(3)
        """
        return self.add_classes(f"mt-{size}")

    def mb(self, size):
        """Sets margin for the bottom side the specified size.

        Args:
            size (int): Size of the margin to set.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").mb(3)
        """
        return self.add_classes(f"mb-{size}")

    def ml(self, size):
        """Sets margin for the left side to the specified size.

        Args:
            size (int): Size of the margin to set.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").ml(3)
        """
        return self.add_classes(f"ml-{size}")

    def mr(self, size):
        """Sets margin for the right side to the specified size.

        Args:
            size (int): Size of the margin to set.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").mr(3)
        """
        return self.add_classes(f"mr-{size}")

    def mx(self, size):
        """Sets margin for left and right sides to the specified size.

        Args:
            size (int): Size of the margin to set.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").mx(3)
        """
        return self.add_classes(f"mx-{size}")

    def my(self, size):
        """Sets margin for top and bottom sides to the specified size.

        Args:
            size (int): Size of the margin to set.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ClassMixin.
            button = Button("Hello").my(3)
        """
        return self.add_classes(f"my-{size}")

class ActionMixin:
    """Mixin for a web component which able to perform an action."""
    def __init__(self):
        super(ActionMixin, self).__init__()
        self._action = None
        self._target = None
        self._menu = None

    def link(self, target):
        """Links to the web-resource.

        Args:
            target (str|WebComponent): The URL to the linking web-page or
                linking `WebComponent`. 

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ActionMixin.
            button = Button("Search").link("https://www.google.com")
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
        """Toggles an other web component.

        Args:
            target (WebComponent): The web component to toggle.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button, Dialog

            # Note, that Button inherits ActionMixin.
            dialog = Dialog(...)
            button = Button("Open").toggle(dialog)
        """
        self._action = Action.TOGGLE
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
            obj (self): The instance of this class.

        Example:
            from bootwrap import Dialog, Button

            # Note, that Button inherits ActionMixin.
            dialog = Dialog(
                ...,
                Button("Bye").dismiss()
            )
        """
        self._action = Action.DISMISS
        return self

    def submit(self):
        """Performes a submit action.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Form, Button

            # Note, that Button inherits ActionMixin.
            form = Form(
                ...,
                Button("Send").submit()
            )
        """
        self._action = Action.SUBMIT
        return self

    def add_menu(self, *menu):
        """Adds dropdown menu.

        Args:
            *menu (list): The list of dropdown menu actions. These actions
                must be represented by `WebComponent`s instantiating
                `ActionMixin` class.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits ActionMixin.
            button = Button('Portfolio').add_menu(
                Button("Buy"),
                Button("Sell"),
                Button("Transfer")
            )
        """
        self._menu = menu
        return self


class AppearanceMixin:
    """Mixin for a web component which appearance can be associated
    with predefined categories."""
    def __init__(self):
        super(AppearanceMixin, self).__init__()
        self._category = None

    def as_primary(self):
        """Makes the 'primary' look to a web components.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Primary").as_primary()
        """
        self._category = 'primary'
        return self

    def as_secondary(self):
        """Makes the 'secondary' look to a web components.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Secondary").as_secondary()
        """
        self._category = 'secondary'
        return self

    def as_success(self):
        """Makes the 'success' look to a web components.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Success").as_success()
        """
        self._category = 'success'
        return self

    def as_danger(self):
        """Makes the 'danger' look to a web components.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Danger").as_danger()
        """
        self._category = 'danger'
        return self

    def as_warning(self):
        """Makes the 'warning' look to a web components.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Warning").as_warning()
        """
        self._category = 'warning'
        return self

    def as_info(self):
        """Makes the 'info' look to a web components.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Info").as_info()
        """
        self._category = 'info'
        return self

    def as_light(self):
        """Makes the 'light' look to a web components.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Light").as_light()
        """
        self._category = 'light'
        return self

    def as_dark(self):
        """Makes the 'dark' look to a web components.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Dark").as_dark()
        """
        self._category = 'dark'
        return self


class OutlineMixin:
    """Mixin for a web component that can be surrounded by a border.
    
    Usually `OutlineMixin` is used in conjunction with `AppearanceMixin` to
    specify the border appearance.
    """
    def __init__(self):
        super(OutlineMixin, self).__init__()
        self._border = False

    def as_outline(self):
        """Makes the web component surrounded by a border.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Primary").as_primary().as_outline()
        """
        self._border = True
        return self


class AvailabilityMixin:
    """Mixin for a web component which can be enabled or disabled.

    By default, every web component is enabled. The web components inheriting
    this class can be forced to be disabled.
    """
    def __init__(self):
        super(AvailabilityMixin, self).__init__()
        self._disabled = False

    def as_disabled(self):
        """Disables a web component.

        Returns:
            obj (self): The instance of this class.

        Example:
            from bootwrap import Button

            # Note, that Button inherits AppearanceMixin.
            button = ("Primary").as_disabled()
        """
        self._disabled = True
        return self


class Breakpoint(str, enum.Enum):
    """The breakpoint constants.

    Breakpoints are defined by Bootstrap and mostly based on minimum
    viewport widths and allow us to scale up elements as the viewport
    changes.

    See <a href="https://getbootstrap.com/docs/4.0/layout/overview/#responsive-breakpoints">
    Bootstrap documentation</a> for more information.
    """
    XS = 'xs'
    SM = 'sm'
    MD = 'md'
    LG = 'lg'
    XL = 'xl'


class Action(str, enum.Enum):
    """The action constants."""
    LINK = 'link'
    TOGGLE = 'toggle'
    DISMISS = 'dismiss'
    SUBMIT = 'submit'
