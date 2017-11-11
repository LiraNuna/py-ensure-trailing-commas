from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import get_insertion_indexes


def test_dict():
    assert get_insertion_indexes(dedent("""
        x = {
            'a': 1,
            'b': 2
        }
    """)) == [29]

    assert get_insertion_indexes(dedent("""
        x = {
            'a': 1,
            'b': 2  # comment
        }
    """)) == [29]

    assert get_insertion_indexes(dedent("""
        x = {
            'a': 1, 'b': 2
        }
    """)) == [25]

    assert get_insertion_indexes(dedent("""
        function_call({
            'a': 1,
            'b': 2
        })
    """)) == [39]


def test_nasted():
    assert get_insertion_indexes(dedent("""
        x = {
            'a': {
                '1': 1,
                '2': 2
            },
            'b': {
                '3': 3
            },
            'c': {
                'd': {
                    'e': {
                        'f': 'g'
                    }
                }
            }
        }
    """)) == [48, 81, 158, 172, 182, 188]


def test_no_add_exists():
    assert get_insertion_indexes(dedent("""
        {
            1: 1,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        {
            1: 1
            ,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {
            'a': 1,
            'b': 2,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {
            'a': 1, 'b': 2,
        }
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call({
            'a': 1,
            'b': 2,
        })
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call({
            'a': 1,
            'b': 2,  # comment
        })
    """)) == []


def test_no_add_ignore():
    assert get_insertion_indexes(dedent("""
        x = {}
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
        x = {'1': 2, '3': 4}
    """)) == []

    assert get_insertion_indexes(dedent("""
        x = {'1': 2,
             '3': 4}
    """)) == []

    assert get_insertion_indexes(dedent("""
        function_call({'1': 2, '3': 4})
    """)) == []
