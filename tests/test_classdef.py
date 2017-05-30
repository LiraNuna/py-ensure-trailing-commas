from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import find_missing_trailing_commas


def test_classdef():
    assert find_missing_trailing_commas(dedent("""
        class Test(
            a,
            b
        ): pass
    """)) == [25]

    assert find_missing_trailing_commas(dedent("""
        class Test(
            a,
            b  # comment
        ): pass
    """)) == [25]

    assert find_missing_trailing_commas(dedent("""
        class Test(
            a,
            metaclass=b
        ): pass
    """)) == [35]

    assert find_missing_trailing_commas(dedent("""
        class Test(
            a,
            not_metaclass=b
        ): pass
    """)) == [39]


def test_no_add_exists():
    assert find_missing_trailing_commas(dedent("""
        class Test(
            a,
            b,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        class Test(
            a,
            b,  # comment
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        class Test(
            a,
            metaclass=b,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        class Test(
            a,
            not_metaclass=b,
        ): pass
    """)) == []


def test_no_add_ignore():
    assert find_missing_trailing_commas(dedent("""
        class Test(object): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        class Test(): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        class Test(
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        class Test(

        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        class Test: pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        class Test(a, b, c): pass
    """)) == []
