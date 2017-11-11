from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import get_insertion_indexes


def test_classdef():
    assert get_insertion_indexes(dedent("""
        class Test(
            a,
            b
        ): pass
    """)) == [25]

    assert get_insertion_indexes(dedent("""
        class Test(
            a,
            b  # comment
        ): pass
    """)) == [25]

    assert get_insertion_indexes(dedent("""
        class Test(
            a,
            metaclass=b
        ): pass
    """)) == [35]

    assert get_insertion_indexes(dedent("""
        class Test(
            a,
            not_metaclass=b
        ): pass
    """)) == [39]


def test_no_add_exists():
    assert get_insertion_indexes(dedent("""
        class Test(
            a,
            b,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test(
            a
            ,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test(
            a,
            b,  # comment
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test(
            a,
            metaclass=b,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test(
            a,
            not_metaclass=b,
        ): pass
    """)) == []


def test_no_add_ignore():
    assert get_insertion_indexes(dedent("""
        class Test(object): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test(): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test(
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test(

        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test: pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        class Test(a, b, c): pass
    """)) == []
