from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import get_insertion_indexes


def test_functiondef():
    assert get_insertion_indexes(dedent("""
        def test(
            a
        ): pass
    """)) == [16]

    assert get_insertion_indexes(dedent("""
        def test(
            param=value
        ): pass
    """)) == [26]

    assert get_insertion_indexes(dedent("""
        def test(
            *args
        ): pass
    """)) == [20]

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            param=value
        ): pass
    """)) == [33]

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            *,
            param=value
        ): pass
    """)) == [40]

    assert get_insertion_indexes(dedent("""
        def test(
            *,
            param=value
        ): pass
    """)) == [33]

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            *args,
            param=value
        ): pass
    """)) == [44]

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            *args,
            param=value,
            **kwargs
        ): pass
    """)) == [58]

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            *args,
            param=value,
            **kwargs  # comment
        ): pass
    """)) == [58]

    assert get_insertion_indexes(dedent("""
        def test(
            a=((),(),())
        ): pass
    """)) == [27]

    assert get_insertion_indexes(dedent("""
        def test(
            a=b() + c(1) + d()
        ): pass
    """)) == [33]

    assert get_insertion_indexes(dedent("""
        def test(
            a=b[c:d]
        ): pass
    """)) == [23]


def test_no_add_exists():
    assert get_insertion_indexes(dedent("""
        def test(
            a,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
            *args,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            *,
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
            *,
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            *args,
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            *args,
            param=value,
            **kwargs,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
            a,
            *args,
            param=value,
            **kwargs,  # comment
        ): pass
    """)) == []


def test_no_add_ignore():
    assert get_insertion_indexes(dedent("""
        def test(): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        def test(

        ): pass
    """)) == []
