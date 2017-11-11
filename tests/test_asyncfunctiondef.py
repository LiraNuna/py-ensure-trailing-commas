from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import get_insertion_indexes


def test_functiondef():
    assert get_insertion_indexes(dedent("""
        async def test(
            a
        ): pass
    """)) == [22]

    assert get_insertion_indexes(dedent("""
        async def test(
            param=value
        ): pass
    """)) == [32]

    assert get_insertion_indexes(dedent("""
        async def test(
            *args
        ): pass
    """)) == [26]

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            param=value
        ): pass
    """)) == [39]

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            *,
            param=value
        ): pass
    """)) == [46]

    assert get_insertion_indexes(dedent("""
        async def test(
            *,
            param=value
        ): pass
    """)) == [39]

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            *args,
            param=value
        ): pass
    """)) == [50]

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            *args,
            param=value,
            **kwargs
        ): pass
    """)) == [64]

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            *args,
            param=value,
            **kwargs  # comment
        ): pass
    """)) == [64]

    assert get_insertion_indexes(dedent("""
        async def test(
            a=((),(),())
        ): pass
    """)) == [33]

    assert get_insertion_indexes(dedent("""
        async def test(
            a=b() + c(1) + d()
        ): pass
    """)) == [39]

    assert get_insertion_indexes(dedent("""
        async def test(
            a=b[c:d]
        ): pass
    """)) == [29]


def test_no_add_exists():
    assert get_insertion_indexes(dedent("""
        async def test(
            a,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
            *args,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            *,
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
            *,
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            *args,
            param=value,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            *args,
            param=value,
            **kwargs,
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
            a,
            *args,
            param=value,
            **kwargs,  # comment
        ): pass
    """)) == []


def test_no_add_ignore():
    assert get_insertion_indexes(dedent("""
        async def test(): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(
        ): pass
    """)) == []

    assert get_insertion_indexes(dedent("""
        async def test(

        ): pass
    """)) == []
