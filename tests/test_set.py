from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import get_insertion_indexes


def test_tuple():
    assert get_insertion_indexes(dedent("""
        x = {
            1,
            2
        }
    """)) == [19]

    assert get_insertion_indexes(dedent("""
        x = {
            1,
            2  # comment
        }
    """)) == [19]

    assert get_insertion_indexes(dedent("""
        x = {
            1, 2
        }
    """)) == [15]

    assert get_insertion_indexes(dedent("""
        a, b = {
            1,
            2
        }
    """)) == [22]

    assert get_insertion_indexes(dedent("""
        function_call({
            1,
            2,
            3
        })
    """)) == [36]


def test_nasted():
    assert get_insertion_indexes(dedent("""
        x = {
            {1, 2},
            {3, 4}
        }
    """)) == [29]

    assert get_insertion_indexes(dedent("""
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
    assert get_insertion_indexes(dedent("""
        {
            1,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        {
            1
            ,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {
            1,
            2,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {
            1, 2,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        a, b = {
            1,
            2,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call({
            1,
            2,
            3,
        })
    """)) == []


def test_no_add_ignore():
    assert get_insertion_indexes(dedent("""
        x = set()
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {

        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {
            # Comment
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {1, 2}
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {1, 2,
             3, 4}
    """)) == []

    assert get_insertion_indexes(dedent("""
        (a, b) = {1, 2}
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call({1, 2, 3})
    """)) == []
