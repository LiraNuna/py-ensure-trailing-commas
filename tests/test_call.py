from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import find_missing_trailing_commas


def test_call():
    assert find_missing_trailing_commas(dedent("""
        function_call(
            a,
            b
        )
    """)) == [28]

    assert find_missing_trailing_commas(dedent("""
        function_call(a,
                      b
                      )
    """)) == [33]

    assert find_missing_trailing_commas(dedent("""
        function_call(another_call(
            a,
            b
        ))
    """)) == [41]

    assert find_missing_trailing_commas(dedent("""
        obj.method(
            a,
            b
        )
    """)) == [25]

    assert find_missing_trailing_commas(dedent("""
        function_call(
            one(
            ),
            two(
                three()
            ),
            four(
                five(
                    seven(
                        eight
                    )
                )
            )
        )
    """)) == [56, 128, 142, 152, 158]


def test_decorator_call():
    assert find_missing_trailing_commas(dedent("""
        @decorator(
            a,
            b
        )
        def function(a, b):
            pass
    """)) == [25]


def test_no_add_exists():
    assert find_missing_trailing_commas(dedent("""
        function_call(
            a,
            b,
            c,
            d,
        )
    """)) == []

    assert find_missing_trailing_commas(dedent("""
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
    assert find_missing_trailing_commas(dedent("""
        function_call(a, b,
                      c, d)
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call(a, b, c, d)
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call()
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call(
        )
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call(

        )
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call(
            # A comment
        )
    """)) == []
