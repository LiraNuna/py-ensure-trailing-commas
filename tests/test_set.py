from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import find_missing_trailing_commas


def test_tuple():
    assert find_missing_trailing_commas(dedent("""
        x = {
            1,
            2
        }
    """)) == [19]

    assert find_missing_trailing_commas(dedent("""
        x = {
            1, 2
        }
    """)) == [15]

    assert find_missing_trailing_commas(dedent("""
        a, b = {
            1,
            2
        }
    """)) == [22]

    assert find_missing_trailing_commas(dedent("""
        function_call({
            1,
            2,
            3
        })
    """)) == [36]


def test_nasted():
    assert find_missing_trailing_commas(dedent("""
        x = {
            {1, 2},
            {3, 4}
        }
    """)) == [29]

    assert find_missing_trailing_commas(dedent("""
        x = {
                1,
                {
                    2,
                    3
                },
            {
                3,
                {
                    4,
                    5
                }
            }
        }
    """)) == [56, 123, 133, 139]


def test_no_add_exists():
    assert find_missing_trailing_commas(dedent("""
        x = {
            1,
            2,
        }
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        x = {
            1, 2,
        }
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        a, b = {
            1,
            2,
        }
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call({
            1,
            2,
            3,
        })
    """)) == []


def test_no_add_ignore():
    assert find_missing_trailing_commas(dedent("""
        x = set()
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        x = {
        }
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        x = {

        }
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        x = {
            # Comment
        }
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        x = {1, 2}
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        x = {1, 2,
             3, 4}
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        (a, b) = {1, 2}
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call({1, 2, 3})
    """)) == []
