import sys

from ensure_trailing_commas.trailing_comma_finder import find_missing_trailing_commas


def main():
    script_name, *file_names = sys.argv
    for filename in file_names:
        with open(filename, 'r+', encoding='utf-8') as file:
            file_contents = file.read()

            trailing_comma_indexes = find_missing_trailing_commas(file_contents)
            if not trailing_comma_indexes:
                continue

            for index in reversed(trailing_comma_indexes):
                file_contents = file_contents[:index] + ',' + file_contents[index:]

            file.seek(0)
            file.write(file_contents)
            file.truncate()


if __name__ == '__main__':
    main()
