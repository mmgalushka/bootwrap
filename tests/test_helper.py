"""
Test for test/helper.py
"""
import pytest

from .helper import Tag, Attr


@pytest.mark.helper
def test_attr():
    a = Attr('a', '0')
    b = Attr('a', '0')
    assert a == b

    a = Attr('a', '0')
    b = Attr('a', '...')
    assert a == b

    a = Attr('a', '0')
    b = Attr('b', '0')
    with pytest.raises(AssertionError):
        assert a == b

    a = Attr('a', '0')
    b = Attr('a', '1')
    with pytest.raises(AssertionError):
        assert a == b


@pytest.mark.helper
def test_tag():
    t0 = Tag('t0')
    t1 = Tag('t0')
    assert t0 == t1

    t0 = Tag('t0')
    t1 = Tag('t1')
    with pytest.raises(AssertionError):
        assert t0 == t1

    t0 = Tag('t')
    t0.add_attr(Attr('a', '0'))
    t0.add_attr(Attr('b', '1'))
    t0.add_attr(Attr('c', '2'))
    t1 = Tag('t')
    t1.add_attr(Attr('a', '0'))
    t1.add_attr(Attr('b', '1'))
    t1.add_attr(Attr('c', '...'))
    assert t0 == t1

    t0 = Tag('t')
    t0.add_attr(Attr('a', '0'))
    t0.add_attr(Attr('b', '1'))
    t1 = Tag('t')
    t1.add_attr(Attr('a', '1'))
    t1.add_attr(Attr('b', '1'))
    with pytest.raises(AssertionError):
        assert t0 == t1

    t0 = Tag('t')
    t0.add_attr(Attr('a', '0'))
    t0.add_attr(Attr('b', '1'))
    t1 = Tag('t')
    t1.add_attr(Attr('a', '0'))
    with pytest.raises(AssertionError):
        assert t0 == t1

    t0 = Tag('t')
    t0.set_data('data_0')
    t1 = Tag('t')
    t1.set_data('data_0')
    assert t0 == t1

    t0 = Tag('t')
    t0.set_data('data_0')
    t1 = Tag('t')
    t1.set_data('data_1')
    with pytest.raises(AssertionError):
        assert t0 == t1

    t0 = Tag('t')
    t0.add_tag(Tag('tt'))
    t1 = Tag('t')
    t1.add_tag(Tag('tt'))
    assert t0 == t1

    t0 = Tag('t')
    t0.add_tag(Tag('tt'))
    t1 = Tag('t')
    with pytest.raises(AssertionError):
        assert t0 == t1
