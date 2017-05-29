from textwrap import dedent

from ensure_trailing_commas.trailing_comma_finder import find_missing_trailing_commas


def test_dict():
    assert find_missing_trailing_commas(dedent("""
        x = {
            'a': 1,
            'b': 2
        }
    """)) == [29]

    assert find_missing_trailing_commas(dedent("""
        x = {
            'a': 1, 'b': 2
        }
    """)) == [25]

    assert find_missing_trailing_commas(dedent("""
        function_call({
            'a': 1,
            'b': 2
        })
    """)) == [39]


def test_nasted():
    assert find_missing_trailing_commas(dedent("""
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
    assert find_missing_trailing_commas(dedent("""
        x = {
            'a': 1,
            'b': 2,
        }
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        x = {
            'a': 1, 'b': 2,
        }
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call({
            'a': 1,
            'b': 2,
        })
    """)) == []


def test_no_add_ignore():
    assert find_missing_trailing_commas(dedent("""
        x = {}
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
        x = {'1': 2, '3': 4}
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        x = {'1': 2,
             '3': 4}
    """)) == []

    assert find_missing_trailing_commas(dedent("""
        function_call({'1': 2, '3': 4})
    """)) == []
