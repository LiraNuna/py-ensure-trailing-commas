from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import find_missing_trailing_commas


def test_functiondef():
    assert find_missing_trailing_commas(dedent("""
        def test(
            a
        ): pass
    """)) == [16]

    assert find_missing_trailing_commas(dedent("""
        def test(
            param=value
        ): pass
    """)) == [26]

    assert find_missing_trailing_commas(dedent("""
        def test(
            *args
        ): pass
    """)) == [20]

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            param=value
        ): pass
    """)) == [33]

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            *,
            param=value
        ): pass
    """)) == [40]

    assert find_missing_trailing_commas(dedent("""
        def test(
            *,
            param=value
        ): pass
    """)) == [33]

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            *args,
            param=value
        ): pass
    """)) == [44]

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            *args,
            param=value,
            **kwargs
        ): pass
    """)) == [58]

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            *args,
            param=value,
            **kwargs  # comment
        ): pass
    """)) == [58]


def test_no_add_exists():
    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
            param=value,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
            *args,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            param=value,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            *,
            param=value,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
            *,
            param=value,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            *args,
            param=value,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            *args,
            param=value,
            **kwargs,
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
            a,
            *args,
            param=value,
            **kwargs,  # comment
        ): pass
    """)) == []


def test_no_add_ignore():
    assert find_missing_trailing_commas(dedent("""
        def test(): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(
        ): pass
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        def test(

        ): pass
    """)) == []
