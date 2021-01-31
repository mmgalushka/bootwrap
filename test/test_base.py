"""
Test for bootwrap/components/base.py
"""

import pytest, re

from bootwrap import (
    WebComponent,
    ClassMixin,
    AppearanceMixin,
    OutlineMixin,
    AvailabilityMixin
)


@pytest.mark.base
def tests_web_component():
    class TestWebComponent(WebComponent):
        def __str__(self):
            return self.identifier
    wc = TestWebComponent()
    regex = re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(str(wc))
    assert bool(match)


@pytest.mark.base
def tests_appearance_mixin():
    class TestAppearanceMixin(AppearanceMixin):
        def __str__(self):
            if self._category:
                return self._category
            return 'blank'
    assert str(TestAppearanceMixin()) == 'blank'
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