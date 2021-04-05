"""
Test for bootwrap/components/base.py
"""

import pytest
import re

from bootwrap import (
    WebComponent,
    ActionMixin,
    AppearanceMixin,
    OutlineMixin,
    AvailabilityMixin,
    Action
)


@pytest.mark.base
def tests_web_component():
    class TestWebComponent(WebComponent):
        def __str__(self):
            return self.identifier
    wc = TestWebComponent()
    regex = re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I) # NOQA
    match = regex.match(str(wc))
    assert bool(match)


@pytest.mark.base
def tests_action_mixin():
    class TestActionMixin(ActionMixin):
        def __str__(self):
            if self._action:
                action = self._action or 'none'
            else:
                action = 'none'

            if self._target:
                if isinstance(self._target, str):
                    target = self._target
                else:
                    target = self._target.identifier
            else:
                target = 'none'

            return f'{action}:{target}'
    assert str(TestActionMixin()) == 'none:none'

    # test link-action
    target = WebComponent()
    assert str(TestActionMixin().link(target)) == Action.LINK + \
        f':{target.identifier}'
    assert str(TestActionMixin().link('somelink')) == Action.LINK + \
        ':somelink'
    with pytest.raises(TypeError):
        str(TestActionMixin().link(None))

    # test toggle-action
    target = WebComponent()
    assert str(TestActionMixin().toggle(target)) == Action.TOGGLE + \
        f':{target.identifier}'
    with pytest.raises(TypeError):
        str(TestActionMixin().toggle(None))

    # test dismiss-action
    assert str(TestActionMixin().dismiss()) == Action.DISMISS + ':none'

    # test dismiss-action
    assert str(TestActionMixin().submit()) == Action.SUBMIT + ':none'


@pytest.mark.base
def tests_appearance_mixin():
    class TestAppearanceMixin(AppearanceMixin):
        def __str__(self):
            if self._category:
                return self._category
            return 'none'
    assert str(TestAppearanceMixin()) == 'none'
    assert str(TestAppearanceMixin().as_primary()) == 'primary'
    assert str(TestAppearanceMixin().as_secondary()) == 'secondary'
    assert str(TestAppearanceMixin().as_success()) == 'success'
    assert str(TestAppearanceMixin().as_danger()) == 'danger'
    assert str(TestAppearanceMixin().as_warning()) == 'warning'
    assert str(TestAppearanceMixin().as_info()) == 'info'
    assert str(TestAppearanceMixin().as_light()) == 'light'
    assert str(TestAppearanceMixin().as_dark()) == 'dark'


@pytest.mark.base
def tests_outline_mixin():
    class TestOutlineMixin(OutlineMixin):
        def __str__(self):
            return 'with border' if self._border else 'without border'
    assert str(TestOutlineMixin()) == 'without border'
    assert str(TestOutlineMixin().as_outline()) == 'with border'


@pytest.mark.base
def tests_availability_mixin():
    class TestAvailabilityMixin(AvailabilityMixin):
        def __str__(self):
            return 'disabled' if self._disabled else 'enabled'
    assert str(TestAvailabilityMixin()) == 'enabled'
    assert str(TestAvailabilityMixin().as_disabled()) == 'disabled'
