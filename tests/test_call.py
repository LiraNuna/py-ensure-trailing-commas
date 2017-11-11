from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import get_insertion_indexes


def test_call():
    assert get_insertion_indexes(dedent("""
        function_call(
            a,
            b
        )
    """)) == [28]

    assert get_insertion_indexes(dedent("""
        function_call(
            a,
            b  # comment
        )
    """)) == [28]

    assert get_insertion_indexes(dedent("""
        function_call(
            a,
            b,
            c=d
        )
    """)) == [37]

    assert get_insertion_indexes(dedent("""
        function_call(
            *args,
            **kwargs
        )
    """)) == [39]

    assert get_insertion_indexes(dedent("""
        function_call(a,
                      b
                      )
    """)) == [33]

    assert get_insertion_indexes(dedent("""
        function_call(a,
                      b,
                      c=d
                      )
    """)) == [52]

    assert get_insertion_indexes(dedent("""
        function_call(another_call(
            a,
            b
        ))
    """)) == [41]

    assert get_insertion_indexes(dedent("""
        function_call(
            another_call(
                a,
                b=c
            ),
            dd=ff
        )
    """)) == [56, 73]

    assert get_insertion_indexes(dedent("""
        obj.method(
            a,
            b
        )
    """)) == [25]

    assert get_insertion_indexes(dedent("""
        function_call(
            one(
            ),
            two(
                three()
            ),
            four(
                five(
                    seven(
                        eight=8
                    )
                )
            )
        )
    """)) == [56, 130, 144, 154, 160]


def test_decorator_call():
    assert get_insertion_indexes(dedent("""
        @decorator(
            a,
            b
        )
        def function(a, b):
            pass
    """)) == [25]


def test_no_add_exists():
    assert get_insertion_indexes(dedent("""
        function_call(
            a,
            b,
            c,
            d,
        )
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call(
            a
            ,
        )
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call(
            a,
            b,
            c,
            d,  # comment
        )
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call(
            one(
            ),
            two(
                three(),
            ),
            four(
                five(
                    seven(
                        eight,
                    ),
                ),
            ),
        )
    """)) == []


def test_no_add_ignore():
    assert get_insertion_indexes(dedent("""
        function_call(a, b,
                      c, d)
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call(a, b, c, d)
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call()
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call(
        )
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call(

        )
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call(
            # A comment
        )
    """)) == []
